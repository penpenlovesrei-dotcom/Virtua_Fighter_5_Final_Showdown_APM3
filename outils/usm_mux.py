#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Multiplexeur USM : convertit un `.sfd` (Sofdec1) en `.usm` (Sofdec2)
SANS REENCODER une seule image.

POURQUOI C'EST POSSIBLE, ET POURQUOI C'EST SANS PERTE

Sofdec2 accepte plusieurs codecs video ; `VIDEO_HDRINFO.mpeg_codec` les
distingue. Dans les films d'APM3 on trouve les deux :

    mpeg_codec = 1   Sofdec.Prime  -> c'est du MPEG, le MEME que dans un .sfd
    mpeg_codec = 5   H.264

Et `AUDIO_HDRINFO.audio_codec = 2` est de l'ADX -- exactement ce qu'un `.sfd`
transporte dans son « private stream 1 » ou son flux audio MPEG.

Un `.sfd` est un flux de programme MPEG ordinaire : sa video est deja un flux
elementaire MPEG et son son est deja de l'ADX. **Il n'y a donc rien a
convertir : il n'y a qu'a remballer.** On demultiplexe le MPEG-PS, on decoupe
la video image par image, l'ADX par blocs, et on ecrit les morceaux Sofdec2
autour. Les octets d'image et les octets de son traversent l'outil INTACTS.

C'est la difference avec le Scaleform Video Encoder (`medianoche.exe`) du
dossier « MP4 to USM » : celui-la DECODE puis REENCODE en H.264. Il produit un
USM lisible, mais il repasse par la case compression -- donc il perd.

CE QUI A ETE MESURE (et non suppose) SUR LES FILMS DU JEU

`vf5adv.usm` (335 Mo, APM3) est un film Prime + ADX. Structure relevee :

    CRID type 1   table CRIUSF_DIR_STREAM, bourree jusqu'a 0x800
    @SFV type 1   table VIDEO_HDRINFO
    @SFA type 1   table AUDIO_HDRINFO
    @SFV type 2   "#HEADER END     ==============="
    @SFA type 2   idem
    @SFV type 3   table VIDEO_SEEKINFO
    @SFV type 2   "#METADATA END   ==============="
    ... morceaux de donnees entrelaces ...
    @SFV type 2   "#CONTENTS END   ==============="
    @SFA type 2   idem

* **une image par morceau video** : 7304 morceaux `@SFV` de donnee pour
  `total_frames = 7304`. Verifie par comptage ;
* un morceau audio = **50 blocs ADX = 1600 echantillons** (1800 octets en
  stereo), et le tout premier morceau audio ne porte que l'en-tete ADX ;
* la table de recherche `VIDEO_SEEKINFO` donne l'offset ABSOLU dans le fichier
  du morceau video, et une ligne par debut de GOP (598 lignes pour 7304
  images) ;
* chaque morceau est bourre pour que sa taille totale soit multiple de 0x20.

CE QUI RESTE INCERTAIN, ET QUI NE SE VOIT QU'A L'ECRAN

Le champ `date` des morceaux video de CRI avance de ~49,95 par image a une
cadence de 6000, soit une duree totale MOITIE de la vraie (60,8 s pour un film
de 121,7 s), alors que l'audio, lui, est juste. Les cinq films du jeu ont tous
ce meme decalage : c'est une convention de l'outil de CRI, pas un accident, et
le lecteur se sert donc de `framerate_n / framerate_d` pour cadencer. On
reproduit la convention observee (`--dates cri`, par defaut) parce que c'est
elle que ce moteur a toujours recue ; `--dates justes` ecrit le temps reel.

LE MULTIPISTE

