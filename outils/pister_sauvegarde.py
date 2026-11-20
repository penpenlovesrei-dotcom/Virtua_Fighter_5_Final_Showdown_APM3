#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""QUI ECRIT LA SAUVEGARDE, ET QUI L'EFFACE. La sonde qui manquait.

POURQUOI ELLE EXISTE (2026-10-05). Frederic, apres trois correctifs rates sur
la sauvegarde du personnage : « il y a un probleme avec ta methode. As tu une
sonde pour surveiller le comportement du jeu lors de la sauvegarde du
personnage modifie et lors du chargement de la sauvegarde au demarrage ? »

Non, je n'en avais pas. J'ai lu du desassemblage par fragments et parie trois
fois sur la structure que je venais de trouver. Celle-ci regarde le jeu FAIRE.

CE QU'ELLE SURVEILLE, et pourquoi ces deux adresses precises.

    LA TABLE DES PERSONNAGES   [0x180752148] + 0x28, 150 entrees de 0x80
                               (0x1801C5A80 ; borne a 150 par `cmp rbx,0x96`)
    L ENREGISTREMENT DE TRAVAIL [0x18070FB10] + 0x18 + joueur*0x5A0
                               (0x1801C5AB0 ; parties equipees en +0x262)

DEUX CORRECTIONS DE METHODE, le 2026-10-05, apres la premiere redaction.

1. ON SURVEILLE D'ABORD L'EMPLACEMENT DU POINTEUR, pas seulement sa cible.
   La premiere version attendait que les deux pointeurs soient non nuls, en
   sondant toutes les 100 ms, puis armait sur la cible. Un effacement qui suit
   l'allocation de quelques microsecondes -- exactement le cas qu'on soupconne,
   puisque notre restauration a l'air defaite aussitot -- passait entre deux
   sondages. Or les deux emplacements de pointeur sont des globales ALIGNEES
   sur huit (0x...148 et 0x...B10) : on peut les surveiller en ecriture. Des
   que le moteur y range son objet, le meme rappel arme la surveillance de la
   cible, a l'instruction qui suit l'allocation, et desarme la surveillance du
   pointeur -- le registre est rendu. Couverture complete, sans trou.

2. NOTRE PROPRE SAUVEGARDE EST COUPEE. Le apm.dll de substitution restaure la
   table au demarrage ; ses memcpy ecrivent donc aux memes adresses que le
   moteur, et les deux relevés se melangeaient. On ne mesure pas un moteur en
   gardant la main dessus : la sonde ecrit « sauvegarde = 0 » dans la copie de
   travail d'apm_entrees.txt avant de lancer, et la remet comme elle etait a la
   fin. `--avec-notre-sauvegarde` garde notre bloc actif, pour la passe
   suivante -- celle qui montrera si notre restauration est defaite, et par qui.

CE QU'ELLE COUTE : rien. Un point d'arret materiel n'ecrit aucun `0xCC` et ne
leve d'exception que lorsqu'on ECRIT a l'adresse surveillee. Le jeu tourne a
sa vitesse normale -- ce qui compte, puisqu'il faut naviguer jusqu'a Customize
et sauvegarder a la main.

CE QU'ON OBTIENT, pour chaque ecriture :

    ECRITURE sur la TABLE DES PERSONNAGES (acces 3)
      qui ecrit : ...dll!.text+0x1D0B21 (VA preferee 0x1801D0B21)
      entrees occupees : 0 -> 1
      --- code a partir de RIP ---

L'adresse a la base PREFEREE est la seule qui se retrouve dans un
desassemblage, et le compte d'entrees occupees dit si l'ecriture GARNIT ou
EFFACE. C'est tout ce qu'il manquait.

Usage :
    py -3 tools/pister_sauvegarde.py [--secondes 900]
    py -3 tools/pister_sauvegarde.py --avec-notre-sauvegarde

