#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le serveur ALL.Net minimal : on laisse le jeu nous dire ce qui manque.

Apres la correction de `System_getGameVersion`, le reseau demarre : `setupLink`
reussit du premier coup, les quatre validations passent, et la machine tourne
dans `Setup` -- elle frappe a `127.0.0.1:8080` (appariement, `abaaslink`) et
`:8081` (serveur de titre, `abaasgs`) sans que personne ne reponde.

Ce serveur repond. Il n'essaie PAS de deviner : il **journalise tout** -- le
chemin, l'en-tete de 16 octets, le JSON dechiffre, et ce qu'on renvoie. Chaque
refus du jeu nommera le champ suivant.

L'enveloppe, telle que `analysis/reseau_allnet.md` #6 la decrit :

    corps = en-tete 16 octets EN CLAIR || AES-256-CBC( zlib( JSON ) )
    et l'en-tete EST le vecteur d'initialisation.

    requete  : h[0]=1 h[1]=1  h[2],h[3]=major,minor  h[4:8]=gameId
               crc32(clair) == be32(h[8:12])
    reponse  : h = 01 01 | be16(code) | be32(crc32) | be32(taille) | 4 aleatoires

    cle Link = SHA256(gameId)  XOR  58b6...13be        (gameId = notre apm.dll)
    cle GS   = titleKey        XOR  58b6...13be        (titleKey = un LITTERAL
                                                        du binaire, 0x1805511D8)

Le `titleKey` a ete remonte le 2026-09-06 : `0x1802198B0` en recopie 32 octets
depuis `0x1805511D8`. Ce n'est donc pas un secret a deviner.

    py -3 tools/serveur_allnet.py
    tools\\serveur_allnet.cmd        (double-cliquable)

Journal au fil de l'eau : analysis\\serveur_allnet.txt
"""
import binascii
import hashlib
import json
import os
import socketserver
import struct
import sys
import threading
import time
import zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from Crypto.Cipher import AES

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
JOURNAL = os.path.join(RACINE, 'analysis', 'serveur_allnet.txt')

# La constante de 32 octets, deja demasquee (`xor al, 0x67` sur 0x1805CC5D0).
CONSTANTE = bytes.fromhex(
    '58b67d7e2caaf2cfccac73eac40586908afa9a6759737225baea4b99ad5213be')
# Le titleKey, littéral en 0x1805511D8, recopie par 0x180219A35.
TITLE_KEY = bytes.fromhex(
    '1469b0169c238709ea4f1bace70217481d6230e6db2abe2f9d17e6336f433481')

VERROU = threading.Lock()
_fichier = None


def note(txt=''):
    with VERROU:
        print(txt)
        if _fichier:
            _fichier.write(txt + os.linesep)
            _fichier.flush()


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def cle_link(game_id):
    """SHA256(gameId) XOR constante -- gameId vient de l'en-tete recu."""
    return xor(hashlib.sha256(game_id).digest(), CONSTANTE)


def cle_gs():
    return xor(TITLE_KEY, CONSTANTE)


def depad(d):
    if not d:
        raise ValueError('corps vide apres dechiffrement')
    n = d[-1]
    if n < 1 or n > 16 or len(d) < n:
        raise ValueError('bourrage PKCS#7 invalide : %d' % n)
    return d[:-n]


def enpad(d):
    n = 16 - (len(d) % 16)
    return d + bytes([n]) * n


def lire(corps, cle_de):
    """Rend (en-tete, JSON en clair) ; leve si quoi que ce soit ne colle pas."""
    if len(corps) < 16:
        raise ValueError('corps trop court : %d octets' % len(corps))
    h, chiffre = corps[:16], corps[16:]
    game_id = h[4:8]
    cle = cle_de(game_id)
    clair = AES.new(cle, AES.MODE_CBC, h).decrypt(chiffre)
    clair = depad(clair)
    if h[0] == 1:                       # octet � compresser �
        clair = zlib.decompress(clair)
    crc_attendu = struct.unpack('>I', h[8:12])[0]
    crc_vu = binascii.crc32(clair) & 0xFFFFFFFF
    if crc_vu != crc_attendu:
        note('        (CRC : recu 0x%08X, calcule 0x%08X -- l en-tete n a '
             'peut-etre pas la disposition qu on croit)' % (crc_attendu, crc_vu))
    return h, clair


def ecrire(obj, cle, code=0):
    """Fabrique le corps d'une reponse."""
    brut = json.dumps(obj, separators=(',', ':')).encode('utf-8')
    z = zlib.compress(brut, 6)
    h = (bytes([1, 1]) + struct.pack('>H', code)
         + struct.pack('>I', binascii.crc32(brut) & 0xFFFFFFFF)
         + struct.pack('>I', len(brut))
         + os.urandom(4))
    return h + AES.new(cle, AES.MODE_CBC, h).encrypt(enpad(z)), brut


