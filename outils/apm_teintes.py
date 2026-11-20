#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""LES TEINTES DES PANNEAUX DE L'INTERFACE APM3.

LE PROBLEME. Les bandeaux, le fond et les boutons de l'ecran sont des `Image`
de l'interface Unity : une texture BLANCHE multipliee par une couleur, gardee
dans le composant. Les PNG extraits ne rendent donc que du #FFFFFF, et les
Material partages ne portent que le blanc et le noir par defaut du nuanceur.
La couleur est dans les COMPOSANTS de la scene.

CE QU'ON PEUT ET CE QU'ON NE PEUT PAS. Un build de sortie n'a pas d'arbre de
types : impossible de nommer les champs. Mais la disposition d'un
`UnityEngine.UI.Image` de 2017.3 est connue et fixe :

    m_GameObject     PPtr                    12 octets
    m_Enabled        1 octet + alignement     4
    m_Script         PPtr                    12
    m_Name           chaine (longueur + octets + alignement)
    m_Material       PPtr                    12
    m_Color          quatre flottants        16      <- ce qu'on cherche
    m_RaycastTarget  1 octet + alignement

On lit donc TOUS les MonoBehaviour (classe 114) a cette disposition. Les
composants qui ne sont pas des Image rendent n'importe quoi -- on ne garde
que ce qui ressemble a une couleur, et on compte les occurrences. Une teinte
d'habillage revient forcement plusieurs fois ; le bruit, non.

C'EST UNE MESURE SOUS PREMISSE, et la premisse est ecrite ci-dessus : si la
disposition d'Image differait, les chiffres seraient faux. Le controle, c'est
que le blanc pur domine -- ce qui est attendu d'une interface dont la plupart
des images ne sont pas teintees.

    py -3 tools/apm_teintes.py
"""
import os
import struct
import sys

BASE = os.path.join('C:' + os.sep, 'Users', 'frede', 'Desktop',
                    'VF5 FS DECOMP', 'APM_V1.04_internal_0',
                    'Apmv3System_Data')
SCENES = ['level1', 'level2']
CLASSE_COMPORTEMENT = 114


class Fichier:
    """Le meme lecteur que tools/apm_camera.py -- voir la-bas pour le format."""

    def __init__(self, chemin):
        self.d = open(chemin, 'rb').read()
        self.objets = []
        self._lire()

    def _lire(self):
        d = self.d
        _, _, version, debut = struct.unpack('>IIII', d[:16])
        if not (16 <= version <= 21):
            raise ValueError('version %d non geree' % version)
        i = 20
        fin = d.index(b'\0', i)
        self.unity = d[i:fin].decode('ascii', 'replace')
        i = fin + 1 + 4
        arbre = d[i]; i += 1
        n_types = struct.unpack('<i', d[i:i + 4])[0]; i += 4
        if arbre:
            raise ValueError('arbre de types present, non gere')
        classes = []
        for _ in range(n_types):
            classe = struct.unpack('<i', d[i:i + 4])[0]; i += 4
            i += 3
            if classe == 114:
                i += 16
            i += 16
            classes.append(classe)
        n_obj = struct.unpack('<i', d[i:i + 4])[0]; i += 4
        for _ in range(n_obj):
            i += (-i) % 4
            _, deb, tail, ityp = struct.unpack('<qIIi', d[i:i + 20])
            i += 20
            classe = classes[ityp] if 0 <= ityp < len(classes) else -1
            self.objets.append((debut + deb, tail, classe))


def teinte_de(b):
    """Rend (r, v, bl, a) si le bloc a la forme d'un Image, sinon None."""
    if len(b) < 60:
        return None
    i = 12                                   # m_GameObject
    i += 4                                   # m_Enabled + alignement
    i += 12                                  # m_Script
    if i + 4 > len(b):
        return None
    lg = struct.unpack('<i', b[i:i + 4])[0]  # m_Name
    if lg < 0 or lg > 200 or i + 4 + lg > len(b):
        return None
    i += 4 + lg
    i += (-i) % 4
    i += 12                                  # m_Material
    if i + 16 > len(b):
        return None
    r, v, bl, a = struct.unpack('<ffff', b[i:i + 16])
    for x in (r, v, bl, a):
        if not (0.0 <= x <= 1.0):
            return None
    return (r, v, bl, a)


def hexa(r, v, b):
    q = lambda x: max(0, min(255, int(round(x * 255.0))))
    return '#%02X%02X%02X' % (q(r), q(v), q(b))


def main():
    compte = {}
    lus = 0
    for nom in SCENES:
        p = os.path.join(BASE, nom)
        if not os.path.exists(p):
            continue
        try:
            f = Fichier(p)
        except ValueError as e:
            print('%s : %s' % (nom, e))
            continue
        n = 0
        for debut, taille, classe in f.objets:
            if classe != CLASSE_COMPORTEMENT:
                continue
            t = teinte_de(f.d[debut:debut + taille])
            if not t:
                continue
            n += 1
            cle = (hexa(t[0], t[1], t[2]), round(t[3], 3))
            compte[cle] = compte.get(cle, 0) + 1
        lus += n
        print('%-8s  Unity %-12s %d composant(s) de forme Image'
              % (nom, f.unity, n))

    if not lus:
        print('Rien de lisible.')
        return 1
    print()
    print('-' * 60)
    print('  %d teinte(s) distincte(s), par frequence :' % len(compte))
    for (h, a), n in sorted(compte.items(), key=lambda kv: -kv[1]):
        marque = '   <-- blanc pur, image non teintee' if h == '#FFFFFF' else ''
        print('     %s  alpha %-6s  %4d fois%s' % (h, a, n, marque))
    print('-' * 60)
    return 0


if __name__ == '__main__':
    sys.exit(main())