Un `.sfd` peut porter plusieurs sons : `vf5verBadv.sfd` en a deux flux, un ADX
simple (la piste principale) et un conteneur **AIX** -- le multipiste de CRI,
trois ADX entrelaces par morceaux `AIXP` etiquetes du numero de leur flux.
L'outil deplie l'AIX et range chaque flux dans sa propre voie `@SFA` : ce film
sort donc en **quatre voies audio**, toutes verifiees octet pour octet.

    py -3 tools/usm_mux.py <entree.sfd> <sortie.usm>
    py -3 tools/usm_mux.py <entree.sfd> <sortie.usm> --nom vf5moe.usm
    py -3 tools/usm_mux.py <entree.sfd> <sortie.usm> --pistes 1
    py -3 tools/usm_mux.py --verifier <sortie.usm>
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import sfd as mod_sfd                                          # noqa: E402
import usm as mod_usm                                          # noqa: E402

ALIGN = 0x20
DEPL = 0x18
CADENCE_VIDEO = 6000
CADENCE_AUDIO = 2997
BLOCS_PAR_MORCEAU = 50            # 50 blocs ADX = 1600 echantillons
ECH_PAR_BLOC = 32
MARQUE_ENTETE = b'#HEADER END     ===============\x00'
MARQUE_META = b'#METADATA END   ===============\x00'
MARQUE_FIN = b'#CONTENTS END   ===============\x00'

# codes de cadence du MPEG (sequence_header), en (numerateur, denominateur)
CADENCES_MPEG = {1: (24000, 1001), 2: (24000, 1000), 3: (25000, 1000),
                 4: (30000, 1001), 5: (30000, 1000), 6: (50000, 1000),
                 7: (60000, 1001), 8: (60000, 1000)}


# ------------------------------------------------------------- ecriture @UTF
def ecrire_utf(nom_table, colonnes, lignes):
    """Construit une table `@UTF`.

    `colonnes` : liste de (nom, type, rangement, constante). Les types et les
    rangements sont ceux decrits dans `tools/usm.py`. Les valeurs des lignes
    sont prises dans le dictionnaire de chaque ligne.
    """
    chaines, pot = {}, bytearray()

    def offset_chaine(s):
        if s not in chaines:
            chaines[s] = len(pot)
            pot.extend(s.encode('utf-8') + b'\x00')
        return chaines[s]

    def empaqueter(t, v):
        fmt = {0: '>B', 1: '>b', 2: '>H', 3: '>h', 4: '>I', 5: '>i',
               6: '>Q', 7: '>q', 8: '>f', 9: '>d'}.get(t)
        if fmt:
            return struct.pack(fmt, v)
        if t == 0xA:
            return struct.pack('>I', offset_chaine(v))
        raise ValueError('type non ecrit : 0x%X' % t)

    off_nom = offset_chaine(nom_table)
    for nom, _, _, _ in colonnes:
        offset_chaine(nom)

    bloc_col = bytearray()
    for nom, typ, rangement, constante in colonnes:
        bloc_col.append(rangement | typ)
        bloc_col.extend(struct.pack('>I', chaines[nom]))
        if rangement == 0x30:
            bloc_col.extend(empaqueter(typ, constante))

    bloc_lig = bytearray()
    long_ligne = 0
    for ligne in lignes:
        avant = len(bloc_lig)
        for nom, typ, rangement, _ in colonnes:
            if rangement != 0x50:
                continue
            bloc_lig.extend(empaqueter(typ, ligne[nom]))
        long_ligne = len(bloc_lig) - avant

    off_lignes = 24 + len(bloc_col)
    off_chaines = off_lignes + len(bloc_lig)
    off_donnees = off_chaines + len(pot)
    corps = bytearray()
    corps.extend(struct.pack('>4I', off_lignes, off_chaines, off_donnees,
                             off_nom))
    corps.extend(struct.pack('>2H', len(colonnes), long_ligne))
    corps.extend(struct.pack('>I', len(lignes)))
    corps.extend(bloc_col)
    corps.extend(bloc_lig)
    corps.extend(pot)
    while len(corps) % 8:                       # CRI aligne la table sur 8
        corps.append(0)
    return b'@UTF' + struct.pack('>I', len(corps)) + bytes(corps)


