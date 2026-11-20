// ===================================================
// 180171E90  ->  FUN_180171e90  (entree 180171e90)
// ===================================================

void FUN_180171e90(longlong param_1,int param_2,undefined4 param_3,undefined8 param_4,
                  undefined4 param_5,undefined4 param_6)

{
  undefined4 uVar1;
  undefined4 local_128 [2];
  undefined8 local_120;
  undefined1 local_118 [16];
  undefined4 local_100;
  undefined4 local_f4;
  
  FUN_180029000(local_128);
  local_f4 = param_5;
  local_100 = param_6;
  local_118 = (undefined1  [16])0x0;
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



