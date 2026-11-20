# capturer_banc_gog.ps1 : lance le banc hybride, laisse monter l'image,
# photographie la fenetre, puis arrete le processus.
#
# POURQUOI UNE CAPTURE ET PAS UN JOURNAL. « Le jeu tourne » et « le jeu
# affiche » sont deux affirmations differentes, et seule la seconde repond a
# la question posee. Un processus vivant 45 s peut tres bien tourner sur une
# fenetre noire.
param(
    [int[]]$Moments = @(25),
    [string]$Suffixe = "",
    [string]$Banc = "banc_gog"
)

$ErrorActionPreference = "Stop"
$banc = "C:\Users\frede\Documents\RECOMP\Virtua Fighter 5 FS\FS APM3\$Banc"
if (-not (Test-Path "$banc\vfes.exe")) { throw "pas de vfes.exe dans $banc" }

# Une autre instance fausserait tout : la capture lit l'ECRAN, et deux
# fenetres se recouvrent. Le 4 novembre 2026, des mesures ont ete rendues
# incoherentes exactement comme cela.
$autres = @(Get-Process vfes -ErrorAction SilentlyContinue)
if ($autres.Count -gt 0) {
    throw ("{0} vfes.exe tourne(nt) deja (PID {1}). Fermer avant de mesurer." `
           -f $autres.Count, ($autres.Id -join ', '))
}

Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public class W {
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
    [DllImport("user32.dll")] public static extern int GetWindowTextW(IntPtr h, StringBuilder s, int n);
    [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h, out R r);
    [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr h, ref P p);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
    public struct R { public int l, t, r, b; }
    public struct P { public int x, y; }
}
"@

$env:APM_INERTE  = "1"
$env:APM_JOURNAL = "$banc\apm_journal.txt"
$env:APM_DETAIL  = "8"

$p = Start-Process -FilePath "$banc\vfes.exe" -WorkingDirectory $banc -PassThru
Write-Output "PID $($p.Id) lance, moments : $($Moments -join ', ') s"

$ecoule = 0
foreach ($m in $Moments) {
    while ($ecoule -lt $m) {
        Start-Sleep -Seconds 1
        $ecoule++
        if ($p.HasExited) { Write-Output "MORT au bout de $ecoule s, code $($p.ExitCode)"; exit 2 }
    }

    $p.Refresh()
    $h = $p.MainWindowHandle
    if ($h -eq [IntPtr]::Zero) {
        Write-Output "${m}s : AUCUNE FENETRE"
        continue
    }

    $sb = New-Object System.Text.StringBuilder 512
    [void][W]::GetWindowTextW($h, $sb, 512)
    $r = New-Object W+R
    [void][W]::GetClientRect($h, [ref]$r)
    $lg = $r.r - $r.l
    $ht = $r.b - $r.t
    if ($lg -le 0 -or $ht -le 0) { Write-Output "${m}s : zone client vide"; continue }

    $o = New-Object W+P
    $o.x = 0; $o.y = 0
    [void][W]::ClientToScreen($h, [ref]$o)
    [void][W]::SetForegroundWindow($h)
    Start-Sleep -Milliseconds 700

    $img = New-Object System.Drawing.Bitmap($lg, $ht)
    $g = [System.Drawing.Graphics]::FromImage($img)
    $g.CopyFromScreen($o.x, $o.y, 0, 0, (New-Object System.Drawing.Size($lg, $ht)))
    $chemin = "$banc\capture$Suffixe`_${m}s.png"
    $img.Save($chemin, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()

    # Un histogramme sommaire : une fenetre noire et une fenetre qui affiche ne
    # se distinguent pas sur une vignette, mais se distinguent sur les octets.
    $somme = 0; $maxi = 0; $nonNoir = 0; $n = 0
    for ($y = 0; $y -lt $ht; $y += 8) {
        for ($x = 0; $x -lt $lg; $x += 8) {
            $c = $img.GetPixel($x, $y)
            $v = [int]$c.R + [int]$c.G + [int]$c.B
            $somme += $v; $n++
            if ($v -gt $maxi) { $maxi = $v }
            if ($v -gt 12) { $nonNoir++ }
        }
    }
    $img.Dispose()
    Write-Output ("{0,4}s  [{1}]  {2}x{3}  moyenne {4,5:N1}/765  max {5,3}  non-noirs {6,7:P2}  -> capture$Suffixe`_{0}s.png" -f $m, $sb.ToString(), $lg, $ht, ($somme / $n), $maxi, ($nonNoir / $n))
}

if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force; Write-Output "processus arrete." }
