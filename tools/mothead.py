#!/usr/bin/env python3
"""Lecteur de mothead_<CHR>.bin - les donnees de mouvement de VF5FS.

Un fichier par personnage, dans rom/rob/. Petit-boutiste.
La section 2 (bloc CCD) est decrite dans docs/formats/mothead.md ; ce script
lit la **section 1**, c'est-a-dire les mouvements eux-memes.

Structure (verifiee sur le corpus et sur le code du moteur, voir la doc) :

    section 1 = en-tete 32 o + enregistrements + table de recherche

    en-tete (a l'offset 32 du fichier, note s1 = base de la section 1)
        +0x00 u32  index du jeu d'animation
        +0x04 u32  plus petit identifiant d'animation du jeu
        +0x08 u32  plus grand identifiant
        +0x0C u32  offset de la table, relatif a s1
        +0x10 u32 x4  zeros

    table : (max - min + 1) u32, bourree a un multiple de 32 octets.
        entree[id - min] = offset de l'enregistrement, relatif a s1 ; 0 = absent

    enregistrement (32 o d'en-tete, puis des donnees partagees)
        +0x00 u32  drapeaux 0        +0x10 u16  drapeaux 4
        +0x04 u32  drapeaux 1        +0x12 u16  drapeaux 5
        +0x08 u32  drapeaux 2        +0x14 u32  -> liste 1  (0 = absente)
        +0x0C u32  drapeaux 3        +0x18 u32  -> liste 2
                                     +0x1C u32  -> liste 3

    liste 1 : entrees de 8 o   (u32 code, u32 -> charge utile)
    liste 2 : entrees de 12 o  (u32 code, u32 trame, u32 -> charge utile)
    liste 3 : tableau de u32   (-> charge utile de 16 o), termine par 0

    Les listes 1 et 2 se terminent sur un code negatif (0xFFFFFFFF).
    **Sur le disque, tous les offsets sont relatifs a s1.** Le moteur les
    convertit au chargement en offsets relatifs au champ qui les porte : c'est
    cette seconde forme que lit le code du DLL, pas celle du fichier.
    Les charges utiles sont **partagees entre enregistrements** : elles ne sont
    pas contenues dans l'enregistrement qui les designe.

Usage :
    py -3 tools/mothead.py info    <mothead.bin>
    py -3 tools/mothead.py list    <mothead.bin> [<mot_db.bin>]
    py -3 tools/mothead.py rec     <mothead.bin> <id> [<mot_db.bin>]
    py -3 tools/mothead.py check   <fichier|dossier> ...
    py -3 tools/mothead.py opcodes <fichier|dossier> ...
    py -3 tools/mothead.py ids     <mot_db.bin> <fichier|dossier> ...
"""
import bisect
import collections
import glob
import os
import struct
import sys

S1 = 32                      # la section 1 commence toujours a 32


class Mothead:
    def __init__(self, path):
        self.path = path
        with open(path, "rb") as fp:
            self.d = d = fp.read()
        self.nsect, self.off1, self.off2 = struct.unpack_from("<3I", d, 0)
        h = struct.unpack_from("<8I", d, S1)
        # ATTENTION : set_index n'indexe pas la table des jeux telle que tools/motdb.py
        # la lit. Il indexe cette liste PRIVEE DE AUTH_CMN (docs/formats/mothead.md 2.1) :
        # cela colle pour 20 personnages sur 21, TAK portant 46 la ou la regle donne 40.
        # Passe tel quel a db.sets[...], il ne valide que 881 identifiants sur 9140.
        # Le lien fiable est le NOM : mothead_XXX.bin <-> le jeu nomme XXX, soit
        # 9140/9140. Voir la commande « ids » ci-dessous.
        self.set_index, self.id_min, self.id_max, self.tbl = h[0], h[1], h[2], h[3]
        self.span = self.id_max - self.id_min + 1
        self.ntbl = (self.off2 - (S1 + self.tbl)) // 4
        self.table = struct.unpack_from("<%dI" % self.ntbl, d, S1 + self.tbl)
        self.ids = [self.id_min + i for i, v in enumerate(self.table) if v]

    # --- acces bas niveau : tous les offsets sont relatifs a la section 1 ---
    def u32(self, off):
        return struct.unpack_from("<I", self.d, S1 + off)[0]

    def s32(self, off):
        return struct.unpack_from("<i", self.d, S1 + off)[0]

    def raw(self, off, n):
        return self.d[S1 + off:S1 + off + n]

    def rec_off(self, mid):
        """Offset (relatif a s1) de l'enregistrement d'une animation, ou None."""
        if not self.id_min <= mid <= self.id_max:
            return None
        return self.table[mid - self.id_min] or None

    def header(self, off):
        f = struct.unpack_from("<4I2H3I", self.d, S1 + off)
        return dict(flags=f[:4], f4=f[4], f5=f[5], l1=f[6], l2=f[7], l3=f[8])

    def list1(self, off):
        """[(code, offset_charge)] ; s'arrete sur un code negatif ou un ptr nul."""
        out, q = [], off
        while True:
            code = self.u32(q)
            if code & 0x80000000:
                break
            p = self.u32(q + 4)
            if p == 0:
                break
            out.append((code, p))
            q += 8
        return out

    def list2(self, off):
        """[(code, trame, offset_charge ou None)]."""
        out, q = [], off
        while True:
            code = self.u32(q)
            if code & 0x80000000:
                break
            p = self.u32(q + 8)
            out.append((code, self.u32(q + 4), p or None))
            q += 12
        return out

    def list3(self, off):
        """[offset_charge] ; termine par 0."""
        out, q = [], off
        while True:
            p = self.u32(q)
            if p == 0:
                break
            out.append(p)
            q += 4
        return out

    def lists(self, off):
        h = self.header(off)
        return (self.list1(h["l1"]) if h["l1"] else [],
                self.list2(h["l2"]) if h["l2"] else [],
                self.list3(h["l3"]) if h["l3"] else [])


