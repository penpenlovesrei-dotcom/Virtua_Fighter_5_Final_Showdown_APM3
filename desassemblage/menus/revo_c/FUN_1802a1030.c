/* FUN_1802a1030  --  VF5FS+0x2a1030
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1802a1030.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* WARNING: Removing unreachable block (ram,0x0001802a114a) */
/* WARNING: Removing unreachable block (ram,0x0001802a1100) */
/* WARNING: Removing unreachable block (ram,0x0001802a1202) */

ulonglong FUN_1802a1030(longlong param_1,undefined8 param_2,undefined4 param_3)

{
  undefined8 *puVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  uint uVar4;
  uint uVar5;
  ulonglong uVar6;
  longlong lVar7;
  undefined4 local_28;
  undefined4 local_24;
  undefined1 local_20 [16];
  undefined8 local_10;
  
  uVar6 = FUN_1802ccab0();
  if ((char)uVar6 != '\0') {
    return uVar6 & 0xffffffffffffff00;
  }
  *(undefined8 *)(param_1 + 0x5960) = param_2;
  *(undefined4 *)(param_1 + 0x5968) = param_3;
  if (*(int *)(param_1 + 0x597c) == 0) {
    *(undefined4 *)(param_1 + 0x597c) = 0;
    if (*(longlong *)(param_1 + 0x5970) != 0) {
      FUN_180279c00();
      *(undefined8 *)(param_1 + 0x5970) = 0;
    }
    *(undefined4 *)(param_1 + 0x5978) = 0;
    *(undefined4 *)(param_1 + 0x5938) = 1;
    *(undefined4 *)(param_1 + 0x593c) = 100;
    local_28 = 7;
    local_24 = 0xa8;
    local_20 = (undefined1  [16])0x0;
    local_10 = 0;
    FUN_18029fea0(param_1 + 0x60,&local_28);
    if (local_20._8_8_ != 0) {
      FUN_180279c00();
    }
    local_28 = 8;
    local_24 = 0xa8;
    local_20 = (undefined1  [16])0x0;
    local_10 = 0;
    FUN_18029fea0(param_1 + 0x60,&local_28);
    if (local_20._8_8_ != 0) {
      FUN_180279c00();
    }
  }
  else {
    uVar4 = FUN_1802cc250(0,*(int *)(param_1 + 0x597c) + -1,0);
    puVar1 = (undefined8 *)(*(longlong *)(param_1 + 0x5970) + (ulonglong)uVar4 * 0x10);
    uVar3 = puVar1[1];
    *(undefined8 *)(param_1 + 0x5950) = *puVar1;
    *(undefined8 *)(param_1 + 0x5958) = uVar3;
    uVar4 = uVar4 + 1;
    uVar5 = *(uint *)(param_1 + 0x597c);
    if ((uVar4 < uVar5) && ((int)uVar4 < (int)uVar5)) {
      lVar7 = (longlong)(int)uVar4 << 4;
      do {
        puVar1 = (undefined8 *)(*(longlong *)(param_1 + 0x5970) + lVar7);
        uVar3 = puVar1[1];
        puVar2 = (undefined8 *)(*(longlong *)(param_1 + 0x5970) + -0x10 + lVar7);
        *puVar2 = *puVar1;
        puVar2[1] = uVar3;
        uVar4 = uVar4 + 1;
        lVar7 = lVar7 + 0x10;
        uVar5 = *(uint *)(param_1 + 0x597c);
      } while ((int)uVar4 < (int)uVar5);
    }
    *(uint *)(param_1 + 0x597c) = uVar5 - 1;
  }
  local_28 = 9;
  local_24 = 0xa8;
  local_20 = (undefined1  [16])0x0;
  local_10 = 0;
  FUN_18029fea0(param_1 + 0x60,&local_28);
  if (local_20._8_8_ != 0) {
    FUN_180279c00();
  }
  uVar6 = FUN_1802cd400(param_1,"CLIP_DL");
  return uVar6;
}
