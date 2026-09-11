#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""LA SONDE D'UN DECOR : force un decor, mene le jeu SEUL jusqu'au combat,
journalise les fichiers ouverts et fait des captures. Aucun clavier.

Pourquoi : plusieurs defauts des decors ajoutes (le brouillard d'Aoi, la
brume de Lei-Fei, l'eau d'Eileen, les grillages de Jean et de Wolf) ne se
tranchent qu'a l'image ou dans la liste des fichiers que le moteur ouvre.
Attendre qu'on navigue a la main jusqu'au bon decor ne passe pas a l'echelle ;
supposer est exclu.

Comment :

  * le decor est FORCE a l'unique point ou le gestionnaire consomme une
    demande : `0x18018EF40` lit l'indice demande en `[rcx+0x60]` (cf. memoire
    « Deux index de decor ») -- un point d'arret y ecrit l'indice voulu ;
  * le apm.dll de substitution joue un scenario d'appuis sur START
    (`apm_entrees.txt`, relu a chaud) : titre, sauvegarde, avertissement,
    SINGLE PLAYER, Arcade, selection -- puis plus rien, l'ordinateur se bat ;
  * CreateFileW/A sont suivis : chaque chemin qui passe le filtre est ecrit ;
  * des captures a heures fixes (`--captures`, ou `--toutes N`).

Le scenario d'entrees MANUEL est sauve avant et REMIS apres : le jeu lance
ensuite a la main ne doit pas appuyer tout seul.

    py -3 tools/sonde_decor.py 48 --toutes 10 --secondes 160
    py -3 tools/sonde_decor.py 48 --fichiers light_param,fog_ --secondes 120
    py -3 tools/sonde_decor.py 54 --captures 90:yk5_a.png,120:yk5_b.png

