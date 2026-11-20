#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""`auth_3d_db.bin` : la base des jeux d'animation, et elle est en CLAIR.

C'EST DU TEXTE. Mesure du 2026-09-09 : 223 565 octets, 8 172 lignes, **zero
octet non imprimable**. Declarer l'animation d'un decor neuf n'est donc pas un
format a retro-concevoir, c'est une edition de texte -- a condition de respecter
la seule regle qui compte, ci-dessous.

    #A3DA__________
    # date time was eliminated.
    category.0.value=ADV
    ...
    category.length=92
    uid.0.category=ADV
    uid.0.size=2960
    uid.0.value=A A010A010_MON_ADV
    ...
    uid.length=3469

LA REGLE QUI COMMANDE TOUT : LES CLES SONT TRIEES COMME DES CHAINES.

`category.10.value` vient AVANT `category.2.value`, et `category.length` apres
`category.9.value` parce que « l » passe apres les chiffres. Ce n'est pas une
curiosite : si on reecrit le fichier dans un autre ordre, on ne sait plus s'il
est encore lisible par le moteur, et l'aller-retour ne prouve plus rien.
`--essai` verifie donc que lire puis reecrire rend le fichier **identique a
l'octet pres**. Tant que cet essai passe, on sait qu'on a compris le format.

CE QUE LE JEU EN FAIT

  . le fichier est charge depuis `rom/auth_3d/auth_3d_db.bin` (chaine en
    0x180348C30) ; il est dans le `.par` sous le nom plat `auth_3d_db.bin`,
    comprime ;
  . une CATEGORIE est le nom d'une archive : `STGDJO` -> `auth_3d/STGDJO.farc`
    (le moteur compose par `auth_3d/%s.farc`, 0x1803F9438) ;
  . un UID nomme un `.a3da` de cette archive. `uid.703.value=A
    S010A010_DJO_STG_01` : le `A ` de tete est un marqueur de type, pas une
    partie du nom ;
  . `size` est une taille par enregistrement. 1 166 uids sur 3 469 n'ont NI
    categorie NI taille : seulement une valeur.

    py -3 tools/a3d_db.py --essai
    py -3 tools/a3d_db.py --lister                    les 92 categories
    py -3 tools/a3d_db.py --montrer STGDJO            ses uids
    py -3 tools/a3d_db.py --ajouter STGTRS --depuis STGDJO --sortie <fichier>

