#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Greffer une section AVEC SES RELOCATIONS, et non plus sans.

POURQUOI CET OUTIL EXISTE
-------------------------

Tout ce qu'on a greffé jusqu'ici a payé la même contrainte : **une section
ajoutée n'a aucune relocation**. La DLL est rebasée à l'exécution
(`0x7FFDB0620000` lors de la mesure du 2026-09-08), et une adresse d'image
écrite dans une section neuve reste à la base préférée `0x180000000` : elle ne
désigne plus rien. D'où la règle du chantier, « aucun pointeur absolu dans la
greffe », et tout le code RIP-relatif qui en découle.

Cette contrainte a fini par bloquer le chantier des décors. Un descripteur de
décor porte **dix-sept pointeurs** ; un emplacement d'essai n'en a que sept
relogés. Cloner celui du dojo dans un emplacement d'essai laissait donc dix
champs à mettre à zéro — dont `+0xC0`, **la table des murs**, et les neuf
reprises de musique. Ce n'était pas un détail : un dojo sans ses murs, c'est un
ring-out là où il n'y en a pas.

LA LEVÉE, ET ELLE EST SIMPLE
----------------------------

La table de relocations n'est pas une propriété de la section `.reloc` : c'est
un **couple (RVA, taille) dans le répertoire de données**, entrée 5, à
`optional_header + 152` en PE32+. Le chargeur lit ce couple, pas la section.

On peut donc :

  1. lire les 209 blocs d'origine (29 720 entrées) ;
  2. y ajouter les nôtres ;
  3. écrire le tout dans une section neuve ;
  4. repointer le répertoire de données.

À partir de là, **une section greffée a des relocations comme n'importe quelle
section du jeu**, et un pointeur absolu y devient légitime.

CE QUI EST VÉRIFIÉ, ET COMMENT
------------------------------

`--essai` fait le tour complet sur une copie de `.origine` : il greffe une
section, y écrit des pointeurs témoins, reconstruit la table, puis **relit le
binaire avec pefile** et contrôle que

  * les 29 720 entrées d'origine sont toutes là, à la même page et au même
    décalage — on n'en perd aucune ;
  * les entrées neuves y sont, de type 10 (`DIR64`) ;
  * un rebasage simulé corrige bien les pointeurs témoins.

C'est le seul moyen d'être sûr sans lancer le jeu, et cela vaut mieux : une
table de relocations fausse ne donne pas un message, elle donne un plantage au
chargement.

