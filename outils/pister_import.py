#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Depiste un decor IMPORTE : ce qui est pose, ce qui est ouvert, ou ca bloque.

Un decor importe peut echouer de trois facons, et elles ne se ressemblent pas a
l'ecran -- toutes les trois donnent le meme ecran de chargement qui tourne :

  1. le fichier n'est PAS LU        -> le nom n'a pas ete masque dans le .par ;
  2. le fichier est lu mais REFUSE  -> un objet demande n'existe pas dedans ;
  3. le fichier est accepte mais une PIECE ANNEXE manque (collision, auth_3d,
     eclairage, son) -> la barriere de l'etat 3 ne passe jamais.

Cet outil repond aux trois, dans cet ordre.

CONTROLE AVANT VOL (sans lancer le jeu)
    les huit fichiers poses, leur taille et leur magie ; les huit noms masques
    dans l'index du .par ; le descripteur du moteur ; et surtout : les objets
    que le descripteur DEMANDE existent-ils dans l'objset qu'on a pose ?

MESURE (jeu lance, clavier rendu)
    . points d'arret sur CreateFileW/A : quels fichiers du decor sont ouverts ;
    . les SEPT portes de la barriere de l'etat 3 de `0x18018F680`, une par une ;
    . l'etat de `TaskStage` (`[0x1807499D8] + 0x58`) releve chaque demi-seconde.

Le verdict nomme la porte qui n'a pas passe.

    py -3 tools/pister_import.py djo
    py -3 tools/pister_import.py djo --controle       (avant vol seulement)
    py -3 tools/pister_import.py djo --secondes 300
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                              # noqa: E402
import objset as mod_objset                                    # noqa: E402
import par_masquer                                             # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
EXE = os.path.join(JEU, 'vfes.exe')
MEDIA = os.path.join(JEU, 'vf5fs_media')
PAR = os.path.join(JEU, 'vf5fs_data.par')
SCENARIO_ACTIF = os.path.join(JEU, 'apm_entrees.txt')
SCENARIO = """# ecrit par tools/pister_import.py -- le clavier mene, on ne force rien.
front   = 200
journal = 0
clavier = 1
manette = 1
0       rien
"""

DECORS = ['tst', 'ts2', 'ts3', 'wht', 'ban', 'ter', 'nyc', 'cas', 'riv', 'jin',
          'sin', 'djo', 'umi', 'hai', 'are', 'slk', 'yuk', 'tak', 'aur', 'bar',
          'tan', 'du1', 'du2', 'du3', 'du4', 'du5', 'trm', 'cid', 'trs',
          'evo00', 'evo01', 'evo02', 'evo03', 'evo04', 'evo05', 'evo06',
          'evo07', 'evo08', 'evo09', 'gym', 'smo']

TABLE_RVA = 0x403430                # 0x180403430, les 41 descripteurs
TACHE_RVA = 0x7499D8                # 0x1807499D8, le singleton TaskStage

# La barriere de l'etat 3, lue dans `analysis/disasm_decors_B.txt`. Chaque
# adresse est le point atteint UNIQUEMENT si la porte precedente a passe : la
# porte la plus haute atteinte designe donc celle qui bloque.
PORTES = [
    (0x18F74A, 'entree de l\'etat 3'),
    (0x18F760, 'porte 1 : l\'OBJSET est pret (geometrie + textures)'),
    (0x18F76D, 'porte 2 : l\'ECLAIRAGE est pret (ibl + light_param)'),
    (0x18F77A, 'porte 3 : la COLLISION est prete (STGxxx_COLI.000.bin)'),
    (0x18F78E, 'porte 4 : l\'auth_3d du DECOR est pret (STGxxx.farc)'),
    (0x18F7A2, 'porte 5 : le drapeau de scene est retombe'),
    (0x18F7B7, 'porte 6 : l\'auth_3d des EFFETS est pret (EFFSTGxxx.farc)'),
    (0x18F7C4, 'porte 7 : les SONS d\'ambiance sont prets'),
]
JALONS = [(0x18FAF5, 'etat 2 : les fichiers annexes sont demandes'),
          (0x18F952, 'etat 3 : la barriere commence'),
          (0x18F821, 'etat 4 : tout est charge'),
          (0x18F73E, 'ETAT 5 : LE DECOR EST EN PLACE')]

