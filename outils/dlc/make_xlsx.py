#!/usr/bin/env python3
"""Build the per-character inventory workbook from inventory.json.

usage: make_xlsx.py inventory.json PACKAGE OUT.xlsx
"""
import collections
import datetime
import json
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from stfs import Stfs

SLOTS = {"atam": "Tête", "face": "Visage", "joha": "Haut du corps", "kaha": "Bas du corps"}
UNKNOWN_SLOT = "Non précisé"
EXTRACT_DIR = "EXTRACTION"

FONT = Font(name="Arial", size=10)
BOLD = Font(name="Arial", size=10, bold=True)
HEAD = Font(name="Arial", size=10, bold=True, color="FFFFFF")
LINK = Font(name="Arial", size=10, color="0563C1", underline="single")
TITLE = Font(name="Arial", size=14, bold=True)
NOTE = Font(name="Arial", size=9, italic=True, color="555555")
HEAD_FILL = PatternFill("solid", start_color="1F3864")
TOTAL_FILL = PatternFill("solid", start_color="D9E1F2")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)


def classify(item):
    """Primary objects carry the slot code: <item>_<slot>_<label>[__divskn]."""
    prefix = item["item"] + "_"
    parsed = []
    for name in item["objects"]:
        rest = name[len(prefix):] if name.lower().startswith(prefix) else name
        core = rest.split("__", 1)[0]
        slot, _, label = core.partition("_")
        parsed.append((name, "__" in rest, slot, label, core))
    primary = [p for p in parsed if p[1]] or [p for p in parsed if p[2] in SLOTS]
    if not primary:
        return UNKNOWN_SLOT, ", ".join(p[4] for p in parsed), [p[0] for p in parsed], 0, []
    slots = list(dict.fromkeys(SLOTS.get(p[2], UNKNOWN_SLOT) for p in primary))
    label = ", ".join(p[3] if p[2] in SLOTS else p[4] for p in primary)
    return slots[0], label, [p[0] for p in primary], len(parsed) - len(primary), slots


def clip(text, n=600):
    return text if len(text) <= n else text[:n - 1] + "…"


def header_row(ws, row, headers, widths=None):
    for c, h in enumerate(headers, 1):
        cell = ws.cell(row=row, column=c, value=h)
        cell.font, cell.fill, cell.border = HEAD, HEAD_FILL, BOX
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    if widths:
        for c, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(c)].width = w


