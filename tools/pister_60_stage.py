#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""QUI DEMANDE le decor -- `TaskStage+0x60`, et non `+0x5C`.

POURQUOI CETTE SONDE REMPLACE `pister_5c_stage.py`

La sonde du 2026-09-09 surveillait `TaskStage+0x5C`. Son journal n'a rendu que
cinq ecritures venues de `ntdll+0x60B82`, valeur `FEEEFEEE` : le remplissage de
tas d'un bloc LIBERE. Deux defauts, tous les deux mesurables et mesures :

1. **le champ etait le mauvais.** `+0x5C` n'est ecrit que par UNE instruction
   dans tout le binaire -- `0x18018EF8B`, dans le validateur `0x18018EF40` :

        0x18018EF44  movsxd rdx, [rcx+0x60]      ; la DEMANDE
        0x18018EF48  cmp edx, -1  ; je ...       ; rien a faire
        0x18018EF65  mov [rcx+0x58], 1           ; etat 1 : chargement
        0x18018EF6C  cmp edx, 0x29 ; jae ...     ; la borne des 41 decors
        0x18018EF71  imul r8, rdx, 0xF0 ...      ; le descripteur
        0x18018EF87  mov [rcx+0x68], r8
        0x18018EF8B  mov [rcx+0x5C], edx         <-- la RECOPIE
        0x18018EF8E  mov [rcx+0x60], -1          ; demande consommee

   Surveiller `+0x5C` ne pouvait donc nommer que cette recopie. **Le decideur
   est celui qui ecrit `+0x60`** ;

2. **l'objet n'etait pas suivi.** `TaskStage` est cree et DETRUIT en cours de
   partie : `0x18018EE30` publie le pointeur en `0x1807499D8`, `0x18018EEA0`
   detruit l'objet et remet le pointeur a zero. Un DR arme une fois sur
   `objet+0x5C` regarde donc un bloc rendu au tas -- ce que le journal disait,
   sans qu'on le lise.

   Un balayage lineaire compte **233** ecritures de 32 bits en `[reg+0x60]`
   dans `.text`. Les departager par la lecture est hors de portee : c'est
   exactement ce que le processeur, lui, sait faire.

