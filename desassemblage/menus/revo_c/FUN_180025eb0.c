/* FUN_180025eb0  --  VF5FS+0x25eb0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180025eb0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined4
FUN_180025eb0(undefined4 param_1,undefined8 param_2,undefined4 param_3,undefined4 param_4,
             undefined8 param_5,undefined8 param_6)

{
  ulonglong uVar1;
  undefined4 uVar2;
  longlong lVar3;
  longlong lVar4;
  uint uVar5;
  ulonglong uVar7;
  undefined4 local_138 [2];
  undefined8 local_130;
  undefined1 local_128 [16];
  undefined4 local_118;
  undefined4 local_114;
  undefined4 local_110;
  undefined4 local_10c;
  undefined4 local_108;
  undefined4 local_104;
  undefined4 local_100;
  undefined1 local_fc;
  undefined1 local_f8 [16];
  undefined8 local_e8;
  undefined8 uStack_e0;
  undefined8 uStack_d8;
  undefined8 uStack_d0;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined4 local_b8;
  longlong local_b0;
  undefined8 local_a8;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  longlong local_58;
  undefined8 local_50;
  undefined4 local_40;
  longlong local_38;
  ulonglong local_30;
  undefined1 local_20;
  ulonglong uVar6;
  
  uVar7 = 0;
  local_b0 = 0;
  local_a8 = 0;
  local_58 = 0;
  local_50 = 0;
  local_38 = 0;
  local_30 = 0;
  local_138[0] = 0xffffffff;
  local_130 = 0;
  local_128 = (undefined1  [16])0x0;
  local_118 = 0xbf800000;
  local_114 = 0xbf800000;
  local_110 = 0;
  local_10c = 0xffffffff;
  local_108 = 0;
  local_104 = 7;
  local_100 = 9;
  local_f8 = (undefined1  [16])0x0;
  local_e8 = 0;
  uStack_e0 = 0x3f8000003f800000;
  uStack_d8 = 0x3f800000;
  uStack_d0 = 0;
  local_c8 = 0x3f8000003f800000;
  uStack_c0 = 0x3f8000003f800000;
  local_b8 = 0x3f800000;
  local_40 = 1;
  local_20 = 0;
  local_98 = 0;
  uStack_90 = 0;
  uStack_88 = 0;
  uStack_80 = 0;
  local_78 = 0;
  uStack_70 = 0;
  uStack_68 = 0;
  uStack_60 = 0;
  local_fc = 1;
  lVar3 = FUN_180020010(DAT_1806af3b8,param_1);
  local_138[0] = *(undefined4 *)(lVar3 + 0x10);
  local_128._8_8_ = param_6;
  local_128._0_8_ = param_5;
  local_130 = param_2;
  local_110 = param_4;
  local_104 = param_3;
  uVar2 = FUN_1800222a0(DAT_1806af3d0,local_138);
  local_30 = local_30 & 0xffffffff;
  if (local_38 != 0) {
    FUN_180279c00();
    local_38 = 0;
  }
  local_30 = local_30 & 0xffffffff00000000;
  uVar6 = uVar7;
  if (local_50._4_4_ != 0) {
    do {
      lVar3 = local_58;
      uVar1 = *(ulonglong *)(local_58 + 8 + uVar6 * 0x10);
      if ((uVar1 & 0xfffffffffff) == 0) {
        *(undefined8 *)(local_58 + 8 + uVar6 * 0x10) = 0;
      }
      else {
        FUN_180279c00((longlong)(uVar1 << 0x14) >> 0x10);
      }
      *(undefined8 *)(lVar3 + 8 + uVar6 * 0x10) = 0;
      lVar4 = *(longlong *)(lVar3 + uVar6 * 0x10) << 0x14;
      if (lVar4 == 0) {
        *(undefined8 *)(lVar3 + uVar6 * 0x10) = 0;
      }
      else {
        FUN_180279c00(lVar4 >> 0x10);
      }
      *(undefined8 *)(lVar3 + uVar6 * 0x10) = 0;
      uVar5 = (int)uVar6 + 1;
      uVar6 = (ulonglong)uVar5;
    } while (uVar5 < local_50._4_4_);
  }
  local_50 = local_50 & 0xffffffff;
  if (local_58 != 0) {
    FUN_180279c00();
    local_58 = 0;
  }
  local_50 = local_50 & 0xffffffff00000000;
  if (local_a8._4_4_ != 0) {
    do {
      lVar3 = local_b0;
      uVar6 = *(ulonglong *)(local_b0 + uVar7 * 0x10);
      if ((uVar6 & 0xfffffffffff) == 0) {
        *(undefined8 *)(local_b0 + uVar7 * 0x10) = 0;
      }
      else {
        FUN_180279c00((longlong)(uVar6 << 0x14) >> 0x10);
      }
      *(undefined8 *)(lVar3 + uVar7 * 0x10) = 0;
      uVar5 = (int)uVar7 + 1;
      uVar7 = (ulonglong)uVar5;
    } while (uVar5 < local_a8._4_4_);
  }
  local_a8 = local_a8 & 0xffffffff;
  if (local_b0 != 0) {
    FUN_180279c00();
  }
  return uVar2;
}
