# -*- coding: utf-8 -*-
"""Les SOUS-NUANCEURS du moteur APM3 et leurs tables de PRESENCE, lus dans la
DLL : pour chaque famille, combien de permutations existent et lesquelles sont
reellement chargees. Le descripteur fait 0x40 octets :

    +0x18 nb de programmes de SOMMETS   +0x1C nb de FRAGMENTS
    +0x20 noms (vp)                     +0x28 noms (fp)
    +0x30 presence (vp)                 +0x38 presence (fp)

Le chargeur 0x180175BF0 ne monte un programme que si son octet de presence est
non nul (0x180175D2B : cmp byte ptr [rax+rbp], 0 / je).

    py -3 desassemblage/brume_aoi_lindbergh_r/outil_presence_nuanceurs.py <dll>
"""
import os
import re
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
sys.path.insert(0, os.path.join(RACINE, 'outils'))
import pe_disasm as P                                           # noqa: E402


def main():
    chemin = sys.argv[1]
    img = P.Image(chemin)
    d = img.data

    def off(va):
        for s in img.secs:
            if s['va'] <= va < s['va'] + s['vsize']:
                o = s['off'] + (va - s['va'])
                return o if o < s['off'] + s['rsize'] else None

    def cstr(va):
        o = off(va)
        if o is None:
            return None
        try:
            e = d.index(b'\x00', o, o + 80)
        except ValueError:
            return None
        t = d[o:e]
        return t.decode('latin-1') if t and all(32 <= c < 127 for c in t) \
            else None

    rd = [s for s in img.secs if s['name'] == '.rdata'][0]
    print('%-18s %-20s %5s %5s %6s %6s' % ('descripteur', 'famille', 'nb_vp',
                                           'nb_fp', 'vp on', 'fp on'))
    for k in range(0, rd['rsize'] - 0x40, 8):
        b = rd['off'] + k
        nvp, nfp = struct.unpack_from('<II', d, b + 0x18)
        if not (0 < nvp <= 1024 and 0 < nfp <= 4096):
            continue
        pvn, pfn, pvp, pfp = struct.unpack_from('<4Q', d, b + 0x20)
        if not all(0x180000000 < x < 0x181000000
                   for x in (pvn, pfn, pvp, pfp)):
            continue
        o1 = off(pvn)
        if o1 is None:
            continue
        p0, = struct.unpack_from('<Q', d, o1)
        n0 = cstr(p0)
        if not n0 or not n0.endswith('.vp'):
            continue
        ov, of_ = off(pvp), off(pfp)
        if ov is None or of_ is None:
            continue
        pv, pf = d[ov:ov + nvp], d[of_:of_ + nfp]
        noms = []
        for i in range(nvp):
            p, = struct.unpack_from('<Q', d, o1 + i * 8)
            noms.append(cstr(p) or '?')
        print('0x%-16X %-20s %5d %5d %6d %6d'
              % (rd['va'] + k, n0.split('.')[0], nvp, nfp,
                 sum(1 for x in pv if x), sum(1 for x in pf if x)))
        ch = [noms[i] for i in range(nvp) if pv[i]]
        print('    vp charges : %s' % (', '.join(ch) if ch else '(aucun)'))


if __name__ == '__main__':
    main()
