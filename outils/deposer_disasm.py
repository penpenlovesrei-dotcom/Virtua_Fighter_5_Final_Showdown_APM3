#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEPOSE LE DESASSEMBLAGE DES FONCTIONS LUES, des deux cotes.

Frederic, 2026-10-04 : « tout ce que tu decompiles de la version xbox 360 ou
APM3 est consigne quelque part ? »

NON, ET CA S'ETAIT PERDU. Les chantiers de septembre deposaient leur lecture
(`analysis/decomp_*.c`, douze fichiers du 10/09 pour les decors ;
`analysis/disasm_*.txt`, quinze fichiers des 01 et 07/09). Les seances
d'octobre -- les curseurs du TERMINAL, la grille Xbox 360, le chargeur
d'objets -- n'ont laisse que des EXTRAITS cites dans `REPRISE.md`. Un extrait
cite prouve ce qu'on en dit ; il ne permet pas de relire la fonction, ni de
voir ce qu'on n'avait pas remarque.

Cet outil rend le depot systematique et REPRODUCTIBLE : la liste des fonctions
lues vit ici, en clair, et une seule commande regenere tout le dossier
`analysis/disasm/` depuis les binaires. Rien n'est recopie a la main -- c'est
la regle du chantier, et recopier a l'oeil coute une ligne sur quatre.

Les deux cotes vont dans le meme dossier, parce que la methode qui marche les
met EN REGARD : le consommateur vivant cote borne, le producteur cote console.

Usage :
    py -3 tools/deposer_disasm.py            tout redeposer
    py -3 tools/deposer_disasm.py --liste    dire ce qui serait depose
