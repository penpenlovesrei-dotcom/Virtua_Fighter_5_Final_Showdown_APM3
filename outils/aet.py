#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lecteur de planches AET -- scenes, compositions, calques, ET LEUR TRANSFORME.

Le format AET est celui de Project DIVA, **et il est explicitement partage par
Virtua Fighter 5**. Structure reprise de `AetPlugin` (samyuu),
`src/comfy/file_format_aet_set.cpp`, lu et non execute :
https://github.com/samyuu/AetPlugin

Pourquoi ce lecteur. La grille de selection de la borne est une SEULE scene,
`SEL_CHARA`, dont les cases sont des calques. La table en memoire compte vingt
cases dont Dural, la planche contient ses calques -- mais elle ne s'affiche
pas. Reste une question que seul le fichier peut trancher : **la composition
place-t-elle vingt cases, ou dix-neuf ?**

Disposition, pointeurs 32 bits :

    fichier   suite de pointeurs de scenes, terminee par un zero

    scene     +0x00 nom (ptr)        +0x04 debut  +0x08 fin  +0x0C cadence
              +0x10 couleur de fond  +0x14 resolution (2 x i32)
              +0x1C camera (ptr)
              +0x20 nb compositions  +0x24 compositions (ptr)
              +0x28 nb videos        +0x2C videos (ptr)
              +0x30 nb audios        +0x34 audios (ptr)

    compo     +0x00 nb calques       +0x04 calques (ptr)     -- 8 octets
              la DERNIERE composition est la racine

    calque    +0x00 nom (ptr)   +0x04 debut  +0x08 fin  +0x0C decalage
              +0x10 echelle de temps  +0x14 drapeaux (u16)
              +0x16 qualite (u8)      +0x17 type (u8)
              +0x18 element (ptr)     +0x1C parent (ptr)
              +0x20 nb marqueurs      +0x24 marqueurs (ptr)
              +0x28 video (ptr)       +0x2C audio (ptr)      -- 48 octets


LE BLOC `+0x28` -- LA TRANSFORME DU CALQUE (mesure le 2026-10-12)
================================================================

