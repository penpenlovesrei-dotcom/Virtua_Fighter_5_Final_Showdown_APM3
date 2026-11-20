#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""LA SONDE D'UN DECOR : force un decor, mene le jeu SEUL jusqu'au combat,
journalise les fichiers ouverts et fait des captures. Aucun clavier.

Pourquoi : plusieurs defauts des decors ajoutes (le brouillard d'Aoi, la
brume de Lei-Fei, l'eau d'Eileen, les grillages de Jean et de Wolf) ne se
tranchent qu'a l'image ou dans la liste des fichiers que le moteur ouvre.
Attendre qu'on navigue a la main jusqu'au bon decor ne passe pas a l'echelle ;
supposer est exclu.

Comment :

  * le decor est FORCE a l'unique point ou le gestionnaire consomme une
    demande : `0x18018EF40` lit l'indice demande en `[rcx+0x60]` (cf. memoire
    « Deux index de decor ») -- un point d'arret y ecrit l'indice voulu ;
  * le apm.dll de substitution joue un scenario d'appuis sur START
    (`apm_entrees.txt`, relu a chaud) : titre, sauvegarde, avertissement,
    SINGLE PLAYER, Arcade, selection -- puis plus rien, l'ordinateur se bat ;
  * CreateFileW/A sont suivis : chaque chemin qui passe le filtre est ecrit ;
  * des captures a heures fixes (`--captures`, ou `--toutes N`).

Le scenario d'entrees MANUEL est sauve avant et REMIS apres : le jeu lance
ensuite a la main ne doit pas appuyer tout seul.

    py -3 tools/sonde_decor.py 48 --toutes 10 --secondes 160
    py -3 tools/sonde_decor.py 72 --surveiller 0x180677660:4:r:drapeau --dr-max 60
    py -3 tools/sonde_decor.py 48 --fichiers light_param,fog_ --secondes 120
    py -3 tools/sonde_decor.py 54 --captures 90:yk5_a.png,120:yk5_b.png

