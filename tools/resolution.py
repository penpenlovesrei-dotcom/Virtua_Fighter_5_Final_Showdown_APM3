#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Observe -- et force -- la resolution de rendu de vfes.exe.

**Fausse piste ecartee.** On avait cru voir une « table de modes d'affichage »
en `.rdata` vers `0x1803FEB80` parce qu'on y lisait 1280x720, 1920x1080,
2560x1440 et 3840x2160 a la suite. C'est un **pool de constantes** : les
references a cette zone sont des `vmulss` et des `vsubss`, pas des lectures de
table. Ces valeurs sont des litteraux d'arithmetique, rien d'autre.

**La vraie chaine**, relevee a l'execution, tient en quatre appels et vit dans
`vfes.exe`, pas dans le moteur :

    CreateWindowExW        320 x 240      la fenetre nait minuscule
    AdjustWindowRectEx    1920 x 1080     on calcule le cadre pour ce client
    SetWindowPos          1920 x 1080     depuis vfes.exe+0x34DDB
    D3D11CreateDeviceAndSwapChain
                          1920 x 1080     depuis vfes.exe+0x35833

Les quatre viennent de **la meme paire de valeurs**, dans la meme fonction.
D'ou la regle : **il faut forcer la fenetre ET la chaine d'echange ensemble.**
Ne forcer que la chaine donne une image ROGNEE -- le moteur garde une vue de
1920x1080 sur une cible de 1280x720, et on ne voit que le coin superieur gauche.

    HRESULT D3D11CreateDeviceAndSwapChain(
        IDXGIAdapter*, D3D_DRIVER_TYPE, HMODULE, UINT,       rcx edx r8 r9d
        const D3D_FEATURE_LEVEL*, UINT, UINT,                [rsp+0x28..0x38]
        const DXGI_SWAP_CHAIN_DESC* pSwapChainDesc,          [rsp+0x40]
        ... )
    DXGI_SWAP_CHAIN_DESC :  Width +0x00   Height +0x04

Usage :
    py -3 tools/resolution.py                       observe seulement
    py -3 tools/resolution.py --liste                les resolutions proposees
    py -3 tools/resolution.py --forcer 1280 720 --fenetre
    py -3 tools/resolution.py --mode 3 --fenetre --secondes 3600
