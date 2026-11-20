// ===================================================
// 180029630  ->  FUN_180029630  (entree 180029630)
// ===================================================

void FUN_180029630(int *param_1,undefined8 param_2,undefined1 param_3,undefined8 param_4)

{
  longlong lVar1;
  int iVar2;
  undefined4 local_128 [72];
  
  if (*param_1 < 0) {
    param_1[0x46] = -1;
  }
  else {
    FUN_180028e90(local_128,param_1,param_3,param_4,0xfffffffffffffffe);
    lVar1 = FUN_180024250(DAT_18066b738,local_128[0]);
    local_128[0] = *(undefined4 *)(lVar1 + 0x28);
    iVar2 = FUN_180026790(DAT_18066b750,local_128);
    FUN_180029140(local_128);
    param_1[0x46] = iVar2;
    if (iVar2 != -1) {
      FUN_1800281d0(DAT_18066b750,iVar2,1);
      return;
    }
  }
  return;
}



// ===================================================
// 1800296E0  ->  FUN_1800296e0  (entree 1800296e0)
// ===================================================

longlong FUN_1800296e0(longlong param_1,undefined8 param_2)

{
  if (*(int *)(param_1 + 0x118) != -1) {
    FUN_1800272e0(DAT_18066b750);
  }
  *(undefined4 *)(param_1 + 0x118) = 0xffffffff;
  FUN_1800293a0(param_1,param_2);
  return param_1;
}



