/* FUN_18020e9b0  --  VF5FS+0x20e9b0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18020e9b0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_18020e9b0(longlong param_1)

{
  undefined8 uVar1;
  
  *(undefined2 *)(param_1 + 0x20) = 1;
  FUN_1801cf1f0(0);
  FUN_1802cd400(&DAT_18073d970,"REPLAY_SCORE");
  FUN_18015a6b0(PTR_DAT_180643220);
  FUN_1800b3660(0);
  uVar1 = FUN_1800b21e0();
  FUN_1800b2f30(uVar1,1,0,0);
  FUN_180041760(0);
  FUN_180041760(1);
  *(undefined2 *)(param_1 + 0x10) = 1;
  *(undefined1 *)(param_1 + 0x12) = 0;
  _guard_check_icall(0xffffffff);
  *(undefined4 *)(param_1 + 0xc) = 600;
  FUN_180363af0(param_1 + 0xe8,0,0x650);
  return;
}
