// ===================================================
// 821DF768  ->  FUN_821df6e0  (entree 821df6e0)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined4 * FUN_821df6e0(undefined4 *param_1)

{
  ulonglong uVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  int iVar4;
  
  puVar3 = param_1 + 0x1a;
  iVar4 = 1;
  *param_1 = &PTR_FUN_8200f6d0;
  do {
    FUN_821df480(puVar3);
    iVar4 = iVar4 + -1;
    puVar3 = puVar3 + 0x14a;
  } while (-1 < iVar4);
  uVar2 = 0;
  *(undefined2 *)(param_1 + 0x2ba) = 0;
  param_1[0x2b9] = &PTR_FUN_8200f6c8;
  param_1[699] = 0;
  param_1[700] = 0;
  param_1[0x2bd] = 2;
  param_1[0x2be] = 0xffffffff;
  FUN_821dc7d0(param_1);
  uVar1 = FUN_82142ee0(0x1d0);
  if ((uVar1 & 0xffffffff) != 0) {
    uVar2 = FUN_822954b0(uVar1,2,10);
  }
  param_1[0x2b8] = uVar2;
  return param_1;
}



