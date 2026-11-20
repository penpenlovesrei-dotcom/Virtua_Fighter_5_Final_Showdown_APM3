#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""LES JEUX DE LA BORNE -- controle et conversion des jaquettes et videos.

Un dossier par jeu dans `borne\jeux\`. Cet outil dit ce qui va, ce qui manque,
et ce qui n'est pas au bon format ; avec --convertir, il remet au format.

LES FORMATS, ET POURQUOI

  jaquette.png   CARREE, 512x512 conseille, 384 minimum.
                 Pourquoi carree : le code de l'APM3 pose ses icones sur une
                 grille carree de 256 px (`iconSize = 256`). Pourquoi 384 au
                 minimum : l'icone selectionnee est agrandie de moitie
                 (`selectedIconRatio = 1.5`), donc 256 x 1,5 = 384 px a
                 l'ecran. En dessous, ca pixellise au centre -- la ou l'oeil
                 regarde. Le PNG garde la transparence ; le JPG est accepte.

  demo.mp4       H.264 (avc1) + AAC, 16:9, 1280x720 suffit.
                 Pourquoi H.264 : Media Foundation, le lecteur video de
                 Windows que le portage C++ utilise, le lit sans rien
                 installer. Le HEVC/H.265 demande un codec PAYANT sur
                 Windows 11 : il est refuse ici expres.

  jeu.json       facultatif. {"titre": "...", "exe": "C:\\...\\jeu.exe",
                              "args": [], "editeur": "...", "annee": 1993}
                 Sans lui, le nom du dossier sert de titre et le premier
                 executable trouve dans le dossier est lance.

USAGE

  py -3 tools/jeux.py                 controle tout, ne touche a rien
  py -3 tools/jeux.py --convertir     remet au format ce qui ne l'est pas
  py -3 tools/jeux.py --dossier <d>   un autre dossier que borne\jeux
"""
import json
import os
import struct
import subprocess
import sys

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JEUX = os.path.join(ICI, 'borne', 'jeux')

JAQUETTE_IDEAL = 512
JAQUETTE_MINI = 384             # 256 * selectedIconRatio (1.5)
VIDEO_CODECS_OK = ('h264',)
VIDEO_LARGEUR_MAX = 1920

IMAGES = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
VIDEOS = ('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.webm', '.m4v', '.mpg')
EXES = ('.exe', '.cmd', '.bat', '.lnk')

# Les outils de MSYS2, deja installes sur cette machine.
MINGW = r'C:\msys64\mingw64\bin'


def outil(nom):
    p = os.path.join(MINGW, nom + '.exe')
    return p if os.path.exists(p) else None


def taille_image(chemin):
    """Rend (largeur, hauteur) en lisant l'en-tete, sans bibliotheque."""
    try:
        f = open(chemin, 'rb')
    except OSError:
        return None
    with f:
        d = f.read(32)
        if d[:8] == b'\x89PNG\r\n\x1a\n' and d[12:16] == b'IHDR':
            return struct.unpack('>II', d[16:24])
        if d[:2] == b'\xff\xd8':                       # JPEG : on parcourt
            f.seek(2)
            while True:
                b = f.read(2)
                if len(b) < 2 or b[0] != 0xFF:
                    return None
                marqueur = b[1]
                if 0xC0 <= marqueur <= 0xCF and marqueur not in (0xC4, 0xC8, 0xCC):
                    f.read(3)
                    h, w = struct.unpack('>HH', f.read(4))
                    return (w, h)
                lg = struct.unpack('>H', f.read(2))[0]
                f.seek(lg - 2, 1)
    return None


def sonde_video(chemin):
    """Rend (codec, largeur, hauteur) via ffprobe, ou None."""
    ff = outil('ffprobe')
    if not ff:
        return None
    try:
        s = subprocess.run(
            [ff, '-v', 'error', '-select_streams', 'v:0', '-show_entries',
             'stream=codec_name,width,height', '-of', 'json', chemin],
            capture_output=True, timeout=30)
        flux = json.loads(s.stdout.decode('utf-8', 'replace'))['streams']
        if not flux:
            return None
        f = flux[0]
        return (f.get('codec_name', '?'), f.get('width', 0), f.get('height', 0))
    except (OSError, ValueError, KeyError, IndexError,
            subprocess.SubprocessError):
        return None


def premier(dossier, extensions, prefixe=None):
    for n in sorted(os.listdir(dossier)):
        b, e = os.path.splitext(n)
        if e.lower() in extensions and (prefixe is None or b.lower() == prefixe):
            return os.path.join(dossier, n)
    return None


def convertir_jaquette(src, dest):
    ff = outil('ffmpeg')
    if not ff:
        return False, 'ffmpeg introuvable dans %s' % MINGW
    # On tient dans un carre de 512 sans deformer, et on centre sur du noir.
    filtre = ('scale=%d:%d:force_original_aspect_ratio=decrease,'
              'pad=%d:%d:(ow-iw)/2:(oh-ih)/2:color=black'
              % (JAQUETTE_IDEAL, JAQUETTE_IDEAL, JAQUETTE_IDEAL, JAQUETTE_IDEAL))
    r = subprocess.run([ff, '-y', '-v', 'error', '-i', src, '-vf', filtre,
                        dest], capture_output=True)
    if r.returncode:
        return False, r.stderr.decode('utf-8', 'replace').strip()[:200]
    return True, os.path.basename(dest)


def convertir_video(src, dest):
    ff = outil('ffmpeg')
    if not ff:
        return False, 'ffmpeg introuvable dans %s' % MINGW
    r = subprocess.run(
        [ff, '-y', '-v', 'error', '-i', src,
         '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
         '-vf', 'scale=1280:-2', '-r', '30', '-crf', '20',
         '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', dest],
        capture_output=True)
    if r.returncode:
        return False, r.stderr.decode('utf-8', 'replace').strip()[:200]
    return True, os.path.basename(dest)


def controler(dossier, convertir):
    """Controle un dossier de jeu. Rend (nb_ok, nb_avertissements)."""
    nom = os.path.basename(dossier)
    lignes = []
    avertis = 0

    fiche = {}
    p = os.path.join(dossier, 'jeu.json')
    if os.path.exists(p):
        try:
            fiche = json.load(open(p, encoding='utf-8'))
            lignes.append('    jeu.json     %s' % (fiche.get('titre') or nom))
        except ValueError as e:
            lignes.append('    jeu.json     ILLISIBLE : %s' % e)
            avertis += 1

    # ---- la jaquette -------------------------------------------------------
    jq = premier(dossier, IMAGES, 'jaquette') or premier(dossier, IMAGES)
    if not jq:
        lignes.append('    jaquette     MANQUANTE')
        avertis += 1
    else:
        t = taille_image(jq)
        b = os.path.basename(jq)
        if not t:
            lignes.append('    jaquette     %s  (taille illisible)' % b)
            avertis += 1
        else:
            w, h = t
            carree = (w == h)
            assez = min(w, h) >= JAQUETTE_MINI
            bien_nommee = os.path.splitext(b)[0].lower() == 'jaquette'
            if carree and assez and bien_nommee:
                lignes.append('    jaquette     %s  %dx%d  OK' % (b, w, h))
            else:
                pourquoi = []
                if not carree:
                    pourquoi.append('pas carree')
                if not assez:
                    pourquoi.append('moins de %d px' % JAQUETTE_MINI)
                if not bien_nommee:
                    pourquoi.append('a renommer jaquette.png')
                lignes.append('    jaquette     %s  %dx%d  -- %s'
                              % (b, w, h, ', '.join(pourquoi)))
                avertis += 1
                if convertir:
                    dest = os.path.join(dossier, 'jaquette.png')
                    src = jq
                    if os.path.abspath(src) == os.path.abspath(dest):
                        src = os.path.join(dossier, '_source_jaquette.png')
                        os.replace(dest, src)
                    ok, quoi = convertir_jaquette(src, dest)
                    lignes.append('       -> %s %s'
                                  % ('CONVERTIE en' if ok else 'ECHEC :', quoi))
                    if ok:
                        avertis -= 1        # c'est repare, ca ne compte plus

    # ---- la video ----------------------------------------------------------
    vd = premier(dossier, VIDEOS, 'demo') or premier(dossier, VIDEOS)
    if not vd:
        lignes.append('    demo         absente  (facultative)')
    else:
        b = os.path.basename(vd)
        s = sonde_video(vd)
        bien_nommee = os.path.splitext(b)[0].lower() == 'demo'
        est_mp4 = b.lower().endswith('.mp4')
        if not s:
            lignes.append('    demo         %s  (illisible par ffprobe)' % b)
            avertis += 1
        else:
            codec, w, h = s
            bon = (codec in VIDEO_CODECS_OK and est_mp4 and bien_nommee
                   and w <= VIDEO_LARGEUR_MAX)
            if bon:
                lignes.append('    demo         %s  %s %dx%d  OK'
                              % (b, codec, w, h))
            else:
                pourquoi = []
                if codec not in VIDEO_CODECS_OK:
                    pourquoi.append('%s -- il faut du h264' % codec)
                if not est_mp4:
                    pourquoi.append('pas un .mp4')
                if w > VIDEO_LARGEUR_MAX:
                    pourquoi.append('plus large que %d' % VIDEO_LARGEUR_MAX)
                if not bien_nommee:
                    pourquoi.append('a renommer demo.mp4')
                lignes.append('    demo         %s  %s %dx%d  -- %s'
                              % (b, codec, w, h, ', '.join(pourquoi)))
                avertis += 1
                if convertir:
                    dest = os.path.join(dossier, 'demo.mp4')
                    src = vd
                    if os.path.abspath(src) == os.path.abspath(dest):
                        src = os.path.join(dossier, '_source_demo.mp4')
                        os.replace(dest, src)
                    ok, quoi = convertir_video(src, dest)
                    lignes.append('       -> %s %s'
                                  % ('CONVERTIE en' if ok else 'ECHEC :', quoi))
                    if ok:
                        avertis -= 1        # c'est repare, ca ne compte plus

    # ---- l'executable ------------------------------------------------------
    exe = fiche.get('exe') or premier(dossier, EXES)
    if not exe:
        # Ce n'est PAS un defaut. La borne SEGA a le meme mode : bootApplication
        # a faux joue l'animation de lancement puis revient sans rien demarrer.
        lignes.append('    executable   aucun  -- mode vitrine')
    elif not os.path.exists(exe):
        lignes.append('    executable   INTROUVABLE : %s' % exe)
        avertis += 1
    else:
        lignes.append('    executable   %s' % os.path.normpath(exe))

    print('  %s' % nom)
    for ligne in lignes:
        print(ligne)
    print()
    return avertis


def main():
    argv = sys.argv[1:]
    convertir = '--convertir' in argv
    dossier = JEUX
    if '--dossier' in argv:
        dossier = argv[argv.index('--dossier') + 1]

    print('=' * 70)
    print('LES JEUX DE LA BORNE   %s' % dossier)
    print('=' * 70)
    if convertir:
        print('MODE CONVERSION : les fichiers hors format seront remis au')
        print('format. L original est garde sous _source_*.')
    else:
        print('Controle seul. Rien n est modifie.')
    print()

    if not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)
        print('  Dossier cree. Il est vide.')
        print()

    noms = [n for n in sorted(os.listdir(dossier))
            if os.path.isdir(os.path.join(dossier, n))]
    if not noms:
        print('  Aucun jeu. Creez un dossier par jeu, par exemple :')
        print()
        print('     borne\\jeux\\Virtua Fighter 5 FS\\jaquette.png')
        print('     borne\\jeux\\Virtua Fighter 5 FS\\demo.mp4')
        print('     borne\\jeux\\Virtua Fighter 5 FS\\jeu.json')
        print()
        print('  Detail : borne\\LISEZ-MOI.txt')
        return 0

    total = 0
    for n in noms:
        total += controler(os.path.join(dossier, n), convertir)

    print('-' * 70)
    if total:
        print('  %d jeu(x), %d point(s) a corriger.' % (len(noms), total))
        if not convertir:
            print('  Pour que je remette les images et videos au format,')
            print('  double-cliquez sur   tools\\jeux_convertir.cmd')
    else:
        print('  %d jeu(x), tout est au format.' % len(noms))
    print('-' * 70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
