#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Ou le dessin du nom de variante fait-il planter ?

Frederic, 2026-09-08 : « le jeu plante juste avant de pouvoir se positionner
sur l'icone du decor de Dural » -- c'est-a-dire a la PREMIERE trame ou
`[rbx+0x5C]` entre dans l'anneau 21..25 et ou `DESSINER` s'execute vraiment.
Avant cette case, la garde le fait sortir tout de suite ; c'est pour cela que
tout allait bien jusque-la.

DESSINER enchaine cinq appels au moteur. On pose un jalon devant chacun : le
DERNIER jalon atteint nomme celui qui fait faute. Le debogueur journalise en
plus l'exception elle-meme, avec son adresse.

    0x180EA1313  avant 0x18019A8C0   construire le DESCRIPTEUR
    0x180EA131F  avant 0x18019A9D0   construire le STYLE
    0x180EA132B  avant 0x18019B6F0   poser le mode 2
    0x180EA1344  avant 0x18019B830   poser la taille (32.0)
    0x180EA13AE  avant 0x18019B2E0   LE DESSIN
    0x180EA13BA  apres le dessin     -- atteint = le dessin a survecu

L'outil patche lui-meme la DLL avec `--variantes-texte` : la build courante
n'a pas le dessin, sinon le jeu serait inutilisable.

    py -3 tools/pister_dessin.py
    py -3 tools/pister_dessin.py --secondes 300
