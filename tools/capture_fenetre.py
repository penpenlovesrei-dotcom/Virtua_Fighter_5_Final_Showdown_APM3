#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capture une fenetre a l'ecran et l'enregistre en PNG.

Sert a voir ou en est vfes.exe pendant qu'un scenario d'entrees le pilote :
le journal du debogueur dit quels boutons sont presses, la capture dit ce que
le jeu en a fait.

La capture passe par l'ecran (BitBlt du bureau) et non par le DC de la fenetre :
un rendu Direct3D ne se recopie pas par GDI.

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


def capturer(rect, chemin):
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
    user32.ShowWindow(hwnd, SW_RESTORE)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.4)
    r = w.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    rect = (r.left, r.top, r.right, r.bottom)
    la, ha = capturer(rect, sortie)
    print('%s : %dx%d, fenetre "%s"' % (sortie, la, ha, nom))
    return 0


if __name__ == '__main__':
    sys.exit(main())