Lanceur : tools\sauvegarde.cmd
"""
import os
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                            # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
EXE = os.path.join(JEU, 'vfes.exe')
DLL = os.path.join(JEU, MOTEUR)
SCENARIO = os.path.join(JEU, 'apm_entrees.txt')
BASE_PREF = 0x180000000
JOURNAL = os.path.join(RACINE, 'analysis', 'pister_sauvegarde.txt')

# Les deux emplacements de pointeur, a la base preferee, et ce qu'il faut
# ajouter au pointeur qu'ils portent.
PERSO_PTR, PERSO_TETE, PERSO_PAS, PERSO_MAX = 0x180752148, 0x28, 0x80, 150
TRAVAIL_PTR, TRAVAIL_TETE, TRAVAIL_PARTS = 0x18070FB10, 0x18, 0x262


def sections(chemin):
    import pefile
    pe = pefile.PE(chemin, fast_load=True)
    return [(s.VirtualAddress,
             s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData),
             s.Name.rstrip(b'\x00').decode('latin-1')) for s in pe.sections]


def regler_sauvegarde(valeur):
    """Met « sauvegarde = <valeur> » dans la copie de travail du scenario.

    Rend l'ancienne valeur, ou None si la ligne etait absente (le stub prend
    alors son defaut, qui est 1). La copie de travail est reecrite a chaque
    generation du stub : on ne touche pas au maitre tools/apm_entrees.txt.
    """
    if not os.path.exists(SCENARIO):
        return None
    with open(SCENARIO, 'r', encoding='latin-1', newline='') as fp:
        lignes = fp.read().split('\n')
    ancien, trouve = None, False
    for i, l in enumerate(lignes):
        nu = l.strip()
        if nu.startswith('#'):
            continue
        if nu.replace(' ', '').startswith('sauvegarde='):
            ancien = nu.split('=', 1)[1].split('#')[0].strip()
            lignes[i] = 'sauvegarde = %d' % valeur
            trouve = True
            break
    if not trouve:
        lignes.append('sauvegarde = %d' % valeur)
    with open(SCENARIO, 'w', encoding='latin-1', newline='') as fp:
        fp.write('\n'.join(lignes))
    return ancien


def main():
    argv = sys.argv[1:]
    secondes = int(argv[argv.index('--secondes') + 1]) \
        if '--secondes' in argv else 900
    notre = '--avec-notre-sauvegarde' in argv

    secs = sections(DLL)
    if os.path.exists(JOURNAL) and os.path.getsize(JOURNAL):
        vieux = '%s.%s.txt' % (JOURNAL[:-4],
                               time.strftime('%Y%m%d-%H%M%S',
                                             time.localtime(
                                                 os.path.getmtime(JOURNAL))))
        try:
            os.replace(JOURNAL, vieux)
            print('passe precedente archivee : %s'
                  % os.path.relpath(vieux, RACINE))
        except OSError:
            pass
    fichier = open(JOURNAL, 'w', encoding='utf-8', newline='\n')
    dbg = instrument.Debugger()
    _dire = dbg.dire

    def dire(txt):
        _dire(txt)
        fichier.write(txt + '\n')
        fichier.flush()                   # AU FIL DE L EAU, toujours

    dbg.dire = dire
    dbg.dr_max = 400                      # on veut TOUS les acces, pas trois
    dbg.dr_auto_desarmer = False
    et = {'ptr_armes': False, 'perso': None, 'travail': None, 'occ': None,
          'm_ptr': {}, 'cible': {}}

    def situer(adresse):
        mod, off = dbg.module_of(adresse)
        b = dbg.base_de(MOTEUR)
        if not b or not (b <= adresse < b + 0x2000000):
            return '%s+0x%X' % (mod, off)
        rva = adresse - b
        for a, z, n in secs:
            if a <= rva < z:
                return '%s!%s+0x%X (VA preferee 0x%X)' % (
                    mod, n, rva - a, BASE_PREF + rva)
        return '%s+0x%X (hors section)' % (mod, rva)

    def desassembler(adresse):
        try:
            import capstone
        except ImportError:
            return
        o = dbg.read(adresse - 24, 56)
        if not o:
            return
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        b = dbg.base_de(MOTEUR) or 0
        dire('      --- code a partir de RIP ---')
        for ins in md.disasm(o[24:], adresse):
            dire('      %s 0x%X  %s %s'
                 % ('>>>' if ins.address == adresse else '   ',
                    BASE_PREF + (ins.address - b), ins.mnemonic, ins.op_str))
            if ins.address > adresse + 16:
                break

    def reelle(va):
        """L'adresse d'execution d'une VA a la base preferee."""
        b = dbg.base_de(MOTEUR)
        return None if not b else b + (va - BASE_PREF)

    def pointeur(va):
        a = reelle(va)
        if a is None:
            return None
        d = dbg.read(a, 8)
        if not d:
            return None
        return int.from_bytes(d, 'little') or None

    def occupees():
        """Combien d'entrees de la table portent un premier octet non nul.

        C'est LE test du moteur lui-meme : `cmp byte [rcx+rbx+0x28], 0` en
        0x1801C5A57 et `cmp byte [rcx+rbx+0x28C], 0` dans le dessin.
        """
        p = et['perso']
        if not p:
            return -1
        d = dbg.read(p, PERSO_PAS * PERSO_MAX)
        if not d:
            return -1
        return sum(1 for i in range(PERSO_MAX) if d[i * PERSO_PAS])

    def armer_cible(quoi):
        """Arme la surveillance de la CIBLE, une fois le pointeur connu.

        L'ALIGNEMENT EST IMPOSE PAR LE x86 : une plage de huit octets doit
        etre alignee sur huit. La tete de la table l'est (pointeur + 0x28) ;
        le mot des parties equipees, lui, est en +0x262, aligne sur deux
        seulement -- d'ou une surveillance de DEUX octets, pas huit.
        """
        if et['cible'].get(quoi):
            return
        if quoi == 'perso':
            p = pointeur(PERSO_PTR)
            if not p:
                return
            et['perso'] = p + PERSO_TETE
            et['occ'] = occupees()
            dire('     table des personnages : 0x%X  (%d entrees occupees)'
                 % (et['perso'], et['occ']))
            m = dbg.armer_materiel(et['perso'], 8, 'w',
                                   nom='perso (tete de table)')
        else:
            p = pointeur(TRAVAIL_PTR)
            if not p:
                return
            et['travail'] = p + TRAVAIL_TETE
            dire('     enregistrement de travail : 0x%X' % et['travail'])
            m = dbg.armer_materiel(et['travail'] + TRAVAIL_PARTS, 2, 'w',
                                   nom='travail (1re partie equipee)')
        if m:
            et['cible'][quoi] = m
            # Le registre du POINTEUR est rendu : il a fait son office.
            mp = et['m_ptr'].pop(quoi, None)
            if mp:
                dbg.desarmer_materiel(mp)
                dire('     (surveillance du pointeur %s rendue)' % quoi)

    def sur_dr(d, m, ctx, tid):
        nom = m.nom or ''
        # --- un EMPLACEMENT DE POINTEUR vient d'etre ecrit -----------------
        if nom.startswith('ptr '):
            quoi = 'perso' if 'perso' in nom else 'travail'
            v = d.read(m.adresse, 8)
            val = int.from_bytes(v, 'little') if v else 0
            dire('')
            dire('  LE POINTEUR %s est pose : 0x%X' % (quoi, val))
            dire('      par : %s' % situer(ctx.Rip))
            if val:
                armer_cible(quoi)
            return
        # --- une CIBLE vient d'etre ecrite --------------------------------
        quoi = 'TABLE DES PERSONNAGES' if 'perso' in nom else \
               'ENREGISTREMENT DE TRAVAIL'
        n = occupees()
        dire('')
        dire('  ECRITURE sur la %s (acces %d)' % (quoi, m.coups))
        dire('      qui ecrit : %s' % situer(ctx.Rip))
        dire('      (le RIP materiel est l instruction SUIVANTE)')
        if n >= 0:
            dire('      entrees occupees : %s -> %d'
                 % ('?' if et['occ'] is None else et['occ'], n))
            et['occ'] = n
        v = d.read(m.adresse, m.taille)
        if v:
            dire('      valeur maintenant : %s' % v.hex())
        desassembler(ctx.Rip)

    dbg.on_dr = sur_dr

    def tic(d, t):
        if not et['ptr_armes']:
            if reelle(PERSO_PTR) is None:
                return                       # le moteur n'est pas charge
            # On surveille les DEUX EMPLACEMENTS de pointeur : c'est la seule
            # facon d'etre la a l'instruction qui suit l'allocation.
            for quoi, va in (('perso', PERSO_PTR), ('travail', TRAVAIL_PTR)):
                if pointeur(va):
                    # deja pose (on arrive tard) : on va droit a la cible
                    armer_cible(quoi)
                else:
                    m = d.armer_materiel(reelle(va), 8, 'w',
                                         nom='ptr %s' % quoi)
                    if m:
                        et['m_ptr'][quoi] = m
            et['ptr_armes'] = True
            dire('')
            dire('  ALLEZ SAUVEGARDER UN PERSONNAGE. Tout ce qui ecrit ces')
            dire('  adresses sera nomme ici, avec le compte avant/apres.')
            dire('')
            return
        # Filet : si un pointeur a ete pose sans que la surveillance le voie
        # (thread cree apres la pose du registre, par exemple), on rattrape.
        for quoi in ('perso', 'travail'):
            if quoi not in et['cible'] and pointeur(
                    PERSO_PTR if quoi == 'perso' else TRAVAIL_PTR):
                armer_cible(quoi)

    dbg.tic = tic

    ancien = None
    if not notre:
        ancien = regler_sauvegarde(0)
    dire('=' * 74)
    dire('SONDE DE SAUVEGARDE -- %d s, le clavier et la manette vous restent'
         % secondes)
    dire('=' * 74)
    dire('notre bloc de sauvegarde : %s (ancienne valeur du scenario : %s)'
         % ('ACTIF' if notre else 'COUPE', ancien))
    dire('sections de %s (RVA) :' % MOTEUR)
    for a, z, n in secs:
        dire('   %-10s 0x%08X .. 0x%08X   (VA preferee 0x%X)'
             % (n, a, z, BASE_PREF + a))
    dire('')
    print()
    print('JOUEZ : TERMINAL > Customize, habillez un personnage, ENREGISTREZ.')
    print('  Journal au fil de l eau : %s' % os.path.relpath(JOURNAL, RACINE))
    print('  Le jeu se ferme seul au bout de %d s.' % secondes)
    print()
    try:
        dbg.run(EXE, JEU, secondes, ())
    finally:
        if not notre:
            # `ancien` est None quand la ligne etait absente : le defaut du
            # stub est 1, c'est donc a 1 qu'on remet, pas a rien.
            regler_sauvegarde(int(ancien) if ancien and ancien.isdigit() else 1)
        dire('')
        dire('-' * 74)
        dire('entrees occupees a la fin : %s' % et['occ'])
        fichier.close()
    print()
    print('journal : %s' % os.path.relpath(JOURNAL, RACINE))
    return 0


if __name__ == '__main__':
    sys.exit(main())
