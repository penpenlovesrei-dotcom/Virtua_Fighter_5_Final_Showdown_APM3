#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""LA SONDE DE PLANTAGE : ou le jeu tombe, et dans QUELLE de nos structures.

POURQUOI CELLE-CI

Frederic, 2026-09-10, apres l'ajout des dix-neuf decors de VF5 R : « nombreux
plantages ». `instrument.py` sait deja rapporter une exception -- code, adresse,
module -- mais pas ce qui compte ici : **est-ce qu'on tombe dans une structure
que nous avons posee**, et **quel decor etait demande** au moment ou ca tombe.

Ce que cette sonde ajoute a `instrument.py run` :

  . la carte des SECTIONS de la DLL, rebasee a l'execution. L'adresse fautive
    est situee dedans, et si elle tombe dans `.decors` ou `.greffe` on dit a
    quel OFFSET de quelle table -- descripteurs, codes, grille, objsets et
    taches, effets a3d, effets mur, charges de mur, chaines ;
  . la DESASSEMBLE autour de RIP (capstone), pour lire l'instruction fautive
    au lieu de la deviner ;
  . l'adresse LUE ou ECRITE d'une violation d'acces, situee elle aussi ;
  . un point d'arret sur `0x18018EF87` -- le SEUL site qui pose le descripteur
    de decor -- qui journalise l'indice demande. Le dernier indice vu avant le
    plantage nomme le decor fautif, et c'est la question qu'on se pose ;
  . un point d'arret sur `0x18006F380` (le createur de taches d'effet) et sur
    `0x1800843A0` (`TaskEffectWall::setStage`), pour savoir jusqu'ou l'etat 3
    est alle ;
  . le journal est ecrit AU FIL DE L'EAU : un debogueur qui se bloque emporte
    tout bilan ecrit a la fin.

CE QU'ELLE NE FAIT PAS

Elle ne navigue pas toute seule. Le plantage est provoque par ce que Frederic
fait a l'ecran ; la sonde regarde. Le scenario d'entrees est donc VIDE, et le
clavier reste a vous.

    py -3 tools/pister_plantage.py
    py -3 tools/pister_plantage.py --secondes 300
    py -3 tools/pister_plantage.py --journal analysis/plantage_2.txt

Lanceur : tools\plantage_5r.cmd
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                              # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
EXE = os.path.join(JEU, 'vfes.exe')
DLL = os.path.join(JEU, MOTEUR)
SCENARIO_ACTIF = os.path.join(JEU, 'apm_entrees.txt')
SCENARIO = """# ecrit par tools/pister_plantage.py -- AUCUNE entree : c est vous
# qui jouez, la sonde ne fait que regarder.
front   = 10
journal = 0
clavier = 1
manette = 1
0       rien
"""

BASE_PREF = 0x180000000
# Les trois sites qui disent OU on en est.
JALONS = (
    (0x18018EF87, 'TaskStage : pose du descripteur', 'edx'),
    (0x18006F380, 'etat 3 : creation des taches d effet', None),
    (0x1800843A0, 'TaskEffectWall::setStage', 'edx'),
    (0x1800706B0, 'TaskEffectAuth3D::setStage', 'edx'),
    (0x1800848C0, 'TaskEffectWall : pose des morceaux', None),
)

# LES SEPT PORTES DE L'ETAT 3, relevees dans `analysis/disasm_decors_B.txt` et
# deja utilisees par `pister_import.py`. Chaque adresse n'est atteinte que si la
# precedente a passe : la plus haute atteinte designe celle qui bloque. Elles
# sont posees a UN SEUL COUP -- l'etat 3 est scrute a chaque trame, et les
# rearmer ferait ramper le jeu sous debogueur.
PORTES = (
    (0x18018F74A, 'entree de l etat 3'),
    (0x18018F760, 'porte 1 : l OBJSET est pret (geometrie + textures)'),
    (0x18018F76D, 'porte 2 : l ECLAIRAGE est pret (ibl + light_param)'),
    (0x18018F77A, 'porte 3 : la COLLISION est prete'),
    (0x18018F78E, 'porte 4 : l auth_3d du DECOR est pret'),
    (0x18018F7A2, 'porte 5 : le drapeau de scene est retombe'),
    (0x18018F7B7, 'porte 6 : l auth_3d des EFFETS est pret'),
    (0x18018F7C4, 'porte 7 : les SONS d ambiance sont prets'),
)


def nom_du_decor(i):
    """« 47 (rv5, la version VF5 R de riv) » plutot que « 47 »."""
    try:
        import patch_moteur as P
        import variantes_5r
    except Exception:
        return str(i)
    if 0 <= i < len(P.DECOR_NOMS):
        return '%d (%s)' % (i, P.DECOR_NOMS[i])
    for modele, code, indice, _ in variantes_5r.DECORS_5R:
        if indice == i:
            return '%d (%s, la version VF5 R de %s)' % (i, code, modele)
    if i == 41:
        return '41 (ALEATOIRE)'
    return '%d (INCONNU -- hors table)' % i


