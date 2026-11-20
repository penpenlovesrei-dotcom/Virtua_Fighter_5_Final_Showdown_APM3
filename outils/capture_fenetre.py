#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capture une fenetre a l'ecran et l'enregistre en PNG.

Sert a voir ou en est vfes.exe pendant qu'un scenario d'entrees le pilote :
le journal du debogueur dit quels boutons sont presses, la capture dit ce que
le jeu en a fait.

La capture passe par l'ecran (BitBlt du bureau) et non par le DC de la fenetre :
un rendu Direct3D ne se recopie pas par GDI. `capturer()` prend donc un `hwnd`
et REFUSE d'ecrire si la fenetre est recouverte -- voir `devant()`.

PIEGE, et il a deja coute une passe entiere de mesures : on photographie la ZONE
D'ECRAN qu'occupe la fenetre, pas la fenetre. Si une autre fenetre la recouvre,
c'est cette autre fenetre qu'on enregistre -- donc l'ecran de l'utilisateur. Le
mode principal de ce script met la fenetre au premier plan avant de declencher ;
tout appelant qui court-circuite cela doit verifier GetForegroundWindow lui-meme,
comme le fait tools/identifier_entrees.py.
Le processus se declare DPI-aware par moniteur : GetWindowRect rend alors des
pixels physiques, et il n'y a pas de facteur d'echelle a appliquer.

Usage :
    py -3 tools/capture_fenetre.py sortie.png
    py -3 tools/capture_fenetre.py sortie.png --titre "Virtua Fighter"
    py -3 tools/capture_fenetre.py sortie.png --attendre 8   (secondes avant la prise)
    py -3 tools/capture_fenetre.py --lister                  (fenetres visibles)
