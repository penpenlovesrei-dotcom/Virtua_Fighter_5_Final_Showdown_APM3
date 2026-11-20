// ===================================================
// 180029000  ->  FUN_180029000  (entree 180029000)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 * FUN_180029000(undefined4 *param_1)

{
  undefined1 auVar1 [16];
  uint uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined1 auVar5 [16];
  
  *(undefined8 *)(param_1 + 0x22) = 0;
  *(undefined8 *)(param_1 + 0x24) = 0;
  *(undefined8 *)(param_1 + 0x26) = 0;
  *(undefined8 *)(param_1 + 0x12) = 0;
  *(undefined8 *)(param_1 + 0x14) = 0;
  *(undefined8 *)(param_1 + 0x18) = 0;
  *(undefined8 *)(param_1 + 0x1a) = 0;
  *(undefined8 *)(param_1 + 0x2e) = 0;
  *(undefined8 *)(param_1 + 0x30) = 0xf;
  *(undefined1 *)(param_1 + 0x2a) = 0;
  *(undefined8 *)(param_1 + 0x32) = 0;
  *(undefined8 *)(param_1 + 0x34) = 0;
  *(undefined8 *)(param_1 + 0x36) = 0;
  *(undefined8 *)(param_1 + 0x3c) = 0;
  *(undefined8 *)(param_1 + 0x3e) = 0;
  *(undefined8 *)(param_1 + 0x40) = 0;
  auVar5._0_12_ = ZEXT812(0);
  auVar5._12_4_ = 0;
  *(undefined8 *)(param_1 + 2) = 0;
  *(undefined8 *)(param_1 + 4) = 0;
  *(undefined8 *)(param_1 + 6) = 0;
  param_1[10] = 0;
  param_1[0xc] = 0;
  auVar1 = vunpcklps_avx(auVar5,auVar5);
  *(longlong *)(param_1 + 0x10) = auVar1._0_8_;
  auVar1 = vunpcklps_avx(auVar5,auVar5);
  *(longlong *)(param_1 + 0x13) = auVar1._0_8_;
  uVar2 = DAT_180346d3c;
  param_1[0x12] = 0;
  auVar1 = vunpcklps_avx(ZEXT416(uVar2),ZEXT416(uVar2));
  *(longlong *)(param_1 + 0x16) = auVar1._0_8_;
  param_1[0x15] = 0;
  auVar1 = vunpcklps_avx(auVar5,auVar5);
  *(longlong *)(param_1 + 0x19) = auVar1._0_8_;
  uVar4 = _UNK_180348bb8;
  uVar3 = _DAT_180348bb0;
  param_1[0x18] = uVar2;
  param_1[0x1b] = 0;
  *(undefined8 *)(param_1 + 0x1d) = uVar3;
  *(undefined8 *)(param_1 + 0x1f) = uVar4;
  *param_1 = 0xffffffff;
  param_1[8] = 0xbf800000;
  param_1[9] = 0xbf800000;
  param_1[0xb] = 0xffffffff;
  param_1[0xd] = 7;
  param_1[0xe] = 9;
  param_1[0x1c] = 0x3f800000;
  param_1[0x3a] = 1;
  *(undefined1 *)(param_1 + 0x44) = 0;
  *(undefined1 *)(param_1 + 0xf) = 1;
  return param_1;
}