"""
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
SORTIE = os.path.join(RACINE, 'analysis', 'disasm')

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')

# (fichier, va, octets, a quoi ca sert -- et ou c'est raconte)
BORNE = [
    ('selitem_update', 0x1801C7440, 0x220,
     "TaskSelItemMenu::update. Appelle le consommateur en 0x1801C7605 et le "
     "repartiteur en 0x1801C7639 -- c'est ce dernier site que "
     "`--selitem-grille` detourne. REPRISE (98)."),
    ('selitem_consommateur', 0x1801C7B50, 0x120,
     "LE CONSOMMATEUR DE MESSAGE MORT de « select item », et la piece "
     "maitresse : en 0x1801C7B83 il fait d'un index ABSOLU le couple "
     "(position +0x9D0, defilement +0x9C8) -- ecretage au total et pas de "
     "huit compris. Types 9 et 10, jamais postes. Et 0x1801C7BF4 recalcule "
     "+0x58 DEPUIS la grille : le curseur du repartiteur en est l'esclave. "
     "REPRISE (97)."),
    ('selitem_dessin', 0x1801C8110, 0x160,
     "Le dessin de la grille. 0x1801C8139 lit table[+0x9D0 + +0x9C8], le "
     "jumeau exact de 0x82231BA0 cote console. REPRISE (96)."),
    ('selpart_curseur', 0x1801C7D00, 0x260,
     "Le curseur de « select part ». Repartiteur en tete (0x1801C7D34), puis "
     "le deplacement par MESSAGE DE TYPE 7 OU 8 (0x1801C7D95), jamais poste. "
     "`cmp rcx, 4 ; ja` en 0x1801C7D9F dit CINQ categories, pas 24. Le "
     "commutateur 0x1801C7E05 etait intact. C'est 0x1801C7D63 que "
     "`--selpart-curseur` detourne. REPRISE (99)."),
    ('selpart_dessin', 0x1801CA040, 0x3D0,
     "Le dessin de « select part ». 0x1801CA140 lit +0xEE0, et le cadre est "
     "place depuis une TABLE de coordonnees par categorie, pas par un pas : "
     "c'est pourquoi la direction n'est pas deductible. REPRISE (99)."),
    ('resolveur_objset', 0x180217E70, 0x220,
     "Le resolveur de nom d'objset, par dichotomie dans une table TRIEE de "
     "0x35E = 862 entrees basee en 0x18054BB30. 0x180218004 n'en est qu'un "
     "FRAGMENT. Les deux espions de `pister_item3d.py` sont a 0x180217E70 "
     "(l'adresse de retour) et 0x18021805E (le nom, dans rbx). REPRISE (102)."),
    ('chargeur_archive', 0x180038600, 0x280,
     "Le demandeur d'archive d'objets, mesure a la sonde : c'est lui qui "
     "demande `objset/akiitm` et `objset/akiitm_patch` (site d'appel "
     "0x180038803). Il construit le nom dans un std::string SUR LA PILE "
     "(bascule SSO a 0x10) -- d'ou l'absence de tout format `objset/%s` dans "
     "le binaire. REPRISE (103)."),
    ('aet_marqueurs_customize', 0x1801CBFE0, 0x100,
     "Ce qu'on avait pris pour le chargeur du modele au changement de "
     "categorie : c'est l'animation 2D de la fenetre. Il construit les "
     "marqueurs AET head_s/head_e/face_s/face_e/arm_s/arm_e/bust_s. "
     "REPRISE (100)."),
    ('itmeq_update', 0x1801C13B0, 0x380,
     "customize::ItmEqTask -- LA TACHE QUI EQUIPE UN OBJET (vtable "
     "0x180530D10, creneau 2, trouvee par le RTTI). Machine a cinq etats dans "
     "[this+0x58] : 4 est l'OISIF (il attend [this+0xd0]), puis 1 (le travail "
     "et les 24 objets), 2 (l'attente du chargeur puis la pose sur le modele) "
     "et 3. L'etat 3 ne contenait plus que le verrou +0x796 et le "
     "basculement ; mis en regard de la console il s'enchaine directement. "
     "REPRISE (105) et (114)."),
    ('itmeq_basculement', 0x1801CE400, 0x60,
     "0x1801CE400 -- CE QUI REND L'OBJET VISIBLE, et il n'equipe rien : il "
     "BASCULE le modele affiche. Il ecrit les deux creneaux ([rcx] et "
     "[rcx+1], complementaires) puis appelle deux fois 0x1801512B0 -- l'un "
     "VISIBLE, l'autre MASQUE. L'objet est pose sur le modele cache pendant "
     "les etats 1 et 2 ; ceci est ce qui le montre. Jumeau de 0x82236528 "
     "cote console. REPRISE (114)."),
    ('taskrobsingle_update', 0x180151CF0, 0x180,
     "TaskRobSingle::update (vtable 0x1803F8E68, creneau 2). L'un des cinq "
     "lecteurs de +0x796 : son etat 4 attend le drapeau pour passer a 5 "
     "(0x180151D3A). Cote console la meme fonction (0x82356840) attend a cet "
     "endroit un singleton de chargement, PAS un drapeau par joueur. C'est ce "
     "lecteur qui a permis de nommer le champ : il appartient aux "
     "COMBATTANTS, pas a Customize. REPRISE (114)."),
    ('publieur_joueur', 0x1801437E0, 0x120,
     "Le publieur de la structure joueur : il recopie les champs d'un objet "
     "source dans [0x180C3B6F0] + index*0xFA88. Il ecrit +0x790, +0x794 "
     "(0x180143859) et +0x797, et saute +0x795 et +0x796. La sonde l'a mesure "
     "a 2758 passages dans Customize, pour les DEUX joueurs : c'etait le "
     "candidat pour poser le drapeau, ecarte au profit du saut. Attention, "
     "0x180143720 qui le precede est un destructeur recursif, pas lui. "
     "REPRISE (114)."),
    ('itemmain_update', 0x1801C2EC0, 0x100,
     "customize::ItemMain::update -- le PILOTE de la tache d'equipement. "
     "Machine a 0x29 etats par table de saut. En 0x1801C2F14 il prend le "
     "singleton de ItmEqTask puis 0x1801C2F1C la demarre -- mais DEUX GARDES "
     "le precedent, 0x180187CC0(0x26B) et 0x180029D40(0x20B), et si l'une "
     "rend vrai on sort sans rien faire. Ce ne sont PAS des bouchons : elles "
     "consultent un gestionnaire et lisent [rax+0x48]. REPRISE (105)."),
    ('repartiteur_curseur', 0x1801BBBE0, 0x180,
     "Le repartiteur de curseur, celui que toutes les pages de "
     "personnalisation appellent. Il lit les comptes +0x224/+0x22C et les "
     "bouclages +0x228/+0x230, et deplace +0x58/+0x5C."),
]

X360 = [
    ('x360_grille_deplacement', 0x82230818, 180,
     "LE PRODUCTEUR, cote console : quatre blocs, un par direction, sur HUIT "
     "colonnes et une fenetre de 0x28 = quarante cases. Les QUATRE masques de "
     "direction du jeu (0x11000, 0x44000, 0x88000, 0x22000) n'apparaissent "
     "qu'ICI dans toute l'image -- mesure de (100). C'est de cette fonction "
     "que vient la geometrie de `--selitem-grille`. REPRISE (96)."),
    ('x360_page_update', 0x82231A50, 170,
     "La mise a jour de la page. 0x82231BA0 calcule table[+0x750 + +0x74C], "
     "le jumeau de notre 0x1801C8139, et 0x82231CB0 appelle la fonction de "
     "deplacement. Etiquetee « page part » parce qu'elle porte "
     "`p_part_plt_lt` : sa GEOMETRIE dit item. Un nom de planche n'identifie "
     "pas une page. REPRISE (96)."),
    ('x360_repartiteur', 0x82217B30, 120,
     "TaskCsMenu::update cote console -- LA PIERRE DE ROSETTE : curseur V/H "
     "en +0x4C/+0x50, comptes en +0x1B4/+0x1BC, bouclages en +0x1B8/+0x1C0. "
     "Voir `analysis/x360_fs.md`."),
    ('x360_itmeq_update', 0x82229750, 260,
     "customize::ItmEqTask::update cote CONSOLE (vtable 0x820113C0, creneau "
     "2), trouvee par `tools/x360_rtti.py`. LA PIECE QUI A TRANCHE : son etat "
     "3 enchaine 0x8222BCB8 -> 0x8221E4F8 -> 0x82236528 -> etat 4 -> "
     "0x82214520, SANS aucun test par joueur. APM3 a insere a cet endroit une "
     "frontiere d'etat et le verrou +0x796. L'attente du chargeur "
     "(0x82353D90 sur le singleton 0x827263D8) est en tete, comme cote borne. "
     "REPRISE (114)."),
    ('x360_taskrobsingle_update', 0x82356840, 110,
     "TaskRobSingle::update cote console (vtable 0x820B20F4, creneau 2). La "
     "ou la borne attend un drapeau par joueur (0x180151D3A), elle interroge "
     "le MEME singleton de chargement que la tache d'equipement. Confirme que "
     "+0x796 n'a pas d'homologue console. REPRISE (114)."),
]

# Le TROISIEME build : l'ELF x86 de la borne Lindbergh. Espace de noms
# `terminal::` au lieu de `customize::`, et les libelles de taches en clair.
LIND = [
    ('lind_itmeq_update', 0x0849893C, 170,
     "terminal::ItmEqTask::update sur la borne LINDBERGH (vtable 0x089AD9E8, "
     "creneau 3 -- GCC pose DEUX destructeurs, le numero de creneau ne se "
     "transpose pas). Elle n'a que QUATRE etats, l'oisif est le 3, et son "
     "etat 2 fait tout d'un trait : attente du chargeur (0x822F7AE sur "
     "0x8B7C030), pose sur le modele, puis le basculement EN LIGNE "
     "(0x08498B66 : [ebx]=1, [ebx+1]=0, deux appels a 0x822CDB2) et retour a "
     "l'oisif. Aucune condition par joueur ici non plus -- et c'est un "
     "binaire d'ARCADE, ce qui ecarte l'idee que le verrou d'APM3 serait une "
     "specificite arcade generale. REPRISE (114)."),
]


def ecrire(nom, titre, commentaire, lignes):
    chemin = os.path.join(SORTIE, nom + '.txt')
    with open(chemin, 'w', encoding='utf-8', newline='\n') as fp:
        fp.write('# %s\n' % titre)
        fp.write('#\n')
        for ligne in _plier(commentaire, 74):
            fp.write('# %s\n' % ligne)
        fp.write('#\n')
        fp.write('# Depose par tools/deposer_disasm.py -- NE PAS EDITER A LA '
                 'MAIN :\n')
        fp.write('# relancez l outil, il repart du binaire.\n')
        fp.write('\n')
        fp.write(lignes)
    return chemin


def _plier(texte, largeur):
    out, courant = [], ''
    for mot in texte.split():
        if len(courant) + len(mot) + 1 > largeur:
            out.append(courant)
            courant = mot
        else:
            courant = (courant + ' ' + mot).strip()
    if courant:
        out.append(courant)
    return out


def main():
    if '--liste' in sys.argv:
        for nom, va, n, _ in BORNE:
            print('  borne  %-28s 0x%X (%d octets)' % (nom, va, n))
        for nom, va, n, _ in X360:
            print('  x360   %-28s 0x%X (%d instructions)' % (nom, va, n))
        for nom, va, n, _ in LIND:
            print('  lind   %-28s 0x%X (%d instructions)' % (nom, va, n))
        return 0
    os.makedirs(SORTIE, exist_ok=True)
    faits = []
    for nom, va, n, note in BORNE:
        r = subprocess.run(
            [sys.executable, os.path.join(ICI, 'plage.py'),
             hex(va), hex(va + n), '--origine'],
            capture_output=True, text=True, cwd=RACINE)
        if r.returncode != 0 or not r.stdout.strip():
            print('ECHEC : %s (0x%X)' % (nom, va))
            print(r.stderr[:400])
            continue
        faits.append(ecrire(nom, 'APM3 (borne) 0x%X -- %d octets' % (va, n),
                            note, r.stdout))
    for nom, va, n, note in X360:
        r = subprocess.run(
            [sys.executable, os.path.join(ICI, 'x360_ppc.py'),
             'func', hex(va), '--max', str(n)],
            capture_output=True, text=True, cwd=RACINE)
        if r.returncode != 0 or not r.stdout.strip():
            print('ECHEC : %s (0x%X)' % (nom, va))
            print(r.stderr[:400])
            continue
        faits.append(ecrire(nom,
                            'Xbox 360 (console) 0x%X -- %d instructions'
                            % (va, n), note, r.stdout))
    for nom, va, n, note in LIND:
        r = subprocess.run(
            [sys.executable, os.path.join(ICI, 'lind_x86.py'),
             'func', hex(va), '--max', str(n)],
            capture_output=True, text=True, cwd=RACINE)
        if r.returncode != 0 or not r.stdout.strip():
            print('ECHEC : %s (0x%X)' % (nom, va))
            print(r.stderr[:400])
            continue
        faits.append(ecrire(nom,
                            'Lindbergh (arcade) 0x%X -- %d instructions'
                            % (va, n), note, r.stdout))

    index = os.path.join(SORTIE, 'README.md')
    with open(index, 'w', encoding='utf-8', newline='\n') as fp:
        fp.write('# Le désassemblage déposé\n\n')
        fp.write('Régénéré par `py -3 tools/deposer_disasm.py`, jamais édité à '
                 'la main.\nLa liste des fonctions vit dans l\'outil, en '
                 'clair, avec pour chacune ce\nqu\'elle sert et où elle est '
                 'racontée.\n\n')
        fp.write('Ce dossier existe parce que les séances d\'octobre '
                 'n\'avaient laissé que des\nextraits cités dans '
                 '`REPRISE.md`. Un extrait prouve ce qu\'on en dit ; il ne\n'
                 'permet pas de relire la fonction, ni de voir ce qu\'on '
                 'n\'avait pas remarqué.\n\n')
        fp.write('## APM3 — la borne\n\n')
        for nom, va, n, note in BORNE:
            fp.write('- [`%s.txt`](%s.txt) — `0x%X`, %d octets. %s\n'
                     % (nom, nom, va, n, note.split('.')[0] + '.'))
        fp.write('\n## Xbox 360 — la console Final Showdown\n\n')
        fp.write('`extracted/X360_FS/sel/default.img` — elle porte `VF5FS`, '
                 '`FINAL SHOWDOWN` et\n`takitm`, et l\'espace de noms '
                 '`customize::`, le même qu\'APM3. **Ce n\'est pas**\nla '
                 'console de 2007 : celle-là est `extracted/X360_VF5/'
                 'vf5_x360.img`.\nUne image ne se nomme pas par son dossier.'
                 '\n\n')
        for nom, va, n, note in X360:
            fp.write('- [`%s.txt`](%s.txt) — `0x%X`, %d instructions. %s\n'
                     % (nom, nom, va, n, note.split('.')[0] + '.'))
        fp.write('\n## Lindbergh — la borne d\'avant\n\n')
        fp.write('`extracted/LIND_FS/sel/vf5` — ELF x86 32 bits, '
                 '`rom_version` 2010, `libsama.so` :\nun binaire **d\'arcade**'
                 '. Espace de noms `terminal::`, et les libellés de\ntâches en'
                 ' clair à côté des noms de types (`TERMINAL_ITEM_EQUIP`).\n'
                 'La personnalisation n\'est donc pas une exclusivité console.'
                 '\n\n')
        for nom, va, n, note in LIND:
            fp.write('- [`%s.txt`](%s.txt) — `0x%X`, %d instructions. %s\n'
                     % (nom, nom, va, n, note.split('.')[0] + '.'))
    print('%d fichier(s) déposé(s) dans analysis/disasm/' % len(faits))
    print('index : analysis/disasm/README.md')
    return 0


if __name__ == '__main__':
    sys.exit(main())
