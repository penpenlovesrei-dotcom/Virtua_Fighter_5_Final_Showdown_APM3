#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""TOUS LES CHAMPS d'une structure rendue par un ACCESSEUR, cote PowerPC.

Le pendant Xbox 360 de `tools/champs_accesseur.py`. Meme question, et elle
s'est posee le 2026-10-18 : l'ecran de statut du Quest lit quatre `u32` en
`profil + 0x17C` a `+0x188`, ou `profil` est la valeur rendue par
`FUN_8230B5B8`. Qui les ECRIT ?

POURQUOI LES DEUX OUTILS EXISTANTS NE SUFFISENT PAS, et chacun pour une
raison de principe :

  . `x360_champ.py` cherche par DEPLACEMENT. Sur `0x17C`, `0x180`, `0x184`
    et `0x188` l'image de 2007 porte 65, 57, 64 et 49 ecritures, et quand on
    regroupe celles qui se suivent sur un meme registre, LA PLUPART ONT `r1`
    POUR BASE -- la pile. Ce sont des cadres de fonction, pas la structure.
    Un releve par deplacement ne dit jamais quel objet tient le registre :
    c'est son angle mort, et il est le meme qu'en x64 ;
  . `x360_ppc.py xref` cherche une ADRESSE construite en deux instructions.
    Ici la structure n'a pas d'adresse : elle arrive par la valeur de retour
    d'une fonction.

CE QUE CELUI-CI FAIT :

  . il recense les `bl <accesseur>` par un balayage exact des mots (op 18,
    LK a 1) -- pas de desassemblage lineaire, donc pas de deraillement ;
  . depuis chaque site, il suit le pointeur rendu dans `r3` vers l'avant,
    et retient les registres qui en sont des ALIAS :
        mr   rD, rS            rD vaut le meme pointeur
        addi rD, rA, n         rD vaut pointeur + n
  . il suit aussi le pointeur A TRAVERS LA PILE. C'est indispensable et non
    accessoire : le compilateur range le pointeur dans son cadre avant un
    appel et le relit apres (`stw r3, 0x50(r1)` … `lwz r31, 0x50(r1)`).
    Sans cela on perd la trace au premier appel, c'est-a-dire tout de suite ;
  . tout acces memoire dont la BASE est un alias est rendu, avec son
    deplacement RAMENE a l'origine de la structure.

LES LIMITES, et elles sont dites parce qu'un controle qui ment coute plus
qu'un controle absent :

  . capstone 5.0.7 ne remplit pas `regs_write` pour PowerPC. Le registre
    ECRIT est donc pris comme la premiere operande quand elle est un
    registre et que l'instruction n'est pas un rangement (`st*`) ni une
    comparaison ni un branchement. C'est exact pour les formes qui nous
    servent et conservateur ailleurs : au pire un alias est OUBLIE, jamais
    invente ;
  . on suit UN SEUL CHEMIN, celui qui ne prend aucun branchement : un
    conditionnel (`beq`, `bne`, `bdnz`…) ne nous arrete pas, on continue sur
    son chemin non pris, qui est une execution reelle. Un branchement
    INCONDITIONNEL (`b`, `blr`, `bctr`) nous arrete, parce qu'apres lui le
    code lineaire appartient a un autre bloc. Un appel (`bl`) ne stoppe pas,
    mais il oublie `r3` a `r12`, qui sont volatiles ;
  . donc le releve est un MINORANT. Ce qu'il montre est vrai ; ce qu'il ne
    montre pas n'est pas prouve absent.

    py -3 tools/x360_suivre.py 0x8230B5B8
    py -3 tools/x360_suivre.py 0x8230B5B8 --ecritures
    py -3 tools/x360_suivre.py 0x8230B5B8 --champ 0x17c 0x180 0x184 0x188
    py -3 tools/x360_suivre.py 0x8230B5B8 --graphe        <- les DEUX cotes
    py -3 tools/x360_suivre.py 0x8230B5B8 --image extracted/X360_FS/sel/default.img

