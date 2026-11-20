#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consigne le role des 55 gestionnaires de la liste 2 de mothead.

Chaque entree vient de la lecture du gestionnaire dans le build APM3
(tools/lire_gestionnaires_liste2.py). Le script met a jour
analysis/mothead_opcodes.csv et ecrit analysis/mothead_liste2_roles.md.

Usage :
    py -3 tools/poser_roles_liste2.py
"""
import collections
import csv
import io
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)

# code -> (nom, confiance, ce qui a ete lu dans le gestionnaire)
ROLES = {
    0: ("Effet sonore date", "CONFIRMED",
        "charge u32 = indice dans la table de 410 noms de sons 0x180401730 ; "
        "le nom part dans 0x180185C20 avec la categorie 2"),
    1: ("Ressource datee", "SUPPORTED",
        "charge u32 = identifiant de ressource a deux niveaux, passe a 0x1801647A0(ROB, id) ; "
        "si l identifiant vaut 0x400 la suite est sautee, sinon 0x180139EA0"),
    2: ("Angle de rotation date", "SUPPORTED",
        "pose le bit 8 de etat+0x1C ; si le bit 3 de ROB+0x6C0 (le miroir) est pose, "
        "retranche la charge u16 de etat+0x35C. Les 114 valeurs sont des angles binaires"),
    3: ("Pose un bit du tableau de drapeaux", "CONFIRMED",
        "charge s32 = numero de bit : [etat+0x1C + (n>>5)*4] |= 1 << (n & 31)"),
    4: ("Efface un bit du tableau de drapeaux", "CONFIRMED",
        "exactement l inverse du code 3 : and avec le complement du bit"),
    5: ("Bascule un bit", "CONFIRMED",
        "sans charge utile : inverse le bit 2 de ROB+0x6C0"),
    6: ("Pose deux drapeaux et remet un champ a zero", "CONFIRMED",
        "sans charge utile : ROB+0x66C = 0, puis etat+0x1C |= 0x400 puis |= 0x800"),
    7: ("Transition conditionnee", "SUPPORTED",
        "consulte l accesseur 0x1800630B0, croise trois bits de la charge avec les "
        "drapeaux ROB+0x508 et ROB+0x6C0"),
    8: ("Effet sonore date, avec evenement", "SUPPORTED",
        "meme entree que le code 0 (0x180164AB0) quand la charge est non nulle, puis "
        "emet un evenement par 0x180087260 avec la trame de l entree"),
    9: ("Commutateur de bits date", "CONFIRMED",
        "charge u16 bornee a 17 : 18 cas qui posent ou effacent un bit du masque etat+0x4A8"),
    10: ("Transition conditionnee par l entree", "SUPPORTED",
         "garde sur etat+0x00C et ROB+0x928 ; charge s16 ; passe par 0x18016A1C0, "
         "puis remet ROB+0x66C a zero et pose un bit"),
    11: ("Degats dates", "SUPPORTED",
         "appelle ScaleDamageByPower (0x1801695C0), incremente deux compteurs de ROB, "
         "ajoute un flottant a ROB+0x66C, puis 0x180169510"),
    12: ("Masque de commandes date", "SUPPORTED",
         "charge u32 rangee en etat+0x4AC, puis huit bits testes un a un, chacun "
         "appelant une fonction du groupe 0x18005592x"),
    13: ("Commande a quatre champs", "LIKELY",
         "lit quatre mots de charge (+0, +4, +8, +12), consulte 0x180063250 et "
         "transmet a 0x180055630"),
    14: ("Compteur de boisson : ajout", "SUPPORTED",
         "0x180169500 fait ROB+0x690 += (s8)charge. ROB+0x690 est le compteur que le "
         "code 70 de la liste 1 decremente (ROB+0x588 dans R.E.V.O., le meme champ au "
         "decalage 0x108 pres) : c est le compteur de boisson de Shun"),
    15: ("Compteur de boisson : ajout conditionnel", "SUPPORTED",
         "comme le code 14, mais le premier u16 de la charge choisit une condition sur "
         "ROB+0x508 ; l octet ajoute est en +2"),
    16: ("Compteur de boisson : ajout conditionnel (variante)", "SUPPORTED",
         "identique au code 15 a une garde pres"),
    17: ("Deplacement date", "SUPPORTED",
         "pose etat+0x4B0 = 1 et trois flottants etat+0x4B4/0x4B8/0x4BC, plus un vecteur "
         "ROB+0x11CC/0x11D0/0x11D4 ; passe par de la trigonometrie (0x1801D3610, "
         "0x1801D3AF0) et une mise a l echelle"),
    18: ("Bifurcation datee", "SUPPORTED",
         "compare un flottant de la charge (+0x10) a ROB+0x5E8 et a ROB+0x2A68, puis "
         "enchaine une longue serie de gardes ; deja identifie comme bifurcation par la "
         "voie hors frise"),
    19: ("Initialise une requete", "LIKELY",
         "si la charge u16 depasse ROB+0x688, prepare une structure par 0x180169A30 "
         "(18 cas ; [.+4] = -1, [.+0x10] = 0x29) puis la transmet a 0x18016A780"),
    20: ("Transition conditionnee par l entree", "SUPPORTED",
         "croise le masque de la charge (+4) avec les drapeaux d entree ROB+0x508 et "
         "ROB+0x510, la fenetre ROB+0x90C et le drapeau ROB+0x91C ; puis 0x18016A1C0 et "
         "un evenement"),
    21: ("Transition conditionnee par l entree (bit 1)", "LIKELY",
         "meme famille que le code 20, avec la garde supplementaire cl & 2"),
    22: ("Transition conditionnee par l entree (bit 1, variante)", "LIKELY",
         "meme famille que le code 20"),
    23: ("Transition conditionnee par l entree (bit 4)", "LIKELY",
         "meme famille que le code 20, avec la garde cl & 0x10"),
    24: ("Transition conditionnee, deux charges", "SUPPORTED",
         "meme famille que le code 20, mais lit deux mots de charge et touche ROB+0x528"),
    25: ("Evenement date avec preparation", "LIKELY",
         "quatre mots de charge, passe par 0x1800E0280 puis emet un evenement ; touche "
         "ROB+0x448 et etat+0x8FA"),
    26: ("Numero de posture", "CONFIRMED",
         "charge u8 rangee en ROB+0x65C -- le meme champ que R.E.V.O. ROB+0x554, au "
         "decalage 0x108 pres -- puis met en cache le pointeur de ressource "
         "correspondant en ROB+0x660"),
    27: ("Commutateur a trois cas", "LIKELY",
         "charge s16 : trois branches ; la branche par defaut remet [[ROB+0x30]+0xCC] "
         "a zero"),
    28: ("Rampe datee", "CONFIRMED",
         "charge s16 = n : etat+0x4B0 = 3, etat+0x4B4 = (float)n, "
         "etat+0x4BC = -0.35 / (n - trame + 1). Meme bloc que le code 17"),
    29: ("Table de sous-entrees", "SUPPORTED",
         "parcourt un tableau de la charge au pas de 0x34, y lit cinq flottants et trois "
         "u16 ; sensible au miroir ROB+0x6C0 bit 3"),
    30: ("Annule le deplacement", "CONFIRMED",
         "sans charge utile : remet etat+0x92C et etat+0x934 a zero, les deux champs que "
         "le code 17 ecrit"),
    31: ("Son d impact de mur", "CONFIRMED",
         "aucune garde et aucune charge : saut direct vers 0x1801905D0, qui emet d abord le "
         "son fixe \"vfx_wall2_building\" puis un second choisi dans une table de 13 noms "
         "(0x180409000) selon un global de decor : vfxse_wall_aquarium, vfxse_wall_greek, "
         "vfxse_wall_harbor, vfxse_wall_religious, vfxse_wall_snow... Les deux passent par "
         "0x180185C20 avec la categorie 2, comme le code 0. Cela recoupe la note tiree des "
         "donnees : codes 17, 30 et 31 = collision murale"),
    32: ("Table de creneaux par bits", "SUPPORTED",
         "le mot de charge +4 est un masque ; pour chaque bit pose, ecrit un drapeau "
         "octet en etat+0x4C6+k et deux flottants"),
    33: ("Bloc a sept champs", "SUPPORTED",
         "lit sept mots de charge et ecrit etat+0x78C et suivants"),
    34: ("Trois champs d etat", "SUPPORTED",
         "lit trois mots de charge et ecrit etat+0x7AC et etat+0x7B0 ; consulte "
         "0x1801583D0 et 0x180169660, qui remet ROB+0x940 a zero en gardant son bit 2"),
    35: ("Code 34 conditionnel", "CONFIRMED",
         "si le bit 0 de ROB+0x500 est efface, execute le gestionnaire du code 34 puis "
         "pose etat+0x7B4 = 1"),
    36: ("Code 4 de la liste 1, date", "CONFIRMED",
         "add rcx, 0x18 puis saut vers 0x180155B10 : ecrit etat+0x14C et etat+0x150"),
    37: ("Code 5 de la liste 1, date", "CONFIRMED",
         "delegue a 0x180155B30 : ecrit les fenetres 0 et 1"),
    38: ("Code 6 de la liste 1, date", "CONFIRMED",
         "delegue a 0x180155E20 : fenetre 0 (etat+0x154)"),
    39: ("Code 7 de la liste 1, date", "CONFIRMED",
         "delegue a 0x180155EA0 : fenetre 1 (etat+0x160)"),
    40: ("Code 8 de la liste 1, date", "CONFIRMED",
         "delegue a 0x180155F20 : fenetre 2 (etat+0x16C)"),
    41: ("Code 9 de la liste 1, date", "CONFIRMED",
         "delegue a 0x180155FA0 : fenetre 3 (etat+0x178)"),
    42: ("Code 10 de la liste 1, date", "CONFIRMED",
         "delegue a 0x180156020 : fenetre 4 (etat+0x184)"),
    43: ("Code 11 de la liste 1, date", "CONFIRMED",
         "delegue a 0x1801560A0 : fenetre 2 (etat+0x16C)"),
    44: ("Code 12 de la liste 1, date", "CONFIRMED",
         "delegue a 0x180156210 : fenetre 5 (etat+0x190)"),
    45: ("Code 13 de la liste 1, date", "CONFIRMED",
         "delegue a 0x180156290 : fenetre 6 (etat+0x19C)"),
    46: ("Code 14 de la liste 1, date", "CONFIRMED",
         "delegue a 0x180156310 : fenetre 7 (etat+0x1A8)"),
    47: ("Code 52 de la liste 1, date", "CONFIRMED",
         "delegue a 0x1801579E0 : le masque de 64 bits etat+0x348"),
    48: ("Code 58 de la liste 1, date", "CONFIRMED",
         "delegue a 0x180157B70 : range le pointeur de charge en etat+0x398"),
    49: ("Code 65 de la liste 1, date", "CONFIRMED",
         "delegue a 0x180157CF0 : ajoute une case au conteneur etat+0x3B8"),
    50: ("Deux champs de ROB", "LIKELY",
         "lit la charge en +0 et +8, ecrit ROB+0x864 et ROB+0x898, passe par 0x18016A210 "
         "et 0x1800E5910"),
    51: ("Transition conditionnee (variante)", "SUPPORTED",
         "meme famille que les codes 20 a 24, avec 0x18016A160 au lieu de 0x18016A1C0"),
    52: ("Requete externe", "SUPPORTED",
         "aucune charge lue : transmet ROB a 0x18013D030"),
    53: ("Cinq champs d etat", "SUPPORTED",
         "lit cinq mots de charge et ecrit etat+0x888 et etat+0x88C"),
    54: ("Evenement date sur l attaque", "LIKELY",
         "lit etat+0x070 et etat+0x06C, ecrit dans le bloc etat+0x8A? et emet un evenement"),
}

# Ce que le jeu en marche a montre : tools/oracle_liste2_vivant.py pose un point
# d'arret a l'entree du gestionnaire et un autre sur son adresse de retour, et
# diffe 12 Ko de ROB entre les deux. Ce qui suit est un releve, pas une lecture.
OBSERVE = {
    21: "jamais vu, et il ne PEUT pas l'etre : le code 21 n'existe que dans le reequilibrage 2.00 (5 entrees), absent de tout jeu de donnees arcade, donc de celui que le jeu charge",
    54: "jamais vu ; trois entrees seulement, chez MSK et SHU",
    27: "jamais vu ; propre a SHUN (index 3 de rob_cmn_mottbl), qui n'est pas apparu",
    22: "jamais vu ; deux entrees seulement dans tout l'arcade 6.000, chez BRA et JEF",
    19: "jamais vu, meme dans un combat contre BRAD (ROB+0x10 = 13), alors que 24 de ses 40 entrees sont chez Brad : le code vit dans des animations que l'adversaire n'a pas jouees",
    1:  "8 passages : ecrit ROB+0x864, ROB+0x86C, ROB+0x870 et etat+0x26A4",
    7:  "2 passages, charge (0x8000, 0.03, -5.0) : ecrit ROB+0x440 et six flottants, "
        "etat+0x914 a etat+0x91C puis etat+0x92C a etat+0x934",
    10: "3 passages : ecrit ROB+0x668, le champ que pose 0x18016A1C0 (la lecture statique "
        "disait ROB+0x66C : c est ROB+0x668)",
    12: "1 passage, charge = masque 0x80000000 puis le flottant 0.05 : ecrit etat+0x4AC, "
        "exactement le champ predit",
    13: "3 passages, aucune ecriture dans les 12 Ko observes. Sa garde est lue : 0x180063250 rend le bit 1 de ROB+0x7B8, teste SUR LES DEUX COMBATTANTS (soi et [ROB+0x20]) ; il faut que les deux soient a zero. Le gestionnaire monte ensuite une structure de huit champs melant les deux combattants et la passe a 0x180055630",
    17: "1 passage, charge u16 = 14 : ecrit etat+0x4B0 = 1, etat+0x4B4 = 14.0, puis "
        "etat+0x4B8, etat+0x4BC et etat+0x4C0",
    18: "2 passages : copie les deux premiers mots de la charge dans etat+0x784 et "
        "etat+0x788, et pose ROB+0x4CC = 5, ROB+0x4D0 et ROB+0x4E4. Les valeurs de "
        "etat+0x784 sont des puissances de deux (1, 4, 64, 256, 0x20000000) : des MASQUES, "
        "et non des identifiants d animation -- l hypothese a ete testee sur le corpus et "
        "rejetee (8 valides sur 532)",
    20: "12 passages, aucune ecriture, y compris en tenant les treize boutons a la fois. Les quatre champs de garde ont ete releves a l entree : ROB+0x508 et ROB+0x510 portent des masques qui varient avec nos entrees (0, 1, 0x15, 0x40001, 0x80003, 0x2080003), ROB+0x90C un FLOTTANT de 15.0 a 19.0 et ROB+0x91C un booleen. C est un TAMPON D ENTREE : masque courant, masque tamponne, trames restantes, tampon actif. L absence d ecriture s explique donc par la garde, et non par une lecture fausse",
    24: "6 passages, aucune ecriture, meme en tenant tous les boutons ; memes champs de garde que le code 20, releves avec les memes valeurs",
    25: "6 passages, aucune ecriture. Charges vues : (1, 0x7f), (2, 0x16), (2, 0x7f)",
    29: "4 passages : a la trame 43 avec une charge u16 de 53, ecrit etat+0x7BC = 43.0 et "
        "etat+0x7C0 = 53.0, plus un bloc etat+0x7E4 a etat+0x818. Sur le corpus, les 394 "
        "charges sont TOUTES superieures a la trame de leur entree, et l ecart vaut 10 dans "
        "333 cas : c est une fenetre de trames",
    31: "2 passages, sans charge utile et sans aucune ecriture dans le ROB -- ce qui est "
        "exactement attendu d un gestionnaire qui ne fait qu emettre deux sons",
    32: "3 passages : ecrit le mot de drapeaux etat+0x4C4 et des flottants dans plusieurs "
        "tables paralleles (etat+0x514 et 0x520 ; etat+0x64C et 0x658 ; etat+0x698 a 0x6A0)",
    33: "2 passages : etat+0x78C recoit la TRAME DE L ENTREE (48.0 puis 64.0) et etat+0x790 "
        "la CHARGE (54.0 puis 70.0). Sur le corpus, 3577 charges sur 3645 sont superieures a "
        "la trame, 63 egales, 5 inferieures",
    51: "5 passages ; l un a ecrit ROB+0x5E8 = 55.0, soit exactement la charge u16 (55). Sur "
        "le corpus, 1425 charges sur 1430 sont superieures a la trame de leur entree",
    52: "2 passages, charge u16 = 28 : ecrit ROB+0x634 = 28.0, un drapeau, et un vecteur "
        "unitaire ROB+0x63C / 0x640 / 0x644. Sur le corpus, les 242 charges sont toutes "
        "superieures a la trame",
    53: "1 passage : ecrit etat+0x888 et etat+0x88C, les deux champs predits. Sur le corpus, "
        "les 44 charges sont toutes superieures a la trame",
}

CSV = 'analysis/mothead_opcodes.csv'
GES = 'analysis/mothead_liste2_gestionnaires.csv'
DOC = 'analysis/mothead_liste2_roles.md'


def main():
    rows = list(csv.DictReader(io.open(CSV, encoding='utf-8')))
    champs = list(rows[0].keys())
    n = 0
    for r in rows:
        if r['liste'] != '2':
            continue
        c = int(r['code'])
        if c not in ROLES:
            continue
        nom, conf, lu = ROLES[c]
        r['nom'] = nom
        r['confiance'] = conf
        if 'GESTIONNAIRE LU' not in r['description']:
            r['description'] = r['description'].rstrip(' ;.') + ' ; GESTIONNAIRE LU : ' + lu
        if c in OBSERVE and 'VU DANS LE JEU' not in r['description']:
            r['description'] = (r['description'].rstrip(' ;.') +
                                ' ; VU DANS LE JEU : ' + OBSERVE[c])
        n += 1
    with open(CSV, 'w', newline='', encoding='utf-8') as fp:
        wr = csv.DictWriter(fp, fieldnames=champs)
        wr.writeheader()
        for r in rows:
            wr.writerow({k: r.get(k, '') for k in champs})

    l2 = [r for r in rows if r['liste'] == '2']
    print('%d codes de liste 2 mis a jour dans %s' % (n, CSV))
    print('confiances :', dict(collections.Counter(r['confiance'] for r in l2)))
    restants = [r['code'] for r in l2 if r['nom'] in ('', 'Inconnu')]
    print('codes de liste 2 encore sans nom :', restants or 'aucun')

    ges = {int(x['code']): x for x in csv.DictReader(io.open(GES, encoding='utf-8'))}
    with open(DOC, 'w', encoding='utf-8') as fp:
        fp.write('# Les 55 codes de la liste 2 de `mothead` — le role de chaque gestionnaire\n\n')
        fp.write('Lu dans le build APM3, gestionnaire par gestionnaire '
                 '(`tools/lire_gestionnaires_liste2.py`).\n')
        fp.write('Adresses des deux builds et drapeaux : '
                 '`analysis/mothead_liste2_gestionnaires.csv`.\n')
        fp.write('Le drapeau « n\'agit qu\'a la trame exacte » (bit 0 du champ `+0x18` de la '
                 'table de repartition)\nvaut pour les codes **0, 1, 8, 25 et 31**.\n\n')
        fp.write('Convention d\'appel, lue dans `MothRunList2` :\n\n')
        fp.write('```\ngestionnaire(rcx = &ctx, rdx = charge utile, r8 = entree de 12 octets)\n'
                 'ctx = [ ROB, ROB+0x440, [ROB+0x20]+0x30C0, ROB, ROB+0x440, ROB+0x8A0 ]\n'
                 '        0     1          2                  3    4          5 = l\'etat\n```\n\n')
        fp.write('Les trois dernieres cases rejouent la convention de la liste 1 : un '
                 'gestionnaire qui fait\n`add rcx, 0x18` delegue donc a un gestionnaire de '
                 'liste 1. Quatorze codes le font.\n\n')
        fp.write('| code | gestionnaire | emplois | role | confiance |\n|---|---|---:|---|---|\n')
        for c in sorted(ROLES):
            nom, conf, _ = ROLES[c]
            g = ges.get(c, {})
            fp.write('| %d | `%s` | %s | %s | %s |\n'
                     % (c, g.get('gestionnaire_APM3', ''),
                        g.get('emplois_donnees') or '—', nom, conf))
        fp.write('\n## Ce que chaque gestionnaire fait\n\n')
        for c in sorted(ROLES):
            nom, conf, lu = ROLES[c]
            fp.write('- **code %d — %s** (%s) : %s' % (c, nom, conf, lu))
            if c in OBSERVE:
                fp.write('\n  - *vu dans le jeu* : %s' % OBSERVE[c])
            fp.write('\n')
    print('%s ecrit' % DOC)
    return 0


if __name__ == '__main__':
    sys.exit(main())