ETATS = {0: 'inactif', 1: 'pesee + demande de geometrie',
         2: 'fichiers annexes', 3: 'BARRIERE D\'ATTENTE', 4: 'derniere attente',
         5: 'EN PLACE', 6: 'dechargement', 7: 'dechargement',
         8: 'dechargement', 9: 'dechargement'}


def morceaux(code):
    """Les DIX fichiers d'un decor. Le dixieme, `envmap_correct_`, a coute un
    ecran de chargement infini le 2026-09-10 : le chargeur d'eclairage
    `0x1800D7130` compose SIX chemins, et celui-la n'existe pas dans le dump
    VF5R. Voir `analysis/decors.md` section 16."""
    return morceaux_source(code) + [
        ('light_param', 'envmap_correct_%s.txt' % code.lower())]


def morceaux_source(code):
    """Les NEUF que la generation source fournit -- ceux qu'un remplacement
    pose sur le disque et masque dans le `.par`."""
    c, C = code.lower(), code.upper()
    return [('objset', 'stg%s.farc' % c),
            ('', 'STG%s_COLI.000.bin' % C),
            ('auth_3d', 'STG%s.farc' % C),
            ('auth_3d', 'EFFSTG%s.farc' % C),
            ('ibl', '%s.ibl' % c),
            ('light_param', 'light_%s.txt' % c),
            ('light_param', 'fog_%s.txt' % c),
            ('light_param', 'glow_%s.txt' % c),
            ('light_param', 'wind_%s.txt' % c)]


def table_des_descripteurs(d):
    """La base de la table, LUE DANS LE BINAIRE et non supposee.

    `--decors-table` la DEMENAGE dans la section `.decors`. Une adresse en dur
    ici lirait le descripteur d'un autre decor sans le dire -- verifie le
    2026-09-10, ou 0x180403430 + 42*0xF0 rendait du5. On relit donc le disp32
    du `lea` de `0x18018EF78`, exactement comme le moteur.
    """
    disp, = struct.unpack_from('<i', d, 0x18EF7B)
    return (0x18018EF7F + disp) - 0x180000000


def descripteur(indice):
    """Rend (objset, [ids demandes]) lus dans le binaire QUI TOURNE."""
    import pefile
    pe = pefile.PE(os.path.join(JEU, MOTEUR), fast_load=True)
    d = pe.get_memory_mapped_image()
    base = table_des_descripteurs(d)
    o = base + indice * 0xF0
    objset, = struct.unpack_from('<i', d, o + 0x10)
    champs = struct.unpack_from('<9i', d, o + 0x14)
    return objset, [v for v in champs if v != -1]


