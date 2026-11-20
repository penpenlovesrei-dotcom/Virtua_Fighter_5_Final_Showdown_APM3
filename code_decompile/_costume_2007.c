// ===================================================
// 82295514  ->  FUN_822954b0  (entree 822954b0)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

undefined4 * FUN_822954b0(undefined4 *param_1,undefined8 param_2,undefined8 param_3)

{
  ulonglong uVar1;
  undefined4 uVar2;
  
  param_1[0x66] = 0;
  param_1[0x67] = 0;
  param_1[0x68] = 0;
  param_1[0x6a] = 0;
  param_1[0x6b] = 0;
  param_1[0x6c] = 0;
  param_1[0x6e] = 0;
  param_1[0x6f] = 0;
  param_1[0x70] = 0;
  FUN_82292b60(param_1 + 1);
  param_1[0x73] = 0;
  param_1[0x72] = &PTR_FUN_8206328c;
  FUN_82295d20();
  uVar1 = FUN_82142ee0(0x254);
  if ((uVar1 & 0xffffffff) == 0) {
    uVar2 = 0;
  }
  else {
    uVar2 = FUN_822953f8(uVar1,param_2,param_3);
  }
  *param_1 = uVar2;
  FUN_82292b60(param_1 + 1);
  *(undefined1 *)(param_1 + 0x71) = 0;
  *(undefined1 *)((int)param_1 + 0x1c5) = 0;
  *(undefined1 *)((int)param_1 + 0x1c6) = 0;
  return param_1;
}



