// ===================================================
// 1800B2F80  ->  FUN_1800b2f80  (entree 1800b2f80)
// ===================================================

void FUN_1800b2f80(longlong param_1,int param_2,undefined4 param_3,undefined4 param_4,
                  undefined4 param_5,undefined4 param_6)

{
  longlong lVar1;
  
  lVar1 = (longlong)param_2;
  *(undefined4 *)(param_1 + 0x38 + lVar1 * 4) = param_5;
  *(undefined4 *)(param_1 + 0x40 + lVar1 * 4) = param_6;
  *(undefined4 *)(param_1 + 0x28 + lVar1 * 4) = param_3;
  *(undefined4 *)(param_1 + 0x30 + lVar1 * 4) = param_4;
  return;
}



// ===================================================
// 18016CF50  ->  FUN_18016cf50  (entree 18016cf50)
// ===================================================

void FUN_18016cf50(longlong param_1)

{
  FUN_180170010(param_1 + 0x68);
  return;
}



// ===================================================
// 18016CF30  ->  FUN_18016cf30  (entree 18016cf30)
// ===================================================

void FUN_18016cf30(longlong param_1)

{
  FUN_18016fff0(param_1 + 0x68);
  return;
}



// ===================================================
// 18016CF20  ->  FUN_18016cf20  (entree 18016cf20)
// ===================================================

void FUN_18016cf20(longlong param_1)

{
  FUN_18016ffd0(param_1 + 0x68);
  return;
}



// ===================================================
// 18016CF40  ->  FUN_18016cf40  (entree 18016cf40)
// ===================================================

void FUN_18016cf40(longlong param_1)

{
  FUN_180007440(param_1 + 0x68);
  return;
}



