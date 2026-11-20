#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le reseau demarre-t-il ? Ou la machine des bornes liees s'arrete-t-elle ?

Le sous-systeme `am::abaas` (bornes liees, STUN/TURN) n'est ni bouchonne ni
garde par un reglage du jeu : `AbaasManager` est cree sans condition dans
`module_start`, et `setupLink` (`0x180219BF0`) est RETENTE A CHAQUE TRAME tant
qu'il echoue. Ce qui le refusait, c'est la validation de sept parametres
d'identite dans `ImplLink::setup` (`0x1802C9D20`), tous fournis par `apm.dll`
-- c'est-a-dire par NOUS.

Notre stub rendait partout `"0000"`. Trois corrections ont ete portees dans
`tools/gen_apm_stub.py` le 2026-09-05 :

    AllnetAuth_getCountryCode  "0000" -> "JPN"      (3 lettres, alphabetiques)
    System_getKeychipId        chaine -> STRUCTURE, 11 caracteres en +0x22
    System_getBoardId          chaine -> STRUCTURE, 11 caracteres en +0x22

Cette sonde mesure si elles suffisent. Les quatre points de validation sont les
CIBLES des sauts d'acceptation, lues au desassembleur :

    0x1802C9DC8  cmp qword [rdx+0x30], 4      je 0x1802C9E03   gameId
    0x1802C9E61  cmp qword [rdx+0x78], 0xb    je 0x1802C9E9C   keychipId
    0x1802C9E9C  cmp qword [rdx+0x98], 0xb    je 0x1802C9EDD   mainId
    0x1802C9EF1  cmp qword [rdx+0x58], 3      je 0x1802C9F2C   countryCode

Atteindre `0x1802C9F2C` signifie que les quatre sont passes.

On observe ensuite le `tic()` des etats, pour voir jusqu'ou la machine monte :
Setup -> Standby -> appariement, ou bien Unavailable, le cul-de-sac.

    tools/pister_link.cmd
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

POINTS = [
    ('SetupLink',    0x219BF0),   # la tentative, a chaque trame tant qu'elle echoue
    # Le CONVERTISSEUR : `setupLink` ne recopie pas ce que rend `apm.dll`, il le
    # fait passer par `0x18021A470`, qui convertit la chaine etroite en chaine
    # large (`mbstowcs_s`) et, EN CAS D'ECHEC, pose une chaine VIDE
    # (`0x18021A50B` -> `0x180347568`, huit octets nuls verifies).
    # La mesure du 2026-09-05 a montre les CINQ champs a taille=0, `gameId`
    # compris -- celui qui n'avait jamais ete touche. Ce n'est donc pas une
    # valeur qui est mauvaise : c'est toute la chaine de transmission. Ces trois
    # points disent OU elle casse.
    ('conv entree',  0x21A470),   # rcx = la chaine rendue par apm.dll
    ('conv SUCCES',  0x21A4BF),   # la taille mesuree est non nulle
    ('conv ECHEC',   0x21A50B),   # -> pose la chaine vide
    # LE TUEUR. `_invalid_parameter` de la CRT : une fonction `_s` a recu un
    # argument invalide, et elle tue le processus par `int 0x29` sans rien dire.
    #
    #     0x180303B24  mov  ecx, 0x17
    #     0x180303B29  call IsProcessorFeaturePresent(23)
    #     0x180303B33  mov  ecx, 5              ; FAST_FAIL_INVALID_ARG
    #     0x180303B38  int  0x29                ; <- le crash observe
    #     0x180303B40  mov  edx, 0xC0000417     ; STATUS_INVALID_CRUNTIME_PARAMETER
    #
    # On se pose a son ENTREE, ou l'adresse de retour est encore sur la pile :
    # c'est le seul moyen de savoir QUI lui a passe un mauvais argument.
    ('_invalid_param', 0x303B20),
    # La conversion qui echoue : `wcstombs_s`-like, six arguments.
    #   rcx = pRetValue   rdx = dst   r8 = dstSize   r9 = src
    # Son retour -2 signifie « destination trop petite » (errno ERANGE 0x22).
    # A son entree, `r8` porte LA TAILLE DU TAMPON -- le chiffre qu'il faut.
    ('wcstombs_s',   0x315F54),
    # Le formatage qui tue, dans le serveur de TITRE (`abaasgs`) :
    #   0x18029E6C2  movzx eax, byte [r15+0x41]   ; minorVersion
    #   0x18029E6C7  movzx r9d, byte [r15+0x40]   ; majorVersion
    #   0x18029E6D7  mov  edx, 5                  ; le tampon ne fait que 5 o
    #   0x18029E6E0  call sprintf_s(buf, 5, "%d.%02d", major, minor)
    # « 1.00 » tient dans cinq octets, « 99.99 » en demande six. On lit donc
    # les deux octets AVANT le formatage, au lieu de les deviner.
    ('versionGS',    0x29E6C2),
    ('ImplSetup',    0x2C9D20),   # l'entree de la validation des sept parametres
    ('okGameId',     0x2C9E03),   # taille == 4    -- passait deja
    ('okKeychipId',  0x2C9E9C),   # taille == 11   -- corrige
    ('okMainId',     0x2C9EDD),   # taille == 11   -- corrige
    ('okCountry',    0x2C9F2C),   # taille == 3 et alphabetique -- corrige
    # Le tic() de chaque etat : jusqu'ou la machine monte-t-elle ?
    ('tic Setup',       0x2D8F80),
    ('tic Standby',     0x2D9920),
    ('tic Unavailable', 0x2E2FA0),
    ('tic MatchAlloc',  0x2D9E20),
    ('tic MatchMatch',  0x2DAAF0),
    ('tic Playing',     0x2E2280),
]
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')