def controle(code, indice):
    """Tout ce qui se verifie SANS lancer le jeu. Rend le nombre de fautes."""
    fautes = []
    print('=' * 72)
    print('CONTROLE AVANT VOL -- decor « %s », indice %d' % (code, indice))
    print('=' * 72)

    # UN REMPLACEMENT N'A PAS A POSER LA DIXIEME PIECE, ET C'EST TOUT LE
    # CONTRAIRE D'UN DETAIL (repare le 2026-09-10). `envmap_correct_<code>.txt`
    # existe dans le `.par` pour les 41 decors du jeu : quand on REMPLACE, son
    # nom n'est pas masque et l'archive continue de le fournir -- l'exiger sur
    # le disque faisait echouer le controle de `decor_5r_akira.cmd`, donc le
    # lanceur validé refusait de partir. Quand on AJOUTE, rien ne repond pour
    # le code neuf : la piece devient obligatoire.
    ajoute = code not in DECORS
    du_par = {n for _, n in morceaux(code)} - {n for _, n in morceaux_source(code)}
    print('\n1. Les fichiers poses dans vf5fs_media/rom/')
    poses = {}
    for dest, nom in morceaux(code):
        p = os.path.join(MEDIA, 'rom', dest, nom)
        if not os.path.exists(p):
            if nom in du_par and not ajoute:
                print('   %-26s absent du disque -- le .par le fournit '
                      '(remplacement)' % nom)
                continue
            print('   %-26s ABSENT' % nom)
            fautes.append('fichier absent : %s' % nom)
            continue
        tete = open(p, 'rb').read(4)
        poses[nom] = p
        print('   %-26s %10d o   %s' % (nom, os.path.getsize(p),
                                        tete.decode('latin-1').strip()))

    print('\n2. Les noms masques dans l\'index du .par')
    with open(PAR, 'rb') as fp:
        entete = fp.read(0x20)
        borne = par_masquer.fin_du_pot(entete + b'')
        fp.seek(0)
        pot = fp.read(borne)
    for _, nom in morceaux(code):
        clair = pot.count(nom.encode() + b'\x00')
        cache = pot.count((nom[:-1] + '_').encode() + b'\x00')
        if clair and nom in du_par and not ajoute:
            print('   %-26s visible EXPRES : c est le .par qui le fournit'
                  % nom)
            continue
        if clair:
            print('   %-26s ENCORE VISIBLE (%d) -> le .par gagne, le fichier '
                  'pose ne sera JAMAIS lu' % (nom, clair))
            fautes.append('nom non masque : %s' % nom)
        else:
            print('   %-26s masque (%d)' % (nom, cache))

    print('\n3. Le descripteur du moteur')
    objset, demandes = descripteur(indice)
    print('   objset demande : %d' % objset)
    print('   objets demandes : %s'
          % ' '.join('%d:%d' % ((v >> 16) & 0xFFFF, v & 0xFFFF)
                     for v in demandes))

    print('\n4. Les objets demandes existent-ils dans l\'objset POSE ?')
    arch = poses.get('stg%s.farc' % code.lower())
    if not arch:
        print('   impossible : l\'archive n\'est pas posee')
    else:
        import farc
        interne = 'stg%s_obj.bin' % code.lower()
        tmp = os.path.join(RACINE, 'extracted', '_controle_%s' % code)
        chemin = os.path.join(tmp, interne)
        # l'archive fait des dizaines de Mo : on ne la redecompresse que si
        # elle a change depuis la derniere fois.
        if not os.path.exists(chemin) or \
                os.path.getmtime(chemin) < os.path.getmtime(arch):
            os.makedirs(tmp, exist_ok=True)
            farc.extract_one(arch, tmp, quiet=True)
        o = mod_objset.Objset(chemin)
        ids = dict(zip(o.ids(), o.noms()))
        print('   l\'objset pose porte %d objets, id max %d'
              % (o.nombre, o.id_max))
        for v in demandes:
            hi, lo = (v >> 16) & 0xFFFF, v & 0xFFFF
            if hi != objset:
                print('   %5d:%-5d objset COMMUN, non verifiable ici' % (hi, lo))
                continue
            if lo in ids:
                print('   %5d:%-5d %s' % (hi, lo, ids[lo]))
            else:
                print('   %5d:%-5d INTROUVABLE dans l\'objset pose' % (hi, lo))
                fautes.append('objet %d absent de l\'objset pose' % lo)

    print('\n' + '-' * 72)
    if fautes:
        print('%d FAUTE(S) -- inutile de lancer le jeu :' % len(fautes))
        for f in fautes:
            print('   . %s' % f)
    else:
        print('Rien a redire : les fichiers sont poses, les noms masques, et')
        print('l\'objset pose contient tous les objets que le moteur demande.')
    print('-' * 72)
    return len(fautes)


