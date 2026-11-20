#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repeint les noms de BGM que le module APM3 demande vers les noms que le
GOG fournit reellement.

POURQUOI CE SENS-LA. L'autre sens -- fabriquer des `vfes_bgm_*` qui pointent
sur les fichiers du GOG -- marcherait aussi, mais il salirait le dossier de
donnees avec 150 alias et rendrait le banc illisible. Ici le dossier du GOG
reste intact et c'est le module qui apprend les noms de son hote.

POURQUOI C'EST SUR. Les noms sont stockes en chemins COMPLETS
(`rom/sound/bgm/vfes_bgm_vf5fs_ban.adx`), chacun dans son emplacement, et
TOUTES les cibles du GOG sont plus COURTES que les noms d'origine :

    rom/sound/bgm/vfes_bgm_vf5fs_ban.adx   36 -> rom/sound/bgm/vf5fs_bgm_ban.adx   31
    rom/sound/bgm/vfes_bgm_vf5r_ban.adx    35 -> rom/sound/bgm/vf5r_ban.adx        26
    rom/sound/bgm/vfes_bgm_vf1_ban.adx     34 -> rom/sound/bgm/h_ban_vf1.adx       27

On ecrit donc le nouveau nom A LA MEME ADRESSE, on complete par des zeros, et
on ne depasse jamais le terminateur d'origine. Aucun pointeur ne bouge, aucune
relocalisation, aucune section a agrandir. Le patch est reversible : le module
d'origine est garde en .origine.

ON NE DEVINE AUCUNE CORRESPONDANCE. Chaque nom candidat est confronte au
dossier `rom/sound/bgm` du GOG ; ce qui n'y existe pas n'est pas patche et est
compte a part. Un nom absent reste absent -- mieux vaut un silence qu'on sait
nommer qu'une substitution qu'on ne sait plus defaire.

    py -3 -I outils\\patcher_bgm_gog.py             # montre, n'ecrit rien
    py -3 -I outils\\patcher_bgm_gog.py --ecrire    # patche le banc
