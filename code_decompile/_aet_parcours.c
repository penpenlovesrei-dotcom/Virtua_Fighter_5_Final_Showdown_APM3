// ===================================================
// 1800297D6  ->  FUN_180029790  (entree 180029790)
// ===================================================

void FUN_180029790(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  longlong lVar1;
  undefined8 uVar2;
  undefined4 local_128 [72];
  
  uVar2 = 0xfffffffffffffffe;
  FUN_180028e90(local_128);
  lVar1 = FUN_180024250(DAT_18066b738,local_128[0]);
  local_128[0] = *(undefined4 *)(lVar1 + 0x28);
  FUN_180024970(DAT_18066b750,param_1,local_128,param_4,uVar2);
  FUN_180029140(local_128);
  return;
}



