// ===================================================
// 18019B800  ->  FUN_18019b800  (entree 18019b800)
// ===================================================

void FUN_18019b800(longlong param_1,undefined8 *param_2,undefined4 param_3)

{
  uint uVar1;
  undefined8 uVar2;
  undefined1 auVar3 [16];
  
  uVar1 = *(uint *)((longlong)param_2 + 4);
  *(undefined4 *)(param_1 + 0x3c) = *(undefined4 *)param_2;
  auVar3._8_8_ = 0;
  auVar3._0_8_ = *(ulonglong *)(param_1 + 0x3c);
  auVar3 = vinsertps_avx(auVar3,ZEXT416(uVar1),0x10);
  *(longlong *)(param_1 + 0x34) = auVar3._0_8_;
  *(longlong *)(param_1 + 0x3c) = auVar3._0_8_;
  *(undefined4 *)(param_1 + 0x2c) = param_3;
  *(undefined1 *)(param_1 + 0x10) = 1;
  uVar2 = param_2[1];
  *(undefined8 *)(param_1 + 0x14) = *param_2;
  *(undefined8 *)(param_1 + 0x1c) = uVar2;
  return;
}



