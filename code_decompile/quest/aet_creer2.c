// ===================================================
// 180171F40  ->  FUN_180171f40  (entree 180171f40)
// ===================================================

void FUN_180171f40(longlong param_1,int param_2,undefined4 param_3,undefined8 param_4,
                  undefined8 *param_5,undefined4 param_6,undefined4 param_7,undefined8 param_8,
                  undefined8 param_9)

{
  undefined4 uVar1;
  undefined4 local_128 [2];
  undefined8 local_120;
  undefined8 local_118;
  undefined8 local_110;
  undefined4 local_100;
  undefined4 local_f4;
  undefined8 local_e8;
  undefined4 local_e0;
  
  FUN_180029000(local_128);
  local_f4 = param_6;
  local_100 = param_7;
  local_118 = param_8;
  local_110 = param_9;
  if (param_5 != (undefined8 *)0x0) {
    local_e8 = *param_5;
    local_e0 = *(undefined4 *)(param_5 + 1);
  }
  local_128[0] = param_3;
  local_120 = param_4;
  if (*(char *)(param_1 + 0x138) == '\0') {
    param_1 = param_1 + (longlong)param_2 * 4;
    if (*(int *)(param_1 + 0x5c) != 0) {
      FUN_180029be0();
      *(undefined4 *)(param_1 + 0x5c) = 0;
    }
    uVar1 = FUN_180029a90(local_128);
    *(undefined4 *)(param_1 + 0x5c) = uVar1;
  }
  FUN_180029140(local_128);
  return;
}



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



