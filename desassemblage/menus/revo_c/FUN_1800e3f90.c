/* FUN_1800e3f90  --  VF5FS+0xe3f90
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800e3f90.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined1 FUN_1800e3f90(void)

{
  undefined8 uVar1;
  char cVar2;
  
  FUN_1801cf1f0(0);
  uVar1 = FUN_1800b21e0();
  FUN_1800da490(&DAT_18074fe70,3);
  FUN_18017bb10(DAT_1807598b8);
  cVar2 = FUN_1800b1b10(uVar1,0);
  if (cVar2 != '\0') {
    FUN_18017b7d0(DAT_1807598b8,0);
  }
  cVar2 = FUN_1800b1b10(uVar1,1);
  if (cVar2 != '\0') {
    FUN_18017b7d0(DAT_1807598b8,1);
  }
  uVar1 = FUN_1800b2390(uVar1);
  FUN_1800b7f30(uVar1);
  _guard_check_icall(900);
  _guard_check_icall();
  DAT_180751490 = 0;
  return 1;
}
