#!/usr/bin/env python3
"""Lecteur d'archives SEGA FARC (variantes FArc et FArC).

Format, gros-boutiste, deduit des en-tetes du dump VF5FS :

    magic       4     'FArc' (brut) ou 'FArC' (compresse)
    header_size 4     octets apres ce champ jusqu'au debut des donnees
    alignment   4     alignement des donnees (1, 0x10, 0x40 observes)
    entrees           jusqu'a epuisement de header_size :
        nom         asciiz
        offset      4
        taille      4          <- FArc : taille du fichier
        taille_dec  4          <- FArC seulement : taille decompressee

Dans les archives FArC, chaque entree est un flux **gzip** (0x1F8B), pas du
deflate brut ; on accepte tout de meme zlib et deflate brut en repli.

Usage :
    py -3 tools/farc.py list <archive>
    py -3 tools/farc.py extract <archive> <dossier_destination>
    py -3 tools/farc.py extract-all <racine> <dossier_destination>
"""
import gzip
import io
import os
import struct
import sys
import zlib


class FarcError(Exception):
    pass


class Farc:
    def __init__(self, path):
        self.path = path
        with open(path, "rb") as fp:
            self.data = fp.read()
        d = self.data
        self.magic = d[:4]
        if self.magic not in (b"FArc", b"FArC", b"FARC"):
            raise FarcError("signature inconnue : %r" % self.magic)
        if self.magic == b"FARC":
            raise FarcError("variante FARC (chiffree/etendue) non prise en charge")
        self.compressed = self.magic == b"FArC"
        self.header_size, self.alignment = struct.unpack(">II", d[4:12])
        self.entries = self._entries()

    def _entries(self):
        d = self.data
        end = 8 + self.header_size          # fin de la zone d'en-tete
        pos = 12                            # apres magic + header_size + alignment
        nfields = 3 if self.compressed else 2
        out = []
        while pos < end:
            nul = d.find(b"\0", pos)
            if nul < 0 or nul + 1 + 4 * nfields > end:
                break
            name = d[pos:nul].decode("latin-1")
            pos = nul + 1
            vals = struct.unpack(">%dI" % nfields, d[pos:pos + 4 * nfields])
            pos += 4 * nfields
            if self.compressed:
                off, csize, usize = vals
            else:
                off, csize = vals
                usize = csize
            out.append(dict(name=name, offset=off, csize=csize, usize=usize))
        return out

    def read(self, entry):
        blob = self.data[entry["offset"]:entry["offset"] + entry["csize"]]
        if not self.compressed:
            return blob
        # Une archive FArC peut contenir des entrees stockees en clair :
        # elles portent une taille decompressee nulle et font `csize` octets.
        if entry["usize"] == 0:
            return blob
        if blob[:2] == b"\x1f\x8b":
            return gzip.GzipFile(fileobj=io.BytesIO(blob)).read()
        # Repli : zlib, puis deflate brut.
        for wbits in (15, -15):
            try:
                return zlib.decompress(blob, wbits)
            except zlib.error:
                continue
        raise FarcError("%s : flux comprime non reconnu (%s)"
                        % (entry["name"], blob[:4].hex()))


def _gz(nom, octets):
    """Un membre gzip a la maniere de SEGA : nom porte, niveau 9, OS Unix.

    Releve sur l'original de `spr_n_fnt32.farc` : `CM=8 FLG=8` (le membre
    porte son nom), `XFL=2` (niveau 9), `OS=3`. Python ecrit 255 pour l'OS ;
    on remet 3, pour que nos archives soient de la meme famille que celles du
    jeu meme a l'octet pres.
    """
    tampon = io.BytesIO()
    with gzip.GzipFile(filename=nom, mode='wb', compresslevel=9,
                       fileobj=tampon, mtime=0) as gz:
        gz.write(octets)
    d = bytearray(tampon.getvalue())
    d[9] = 3
    return bytes(d)


def comme(modele, chemin, membres):
    """Reecrit `chemin` DANS LA FORME de `modele` : variante et alignement.

    TOUT CE QUI REMPLACE UN FICHIER DU JEU passe par ici. Poser un `FArc` la
    ou le jeu avait un `FArC` ferme le jeu -- voir `ecrire_farc`.
    """
    m = Farc(modele)
    return ecrire_farc(chemin, membres, m.alignment or 1, m.compressed)


