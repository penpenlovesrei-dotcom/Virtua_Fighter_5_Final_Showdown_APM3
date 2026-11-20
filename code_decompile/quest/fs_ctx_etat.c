// ===================================================
// 18018C6A0  ->  FUN_18018c6a0  (entree 18018c6a0)
// ===================================================

undefined4 FUN_18018c6a0(longlong param_1)

{
  return *(undefined4 *)(param_1 + 0x828);
}



// ===================================================
// 18018E810  ->  FUN_18018e810  (entree 18018e810)
// ===================================================

void FUN_18018e810(longlong param_1,undefined4 param_2)

{
  *(undefined4 *)(param_1 + 0x828) = param_2;
  return;
}



// ===================================================
// 180189880  ->  FUN_180189880  (entree 180189880)
// ===================================================

undefined4 * FUN_180189880(undefined4 *param_1)

{
  undefined1 auVar1 [16];
  uint uVar2;
  undefined1 auVar3 [16];
  undefined1 auVar4 [64];
  
  *(undefined8 *)(param_1 + 10) = 0;
  *(undefined8 *)(param_1 + 0xc) = 0;
  *(undefined8 *)(param_1 + 0xe) = 0;
  *(undefined8 *)(param_1 + 0x10) = 0;
  *(undefined8 *)(param_1 + 0x12) = 0;
  *(undefined8 *)(param_1 + 0x14) = 0;
  FUN_180211a00(param_1 + 0x18);
  *(undefined8 *)(param_1 + 0x31) = 0;
  param_1[0x33] = 0;
  auVar3._0_12_ = ZEXT812(0);
  auVar3._12_4_ = 0;
  auVar4 = ZEXT1664(auVar3);
  auVar1 = vunpcklps_avx(auVar3,auVar3);
  *(longlong *)(param_1 + 10) = auVar1._0_8_;
  auVar1 = vunpcklps_avx(auVar3,auVar3);
  *(longlong *)(param_1 + 0xd) = auVar1._0_8_;
  uVar2 = DAT_180346d3c;
  param_1[0xc] = 0;
  auVar1 = vunpcklps_avx(ZEXT416(uVar2),ZEXT416(uVar2));
  *(longlong *)(param_1 + 0x10) = auVar1._0_8_;
  param_1[0xf] = 0;
  auVar1 = vunpcklps_avx(auVar3,auVar3);
  param_1[0x12] = uVar2;
  *(longlong *)(param_1 + 0x13) = auVar1._0_8_;
  param_1[0x15] = 0;
  *param_1 = 0;
  *(undefined8 *)(param_1 + 1) = 0xffffffffffffffff;
  *(undefined8 *)(param_1 + 3) = 0;
  param_1[5] = 0xffffffff;
  param_1[6] = 0;
  param_1[7] = 7;
  param_1[8] = 9;
  param_1[9] = 9;
  *(undefined8 *)(param_1 + 0x16) = 0;
  FUN_180213910(param_1 + 0x18);
  auVar1 = vunpcklps_avx(auVar4._0_16_,auVar4._0_16_);
  *(undefined8 *)(param_1 + 0x28) = 0;
  *(undefined2 *)(param_1 + 0x2a) = 0;
  *(longlong *)(param_1 + 0x31) = auVar1._0_8_;
  param_1[0x33] = auVar4._0_4_;
  param_1[0x2b] = 0;
  param_1[0x30] = 0;
  *(undefined8 *)(param_1 + 0x34) = 0;
  *(undefined8 *)(param_1 + 0x36) = 0;
  *(undefined8 *)(param_1 + 0x38) = 0;
  *(undefined8 *)(param_1 + 0x2c) = 0;
  *(undefined8 *)(param_1 + 0x2e) = 0;
  return param_1;
}



