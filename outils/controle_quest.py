#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TOUT CE QUI SE VERIFIE SANS LANCER LE JEU.

Frederic a interdit de lancer le jeu ; le portage du mode Quest, lui, touche
a une dizaine de fichiers et a une quinzaine de sites du moteur. Sans filet,
chaque seance repart en aveugle. Cet outil est le filet : il **compile** le
module, **patche** le moteur avec la ligne exacte de `tools/quest.cmd`, puis
**mesure dans le binaire produit** que chaque chose y est.

Il ne juge que ce qui est mesurable. Ce qui demande un ecran est marque
« a voir », jamais « bon ».

    py -3 tools/controle_quest.py --tout      compiler, patcher, tout mesurer
    py -3 tools/controle_quest.py             mesurer seulement (rien n'est
                                              recompile ni repatche)
    py -3 tools/controle_quest.py --rapide    idem, sans le balayage des
                                              libelles (le plus long)

Code de sortie **non nul au premier defaut**. Rapport complet dans
`analysis/controle_quest.txt`, quoi qu'il arrive.
"""
import os
import struct
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
MEDIA = os.path.join(JEU, 'vf5fs_media')
DLL = os.path.join(JEU, 'vf5fs-pxd-w64-Retail_APM3.dll')
ORIGINE = DLL + '.origine'
RAPPORT = os.path.join(RACINE, 'analysis', 'controle_quest.txt')

# La ligne de patch de `tools/quest.cmd`, mot pour mot. Si elle change la-bas,
# elle doit changer ici : `tools/regression.py` le verifie.
LIGNE_QUEST = [
    '--resolution', '1280', '720', '--langue', '--logo-japonais',
    '--dural', '--wxga', '--dural-grille', '--mode', '0', '--menu-init',
    '--sousmenu', '--transition-game', '--sp-menu', '--sp-lancer',
    '--sp-sparring', '--joueur2', '--menu-fermer', '--options-raccourci',
    '--dojo-howto', '--dojo-cadre', '--options-sans-howto', '--menu-exit',
    '--legende-sousmenu', '--attract-retour-titre', '--sans-now-loading',
    '--options-tips', '--decor-perso', 'djo', '--decors-dural', 'cas',
    '--variantes', '--du2-collision', '--bases-2d-libres', '--quest-ecran',
    '--textes-quest', '--terminal-boutons', '--customize-curseur',
    '--replays-sans-gel', '--vignettes-costume',
]

# Les planches 2D que le Quest importe (voir tools/bases_2d.py).
PLANCHES = ['que', 'qwin', 'tnt', 'tnto', 'qdan']
# Les 492 libelles ajoutes a string_array.
LIB_PREMIER, LIB_DERNIER = 23052, 23543
# npc_tbl.bin
NPC_NOMBRE, NPC_PAS = 1000, 0x90


class Defaut(Exception):
    pass


class Rapport:
    """Un journal qui s'ecrit sur le disque meme quand on s'arrete en route."""

    def __init__(self):
        self.lignes = []
        self.defauts = 0

    def titre(self, t):
        self.dire('')
        self.dire('=' * 74)
        self.dire(t)
        self.dire('=' * 74)

    def dire(self, t=''):
        print(t)
        self.lignes.append(t)

    def bon(self, quoi, detail=''):
        self.dire('  OK      %-42s %s' % (quoi, detail))

    def voir(self, quoi, detail=''):
        self.dire('  A VOIR  %-42s %s' % (quoi, detail))

    def mauvais(self, quoi, detail=''):
        self.defauts += 1
        self.dire('  DEFAUT  %-42s %s' % (quoi, detail))
        raise Defaut('%s : %s' % (quoi, detail))

    def ecrire(self):
        os.makedirs(os.path.dirname(RAPPORT), exist_ok=True)
        txt = '\n'.join(self.lignes) + '\n'
        with open(RAPPORT, 'w', encoding='utf-8') as fp:
            fp.write(txt)


def lancer(r, titre, argv):
    """Un sous-processus, sortie NON filtree (c'est la regle du chantier)."""
    r.dire('  $ %s' % ' '.join(argv))
    p = subprocess.run([sys.executable] + argv, cwd=RACINE,
                       capture_output=True, text=True, errors='replace')
    for l in (p.stdout + p.stderr).splitlines():
        r.dire('    | %s' % l)
    if p.returncode:
        r.mauvais(titre, 'code de retour %d' % p.returncode)
    return p


# ---------------------------------------------------------------------------
# 1. LE MOTEUR PATCHE : les octets attendus a chaque site
# ---------------------------------------------------------------------------

def controler_moteur(r):
    import pe_disasm as P
    import patch_moteur as PM

    r.titre('1. LE MOTEUR PATCHE')
    if not os.path.exists(DLL):
        r.mauvais('la DLL patchee', 'absente')
    img = P.Image(DLL)
    ori = P.Image(ORIGINE)

    greffe = [s for s in img.secs if s['name'] == '.greffe']
    if not greffe:
        r.mauvais('la section .greffe', 'absente de la DLL patchee')
    g = greffe[0]
    if not (g['exec'] and g['vsize'] >= PM.GREFFE_TAILLE):
        r.mauvais('.greffe', 'vsize 0x%X, executable=%s'
                  % (g['vsize'], g['exec']))
    r.bon('.greffe', 'VA 0x%X, 0x%X octets, executable'
          % (g['va'], g['vsize']))

    try:
        PM.verifier_disposition(PM.GREFFE_TAILLE)
    except AssertionError as e:
        r.mauvais('disposition de la greffe', str(e))
    zones = sorted(PM._disposition(), key=lambda z: z[1])
    r.bon('disposition de la greffe',
          '%d zones, aucun recouvrement, tout tient dans 0x%X'
          % (len(zones), PM.GREFFE_TAILLE))
    for n, d, t in zones:
        r.dire('            %-10s 0x%04X .. 0x%04X' % (n, d, d + t))

    # --- le site d'appel de SCOREBOARDS ------------------------------------
    av = ori.read(PM.QUEST_SITE_APPEL, 5)
    ap = img.read(PM.QUEST_SITE_APPEL, 5)
    if av == ap:
        r.mauvais('SCOREBOARDS (0x%X)' % PM.QUEST_SITE_APPEL,
                  'le `call` n a pas ete detourne (%s)' % ap.hex())
    if ap[0] != 0xE8:
        r.mauvais('SCOREBOARDS (0x%X)' % PM.QUEST_SITE_APPEL,
                  'ce n est plus un `call` (%s)' % ap.hex())
    cible = PM.QUEST_SITE_APPEL + 5 + struct.unpack('<i', ap[1:])[0]
    if not (g['va'] <= cible < g['va'] + g['vsize']):
        r.mauvais('SCOREBOARDS (0x%X)' % PM.QUEST_SITE_APPEL,
                  'le detour ne pointe pas dans .greffe (0x%X)' % cible)
    r.bon('SCOREBOARDS (0x%X)' % PM.QUEST_SITE_APPEL,
          'call -> 0x%X (.greffe+0x%X)' % (cible, cible - g['va']))

    # --- les deux enregistrements d'etat -----------------------------------
    for nom, va, off in (('mode DATA_TEST', PM.QUEST_MODE_REC, 0x10),
                         ('sous-etat 35, milieu', PM.QUEST_SOUS_REC, 0x10),
                         ('sous-etat 35, sortie', PM.QUEST_SOUS_REC, 0x18)):
        p = struct.unpack('<Q', img.read(va + off, 8))[0]
        o = struct.unpack('<Q', ori.read(va + off, 8))[0]
        if p == o:
            r.mauvais(nom, 'inchange (0x%X)' % p)
        if not (g['va'] <= p < g['va'] + g['vsize']):
            r.mauvais(nom, 'ne pointe pas dans .greffe (0x%X)' % p)
        r.bon(nom, '0x%X -> 0x%X (.greffe+0x%X)' % (o, p, p - g['va']))
    mm = struct.unpack('<I', img.read(PM.QUEST_MODE_REC + 0x60, 4))[0]
    if mm != PM.QUEST_MENU_MODE:
        r.mauvais('mode de retour', '%d au lieu de %d'
                  % (mm, PM.QUEST_MENU_MODE))
    r.bon('mode de retour', '%d = MENU' % mm)

    # --- le creneau 4 d'AetMgr ---------------------------------------------
    p = struct.unpack('<Q', img.read(PM.QUEST_AETMGR_SLOT, 8))[0]
    if p == PM.QUEST_AETMGR_ORIGINAL:
        r.mauvais('creneau 4 d AetMgr', 'inchange (0x%X)' % p)
    if not (g['va'] <= p < g['va'] + g['vsize']):
        r.mauvais('creneau 4 d AetMgr', 'hors .greffe (0x%X)' % p)
    r.bon('creneau 4 d AetMgr', '0x%X -> 0x%X' % (PM.QUEST_AETMGR_ORIGINAL, p))

    # --- la boite aux lettres ----------------------------------------------
    boite = img.read(g['va'] + PM.GRE_QUEST, 8)
    if boite != PM.QUEST_MAGIE:
        r.mauvais('la boite aux lettres QUESTBOX',
                  '%r au lieu de %r' % (boite, PM.QUEST_MAGIE))
    r.bon('la boite aux lettres', '%r en 0x%X'
          % (PM.QUEST_MAGIE.decode(), g['va'] + PM.GRE_QUEST))

    # --- les deux boutons du TERMINAL --------------------------------------
    for va, tete, code, quoi in PM.TERMINAL_BOUTONS:
        avant = ori.read(va, 5)
        apres = img.read(va, 5)
        if avant != tete:
            r.mauvais('TERMINAL 0x%X' % va,
                      'le .origine ne porte plus %s mais %s'
                      % (tete.hex(), avant.hex()))
        if apres == tete:
            r.mauvais('TERMINAL 0x%X (%s)' % (va, quoi), 'non detourne')
        c = va + 5 + struct.unpack('<i', apres[1:])[0]
        if not (g['va'] + PM.GRE_TERM <= c
                < g['va'] + PM.GRE_TERM + PM.GRE_TERM_TAILLE):
            r.mauvais('TERMINAL 0x%X' % va, 'hors de la zone TERM (0x%X)' % c)
        # le relais : sub rsp,0x28 (4) ; mov rcx,[rip+d] (7) ; BA <code>
        stub = img.read(c, 0x24)
        if stub[0x0B] != 0xBA or struct.unpack_from('<I', stub, 0x0C)[0] != code:
            r.mauvais('TERMINAL 0x%X' % va,
                      'le relais ne demande pas le code %d' % code)
        r.bon('TERMINAL 0x%X (%s)' % (va, quoi),
              'relais 0x%X, code %d' % (c, code))

    # --- le curseur de l'ecran de personnalisation -------------------------
    # Constat de Frederic a l'ecran (2026-09-30) : le curseur ne bougeait
    # nulle part. Trois pages posaient leur compte puis l'effacaient.
    for va, tete, quoi in PM.CUSTOMIZE_CURSEUR:
        if ori.read(va, len(tete)) != tete:
            r.mauvais('curseur 0x%X' % va,
                      'le .origine ne porte plus l effacement attendu')
        ap = img.read(va, len(tete))
        if ap != b'\x90' * len(tete):
            r.mauvais('curseur 0x%X (%s)' % (va, quoi.split(' :')[0]),
                      'l effacement n est pas neutralise (%s)' % ap.hex())
        r.bon('curseur %s' % quoi.split(' :')[0],
              '%d octets neutralises en 0x%X' % (len(tete), va))

    # --- le compte qu'il a fallu ECRIRE, faute d'effacement ----------------
    # Constat de Frederic a l'ecran (2026-10-01) : « gauche et droite ne
    # fonctionnent que sur l'ecran Character Select ». TaskCostumeMenu
    # n'effacait rien -- il n'avait jamais rien pose -- mais il COMPTE ses
    # costumes dans [rbx+0x420]. On lui fait relire son propre compte.
    for va, vieux, neuf, quoi in PM.CURSEUR_REBATI:
        if ori.read(va, len(vieux)) != vieux:
            r.mauvais('compte 0x%X' % va,
                      'le .origine ne porte plus la sequence attendue')
        ap = img.read(va, len(neuf))
        if ap != neuf:
            r.mauvais('compte 0x%X (%s)' % (va, quoi.split(' :')[0]),
                      'le calcul n est pas pose (%s)' % ap.hex())
        r.bon('compte %s' % quoi.split(' :')[0],
              '%d octets reecrits en 0x%X : le compte vient de [rbx+0x420]'
              % (len(neuf), va))

    # --- le compte de DataSelector, pose par relais ------------------------
    # Deuxieme page nommee par Frederic le 2026-10-01 : les CINQ lignes de
    # donnees du premier ecran. Dix-sept octets a ecrire, douze disponibles :
    # on detourne vers la greffe.
    va_d = PM.DATASELECTOR_COMPTE_VA
    if ori.read(va_d, len(PM.DATASELECTOR_COMPTE_TETE)) !=             PM.DATASELECTOR_COMPTE_TETE:
        r.mauvais('DataSelector 0x%X' % va_d,
                  'le .origine ne porte plus l effacement attendu')
    ap = img.read(va_d, 5)
    if ap[0] != 0xE9:
        r.mauvais('DataSelector 0x%X' % va_d,
                  'le saut vers le relais n est pas pose (%s)' % ap.hex())
    cible = va_d + 5 + struct.unpack('<i', ap[1:5])[0]
    corps = img.read(cible, 24)
    if corps[:6] != bytes.fromhex('C78324020000') or             struct.unpack('<I', corps[6:10])[0] != PM.DATASELECTOR_COMPTE_CRANS:
        r.mauvais('DataSelector relais 0x%X' % cible,
                  'le relais ne pose pas %d crans (%s)'
                  % (PM.DATASELECTOR_COMPTE_CRANS, corps[:10].hex()))
    if corps[10:17] != bytes.fromhex('C6832802000001'):
        r.mauvais('DataSelector relais 0x%X' % cible,
                  'le relais ne met pas le bouclage (%s)' % corps[10:17].hex())
    retour = cible + 22 + struct.unpack('<i', corps[18:22])[0]
    if corps[17] != 0xE9 or retour != PM.DATASELECTOR_COMPTE_RETOUR:
        r.mauvais('DataSelector relais 0x%X' % cible,
                  'le retour ne vise pas 0x%X (0x%X)'
                  % (PM.DATASELECTOR_COMPTE_RETOUR, retour))
    r.bon('compte DataSelector',
          'relais 0x%X : %d crans bouclants, retour 0x%X'
          % (cible, PM.DATASELECTOR_COMPTE_CRANS, retour))

    # --- le SECOND verrou : l'accepteur de vtable --------------------------
    # Le compteur ne suffisait pas : si le creneau 7/8 refuse, 0x1801BBBE0
    # RESTAURE le curseur. Deuxieme essai de Frederic, 2026-09-30.
    for va, avant, neuf, quoi in PM.CURSEUR_ACCEPTEURS:
        if struct.unpack('<Q', ori.read(va, 8))[0] != avant:
            r.mauvais('accepteur 0x%X' % va, 'le .origine a change')
        lu = struct.unpack('<Q', img.read(va, 8))[0]
        if lu != neuf:
            r.mauvais('accepteur 0x%X' % va,
                      'porte 0x%X au lieu de 0x%X' % (lu, neuf))
        r.bon('accepteur %s' % quoi.split(' :')[0],
              '0x%X -> 0x%X' % (avant, neuf))

    # --- les vignettes de costume -----------------------------------------
    # Mesure a l'ecran (sonde du 2026-10-01) : « Costume settings » dessine
    # AVANT que l'etat 40 n'ait charge spr_t_itm<perso>.
    lu = struct.unpack('<Q', img.read(PM.VIGNETTES_SLOT, 8))[0]
    if struct.unpack('<Q', ori.read(PM.VIGNETTES_SLOT, 8))[0] !=             PM.VIGNETTES_DESSIN:
        r.mauvais('vignettes 0x%X' % PM.VIGNETTES_SLOT, 'le .origine a change')
    if lu == PM.VIGNETTES_DESSIN:
        r.mauvais('vignettes 0x%X' % PM.VIGNETTES_SLOT,
                  'le creneau 4 de TaskCostumeMenu n est pas detourne')
    if not (g['va'] + PM.GRE_COS <= lu
            < g['va'] + PM.GRE_COS + PM.GRE_COS_TAILLE):
        r.mauvais('vignettes 0x%X' % PM.VIGNETTES_SLOT,
                  'le detour est hors de la zone COS (0x%X)' % lu)
    r.bon('vignettes (creneau 4 TaskCostumeMenu)',
          'relais 0x%X : la planche est chargee avant le dessin' % lu)

    # --- Replays ne fige plus ---------------------------------------------
    va, tete, neuf = PM.REPLAYS_SANS_GEL
    if ori.read(va, len(tete)) != tete:
        r.mauvais('replays 0x%X' % va, 'le .origine a change')
    if img.read(va, len(neuf)) != neuf:
        r.mauvais('replays 0x%X' % va,
                  '« Your data » fige encore (%s)' % img.read(va, 4).hex())
    r.bon('replays 0x%X' % va,
          '« Your data » referme la page au lieu de figer')
    va, tete, neuf = PM.REPLAYS_SANS_RANKING
    if ori.read(va, len(tete)) != tete:
        r.mauvais('replays 0x%X' % va, 'le .origine ne porte pas `cmp edi,2`')
    if img.read(va, len(neuf)) != neuf:
        r.mauvais('replays 0x%X' % va,
                  '« Online data » ouvre encore la page des classements')
    r.bon('replays 0x%X' % va,
          '« Online data » referme la page (cmp edi,2 -> cmp edi,3)')


# ---------------------------------------------------------------------------
# 2. LES DONNEES POSEES A COTE DU JEU
# ---------------------------------------------------------------------------

def controler_libelles(r, rapide):
    r.titre('2. LES 492 LIBELLES DU QUEST')
    if rapide:
        r.dire('  (saute : --rapide)')
        return
    import textes_quest as T
    fautes = T.controle()
    if fautes:
        r.mauvais('libelles %d..%d' % (LIB_PREMIER, LIB_DERNIER),
                  ' ; '.join(fautes))
    r.bon('libelles %d..%d' % (LIB_PREMIER, LIB_DERNIER),
          '%d chaines, presentes dans string_array'
          % (LIB_DERNIER - LIB_PREMIER + 1))


def controler_rivaux(r):
    r.titre('3. npc_tbl.bin -- LES MILLE RIVAUX')
    import rivaux as R
    if not os.path.exists(R.CIBLE):
        r.mauvais('npc_tbl.bin', 'absent (%s)' % R.CIBLE)
    d = open(R.CIBLE, 'rb').read()
    if len(d) < NPC_NOMBRE * NPC_PAS:
        r.mauvais('npc_tbl.bin', '%d octets, il en faut au moins %d'
                  % (len(d), NPC_NOMBRE * NPC_PAS))
    fautes = R.controle()
    if fautes:
        r.mauvais('npc_tbl.bin', ' ; '.join(fautes))
    r.bon('npc_tbl.bin', '%d octets, %d rivaux de 0x%X'
          % (len(d), NPC_NOMBRE, NPC_PAS))

    # GROS-BOUTISME : l'offset du nom du rival 0 doit tomber DANS le fichier,
    # lu en gros-boutiste, et PAS en petit-boutiste. C'est le controle qui
    # attrape une table reconvertie par erreur.
    gb = struct.unpack_from('>I', d, 0)[0]
    pb = struct.unpack_from('<I', d, 0)[0]
    if not (NPC_NOMBRE * NPC_PAS <= gb < len(d)):
        r.mauvais('npc_tbl gros-boutisme',
                  'l offset du nom 0 vaut 0x%X, hors du reservoir' % gb)
    if NPC_NOMBRE * NPC_PAS <= pb < len(d):
        r.mauvais('npc_tbl gros-boutisme',
                  'il se lit AUSSI en petit-boutiste : table suspecte')
    r.bon('npc_tbl gros-boutisme', 'nom 0 en 0x%X (0x%X en petit-boutiste, '
          'hors reservoir : bon signe)' % (gb, pb))

    # UN ENREGISTREMENT TEMOIN, lu champ par champ.
    t = R.lire(d)
    nom, r1, r2, perso = t[0]
    # +0x7C le grade, +0x88 le lieu : des OCTETS, pas des mots. Le premier
    # jet les lisait en u32 gros-boutiste et annoncait « lieu 50529024 »
    # (0x03030300) : l'octet utile est le premier, les trois suivants
    # appartiennent aux champs d'a cote.
    grade = d[0x7C]
    lieu = d[0x88]
    if not nom:
        r.mauvais('rival temoin 0', 'sans nom')
    if not 0 <= perso <= 16:
        r.mauvais('rival temoin 0', 'personnage %d hors 0..16' % perso)
    if grade > 41:
        r.mauvais('rival temoin 0', 'grade %d hors 0..41' % grade)
    r.bon('rival temoin 0', 'nom %r, perso %d, grade %d, lieu %d'
          % (nom, perso, grade, lieu))
    r.dire('            replique 1 : %r' % r1[:48])
    r.dire('            replique 2 : %r' % r2[:48])


def controler_objets(r):
    r.titre('4. quest_objets.bin -- LA BOUTIQUE')
    chemin = os.path.join(JEU, 'quest_objets.bin')
    if not os.path.exists(chemin):
        r.mauvais('quest_objets.bin', 'absent (%s)' % chemin)
    d = open(chemin, 'rb').read()
    if d[:4] != b'QOBJ':
        r.mauvais('quest_objets.bin', 'en-tete %r au lieu de QOBJ' % d[:4])
    version, nb = struct.unpack_from('<II', d, 4)
    if nb == 0 or nb > 64:
        r.mauvais('quest_objets.bin', '%d personnages : invraisemblable' % nb)
    total, sans_prix, exemple = 0, 0, None
    for i in range(nb):
        o = struct.unpack_from('<I', d, 12 + 4 * i)[0]
        if not (0 < o < len(d)):
            r.mauvais('quest_objets.bin',
                      'le personnage %d pointe hors du fichier (0x%X)'
                      % (i, o))
        n = struct.unpack_from('<I', d, o)[0]
        total += n
        for k in range(n):
            id_fs, prix = struct.unpack_from('<HH', d, o + 4 + k * 8)
            if prix == 0:
                sans_prix += 1
            elif exemple is None:
                exemple = (i, id_fs, prix)
    if total == 0:
        r.mauvais('quest_objets.bin', 'aucun objet')
    if sans_prix == total:
        r.mauvais('quest_objets.bin', 'AUCUN prix : la colonne Point du CSV '
                  'de FS n a pas ete lue')
    r.bon('quest_objets.bin', 'version %d, %d personnages, %d objets, '
          '%d sans prix' % (version, nb, total, sans_prix))
    if exemple:
        r.dire('            temoin : perso %d, objet FS 0x%X, prix %d G'
               % exemple)


def controler_musique(r):
    r.titre('5. LA MUSIQUE')
    import musique_quest as M
    if not os.path.exists(M.CIBLE):
        r.mauvais('vf5ps3_b03map.adx', 'absent (%s)' % M.CIBLE)
    n = os.path.getsize(M.CIBLE)
    with open(M.CIBLE, 'rb') as fp:
        entete = fp.read(4)
    # ADX : 0x80 0x00 puis le decalage du bloc de donnees.
    if entete[0] != 0x80:
        r.mauvais('vf5ps3_b03map.adx', 'en-tete %s : ce n est pas un ADX'
                  % entete.hex())
    r.bon('vf5ps3_b03map.adx', '%d octets, en-tete ADX' % n)


def controler_planches(r):
    r.titre('6. LES PLANCHES 2D DU QUEST')
    import bases_2d as B
    fautes = B.controle()
    if fautes:
        r.mauvais('bases 2D', ' ; '.join(fautes))
    r.bon('bases 2D', 'les planches %s sont declarees' % ' '.join(PLANCHES))


def controler_sondes(r):
    """Les sondes passent-elles leur ESSAI A VIDE ?

    Le 2026-10-01 `sonde_vignettes.py` a plante APRES avoir lance le jeu,
    sur une cle de dictionnaire oubliee. Frederic avait deja attendu deux
    minutes pour rien. Un rappel de point d'arret ne se compile pas : il
    faut l'executer. On l'execute donc ici, sur un faux contexte, et le
    controle refuse de passer si une sonde est cassee.
    """
    r.titre('9. LES SONDES, A VIDE')
    p = subprocess.run([sys.executable,
                        os.path.join('tools', 'sonde_vignettes.py'),
                        '--essai'], cwd=RACINE, capture_output=True,
                       text=True, errors='replace')
    for l in (p.stdout + p.stderr).splitlines():
        r.dire('    | %s' % l)
    if p.returncode:
        r.mauvais('sonde_vignettes.py', 'son rappel est casse (code %d)'
                  % p.returncode)
    r.bon('sonde_vignettes.py', 'le rappel et le rapport tiennent')


def controler_profil(r):
    r.titre('7. LE PROFIL PERSISTANT')
    chemin = os.path.join(JEU, 'quest_profil.bin')
    if not os.path.exists(chemin):
        r.voir('quest_profil.bin', 'absent -- normal tant que le Quest n a '
               'pas ete ouvert une fois ; il se cree au premier passage')
        return
    d = open(chemin, 'rb').read()
    if d[:8] != b'QUESTPRF':
        r.mauvais('quest_profil.bin', 'en-tete %r' % d[:8])
    v = struct.unpack_from('<I', d, 8)[0]
    r.bon('quest_profil.bin', 'version %d, %d octets' % (v, len(d)))
    if len(d) >= 0x250:
        perso, argent, w, l, grade = struct.unpack_from('<iiiii', d, 0x11C)
        r.dire('            perso %d, %d G, W %d, L %d, grade %d'
               % (perso, argent, w, l, grade))
        if argent < 0 or argent > 999999:
            r.mauvais('quest_profil.bin', 'argent %d hors 0..999999' % argent)


def controler_module(r):
    r.titre('8. LE MODULE apm.dll')
    chemin = os.path.join(JEU, 'apm.dll')
    if not os.path.exists(chemin):
        r.mauvais('apm.dll', 'absent')
    d = open(chemin, 'rb').read()
    if d[:2] != b'MZ':
        r.mauvais('apm.dll', 'ce n est pas un PE')
    # Le piege paye : un apm.dll construit en UTF-16 fait planter le jeu au
    # demarrage. Le nom exporte doit se lire en ASCII dans le fichier.
    for nom in (b'Input_isOn', b'Input_isOnNow', b'QUESTBOX'):
        if nom not in d:
            r.mauvais('apm.dll', 'le symbole %r est introuvable dans le '
                      'fichier -- construit en UTF-16 ?' % nom)
    r.bon('apm.dll', '%d octets, exports Input_isOn / Input_isOnNow, '
          'magie QUESTBOX presente' % len(d))


def main():
    argv = sys.argv[1:]
    r = Rapport()
    r.dire('CONTROLE DU MODE QUEST -- tout ce qui se verifie sans lancer '
           'le jeu')
    r.dire('atelier : %s' % RACINE)
    code = 0
    try:
        if '--tout' in argv:
            import subprocess as _sp
            del _sp
            r.titre('0. CONSTRUIRE')
            if _tourne():
                r.mauvais('vfes.exe', 'il TOURNE. On ne patche jamais un '
                          'moteur en cours d execution.')
            lancer(r, 'compilation du module',
                   [os.path.join('tools', 'gen_apm_stub.py')])
            for outil, opt in (('bases_2d.py', ['--ajouter'] + PLANCHES),
                               ('textes_quest.py', ['--ajouter']),
                               ('rivaux.py', ['--ajouter']),
                               ('musique_quest.py', ['--ajouter']),
                               ('objets_quest.py', ['--ecrire'])):
                chk = ['--controle'] if outil != 'objets_quest.py' else None
                if chk:
                    p = subprocess.run(
                        [sys.executable, os.path.join('tools', outil)] + chk,
                        cwd=RACINE, capture_output=True, text=True,
                        errors='replace')
                    if p.returncode == 0:
                        r.dire('  deja en place : %s' % outil)
                        continue
                lancer(r, outil, [os.path.join('tools', outil)] + opt)
            lancer(r, 'patch du moteur',
                   [os.path.join('tools', 'patch_moteur.py')] + LIGNE_QUEST)
        controler_module(r)
        controler_moteur(r)
        controler_libelles(r, '--rapide' in argv)
        controler_rivaux(r)
        controler_objets(r)
        controler_musique(r)
        controler_planches(r)
        controler_sondes(r)
        controler_profil(r)
        r.titre('BILAN')
        r.dire('  Aucun defaut. Tout ce qui se mesure sans ecran est en '
               'place.')
        r.dire('  Ce que ce controle NE dit PAS : que cela s affiche. Les '
               'lignes « A VOIR »')
        r.dire('  et tout le §4.1 du cahier des charges demandent un '
               'lancement.')
    except Defaut as e:
        r.titre('BILAN')
        r.dire('  ARRET AU PREMIER DEFAUT : %s' % e)
        code = 1
    except Exception as e:                                   # noqa: BLE001
        r.titre('BILAN')
        r.dire('  ERREUR DE L OUTIL : %s: %s' % (type(e).__name__, e))
        code = 2
    r.dire('')
    r.dire('rapport : %s' % os.path.relpath(RAPPORT, RACINE))
    r.ecrire()
    return code


def _tourne():
    try:
        p = subprocess.run(['tasklist', '/fi', 'IMAGENAME eq vfes.exe'],
                           capture_output=True, text=True, errors='replace')
        return 'vfes.exe' in p.stdout
    except OSError:
        return False


if __name__ == '__main__':
    sys.exit(main())