USAGE
-----

    import pe_sections

    va, off = pe_sections.ajouter_section(chemin, b'.decors\x00', 0x10000)
    ...  # on écrit le contenu, en notant les VA qui portent un pointeur
    pe_sections.reconstruire_relocations(chemin, va_a_reloger)

    py -3 tools/pe_sections.py --essai        (l'auto-contrôle)
    py -3 tools/pe_sections.py --etat <dll>   (sections et relocations)
"""
import os
import shutil
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
ORIGINE = os.path.join(JEU, 'vf5fs-pxd-w64-Retail_APM3.dll.origine')

# PE32+ : les décalages dont on se sert, tous comptés depuis l'en-tête optionnel
OPT_IMAGE_BASE = 24
OPT_ALIGN_SEC = 32
OPT_ALIGN_FIC = 36
OPT_TAILLE_IMAGE = 56
OPT_TAILLE_ENTETES = 60
OPT_NB_REPERTOIRES = 108
OPT_REPERTOIRES = 112
REPERTOIRE_RELOC = 5

# Caractéristiques usuelles. Les tables de décors sont des DONNÉES en lecture
# seule : pas d'exécution, pas d'écriture. La greffe de code, elle, prend
# 0xE0000020 (code + lecture + écriture + exécution) — c'est `patch_moteur.py`
# qui la pose, pas nous.
CARAC_DONNEES = 0x40000040          # initialisées, lecture
CARAC_RELOC = 0x42000040            # initialisées, lecture, rejetables

TYPE_DIR64 = 10                     # IMAGE_REL_BASED_DIR64
TYPE_ABSOLU = 0                     # IMAGE_REL_BASED_ABSOLUTE, le bourrage


class Pe:
    """Le strict nécessaire pour greffer : en-têtes, sections, répertoires.

    On n'utilise pas `pefile` ici — il sait lire, pas réécrire des en-têtes —
    mais l'auto-contrôle, lui, relit avec `pefile` : l'outil qui écrit ne doit
    pas être celui qui se donne raison.
    """

    def __init__(self, chemin):
        self.chemin = chemin
        with open(chemin, 'rb') as fp:
            self.entetes = bytearray(fp.read(0x1000))
        self.e_lfanew = struct.unpack_from('<I', self.entetes, 0x3C)[0]
        if self.entetes[self.e_lfanew:self.e_lfanew + 4] != b'PE\x00\x00':
            raise ValueError('%s n est pas un PE' % chemin)
        self.n_sec = struct.unpack_from('<H', self.entetes, self.e_lfanew + 6)[0]
        taille_opt = struct.unpack_from('<H', self.entetes, self.e_lfanew + 20)[0]
        self.opt = self.e_lfanew + 24
        self.table = self.opt + taille_opt
        self.base = self._u64(OPT_IMAGE_BASE)
        self.align_sec = self._u32(OPT_ALIGN_SEC)
        self.align_fic = self._u32(OPT_ALIGN_FIC)

    # --- lectures d'en-tête -------------------------------------------------
    def _u32(self, o):
        return struct.unpack_from('<I', self.entetes, self.opt + o)[0]

    def _u64(self, o):
        return struct.unpack_from('<Q', self.entetes, self.opt + o)[0]

    def _pose32(self, o, v):
        struct.pack_into('<I', self.entetes, self.opt + o, v)

    def sections(self):
        for i in range(self.n_sec):
            h = self.table + i * 40
            yield {
                'nom': bytes(self.entetes[h:h + 8]),
                'vsize': struct.unpack_from('<I', self.entetes, h + 8)[0],
                'va': struct.unpack_from('<I', self.entetes, h + 12)[0],
                'rsize': struct.unpack_from('<I', self.entetes, h + 16)[0],
                'roff': struct.unpack_from('<I', self.entetes, h + 20)[0],
                'carac': struct.unpack_from('<I', self.entetes, h + 36)[0],
                '_h': h,
            }

    def section_par_nom(self, nom):
        for s in self.sections():
            if s['nom'] == nom:
                return s
        return None

    def repertoire(self, k):
        o = self.opt + OPT_REPERTOIRES + k * 8
        return struct.unpack_from('<II', self.entetes, o)

    def poser_repertoire(self, k, rva, taille):
        o = self.opt + OPT_REPERTOIRES + k * 8
        struct.pack_into('<II', self.entetes, o, rva, taille)

    def ecrire_entetes(self):
        with open(self.chemin, 'r+b') as fp:
            fp.seek(0)
            fp.write(bytes(self.entetes))

    def lire(self, rva, n):
        for s in self.sections():
            if s['va'] <= rva < s['va'] + max(s['vsize'], s['rsize']):
                o = s['roff'] + (rva - s['va'])
                with open(self.chemin, 'rb') as fp:
                    fp.seek(o)
                    return fp.read(n)
        raise KeyError('RVA 0x%X hors sections' % rva)


def _aligner(v, a):
    return (v + a - 1) & ~(a - 1)


def ajouter_section(chemin, nom, taille, carac=CARAC_DONNEES):
    """Greffe une section, ou retrouve celle qui porte déjà ce nom.

    Rend `(va_absolue, offset_fichier)`. `nom` fait exactement huit octets,
    complétés par des zéros — c'est le champ du format, pas une convention.
    """
    if len(nom) != 8:
        raise ValueError('un nom de section fait huit octets, pas %d' % len(nom))
    pe = Pe(chemin)
    deja = pe.section_par_nom(nom)
    if deja is not None:
        if deja['rsize'] < taille:
            raise AssertionError(
                'la section %r existe deja mais ne fait que %d octets, on en '
                'demande %d' % (nom.rstrip(b'\x00'), deja['rsize'], taille))
        return pe.base + deja['va'], deja['roff']

    h_neuf = pe.table + pe.n_sec * 40
    fin_entetes = struct.unpack_from('<I', pe.entetes,
                                     pe.opt + OPT_TAILLE_ENTETES)[0]
    if h_neuf + 40 > fin_entetes:
        raise AssertionError(
            'plus de place pour un en-tete de section : la table finirait en '
            '0x%X et les en-tetes s arretent a 0x%X' % (h_neuf + 40, fin_entetes))

    derniere = list(pe.sections())[-1]
    va = _aligner(derniere['va'] + derniere['vsize'], pe.align_sec)
    rsize = _aligner(taille, pe.align_fic)

    with open(chemin, 'r+b') as fp:
        fp.seek(0, 2)
        off = fp.tell()
        if off % pe.align_fic:
            fp.write(b'\x00' * (pe.align_fic - off % pe.align_fic))
            off = fp.tell()
        fp.write(b'\x00' * rsize)

    struct.pack_into('<8s', pe.entetes, h_neuf, nom)
    struct.pack_into('<I', pe.entetes, h_neuf + 8, taille)      # VirtualSize
    struct.pack_into('<I', pe.entetes, h_neuf + 12, va)         # VirtualAddress
    struct.pack_into('<I', pe.entetes, h_neuf + 16, rsize)      # SizeOfRawData
    struct.pack_into('<I', pe.entetes, h_neuf + 20, off)        # PointerToRawData
    struct.pack_into('<I', pe.entetes, h_neuf + 36, carac)
    struct.pack_into('<H', pe.entetes, pe.e_lfanew + 6, pe.n_sec + 1)
    pe._pose32(OPT_TAILLE_IMAGE, _aligner(va + taille, pe.align_sec))
    pe.ecrire_entetes()
    return pe.base + va, off


def lire_relocations(chemin):
    """Rend `[(page_rva, [(type, decalage), ...]), ...]`, dans l'ordre du fichier."""
    pe = Pe(chemin)
    rva, taille = pe.repertoire(REPERTOIRE_RELOC)
    if not rva:
        return []
    brut = pe.lire(rva, taille)
    blocs, o = [], 0
    while o + 8 <= len(brut):
        page, n = struct.unpack_from('<II', brut, o)
        if n < 8:
            break                      # bloc vide : fin de table
        entrees = []
        for k in range(o + 8, o + n, 2):
            v = struct.unpack_from('<H', brut, k)[0]
            entrees.append((v >> 12, v & 0xFFF))
        blocs.append((page, entrees))
        o += n
    return blocs


def _assembler(blocs):
    """Sérialise des blocs. La taille d'un bloc DOIT être multiple de quatre :
    un bourrage `ABSOLUTE` est ajouté quand le nombre d'entrées est impair.
    C'est ce que fait l'éditeur de liens, et le chargeur n'accepte rien d'autre.
    """
    out = bytearray()
    for page, entrees in blocs:
        e = list(entrees)
        if len(e) % 2:
            e.append((TYPE_ABSOLU, 0))
        n = 8 + 2 * len(e)
        out += struct.pack('<II', page, n)
        for t, d in e:
            out += struct.pack('<H', (t << 12) | d)
    return bytes(out)


def reconstruire_relocations(chemin, va_a_reloger, nom=b'.reloc2\x00'):
    """Réécrit la table entière — l'originale PLUS nos adresses — ailleurs.

    `va_a_reloger` : les adresses VIRTUELLES ABSOLUES (base comprise) des
    qwords qui portent un pointeur d'image dans nos sections greffées.

    Rend `(rva, taille)` de la nouvelle table.
    """
    pe = Pe(chemin)
    blocs = lire_relocations(chemin)
    n_avant = sum(len(e) for _, e in blocs)

    # nos entrées, groupées par page de 4 Ko et triées : le chargeur parcourt
    # la table dans l'ordre, et les pages croissantes sont la convention.
    par_page = {}
    for va in va_a_reloger:
        rva = va - pe.base
        if rva & 7:
            raise AssertionError('0x%X n est pas aligne sur huit octets' % va)
        par_page.setdefault(rva & ~0xFFF, []).append(rva & 0xFFF)
    for page in sorted(par_page):
        entrees = [(TYPE_DIR64, d) for d in sorted(set(par_page[page]))]
        blocs.append((page, entrees))

    brut = _assembler(blocs)
    # La table se décrit elle-même par (RVA, taille) : elle peut vivre
    # n'importe où. On la met dans une section à elle, jamais dans `.reloc`,
    # dont le mou (328 octets) ne tiendrait pas nos blocs.
    va, off = ajouter_section(chemin, nom, len(brut), CARAC_RELOC)
    with open(chemin, 'r+b') as fp:
        fp.seek(off)
        fp.write(brut)
    pe = Pe(chemin)                    # relire : la section vient d'être ajoutée
    pe.poser_repertoire(REPERTOIRE_RELOC, va - pe.base, len(brut))
    pe.ecrire_entetes()
    n_apres = sum(len(e) for _, e in lire_relocations(chemin))
    if n_apres < n_avant + len(set(va_a_reloger)):
        raise AssertionError('relecture : %d entrees, attendu au moins %d'
                             % (n_apres, n_avant + len(set(va_a_reloger))))
    return va - pe.base, len(brut)


# ---------------------------------------------------------------------------
# L'AUTO-CONTRÔLE
#
# Il relit avec `pefile`, pas avec le code ci-dessus : un outil qui se relit
# lui-même ne prouve rien. Et il simule le rebasage, parce que c'est la seule
# chose qui compte vraiment.
# ---------------------------------------------------------------------------
def essai():
    import pefile

    tmp = os.path.join(RACINE, 'extracted', '_essai_sections.dll')
    shutil.copy2(ORIGINE, tmp)

    avant = pefile.PE(ORIGINE, fast_load=True)
    avant.parse_data_directories(directories=[
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_BASERELOC']])
    ref = set()
    for b in avant.DIRECTORY_ENTRY_BASERELOC:
        for e in b.entries:
            if e.type:
                ref.add((e.rva, e.type))
    print('origine : %d sections, %d relocations utiles'
          % (avant.FILE_HEADER.NumberOfSections, len(ref)))

    TAILLE = 0x10000
    va, off = ajouter_section(tmp, b'.decors\x00', TAILLE)
    print('greffe  : .decors en 0x%X (offset fichier 0x%X), %d octets'
          % (va, off, TAILLE))

    # Trois pointeurs témoins : un au tout début, un au milieu, un sur la
    # dernière frontière de page utilisable (0xFF8) — c'est le cas limite,
    # celui où huit octets finissent exactement sur la fin de page.
    temoins = [(0x0000, avant.OPTIONAL_HEADER.ImageBase + 0x403430),
               (0x1008, avant.OPTIONAL_HEADER.ImageBase + 0x4067A0),
               (0x1FF8, avant.OPTIONAL_HEADER.ImageBase + 0x39F7A0)]
    with open(tmp, 'r+b') as fp:
        for d, cible in temoins:
            fp.seek(off + d)
            fp.write(struct.pack('<Q', cible))

    rva, taille = reconstruire_relocations(tmp, [va + d for d, _ in temoins])
    print('reloc   : table reecrite en RVA 0x%X, %d octets' % (rva, taille))

    apres = pefile.PE(tmp, fast_load=True)
    apres.parse_data_directories(directories=[
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_BASERELOC']])
    vu = set()
    for b in apres.DIRECTORY_ENTRY_BASERELOC:
        for e in b.entries:
            if e.type:
                vu.add((e.rva, e.type))
    print('apres   : %d sections, %d relocations utiles'
          % (apres.FILE_HEADER.NumberOfSections, len(vu)))

    fautes = []
    perdues = ref - vu
    if perdues:
        fautes.append('%d relocations d origine PERDUES (ex. 0x%X)'
                      % (len(perdues), sorted(perdues)[0][0]))
    for d, _ in temoins:
        cle = (va + d - apres.OPTIONAL_HEADER.ImageBase, TYPE_DIR64)
        if cle not in vu:
            fautes.append('le temoin +0x%X n est pas dans la table' % d)
    if apres.OPTIONAL_HEADER.SizeOfImage < (va - apres.OPTIONAL_HEADER.ImageBase
                                            + TAILLE):
        fautes.append('SizeOfImage trop petit')

    # LE REBASAGE SIMULÉ. C'est le seul contrôle qui vaut : on applique le
    # delta comme le chargeur, et on regarde si nos témoins tombent juste.
    delta = 0x7FFDB0620000 - apres.OPTIONAL_HEADER.ImageBase
    brut = bytearray(open(tmp, 'rb').read())
    sec = None
    for s in apres.sections:
        if s.Name.rstrip(b'\x00') == b'.decors':
            sec = s
    corrigees = 0
    for b in apres.DIRECTORY_ENTRY_BASERELOC:
        for e in b.entries:
            if e.type != TYPE_DIR64:
                continue
            r = e.rva
            if not (sec.VirtualAddress <= r < sec.VirtualAddress + TAILLE):
                continue
            o = sec.PointerToRawData + (r - sec.VirtualAddress)
            v = struct.unpack_from('<Q', brut, o)[0]
            struct.pack_into('<Q', brut, o, (v + delta) & 0xFFFFFFFFFFFFFFFF)
            corrigees += 1
    for d, cible in temoins:
        o = sec.PointerToRawData + (va - apres.OPTIONAL_HEADER.ImageBase
                                    - sec.VirtualAddress) + d
        v = struct.unpack_from('<Q', brut, o)[0]
        if v != cible + delta:
            fautes.append('temoin +0x%X : 0x%X au lieu de 0x%X'
                          % (d, v, cible + delta))
    print('rebasage simule : %d pointeurs corriges dans .decors' % corrigees)

    print()
    if fautes:
        print('%d FAUTE(S) :' % len(fautes))
        for f in fautes:
            print('   . %s' % f)
        return 1
    print('AUCUNE FAUTE. Les %d relocations d origine sont conservees, les '
          'trois temoins' % len(ref))
    print('sont relogeables, et le rebasage simule les corrige tous les trois.')
    print('Fichier d essai : %s' % tmp)
    return 0


def etat(chemin):
    pe = Pe(chemin)
    print('%s' % chemin)
    print('  base 0x%X, alignements %d / %d' % (pe.base, pe.align_sec,
                                                pe.align_fic))
    fin = pe.table + pe.n_sec * 40
    entetes = struct.unpack_from('<I', pe.entetes, pe.opt + OPT_TAILLE_ENTETES)[0]
    print('  %d sections ; place pour %d en-tete(s) de plus'
          % (pe.n_sec, (entetes - fin) // 40))
    for s in pe.sections():
        print('    %-10s VA 0x%09X  vsize %9d  raw 0x%08X  carac %08X'
              % (s['nom'].rstrip(b'\x00').decode(), pe.base + s['va'],
                 s['vsize'], s['roff'], s['carac']))
    rva, taille = pe.repertoire(REPERTOIRE_RELOC)
    blocs = lire_relocations(chemin)
    print('  relocations : RVA 0x%X, %d octets, %d blocs, %d entrees utiles'
          % (rva, taille, len(blocs),
             sum(1 for _, e in blocs for t, _ in e if t)))
    return 0


def main():
    argv = sys.argv[1:]
    if '--essai' in argv:
        return essai()
    if '--etat' in argv:
        i = argv.index('--etat') + 1
        return etat(argv[i] if i < len(argv) else ORIGINE)
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
