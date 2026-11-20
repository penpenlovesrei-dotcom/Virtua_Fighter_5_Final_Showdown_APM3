#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""LES SIX VIGNETTES NOIRES : la sonde qui nomme la cause.

TOUT CE QUI SE MESURE SANS LANCER A ETE MESURE, et tous les maillons sont
SAINS (`py -3 tools/vignettes_costume.py` les imprime) :

  1. `0x1801CB030` batit sur la pile une table 19 x 6 d'identifiants de
     sprite et rend `table[personnage][type]` ;
  2. les 114 identifiants EXISTENT dans `spr_db` -- ce sont les
     `SPR_T_ITM<perso>_BODY01..06` ;
  3. leurs rangs pointent sur les SIX DERNIERS sprites de la planche
     (`BODY01`..`BODY06`, rangs 764 a 769 pour Akira) ;
  4. ces six images EXISTENT vraiment dans `spr_t_itmaki.farc`, verifie en
     sortant la planche du `.par` et en lisant ses 770 noms ;
  5. les dix-neuf planches sont dans le `.par`, dossier `2d` ;
  6. l'etat 40 de `CUST_MAIN` CHARGE la planche du personnage --
     `0x1801C3FCA` lit la table `0x18052FAE0` (45 = SPR_T_ITMAKI, 455, 456)
     et appelle `0x180187C50` ; aucun bouchon sur ce chemin ;
  7. notre `spr_db` n'a modifie AUCUNE entree existante (0 planche changee,
     0 sprite perdu) : ce n'est pas nous.

La cause est donc a l'EXECUTION, et il n'y a plus qu'une facon de la nommer.
Cette sonde mene le jeu toute seule jusqu'a TERMINAL > Customize, pose cinq
points d'arret, et ecrit ce qu'elle voit :

    0x180187C50   charger une planche      -> QUEL identifiant, combien de fois
    0x180187CC0   la planche est-elle prete ? -> l'identifiant interroge
    0x180187A30   decharger une planche    -> lequel, et QUAND
    0x1801CB030   l'identifiant de vignette demande -> la valeur rendue
    CreateFileW/A filtre sur « itm »       -> QUEL FICHIER est vraiment ouvert

Si `spr_t_itmaki` n'apparait jamais dans les fichiers ouverts, la planche
n'est pas trouvee. Si elle est ouverte mais que `0x180187CC0` rend toujours
faux, elle ne finit pas de charger. Si tout passe, c'est le RANG de dessin
et il faudra regarder le descripteur.

    py -3 tools/sonde_vignettes.py [--secondes N] [--directions]

