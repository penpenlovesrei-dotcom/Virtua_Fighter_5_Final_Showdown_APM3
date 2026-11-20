#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Lance les deux applications Unity du systeme APM, HORS LIGNE, sous mesure.

CE QUI REND LA CHOSE SURE, et c'est structurel, pas une promesse :

  . `amdaemon.exe` est le SEUL binaire du systeme qui parle a ALL.Net. Il
    porte sept noms de domaine (`aime.naominet.jp`, `naominet.jp`,
    `at.sys-all.net`, `amlog.sys-all.net`, `d-amlog.sys-all.net`, ...) et les
    API `connect`, `WinHttpOpen`, `getaddrinfo`, `send` ;
  . `Apmv3System.exe` et `emoneyUI.exe` n'ont **AUCUNE API reseau**. Leurs
    seuls noms de domaine sont les schemas XML de leur manifeste Windows. Ils
    parlent au daemon par `AMDaemon.NET.dll`, en local.

    -> on ne lance PAS le daemon. Les deux applications n'ont alors aucun
       chemin vers l'exterieur.

LE RISQUE QUI RESTE, et il faut le dire : `UnityPlayer.dll` embarque le
rapport de plantage Unity (`perf-events.cloud.unity3d.com`) et `WSAStartup` /
`getaddrinfo`. Il ne se declenche qu'en cas de plantage, mais je ne peux pas le
prouver inerte. D'ou la MESURE : on releve les connexions TCP du processus a
chaque seconde et on les ecrit dans le journal.

CE QUE CE SCRIPT NE FAIT JAMAIS :

  . il ne lance pas `game.bat`. Ce script d'arcade efface `Y:\`, ecrit dans
    `HKLM\System\SEGA\...` et FLASHE les micrologiciels de la carte USB IO, de
    la carte LED (COM2, 115200) et de la dalle tactile. Sur un PC ordinaire
    c'est destructeur ;
  . il ne touche ni au pare-feu, ni au fichier `hosts`, ni a la base de
    registre. Ce sont des reglages systeme : c'est a Frederic de les changer
    s'il le veut, pas a moi ;
  . il ne travaille jamais sur le dossier d'origine : tout se passe dans une
    COPIE, `runtime/apm_bac/`.

    py -3 tools/apm_lancer.py --preparer        (la copie, une seule fois)
    py -3 tools/apm_lancer.py emoneyUI
    py -3 tools/apm_lancer.py Apmv3System --secondes 30