CE QUE CETTE SONDE FAIT

  . DR sur le POINTEUR `0x1807499D8` (8 o, ecriture) : chaque creation et
    chaque destruction de la tache est vue, et les autres DR sont **rearmes**
    sur le nouvel objet ;
  . DR sur `tache+0x60` : la DEMANDE. Pour chaque ecriture, l'instruction, sa
    RVA, la valeur, et la CHAINE D'APPEL encore sur la pile ;
  . DR sur `tache+0x5C` : la recopie. Elle doit toujours venir de la RVA
    `0x18EF8E` -- si elle vient d'ailleurs, mon modele est faux, et je veux
    le savoir ;
  . QUATRE points d'arret logiciels le long de la chaine amont, lue le
    2026-09-10 : `0x18020AE60` (l'indice que le mode pose), `0x180203F2E`
    (l'ECRETAGE a 40 vers gym -- il dit la valeur qui arrive, la borne VIVANTE
    et le repli VIVANT, donc il reste juste quand on patche), `0x18018FCF0`
    (la demande) et `0x1800D7130` (le chargeur) ;
  . a chaque tic, une relecture des deux champs : si une valeur a change sans
    qu'un DR l'ait vue, la sonde le DIT au lieu de se taire.

Les valeurs sont toujours ecrites en clair ET nommees : `39 (gym)`. Le journal
de la veille affichait `tst` pour un champ a zero, ce qui se lisait comme un
resultat alors que c'etait un champ vide.

    py -3 tools/pister_60_stage.py
    py -3 tools/pister_60_stage.py --secondes 420
"""
import os
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                              # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
EXE = os.path.join(JEU, 'vfes.exe')
SCENARIO_ACTIF = os.path.join(JEU, 'apm_entrees.txt')
SCENARIO = """# ecrit par tools/pister_60_stage.py -- le clavier mene.
front   = 10
journal = 0
clavier = 1
manette = 1
0       rien
"""

TACHE_RVA = 0x7499D8           # le pointeur vers le singleton TaskStage
DEMANDE = 0x60                 # le decor DEMANDE  (-1 = rien a faire)
COURANT = 0x5C                 # le decor courant, recopie de la demande
CHARGEUR_RVA = 0x0D7130
RECOPIE_RVA = 0x18EF8E         # le rip attendu apres `mov [rcx+0x5C], edx`
CREATION_RVA = 0x18EE7F        # apres la publication du pointeur
DESTRUCTION = (0x18EE90, 0x18EEC5)  # apres une remise a zero

# LES TROIS MAILLONS EN AMONT, lus le 2026-09-10 (voir le commentaire de
# `--decor-ecretage` dans patch_moteur.py). Un point d'arret LOGICIEL sur
# chacun : ils passent une fois par combat, le jeu ne ralentit pas.
MODE_RVA = 0x20AE60            # mov [0x180754A58], r9d -- l'indice du mode
ECRETAGE_RVA = 0x203F2E        # cmova ebp, eax -- l'ecretage a 40 vers gym
ECRETAGE_IMM = 0x203F20        # l'octet de la borne, relu VIVANT
ECRETAGE_REPLI = 0x203F10      # l'immediat du repli, relu VIVANT
REQUETE_RVA = 0x18FCF0         # TaskStage::demander(ecx)
MODE_GLOBAL = 0x754A58         # l'indice de decor du mode

NOMS = ['tst', 'ts2', 'ts3', 'wht', 'ban', 'ter', 'nyc', 'cas', 'riv', 'jin',
        'sin', 'djo', 'umi', 'hai', 'are', 'slk', 'yuk', 'tak', 'aur', 'bar',
        'tan', 'du1', 'du2', 'du3', 'du4', 'du5', 'trm', 'cid', 'trs', 'evo00',
        'evo01', 'evo02', 'evo03', 'evo04', 'evo05', 'evo06', 'evo07', 'evo08',
        'evo09', 'gym', 'smo', 'ALEA(41)', 'ajoute-42', 'ajoute-43']

# Les remplissages de tas du CRT et de Windows. Les voir est un RESULTAT (le
# bloc a ete rendu), pas une ecriture du jeu.
TAS = (0xFEEEFEEE, 0xEEFEEEFE, 0xEEEEFEEE, 0xFEFEEEEE, 0xCDCDCDCD, 0xDDDDDDDD,
       0xBAADF00D, 0xABABABAB)


def valeur(v):
    """Toujours le nombre, puis le nom -- jamais le nom seul."""
    if v is None:
        return '?'
    if v == 0xFFFFFFFF:
        return '-1 (rien)'
    if v in TAS:
        return '0x%08X (remplissage de TAS : le bloc est LIBERE)' % v
    if 0 <= v < len(NOMS):
        return '%d (%s)' % (v, NOMS[v])
    return '%d (hors table)' % v


def main():
    argv = sys.argv[1:]
    secondes = 420
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    journal = os.path.join(RACINE, 'analysis', 'pister_60_stage.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.sortie = fichier
    dbg.bp_max = 200
    dbg.dr_max = 400                  # on veut TOUTES les ecritures
    dbg.dr_auto_desarmer = False
    t0 = time.monotonic()

    et = {'base': 0, 'tache': 0, 'pose': False,
          'ptr': None, 'dr60': None, 'dr5c': None,
          'vu60': None, 'vu5c': None, 'n60': 0}

    def t():
        return time.monotonic() - t0

    def rva(adresse):
        return adresse - et['base'] if et['base'] else 0

    def qui(d, ctx):
        """La chaine d'appel encore sur la pile, cote MOTEUR seulement."""
        pile = d.read(ctx.Rsp, 8 * 96) or b''
        vus = 0
        for i in range(0, len(pile) - 7, 8):
            v = int.from_bytes(pile[i:i + 8], 'little')
            mod, off = d.module_of(v)
            if mod and MOTEUR in mod and vus < 8:
                d.dire('              retour [rsp+0x%03X] -> rva 0x%X'
                       % (i, off))
                vus += 1
        if not vus:
            d.dire('              aucune adresse de retour du moteur '
                   'sur la pile')

    def rearmer(d, tache):
        """Desarme les DR de champ et les repose sur `tache`."""
        for cle in ('dr60', 'dr5c'):
            if et[cle] is not None:
                d.desarmer_materiel(et[cle])
                et[cle] = None
        et['tache'] = tache
        et['vu60'] = et['vu5c'] = None
        if not tache:
            d.dire('  t=%6.1f s  la tache n\'existe plus (pointeur nul)' % t())
            return
        et['dr60'] = d.armer_materiel(tache + DEMANDE, 4, 'w',
                                      nom='tache+0x60 DEMANDE')
        et['dr5c'] = d.armer_materiel(tache + COURANT, 4, 'w',
                                      nom='tache+0x5C courant')
        et['vu60'] = d.u32(tache + DEMANDE)
        et['vu5c'] = d.u32(tache + COURANT)
        d.dire('  t=%6.1f s  TACHE 0x%X  --  demande %s, courant %s'
               % (t(), tache, valeur(et['vu60']), valeur(et['vu5c'])))

    def sur_dr(d, m, ctx, tid):
        """Le DR se declenche APRES l'ecriture : rip pointe la suivante."""
        r = rva(ctx.Rip)
        if m is et['ptr']:
            nouvelle = d.u64(et['base'] + TACHE_RVA) or 0
            quoi = ('CREATION' if r == CREATION_RVA else
                    'DESTRUCTION' if r in DESTRUCTION else 'ecriture')
            d.dire('  t=%6.1f s  POINTEUR : %s depuis rva 0x%X -> 0x%X'
                   % (t(), quoi, r, nouvelle))
            return                              # le rearmement se fait au tic
        if m is et['dr60']:
            v = d.u32(m.adresse)
            et['vu60'] = v
            et['n60'] += 1
            d.dire('  t=%6.1f s  DEMANDE <- %s   par rva 0x%X'
                   % (t(), valeur(v), r))
            qui(d, ctx)
            return
        if m is et['dr5c']:
            v = d.u32(m.adresse)
            et['vu5c'] = v
            marque = '' if r == RECOPIE_RVA else '   <-- PAS la recopie connue'
            d.dire('  t=%6.1f s  courant <- %s   par rva 0x%X%s'
                   % (t(), valeur(v), r, marque))
            if marque:
                qui(d, ctx)

    def sur_bp(d, bp, ctx, tid):
        base = et['base']
        retour = d.u64(ctx.Rsp) or 0
        if bp.nom == 'Chargeur':
            index = ctx.Rcx & 0xFFFFFFFF
            tache = d.u64(base + TACHE_RVA) or 0
            d.dire('  t=%6.1f s  CHARGEMENT : %s   <- retour rva 0x%X'
                   % (t(), valeur(index), rva(retour)))
            if tache != et['tache']:
                d.dire('              la tache a CHANGE : 0x%X '
                       '(surveillee 0x%X)' % (tache, et['tache']))
            return
        if bp.nom == 'Mode':
            # `mov [0x180754A58], r9d` : r9d n'est pas encore ecrit.
            d.dire('  t=%6.1f s  MODE : mode=%d, drapeau dl=%d, indice r9d=%s'
                   '   <- retour rva 0x%X'
                   % (t(), ctx.Rcx & 0xFFFFFFFF, ctx.Rdx & 0xFF,
                      valeur(ctx.R9 & 0xFFFFFFFF), rva(retour)))
            return
        if bp.nom == 'Ecretage':
            # `cmova ebp, eax` : ebp est l'indice demande, eax le repli.
            demande = ctx.Rbp & 0xFFFFFFFF
            borne = (d.read(b + ECRETAGE_IMM, 1) or b'\xff')[0]
            repli = d.u32(base + ECRETAGE_REPLI)
            ecrete = demande > borne          # cmova : NON SIGNE
            d.dire('  t=%6.1f s  ECRETAGE : demande %s, borne %d, repli %s'
                   ' -> %s' % (t(), valeur(demande), borne, valeur(repli),
                               'ECRETE' if ecrete else 'passe'))
            d.dire('              <- retour rva 0x%X' % rva(retour))
            return
        if bp.nom == 'Requete':
            d.dire('  t=%6.1f s  DEMANDE(%s)   <- retour rva 0x%X'
                   % (t(), valeur(ctx.Rcx & 0xFFFFFFFF), rva(retour)))
            return

    def tic(d, _t):
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['base'] = b
        if not et['pose']:
            et['pose'] = True
            for nom, adr in (('Chargeur', CHARGEUR_RVA),
                             ('Mode', MODE_RVA),
                             ('Ecretage', ECRETAGE_RVA),
                             ('Requete', REQUETE_RVA)):
                bp = instrument.PointArret(nom, b + adr, max_coups=5000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)
            et['ptr'] = d.armer_materiel(b + TACHE_RVA, 8, 'w',
                                         nom='pointeur TaskStage')
            d.dire('  t=%6.1f s  quatre points d\'arret et le pointeur armes'
                   % t())
            d.dire('              borne d ecretage VIVANTE : %d, repli %s'
                   % ((d.read(b + ECRETAGE_IMM, 1) or b'\xff')[0],
                      valeur(d.u32(b + ECRETAGE_REPLI))))
        tache = d.u64(b + TACHE_RVA) or 0
        if tache != et['tache']:
            rearmer(d, tache)
            return
        if not tache:
            return
        # Relecture : une ecriture qu'aucun DR n'a vue doit se DIRE.
        for cle, champ, nom in (('vu60', DEMANDE, 'DEMANDE'),
                                ('vu5c', COURANT, 'courant')):
            v = d.u32(tache + champ)
            if v is not None and v != et[cle]:
                d.dire('  t=%6.1f s  %s a change SANS DR : %s -> %s'
                       % (t(), nom, valeur(et[cle]), valeur(v)))
                et[cle] = v

    dbg.on_dr = sur_dr
    dbg.on_bp = sur_bp
    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)

    print('MESURE : qui DEMANDE le decor (TaskStage+0x60).')
    print()
    print('  Le clavier est a VOUS. MENU -> DOJO -> entrainement,')
    print('  puis fermez le jeu.')
    print('  journal : %s' % journal)
    print()
    dbg.run(EXE, JEU, secondes, ())
    if not et['n60']:
        dbg.dire('\nAUCUNE ecriture de la demande n\'a ete vue. Si un')
        dbg.dire('CHARGEMENT a eu lieu quand meme, la demande passe par un')
        dbg.dire('autre chemin que ce champ, et c\'est un resultat.')
    fichier.close()
    print()
    print('Journal ecrit : %s' % journal)
    return 0


if __name__ == '__main__':
    sys.exit(main())
