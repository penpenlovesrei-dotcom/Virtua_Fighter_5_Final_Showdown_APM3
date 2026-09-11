#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""La greffe relogeable, montree DANS LE PROCESSUS VIVANT.

Une section greffee avec ses relocations ne se voit pas a l'ecran : le jeu
demarre pareil. Le seul controle qui vaille est donc de lire la memoire du
processus et de regarder si le chargeur a corrige notre pointeur.

    --poser   greffe `.decors` sur la DLL DEJA PATCHEE, y ecrit un pointeur
              temoin (0x180403430, la table des descripteurs) en ABSOLU, et
              reconstruit la table de relocations.
    --lire    trouve vfes.exe, sa base de chargement reelle, et relit le
              temoin. Verdict.

Sans relocation, le temoin resterait a `0x180403430` -- la base preferee, qui
ne designe rien une fois le module rebase. Avec, il doit valoir
`base_reelle + 0x403430`.

Lanceur : `tools\essai_relocations.cmd` (double-cliquable).
"""
import ctypes
import ctypes.wintypes as w
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
DLL = os.path.join(JEU, 'vf5fs-pxd-w64-Retail_APM3.dll')

import pe_sections                                             # noqa: E402

SECTION = b'.decors\x00'
TAILLE = 0x10000
TEMOIN_CIBLE = 0x180403430          # la table des 41 descripteurs
TEMOIN_OFFSET = 0                   # au tout debut de la section

TH32CS_SNAPPROCESS = 0x2
TH32CS_SNAPMODULE = 0x8
TH32CS_SNAPMODULE32 = 0x10
PROCESS_VM_READ = 0x10
PROCESS_QUERY_INFORMATION = 0x400
k = ctypes.windll.kernel32


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [('dwSize', w.DWORD), ('cntUsage', w.DWORD),
                ('th32ProcessID', w.DWORD),
                ('th32DefaultHeapID', ctypes.c_void_p),
                ('th32ModuleID', w.DWORD), ('cntThreads', w.DWORD),
                ('th32ParentProcessID', w.DWORD),
                ('pcPriClassBase', ctypes.c_long),
                ('dwFlags', w.DWORD), ('szExeFile', ctypes.c_char * 260)]


class MODULEENTRY32(ctypes.Structure):
    _fields_ = [('dwSize', w.DWORD), ('th32ModuleID', w.DWORD),
                ('th32ProcessID', w.DWORD), ('GlblcntUsage', w.DWORD),
                ('ProccntUsage', w.DWORD),
                ('modBaseAddr', ctypes.POINTER(ctypes.c_byte)),
                ('modBaseSize', w.DWORD), ('hModule', w.HMODULE),
                ('szModule', ctypes.c_char * 256),
                ('szExePath', ctypes.c_char * 260)]


def pid(nom):
    s = k.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    e = PROCESSENTRY32()
    e.dwSize = ctypes.sizeof(e)
    if not k.Process32First(s, ctypes.byref(e)):
        return None
    while True:
        if e.szExeFile.lower() == nom.encode():
            return e.th32ProcessID
        if not k.Process32Next(s, ctypes.byref(e)):
            return None


def module(p, nom):
    s = k.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, p)
    e = MODULEENTRY32()
    e.dwSize = ctypes.sizeof(e)
    if not k.Module32First(s, ctypes.byref(e)):
        return None, 0
    while True:
        if nom.lower() in e.szModule.decode('latin-1').lower():
            return (ctypes.cast(e.modBaseAddr, ctypes.c_void_p).value,
                    e.modBaseSize)
        if not k.Module32Next(s, ctypes.byref(e)):
            return None, 0


def poser():
    avant = pe_sections.Pe(DLL)
    print('DLL patchee : %d sections' % avant.n_sec)
    if avant.section_par_nom(SECTION) is not None:
        print('   .decors est deja la : rien a faire.')
        return 0
    va, off = pe_sections.ajouter_section(DLL, SECTION, TAILLE)
    with open(DLL, 'r+b') as fp:
        fp.seek(off + TEMOIN_OFFSET)
        fp.write(struct.pack('<Q', TEMOIN_CIBLE))
    rva, taille = pe_sections.reconstruire_relocations(DLL,
                                                       [va + TEMOIN_OFFSET])
    apres = pe_sections.Pe(DLL)
    blocs = pe_sections.lire_relocations(DLL)
    print('   .decors greffee en 0x%X (%d octets)' % (va, TAILLE))
    print('   temoin ABSOLU 0x%X ecrit en 0x%X' % (TEMOIN_CIBLE,
                                                   va + TEMOIN_OFFSET))
    print('   table de relocations reecrite : RVA 0x%X, %d octets, %d blocs, '
          '%d entrees' % (rva, taille, len(blocs),
                          sum(1 for _, e in blocs for t, _ in e if t)))
    print('   %d sections' % apres.n_sec)
    # l'ecart de VA entre la section et la base preferee : c'est ce que
    # `--lire` ira chercher dans le processus.
    with open(os.path.join(RACINE, 'analysis', '_temoin_reloc.txt'), 'w') as fp:
        fp.write('%d %d\n' % (va - avant.base + TEMOIN_OFFSET,
                              TEMOIN_CIBLE - avant.base))
    return 0


def lire():
    p = pid('vfes.exe')
    if not p:
        print('vfes.exe ne tourne pas -- rien a lire.')
        return 1
    base, taille = module(p, 'vf5fs-pxd')
    if not base:
        print('vfes.exe tourne (pid %d) mais le moteur n est pas encore '
              'charge. Reessayez dans quelques secondes.' % p)
        return 1
    marque = os.path.join(RACINE, 'analysis', '_temoin_reloc.txt')
    if not os.path.exists(marque):
        print('pas de temoin pose : lancez --poser d abord.')
        return 1
    rva_temoin, rva_cible = [int(x) for x in open(marque).read().split()]

    print('vfes.exe pid %d ; moteur charge en 0x%X (%d octets)'
          % (p, base, taille))
    print('delta de rebasage : 0x%X' % (base - 0x180000000))
    h = k.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, p)
    buf = ctypes.create_string_buffer(8)
    lu = ctypes.c_size_t(0)
    adr = base + rva_temoin
    if not k.ReadProcessMemory(h, ctypes.c_void_p(adr), buf, 8,
                               ctypes.byref(lu)):
        print('lecture impossible en 0x%X (erreur %d)' % (adr, k.GetLastError()))
        return 1
    v = int.from_bytes(buf.raw, 'little')
    attendu = base + rva_cible
    print()
    print('   temoin en 0x%X : 0x%X' % (adr, v))
    print('   attendu        : 0x%X' % attendu)
    print()
    if v == attendu:
        print('=' * 68)
        print('  RELOCATION APPLIQUEE. Le chargeur de Windows a lu NOTRE table.')
        print('  Une section greffee peut donc porter des pointeurs absolus :')
        print('  les murs d un decor (+0xC0), ses neuf musiques, ses noms.')
        print('=' * 68)
        return 0
    if v == TEMOIN_CIBLE:
        print('NON RELOGE : la valeur est restee a la base preferee. La table')
        print('n a pas ete lue -- le repertoire de donnees n 5 pointe ailleurs.')
    else:
        print('VALEUR INATTENDUE : ni la cible relogee, ni la base preferee.')
    return 1


def main():
    argv = sys.argv[1:]
    if '--poser' in argv:
        return poser()
    if '--lire' in argv:
        return lire()
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
