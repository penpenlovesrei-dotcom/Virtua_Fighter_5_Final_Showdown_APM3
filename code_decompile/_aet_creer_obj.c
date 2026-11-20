// ===================================================
// 180029A90  ->  FUN_180029a90  (entree 180029a90)
// ===================================================

undefined4
FUN_180029a90(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined4 uVar1;
  longlong lVar2;
  undefined4 local_128 [72];
  
  FUN_180028e90(local_128,param_1,param_3,param_4,0xfffffffffffffffe);
  lVar2 = FUN_180024250(DAT_18066b738,local_128[0]);
  local_128[0] = *(undefined4 *)(lVar2 + 0x28);
  uVar1 = FUN_180026790(DAT_18066b750,local_128);
  FUN_180029140(local_128);
  return uVar1;
}



