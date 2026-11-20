// ===================================================
// 1801b6eb0  ->  FUN_1801b6eb0  (entree 1801b6eb0)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

ulonglong FUN_1801b6eb0(longlong param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  longlong lVar1;
  int iVar2;
  ulonglong in_RAX;
  undefined8 ****ppppuVar3;
  undefined8 uVar4;
  undefined1 local_50;
  undefined7 uStack_4f;
  undefined8 local_40;
  ulonglong uStack_38;
  undefined8 ***local_30 [3];
  ulonglong local_18;
  
  uVar4 = 0xfffffffffffffffe;
  if (param_1 != 0) {
    in_RAX = FUN_1802161c0(DAT_180752148 + 0x67b8);
    if ((char)in_RAX != '\0') {
      local_40 = _DAT_1803478a0;
      uStack_38 = _UNK_1803478a8;
      local_50 = 0;
      FUN_1800524e0(&local_50,param_1,param_3,param_4,uVar4);
      FUN_1802115e0(local_30,&local_50);
      if (0xf < uStack_38) {
        if (0xfff < uStack_38 + 1) {
          lVar1 = *(longlong *)(CONCAT71(uStack_4f,local_50) + -8);
          if (0x1f < (CONCAT71(uStack_4f,local_50) - lVar1) - 8U) {
                    /* WARNING: Subroutine does not return */
            FUN_180303af0(lVar1,uStack_38 + 0x28);
          }
        }
        FUN_1802fdd80();
      }
      local_40 = _DAT_1803478a0;
      uStack_38 = _UNK_1803478a8;
      local_50 = 0;
      ppppuVar3 = local_30;
      if (0xf < local_18) {
        ppppuVar3 = (undefined8 ****)local_30[0];
      }
      iVar2 = FUN_180215e60(DAT_180752148 + 0x67b8,ppppuVar3);
      if (0xf < local_18) {
        if (0xfff < local_18 + 1) {
          if (0x1f < (ulonglong)((longlong)local_30[0] + (-8 - (longlong)local_30[0][-1]))) {
                    /* WARNING: Subroutine does not return */
            FUN_180303af0(local_30[0][-1],local_18 + 0x28);
          }
        }
        FUN_1802fdd80();
      }
      return (ulonglong)(-1 < iVar2);
    }
  }
  return in_RAX & 0xffffffffffffff00;
}



// ===================================================
// 180217c60  ->  FUN_180217c60  (entree 180217c60)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8
FUN_180217c60(undefined4 *param_1,char *param_2,char *param_3,undefined4 param_4,undefined1 param_5,
             undefined1 param_6)

{
  undefined8 *puVar1;
  longlong lVar2;
  char cVar3;
  undefined4 uVar4;
  undefined8 uVar5;
  undefined1 *puVar6;
  undefined4 *local_res8;
  undefined1 local_50;
  undefined7 uStack_4f;
  undefined8 local_40;
  ulonglong uStack_38;
  
  if (((param_2 != (char *)0x0) && (*param_2 == '.')) && (param_2[1] == '/')) {
    param_2 = param_2 + 2;
  }
  if (((param_3 != (char *)0x0) && (*param_3 == '.')) && (param_3[1] == '/')) {
    param_3 = param_3 + 2;
  }
  local_40 = _DAT_1803478a0;
  uStack_38 = _UNK_1803478a8;
  local_50 = 0;
  *(undefined8 *)(param_1 + 0x1e) = 0;
  *(undefined8 *)(param_1 + 0x20) = 0;
  *(undefined1 *)(param_1 + 0x22) = param_6;
  uVar5 = 0;
  if (param_3 != (char *)0x0) {
    cVar3 = FUN_180217bf0();
    if (cVar3 == '\0') {
      puVar6 = (undefined1 *)0x0;
      if (param_2 == (char *)0x0) {
        cVar3 = FUN_180217950(&local_50,param_3,1);
        if (cVar3 == '\0') goto LAB_180217dd7;
        puVar6 = &local_50;
        if (0xf < uStack_38) {
          puVar6 = (undefined1 *)CONCAT71(uStack_4f,local_50);
        }
      }
      cVar3 = FUN_1802164b0(param_1,param_2,param_3,puVar6);
      if (cVar3 != '\0') {
        param_1[1] = 3;
        *param_1 = 1;
        param_1[2] = 1;
        uVar4 = param_1[2];
        if (param_2 != (char *)0x0) {
          uVar4 = 7;
        }
        param_1[2] = uVar4;
        *(undefined1 *)((longlong)param_1 + 0x89) = param_5;
        param_1[10] = param_4;
        param_1[0x19] = 0;
        *(undefined8 *)(param_1 + 0x1a) = 0;
        *(undefined8 *)(param_1 + 0x1c) = 0;
        lVar2 = DAT_180c3bd38;
        if (param_1 == (undefined4 *)(DAT_180c3bd38 + 0x28)) {
          *(undefined1 *)(DAT_180c3bd38 + 0xf2) = 1;
          uVar5 = 1;
        }
        else {
          puVar1 = *(undefined8 **)(DAT_180c3bd38 + 8);
          local_res8 = param_1;
          if (*(undefined8 **)(DAT_180c3bd38 + 0x10) == puVar1) {
            FUN_18002c630(DAT_180c3bd38,puVar1,&local_res8);
            uVar5 = 1;
          }
          else {
            *puVar1 = param_1;
            *(longlong *)(lVar2 + 8) = *(longlong *)(lVar2 + 8) + 8;
            uVar5 = 1;
          }
        }
        goto LAB_180217e07;
      }
    }
  }
LAB_180217dd7:
  lVar2 = DAT_180c3bd38;
  if ((*(char *)(DAT_180c3bd38 + 0x1d8) == '\0') &&
     (param_1[2] = 0xf, *(char *)(param_1 + 0x22) == '\0')) {
    *(undefined1 *)(lVar2 + 0x1d8) = 1;
    _guard_check_icall();
  }
  param_1[2] = 0;
LAB_180217e07:
  if (0xf < uStack_38) {
    if (0xfff < uStack_38 + 1) {
      lVar2 = *(longlong *)(CONCAT71(uStack_4f,local_50) + -8);
      if (0x1f < (CONCAT71(uStack_4f,local_50) - lVar2) - 8U) {
                    /* WARNING: Subroutine does not return */
        FUN_180303af0(lVar2,uStack_38 + 0x28);
      }
    }
    FUN_1802fdd80();
  }
  return uVar5;
}