def morceau(sig, type_, voie, date, cadence, charge, bourrage_mini=0):
    """Un morceau USM complet, bourre jusqu'a un multiple de 0x20."""
    total = DEPL + 8 + len(charge) + bourrage_mini
    reste = (-total) % ALIGN
    bourrage = bourrage_mini + reste
    taille = DEPL + len(charge) + bourrage
    tete = (sig + struct.pack('>I', taille)
            + bytes([0, DEPL]) + struct.pack('>H', bourrage)
            + bytes([voie, 0, 0, type_])
            + struct.pack('>2I', date, cadence)
            + struct.pack('>2I', 0, 0))
    assert len(tete) == 0x20, len(tete)
    return tete + charge + b'\x00' * bourrage


# ------------------------------------------------------ lecture du flux video
def decouper_video(chemin_es):
    """Rend [(offset, longueur, gop)] : une entree par IMAGE.

    Une unite commence a l'en-tete de sequence (`B3`) ou de GOP (`B8`) qui
    precede l'image, sinon au code d'image (`00`) lui-meme. `gop` dit si
    l'unite ouvre un groupe -- c'est la que la table de recherche pose une
    ligne.
    """
    d = open(chemin_es, 'rb').read()
    unites, debut_en_attente, gop_en_attente = [], None, False
    i, n = 0, len(d)
    positions = []
    while True:
        i = d.find(b'\x00\x00\x01', i)
        if i < 0 or i + 3 >= n:
            break
        code = d[i + 3]
        if code in (0xB3, 0xB8):
            if debut_en_attente is None:
                debut_en_attente = i
            gop_en_attente = True
        elif code == 0x00:                       # picture_start_code
            deb = debut_en_attente if debut_en_attente is not None else i
            positions.append((deb, gop_en_attente))
            debut_en_attente, gop_en_attente = None, False
        elif code in (0xB5, 0xB2):
            pass                                  # extension, donnees privees
        else:
            debut_en_attente = None
        i += 3
    for k, (deb, gop) in enumerate(positions):
        fin = positions[k + 1][0] if k + 1 < len(positions) else n
        unites.append((deb, fin - deb, gop))
    return d, unites


def lire_sequence(d):
    """Largeur, hauteur, cadence, lues dans l'en-tete de sequence MPEG."""
    i = d.find(b'\x00\x00\x01\xb3')
    if i < 0:
        raise ValueError('aucun en-tete de sequence MPEG dans la video')
    o = i + 4
    larg = (d[o] << 4) | (d[o + 1] >> 4)
    haut = ((d[o + 1] & 0x0F) << 8) | d[o + 2]
    code = d[o + 3] & 0x0F
    num, den = CADENCES_MPEG.get(code, (30000, 1001))
    # extension MPEG-2 : elle etend la taille et peut multiplier la cadence
    j = d.find(b'\x00\x00\x01\xb5', i, i + 512)
    if j > 0 and (d[j + 4] >> 4) == 1:           # sequence_extension
        e = d[j + 4:j + 10]
        larg |= ((e[1] & 0x01) << 13) | ((e[2] & 0x80) << 5)
        haut |= (e[2] & 0x60) << 7
        num *= ((e[5] >> 5) & 3) + 1
        den *= (e[5] & 0x1F) + 1
    return larg, haut, num, den


