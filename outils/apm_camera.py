#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""LA COULEUR DE FOND DE L'INTERFACE APM3 -- lue dans la camera.

LE CHEMIN QUI N'A PAS MARCHE, et pourquoi il faut le savoir : les panneaux de
`GameSelect.Design` sont des Material dont les textures sont des masques
BLANCS. Prelever la couleur sur les PNG rend #FFFFFF, et lire la table
`m_Colors` des materiaux ne rend que le blanc et le noir des valeurs par
defaut du nuanceur. La couleur de fond n'est dans aucun des deux.

ELLE EST DANS LA CAMERA. `m_BackGroundColor` est ce que Unity peint avant tout
le reste. Il faut donc ouvrir vraiment le fichier de scene : en-tete, table
des types, table des objets, puis les objets de classe 20.

LE FORMAT SerializedFile, pour qui reprendra :

    en-tete GROS-BOUTIEN : tailleMeta, tailleFichier, version, debutDonnees,
                           boutisme, 3 octets reserves
    puis, en petit-boutien :
      version d'Unity (chaine terminee par zero), plateforme,
      presence de l'arbre de types (1 octet),
      N types   : classe (i32), type ampute (u8), index de script (i16),
                  16 octets de hachage si classe 114, puis 16 octets
      M objets  : aligne sur 4, identifiant (i64), debut (u32), taille (u32),
                  index de type (i32)

Un build de sortie n'a PAS d'arbre de types : on ne peut donc pas nommer les
champs, seulement les compter. La camera de Unity 2017.3 commence par :

    m_GameObject   PPtr = 12 octets
    m_Enabled      1 octet, puis alignement sur 4
    m_ClearFlags   4 octets
    m_BackGroundColor   4 flottants        <- ce qu'on cherche

    py -3 tools/apm_camera.py
"""
import os
import struct
import sys

BASE = os.path.join('C:' + os.sep, 'Users', 'frede', 'Desktop',
                    'VF5 FS DECOMP', 'APM_V1.04_internal_0',
                    'Apmv3System_Data')
SCENES = ['level0', 'level1', 'level2', 'level3', 'level4']
CLASSE_CAMERA = 20


class Fichier:
    def __init__(self, chemin):
        self.d = open(chemin, 'rb').read()
        self.objets = []          # (identifiant, debut, taille, classe)
        self._lire()

    def _lire(self):
        d = self.d
        taille_meta, taille, version, debut = struct.unpack('>IIII', d[:16])
        boutisme = d[16]
        if version < 16 or version > 21:
            raise ValueError('version de SerializedFile non geree : %d' % version)
        i = 20
        fin = d.index(b'\0', i)
        self.unity = d[i:fin].decode('ascii', 'replace')
        i = fin + 1
        i += 4                                     # plateforme
        arbre = d[i]; i += 1
        n_types = struct.unpack('<i', d[i:i + 4])[0]; i += 4
        if arbre:
            raise ValueError('ce fichier porte un arbre de types, non gere ici')
        classes = []
        for _ in range(n_types):
            classe = struct.unpack('<i', d[i:i + 4])[0]; i += 4
            i += 1                                 # type ampute
            i += 2                                 # index de script
            if classe == 114:
                i += 16                            # hachage du script
            i += 16                                # hachage du type
            classes.append(classe)
        n_obj = struct.unpack('<i', d[i:i + 4])[0]; i += 4
        for _ in range(n_obj):
            i += (-i) % 4
            ident, deb, tail, ityp = struct.unpack('<qIIi', d[i:i + 20])
            i += 20
            classe = classes[ityp] if 0 <= ityp < len(classes) else -1
            self.objets.append((ident, debut + deb, tail, classe))

    def corps(self, debut, taille):
        return self.d[debut:debut + taille]


def hexa(r, v, b):
    q = lambda x: max(0, min(255, int(round(x * 255.0))))
    return '#%02X%02X%02X' % (q(r), q(v), q(b))


def main():
    trouve = 0
    for nom in SCENES:
        p = os.path.join(BASE, nom)
        if not os.path.exists(p):
            continue
        try:
            f = Fichier(p)
        except ValueError as e:
            print('%-8s : %s' % (nom, e))
            continue
        cams = [o for o in f.objets if o[3] == CLASSE_CAMERA]
        print('%-8s  Unity %-12s %4d objets, %d camera(s)'
              % (nom, f.unity, len(f.objets), len(cams)))
        for ident, debut, taille, _ in cams:
            b = f.corps(debut, taille)
            if len(b) < 36:
                print('        camera trop courte (%d octets)' % len(b))
                continue
            drapeaux = struct.unpack('<I', b[16:20])[0]
            r, v, bl, a = struct.unpack('<ffff', b[20:36])
            if not all(-0.01 <= x <= 8.0 for x in (r, v, bl, a)):
                print('        valeurs hors bornes, disposition differente')
                continue
            trouve += 1
            mode = {1: 'ciel', 2: 'couleur unie', 3: 'profondeur seule',
                    4: 'rien'}.get(drapeaux, str(drapeaux))
            print('        FOND %s  alpha %.3f   effacement : %s'
                  % (hexa(r, v, bl), a, mode))
            print('                    (%.4f %.4f %.4f)' % (r, v, bl))
    print()
    if not trouve:
        print('Aucune camera lisible.')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
