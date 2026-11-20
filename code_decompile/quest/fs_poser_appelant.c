// ===================================================
// 180203315  ->  FUN_1802031c0  (entree 1802031c0)
// ===================================================

undefined8 FUN_1802031c0(undefined1 *param_1)

{
  int iVar1;
  char cVar2;
  int iVar3;
  undefined4 uVar4;
  undefined8 uVar5;
  ulonglong uVar6;
  uint uVar7;
  ulonglong uVar9;
  uint local_res10 [6];
  undefined4 auStack_38 [4];
  ulonglong uVar8;
  
  uVar5 = FUN_1800b23a0();
  cVar2 = FUN_180244ea0(DAT_180714928);
  if (cVar2 == '\0') {
    cVar2 = FUN_18016d360(DAT_180714928);
    if (cVar2 == '\0') {
      FUN_180101a30(DAT_18070fb10);
      return 1;
    }
    FUN_180186d40(0);
    *param_1 = 1;
    return 1;
  }
  iVar3 = FUN_1800244d0(uVar5);
  iVar1 = *(int *)(&DAT_18034b208 + (longlong)iVar3 * 4);
  cVar2 = FUN_18016d330(DAT_180714928);
  if (cVar2 == '\0') {
    cVar2 = FUN_18016d2f0(DAT_180714928,iVar3);
    if (cVar2 != '\0') {
      FUN_1801a3870(iVar3,0xffffffff);
      FUN_1801a3870(iVar1,iVar3);
    }
    return 0;
  }
  uVar6 = 0;
  uVar8 = uVar6;
  uVar9 = uVar6;
  do {
    *(undefined4 *)((longlong)local_res10 + uVar9 + 8) = 0x14;
    *(undefined4 *)((longlong)auStack_38 + uVar9) = 0;
    *(undefined4 *)((longlong)local_res10 + uVar9) = 0;
    *(undefined4 *)((longlong)local_res10 + uVar9 + 0x10) = 0;
    cVar2 = FUN_1800b1d30(uVar5,uVar8);
    if (cVar2 != '\0') {
      uVar4 = FUN_18016cf50(DAT_180714928,uVar8);
      *(undefined4 *)((longlong)local_res10 + uVar9 + 8) = uVar4;
      uVar4 = FUN_18016cf30(DAT_180714928,uVar8);
      *(undefined4 *)((longlong)auStack_38 + uVar9) = uVar4;
      uVar4 = FUN_18016cf20(DAT_180714928,uVar8,uVar4);
      *(undefined4 *)((longlong)local_res10 + uVar9) = uVar4;
      uVar4 = FUN_18016cf40(DAT_180714928,uVar8);
      *(undefined4 *)((longlong)local_res10 + uVar9 + 0x10) = uVar4;
    }
    uVar7 = (int)uVar8 + 1;
    uVar8 = (ulonglong)uVar7;
    uVar9 = uVar9 + 4;
  } while ((int)uVar7 < 2);
  uVar8 = uVar6;
  if ((local_res10[2] == local_res10[3]) && (local_res10[0] == local_res10[1])) {
    local_res10[iVar1] = (uint)(local_res10[iVar1] == 0);
  }
  do {
    FUN_1800b2f80(uVar5,uVar6,*(undefined4 *)((longlong)local_res10 + uVar8 + 8),
                  *(undefined4 *)((longlong)local_res10 + uVar8),
                  *(undefined4 *)((longlong)auStack_38 + uVar8),
                  *(undefined4 *)((longlong)local_res10 + uVar8 + 0x10));
    uVar7 = (int)uVar6 + 1;
    uVar6 = (ulonglong)uVar7;
    uVar8 = uVar8 + 4;
  } while ((int)uVar7 < 2);
  FUN_1801a3870(iVar3,iVar3);
  FUN_1801a3870(iVar1,0xffffffff);
  return 0;
}



