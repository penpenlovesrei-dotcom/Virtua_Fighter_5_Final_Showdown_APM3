// ===================================================
// 180187C50  ->  FUN_180187c50  (entree 180187c50)
// ===================================================

void FUN_180187c50(undefined4 param_1)

{
  longlong lVar1;
  longlong *plVar2;
  
  lVar1 = FUN_18018c420(DAT_180719908,param_1);
  plVar2 = (longlong *)(lVar1 + 0x28);
  if (0xf < *(ulonglong *)(lVar1 + 0x40)) {
    plVar2 = (longlong *)*plVar2;
  }
  lVar1 = FUN_18018c420(DAT_180719908,param_1);
  FUN_18018e5a0(DAT_180719900,*(undefined4 *)(lVar1 + 0x48),plVar2);
  return;
}



