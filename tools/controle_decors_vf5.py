# -*- coding: utf-8 -*-
r"""Controle avant vol des decors AJOUTES d'une generation -- VF5 R ou le VF5
d'origine (ver.B) --, dans la DLL patchee, CONTRE LE BINAIRE DE LA GENERATION.

Depuis le 2026-09-11 (Frederic : « applique a VF5 R ses propres listes, rien
ne doit venir de FS, applique les effets VF5 a VF5 »), ce que le decor
CONTIENT vient de sa generation. Ce controle le remesure par un AUTRE chemin
que le patcheur (un controle ne doit pas repeter l'hypothese de l'outil qu'il
controle) : il relit la DLL patchee, remet chaque identifiant dans la
nomenclature de la generation, et compare a `generation.py`.

  1. les pieces posees ;
  2. `obj_db` : chaque objset pose est declare, ni plus ni moins que son
     archive, objets bien renommes ;
  3. `auth_3d_db` : chaque uid a son `.a3da`, chaque objet nomme est declare ;
  4. les TEXTURES de nos objsets : chaque identifiant designe chez FS la
     texture du meme nom, ou n'y est pas (ver.B : renumerotees) ;
  5. le DESCRIPTEUR : objets relus PAR NOM (`STG<source>_GND`...), chaines,
     reflets d'objectif ;
  6. les objsets EN PLUS (le ciel des Dural de ver.B) ;
  7. les TACHES : aucune que la generation n'avait, et chacune a son dossier ;
  8. les DOSSIERS d'effet : les memes valeurs que ceux de la generation ;
  9. le MUR : morceaux (noms ET positions), uid, paires -- ceux de la
     generation ;
 10. les ANIMATIONS et la poussiere de chute : celles de la generation ;
 11. le SHADER DES EMPREINTES, des qu'une entree recoit SNOW_RING : le site
     0x180176829 passe par un stub qui ouvre NOTRE archive pour le seul
     « snow_footprint..vp », et cette archive est conforme
     (`shader_empreintes.controler`).

    py -3 tools/controle_decors_vf5.py          le VF5 d'origine (ver.B)
    py -3 tools/controle_decors_vf5.py r        VF5 R
"""
import os
import re
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
MEDIA = os.path.join(RACINE, r'runtime\media\vf5fs\vf5fs_media')
DLL = os.path.join(RACINE, r'runtime\media\vf5fs\vf5fs-pxd-w64-Retail_APM3.dll')
BASE = 0x180000000

import a3d_db                                                   # noqa: E402
import obj_db as mod_objdb                                      # noqa: E402
import pefile                                                   # noqa: E402
import variantes_5r                                             # noqa: E402
import variantes_vf5                                            # noqa: E402
import decor_neuf                                               # noqa: E402
import patch_moteur                                             # noqa: E402
import generation                                               # noqa: E402

EFFETS_NOMS = patch_moteur.EFFETS_NOMS
DECOR_NOMS = patch_moteur.DECOR_NOMS
SERVIS = patch_moteur.EFFETS_SERVIS
ROLES = ('gnd', 'ring', 'sky', 'sdw', 'reflect')
# les tables des dossiers, relues dans la DLL patchee par le site qui les
# nomme : (nom, numero de tache, site du disp32, pas, decalage de l'indice)
SITES = (('SNOW', 5, 0x18007D211, 0x58, 0), ('THUNDER', 9, 0x180082619, 0x20,
                                              0x1C),
         ('SPLASH', 14, 0x180080A33, 0x38, 0), ('FOG_ANIM', 16, 0x180071B41,
                                                0x34, 0),
         ('BREATH', 19, 0x180070E06, 0x14, 0), ('RIPPLE', 7, 0x18007AE25,
                                                0x2C, 0),
         ('LEAF', 3, 0x180074ECD, 0x0C, 0))


