// ===================================================
// 180187A18  ->  FUN_180187a10  (entree 180187a10)
// ===================================================

void FUN_180187a10(undefined4 param_1,undefined4 param_2)

{
  FUN_18018bbd0(DAT_180719900,param_1,param_2);
  return;
}



// ===================================================
// 180187A6C  ->  FUN_180187a60  (entree 180187a60)
// ===================================================

undefined8 * FUN_180187a60(undefined8 *param_1)

{
  undefined8 uVar1;
  longlong lVar2;
  undefined8 *puVar3;
  undefined1 local_18 [16];
  
  lVar2 = FUN_18018c610(DAT_180719908);
  puVar3 = (undefined8 *)FUN_18018c3b0(DAT_180719900,local_18,*(undefined4 *)(lVar2 + 0x28));
  uVar1 = puVar3[1];
  *param_1 = *puVar3;
  param_1[1] = uVar1;
  return param_1;
}