def mesurer(code, secondes):
    noms_attendus = [n.lower() for _, n in morceaux(code)]
    journal = os.path.join(RACINE, 'analysis', 'pister_import_%s.txt' % code)
    fichier = open(journal, 'w', encoding='utf-8')

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = True
    dbg.bp_max = 200000
    dbg.sortie = fichier

    et = {'poses': False, 'fichiers': {}, 'portes': {}, 'jalons': {},
          'etat': None, 'histoire': [], 'base': 0, 'chrono3': None}

    par_bp = {}

    def sur_bp(d, bp, ctx, tid):
        if bp.nom in ('CreateFileW', 'CreateFileA'):
            brut = d.read(ctx.Rcx, 520) if ctx.Rcx else None
            if not brut:
                return
            if bp.nom.endswith('W'):
                t = brut.decode('utf-16-le', 'ignore').split('\x00', 1)[0]
            else:
                t = brut.split(b'\x00', 1)[0].decode('latin-1', 'ignore')
            bas = t.lower()
            for n in noms_attendus:
                if bas.endswith('\\' + n) or bas.endswith('/' + n):
                    et['fichiers'][n] = et['fichiers'].get(n, 0) + 1
                    if et['fichiers'][n] == 1:
                        d.dire('  OUVERT : %s' % t)
                    return
            return
        cible = par_bp[bp.nom]
        if cible[0] == 'porte':
            et['portes'][cible[1]] = et['portes'].get(cible[1], 0) + 1
        else:
            if cible[1] not in et['jalons']:
                d.dire('  JALON : %s' % cible[2])
            et['jalons'][cible[1]] = et['jalons'].get(cible[1], 0) + 1

    def tic(d, t):
        if not et['poses']:
            b = d.base_de(MOTEUR)
            if not b:
                return
            et['base'] = b
            et['poses'] = True
            for i, (rva, texte) in enumerate(PORTES):
                nom = 'porte%d' % i
                par_bp[nom] = ('porte', i, texte)
                bp = instrument.PointArret(nom, b + rva, max_coups=200000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)
            for i, (rva, texte) in enumerate(JALONS):
                nom = 'jalon%d' % i
                par_bp[nom] = ('jalon', i, texte)
                bp = instrument.PointArret(nom, b + rva, max_coups=200000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)
            import ctypes
            k32 = ctypes.WinDLL('kernel32', use_last_error=True)
            k32.GetModuleHandleW.restype = ctypes.c_void_p
            k32.GetProcAddress.restype = ctypes.c_void_p
            k32.GetProcAddress.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
            for mod in ('KERNELBASE.dll', 'KERNEL32.DLL'):
                bm = d.base_de(mod)
                h = k32.GetModuleHandleW(mod)
                if not bm or not h:
                    continue
                for fn in ('CreateFileW', 'CreateFileA'):
                    p = k32.GetProcAddress(ctypes.c_void_p(h), fn.encode())
                    if not p:
                        continue
                    bp = instrument.PointArret(fn, bm + (p - h),
                                               max_coups=200000)
                    bp.silencieux = True
                    d.bps.append(bp)
                    d.armer_logiciel(bp)
            d.dire('  instruments poses a t=%.1f s' % t)
            return
        singleton = d.u64(et['base'] + TACHE_RVA)
        if not singleton:
            return
        etat = d.u32(singleton + 0x58)
        courant = d.u32(singleton + 0x5C)
        if etat is None:
            return
        if etat != et['etat']:
            et['etat'] = etat
            nom = (DECORS[courant] if courant is not None
                   and courant < len(DECORS)
                   else ('AJOUTE-%d' % courant if courant is not None
                         and courant < 0x100 else '?'))
            et['histoire'].append((t, etat, nom))
            d.dire('  t=%6.1f s  etat %d (%s)  decor courant %s'
                   % (t, etat, ETATS.get(etat, '?'), nom))
            et['chrono3'] = t if etat == 3 else None

    dbg.on_bp = sur_bp
    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)

    print('\nLe jeu se lance ; le clavier est a vous.')
    print('  Allez au DOJO avec Akira en partenaire, ou STAGE SELECT.')
    print('  journal : %s' % journal)
    print()
    dbg.run(EXE, JEU, secondes, ())
    fichier.close()

    etats_vus = {e for _, e, _ in et['histoire']}
    demande = bool(etats_vus - {0})

    print()
    print('=' * 72)
    print('CE QUI A ETE OUVERT SUR LE DISQUE')
    for _, n in morceaux(code):
        k = n.lower()
        if k in et['fichiers']:
            print('   %-26s ouvert %d fois' % (n, et['fichiers'][k]))
        else:
            print('   %-26s JAMAIS OUVERT' % n)
    if not et['fichiers'] and demande:
        print('   -> aucun, alors qu\'un decor a ete demande. Le moteur lit')
        print('      donc encore le .par : les noms ne sont pas masques.')
    elif not et['fichiers']:
        print('   -> aucun, et aucun decor n\'a ete demande non plus : la')
        print('      mesure n\'a rien pu voir.')

    print()
    print('L\'ETAT DE LA TACHE, AU FIL DU TEMPS')
    if not et['histoire']:
        print('   jamais releve (la tache n\'a pas ete atteinte)')
    for t, e, nom in et['histoire']:
        print('   t=%6.1f s  etat %d  %-24s decor %s'
              % (t, e, ETATS.get(e, '?'), nom))

    print()
    print('LA BARRIERE DE L\'ETAT 3, PORTE PAR PORTE')
    derniere = -1
    for i, (_, texte) in enumerate(PORTES):
        n = et['portes'].get(i, 0)
        if n:
            derniere = i
        print('   %-64s %s' % (texte, ('%d passage(s)' % n) if n
                               else 'JAMAIS ATTEINTE'))

    print()
    print('=' * 72)
    if not demande:
        print('PAS DE VERDICT : aucun decor n\'a ete demande pendant la')
        print('  mesure -- la tache est restee a l\'etat 0. Relancez et allez')
        print('  jusqu\'au DOJO ou jusqu\'a un combat : c\'est la demande de')
        print('  decor qui declenche tout ce que cet outil observe.')
    elif et['jalons'].get(3):
        print('VERDICT : le decor est arrive a l\'ETAT 5 -- il s\'est charge.')
    elif derniere < 0:
        print('VERDICT : la barriere n\'a jamais ete atteinte. Le blocage est')
        print('  EN AMONT : etat 1 (la demande de geometrie) ou etat 2.')
        print('  Regardez la liste des fichiers ouverts ci-dessus.')
    elif derniere + 1 < len(PORTES):
        print('VERDICT : bloque sur « %s ».' % PORTES[derniere + 1][1])
        print('  C\'est la premiere porte jamais franchie ; celle d\'avant')
        print('  passe. La piece a mettre en cause est celle qu\'elle nomme.')
    else:
        print('VERDICT : les sept portes passent, mais l\'etat 5 n\'est pas')
        print('  atteint : le blocage est a l\'etat 4 (0x1800F8A40).')
    print('=' * 72)
    return 0


def main():
    argv = sys.argv[1:]
    secondes = 240
    if '--secondes' in argv:
        i = argv.index('--secondes')
        secondes = int(argv[i + 1])
        del argv[i:i + 2]
    codes = [a for a in argv if not a.startswith('--')]
    if not codes:
        print(__doc__)
        return 1
    indice = None
    if '--indice' in argv:
        i = argv.index('--indice')
        indice = int(argv[i + 1], 0)
        del argv[i:i + 2]
    codes = [a for a in argv if not a.startswith('--')]
    code = codes[0].lower()
    if indice is None:
        if code not in DECORS:
            print('decor inconnu : %s. Un decor AJOUTE n\'est pas dans la '
                  'liste des 41 : donnez son indice avec --indice <n>.' % code)
            return 1
        indice = DECORS.index(code)
    fautes = controle(code, indice)
    if '--controle' in argv:
        return 1 if fautes else 0
    if fautes:
        print('\nLe jeu n\'est PAS lance : corrigez d\'abord ce qui precede.')
        print('  py -3 tools/importer_decor.py --poser %s --source VF5R' % code)
        return 1
    return mesurer(code, secondes)


if __name__ == '__main__':
    sys.exit(main())
