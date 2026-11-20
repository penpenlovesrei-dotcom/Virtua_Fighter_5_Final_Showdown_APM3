#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Construit le dossier VF5_APM3_DECOMP du Bureau a partir du depot.

Ce que la copie EXCLUT, et pourquoi : les *.png (396 Mo de captures d'ecran
et de releves visuels), les outils TIERS livres dans tools/ (Sofdec2,
PARtool, PS4 PKG Tool, FFmpeg...), les __pycache__ et les *.pyc. Le reste
du texte est copie tel quel.
"""
import hashlib
import os
import shutil
import sys

DEPOT = r'C:\Users\frede\Desktop\VF5RE'
CIBLE = r'C:\Users\frede\Desktop\VF5_APM3_DECOMP'

# outils tiers : des executables, pas notre travail
TIERS = {'Sofdec2', 'PS4 PKG Tool (extraction ISO PS4)',
         'PARtool v1.3.windows-x64', 'loaders',
         'FFmpeg-based-ADX-converter',
         'PSN.PKG.Decryptor.&.Extractor.v1.85-LMAN',
         '__pycache__'}
TEXTE = ('.md', '.c', '.h', '.py', '.java', '.txt', '.json', '.csv',
         '.cmd', '.bat', '.cs', '.ini', '.cfg')

copies = []


def copier(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    copies.append((os.path.relpath(dst, CIBLE),
                   os.path.relpath(src, DEPOT), os.path.getsize(src)))


def copier_arbre(sous_dossier, dest, exts=TEXTE, recursif=True):
    """Copie les fichiers TEXTE d'un sous-dossier du depot."""
    racine = os.path.join(DEPOT, sous_dossier)
    if not os.path.isdir(racine):
        return
    for r, ds, fs in os.walk(racine):
        ds[:] = [d for d in ds if d not in TIERS]
        if not recursif and r != racine:
            continue
        for fn in fs:
            if not fn.lower().endswith(exts):
                continue
            rel = os.path.relpath(os.path.join(r, fn), racine)
            copier(os.path.join(r, fn), os.path.join(CIBLE, dest, rel))


def copier_motif(dossier, dest, exts):
    racine = os.path.join(DEPOT, dossier)
    for fn in sorted(os.listdir(racine)):
        p = os.path.join(racine, fn)
        if os.path.isfile(p) and fn.lower().endswith(exts):
            copier(p, os.path.join(CIBLE, dest, fn))


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    if os.path.exists(CIBLE):
        print('le dossier existe deja : %s' % CIBLE)
        print('supprime-le ou renomme-le d abord, je ne l ecrase pas.')
        return 1
    os.makedirs(CIBLE)

    # 1. les binaires de reference
    bins = [
        ('runtime/media/vf5fs/vfes.exe.origine',
         'binaires/vfes.exe.origine'),
        ('runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll.origine',
         'binaires/vf5fs-pxd-w64-Retail_APM3.dll.origine'),
        ('runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll',
         'binaires/vf5fs-pxd-w64-Retail_APM3.dll.PATCHEE'),
        ('runtime/media/vf5fs/vfes.exe',
         'binaires/vfes.exe.PATCHE'),
        ('runtime/media/vf5fs/apm.reelle.dll',
         'binaires/apm.reelle.dll'),
        ('runtime/media/vf5fs/apmgamepad.dll',
         'binaires/apmgamepad.dll'),
        ('runtime/media/vf5fs/apm.dll',
         'binaires/apm.dll.notre_greffe'),
    ]
    empreintes = []
    for src, dst in bins:
        s = os.path.join(DEPOT, src)
        if not os.path.exists(s):
            print('  ABSENT : %s' % src)
            continue
        d = os.path.join(CIBLE, dst)
        copier(s, d)
        empreintes.append((dst, os.path.getsize(s), sha(s)))

    # 2. la documentation redigee
    copier_motif('analysis', 'documentation', ('.md',))
    for f in ('REPRISE.md', 'REPRISE_QUEST.md', 'REPRISE_PROMPT.md',
              'PROMPT_TERMINAL_ET_QUEST.md', 'A FAIRE.txt'):
        p = os.path.join(DEPOT, f)
        if os.path.exists(p):
            copier(p, os.path.join(CIBLE, 'documentation', '_journal', f))
    copier_arbre('notes', 'documentation/notes')
    copier_arbre('docs', 'documentation/docs')

    # 3. le C decompile par Ghidra
    copier_motif('analysis', 'code_decompile', ('.c',))
    copier_arbre('analysis/quest', 'code_decompile/quest', ('.c',))

    # 4. le desassemblage
    copier_arbre('analysis/disasm', 'desassemblage')
    for fn in sorted(os.listdir(os.path.join(DEPOT, 'analysis'))):
        if fn.startswith('disasm') and fn.endswith('.txt'):
            copier(os.path.join(DEPOT, 'analysis', fn),
                   os.path.join(CIBLE, 'desassemblage', fn))

    # 5. les donnees : releves, inventaires, tables
    copier_motif('analysis', 'donnees', ('.json', '.csv'))
    for fn in sorted(os.listdir(os.path.join(DEPOT, 'analysis'))):
        if fn.endswith('.txt') and not fn.startswith('disasm'):
            copier(os.path.join(DEPOT, 'analysis', fn),
                   os.path.join(CIBLE, 'donnees', fn))
    copier_arbre('analysis/inventory', 'donnees/inventory')
    copier_arbre('analysis/quest', 'donnees/quest',
                 ('.txt', '.json', '.md'))
    copier_arbre('analysis/dlc', 'donnees/dlc', ('.json',))
    copier_arbre('analysis/yamp', 'donnees/yamp')

    # 6. le C# de la borne APM3
    copier_arbre('analysis/apm3_source', 'csharp_apm3', ('.cs',))

    # 7. les outils
    copier_arbre('tools', 'outils')
    copier_arbre('scripts', 'outils/scripts')

    # le manifeste
    man = os.path.join(CIBLE, 'MANIFESTE.txt')
    with open(man, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write('MANIFESTE DE VF5_APM3_DECOMP\r\n')
        f.write('=' * 60 + '\r\n\r\n')
        f.write('Source : %s\r\n\r\n' % DEPOT)
        f.write('EMPREINTES SHA-256 DES BINAIRES\r\n')
        for d, t, h in empreintes:
            f.write('  %-52s %9d o\r\n    %s\r\n' % (d, t, h))
        f.write('\r\nFICHIERS COPIES : %d\r\n' % len(copies))
        f.write('%-62s %-52s %10s\r\n' % ('dans ce dossier',
                                          'depuis le depot', 'octets'))
        f.write('-' * 128 + '\r\n')
        for d, s, t in sorted(copies):
            f.write('%-62s %-52s %10d\r\n' % (d, s, t))
    tot = sum(t for _, _, t in copies)
    print('%d fichiers, %.1f Mo' % (len(copies), tot / 1048576.0))
    for d in sorted(os.listdir(CIBLE)):
        p = os.path.join(CIBLE, d)
        if os.path.isdir(p):
            n = sum(len(fs) for _, _, fs in os.walk(p))
            o = sum(os.path.getsize(os.path.join(r, x))
                    for r, _, fs in os.walk(p) for x in fs)
            print('  %-20s %4d fichiers  %8.1f Mo' % (d, n, o / 1048576.0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
