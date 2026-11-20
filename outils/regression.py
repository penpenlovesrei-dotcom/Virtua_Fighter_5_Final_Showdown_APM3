#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""LE FILET : on peut toucher au patcheur sans rien defaire.

Trois etages, du plus rapide au plus lent :

  1. `verifier_lanceurs.py --sans-patch` : fins de ligne, caracteres de
     controle, fichiers cites. C'est le controle qui a ete ecrit apres
     « tu as casse la plupart des cmd hier soir ».
  2. `controle_quest.py --tout` : compile, patche avec la ligne exacte de
     `quest.cmd`, puis mesure dans le binaire produit.
  3. L'EMPREINTE. On compare la DLL produite a celle du dernier etat
     valide -- **correctif par correctif**, pas seulement en gros : pour
     chaque plage d'octets qui differe du `.origine`, on dit quel correctif
     la revendique. Une plage qui apparait, disparait ou change de taille
     est signalee par son adresse.

Pourquoi « correctif par correctif » : la seance du 2026-09-06 a ete perdue
parce que la legende du bas et License Challenge logeaient leur caverne a la
MEME adresse (`0x1801A71D8`), et que la legende ecrasait le lancement. Une
empreinte globale aurait dit « ca a change » ; celle-ci dit OU.

    py -3 tools/regression.py               tout controler
    py -3 tools/regression.py --poser       prendre l'etat actuel pour
                                            reference (a faire APRES que
                                            Frederic a valide a l'ecran)
    py -3 tools/regression.py --rapide      sauter le rebuild (etage 2
                                            en mesure seule)

Reference : `analysis/empreinte_quest.json`. Rapport :
`analysis/regression.txt`. Code de sortie non nul au premier defaut.
"""
import hashlib
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
DLL = os.path.join(JEU, 'vf5fs-pxd-w64-Retail_APM3.dll')
ORIGINE = DLL + '.origine'
REFERENCE = os.path.join(RACINE, 'analysis', 'empreinte_quest.json')
RAPPORT = os.path.join(RACINE, 'analysis', 'regression.txt')
# Deux plages d'octets separees par moins de ceci comptent pour une seule
# modification : un correctif de cinq octets suivi de deux `nop` ne doit pas
# se compter pour deux.
COLLE = 16


def sha(chemin):
    h = hashlib.sha256()
    with open(chemin, 'rb') as fp:
        for bloc in iter(lambda: fp.read(1 << 20), b''):
            h.update(bloc)
    return h.hexdigest()


def plages():
    """Les plages d'octets ou la DLL patchee differe du `.origine`.

    Rend une liste de (offset, longueur, sha court, VA si connue). La
    section greffee n'existe pas dans le `.origine` : elle est traitee a
    part, comme UNE plage nommee.
    """
    import pe_disasm as P
    a = open(ORIGINE, 'rb').read()
    b = open(DLL, 'rb').read()
    img = P.Image(DLL)
    n = min(len(a), len(b))
    out, deb = [], None
    i = 0
    while i < n:
        if a[i] != b[i]:
            if deb is None:
                deb = i
            fin = i
            j = i + 1
            while j < n and j - fin <= COLLE:
                if a[j] != b[j]:
                    fin = j
                j += 1
            i = fin + 1
            out.append((deb, fin - deb + 1))
            deb = None
        else:
            i += 1
    res = []
    for off, lg in out:
        va = img.off2va(off)
        res.append({'offset': off, 'longueur': lg,
                    'va': ('0x%X' % va) if va else None,
                    'sha': hashlib.sha256(b[off:off + lg]).hexdigest()[:16]})
    if len(b) > len(a):
        res.append({'offset': len(a), 'longueur': len(b) - len(a),
                    'va': '.greffe (section ajoutee)',
                    'sha': hashlib.sha256(b[len(a):]).hexdigest()[:16]})
    return res


def revendiquer(res):
    """Quel correctif revendique chaque plage ? Par son adresse, pas par foi."""
    import patch_moteur as PM
    connus = {}

    def poser(va, quoi):
        connus.setdefault(va, []).append(quoi)

    poser(PM.QUEST_SITE_APPEL, 'quest : SCOREBOARDS')
    poser(PM.QUEST_MODE_REC + 0x10, 'quest : mode DATA_TEST')
    poser(PM.QUEST_MODE_REC + 0x60, 'quest : mode de retour')
    poser(PM.QUEST_SOUS_REC + 0x10, 'quest : sous-etat 35, milieu')
    poser(PM.QUEST_SOUS_REC + 0x18, 'quest : sous-etat 35, sortie')
    poser(PM.QUEST_AETMGR_SLOT, 'quest : creneau 4 d AetMgr')
    for va, _, code, quoi in PM.TERMINAL_BOUTONS:
        poser(va, 'terminal : %s (code %d)' % (quoi, code))
    poser(PM.SOUSMENU_GARDE, 'sous-menu / legende : la garde')
    poser(PM.SOUSMENU_RANKING[1], 'sous-menu : la page RANKING')
    poser(PM.JOUEUR2_SHL[1], 'joueur 2 : shl ebp, 4')
    for va, _, code in PM.JOUEUR2_CODES:
        poser(va, 'joueur 2 : code %d relatif' % code)
    for va, _ in PM.SORTIE_HOOKS:
        poser(va, 'transition : Echap quitte le mode')
    poser(PM.DOJO_HOOK, 'dojo : le relais')

    for p in res:
        p['revendique'] = []
        if not p['va'] or not p['va'].startswith('0x'):
            p['revendique'] = ['.greffe']
            continue
        v = int(p['va'], 16)
        for va, noms in connus.items():
            if v <= va < v + p['longueur'] or va <= v < va + 16:
                p['revendique'] += noms
    return res


def main():
    argv = sys.argv[1:]
    lignes = []

    def dire(t=''):
        print(t)
        lignes.append(t)

    def fin(code):
        os.makedirs(os.path.dirname(RAPPORT), exist_ok=True)
        with open(RAPPORT, 'w', encoding='utf-8') as fp:
            fp.write('\n'.join(lignes) + '\n')
        dire('')
        print('rapport : %s' % os.path.relpath(RAPPORT, RACINE))
        return code

    dire('REGRESSION -- le filet du patcheur')
    dire('=' * 74)
    dire()

    dire('1. LES LANCEURS')
    p = subprocess.run([sys.executable,
                        os.path.join('tools', 'verifier_lanceurs.py'),
                        '--sans-patch'], cwd=RACINE, capture_output=True,
                       text=True, errors='replace')
    for l in (p.stdout + p.stderr).splitlines():
        dire('   | %s' % l)
    if 'A REPARER' in p.stdout:
        dire('   DEFAUT : au moins un lanceur est a reparer.')
        return fin(1)
    dire('   OK')
    dire()

    dire('2. LE CONTROLE DU QUEST')
    a2 = ['--tout'] if '--rapide' not in argv else []
    p = subprocess.run([sys.executable,
                        os.path.join('tools', 'controle_quest.py')] + a2,
                       cwd=RACINE, capture_output=True, text=True,
                       errors='replace')
    for l in (p.stdout + p.stderr).splitlines():
        if l.strip().startswith(('OK', 'DEFAUT', 'A VOIR', 'ARRET')):
            dire('   | %s' % l.strip())
    if p.returncode:
        dire('   DEFAUT : controle_quest a rendu %d.' % p.returncode)
        return fin(1)
    dire('   OK')
    dire()

    dire('3. L EMPREINTE, CORRECTIF PAR CORRECTIF')
    res = revendiquer(plages())
    courant = {'sha_dll': sha(DLL), 'sha_origine': sha(ORIGINE),
               'plages': res}
    dire('   %d plage(s) modifiee(s) par rapport au .origine.' % len(res))
    orphelines = [p for p in res if not p['revendique']]
    if orphelines:
        dire('   %d plage(s) que AUCUN correctif connu ne revendique :'
             % len(orphelines))
        for p in orphelines[:40]:
            dire('     %-14s %5d o  %s'
                 % (p['va'] or '?', p['longueur'], p['sha']))
        dire('   (ce n est pas forcement un defaut : la table des correctifs')
        dire('    connus de regression.py est volontairement partielle.)')

    if '--poser' in argv:
        # `--valide` n'est a mettre que quand Frederic a dit qu'il l'a VU
        # marcher. Sans lui, la reference sert quand meme -- elle detecte
        # qu'un correctif a disparu -- mais elle ne certifie rien.
        courant['valide_a_l_ecran'] = '--valide' in argv
        courant['note'] = (sys.argv[sys.argv.index('--note') + 1]
                           if '--note' in sys.argv else '')
        with open(REFERENCE, 'w', encoding='utf-8') as fp:
            json.dump(courant, fp, indent=1, sort_keys=True)
        dire('   valide a l ecran : %s'
             % ('OUI' if courant['valide_a_l_ecran'] else
                'NON -- reference de travail, elle ne certifie rien'))
        dire('   REFERENCE POSEE : %s' % os.path.relpath(REFERENCE, RACINE))
        dire('   (a ne faire qu APRES une validation a l ecran)')
        return fin(0)

    if not os.path.exists(REFERENCE):
        dire('   Aucune reference. Posez-la avec --poser, une fois que')
        dire('   Frederic a valide l etat a l ecran.')
        return fin(0)

    with open(REFERENCE, encoding='utf-8') as fp:
        ref = json.load(fp)
    dire('   reference du %s : %s%s'
         % (REFERENCE and 'depot',
            'VALIDEE A L ECRAN' if ref.get('valide_a_l_ecran')
            else 'de travail (jamais vue a l ecran)',
            (' -- %s' % ref['note']) if ref.get('note') else ''))
    if ref['sha_origine'] != courant['sha_origine']:
        dire('   DEFAUT : le .origine a change depuis la reference.')
        return fin(1)
    if ref['sha_dll'] == courant['sha_dll']:
        dire('   La DLL est OCTET POUR OCTET celle de la reference.')
        return fin(0)

    avant = {p['va']: p for p in ref['plages']}
    apres = {p['va']: p for p in res}
    perdus = [v for v in avant if v not in apres]
    neufs = [v for v in apres if v not in avant]
    changes = [v for v in avant if v in apres
               and avant[v]['sha'] != apres[v]['sha']]
    for titre, liste in (('DISPARUES (un correctif ne s applique plus)',
                          perdus),
                         ('NOUVELLES', neufs),
                         ('MODIFIEES', changes)):
        if not liste:
            continue
        dire('   %s : %d' % (titre, len(liste)))
        for v in sorted(liste, key=str)[:40]:
            p = apres.get(v) or avant[v]
            dire('     %-14s %5d o   %s'
                 % (v, p['longueur'],
                    ', '.join(p.get('revendique') or ['-'])))
    if perdus:
        dire('   DEFAUT : un correctif valide a disparu.')
        return fin(1)
    dire('   La DLL differe de la reference, mais aucun correctif n a '
         'disparu.')
    dire('   Relisez les plages ci-dessus, puis --poser si c est voulu.')
    return fin(0)


if __name__ == '__main__':
    sys.exit(main())
