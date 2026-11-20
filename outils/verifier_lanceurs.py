#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Controle avant vol de TOUS les lanceurs .cmd, sans lancer le jeu.

Ecrit le 2026-09-09 apres que Frederic a dit : « tu as casse la plupart des cmd
hier soir ». Il avait raison sur au moins un point -- j'avais reecrit
`variantes_texte.cmd` en fins de ligne UNIX, et `cmd.exe` casse dessus sans
rien dire. Un lanceur ne doit pas pouvoir se casser en silence.

Trois controles, tous mecaniques :

  1. FINS DE LIGNE. Un `.cmd` en LF seul rend les blocs `if ( ... )` et la
     continuation `^` illisibles par cmd.exe.
  2. LA LIGNE DE PATCH. On extrait l'appel a `patch_moteur.py` (continuations
     `^` comprises) et on l'execute vraiment : c'est le seul moyen de savoir
     qu'aucune option n'a ete refusee ou renommee.
  3. LES FICHIERS CITES. Tout `tools\xxx.py`, `tools\xxx.cmd` ou chemin cite
     dans le lanceur doit exister.

    py -3 tools/verifier_lanceurs.py
    py -3 tools/verifier_lanceurs.py --sans-patch     (rapide, sans rebuild)
"""
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)


def lire(p):
    return open(p, 'rb').read()


def ligne_de_patch(texte):
    """Rend la ligne `patch_moteur.py ...`, continuations `^` recollees."""
    lignes = texte.split('\r\n')
    for i, l in enumerate(lignes):
        # Un `rem` peut CITER patch_moteur.py -- console.cmd le fait ligne 28,
        # et prendre la premiere occurrence donnait un faux ECHEC.
        if 'patch_moteur.py' not in l or l.lstrip().lower().startswith('rem'):
            continue
        bloc = l
        j = i
        while bloc.rstrip().endswith('^'):
            j += 1
            bloc = bloc.rstrip()[:-1] + ' ' + lignes[j]
        return bloc
    return None


def main():
    argv = sys.argv[1:]
    avec_patch = '--sans-patch' not in argv
    noms = sorted(f for f in os.listdir(ICI) if f.endswith('.cmd'))
    defauts = []

    print('=' * 74)
    print('CONTROLE DES %d LANCEURS' % len(noms))
    print('=' * 74)

    # --- 0. caracteres de controle parasites --------------------------------
    # Un `.cmd` ne contient que de l'imprimable, plus CR, LF et la tabulation.
    # Tout le reste est le signe d'un antislash mange en chemin : `\v`, `\b`,
    # `\f`, `\a` sortent d'un `\vf5fs`, d'un `\bin`, d'un `\fichier`...
    # Le lanceur reste syntaxiquement valide et `cmd.exe` ne dit rien : il
    # cherche simplement un chemin qui n'existe pas, en silence.
    # LE CR ISOLE EST LE PLUS SOURNOIS, et ce controle l'a laisse passer.
    #
    # Mesure du 2026-09-27 : `quest.cmd` portait `py -3 tools<CR>ivaux.py`
    # -- une echappee de mon script Python devenue un RETOUR CHARIOT au lieu
    # d'un antislash. Le jeu n'est jamais parti (« toolsivaux.py »
    # introuvable), et CE CONTROLE A DIT « AUCUN DEFAUT » : l'octet 13
    # etait excuse sans regarder ce qui le suivait, et le controle 1 ne
    # compare que des NOMBRES -- un CR isole laisse count(CRLF) == count(LF),
    # il est donc invisible des deux cotes. Le controle 2 ne voyait rien non
    # plus : `tools<CR>ivaux.py` ne ressemble plus a un chemin.
    #
    # Un CR n'est legitime QUE devant un LF. On le verifie desormais.
    print('\n0. CARACTERES DE CONTROLE')
    sales = []
    for n in noms:
        d = lire(os.path.join(ICI, n))
        parasites = sorted({b for b in d if b < 0x20 and b not in (9, 10, 13)})
        seuls = [i for i in range(len(d))
                 if d[i] == 13 and (i + 1 >= len(d) or d[i + 1] != 10)]
        if parasites or seuls:
            sales.append((n, parasites, seuls))
    if sales:
        for n, par, seuls in sales:
            d = lire(os.path.join(ICI, n))
            if par:
                print('   ECHEC  %-24s octets %s'
                      % (n, ' '.join('0x%02X' % b for b in par)))
            for i in seuls[:3]:
                deb_l = d.rfind(b'\n', 0, i) + 1
                fin_l = d.find(b'\n', i)
                print('   ECHEC  %-24s CR ISOLE en %d : %r'
                      % (n, i, d[deb_l:fin_l if fin_l > 0 else len(d)]))
            print('          un antislash a ete mange -- reecrire le fichier '
                  'avec l outil Write, jamais par un heredoc bash ni par '
                  'une echappee Python')
            defauts.append(n)
    else:
        print('   aucun caractere de controle parasite, aucun CR isole.')

    # --- 1. fins de ligne ---------------------------------------------------
    print('\n1. FINS DE LIGNE')
    mauvais = []
    for n in noms:
        d = lire(os.path.join(ICI, n))
        if d.count(b'\r\n') != d.count(b'\n'):
            mauvais.append(n)
    if mauvais:
        for n in mauvais:
            print('   CASSE  %s  -- fins de ligne UNIX' % n)
        defauts += mauvais
    else:
        print('   les %d sont en CRLF.' % len(noms))

    # --- 2. fichiers cites --------------------------------------------------
    print('\n2. FICHIERS CITES')
    manquants = []
    motif = re.compile(r'tools\\([A-Za-z0-9_]+\.(?:py|cmd))')
    for n in noms:
        t = lire(os.path.join(ICI, n)).decode('latin-1')
        for m in set(motif.findall(t)):
            if not os.path.exists(os.path.join(ICI, m)):
                manquants.append((n, m))
    if manquants:
        for n, m in manquants:
            print('   ABSENT %s  cite tools\\%s' % (n, m))
        defauts += [n for n, _ in manquants]
    else:
        print('   tous les tools\\*.py et tools\\*.cmd cites existent.')

    # --- 3. la ligne de patch s'execute-t-elle ? ----------------------------
    print('\n3. LIGNE DE PATCH')
    # LE JEU TOURNE ? Alors il TIENT la DLL, et aucun patch ne peut aboutir.
    # Ce n'est pas un defaut des lanceurs : c'est une PermissionError, et la
    # signaler comme un defaut envoie chercher ce qui n'existe pas.
    jeu = False
    try:
        r = subprocess.run(['tasklist', '/fi', 'IMAGENAME eq vfes.exe'],
                           capture_output=True, text=True)
        jeu = 'vfes.exe' in (r.stdout or '')
    except Exception:
        pass
    if jeu and avec_patch:
        print('   VFES.EXE TOURNE : il tient la DLL, aucun patch ne peut')
        print('   aboutir. Ce controle-la est SAUTE -- ce n est pas un defaut')
        print('   des lanceurs. Fermez le jeu et relancez.')
        avec_patch = False
    if not avec_patch:
        print('   (saute)')
    else:
        for n in noms:
            t = lire(os.path.join(ICI, n)).decode('latin-1')
            bloc = ligne_de_patch(t)
            if bloc is None:
                continue
            if '%1' in bloc or '%~1' in bloc:
                bloc = bloc.replace('%1', 'trm').replace('%~1', 'trm')
            # LES VARIABLES RETARDEES DE CMD.EXE. Le lanceur ecrit
            # `--resolution !RL! !RH!`, et cmd les remplace a l execution ;
            # nous, nous les passions telles quelles, et `int('!RL!')`
            # levait. Le controle annoncait alors un ECHEC qui n existait
            # pas -- c est ce qu il a fait le 2026-10-12 sur item_porte.cmd.
            bloc = bloc.replace('!RL!', '1920').replace('!RH!', '1080')
            bloc = re.sub(r'>>\s*"[^"]*"\s*2>&1', '', bloc)
            bloc = re.sub(r'\s(?:1)?>+\s*(?:nul|NUL)\b', ' ', bloc)
            args = bloc.strip().split()
            if args[:2] == ['py', '-3']:
                args = args[2:]
            args = [sys.executable, os.path.join(ICI, os.path.basename(args[0]))] \
                + args[1:]
            r = subprocess.run(args, cwd=RACINE, capture_output=True, text=True,
                               errors='replace')
            sortie = (r.stdout or '') + (r.stderr or '')
            refus = [l for l in sortie.splitlines()
                     if 'REFUS' in l or 'Traceback' in l or 'attend' in l]
            if r.returncode:
                print('   ECHEC  %-24s code %d' % (n, r.returncode))
                for l in refus[:2]:
                    print('          %s' % l[:110])
                defauts.append(n)
            else:
                print('   ok     %-24s' % n)

    print('\n' + '=' * 74)
    if defauts:
        print('%d LANCEUR(S) A REPARER : %s'
              % (len(set(defauts)), ' '.join(sorted(set(defauts)))))
    else:
        print('AUCUN DEFAUT.')
    print('=' * 74)
    return 1 if defauts else 0


if __name__ == '__main__':
    sys.exit(main())