# --- ce qu'on repond, route par route ---------------------------------------
# Rien ici n'est devine gratuitement : `turninfo` vient du #10.2 (quatre cles,
# types controles) ; les autres sont volontairement MINIMALES, pour que le
# refus du jeu nous dise quel champ ajouter.
REPONSES_LINK = {
    '/api/alive':     lambda d: {},
    '/api/turninfo':  lambda d: {'host': '127.0.0.1', 'port': 3478,
                                 'id': 'vf5', 'pw': 'vf5'},
    '/api/config':    lambda d: {},
    # Types lus dans le decodeur 0x1802F7DF0 : status nombre, req_id chaine,
    # match objet, route chaine, ready nombre.
    '/api/match':     lambda d: {'status': 0,
                                 'req_id': _req_id(d),
                                 'match': {}, 'route': '', 'ready': 0},
    '/api/log/match_summary':      lambda d: {},
    '/api/log/match_path_quality': lambda d: {},
}


def _req_id(d):
    """Le decodeur exige une chaine ; on renvoie celle que le jeu a envoyee."""
    try:
        m = d.get('match') if isinstance(d, dict) else None
        if isinstance(m, dict) and isinstance(m.get('req_id'), str):
            return m['req_id']
        if isinstance(d, dict) and isinstance(d.get('req_id'), str):
            return d['req_id']
    except Exception:
        pass
    return ''


class Poignee(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, *a):
        pass                                    # on tient notre propre journal

    @property
    def role(self):
        """Link ou GS : les chemins des deux bibliotheques sont disjoints."""
        return 'link' if self.path in REPONSES_LINK else 'gs'

    def do_POST(self):
        t = time.strftime('%H:%M:%S')
        n = int(self.headers.get('Content-Length') or 0)
        corps = self.rfile.read(n)
        note('%s  [%s] POST %s   %d octets' % (t, self.role, self.path, n))
        note('        en-tete : %s' % corps[:16].hex())

        cle_de = cle_link if self.role == 'link' else (lambda _g: cle_gs())
        recu = None
        try:
            h, clair = lire(corps, cle_de)
            note('        version %d.%02d   gameId %r'
                 % (h[2], h[3], bytes(h[4:8])))
            try:
                recu = json.loads(clair)
                note('        JSON recu : %s'
                     % json.dumps(recu, ensure_ascii=False)[:900])
            except Exception:
                note('        clair (non JSON) : %r' % clair[:300])
        except Exception as e:
            note('        DECHIFFREMENT IMPOSSIBLE : %s' % e)
            note('        (corps brut : %s)' % corps[:64].hex())

        table = REPONSES_LINK if self.role == 'link' else {}
        fabrique = table.get(self.path)
        obj = fabrique(recu) if fabrique else {}
        if not fabrique:
            note('        route inconnue -> on repond {} (code 0)')

        cle = cle_de(corps[4:8] if len(corps) >= 8 else b'0000')
        try:
            charge, brut = ecrire(obj, cle)
        except Exception as e:
            note('        ECHEC DE FABRICATION : %s' % e)
            self.send_response(500)
            self.send_header('Content-Length', '0')
            self.end_headers()
            return
        note('        JSON rendu : %s' % brut.decode('utf-8'))
        self.send_response(200)
        self.send_header('Content-Type', 'application/octet-stream')
        self.send_header('Content-Length', str(len(charge)))
        self.end_headers()
        self.wfile.write(charge)

    def do_GET(self):
        note('%s  [%s] GET %s  (inattendu : le jeu ne fait que des POST)'
             % (time.strftime('%H:%M:%S'), self.role, self.path))
        self.send_response(200)
        self.send_header('Content-Length', '0')
        self.end_headers()


def servir(port, poignee):
    srv = ThreadingHTTPServer(('127.0.0.1', port), poignee)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    global _fichier
    os.makedirs(os.path.dirname(JOURNAL), exist_ok=True)
    _fichier = open(JOURNAL, 'w', encoding='utf-8')
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    note('SERVEUR ALL.Net minimal')
    note('  cle Link : SHA256(gameId) XOR constante  (gameId lu dans l en-tete)')
    note('  cle GS   : %s' % cle_gs().hex())
    note('  journal  : %s' % JOURNAL)
    note()
    # Le PORT est cable a 80 dans le moteur : il colle ":80" (0x1805BE120)
    # entre le nom d'hote et le chemin. Les deux bibliotheques partagent donc
    # ce serveur, et se distinguent par leurs chemins.
    servir(80, Poignee)
    note('a l ecoute sur 127.0.0.1:80 -- Link ET GS (chemins disjoints).')
    note('Lancez le jeu, puis fermez cette fenetre pour arreter.')
    note()
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        note('arret.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
