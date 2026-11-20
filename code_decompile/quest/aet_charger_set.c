// ===================================================
// 180029C20  ->  FUN_180029c20  (entree 180029c20)
// ===================================================

void FUN_180029c20(undefined4 param_1)

{
  longlong lVar1;
  longlong *plVar2;
  
  lVar1 = FUN_1800248d0(DAT_18066b738,param_1);
  plVar2 = (longlong *)(lVar1 + 0x28);
  if (0xf < *(ulonglong *)(lVar1 + 0x40)) {
    plVar2 = (longlong *)*plVar2;
  }
  lVar1 = FUN_1800248d0(DAT_18066b738,param_1);
  FUN_180027740(DAT_18066b750,*(undefined4 *)(lVar1 + 0x48),plVar2);
  return;
}