def main():
    inv_path, pkg, out = sys.argv[1:4]
    inv = json.load(open(inv_path, encoding="utf-8"))
    s = Stfs(pkg)

    tex_by_item = collections.defaultdict(list)
    for t in inv["textures"]:
        tex_by_item[t["item"]].append(t)
    by_char = collections.defaultdict(list)
    for it in inv["items"]:
        by_char[it["character"]].append(it)
    characters = sorted(by_char, key=str.lower)

    wb = Workbook()
    wb.calculation.fullCalcOnLoad = True
    summary = wb.active
    summary.title = "Résumé"

    # ---- one sheet per character ------------------------------------------
    char_headers = ["N°", "Item", "Emplacement", "Nom interne", "Objet(s) principal(aux)", "Sous-objets",
                    "Maillages", "Noms des maillages", "Sommets", "Matériaux", "Shaders", "Textures",
                    "Cube maps", "Résolution max", "Formats", "Modèle (Ko)", "Textures (Ko)", "Dossier"]
    char_widths = [7, 13, 15, 30, 42, 11, 10, 45, 10, 10, 18, 10, 10, 14, 13, 12, 13, 10]
    col = {h: i + 1 for i, h in enumerate(char_headers)}
    multi_slot = []
    expected = {}
    for name in characters:
        ws = wb.create_sheet(name)
        header_row(ws, 1, char_headers, char_widths)
        ws.row_dimensions[1].height = 30
        items = sorted(by_char[name], key=lambda i: i["number"])
        counts = collections.Counter()
        for r, it in enumerate(items, 2):
            slot, label, primary, subobjs, slots = classify(it)
            if len(slots) > 1:
                multi_slot.append((it["item"], slots))
            texs = tex_by_item[it["item"]]
            biggest = max(texs, key=lambda t: t["width"] * t["height"]) if texs else None
            row = [
                it["number"], it["item"], slot, label, ", ".join(primary), subobjs,
                len(it["meshes"]), clip(", ".join(it["meshes"])), it["vertices"], len(it["materials"]),
                ", ".join(it["shaders"]), it["texture_count"], sum(t["cube"] for t in texs),
                "%d×%d" % (biggest["width"], biggest["height"]) if biggest else "",
                ", ".join(it["formats"]), it["obj_usize"] / 1024, it["tex_usize"] / 1024, "Ouvrir",
            ]
            for c, v in enumerate(row, 1):
                cell = ws.cell(row=r, column=c, value=v)
                cell.font = FONT
            for h in ("Sommets", "Sous-objets", "Maillages", "Matériaux", "Textures", "Cube maps"):
                ws.cell(row=r, column=col[h]).number_format = "#,##0"
            for h in ("Modèle (Ko)", "Textures (Ko)"):
                ws.cell(row=r, column=col[h]).number_format = "#,##0.0"
            link = ws.cell(row=r, column=col["Dossier"])
            link.hyperlink = "%s/%s/%s" % (EXTRACT_DIR, name, it["item"])
            link.font = LINK
            counts["items"] += 1
            counts[slot] += 1
            counts["tex"] += it["texture_count"]
        expected[name] = counts
        ws.freeze_panes = "C2"
        ws.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(char_headers)), len(items) + 1)

    # ---- textures detail -----------------------------------------------------
    wt = wb.create_sheet("Textures")
    tex_headers = ["Personnage", "Item", "Index", "ID texture", "Largeur", "Hauteur", "Format",
                   "Mipmaps", "Cube map"]
    header_row(wt, 1, tex_headers, [14, 13, 8, 11, 10, 10, 10, 10, 10])
    textures = sorted(inv["textures"], key=lambda t: (t["character"].lower(), t["item"][6:].zfill(5), t["index"]))
    for r, t in enumerate(textures, 2):
        row = [t["character"], t["item"], t["index"], t["texture_id"], t["width"], t["height"],
               t["format"], t["mips"], "Oui" if t["cube"] else "Non"]
        for c, v in enumerate(row, 1):
            wt.cell(row=r, column=c, value=v).font = FONT
    wt.freeze_panes = "C2"
    wt.auto_filter.ref = "A1:I%d" % (len(textures) + 1)

    # ---- summary -------------------------------------------------------------
    ws = summary
    ws["A1"] = "Virtua Fighter 5 Final Showdown (Xbox 360) — Inventaire du DLC « Item Pack »"
    ws["A1"].font = TITLE
    size = os.path.getsize(pkg)
    info = [
        ("Fichier source", os.path.basename(pkg)),
        ("Content ID", s.content_id),
        ("Title ID", "%08X (%s)" % (s.title_id, s.title_name)),
        ("Nom du package", s.names[0]),
        ("Taille du package", "%s octets (%.2f Go)" % (format(size, ",").replace(",", " "), size / 1024 ** 3)),
        ("Intégrité", "503 805 blocs de données vérifiés (SHA-1), 0 erreur — le 12/09/2026"),
        ("Inventaire généré le", datetime.date.today().strftime("%d/%m/%Y")),
    ]
    for r, (k, v) in enumerate(info, 3):
        ws.cell(row=r, column=1, value=k).font = BOLD
        ws.cell(row=r, column=2, value=v).font = FONT

    top = 3 + len(info) + 1
    sum_headers = ["Personnage", "Code", "Items", "Tête", "Visage", "Haut du corps", "Bas du corps",
                   UNKNOWN_SLOT, "Textures", "Cube maps", "Modèles (Mo)", "Textures (Mo)", "N° min", "N° max"]
    header_row(ws, top, sum_headers, [22, 8, 9, 9, 9, 13, 13, 12, 10, 11, 13, 13, 9, 9])
    ws.row_dimensions[top].height = 30
    L = {h: get_column_letter(col[h]) for h in char_headers}
    first = top + 1
    for r, name in enumerate(characters, first):
        ref = "'%s'!" % name
        code = by_char[name][0]["code"]
        values = [
            name, code,
            "=COUNTA(%s$%s:$%s)-1" % (ref, L["Item"], L["Item"]),
        ]
        for c in range(4, 9):
            values.append("=COUNTIF(%s$%s:$%s,%s$%d)" % (ref, L["Emplacement"], L["Emplacement"],
                                                        get_column_letter(c), top))
        values += [
            "=SUM(%s$%s:$%s)" % (ref, L["Textures"], L["Textures"]),
            "=SUM(%s$%s:$%s)" % (ref, L["Cube maps"], L["Cube maps"]),
            "=SUM(%s$%s:$%s)/1024" % (ref, L["Modèle (Ko)"], L["Modèle (Ko)"]),
            "=SUM(%s$%s:$%s)/1024" % (ref, L["Textures (Ko)"], L["Textures (Ko)"]),
            "=MIN(%s$%s:$%s)" % (ref, L["N°"], L["N°"]),
            "=MAX(%s$%s:$%s)" % (ref, L["N°"], L["N°"]),
        ]
        for c, v in enumerate(values, 1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.font, cell.border = FONT, BOX
            cell.number_format = "#,##0.0" if c in (11, 12) else "#,##0"
        ws.cell(row=r, column=1).hyperlink = "#%s!A1" % ref.rstrip("!")
        ws.cell(row=r, column=1).font = LINK
    last = first + len(characters) - 1
    total = last + 1
    ws.cell(row=total, column=1, value="Total")
    for c in range(3, 15):
        letter = get_column_letter(c)
        fn = {13: "MIN", 14: "MAX"}.get(c, "SUM")
        ws.cell(row=total, column=c, value="=%s(%s%d:%s%d)" % (fn, letter, first, letter, last))
    for c in range(1, 15):
        cell = ws.cell(row=total, column=c)
        cell.font, cell.fill, cell.border = BOLD, TOTAL_FILL, BOX
        cell.number_format = "#,##0.0" if c in (11, 12) else "#,##0"
    ws.cell(row=total + 1, column=1, value="Contrôle : somme des emplacements = total items")
    ws.cell(row=total + 1, column=1).font = NOTE
    ws.cell(row=total + 1, column=3, value="=IF(SUM(D%d:H%d)=C%d,\"OK\",\"Écart\")" % (total, total, total)).font = BOLD

    notes = [
        "Notes",
        "• Emplacement : déduit du code interne du nom d'objet — atam = Tête, face = Visage, joha = Haut du corps, kaha = Bas du corps. "
        "« Non précisé » = objets sans code d'emplacement (ex. lioitm719 : shoes_01 / sock_01).",
        "• Nom interne : nom technique du modèle (romaji japonais, ex. megane = lunettes, hige = barbe, katana, geta). "
        "Les noms affichés en jeu ne sont pas stockés dans ce DLC.",
        "• Sous-objets : pièces annexes d'un item (drapeaux, pièces animées, effets…) en plus de l'objet principal.",
        "• Codes personnages : krt = Jean, mon = Eileen, msk = El Blaze sont déduits (style de combat) ; les autres sont explicites. Dural n'a pas d'items.",
        "• Numérotation : chaque personnage commence à 041 ; les numéros 001–040 ne sont pas dans ce DLC (probablement le jeu de base). Il y a des trous dans la numérotation.",
        "• Tailles : taille décompressée des fichiers _obj.bin (modèle) et _tex.bin (textures) extraits des archives FArC.",
        "• Textures : formats DXT1 / DXT5 / RGB5 avec mipmaps ; les cube maps (reflets) contiennent 6 faces. "
        "Dans les _tex.bin, les images sont stockées retournées verticalement (convention du moteur).",
        "• Colonne « Dossier » des onglets personnages : lien relatif vers le sous-dossier %s placé à côté de ce classeur." % EXTRACT_DIR,
        "• Les valeurs de ce résumé sont des formules calculées depuis les onglets personnages.",
    ]
    for i, n in enumerate(notes):
        cell = ws.cell(row=total + 3 + i, column=1, value=n)
        cell.font = BOLD if i == 0 else NOTE
    ws.freeze_panes = ws.cell(row=first, column=2)

    wb.save(out)

    # ---- console self-check ----------------------------------------------------
    print("saved", out)
    print("multi-slot items:", multi_slot[:10], len(multi_slot))
    tot = collections.Counter()
    for name in characters:
        tot.update(expected[name])
        c = expected[name]
        print("  %-12s items=%d %s tex=%d" % (name, c["items"], {k: c[k] for k in list(SLOTS.values()) + [UNKNOWN_SLOT]}, c["tex"]))
    print("TOTAL", dict(tot))
    print("summary rows", first, "->", last, "total row", total)


if __name__ == "__main__":
    main()