"""
import os
import struct
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                              # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
EXE = os.path.join(JEU, 'vfes.exe')
SCENARIO_ACTIF = os.path.join(JEU, 'apm_entrees.txt')
SCENARIO = """# ecrit par tools/pister_dessin.py -- le clavier mene.
front   = 10
journal = 0
clavier = 1
manette = 1
0       rien
"""

GREFFE = 0xEA1000
JALONS = [
    (0x0313, 'construire le DESCRIPTEUR (0x18019A8C0)'),
    (0x031F, 'construire le STYLE (0x18019A9D0)'),
    (0x032B, 'poser le mode 2 (0x18019B6F0)'),
    (0x0344, 'poser la taille 32.0 (0x18019B830)'),
    (0x03B9, 'LE DESSIN (0x18019B2E0)'),
    (0x03BE, 'apres -- ATTENTION : la garde y saute aussi'),
]
DUMP = 0x03B9          # la, rcx = descripteur, rdx = 0x28, r8 = la chaine

OPTIONS = ('--resolution 1280 720 --langue --logo-japonais --dural --wxga '
           '--dural-grille --mode 0 --menu-init --sousmenu --transition-game '
           '--sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer '
           '--options-raccourci --dojo-howto --dojo-cadre --options-sans-howto '
           '--menu-exit --legende-sousmenu --attract-retour-titre '
           '--sans-now-loading --options-tips --decor-perso djo '
           '--decors-dural cas --variantes --variantes-texte '
           '--du2-collision').split()


def main():
    argv = sys.argv[1:]
    secondes = 300
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    print('1/2  patch AVEC le dessin (--variantes-texte)')
    r = subprocess.run([sys.executable,
                        os.path.join(ICI, 'patch_moteur.py')] + OPTIONS,
                       capture_output=True, text=True, cwd=RACINE)
    if r.returncode:
        print(r.stdout[-2000:])
        print('le patch a echoue')
        return 1

    journal = os.path.join(RACINE, 'analysis', 'pister_dessin.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = True
    dbg.bp_max = 200000
    dbg.sortie = fichier
    et = {'poses': False, 'atteints': {}, 'ordre': [], 'dumps': 0}

    def sur_bp(d, bp, ctx, tid):
        if bp.nom not in et['atteints']:
            et['ordre'].append(bp.nom)
            d.dire('  JALON atteint : %s' % bp.nom)
        et['atteints'][bp.nom] = et['atteints'].get(bp.nom, 0) + 1
        if not bp.nom.startswith('LE DESSIN') or et['dumps'] >= 2:
            return
        et['dumps'] += 1
        desc, chaine = ctx.Rcx, ctx.R8
        od = d.read(desc, 0x50)
        if len(od) < 0x50:
            d.dire('  descripteur illisible a 0x%X' % desc)
            return
        f = lambda o: struct.unpack_from('<f', od, o)[0]
        u = lambda o: struct.unpack_from('<I', od, o)[0]
        style = struct.unpack_from('<Q', od, 0x48)[0]
        txt = d.read(chaine, 24)
        d.dire('  --- ce que le dessin recoit ---')
        d.dire('    chaine   0x%X = %r' % (chaine, txt.partition(bytes(1))[0]))
        d.dire('    couleur  +0x08 = 0x%08X   +0x0C = 0x%08X' % (u(8), u(0x0C)))
        d.dire('    modes    +0x24 = %d   +0x2C = %d' % (u(0x24), u(0x2C)))
        d.dire('    x1 y1    %g %g' % (f(0x34), f(0x38)))
        d.dire('    x2 y2    %g %g' % (f(0x3C), f(0x40)))
        d.dire('    style    0x%X' % style)
        os_ = d.read(style, 0x40)
        if len(os_) >= 0x40:
            g = lambda o: struct.unpack_from('<f', os_, o)[0]
            d.dire('      mode +0x00 = %d   police +0x08 = 0x%X'
                   % (struct.unpack_from('<I', os_, 0)[0],
                      struct.unpack_from('<Q', os_, 8)[0]))
            d.dire('      metriques +0x14 = %g   +0x18 = %g' % (g(0x14), g(0x18)))
            d.dire('      echelles  +0x24 = %g  +0x28 = %g  +0x2C = %g  +0x30 = %g'
                   % (g(0x24), g(0x28), g(0x2C), g(0x30)))
        else:
            d.dire('      style illisible')

    def tic(d, t):
        if et['poses']:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['poses'] = True
        for rva, nom in JALONS:
            bp = instrument.PointArret(nom, b + GREFFE + rva, max_coups=200000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  six jalons poses dans DESSINER (t=%.1f s)' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)

    print('2/2  le jeu se lance AVEC le dessin -- il va probablement planter.')
    print()
    print('  Allez a STAGE SELECT et amenez le curseur sur la case de DURAL.')
    print('  C est la que le dessin s execute pour la premiere fois.')
    print('  journal : %s' % journal)
    print()
    dbg.run(EXE, JEU, secondes, ())
    fichier.close()

    print()
    print('=' * 70)
    print('%-46s %s' % ('jalon', 'passages'))
    dernier = None
    for rva, nom in JALONS:
        n = et['atteints'].get(nom, 0)
        if n:
            dernier = nom
        print('  %-44s %s' % (nom, n if n else 'JAMAIS ATTEINT'))
    print()
    dessin = et['atteints'].get(JALONS[4][1], 0)
    if not dessin:
        print('VERDICT : le DESSIN n a jamais ete atteint. Soit le curseur n a')
        print('  pas touche la case de Dural, soit la garde de l anneau ferme,')
        print('  soit l entree B (0x1801747C0) n est pas jouee sur cet ecran.')
    else:
        print('VERDICT : le dessin a bien ete APPELE %d fois.' % dessin)
        print('  Rien a l ecran : la reponse est dans le vidage')
        print('  « ce que le dessin recoit » du journal.')
        print('    . echelles a 0 ou NaN    -> le style n est pas initialise.')
        print('      Le site d origine appelle 0x180187AA0 puis')
        print('      0x180187CB0(2) AVANT de poser le mode ; je les ai sautes.')
        print('    . coordonnees aberrantes -> le texte tombe hors ecran ;')
        print('    . tout est bon           -> le dessin part, mais quelque')
        print('      chose le recouvre, ou il faut le faire en phase de RENDU')
        print('      et non dans l update.')
    print()
    print('  ATTENTION : le jalon « apres » est aussi celui ou saute la garde ;')
    print('  il ne prouve rien a lui seul.')
    print('  Le journal porte l EXCEPTION eventuelle, avec son adresse.')
    print('  Pour retrouver une build jouable : variantes.cmd')
    print('=' * 70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
