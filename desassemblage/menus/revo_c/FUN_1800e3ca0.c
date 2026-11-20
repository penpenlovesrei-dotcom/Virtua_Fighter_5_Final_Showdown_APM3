/* FUN_1800e3ca0  --  VF5FS+0xe3ca0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800e3ca0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined4 FUN_1800e3ca0(void)

{
  undefined8 uVar1;
  int iVar2;
  
  FUN_1800da490(&DAT_18074fe70,3);
  FUN_1802cd400(&DAT_180751430,"INVITATION_SHIFT_SCENE");
  DAT_18075148a = 1;
  FUN_1800b7ba0();
  FUN_18015a6b0(PTR_DAT_180643220);
  FUN_1802cd400(&DAT_18073d970,"GAME SCORE");
  uVar1 = FUN_180092000();
  FUN_1800925f0(uVar1);
  _guard_check_icall(0x708);
  _guard_check_icall(0x4b0);
  iVar2 = FUN_1801aa6c0();
  if (iVar2 == 2) {
    FUN_1801fee80();
  }
  FUN_1800a6680();
  FUN_1801cf1f0(0);
  _guard_check_icall(0xffffffff);
  return 1;
}
