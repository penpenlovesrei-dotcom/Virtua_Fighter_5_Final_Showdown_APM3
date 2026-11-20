#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lire une image ext2 -- lister son arborescence, en sortir des fichiers.

POURQUOI. Les images Lindbergh (`vf5r.bin`, `vf5r_rom.bin` de VF5 R) sont des
systemes de fichiers **ext2** : magie `0xEF53` au `+0x438` de l image, c est a
dire a `+0x38` du superbloc, lui-meme a l octet 1024. Rien a deviner, c est
ecrit. L atelier n avait pas de lecteur ; en voici un, qui ne depend de rien.

CE QU IL LIT, et c est tout ce qu ext2 demande :

    superbloc (offset 1024)   taille de bloc, inodes par groupe, taille
                              d inode, premier bloc de donnees
    descripteurs de groupe    un par groupe, 32 octets, juste apres le
                              superbloc ; `bg_inode_table` donne la table
    inode                     mode, taille, et QUINZE pointeurs de bloc :
                              douze directs, un indirect, un double, un triple
    repertoire                suite d entrees {inode, rec_len, name_len,
                              file_type, nom}, chacune alignee sur 4

PIEGE : la TAILLE d un fichier de plus de 4 Go tient sur DEUX champs --
`i_size` en `+0x04` et `i_dir_acl` en `+0x6C`, qui sert de poids fort pour un
fichier ordinaire. Un lecteur qui ne lit que le premier tronque en silence.

    py -3 tools/ext2.py lister <image> [motif]
    py -3 tools/ext2.py sortir <image> <chemin dans l image> <fichier>
    py -3 tools/ext2.py sortir-tout <image> <motif> <dossier>
