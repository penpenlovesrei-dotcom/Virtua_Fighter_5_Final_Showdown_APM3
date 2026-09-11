#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Sort les sons du systeme de paiement du dossier APM.

Le dossier `APM_V1.04_internal_0` contient **114 fichiers `.wav`** repartis
dans six dossiers `tfps-res-*` (dev / pro / stg, plus leurs variantes
`-proxy`). Ce sont **six copies du meme jeu** : il n'y a que
**DIX-NEUF sons distincts**, verifie au SHA-256.

Ce sont les jingles du systeme de paiement Thinca -- courts (0,22 s a 3,59 s),
mono 44,1 kHz 16 bits pour la plupart, deux en stereo. Aucune musique, et
aucun `AudioClip` dans les assets Unity : les deux applications ne portent pas
un son en propre, elles jouent ceux-la.

`resource.xml` associe a chaque marque ses sons, par un `id` de 0 a 3 --
**dont il ne documente pas le sens**. On garde donc l'id tel quel dans le nom
plutot que d'inventer « succes » ou « erreur ».

    py -3 tools/apm_sons.py
    py -3 tools/apm_sons.py --dossier <APM_V1.04_internal_0>
"""
import hashlib
import os
import re
import shutil
import sys
import wave

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
APM = r'C:\Users\frede\Desktop\VF5 FS DECOMP\APM_V1.04_internal_0'
SORTIE = os.path.join(RACINE, 'extracted', 'apm_sons')


def marques(xml):
    """{code: nom} et {fichier: [(code, id_son), ...]}, lus dans resource.xml."""
    d = open(xml, encoding='utf-8', errors='replace').read()
    noms, sons = {}, {}
    blocs = list(re.finditer(r'<brand code="(\d+)"', d))
    for k, m in enumerate(blocs):
        code = m.group(1)
        fin = blocs[k + 1].start() if k + 1 < len(blocs) else len(d)
        bloc = d[m.end():fin]
        n = re.search(r'<name[^>]*>([^<]+)</name>', bloc)
        noms[code] = n.group(1) if n else code
        for s in re.finditer(r'<sound id="(\d+)">([^<]+)</sound>', bloc):
            sons.setdefault(s.group(2), []).append((code, s.group(1)))
    return noms, sons


def main():
    argv = sys.argv[1:]
    base = APM
    if '--dossier' in argv:
        base = argv[argv.index('--dossier') + 1]
    if not os.path.isdir(base):
        print('introuvable : %s' % base)
        return 1

    # 1. tous les .wav, dedupliques
    par_hash = {}
    total = 0
    for r, _, fs in os.walk(base):
        for f in fs:
            if not f.lower().endswith('.wav'):
                continue
            total += 1
            p = os.path.join(r, f)
            h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
            par_hash.setdefault(h, []).append(p)

    # 2. les noms de marque
    xml = os.path.join(base, 'tfps-res-pro', 'resource.xml')
    noms, sons = marques(xml) if os.path.exists(xml) else ({}, {})

    os.makedirs(SORTIE, exist_ok=True)
    print('=' * 74)
    print('LES SONS DU SYSTEME DE PAIEMENT APM')
    print('   %d fichiers .wav, %d DISTINCTS (six environnements identiques)'
          % (total, len(par_hash)))
    print('=' * 74)

    index = []
    for h, chemins in sorted(par_hash.items(), key=lambda x: os.path.basename(x[1][0])):
        src = chemins[0]
        nom = os.path.basename(src)
        usages = sons.get(nom, [])
        etiq = ' '.join('%s(id%s)' % (noms.get(c, c), i) for c, i in usages)
        try:
            w = wave.open(src, 'rb')
            duree = w.getnframes() / float(w.getframerate())
            desc = '%d voie(s) %d Hz %d bits %.2f s' % (
                w.getnchannels(), w.getframerate(), w.getsampwidth() * 8, duree)
            w.close()
        except Exception as e:
            desc = '(illisible : %s)' % e
        cible = os.path.join(SORTIE, nom)
        shutil.copy2(src, cible)
        print('   %-16s %-34s %d copie(s)   %s'
              % (nom, desc, len(chemins), etiq))
        index.append((nom, desc, len(chemins), etiq))

    with open(os.path.join(SORTIE, '_index.txt'), 'w', encoding='utf-8') as fp:
        fp.write('Les sons du systeme de paiement APM (Thinca)\n')
        fp.write('%d fichiers .wav dans le dossier, %d distincts.\n\n'
                 % (total, len(par_hash)))
        fp.write("resource.xml associe chaque son a une marque par un id de 0 a 3,\n"
                 "dont il ne documente PAS le sens : l'id est garde tel quel.\n\n")
        for nom, desc, n, etiq in index:
            fp.write('%-16s %-34s %d copie(s)  %s\n' % (nom, desc, n, etiq))

    print()
    print('%d son(s) ecrit(s) dans %s' % (len(index), SORTIE))
    return 0


if __name__ == '__main__':
    sys.exit(main())
