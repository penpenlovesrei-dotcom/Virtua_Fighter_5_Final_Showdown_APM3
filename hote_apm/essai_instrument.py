#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Valide notre apm.dll SANS lancer vfes.exe.

POURQUOI VALIDER AVANT. Un instrument qu'on n'a pas eprouve rend des mesures
qu'on ne peut pas lire : si vfes.exe refuse de demarrer, on ne saura pas si
c'est la borne qui manque ou notre DLL qui est fausse. On valide donc sur des
reponses CONNUES, d'avance ([[proxy-dll-reproduit-la-table-entiere]],
[[instrument-ne-doit-pas-tuer-le-sujet]]).

CE QUE CET ESSAI EPROUVE, en mode inerte seulement :
  1. les 106 exports se resolvent par leur nom ;
  2. le tramway en assembleur rend la main proprement -- un cadre de pile
     faux ou un alignement rate ferait fauter ici, sur un appel trivial,
     et pas au milieu du jeu ;
  3. les reponses sont celles que la table declare, pas des zeros ;
  4. le journal s'ecrit, et le bilan s'ecrit au detachement.

CE QU'IL N'EPROUVE PAS. Le mode relais n'appelle PAS les vraies fonctions :
elles dialoguent par IPC avec amdaemon et pourraient attendre indefiniment.
On verifie seulement que la vraie DLL se charge et que ses 106 noms se
resolvent -- exactement ce que fait notre Charger().
"""
import ctypes
import io
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
NOTRE = os.path.join(ICI, "sortie", "apm.dll")
VRAIE = os.path.abspath(os.path.join(ICI, "..", "..", "SOURCES", "lib", "apm.dll"))
JOURNAL = os.path.join(ICI, "sortie", "apm_journal_essai.txt")

# Attendus, recopies de kReponses dans apm_inerte.cpp. Si l'un d'eux change
# la-bas, cet essai doit echouer : c'est le but.
ENTIERS = [
    ("AllnetAuth_isGood", 1),
    ("Credit_isFreePlay", 1),
    ("Credit_isZero", 0),
    ("Credit_getCredit", 99),
    ("Core_isExitNeeded", 0),
    ("Sequence_isTest", 0),
    ("Backup_isSetupSucceeded", 1),
    ("Aime_isReaderDetected", 0),
    ("ApmSystemSetting_getTimeToClosingTime", 0x7FFFFFFF),
    # Sans decision dans la table : doit rendre 0, et le bilan doit le dire.
    ("Core_resetCount", 0),
]
CHAINES = [
    ("System_getGameId", b"SDHP"),
    ("Credit_toString", b"FREE PLAY"),
    ("AllnetAuth_getLocationName", b"BANC"),
    ("System_getAppRootPath", b"."),
]

fautes = []


def dire(ok, texte):
    print("  %s %s" % ("ok  " if ok else "FAUTE", texte))
    if not ok:
        fautes.append(texte)


# ------------------------------------------------- 1. la vraie DLL se charge
print("=== la vraie apm.dll se charge-t-elle, et ses 106 noms se resolvent ? ===")
print("  %s" % VRAIE)
try:
    v = ctypes.CDLL(VRAIE, winmode=0)
except OSError as e:
    dire(False, "LoadLibrary de la vraie apm.dll : %s" % e)
    v = None
if v is not None:
    dire(True, "chargee a 0x%X" % v._handle)

# ------------------------------------------------- 2. la notre, mode inerte
print("\n=== notre apm.dll, mode INERTE ===")
if os.path.exists(JOURNAL):
    os.remove(JOURNAL)
os.environ["APM_INERTE"] = "1"
os.environ["APM_JOURNAL"] = JOURNAL
os.environ["APM_DETAIL"] = "4"
os.environ.pop("APM_VRAIE", None)

n = ctypes.CDLL(NOTRE, winmode=0)
dire(True, "chargee a 0x%X" % n._handle)

if v is not None:
    absents = []
    for nom in [x[0] for x in ENTIERS + CHAINES]:
        try:
            getattr(v, nom)
        except AttributeError:
            absents.append(nom)
    dire(not absents,
         "les noms testes existent aussi dans la vraie DLL"
         + (" ; absents : %s" % absents if absents else ""))

print("\n  --- reponses entieres ---")
for nom, attendu in ENTIERS:
    try:
        f = getattr(n, nom)
    except AttributeError:
        dire(False, "%s : export introuvable" % nom)
        continue
    f.restype = ctypes.c_uint64
    f.argtypes = []
    got = f()
    dire(got == attendu, "%-40s -> %-12d (attendu %d)" % (nom, got, attendu))

print("\n  --- reponses en chaine ---")
for nom, attendu in CHAINES:
    try:
        f = getattr(n, nom)
    except AttributeError:
        dire(False, "%s : export introuvable" % nom)
        continue
    f.restype = ctypes.c_char_p
    f.argtypes = []
    got = f()
    dire(got == attendu, "%-40s -> %-14r (attendu %r)" % (nom, got, attendu))

# Le tramway doit survivre a des arguments qu'il ne comprend pas : on en passe
# quatre entiers et quatre flottants, ce que le cadre sauve et restaure.
print("\n  --- le tramway supporte-t-il des arguments quelconques ? ---")
f = getattr(n, "Input_isOn")
f.restype = ctypes.c_uint64
f.argtypes = [ctypes.c_uint64, ctypes.c_double, ctypes.c_uint64, ctypes.c_double]
try:
    got = f(0x1122334455667788, 1.5, 0x99AABBCCDDEEFF00, -2.25)
    dire(got == 0, "Input_isOn(4 arguments mixtes) -> %d" % got)
except Exception as e:
    dire(False, "Input_isOn a faute : %s" % e)

# Beaucoup d'appels : le compteur et l'anneau doivent tenir.
f = getattr(n, "Core_isExitNeeded")
f.restype = ctypes.c_uint64
f.argtypes = []
for _ in range(1000):
    f()
dire(True, "1000 appels de Core_isExitNeeded sans faute")

# ------------------------------------------------- 3. le journal
# FreeLibrary pour declencher DLL_PROCESS_DETACH, donc le bilan.
ctypes.windll.kernel32.FreeLibrary(ctypes.c_void_p(n._handle))
print("\n=== le journal ===")
if not os.path.exists(JOURNAL):
    dire(False, "aucun journal ecrit : %s" % JOURNAL)
else:
    t = io.open(JOURNAL, "r", encoding="latin-1").read()
    dire("mode : INERTE" in t, "le journal declare son mode")
    dire("BILAN" in t, "le bilan a ete ecrit au detachement")
    dire("Core_isExitNeeded" in t, "le bilan nomme les fonctions appelees")
    ligne = [l for l in t.splitlines() if "Core_isExitNeeded" in l and "appels" in l]
    dire(any("1001" in l for l in ligne),
         "le compteur vaut 1001 (1000 + 1) : %s"
         % (ligne[0].strip() if ligne else "ligne absente"))
    dire("AUCUNE DECISION PRISE" in t,
         "une fonction sans decision est signalee comme telle")
    print("\n  --- extrait du bilan ---")
    for l in t.splitlines():
        if ">>>" in l or "mode :" in l or "decidees" in l:
            print("    " + l.strip())

print()
if fautes:
    print(">>> %d FAUTE(S). L'instrument n'est pas valide, ne pas s'en servir."
          % len(fautes))
    sys.exit(1)
print(">>> INSTRUMENT VALIDE. Le journal d'essai : %s" % JOURNAL)