// ===================================================
// 180217e70  ->  FUN_180217e70  (entree 180217e70)
// ===================================================

void FUN_180217e70(undefined8 param_1,undefined8 param_2,undefined4 param_3)

{
  FUN_180217c60(param_1,0,param_2,param_3,0,0);
  return;
}



// ===================================================
// 1800f91b0  ->  FUN_1800f91b0  (entree 1800f91b0)
// ===================================================

longlong FUN_1800f91b0(uint param_1,int param_2)

{
  int iVar1;
  uint *puVar2;
  longlong lVar3;
  longlong lVar4;
  longlong lVar5;
  longlong lVar6;
  uint *puVar7;
  
  lVar6 = 0;
  lVar4 = *(longlong *)(DAT_18070fa88 + 0x98);
  if (*(int *)(DAT_18070fa88 + 0xa4) < (int)param_1) {
    return 0;
  }
  puVar7 = *(uint **)(DAT_18070fa88 + 0xa8);
  puVar2 = *(uint **)(DAT_18070fa88 + 0xb0);
  lVar3 = (longlong)puVar2 - (longlong)puVar7 >> 3;
  while (lVar5 = lVar3, 0 < lVar5) {
    lVar3 = lVar5 >> 1;
    if (puVar7[lVar3 * 2] < param_1) {
      puVar7 = puVar7 + lVar3 * 2 + 2;
      lVar3 = lVar5 + (-1 - lVar3);
    }
  }
  if ((puVar7 == puVar2) || (param_1 < *puVar7)) {
    puVar7 = puVar2;
  }
  if (puVar7 != puVar2) {
    lVar3 = (longlong)(int)puVar7[1];
    if ((int)puVar7[1] < 0) {
      return 0;
    }
    lVar5 = lVar6;
    if (param_2 == 0) {
      if (*(int *)(lVar4 + 8) != 0) {
        lVar5 = lVar4 + 8 + (longlong)*(int *)(lVar4 + 8);
      }
      lVar4 = lVar3 * 8 + 2;
    }
    else if (param_2 == 1) {
      if (*(int *)(lVar4 + 8) != 0) {
        lVar5 = lVar4 + 8 + (longlong)*(int *)(lVar4 + 8);
      }
      lVar4 = lVar3 * 8 + 3;
    }
    else {
      if (param_2 != 2) {
        return 0;
      }
      if (*(int *)(lVar4 + 8) != 0) {
        lVar5 = lVar4 + 8 + (longlong)*(int *)(lVar4 + 8);
      }
      lVar4 = lVar3 * 8 + 4;
    }
    iVar1 = *(int *)(lVar5 + (lVar4 + lVar3) * 4);
    if (iVar1 != 0) {
      lVar6 = lVar5 + (lVar4 + lVar3) * 4 + (longlong)iVar1;
    }
    return lVar6;
  }
  return 0;
}