"""
import os
import re
import struct
import sys


class Ext2(object):
    def __init__(self, chemin):
        self.f = open(chemin, 'rb')
        self.f.seek(1024)
        sb = self.f.read(1024)
        if struct.unpack_from('<H', sb, 0x38)[0] != 0xEF53:
            raise SystemExit('%s : pas de magie ext2 au superbloc' % chemin)
        self.blocs = struct.unpack_from('<I', sb, 4)[0]
        self.premier = struct.unpack_from('<I', sb, 20)[0]
        self.taille_bloc = 1024 << struct.unpack_from('<I', sb, 24)[0]
        self.inodes_par_groupe = struct.unpack_from('<I', sb, 40)[0]
        rev = struct.unpack_from('<I', sb, 76)[0]
        self.taille_inode = struct.unpack_from('<H', sb, 88)[0] if rev else 128
        self.ptr_par_bloc = self.taille_bloc // 4
        self.gd = self._bloc(self.premier + 1)

    def _bloc(self, n):
        if n == 0:
            return b'\x00' * self.taille_bloc
        self.f.seek(n * self.taille_bloc)
        d = self.f.read(self.taille_bloc)
        if len(d) < self.taille_bloc:
            d += b'\x00' * (self.taille_bloc - len(d))
        return d

    def inode(self, num):
        g = (num - 1) // self.inodes_par_groupe
        i = (num - 1) % self.inodes_par_groupe
        table = struct.unpack_from('<I', self.gd, g * 32 + 8)[0]
        self.f.seek(table * self.taille_bloc + i * self.taille_inode)
        return self.f.read(self.taille_inode)

    @staticmethod
    def mode(ino):
        return struct.unpack_from('<H', ino, 0)[0]

    @staticmethod
    def taille(ino):
        bas = struct.unpack_from('<I', ino, 4)[0]
        haut = struct.unpack_from('<I', ino, 0x6C)[0]
        return bas | (haut << 32)

    def _liste_blocs(self, ino, combien):
        """Les numeros de bloc d un inode, dans l ordre, jusqu a `combien`."""
        p = [struct.unpack_from('<I', ino, 40 + 4 * k) [0] for k in range(15)]
        out = []
        fmt = '<%dI' % self.ptr_par_bloc

        def ajoute(n):
            out.append(n)
            return len(out) >= combien

        for k in range(12):
            if ajoute(p[k]):
                return out
        if p[12]:
            for n in struct.unpack(fmt, self._bloc(p[12])):
                if ajoute(n):
                    return out
        if p[13]:
            for m in struct.unpack(fmt, self._bloc(p[13])):
                if not m:
                    continue
                for n in struct.unpack(fmt, self._bloc(m)):
                    if ajoute(n):
                        return out
        if p[14]:
            for k1 in struct.unpack(fmt, self._bloc(p[14])):
                if not k1:
                    continue
                for m in struct.unpack(fmt, self._bloc(k1)):
                    if not m:
                        continue
                    for n in struct.unpack(fmt, self._bloc(m)):
                        if ajoute(n):
                            return out
        return out

    def lire(self, num, sortie=None):
        """Rend le contenu d un inode, ou l ecrit dans `sortie`."""
        ino = self.inode(num)
        n = self.taille(ino)
        combien = (n + self.taille_bloc - 1) // self.taille_bloc
        blocs = self._liste_blocs(ino, combien)
        if sortie is None:
            return b''.join(self._bloc(b) for b in blocs)[:n]
        reste = n
        with open(sortie, 'wb') as fp:
            for b in blocs:
                d = self._bloc(b)
                if reste < len(d):
                    d = d[:reste]
                fp.write(d)
                reste -= len(d)
                if reste <= 0:
                    break
        return n

    def entrees(self, num):
        """Les entrees d un repertoire : (nom, inode, type)."""
        d = self.lire(num)
        out = []
        o = 0
        while o + 8 <= len(d):
            ino, rec, nlen, typ = struct.unpack_from('<IHBB', d, o)
            if rec < 8:
                break
            nom = d[o + 8:o + 8 + nlen].decode('utf-8', 'replace')
            if ino and nom not in ('.', '..'):
                out.append((nom, ino, typ))
            o += rec
        return out

    def parcourir(self, num=2, chemin='', vus=None):
        """Tout l arbre, en profondeur : (chemin, inode, taille, dossier?)."""
        vus = vus if vus is not None else set()
        if num in vus:
            return
        vus.add(num)
        for nom, ino, typ in self.entrees(num):
            p = chemin + '/' + nom
            if typ:
                dossier = (typ == 2)
            else:
                dossier = (self.mode(self.inode(ino)) & 0xF000) == 0x4000
            if dossier:
                yield (p, ino, 0, True)
                for x in self.parcourir(ino, p, vus):
                    yield x
            else:
                yield (p, ino, self.taille(self.inode(ino)), False)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd, image = argv[0], argv[1]
    fs = Ext2(image)
    if cmd == 'lister':
        motif = argv[2] if len(argv) > 2 else ''
        n = 0
        for p, _i, t, d in fs.parcourir():
            if motif and motif.lower() not in p.lower():
                continue
            print('%-14s %s' % ('<dossier>' if d else '%d' % t, p))
            n += 1
        print('%d entree(s)' % n)
        return 0
    if cmd == 'sortir':
        cible, sortie = argv[2], argv[3]
        for p, i, _t, d in fs.parcourir():
            if not d and p.lower() == cible.lower():
                n = fs.lire(i, sortie)
                print('%s -> %s (%d octets)' % (p, sortie, n))
                return 0
        print('introuvable : %s' % cible)
        return 1
    if cmd == 'sortir-tout':
        motif, dossier = re.compile(argv[2], re.I), argv[3]
        os.makedirs(dossier, exist_ok=True)
        for p, i, t, d in fs.parcourir():
            if d or not motif.search(p):
                continue
            s = os.path.join(dossier, os.path.basename(p))
            fs.lire(i, s)
            print('%s -> %s (%d octets)' % (p, s, t))
        return 0
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
