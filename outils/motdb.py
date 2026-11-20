#!/usr/bin/env python3
"""Lecteur de la base d'animations VF5FS : mot_db.bin et rob_cmn_mottbl.bin.

mot_db.bin donne le nom de chaque animation et le jeu auquel elle appartient.
rob_cmn_mottbl.bin donne, pour chaque personnage et chaque posture, la table des
363 roles logiques -> identifiant d'animation.

Usage:
    py -3 tools/motdb.py sets   <mot_db.bin>
    py -3 tools/motdb.py name   <mot_db.bin> <id> [<id> ...]
    py -3 tools/motdb.py bones  <mot_db.bin>
    py -3 tools/motdb.py chars  <rob_cmn_mottbl.bin> [<mot_db.bin>]
    py -3 tools/motdb.py slots  <rob_cmn_mottbl.bin> <mot_db.bin> <entree> [<set>]
    py -3 tools/motdb.py diff   <mot_db.bin> <tblA> <tblB>   compare deux versions
"""
import collections
import struct
import sys


def _u32(d, o):
    return struct.unpack("<I", d[o:o + 4])[0]


def _cstr(d, o):
    return d[o:d.index(b"\0", o)].decode("latin-1")


class MotDb:
    """mot_db.bin — 45 jeux d'animation, 11 026 noms, 149 os (version 6.000)."""

    def __init__(self, path):
        with open(path, "rb") as fp:
            self.d = d = fp.read()
        self.version = _u32(d, 0)
        self.set_tbl = _u32(d, 4)
        self.nset = _u32(d, 0xC)
        self.bone_tbl = _u32(d, 0x10)
        self.nbone = _u32(d, 0x14)
        self.sets = []
        self.id2name = {}
        for i in range(self.nset):
            o = self.set_tbl + 16 * i
            name = _cstr(d, _u32(d, o))
            names_tbl, cnt, id_tbl = _u32(d, o + 4), _u32(d, o + 8), _u32(d, o + 12)
            motions = []
            for k in range(cnt):
                mid = _u32(d, id_tbl + 4 * k)
                nm = _cstr(d, _u32(d, names_tbl + 4 * k))
                motions.append((mid, nm))
                self.id2name[mid] = (name, nm)
            self.sets.append(dict(name=name, count=cnt, motions=motions))

    def bones(self):
        return [_cstr(self.d, _u32(self.d, self.bone_tbl + 4 * i))
                for i in range(self.nbone)]


class RobMotTbl:
    """rob_cmn_mottbl.bin — table des roles logiques d'animation.

    en-tete : [0] nb d'entrees, [4] nb de roles - 1, [8] offset du tableau
    tableau : nb d'entrees paires (offset, nb de postures)
    a `offset` : les offsets des blocs ; chaque bloc = `nb de roles` u32
    """

    def __init__(self, path):
        with open(path, "rb") as fp:
            self.d = d = fp.read()
        self.count = _u32(d, 0)
        self.nslot = _u32(d, 4)          # dernier index ; 363 roles
        self.tbl = _u32(d, 8)
        self.entries = []
        for i in range(self.count):
            o = self.tbl + 8 * i
            off, nposture = _u32(d, o), _u32(d, o + 4)
            blocks = [_u32(d, off + 4 * k) for k in range(nposture)]
            self.entries.append(dict(off=off, nposture=nposture, blocks=blocks))

    def slots(self, entry, posture=0):
        b = self.entries[entry]["blocks"][posture]
        return [_u32(self.d, b + 4 * k) for k in range(self.nslot)]

    def label(self, entry, db):
        """Jeu d'animation dominant, hors CMN : identifie le personnage."""
        cnt = collections.Counter()
        for p in range(self.entries[entry]["nposture"]):
            for mid in self.slots(entry, p):
                s = db.id2name.get(mid)
                if s:
                    cnt[s[0]] += 1
        for name, _n in cnt.most_common():
            if name != "CMN":
                return name
        return "?"


def main():
    cmd = sys.argv[1]
    if cmd == "sets":
        db = MotDb(sys.argv[2])
        print("version=%d  jeux=%d  os=%d" % (db.version, db.nset, db.nbone))
        tot = 0
        for i, s in enumerate(db.sets):
            tot += s["count"]
            print("%3d %-14s %6d  %s" % (i, s["name"], s["count"],
                                         s["motions"][0][1] if s["motions"] else ""))
        print("total : %d animations nommees" % tot)
    elif cmd == "name":
        db = MotDb(sys.argv[2])
        for a in sys.argv[3:]:
            mid = int(a, 0)
            v = db.id2name.get(mid)
            print("%-8d %s" % (mid, "%s / %s" % v if v else "(inconnu)"))
    elif cmd == "bones":
        db = MotDb(sys.argv[2])
        for i, b in enumerate(db.bones()):
            print("%3d %s" % (i, b))
    elif cmd == "chars":
        tb = RobMotTbl(sys.argv[2])
        db = MotDb(sys.argv[3]) if len(sys.argv) > 3 else None
        print("entrees=%d  roles=%d" % (tb.count, tb.nslot))
        for i, e in enumerate(tb.entries):
            lab = tb.label(i, db) if db else ""
            print("%3d  postures=%d  bloc0=0x%06X  %s"
                  % (i, e["nposture"], e["blocks"][0], lab))
    elif cmd == "slots":
        tb = RobMotTbl(sys.argv[2])
        db = MotDb(sys.argv[3])
        entry = int(sys.argv[4], 0)
        posture = int(sys.argv[5], 0) if len(sys.argv) > 5 else 0
        print("entree %d (%s), posture %d" % (entry, tb.label(entry, db), posture))
        for k, mid in enumerate(tb.slots(entry, posture)):
            if mid in (0, 0xFFFFFFFF):
                print("  role %3d  -" % k)
            else:
                v = db.id2name.get(mid)
                print("  role %3d  id=%-7d %s" % (k, mid, "%s / %s" % v if v else "?"))
    elif cmd == "diff":
        db = MotDb(sys.argv[2])
        a, b = RobMotTbl(sys.argv[3]), RobMotTbl(sys.argv[4])
        print("A: entrees=%d roles=%d   B: entrees=%d roles=%d"
              % (a.count, a.nslot, b.count, b.nslot))
        for i in range(min(a.count, b.count)):
            for p in range(min(a.entries[i]["nposture"], b.entries[i]["nposture"])):
                sa, sb = a.slots(i, p), b.slots(i, p)
                d = [k for k in range(min(len(sa), len(sb))) if sa[k] != sb[k]]
                if d:
                    print("entree %d (%s) posture %d : %d roles differents"
                          % (i, a.label(i, db), p, len(d)))
                    for k in d[:10]:
                        print("    role %3d : %s -> %s"
                              % (k, db.id2name.get(sa[k], sa[k]),
                                 db.id2name.get(sb[k], sb[k])))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