"""
import os
import re
import shutil
import sys
import collections

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANC = os.path.join(RACINE, 'banc_gog')
MODULE = os.path.join(BANC, 'vf5fs-pxd-w64-Retail_APM3.dll')
ORIGINE = MODULE + '.origine'
BGM_GOG = os.path.join(
    os.path.dirname(RACINE), 'SOURCES', 'Yakuza_6_FS_GOG',
    'Yakuza 6 - vf5fs', 'vf5fs_media', 'rom', 'sound', 'bgm')

PREFIXE = 'rom/sound/bgm/'

# Les familles d'APM3 et la regle qui mene a celle du GOG. L'ordre compte :
# vf5fs_ et vf5r_ doivent passer avant la regle generique vfN_.
REGLES = [
    (re.compile(r'^vfes_bgm_vf5fs_(\w+)$'), lambda m: 'vf5fs_bgm_%s' % m.group(1)),
    (re.compile(r'^vfes_bgm_vf5r_(\w+)$'),  lambda m: 'vf5r_%s' % m.group(1)),
    (re.compile(r'^vfes_bgm_(vf1|vf2|vf3|vf4ev|vf4|vf5|vfk)_(\w+)$'),
     lambda m: 'h_%s_%s' % (m.group(2), m.group(1))),
    (re.compile(r'^vfes_bgm_stg_(\w+)$'),   lambda m: 'vf5fs_bgm_%s' % m.group(1)),
]

# LES PAIRES QUE LE MODULE ETABLIT LUI-MEME.
#
# Le module porte DEUX tables de noms : la table arcade (`vfes_*`) et la table
# console (`vf5fs_*`). Elles se touchent dans le binaire -- 24 ou 32 octets
# d'ecart, c'est-a-dire l'emplacement voisin :
#
#   003961d0  rom/sound/bgm/vfes_jng_ovr.adx
#   003961f0  rom/sound/bgm/vf5fs_jng_ovr.adx     (+32)
#   0039a4e0  vfes_jng_win.adx
#   0039a4f8  vf5fs_jng_win.adx                   (+24)
#   0039a540  rom/sound/bgm/vfes_bgm_con.adx
#   0039a560  rom/sound/bgm/vf5fs_lp_cnt.adx      (+32)
#   003fdc60  rom/sound/bgm/vf5fs_bgm_sel.adx
#   003fdc80  rom/sound/bgm/vfes_bgm_sel.adx      (+32)
#
# Ce n'est pas une regle que j'invente : c'est le code d'origine qui choisit
# entre les deux selon la cible, et il a laisse les deux noms cote a cote. Et
# le GOG livre precisement ceux de la table console. La correspondance est
# donc ETABLIE PAR LE BINAIRE, pas devinee par moi -- et chacune est quand
# meme confrontee au dossier avant d'etre ecrite.
PAIRES = {
    'vfes_jng_ovr':  'vf5fs_jng_ovr',
    'vfes_jng_los':  'vf5fs_jng_los',
    'vfes_jng_win':  'vf5fs_jng_win',
    'vfes_bgm_con':  'vf5fs_lp_cnt',
    'vfes_bgm_sel':  'vf5fs_bgm_sel',
}

# CE QU'ON NE DEVINE PAS. `vfes_bgm_mnu`, `vfes_bgm_cus`, `vfes_bgm_aim`,
# `vfes_jng_lod` et `vfes_se_logo_sega` n'ont PAS de jumeau console dans le
# module. Le GOG porte bien `vf5fs_bgm_adv`, `vf5fs_bgm_kot`,
# `vf5fs_jng_ld1`... mais rien ne dit lequel repond a quoi, et une
# substitution au jugé ne se defait plus. Elles restent muettes, et nommees.


def candidat(nom):
    """nom sans dossier ni extension -> nom GOG candidat, ou None."""
    if nom in PAIRES:
        return PAIRES[nom]
    for motif, rendu in REGLES:
        m = motif.match(nom)
        if m:
            return rendu(m)
    return None


def main():
    ecrire = '--ecrire' in sys.argv[1:]

    if not os.path.isfile(MODULE):
        sys.exit('module introuvable : %s\nMonter le banc d abord.' % MODULE)
    if not os.path.isdir(BGM_GOG):
        sys.exit('dossier bgm du GOG introuvable : %s' % BGM_GOG)

    presents = set(os.listdir(BGM_GOG))
    print('bgm du GOG : %d fichiers' % len(presents))

    with open(MODULE, 'rb') as fp:
        brut = bytearray(fp.read())
    print('module     : %d octets' % len(brut))
    print()

    motif = re.compile(rb'[\x20-\x7e]{4,}\x00')
    pref = PREFIXE.encode('ascii')

    patchs = []
    sans_cible = []
    hors_regle = []

    for m in motif.finditer(bytes(brut)):
        s = m.group()[:-1]
        if not s.endswith(b'.adx'):
            continue
        chaine = s.decode('ascii')
        # Deux formes coexistent dans le module : le chemin complet
        # `rom/sound/bgm/vfes_...adx` et le nom NU `vfes_jng_win.adx`. On
        # garde la forme d'origine pour la reecrire a l'identique.
        if chaine.startswith(PREFIXE):
            dossier, nom = PREFIXE, chaine[len(PREFIXE):-4]
        elif '/' not in chaine and '\\' not in chaine:
            dossier, nom = '', chaine[:-4]
        else:
            continue
        if not nom.startswith('vfes_'):
            continue                      # deja un nom de console, on laisse
        cible = candidat(nom)
        if cible is None:
            hors_regle.append((m.start(), chaine))
            continue
        fichier = cible + '.adx'
        if fichier not in presents:
            sans_cible.append((m.start(), chaine, fichier))
            continue
        neuf = dossier + fichier
        # LE BOURRAGE. Les chaines sont alignees sur 8 octets : apres le
        # terminateur il reste souvent des zeros jusqu'a la suivante. Quatre
        # cibles font un caractere de PLUS que l'original
        # (`vf5fs_jng_ovr` contre `vfes_jng_ovr`), et elles tiennent dans ce
        # bourrage. Mais on ne le suppose pas : on compte les octets NULS qui
        # suivent reellement, et on n'ecrit jamais au-dela.
        fin = m.start() + len(chaine) + 1
        marge = 0
        while fin + marge < len(brut) and brut[fin + marge] == 0:
            marge += 1
        if len(neuf) > len(chaine) + marge:
            sans_cible.append((
                m.start(), chaine,
                '%s (TROP LONG de %d, marge %d)'
                % (fichier, len(neuf) - len(chaine), marge)))
            continue
        patchs.append((m.start(), chaine, neuf))

    # --- bilan avant d ecrire quoi que ce soit --------------------------------
    print('=== A PATCHER : %d ===' % len(patchs))
    familles = collections.Counter()
    for _, vieux, neuf in patchs:
        familles[neuf.rsplit('/', 1)[-1].split('_')[0]] += 1
    for f, n in sorted(familles.items(), key=lambda kv: -kv[1]):
        print('  vers %-8s %4d' % (f + '_*', n))
    print()
    for off, vieux, neuf in patchs[:10]:
        print('  %08x  %-38s -> %s' % (off, vieux, neuf))
    if len(patchs) > 10:
        print('  ... (%d de plus)' % (len(patchs) - 10))
    print()

    print('=== LAISSES TELS QUELS, FAUTE DE FICHIER AU GOG : %d ===' % len(sans_cible))
    fam2 = collections.Counter()
    for _, vieux, manquant in sans_cible:
        fam2[manquant.split('_')[0]] += 1
    for f, n in sorted(fam2.items(), key=lambda kv: -kv[1]):
        print('  %-10s %4d manquant(s)' % (f + '_*', n))
    for off, vieux, manquant in sans_cible[:8]:
        print('  %08x  %-38s  il faudrait %s' % (off, vieux, manquant))
    if len(sans_cible) > 8:
        print('  ... (%d de plus)' % (len(sans_cible) - 8))
    print()

    if hors_regle:
        print('=== HORS REGLE : %d ===' % len(hors_regle))
        for off, chaine in hors_regle[:20]:
            print('  %08x  %s' % (off, chaine))
        print()

    if not ecrire:
        print('--- RIEN ECRIT. Relancer avec --ecrire pour patcher. ---')
        return 0

    # --- le lien dur ---------------------------------------------------------
    # Le module du banc est un LIEN DUR vers SOURCES. Ecrire dedans, c est
    # ecrire dans SOURCES. On le remplace par une vraie copie AVANT tout.
    st = os.stat(MODULE)
    liens = getattr(st, 'st_nlink', 1)
    print('liens durs sur le module : %d' % liens)
    if liens > 1:
        provisoire = MODULE + '.copie'
        shutil.copyfile(MODULE, provisoire)
        os.remove(MODULE)
        os.rename(provisoire, MODULE)
        print('  lien dur CASSE : le banc a maintenant sa propre copie.')
        st2 = os.stat(MODULE)
        if getattr(st2, 'st_nlink', 1) > 1:
            sys.exit('  ECHEC : le lien dur subsiste. Rien patche.')
    if not os.path.exists(ORIGINE):
        shutil.copyfile(MODULE, ORIGINE)
        print('  module d origine garde en .origine')
    print()

    for off, vieux, neuf in patchs:
        # On reecrit sur toute l'empreinte de l'ancienne chaine, terminateur
        # compris, et on comble le reste de zeros. Quand le neuf est plus
        # long, les octets supplementaires ont ete verifies nuls plus haut.
        large = max(len(vieux), len(neuf)) + 1
        brut[off:off + large] = (
            neuf.encode('ascii') + b'\x00' * (large - len(neuf)))

    with open(MODULE, 'wb') as fp:
        fp.write(brut)
    print('=== %d chaines repeintes dans %s ===' % (len(patchs), os.path.basename(MODULE)))
    print('    (taille inchangee : %d octets)' % len(brut))
    return 0


if __name__ == '__main__':
    sys.exit(main())