def lire_stub(rd, nom, indice):
    """Le dossier que le STUB de `nom` recopie pour `indice` (voir
    patch_moteur.GENERATION_STUBS), relu dans la DLL patchee en suivant le
    code : l'appel (ou le creneau de vtable) -> le stub -> son `lea`.
    Rend (dossier, None) ou (None, raison)."""
    if nom == 'YUKA':
        d = dict(vtable=patch_moteur.YUKA_VTABLE,
                 defaut=patch_moteur.YUKA_SETSTAGE,
                 pas=generation.CHAMPS['YUKA']['pas'], indice=True)
        # les cinq litteraux : trois `call` et deux `mov rax, [rip+var]`
        for s in (patch_moteur.YUKA_SITE_JEU, patch_moteur.YUKA_SITE_UID,
                  patch_moteur.YUKA_SITE_OBJET):
            if rd(s, 1) != b'\xe8':
                return None, 'le litteral 0x%X n est pas detourne' % s
        for s in patch_moteur.YUKA_SITES_TABLE:
            if rd(s, 3) != b'\x48\x8b\x05':
                return None, 'la table 0x%X est encore lue en dur' % s
    else:
        d = patch_moteur.GENERATION_STUBS[nom]
    if 'site' in d:
        brut = rd(d['site'], 5)
        if brut[0] != 0xE8:
            return None, 'l appel 0x%X n est pas detourne' % d['site']
        stub = d['site'] + 5 + struct.unpack('<i', brut[1:])[0]
    else:
        stub = struct.unpack('<Q', rd(d['vtable'], 8))[0]
        if stub == d['defaut']:
            return None, 'le creneau 0x%X est encore le `ret 0`' % d['vtable']
    if rd(stub, 3) != b'\x48\x8d\x05' or rd(stub + 7, 2) != b'\x41\xb9':
        return None, 'le stub 0x%X n a pas la forme attendue' % stub
    table = stub + 7 + struct.unpack('<i', rd(stub + 3, 4))[0]
    n = struct.unpack('<I', rd(stub + 9, 4))[0]
    pas = d['pas'] if d['indice'] else 4 + d['pas']
    for r in range(n):
        e = rd(table + r * pas, pas)
        if struct.unpack_from('<i', e, 0)[0] == indice:
            return (e if d['indice'] else e[4:]), None
    return None, 'indice %d absent de la table du stub' % indice


def table_stub(rd, site, cible_attendue=None):
    """La table {a, b} (fin -1) d'un stub de la greffe atteint par le `call`
    en `site` (ou, si `site` est un creneau de vtable, par son pointeur). Le
    stub porte un seul `lea rcx, [rip+table]`. Rend {a: b} ou None."""
    brut = rd(site, 8)
    if cible_attendue is None:              # un creneau de vtable
        stub = struct.unpack('<Q', brut)[0]
    elif brut[0] == 0xE8:
        stub = site + 5 + struct.unpack('<i', brut[1:5])[0]
    else:
        return None
    code = rd(stub, 0x40)
    k = code.find(b'\x48\x8d\x0d')
    if k < 0:
        return None
    t = stub + k + 7 + struct.unpack('<i', code[k + 3:k + 7])[0]
    out = {}
    for r in range(64):
        a, b = struct.unpack('<iI', rd(t + 8 * r, 8))
        if a == -1:
            break
        out[a] = b
    return out


def lire_ringout(rd, indice):
    """Le dossier RINGOUT_SPLASH de `indice`, dans le tableau que les deux
    `lea` du setStage bornent (il n'a pas de terminateur), et le texte de sa
    chaine. Rend (dossier, texte) ou (None, raison)."""
    def cible(site):
        return site + 4 + struct.unpack('<i', rd(site, 4))[0]
    debut = cible(patch_moteur.RINGOUT_SITE_DEBUT)
    fin = cible(patch_moteur.RINGOUT_SITE_FIN)
    pas = patch_moteur.RINGOUT_TABLE_PAS
    if (fin - debut) % pas or not 0 < fin - debut <= 64 * pas:
        return None, 'bornes 0x%X..0x%X incoherentes' % (debut, fin)
    brut = rd(patch_moteur.RINGOUT_SITE_POUSSEE, 5)
    stub = patch_moteur.RINGOUT_SITE_POUSSEE + 5 + struct.unpack(
        '<i', brut[1:])[0]
    if brut[0] != 0xE8 or rd(stub, 5) != b'\x83\x7c\x3b\x4c\xff':
        return None, 'la poussee de 0x%X n est pas gardee' % (
            patch_moteur.RINGOUT_SITE_POUSSEE)
    for a in range(debut, fin, pas):
        e = rd(a, pas)
        if struct.unpack_from('<i', e, 0)[0] == indice:
            p = struct.unpack_from('<Q', e, 0x10)[0]
            t = rd(p, patch_moteur.RINGOUT_CHAINE_MAX)
            return e, t[:t.find(b'\x00')].decode('latin-1')
    return None, 'indice %d absent du tableau' % indice


