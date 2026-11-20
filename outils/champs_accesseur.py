#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""TOUS LES CHAMPS d'une structure rendue par un ACCESSEUR, bases decalees
comprises.

POURQUOI IL MANQUAIT (2026-10-04). On veut agrandir le tableau de cases de
« select item ». La structure est a adresse fixe et `0x1801C3650` en est
l'unique fournisseur (`lea rax, 0x180752260` ; sept appelants). Mais
l'agrandir veut dire DEPLACER des champs, et les deplacements sont codes en
dur dans les instructions : en rater un seul, c'est corrompre la memoire en
silence.

Les deux outils existants ne suffisent pas, et chacun pour une raison de
principe :

  . `voisinage_x64.py` cherche par DEPLACEMENT. Or `0x1801C3650` ne laisse
    aucune reference RIP-relative a la structure : tout passe par l'appel. Et
    surtout, un champ atteint depuis une base DEJA DECALEE porte un autre
    deplacement -- du code qui tient `p = struct+0x60` ecrit `[p + i*4 +
    0x14]`, et le champ touche est `+0x74`. Le releve par deplacement ne le
    voit pas, c'est son second angle mort documente ;
  . `champs_globale.py` suit bien un registre vers l'avant, mais il part d'un
    POINTEUR GLOBAL charge en RIP-relatif. Ici la structure arrive par la
    valeur de retour d'une fonction, et elle est aussi passee EN ARGUMENT a
    une autre (`0x1801CC130` la recoit dans `rdx`).

CE QUE CELUI-CI FAIT, et c'est la seule facon d'obtenir un inventaire sur
lequel on puisse PATCHER :

  . il recense les `call <accesseur>` ;
  . il suit la valeur rendue vers l'avant avec un BIAIS par registre : non pas
    « ce registre porte la structure » mais « ce registre porte la structure
    PLUS k ». `mov rX, rY` recopie le biais, `lea rX, [rY + k]` l'augmente de
    k, `add rX, k` aussi ;
  . chaque acces memoire est donc rendu a son offset EFFECTIF, biais compris ;
  . et quand un registre suivi part en argument (`rcx`, `rdx`, `r8`, `r9`)
    dans un `call`, il descend dans la fonction appelee avec le biais, sur
    deux niveaux. C'est ce qui attrape `0x1801CC130`.

