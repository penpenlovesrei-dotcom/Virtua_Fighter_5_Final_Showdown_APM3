#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES FILMS DE VF.TV EN `.mpg` REGARDABLES, AVEC LE SON.

CE QUE FAISAIT `films_a_regarder.py`, ET POURQUOI CA NE SUFFISAIT PLUS. Un
`.sfd` Sofdec1 EST un flux de programme MPEG-1 : poser a cote un LIEN DUR en
`.mpg` donne l image sans copier un octet. Mais **pas le son** -- CRI range son
ADX dans le flux 0xC0, declare « audio MPEG », et aucun lecteur ne le decode a
cette place. Onze films muets, c est tout ce qu on avait.

CE QU ON FAIT ICI, et c est mesure, pas suppose :

    0xE0  video MPEG-1    commence par 00 00 01 B3 (en-tete de sequence)
    0xC0  « audio MPEG »  commence par 80 00 ..... : c est un EN-TETE ADX
                          (0x8000, decalage du copyright, type 3, bloc 18,
                          4 bits, 2 voies, 48 000 Hz)

On concatene chaque flux dans son coin -- la video donne un `.m1v` lisible tel
quel, l audio un `.adx` complet, en-tete compris -- puis on les remballe en un
vrai MPEG-1 System avec le son en MP2. Aucun reencodage de l image : `-c:v
copy`. Seul le son est converti, parce qu aucun conteneur MPEG ne sait porter
de l ADX.

L OUTIL QU IL FAUT. Le ffmpeg livre dans `tools/FFmpeg-based-ADX-converter`
est TAILLE POUR L ADX ET RIEN D AUTRE : son `configuration` desactive les
muxers sauf adx/wav/flac, et tous les encodeurs sauf trois. Il decode l ADX
mais ne sait pas fabriquer un `.mpg`. On cherche donc un ffmpeg complet sur la
machine, et on exige de lui DEUX choses avant de s en servir : le decodeur
`adpcm_adx` et le muxer `mpeg`. S il manque l un des deux, on le dit et on ne
produit rien plutot que de produire un film muet de plus.

LE PIEGE A EVITER ABSOLUMENT. Les `.mpg` deja presents dans `MOVIES/A_REGARDER`
sont des **liens durs** vers les `.sfd` : le meme fichier sous deux noms.
Ecrire « par-dessus » le `.mpg` ecrirait DANS LE `.sfd`. On ecrit donc toujours
a cote, puis on REMPLACE le nom -- `os.replace` defait le lien sans toucher a
la source.

    py -3 tools/films_mpg.py              les onze films de /tv/ de VF5 R
    py -3 tools/films_mpg.py --tous       les treize, opening et ending compris
    py -3 tools/films_mpg.py --refaire    refait meme ce qui est deja converti
