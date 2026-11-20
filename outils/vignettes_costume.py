#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""LES SIX VIGNETTES NOIRES DE « Costume settings ».

Constat de Frederic, a l'ecran, le 2026-09-30 :

    « l'ecran costume settings n'affiche pas les images des differents
      costumes »

-- les six cases Type A..S sont NOIRES, alors que leurs libelles s'affichent.

CE QUE LE CODE DIT, et il le dit entierement.

`0x1801C8F60` dessine la page. Pour chaque case elle fait :

    0x1801C929B  rcx = [r14]                 ; la page
    0x1801C929E  call 0x1801CB030            ; -> ax = L'IDENTIFIANT du sprite
    0x1801C92A3  movzx ebx, ax
    0x1801C92AA  call 0x180189880(desc)      ; preparer le descripteur
    0x1801C92AF  [desc+0x04] = ebx           ; <- l'identifiant
    0x1801C92B9  [desc+0x34] = position
    0x1801C92C8  [desc+0x0C] = 0x400000      ; drapeaux
    0x1801C92E3  call 0x180187C00(desc)      ; dessiner

et `0x1801CB030` est une TABLE 19 x 6 D'IDENTIFIANTS DE SPRITE, batie sur la
PILE a chaque appel -- le meme idiome que la table d'entrees de menu du
§1.3 de `customize_0x299.md`. C'est pour cela qu'aucun balayage de donnees
ne la trouvait :

    0x1801CB2C6  call 0x1801C3830 ; call 0x1801C3460   ; -> le PERSONNAGE
    0x1801CB2D5  cmp rbx, 6 ; cmovb rdx, rbx           ; le TYPE, borne a 6
    0x1801CB2E7  cmp eax, 0x12 ; cmovg eax, ecx        ; le perso, borne a 18
    0x1801CB2F0  rax = [rbp + perso*8 + 0x50]          ; la ligne du perso
    0x1801CB2F5  eax = word [rax + type*2]             ; L'IDENTIFIANT
    0x1801CB301  ret

Cet outil reconstruit la table en SIMULANT les ecritures immediates de la
fonction (rbp = rsp + 0x100 : `lea rbp,[rsp-0x100]` apres un `push`, puis
`sub rsp,0x200`), puis confronte chaque identifiant a la base de sprites que
le jeu lit reellement.

    py -3 tools/vignettes_costume.py            la table et le verdict
    py -3 tools/vignettes_costume.py --table    la table seule
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import pe_disasm as P                                        # noqa: E402
import boutons_terminal as B                                 # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')
FOURNISSEUR = 0x1801CB030        # la fonction qui rend l'identifiant
TABLE_PTR = 0x50                 # [rbp + 0x50 + perso*8] = la ligne
N_PERSO, N_TYPE = 19, 6
RBP_MOINS_RSP = 0x100            # mesure sur le prologue, voir le docstring
TYPES = ['Type A', 'Type B', 'Type C', 'Type D', 'Type E', 'Type S']
# L'ordre des personnages de FS, tel que la grille les numerote. Il sert a
# LIRE la table, pas a la produire : si l'ordre etait faux, les identifiants
# resteraient les memes, seuls les noms de lignes bougeraient.
PERSOS = ['Akira', 'Pai', 'Lau', 'Wolf', 'Jeffry', 'Kage', 'Sarah', 'Jacky',
          'Shun', 'Lion', 'Aoi', 'Lei-Fei', 'Vanessa', 'Brad', 'Goh',
          'Eileen', 'El Blaze', 'Jean', 'Taka-Arashi']