Sorties : `analysis/sonde_decor.txt` et les captures dans `analysis/sonde/`.
"""
import os
import shutil
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402
import tracer_fichiers                                     # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
DEMANDE = 0x18EF40              # rva du consommateur de la demande de decor
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                              'apm_entrees.txt')
APPUIS = (20, 24, 28, 32, 38, 44, 52, 58, 64, 70)


def scenario(appuis):
    lignes = ['# ecrit par tools/sonde_decor.py -- remplace le temps d une sonde',
              'nom start = 7', 'front   = 20', 'journal = 0', 'clavier = 1',
              'manette = 1', '', '0       rien']
    for t in appuis:
        ms = int(t * 1000)
        lignes += ['%d   start' % ms, '%d   rien' % (ms + 300)]
    return ('\n'.join(lignes) + '\n').encode('ascii')


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith('--'):
        print(__doc__)
        return 1
    indice = int(a[0], 0)
    secondes = 150
    if '--secondes' in a:
        secondes = int(a[a.index('--secondes') + 1])
    appuis = APPUIS
    if '--appuis' in a:
        appuis = [float(x) for x in a[a.index('--appuis') + 1].split(',')]
    # --bp 0x180072BA0:dessin,0x180072C3F:texture  -> journal rax/rcx/rdx
    espions = []
    if '--bp' in a:
        for spec in a[a.index('--bp') + 1].split(','):
            morceaux = spec.split(':')
            mem = (int(morceaux[2], 16) - 0x180000000
                   if len(morceaux) > 2 else None)
            espions.append((int(morceaux[0], 16) - 0x180000000, morceaux[1],
                            mem))
    # --histo 0x18007E322:empreinte:Rbp+xmm6  -> compte chaque valeur prise
    # (les entiers tels quels, un xmm en flottant arrondi au 0,05) ; le
    # tableau est ecrit a la fin du journal
    histos = []
    if '--histo' in a:
        for spec in a[a.index('--histo') + 1].split(','):
            adr, nom, regs = spec.split(':')
            histos.append((int(adr, 16) - 0x180000000, nom, regs.split('+')))
    filtres = []
    if '--fichiers' in a:
        filtres = [x.strip().lower()
                   for x in a[a.index('--fichiers') + 1].split(',')]
    dossier = os.path.join(RACINE, 'analysis', 'sonde')
    os.makedirs(dossier, exist_ok=True)
    captures = []
    if '--captures' in a:
        for spec in a[a.index('--captures') + 1].split(','):
            t, nom = spec.split(':', 1)
            captures.append((os.path.join(dossier, nom), float(t),
                             'Virtua Fighter'))
    if '--toutes' in a:
        pas = float(a[a.index('--toutes') + 1])
        debut = float(a[a.index('--depuis') + 1]) if '--depuis' in a else 40
        t = debut
        while t < secondes - 2:
            captures.append((os.path.join(dossier, 'd%d_t%03d.png'
                                          % (indice, t)), t, 'Virtua Fighter'))
            t += pas

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = True
    dbg.bp_max = 400000
    journal = os.path.join(RACINE, 'analysis', 'sonde_decor.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'forces': 0, 'vus': {}, 'poses': set(), 'mem': {},
          'histos': {}}
    regs_de = {'histo:' + nom: regs for _, nom, regs in histos}

    def valeur(ctx, r):
        if r.lower().startswith('xmm'):
            bas = ctx.FltSave.XmmRegisters[int(r[3:])].Low & 0xFFFFFFFF
            f = struct.unpack('<f', struct.pack('<I', bas))[0]
            return round(f * 20) / 20
        return getattr(ctx, r) & 0xFFFFFFFF

    def sur_bp(d, bp, ctx, tid):
        if bp.nom.startswith('histo:'):
            cle = tuple(valeur(ctx, r) for r in regs_de[bp.nom])
            h = et['histos'].setdefault(bp.nom[6:], {})
            h[cle] = h.get(cle, 0) + 1
            return
        if bp.nom.startswith('espion:'):
            n = et.setdefault('espions', {}).get(bp.nom, 0) + 1
            et['espions'][bp.nom] = n
            if n <= 6 or n in (50, 500, 5000):
                mem = et['mem'].get(bp.nom)
                d.dire('  %s #%d : rax=0x%X rcx=0x%X rdx=0x%X rbx=0x%X%s'
                       % (bp.nom[7:], n, ctx.Rax, ctx.Rcx, ctx.Rdx, ctx.Rbx,
                          '' if mem is None else ' [mem]=0x%X' % d.u32(mem)))
            return
        if bp.nom == 'demande':
            v = d.u32(ctx.Rcx + 0x60)
            if v in (0xFFFFFFFF, indice):
                return
            d.write(ctx.Rcx + 0x60, indice.to_bytes(4, 'little'))
            et['forces'] += 1
            d.dire('  decor demande %d -> force a %d' % (v, indice))
            return
        adr = ctx.Rcx                  # 1er argument de CreateFile (x64)
        if not adr:
            return
        brut = d.read(adr, 520)
        if not brut:
            return
        if bp.nom.endswith('W'):
            t = brut.decode('utf-16-le', 'ignore').split('\x00', 1)[0]
        else:
            t = brut.split(b'\x00', 1)[0].decode('latin-1', 'ignore')
        if not t or (filtres and not any(f in t.lower() for f in filtres)):
            return
        if t not in et['vus']:
            d.dire('  fichier : %s' % t)
        et['vus'][t] = et['vus'].get(t, 0) + 1

    def tic(d, t):
        b = d.base_de(MOTEUR)
        if b and not et['pose']:
            et['pose'] = True
            bp = instrument.PointArret('demande', b + DEMANDE, max_coups=100000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
            d.dire('  point d arret sur la demande de decor, t=%.0f s' % t)
            for rva, nom, mem in espions:
                if mem is not None:
                    et['mem']['espion:' + nom] = b + mem
                bp = instrument.PointArret('espion:' + nom, b + rva,
                                           max_coups=100000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)
            for rva, nom, _ in histos:
                bp = instrument.PointArret('histo:' + nom, b + rva,
                                           max_coups=100000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)
        if not filtres:
            return
        for mod in tracer_fichiers.MODULES:
            for fn in tracer_fichiers.FONCTIONS:
                if (mod, fn) in et['poses']:
                    continue
                base = d.base_de(mod)
                off = tracer_fichiers.deplacement(mod, fn)
                if not base or off is None:
                    continue
                et['poses'].add((mod, fn))
                bp = instrument.PointArret(fn, base + off, max_coups=400000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    sauve = SCENARIO_ACTIF + '.avant_sonde'
    shutil.copyfile(SCENARIO_ACTIF, sauve)
    try:
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(scenario(appuis))
        print('decor force : %d ; %d s ; %d capture(s) ; journal %s'
              % (indice, secondes, len(captures), journal))
        r = dbg.run(EXE, os.path.dirname(EXE), secondes, tuple(captures))
    finally:
        shutil.copyfile(sauve, SCENARIO_ACTIF)
        os.remove(sauve)
        for nom, h in sorted(et['histos'].items()):
            fichier.write('  histo %s : %d coups, %d valeurs\n'
                          % (nom, sum(h.values()), len(h)))
            for cle, n in sorted(h.items(), key=lambda kv: -kv[1])[:60]:
                fichier.write('    %-28s %d\n' % (cle, n))
        fichier.close()
    with open(journal, encoding='utf-8') as fp:
        for ligne in fp:
            if ligne.startswith('  ') or 'REFUS' in ligne or 'EXCEPTION' in ligne:
                sys.stdout.write(ligne)
    print('\n%d forcage(s) ; %d fichier(s) distinct(s) ; scenario manuel remis'
          % (et['forces'], len(et['vus'])))
    return r


if __name__ == '__main__':
    sys.exit(main())