"""
import ctypes
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402
from chercher_selection import balayer, MEM_IMAGE, MEM_PRIVATE   # noqa: E402

# Les globaux qui tiennent encore 1920x1080 quand la chaine d'echange est
# forcee ailleurs -- trouves par balayage tardif, en plein combat. Ce sont eux
# qui dimensionnent la passe 3D : la forcer sur la seule chaine d'echange donne
# une image ZOOMEE, l'ATS etant compose a la bonne taille par-dessus.
GLOBAUX = [
    ('vfes.exe', 0x1E43A8),
    ('vf5fs-pxd-w64-Retail_APM3.dll', 0x6490DC),
    ('vf5fs-pxd-w64-Retail_APM3.dll', 0x649104),
]

EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')

# les fonctions par lesquelles une chaine d'echange peut naitre
CIBLES = [
    ('d3d11.dll', 'D3D11CreateDeviceAndSwapChain'),
    ('USER32.dll', 'CreateWindowExW'),
    # la fenetre nait en 320x240 : quelqu'un la redimensionne ensuite, et
    # c'est probablement de la que la resolution de rendu descend.
    ('USER32.dll', 'SetWindowPos'),
    ('USER32.dll', 'MoveWindow'),
    ('USER32.dll', 'AdjustWindowRectEx'),
]

# Les resolutions proposees par le lanceur. La native de la borne est
# 1920x1080 : c'est le mode 4, et c'est celui qui ne force rien.
MODES = [
    ('1024 x 768',   1024, 768,  '4:3, le mode le plus bas connu du moteur'),
    ('1280 x 720',   1280, 720,  '720p -- teste et valide'),
    ('1600 x 900',   1600, 900,  '16:9'),
    ('1920 x 1080',  1920, 1080, "natif de la borne : aucun forcage"),
    ('2560 x 1440',  2560, 1440, '1440p'),
    ('3440 x 1440',  3440, 1440, 'ultra-large 21:9'),
    ('3840 x 2160',  3840, 2160, '4K'),
]

FORMATS = {0: 'INCONNU', 28: 'R8G8B8A8_UNORM', 87: 'B8G8R8A8_UNORM',
           24: 'R10G10B10A2_UNORM', 10: 'R16G16B16A16_FLOAT',
           29: 'R8G8B8A8_UNORM_SRGB', 91: 'B8G8R8A8_UNORM_SRGB'}

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
k32.GetModuleHandleW.restype = ctypes.c_void_p
k32.LoadLibraryW.restype = ctypes.c_void_p
k32.GetProcAddress.restype = ctypes.c_void_p
k32.GetProcAddress.argtypes = [ctypes.c_void_p, ctypes.c_char_p]


def deplacement(module, fonction):
    h = k32.GetModuleHandleW(module) or k32.LoadLibraryW(module)
    if not h:
        return None
    p = k32.GetProcAddress(ctypes.c_void_p(h), fonction.encode())
    return (p - h) if p else None


def main():
    argv = sys.argv[1:]
    secondes = 100
    forcer = None
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'select_a.txt')
    if '--liste' in argv:
        print('  n  resolution      remarque')
        for i, (nom, l, h, note) in enumerate(MODES, 1):
            print('  %d  %-14s  %s' % (i, nom, note))
        return 0
    if '--mode' in argv:
        n = int(argv[argv.index('--mode') + 1])
        if not 1 <= n <= len(MODES):
            print('mode inconnu : %d (voir --liste)' % n)
            return 1
        _, l, h, _n = MODES[n - 1]
        forcer = (l, h)
    if '--forcer' in argv:
        i = argv.index('--forcer')
        forcer = (int(argv[i + 1]), int(argv[i + 2]))
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]
    captures = []
    if '--captures' in argv:
        for spec in argv[argv.index('--captures') + 1].split(','):
            t, chemin = spec.split(':', 1)
            captures.append((os.path.join(RACINE, 'analysis', chemin),
                             float(t), 'Virtua Fighter'))

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 400000
    journal = os.path.join(RACINE, 'analysis', 'resolution.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'poses': set(), 'vus': 0, 'fenetres': 0,
          'chercher': '--chercher' in argv,
          'fenetre_aussi': '--fenetre' in argv,
          'scan_a': float(argv[argv.index('--scan-a') + 1])
                    if '--scan-a' in argv else 0,
          'globaux': '--globaux' in argv, 'dits': set(),
          'cibles': '--cibles' in argv, 'textures': {},
          'vue': '--vue' in argv, 'vues': {}}

    def sur_bp(d, bp, ctx, tid):
        if bp.nom == 'CreateWindowExW':
            # CreateWindowExW(dwExStyle, lpClassName, lpWindowName, dwStyle,
            #                 X, Y, nWidth, nHeight, ...)
            # X et Y sont a [rsp+0x28] et [rsp+0x30], nWidth [rsp+0x38],
            # nHeight [rsp+0x40]
            pile = d.read(ctx.Rsp + 0x28, 0x20)
            if not pile or len(pile) < 0x20:
                return
            x, y, larg, haut = struct.unpack('<iiii', pile[0:4] + pile[8:12]
                                             + pile[16:20] + pile[24:28])
            titre = d.read(ctx.R8, 120)
            nom = ''
            if titre:
                nom = titre.decode('utf-16-le', 'ignore').split('\x00', 1)[0]
            if larg > 100 and haut > 100:
                et['fenetres'] += 1
                d.dire('  fenetre creee : %d x %d  en (%d, %d)   « %s »'
                       % (larg, haut, x, y, nom[:50]))
            return

        if bp.nom == 'retour_D3D11':
            # le device existe maintenant : sa vtable donne CreateTexture2D
            dev = d.u64(et.get('ppdevice') or 0)
            if dev:
                vt = d.u64(dev)
                if vt:
                    fn = d.u64(vt + 8 * 5)      # ID3D11Device::CreateTexture2D
                    if fn:
                        bp3 = instrument.PointArret('CreateTexture2D', fn,
                                                    max_coups=100000)
                        bp3.silencieux = True
                        d.bps.append(bp3)
                        d.armer_logiciel(bp3)
                        d.dire('  device 0x%X  CreateTexture2D 0x%X' % (dev, fn))
            # et le contexte : sa vtable donne RSSetViewports (indice 44)
            ctxt = d.u64(et.get('ppcontexte') or 0)
            if ctxt and et.get('vue'):
                vt2 = d.u64(ctxt)
                if vt2:
                    fn2 = d.u64(vt2 + 8 * 44)
                    if fn2:
                        bp4 = instrument.PointArret('RSSetViewports', fn2,
                                                    max_coups=200000)
                        bp4.silencieux = True
                        d.bps.append(bp4)
                        d.armer_logiciel(bp4)
                        d.dire('  contexte 0x%X  RSSetViewports 0x%X'
                               % (ctxt, fn2))
            d.desarmer_logiciel(bp)
            return

        if bp.nom == 'RSSetViewports':
            # RSSetViewports(this, NumViewports, pViewports)
            #                rcx   edx           r8
            # D3D11_VIEWPORT : X+0 Y+4 W+8 H+0xC (flottants)
            n = ctx.Rdx & 0xFFFFFFFF
            if not n or not ctx.R8:
                return
            v = d.read(ctx.R8, 0x18)
            if not v or len(v) < 0x10:
                return
            x, y, vw, vh = struct.unpack_from('<4f', v, 0)
            # La vue posee par vfes.exe+0x3DA0F reste a 1920x1080 meme quand
            # toutes les cibles sont en 720p : elle dessine donc 1,5 fois trop
            # grand sur une cible plus petite, et l'on n'en voit que le coin.
            # C'est le zoom. On la force ici, a la source, pour chaque vue
            # restee a l'ancienne definition.
            if forcer and (round(vw), round(vh)) == (1920, 1080):
                d.write(ctx.R8 + 8, struct.pack('<2f', float(forcer[0]),
                                                float(forcer[1])))
                vw, vh = float(forcer[0]), float(forcer[1])
                # ... et surtout la SOURCE, pour pouvoir desarmer ensuite.
                # 0x14003D89A charge la vue depuis [0x1403E8250], ou depuis
                # [*(0x1403E81C0) + 0x70] selon la branche. On corrige les deux
                # une fois pour toutes : s'arreter a chaque RSSetViewports coute
                # un evenement de debogage par passe et par trame, ce qui rend
                # le jeu inutilisable.
                bexe = d.base_de('vfes.exe')
                if bexe:
                    for src in (bexe + 0x3E8250, bexe + 0x3E8250 + 0x10):
                        cur = d.read(src, 16)
                        if cur and len(cur) == 16:
                            xx, yy, ww, hh = struct.unpack('<4f', cur)
                            if (round(ww), round(hh)) == (1920, 1080):
                                d.write(src + 8, struct.pack(
                                    '<2f', float(forcer[0]), float(forcer[1])))
                                d.dire('  source de vue 0x%X corrigee' % src)
                    obj = d.u64(bexe + 0x3E81C0)
                    if obj:
                        cur = d.read(obj + 0x70, 16)
                        if cur and len(cur) == 16:
                            xx, yy, ww, hh = struct.unpack('<4f', cur)
                            if (round(ww), round(hh)) == (1920, 1080):
                                d.write(obj + 0x70 + 8, struct.pack(
                                    '<2f', float(forcer[0]), float(forcer[1])))
                                d.dire('  source de vue [0x%X+0x70] corrigee'
                                       % obj)
                et['vues_forcees'] = et.get('vues_forcees', 0) + 1
                if et['vues_forcees'] >= 3:
                    d.desarmer_logiciel(bp)
                    d.dire('  point d arret RSSetViewports desarme '
                           '(la source est corrigee)')
            cle = (round(x), round(y), round(vw), round(vh))
            if cle in et['vues']:
                et['vues'][cle] += 1
                return
            et['vues'][cle] = 1
            ret3 = d.u64(ctx.Rsp)
            nm, dp = d.module_of(ret3) if ret3 else ('?', 0)
            d.dire('  vue %4.0f x %-4.0f  en (%.0f, %.0f)   par %s+0x%X'
                   % (vw, vh, x, y, nm, dp))
            return

        if bp.nom == 'CreateTexture2D':
            # D3D11_TEXTURE2D_DESC : W+0 H+4 Mip+8 Arr+0xC Fmt+0x10
            #                        SampleCount+0x14 Usage+0x1C Bind+0x20
            desc2 = d.read(ctx.Rdx, 0x2C)
            if not desc2 or len(desc2) < 0x24:
                return
            w, h, mip, arr, fmt = struct.unpack_from('<5I', desc2, 0)
            ech2 = struct.unpack_from('<I', desc2, 0x14)[0]
            bind = struct.unpack_from('<I', desc2, 0x20)[0]
            et['ntex'] = et.get('ntex', 0) + 1
            if not (bind & 0x60):        # ni cible de rendu ni tampon de profondeur
                return
            cle = (w, h, fmt, bind, ech2)
            if cle in et['textures']:
                et['textures'][cle] += 1
                return
            et['textures'][cle] = 1
            # Forcer a la SOURCE est fragile : deux cibles naissent avant que
            # les globaux soient patches (l'une dans vfes.exe+0x34EC4, l'autre
            # dans le moteur avant meme qu'on ait sa base). On force donc ici,
            # au moment ou la cible est creee : c'est exact et sans course.
            if forcer and (w, h) == (1920, 1080):
                d.write(ctx.Rdx, struct.pack('<II', forcer[0], forcer[1]))
                w, h = forcer
                cle = (w, h, fmt, bind, ech2)
                if cle in et['textures']:
                    et['textures'][cle] += 1
                    return
                et['textures'][cle] = 1
            ret2 = d.u64(ctx.Rsp)
            nom_mod, dep2 = d.module_of(ret2) if ret2 else ('?', 0)
            d.dire('  cible %4d x %-4d  format %-3d  ech %d  usage %-12s  par %s+0x%X'
                   % (w, h, fmt, ech2,
                      ('rendu' if bind & 0x20 else '') +
                      ('+profondeur' if bind & 0x40 else ''),
                      nom_mod, dep2))
            return

        if bp.nom == 'SetWindowPos':
            # SetWindowPos(hWnd, hWndAfter, X, Y, cx, cy, uFlags)
            #   rcx      rdx        r8d r9d  [rsp+0x28] [rsp+0x30] [rsp+0x38]
            pile = d.read(ctx.Rsp + 0x28, 0x18)
            if not pile:
                return
            cx, cy, drapeaux = struct.unpack('<iii', pile[0:4] + pile[8:12] + pile[16:20])
            if cx > 100 and cy > 100:
                nom_mod, dep = d.module_of(d.u64(ctx.Rsp) or 0)
                d.dire('  SetWindowPos : %d x %d  en (%d, %d)  depuis %s+0x%X'
                       % (cx, cy, ctx.R8 & 0xFFFFFFFF, ctx.R9 & 0xFFFFFFFF,
                          nom_mod, dep))
                if forcer and et.get('fenetre_aussi'):
                    d.write(ctx.Rsp + 0x28, struct.pack('<q', forcer[0]))
                    d.write(ctx.Rsp + 0x30, struct.pack('<q', forcer[1]))
                    d.dire('      >>> fenetre forcee a %d x %d' % forcer)
                # et le global de vfes.exe TOUT DE SUITE : la premiere cible de
                # rendu (le tampon de profondeur) nait avant le premier tour de
                # tic(), donc avant que --globaux ait pu agir.
                if forcer and et.get('globaux'):
                    b = d.base_de('vfes.exe')
                    if b:
                        a = b + GLOBAUX[0][1]
                        d.write(a, struct.pack('<II', forcer[0], forcer[1]))
                        et['dits'].add(GLOBAUX[0])
                        d.dire('      >>> vfes.exe+0x%X force des maintenant'
                               % GLOBAUX[0][1])
            return
        if bp.nom == 'MoveWindow':
            # MoveWindow(hWnd, X, Y, nWidth, nHeight, bRepaint)
            #   rcx      edx r8d  r9d          [rsp+0x28]
            brut = d.read(ctx.Rsp + 0x28, 4)
            haut_f = struct.unpack('<i', brut)[0] if brut else 0
            larg_f = ctx.R9 & 0xFFFFFFFF
            if larg_f > 100 and haut_f > 100:
                nom_mod, dep = d.module_of(d.u64(ctx.Rsp) or 0)
                d.dire('  MoveWindow : %d x %d  depuis %s+0x%X'
                       % (larg_f, haut_f, nom_mod, dep))
            return
        if bp.nom == 'AdjustWindowRectEx':
            r = d.read(ctx.Rcx, 16)
            if r:
                g, h, dr, b = struct.unpack('<4i', r)
                d.dire('  AdjustWindowRectEx : %d x %d' % (dr - g, b - h))
            return

        # D3D11CreateDeviceAndSwapChain : le descripteur est le 8e argument
        if bp.nom != 'D3D11CreateDeviceAndSwapChain':
            d.dire('  %s appele' % bp.nom)
            return
        pdesc = d.u64(ctx.Rsp + 0x40)
        if not pdesc:
            d.dire('  D3D11CreateDeviceAndSwapChain sans descripteur')
            return
        desc = d.read(pdesc, 0x40)
        if not desc:
            return
        (larg, haut, num, den, fmt) = struct.unpack_from('<5I', desc, 0)
        ech, qual = struct.unpack_from('<2I', desc, 0x1C)
        tampons = struct.unpack_from('<I', desc, 0x28)[0]
        fenetre = struct.unpack_from('<I', desc, 0x38)[0]
        et['vus'] += 1
        # qui appelle ? [rsp] porte l'adresse de retour, donc le site d'appel
        ret = d.u64(ctx.Rsp)
        if ret:
            nom_mod, dep = d.module_of(ret)
            d.dire('  appele depuis %s+0x%X   (descripteur en 0x%X)'
                   % (nom_mod, dep, pdesc))
        d.dire('  chaine d\'echange demandee : %d x %d  a %s Hz  format %s'
               % (larg, haut, ('%g' % (num / den)) if den else '?',
                  FORMATS.get(fmt, fmt)))
        d.dire('      echantillons %d (qualite %d)   tampons %d   fenetre %s'
               % (ech, qual, tampons, 'oui' if fenetre else 'non (plein ecran)'))
        if et.get('chercher'):
            # d'ou vient 1920x1080 ? On balaie la memoire pour le COUPLE
            # (largeur, hauteur) en u32 adjacents : si le moteur tient sa
            # resolution dans un global, il se montre ici.
            import struct as _s
            trouve, vus = balayer(d, [larg, haut], (MEM_IMAGE,))
            for v, nom_v in ((larg, 'largeur'), (haut, 'hauteur')):
                dans = []
                for a in trouve[v]:
                    nom_mod, dep = d.module_of(a)
                    if nom_mod.lower().endswith(('vfes.exe', 'apm3.dll')):
                        dans.append('%s+0x%X' % (nom_mod, dep))
                d.dire('  %s = %d : %d occurrence(s) dans les binaires du jeu'
                       % (nom_v, v, len(dans)))
                for b in dans[:30]:
                    d.dire('      %s' % b)
            d.dire('  (%.0f Mo de zones image balayes)' % (vus / 1048576.0))

        # --cibles : suivre la creation des CIBLES DE RENDU. C'est la seule
        # mesure qui dise a quelle definition la passe 3D travaille vraiment.
        # On recupere le device rendu par l'appel (argument 10, ppDevice), en
        # posant un point d'arret sur l'adresse de retour.
        if et.get('cibles') or et.get('vue'):
            # arg8 pSwapChainDesc=[rsp+0x40], arg9 ppSwapChain=[rsp+0x48],
            # arg10 ppDevice=[rsp+0x50]. J'avais pris 0x48 : c'etait la chaine
            # d'echange, dont la vtable n'a evidemment pas CreateTexture2D.
            et['ppdevice'] = d.u64(ctx.Rsp + 0x50)
            et['ppcontexte'] = d.u64(ctx.Rsp + 0x60)   # arg12 (0x58 = arg11)
            r = d.u64(ctx.Rsp)
            if r and not et.get('bp_retour'):
                et['bp_retour'] = True
                bp2 = instrument.PointArret('retour_D3D11', r, max_coups=2)
                bp2.silencieux = True
                d.bps.append(bp2)
                d.armer_logiciel(bp2)

        if forcer and (larg, haut) != forcer:
            d.write(pdesc, struct.pack('<II', forcer[0], forcer[1]))
            relu = d.read(pdesc, 8)
            d.dire('  >>> FORCE a %d x %d   (relu : %d x %d)'
                   % (forcer[0], forcer[1], *struct.unpack('<II', relu)))

    def tic(d, t):
        # balayage TARDIF : une fois le moteur charge et le combat en cours,
        # on cherche qui tient encore 1920x1080 alors que la chaine d'echange
        # est forcee ailleurs. C'est cette valeur-la qui dimensionne la passe 3D.
        if et.get('scan_a') and not et.get('scan_fait') and t >= et['scan_a']:
            et['scan_fait'] = True
            import struct as _s
            for portee, types in (('image', (MEM_IMAGE,)),
                                  ('privee', (MEM_PRIVATE,))):
                trouve, vus = balayer(d, [1920], types)
                bons = []
                for a in trouve[1920]:
                    suite = d.read(a + 4, 4)
                    if suite and _s.unpack('<I', suite)[0] == 1080:
                        nom_mod, dep = d.module_of(a)
                        bons.append('%s+0x%X' % (nom_mod, dep))
                d.dire('  [t=%.0f s] couple 1920x1080 en zone %s : %d '
                       '(%.0f Mo lus)' % (t, portee, len(bons), vus / 1048576.0))
                for b in bons[:40]:
                    d.dire('      %s' % b)
        # --globaux : reecrire la resolution dans les globaux de la passe 3D,
        # a chaque tour tant que le moteur n'a pas fige ses cibles de rendu.
        if forcer and et.get('globaux'):
            for mod, dep in GLOBAUX:
                b = d.base_de(mod)
                if not b:
                    continue
                a = b + dep
                cur = d.read(a, 8)
                if not cur or len(cur) < 8:
                    continue
                l, h = struct.unpack('<II', cur)
                if (l, h) != forcer and l > 100 and h > 100:
                    d.write(a, struct.pack('<II', forcer[0], forcer[1]))
                    if (mod, dep) not in et['dits']:
                        et['dits'].add((mod, dep))
                        d.dire('  [t=%.0f s] %s+0x%X : %d x %d -> %d x %d'
                               % (t, mod, dep, l, h, forcer[0], forcer[1]))
        for mod, fn in CIBLES:
            if (mod, fn) in et['poses']:
                continue
            base = d.base_de(mod)
            off = deplacement(mod, fn)
            if not base or off is None:
                continue
            et['poses'].add((mod, fn))
            bp = instrument.PointArret(fn, base + off, max_coups=4000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
            d.dire('  point d\'arret sur %s!%s' % (mod, fn))

    dbg.on_bp = sur_bp
    dbg.tic = tic

    if scenario and os.path.exists(scenario):
        with open(scenario, 'rb') as fp:
            data = fp.read()
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(data)
    print('journal : %s%s' % (journal,
                              ('  ; forcage %dx%d' % forcer) if forcer else ''))
    dbg.run(EXE, os.path.dirname(EXE), secondes, tuple(captures))
    fichier.close()
    with open(journal, encoding='utf-8') as fp:
        for ligne in fp:
            if ligne.startswith('  '):
                sys.stdout.write(ligne)
    return 0


if __name__ == '__main__':
    sys.exit(main())