L'IMAGE PAR DEFAUT EST CELLE DE 2007 (`extracted/X360_VF5/vf5_x360.img`),
et c'est voulu : `x360_ppc.py` porte en dur celle de FINAL SHOWDOWN, les
deux ont la meme base `0x82000000`, et une adresse de 2007 y repond donc
AUTRE CHOSE sans la moindre erreur. On ne melange pas les deux builds.
"""
import os
import struct
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, 'tools'))

import capstone                                        # noqa: E402
from capstone import ppc                                # noqa: E402
import x360_ppc                                         # noqa: E402

IMAGE_2007 = os.path.join(RACINE, 'extracted', 'X360_VF5', 'vf5_x360.img')

# Les mnemoniques dont la premiere operande N'EST PAS le registre ecrit.
PAS_DEST = ('st', 'cmp', 'b', 'tw', 'td', 'mt', 'dcb', 'icbi', 'sync',
            'eieio', 'isync', 'trap')
# Un APPEL ne termine pas le chemin : il oublie les registres volatiles.
APPELS = ('bl', 'bla', 'bctrl')
# Un branchement INCONDITIONNEL le termine : apres lui, le code lineaire
# appartient a un autre chemin. Les conditionnels (beq, bne, bdnz…) ne le
# terminent pas -- on suit le chemin NON PRIS, qui est bien une execution
# reelle. C'etait le defaut de la premiere version : la premiere chose que
# fait un appelant est `cmplwi cr6, r3, 0 ; beq …`, le test de nullite, et
# s'arreter la ne laissait RIEN a relever sur aucun des 21 sites.
ARRETS = ('b', 'ba', 'blr', 'bctr')


def sext(v, bits):
    s = 1 << (bits - 1)
    return (v & (s - 1)) - (v & s)


def sites_bl(img, cible):
    """Les `bl cible` des sections executables, par balayage exact."""
    out = []
    for s in img.secs:
        if not s['exec']:
            continue
        va0 = s['va'] & ~3
        brut = img.d[img.off(va0):img.off(va0) + s['vsize']]
        for i in range(0, len(brut) - 3, 4):
            w = struct.unpack_from('>I', brut, i)[0]
            if w >> 26 != 18 or (w & 3) != 1:
                continue
            va = va0 + i
            if va + sext(w & 0x03FFFFFC, 26) == cible:
                out.append(va)
    return out


def dest(insn):
    """Le registre ecrit, ou None. Voir LES LIMITES dans l'en-tete."""
    if insn.mnemonic.startswith(PAS_DEST):
        return None
    ops = insn.operands
    if ops and ops[0].type == ppc.PPC_OP_REG:
        return ops[0].reg
    return None