def main():
    argv = sys.argv[1:]
    secondes = 300
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 400
    journal = os.path.join(RACINE, 'analysis', 'pister_link.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'compte': collections.Counter(), 'recit': [],
          't0': None, 'base': None, 'vus': set()}

    def note(txt):
        # Au fil de l'eau : le debogueur se bloque parfois en fin de session, et
        # un bilan ecrit seulement a la fin serait perdu.
        et['recit'].append(txt)
        fichier.write(txt + os.linesep)
        fichier.flush()

    def texte_std(d, adr):
        """Une std::string / std::wstring MSVC : 0x20 octets, tampon SSO de 16,
        taille en +0x10, capacite en +0x18. Au-dela de la capacite SSO, le
        contenu est au bout du pointeur range en +0x00."""
        brut = d.read(adr, 0x20) or bytes(0x20)
        taille = int.from_bytes(brut[0x10:0x18], 'little')
        cap = int.from_bytes(brut[0x18:0x20], 'little')
        if taille > 0x1000:                       # manifestement pas une chaine
            return taille, '?'
        if cap >= 16:
            ptr = int.from_bytes(brut[0:8], 'little')
            data = d.read(ptr, min(taille * 2 + 2, 64)) or b''
        else:
            data = brut[0:16]
        # On ne sait pas si c'est etroit ou large : on rend ce qui est lisible.
        etroit = bytes(b for b in data[:32] if 0x20 <= b < 0x7F)
        return taille, etroit.decode('latin-1')

    def sur_bp(d, bp, ctx, tid):
        et['compte'][bp.nom] += 1
        if et['t0'] is None:
            et['t0'] = time.time()
        ms = (time.time() - et['t0']) * 1000.0

        # Les deux octets de version, juste avant le sprintf_s qui deborde.
        if bp.nom == 'versionGS' and et['compte'][bp.nom] <= 6:
            r15 = ctx.R15 & 0xFFFFFFFFFFFFFFFF
            v = d.read(r15 + 0x40, 2) or b'\xff\xff'
            rendu = '%d.%02d' % (v[0], v[1])
            note('%9.1f ms  version GS : major=%d minor=%d -> "%s" '
                 '(%d octets + NUL, le tampon en fait 5)'
                 % (ms, v[0], v[1], rendu, len(rendu)))
            return

        # La conversion : quelle chaine, et dans quel tampon ?
        if bp.nom == 'wcstombs_s' and et['compte'][bp.nom] <= 20:
            dst_taille = ctx.R8 & 0xFFFFFFFFFFFFFFFF
            src = ctx.R9 & 0xFFFFFFFFFFFFFFFF
            brut = d.read(src, 96) or b''
            z = brut.find(b'\x00\x00')
            if z % 2:
                z += 1
            try:
                txt = brut[:z].decode('utf-16-le', 'replace')
            except Exception:
                txt = '?'
            note('%9.1f ms  wcstombs_s : tampon=%d octets  <- %r (%d car.)'
                 % (ms, dst_taille, txt[:40], len(txt)))
            return

        # Le tueur : on remonte la pile pour nommer l'appelant. Les adresses
        # sont RELOGEES a l'execution ; on les ramene a la VA statique du
        # binaire (base 0x180000000) pour pouvoir les desassembler ensuite.
        if bp.nom == '_invalid_param':
            b = et['base'] or 0
            note('%9.1f ms  *** _invalid_parameter -- LE CRASH ***' % ms)
            # On lit PROFOND, et on separe le code applicatif de la CRT : les
            # quatre adresses du premier releve etaient toutes en 0x1803xxxxx,
            # c'est-a-dire dans la CRT -- elles ne nomment pas le fautif.
            pile = d.read(ctx.Rsp, 8 * 96) or b''
            appli, crt = [], []
            for i in range(0, len(pile) - 7, 8):
                v = int.from_bytes(pile[i:i + 8], 'little')
                if b and b <= v < b + 0x345000:
                    va = v - b + 0x180000000
                    (crt if va >= 0x1802F0000 else appli).append((i, va))
            for i, va in appli[:10]:
                note('              APPLICATIF [rsp+0x%03X] -> 0x%X' % (i, va))
            for i, va in crt[:6]:
                note('              (crt)      [rsp+0x%03X] -> 0x%X' % (i, va))
            if not appli:
                note('              (aucune adresse applicative sur la pile)')
            return

        # Ce que `apm.dll` a REELLEMENT rendu, avant toute conversion. Si la
        # chaine est bonne ici mais que le champ finit vide, la casse est dans
        # la conversion ; si elle est deja vide ou illisible, elle est dans le
        # pont entre le moteur et notre DLL.
        if bp.nom == 'conv entree' and et['compte'][bp.nom] <= 12:
            src = ctx.Rcx & 0xFFFFFFFFFFFFFFFF
            brut = d.read(src, 96) or b''
            # Le convertisseur est `wcstombs_s` : l'entree DOIT etre large.
            # On rend les deux lectures, pour voir laquelle est la bonne.
            fin = brut.find(b'\x00')
            etroit = brut[:fin if fin >= 0 else 32]
            large = ''
            try:
                z = brut.find(b'\x00\x00')
                if z % 2:
                    z += 1
                large = brut[:z].decode('utf-16-le', 'replace')
            except Exception:
                large = '?'
            note('%9.1f ms  conversion <- 0x%X  large=%r  etroit=%r'
                 % (ms, src, large[:40], etroit[:20]))
            return

        # A l'entree de la validation, LIRE les sept parametres : c'est ce qui
        # nomme le champ fautif au lieu de le deviner. Les champs font 0x20
        # octets chacun, et leur taille est en +0x10 de chacun.
        if bp.nom == 'ImplSetup' and et['compte'][bp.nom] <= 3:
            p = ctx.Rdx & 0xFFFFFFFFFFFFFFFF
            champs = [('serverURI', 0x00), ('gameId', 0x20),
                      ('countryCode', 0x48), ('keychipId', 0x68),
                      ('mainId', 0x88)]
            note('%9.1f ms  ImplSetup : les parametres recus' % ms)
            for nom_, off in champs:
                taille, vu = texte_std(d, p + off)
                note('              %-12s taille=%-4d  %s'
                     % (nom_, taille, vu))
            return

        # `setupLink` est retente a CHAQUE TRAME : on ne note qu'une fois par
        # point, sinon le journal deborde en une seconde. Les COMPTES, eux,
        # sont ecrits periodiquement -- sans quoi on ne distingue pas « ca
        # boucle » de « ca s'est arrete », defaut du releve du 2026-09-05.
        if bp.nom in et['vus']:
            if time.time() - et.get('dernier_bilan', 0) > 10.0:
                et['dernier_bilan'] = time.time()
                note('%9.1f ms  --- comptes : %s' % (ms, ', '.join(
                    '%s=%d' % (n, c) for n, c in sorted(et['compte'].items()))))
            return
        et['vus'].add(bp.nom)
        note('%9.1f ms  PREMIERE FOIS : %s' % (ms, bp.nom))

    def tic(d, t):
        # Poser DES QUE le moteur est charge, et non a t=8 s : le crash du
        # 2026-09-06 tombait avant, ce qui rendait la sonde aveugle -- le
        # releve ne montrait que le chargement des modules.
        if et['pose']:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        et['base'] = b
        for nom_, rva in POINTS:
            bp = instrument.PointArret(nom_, b + rva, max_coups=400000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  points d\'arret poses a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    print('MESURE : le reseau des bornes liees demarre-t-il ?')
    print()
    print('  Le jeu va se lancer. Laissez-le simplement tourner une minute')
    print('  sur l\'ecran d\'attract, puis fermez-le. Aucune touche n\'est')
    print('  necessaire : le reseau se met en route tout seul.')
    print()
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    lignes = []

    # La console Windows est en cp1252 : les chaines relues en memoire (du
    # texte etroit lu comme de l'UTF-16) contiennent des ideogrammes, et un
    # `print` brut leve UnicodeEncodeError. La releve du 2026-09-06 a ainsi
    # perdu son bilan APRES une mesure reussie. Le fichier est desormais ecrit
    # AVANT tout affichage, et l'affichage ne peut plus rien faire echouer.
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

    def dit(txt=''):
        lignes.append(txt)

    dit()
    dit('=' * 72)
    dit('COMPTES (nombre de passages) :')
    for nom_, _ in POINTS:
        dit('   %-16s %d' % (nom_, et['compte'][nom_]))
    dit()
    dit('RECIT :')
    for t in et['recit']:
        dit('   ' + t)
    dit()
    dit('LECTURE :')
    dit('   conv entree a 0  -> les getters d apm.dll ne sont PAS appeles :')
    dit('                       la casse est en amont, dans setupLink.')
    dit('   conv entree > 0, chaines lisibles, mais conv ECHEC > 0')
    dit('                    -> nos valeurs arrivent bien et c est la')
    dit('                       CONVERSION qui les refuse.')
    dit('   conv entree > 0 mais chaines illisibles (???)')
    dit('                    -> le pont moteur <-> apm.dll ne transmet pas ce')
    dit('                       que nous croyons : mauvaise signature.')
    dit('   conv SUCCES > 0 et champs encore vides -> la casse est APRES,')
    dit('                       entre la conversion et la structure.')
    dit('   okCountry > 0    -> LES QUATRE VALIDATIONS PASSENT. `setup`')
    dit('                       reussit, la machine est construite.')
    dit('   tic Setup > 0    -> la machine tourne et tente son dialogue HTTP.')
    dit('   tic Unavailable  -> elle a abandonne : c est le cul-de-sac. Il')
    dit('                       faudra lui servir un serveur.')
    dit('   tic MatchAlloc   -> elle est allee jusqu a l appariement TURN.')
    bilan = os.path.join(RACINE, 'analysis', 'pister_link_bilan.txt')
    with open(bilan, 'w', encoding='utf-8') as fp:
        fp.write(os.linesep.join(lignes) + os.linesep)
    for txt in lignes:
        try:
            print(txt)
        except UnicodeEncodeError:
            print(txt.encode('ascii', 'replace').decode('ascii'))
    print()
    print('bilan ecrit dans %s' % bilan)
    return 0


if __name__ == '__main__':
    sys.exit(main())