LE SCENARIO MANUEL EST SAUVE AVANT ET REMIS APRES.
Sortie : `analysis/sonde_vignettes.txt` et les PNG dans `analysis/sonde/`.
"""
import os
import shutil
import struct
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                            # noqa: E402
import tracer_fichiers                                       # noqa: E402

JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
EXE = os.path.join(JEU, 'vfes.exe')
SCENARIO = os.path.join(JEU, 'apm_entrees.txt')
MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
JOURNAL = os.path.join(RACINE, 'analysis', 'sonde_vignettes.txt')
DOSSIER = os.path.join(RACINE, 'analysis', 'sonde')

# (rva, nom) -- les adresses sont des VA d'image, on retire la base.
ESPIONS = [
    (0x180187C50, 'charger', 'rcx'),      # ecx = l'identifiant de planche
    (0x180187CC0, 'pret ?', 'rcx'),       # ecx = l'identifiant interroge
    (0x180187A30, 'decharger', 'rcx'),    # ecx = l'identifiant
    (0x1801CB030, 'id vignette', 'rcx'),  # rcx = le type de costume
    # LE CURSEUR, ET C'EST LA MESURE QUI MANQUAIT A TOUT LE RESTE.
    # Deux correctifs ont ete poses sur le Character Select -- le compteur
    # (0x1801D0562) puis l'accepteur (creneau 8 de TaskDataSelector) -- et
    # gauche/droite ne bougent toujours pas. Au lieu de deviner un
    # troisieme verrou, on regarde ce que le repartiteur RECOIT :
    #
    #   0x1801BBBE0(rcx = la page)                 -> QUELLE page ?
    #   0x1801A2D60(rcx = &curseur, edx = compte,  -> le COMPTE est-il > 0 ?
    #               r8b = boucle)
    #
    # Si `edx` vaut 0, c'est encore le compteur, et sur une page que je n'ai
    # pas corrigee (la SOUS-PAGE CharSelector en +0x2A0, dont l'entree
    # 0x1801D0260 remet les quatre champs a zero, plutot que la tache mere).
    # Si `edx` vaut 18 et que rien ne bouge, c'est l'accepteur.
    (0x1801BBBE0, 'repartiteur', 'rcx'),
    (0x1801A2D60, 'curseur H', 'rcx,rdx,r8'),
    (0x1801A2EC0, 'curseur V', 'rcx,rdx,r8'),
    # AJOUTES LE 2026-10-01, ET POUR UNE RAISON PRECISE. Le relais du compte
    # de `DataSelector` est bien dans le binaire (le controle le verifie
    # octet par octet) et pourtant la page tourne 149 fois sans que le
    # curseur vertical soit APPELE une seule fois -- donc son compte vaut
    # toujours zero a l'execution. Deux lectures restent : ou bien l'entree
    # de la page n'est jamais appelee et le relais ne tourne pas, ou bien
    # quelque chose remet le compte a zero apres elle. Un espion sur chacune
    # les separe.
    (0x1801D0280, 'entree DataSel', 'rcx'),
    (0x1801D01D0, 'accepteur H DataSel', 'rcx'),
]
# TERMINAL est l'entree 4 du menu principal (menu_console.md §8.4) : quatre
# « bas » depuis l'entree 0, puis valider. Puis Customize est la premiere
# ligne de la page TERMINAL, donc valider encore. Appuis de 80 ms : a 200 ms
# la repetition du menu fait descendre de DEUX crans (mesure sonde_decor).
OUVERTURE = ([(20.0, 'start'), (24.0, 'start'), (28.0, 'start')]
             + [(33.0 + 0.8 * i, 'bas') for i in range(4)]
             + [(37.0, 'start'),    # ouvrir TERMINAL
                (39.0, 'start')])   # valider « Customize »


def appuis(mode):
    """Le scenario d'appuis. Deux modes, et le second existe a cause d'une
    mesure.

    TROIS ESSAIS, TROIS LECONS.

    1. Six appuis a un instant precis (t=48..54). Rates : le demarrage avait
       decale le scenario de trois secondes et demie et le Character Select
       n'etait actif que 51 trames. UN INSTANT PRECIS NE RESISTE PAS A UN
       DEMARRAGE QUI VARIE.

    2. Martelage ALTERNE gauche/droite. Le curseur a bien bouge -- 0 <-> 18,
       Akira <-> T-Arashi a l'ecran -- mais JAMAIS un cran intermediaire :
       gauche depuis 0 et droite depuis 18 rebouclent toutes deux sur l'autre
       butee. « Il decremente avec rebouclage » et « il saute a la butee »
       donnent exactement la meme trace. UNE TRACE COMPATIBLE AVEC DEUX
       LECTURES NE MESURE RIEN.

    3. Douze droites groupees, de t=40,0 a t=53,2. Rate aussi, et pour une
       raison nouvelle : le Character Select n'a vecu que 75 trames, ouvert a
       t=42,4 et VALIDE a t=42,6. Les douze droites sont tombees dans le
       « Costume settings », ou le curseur horizontal n'a pas de compte et ne
       bouge donc pas -- en silence.

    POURQUOI LES DEUX HORLOGES NE SONT PAS LA MEME. apm.dll date ses appuis
    avec `GetTickCount() - g_t0`, et `g_t0` est pris au PREMIER appel de
    `Input_isOn` ; la sonde, elle, compte depuis la creation du processus.
    L'ecart entre les deux varie de plusieurs secondes d'un lancement a
    l'autre. Deux essais au scenario identique ont donne au Character Select
    2065 trames puis 75.

    ET POURQUOI UN APPUI PEUT VALIDER DEUX ECRANS. `Input_isOnNow` n'est pas
    un bit de front dans notre stub mais une FENETRE DE TEMPS de `front`
    millisecondes (le vrai front a ete essaye et le jeu ne quittait plus
    APM3_ENTRY -- c'est ecrit dans gen_apm_stub.py). Un ecran qui s'ouvre
    pendant la fenetre voit le meme appui et se valide a son tour.

    LE MODE « directions » EN TIRE LES CONSEQUENCES : plus aucun `start`
    apres l'ouverture, donc rien qui puisse quitter l'ecran ; et des droites
    TOUTES LES 0,3 s DE t=38 A t=100, pour qu'un ecran qui ne vivrait qu'une
    seconde en recoive quand meme trois. Une droite ne valide rien et ne
    ferme rien : la marteler partout ne coute que du temps.
    """
    if mode == 'directions':
        n = int((100.0 - 38.0) / 0.3) + 1
        return OUVERTURE + [(38.0 + 0.3 * i, 'droite') for i in range(n)]
    return (OUVERTURE
            + [(40.0 + 1.2 * i, 'droite') for i in range(12)]
            + [(54.4 + 1.2 * i, 'gauche') for i in range(6)]
            + [(62.0, 'start')]       # valider le personnage : la main passe
                                      # aux CINQ lignes de donnees
            # LES CINQ LIGNES `---`. Leur compte vertical vient d'etre pose
            # par relais (DATASELECTOR_COMPTE). Six BAS pour faire le tour
            # des cinq crans et reboucler : le cadre doit descendre.
            + [(63.0 + 0.7 * i, 'bas') for i in range(6)]
            + [(68.0, 'start'),
               (80.0, 'piece'),       # la barre espace : Customization menu
               (82.0, 'bas'),         # « Costume settings »
               (84.0, 'start')]
            # ET UNE FOIS DANS « Costume settings », ON MARTELE AUSSI.
            # C'est le nouvel ecran a verifier : son compte horizontal
            # n'existait pas (il n'y avait meme rien a neutraliser, il a
            # fallu ECRIRE le calcul -- CURSEUR_REBATI). Si le correctif
            # tient, le cadre de selection doit passer de Type A a Type B,
            # C, D... et le libelle en bas changer avec lui.
            + [(88.0 + 1.5 * i, 'droite') for i in range(10)])


CODES = {'bas': 3, 'start': 7, 'piece': 6, 'carre': 8,
         'gauche': 4, 'droite': 5}


def scenario(mode='complet'):
    l = ['# ecrit par tools/sonde_vignettes.py -- remis apres la sonde']
    for k, c in sorted(CODES.items(), key=lambda kv: kv[1]):
        l.append('nom %-6s = %d' % (k, c))
    l += ['front   = 20', 'journal = 0', 'clavier = 0', 'manette = 0',
          '', '0       rien']
    h = []
    for t, k in appuis(mode):
        ms = int(t * 1000)
        h += [(ms, '%-7d %s' % (ms, k)), (ms + 80, '%-7d rien' % (ms + 80))]
    l += [x for _, x in sorted(h)]
    txt = '\n'.join(l) + '\n'
    txt.encode('ascii')                  # verifier AVANT d'ouvrir en ecriture
    return txt


ETAT_ENTREES = 0x180751040          # l'etat d'entrees, 0x54 par joueur
ETAT_REPETITION = 0x18             # ce que le deplaceur de curseur LIT
ETAT_FRONT = 0x10


# Les vtables des pages du parcours TERMINAL > Customize, par leur VA dans
# l'image non rebasee. La sonde lit `[page]` et donne ainsi le NOM de la page,
# au lieu de me laisser deduire sa classe d'une soustraction de pointeurs --
# ce que j'ai fait le 2026-10-01, et mal : j'ai pris pour `DataSelector` une
# page reconnue au seul ecart `0x550` avec sa mere.
VTABLES = {
    0x180530FF0: 'TaskDataSelector', 0x180530F30: 'CharSelector',
    0x180530F90: 'DataSelector', 0x180530420: 'TaskCustomizeMenu',
    0x1805303C0: 'TaskCostumeMenu', 0x1805304E0: 'TaskSelItemMenu',
    0x180530540: 'TaskSelPartMenu', 0x180530360: 'TaskExclWarning',
    0x180530480: 'TaskHelpWindow', 0x180532A28: 'TaskMenuTerminal',
}


def _dire_page(d, et, ctx):
    """Nomme la page que le repartiteur recoit, et dit ses deux comptes.

    C'est la mesure qui manquait : `COMPTE=` n'apparait que si le curseur
    est APPELE, donc jamais quand le compte vaut zero -- et une page sans
    compte reste muette, indistinguable d'une page absente. Ici on lit le
    compte a la source, a chaque changement.
    """
    base = d.base_de(MOTEUR) if hasattr(d, 'base_de') else None
    if not base:
        return
    try:
        vt = struct.unpack('<Q', d.read(ctx.Rcx, 8))[0]
        v = d.u32(ctx.Rcx + 0x224)
        h = d.u32(ctx.Rcx + 0x22C)
    except Exception:                                        # noqa: BLE001
        return
    va = vt - base + 0x180000000
    nom = VTABLES.get(va, 'inconnue 0x%X' % va)
    cle = (nom, v, h)
    if cle in et.setdefault('pages', set()):
        return
    et['pages'].add(cle)
    d.dire('  PAGE       t=%6.1f %-18s V=%-4d H=%-4d  (vtable 0x%X)'
           % (time.time() - et.get('t0', 0), nom, v, h, va))


def _dire_curseur(d, et, nom, compte, ctx):
    """Imprime un passage du deplaceur, mais seulement s'il apprend quelque
    chose : le curseur a bouge, ou une touche repetable est tenue."""
    base = d.base_de(MOTEUR) if hasattr(d, 'base_de') else None
    rep = front = 0
    if base:
        o = base + (ETAT_ENTREES - 0x180000000)
        try:
            rep, front = d.u32(o + ETAT_REPETITION), d.u32(o + ETAT_FRONT)
        except Exception:                                    # noqa: BLE001
            rep = front = 0
    try:
        cur = d.u32(ctx.Rcx)
    except Exception:                                        # noqa: BLE001
        cur = -1
    cle = (nom, ctx.Rcx)
    avant = et['curseur'].get(cle)
    et['curseur'][cle] = cur
    bouge = avant is not None and avant != cur
    if not (bouge or rep or front):
        return
    # Le plafond etait a 60 lignes, soit une trentaine de deplacements : trop
    # peu pour le mode « directions », qui envoie plus de deux cents droites
    # et dont TOUTE la demonstration tient dans la SUITE des crans visites.
    vus = et['imp'].get(nom, 0)
    if vus >= et.get('max_lignes', 60):
        return
    et['imp'][nom] = vus + 1
    d.dire('  %-10s t=%6.1f COMPTE=%-3d curseur=%-3d%s  rep=0x%06X '
           'front=0x%06X  page=0x%X'
           % (nom, time.time() - et.get('t0', 0), compte, cur,
              ' <<< A BOUGE' if bouge else '', rep & 0xFFFFFF,
              front & 0xFFFFFF,
              ctx.Rcx - (0x58 if nom.startswith('curseur V') else 0x5C)))


class _FauxContexte:
    """Juste ce que le rappel lit d'un CONTEXT."""
    Rcx = 0x2D
    Rdx = 18
    R8 = 1
    Rax = 0


class _FauxDebogueur:
    """Un debogueur qui ne debogue rien : il encaisse les appels."""

    def __init__(self):
        self.lignes = []

    def dire(self, txt):
        self.lignes.append(txt)

    def base_de(self, nom):
        return 0x180000000

    def u32(self, adresse):
        return 0x22000

    def read(self, adresse, n):
        # PAS b'' : un lecteur qui rend toujours du vide ne fait pas tourner
        # les rappels qui DESEMPILENT ce qu'ils lisent. `_dire_page` fait un
        # `struct.unpack('<Q', ...)` -- avec b'' il part en exception et
        # l'essai a vide ne prouve plus rien, puisque le rappel l'attrape.
        # On rend donc n octets credibles : une vtable connue.
        return struct.pack('<Q', 0x180530F90)[:n].ljust(n, bytes(1))


def _essai_a_vide(sur_bp, et):
    """Fait tourner le rappel et le rapport sur un faux contexte.

    Rend False, en expliquant, si quoi que ce soit leve. C'est le controle
    qui manquait : un rappel de point d'arret ne se compile pas, il faut
    l'executer.
    """
    class _Bp:
        def __init__(self, nom):
            self.nom = nom

    d, ctx = _FauxDebogueur(), _FauxContexte()
    try:
        for _, nom, _regs in ESPIONS:
            for _ in range(3):
                sur_bp(d, _Bp('espion:' + nom), ctx, 0)
        sur_bp(d, _Bp('CreateFileW'), ctx, 0)
        sur_bp(d, _Bp('CreateFileA'), ctx, 0)
        # et le rapport, qui est ce qui avait plante la deuxieme fois
        for (nom, arg), m in sorted(et['par_id'].items(),
                                    key=lambda kv: (kv[0][0], -kv[1])):
            '%-12s id=0x%-5X %d' % (nom, arg, m)
        for nom, n in sorted(et['compte'].items()):
            '%-14s %d' % (nom, n)
    except Exception as e:                                   # noqa: BLE001
        print()
        print('ESSAI A VIDE : LE RAPPEL DE LA SONDE EST CASSE.')
        print('   %s: %s' % (type(e).__name__, e))
        print()
        print('Le jeu n a PAS ete lance. Corrigez tools/sonde_vignettes.py,')
        print('puis `py -3 tools/sonde_vignettes.py --essai` pour verifier.')
        return False
    # l'essai ne doit rien laisser derriere lui
    et['compte'].clear()
    et['par_id'].clear()
    et['fichiers'].clear()
    return True


def main():
    a = sys.argv[1:]
    secondes = int(a[a.index('--secondes') + 1]) if '--secondes' in a else 110
    os.makedirs(DOSSIER, exist_ok=True)
    # t=42 a t=58 : cinq images espacees de quatre secondes, donc d'un peu
    # plus de trois appuis. Si le Character Select defile vraiment, chacune
    # doit porter un nom de personnage DIFFERENT et plus loin dans la liste
    # que la precedente. t=70 et au-dela : le « Costume settings » du
    # selecteur -- celui qui etait noir, et qui ne l'est plus.
    mode = 'directions' if '--directions' in a else 'complet'
    if mode == 'directions' and '--secondes' not in a:
        secondes = 115
    # En mode « directions » on ne cherche plus les vignettes -- elles sont
    # validees -- mais le NOM du personnage, qui doit avancer d'une capture a
    # l'autre. Dix images de t=44 a t=98 : a 0,3 s par droite, chacune est
    # separee de la precedente par une vingtaine de crans, donc par un nom
    # franchement different. Si deux images voisines portent le meme nom,
    # c'est que le curseur ne defile pas.
    prefixe, instants = (('directions_t%03d.png',
                          (44, 50, 56, 62, 68, 74, 80, 86, 92, 98))
                         if mode == 'directions'
                         else ('vignettes_t%03d.png',
                               (42, 46, 50, 54, 58, 64, 66, 70, 76, 88,
                                91, 94, 97, 100, 103)))
    captures = [(os.path.join(DOSSIER, prefixe % t), float(t),
                 'Virtua Fighter')
                for t in instants if t < secondes - 2]

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = True
    dbg.bp_max = 400000
    fichier = open(JOURNAL, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'poses': set(), 'compte': {}, 'fichiers': {},
          'par_id': {}, 'regs': {n: r for _, n, r in ESPIONS},
          'curseur': {}, 'imp': {}, 't0': time.time(),
          'max_lignes': 300 if mode == 'directions' else 60}

    def sur_bp(d, bp, ctx, tid):
        if bp.nom.startswith('espion:'):
            nom = bp.nom[7:]
            n = et['compte'].get(nom, 0) + 1
            et['compte'][nom] = n
            regs = et['regs'].get(nom, 'rcx')
            if regs == 'rcx':
                arg = ctx.Rcx & 0xFFFFFFFF
            else:
                # (page, compte, boucle) : la cle est le COMPTE, c'est lui
                # qu'on cherche. L'adresse de la page part dans le texte.
                arg = ctx.Rdx & 0xFFFFFFFF
            # LA BORNE QUI M'AVAIT AVEUGLE. Le premier jet n'imprimait que
            # les 24 premiers passages de chaque espion : `pret ?` en compte
            # des centaines, et je n'ai donc jamais su si quelqu'un
            # interrogeait la planche du personnage (0x2D) pendant le
            # selecteur. On suit maintenant CHAQUE identifiant separement,
            # et on imprime les premiers de chacun -- plus un compte par
            # identifiant, imprime a la fin.
            cle = (nom, arg)
            m = et['par_id'].get(cle, 0) + 1
            et['par_id'][cle] = m
            if nom == 'repartiteur':
                _dire_page(d, et, ctx)
            if m <= 6:
                if regs == 'rcx':
                    d.dire('  %-12s #%-4d id=0x%X (%d)   [%d-e pour cet id]'
                           % (nom, n, arg, arg, m))
                else:
                    _dire_curseur(d, et, nom, arg, ctx)
            elif regs != 'rcx':
                # LES SIX PREMIERS NE SUFFISENT PAS, ET J'AI LU MA PROPRE
                # MESURE DE TRAVERS A CAUSE DE CA : ils tombent a l'ouverture
                # de la page, bien avant le moindre appui, et « curseur = 0 »
                # n'y prouve rien. On imprime donc desormais quand le curseur
                # CHANGE, ou quand une touche repetable est tenue -- avec
                # l'instant, et l'etat d'entrees lu au meme moment.
                _dire_curseur(d, et, nom, arg, ctx)
            return
        adr = ctx.Rcx                    # CreateFile : 1er argument
        if not adr:
            return
        brut = d.read(adr, 520)
        if not brut:
            return
        if bp.nom.endswith('W'):
            t = brut.decode('utf-16-le', 'ignore').split('\x00', 1)[0]
        else:
            t = brut.split(b'\x00', 1)[0].decode('latin-1', 'ignore')
        if not t or 'itm' not in t.lower():
            return
        if t not in et['fichiers']:
            d.dire('  FICHIER : %s' % t)
        et['fichiers'][t] = et['fichiers'].get(t, 0) + 1

    def tic(d, t):
        b = d.base_de(MOTEUR)
        if b and not et['pose']:
            et['pose'] = True
            for va, nom, _regs in ESPIONS:
                bp = instrument.PointArret('espion:' + nom,
                                           b + (va - 0x180000000),
                                           max_coups=100000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)
            d.dire('  %d point(s) d arret poses a t=%.0f s' % (len(ESPIONS), t))
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

    # L'ESSAI A VIDE, ET POURQUOI IL EXISTE.
    # Le 2026-10-01 la sonde a plante APRES avoir lance le jeu, sur un
    # `KeyError: 'regs'` -- une cle que j'avais oublie d'ajouter au
    # dictionnaire d'etat. Frederic avait deja attendu deux minutes. Le
    # rappel de point d'arret ne se compile pas : il faut l'EXECUTER pour
    # savoir qu'il tient. On l'execute donc ici, sur un faux contexte, avant
    # d'ouvrir quoi que ce soit. `--essai` s'arrete apres.
    if not _essai_a_vide(sur_bp, et):
        return 2
    if '--essai' in a:
        print('essai a vide : le rappel et le rapport tiennent. '
              'Rien n a ete lance.')
        return 0

    sauve = SCENARIO + '.avant_sonde'
    shutil.copyfile(SCENARIO, sauve)
    try:
        with open(SCENARIO, 'w', encoding='ascii', newline='\n') as fp:
            fp.write(scenario(mode))
        print('sonde (%s) : %d s, %d capture(s), %d appui(s)'
              % (mode, secondes, len(captures), len(appuis(mode))))
        et['t0'] = time.time()          # les instants comptent d'ICI
        et['imp'].clear()
        dbg.run(EXE, os.path.dirname(EXE), secondes, tuple(captures))
    finally:
        shutil.copyfile(sauve, SCENARIO)
        os.remove(sauve)
        fichier.write('\n')
        refusees = getattr(dbg, '_captures_refusees', 0)
        if refusees:
            avis = ('\n!!! %d CAPTURE(S) REFUSEE(S) : la fenetre du jeu etait recouverte.'
                    '\n    Les images manquent, et la mesure visuelle de cette'
                    ' passe ne vaut rien.\n    Relancez sans rien laisser'
                    ' par-dessus le jeu.\n' % refusees)
            print(avis)
            fichier.write(avis)
        fichier.write('COMPTES\n')
        for nom, n in sorted(et['compte'].items()):
            fichier.write('  %-14s %d passage(s)\n' % (nom, n))
        fichier.write('\nPAR IDENTIFIANT -- le tableau qui manquait\n')
        for (nom, arg), m in sorted(et['par_id'].items(),
                                    key=lambda kv: (kv[0][0], -kv[1])):
            fichier.write('  %-12s id=0x%-5X %d passage(s)\n'
                          % (nom, arg, m))
        fichier.write('FICHIERS OUVERTS CONTENANT « itm » : %d\n'
                      % len(et['fichiers']))
        for t, n in sorted(et['fichiers'].items()):
            fichier.write('  %-60s %d\n' % (t, n))
        fichier.close()

    print()
    for nom, n in sorted(et['compte'].items()):
        print('  %-14s %d passage(s)' % (nom, n))
    print()
    print('  LA PLANCHE DU PERSONNAGE (identifiants 45, 455, 456) :')
    vus = [(nom, arg, m) for (nom, arg), m in et['par_id'].items()
           if arg in (45, 455, 456)]
    if not vus:
        print('    aucun passage -- elle n est ni chargee ni interrogee.')
    for nom, arg, m in sorted(vus):
        print('    %-12s id=%-4d %d passage(s)' % (nom, arg, m))
    print()
    if not et['fichiers']:
        print('  Aucun fichier « itm » ouvert -- ce qui ne prouve RIEN : le')
        print('  moteur lit la planche depuis vf5fs_data.par, deja ouvert.')
    else:
        print('  %d fichier(s) « itm » ouvert(s) :' % len(et['fichiers']))
        for t in sorted(et['fichiers']):
            print('    %s' % t)
    print()
    print('journal : %s' % os.path.relpath(JOURNAL, RACINE))
    print('captures : %s' % os.path.relpath(DOSSIER, RACINE))
    return 0


if __name__ == '__main__':
    sys.exit(main())