def suivre(img, md, site, limite=160):
    """Depuis un `bl`, rend [(va, mnemo, op_str, offset, ecrit, indexe)]."""
    # r3 porte le pointeur au retour de l'appel ; r1 est le cadre.
    alias = {_reg(md, 'r3'): 0}     # registre -> offset depuis la structure
    pile = {}                       # deplacement sur r1 -> offset
    cadre = _reg(md, 'r1')
    trouves = []
    deb = site + 4
    code = img.lire(deb, limite * 4)
    for insn in md.disasm(code, deb):
        m = insn.mnemonic
        # 1. les acces memoire dont la base est un alias
        for o in insn.operands:
            if o.type != ppc.PPC_OP_MEM:
                continue
            b = o.mem.base
            if b in alias:
                trouves.append((insn.address, m, insn.op_str,
                                alias[b] + o.mem.disp,
                                m.startswith('st'), False))
            elif b == cadre and m.startswith(('lwz', 'ld')):
                if o.mem.disp in pile:
                    d = dest(insn)
                    if d is not None:
                        alias[d] = pile[o.mem.disp]
        # 1 bis. LES FORMES INDEXEES. capstone ne les rend PAS comme un acces
        # memoire : `lwzx rD, rA, rB` sort en trois registres. Sans ce cas on
        # perdrait tout parcours de tableau, et le champ d'objets du profil en
        # est un. Le deplacement n'est pas constant : on le dit INDEXE.
        if (len(m) > 2 and m.endswith(('x', 'ux'))
                and m.startswith(('lwz', 'lbz', 'lhz', 'lha', 'ld',
                                  'stw', 'stb', 'sth', 'std'))):
            for o in insn.operands[1:]:
                if o.type == ppc.PPC_OP_REG and o.reg in alias:
                    trouves.append((insn.address, m, insn.op_str,
                                    alias[o.reg], m.startswith('st'), True))
                    break
        # 2. le pointeur range dans le cadre, pour etre relu apres un appel
        if m.startswith(('stw', 'std')):
            ops = insn.operands
            if (len(ops) >= 2 and ops[0].type == ppc.PPC_OP_REG
                    and ops[0].reg in alias
                    and ops[1].type == ppc.PPC_OP_MEM
                    and ops[1].mem.base == cadre):
                pile[ops[1].mem.disp] = alias[ops[0].reg]
        # 3. les branchements
        if m in APPELS:
            for n in range(3, 13):
                alias.pop(_reg(md, 'r%d' % n), None)
            if not alias and not pile:
                break
            continue
        if m in ARRETS:
            break
        if m.startswith('b'):
            continue                # conditionnel : on suit le chemin non pris
        # 4. les alias
        ops = insn.operands
        if m == 'mr' and len(ops) == 2 and ops[1].reg in alias:
            alias[ops[0].reg] = alias[ops[1].reg]
            continue
        if (m == 'addi' and len(ops) == 3
                and ops[1].type == ppc.PPC_OP_REG and ops[1].reg in alias):
            alias[ops[0].reg] = alias[ops[1].reg] + ops[2].imm
            continue
        # 5. tout le reste ECRASE ce qu'il ecrit
        d = dest(insn)
        if d is not None:
            alias.pop(d, None)
        if not alias and not pile:
            break
    return trouves


# ---------------------------------------------------------------------------
# LE PARCOURS SUR GRAPHE DE FLOT
#
# POURQUOI (2026-10-18, §14.8). Le parcours en ligne droite ci-dessus est
# valide, et il a rendu vingt-cinq champs du profil de 2007 avec leurs
# ecrivains. Mais il n'atteint PAS les quatre `u32` de `profil + 0x17C`,
# que `FUN_82310598` lit pourtant : cette fonction prend le profil au debut
# et les lit tres loin en aval, apres des branchements inconditionnels. Un
# chemin unique ne peut pas y arriver, et augmenter la borne n'y change rien
# -- ce n'est pas la longueur, c'est le chemin.
#
# CE QUE CELUI-CI FAIT DE PLUS : il suit LES DEUX cotes de chaque
# conditionnel et traverse les `b`. Il reste borne a la fonction qui porte
# l'appel, par `.pdata` (`quest_x360.Image().fonctions()`), ce qui evite de
# partir chez le voisin.
#
# ET UNE CHOSE QUI N'EST PAS UN RISQUE ICI : desassembler la fonction d'une
# traite. En PowerPC chaque instruction tient en UN mot de quatre octets
# aligne -- il n'y a pas de recalage possible, donc pas de deraillement. La
# regle du desassemblage lineaire est une regle x86.
# ---------------------------------------------------------------------------


def cible_branchement(insn):
    """L'adresse visee par un branchement, ou None."""
    for o in insn.operands:
        if o.type == ppc.PPC_OP_IMM:
            return o.imm
    return None


