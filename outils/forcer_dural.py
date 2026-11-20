#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Force Dural a la place du personnage choisi, au moment du chargement.

Le chemin est etabli statiquement :

    0x180151F5E  mov rax, [rdi+0x60]      ; l'objet joueur 1 (le ROB)
    0x180151F62  mov ecx, [rax+0x10]      ; <-- l'indice de personnage
    0x180151F65  call 0x18012CA90         ; CodeDuPersonnage(indice) -> "LIO"
    0x180151F6D  lea r8, "mot_%s.bin"     ; le nom de fichier est bati avec

`CodeDuPersonnage` borne son argument par `cmp ecx, 0x15` -- donc **0 a 20**, et
la table de 21 entrees qu'elle indexe porte en 20 le code `DUR` et le nom
`DURAL`. L'indice de Dural est dans les clous de l'accesseur.

Il suffit donc d'ecrire 20 dans `joueur+0x10` juste avant que le chargeur le
lise. Ce n'est pas un point d'arret en ecriture (essaye : zero acces, le champ
est ecrit a la construction du ROB, avant que son adresse existe) mais une
substitution a la lecture, exactement comme la deviation de sous-etat qui a
ouvert le mode DOJO.

Usage :
    py -3 tools/forcer_dural.py                 force le joueur 1
    py -3 tools/forcer_dural.py --joueur 2
    py -3 tools/forcer_dural.py --perso 18      un temoin : Taka-Arashi
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
CHARGE_J1 = 0x151F5E          # mov rax,[rdi+0x60] ; mov ecx,[rax+0x10]
CHARGE_J2 = 0x152127          # idem, [rdi+0x68] pour le joueur 2
CODE_PERSO = 0x12CA90         # CodeDuPersonnage(ecx) ; borne cmp ecx,0x15
MOTH_APPLY_RECORD = 0x158B40
DECALAGE = {1: 0x60, 2: 0x68}
DUR = 20
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')
PERSOS = ['AKI', 'SAR', 'LAU', 'SHU', 'JEF', 'PAI', 'JAK', 'KAG', 'LIO', 'WOL',
          'AOI', 'LEI', 'VAN', 'BRA', 'GOH', 'MON', 'MSK', 'KRT', 'TAK', 'TE2', 'DUR']


def nom(c):
    return PERSOS[c] if c is not None and 0 <= c < len(PERSOS) else '?%s' % c


def main():
    argv = sys.argv[1:]
    joueur = 1
    perso = DUR
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'select_a.txt')
    secondes, pose_a = 150, 20.0
    if '--joueur' in argv:
        joueur = int(argv[argv.index('--joueur') + 1])
    if '--perso' in argv:
        perso = int(argv[argv.index('--perso') + 1], 0)
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    captures = []
    if '--captures' in argv:
        for spec in argv[argv.index('--captures') + 1].split(','):
            t, chemin = spec.split(':', 1)
            captures.append((os.path.join(RACINE, 'analysis', chemin),
                             float(t), 'Virtua Fighter'))

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 200
    journal = os.path.join(RACINE, 'analysis', 'forcer_dural.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'faits': 0, 'robs': []}

    def sur_bp(d, bp, ctx, tid):
        if bp.nom == 'chargement':
            p = d.u64(ctx.Rdi + DECALAGE[joueur])
            if not p:
                return
            avant = d.u32(p + 0x10)
            if avant == perso:
                return
            d.write(p + 0x10, perso.to_bytes(4, 'little'))
            apres = d.u32(p + 0x10)
            et['faits'] += 1
            d.dire('  joueur %d : personnage %s (%s) -> %s (%s)   [objet 0x%X]'
                   % (joueur, avant, nom(avant), apres, nom(apres), p))
            return
        if bp.nom == 'MothApplyRecord':
            rob = ctx.Rdx
            if rob and rob not in et['robs']:
                et['robs'].append(rob)
                c = d.u32(rob + 0x10)
                d.dire('  en combat : ROB %d = 0x%X   personnage %s (%s)'
                       % (len(et['robs']), rob, c, nom(c)))
            if len(et['robs']) >= 2:
                d.desarmer_logiciel(bp)

    def tic(d, t):
        if et['pose']:
            return
        b = d.base_de(MOTEUR)
        if not b or t < pose_a:
            return
        et['pose'] = True
        for n, rva, maxi in (('chargement', CHARGE_J1 if joueur == 1 else CHARGE_J2, 200),
                             ('MothApplyRecord', MOTH_APPLY_RECORD, 60)):
            bp = instrument.PointArret(n, b + rva, max_coups=maxi)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  points d\'arret poses a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    with open(scenario, 'rb') as fp:
        data = fp.read()
    with open(SCENARIO_ACTIF, 'wb') as fp:
        fp.write(data)
    print('scenario %s ; joueur %d force vers %d (%s)'
          % (os.path.basename(scenario), joueur, perso, nom(perso)))
    dbg.run(EXE, os.path.dirname(EXE), secondes, tuple(captures))
    fichier.close()
    with open(journal, encoding='utf-8') as fp:
        for ligne in fp:
            if ligne.startswith('  ') or 'EXCEPTION' in ligne:
                sys.stdout.write(ligne)
    print('\nsubstitutions : %d' % et['faits'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