Le suivi s'arrete a `ret`, a un saut sortant, et des que le registre suivi est
REELLEMENT reecrit (`regs_access`, pas le premier operande : `test rdx, rdx`
n'ecrit rien).

CE QU'IL NE FAIT PAS, et c'est dit plutot que tu : il ne traverse pas un
champ qui serait RANGE en memoire puis relu ailleurs, et il ne suit pas un
index calcule. Un inventaire n'est une autorisation de patcher que si on
confronte son total au nombre de sites attendus.

Usage :
    py -3 tools/champs_accesseur.py 0x1801C3650
    py -3 tools/champs_accesseur.py 0x1801C3650 --min 0x274
    py -3 tools/champs_accesseur.py 0x1801C3650 --patche
"""
import os
import sys

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                        # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')

SUIVI_MAX = 400         # instructions suivies par depart
PROFONDEUR = 2          # niveaux d'appel traverses
ARGS = ('rcx', 'rdx', 'r8', 'r9')


def appelants(img, cible):
    """Les `call <cible>` directs, par balayage des fonctions de .pdata."""
    out = []
    for beg, blob in P.iter_code(img):
        for i in img.md.disasm(blob, beg):
            if i.mnemonic == 'call' and i.op_str.startswith('0x') \
                    and int(i.op_str, 16) == cible:
                out.append((beg, i.address + i.size))
    return out


def _corps(img, va, taille=0x1200):
    o = img.va2off(va)
    if o is None:
        return b''
    return img.data[o:o + taille]


def suivre(img, depart, biais_init, trouves, vus, profondeur):
    """Suit {registre: biais} depuis `depart`, en relevant les acces."""
    cle_depart = (depart, tuple(sorted(biais_init.items())))
    if cle_depart in vus or profondeur < 0:
        return
    vus.add(cle_depart)
    biais = dict(biais_init)
    blob = _corps(img, depart)
    if not blob:
        return
    for k, x in enumerate(img.md.disasm(blob, depart)):
        if k > SUIVI_MAX or x.mnemonic == 'ret':
            return
        if not biais:
            return
        noms = {}
        try:
            lus, ecrits = x.regs_access()
        except Exception:
            lus, ecrits = (), ()
        # --- les acces memoire, a leur offset EFFECTIF -------------------
        touche = set()
        for op in x.operands:
            if op.type != capstone.x86.X86_OP_MEM:
                continue
            base = (x.reg_name(op.mem.base) if op.mem.base else None)
            if base not in biais:
                continue
            touche.add(base)
            dep = biais[base] + op.mem.disp
            ech = op.mem.scale if op.mem.index else 0
            prem = x.operands[0]
            ecrit = (prem.type == capstone.x86.X86_OP_MEM
                     and prem.mem.disp == op.mem.disp
                     and prem.mem.base == op.mem.base
                     and x.mnemonic not in ('cmp', 'test', 'lea'))
            if x.mnemonic == 'lea':
                continue              # une derivation, traitee plus bas
            trouves.setdefault((dep, ech, ecrit), []).append(
                (x.address, '%s %s' % (x.mnemonic, x.op_str)))
        # --- les derivations : lea rX, [rY + k] --------------------------
        if x.mnemonic == 'lea' and x.operands:
            d = x.operands[0]
            m = x.operands[1]
            if d.type == capstone.x86.X86_OP_REG \
                    and m.type == capstone.x86.X86_OP_MEM and m.mem.base:
                b = x.reg_name(m.mem.base)
                if b in biais and not m.mem.index:
                    biais[x.reg_name(d.reg)] = biais[b] + m.mem.disp
                    continue
        # --- la recopie : mov rX, rY -------------------------------------
        if x.mnemonic == 'mov' and len(x.operands) == 2 \
                and x.operands[0].type == capstone.x86.X86_OP_REG \
                and x.operands[1].type == capstone.x86.X86_OP_REG:
            s = x.reg_name(x.operands[1].reg)
            d = x.reg_name(x.operands[0].reg)
            if s in biais:
                biais[d] = biais[s]
                continue
            biais.pop(d, None)
            continue
        # --- l'avance : add rX, imm -------------------------------------
        if x.mnemonic == 'add' and len(x.operands) == 2 \
                and x.operands[0].type == capstone.x86.X86_OP_REG \
                and x.operands[1].type == capstone.x86.X86_OP_IMM:
            d = x.reg_name(x.operands[0].reg)
            if d in biais:
                biais[d] += x.operands[1].imm
                continue
        # --- un appel : on descend si un suivi part en argument ---------
        if x.mnemonic == 'call':
            passes = {r: biais[r] for r in ARGS if r in biais}
            if passes and x.op_str.startswith('0x'):
                suivre(img, int(x.op_str, 16), passes, trouves, vus,
                       profondeur - 1)
            # convention Microsoft x64 : les volatils sont perdus
            for r in ('rax', 'rcx', 'rdx', 'r8', 'r9', 'r10', 'r11'):
                biais.pop(r, None)
            continue
        # --- un registre reecrit cesse de porter la structure ------------
        for r in ecrits:
            n = x.reg_name(r)
            if n in biais and n not in touche:
                biais.pop(n, None)
        for n in noms:
            biais.pop(n, None)


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    acc = int(a[0], 0)
    mini = int(a[a.index('--min') + 1], 0) if '--min' in a else 0
    chemin = MOTEUR + ('' if '--patche' in a else '.origine')
    img = P.Image(chemin)
    img.md.detail = True
    print('image : %s' % os.path.basename(chemin))
    sites = appelants(img, acc)
    print('accesseur 0x%X : %d appel(s)' % (acc, len(sites)))
    trouves, vus = {}, set()
    for fn, apres in sites:
        suivre(img, apres, {'rax': 0}, trouves, vus, PROFONDEUR)
    print('champs touches (offset EFFECTIF, biais compris) :')
    print('-' * 74)
    for (dep, ech, ecrit) in sorted(trouves):
        if dep < mini:
            continue
        sites_c = trouves[(dep, ech, ecrit)]
        print('  +0x%04X  %-6s %-5s %d site(s)'
              % (dep, 'x%d' % ech if ech else 'direct',
                 'ECRIT' if ecrit else 'lit', len(sites_c)))
        for adr, txt in sites_c:
            print('             0x%X  %s' % (adr, txt))
    return 0


if __name__ == '__main__':
    sys.exit(main())