Sorties : `analysis/sonde_decor.txt` et les captures dans `analysis/sonde/`.
"""
import os
import re
import shutil
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402
import tracer_fichiers                                     # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
# LA MOITIE GRAPHIQUE DU JEU EST DANS L EXECUTABLE. `vfes.exe` porte la
# couche Direct3D 11 : c est lui qui importe d3d11.dll, dxgi.dll et
# d3dcompiler_47.dll, que la DLL du moteur n importe pas. On reconnait ses
# adresses a leur base preferee -- 0x140000000, contre 0x180000000 pour la
# DLL -- et la sonde choisit donc le module TOUTE SEULE.
EXE_NOM = 'vfes.exe'
EXE_BASE = 0x140000000
DLL_BASE = 0x180000000


def _module_et_rva(adr):
    """(nom du module, rva), d apres la base preferee de l adresse."""
    if EXE_BASE <= adr < DLL_BASE:
        return EXE_NOM, adr - EXE_BASE
    return MOTEUR, adr - DLL_BASE
DEMANDE = 0x18EF40              # rva du consommateur de la demande de decor
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                              'apm_entrees.txt')
APPUIS = (20, 24, 28, 32, 38, 44, 52, 58, 64, 70)


def _lire_memoire(d, mem):
    """Rend quatre mots a l adresse voulue, en hexa ET en flottant.

    `mem` est (forme, adresse, offset). La forme `*` deref l adresse puis
    ajoute l offset -- les structures du moteur vivent au bout d un pointeur
    global, et leur adresse change a chaque lancement.
    """
    forme, adr, off, off2 = mem
    if forme == '**':
        try:
            p = d.u64(adr)
            if not p:
                return '[mem] pointeur 0x%X = 0' % adr
            p2 = d.u64(p + off)
        except Exception as e:
            return '[mem] double indirection depuis 0x%X : %s' % (adr, e)
        if not p2:
            return '[mem] le descripteur 0x%X ne porte aucun pointeur' % (p + off)
        adr = p2 + off2
    elif forme == '*':
        try:
            p = d.u64(adr)
        except Exception as e:
            return '[mem] pointeur 0x%X illisible (%s)' % (adr, e)
        if not p:
            return '[mem] pointeur 0x%X = 0 -- la structure n existe pas' % adr
        adr = p + off
    mots = []
    for k in range(4):
        try:
            v = d.u32(adr + 4 * k)
        except Exception as e:
            return '[mem] 0x%X illisible (%s)' % (adr + 4 * k, e)
        if v is None:                      # u32 rend None quand la page
            return '[mem] 0x%X illisible' % (adr + 4 * k)   # n est pas lisible
        mots.append(v)
    flot = struct.unpack('<4f', struct.pack('<4I', *mots))
    return ('[mem 0x%X] %s  =  %s'
            % (adr, ' '.join('%08X' % v for v in mots),
               ' '.join('%g' % f for f in flot)))


def scenario(appuis, quest=0, touches=()):
    lignes = ['# ecrit par tools/sonde_decor.py -- remplace le temps d une sonde',
              'nom start = 7', 'front   = 20', 'journal = 0', 'clavier = 1',
              'manette = 1']
    if quest:
        # le module Quest d apm.dll ne fait rien sans cette ligne
        lignes.append('quest   = %g' % quest)
    lignes += ['', '0       rien']
    horaire = []
    for t in appuis:
        ms = int(t * 1000)
        horaire += [(ms, '%d   start' % ms), (ms + 300, '%d   rien' % (ms + 300))]
    # --touches 40:5,43:5 : d autres boutons que START (codes ou noms), pour
    # eprouver un ecran a nous -- le mode Quest lit 4 (gauche) et 5 (droite)
    #
    # DUREE DE L'APPUI : 80 ms, pas 200. MESURE du 2026-09-12 : a 200 ms, une
    # seule ligne « 48:3 » faisait descendre le curseur du menu de DEUX crans
    # (SCOREBOARDS puis OPTIONS) -- la repetition automatique du menu tombait
    # dedans. 80 ms font cinq trames : assez pour etre vu, trop peu pour
    # repeter.
    for t, nom in touches:
        ms = int(t * 1000)
        horaire += [(ms, '%d   %s' % (ms, nom)),
                    (ms + 80, '%d   rien' % (ms + 80))]
    lignes += [l for _, l in sorted(horaire)]
    return ('\n'.join(lignes) + '\n').encode('ascii')


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith('--'):
        print(__doc__)
        return 1
    indice = int(a[0], 0)
    secondes = 150
    if '--secondes' in a:
        secondes = int(a[a.index('--secondes') + 1])
    appuis = APPUIS
    if '--appuis' in a:
        appuis = [float(x) for x in a[a.index('--appuis') + 1].split(',')]
    # --quest 80 : arme l essai du mode Quest dans apm.dll a 80 s
    quest = float(a[a.index('--quest') + 1]) if '--quest' in a else 0
    touches = []
    if '--touches' in a:
        for spec in a[a.index('--touches') + 1].split(','):
            q, nom = spec.split(':', 1)
            touches.append((float(q), nom))
    # --bp 0x180072BA0:dessin,0x180072C3F:texture  -> journal rax/rcx/rdx
    #
    # Un troisieme champ donne une MEMOIRE a lire a chaque passage :
    #
    #   . directe   `0x180715498`            une adresse de la DLL ;
    #   . INDIRECTE `*0x180C414F8+0x759A0`   on deref le pointeur, PUIS on
    #                                        ajoute l offset.
    #
    # L indirecte est la seule facon d atteindre les structures du moteur :
    # elles vivent au bout d un pointeur global, jamais a une adresse fixe.
    # Dans les deux cas le journal rend QUATRE mots, en hexa et en flottant --
    # un `env` du moteur est un vec4, et c est le flottant qui parle.
    espions = []
    if '--bp' in a:
        for spec in a[a.index('--bp') + 1].split(','):
            morceaux = spec.split(':')
            mem = None
            if len(morceaux) > 2:
                m2 = re.match(r'^\*\*(0x[0-9a-fA-F]+)\+(0x[0-9a-fA-F]+)'
                              r'\+(0x[0-9a-fA-F]+)$', morceaux[2])
                m = re.match(r'^\*(0x[0-9a-fA-F]+)\+(0x[0-9a-fA-F]+)$',
                             morceaux[2])
                if m2:
                    # double indirection : [[A]+B]+C -- un descripteur qui
                    # porte un POINTEUR vers ses donnees
                    mm, mr = _module_et_rva(int(m2.group(1), 16))
                    mem = ('**', mr, int(m2.group(2), 16),
                           int(m2.group(3), 16), mm)
                elif m:
                    mm, mr = _module_et_rva(int(m.group(1), 16))
                    mem = ('*', mr, int(m.group(2), 16), 0, mm)
                else:
                    mm, mr = _module_et_rva(int(morceaux[2], 16))
                    mem = ('=', mr, 0, 0, mm)
            mod, rva = _module_et_rva(int(morceaux[0], 16))
            espions.append((rva, morceaux[1], mem, mod))
    # --histo 0x18007E322:empreinte:Rbp+xmm6  -> compte chaque valeur prise
    # (les entiers tels quels, un xmm en flottant arrondi au 0,05) ; le
    # tableau est ecrit a la fin du journal
    histos = []
    if '--histo' in a:
        for spec in a[a.index('--histo') + 1].split(','):
            adr, nom, regs = spec.split(':')
            histos.append((int(adr, 16) - 0x180000000, nom, regs.split('+')))
    # --surveiller 0x180677660:4:r:drapeau_water_ring
    #   pose un POINT D ARRET MATERIEL sur une adresse de DONNEES : le
    #   processeur arrete le jeu a chaque acces et le journal donne le RIP de
    #   l instruction fautive. C est la seule facon de savoir qui lit un champ
    #   quand la lecture statique ne trouve personne.
    #   Le x86 n a pas de surveillance en LECTURE SEULE : 'r' rapporte aussi
    #   les ecritures (DR7 code 11). 'w' ne rapporte que les ecritures.
    surveiller = []
    if '--surveiller' in a:
        for spec in a[a.index('--surveiller') + 1].split(','):
            m = spec.split(':')
            surveiller.append((int(m[0], 16) - 0x180000000,
                               int(m[1]) if len(m) > 1 else 4,
                               m[2] if len(m) > 2 else 'r',
                               m[3] if len(m) > 3 else m[0]))
    filtres = []
    if '--fichiers' in a:
        filtres = [x.strip().lower()
                   for x in a[a.index('--fichiers') + 1].split(',')]
    dossier = os.path.join(RACINE, 'analysis', 'sonde')
    os.makedirs(dossier, exist_ok=True)
    captures = []
    if '--captures' in a:
        for spec in a[a.index('--captures') + 1].split(','):
            t, nom = spec.split(':', 1)
            captures.append((os.path.join(dossier, nom), float(t),
                             'Virtua Fighter'))
    if '--toutes' in a:
        pas = float(a[a.index('--toutes') + 1])
        debut = float(a[a.index('--depuis') + 1]) if '--depuis' in a else 40
        t = debut
        while t < secondes - 2:
            captures.append((os.path.join(dossier, 'd%d_t%03d.png'
                                          % (indice, t)), t, 'Virtua Fighter'))
            t += pas

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = True
    dbg.bp_max = 400000
    if '--dr-max' in a:
        dbg.dr_max = int(a[a.index('--dr-max') + 1])
    journal = os.path.join(RACINE, 'analysis', 'sonde_decor.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'forces': 0, 'vus': {}, 'poses': set(), 'mem': {},
          'histos': {}}
    regs_de = {'histo:' + nom: regs for _, nom, regs in histos}

    def valeur(ctx, r):
        if r.lower().startswith('xmm'):
            bas = ctx.FltSave.XmmRegisters[int(r[3:])].Low & 0xFFFFFFFF
            f = struct.unpack('<f', struct.pack('<I', bas))[0]
            return round(f * 20) / 20
        return getattr(ctx, r) & 0xFFFFFFFF

    def sur_bp(d, bp, ctx, tid):
        if bp.nom.startswith('histo:'):
            cle = tuple(valeur(ctx, r) for r in regs_de[bp.nom])
            h = et['histos'].setdefault(bp.nom[6:], {})
            h[cle] = h.get(cle, 0) + 1
            return
        if bp.nom.startswith('espion:'):
            n = et.setdefault('espions', {}).get(bp.nom, 0) + 1
            et['espions'][bp.nom] = n
            if n <= 6 or n in (50, 500, 5000):
                d.dire('  %s #%d [fil %d] : rax=0x%X rcx=0x%X rdx=0x%X '
                       'rbx=0x%X rdi=0x%X rsi=0x%X r8=0x%X'
                       % (bp.nom[7:], n, tid, ctx.Rax, ctx.Rcx, ctx.Rdx,
                          ctx.Rbx, ctx.Rdi, ctx.Rsi, ctx.R8))
                mem = et['mem'].get(bp.nom)
                if mem is not None:
                    d.dire('      %s' % _lire_memoire(d, mem))
            return
        if bp.nom == 'demande':
            v = d.u32(ctx.Rcx + 0x60)
            if v in (0xFFFFFFFF, indice):
                return
            d.write(ctx.Rcx + 0x60, indice.to_bytes(4, 'little'))
            et['forces'] += 1
            d.dire('  decor demande %d -> force a %d' % (v, indice))
            return
        adr = ctx.Rcx                  # 1er argument de CreateFile (x64)
        if not adr:
            return
        brut = d.read(adr, 520)
        if not brut:
            return
        if bp.nom.endswith('W'):
            t = brut.decode('utf-16-le', 'ignore').split('\x00', 1)[0]
        else:
            t = brut.split(b'\x00', 1)[0].decode('latin-1', 'ignore')
        if not t or (filtres and not any(f in t.lower() for f in filtres)):
            return
        if t not in et['vus']:
            d.dire('  fichier : %s' % t)
        et['vus'][t] = et['vus'].get(t, 0) + 1

    def tic(d, t):
        b = d.base_de(MOTEUR)
        if b and not et['pose']:
            et['pose'] = True
            bp = instrument.PointArret('demande', b + DEMANDE, max_coups=100000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
            d.dire('  point d arret sur la demande de decor, t=%.0f s' % t)
            for rva, nom, mem, mod in espions:
                bmod = b if mod == MOTEUR else d.base_de(mod)
                if bmod is None:
                    d.dire('  %s pas encore charge : espion %s NON arme'
                           % (mod, nom))
                    continue
                if mem is not None:
                    # chaque adresse suit la base de SON module : on peut
                    # arreter dans l exe et lire une globale de la DLL
                    bmem = b if mem[4] == MOTEUR else d.base_de(mem[4])
                    if bmem is None:
                        d.dire('  %s pas encore charge : lecture memoire de '
                               '%s abandonnee' % (mem[4], nom))
                    else:
                        et['mem']['espion:' + nom] = (mem[0], bmem + mem[1],
                                                      mem[2], mem[3])
                bp = instrument.PointArret('espion:' + nom, bmod + rva,
                                           max_coups=100000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)
            for rva, nom, _ in histos:
                bp = instrument.PointArret('histo:' + nom, b + rva,
                                           max_coups=100000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)
            for rva, taille, acces, nom in surveiller:
                d.armer_materiel(b + rva, taille, acces, nom)
        if not filtres:
            return
        for mod in tracer_fichiers.MODULES:
            for fn in tracer_fichiers.FONCTIONS:
                if (mod, fn) in et['poses']:
                    continue
                base = d.base_de(mod)
                off = tracer_fichiers.deplacement(mod, fn)
                if not base or off is None:
                    continue
                et['poses'].add((mod, fn))
                bp = instrument.PointArret(fn, base + off, max_coups=400000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    sauve = SCENARIO_ACTIF + '.avant_sonde'
    shutil.copyfile(SCENARIO_ACTIF, sauve)
    try:
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(scenario(appuis, quest, touches))
        print('decor force : %d ; %d s ; %d capture(s) ; journal %s'
              % (indice, secondes, len(captures), journal))
        r = dbg.run(EXE, os.path.dirname(EXE), secondes, tuple(captures))
    finally:
        shutil.copyfile(sauve, SCENARIO_ACTIF)
        os.remove(sauve)
        for nom, h in sorted(et['histos'].items()):
            fichier.write('  histo %s : %d coups, %d valeurs\n'
                          % (nom, sum(h.values()), len(h)))
            for cle, n in sorted(h.items(), key=lambda kv: -kv[1])[:60]:
                fichier.write('    %-28s %d\n' % (cle, n))
        fichier.close()
    with open(journal, encoding='utf-8') as fp:
        for ligne in fp:
            if ligne.startswith('  ') or 'REFUS' in ligne or 'EXCEPTION' in ligne:
                sys.stdout.write(ligne)
    for t in [x for x in getattr(dbg, 'debug_strings', []) if '[quest]' in x]:
        print('  %s' % t)
    print('\n%d forcage(s) ; %d fichier(s) distinct(s) ; scenario manuel remis'
          % (et['forces'], len(et['vus'])))
    return r


if __name__ == '__main__':
    sys.exit(main())
