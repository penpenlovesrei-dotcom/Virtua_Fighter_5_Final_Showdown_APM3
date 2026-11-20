#!/usr/bin/env python3
"""Build the VF5 (2007) <-> Final Showdown item comparison workbook from matches.json.

usage: make_comparison_xlsx.py matches.json OUT.xlsx [games_inventory.json thumbs.json]
"""
import collections
import datetime
import json
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from match_items import STATUSES
from sources import GAMES, ROOT
from texture_pairs import NORMAL_MAP_FORMAT, higher_res_textures

HIRES_SHEET = "Textures VF5 haute résolution"

SLOTS = {"atam": "Tête", "face": "Visage", "joha": "Haut du corps", "kaha": "Bas du corps"}
SOURCE = {"fs": "Base", "dlc": "DLC"}

FONT = Font(name="Arial", size=10)
BOLD = Font(name="Arial", size=10, bold=True)
HEAD = Font(name="Arial", size=10, bold=True, color="FFFFFF")
LINK = Font(name="Arial", size=10, color="0563C1", underline="single")
TITLE = Font(name="Arial", size=14, bold=True)
NOTE = Font(name="Arial", size=9, italic=True, color="555555")
HEAD_FILL = PatternFill("solid", start_color="1F3864")
TOTAL_FILL = PatternFill("solid", start_color="D9E1F2")
STATUS_FILL = {
    "Identique": PatternFill("solid", start_color="C6EFCE"),
    "Modifié": PatternFill("solid", start_color="FFF2CC"),
    "Refait": PatternFill("solid", start_color="FCE4D6"),
    "Incertain": PatternFill("solid", start_color="DDEBF7"),
    "Absent du FS": PatternFill("solid", start_color="F8CBAD"),
}
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)


def rel_dir(game, character, item):
    path = os.path.join(GAMES[game]["extract_dir"], character, item)
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def slot_of(label, number):
    first = label.split(",")[0].strip()
    head = first.split("_")[0]
    if head in SLOTS:
        return SLOTS[head]
    if number == 0:
        return "Corps de base"
    return "—" if not first else "Autre"


def pct(x):
    return None if x is None else round(x, 4)


def fmt_label(fmt):
    return "Non compressé 16 bits" if fmt == NORMAL_MAP_FORMAT else fmt