def load_names(dbpath):
    if not dbpath:
        return {}
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from motdb import MotDb
    db = MotDb(dbpath)
    return {m[0]: m[1] for s in db.sets for m in s["motions"]}


def gather(args):
    out = []
    for a in args:
        if os.path.isdir(a):
            out += sorted(glob.glob(os.path.join(a, "mothead_*.bin")))
        else:
            out.append(a)
    return out


def cmd_info(path):
    m = Mothead(path)
    print("fichier      %s (%d octets)" % (os.path.basename(path), len(m.d)))
    print("sections     %d   section 1 [%d, %d)   section 2 [%d, %d)"
          % (m.nsect, m.off1, m.off2, m.off2, len(m.d)))
    print("jeu d'anim.  index %d" % m.set_index)
    print("identifiants %d .. %d  (%d)" % (m.id_min, m.id_max, m.span))
    print("table        offset s1+0x%X, %d entrees (%d de bourrage), %d pourvues"
          % (m.tbl, m.ntbl, m.ntbl - m.span, len(m.ids)))
    n1 = n2 = n3 = 0
    for mid in m.ids:
        a, b, c = m.lists(m.rec_off(mid))
        n1 += len(a)
        n2 += len(b)
        n3 += len(c)
    print("listes       %d entrees en liste 1, %d en liste 2, %d en liste 3"
          % (n1, n2, n3))


def cmd_list(path, db=None):
    m = Mothead(path)
    names = load_names(db)
    for mid in m.ids:
        o = m.rec_off(mid)
        h = m.header(o)
        a, b, c = m.lists(o)
        print("%6d  s1+0x%06X  f=%08X %08X %08X %08X %04X %04X  "
              "L1=%-3d L2=%-3d L3=%-2d  %s"
              % (mid, o, h["flags"][0], h["flags"][1], h["flags"][2],
                 h["flags"][3], h["f4"], h["f5"], len(a), len(b), len(c),
                 names.get(mid, "")))


def cmd_rec(path, mid, db=None):
    m = Mothead(path)
    names = load_names(db)
    o = m.rec_off(mid)
    if o is None:
        print("identifiant %d : aucun enregistrement" % mid)
        return
    h = m.header(o)
    print("animation %d  %s" % (mid, names.get(mid, "")))
    print("enregistrement s1+0x%06X" % o)
    print("  drapeaux  %08X %08X %08X %08X   %04X %04X"
          % (h["flags"] + (h["f4"], h["f5"])))
    a, b, c = m.lists(o)
    if a:
        print("  liste 1 (%d) :" % len(a))
        for code, p in a:
            print("    code %2d (0x%02X)  charge s1+0x%06X  %s"
                  % (code, code, p, m.raw(p, 16).hex()))
    if b:
        print("  liste 2 (%d) :" % len(b))
        for code, frame, p in b:
            print("    code %2d (0x%02X)  trame %3d  charge %-14s %s"
                  % (code, code, frame,
                     ("s1+0x%06X" % p) if p is not None else "aucune",
                     m.raw(p, 16).hex() if p is not None else ""))
    if c:
        print("  liste 3 (%d) :" % len(c))
        for p in c:
            print("    charge s1+0x%06X  %s" % (p, m.raw(p, 16).hex()))