# -------------------------------------------------------- lecture du flux ADX
def lire_aix(d):
    """Deplie un conteneur AIX en ses flux ADX. Rend une liste d'octets.

    L'AIX est le multipiste de CRI : un en-tete, puis des morceaux `AIXP`
    entrelaces, chacun etiquete du numero du flux auquel il appartient.
    Releve sur la piste 0xC2 de `vf5verBadv.sfd` :

        en-tete, gros-boutiste
          +0x00  'AIXF'
          +0x04  u32  offset du premier AIXP, moins 8
          +0x20  u32  offset des donnees (0x1800)
          +0x24  u32  taille totale des donnees
          +0x28  u32  nombre d'echantillons
          +0x2C  u32  frequence
          +0x40  u8   NOMBRE DE FLUX
          +0x48  par flux : u32 frequence, u8 canaux, 3 octets de bourrage

        morceau AIXP
          +0x00  'AIXP'
          +0x04  u32  taille de la charge, BOURRAGE COMPRIS
          +0x08  u8   numero du flux         +0x09  u8  nombre de flux
          +0x0A  u16  longueur UTILE de la charge
          +0x0C  u32  numero de bloc (0xFFFFFFFF pour l'en-tete ADX)
          +0x10  la charge

    Il suffit donc de recoller, flux par flux, les charges utiles : le premier
    morceau de chaque flux porte son en-tete ADX, les suivants ses blocs. Rien
    n'est decode, rien n'est recalcule.
    """
    if d[:4] != b'AIXF':
        return []
    n_flux = d[0x40]
    if not 1 <= n_flux <= 32:
        return []
    debut, = struct.unpack_from('>I', d, 0x20)
    bouts = [bytearray() for _ in range(n_flux)]
    o = debut
    while o + 16 <= len(d):
        if d[o:o + 4] != b'AIXP':
            break                               # 'AIXE' ou fin
        taille, = struct.unpack_from('>I', d, o + 4)
        flux = d[o + 8]
        utile, = struct.unpack_from('>H', d, o + 0x0A)
        if flux < n_flux:
            bouts[flux] += d[o + 0x10:o + 0x10 + utile]
        o += 8 + taille
    return [bytes(b) for b in bouts if b]


def lire_adx(source):
    """`source` est un chemin ou des octets."""
    d = open(source, 'rb').read() if isinstance(source, str) else source
    if d[:2] != b'\x80\x00':
        return None
    copyright_offset, = struct.unpack_from('>H', d, 2)
    entete = copyright_offset + 4
    bloc = d[5]
    voies = d[7]
    frequence, = struct.unpack_from('>I', d, 8)
    total, = struct.unpack_from('>I', d, 0x0C)
    return {'octets': d, 'entete': entete, 'bloc': bloc, 'voies': voies,
            'frequence': frequence, 'total': total}