def un_pas(md, insn, alias, pile, cadre, trouves):
    """Applique une instruction a l'etat. Rend l'action a faire ensuite :
    'suite', 'arret', ou ('cond', cible), ou ('saut', cible)."""
    m = insn.mnemonic
    # 1. les acces memoire dont la base est un alias
    for o in insn.operands:
        if o.type != ppc.PPC_OP_MEM:
            continue
        b = o.mem.base
        if b in alias:
            trouves.append((insn.address, m, insn.op_str,
                            alias[b] + o.mem.disp,
                            m.startswith('st'), False))
        elif b == cadre and m.startswith(('lwz', 'ld')):
            if o.mem.disp in pile:
                d = dest(insn)
                if d is not None:
                    alias[d] = pile[o.mem.disp]
    # 1 bis. les formes indexees, que capstone ne rend pas comme memoire
    if (len(m) > 2 and m.endswith(('x', 'ux'))
            and m.startswith(('lwz', 'lbz', 'lhz', 'lha', 'ld',
                              'stw', 'stb', 'sth', 'std'))):
        for o in insn.operands[1:]:
            if o.type == ppc.PPC_OP_REG and o.reg in alias:
                trouves.append((insn.address, m, insn.op_str,
                                alias[o.reg], m.startswith('st'), True))
                break
    # 2. le pointeur range dans le cadre
    if m.startswith(('stw', 'std')):
        ops = insn.operands
        if (len(ops) >= 2 and ops[0].type == ppc.PPC_OP_REG
                and ops[0].reg in alias
                and ops[1].type == ppc.PPC_OP_MEM
                and ops[1].mem.base == cadre):
            pile[ops[1].mem.disp] = alias[ops[0].reg]
    # 3. les branchements
    if m in APPELS:
        # LE POINTEUR PART-IL EN ARGUMENT ? r3..r10 sont les arguments de
        # l'ABI PowerPC. On le dit AVANT d'oublier les volatiles : une
        # ecriture faite dans l'appelee est invisible a ce parcours, et
        # c'est la seule facon de savoir ou aller regarder.
        for n in range(3, 11):
            r = _reg(md, 'r%d' % n)
            if r in alias:
                c = cible_branchement(insn)
                trouves.append((insn.address, 'ARG r%d' % n,
                                'vers 0x%08X' % c if c else insn.op_str,
                                alias[r], False, False))
        for n in range(3, 13):
            alias.pop(_reg(md, 'r%d' % n), None)
        return 'suite'
    if m in ARRETS:
        if m in ('b', 'ba'):
            c = cible_branchement(insn)
            return ('saut', c) if c else 'arret'
        return 'arret'
    if m.startswith('b'):
        c = cible_branchement(insn)
        return ('cond', c) if c else 'suite'
    # 4. les alias
    ops = insn.operands
    if m == 'mr' and len(ops) == 2 and ops[1].reg in alias:
        alias[ops[0].reg] = alias[ops[1].reg]
        return 'suite'
    if (m == 'addi' and len(ops) == 3
            and ops[1].type == ppc.PPC_OP_REG and ops[1].reg in alias):
        alias[ops[0].reg] = alias[ops[1].reg] + ops[2].imm
        return 'suite'
    # 5. tout le reste ECRASE ce qu'il ecrit
    d = dest(insn)
    if d is not None:
        alias.pop(d, None)
    return 'suite'


def fonctions_pdata(chemin):
    """{debut: fin} des fonctions de .pdata. Les feuilles n'y sont pas."""
    import quest_x360
    img = quest_x360.Image(chemin)
    return [(a, a + n) for a, n in img.fonctions() if n]


def bornes_de(fcts, va, defaut=0x8000):
    for a, b in fcts:
        if a <= va < b:
            return a, b
    return va - 0x200, va + defaut


