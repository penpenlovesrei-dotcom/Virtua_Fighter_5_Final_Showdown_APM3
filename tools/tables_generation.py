# -*- coding: utf-8 -*-
r"""Les tables de decor d'une generation Lindbergh (VF5 ver.B, VF5 R), lues
dans SON binaire -- et comparees a ce que la DLL patchee applique.

Pourquoi : un decor importe a SES effets, SES murs et SES animations. On les
clonait sur le modele Final Showdown ; la table de VF5 R dit par exemple que
`hai` n'avait pas de tonnerre, ce que Frederic a vu a l'ecran sur hi5.

Rien n'est en dur ici hormis la FORME des tables : chacune est RETROUVEE dans
l'ELF par une valeur connue, puis parcourue jusqu'a ses bornes.

  descripteurs   le pointeur vers « STGDJO » ; pas = ecart djo(11) - ban(4)
  noms d'effets  le tableau de pointeurs vers « EFFECT_HIT »
  taches         0x60 par decor (comme 0x18034D570) : la liste de `slk`
  murs           {indice, morceaux, uid, paires, ...} : l'entree dont les
                 morceaux sont ceux de `djo`
  animations     {indice, liste} de 8 : la liste de `djo`

    py -3 tools/tables_generation.py r        VF5 R contre les entrees 42-60
    py -3 tools/tables_generation.py verb     VF5 ver.B contre 61-81
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

GENERATIONS = {
    'r': dict(elf=os.path.join(RACINE, 'extracted', 'LIND_R', 'id', 'disk0',
                               'vf5'),
              db=os.path.join(RACINE, 'extracted', 'decors', 'VF5R', '_db'),
              nom='VF5 R'),
    'verb': dict(elf=os.path.join(RACINE, 'extracted', 'LIND_VF5', 'id',
                                  'disk0', 'vf5'),
                 db=os.path.join(RACINE, 'extracted', 'decors', 'VF5_VERB',
                                 '_db'),
                 nom='VF5 ver.B'),
}


class Elf(object):
    def __init__(self, chemin):
        self.d = d = open(chemin, 'rb').read()
        shoff, = struct.unpack_from('<I', d, 0x20)
        shentsize, shnum, shstrndx = struct.unpack_from('<HHH', d, 0x2E)
        secs = []
        for i in range(shnum):
            nm, typ, flg, addr, off, size = struct.unpack_from(
                '<6I', d, shoff + i * shentsize)
            secs.append([nm, typ, flg, addr, off, size])
        stro = secs[shstrndx][4]
        self.sections = {}
        for s in secs:
            n = d[stro + s[0]:d.index(b'\x00', stro + s[0])].decode()
            if s[3] and s[1] != 8:                      # pas NOBITS
                self.sections[n] = (s[3], s[4], s[5])

    def off(self, va):
        for va0, o0, sz in self.sections.values():
            if va0 <= va < va0 + sz:
                return va - va0 + o0
        return None

    def va(self, off):
        for va0, o0, sz in self.sections.values():
            if o0 <= off < o0 + sz:
                return off - o0 + va0
        return None

    def u32(self, va):
        return struct.unpack_from('<I', self.d, self.off(va))[0]

    def i32(self, va):
        return struct.unpack_from('<i', self.d, self.off(va))[0]

    def chaine(self, va):
        o = self.off(va)
        if o is None:
            return None
        f = self.d.find(b'\x00', o)
        t = self.d[o:f]
        if f - o > 80 or not all(32 <= c < 127 for c in t):
            return None
        return t.decode()

    def refs(self, va):
        p = struct.pack('<I', va)
        out, i = [], -1
        while True:
            i = self.d.find(p, i + 1)
            if i < 0:
                return out
            v = self.va(i)
            if v is not None:
                out.append(v)


def lire(gen):
    """Toutes les tables de la generation, par CODE de decor."""
    import a3d_db
    g = GENERATIONS[gen]
    e = Elf(g['elf'])
    d = e.d

    # --- les descripteurs --------------------------------------------------
    def ptr_vers(texte):
        # « STGDJO » est souvent la QUEUE de « EFFSTGDJO » : l'editeur de
        # liens fusionne les chaines. On prend l'occurrence qui est pointee.
        o = -1
        while True:
            o = d.find(texte.encode() + b'\x00', o + 1)
            if o < 0:
                return []
            v = e.va(o)
            if v is None:
                continue
            r = e.refs(v)
            if r:
                return r
    p_djo = ptr_vers('STGDJO')
    p_ban = ptr_vers('STGBAN')
    if not p_djo or not p_ban:
        raise ValueError('descripteurs introuvables')
    pas = (p_djo[0] - p_ban[0]) // 7
    debut = p_djo[0] - 11 * pas
    codes = []
    k = 0
    while True:
        n = e.chaine(e.u32(debut + k * pas)) if e.off(debut + k * pas) else None
        if not n or not n.startswith('STG') or k > 64:
            break
        codes.append(n[3:].lower())
        k += 1

    # --- les noms des taches ------------------------------------------------
    o_hit = d.find(b'EFFECT_HIT\x00')
    p = e.refs(e.va(o_hit))[0]
    noms_t = []
    while True:
        s = e.chaine(e.u32(p + 4 * len(noms_t)))
        if not s or not s.startswith('EFFECT_'):
            break
        noms_t.append(s[len('EFFECT_'):])

    # --- les taches : la liste de slk, puis le debut de la table -----------
    i_wall = noms_t.index('WALL')
    slk = [noms_t.index(x) for x in ('WALL', 'WATER_RING', 'RIPPLE', 'SPLASH')]
    o = d.find(struct.pack('<4i', *slk))
    if o < 0:
        raise ValueError('liste de taches de slk introuvable')
    t_taches = e.va(o) - 0x20 - codes.index('slk') * 0x60
    taches, plus = {}, {}
    for i, c in enumerate(codes):
        base = t_taches + i * 0x60
        lst, ex = [], []
        for j in range(16):
            v = e.i32(base + 0x20 + 4 * j)
            if v == -1:
                break
            lst.append(noms_t[v])
        for j in range(8):
            v = e.i32(base + 4 * j)
            if v == -1:
                break
            ex.append(v)
        taches[c], plus[c] = lst, ex

    # --- les bases : uid -> nom, objet -> nom ------------------------------
    base_a = a3d_db.charger(os.path.join(g['db'], 'auth_3d_db.bin')).uids()
    od = open(os.path.join(g['db'], 'obj_db.bin'), 'rb').read()
    nj, _, tj, no, to = struct.unpack_from('<5I', od, 0)
    objets = {}
    for k in range(no):
        ident, po = struct.unpack_from('<2I', od, to + k * 8)
        objets[ident] = od[po:od.index(b'\x00', po)].decode('latin-1')
    jeux = {}
    for k in range(nj):
        po, ident = struct.unpack_from('<2I', od, tj + k * 0x24)
        jeux[od[po:od.index(b'\x00', po)].decode('latin-1')] = ident

    def nom_uid(u):
        return base_a.get(u, {}).get('value', '?%d' % u).split()[-1]

    # --- les animations : la liste de djo ----------------------------------
    uid_de = dict((v.get('value', '').split()[-1], k)
                  for k, v in base_a.items())
    djo = [uid_de[x] for x in ('STGDJO_EFF_HATA', 'STGDJO_EFF_FIRE',
                               'STGDJO_EFF_FIRE_REFLECT') if x in uid_de]
    anims = {}
    o = -1
    t_anims = None
    while True:
        o = d.find(struct.pack('<%di' % len(djo), *djo), o + 1)
        if o < 0:
            break
        for r in e.refs(e.va(o)):
            if e.i32(r - 4) == codes.index('djo'):
                t_anims = r - 4
    if t_anims is None:
        raise ValueError('table des animations introuvable')
    while 0 <= e.i32(t_anims - 8) < len(codes) and e.off(e.u32(t_anims - 4)):
        t_anims -= 8
    k = 0
    while e.i32(t_anims + 8 * k) != -1:
        i, lp = e.i32(t_anims + 8 * k), e.u32(t_anims + 8 * k + 4)
        lst = []
        while e.i32(lp + 4 * len(lst)) != -1:
            lst.append(nom_uid(e.i32(lp + 4 * len(lst))))
        anims[codes[i]] = lst
        k += 1

    # --- les murs : l'entree de djo -----------------------------------------
    id_djo = jeux['STGDJO']
    o = -1
    t_murs = pas_m = None
    while t_murs is None:
        o = d.find(struct.pack('<i', codes.index('djo')), o + 1)
        if o < 0:
            break
        if o % 4:
            continue
        v0 = e.va(o)
        if v0 is None:
            continue
        pm = struct.unpack_from('<I', d, o + 4)[0]
        if not e.off(pm):
            continue
        premier = e.u32(pm) if e.off(pm) else 0
        if premier >> 16 != id_djo:
            continue
        # le pas : l'entree suivante porte un indice de decor et un pointeur
        for cand in (0x14, 0x20, 0x24, 0x1C, 0x18):
            i2 = e.i32(v0 + cand)
            if 0 <= i2 < len(codes) or i2 == -1:
                p2 = e.u32(v0 + cand + 4)
                if i2 == -1 or (e.off(p2) and e.u32(p2) >> 16 == jeux.get(
                        'STG%s' % codes[i2].upper(), -2)):
                    t_murs, pas_m = v0, cand
                    break
    if t_murs is None:
        raise ValueError('table des murs introuvable')
    while True:
        i0 = e.i32(t_murs - pas_m)
        p0 = e.u32(t_murs - pas_m + 4)
        if 0 <= i0 < len(codes) and e.off(p0) and e.u32(p0) >> 16 == \
                jeux.get('STG%s' % codes[i0].upper(), -2):
            t_murs -= pas_m
        else:
            break
    # la taille d'un morceau : 0x28 (ver.B) ou 0x2C (FS) -- les deux premiers
    # morceaux de djo portent le meme objet, on cherche le pas qui le retrouve
    p_djo_m = None
    k = 0
    while e.i32(t_murs + k * pas_m) != -1:
        if e.i32(t_murs + k * pas_m) == codes.index('djo'):
            p_djo_m = e.u32(t_murs + k * pas_m + 4)
        k += 1
    pas_morceau = None
    for cand in (0x28, 0x2C, 0x30):
        if e.u32(p_djo_m + cand) >> 16 == id_djo and \
                e.u32(p_djo_m + 2 * cand) >> 16 == id_djo:
            pas_morceau = cand
            break
    murs = {}
    k = 0
    while e.i32(t_murs + k * pas_m) != -1:
        base = t_murs + k * pas_m
        i = e.i32(base)
        champs = [e.u32(base + 4 + 4 * j) for j in range((pas_m - 4) // 4)]
        pieces = []
        pp = champs[0]
        while e.i32(pp + len(pieces) * pas_morceau) != -1:
            o_p = e.off(pp + len(pieces) * pas_morceau)
            obj = struct.unpack_from('<I', d, o_p)[0]
            # 0x2C = le format de FS, un entier a +4 puis neuf flottants ;
            # 0x28 = celui de ver.B, les neuf flottants tout de suite.
            fl = struct.unpack_from('<9f', d,
                                    o_p + (8 if pas_morceau == 0x2C else 4))
            pieces.append((objets.get(obj, '?%X' % obj), fl))
        uids = []
        if champs[1]:
            while e.i32(champs[1] + 4 * len(uids)) != -1:
                uids.append(nom_uid(e.i32(champs[1] + 4 * len(uids))))
        paires = []
        if champs[2]:
            while e.i32(champs[2] + 0x10 * len(paires)) != -1:
                q = [e.i32(champs[2] + 0x10 * len(paires) + 4 * j)
                     for j in range(4)]
                paires.append((objets.get(q[0] & 0xFFFFFFFF, '-'),
                               objets.get(q[1] & 0xFFFFFFFF, '-'),
                               nom_uid(q[2]) if q[2] != -1 else '-',
                               nom_uid(q[3]) if q[3] != -1 else '-'))
        murs[codes[i]] = dict(pieces=pieces, uids=uids, paires=paires,
                              autres=[hex(x) for x in champs[3:] if x])
        k += 1
    return dict(codes=codes, noms_taches=noms_t, taches=taches, plus=plus,
                anims=anims, murs=murs, adresses=dict(
                    descripteurs=debut, pas_desc=pas, taches=t_taches,
                    animations=t_anims, murs=t_murs, pas_murs=pas_m,
                    pas_morceau=pas_morceau))


# ---------------------------------------------------------------------------
# CE QUE LA DLL PATCHEE APPLIQUE
# ---------------------------------------------------------------------------
def applique(indices_codes, source_de):
    """{code neuf: {'taches', 'anims', 'mur'}} lus dans la DLL PATCHEE.

    `source_de[code]` = le code du decor source (pour remettre les noms dans
    la nomenclature de la generation : STGBN5_ -> STGBAN_)."""
    import pefile
    import a3d_db
    import obj_db
    import patch_moteur as pm
    media = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media')
    dll = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                       'vf5fs-pxd-w64-Retail_APM3.dll')
    pe = pefile.PE(dll, fast_load=True)
    B = 0x180000000

    def rd(a, n):
        return pe.get_data(a - B, n)

    def table(site):
        return site + 4 + struct.unpack('<i', rd(site, 4))[0]

    def entree(site, pas, indice):
        t = table(site)
        for r in range(256):
            e = rd(t + r * pas, pas)
            v = struct.unpack_from('<i', e, 0)[0]
            if v == -1:
                return None
            if v == indice:
                return e
        return None
    pose = a3d_db.charger(os.path.join(media, 'rom', 'auth_3d',
                                       'auth_3d_db.bin')).uids()
    o = obj_db.charger(os.path.join(media, 'rom', 'objset', 'obj_db.bin'))
    noms_obj = dict((i, o.nom_b(p)) for i, p in o.objets)
    t_obj = table(0x18006F675)
    out = {}
    for indice, code in indices_codes:
        src = source_de[code]

        def remettre(n, _c=code, _s=src):
            return n.replace('STG%s_' % _c.upper(), 'STG%s_' % _s.upper())
        t = []
        for j in range(16):
            v = struct.unpack_from('<i', rd(t_obj + indice * 0x60 + 0x20 + 4 * j,
                                            4))[0]
            if v == -1:
                break
            t.append(pm.EFFETS_NOMS[v].replace('EFFECT_', ''))
        anims = []
        e_a = entree(0x1800706BC, 0x10, indice)
        if e_a is not None:
            p = struct.unpack_from('<Q', e_a, 8)[0]
            while True:
                v = struct.unpack('<i', rd(p + 4 * len(anims), 4))[0]
                if v == -1:
                    break
                anims.append(remettre(pose.get(v, {}).get('value',
                                                         '?%d' % v).split()[-1]))
        mur = None
        e_m = entree(0x1800843B0, 0x40, indice)
        if e_m is not None:
            q = struct.unpack_from('<7Q', e_m, 8)
            pieces = []
            while True:
                rec = rd(q[0] + len(pieces) * 0x2C, 0x2C)
                ob = struct.unpack_from('<I', rec, 0)[0]
                if ob == 0xFFFFFFFF:
                    break
                pieces.append((remettre(noms_obj.get(ob, '?%X' % ob)),
                               struct.unpack_from('<9f', rec, 8)))
            uids = []
            if q[1]:
                while True:
                    v = struct.unpack('<i', rd(q[1] + 4 * len(uids), 4))[0]
                    if v == -1:
                        break
                    uids.append(remettre(pose.get(v, {}).get(
                        'value', '?%d' % v).split()[-1]))
            mur = dict(pieces=pieces, uids=uids)
        out[code] = dict(taches=t, anims=anims, mur=mur)
    return out


def _cle_piece(nom, fl):
    return (nom.upper(), tuple(round(x, 2) for x in fl[:6]))


def comparer(gen):
    """Rend [(code neuf, source, manques, en_trop)] par categorie."""
    g = lire(gen)
    if gen == 'r':
        import variantes_5r
        lot = [(i, c, m) for m, c, i, _ in variantes_5r.DECORS_5R]
    else:
        import variantes_vf5
        lot = [(e['indice'], e['code'],
                e['verb']) for e in variantes_vf5.entrees()]
    source_de = {}
    for i, c, s in lot:
        if gen == 'verb':
            import variantes_vf5
            source_de[c] = variantes_vf5.par_code(
                variantes_vf5.par_code(c)['geo'])['source']
        else:
            source_de[c] = s
    ap = applique([(i, c) for i, c, _ in lot], source_de)
    lignes = []
    for i, c, s in lot:
        a = ap[c]
        t_gen = [x for x in g['taches'].get(s, [])]
        an_gen = g['anims'].get(s, [])
        m_gen = g['murs'].get(s)
        r = dict(code=c, source=s, indice=i)
        r['taches_manquent'] = [x for x in t_gen if x not in a['taches']]
        r['taches_en_trop'] = [x for x in a['taches'] if x not in t_gen]
        r['anims_manquent'] = [x for x in an_gen if x not in a['anims']]
        r['anims_en_trop'] = [x for x in a['anims'] if x not in an_gen]
        if m_gen is None and a['mur'] is None:
            r['mur'] = 'aucun des deux cotes'
        elif m_gen is None:
            r['mur'] = 'EN TROP : %d morceaux (%s) que %s n avait pas' % (
                len(a['mur']['pieces']),
                ' '.join(sorted(set(p[0].split('_EFF_')[-1]
                                    for p in a['mur']['pieces']))),
                GENERATIONS[gen]['nom'])
        elif a['mur'] is None:
            r['mur'] = 'MANQUE : %d morceaux (%s)' % (
                len(m_gen['pieces']),
                ' '.join(sorted(set(p[0].upper().split('_EFF_')[-1]
                                    for p in m_gen['pieces']))))
        else:
            kg = sorted(_cle_piece(n, f) for n, f in m_gen['pieces'])
            ka = sorted(_cle_piece(n, f[:6]) for n, f in a['mur']['pieces'])
            # FS a un entier en +4 : ses 9 flottants sont a +8 ; ver.B et R
            # ont les leurs a +4. On compare x y z rx ry rz.
            if kg == ka:
                r['mur'] = 'identique (%d morceaux)' % len(kg)
            else:
                ng = sorted(set(n for n, _ in kg))
                na = sorted(set(n for n, _ in ka))
                r['mur'] = 'DIFFERENT : %s a %d morceaux %s ; applique %d %s' % (
                    GENERATIONS[gen]['nom'], len(kg),
                    ' '.join(x.split('_EFF_')[-1] for x in ng), len(ka),
                    ' '.join(x.split('_EFF_')[-1] for x in na))
            um = [x for x in m_gen['uids'] if x.upper() not in
                  [y.upper() for y in a['mur']['uids']]]
            if um:
                r['mur'] += ' ; uid manquants %s' % um
        lignes.append(r)
    return g, lignes


def main():
    gen = sys.argv[1] if len(sys.argv) > 1 else 'r'
    g, lignes = comparer(gen)
    print('%s -- tables relues : %s' % (GENERATIONS[gen]['nom'], dict(
        (k, hex(v) if isinstance(v, int) else v)
        for k, v in g['adresses'].items())))
    for r in lignes:
        print('%-4s (%s, %d)' % (r['code'], r['source'], r['indice']))
        print('   taches : manquent %s   en trop %s'
              % (r['taches_manquent'] or '-', r['taches_en_trop'] or '-'))
        print('   anims  : manquent %s   en trop %s'
              % (r['anims_manquent'] or '-', r['anims_en_trop'] or '-'))
        print('   mur    : %s' % r['mur'])


if __name__ == '__main__':
    main()