def header_row(ws, headers, widths):
    for c, (h, w) in enumerate(zip(headers, widths), 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.font, cell.fill, cell.border = HEAD, HEAD_FILL, BOX
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = "D2"


def write_row(ws, r, values, formats=None):
    for c, v in enumerate(values, 1):
        cell = ws.cell(row=r, column=c, value=v)
        cell.font = FONT
        if formats and c in formats:
            cell.number_format = formats[c]


def link(ws, r, c, target, text="Ouvrir"):
    cell = ws.cell(row=r, column=c, value=text)
    cell.hyperlink = target
    cell.font = LINK


def reason(best):
    parts = []
    parts.append("même numéro" if best["same_num"] else "numéro différent")
    parts.append("même nom interne" if best["same_stem"] else "nom interne différent")
    if best["geo"] > 0:
        parts.append("géométrie identique à %d %%" % round(100 * best["geo"]))
    if best["mesh"] > 0:
        parts.append("maillages communs à %d %%" % round(100 * best["mesh"]))
    if best["tex"]:
        parts.append("textures identiques à %d %%" % round(100 * best["tex"]))
    return ", ".join(parts)


def main():
    matches_path, out = sys.argv[1:3]
    here = os.path.dirname(os.path.abspath(__file__))
    inv_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(here, "games_inventory.json")
    thumbs_path = sys.argv[4] if len(sys.argv) > 4 else os.path.join(here, "thumbs.json")
    data = json.load(open(matches_path, encoding="utf-8"))
    vf5 = sorted(data["vf5"], key=lambda r: (r["character"].lower(), r["number"]))
    fs = sorted(data["fs"], key=lambda f: (f["character"].lower(), f["game"] != "fs", f["number"]))
    fs_by_num = collections.defaultdict(dict)
    for f in fs:
        fs_by_num[f["code"]].setdefault(f["number"], f)

    wb = Workbook()
    wb.calculation.fullCalcOnLoad = True
    summary = wb.active
    summary.title = "Résumé"

    # ---- Correspondances ----------------------------------------------------------
    ws = wb.create_sheet("Correspondances")
    heads = ["Personnage", "N° VF5", "Item VF5", "Nom anglais (VF5)", "Variantes de couleur", "Emplacement",
             "Nom interne VF5", "Statut", "Source FS", "Item FS", "N° FS", "Nom interne FS", "Même n°",
             "Modèle 3D", "Textures", "Géométrie identique", "Maillages communs", "Textures identiques",
             "Autres items FS correspondants", "Dossier VF5", "Dossier FS"]
    header_row(ws, heads, [12, 8, 12, 28, 34, 14, 30, 13, 9, 12, 7, 30, 9, 30, 19, 11, 11, 11, 32, 9, 9])
    pct_cols = {16: "0%", 17: "0%", 18: "0%"}
    for r, it in enumerate(vf5, 2):
        b = it["best"]
        shown = b if b else {}
        others = ", ".join("%s:%s" % (SOURCE[o["game"]], o["item"]) for o in it["others"])
        write_row(ws, r, [
            it["character"], it["number"], it["item"], it["name"], ", ".join(it["variants"]),
            slot_of(it["label"], it["number"]), it["label"], it["status"],
            SOURCE.get(shown.get("game")), shown.get("item"), shown.get("number"), shown.get("label"),
            ("Oui" if shown.get("same_num") else "Non") if b else None,
            shown.get("model"), shown.get("textures"),
            pct(shown.get("geo")), pct(shown.get("mesh")), pct(shown.get("tex")), others or None,
        ], pct_cols)
        ws.cell(row=r, column=8).fill = STATUS_FILL[it["status"]]
        link(ws, r, 20, rel_dir("vf5", it["character"], it["item"]))
        if b:
            link(ws, r, 21, rel_dir(b["game"], it["character"], b["item"]))
    ws.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(heads)), len(vf5) + 1)
    corr_rows = len(vf5) + 1

    # ---- Absents du FS ----------------------------------------------------------
    wa = wb.create_sheet("Absents du FS")
    heads_a = ["Personnage", "N° VF5", "Item VF5", "Nom anglais (VF5)", "Variantes de couleur", "Emplacement",
               "Nom interne VF5", "Remarque", "Dossier VF5"]
    header_row(wa, heads_a, [12, 8, 12, 28, 34, 14, 32, 60, 10])
    r = 2
    for it in vf5:
        if it["status"] != "Absent du FS":
            continue
        notes = []
        if not it["label"]:
            notes.append("Texture seule, sans modèle 3D")
        if not it["name"]:
            notes.append("Sans nom dans la table VF5 (pièce de costume ou item non listé)")
        same = fs_by_num[it["code"]].get(it["number"])
        if same:
            notes.append("N° %d utilisé dans le FS (%s) par un autre item : %s" % (it["number"], SOURCE[same["game"]], same["label"]))
        write_row(wa, r, [it["character"], it["number"], it["item"], it["name"], ", ".join(it["variants"]),
                          slot_of(it["label"], it["number"]), it["label"], " ; ".join(notes) or None])
        link(wa, r, 9, rel_dir("vf5", it["character"], it["item"]))
        r += 1
    wa.auto_filter.ref = "A1:I%d" % max(r - 1, 1)

    # ---- Incertains -------------------------------------------------------------
    wi = wb.create_sheet("Incertains")
    heads_i = ["Personnage", "N° VF5", "Item VF5", "Nom anglais (VF5)", "Nom interne VF5", "Candidat FS",
               "Source", "Nom interne FS", "Indices", "Autres candidats faibles", "Dossier VF5", "Dossier FS"]
    header_row(wi, heads_i, [12, 8, 12, 28, 30, 12, 8, 30, 60, 34, 10, 10])
    r = 2
    for it in vf5:
        if it["status"] != "Incertain":
            continue
        b = it["best"]
        write_row(wi, r, [it["character"], it["number"], it["item"], it["name"], it["label"], b["item"],
                          SOURCE[b["game"]], b["label"], reason(b),
                          ", ".join("%s:%s" % (SOURCE[w["game"]], w["item"]) for w in it["weak"]) or None])
        link(wi, r, 11, rel_dir("vf5", it["character"], it["item"]))
        link(wi, r, 12, rel_dir(b["game"], it["character"], b["item"]))
        r += 1
    wi.auto_filter.ref = "A1:L%d" % max(r - 1, 1)

    # ---- Textures VF5 haute résolution -----------------------------------------------
    hires = higher_res_textures(data, json.load(open(inv_path, encoding="utf-8"))["items"],
                                json.load(open(thumbs_path, encoding="utf-8")))
    hires.sort(key=lambda p: (p["fs"]["model"] != "Identique", p["vf5"]["character"].lower(),
                              p["vf5"]["number"], p["i"]))
    wt = wb.create_sheet(HIRES_SHEET)
    heads_t = ["Personnage", "Item VF5", "Nom anglais (VF5)", "Statut de l'item", "Modèle 3D identique dans le FS",
               "Modèle 3D FS", "Type de texture", "Texture VF5", "Résolution VF5", "Format VF5", "Source FS",
               "Item FS", "Texture FS", "Résolution FS", "Format FS", "Pixels VF5 / FS", "Même position",
               "Dossier VF5", "Dossier FS"]
    header_row(wt, heads_t, [12, 12, 26, 11, 14, 30, 18, 9, 12, 20, 9, 12, 9, 12, 10, 10, 10, 10, 10])
    for r, p in enumerate(hires, 2):
        it, b = p["vf5"], p["fs"]
        wa, ha, fa = p["vf5_tex"][:3]
        wb_, hb, fb = p["fs_tex"][:3]
        same_model = b["model"] == "Identique"
        write_row(wt, r, [
            it["character"], it["item"], it["name"] or None, it["status"], "Oui" if same_model else "Non",
            b["model"], "Normal map (relief)" if p["normal_map"] else "Couleur / autre",
            "tex%02d" % p["i"], "%d × %d" % (wa, ha), fmt_label(fa), SOURCE[b["game"]], b["item"],
            "tex%02d" % p["j"], "%d × %d" % (wb_, hb), fmt_label(fb), (wa * ha) / (wb_ * hb),
            "Oui" if p["i"] == p["j"] else "Non",
        ], {16: '"×"0'})
        wt.cell(row=r, column=5).fill = STATUS_FILL["Identique"] if same_model else STATUS_FILL["Refait"]
        link(wt, r, 18, rel_dir("vf5", it["character"], it["item"]))
        link(wt, r, 19, rel_dir(b["game"], it["character"], b["item"]))
    wt.auto_filter.ref = "A1:S%d" % max(len(hires) + 1, 2)

    # ---- Items FS ----------------------------------------------------------------
    wf = wb.create_sheet("Items FS")
    heads_f = ["Personnage", "Source", "N° FS", "Item FS", "Emplacement", "Nom interne FS",
               "Équivalent VF5", "Items VF5 correspondants", "Dossier FS"]
    header_row(wf, heads_f, [12, 8, 8, 12, 14, 34, 11, 34, 10])
    for r, f in enumerate(fs, 2):
        write_row(wf, r, [f["character"], SOURCE[f["game"]], f["number"], f["item"], slot_of(f["label"], f["number"]),
                          f["label"], "Oui" if f["vf5"] else "Non", ", ".join(f["vf5"]) or None])
        link(wf, r, 9, rel_dir(f["game"], f["character"], f["item"]))
    wf.auto_filter.ref = "A1:I%d" % (len(fs) + 1)

    # ---- Résumé -------------------------------------------------------------------
    ws = summary
    ws["A1"] = "Virtua Fighter 5 (2007) ↔ Final Showdown — comparaison des items de personnalisation"
    ws["A1"].font = TITLE
    info = [
        ("VF5 (2007)", "Xbox 360, Title ID 534507EE — dossier « Virtua Fight3r 5 AnDreXplay »"),
        ("Final Showdown", "Xbox 360 (XBLA), Title ID 584111FE — jeu de base (package 7D2DF36B…) + DLC « Item Pack » (408E3ECB…)"),
        ("Noms des items", "Table anglaise de VF5 (media/lang/en/rom/chritm_tbl.farc)"),
        ("Généré le", datetime.date.today().strftime("%d/%m/%Y")),
    ]
    for i, (k, v) in enumerate(info, 3):
        ws.cell(row=i, column=1, value=k).font = BOLD
        ws.cell(row=i, column=2, value=v).font = FONT

    top = 3 + len(info) + 1
    chars = sorted({x["character"] for x in vf5} | {x["character"] for x in fs}, key=str.lower)
    sum_heads = ["Personnage", "Items VF5", "Nommés"] + STATUSES + ["Items FS (base)", "Items FS (DLC)",
                                                                   "FS avec équivalent VF5", "FS sans équivalent VF5"]
    widths = [22, 10, 9, 10, 10, 10, 10, 12, 12, 12, 13, 13]
    for c, (h, w) in enumerate(zip(sum_heads, widths), 1):
        cell = ws.cell(row=top, column=c, value=h)
        cell.font, cell.fill, cell.border = HEAD, HEAD_FILL, BOX
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.row_dimensions[top].height = 32
    C = "'Correspondances'!"
    F = "'Items FS'!"
    first = top + 1
    for r, name in enumerate(chars, first):
        row = [name,
               "=COUNTIF(%s$A:$A,$A%d)" % (C, r),
               "=COUNTIFS(%s$A:$A,$A%d,%s$D:$D,\"<>\")" % (C, r, C)]
        for k in range(len(STATUSES)):
            col = get_column_letter(4 + k)
            row.append("=COUNTIFS(%s$A:$A,$A%d,%s$H:$H,%s$%d)" % (C, r, C, col, top))
        row += ["=COUNTIFS(%s$A:$A,$A%d,%s$B:$B,\"Base\")" % (F, r, F),
                "=COUNTIFS(%s$A:$A,$A%d,%s$B:$B,\"DLC\")" % (F, r, F),
                "=COUNTIFS(%s$A:$A,$A%d,%s$G:$G,\"Oui\")" % (F, r, F),
                "=COUNTIFS(%s$A:$A,$A%d,%s$G:$G,\"Non\")" % (F, r, F)]
        for c, v in enumerate(row, 1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.font, cell.border = FONT, BOX
            if c > 1:
                cell.number_format = "#,##0"
    last = first + len(chars) - 1
    total = last + 1
    ws.cell(row=total, column=1, value="Total")
    for c in range(2, len(sum_heads) + 1):
        L = get_column_letter(c)
        ws.cell(row=total, column=c, value="=SUM(%s%d:%s%d)" % (L, first, L, last))
    for c in range(1, len(sum_heads) + 1):
        cell = ws.cell(row=total, column=c)
        cell.font, cell.fill, cell.border = BOLD, TOTAL_FILL, BOX
        cell.number_format = "#,##0"
    for k, s in enumerate(STATUSES):
        ws.cell(row=top, column=4 + k).fill = HEAD_FILL
    ctrl = total + 1
    ws.cell(row=ctrl, column=1, value="Contrôles : statuts = items VF5 ; FS avec + sans équivalent = base + DLC").font = NOTE
    ws.cell(row=ctrl, column=2, value="=IF(SUM(D%d:H%d)=B%d,\"OK\",\"Écart\")" % (total, total, total)).font = BOLD
    ws.cell(row=ctrl, column=9, value="=IF(K%d+L%d=I%d+J%d,\"OK\",\"Écart\")" % (total, total, total, total)).font = BOLD

    notes = [
        "Comment lire ce classeur",
        "• Correspondances : une ligne par item VF5, avec l'item Final Showdown le plus proche (jeu de base ou DLC) du même personnage.",
        "• Statuts : Identique = même modèle 3D (sommets identiques) et textures visuellement identiques ; Modifié = même item mais modèle "
        "et/ou textures retouchés ; Refait = même item (même numéro et même nom interne) mais modèle et textures entièrement refaits ; "
        "Incertain = indices partiels, à vérifier ; Absent du FS = aucun item correspondant trouvé.",
        "• Identification : les numéros d'items ont en grande partie été conservés entre les deux jeux ; un même numéro associé au même nom "
        "interne (ex. joha_outer_02) désigne le même item. Sans cet accord, la correspondance repose sur le contenu.",
        "• Contenu : géométrie = sommets identiques octet pour octet ; maillages communs = mêmes noms et nombres de sommets ; textures "
        "comparées sur des miniatures (les textures ont été réencodées dans le FS, leurs octets diffèrent même quand l'image est la même) ; "
        "les textures unies (remplissage) sont ignorées et les normal maps, converties en DXT5 dans le FS, sont comparées sur leurs deux "
        "canaux utiles. Les petits maillages (< 32 sommets) ne comptent que s'il n'y en a pas d'autres.",
        "• Noms : noms anglais de VF5. Les items sans nom sont des pièces de costume ou des éléments absents de la table. La table de noms du "
        "FS est compressée (XMemCompress) et n'a pas été lue : les items FS sont désignés par leur nom interne.",
        "• Jean et Taka-Arashi n'existent pas dans VF5 : tous leurs items FS sont sans équivalent.",
        "• Textures VF5 haute résolution : textures présentes dans les deux jeux (même image en miniature) mais avec plus de pixels "
        "dans VF5. « Modèle 3D identique » = Oui : la texture VF5 devrait se placer sans décalage sur le modèle FS ; sinon le modèle "
        "a été retouché ou refait et l'alignement est à vérifier. « Même position » = même rang dans le jeu de textures de l'item. "
        "Réinjection non testée : le FS n'utilise pas le format non compressé de VF5 et un package modifié doit être re-signé "
        "(console RGH/JTAG ou Xenia).",
        "• Liens « Ouvrir » : dossiers des fichiers bruts extraits (EXTRACTION de chaque jeu), relatifs à l'emplacement de ce classeur.",
    ]
    for i, n in enumerate(notes):
        ws.cell(row=ctrl + 2 + i, column=1, value=n).font = BOLD if i == 0 else NOTE
    ws.freeze_panes = ws.cell(row=first, column=2)

    wb.save(out)
    st = collections.Counter(x["status"] for x in vf5)
    print("saved", out)
    print("rows: correspondances=%d absents=%d incertains=%d items FS=%d" % (
        len(vf5), st["Absent du FS"], st["Incertain"], len(fs)))
    print("textures VF5 haute résolution: %d (items %d, modèle identique %d)" % (
        len(hires), len({p["vf5"]["item"] for p in hires}), sum(p["fs"]["model"] == "Identique" for p in hires)))
    print("summary rows %d-%d total %d, characters: %s" % (first, last, total, chars))


if __name__ == "__main__":
    main()
