#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""NE REPATCHER LE MOTEUR QUE SI QUELQUE CHOSE A CHANGE.

MESURE DU 2026-10-15, tools/chrono_lanceur.py :

       1.78 s   apm.dll (gcc)
       0.96 s   decors 5r+vf5 (bases)
       0.11 s   empreintes de shaders
       0.19 s   style de boutons
      21.50 s   patch du moteur (60 chantiers)
    ------------------------------------------
      24.55 s   avant meme que vfes.exe demarre

**Quatre-vingt-huit pour cent du temps d avant-lancement va au patch**, et il
refait exactement le meme travail a chaque double-clic. Le profil BOOT, lui,
montre que le jeu tourne ensuite a 60 images par seconde sans faiblir : il n y
a rien a gagner de ce cote.

Or le patch est DETERMINISTE : memes entrees, meme DLL. On garde donc une
empreinte, et on saute le patch quand rien n a bouge.

CE QU ON COMPARE -- et le dernier point est celui qui empeche de servir une
DLL perimee :

    1. le `.origine`                taille et date
    2. `patch_moteur.py`            taille et date
    3. le socle `.pyc`              taille et date
    4. la ligne d options entiere   mot pour mot
    5. **le sha256 de la DLL PATCHEE elle-meme**

Si la DLL a ete touchee par quoi que ce soit -- une autre option, un autre
lanceur, une main -- son empreinte ne correspond plus et on repatche. Le saut
n est donc jamais un pari : il est verifie sur le resultat, pas sur l intention.

    py -3 tools/patch_si_besoin.py <les memes options que patch_moteur.py>
    py -3 tools/patch_si_besoin.py --toujours <options>    saute le cache
"""
import hashlib
import json
import os
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTILS = os.path.join(RACINE, 'tools')
RAM = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'ram')
EMPREINTE = os.path.join(RAM, 'patch_empreinte.json')


def _dll():
    """Le chemin de la DLL du moteur, demande au patcheur lui-meme."""
    sys.path.insert(0, OUTILS)
    import patch_moteur                                   # noqa: E402
    return os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                        patch_moteur._s.DLL)


def _marque(chemin):
    """(taille, date) d un fichier, ou None s il manque."""
    try:
        st = os.stat(chemin)
    except OSError:
        return None
    return [st.st_size, int(st.st_mtime)]


def _sha(chemin):
    h = hashlib.sha256()
    try:
        with open(chemin, 'rb') as fp:
            for bloc in iter(lambda: fp.read(1 << 20), b''):
                h.update(bloc)
    except IOError:
        return None
    return h.hexdigest()


def _socle_pyc():
    for n in sorted(os.listdir(OUTILS)):
        if n.startswith('socle_') and n.endswith('.pyc'):
            return os.path.join(OUTILS, n)
    return None


def _etat(dll, options):
    return {
        'origine': _marque(dll + '.origine'),
        'patcheur': _marque(os.path.join(OUTILS, 'patch_moteur.py')),
        'socle': _marque(_socle_pyc() or ''),
        'options': options,
        'dll': _sha(dll),
    }


def main(argv):
    toujours = '--toujours' in argv
    options = [a for a in argv if a != '--toujours']
    dll = _dll()
    voulu = _etat(dll, options)

    if not toujours and voulu['dll'] is not None:
        try:
            with open(EMPREINTE) as fp:
                connu = json.load(fp)
        except (IOError, ValueError):
            connu = None
        if connu == voulu:
            # SUR LA SORTIE D ERREUR, et c est voulu : item_porte.cmd redirige
            # la sortie normale vers nul. Un saut silencieux laisserait croire
            # que le patch a tourne.
            sys.stderr.write('  Patch du moteur : rien n a change, on garde '
                             'la DLL en place (21 s economisees).\n')
            return 0

    r = subprocess.call([sys.executable,
                         os.path.join(OUTILS, 'patch_moteur.py')] + options)
    if r:
        # UN ECHEC N ECRIT PAS D EMPREINTE, et efface celle d avant : sinon le
        # tour suivant sauterait un patch qui n a jamais abouti.
        try:
            os.remove(EMPREINTE)
        except OSError:
            pass
        return r

    # L EMPREINTE SE PREND SUR LE RESULTAT, pas sur l intention.
    fait = _etat(dll, options)
    if not os.path.isdir(RAM):
        os.makedirs(RAM)
    tmp = EMPREINTE + '.neuf'
    with open(tmp, 'w') as fp:
        json.dump(fait, fp, indent=1, sort_keys=True)
    os.replace(tmp, EMPREINTE)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
