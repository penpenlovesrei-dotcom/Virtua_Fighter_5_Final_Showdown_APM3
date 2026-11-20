#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Met un `.cmd` en ASCII pur et en CRLF, sans rien lui retirer d'autre.

Les accents et les guillemets francais sont translitteres ; tout octet qui
resterait hors ASCII arrete l'outil plutot que de l'ecrire (c'est la regle :
verifier l'encodage AVANT d'ouvrir en ecriture).

    py -3 tools/_normaliser_cmd.py tools/terminal.cmd [...]
"""
import sys
import unicodedata

REMPLACEMENTS = {
    '«': '"', '»': '"', '‘': "'", '’': "'",
    '“': '"', '”': '"', '–': '-', '—': '--',
    '…': '...', '§': 'S', '°': ' deg', ' ': ' ',
    'æ': 'ae', 'œ': 'oe', 'Æ': 'AE', 'Œ': 'OE',
}


def aplatir(txt):
    for k, v in REMPLACEMENTS.items():
        txt = txt.replace(k, v)
    txt = unicodedata.normalize('NFKD', txt)
    return ''.join(c for c in txt if not unicodedata.combining(c))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for chemin in sys.argv[1:]:
        with open(chemin, 'rb') as fp:
            brut = fp.read()
        # Les lanceurs anciens ne sont pas tous en UTF-8 : certains portent
        # un « seul (0xAB), ce qui n'est pas de l'UTF-8 valide. On essaie
        # l'UTF-8 d'abord -- strict, pour ne jamais fabriquer de U+FFFD --
        # puis cp1252, qui est ce que Windows ecrit par defaut. Jamais
        # d'erreurs='replace' : un caractere perdu ne se retrouve pas, et on
        # en a deja perdu six dans tools/console.cmd de cette facon.
        try:
            txt = brut.decode('utf-8', 'strict')
        except UnicodeDecodeError:
            txt = brut.decode('cp1252', 'strict')
            print('%s : lu en cp1252 (ce n etait pas de l UTF-8)' % chemin)
        if '�' in txt:
            sys.exit('%s : le fichier contient deja U+FFFD -- un caractere y '
                     'a ete perdu avant nous. Rien n a ete ecrit : il faut le '
                     'retrouver a la main.' % chemin)
        txt = aplatir(txt).replace('\r\n', '\n').replace('\n', '\r\n')
        try:
            octets = txt.encode('ascii')
        except UnicodeEncodeError as e:
            sys.exit('%s : caractere non ASCII %r a la position %d -- rien n '
                     'a ete ecrit.' % (chemin, txt[e.start:e.end], e.start))
        with open(chemin, 'wb') as fp:
            fp.write(octets)
        print('%s : %d -> %d octets, ASCII + CRLF'
              % (chemin, len(brut), len(octets)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
