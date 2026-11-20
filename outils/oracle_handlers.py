#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fait executer les gestionnaires de codes de mothead par le moteur lui-meme.

La DLL du build APM3 n'a que des imports systeme : elle se charge dans un processus
Python ordinaire. On y fabrique un faux combattant (ROB) entierement a zero, on
appelle un gestionnaire avec une charge utile marquee, et on releve les octets de
l'etat qui ont change. Cela ne dit pas QUI lit un champ, mais cela confirme
dynamiquement CE QUI EST ECRIT par chaque code, sans desassemblage.

Convention d'appel, tiree du repartiteur (docs/formats/mothead.md section 4) :
    handler(rcx = &ctx, rdx = charge utile, r8 = entree de 8 octets)
    ctx[0] = ROB          ctx[1] = ROB + 0x338          ctx[2] = ROB + 0x798 (l'etat)

Chaque code est essaye dans un sous-processus : un gestionnaire qui touche un global
non initialise plante, et le plantage ne doit pas emporter le releve des autres.

Usage :
    py -3 tools/oracle_handlers.py               tous les codes, tableau comparatif
    py -3 tools/oracle_handlers.py --code 54     un seul code, detail
"""
import ctypes
import json
import os
import struct
import subprocess
import sys

DLL = 'runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll'
VA_TABLE = 0x1803F95B0        # table des 84 gestionnaires, trouvee par la forme du repartiteur
IMAGE_BASE = 0x180000000

ROB_SIZE = 0x20000
# ATTENTION : ces deux offsets sont ceux du build R.E.V.O. Dans le build APM3, que cet
# oracle charge, l'etat est a ROB+0x8A0 et ctx[1] a ROB+0x440 (lu dans MothApplyRecord
# 0x180158B40, voir analysis/fenetres_temporelles.md). Cela ne fausse PAS les releves :
# l'oracle fabrique lui-meme le contexte, et les gestionnaires ne font qu'utiliser les
# pointeurs recus. Seuls les libelles imprimes suivent cette convention.
ST = 0x798                    # position de l'etat dans le faux ROB de l'oracle
CTX1 = 0x338
PAYLOAD = 128


def handler_addrs(base):
    """Les 84 adresses, lues dans la DLL chargee."""
    out = []
    for k in range(84):
        v = ctypes.c_uint64.from_address(base + (VA_TABLE - IMAGE_BASE) + 8 * k).value
        out.append(v)
    return out


def run_one(code):
    dll = ctypes.WinDLL(os.path.abspath(DLL))
    base = dll._handle
    h = handler_addrs(base)[code]
    if not h:
        return {'code': code, 'handler': None, 'etat': 'aucun gestionnaire'}

    rob = ctypes.create_string_buffer(ROB_SIZE)
    robp = ctypes.addressof(rob)
    ctx = (ctypes.c_uint64 * 3)(robp, robp + CTX1, robp + ST)

    # [entree(8) | terminateur(8) | charge utile(128)] dans un seul tampon
    lst = ctypes.create_string_buffer(16 + PAYLOAD)
    lp = ctypes.addressof(lst)
    pay = lp + 16
    struct.pack_into('<Ii', lst, 0, code, (pay - (lp + 4)))   # code, offset auto-relatif
    struct.pack_into('<Ii', lst, 8, 0xFFFFFFFF, 0)            # fin de liste
    for i in range(PAYLOAD):                                   # charge marquee : 1, 2, 3...
        lst[16 + i] = bytes([(i + 1) & 0xFF])

    avant = bytes(rob)
    F = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(h)
    F(ctypes.addressof(ctx), pay, lp)
    apres = bytes(rob)

    # mots de 4 octets modifies : un flottant dont l'octet de poids faible est nul
    # ferait autrement demarrer la plage un octet trop loin
    mots = sorted({(i // 4) * 4 for i in range(ROB_SIZE) if avant[i] != apres[i]})
    diffs = [(m, apres[m:m + 4].hex()) for m in mots]
    return {'code': code, 'handler': '0x%X' % (h - base + IMAGE_BASE),
            'diffs': [[a, b] for a, b in diffs]}


def libelle(off):
    if off >= ST:
        return 'etat+0x%03X' % (off - ST)
    if off >= CTX1:
        return 'ctx1+0x%03X' % (off - CTX1)
    return 'ROB+0x%03X' % off


def statiques():
    """Offsets attendus, deduits statiquement de la DLL R.E.V.O. (session precedente)."""
    p = 'analysis/mothead_opcodes.csv'
    import csv
    import io
    out = {}
    for r in csv.DictReader(io.open(p, encoding='utf-8')):
        if r['liste'] == '1' and r['champ_etat']:
            out[int(r['code'])] = r['champ_etat']
    return out


def main():
    if '--code' in sys.argv:
        code = int(sys.argv[sys.argv.index('--code') + 1])
        res = run_one(code)
        if '--json' in sys.argv:
            print(json.dumps(res))
        else:
            print('code %d, gestionnaire %s' % (code, res.get('handler')))
            for off, hx in res.get('diffs', []):
                print('   %-14s %s' % (libelle(off), hx))
        return 0

    attendu = statiques()
    import re
    stat = {}
    for c, txt in attendu.items():
        stat[c] = sorted(int(x, 16) for x in re.findall(r'0x([0-9A-Fa-f]{3})', txt))
    tot = {'identique': 0, 'decale 0x18': 0, 'decale 0x78': 0,
           'a voir': 0, 'rien ecrit': 0, 'plantage': 0, 'aucun': 0}
    print("L'oracle tourne sur le build APM3 (2021). Les offsets documentes viennent du")
    print("build R.E.V.O. (2025) : deux tableaux ont grossi entre les deux, d'ou les decalages.")
    print()
    print('%-5s %-12s %-14s %s' % ('code', 'gestionnaire', 'verdict', 'champs ecrits (APM3)'))
    for code in range(84):
        r = subprocess.run([sys.executable, __file__, '--code', str(code), '--json'],
                           capture_output=True, text=True, timeout=60)
        if r.returncode != 0 or not r.stdout.strip():
            print('%-5d %-12s %-14s' % (code, '', 'PLANTAGE'))
            tot['plantage'] += 1
            continue
        d = json.loads(r.stdout.strip().splitlines()[-1])
        if d.get('handler') is None:
            print('%-5d %-12s %-14s' % (code, '-', 'aucun'))
            tot['aucun'] += 1
            continue
        obs = sorted(o - ST for o, _ in d['diffs'] if o >= ST)
        att = stat.get(code, [])
        if not obs:
            v = 'rien ecrit'
        elif att and obs[0] == att[0]:
            v = 'identique'
        elif att and obs[0] + 0x18 == att[0]:
            v = 'decale 0x18'
        elif att and obs[0] + 0x78 == att[0]:
            v = 'decale 0x78'
        else:
            v = 'a voir'
        tot[v] += 1
        print('%-5d %-12s %-14s %s' % (code, d['handler'], v,
                                       ' '.join('%03X' % o for o in obs)[:80]))
    print()
    for k, n in tot.items():
        if n:
            print('  %-12s %d' % (k, n))
    return 0


if __name__ == '__main__':
    sys.exit(main())