"""
import json
import os
import shutil
import subprocess
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
SOURCE = r'C:\Users\frede\Desktop\VF5 FS DECOMP\APM_V1.04_internal_0'
BAC = os.path.join(RACINE, 'runtime', 'apm_bac')
JOURNAL = os.path.join(RACINE, 'analysis', 'apm_lancement.log')
APPS = {'emoneyUI': 'emoneyUI.exe', 'Apmv3System': 'Apmv3System.exe'}
# Ce qu'on met a `false` dans la COPIE de la configuration. Ceinture et
# bretelles : le daemon n'est pas lance, mais si quelqu'un le lançait un jour
# depuis le bac, il ne sortirait pas.
A_COUPER = [('allnet_auth', 'enable'), ('allnet_accounting', 'enable'),
            ('network', 'enable'), ('aime', 'enable'), ('usb_io', 'enable'),
            ('apm', 'enable')]


def dire(fp, texte):
    print(texte)
    fp.write(texte + '\n')
    fp.flush()


def preparer(fp):
    if not os.path.isdir(SOURCE):
        dire(fp, 'SOURCE INTROUVABLE : %s' % SOURCE)
        return False
    if not os.path.isdir(BAC):
        dire(fp, 'copie de %s' % SOURCE)
        dire(fp, '   vers  %s   (241 Mo, une seule fois)' % BAC)
        shutil.copytree(SOURCE, BAC)
    else:
        dire(fp, 'bac deja en place : %s' % BAC)

    # on NE lance pas le daemon, mais on desamorce sa configuration quand meme
    cfg = os.path.join(BAC, 'daemon_config', 'common.json')
    if os.path.exists(cfg):
        brut = open(cfg, encoding='utf-8-sig').read()
        try:
            j = json.loads(brut)
        except ValueError as e:
            dire(fp, 'configuration illisible (%s) : laissee telle quelle' % e)
            return True
        change = []
        for bloc, cle in A_COUPER:
            if isinstance(j.get(bloc), dict) and j[bloc].get(cle) is not False:
                j[bloc][cle] = False
                change.append('%s.%s' % (bloc, cle))
        if change:
            with open(cfg, 'w', encoding='utf-8') as g:
                json.dump(j, g, indent=4, ensure_ascii=False)
            dire(fp, 'configuration du bac desamorcee : %s' % ', '.join(change))
        else:
            dire(fp, 'configuration du bac : deja desamorcee')
    return True


def connexions(pid):
    """Les connexions TCP du processus, par PowerShell. Observation seule."""
    r = subprocess.run(
        ['powershell', '-NoProfile', '-Command',
         "Get-NetTCPConnection -OwningProcess %d -ErrorAction SilentlyContinue"
         " | ForEach-Object { \"$($_.State) $($_.RemoteAddress):"
         "$($_.RemotePort)\" }" % pid],
        capture_output=True, text=True)
    return [l.strip() for l in r.stdout.splitlines() if l.strip()]


def main():
    argv = sys.argv[1:]
    os.makedirs(os.path.dirname(JOURNAL), exist_ok=True)
    fp = open(JOURNAL, 'w', encoding='utf-8')
    dire(fp, '=' * 70)
    dire(fp, 'APM HORS LIGNE -- %s' % time.strftime('%Y-%m-%d %H:%M:%S'))
    dire(fp, '=' * 70)

    if not preparer(fp):
        return 1
    if '--preparer' in argv:
        dire(fp, '\nbac pret. Relancez avec le nom d une application.')
        return 0

    quelles = [a for a in argv if a in APPS] or ['emoneyUI']
    secondes = 20
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    for nom in quelles:
        exe = os.path.join(BAC, APPS[nom])
        if not os.path.exists(exe):
            dire(fp, 'introuvable : %s' % exe)
            continue
        dire(fp, '\n--- %s ---' % nom)
        dire(fp, 'amdaemon.exe n est PAS lance : aucun chemin vers ALL.Net.')
        p = subprocess.Popen([exe, '-logFile',
                              os.path.join(RACINE, 'analysis',
                                           'unity_%s.log' % nom)],
                             cwd=BAC)
        dire(fp, 'demarre, pid %d' % p.pid)
        sorties = set()
        for s in range(secondes):
            time.sleep(1)
            if p.poll() is not None:
                dire(fp, '   arrete tout seul apres %d s (code %s)'
                     % (s + 1, p.returncode))
                break
            for c in connexions(p.pid):
                if c not in sorties:
                    sorties.add(c)
                    dire(fp, '   CONNEXION : %s' % c)
        if p.poll() is None:
            dire(fp, '   toujours en vie apres %d s -- on l arrete' % secondes)
            p.kill()
            p.wait()
        dire(fp, '   connexions relevees : %d' % len(sorties))
        if not sorties:
            dire(fp, '   AUCUNE connexion sortante observee.')
        ulog = os.path.join(RACINE, 'analysis', 'unity_%s.log' % nom)
        if os.path.exists(ulog):
            lignes = open(ulog, encoding='utf-8', errors='replace').read()
            dire(fp, '   journal Unity : %d octets' % len(lignes))
            for l in lignes.splitlines()[:15]:
                dire(fp, '      %s' % l[:110])

    dire(fp, '\njournal : %s' % JOURNAL)
    fp.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
