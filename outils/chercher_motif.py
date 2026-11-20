#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Cherche des motifs texte (ASCII et UTF-16LE, insensible a la casse) dans un
ou plusieurs fichiers binaires, y compris tres gros (lecture par blocs).

    py -3 tools/chercher_motif.py <fichier...> --motifs kotrial knockout trial

Affiche pour chaque occurrence : fichier, offset, encodage, et le contexte
imprimable autour.
"""
import argparse
import os
import re
import sys

BLOC = 8 << 20   # 8 Mio
CHEVAUCHE = 4096


def contexte(donnees, pos, taille, avant=48, apres=64):
    a = max(0, pos - avant)
    b = min(len(donnees), pos + taille + apres)
    brut = donnees[a:b]
    return ''.join(chr(c) if 32 <= c < 127 else '.' for c in brut)


def chercher(chemin, motifs, utf16=True, limite=None):
    taille = os.path.getsize(chemin)
    trouves = 0
    regs = []
    for m in motifs:
        regs.append(('ascii', re.compile(re.escape(m.encode('ascii')), re.I)))
        if utf16:
            u = m.encode('utf-16le')
            regs.append(('utf16', re.compile(re.escape(u), re.I)))
    with open(chemin, 'rb') as f:
        base = 0
        reste = b''
        while True:
            bloc = f.read(BLOC)
            if not bloc:
                break
            donnees = reste + bloc
            depart_abs = base - len(reste)
            for enc, reg in regs:
                for mo in reg.finditer(donnees):
                    off = depart_abs + mo.start()
                    if off < base - CHEVAUCHE and reste:
                        continue
                    print('%-28s off=0x%08X  %-5s  %s'
                          % (os.path.basename(chemin), off, enc,
                             contexte(donnees, mo.start(), len(mo.group(0)))))
                    trouves += 1
                    if limite and trouves >= limite:
                        return trouves
            base += len(bloc)
            reste = donnees[-CHEVAUCHE:]
            sys.stderr.write('\r%s : %.1f%%   ' % (os.path.basename(chemin),
                                                   100.0 * base / max(1, taille)))
            sys.stderr.flush()
    sys.stderr.write('\r' + ' ' * 60 + '\r')
    return trouves


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fichiers', nargs='+')
    ap.add_argument('--motifs', nargs='+', required=True)
    ap.add_argument('--sans-utf16', action='store_true')
    ap.add_argument('--limite', type=int, default=0)
    a = ap.parse_args()
    total = 0
    for c in a.fichiers:
        if not os.path.exists(c):
            print('!! absent : %s' % c)
            continue
        n = chercher(c, a.motifs, utf16=not a.sans_utf16,
                     limite=a.limite or None)
        print('-- %s : %d occurrence(s)' % (os.path.basename(c), n))
        total += n
    print('== total %d' % total)


if __name__ == '__main__':
    main()
