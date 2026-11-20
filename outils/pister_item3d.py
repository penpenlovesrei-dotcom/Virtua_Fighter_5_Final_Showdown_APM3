#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""POURQUOI LE MODELE 3D D'UN OBJET NE SE POSE PAS SUR LE PERSONNAGE.

Frederic, 2026-10-04 : « une fois un item selectionne, son modele 3D n'est pas
charge sur le personnage ».

LA QUESTION, ET ELLE N'A QUE DEUX REPONSES :

    le jeu DEMANDE l'archive `<perso>itm` et n'y arrive pas   -> resolution
    le jeu ne la demande JAMAIS                               -> chargeur mort

Les deux appellent des reparations opposees, et aucune analyse statique ne
tranche : il faut regarder le jeu le faire.

CE QUI EST DEJA ECARTE (journal 100) :

  . les DONNEES SONT LA -- `akiitm.farc` fait 26 Mo et `akiitm_patch.farc`
    103 Mo dans `vf5fs_data.par`, soit 62 fichiers « itm » en tout, et
    `chritm_tbl` porte 14 444 objets sur 20 personnages ;
  . les CRENEAUX 5 ET 6 des vtables sont des bouchons `ret 0` sur TOUTES les
    pages de personnalisation, y compris `TaskCostumeMenu` dont le costume
    s'applique tres bien. Ce n'est pas la cause ;
  . `0x1801CBFE0` n'est pas le chargeur du modele : il construit les marqueurs
    AET `head_s`/`face_s`/`arm_s`... c'est l'animation 2D de la fenetre.

POURQUOI PAS `sonde_vignettes.py`. Elle espionne `CreateFile`, et son propre
rapport le dit : « Aucun fichier itm ouvert -- ce qui ne prouve RIEN », parce
que le moteur lit dans `vf5fs_data.par`, deja ouvert. Aucun appel systeme n'en
sort. L'espion doit se poser sur le RESOLVEUR DE NOMS, en amont.

OU ON SE POSE, ET POURQUOI LA.

`0x180218004` resout un nom d'archive d'objset en identifiant, par dichotomie
dans une table TRIEE de 0x35E = 862 entrees de seize octets basee en
`0x18054BB30`. C'est la SEULE reference de tout le binaire a la plage ou
vivent les chaines `objset/aki`, `objset/akiitm`, `objset/akiitm_patch` --
mesure de `refs_plage.py`, une seule reference pour 4096 octets.

On se pose en `0x18021805E`, juste apres que `rbx` ait recu le nom recopie
(`0x180218059 lea rbx, [rsp+0x20]`) et avant la dichotomie : UN passage par
recherche, et le nom est lisible. Se poser dans la boucle en aurait donne dix
par recherche, pour rien.

LE CLAVIER VOUS RESTE. La sonde ne conduit pas le jeu -- c'est a vous d'aller
dans TERMINAL > Customize et de choisir un objet. Le journal s'ecrit AU FIL DE
L'EAU : meme si le debogueur se bloque, ce qui a ete vu est sur le disque.

Usage :
    py -3 tools/pister_item3d.py [--secondes 420] [--tout]