def carte_decors():
    """Les tables que `--decors-table` a deplacees, avec leur offset dans
    `.decors`. On refait le calcul du patcheur plutot que de le supposer."""
    import patch_moteur as P
    import variantes_5r
    n = max(e[2] for e in variantes_5r.DECORS_5R) + 1
    neufs = n - P.DECORS_TABLE_N
    off_codes = (n * P.DECORS_TABLE_PAS + 0xF) & ~0xF
    off_grille = (off_codes + n * P.DECORS_CODES_PAS + 0xF) & ~0xF
    tg = P.GRILLE_TABLE_N * P.GRILLE_TABLE_PAS
    off_objsets = (off_grille + tg + 0xF) & ~0xF
    off_a3d = (off_objsets + n * P.OBJSETS_TABLE_PAS + 0xF) & ~0xF
    off_mur = (off_a3d + (P.EFFETS_A3D_N + neufs + 1) * P.EFFETS_A3D_PAS
               + 0xF) & ~0xF
    off_uids = (off_mur + (P.EFFETS_MUR_N + neufs + 1) * P.EFFETS_MUR_PAS
                + 0xF) & ~0xF
    off_charges = (off_uids + neufs * P.EFFETS_UIDS_MAX * 4 + 0xF) & ~0xF
    return [(0, 'descripteurs (%d x 0x%X)' % (n, P.DECORS_TABLE_PAS)),
            (off_codes, 'codes'),
            (off_grille, 'grille'),
            (off_objsets, 'objsets + taches d effet'),
            (off_a3d, 'effets a3d'),
            (off_mur, 'effets mur'),
            (off_uids, 'uid des decors neufs'),
            (off_charges, 'charges de mur, puis les chaines')]


def sections(chemin):
    import pefile
    pe = pefile.PE(chemin, fast_load=True)
    out = []
    for s in pe.sections:
        n = s.Name.rstrip(b'\x00').decode('latin-1')
        out.append((s.VirtualAddress,
                    s.VirtualAddress + max(s.Misc_VirtualSize,
                                           s.SizeOfRawData), n))
    return out


