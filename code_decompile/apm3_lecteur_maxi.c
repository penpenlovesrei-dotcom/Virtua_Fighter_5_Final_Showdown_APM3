// ===================================================
// 1801A6E0D  ->  FUN_1801a6df0  (entree 1801a6df0)
// ===================================================

void FUN_1801a6df0(undefined8 param_1,int *param_2,short *param_3)

{
  short *psVar1;
  short *psVar2;
  int iVar3;
  int iVar4;
  
  psVar2 = &DAT_180410d78;
  iVar3 = 0;
  psVar1 = &DAT_180410d78;
  do {
    iVar4 = iVar3;
    if (*param_3 == *psVar1) break;
    iVar3 = iVar3 + 1;
    psVar1 = psVar1 + 1;
    iVar4 = 0;
  } while ((longlong)psVar1 < 0x180410d88);
  *param_2 = iVar4;
  iVar3 = 0;
  psVar1 = &DAT_180410d78;
  do {
    iVar4 = iVar3;
    if (param_3[1] == *psVar1) break;
    iVar3 = iVar3 + 1;
    psVar1 = psVar1 + 1;
    iVar4 = 0;
  } while ((longlong)psVar1 < 0x180410d88);
  param_2[1] = iVar4;
  psVar1 = &DAT_180410d78;
  iVar3 = 0;
  do {
    iVar4 = iVar3;
    if (param_3[2] == *psVar1) break;
    iVar3 = iVar3 + 1;
    psVar1 = psVar1 + 1;
    iVar4 = 0;
  } while ((longlong)psVar1 < 0x180410d88);
  param_2[2] = iVar4;
  psVar1 = &DAT_180410d78;
  iVar3 = 0;
  do {
    iVar4 = iVar3;
    if (param_3[3] == *psVar1) break;
    iVar3 = iVar3 + 1;
    psVar1 = psVar1 + 1;
    iVar4 = 0;
  } while ((longlong)psVar1 < 0x180410d88);
  param_2[3] = iVar4;
  psVar1 = &DAT_180410d78;
  iVar3 = 0;
  do {
    iVar4 = iVar3;
    if (param_3[4] == *psVar1) break;
    iVar3 = iVar3 + 1;
    psVar1 = psVar1 + 1;
    iVar4 = 0;
  } while ((longlong)psVar1 < 0x180410d88);
  param_2[4] = iVar4;
  psVar1 = &DAT_180410d78;
  iVar3 = 0;
  do {
    iVar4 = iVar3;
    if (param_3[5] == *psVar1) break;
    iVar3 = iVar3 + 1;
    psVar1 = psVar1 + 1;
    iVar4 = 0;
  } while ((longlong)psVar1 < 0x180410d88);
  param_2[5] = iVar4;
  psVar1 = &DAT_180410d78;
  iVar3 = 0;
  do {
    iVar4 = iVar3;
    if (param_3[6] == *psVar1) break;
    iVar3 = iVar3 + 1;
    psVar1 = psVar1 + 1;
    iVar4 = 0;
  } while ((longlong)psVar1 < 0x180410d88);
  param_2[6] = iVar4;
  iVar3 = 0;
  do {
    if (param_3[7] == *psVar2) {
      param_2[7] = iVar3;
      return;
    }
    iVar3 = iVar3 + 1;
    psVar2 = psVar2 + 1;
  } while ((longlong)psVar2 < 0x180410d88);
  param_2[7] = 0;
  return;
}



// ===================================================
// 1801AA766  ->  FUN_1801aa6e0  (entree 1801aa6e0)
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



