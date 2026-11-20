#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carte complete d'une zone de code : toutes les fonctions, d'un coup.

Pourquoi cet outil existe. Pendant toute la journee du 2026-09-04 j'ai
desassemble **a la demande** -- une fonction, une question, une fonction --
ce qui donne l'illusion d'avancer et fait tourner en rond : quatre fausses
pistes sur le selecteur, dont trois correctifs bâtis sur des lectures locales.
Frederic : « je ne comprends pas pourquoi toutes les fonctions de l'ecran de
selection ne sont pas encore desassemblees ».

Il a raison. Cartographier une zone entiere coute une minute et remplace
vingt questions. Pour chaque fonction de la plage demandee, on releve :

  * ses bornes `.pdata` et sa taille ;
  * qui elle appelle, et qui l'appelle ;
  * les **chaines** qu'elle reference (c'est ce qui nomme une fonction) ;
  * les **globaux connus** qu'elle lit (drapeaux de mode, etc.) ;
  * les **immediats remarquables** : identifiants de scene, bornes de roster ;
  * si c'est un bouchon.

Usage :
    py -3 tools/carte_zone.py 0x180160000 0x180178000 selecteur
    py -3 tools/carte_zone.py 0x18023A000 0x180242000 apm3
"""
import collections
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import pe_disasm as P                                       # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')

GLOBAUX = {
    0x180C3B700: 'is_dural_unlocked',
    0x180C3B701: 'game_mode!=0',
    0x180C3B702: 'game_mode==2',
    0x180C3B703: 'is_triangle_start',
    0x1806490D0: 'reglages(+0x20 = VGA/WXGA)',
    0x180752148: 'contexte global',
    0x180714928: 'objet du selecteur',
    0x18064D950: 'vf5fs_game_config_t',
}
BOUCHONS = {0x180007430, 0x180007440, 0x180007450, 0x180029FB0, 0x1801294B0}
# identifiants de scene du selecteur, lus dans aet_db
SCENES = {0x149: 'SELCHA_VGA', 0x14A: 'SELCHA_WXGA', 0x14B: 'SELCMN_VGA',
          0x14C: 'SELCMN_WXGA', 0x14D: 'SELMOD_MAIN', 0x14E: 'SELMOD_POINT',
          0x14F: 'SELSTG_VGA', 0x150: 'SELSTG_WXGA'}
# valeurs qui comptent dans la numerotation d'affichage de la grille
NOTABLES = {0x12: '18 (borne de roster)', 0x13: '19 = DURAL',
            0x14: '20 = ALEATOIRE', 0x15: '21 = aucun'}


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 1
    lo, hi, nom = int(sys.argv[1], 0), int(sys.argv[2], 0), sys.argv[3]
    img = P.Image(MOTEUR)
    d = img.data
    fs = P.runtime_functions(img)
    debuts = {a: b for a, b in fs}

    def cstr(va):
        for s in img.secs:
            if s['va'] <= va < s['va'] + max(s.get('vsize', 0), s['rsize']):
                o = s['off'] + (va - s['va'])
                e = d.find(b'\0', o)
                t = d[o:e]
                if 2 <= len(t) <= 48 and all(32 <= c < 127 for c in t):
                    return t.decode('latin-1')
        return None

    infos = {}
    appelants = collections.defaultdict(set)
    for deb, fin in fs:
        o = img.va2off(deb)
        if o is None:
            continue
        ins = list(img.md.disasm(d[o:o + (fin - deb)], deb))
        appels, chaines, globaux, notables, scenes = [], [], [], [], []
        for x in ins:
            if x.mnemonic == 'call' and x.op_str.startswith('0x'):
                c = int(x.op_str, 16)
                appels.append(c)
                if lo <= c < hi or lo <= deb < hi:
                    appelants[c].add(deb)
            if 'rip + ' in x.op_str or 'rip - ' in x.op_str:
                try:
                    signe = 1 if 'rip + ' in x.op_str else -1
                    part = x.op_str.split('rip + ' if signe > 0 else 'rip - ')[1]
                    c = x.address + x.size + signe * int(part.rstrip(']'), 16)
                except Exception:
                    c = None
                if c is not None:
                    if c in GLOBAUX:
                        globaux.append(GLOBAUX[c])
                    s = cstr(c)
                    if s:
                        chaines.append(s)
            for part in x.op_str.split(', '):
                try:
                    v = int(part, 0)
                except ValueError:
                    continue
                if v in SCENES:
                    scenes.append('0x%X=%s' % (v, SCENES[v]))
                elif v in NOTABLES and x.mnemonic in ('cmp', 'mov'):
                    notables.append('%s %s' % (x.mnemonic, NOTABLES[v]))
        bouchon = (fin - deb) <= 16 and len(ins) <= 3 and ins and ins[-1].mnemonic == 'ret'
        if lo <= deb < hi:
            infos[deb] = dict(fin=fin, taille=fin - deb, appels=appels,
                              chaines=list(dict.fromkeys(chaines)),
                              globaux=list(dict.fromkeys(globaux)),
                              notables=list(dict.fromkeys(notables)),
                              scenes=list(dict.fromkeys(scenes)),
                              bouchon=bouchon, n_ins=len(ins))

    sortie = os.path.join(RACINE, 'analysis', 'carte_%s.md' % nom)
    with open(sortie, 'w', encoding='utf-8') as fp:
        fp.write('# Carte de la zone 0x%X - 0x%X (%s)\n\n' % (lo, hi, nom))
        fp.write('%d fonctions, %d octets de code.\n\n'
                 % (len(infos), sum(v['taille'] for v in infos.values())))
        fp.write('Genere par `tools/carte_zone.py`. Pour chaque fonction : sa '
                 'taille, ses appelants **internes a la zone**, les chaines '
                 'qu\'elle nomme, les globaux connus qu\'elle lit, et les '
                 'immediats remarquables.\n\n')
        for deb in sorted(infos):
            v = infos[deb]
            fp.write('## 0x%X  (%d octets, %d instructions)%s\n'
                     % (deb, v['taille'], v['n_ins'],
                        '  **BOUCHON**' if v['bouchon'] else ''))
            ap = sorted(appelants.get(deb, ()))
            fp.write('- appelee par : %s\n'
                     % (', '.join('0x%X' % a for a in ap) if ap
                        else '_aucun appelant direct (vtable ?)_'))
            internes = sorted(set(c for c in v['appels'] if lo <= c < hi))
            if internes:
                fp.write('- appelle (dans la zone) : %s\n'
                         % ', '.join('0x%X' % c for c in internes))
            bouch = sorted(set(c for c in v['appels'] if c in BOUCHONS))
            if bouch:
                fp.write('- **appelle des bouchons** : %s\n'
                         % ', '.join('0x%X' % c for c in bouch))
            if v['chaines']:
                fp.write('- chaines : %s\n'
                         % ', '.join('`%s`' % s for s in v['chaines'][:12]))
            if v['globaux']:
                fp.write('- globaux : %s\n' % ', '.join(v['globaux']))
            if v['scenes']:
                fp.write('- **scenes** : %s\n' % ', '.join(v['scenes']))
            if v['notables']:
                fp.write('- immediats : %s\n' % ', '.join(v['notables']))
            fp.write('\n')
    print('%s : %d fonctions, %d octets'
          % (sortie, len(infos), sum(v['taille'] for v in infos.values())))
    # resume a l ecran : ce qui nomme
    print()
    print('--- fonctions qui referencent une scene du selecteur ---')
    for deb in sorted(infos):
        if infos[deb]['scenes']:
            print('  0x%X : %s' % (deb, ', '.join(infos[deb]['scenes'])))
    print()
    print('--- fonctions nommees par une chaine ---')
    for deb in sorted(infos):
        ch = [s for s in infos[deb]['chaines'] if s.isupper() or '_' in s]
        if ch:
            print('  0x%X : %s' % (deb, ', '.join('`%s`' % s for s in ch[:5])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
