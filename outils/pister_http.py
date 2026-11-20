#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ou la requete HTTP s'arrete-t-elle avant de partir ?

Le serveur `tools/serveur_allnet.py` ecoute bien sur 8080 et 8081, et le jeu
ne lui envoie RIEN -- alors que `Setup::tic` (`0x1802D8F80`, alias
`requestTurnInfo`) tourne 20 661 fois. La requete echoue donc tot, et a chaque
trame.

On pose un point sur chaque maillon du chemin d'emission, du plus haut au plus
bas. Le dernier maillon atteint nomme la marche qui bloque.

    requestTurnInfo   0x1802D8F80   l'etat Setup, appele en boucle
    route turninfo    0x1802D5C50   construit l'URL et le corps vide
    emetteur          0x1802D57C0   garde d'occupation, puis dispatch
    Request::send     0x1802EBA20   controle le creneau (< 6)
    Request::sendData 0x1802EBAC0   recoud l'enveloppe, chiffre, poste
    make request      0x1802FA7F0   zlib + AES
    post              0x1802922B0   curl_easy_setopt + multi_add_handle
    curl update       0x1802927D0   la pompe du transfert

    py -3 tools/pister_http.py --secondes 90
"""
import collections
import os
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                            # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')

POINTS = [
    ('requestTurnInfo',  0x2D8F80),
    ('route turninfo',   0x2D5C50),
    ('emetteur',         0x2D57C0),
    ('emetteur OCCUPE',  0x2D5805),   # la branche � deja en cours �
    ('Request::send',    0x2EBA20),
    ('Request::sendData', 0x2EBAC0),
    ('make request',     0x2FA7F0),
    ('post',             0x2922B0),
    # Juste avant `curl_easy_setopt(CURLOPT_URL)` : `r8` porte l'URL en clair.
    #   0x1802923B7  mov r8, r12
    #   0x1802923BA  mov edx, 0x2712        <- ICI
    #   0x1802923C2  call curl_easy_setopt
    ('URL', 0x2923BA),
    ('curl update',      0x2927D0),
]


def main():
    argv = sys.argv[1:]
    secondes = 90
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 400
    journal = os.path.join(RACINE, 'analysis', 'pister_http.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'compte': collections.Counter(), 't0': None,
          'vus': set(), 'dernier': 0.0}

    def note(txt):
        fichier.write(txt + os.linesep)
        fichier.flush()

    def sur_bp(d, bp, ctx, tid):
        et['compte'][bp.nom] += 1
        if et['t0'] is None:
            et['t0'] = time.time()
        ms = (time.time() - et['t0']) * 1000.0

        if bp.nom == 'URL' and et['compte'][bp.nom] <= 12:
            r8 = ctx.R8 & 0xFFFFFFFFFFFFFFFF
            brut = d.read(r8, 160) or b''
            fin = brut.find(b'\x00')
            note('%9.1f ms  URL donnee a libcurl : %r'
                 % (ms, brut[:fin if fin >= 0 else 80]))
            return

        if bp.nom not in et['vus']:
            et['vus'].add(bp.nom)
            note('%9.1f ms  PREMIERE FOIS : %s' % (ms, bp.nom))
        elif time.time() - et['dernier'] > 10.0:
            et['dernier'] = time.time()
            note('%9.1f ms  --- comptes : %s' % (ms, ', '.join(
                '%s=%d' % (n, c) for n, c in sorted(et['compte'].items()))))

    def tic(d, t):
        if et['pose']:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        for nom_, rva in POINTS:
            bp = instrument.PointArret(nom_, b + rva, max_coups=2000000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  points d\'arret poses a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    print('MESURE : ou la requete HTTP s arrete-t-elle ?')
    print()
    print('  Laissez tourner sur l ecran d attract. Aucune touche.')
    print()
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    lignes = []

    def dit(txt=''):
        lignes.append(txt)

    dit()
    dit('=' * 72)
    dit('COMPTES, du plus haut maillon au plus bas :')
    for nom_, _ in POINTS:
        dit('   %-18s %d' % (nom_, et['compte'][nom_]))
    dit()
    dit('LECTURE : le dernier maillon a compte non nul est le dernier franchi.')
    dit('   � emetteur OCCUPE � > 0 -> la garde d occupation ne retombe jamais :')
    dit('                             une requete precedente n a jamais ete')
    dit('                             soldee, et toutes les suivantes sont')
    dit('                             refusees.')
    bilan = os.path.join(RACINE, 'analysis', 'pister_http_bilan.txt')
    with open(bilan, 'w', encoding='utf-8') as fp:
        fp.write(os.linesep.join(lignes) + os.linesep)
    for t in lignes:
        try:
            print(t)
        except UnicodeEncodeError:
            print(t.encode('ascii', 'replace').decode('ascii'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