def reconstruire(img):
    """Rend {perso: [6 identifiants]} en simulant la fonction."""
    frag = B.fonction_de(B.pdata(img), FOURNISSEUR)
    if frag is None:
        raise SystemExit('0x%X introuvable dans .pdata' % FOURNISSEUR)
    deb, fin = frag
    off = img.va2off(deb)
    mem = {}                     # offset depuis rsp -> octet
    ptr = {}                     # index -> offset de la ligne
    reg = {}                     # nom de registre -> offset (pour les `lea`)

    def poser(base, delta, val, n):
        a = base + delta
        for k in range(n):
            mem[a + k] = (val >> (8 * k)) & 0xFF

    def depuis(txt):
        """« rsp + 0x20 », « rbp - 0x40 », « rbp » -> l'offset depuis rsp."""
        t = txt.strip().strip('[]')
        base = RBP_MOINS_RSP if t.startswith('rbp') else 0
        reste = t[3:].strip()
        if not reste:
            return base
        signe = -1 if reste[0] == '-' else 1
        return base + signe * int(reste[1:].strip(), 0)

    for i in img.md.disasm(img.data[off:off + (fin - deb)], deb):
        m, o = i.mnemonic, i.op_str
        if m == 'lea' and ', [' in o:
            r, src = o.split(', [', 1)
            if src.rstrip(']').strip().startswith(('rsp', 'rbp')):
                reg[r.strip()] = depuis(src)
            continue
        if m != 'mov' or not o.startswith(('dword ptr [', 'qword ptr [')):
            continue
        taille = 4 if o.startswith('dword') else 8
        cible, src = o.split('], ', 1)
        cible = cible.split('[', 1)[1]
        if not cible.strip().startswith(('rsp', 'rbp')):
            continue
        a = depuis(cible)
        if src.startswith('0x') or src.isdigit():
            poser(a, 0, int(src, 0), taille)
        elif src in reg and taille == 8:
            # la table de pointeurs : [rbp + 0x50 + i*8] = &ligne
            d = a - RBP_MOINS_RSP - TABLE_PTR
            if d >= 0 and d % 8 == 0:
                ptr[d // 8] = reg[src]
    out = {}
    for p in range(N_PERSO):
        if p not in ptr:
            continue
        base = ptr[p]
        ids = []
        for t in range(N_TYPE):
            b = [mem.get(base + 2 * t + k) for k in (0, 1)]
            ids.append(None if None in b else b[0] | (b[1] << 8))
        out[p] = ids
    return out


def sprites_du_jeu():
    """{identifiant: nom} de la base de sprites que le moteur lit vraiment.

    Si `rom/2d/spr_db.bin` existe (c'est le cas des que `--bases-2d-libres`
    a masque les noms dans l'archive embarquee), c'est CELLE-LA que le jeu
    ouvre. Sinon, celle qui est dans le binaire.
    """
    import bases_2d as BD
    chemin = os.path.join(BD.DEUXD, 'spr_db.bin')
    if os.path.exists(chemin):
        d, source = open(chemin, 'rb').read(), os.path.relpath(chemin, RACINE)
    else:
        d, source = BD.bases_origine()['spr_db.bin'], 'l archive embarquee'
    _, sec = BD.lire_base(d, 0x10, 0x0C)
    return {e[0]: e[1] for e in sec}, source, len(sec)


def main():
    argv = sys.argv[1:]
    img = P.Image(MOTEUR)
    table = reconstruire(img)
    print()
    print('LES VIGNETTES DE « Costume settings » -- la table 19 x 6 de '
          '0x%X' % FOURNISSEUR)
    print()
    if not table:
        print('REFUS : la table n a pas pu etre reconstruite.')
        return 2

    connus, source, total = ({}, '(non lue)', 0)
    if '--table' not in argv:
        try:
            connus, source, total = sprites_du_jeu()
        except Exception as e:                               # noqa: BLE001
            print('la base de sprites n a pas pu etre lue : %s: %s'
                  % (type(e).__name__, e))
            print()

    print('%-14s %s' % ('personnage', '  '.join('%-7s' % t for t in TYPES)))
    print('-' * 74)
    manquants, presents = [], []
    for p in sorted(table):
        nom = PERSOS[p] if p < len(PERSOS) else '?%d' % p
        cases = []
        for t, i in enumerate(table[p]):
            if i is None:
                cases.append('  --   ')
                continue
            marque = ' ' if not connus else ('.' if i in connus else '!')
            cases.append('0x%04X%s' % (i, marque))
            (presents if i in connus else manquants).append((p, t, i))
        print('%-14s %s' % (nom, '  '.join(cases)))
    print()
    if not connus:
        print('(base de sprites non consultee : --table)')
        return 0
    print('Base de sprites lue : %s -- %d sprites declares.' % (source, total))
    print('   « . » = l identifiant EXISTE dans la base')
    print('   « ! » = il N Y EST PAS')
    print()
    print('%d identifiant(s) present(s), %d ABSENT(S).'
          % (len(presents), len(manquants)))
    print()
    if presents:
        print('Exemples de ceux qui existent :')
        for p, t, i in presents[:8]:
            print('   %-12s %-7s 0x%04X  %s'
                  % (PERSOS[p] if p < len(PERSOS) else p, TYPES[t], i,
                     connus[i]))
        print()
    if manquants:
        vus = sorted({i for _, _, i in manquants})
        print('Les identifiants absents (%d distincts) : %s%s'
              % (len(vus), ' '.join('0x%04X' % i for i in vus[:24]),
                 ' ...' if len(vus) > 24 else ''))
        print()
        print('VERDICT : les cases sont noires parce que le moteur demande')
        print('des sprites que sa base ne declare pas. Ce ne sont pas des')
        print('images mal placees : elles n existent pas.')
    else:
        print('VERDICT : tous les identifiants existent dans la base. Les')
        print('cases noires viennent donc d ailleurs -- du CHARGEMENT de la')
        print('planche, pas de son declaratif.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
