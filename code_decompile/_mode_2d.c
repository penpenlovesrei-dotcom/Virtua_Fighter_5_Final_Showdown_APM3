// ===================================================
// 1800DA381  ->  FUN_1800da2c0  (entree 1800da2c0)
// ===================================================

undefined8 FUN_1800da2c0(undefined4 param_1,undefined8 param_2)

{
  undefined1 *puVar1;
  undefined4 uVar2;
  undefined8 *puVar3;
  
  puVar1 = DAT_18070c4e8;
  puVar3 = (undefined8 *)(DAT_18070c4e8 + 0x58);
  *DAT_18070c4e8 = 0;
  *(undefined8 *)(puVar1 + 8) = 0xffffffffffffffff;
  *(undefined4 *)(puVar1 + 0x10) = 0xffffffff;
  *(undefined2 *)(puVar1 + 0x14) = 0;
  *(undefined8 *)(puVar1 + 0x18) = 1;
  *(undefined4 *)(puVar1 + 0x20) = 0;
  puVar1[0x24] = 0;
  *(undefined4 *)(puVar1 + 0x28) = 0;
  *(undefined4 *)(puVar1 + 0x54) = 2;
  for (; puVar3 != (undefined8 *)(puVar1 + 0xb8); puVar3 = puVar3 + 2) {
    *puVar3 = 0;
    puVar3[1] = 0;
  }
  FUN_1802183b0();
  FUN_180191670();
  puVar1 = DAT_18070c4e8;
  uVar2 = thunk_FUN_1802447f0();
  *(undefined4 *)(puVar1 + 0x18) = uVar2;
  if (*(int *)(DAT_18070c4e8 + 0x18) == 9) {
    *(undefined4 *)(DAT_18070c4e8 + 0x20) = 1;
  }
  FUN_1800d9670(param_1,param_2);
  FUN_18016b0d0(*(undefined4 *)(DAT_18070c4e8 + 0x18));
  FUN_1801917a0(DAT_18070c4e8[0x14]);
  FUN_18010cea0();
  _guard_check_icall();
  FUN_180007440();
  thunk_FUN_180245cd0(FUN_1800d92a0);
  _guard_check_icall();
  return 0;
}



