// ===================================================
// 1801AB990  ->  FUN_1801ab990  (entree 1801ab990)
// ===================================================

undefined8 FUN_1801ab990(longlong param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 uVar2;
  
  iVar1 = *(int *)(param_1 + 0x58);
  if (*(char *)((longlong)iVar1 + 0x311 + param_1) != '\0') {
    return 0;
  }
  if (iVar1 < 4) {
    iVar1 = *(int *)(param_1 + 0x240 + (longlong)iVar1 * 4);
    *(int *)(param_1 + 0x5c) = iVar1;
    FUN_1801be850(param_1 + 0x31c,0xffffffff,0 < iVar1);
    FUN_1801be850(param_1 + 0x31c,1,
                  *(int *)(param_1 + 0x5c) <
                  *(int *)(&DAT_180410d88 + (longlong)*(int *)(param_1 + 0x58) * 4));
    uVar2 = *(undefined4 *)(&DAT_180410d88 + (longlong)*(int *)(param_1 + 0x58) * 4);
  }
  else {
    uVar2 = 0;
  }
  *(undefined4 *)(param_1 + 0x22c) = uVar2;
  *(undefined1 *)(param_1 + 0x230) = 0;
  FUN_1801bd080(param_1,param_2);
  return 1;
}



