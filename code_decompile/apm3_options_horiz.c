// ===================================================
// 1801AA6E0  ->  FUN_1801aa6e0  (entree 1801aa6e0)
// ===================================================

undefined8 FUN_1801aa6e0(longlong param_1,undefined4 param_2)

{
  longlong lVar1;
  undefined4 local_18;
  undefined4 uStack_14;
  undefined4 local_10;
  
  if (*(int *)(param_1 + 0x58) < 4) {
    *(undefined4 *)(param_1 + 0x240 + (longlong)*(int *)(param_1 + 0x58) * 4) =
         *(undefined4 *)(param_1 + 0x5c);
    if (*(uint *)(param_1 + 0x58) < 2) {
      lVar1 = FUN_1801b8a30();
      local_10 = *(undefined4 *)(lVar1 + 8);
      _local_18 = CONCAT44(*(undefined4 *)(param_1 + 0x240),*(undefined4 *)(param_1 + 0x244));
      FUN_1801ba0d0(&local_18);
    }
    FUN_1801be850(param_1 + 0x31c,0xffffffff,0 < *(int *)(param_1 + 0x5c));
    FUN_1801be850(param_1 + 0x31c,1,
                  *(int *)(param_1 + 0x5c) <
                  *(int *)(&DAT_180410d88 + (longlong)*(int *)(param_1 + 0x58) * 4));
    FUN_1800b2f70(param_1 + 0x31c,param_2);
    FUN_1801bd080(param_1,param_2);
    return 1;
  }
  return 0;
}



// ===================================================
// 1801A80E0  ->  FUN_1801a80e0  (entree 1801a80e0)
// ===================================================

void FUN_1801a80e0(longlong param_1,undefined4 param_2)

{
  char cVar1;
  
  cVar1 = FUN_1801b7010();
  if (cVar1 != '\0') {
    FUN_1801bc010(param_1,param_2);
    FUN_1801bbae0(param_1);
    FUN_1801bba20(param_1 + 0x260);
    FUN_1801bba20(param_1 + 0x2b8);
    FUN_1801be4b0(param_1 + 0x31c);
    *(undefined1 *)(param_1 + 0x310) = 1;
  }
  return;
}



