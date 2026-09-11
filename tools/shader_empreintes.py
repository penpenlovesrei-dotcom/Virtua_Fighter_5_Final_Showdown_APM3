#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Le shader des EMPREINTES DANS LA NEIGE, rendu au portage PC (ykb, ver.B).

POURQUOI (2026-09-11, mesure a la sonde, puis lu dans le code et les donnees)

Frederic : « les empreintes de pas dans la neige ne fonctionnent toujours
pas » -- et « dans la version FS du stage de Wolf, il n'y a pas de neige sur
le sol du ring ». FS n'utilise JAMAIS SNOW_RING : son code et ses shaders sont
la, aucun de ses decors ne cree la tache. Le defaut est donc passe inapercu
au portage PC.

  * la logique est saine : a la sonde sur ykb, les chevilles et les orteils
    (os 12 a 15 de la table 0x180350FF0, y de 0,0 a 0,15 m) ajoutent des
    milliers d'empreintes par combat ; la table d'os et les squelettes sont
    identiques chez ver.B et FS (`bone_data.bin`, 149 os d'objet) ;
  * chaque empreinte est un POINT (`glPointSize(6)`, mode 2 -> topologie
    D3D11 POINTLIST, 0x180245EA0) dessine dans une cible de 512 x 512 qui
    couvre un anneau de 12 m : 6 pixels = 14 cm, un pied ;
  * le moteur APM3 tourne sur Direct3D 11, ou un point fait TOUJOURS un
    pixel. Le portage a donc donne un geometry shader aux cinq programmes de
    points (conteneurs `GSFX` : fog_ptcl, particle.1, snow_particle.0/1,
    water_particle) -- et PAS a `snow_footprint..vp`, reste un simple `GSVS`
    alors que son shader de sommets sort deja la taille (COLOR1.x, lue en
    TEXCOORD6 = l'attribut 14 pose par 0x18007E420). Les empreintes font 1
    pixel (2,3 cm) : un corps qui glisse creuse un sillon, un pas rien.

LE REMEDE : le conteneur `GSFX` qui manque, fait comme les cinq du portage.

  GSFX   +0x00 'GSFX', 0x20, 0x00050001, taille totale
         +0x10 u16 somme des lettres du nom, puis le nom (cle du cache,
               0x180269BD0 -- 0x57A = « snow_particle », verifie)
         +0x30 (decalage, taille) du GSVS, du GSPS, du GSGS ; +0x48 la
               taille totale, +0x4C 0 (pas de stream-out)
  GSVS   celui de FS, TEL QUEL (le shader de sommets est bon)
  GSPS   le pixel shader nul des conteneurs du portage, TEL QUEL
  GSGS   +0x00 'GSGS', 0x20, 0x00050001, taille du DXBC ; +0x10 0x10000000 ;
         +0x18 0x80, taille ; +0x20 vingt octets = CLE du cache
         (0x1802716A0 compare les seize premiers) ; DXBC en +0x80

Le geometry shader reprend a l'instruction pres celui des flocons : un point
devient un carre de `taille` pixels, `cb12[28].xy` valant (2/L, -2/H) du
viewport COURANT (0x18025E830, recalcule a chaque viewport par
0x180261840 -- 512 x 512 pendant la passe des empreintes).

Le moteur lit chaque shader PAR SON NOM dans `w64/shader_pxd_w64.farc`
(0x1801767D0). L'archive de FS n'est pas touchee : on pose a cote
`w64/shader_vf5_w64.farc`, qui ne contient QUE `snow_footprint..vp`, et le
patcheur fait ouvrir celle-ci pour ce seul nom (voir patch_moteur,
SHADER_EMPREINTES_SITE).

    py -3 tools/shader_empreintes.py              fabrique et pose
    py -3 tools/shader_empreintes.py --controle   relit ce qui est pose
"""
import ctypes
import hashlib
import os
import re
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import farc                                                  # noqa: E402

MEDIA = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media')
ARCHIVE_FS = os.path.join(MEDIA, 'w64', 'shader_pxd_w64.farc')
ARCHIVE_VF5 = os.path.join(MEDIA, 'w64', 'shader_vf5_w64.farc')
CHEMIN_VF5 = 'w64/shader_vf5_w64.farc'        # tel que le moteur l'ouvre
MEMBRE = 'snow_footprint..vp'
NOM_EFFET = 'snow_footprint'
MODELE_GSFX = 'snow_particle.0.vp'            # le GSPS nul vient d'ici
VERSION = 0x00050001

# Signature de SORTIE du shader de sommets de FS (lue au desassembleur) : le
# geometry shader la reprend a l'identique en entree ET en sortie, pour que
# le pixel shader se lie exactement comme sans lui.
HLSL = r"""
cbuffer CB12 : register(b12) { float4 c[29]; };
struct V {
    float4 col  : TEXCOORD8;
    float4 tex  : TEXCOORD0;
    float  size : COLOR1;
    float4 pos  : SV_POSITION;
};
[maxvertexcount(4)]
void main(point V i[1], inout TriangleStream<V> s)
{
    float2 h = c[28].xy * i[0].size * i[0].pos.w * 0.5;
    V o;
    o.col = i[0].col;
    o.size = i[0].size;
    o.tex = float4(0, 0, 0, 1); o.pos = i[0].pos + float4(-h.x, -h.y, 0, 0); s.Append(o);
    o.tex = float4(0, 1, 0, 1); o.pos = i[0].pos + float4(-h.x,  h.y, 0, 0); s.Append(o);
    o.tex = float4(1, 0, 0, 1); o.pos = i[0].pos + float4( h.x, -h.y, 0, 0); s.Append(o);
    o.tex = float4(1, 1, 0, 1); o.pos = i[0].pos + float4( h.x,  h.y, 0, 0); s.Append(o);
    s.RestartStrip();
}
"""


class Refus(Exception):
    pass


# ---------------------------------------------------------------------------
# d3dcompiler_47 (Windows) : compiler et desassembler
# ---------------------------------------------------------------------------
def _d3d():
    return ctypes.WinDLL('d3dcompiler_47.dll')


def _blob(p):
    vt = ctypes.cast(ctypes.cast(p, ctypes.POINTER(ctypes.c_void_p))[0],
                     ctypes.POINTER(ctypes.c_void_p))
    ptr = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(vt[3])(p)
    n = ctypes.WINFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p)(vt[4])(p)
    octets = ctypes.string_at(ptr, n)
    ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)(vt[2])(p)
    return octets


def compiler(source, entree, cible):
    d3d = _d3d()
    code = ctypes.c_void_p()
    err = ctypes.c_void_p()
    src = source.encode('ascii')
    hr = d3d.D3DCompile(src, ctypes.c_size_t(len(src)), b'empreintes', None,
                        None, entree.encode(), cible.encode(), 0, 0,
                        ctypes.byref(code), ctypes.byref(err))
    if hr != 0:
        msg = _blob(err).decode('latin-1') if err.value else ''
        raise Refus('D3DCompile 0x%X : %s' % (hr & 0xFFFFFFFF, msg))
    return _blob(code)


def desassembler(dxbc):
    d3d = _d3d()
    out = ctypes.c_void_p()
    buf = ctypes.create_string_buffer(dxbc, len(dxbc))
    hr = d3d.D3DDisassemble(buf, ctypes.c_size_t(len(dxbc)), 0, None,
                            ctypes.byref(out))
    if hr != 0:
        raise Refus('D3DDisassemble 0x%X' % (hr & 0xFFFFFFFF))
    return _blob(out).decode('latin-1').rstrip('\0')


def signature(texte, genre):
    """Les elements (nom, indice, registre) d'une signature desassemblee."""
    lignes = texte.split('// %s signature:' % genre, 1)[1].splitlines()
    elements = []
    tirets = False
    for ligne in lignes[1:]:
        if ligne.startswith('// ----'):
            tirets = True
            continue
        if not tirets:
            continue
        if ligne.strip() in ('//', ''):
            break
        m = re.match(r'//\s+(\w+)\s+(\d+)\s+([xyzw ]+?)\s+(\d+)\s', ligne)
        if not m:
            raise Refus('ligne de signature illisible : %r' % ligne)
        elements.append((m.group(1).upper(), int(m.group(2)),
                         m.group(3).strip(), int(m.group(4))))
    if not elements:
        raise Refus('signature %s vide ou illisible' % genre)
    return elements


# ---------------------------------------------------------------------------
# Les conteneurs du portage
# ---------------------------------------------------------------------------
def dxbc_de(cont):
    off, taille = struct.unpack_from('<II', cont, 0x18)
    return cont[off:off + taille]


def sous_blocs(gsfx):
    if gsfx[:4] != b'GSFX':
        raise Refus('pas un GSFX')
    blocs = []
    for k in range(3):
        off, taille = struct.unpack_from('<II', gsfx, 0x30 + 8 * k)
        blocs.append(gsfx[off:off + taille])
    return blocs


def conteneur_gs(dxbc):
    tete = bytearray(0x80)
    tete[0:4] = b'GSGS'
    struct.pack_into('<III', tete, 4, 0x20, VERSION, len(dxbc))
    struct.pack_into('<IIII', tete, 0x10, 0x10000000, 0, 0x80, len(dxbc))
    tete[0x20:0x34] = hashlib.sha1(dxbc).digest()
    return bytes(tete) + dxbc


def gsfx(nom, vs, ps, gs):
    def aligne(n):
        return (n + 0xF) & ~0xF
    off_vs = 0x50
    off_ps = aligne(off_vs + len(vs))
    off_gs = aligne(off_ps + len(ps))
    total = aligne(off_gs + len(gs))
    b = bytearray(total)
    b[0:4] = b'GSFX'
    struct.pack_into('<III', b, 4, 0x20, VERSION, total)
    struct.pack_into('<H', b, 0x10, sum(nom.encode('ascii')) & 0xFFFF)
    b[0x12:0x12 + len(nom)] = nom.encode('ascii')
    struct.pack_into('<8I', b, 0x30, off_vs, len(vs), off_ps, len(ps),
                     off_gs, len(gs), total, 0)
    b[off_vs:off_vs + len(vs)] = vs
    b[off_ps:off_ps + len(ps)] = ps
    b[off_gs:off_gs + len(gs)] = gs
    return bytes(b)


def membre_fs(nom):
    a = farc.Farc(ARCHIVE_FS)
    for e in a.entries:
        if e['name'] == nom:
            return a.read(e)
    raise Refus('%s absent de %s' % (nom, ARCHIVE_FS))


def fabriquer():
    vs = membre_fs(MEMBRE)
    if vs[:4] != b'GSVS':
        raise Refus('%s de FS n est pas un GSVS (%r) : deja un GSFX ?'
                    % (MEMBRE, vs[:4]))
    ps = sous_blocs(membre_fs(MODELE_GSFX))[1]
    if ps[:4] != b'GSPS':
        raise Refus('le second bloc de %s n est pas un GSPS' % MODELE_GSFX)
    gs_dxbc = compiler(HLSL, 'main', 'gs_5_0')
    # la liaison : sortie du VS == entree du GS, et la sortie du GS la meme
    t_vs = desassembler(dxbc_de(vs))
    t_gs = desassembler(gs_dxbc)
    s_vs = signature(t_vs, 'Output')
    e_gs = signature(t_gs, 'Input')
    s_gs = signature(t_gs, 'Output')
    if not (s_vs == e_gs == s_gs):
        raise Refus('signatures : VS %s / GS entree %s / GS sortie %s'
                    % (s_vs, e_gs, s_gs))
    if 'gs_5_0' not in t_gs or 'cb12[28]' not in t_gs:
        raise Refus('le geometry shader compile ne lit pas cb12[28]')
    return gsfx(NOM_EFFET, vs, ps, conteneur_gs(gs_dxbc)), s_vs


def controler():
    """Relit l'archive posee : un seul membre, un GSFX dont le GSVS est celui
    de FS octet pour octet et dont le GS a la bonne signature."""
    if not os.path.exists(ARCHIVE_VF5):
        return ['%s absente' % ARCHIVE_VF5]
    a = farc.Farc(ARCHIVE_VF5)
    # (le lecteur voit une entree vide dans le remplissage de l'en-tete
    # qu'ecrit `ecrire_farc` ; le moteur lit ces archives -- celles des
    # decors en sortent -- et on ne compte donc que les noms)
    entrees = [e for e in a.entries if e['name']]
    noms = [e['name'] for e in entrees]
    if noms != [MEMBRE]:
        return ['membres %s, attendu [%s]' % (noms, MEMBRE)]
    b = a.read(entrees[0])
    fautes = []
    try:
        vs, ps, gs = sous_blocs(b)
    except Refus as e:
        return [str(e)]
    if vs != membre_fs(MEMBRE):
        fautes.append('le GSVS differe de celui de FS')
    if ps != sous_blocs(membre_fs(MODELE_GSFX))[1]:
        fautes.append('le GSPS differe de celui de %s' % MODELE_GSFX)
    if gs[:4] != b'GSGS' or gs[0x20:0x34] != hashlib.sha1(dxbc_de(gs)).digest():
        fautes.append('le GSGS est mal forme')
    else:
        t = desassembler(dxbc_de(gs))
        if signature(t, 'Input') != signature(desassembler(dxbc_de(vs)),
                                              'Output'):
            fautes.append('le GS ne prend pas la sortie du VS')
    nom = b[0x12:0x30].split(b'\0', 1)[0].decode('ascii')
    if nom != NOM_EFFET or struct.unpack_from('<H', b, 0x10)[0] != \
            sum(NOM_EFFET.encode()) & 0xFFFF:
        fautes.append('cle du GSFX : %r' % nom)
    return fautes


def main():
    a = sys.argv[1:]
    try:
        if '--controle' in a:
            fautes = controler()
            for f in fautes:
                print('FAUTE : %s' % f)
            print('shader des empreintes : %s'
                  % ('CONFORME' if not fautes else '%d faute(s)' % len(fautes)))
            return 1 if fautes else 0
        b, sig = fabriquer()
        farc.ecrire_farc(ARCHIVE_VF5, {MEMBRE: b})
        print('pose : %s (%s, %d octets ; signature %s)'
              % (ARCHIVE_VF5, MEMBRE, len(b),
                 ' '.join('%s%d.%s/r%d' % s for s in sig)))
        fautes = controler()
        for f in fautes:
            print('FAUTE : %s' % f)
        return 1 if fautes else 0
    except Refus as e:
        print('REFUS : %s' % e)
        return 1


if __name__ == '__main__':
    sys.exit(main())
