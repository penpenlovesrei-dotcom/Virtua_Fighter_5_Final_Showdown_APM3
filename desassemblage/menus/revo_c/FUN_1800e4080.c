/* FUN_1800e4080  --  VF5FS+0xe4080
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800e4080.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


ulonglong FUN_1800e4080(void)

{
  ulonglong uVar1;
  
  uVar1 = FUN_1802cb570();
  if ((char)uVar1 != '\0') {
    uVar1 = 0;
    if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
      uVar1 = (**(code **)(DAT_180c8df28 + 0x1ff08))
                        (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xba,0);
    }
  }
  return uVar1 & 0xffffffffffffff00;
}