def suivre_graphe(img, md, site, fcts, visites_max=40000):
    """Comme `suivre`, mais sur le graphe de flot de la fonction appelante."""
    cadre = _reg(md, 'r1')
    deb, fin = bornes_de(fcts, site)
    try:
        code = img.lire(deb, fin - deb)
    except Exception:
        return []
    insns = {}
    for insn in md.disasm(code, deb):
        insns[insn.address] = insn
    trouves = []
    vus = set()
    travail = [(site + 4, {_reg(md, 'r3'): 0}, {})]
    visites = 0
    while travail and visites < visites_max:
        adr, alias, pile = travail.pop()
        while True:
            visites += 1
            if visites >= visites_max:
                break
            # LA CLE NE PORTE PAS LES VALEURS, ET C'EST LE POINT.
            # Premiere version : la cle etait `frozenset(alias.items())`. Une
            # boucle de copie incremente son registre d'alias a chaque tour
            # (`addi r9, r9, 4`), l'etat differait donc a chaque passage, rien
            # n'etait jamais "deja vu", et le parcours s'elargissait sans fin :
            # 4 221 "champs" pour le profil, un par octet, chacun avec une
            # ecriture. Un releve qui AVAIT L'AIR d'une mesure.
            # En ne gardant que les registres SUIVIS, le second tour d'une
            # boucle est deja vu et le parcours converge. Le prix est dit :
            # un champ atteint seulement au Nieme tour n'est pas rendu -- le
            # releve reste un MINORANT, ce qui est le contrat annonce.
            cle = (adr, frozenset(alias), frozenset(pile))
            if cle in vus:
                break
            vus.add(cle)
            insn = insns.get(adr)
            if insn is None:
                break
            act = un_pas(md, insn, alias, pile, cadre, trouves)
            if not alias and not pile:
                break
            if act == 'arret':
                break
            if isinstance(act, tuple):
                quoi, c = act
                if quoi == 'saut':
                    if c not in insns:
                        break
                    adr = c
                    continue
                if c in insns:           # conditionnel : les DEUX cotes
                    travail.append((c, dict(alias), dict(pile)))
            adr += 4
    return trouves


_CACHE = {}


def _reg(md, nom):
    """Le numero capstone d'un registre, par son nom."""
    if not _CACHE:
        for n in range(1, 400):
            try:
                _CACHE[md.reg_name(n)] = n
            except Exception:
                pass
    return _CACHE.get(nom)


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    chemin = IMAGE_2007
    if '--image' in a:
        k = a.index('--image')
        chemin = a[k + 1]
        del a[k:k + 2]
    champs = None
    if '--champ' in a:
        k = a.index('--champ')
        champs = set()
        j = k + 1
        while j < len(a) and not a[j].startswith('--'):
            champs.add(int(a[j], 0))
            j += 1
        del a[k:j]
    limite = 160
    if '--limite' in a:
        k = a.index('--limite')
        limite = int(a[k + 1], 0)
        del a[k:k + 2]
    ecritures = '--ecritures' in a
    cibles = [int(x, 0) for x in a if not x.startswith('--')]

    graphe = '--graphe' in a
    img = x360_ppc.Image(chemin)
    fcts = fonctions_pdata(chemin) if graphe else None
    md = capstone.Cs(capstone.CS_ARCH_PPC,
                     capstone.CS_MODE_32 | capstone.CS_MODE_BIG_ENDIAN)
    md.detail = True
    print('image : %s' % os.path.basename(chemin))

    for cible in cibles:
        sites = sites_bl(img, cible)
        print()
        print('=== 0x%08X : %d appelant(s) ===' % (cible, len(sites)))
        par_champ = {}
        for s in sites:
            lst = (suivre_graphe(img, md, s, fcts) if graphe
                   else suivre(img, md, s, limite))
            for va, m, ops, off, ecr, idx in lst:
                if champs is not None and off not in champs:
                    continue
                if ecritures and not ecr:
                    continue
                par_champ.setdefault(off, []).append((va, m, ops, ecr, idx, s))
        if not par_champ:
            print('  aucun acces retenu')
            continue
        for off in sorted(par_champ):
            lst = par_champ[off]
            necr = sum(1 for x in lst if x[3])
            print('  +0x%-5X %2d acces, dont %d ECRITURE(S)' % (off, len(lst), necr))
            for va, m, ops, ecr, idx, s in sorted(lst):
                etat = 'ECRIT' if ecr else ('PASSE' if m.startswith('ARG')
                                            else 'lit')
                print('      0x%08X  %-5s %-7s %-24s%s  [appel 0x%08X]'
                      % (va, etat, m, ops,
                         ' INDEXE' if idx else '', s))
    return 0


if __name__ == '__main__':
    sys.exit(main())
