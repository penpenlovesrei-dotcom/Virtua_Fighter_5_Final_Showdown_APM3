/* FUN_1801b82d0  --  VF5FS+0x1b82d0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801b82d0.
 * Vidée le 2026-11-09.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1801b82d0(longlong param_1)

{
  char cVar1;
  undefined4 uVar2;
  undefined8 uVar3;
  undefined4 local_res8;
  undefined4 local_a8;
  undefined4 local_a4;
  float local_a0;
  undefined1 local_98 [8];
  undefined4 local_90;
  undefined4 local_74;
  undefined4 local_6c;
  undefined4 local_64;
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined1 *local_50;
  undefined1 local_48 [64];
  
  local_a8 = 0;
  local_a4 = 0;
  local_a0 = 0.0;
  uVar2 = FUN_180195e10();
  FUN_180196120(2);
  cVar1 = FUN_1801e0460(param_1 + 0x14d0);
  if (cVar1 != '\0') {
    cVar1 = FUN_1801df7c0(param_1 + 0x14d0,&local_a8,"head_tit_ct",1,0);
    if (cVar1 != '\0') {
      FUN_1801a79f0(local_98);
      FUN_1801a7a40(local_48,2);
      FUN_1801a89d0(local_48,0x42000000);
      local_50 = local_48;
      local_74 = 10;
      local_5c = local_a8;
      local_58 = local_a4;
      local_64 = local_a8;
      local_60 = local_a4;
      local_6c = 9;
      local_res8 = CONCAT13((char)(int)(local_a0 * 255.0),0x39b7ff);
      local_90 = local_res8;
      uVar3 = FUN_1802316e0(0x183);
      FUN_1801a86c0(local_98,uVar3);
    }
  }
  FUN_180196120(uVar2);
  return;
}