`--ajouter` recopie les noms de `.a3da` du modele **VERBATIM**, et c'est le bon
defaut : `importer_decor.py --vers` renomme les deux entrees de l'objset dans
l'en-tete du `FArC`, **pas** les `.a3da` de l'archive d'animation. Les noms
doivent donc rester ceux que l'archive porte reellement. `--renommer` substitue
le code -- a n'utiliser que si l'archive a ete reecrite aussi.
"""
import io
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
DEFAUT = os.path.join(RACINE, 'extracted', 'auth_3d_db.bin')

MAGIE = '#A3DA'


class Base:
    """Le fichier, en memoire : des lignes d'en-tete et un dictionnaire.

    On ne garde PAS les lignes telles quelles : on garde les paires, et on les
    reecrit triees. C'est ce qui permet d'ajouter une entree au bon endroit
    sans y penser -- et l'aller-retour prouve que le tri est le bon.
    """

    def __init__(self, texte):
        self.entete = []
        self.paires = {}
        self.fin_de_ligne = '\r\n' if '\r\n' in texte else '\n'
        for ligne in texte.split(self.fin_de_ligne):
            if not ligne:
                continue
            if ligne.startswith('#'):
                self.entete.append(ligne)
                continue
            if '=' not in ligne:
                raise ValueError('ligne sans « = » : %r' % ligne[:60])
            cle, valeur = ligne.split('=', 1)
            if cle in self.paires:
                raise ValueError('cle en double : %r' % cle)
            self.paires[cle] = valeur

    def texte(self):
        lignes = list(self.entete)
        lignes += ['%s=%s' % (k, self.paires[k]) for k in sorted(self.paires)]
        return self.fin_de_ligne.join(lignes) + self.fin_de_ligne

    # --- lectures -----------------------------------------------------------
    def categories(self):
        n = int(self.paires['category.length'])
        return [self.paires['category.%d.value' % i] for i in range(n)]

    def uids(self):
        """{numero: {'category':…, 'size':…, 'value':…}} -- champs facultatifs."""
        out = {}
        for cle, val in self.paires.items():
            if not cle.startswith('uid.'):
                continue
            p = cle.split('.')
            if len(p) != 3:
                continue                      # uid.length
            out.setdefault(int(p[1]), {})[p[2]] = val
        return out

    def uids_de(self, categorie):
        return {k: v for k, v in self.uids().items()
                if v.get('category') == categorie}

    # --- ecriture -----------------------------------------------------------
    def ajouter_categorie(self, nom):
        """Ajoute une categorie et RENUMEROTE, l'ordre etant alphabetique.

        Les 92 categories d'origine sont classees par nom. Inserer sans
        renumeroter donnerait une table qui n'est plus triee -- et rien ne dit
        que le moteur ne fasse pas une dichotomie dessus. On ne prend pas ce
        risque pour economiser vingt lignes.
        """
        cats = self.categories()
        if nom in cats:
            raise ValueError('la categorie %r existe deja' % nom)
        cats.append(nom)
        cats.sort()
        for cle in [k for k in self.paires if k.startswith('category.')]:
            del self.paires[cle]
        for i, c in enumerate(cats):
            self.paires['category.%d.value' % i] = c
        self.paires['category.length'] = str(len(cats))
        return cats.index(nom)

    def ajouter_uid(self, categorie, valeur, taille):
        """Ajoute un uid A LA FIN. Rend son numero.

        Les uids ne sont PAS tries par categorie dans le fichier d'origine
        (ceux de STGDJO sont 703, 704, 705, au milieu des autres) : leur
        numero est un identifiant, pas un rang. On peut donc ajouter a la fin
        sans rien renumeroter, et c'est bien plus sur.
        """
        n = int(self.paires['uid.length'])
        self.paires['uid.%d.category' % n] = categorie
        self.paires['uid.%d.size' % n] = str(taille)
        self.paires['uid.%d.value' % n] = valeur
        self.paires['uid.length'] = str(n + 1)
        return n


def charger(chemin=DEFAUT):
    brut = io.open(chemin, 'rb').read()
    sales = [b for b in brut if b < 9 or (13 < b < 32) or b > 126]
    if sales:
        raise ValueError('%d octets non imprimables : ce n est pas le fichier '
                         'texte attendu' % len(sales))
    texte = brut.decode('ascii')
    if not texte.startswith(MAGIE):
        raise ValueError('en-tete %r au lieu de %r' % (texte[:5], MAGIE))
    return Base(texte)


def essai(chemin=DEFAUT):
    """L'aller-retour. Tant qu'il passe, on a compris le format."""
    brut = io.open(chemin, 'rb').read()
    b = charger(chemin)
    rendu = b.texte().encode('ascii')
    print('fichier   : %s' % chemin)
    print('            %d octets, %d lignes d en-tete, %d paires'
          % (len(brut), len(b.entete), len(b.paires)))
    print('            %d categories, %s uids'
          % (len(b.categories()), b.paires['uid.length']))
    print('reecrit   : %d octets' % len(rendu))
    if rendu == brut:
        print()
        print('ALLER-RETOUR IDENTIQUE A L OCTET PRES.')
        print('Les cles sont bien triees comme des CHAINES : `category.10`')
        print('avant `category.2`, et `category.length` en dernier.')
        return 0
    k = next((i for i in range(min(len(rendu), len(brut)))
              if rendu[i] != brut[i]), min(len(rendu), len(brut)))
    print()
    print('ECART au premier octet 0x%X :' % k)
    print('   attendu %r' % brut[max(0, k - 40):k + 40])
    print('   obtenu  %r' % rendu[max(0, k - 40):k + 40])
    return 1


def main():
    argv = sys.argv[1:]
    chemin = DEFAUT
    if '--fichier' in argv:
        i = argv.index('--fichier')
        chemin = argv[i + 1]
        del argv[i:i + 2]

    if '--essai' in argv or not argv:
        return essai(chemin)

    b = charger(chemin)

    if '--lister' in argv:
        cats = b.categories()
        u = b.uids()
        print('%d categories, %s uids (%d avec une categorie)'
              % (len(cats), b.paires['uid.length'],
                 sum(1 for v in u.values() if 'category' in v)))
        for i, c in enumerate(cats):
            n = sum(1 for v in u.values() if v.get('category') == c)
            print('   %2d  %-14s %4d uid(s)' % (i, c, n))
        return 0

    if '--montrer' in argv:
        nom = argv[argv.index('--montrer') + 1]
        d = b.uids_de(nom)
        if not d:
            print('aucune categorie « %s ». Les %d connues : %s'
                  % (nom, len(b.categories()), ' '.join(b.categories())))
            return 1
        print('%s : %d uid(s)' % (nom, len(d)))
        for k in sorted(d):
            print('   uid.%-5d size %-6s %s'
                  % (k, d[k].get('size', '-'), d[k].get('value', '-')))
        return 0

    if '--ajouter' in argv:
        nom = argv[argv.index('--ajouter') + 1]
        depuis = argv[argv.index('--depuis') + 1] if '--depuis' in argv else None
        if not depuis:
            print('--ajouter demande --depuis <categorie modele> : les noms de '
                  '`.a3da` en sont recopies, faute de savoir en inventer.')
            return 1
        modele = b.uids_de(depuis)
        if not modele:
            print('categorie modele « %s » inconnue' % depuis)
            return 1
        renommer = '--renommer' in argv
        i = b.ajouter_categorie(nom)
        ajoutes = []
        for k in sorted(modele):
            v = modele[k]
            neuf = v['value']
            if renommer:
                neuf = neuf.replace(depuis, nom).replace(depuis.lower(),
                                                         nom.lower())
            ajoutes.append((b.ajouter_uid(nom, neuf, v.get('size', '0')), neuf))
        print('categorie « %s » ajoutee au rang %d ; %d uid(s) :'
              % (nom, i, len(ajoutes)))
        for num, val in ajoutes:
            print('   uid.%-5d %s' % (num, val))
        print()
        if renommer:
            print('--renommer : le code a ete substitue dans les noms de')
            print('`.a3da`. Ils ne vaudront que si l archive a ete reecrite en')
            print('consequence -- ce que `importer_decor.py --vers` ne fait')
            print('PAS : il ne renomme que les deux entrees de l objset.')
        else:
            print('Les noms de `.a3da` sont recopies VERBATIM du modele : c est')
            print('ce que porte reellement une archive importee puis renommee.')
            print('Un nom qui ne correspond a rien dans l archive fait charger')
            print('le decor SANS son animation, et sans un message.')
        if '--sortie' in argv:
            s = argv[argv.index('--sortie') + 1]
            io.open(s, 'wb').write(b.texte().encode('ascii'))
            print()
            print('ecrit : %s (%d octets)' % (s, os.path.getsize(s)))
        else:
            print()
            print('(rien n a ete ecrit : ajoutez --sortie <fichier>)')
        return 0

    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