# ------------------------------------------------------------------ le muxage
def convertir(entree, sortie, nom_interne=None, dates='cri', verbeux=True,
              limite_pistes=0):
    travail = sortie + '.demux'
    os.makedirs(travail, exist_ok=True)
    if verbeux:
        print('1/4  demultiplexage de %s' % os.path.basename(entree))
    mod_sfd.cmd_demux(entree, travail)
    fichiers = os.listdir(travail)
    v = [f for f in fichiers if f.endswith('.m2v')]
    a = [f for f in fichiers if f.endswith('.bin')]
    if not v:
        print('REFUS : aucun flux video MPEG dans %s' % entree)
        return 1
    chemin_v = os.path.join(travail, v[0])
    # Un .sfd peut porter PLUSIEURS pistes (vf5verBadv en a deux, 0xC1 et
    # 0xC2). Sofdec2 les range en voies : @SFA voie 0, voie 1, ...
    adxs, ecartes = [], []
    for f in sorted(a):
        chemin = os.path.join(travail, f)
        with open(chemin, 'rb') as fp:
            magie = fp.read(4)
        if magie == b'AIXF':
            brut = open(chemin, 'rb').read()
            flux = lire_aix(brut)
            if not flux:
                ecartes.append((f, 'AIX illisible', os.path.getsize(chemin)))
                continue
            for k, morceau_adx in enumerate(flux):
                x = lire_adx(morceau_adx)
                if x:
                    x['source'] = '%s [AIX %d/%d]' % (f, k + 1, len(flux))
                    adxs.append(x)
                else:
                    ecartes.append(('%s [AIX %d]' % (f, k), 'sous-flux non ADX',
                                    len(morceau_adx)))
            continue
        x = lire_adx(chemin)
        if x:
            x['source'] = f
            adxs.append(x)
        else:
            ecartes.append((f, magie.hex(' '), os.path.getsize(chemin)))
    if limite_pistes:
        adxs = adxs[:limite_pistes]
    adx = adxs[0] if adxs else None
    if verbeux:
        print('     video : %s (%d octets)' % (v[0], os.path.getsize(chemin_v)))
        if not adxs:
            print('     audio : aucun')
        for k, x in enumerate(adxs):
            print('     audio voie %d : %s, ADX %d canaux, %d Hz, %d '
                  'echantillons'
                  % (k, x['source'], x['voies'], x['frequence'], x['total']))
    for f, quoi, n in ecartes:
        print('     ATTENTION : %s (%d octets) -- %s, ecarte.' % (f, n, quoi))

    if verbeux:
        print('2/4  decoupage image par image')
    video, unites = decouper_video(chemin_v)
    larg, haut, num, den = lire_sequence(video)
    n_images = len(unites)
    if verbeux:
        print('     %d images, %dx%d, %.3f images/s'
              % (n_images, larg, haut, num / den))

    # --- les morceaux audio, une liste par voie ---
    pistes = []
    for x in adxs:
        pas = BLOCS_PAR_MORCEAU * x['bloc'] * x['voies']
        bouts = [x['octets'][:x['entete']]]
        o = x['entete']
        while o < len(x['octets']):
            bouts.append(x['octets'][o:o + pas])
            o += pas
        pistes.append(bouts)

    def date_video(i):
        if dates == 'justes':
            return int(round(i * CADENCE_VIDEO * den / num))
        return 0 if i == 0 else 50 * i - 1        # convention relevee chez CRI

    def date_audio(i):
        if i == 0:
            return 0
        return (i - 1) * 100

    # --- premiere passe : tailles, pour la table de recherche ---
    lignes_seek = [k for k, (_, _, gop) in enumerate(unites) if gop]
    if not lignes_seek:
        lignes_seek = [0]
    seek = [{'ofs_byte': 0, 'ofs_frmid': k} for k in lignes_seek]
    # schema releve dans vf5adv.usm : seuls les deux premiers champs sont
    # ecrits par ligne (ligne de 12 octets), les deux autres sont des
    # constantes de colonne.
    col_seek = [('ofs_byte', 6, 0x50, None), ('ofs_frmid', 5, 0x50, None),
                ('num_skip', 3, 0x30, 0), ('resv', 3, 0x30, 0)]
    PAS_SEEK = 12

    duree = n_images * den / num
    taille_max_v = max(l for _, l, _ in unites) + 0x40
    taille_max_a = max((len(m) for p in pistes for m in p), default=0) + 0x40
    ix_v = taille_max_v * 8
    ix_a = taille_max_a * 8

    nom_interne = nom_interne or os.path.basename(sortie)
    col_dir = [('fmtver', 4, 0x30, 0), ('filename', 0xA, 0x50, None),
               ('filesize', 4, 0x50, None), ('datasize', 4, 0x30, 0),
               ('stmid', 4, 0x50, None), ('chno', 2, 0x50, None),
               ('minchk', 2, 0x50, None), ('minbuf', 4, 0x50, None),
               ('avbps', 4, 0x50, None)]
    col_video = [(n, 4, 0x50, None) for n in
                 ('width', 'height', 'mat_width', 'mat_height', 'disp_width',
                  'disp_height', 'scrn_width')]
    col_video += [('mpeg_dcprec', 0, 0x50, None), ('mpeg_codec', 0, 0x50, None)]
    col_video += [(n, 4, 0x50, None) for n in
                  ('alpha_type', 'total_frames', 'framerate_n', 'framerate_d',
                   'metadata_count', 'metadata_size', 'ixsize', 'pre_padding',
                   'max_picture_size', 'color_space', 'picture_type')]
    col_audio = [('audio_codec', 0, 0x50, None),
                 ('sampling_rate', 4, 0x50, None),
                 ('total_samples', 4, 0x50, None),
                 ('num_channels', 0, 0x50, None),
                 ('metadata_count', 4, 0x50, None),
                 ('metadata_size', 4, 0x50, None),
                 ('ixsize', 4, 0x50, None), ('ambisonics', 0, 0x50, None)]

    def entetes(taille_fichier, meta_seek):
        lignes_dir = [{'filename': nom_interne, 'filesize': taille_fichier,
                       'stmid': 0, 'chno': 0xFFFF, 'minchk': 1,
                       'minbuf': max(ix_v, ix_a),
                       'avbps': int(taille_fichier * 8 / max(duree, 1e-6))},
                      {'filename': nom_interne, 'filesize': taille_fichier,
                       'stmid': 0x40534656, 'chno': 0, 'minchk': 3,
                       'minbuf': ix_v,
                       'avbps': int(len(video) * 8 / max(duree, 1e-6))}]
        for k, x in enumerate(adxs):
            lignes_dir.append(
                {'filename': nom_interne, 'filesize': taille_fichier,
                 'stmid': 0x40534641, 'chno': k, 'minchk': 1, 'minbuf': ix_a,
                 'avbps': int(len(x['octets']) * 8 / max(duree, 1e-6))})
        d_crid = ecrire_utf('CRIUSF_DIR_STREAM', col_dir, lignes_dir)
        d_video = ecrire_utf('VIDEO_HDRINFO', col_video, [{
            'width': larg, 'height': haut, 'mat_width': larg,
            'mat_height': haut, 'disp_width': larg, 'disp_height': haut,
            'scrn_width': 0, 'mpeg_dcprec': 9, 'mpeg_codec': 1,
            'alpha_type': 0, 'total_frames': n_images, 'framerate_n': num,
            'framerate_d': den, 'metadata_count': 1,
            'metadata_size': len(meta_seek), 'ixsize': ix_v, 'pre_padding': 0,
            'max_picture_size': 0, 'color_space': 0, 'picture_type': 0}])
        d_audio = [ecrire_utf('AUDIO_HDRINFO', col_audio, [{
            'audio_codec': 2, 'sampling_rate': x['frequence'],
            'total_samples': x['total'], 'num_channels': x['voies'],
            'metadata_count': 0, 'metadata_size': 0, 'ixsize': ix_a,
            'ambisonics': 0}]) for x in adxs]
        return d_crid, d_video, d_audio

    def assembler(taille_fichier, fp):
        """Ecrit le film, ou -- si `fp` est None -- se contente de mesurer.

        Tous les champs sont de taille FIXE : la mise en page ne depend donc
        pas des valeurs. Une passe a blanc suffit a connaitre la taille finale
        et la position de chaque image ; la vraie passe ecrit directement sur
        le disque, sans jamais tenir le film entier en memoire.
        """
        meta_seek = ecrire_utf('VIDEO_SEEKINFO', col_seek, seek)
        d_crid, d_video, d_audio = entetes(taille_fichier, meta_seek)
        pos = [0]

        def poser(sig, type_, date, cadence, charge, bourrage_mini=0, voie=0):
            m = morceau(sig, type_, voie, date, cadence, charge, bourrage_mini)
            if fp is not None:
                fp.write(m)
            pos[0] += len(m)

        poser(b'CRID', 1, 0, 30, d_crid,
              bourrage_mini=0x800 - 0x20 - len(d_crid))
        poser(b'@SFV', 1, 0, 30, d_video)
        for k, d in enumerate(d_audio):
            poser(b'@SFA', 1, 0, 30, d, voie=k)
        poser(b'@SFV', 2, 0, 30, MARQUE_ENTETE)
        for k in range(len(d_audio)):
            poser(b'@SFA', 2, 0, 30, MARQUE_ENTETE, voie=k)
        # Ou commencent les LIGNES de la table de recherche dans le fichier :
        # tete du morceau (0x20) + les 8 octets de '@UTF' et de sa taille +
        # l'offset que la table declare elle-meme.
        off_lignes, = struct.unpack_from('>I', meta_seek, 8)
        pos_seek = pos[0] + 0x20 + 8 + off_lignes
        poser(b'@SFV', 3, 0, 30, meta_seek)
        poser(b'@SFV', 2, 0, 30, MARQUE_META)

        positions = {}
        iv = 0
        ia = [0] * len(pistes)

        def temps_audio(k):
            if ia[k] >= len(pistes[k]):
                return 1e30
            return (max(ia[k] - 1, 0) * BLOCS_PAR_MORCEAU * ECH_PAR_BLOC
                    / adxs[k]['frequence'])

        while iv < n_images or any(ia[k] < len(pistes[k])
                                   for k in range(len(pistes))):
            t_v = iv * den / num if iv < n_images else 1e30
            k_min, t_a = -1, 1e30
            for k in range(len(pistes)):
                t = temps_audio(k)
                if t < t_a:
                    k_min, t_a = k, t
            if t_v <= t_a:
                deb, lg, _ = unites[iv]
                positions[iv] = pos[0]
                poser(b'@SFV', 0, date_video(iv), CADENCE_VIDEO,
                      video[deb:deb + lg])
                iv += 1
            else:
                poser(b'@SFA', 0, date_audio(ia[k_min]), CADENCE_AUDIO,
                      pistes[k_min][ia[k_min]], voie=k_min)
                ia[k_min] += 1
        poser(b'@SFV', 2, 0, 30, MARQUE_FIN)
        for k in range(len(pistes)):
            poser(b'@SFA', 2, 0, 30, MARQUE_FIN, voie=k)
        return pos[0], pos_seek, positions

    if verbeux:
        print('3/4  mise en page a blanc (la table de recherche porte des '
              'offsets absolus)')
    taille, pos_seek, positions = assembler(0, None)
    for ligne in seek:
        ligne['ofs_byte'] = positions[ligne['ofs_frmid']]

    if verbeux:
        print('4/4  ecriture de %s' % sortie)
    with open(sortie, 'wb') as fp:
        taille2, pos_seek2, positions2 = assembler(taille, fp)
    if (taille2, pos_seek2, positions2) != (taille, pos_seek, positions):
        print('REFUS : la deuxieme passe ne rend pas la meme mise en page que '
              'la premiere. Le fichier ecrit est faux ; ne l utilisez pas.')
        return 1
    for f in os.listdir(travail):
        os.remove(os.path.join(travail, f))
    os.rmdir(travail)
    print('\n%s : %d octets, %d images %dx%d a %.3f/s%s'
          % (os.path.basename(sortie), taille, n_images, larg, haut,
             num / den,
             ', %d piste(s) ADX %d canaux %d Hz'
             % (len(adxs), adxs[0]['voies'], adxs[0]['frequence'])
             if adxs else ', sans son'))
    return 0