C'est la piece qui manquait, et c'est la qu'habite **l'echelle**. Quarante-huit
octets, releves sur `aet_n_adv.bin` :

    +0x00 u8 mode de transfert   +0x01 u8 drapeaux   +0x02 u8 cache   +0x03 ---
    +0x04 Origine.X     \\
    +0x0C Origine.Y      |
    +0x14 Position.X     |
    +0x1C Position.Y     |  HUIT proprietes, 8 octets chacune :
    +0x24 Rotation       |      u32 nombre de cles   u32 pointeur
    +0x2C Echelle.X      |
    +0x34 Echelle.Y      |
    +0x3C Opacite       /
    +0x44 perspective / 3D (ptr, nul sur tout ce qu'on a lu)

**CE QUI PROUVE L'ORDRE**, et ce n'est pas la documentation : sur la scene
`MAIN` de `aet_n_adv` (resolution 1280x768), les deux calques racine donnent

    Origine  = (640, 384)      Position = (640, 384)
    Rotation = 0   Echelle = (1, 1)   Opacite = 1

soit **exactement le centre de la scene**, pour l'ancre comme pour le
placement. Un ordre decale ne produirait pas deux fois 640/384.

Second temoin : la cinquieme propriete (Rotation) pointe souvent AILLEURS que
ses voisines -- `0x20E0` quand les autres se suivent en `0x19D0`.. -- parce que
sa valeur, 0, est mise en commun par l'ecrivain. La seule propriete
systematiquement nulle est bien la rotation.

LES CLES. `nombre == 1` : le pointeur designe **un seul flottant**, la valeur
constante. `nombre > 1` : N trames, PUIS N couples (valeur, courbe) -- soit
3N flottants d'affilee. Verifie octet pour octet sur l'opacite de
`n_adv_beta_black.pic` (7 cles en `0x270`) : trames 0, 311, 312, 313, 321,
322, 323 -- croissantes et dans la duree de la scene -- et valeurs 1, 1, 1,
0,9, 0,1, 0, 0,0024, c'est-a-dire un fondu. Le bloc s'arrete a 0x2C4 = 0x270 +
3 x 7 x 4, et la suite est a zero.


LA SURFACE (`video`) -- 20 octets, et elle NOMME LE SPRITE
=========================================================

    +0x00 u32 couleur       +0x04 u16 largeur   +0x06 u16 hauteur
    +0x08 f32 images par fichier
    +0x0C u32 nb sources    +0x10 u32 sources (ptr)
    source : +0x00 nom (ptr)   +0x04 identifiant       -- 8 octets

Le COMPTE PRECEDE le pointeur, contrairement aux compositions. Mesure sur
`aet_n_adv` : douze surfaces, dont la premiere fait **902 x 186** -- la taille
meme que `analysis` releve pour le sprite `ATTENTION_01` de `spr_n_adv` -- et
sa source se nomme `N_ADV_ATTENTION_01`. Les noms des dix sources se lisent en
clair ; deux surfaces sont des bouchons (32x32, zero source).

C'est ce chainon qui permet de repondre a la question utile : **quels calques
dessinent telle planche**, et donc lesquels remettre a l'echelle quand on
remplace une texture par sa version 4K.

Usage :
    py -3 tools/aet.py <fichier.bin>                 la liste des scenes
    py -3 tools/aet.py <fichier.bin> <scene>         les calques, transforme
                                                     comprise
    py -3 tools/aet.py <fichier.bin> --surfaces      les surfaces et leurs
                                                     sprites
    py -3 tools/aet.py <fichier.bin> --sprite <nom>  les calques qui dessinent
                                                     ce sprite (motif libre)
"""
import struct
import sys

TAILLE_CALQUE = 0x30
TAILLE_VIDEO = 0x14
TAILLE_TRANSFORME = 0x48
TYPES = {0: 'aucun', 1: 'video', 2: 'audio', 3: 'composition'}
# L'ordre est MESURE (voir l'en-tete), pas repris d'une documentation.
PROPRIETES = ('Origine.X', 'Origine.Y', 'Position.X', 'Position.Y',
              'Rotation', 'Echelle.X', 'Echelle.Y', 'Opacite')


class Aet:
    def __init__(self, chemin):
        with open(chemin, 'rb') as fp:
            self.d = fp.read()

    # --- lectures de base -------------------------------------------------
    def u32(self, o):
        return struct.unpack_from('<I', self.d, o)[0]

    def u16(self, o):
        return struct.unpack_from('<H', self.d, o)[0]

    def f32(self, o):
        return struct.unpack_from('<f', self.d, o)[0]

    def tient(self, o, n):
        """Vrai si `n` octets tiennent a partir de `o`. Un fichier qui n'est
        pas un AetSet -- `aet_db.bin`, par exemple -- donne des pointeurs
        absurdes, et le lecteur doit le dire plutot que lever."""
        return o > 0 and o + n <= len(self.d)

    def chaine(self, o):
        if not o or o >= len(self.d):
            return ''
        fin = self.d.index(b'\0', o)
        return self.d[o:fin].decode('latin-1')

    # --- scenes, compositions, calques ------------------------------------
    def scenes(self):
        out = []
        o = 0
        while self.tient(o + 1, 4):
            p = self.u32(o)
            if p == 0:
                break
            out.append(p)
            o += 4
        return out

    def scene(self, p):
        return dict(
            offset=p,
            nom=self.chaine(self.u32(p)),
            debut=self.f32(p + 4), fin=self.f32(p + 8),
            cadence=self.f32(p + 0xC),
            resolution=(self.u32(p + 0x14), self.u32(p + 0x18)),
            n_compo=self.u32(p + 0x20), compos=self.u32(p + 0x24),
            n_video=self.u32(p + 0x28), videos=self.u32(p + 0x2C),
            n_audio=self.u32(p + 0x30), audios=self.u32(p + 0x34))

    def compositions(self, sc):
        out = []
        for i in range(sc['n_compo']):
            o = sc['compos'] + 8 * i
            if not self.tient(o, 8):
                break
            out.append((self.u32(o), self.u32(o + 4)))
        return out

    def calques(self, n, p):
        out = []
        for i in range(n):
            o = p + TAILLE_CALQUE * i
            if not self.tient(o, TAILLE_CALQUE):
                break
            out.append(dict(
                offset=o,
                nom=self.chaine(self.u32(o)),
                debut=self.f32(o + 4), fin=self.f32(o + 8),
                type=self.d[o + 0x17],
                element=self.u32(o + 0x18),
                parent=self.u32(o + 0x1C),
                video=self.u32(o + 0x28)))
        return out

    # --- la transforme : le bloc `+0x28` ----------------------------------
    def propriete(self, o):
        """Rend une propriete animable. `o` designe le couple (nombre, ptr).

        Constante : {'valeur': x}. Animee : {'cles': [(trame, valeur,
        courbe), ...]}. Les deux portent toujours `nombre` et `ptr`, pour
        qu'on puisse ECRIRE dessus sans refaire la recherche.
        """
        n, p = struct.unpack_from('<II', self.d, o)
        r = dict(offset=o, nombre=n, ptr=p, valeur=None, cles=None)
        if n == 1 and self.tient(p, 4):
            r['valeur'] = self.f32(p)
        elif n > 1 and self.tient(p, 12 * n):
            trames = struct.unpack_from('<%df' % n, self.d, p)
            reste = struct.unpack_from('<%df' % (2 * n), self.d, p + 4 * n)
            r['cles'] = [(trames[i], reste[2 * i], reste[2 * i + 1])
                         for i in range(n)]
        return r

    def transforme(self, v):
        """Les 0x48 octets du bloc `+0x28` d'un calque."""
        if not self.tient(v, TAILLE_TRANSFORME):
            return None
        t = dict(offset=v, transfert=self.d[v], drapeaux=self.d[v + 1],
                 cache=self.d[v + 2],
                 perspective=self.u32(v + 4 + 8 * 8))
        for k, nom in enumerate(PROPRIETES):
            t[nom] = self.propriete(v + 4 + 8 * k)
        return t

    # --- les surfaces, et le sprite qu'elles nomment ----------------------
    def surfaces(self, sc):
        out = []
        for i in range(sc['n_video']):
            o = sc['videos'] + TAILLE_VIDEO * i
            if not self.tient(o, TAILLE_VIDEO):
                break
            n, p = self.u32(o + 0xC), self.u32(o + 0x10)
            src = []
            for k in range(n):
                q = p + 8 * k
                if not self.tient(q, 8):
                    break
                src.append((self.chaine(self.u32(q)), self.u32(q + 4)))
            out.append(dict(offset=o, couleur=self.u32(o),
                            largeur=self.u16(o + 4), hauteur=self.u16(o + 6),
                            cadence=self.f32(o + 8), sources=src))
        return out


def _val(p):
    if p is None:
        return '?'
    if p['valeur'] is not None:
        return '%g' % p['valeur']
    if p['cles']:
        return '%d cles %g..%g' % (p['nombre'], p['cles'][0][1],
                                   p['cles'][-1][1])
    return '?'


def _tous_calques(a, sc):
    """Tous les calques de la scene, composition par composition."""
    for i, (n, ptr) in enumerate(a.compositions(sc)):
        for c in a.calques(n, ptr):
            yield i, c


def cmd_surfaces(a, sc):
    print('     %d surface(s) :' % sc['n_video'])
    for i, s in enumerate(a.surfaces(sc)):
        noms = ', '.join(n for n, _ in s['sources']) or '(aucune source)'
        print('       %2d  %4d x %-4d  %s' % (i, s['largeur'], s['hauteur'],
                                              noms))


def cmd_sprite(a, sc, motif):
    """Les calques qui dessinent un sprite dont le nom contient `motif`."""
    par_offset = {s['offset']: s for s in a.surfaces(sc)}
    m = motif.lower()
    trouves = 0
    for i, c in _tous_calques(a, sc):
        if c['type'] != 1:
            continue
        s = par_offset.get(c['element'])
        if s is None:
            continue
        if not any(m in n.lower() for n, _ in s['sources']):
            continue
        t = a.transforme(c['video'])
        trouves += 1
        print('       compo %-3d calque %-28s surface %4d x %-4d  %s'
              % (i, c['nom'], s['largeur'], s['hauteur'],
                 ', '.join(n for n, _ in s['sources'])))
        if t:
            print('                  position (%s, %s)  echelle (%s, %s)  '
                  'origine (%s, %s)  opacite %s'
                  % (_val(t['Position.X']), _val(t['Position.Y']),
                     _val(t['Echelle.X']), _val(t['Echelle.Y']),
                     _val(t['Origine.X']), _val(t['Origine.Y']),
                     _val(t['Opacite'])))
            print('                  echelle ecrite en 0x%X / 0x%X'
                  % (t['Echelle.X']['ptr'], t['Echelle.Y']['ptr']))
    if not trouves:
        print('       aucun calque ne dessine un sprite contenant %r' % motif)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    a = Aet(sys.argv[1])
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    motif = None
    if arg == '--sprite':
        if len(sys.argv) < 4:
            print('--sprite attend un nom (ou un morceau de nom)')
            return 1
        motif = sys.argv[3]
        arg = None
    ps = a.scenes()
    print('%d scene(s)' % len(ps))
    for p in ps:
        if not a.tient(p, 0x38):
            print('  pointeur de scene hors bornes (0x%X) -- ce fichier n est '
                  'pas un AetSet' % p)
            continue
        sc = a.scene(p)
        print('  scene "%s"  %d composition(s), %d video(s), %.0f images/s, '
              '%dx%d' % (sc['nom'], sc['n_compo'], sc['n_video'],
                         sc['cadence'], sc['resolution'][0],
                         sc['resolution'][1]))
        if motif is not None:
            cmd_sprite(a, sc, motif)
            continue
        if arg == '--surfaces':
            cmd_surfaces(a, sc)
            continue
        if arg and arg.lower() not in sc['nom'].lower():
            continue
        compos = a.compositions(sc)
        for i, (n, ptr) in enumerate(compos):
            racine = ' (RACINE)' if i == len(compos) - 1 else ''
            if not arg and not racine:
                continue
            print('     composition %d%s : %d calque(s)' % (i, racine, n))
            for k, c in enumerate(a.calques(n, ptr)):
                print('        %3d  %-34s %-12s %.0f-%.0f'
                      % (k, c['nom'], TYPES.get(c['type'], '?%d' % c['type']),
                         c['debut'], c['fin']))
                t = a.transforme(c['video'])
                if t is None:
                    continue
                print('             position (%s, %s)  echelle (%s, %s)  '
                      'rotation %s  opacite %s'
                      % (_val(t['Position.X']), _val(t['Position.Y']),
                         _val(t['Echelle.X']), _val(t['Echelle.Y']),
                         _val(t['Rotation']), _val(t['Opacite'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
