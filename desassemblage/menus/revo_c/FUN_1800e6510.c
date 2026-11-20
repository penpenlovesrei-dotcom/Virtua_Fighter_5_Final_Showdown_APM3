/* FUN_1800e6510  --  VF5FS+0xe6510
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800e6510.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined8 FUN_1800e6510(void)

{
  undefined8 uVar1;
  
  uVar1 = DAT_1807514c0;
  if (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0) {
    if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
      (**(code **)(DAT_180c8df28 + 0x1ff08))(*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xe,0);
    }
    FUN_1802cd400(uVar1,"title");
  }
  DAT_1807514d4 = 0;
  DAT_1807514d8 = 0;
  return 1;
}