"""
import os
import shutil
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
sys.path.insert(0, ICI)

import sfd as mod_sfd                                          # noqa: E402

SOURCES = (os.path.join(RACINE, 'extracted', 'VF5R_movies'),)
SORTIE = os.path.join(RACINE, 'MOVIES', 'A_REGARDER')
TRAVAIL = os.path.join(RACINE, 'MOVIES', '_travail')

# Les onze films de `/tv/` -- le contenu VF.TV de la borne R. `vf5adv` et
# `vf5end` n y sont pas : ils se nomment seuls et sont deja dans le Movie
# Theater. `--tous` les prend quand meme.
TV = ('vd_RikoReis_00', 'vd_VF5RReis_00', 'vd_RikoDesi_00', 'vd_RikoVFNT_00',
      'vd_RikoTmnl_00', 'vd_RikoVSmv_00', 'cm_VER_R_00', 'bngf_hp_01',
      'ec_00000000_00', 'ec_00000000_01', 'ec_00000000_02')

# Ou chercher un ffmpeg COMPLET. Le premier qui sait decoder l ADX et ecrire un
# MPEG-1 System gagne.
CANDIDATS = (
    shutil.which('ffmpeg'),
    r'C:\Program Files\Shutter Encoder\Library\ffmpeg.exe',
    r'C:\Program Files\freac\codecs\cmdline\ffmpeg.exe',
    r'C:\Users\frede\AppData\Roaming\Digiarty\VideoProc Converter AI'
    r'\ffmpeg.exe',
    r'C:\Program Files (x86)\Digiarty\VideoProc Converter AI\ffmpeg.exe',
)


def _sait(exe, drapeau, motif):
    try:
        r = subprocess.run([exe, '-hide_banner', drapeau],
                           capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return False
    return motif in (r.stdout or '') + (r.stderr or '')


def trouver_ffmpeg():
    """Un ffmpeg qui decode l ADX **et** sait ecrire un MPEG-1 System."""
    for exe in CANDIDATS:
        if not exe or not os.path.exists(exe):
            continue
        if not _sait(exe, '-decoders', 'adpcm_adx'):
            print('   %s : pas de decodeur ADX' % exe)
            continue
        if not _sait(exe, '-muxers', ' mpeg '):
            print('   %s : pas de muxer MPEG-1 System' % exe)
            continue
        return exe
    return None


def demuxer(chemin, dossier):
    """Rend (video .m1v, audio .adx) -- ou (video, None) si le film est muet.

    On ne garde que le PREMIER flux de chaque sorte : les onze films de /tv/
    n en ont qu un (releve de `sfd.py plan`), et prendre le premier evite de
    produire des pistes vides pour un film qui en aurait deux.
    """
    base = os.path.splitext(os.path.basename(chemin))[0]
    f_v = os.path.join(dossier, base + '.m1v')
    f_a = os.path.join(dossier, base + '.adx')
    id_v = id_a = None
    n_v = n_a = 0
    with open(f_v, 'wb') as sv, open(f_a, 'wb') as sa:
        for ident, charge, _ in mod_sfd.paquets(chemin):
            if 0xE0 <= ident <= 0xEF:
                if id_v is None:
                    id_v = ident
                if ident == id_v:
                    sv.write(charge)
                    n_v += len(charge)
            elif 0xC0 <= ident <= 0xDF:
                if id_a is None:
                    id_a = ident
                if ident == id_a:
                    sa.write(charge)
                    n_a += len(charge)
    if n_a == 0:
        os.remove(f_a)
        return f_v, None
    with open(f_a, 'rb') as fp:
        tete = fp.read(4)
    if tete[:2] != b'\x80\x00':
        print('   son inattendu (%s) : on le laisse de cote.' % tete.hex(' '))
        os.remove(f_a)
        return f_v, None
    return f_v, f_a


def convertir(exe, chemin, refaire):
    base = os.path.splitext(os.path.basename(chemin))[0]
    cible = os.path.join(SORTIE, base + '.mpg')
    if os.path.exists(cible) and not refaire:
        # UN LIEN DUR N EST PAS UNE CONVERSION. Les anciens `.mpg` sont le
        # `.sfd` lui-meme sous un autre nom ; on les refait.
        if os.stat(cible).st_nlink == 1:
            print('   deja converti : %s' % os.path.basename(cible))
            return True
        print('   %s etait un LIEN vers le .sfd -- on le convertit.'
              % os.path.basename(cible))
    print('   %s ...' % base)
    f_v, f_a = demuxer(chemin, TRAVAIL)
    tmp = os.path.join(TRAVAIL, base + '.mpg')
    cmd = [exe, '-hide_banner', '-loglevel', 'error', '-y', '-i', f_v]
    if f_a:
        cmd += ['-i', f_a, '-c:a', 'mp2', '-b:a', '224k']
    cmd += ['-c:v', 'copy', '-f', 'mpeg', tmp]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode or not os.path.exists(tmp):
        print('      ECHEC : %s' % (r.stderr or '').strip()[:400])
        return False
    os.makedirs(SORTIE, exist_ok=True)
    os.replace(tmp, cible)          # defait le lien dur sans toucher au .sfd
    for f in (f_v, f_a):
        if f and os.path.exists(f):
            os.remove(f)
    print('      -> %s   %.1f Mo%s'
          % (os.path.basename(cible), os.path.getsize(cible) / 1048576.0,
             '' if f_a else '   (muet : aucun ADX dans le film)'))
    return True


def main(argv):
    exe = trouver_ffmpeg()
    if exe is None:
        print('REFUS : aucun ffmpeg complet trouve. Il en faut un qui decode '
              'l ADX (adpcm_adx) ET sache ecrire un MPEG-1 System (muxer '
              'mpeg). Celui de tools/FFmpeg-based-ADX-converter ne sait que '
              'le premier.')
        return 2
    print('ffmpeg : %s' % exe)
    tous = '--tous' in argv
    refaire = '--refaire' in argv
    os.makedirs(TRAVAIL, exist_ok=True)
    os.makedirs(SORTIE, exist_ok=True)
    n, mal = 0, 0
    for dossier in SOURCES:
        if not os.path.isdir(dossier):
            continue
        for nom in sorted(os.listdir(dossier)):
            if not nom.lower().endswith('.sfd'):
                continue
            base = nom[:-4]
            if not tous and base not in TV:
                continue
            if convertir(exe, os.path.join(dossier, nom), refaire):
                n += 1
            else:
                mal += 1
    try:
        os.rmdir(TRAVAIL)
    except OSError:
        pass
    print('\n%d film(s) pret(s) dans %s%s'
          % (n, SORTIE, ', %d en echec' % mal if mal else ''))
    return 1 if mal else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