def main():
    argv = sys.argv[1:]
    secondes = int(argv[argv.index('--secondes') + 1]) if '--secondes' in argv \
        else 300
    journal = (argv[argv.index('--journal') + 1] if '--journal' in argv
               else os.path.join(RACINE, 'analysis', 'pister_plantage.txt'))
    if not os.path.isabs(journal):
        journal = os.path.join(RACINE, journal)

    secs = sections(DLL)
    try:
        tables = carte_decors()
    except Exception as e:
        tables = []
        print('  (carte de .decors indisponible : %s)' % e)

    fichier = open(journal, 'w', encoding='utf-8', newline='\n')
    dbg = instrument.Debugger()
    _dire = dbg.dire

    def dire(txt):
        _dire(txt)
        fichier.write(txt + '\n')
        fichier.flush()                 # AU FIL DE L EAU, toujours

    dbg.dire = dire
    dbg.bp_max = 4000
    etat = {'dernier_decor': None, 'decors': [], 'plantages': 0, 'portes': []}

    def base_moteur():
        return dbg.base_de(MOTEUR)

    def situer(adresse):
        """Ou tombe cette adresse : module, section, et notre table."""
        mod, off = dbg.module_of(adresse)
        b = base_moteur()
        if not b or not (b <= adresse < b + 0x2000000):
            return '%s+0x%X' % (mod, off)
        rva = adresse - b
        for a, z, n in secs:
            if a <= rva < z:
                txt = '%s!%s+0x%X (VA preferee 0x%X)' % (mod, n, rva - a,
                                                         BASE_PREF + rva)
                if n == '.decors' and tables:
                    d = rva - a
                    quoi = None
                    for o, nom in tables:
                        if d >= o:
                            quoi = (o, nom)
                    if quoi:
                        txt += '\n        -> dans NOTRE table « %s », +0x%X' \
                               % (quoi[1], d - quoi[0])
                return txt
        return '%s+0x%X (hors section)' % (mod, rva)

    def desassembler(adresse, avant=16, apres=32):
        try:
            import capstone
        except ImportError:
            return
        b = base_moteur()
        octets = dbg.read(adresse - avant, avant + apres)
        if not octets:
            return
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        dire('      --- code autour de RIP ---')
        for ins in md.disasm(octets[avant:], adresse):
            marque = '>>>' if ins.address == adresse else '   '
            va = ins.address - b + BASE_PREF if b else ins.address
            dire('      %s 0x%X  %s %s' % (marque, va, ins.mnemonic,
                                           ins.op_str))
            if ins.address > adresse + 24:
                break

    # --- l'exception : on enrichit celle d'instrument.py -------------------
    _exception = dbg.exception

    def exception(ev, tid):
        r = ev.u.Exception.ExceptionRecord
        c = r.ExceptionCode & 0xFFFFFFFF
        interessante = c not in (0x80000003, 0x80000004, 0x406D1388)
        status = _exception(ev, tid)
        if interessante:
            etat['plantages'] += 1
            a = r.ExceptionAddress or 0
            dire('      ou      : %s' % situer(a))
            if c == 0xC0000005 and r.NumberParameters >= 2:
                quoi = {0: 'LECTURE', 1: 'ECRITURE', 8: 'EXECUTION'}.get(
                    r.ExceptionInformation[0], '?')
                cible = r.ExceptionInformation[1] & 0xFFFFFFFFFFFFFFFF
                dire('      acces   : %s de 0x%016X' % (quoi, cible))
                dire('      cible   : %s' % situer(cible))
            ctx = dbg.contexte(tid)
            if ctx is not None:
                dire('        %s' % dbg.registres(ctx))
                desassembler(ctx.Rip)
            if etat['decors']:
                dire('      dernier decor demande : %s'
                     % nom_du_decor(etat['decors'][-1]))
                dire('      les precedents       : %s'
                     % ' '.join(str(x) for x in etat['decors'][-8:]))
            else:
                dire('      AUCUN decor demande avant ce plantage.')
            if etat['portes']:
                dire('      derniere porte franchie : %s' % etat['portes'][-1])
        return status

    dbg.exception = exception

    # --- les jalons ---------------------------------------------------------
    def sur_bp(d, bp, ctx, tid):
        if bp.nom.startswith('TaskStage'):
            idx = ctx.Rdx & 0xFFFFFFFF
            etat['decors'].append(idx)
            etat['dernier_decor'] = idx
            etat['portes'] = []
            d.dire('  >>> DECOR DEMANDE : %s' % nom_du_decor(idx))
        elif bp.nom.startswith('TaskEffectWall::setStage'):
            d.dire('  >>> mur : setStage(%s)'
                   % nom_du_decor(ctx.Rdx & 0xFFFFFFFF))
        elif bp.nom.startswith('TaskEffectAuth3D'):
            d.dire('  >>> animations : setStage(%s)'
                   % nom_du_decor(ctx.Rdx & 0xFFFFFFFF))
        elif bp.nom.startswith('TaskEffectWall : pose'):
            d.dire('  >>> mur : pose des morceaux (rdx=0x%X rcx=0x%X)'
                   % (ctx.Rdx, ctx.Rcx))
        elif bp.nom.startswith('porte') or bp.nom.startswith('entree'):
            etat['portes'].append(bp.nom)
            d.dire('  >>> %s' % bp.nom)

    dbg.on_bp = sur_bp
    # Les points d'arret sont DIFFERES : l'adresse n'est connue qu'une fois la
    # DLL chargee et rebasee. `instrument.armer_en_attente` est le crochet
    # appele a chaque module charge.
    reste = list(JALONS)
    reste_portes = list(PORTES)

    def apres_module():
        b = dbg.base_de(MOTEUR)
        if not b:
            return
        for item in list(reste):
            va, nom, _ = item
            bp = instrument.PointArret('%s @0x%X' % (nom, va),
                                       b + (va - BASE_PREF))
            bp.silencieux = True
            dbg.bps.append(bp)
            dbg.armer_logiciel(bp)
            reste.remove(item)
        # les sept portes : UN SEUL COUP chacune, sinon le jeu rampe
        for va, nom in reste_portes[:]:
            bp = instrument.PointArret(nom, b + (va - BASE_PREF), max_coups=1)
            bp.silencieux = True
            dbg.bps.append(bp)
            dbg.armer_logiciel(bp)
            reste_portes.remove((va, nom))

    dbg.armer_en_attente = apres_module

    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)

    dire('=' * 74)
    dire('SONDE DE PLANTAGE -- %d s, le clavier est a vous' % secondes)
    dire('=' * 74)
    dire('sections de %s (RVA) :' % MOTEUR)
    for a, z, n in secs:
        dire('   %-10s 0x%08X .. 0x%08X   (VA preferee 0x%X)'
             % (n, a, z, BASE_PREF + a))
    if tables:
        dire('carte de .decors :')
        for o, n in tables:
            dire('   +0x%06X  %s' % (o, n))
    dire('')
    print()
    print('JOUEZ NORMALEMENT, et faites planter le jeu.')
    print('  Le journal s ecrit au fil de l eau : %s' % journal)
    print('  Le jeu se ferme seul au bout de %d s.' % secondes)
    print()
    dbg.run(EXE, JEU, secondes, ())
    dire('')
    dire('-' * 74)
    dire('%d exception(s) retenue(s).' % etat['plantages'])
    if etat['decors']:
        dire('decors demandes, dans l ordre :')
        for x in etat['decors']:
            dire('   %s' % nom_du_decor(x))
    else:
        dire('AUCUN decor demande : le plantage est avant tout chargement de '
             'decor.')
    fichier.close()
    print()
    print('Journal ecrit : %s' % journal)
    return 0


if __name__ == '__main__':
    sys.exit(main())
