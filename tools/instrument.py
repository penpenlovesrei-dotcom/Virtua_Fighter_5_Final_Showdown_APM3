#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debogueur Win32 minimal pour instrumenter les builds VF5FS sous Windows.

Concu pour observer ce qu'une recherche statique ne peut pas atteindre : qui lit
quel champ de l'etat de mouvement, quels codes de mothead sont reellement
consommes. Aucun outil tiers n'est necessaire : ctypes et l'API de debogage.

Ce qu'il sait faire
    - lancer un executable sous debogage et journaliser les DLL chargees,
      avec leur base, au fur et a mesure ;
    - rapporter chaque exception avec son code, son adresse et le module qui la
      contient (premiere et seconde chance), avec le type C++ demangle ;
    - poser des points d'arret LOGICIELS (INT3) a une adresse relative a un
      module, journaliser les registres a chaque passage, et se rearmer tout
      seul (restauration de l'octet, drapeau de trace, reecriture du 0xCC) ;
    - poser des points d'arret MATERIELS en lecture ou en ecriture sur une
      adresse de donnees (registres DR0 a DR3), sur TOUS les threads, y compris
      ceux crees apres la pose. C'est le seul moyen de repondre a
      « qui lit ce champ » ;
    - prendre une capture d'ecran de la fenetre du jeu a un instant choisi.

Usage :
    py -3 tools/instrument.py run <exe> [--cwd <dossier>] [--secondes N]
                                        [--silencieux] [--journal <fichier>]
                                        [--bp <module>+<offset hex>] ...
                                        [--bp-max N]
                                        [--dr <adresse hex>[:taille[:r|w|x]]] ...
                                        [--dr-max N]
                                        [--capture <png>@<secondes>] ...

Exemples :
    py -3 tools/instrument.py run runtime/media/vf5fs/vfes.exe --secondes 30
    py -3 tools/instrument.py run ... --bp vf5fs-pxd-w64-Retail_APM3.dll+0x158B51
    py -3 tools/instrument.py run ... --dr 0x1F2C0A954:4:r
    py -3 tools/instrument.py run ... --capture analysis/ecran.png@12

Note : une adresse de donnees n'est en general connue qu'a l'execution. Le cas
courant est donc « point d'arret logiciel sur la fonction qui installe un
enregistrement, on y lit le pointeur dans un registre, puis on arme un DR sur
ce pointeur + offset ». C'est ce que fait tools/pister_etat.py.
"""
import atexit
import ctypes
import ctypes.wintypes as w
import os
import sys
import threading
import time

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
psapi = ctypes.WinDLL('psapi', use_last_error=True)

# ---------------------------------------------------------------------------
# RENDRE LE CLAVIER. Vingt-deux outils du dossier ecrivent leur propre scenario
# dans `runtime/media/vf5fs/apm_entrees.txt` -- typiquement deux impulsions
# START, pour traverser l'ecran-titre et aller mesurer plus loin. Aucun ne le
# remettait en etat, si bien que la partie SUIVANTE, jouee a la main, voyait le
# jeu appuyer sur START tout seul. Frederic l'a signale QUATRE FOIS.
#
# La correction est ici, au seul endroit que tous ces outils traversent : la
# fin de `Debugger.run()`. Le maitre `tools/apm_entrees.txt` (une seule ligne,
# « 0 rien ») est recopie des que la mesure est finie, quoi qu'il arrive.
_ICI = os.path.dirname(os.path.abspath(__file__))
_RACINE = os.path.dirname(_ICI)
SCENARIO_MAITRE = os.path.join(_ICI, 'apm_entrees.txt')
SCENARIO_ACTIF = os.path.join(_RACINE, 'runtime', 'media', 'vf5fs',
                              'apm_entrees.txt')


def rendre_le_clavier(dire=None):
    """Remet le scenario d'entrees en jeu MANUEL. Jamais fatal."""
    try:
        with open(SCENARIO_MAITRE, 'rb') as fp:
            maitre = fp.read()
    except OSError:
        return False
    try:
        with open(SCENARIO_ACTIF, 'rb') as fp:
            if fp.read() == maitre:
                return True                       # deja propre
    except OSError:
        pass
    try:
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(maitre)
    except OSError as e:
        if dire:
            dire('  ATTENTION : scenario d entrees NON remis (%s)' % e)
        return False
    if dire:
        dire('  scenario d entrees remis en jeu manuel')
    return True


# Et en ceinture : meme si la sonde plante, est interrompue par Ctrl+C, ou sort
# par un chemin d'erreur, le clavier est rendu. `presser.py` -- le seul outil
# dont le scenario DOIT survivre a la sortie -- n'importe pas ce module.
atexit.register(rendre_le_clavier)


def jeu_deja_lance():
    """Un vfes.exe tourne-t-il deja ?

    Rendre le clavier a la FIN d'une mesure ne suffit pas : pendant qu'elle
    tourne, le scenario est sali, et le fichier est PARTAGE avec toute partie
    deja en cours -- le stub le relit toutes les 250 ms. Frederic a vu sa
    partie appuyer sur START pendant qu'une sonde mesurait a cote. On refuse
    donc de demarrer dans ce cas.
    """
    try:
        r = __import__('subprocess').run(
            [os.path.join(os.environ.get('SystemRoot', r'C:\Windows'),
                          'System32', 'tasklist.exe'),
             '/FI', 'IMAGENAME eq vfes.exe', '/NH'],
            capture_output=True, text=True, timeout=10)
        return 'vfes.exe' in (r.stdout or '')
    except Exception:
        return False                                  # dans le doute, on laisse

DEBUG_ONLY_THIS_PROCESS = 0x00000002
DBG_CONTINUE = 0x00010002
DBG_EXCEPTION_NOT_HANDLED = 0x80010001
INFINITE = 0xFFFFFFFF

EXCEPTION_DEBUG_EVENT = 1
CREATE_THREAD_DEBUG_EVENT = 2
CREATE_PROCESS_DEBUG_EVENT = 3
EXIT_THREAD_DEBUG_EVENT = 4
EXIT_PROCESS_DEBUG_EVENT = 5
LOAD_DLL_DEBUG_EVENT = 6
UNLOAD_DLL_DEBUG_EVENT = 7
OUTPUT_DEBUG_STRING_EVENT = 8
RIP_EVENT = 9

EXC = {
    0x80000003: 'BREAKPOINT', 0x80000004: 'SINGLE_STEP',
    0xC0000005: 'ACCESS_VIOLATION', 0xC000001D: 'ILLEGAL_INSTRUCTION',
    0xC0000094: 'INTEGER_DIVIDE_BY_ZERO', 0xC0000096: 'PRIVILEGED_INSTRUCTION',
    0xC00000FD: 'STACK_OVERFLOW', 0xC0000409: 'STACK_BUFFER_OVERRUN (__fastfail)',
    0xC0000374: 'HEAP_CORRUPTION', 0x406D1388: 'nom de thread (VS)',
    0xE06D7363: 'exception C++', 0xC0000135: 'DLL_NOT_FOUND',
    0xC0000139: 'ENTRYPOINT_NOT_FOUND',
}

CONTEXT_AMD64 = 0x00100000
CONTEXT_CONTROL = CONTEXT_AMD64 | 0x1
CONTEXT_INTEGER = CONTEXT_AMD64 | 0x2
CONTEXT_SEGMENTS = CONTEXT_AMD64 | 0x4
CONTEXT_FLOATING_POINT = CONTEXT_AMD64 | 0x8
CONTEXT_DEBUG_REGISTERS = CONTEXT_AMD64 | 0x10
CONTEXT_FULL = CONTEXT_CONTROL | CONTEXT_INTEGER | CONTEXT_FLOATING_POINT

THREAD_ALL_ACCESS = 0x1FFFFF
TRAP_FLAG = 0x100

# Codes d'acces des registres DR7 : 00 execution, 01 ecriture, 11 lecture OU
# ecriture. Le x86 n'a pas de « lecture seule » : un DR pose en lecture
# rapporte aussi les ecritures.
ACCES = {'x': 0, 'w': 1, 'r': 3}
LONGUEUR = {1: 0, 2: 1, 8: 2, 4: 3}


class STARTUPINFOW(ctypes.Structure):
    _fields_ = [('cb', w.DWORD), ('lpReserved', w.LPWSTR), ('lpDesktop', w.LPWSTR),
                ('lpTitle', w.LPWSTR), ('dwX', w.DWORD), ('dwY', w.DWORD),
                ('dwXSize', w.DWORD), ('dwYSize', w.DWORD), ('dwXCountChars', w.DWORD),
                ('dwYCountChars', w.DWORD), ('dwFillAttribute', w.DWORD),
                ('dwFlags', w.DWORD), ('wShowWindow', w.WORD), ('cbReserved2', w.WORD),
                ('lpReserved2', ctypes.POINTER(ctypes.c_byte)),
                ('hStdInput', w.HANDLE), ('hStdOutput', w.HANDLE), ('hStdError', w.HANDLE)]


class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [('hProcess', w.HANDLE), ('hThread', w.HANDLE),
                ('dwProcessId', w.DWORD), ('dwThreadId', w.DWORD)]


class EXCEPTION_RECORD(ctypes.Structure):
    _fields_ = [('ExceptionCode', w.DWORD), ('ExceptionFlags', w.DWORD),
                ('ExceptionRecord', ctypes.c_void_p), ('ExceptionAddress', ctypes.c_void_p),
                ('NumberParameters', w.DWORD), ('__pad', w.DWORD),
                ('ExceptionInformation', ctypes.c_ulonglong * 15)]


class EXCEPTION_DEBUG_INFO(ctypes.Structure):
    _fields_ = [('ExceptionRecord', EXCEPTION_RECORD), ('dwFirstChance', w.DWORD)]


class CREATE_PROCESS_DEBUG_INFO(ctypes.Structure):
    _fields_ = [('hFile', w.HANDLE), ('hProcess', w.HANDLE), ('hThread', w.HANDLE),
                ('lpBaseOfImage', ctypes.c_void_p), ('dwDebugInfoFileOffset', w.DWORD),
                ('nDebugInfoSize', w.DWORD), ('lpThreadLocalBase', ctypes.c_void_p),
                ('lpStartAddress', ctypes.c_void_p), ('lpImageName', ctypes.c_void_p),
                ('fUnicode', w.WORD)]


class LOAD_DLL_DEBUG_INFO(ctypes.Structure):
    _fields_ = [('hFile', w.HANDLE), ('lpBaseOfDll', ctypes.c_void_p),
                ('dwDebugInfoFileOffset', w.DWORD), ('nDebugInfoSize', w.DWORD),
                ('lpImageName', ctypes.c_void_p), ('fUnicode', w.WORD)]


class CREATE_THREAD_DEBUG_INFO(ctypes.Structure):
    _fields_ = [('hThread', w.HANDLE), ('lpThreadLocalBase', ctypes.c_void_p),
                ('lpStartAddress', ctypes.c_void_p)]


class EXIT_INFO(ctypes.Structure):
    _fields_ = [('dwExitCode', w.DWORD)]


class OUTPUT_DEBUG_STRING_INFO(ctypes.Structure):
    _fields_ = [('lpDebugStringData', ctypes.c_void_p), ('fUnicode', w.WORD),
                ('nDebugStringLength', w.WORD)]


class DEBUG_UNION(ctypes.Union):
    _fields_ = [('Exception', EXCEPTION_DEBUG_INFO),
                ('CreateThread', CREATE_THREAD_DEBUG_INFO),
                ('CreateProcessInfo', CREATE_PROCESS_DEBUG_INFO),
                ('ExitThread', EXIT_INFO), ('ExitProcess', EXIT_INFO),
                ('LoadDll', LOAD_DLL_DEBUG_INFO), ('UnloadDll', ctypes.c_void_p),
                ('DebugString', OUTPUT_DEBUG_STRING_INFO),
                ('__raw', ctypes.c_byte * 200)]


class DEBUG_EVENT(ctypes.Structure):
    _fields_ = [('dwDebugEventCode', w.DWORD), ('dwProcessId', w.DWORD),
                ('dwThreadId', w.DWORD), ('u', DEBUG_UNION)]
    _anonymous_ = ()


class M128A(ctypes.Structure):
    _fields_ = [('Low', ctypes.c_ulonglong), ('High', ctypes.c_longlong)]


class XSAVE_FORMAT(ctypes.Structure):
    _fields_ = [('ControlWord', w.WORD), ('StatusWord', w.WORD),
                ('TagWord', ctypes.c_ubyte), ('Reserved1', ctypes.c_ubyte),
                ('ErrorOpcode', w.WORD), ('ErrorOffset', w.DWORD),
                ('ErrorSelector', w.WORD), ('Reserved2', w.WORD),
                ('DataOffset', w.DWORD), ('DataSelector', w.WORD),
                ('Reserved3', w.WORD), ('MxCsr', w.DWORD), ('MxCsr_Mask', w.DWORD),
                ('FloatRegisters', M128A * 8), ('XmmRegisters', M128A * 16),
                ('Reserved4', ctypes.c_ubyte * 96)]


class CONTEXT(ctypes.Structure):
    """CONTEXT x64. Doit etre aligne sur 16 octets : voir contexte_neuf()."""
    _pack_ = 16
    _fields_ = [
        ('P1Home', ctypes.c_ulonglong), ('P2Home', ctypes.c_ulonglong),
        ('P3Home', ctypes.c_ulonglong), ('P4Home', ctypes.c_ulonglong),
        ('P5Home', ctypes.c_ulonglong), ('P6Home', ctypes.c_ulonglong),
        ('ContextFlags', w.DWORD), ('MxCsr', w.DWORD),
        ('SegCs', w.WORD), ('SegDs', w.WORD), ('SegEs', w.WORD),
        ('SegFs', w.WORD), ('SegGs', w.WORD), ('SegSs', w.WORD),
        ('EFlags', w.DWORD),
        ('Dr0', ctypes.c_ulonglong), ('Dr1', ctypes.c_ulonglong),
        ('Dr2', ctypes.c_ulonglong), ('Dr3', ctypes.c_ulonglong),
        ('Dr6', ctypes.c_ulonglong), ('Dr7', ctypes.c_ulonglong),
        ('Rax', ctypes.c_ulonglong), ('Rcx', ctypes.c_ulonglong),
        ('Rdx', ctypes.c_ulonglong), ('Rbx', ctypes.c_ulonglong),
        ('Rsp', ctypes.c_ulonglong), ('Rbp', ctypes.c_ulonglong),
        ('Rsi', ctypes.c_ulonglong), ('Rdi', ctypes.c_ulonglong),
        ('R8', ctypes.c_ulonglong), ('R9', ctypes.c_ulonglong),
        ('R10', ctypes.c_ulonglong), ('R11', ctypes.c_ulonglong),
        ('R12', ctypes.c_ulonglong), ('R13', ctypes.c_ulonglong),
        ('R14', ctypes.c_ulonglong), ('R15', ctypes.c_ulonglong),
        ('Rip', ctypes.c_ulonglong),
        ('FltSave', XSAVE_FORMAT),
        ('VectorRegister', M128A * 26), ('VectorControl', ctypes.c_ulonglong),
        ('DebugControl', ctypes.c_ulonglong),
        ('LastBranchToRip', ctypes.c_ulonglong),
        ('LastBranchFromRip', ctypes.c_ulonglong),
        ('LastExceptionToRip', ctypes.c_ulonglong),
        ('LastExceptionFromRip', ctypes.c_ulonglong),
    ]


assert ctypes.sizeof(CONTEXT) == 0x4D0, ctypes.sizeof(CONTEXT)
assert CONTEXT.Dr0.offset == 0x48
assert CONTEXT.Rip.offset == 0xF8


def contexte_neuf(flags):
    """Un CONTEXT aligne sur 16 octets (exigence de GetThreadContext x64)."""
    brut = (ctypes.c_char * (ctypes.sizeof(CONTEXT) + 16))()
    adr = ctypes.addressof(brut)
    ctx = CONTEXT.from_address((adr + 15) & ~15)
    ctx._brut = brut                       # empeche le ramasse-miettes
    ctx.ContextFlags = flags
    return ctx


k32.WaitForDebugEvent.argtypes = [ctypes.POINTER(DEBUG_EVENT), w.DWORD]
k32.ContinueDebugEvent.argtypes = [w.DWORD, w.DWORD, w.DWORD]
k32.CreateProcessW.argtypes = [w.LPCWSTR, w.LPWSTR, ctypes.c_void_p, ctypes.c_void_p,
                               w.BOOL, w.DWORD, ctypes.c_void_p, w.LPCWSTR,
                               ctypes.POINTER(STARTUPINFOW), ctypes.POINTER(PROCESS_INFORMATION)]
k32.GetThreadContext.argtypes = [w.HANDLE, ctypes.POINTER(CONTEXT)]
k32.SetThreadContext.argtypes = [w.HANDLE, ctypes.POINTER(CONTEXT)]
k32.OpenThread.argtypes = [w.DWORD, w.BOOL, w.DWORD]
k32.OpenThread.restype = w.HANDLE
psapi.GetModuleFileNameExW.argtypes = [w.HANDLE, ctypes.c_void_p, w.LPWSTR, w.DWORD]


class PointArret:
    """Point d'arret logiciel : un 0xCC ecrit a la place du premier octet."""

    def __init__(self, nom, adresse, max_coups=None):
        self.nom = nom
        self.adresse = adresse
        self.octet = None
        self.coups = 0
        self.arme = False
        self.max_coups = max_coups     # None : on suit dbg.bp_max
        self.silencieux = False        # ne pas journaliser les registres


class Materiel:
    """Point d'arret materiel : une adresse de donnees surveillee par un DRn."""

    def __init__(self, adresse, taille, acces, nom=None):
        self.adresse = adresse
        self.taille = taille
        self.acces = acces                 # 'r', 'w' ou 'x'
        self.nom = nom or ('0x%X' % adresse)
        self.slot = None
        self.coups = 0


class Debugger:
    def __init__(self):
        self.modules = {}          # base -> nom
        self.hproc = None
        self.pid = None
        self.log = []
        self.debug_strings = []
        self.quiet = False
        self.threads = {}          # tid -> handle
        self.bps = []              # PointArret en attente ou armes
        self.bp_max = 4
        self.dr = [None, None, None, None]   # slot -> Materiel
        self.dr_max = 20
        self.dr_auto_desarmer = True   # libere le registre apres dr_max acces
        self.dr_finis = []             # materiels desarmes, pour le bilan
        self.dr_ignorer = set()        # RIP dont les acces ne comptent pas
        self.dr_ignores = {}           # RIP ignore -> nombre d'acces
        self.dr_plages_ignorees = []   # (lo, hi) : plages de RIP sans interet
        self.rearmer = {}          # tid -> PointArret a reecrire apres la trace
        self.sortie = sys.stdout
        self.on_bp = None          # callback(dbg, bp, ctx, tid) -> None
        self.on_dr = None          # callback(dbg, mat, ctx, tid) -> None
        self.tic = None            # callback(dbg, secondes) a chaque tour de boucle
        self.muet = False          # mettre la session audio du processus en sourdine

    # ---------------------------------------------------------------- sortie
    def dire(self, txt):
        print(txt, file=self.sortie)
        if self.sortie is not sys.stdout:
            self.sortie.flush()

    # --------------------------------------------------------------- modules
    def module_of(self, addr):
        best, name = None, None
        for b, n in self.modules.items():
            if b <= addr and (best is None or b > best):
                best, name = b, n
        if best is None:
            return '?', addr
        return name, addr - best

    def base_de(self, nom):
        nom = nom.lower()
        for b, n in self.modules.items():
            if n.lower() == nom:
                return b
        return None

    def name_of(self, base):
        buf = ctypes.create_unicode_buffer(512)
        if self.hproc and psapi.GetModuleFileNameExW(self.hproc, ctypes.c_void_p(base),
                                                     buf, 512):
            return os.path.basename(buf.value)
        if self.hproc and psapi.GetMappedFileNameW(self.hproc, ctypes.c_void_p(base),
                                                   buf, 512):
            return os.path.basename(buf.value)
        return '0x%X' % base

    # -------------------------------------------------------------- memoire
    def read(self, addr, n):
        buf = (ctypes.c_char * n)()
        got = ctypes.c_size_t(0)
        if not k32.ReadProcessMemory(self.hproc, ctypes.c_void_p(addr), buf, n,
                                     ctypes.byref(got)):
            return b''
        return bytes(buf[:got.value])

    def write(self, addr, data):
        old = w.DWORD(0)
        k32.VirtualProtectEx(self.hproc, ctypes.c_void_p(addr), len(data),
                             0x40, ctypes.byref(old))       # PAGE_EXECUTE_READWRITE
        put = ctypes.c_size_t(0)
        ok = k32.WriteProcessMemory(self.hproc, ctypes.c_void_p(addr), data,
                                    len(data), ctypes.byref(put))
        k32.VirtualProtectEx(self.hproc, ctypes.c_void_p(addr), len(data),
                             old, ctypes.byref(old))
        k32.FlushInstructionCache(self.hproc, ctypes.c_void_p(addr), len(data))
        return bool(ok)

    def u32(self, a):
        d = self.read(a, 4)
        return int.from_bytes(d, 'little') if len(d) == 4 else None

    def u64(self, a):
        d = self.read(a, 8)
        return int.from_bytes(d, 'little') if len(d) == 8 else None

    def cstr(self, a, n=200):
        d = self.read(a, n)
        i = d.find(bytes([0]))
        return d[:i if i >= 0 else n].decode('latin-1')

    # -------------------------------------------------------------- threads
    def handle_thread(self, tid):
        h = self.threads.get(tid)
        if h:
            return h
        h = k32.OpenThread(THREAD_ALL_ACCESS, False, tid)
        if h:
            self.threads[tid] = h
        return h

    def contexte(self, tid, flags=CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS):
        h = self.handle_thread(tid)
        if not h:
            return None
        ctx = contexte_neuf(flags)
        if not k32.GetThreadContext(h, ctypes.byref(ctx)):
            return None
        return ctx

    def poser_contexte(self, tid, ctx):
        h = self.handle_thread(tid)
        return bool(h and k32.SetThreadContext(h, ctypes.byref(ctx)))

    # ------------------------------------------- points d'arret materiels
    def dr7_courant(self):
        """Valeur de DR7 correspondant a self.dr."""
        v = 0
        for i, m in enumerate(self.dr):
            if m is None:
                continue
            v |= 1 << (2 * i)                                  # Ln : local
            v |= ACCES[m.acces] << (16 + 4 * i)                # R/W
            v |= LONGUEUR[m.taille] << (18 + 4 * i)            # LEN
        if v:
            v |= 0x100 | 0x200                                 # LE, GE
        return v

    def appliquer_dr(self, tid=None):
        """Ecrit DR0-DR3 et DR7 sur un thread, ou sur tous."""
        dr7 = self.dr7_courant()
        cibles = [tid] if tid is not None else list(self.threads)
        pose = 0
        for t in cibles:
            ctx = self.contexte(t, CONTEXT_DEBUG_REGISTERS)
            if ctx is None:
                continue
            for i, m in enumerate(self.dr):
                setattr(ctx, 'Dr%d' % i, m.adresse if m else 0)
            ctx.Dr6 = 0
            ctx.Dr7 = dr7
            ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS
            if self.poser_contexte(t, ctx):
                pose += 1
        return pose

    def armer_materiel(self, adresse, taille=4, acces='r', nom=None):
        """Occupe un slot DR et l'applique a tous les threads connus."""
        if adresse % taille:
            self.dire('  DR refuse : 0x%X n\'est pas aligne sur %d octets'
                      % (adresse, taille))
            return None
        libre = next((i for i, m in enumerate(self.dr) if m is None), None)
        if libre is None:
            self.dire('  DR refuse : les quatre registres sont occupes')
            return None
        m = Materiel(adresse, taille, acces, nom)
        m.slot = libre
        self.dr[libre] = m
        n = self.appliquer_dr()
        self.dire('  DR%d arme sur %s (%d o, %s) -- %d thread(s)'
                  % (libre, m.nom, taille, acces, n))
        return m

    def desarmer_materiel(self, m):
        if m.slot is not None and self.dr[m.slot] is m:
            self.dr[m.slot] = None
            self.appliquer_dr()
        if m not in self.dr_finis:
            self.dr_finis.append(m)

    # -------------------------------------------- points d'arret logiciels
    def armer_logiciel(self, bp):
        octet = self.read(bp.adresse, 1)
        if len(octet) != 1:
            self.dire('  BP refuse : %s illisible' % bp.nom)
            return False
        bp.octet = octet
        if not self.write(bp.adresse, b'\xCC'):
            self.dire('  BP refuse : ecriture impossible en %s' % bp.nom)
            return False
        bp.arme = True
        self.dire('  BP arme sur %s = 0x%X (octet d\'origine 0x%02X)'
                  % (bp.nom, bp.adresse, octet[0]))
        return True

    def desarmer_logiciel(self, bp):
        if bp.arme and bp.octet is not None:
            self.write(bp.adresse, bp.octet)
        bp.arme = False

    def bp_a(self, adresse):
        for bp in self.bps:
            if bp.arme and bp.adresse == adresse:
                return bp
        return None

    # ------------------------------------------------------------ rapports
    def registres(self, ctx):
        return ('rax=%016X rcx=%016X rdx=%016X rbx=%016X\n'
                '        rsp=%016X rbp=%016X rsi=%016X rdi=%016X\n'
                '        r8 =%016X r9 =%016X r10=%016X r11=%016X'
                % (ctx.Rax, ctx.Rcx, ctx.Rdx, ctx.Rbx,
                   ctx.Rsp, ctx.Rbp, ctx.Rsi, ctx.Rdi,
                   ctx.R8, ctx.R9, ctx.R10, ctx.R11))

    def cxx_exception(self, params):
        """Type et message d'une exception C++ MSVC x64."""
        if len(params) < 4:
            return None, None
        obj, throwinfo, imgbase = params[1], params[2], params[3]
        try:
            cta_rva = self.u32(throwinfo + 12)
            if not cta_rva:
                return None, None
            cta = imgbase + cta_rva
            n = self.u32(cta)
            noms = []
            for k in range(min(n or 0, 6)):
                ct = imgbase + self.u32(cta + 4 + 4 * k)
                td = imgbase + self.u32(ct + 4)
                noms.append(self.cstr(td + 16, 120))
            msg = None
            # std::exception MSVC : vftable, puis _Data.name (char*)
            p = self.u64(obj + 8)
            if p:
                cand = self.cstr(p, 300)
                if cand and all(32 <= ord(c) < 127 for c in cand[:60]):
                    msg = cand
            return noms, msg
        except Exception:
            return None, None

    # ------------------------------------------------------- boucle de jeu
    def _couper_le_son(self, pid, duree):
        """Met en sourdine la seule session audio de ce processus.

        Le volume general de Windows n'est pas touche : c'est le volume par
        application. La session n'existe qu'une fois le moteur audio ouvert, ce
        qui prend quelques secondes -- d'ou la boucle.

        ATTENTION (2026-09-11) : Windows MEMORISE la sourdine par application.
        Un jeu coupe par la sonde restait muet aux lancements suivants, a la
        main -- Frederic : « reactive le son du jeu ». `_rendre_le_son` la
        leve donc avant de fermer le jeu."""
        self._son_arret = threading.Event()

        def travail():
            try:
                from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
            except ImportError:
                self.dire('  sourdine : pycaw absent, le son reste actif')
                return
            t0 = time.time()
            fait = False
            while time.time() - t0 < duree and not self._son_arret.is_set():
                try:
                    for sess in AudioUtilities.GetAllSessions():
                        if getattr(sess, 'ProcessId', None) == pid:
                            sess._ctl.QueryInterface(ISimpleAudioVolume).SetMute(1, None)
                            if not fait:
                                self.dire('  sourdine : session audio du processus %d '
                                          'coupee apres %.0f s' % (pid, time.time() - t0))
                                fait = True
                except Exception:
                    pass
                time.sleep(1.0)
            if not fait:
                self.dire('  sourdine : aucune session audio trouvee pour %d' % pid)
        t = threading.Thread(target=travail, daemon=True)
        t.start()
        self._son_fil = t
        return t

    def _rendre_le_son(self, pid):
        """Arrete la boucle de sourdine et leve la sourdine de la session
        tant qu'elle existe encore (le jeu tourne) : sinon Windows la
        garderait pour les lancements suivants."""
        if getattr(self, '_son_arret', None) is None:
            return
        self._son_arret.set()
        if getattr(self, '_son_fil', None) is not None:
            self._son_fil.join(3.0)
        try:
            from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
        except ImportError:
            return
        n = 0
        try:
            for sess in AudioUtilities.GetAllSessions():
                if getattr(sess, 'ProcessId', None) == pid:
                    sess._ctl.QueryInterface(ISimpleAudioVolume).SetMute(0, None)
                    n += 1
        except Exception:
            pass
        self.dire('  sourdine levee avant de fermer le jeu (%d session(s))' % n
                  if n else '  sourdine : plus de session a lever -- si le jeu '
                  'reste muet : py -3 tools/muet.py --rendre, jeu lance')

    def _capture_plus_tard(self, chemin, delai, titre):
        def travail():
            time.sleep(delai)
            try:
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                import capture_fenetre as cap
                cap.dpi_aware()
                hwnd, nom, rect = cap.trouver(titre)
                if not hwnd:
                    self.dire('  capture : aucune fenetre "%s" a t=%s s'
                              % (titre, delai))
                    return
                cap.user32.ShowWindow(hwnd, cap.SW_RESTORE)
                cap.user32.SetForegroundWindow(hwnd)
                time.sleep(0.4)
                r = w.RECT()
                cap.user32.GetWindowRect(hwnd, ctypes.byref(r))
                la, ha = cap.capturer((r.left, r.top, r.right, r.bottom), chemin)
                self.dire('  capture : %s (%dx%d) a t=%s s' % (chemin, la, ha, delai))
            except Exception as e:
                self.dire('  capture : echec (%s)' % e)
        t = threading.Thread(target=travail, daemon=True)
        t.start()
        return t

    def run(self, exe, cwd=None, seconds=30, captures=()):
        if jeu_deja_lance():
            self.dire('REFUS : un vfes.exe tourne DEJA.')
            self.dire('  Une sonde ecrit son propre scenario dans')
            self.dire('  runtime/media/vf5fs/apm_entrees.txt -- fichier PARTAGE,')
            self.dire('  relu toutes les 250 ms. La partie en cours se mettrait a')
            self.dire('  appuyer sur START toute seule.')
            self.dire('  Fermez le jeu, puis relancez la mesure.')
            return 3
        si = STARTUPINFOW()
        si.cb = ctypes.sizeof(si)
        pi = PROCESS_INFORMATION()
        cmd = ctypes.create_unicode_buffer(exe)
        ok = k32.CreateProcessW(exe, cmd, None, None, False,
                                DEBUG_ONLY_THIS_PROCESS, None, cwd,
                                ctypes.byref(si), ctypes.byref(pi))
        if not ok:
            self.dire('CreateProcessW a echoue : %d' % ctypes.get_last_error())
            return 1
        self.dire('processus %d lance sous debogage' % pi.dwProcessId)
        self.hproc = pi.hProcess
        self.pid = pi.dwProcessId
        if self.muet:
            self._couper_le_son(pi.dwProcessId, seconds)
        for chemin, delai, titre in captures:
            self._capture_plus_tard(chemin, delai, titre)
        ev = DEBUG_EVENT()
        t0 = time.time()
        fini = False
        while not fini:
            if not k32.WaitForDebugEvent(ctypes.byref(ev), 100):
                if self.tic:
                    self.tic(self, time.time() - t0)
                if time.time() - t0 > seconds:
                    break
                continue
            code = ev.dwDebugEventCode
            tid = ev.dwThreadId
            status = DBG_CONTINUE

            if code == CREATE_PROCESS_DEBUG_EVENT:
                b = ev.u.CreateProcessInfo.lpBaseOfImage
                self.modules[b] = os.path.basename(exe)
                self.threads[tid] = ev.u.CreateProcessInfo.hThread
                self.dire('  image     0x%016X  %s' % (b, os.path.basename(exe)))
                self.armer_en_attente()
            elif code == CREATE_THREAD_DEBUG_EVENT:
                self.threads[tid] = ev.u.CreateThread.hThread
                if any(self.dr):
                    self.appliquer_dr(tid)      # les DR sont par thread
            elif code == EXIT_THREAD_DEBUG_EVENT:
                self.threads.pop(tid, None)
            elif code == LOAD_DLL_DEBUG_EVENT:
                b = ev.u.LoadDll.lpBaseOfDll
                n = self.name_of(b)
                self.modules[b] = n
                if any(s in n.lower() for s in ('vf5fs', 'apm', 'd3d', 'dxgi')):
                    self.dire('  dll       0x%016X  %s' % (b, n))
                self.armer_en_attente()
            elif code == OUTPUT_DEBUG_STRING_EVENT:
                d = ev.u.DebugString
                n = min(d.nDebugStringLength, 400)
                raw = self.read(d.lpDebugStringData, n)
                try:
                    txt = (raw.decode('utf-16-le') if d.fUnicode
                           else raw.decode('latin-1'))
                except Exception:
                    txt = ''
                txt = txt.split(chr(0))[0].strip()
                if txt:
                    self.debug_strings.append(txt)
                    if not self.quiet:
                        self.dire('  [dbg] %s' % txt)
            elif code == EXCEPTION_DEBUG_EVENT:
                status = self.exception(ev, tid)
            elif code == EXIT_PROCESS_DEBUG_EVENT:
                self.dire('  sortie du processus, code 0x%08X'
                          % ev.u.ExitProcess.dwExitCode)
                k32.ContinueDebugEvent(ev.dwProcessId, tid, status)
                fini = True
                break
            k32.ContinueDebugEvent(ev.dwProcessId, tid, status)
            ecoule = time.time() - t0
            if self.tic:
                self.tic(self, ecoule)
            if ecoule > seconds:
                break

        if self.muet:
            self._rendre_le_son(pi.dwProcessId)
        if not fini:
            self.dire('--- %d s ecoulees, on arrete ---' % seconds)
            k32.DebugActiveProcessStop(pi.dwProcessId)
            k32.TerminateProcess(pi.hProcess, 0)
        self.dire('\n%d module(s) charge(s)' % len(self.modules))
        for bp in self.bps:
            self.dire('  BP %s : %d passage(s)' % (bp.nom, bp.coups))
        for m in [x for x in self.dr if x] + self.dr_finis:
            self.dire('  DR%d %s : %d acces' % (m.slot, m.nom, m.coups))
        for rip, n in sorted(self.dr_ignores.items(), key=lambda kv: -kv[1]):
            mod, off = self.module_of(rip)
            self.dire('  ignore : %d acces apres 0x%016X = %s+0x%X'
                      % (n, rip, mod, off))
        rendre_le_clavier(self.dire)
        return 0

    def armer_en_attente(self):
        """Appele a chaque chargement de module. Remplace par main() quand des
        points d'arret differes (module+offset) attendent leur base."""
        pass

    def violation(self, tid, r):
        """Une ACCESS_VIOLATION : dire QUI copiait, et QUOI.

        Le message d'exception seul ne nomme que la fonction fautive -- souvent
        `memcpy`, qui ne dit rien. Ce qui renseigne, ce sont les registres
        d'appel (`rcx` destination, `rdx`/`rsi` source, `r8`/`rcx` longueur) et
        les adresses de retour APPLICATIVES encore sur la pile.
        """
        try:
            ctx = self.contexte(tid)
        except Exception:
            return
        try:
            lecture = r.ExceptionInformation[0]
            adresse = r.ExceptionInformation[1]
            self.dire('      acces en %s a 0x%016X'
                      % ('ECRITURE' if lecture else 'LECTURE', adresse))
        except Exception:
            pass
        self.dire('      rcx=0x%X  rdx=0x%X  r8=0x%X  rdi=0x%X  rsi=0x%X'
                  % (ctx.Rcx & 0xFFFFFFFFFFFFFFFF, ctx.Rdx & 0xFFFFFFFFFFFFFFFF,
                     ctx.R8 & 0xFFFFFFFFFFFFFFFF, ctx.Rdi & 0xFFFFFFFFFFFFFFFF,
                     ctx.Rsi & 0xFFFFFFFFFFFFFFFF))
        pile = self.read(ctx.Rsp, 8 * 128) or b''
        vus = 0
        for i in range(0, len(pile) - 7, 8):
            v = int.from_bytes(pile[i:i + 8], 'little')
            m, o = self.module_of(v)
            if m and m != '?' and o < 0x800000 and vus < 12:
                self.dire('      [rsp+0x%03X] -> %s+0x%X' % (i, m, o))
                vus += 1

    def exception(self, ev, tid):
        r = ev.u.Exception.ExceptionRecord
        c = r.ExceptionCode & 0xFFFFFFFF
        a = r.ExceptionAddress or 0
        first = ev.u.Exception.dwFirstChance

        # --- point d'arret logiciel
        if c == 0x80000003:
            # Windows rapporte l'adresse de l'INT3 lui-meme ; le RIP du contexte,
            # lui, pointe l'octet suivant. On cherche donc les deux.
            bp = self.bp_a(a) or self.bp_a(a - 1)
            if bp is not None:
                return self.frapper_logiciel(bp, tid)

        # --- point d'arret materiel (ou pas a pas de rearmement)
        if c == 0x80000004:
            ctx = self.contexte(tid)
            if ctx is not None:
                dr6 = ctx.Dr6
                traite = False
                for i in range(4):
                    if dr6 & (1 << i) and self.dr[i] is not None:
                        if (ctx.Rip in self.dr_ignorer or
                                any(lo <= ctx.Rip < hi
                                    for lo, hi in self.dr_plages_ignorees)):
                            # acces connu et sans interet (le copieur d'etat) :
                            # on le compte a part et on ne consomme pas de quota
                            self.dr_ignores[ctx.Rip] = self.dr_ignores.get(ctx.Rip, 0) + 1
                        else:
                            self.frapper_materiel(self.dr[i], ctx, tid)
                        traite = True
                bp = self.rearmer.pop(tid, None)
                plafond = (self.bp_max if bp is None or bp.max_coups is None
                           else bp.max_coups)
                if bp is not None and bp.coups < plafond:
                    self.write(bp.adresse, b'\xCC')
                    bp.arme = True
                    traite = True
                elif bp is not None:
                    traite = True
                # On reecrit les registres depuis l'etat courant : un materiel
                # desarme pendant ce traitement serait sinon remis en place par
                # le DR7 perime que porte encore ce contexte.
                for i in range(4):
                    m = self.dr[i]
                    setattr(ctx, 'Dr%d' % i, m.adresse if m else 0)
                ctx.Dr6 = 0
                ctx.Dr7 = self.dr7_courant()
                ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS
                self.poser_contexte(tid, ctx)
                if traite:
                    return DBG_CONTINUE

        mod, off = self.module_of(a)
        nom = EXC.get(c, '0x%08X' % c)
        if c not in (0x406D1388,):
            self.dire('  EXCEPTION %s %s  a 0x%016X = %s+0x%X' %
                      (nom, '(1re chance)' if first else '(2e chance)', a, mod, off))
            self.log.append((nom, a, mod, off, bool(first)))
            if c == 0xC0000005 and first:
                self.violation(tid, r)
            if c == 0xE06D7363:
                prm = [r.ExceptionInformation[i]
                       for i in range(min(r.NumberParameters, 6))]
                noms, msg = self.cxx_exception(prm)
                if noms:
                    self.dire('      type    : %s' % ' / '.join(noms))
                if msg:
                    self.dire('      message : %s' % msg)
        if c in (0x80000003, 0x80000004, 0x406D1388):
            return DBG_CONTINUE
        return DBG_EXCEPTION_NOT_HANDLED

    def frapper_logiciel(self, bp, tid):
        bp.coups += 1
        ctx = self.contexte(tid)
        if ctx is None:
            return DBG_CONTINUE
        ctx.Rip = bp.adresse                       # revenir sur l'instruction
        self.write(bp.adresse, bp.octet)           # rendre l'octet d'origine
        bp.arme = False
        ctx.EFlags |= TRAP_FLAG                    # tracer un pas puis rearmer
        ctx.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS
        self.poser_contexte(tid, ctx)
        self.rearmer[tid] = bp
        plafond = self.bp_max if bp.max_coups is None else bp.max_coups
        if bp.coups <= plafond and not bp.silencieux:
            self.dire('  BP %s coup %d, thread %d\n        %s'
                      % (bp.nom, bp.coups, tid, self.registres(ctx)))
        if self.on_bp:
            self.on_bp(self, bp, ctx, tid)
        return DBG_CONTINUE

    def frapper_materiel(self, m, ctx, tid):
        m.coups += 1
        if m.coups <= self.dr_max:
            mod, off = self.module_of(ctx.Rip)
            val = self.read(m.adresse, m.taille)
            self.dire('  DR%d %s acces %d : apres 0x%016X = %s+0x%X, valeur %s'
                      % (m.slot, m.nom, m.coups, ctx.Rip, mod, off,
                         val.hex() if val else '?'))
            self.log.append(('DR%d' % m.slot, ctx.Rip, mod, off, True))
        if m.coups == self.dr_max:
            if self.dr_auto_desarmer:
                self.desarmer_materiel(m)
                self.dire('  DR%d %s : %d acces releves, registre libere '
                          '(le jeu reprend sa vitesse)' % (m.slot, m.nom, self.dr_max))
            else:
                self.dire('  DR%d %s : %d acces atteints, on cesse de detailler'
                          % (m.slot, m.nom, self.dr_max))
        if self.on_dr:
            self.on_dr(self, m, ctx, tid)


def main():
    if len(sys.argv) < 3 or sys.argv[1] != 'run':
        print(__doc__)
        return 1
    argv = sys.argv
    exe = os.path.abspath(argv[2])
    cwd = os.path.dirname(exe)
    secs = 30
    dbg = Debugger()
    dbg.quiet = '--silencieux' in argv
    if '--cwd' in argv:
        cwd = os.path.abspath(argv[argv.index('--cwd') + 1])
    if '--secondes' in argv:
        secs = int(argv[argv.index('--secondes') + 1])
    if '--bp-max' in argv:
        dbg.bp_max = int(argv[argv.index('--bp-max') + 1])
    if '--dr-max' in argv:
        dbg.dr_max = int(argv[argv.index('--dr-max') + 1])

    fichier = None
    if '--journal' in argv:
        chemin = argv[argv.index('--journal') + 1]
        os.makedirs(os.path.dirname(os.path.abspath(chemin)), exist_ok=True)
        fichier = open(chemin, 'w', encoding='utf-8')
        dbg.sortie = fichier
        print('journal : %s' % chemin)

    # points d'arret differes : module+offset, resolus quand la DLL arrive
    attente = []
    for i, a in enumerate(argv):
        if a == '--bp':
            s = argv[i + 1]
            if '+' in s:
                mod, off = s.rsplit('+', 1)
                attente.append((mod, int(off, 0), s))
            else:
                dbg.bps.append(PointArret(s, int(s, 0)))
    materiels = []
    for i, a in enumerate(argv):
        if a == '--dr':
            p = argv[i + 1].split(':')
            adr = int(p[0], 0)
            taille = int(p[1]) if len(p) > 1 else 4
            acces = p[2] if len(p) > 2 else 'r'
            materiels.append((adr, taille, acces))
    captures = []
    titre = 'Virtua Fighter'
    if '--titre' in argv:
        titre = argv[argv.index('--titre') + 1]
    for i, a in enumerate(argv):
        if a == '--capture':
            p = argv[i + 1]
            chemin, _, quand = p.partition('@')
            captures.append((os.path.abspath(chemin), float(quand or 5), titre))

    # resolution differee : on branche sur le chargement des modules
    if attente or materiels:
        base_run = dbg.run

        def run(exe_, cwd_, secondes_, captures_):
            reste = list(attente)

            def apres_module():
                for item in list(reste):
                    mod, off, s = item
                    b = dbg.base_de(mod)
                    if b:
                        bp = PointArret(s, b + off)
                        dbg.bps.append(bp)
                        dbg.armer_logiciel(bp)
                        reste.remove(item)
                for adr, taille, acces in materiels:
                    if not any(m and m.adresse == adr for m in dbg.dr):
                        dbg.armer_materiel(adr, taille, acces)
                materiels.clear()

            dbg.armer_en_attente = apres_module
            return base_run(exe_, cwd_, secondes_, captures_)

        dbg.run = run

    r = dbg.run(exe, cwd, secs, captures)
    if dbg.quiet:
        import collections
        c = collections.Counter(dbg.debug_strings)
        dbg.dire('%d message(s) de debogage, %d distincts :'
                 % (len(dbg.debug_strings), len(c)))
        for t, n in c.most_common(80):
            dbg.dire('   %5d x  %s' % (n, t))
    if fichier:
        fichier.close()
        print('journal ecrit : %s' % argv[argv.index('--journal') + 1])
    return r


if __name__ == '__main__':
    sys.exit(main())