`--tout` ne filtre plus sur « itm » et montre TOUS les objsets demandes --
a utiliser si le relevé filtre revient vide, pour prouver que l'espion est
bien pose et que la fonction est bien celle qui tourne.
"""
import os
import time
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                            # noqa: E402

JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
EXE = os.path.join(JEU, 'vfes.exe')
MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
BASE_PREF = 0x180000000
JOURNAL = os.path.join(RACINE, 'analysis', 'pister_item3d.txt')

# L'espion : apres `lea rbx, [rsp+0x20]`, avant la dichotomie. `rbx` porte le
# nom recopie, termine par zero.
RESOLVEUR_OBJSET = 0x18021805E
# L'ENTREE REELLE de la meme fonction (`pe_disasm back`), ou `[rsp]` porte
# encore l'adresse de RETOUR : c'est elle qui nomme le demandeur. Les deux
# espions sont dans la meme fonction et passent dans l'ordre entree -> nom,
# sur le meme fil : le dernier retour vu est bien celui du nom qui suit.
RESOLVEUR_ENTREE = 0x180217E70

# LA CHAINE D'EQUIPEMENT, trouvee par le RTTI : `customize::ItmEqTask`
# (vtable 0x180530D10) est la tache qui pose un objet sur le modele. Sa mise
# a jour est une machine a CINQ etats dans `[this+0x58]`, et l'etat 0 ne fait
# RIEN -- or c'est la valeur que son init (creneau 1, 0x180150A20) y pose.
# Elle est demarree par `customize::ItemMain::update` (0x1801C2EC0), elle-meme
# une machine a 0x29 etats par table de saut, qui prend le singleton
# (0x1801C5C50) puis appelle 0x1801C5DB0.
#
# DEUX GARDES la precedent : 0x180187CC0(0x26B) et 0x180029D40(0x20B). Ce ne
# sont PAS des bouchons -- elles consultent un gestionnaire avec un
# identifiant et lisent [rax+0x48] : une attente d'animation, legitime. D'ou
# la mesure plutot que la supposition.
ITEMMAIN_ETAT = 0x1801C2ECA      # movsxd rax, [rcx+0x58]
ITMEQ_ETAT = 0x1801C13DA         # mov ecx, [rcx+0x58]
ITMEQ_DEMARRAGE = 0x1801C2F1C    # le call qui lance la tache

# LE DRAPEAU, et comment on le lit a l'execution. `0x180C3B6F0` porte un
# POINTEUR vers le tableau des joueurs (0xFA88 par joueur) ; `+0x796` est le
# drapeau du joueur 1, `+0x1021E` celui du joueur 2. On les relit a chaque
# passage de la tache : c'est la seule facon de distinguer « le drapeau n'est
# pas pose » de « il est pose et ca ne suffit pas ».
GLOBALE_JOUEURS = 0x180C3B6F0
DRAPEAU_J1 = 0x796
DRAPEAU_J2 = 0x1021E
POSE_DRAPEAU = 0x180143859       # le site que --joueur-pret detourne
# Le jeu met une bonne vingtaine de secondes a atteindre le menu.
DELAI_POSE = 30.0


def main():
    a = sys.argv[1:]
    secondes = int(a[a.index('--secondes') + 1]) if '--secondes' in a else 420
    global DELAI_POSE
    if '--delai' in a:
        DELAI_POSE = float(a[a.index('--delai') + 1])
    tout = '--tout' in a
    sans_pose = '--sans-pose' in a

    # ON N'ECRASE PLUS LE JOURNAL PRECEDENT. Le 2026-10-04, une passe lancee
    # ici pendant que Frederic essayait de son cote a efface SA mesure : le
    # journal s'ouvrait en 'w', sans rien garder. Chaque passe archive donc
    # maintenant la precedente sous son horodatage, et `pister_item3d.txt`
    # reste le dernier en date. Une mesure qui demande d'aller a l'ecran ne
    # doit pas pouvoir disparaitre par inadvertance.
    if os.path.exists(JOURNAL) and os.path.getsize(JOURNAL):
        vieux = '%s.%s.txt' % (
            JOURNAL[:-4],
            time.strftime('%Y%m%d-%H%M%S',
                          time.localtime(os.path.getmtime(JOURNAL))))
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
        fichier.flush()                       # AU FIL DE L EAU, toujours

    dbg.dire = dire
    dbg.bp_max = 2000000
    et = {'pose': False, 'noms': {}, 'itm': {}, 'retour': {},
          'demandeurs': {}, 'main': None, 'eq': None, 'lance': 0,
          'vus_main': set(), 'vus_eq': set(), 'pose': 0, 'drap': None,
          'poseurs': {}}

    def sur_bp(d, bp, ctx, tid):
        # LES TROIS ESPIONS DE LA CHAINE D'EQUIPEMENT. On n'imprime que les
        # CHANGEMENTS : ces machines tournent a chaque trame, et un journal
        # qui repete le meme etat soixante fois par seconde ne se lit pas.
        if bp.nom == 'ItemMain':
            v = ctx.Rcx
            e = d.read(v + 0x58, 4)
            if e:
                n = int.from_bytes(e, 'little')
                if n != et['main']:
                    et['main'] = n
                    et['vus_main'].add(n)
                    d.dire('  ItemMain   -> etat %d' % n)
            return
        if bp.nom == 'pose drapeau':
            et['pose'] += 1
            # QUEL JOUEUR EST VISE, ET L'ECRITURE PREND-ELLE ? Au site,
            # `rcx` = index * 0xFA88 et `rax` = la base des joueurs. On
            # imprime l'index effectif, et on RELIT l'octet juste apres pour
            # voir si le stub a vraiment ecrit. Un code qui passe 2164 fois
            # sans que le drapeau bouge ne laisse pas d'autre question.
            idx = ctx.Rcx // 0xFA88 if ctx.Rcx else 0
            cle = (idx, ctx.Rax)
            if cle not in et['poseurs'] and len(et['poseurs']) < 12:
                et['poseurs'][cle] = et['pose']
                apres = d.read(ctx.Rax + ctx.Rcx + DRAPEAU_J1, 1)
                d.dire('  >>> POSE : joueur %d  base=0x%X  octet avant=%s'
                       % (idx, ctx.Rax,
                          apres[0] if apres else '?'))
            return
        if bp.nom == 'ItmEqTask':
            b = d.base_de(MOTEUR)
            if b:
                g = d.read(b + (GLOBALE_JOUEURS - BASE_PREF), 8)
                if g:
                    ptr = int.from_bytes(g, 'little')
                    if ptr:
                        d1 = d.read(ptr + DRAPEAU_J1, 1)
                        d2 = d.read(ptr + DRAPEAU_J2, 1)
                        # LE VOISIN +0x795, celui qui a GARDE son poseur.
                        # S'il vaut 1 et pas le notre, c'est notre stub qui
                        # n'ecrit pas ; si les deux sont a zero, c'est la
                        # fonction qui ne passe pas. Sans ce temoin on ne
                        # peut pas les distinguer.
                        t1 = d.read(ptr + DRAPEAU_J1 - 1, 1)
                        v = (d1[0] if d1 else -1, d2[0] if d2 else -1,
                             t1[0] if t1 else -1)
                        if v != et['drap'] or ptr != et.get('ptr'):
                            et['drap'] = v
                            et['ptr'] = ptr
                            d.dire('  DRAPEAUX   -> +0x796 j1=%d j2=%d  |  '
                                   'temoin +0x795 j1=%d   (base=0x%X)'
                                   % (v[0], v[1], v[2], ptr))
            e = d.read(ctx.Rcx + 0x58, 4)
            if e:
                n = int.from_bytes(e, 'little')
                if n != et['eq']:
                    et['eq'] = n
                    et['vus_eq'].add(n)
                    d.dire('  ItmEqTask  -> etat %d' % n)
            return
        if bp.nom == 'demarrage':
            et['lance'] += 1
            d.dire('  >>> LA TACHE D EQUIPEMENT EST DEMARREE (%d-e fois)'
                   % et['lance'])
            return
        if bp.nom == 'entree resolveur':
            pile = d.read(ctx.Rsp, 8)
            if pile:
                et['retour'][tid] = int.from_bytes(pile, 'little')
            return
        brut = d.read(ctx.Rbx, 64)
        if not brut:
            return
        nom = brut.split(b'\x00', 1)[0].decode('latin-1', 'ignore')
        if not nom:
            return
        et['noms'][nom] = et['noms'].get(nom, 0) + 1
        vise = 'itm' in nom.lower()
        if vise:
            et['itm'][nom] = et['itm'].get(nom, 0) + 1
        if not (tout or vise):
            return
        # On n'imprime que les PREMIERS passages de chaque nom : la fonction
        # est appelee des milliers de fois et un journal noye ne se lit pas.
        n = et['noms'][nom]
        ret = et['retour'].get(tid)
        if vise and ret:
            b = d.base_de(MOTEUR)
            # On rend l'adresse a la base PREFEREE : la DLL est rebasee a
            # l'execution, et une adresse vive ne se retrouve dans aucun
            # desassemblage.
            if b and b <= ret < b + 0x2000000:
                va = BASE_PREF + (ret - b)
            else:
                va = ret
            cle = (nom, va)
            et['demandeurs'][cle] = et['demandeurs'].get(cle, 0) + 1
        if n <= 3:
            ou = ''
            if vise and ret:
                ou = '   demande par 0x%X' % va
            d.dire('  OBJSET DEMANDE : %-40s (%d-e fois)%s' % (nom, n, ou))

    def tic(d, t):
        # ON NE POSE PAS L'ESPION TOUT DE SUITE. Le resolveur est appele des
        # milliers de fois pendant le chargement initial, et chaque point
        # d'arret logiciel coute une exception plus une reprise : pose des la
        # DLL chargee, il rendrait le demarrage -- deja lent -- insupportable,
        # et noierait le journal sous les objsets du titre. On attend donc que
        # le jeu soit arrive au menu.
        if t < DELAI_POSE:
            return
        b = d.base_de(MOTEUR)
        if b and not et['pose']:
            et['pose'] = True
            bp = instrument.PointArret('resolveur objset',
                                       b + (RESOLVEUR_OBJSET - BASE_PREF),
                                       max_coups=2000000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
            bpe = instrument.PointArret('entree resolveur',
                                        b + (RESOLVEUR_ENTREE - BASE_PREF),
                                        max_coups=2000000)
            bpe.silencieux = True
            d.bps.append(bpe)
            d.armer_logiciel(bpe)
            for va_e, nom_e in ((ITEMMAIN_ETAT, 'ItemMain'),
                                (ITMEQ_ETAT, 'ItmEqTask'),
                                (ITMEQ_DEMARRAGE, 'demarrage'),
                                (POSE_DRAPEAU, 'pose drapeau')):
                # L'ESPION QUI PEUT CASSER CE QU'IL OBSERVE. `POSE_DRAPEAU`
                # est l'adresse meme ou `--joueur-pret` a pose son `jmp` : y
                # mettre un point d'arret, c'est ecrire 0xCC sur le premier
                # octet du saut, et la reprise du debogueur doit le restaurer
                # avant de le franchir. `--sans-pose` le retire, pour pouvoir
                # distinguer « le correctif n'ecrit pas » de « la sonde
                # l'empeche d'ecrire ». Sans cette option, un drapeau reste a
                # zero sans qu'on sache lequel des deux est en cause.
                if nom_e == 'pose drapeau' and sans_pose:
                    continue
                bq = instrument.PointArret(nom_e, b + (va_e - BASE_PREF),
                                           max_coups=2000000)
                bq.silencieux = True
                d.bps.append(bq)
                d.armer_logiciel(bq)
            d.dire('  six espions poses a t=%.0f s' % t)
            d.dire('  LE CLAVIER EST A VOUS : TERMINAL > Customize, puis')
            d.dire('  choisissez un objet et regardez le personnage.')

    dbg.on_bp = sur_bp
    dbg.tic = tic

    print('sonde item3d : %d s, le clavier vous reste.' % secondes)
    print('journal : %s' % os.path.relpath(JOURNAL, RACINE))
    try:
        dbg.run(EXE, JEU, secondes, ())
    finally:
        fichier.write('\n')
        fichier.write('=' * 70 + '\n')
        if et['itm']:
            fichier.write('LE JEU A DEMANDE CES ARCHIVES D OBJETS :\n')
            for nom, n in sorted(et['itm'].items()):
                fichier.write('  %-44s %d fois\n' % (nom, n))
            fichier.write('\nDonc la demande PART. Si le modele ne s affiche'
                          ' pas, le defaut est en AVAL : resolution dans le'
                          ' .par, chargement, ou pose sur le modele.\n')
        else:
            fichier.write('AUCUNE ARCHIVE « itm » DEMANDEE.\n')
            fichier.write('Donc la demande NE PART PAS : le chargeur est mort'
                          ' ou n est jamais appele. Le defaut est en AMONT,'
                          ' dans la page qui devrait le declencher.\n')
        fichier.write('\n%d objset(s) distinct(s) demande(s) en tout.\n'
                      % len(et['noms']))
        if not et['noms']:
            fichier.write('ET AUCUN OBJSET DU TOUT : l espion n a pas vu'
                          ' passer la fonction. Relancez avec --tout, et si'
                          ' c est toujours vide, c est l ESPION qui est en'
                          ' cause, pas le jeu.\n')
        else:
            fichier.write('Les vingt plus demandes :\n')
            for nom, n in sorted(et['noms'].items(),
                                 key=lambda kv: -kv[1])[:20]:
                fichier.write('  %-44s %d\n' % (nom, n))
        fichier.close()
    print()
    print('archives « itm » demandees : %d' % len(et['itm']))
    for nom in sorted(et['itm']):
        print('   %s' % nom)
    print('objsets distincts vus : %d' % len(et['noms']))
    print('journal : %s' % os.path.relpath(JOURNAL, RACINE))
    return 0


if __name__ == '__main__':
    sys.exit(main())