def ecrire_farc(chemin, membres, alignement=0x10, comprime=False):
    """Ecrit une archive FARC : {nom: octets}. `comprime` choisit la variante.

    « LE MOTEUR LIT LES DEUX VARIANTES, ON PEUT DONC TOUJOURS ECRIRE BRUT » --
    LA SECONDE MOITIE EST FAUSSE, ET C'EST MESURE (2026-10-11)

    C'est ce que disait ce commentaire depuis le 2026-09-10, et c'est ce qui a
    coute « Buttons style ». L'ESSAI QUI TRANCHE : `spr_n_fnt32.farc` reecrite
    en `FArc` BRUT avec le membre d'origine, OCTET POUR OCTET -- meme contenu,
    seul le conteneur change. Le jeu s'est ferme sur un acces interdit
    (0xC0000005) avant meme le menu. Rendue en `FArC`, elle passe.

    CE QUI N'EST PAS DIT PAR LA : que `FArc` soit refuse partout. Le jeu en
    porte lui-meme -- `shader_pxd_w64.farc`, `string_array.farc` -- et nous
    reecrivons celles-la depuis des semaines sans ennui. CE QUI EST MESURE est
    plus etroit, et suffit : CHANGER LA FORME d'une archive qu'on remplace
    peut fermer le jeu. On ne la change donc pas.

    ON ECRIT LA FORME DU FICHIER QU'ON REMPLACE : `comme()` la relit.

        magic 'FArc'/'FArC' | header_size (BE) | alignement (BE)
        entrees : nom asciiz, offset (BE), taille (BE) [, taille_dec (BE)]
        puis les donnees, chacune alignee.
    """
    noms = list(membres)
    champs = 3 if comprime else 2
    charges = dict((n, _gz(n, membres[n]) if comprime else membres[n])
                   for n in noms)
    taille_entetes = sum(len(n.encode('latin-1')) + 1 + 4 * champs
                         for n in noms)
    # `header_size` compte les octets APRES ce champ : l'alignement et les
    # ENTREES -- PAS le remplissage.
    #
    # DEFAUT TROUVE LE 2026-10-11, ET IL A PLANTE LE JEU. En y comptant le
    # remplissage, la zone d'en-tete se terminait sur des zeros, et le
    # lecteur -- le notre comme CELUI DU MOTEUR -- y voyait une entree de plus :
    # un nom vide, taille zero. Les archives de decor l'ont tolere ; la planche
    # de police, non -- `spr_n_fnt32.farc` reecrite ainsi fermait le jeu sur un
    # acces interdit avant meme le menu.
    #
    # L'ORIGINAL LE DIT : `FArC`, header_size = 0x20, alignement = 1, une
    # entree de 0x1C octets -- 12 + 0x1C = 0x28, et les donnees commencent
    # a 0x28. Pas un octet de marge.
    debut = 12 + taille_entetes
    debut = (debut + alignement - 1) // alignement * alignement
    entetes = bytearray()
    donnees = bytearray()
    pos = debut
    for n in noms:
        octets = charges[n]
        entetes += n.encode('latin-1') + b'\x00'
        entetes += struct.pack('>II', pos, len(octets))
        if comprime:
            entetes += struct.pack('>I', len(membres[n]))
        donnees += octets
        avance = (len(octets) + alignement - 1) // alignement * alignement
        donnees += b'\x00' * (avance - len(octets))
        pos += avance
    tete = bytearray(b'FArC' if comprime else b'FArc')
    tete += struct.pack('>II', 4 + taille_entetes, alignement)
    tete += entetes
    tete += b'\x00' * (debut - len(tete))
    with open(chemin, 'wb') as fp:
        fp.write(bytes(tete) + bytes(donnees))
    return len(noms)


def cmd_list(path):
    f = Farc(path)
    print("%s  magic=%s alignment=%d  %d entree(s)"
          % (os.path.basename(path), f.magic.decode(), f.alignment, len(f.entries)))
    print("%-52s %10s %12s %12s" % ("nom", "offset", "stocke", "reel"))
    for e in f.entries:
        print("%-52s 0x%08X %12d %12d"
              % (e["name"], e["offset"], e["csize"], e["usize"]))


def extract_one(path, dest, quiet=False):
    f = Farc(path)
    os.makedirs(dest, exist_ok=True)
    n = 0
    for e in f.entries:
        blob = f.read(e)
        if e["usize"] and len(blob) != e["usize"] and f.compressed:
            print("  ! %s : %d octets obtenus, %d annonces"
                  % (e["name"], len(blob), e["usize"]), file=sys.stderr)
        out = os.path.join(dest, e["name"].replace("/", os.sep))
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        with open(out, "wb") as fp:
            fp.write(blob)
        n += 1
        if not quiet:
            print("%10d  %s" % (len(blob), e["name"]))
    return n


def cmd_extract_all(root, dest):
    total_a = total_f = 0
    errors = []
    for dp, _dn, fns in os.walk(root):
        for fn in fns:
            src = os.path.join(dp, fn)
            try:
                with open(src, "rb") as fp:
                    if fp.read(4) not in (b"FArc", b"FArC"):
                        continue
            except OSError:
                continue
            rel = os.path.relpath(src, root)
            sub = os.path.join(dest, os.path.splitext(rel)[0])
            try:
                total_f += extract_one(src, sub, quiet=True)
                total_a += 1
            except (FarcError, OSError, zlib.error) as exc:
                errors.append((rel, str(exc)))
            if total_a % 25 == 0:
                print("  %d archives, %d fichiers" % (total_a, total_f), flush=True)
    print("%d archives -> %d fichiers dans %s" % (total_a, total_f, dest))
    for rel, msg in errors:
        print("ECHEC %s : %s" % (rel, msg), file=sys.stderr)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "list":
        cmd_list(sys.argv[2])
    elif cmd == "extract":
        n = extract_one(sys.argv[2], sys.argv[3])
        print("%d fichier(s) -> %s" % (n, sys.argv[3]))
    elif cmd == "extract-all":
        cmd_extract_all(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