def cmd_check(paths):
    tot = collections.Counter()
    for path in paths:
        m = Mothead(path)
        r = collections.Counter()
        if m.nsect != 2 or m.off1 != S1:
            r["en-tete de fichier"] += 1
        if (m.off2 - S1) % 32:
            r["section 1 non multiple de 32"] += 1
        if not 0 <= m.ntbl - m.span < 8:
            r["bourrage de table"] += 1
        hi = m.tbl                      # fin de la zone des enregistrements
        for mid in m.ids:
            o = m.rec_off(mid)
            if o % 32 or not 0x20 <= o < hi:
                r["offset d'enregistrement"] += 1
                continue
            a, b, c = m.lists(o)
            for code, p in a:
                if not 0x20 <= p < hi:
                    r["L1 charge hors section"] += 1
                if code > 83:
                    r["L1 code > 83"] += 1
            fr = -1
            for code, frame, p in b:
                if p is not None and not 0x20 <= p < hi:
                    r["L2 charge hors section"] += 1
                if frame < fr:
                    r["L2 trames non croissantes"] += 1
                fr = frame
            for p in c:
                if not 0x20 <= p < hi:
                    r["L3 charge hors section"] += 1
        tot["fichiers"] += 1
        tot["conformes" if not r else "NON CONFORMES"] += 1
        if r:
            print("%-40s %s" % (os.path.basename(path), dict(r)))
    print("%d fichier(s) : %d conforme(s), %d non conforme(s)"
          % (tot["fichiers"], tot["conformes"], tot["NON CONFORMES"]))


def cmd_ids(paths, dbpath):
    """Chaque identifiant d'animation appartient-il au jeu du personnage ?

    L'appariement se fait par NOM (mothead_XXX.bin <-> le jeu nomme XXX) et non par
    le champ set_index de l'en-tete, qui ne designe pas ce que l'on croit."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from motdb import MotDb
    db = MotDb(dbpath)
    parnom = {s["name"]: set(m[0] for m in s["motions"]) for s in db.sets}
    tot = ok = 0
    faux = []
    for path in paths:
        m = Mothead(path)
        perso = os.path.basename(path)[8:-4]
        ens = parnom.get(perso)
        if ens is None:
            faux.append((perso, "aucun jeu de ce nom dans mot_db"))
            continue
        n = len(m.ids)
        v = sum(1 for i in m.ids if i in ens)
        tot += n
        ok += v
        if v != n:
            faux.append((perso, "%d/%d" % (v, n)))
    for perso, quoi in faux:
        print("%-6s %s" % (perso, quoi))
    print("%d identifiant(s) : %d dans le jeu du personnage, %d hors du jeu"
          % (tot, ok, tot - ok))
    return 0


def cmd_opcodes(paths):
    """Inventaire des codes et taille de leur charge utile.

    La taille est deduite de l'ecart jusqu'a la charge suivante du fichier : le
    minimum observe est la taille reelle, les ecarts plus grands venant du
    partage des charges entre enregistrements.
    """
    use = {1: collections.Counter(), 2: collections.Counter(),
           3: collections.Counter()}
    size = {1: collections.defaultdict(collections.Counter),
            2: collections.defaultdict(collections.Counter),
            3: collections.defaultdict(collections.Counter)}
    for path in paths:
        m = Mothead(path)
        tagged = []
        for mid in m.ids:
            a, b, c = m.lists(m.rec_off(mid))
            for code, p in a:
                use[1][code] += 1
                tagged.append((p, 1, code))
            for code, fr, p in b:
                use[2][code] += 1
                if p is not None:
                    tagged.append((p, 2, code))
            for p in c:
                use[3][0] += 1
                tagged.append((p, 3, 0))
        pts = sorted({t[0] for t in tagged})
        for p, lst, code in tagged:
            k = bisect.bisect_right(pts, p)
            size[lst][code][(pts[k] if k < len(pts) else m.tbl) - p] += 1
    for lst in (1, 2, 3):
        print("=== liste %d ===" % lst)
        for code in sorted(use[lst]):
            c = size[lst][code]
            print("  code %2d (0x%02X)  %7d emploi(s)  charge utile %s octets"
                  % (code, code, use[lst][code], min(c) if c else "?"))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "info":
        cmd_info(rest[0])
    elif cmd == "list":
        cmd_list(rest[0], rest[1] if len(rest) > 1 else None)
    elif cmd == "rec":
        cmd_rec(rest[0], int(rest[1], 0), rest[2] if len(rest) > 2 else None)
    elif cmd == "check":
        cmd_check(gather(rest))
    elif cmd == "opcodes":
        cmd_opcodes(gather(rest))
    elif cmd == "ids":
        return cmd_ids(gather(rest[1:]), rest[0])
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
