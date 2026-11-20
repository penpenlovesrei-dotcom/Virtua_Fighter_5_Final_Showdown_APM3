#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pourquoi le menu console reste vide : lire la garde, plutot que la deviner.

Le mode console est atteint (`game_mode = 0` dans le `vf5fs_game_config_t`), le
parcours d'etats est celui de la PS3 -- CS_TITLE, CS_SIGNIN, WARNING,
CS_AUTOLOAD, puis l'etat MENU -- et le cadre du menu est bel et bien dessine.
Seules les ENTREES manquent.

La fonction qui dessine le menu est autour de `0x1801E0DA8`. Elle pose trois
scenes AET :

    0x1801E0DC4   "p_main_head_lt"    l'en-tete       objet [rsi+0x240]
    0x1801E0E7B   "p_menutxt_PS3_lt"  le texte        objet [rsi+0x298]
    0x1801E0E9B   "p_menutxt_02_rb"   le texte        objet [rsi+0x298]

et chaque bloc est garde par le meme predicat minuscule :

    0x1801BDA10   cmp dword ptr [rcx], 3 ; sete al ; ret

Autrement dit : **l'objet AET doit etre a l'etat 3**. Si le texte ne s'affiche
pas, c'est que `[rsi+0x298]` ne vaut pas 3 -- et la valeur qu'il porte dit a
quel stade le chargement s'arrete. Ce script la lit, au lieu de la supposer.

    py -3 tools/pister_menu.py                    observe les deux etats
    py -3 tools/pister_menu.py --forcer           rend la garde vraie