def lire_wet_cloth(rd, indice):
    """Le scalaire que FS choisira pour `indice` : 0,4 si le stub rend
    l'indice (il est dans sa table), sinon 0,001 (indice != 19)."""
    brut = rd(patch_moteur.WET_CLOTH_SITE, 5)
    dans = False
    if brut[0] == 0xE8:
        stub = patch_moteur.WET_CLOTH_SITE + 5 + struct.unpack('<i',
                                                              brut[1:])[0]
        t = stub + 10 + struct.unpack('<i', rd(stub + 6, 4))[0]
        for r in range(64):
            v = struct.unpack('<i', rd(t + 4 * r, 4))[0]
            if v == -1:
                break
            dans = dans or v == indice
    elif brut != b'\xb8\x13\x00\x00\x00':
        return None
    return struct.pack('<I', 0x3ECCCCCD if dans or indice == 19
                       else 0x3A83126F)


def main(lot='verb'):
    fautes = []
    pe = pefile.PE(DLL, fast_load=True)
    sec = [s for s in pe.sections if s.Name.rstrip(b'\x00') == b'.decors']
    if not sec:
        print('REFUS : la DLL n a pas de section .decors.')
        return 1
    va = BASE + sec[0].VirtualAddress

    def rd(a, n):
        return pe.get_data(a - BASE, n)

    def ch(v):
        if not v:
            return ''
        d = rd(v, 96)
        return d[:d.find(b'\x00')].decode('latin-1')

    def table(site):
        return site + 4 + struct.unpack('<i', rd(site, 4))[0]

    def entree(site, pas, indice, decal=0):
        t = table(site)
        for r in range(256):
            e = rd(t + r * pas, pas)
            v = struct.unpack_from('<i', e, decal)[0]
            if v == -1:
                return None
            if v == indice:
                return e
        return None

    def dense(site, indice):
        return struct.unpack('<i', rd(table(site) + indice * 4, 4))[0]

    def liste(a, pas, champs):
        out = []
        while True:
            rec = rd(a + len(out) * pas, pas)
            if struct.unpack_from('<i', rec, 0)[0] == -1 or len(out) > 512:
                break
            out.append(struct.unpack_from('<%di' % champs, rec, 0))
        return out

    t_obj = table(0x18006F675)
    o = mod_objdb.charger(os.path.join(MEDIA, r'rom\objset\obj_db.bin'))
    a = a3d_db.charger(os.path.join(MEDIA, r'rom\auth_3d\auth_3d_db.bin'))
    import tex_db
    _t = tex_db.charger(os.path.join(RACINE, 'extracted', 'tex_db.bin'))
    fs = dict((i, _t.nom(p)) for i, p in _t.textures)
    ids_r = variantes_vf5.ids_textures_5r()
    if lot == 'r':
        # les quatre Dural de VF5 R, s'ils sont DANS LA DLL (le descripteur 82
        # porte leur objset) : le controle suit ce qui est patche
        d82 = struct.unpack('<I', rd(va + variantes_5r.DURAL_5R[0][2] * 0xF0
                                     + 0x10, 4))[0]
        ents = variantes_5r.entrees(dural=d82 == variantes_5r.DURAL_5R[0][3])
        poses = [(e['geo'], e['objset'], e['source']) for e in ents]
        g = generation.generation('r')
    else:
        ents = variantes_vf5.entrees()
        poses = variantes_vf5.objsets_poses()
        g = generation.generation('verb')
        carte, _, _ = variantes_vf5.carte_textures()

    print('=' * 78)
    print('CONTROLE AVANT VOL -- les %d entrees de %s, contre SON binaire'
          % (len(ents), g.nom))
    print('=' * 78)
    print('%-4s %-4s %-3s %-5s %-7s %-7s %-24s %s'
          % ('code', 'mod', 'idx', 'objst', 'pieces', 'obj_db', 'taches',
             'mur'))

    # --- 2 et 4 : chaque OBJSET pose, une fois ---------------------------
    objsets_ok = {}
    for code, objset, source in poses:
        f_o = []
        _, e = o.jeu('STG%s' % code.upper())
        decl = dict(o.objets_de(objset)) if e else {}
        arch = variantes_5r.objets_archive(code) or []
        ids_obj = set(r for r, _ in arch)
        if e is None:
            f_o.append('STG%s absent d obj_db' % code.upper())
        elif e[1] != objset:
            f_o.append('obj_db donne l identifiant %d' % e[1])
        if set(decl) != ids_obj:
            f_o.append('obj_db ne decrit pas l archive (%d declares, %d '
                       'presents)' % (len(decl), len(ids_obj)))
        attendus = dict((r, n.upper().replace('STG%s_' % source.upper(),
                                              'STG%s_' % code.upper()))
                        for r, n in arch)
        faux = [r for r in decl if decl[r].upper() != attendus.get(r)]
        if faux:
            f_o.append('%d objet(s) mal nommes dans obj_db' % len(faux))
        tex = variantes_vf5.textures_objset(code) or []
        mauvais = []
        for t in tex:
            n_fs = fs.get(t)
            if lot == 'r':
                n_gen = g.nom_texture(t)
                if n_fs is not None and n_gen is not None and n_fs != n_gen:
                    mauvais.append('%d=%s/%s' % (t, n_gen, n_fs))
            elif n_fs is not None:
                if carte.get(n_fs) != t:
                    mauvais.append('%d=%s' % (t, n_fs))
            elif t in ids_r:
                mauvais.append('%d (pris par VF5 R)' % t)
        if len(set(tex)) != len(tex):
            f_o.append('identifiants de texture en double')
        if mauvais:
            f_o.append('%d texture(s) dont le numero designe AUTRE CHOSE '
                       'chez FS (%s)' % (len(mauvais), mauvais[:2]))
        objsets_ok[code] = (len(decl), len(ids_obj), f_o, dict(arch))
        fautes += ['stg%s : %s' % (code, x) for x in f_o]

    neige = []                          # les entrees qui recoivent SNOW_RING
    for e in ents:
        ligne_fautes, notes = [], []
        code, indice, cle = e['code'], e['indice'], e['cle']
        geo, src_geo = e['geo'], e['src_geo']
        arch_geo = objsets_ok[geo][3]

        def remettre(valeur):
            return valeur.replace('STG%s_' % geo.upper(),
                                  'STG%s_' % src_geo.upper())

        # 1. les pieces
        lot_p = (decor_neuf.pieces_vf5(e) if lot == 'verb'
                 else decor_neuf.toutes_les_pieces(code))
        pp = [os.path.exists(os.path.join(MEDIA, 'rom', dest, nom))
              for _, nom, dest in lot_p]
        if not all(pp):
            ligne_fautes.append('%d piece(s) absente(s)' % (len(pp) - sum(pp)))

        # 3. auth_3d_db
        eff = a.uids_de('EFFSTG%s' % e['eff'].upper())
        a_nous = set(eff)
        if e['source'] is not None:
            import farc as mod_farc
            for prefixe in ('STG', 'EFFSTG'):
                cat = '%s%s' % (prefixe, code.upper())
                arch_a = os.path.join(MEDIA, 'rom', 'auth_3d', '%s.farc' % cat)
                membres, nommes = set(), set()
                if os.path.exists(arch_a):
                    f = mod_farc.Farc(arch_a)
                    membres = set(x['name'] for x in f.entries)
                    for x in f.entries:
                        for mm in re.findall(rb'uid_name=([A-Za-z0-9_]+)',
                                             f.read(x)):
                            nommes.add(mm.decode().upper())
                sans = [v for v in a.uids_de(cat).values()
                        if v['value'].split()[-1] + '.a3da' not in membres]
                if sans:
                    ligne_fautes.append('%s : %d uid sans .a3da'
                                        % (cat, len(sans)))
                decl_noms = set(n.upper().replace(
                    'STG%s_' % src_geo.upper(), 'STG%s_' % geo.upper())
                    for n in arch_geo.values())
                hors = sorted(x for x in nommes if x not in decl_noms)
                if hors:
                    ligne_fautes.append('%s nomme %d objet(s) hors obj_db '
                                        '(%s)' % (cat, len(hors), hors[:2]))

        # 5. le descripteur -- les objets PAR NOM
        d = rd(va + indice * 0xF0, 0xF0)
        if struct.unpack_from('<I', d, 0x10)[0] != e['objset']:
            ligne_fautes.append('objset %d au lieu de %d'
                                % (struct.unpack_from('<I', d, 0x10)[0],
                                   e['objset']))
        textes = [ch(struct.unpack_from('<Q', d, k)[0]) for k in (0, 8, 0x48)]
        attendus = [e['a3d'], 'EFFSTG%s' % e['eff'].upper(),
                    'rom/STG%s_COLI.000.bin' % e['coli'].upper()]
        if textes != attendus:
            ligne_fautes.append('chaines %s au lieu de %s'
                                % (textes, attendus))
        dg = g.descripteur(cle)
        objets = struct.unpack_from('<5I', d, 0x14)
        for role, v in zip(ROLES, objets):
            voulu = dg['objets'].get(role, 0xFFFFFFFF)
            if v == 0xFFFFFFFF or voulu == 0xFFFFFFFF:
                if (v == 0xFFFFFFFF) != (voulu == 0xFFFFFFFF):
                    ligne_fautes.append('%s : %s au lieu de %s'
                                        % (role, v, voulu))
                continue
            hi, rang = v >> 16, v & 0xFFFF
            if hi == e['objset']:
                nom = arch_geo.get(rang)
            elif e['ciel'] is not None and hi == e['ciel'][1]:
                nom = objsets_ok[e['ciel'][0]][3].get(rang)
            else:
                ligne_fautes.append('%s : objset %d inattendu' % (role, hi))
                continue
            if nom is None or nom.upper() != g.objets.get(voulu, '').upper():
                ligne_fautes.append('%s = %s au lieu de %s'
                                    % (role, nom, g.objets.get(voulu)))
        notes.append('+'.join(r for r, v in zip(ROLES, objets)
                              if v != 0xFFFFFFFF))

        # 6. les objsets en plus -- lus COMME LE MOTEUR, jusqu'au premier -1
        plus = []
        for v in struct.unpack_from('<8i', rd(t_obj + indice * 0x60, 0x20), 0):
            if v == -1:
                break
            plus.append(v)
        voulu_plus = [e['ciel'][1]] if e['ciel'] is not None else []
        if plus != voulu_plus:
            ligne_fautes.append('objsets en plus %s au lieu de %s'
                                % (plus, voulu_plus))

        # 7. les taches
        t_n = list(struct.unpack_from('<16i', rd(t_obj + indice * 0x60, 0x60),
                                      0x20))
        t_n = t_n[:t_n.index(-1)] if -1 in t_n else t_n
        if EFFETS_NOMS.index('EFFECT_SNOW_RING') in t_n:
            neige.append(code)
        t_g = g.taches(cle)
        for v in t_n:
            if v not in t_g or v not in SERVIS:
                ligne_fautes.append('tache %s absente de %s ou non servie'
                                    % (EFFETS_NOMS[v], g.nom))
        manquees = [EFFETS_NOMS[v].replace('EFFECT_', '')
                    for v in t_g if v not in t_n]
        if manquees:
            notes.append('%s avait aussi %s' % (g.nom.split()[-1],
                                                '/'.join(manquees)))

        # 8. les dossiers : ceux de la generation
        tex_geo = set(variantes_vf5.textures_objset(geo) or [])
        if e['ciel'] is not None:
            tex_geo |= set(variantes_vf5.textures_objset(e['ciel'][0]) or [])
        a_verifier = []
        for nom_t, num_t, site_t, pas_t, decal_t in SITES:
            if num_t not in t_n:
                continue
            rec = entree(site_t, pas_t, indice, decal_t)
            if rec is None:
                ligne_fautes.append('%s demandee sans dossier' % nom_t)
                continue
            a_verifier.append((nom_t, rec, pas_t, decal_t))
        # 8 bis. les taches a STUB : le dossier que le stub recopie
        for nom_t, num_t in patch_moteur.GENERATION_TACHES:
            if num_t not in t_n:
                continue
            if nom_t == 'WET_CLOTH':
                rec, pourquoi = lire_wet_cloth(rd, indice), 'site modifie'
            else:
                rec, pourquoi = lire_stub(rd, nom_t, indice)
            if rec is None:
                ligne_fautes.append('%s demandee, mais %s' % (nom_t, pourquoi))
                continue
            champs_t = generation.CHAMPS[nom_t]
            a_verifier.append((nom_t, rec, champs_t['pas'],
                               None if champs_t.get('sans_indice') else 0))
        if 12 in t_n:
            rec, texte = lire_ringout(rd, indice)
            if rec is None:
                ligne_fautes.append('RINGOUT_SPLASH demandee, mais %s' % texte)
            else:
                a_verifier.append(('RINGOUT_SPLASH', rec, 0x20, 0))
                ref_r = g.dossiers('RINGOUT_SPLASH').get(cle)
                if ref_r is not None and texte != g.chaine(
                        struct.unpack_from('<Q', ref_r, 0x10)[0]):
                    ligne_fautes.append('RINGOUT_SPLASH : chaine « %s »'
                                        % texte)
        for nom_t, rec, pas_t, decal_t in a_verifier:
            ref = g.dossiers(nom_t).get(cle)
            if ref is None:
                ligne_fautes.append('%s : %s n a pas de dossier' % (nom_t,
                                                                   g.nom))
                continue
            champs = generation.CHAMPS[nom_t]
            speciaux = set(champs.get('uids', ())) | set(
                champs.get('tex', ())) | set(champs.get('objets', ())) | set(
                champs.get('jeux', ()))
            if 'chaine' in champs:          # un pointeur : relu a part
                speciaux |= {champs['chaine'], champs['chaine'] + 4}
            for k in champs.get('jeux', ()):
                if struct.unpack_from('<I', rec, k)[0] != e['objset'] or \
                        struct.unpack_from('<I', ref, k)[0] != \
                        g.objset_de(src_geo):
                    ligne_fautes.append('%s : objset +0x%X' % (nom_t, k))
            if nom_t == 'THUNDER':
                speciaux.add(0x1C)
            elif decal_t is not None:
                speciaux.add(decal_t)
            diff = [k for k in range(0, pas_t, 4) if k not in speciaux and
                    rec[k:k + 4] != ref[k:k + 4]]
            if diff:
                ligne_fautes.append('%s : %d champ(s) differents de %s (+%s)'
                                    % (nom_t, len(diff), g.nom,
                                       ' +'.join('0x%X' % k for k in diff[:3])))
            # les TEXTURES : dans nos objsets, et la meme image que chez la
            # generation (par NOM chez ver.B, par numero chez R)
            for k in champs.get('tex', ()):
                t_n_ = struct.unpack_from('<I', rec, k)[0]
                t_g_ = struct.unpack_from('<I', ref, k)[0]
                if 0xFFFFFFFF in (t_n_, t_g_):      # « pas de texture »
                    if t_n_ != t_g_:
                        ligne_fautes.append('%s : texture +0x%X %d au lieu '
                                            'de %d' % (nom_t, k, t_n_, t_g_))
                    continue
                if t_n_ not in tex_geo:
                    ligne_fautes.append('%s : texture %d hors de nos objsets'
                                        % (nom_t, t_n_))
                elif lot == 'r' and t_n_ != t_g_:
                    ligne_fautes.append('%s : texture %d au lieu de %d'
                                        % (nom_t, t_n_, t_g_))
                elif lot == 'verb' and carte.get(g.nom_texture(t_g_)) != t_n_:
                    ligne_fautes.append('%s : texture %d n est pas %s'
                                        % (nom_t, t_n_, g.nom_texture(t_g_)))
            # les OBJETS : notre objset, le rang qui porte le meme nom
            fautes_o = len(ligne_fautes)
            for k in champs.get('objets', ()):
                if len(ligne_fautes) - fautes_o >= 3:
                    ligne_fautes.append('%s : ...' % nom_t)
                    break
                o_n = struct.unpack_from('<I', rec, k)[0]
                o_g = struct.unpack_from('<I', ref, k)[0]
                if 0xFFFFFFFF in (o_n, o_g):        # « pas d'objet »
                    if o_n != o_g:
                        ligne_fautes.append('%s : objet +0x%X 0x%X au lieu '
                                            'de 0x%X' % (nom_t, k, o_n, o_g))
                    continue
                if o_n >> 16 == e['objset']:
                    arch_o = arch_geo
                elif e['ciel'] is not None and o_n >> 16 == e['ciel'][1]:
                    arch_o = objsets_ok[e['ciel'][0]][3]
                else:
                    arch_o = {}
                if arch_o.get(o_n & 0xFFFF, '').upper() != \
                        g.objets.get(o_g, '?').upper():
                    ligne_fautes.append('%s : objet %d:%d au lieu de %s'
                                        % (nom_t, o_n >> 16, o_n & 0xFFFF,
                                           g.objets.get(o_g)))
            for k in champs.get('uids', ()):
                u_n = struct.unpack_from('<i', rec, k)[0]
                u_g = struct.unpack_from('<i', ref, k)[0]
                if (u_n == -1) != (u_g == -1):
                    ligne_fautes.append('%s : uid +0x%X' % (nom_t, k))
                elif u_n != -1 and remettre(eff.get(u_n, {}).get(
                        'value', '?')) != g.valeur_uid(u_g):
                    ligne_fautes.append('%s : uid +0x%X = %s' % (
                        nom_t, k, eff.get(u_n, {}).get('value')))
        # 8 ter. LES COMPORTEMENTS CABLES (patch_moteur.CABLAGES_APPELS) :
        # ceux que la generation a, relus dans la DLL site par site
        for nom_c, c_c in sorted(g.cablages().items()):
            if cle in c_c['codes']:
                alias = DECOR_NOMS.index(cle)
                for s_c in patch_moteur.CABLAGES_APPELS.get(nom_c, ()):
                    tab = table_stub(rd, s_c, True) or {}
                    if tab.get(indice) != alias:
                        ligne_fautes.append('%s : 0x%X ne rend pas %d -> %d'
                                            % (nom_c, s_c, indice, alias))
                if nom_c in patch_moteur.CABLAGES_DRAPEAUX:
                    tab = table_stub(rd, patch_moteur.A3D_VTABLE7) or {}
                    if tab.get(indice) != patch_moteur.CABLAGES_DRAPEAUX[nom_c]:
                        ligne_fautes.append('%s : drapeau +0x%X absent'
                                            % (nom_c, patch_moteur.
                                               CABLAGES_DRAPEAUX[nom_c]))
                if c_c['objet'] is not None:
                    tab = table_stub(rd, patch_moteur.CABLAGE_REFLET_SITE,
                                     True) or {}
                    o_n = tab.get(indice)
                    if o_n is None or o_n >> 16 != e['objset'] or \
                            arch_geo.get(o_n & 0xFFFF, '').upper() != \
                            g.objets.get(c_c['objet'], '?').upper():
                        ligne_fautes.append('%s : objet %s' % (nom_c, o_n))
                notes.append('cable:%s' % nom_c)
            for nom_a in c_c['uids']:
                n_u = [k for k, v in eff.items()
                       if remettre(v.get('value', '')).split()[-1] == nom_a]
                if not n_u:
                    continue
                tabs = [table_stub(rd, s, True) or {}
                        for s in patch_moteur.A3D_UID_SITES]
                if not tabs or any(t.get(n_u[0]) is None for t in tabs) or \
                        len(set(t.get(n_u[0]) for t in tabs)) != 1:
                    ligne_fautes.append('uid %s non traduit aux quatre sites'
                                        % nom_a)
                notes.append('uid:%s' % nom_a.split('_EFF_')[-1])
        if 13 in t_n:
            saut = struct.unpack('<i', rd(0x180085631, 4))[0]
            stub = 0x180085630 + 5 + saut
            tw = stub + 3 + 7 + struct.unpack('<i', rd(stub + 6, 4))[0]
            vu = None
            for r in range(64):
                i_e, o_e = struct.unpack('<iI', rd(tw + r * 8, 8))
                if i_e == -1:
                    break
                if i_e == indice:
                    vu = o_e
            o_g, r_g = g.objet_anneau_eau()
            if vu is None or vu >> 16 != e['objset'] or \
                    arch_geo.get(vu & 0xFFFF, '').upper() != \
                    g.objets.get((o_g << 16) | r_g, '').upper():
                ligne_fautes.append('WATER_RING : objet %s' % vu)
        v_d = dense(0x1800713EF, indice)
        g_d = g.down(cle)
        if (v_d == -1) != (g_d is None):
            ligne_fautes.append('DOWN %d au lieu de %s' % (v_d, g_d))
        elif v_d != -1 and remettre(eff.get(v_d, {}).get('value', '?')) != g_d:
            ligne_fautes.append('DOWN = %s au lieu de %s'
                                % (eff.get(v_d, {}).get('value'), g_d))
        if dense(0x1800770AF, indice) != -1:
            ligne_fautes.append('MOVE pose, alors que %s n a pas EFF_DASH'
                                % g.nom)

        # 9. le mur -- celui de la generation, PAR NOM et PAR POSITION
        dit_mur = '-'
        e_mur = entree(0x1800843B0, 0x40, indice)
        w = g.mur(cle)
        if 2 in t_n and e_mur is None:
            ligne_fautes.append('WALL demandee sans entree de mur')
        if e_mur is not None and 2 not in t_n:
            ligne_fautes.append('entree de mur sans la tache WALL')
        if e_mur is not None and w is None:
            ligne_fautes.append('entree de mur alors que %s n en a pas'
                                % g.nom)
        if e_mur is None and w is not None and 2 in t_g:
            notes.append('SANS le mur de %s' % g.nom)
        if e_mur is not None and w is not None:
            q = struct.unpack_from('<7Q', e_mur, 8)
            recs = []
            while True:
                rec = rd(q[0] + len(recs) * 0x2C, 0x2C)
                if struct.unpack_from('<i', rec, 0)[0] == -1 or len(recs) > 256:
                    break
                recs.append(rec)
            dit_mur = '%d morceaux' % len(recs)
            if len(recs) != len(w['pieces']):
                ligne_fautes.append('%d morceaux au lieu des %d de %s'
                                    % (len(recs), len(w['pieces']), g.nom))
            for rec, (obj_g, flottants) in zip(recs, w['pieces']):
                obj = struct.unpack_from('<I', rec, 0)[0]
                if obj >> 16 != e['objset'] or \
                        arch_geo.get(obj & 0xFFFF, '').upper() != \
                        g.objets.get(obj_g, '').upper():
                    ligne_fautes.append('morceau %d:%d au lieu de %s'
                                        % (obj >> 16, obj & 0xFFFF,
                                           g.objets.get(obj_g)))
                    break
                if rec[8:0x2C] != flottants:
                    ligne_fautes.append('morceau : position differente de %s'
                                        % g.nom)
                    break
            lus = [remettre(eff.get(v, {}).get('value', '?'))
                   for (v,) in (liste(q[1], 4, 1) if q[1] else [])]
            voulus = [x for x in w['uids']]
            if lus != voulus:
                ligne_fautes.append('uid de mur %s au lieu de %s'
                                    % ([x.split()[-1] for x in lus],
                                       [x.split()[-1] for x in voulus]))
            if (w['p20'] is not None) != bool(q[3]):
                ligne_fautes.append('second tableau de morceaux')
            for nom_c, k_c in (('u28', 4), ('o30', 5), ('u38', 6)):
                if w[nom_c] is not None and not q[k_c]:
                    notes.append('sans %s' % nom_c)

        # 10. les animations -- celles de la generation, PAR NOM
        e_a3d = entree(0x1800706BC, 0x10, indice)
        lues = []
        if e_a3d is not None:
            for (v,) in liste(struct.unpack_from('<Q', e_a3d, 8)[0], 4, 1):
                if v not in a_nous:
                    ligne_fautes.append('animation : uid %d etranger' % v)
                else:
                    lues.append(remettre(eff[v]['value']).split()[-1])
        voulues = [x.split()[-1] for x in g.animations(cle)]
        if lues != voulues:
            ligne_fautes.append('animations %s au lieu de %s'
                                % ([x.split()[-1] for x in lues],
                                   [x.split()[-1] for x in voulues]))
        if lues:
            notes.append('%d anim' % len(lues))

        dit_t = ' '.join(EFFETS_NOMS[v].replace('EFFECT_', '')
                         for v in t_n) or '-'
        nb_decl, nb_arch, _, _ = objsets_ok[geo]
        print('%-4s %-4s %-3d %-5d %-7s %-7s %-24s %s%s%s'
              % (code, e['modele'], indice, e['objset'],
                 '%d/%d' % (sum(pp), len(pp)), '%d/%d' % (nb_decl, nb_arch),
                 dit_t, dit_mur,
                 '  (%s)' % ' '.join(notes) if notes else '',
                 '' if not ligne_fautes
                 else '   <<< ' + ' ; '.join(ligne_fautes)))
        fautes += ['%s : %s' % (code, x) for x in ligne_fautes]

    # 11. le SHADER DES EMPREINTES -- relu dans ce que la DLL porte : le site,
    # les trois `lea` du stub et leurs cibles, puis l'archive posee
    if neige:
        import shader_empreintes
        f_sh = []
        s = patch_moteur.SHADER_EMPREINTES_SITE
        b = rd(s, 7)
        if b[0] != 0xE8 or b[5:] != b'\x66\x90':
            f_sh.append('0x%X n appelle pas de stub (%s)' % (s, b.hex()))
        else:
            v = s + 5 + struct.unpack('<i', b[1:5])[0]
            code_s = rd(v, 45)

            def cible(k):
                return v + k + 7 + struct.unpack('<i', code_s[k + 3:k + 7])[0]
            vus = [(code_s[k:k + 3], cible(k)) for k in (0, 7, 37)]
            if vus[0] != (b'\x48\x8d\x15', patch_moteur.SHADER_ARCHIVE_FS_VA) \
                    or ch(vus[0][1]) != 'w64/shader_pxd_w64.farc':
                f_sh.append('le stub ne rend pas le chemin de FS par defaut')
            if vus[1][0] != b'\x4c\x8d\x15' or \
                    ch(vus[1][1]) != shader_empreintes.MEMBRE:
                f_sh.append('le stub ne compare pas a « %s »'
                            % shader_empreintes.MEMBRE)
            if vus[2][0] != b'\x48\x8d\x15' or \
                    ch(vus[2][1]) != shader_empreintes.CHEMIN_VF5:
                f_sh.append('le stub ne rend pas %s'
                            % shader_empreintes.CHEMIN_VF5)
            if code_s != patch_moteur.stub_shader_empreintes(
                    v, vus[1][1], vus[2][1]):
                f_sh.append('le stub en 0x%X differe de celui du patcheur' % v)
        f_sh += shader_empreintes.controler()
        print('shader des empreintes (%s) : %s'
              % (' '.join(neige), 'conforme' if not f_sh
                 else '<<< ' + ' ; '.join(f_sh)))
        fautes += ['empreintes : %s' % x for x in f_sh]

    print()
    print('-' * 78)
    if fautes:
        print('%d FAUTE(S) :' % len(fautes))
        for x in fautes:
            print('   . %s' % x)
        return 1
    print('RIEN A REDIRE -- les %d entrees de %s sont conformes a SON binaire.'
          % (len(ents), g.nom))
    print('-' * 78)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'verb'))