def verifier(chemin):
    """Relit le fichier produit avec notre propre lecteur."""
    print('relecture de %s' % os.path.basename(chemin))
    compte = {}
    with open(chemin, 'rb') as fp:
        for m in mod_usm.morceaux(chemin):
            cle = (m['sig'], m['type'])
            compte[cle] = compte.get(cle, 0) + 1
            if m['type'] in (1, 3):
                d = mod_usm.charge(fp, m)
                if d[:4] == b'@UTF':
                    nom, lignes, _ = mod_usm.lire_utf(d)
                    print('  table %-20s %d ligne(s)' % (nom, len(lignes)))
    for cle in sorted(compte):
        print('  %-4s type %d : %d morceau(x)' % (cle[0], cle[1], compte[cle]))
    return 0


def main():
    a = sys.argv[1:]
    if '--verifier' in a:
        i = a.index('--verifier')
        return verifier(a[i + 1])
    dates = 'cri'
    if '--dates' in a:
        i = a.index('--dates')
        dates = a[i + 1]
        del a[i:i + 2]
    nom = None
    if '--nom' in a:
        i = a.index('--nom')
        nom = a[i + 1]
        del a[i:i + 2]
    limite = 0
    if '--pistes' in a:
        i = a.index('--pistes')
        limite = int(a[i + 1])
        del a[i:i + 2]
    a = [x for x in a if not x.startswith('--')]
    if len(a) < 2:
        print(__doc__)
        return 1
    if not os.path.exists(a[0]):
        print('introuvable : %s' % a[0])
        return 1
    return convertir(a[0], a[1], nom, dates, limite_pistes=limite)


if __name__ == '__main__':
    sys.exit(main())