"""
import collections
import os
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
# RVA, base d'image 0x180000000
GARDE_TEXTE = 0x1E0E5F        # lea rcx, [rsi+0x298]   -- rsi encore vivant
APRES_GARDE = 0x1E0E6B        # test al, al            -- juste apres l'appel
CTX_GLOBAL = 0x752148                 # RVA du pointeur de contexte global
                                      # (VA 0x180752148, base d'image 0x180000000)
TETE_COURANTE = 0x70C4F0  # la tete courante, lue par 0x1800DA618
TETE_PHASE    = 0x70C4FC  # sa phase
SS_COURANT = 0x70C50C     # le sous-etat courant, lu par 0x1800DA701
SS_PHASE   = 0x70C518     # sa phase : 0 = entree, 1 = milieu, 2 = sortie
SET_STATE = 0x0DA800      # le changement d etat, comme dans tracer_etats
PAD_LECTEUR = 0x2440F4   # dans 0x180243ED0, rsi et rdi vivants
PAD_BASE = 0x4FD0                     # les trois structures de 0x44 octets
PAD_TAILLE = 0xCC                     # 0x4FD0, 0x5014, 0x5058
OBJ_ENTETE = 0x240            # "p_main_head_lt"
OBJ_TEXTE = 0x298             # "p_menutxt_PS3_lt" et "p_menutxt_02_rb"
# Le constructeur 0x1801DA550 ecrit jusqu'a +0x2A00 au moins ; on prend large.
OBJ_TAILLE = 0x2B00
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')

# L'etat d'un objet AET, tel que le predicat le lit. 3 = pret a etre pose ;
# les autres valeurs sont a nommer, et c'est justement l'objet de la mesure.
ETATS = {0: 'vide / jamais charge', 1: '?', 2: '?', 3: 'PRET'}


def nom_etat(v):
    if v is None:
        return 'illisible'
    return '%d (%s)' % (v, ETATS.get(v, '?'))


def depl_export(chemin, nom):
    """La RVA d'un export, lue dans le fichier -- comme config_module.py."""
    import pefile
    pe = pefile.PE(chemin, fast_load=True)
    pe.parse_data_directories(
        [pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT']])
    for e in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if e.name and e.name.decode() == nom:
            return e.address
    return None


def main():
    argv = sys.argv[1:]
    secondes, pose_a = 60, 12.0
    forcer = '--forcer' in argv
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'console_start.txt')
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--a' in argv:
        pose_a = float(argv[argv.index('--a') + 1])
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]
    captures = []
    if '--captures' in argv:
        for spec in argv[argv.index('--captures') + 1].split(','):
            t, chemin = spec.split(':', 1)
            captures.append((os.path.join(RACINE, 'analysis', chemin),
                             float(t), 'Virtua Fighter'))

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 200000
    journal = os.path.join(RACINE, 'analysis', 'pister_menu.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    manettes = '--manettes' in argv
    objet = '--objet' in argv
    sites = '--sites' in argv
    pad = '--pad' in argv
    devier = None
    tete = None
    sous_etat = None
    a_t = 30.0
    if '--sous-etat' in argv:
        sous_etat = int(argv[argv.index('--sous-etat') + 1], 0)
    tete_g = None
    if '--forcer-tete' in argv:
        tete_g = int(argv[argv.index('--forcer-tete') + 1], 0)
    if '--a-t' in argv:
        a_t = float(argv[argv.index('--a-t') + 1])
    if '--devier' in argv:
        i = argv.index('--devier')
        devier = (int(argv[i + 1], 0), int(argv[i + 2], 0))
    if '--tete' in argv:
        tete = int(argv[argv.index('--tete') + 1], 0)
    jalons = []
    if '--jalons' in argv:
        for spec in argv[argv.index('--jalons') + 1].split(','):
            nom_j, rva_j = spec.split(':')
            jalons.append(('jalon ' + nom_j, int(rva_j, 0)))
    fenetres = []
    if '--appuis' in argv:
        for spec in argv[argv.index('--appuis') + 1].split(','):
            a, b = spec.split('-')
            fenetres.append((float(a), float(b)))
    et = {'pose': False, 'vus': collections.Counter(), 'forces': 0,
          'n': 0, 'pads': {}, 'bouge': {}, 'avant': None,
          't0': time.time(), 'sites': collections.Counter(), 'pad': {},
          'jalons': collections.Counter(),
          'jalons_r8': collections.Counter()}

    def sur_bp(d, bp, ctx, tid):
        # --pad : lire l'etat de manette que le moteur vient de construire.
        # 0x180243ED0 est LE lecteur d'entrees : une boucle sur deux joueurs,
        # un enregistrement de 0x54 octets chacun, et les boutons lus pour le
        # seul joueur 0. Elle range :
        #     [rdi+0x08] tenu      [rdi+0x0C] tenu a la trame precedente
        #     [rdi+0x10] front montant       [rdi+0x14] relache
        #     [rdi+0x18] REPETITION, et c'est la que ca se joue :
        #        elle est masquee par [rsi+0xA8], retardee de [rsi+0xAC] et
        #        cadencee par [rsi+0xAD]. Masque nul = pas de repetition.
        # --jalons : simple comptage de passages sur des adresses donnees.
        # Sert ici a savoir si la mise a jour du menu prend une de ses deux
        # sorties anticipees vers 0x1801DCE33, auquel cas son corps -- et donc
        # sa navigation -- ne tourne jamais.
        # --devier A B [--tete T] : meme deviation que tracer_etats.py, mais
        # dans CET outil, pour pouvoir mesurer dans la meme passe ce que la
        # deviation produit. Deux mesures separees ne se comparent pas : le
        # jeu n'est pas deterministe d'une execution a l'autre.
        if bp.nom == 'SetState':
            if devier and (ctx.Rdx & 0xFFFFFFFF) == devier[0]:
                ctx.Rdx = devier[1]
                if tete is not None:
                    ctx.Rcx = tete
                ctx.ContextFlags = (instrument.CONTEXT_FULL
                                    | instrument.CONTEXT_DEBUG_REGISTERS)
                d.poser_contexte(tid, ctx)
                et['devie'] = et.get('devie', 0) + 1
            return
        if bp.nom.startswith('jalon'):
            et['jalons'][bp.nom] += 1
            # Un jalon dont le nom commence par "r8_" releve aussi r8 : sert a
            # lire le parametre que 0x1801D0800 passe a 0x1801D0B80, celui qui
            # vaut 2 sans Dural et 6 avec -- et dont le bit 2 fait passer la
            # grille de selection de 18 a 20 cases.
            if 'r8_' in bp.nom:
                et['jalons_r8'][(bp.nom, ctx.R8 & 0xFF, ctx.Rdx & 0xFF)] += 1
            return
        if bp.nom == 'Pad':
            rsi, rdi = ctx.Rsi, ctx.Rdi
            octets = d.read(rsi + 0xAC, 2) or b'\0\0'
            t = (d.u32(rsi + 0xA8), octets[0], octets[1],
                 d.u32(rdi + 0x08), d.u32(rdi + 0x10), d.u32(rdi + 0x18))
            et['pad'][t] = et['pad'].get(t, 0) + 1
            return
        # Qui, dans le MOTEUR, interroge les entrees ? Les troncs de vfes.exe
        # sont des `jmp`, donc l'adresse de retour empilee lors de l'appel au
        # stub designe directement le site du moteur.
        if bp.nom == 'InputIsOn':
            ret = d.u64(ctx.Rsp)
            if ret:
                nm, dp = d.module_of(ret)
                et['sites'][('%s+0x%X' % (nm, dp), ctx.Rcx & 0xFFFFFFFF)] += 1
            return
        if bp.nom == 'ApresGarde':
            if forcer:
                ctx.Rax = (ctx.Rax & ~0xFF) | 1
                ctx.ContextFlags = (instrument.CONTEXT_FULL
                                    | instrument.CONTEXT_DEBUG_REGISTERS)
                d.poser_contexte(tid, ctx)
                et['forces'] += 1
                if et['forces'] == 1:
                    d.dire('      >>> garde forcee a VRAI ; le bloc de texte '
                           'est desormais joue')
            return
        et['n'] += 1
        rsi = ctx.Rsi
        # Les trois structures de 0x44 octets que la mise a jour du menu
        # consulte 21 fois par trame, via les accesseurs 0x1801B89E0..8A30 :
        # ctx+0x4FD0, ctx+0x5014, ctx+0x5058. Si le menu ne se navigue pas,
        # la question est de savoir si elles bougent quand on appuie.
        if manettes and et['n'] % 5 == 0:
            base = d.u64(d.base_de(MOTEUR) + CTX_GLOBAL)
            if base:
                brut = d.read(base + PAD_BASE, PAD_TAILLE)
                if brut:
                    cle = brut.hex()
                    if cle not in et['pads']:
                        et['pads'][cle] = et['n']
        # --objet : ne rien presupposer. On echantillonne l'objet de page
        # entier et on note, mot par mot, QUAND il change. Il n'y a plus qu'a
        # regarder si les changements tombent dans les fenetres d'appui du
        # scenario. Rien qui bouge = l'entree n'atteint pas la page.
        if objet:
            brut = d.read(rsi, OBJ_TAILLE)
            if brut:
                avant = et.get('avant')
                if avant is not None and len(avant) == len(brut):
                    t = time.time() - et['t0']
                    for k in range(0, len(brut) - 3, 4):
                        if brut[k:k + 4] != avant[k:k + 4]:
                            et['bouge'].setdefault(k, []).append(t)
                et['avant'] = brut
        entete = d.u32(rsi + OBJ_ENTETE)
        texte = d.u32(rsi + OBJ_TEXTE)
        cle = (entete, texte)
        premier = cle not in et['vus']
        et['vus'][cle] += 1
        if premier:
            d.dire('  menu : objet 0x%X   en-tete = %s   texte = %s'
                   % (rsi, nom_etat(entete), nom_etat(texte)))

    def tic(d, t):
        # --sous-etat N --a-t T : ecrire directement les globaux du repartiteur
        # (analysis/machine_console.md). Devier `shift_next_mode` ne fait que
        # changer l'etiquette ; ici on pose le sous-etat ET sa phase a 0, ce qui
        # amene le repartiteur a appeler le gestionnaire d'ENTREE du sous-etat,
        # c'est-a-dire celui qui construit et arme la page.
        if sous_etat is not None and t >= a_t and not et.get('force_ss'):
            b = d.base_de(MOTEUR)
            if b:
                et['force_ss'] = True
                if tete_g is not None:
                    d.write(b + TETE_COURANTE,
                            int(tete_g).to_bytes(4, 'little'))
                    d.write(b + TETE_PHASE, (0).to_bytes(4, 'little'))
                d.write(b + SS_COURANT, int(sous_etat).to_bytes(4, 'little'))
                d.write(b + SS_PHASE, (0).to_bytes(4, 'little'))
                d.dire('  >>> sous-etat force a %d, phase 0, a t=%.1f s'
                       % (sous_etat, t))
        if et['pose'] or t < pose_a:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        liste = [('GardeTexte', b + GARDE_TEXTE)]
        if forcer:
            liste.append(('ApresGarde', b + APRES_GARDE))
        if pad:
            liste.append(('Pad', b + PAD_LECTEUR))
        if devier:
            liste.append(('SetState', b + SET_STATE))
        for nom_j, rva_j in jalons:
            liste.append((nom_j, b + rva_j))
        if sites:
            base_apm = d.base_de('apm.dll')
            rva = depl_export(os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                                           'apm.dll'), 'Input_isOn')
            if base_apm and rva:
                liste.append(('InputIsOn', base_apm + rva))
            else:
                d.dire('  Input_isOn du stub introuvable (base=%s rva=%s)'
                       % (base_apm, rva))
        for n, adr in liste:
            bp = instrument.PointArret(n, adr, max_coups=400000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  points d\'arret poses a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    if scenario and os.path.exists(scenario):
        with open(scenario, 'rb') as fp:
            data = fp.read()
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(data)
    print('journal : %s%s' % (journal, '   (garde forcee)' if forcer else ''))
    dbg.run(EXE, os.path.dirname(EXE), secondes, tuple(captures))
    fichier.close()

    # Le stub journalise chaque appel d'entree via OutputDebugString ; le
    # debogueur les collecte dans `debug_strings` mais ne les ecrit qu'en mode
    # bavard. On les depouille ici : quels codes le jeu interroge, et lesquels
    # il a vus tenus. Demande " journal = 1 " dans le scenario.
    entrees = collections.Counter()
    ouis = collections.Counter()
    for ligne in getattr(dbg, 'debug_strings', ()):
        if not ligne.startswith('[apm] Input_is'):
            continue
        corps = ligne[len('[apm] '):]
        fn, reste = corps.split('(', 1)
        code = reste.split(')', 1)[0]
        entrees[(fn, code)] += 1
        if '= OUI' in ligne:
            ouis[(fn, code)] += 1
    if entrees:
        print('\n--- codes d entree interroges pendant la passe ---')
        print('  (les directions 2 a 5 sont une hypothese de disposition,')
        print('   jamais identifiee : voir tools/scenarios/jouer.txt)')
        for (fn, code), n in sorted(entrees.items(),
                                    key=lambda kv: (kv[0][0], int(kv[0][1]))):
            oui = ouis.get((fn, code), 0)
            print('  %-16s code %-3s  %7d appels   %s'
                  % (fn, code, n,
                     ('%d fois VRAI' % oui) if oui else 'jamais vrai'))
    if jalons:
        print('\n--- passages sur les jalons ---')
        for nom_j, rva_j in jalons:
            print('  %-24s RVA 0x%-9X %8d passage(s)'
                  % (nom_j, rva_j, et['jalons'][nom_j]))
    if pad:
        print('\n--- etat de manette construit par 0x180243ED0 ---')
        print('  masque repetition / delai / periode  |  tenu     front    repet')
        for (m, de, pe, tenu, front, rep), n in sorted(
                et['pad'].items(), key=lambda kv: -kv[1])[:14]:
            print('  0x%08X  %3d  %3d              |  %08X %08X %08X   (%d x)'
                  % (m, de, pe, tenu, front, rep, n))
        masques = set(k[0] for k in et['pad'])
        if masques == {0}:
            print('  Le masque de repetition est NUL : [rdi+0x18] ne peut jamais')
            print('  valoir autre chose que zero. Aucune repetition de curseur.')
    if sites:
        print('\n--- qui interroge les entrees, vu depuis le stub ---')
        par_site = collections.Counter()
        for (site, code), n in et['sites'].items():
            par_site[site] += n
        if not par_site:
            print('  aucun appel releve.')
        for site, n in par_site.most_common(12):
            codes = sorted(c for (s2, c) in et['sites'] if s2 == site)
            print('  %8d appels   %-30s  codes %s'
                  % (n, site, ' '.join(str(c) for c in codes)))
    if objet:
        print('\n--- ce qui bouge dans l objet de page (0x%X octets) ---'
              % OBJ_TAILLE)
        print('  %d mot(s) de 4 octets ont change au moins une fois'
              % len(et['bouge']))
        if fenetres:
            print('  fenetres d appui declarees : %s'
                  % ', '.join('%.1f-%.1f s' % f for f in fenetres))

            def dedans(t):
                return any(a <= t <= b for a, b in fenetres)

            candidats = []
            for k, ts in et['bouge'].items():
                n_dans = sum(1 for t in ts if dedans(t))
                if n_dans and n_dans == len(ts):
                    candidats.append((n_dans, k, ts))
            candidats.sort(reverse=True)
            print('  %d mot(s) ne changent QUE pendant les appuis :'
                  % len(candidats))
            for n_dans, k, ts in candidats[:20]:
                print('    +0x%04X   %d changement(s) a %s'
                      % (k, n_dans, ', '.join('%.1f' % t for t in ts[:8])))
            if not candidats:
                print('    aucun. L entree n atteint pas cet objet.')
        else:
            for k, ts in sorted(et['bouge'].items(),
                                key=lambda kv: -len(kv[1]))[:20]:
                print('    +0x%04X   %d changement(s)' % (k, len(ts)))
    if manettes:
        print('\n--- etat de manette lu par le menu (ctx+0x4FD0 .. +0x509B) ---')
        print('  %d valeur(s) distincte(s) sur la passe' % len(et['pads']))
        for cle, n in list(et['pads'].items())[:8]:
            brut = bytes.fromhex(cle)
            nonnuls = [(k, brut[k]) for k in range(len(brut)) if brut[k]]
            print('    trame %-6d  %s'
                  % (n, ' '.join('+0x%X=%02X' % t for t in nonnuls[:18])
                     or '(tout a zero)'))
        if len(et['pads']) <= 1:
            print('  UNE SEULE valeur : ces structures ne bougent pas quand on')
            print('  appuie. Le menu lit donc un etat de manette que rien ne')
            print('  remplit dans ce build.')
    print('\n--- etats vus a la garde du menu ---')
    if not et['vus']:
        print('  AUCUN passage : la fonction de dessin du menu n a pas ete')
        print('  atteinte. Ce n est donc pas la garde qui bloque.')
    for (entete, texte), n in et['vus'].most_common(20):
        print('  %8d x  en-tete = %-24s texte = %s'
              % (n, nom_etat(entete), nom_etat(texte)))
    if forcer:
        print('\ngardes forcees : %d' % et['forces'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