"""
import ctypes
import ctypes.wintypes as w
import sys
import time

user32 = ctypes.WinDLL('user32', use_last_error=True)
gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

SRCCOPY = 0x00CC0020
SW_RESTORE = 9
DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = ctypes.c_void_p(-4)

WNDENUMPROC = ctypes.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [('biSize', w.DWORD), ('biWidth', ctypes.c_long),
                ('biHeight', ctypes.c_long), ('biPlanes', w.WORD),
                ('biBitCount', w.WORD), ('biCompression', w.DWORD),
                ('biSizeImage', w.DWORD), ('biXPelsPerMeter', ctypes.c_long),
                ('biYPelsPerMeter', ctypes.c_long), ('biClrUsed', w.DWORD),
                ('biClrImportant', w.DWORD)]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [('bmiHeader', BITMAPINFOHEADER), ('bmiColors', w.DWORD * 3)]


def dpi_aware():
    try:
        user32.SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)
    except AttributeError:
        try:
            ctypes.WinDLL('shcore').SetProcessDpiAwareness(2)
        except Exception:
            user32.SetProcessDPIAware()


def fenetres():
    """Toutes les fenetres visibles avec un titre : (hwnd, titre, rect)."""
    out = []

    def cb(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        n = user32.GetWindowTextLengthW(hwnd)
        if n <= 0:
            return True
        buf = ctypes.create_unicode_buffer(n + 1)
        user32.GetWindowTextW(hwnd, buf, n + 1)
        r = w.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(r))
        if r.right - r.left < 32 or r.bottom - r.top < 32:
            return True
        out.append((hwnd, buf.value, (r.left, r.top, r.right, r.bottom)))
        return True

    user32.EnumWindows(WNDENUMPROC(cb), 0)
    return out


def trouver(titre):
    t = titre.lower()
    for hwnd, nom, rect in fenetres():
        if t in nom.lower():
            return hwnd, nom, rect
    return None, None, None


GA_ROOT = 2


def devant(hwnd, rect, points=5):
    """Vrai si `hwnd` est bien ce qu'on verrait a l'ecran dans `rect`.

    POURQUOI CE CONTROLE EXISTE. `SetForegroundWindow` ECHOUE EN SILENCE
    quand le processus appelant n'est pas deja au premier plan -- c'est une
    protection de Windows contre le vol de focus. La sonde du 2026-10-01 l'a
    appele, a cru la fenetre devant, et a photographie le navigateur de
    Frederic pendant toute une passe : quinze images de son bureau, et pas
    une du jeu. L'en-tete de ce fichier avertissait du piege depuis le debut ;
    ce qui manquait, c'etait de VERIFIER au lieu d'esperer.

    On interroge cinq points -- le centre et les quatre quarts -- parce qu'un
    recouvrement partiel laisse le centre libre.
    """
    x, y, x2, y2 = rect
    la, ha = x2 - x, y2 - y
    if la <= 0 or ha <= 0:
        return False
    essais = [(x + la // 2, y + ha // 2)]
    if points > 1:
        essais += [(x + la // 4, y + ha // 4), (x + 3 * la // 4, y + ha // 4),
                   (x + la // 4, y + 3 * ha // 4),
                   (x + 3 * la // 4, y + 3 * ha // 4)]
    for px, py in essais:
        pt = w.POINT(px, py)
        sous = user32.WindowFromPoint(pt)
        if not sous:
            return False
        racine = user32.GetAncestor(sous, GA_ROOT) or sous
        if racine != hwnd:
            return False
    return True


def capturer(rect, chemin, hwnd=None):
    """Enregistre la zone d'ecran `rect`. Avec `hwnd`, REFUSE si elle est
    recouverte -- et dans ce cas n'ecrit aucun fichier, pour ne pas laisser
    une image du bureau de l'utilisateur dans le dossier des mesures.
    """
    if hwnd is not None and not devant(hwnd, rect):
        raise RuntimeError(
            'la fenetre est RECOUVERTE : rien n a ete enregistre. Ne '
            'laissez aucune fenetre par-dessus le jeu pendant la mesure.')
    from PIL import Image
    x, y, x2, y2 = rect
    la, ha = x2 - x, y2 - y
    ecran = user32.GetDC(0)
    memdc = gdi32.CreateCompatibleDC(ecran)
    bmp = gdi32.CreateCompatibleBitmap(ecran, la, ha)
    gdi32.SelectObject(memdc, bmp)
    gdi32.BitBlt(memdc, 0, 0, la, ha, ecran, x, y, SRCCOPY)

    bi = BITMAPINFO()
    bi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bi.bmiHeader.biWidth = la
    bi.bmiHeader.biHeight = -ha            # negatif : lignes de haut en bas
    bi.bmiHeader.biPlanes = 1
    bi.bmiHeader.biBitCount = 32
    buf = ctypes.create_string_buffer(la * ha * 4)
    gdi32.GetDIBits(memdc, bmp, 0, ha, buf, ctypes.byref(bi), 0)

    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(0, ecran)

    img = Image.frombuffer('RGBA', (la, ha), buf, 'raw', 'BGRA', 0, 1).convert('RGB')
    img.save(chemin)
    return la, ha


def main():
    dpi_aware()
    if '--lister' in sys.argv:
        for hwnd, nom, r in fenetres():
            print('0x%08X  %4dx%-4d  %s' % (hwnd, r[2] - r[0], r[3] - r[1], nom))
        return 0

    if len(sys.argv) < 2 or sys.argv[1].startswith('--'):
        print(__doc__)
        return 1
    sortie = sys.argv[1]
    titre = 'Virtua Fighter'
    if '--titre' in sys.argv:
        titre = sys.argv[sys.argv.index('--titre') + 1]
    if '--attendre' in sys.argv:
        time.sleep(float(sys.argv[sys.argv.index('--attendre') + 1]))

    hwnd, nom, rect = trouver(titre)
    if not hwnd:
        print('aucune fenetre visible dont le titre contient "%s"' % titre)
        print('fenetres visibles :')
        for h, n, r in fenetres():
            print('   %4dx%-4d  %s' % (r[2] - r[0], r[3] - r[1], n))
        return 1
    # LA GARDE EXISTAIT ET N ETAIT PAS BRANCHEE (corrige le 2026-10-19).
    # `main()` appelait `capturer(rect, sortie)` SANS `hwnd` : le controle
    # `devant()` ne tournait donc jamais, et le piege que l en-tete de ce
    # fichier decrit depuis le debut s est reproduit -- une capture de la
    # fenetre de Frederic au lieu du jeu. `SetForegroundWindow` echoue en
    # silence quand l appelant n est pas deja au premier plan ; on insiste,
    # puis on VERIFIE.
    for essai in range(6):
        user32.ShowWindow(hwnd, SW_RESTORE)
        user32.SetForegroundWindow(hwnd)
        time.sleep(0.4)
        r = w.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(r))
        rect = (r.left, r.top, r.right, r.bottom)
        if devant(hwnd, rect):
            break
        print('   la fenetre n est pas devant (essai %d/6)' % (essai + 1))
    try:
        la, ha = capturer(rect, sortie, hwnd)
    except RuntimeError as e:
        print('REFUS : %s' % e)
        return 1
    print('%s : %dx%d, fenetre "%s"' % (sortie, la, ha, nom))
    return 0


if __name__ == '__main__':
    sys.exit(main())
