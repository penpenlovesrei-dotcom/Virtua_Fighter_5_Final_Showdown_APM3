// ===================================================
// 82214558  ->  FUN_82214550  (entree 82214550)
// ===================================================

undefined8 FUN_82214550(void)

{
  if (DAT_829b4ba5 == '\0') {
    return 0;
  }
  if (DAT_829b4ba6 == '\0') {
    return 0;
  }
  DAT_829b4ba6 = 0;
  return 1;
}



// ===================================================
// 82214874  ->  FUN_82214870  (entree 82214870)
// ===================================================

undefined8 FUN_82214870(void)

{
  return 0xffffffff829afa48;
}



// ===================================================
// 822148B0  ->  FUN_82214898  (entree 82214898)
// ===================================================

longlong FUN_82214898(undefined8 param_1)

{
  longlong lVar1;
  
  lVar1 = -0x7d655598;
  if (DAT_829b4ba4 == '\0') {
    if ((int)param_1 == 0) {
LAB_822148ec:
      return lVar1 + 0x4fe4;
    }
    if ((int)param_1 == 1) {
      if (-1 < DAT_829b4a64) {
        lVar1 = -0x7d65059c;
        goto LAB_822148ec;
      }
    }
  }
  FUN_821fdd20(param_1,0xffffffff829aaa50,0xffffffff829aaa56,0xffffffff829aaa54);
  return -0x7d6555b0;
}



// ===================================================
// 82214A54  ->  FUN_82214938  (entree 82214938)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

bool FUN_82214938(undefined8 param_1,int *param_2)

{
  short sVar1;
  short sVar2;
  int iVar3;
  int iVar4;
  short *psVar5;
  undefined4 *puVar6;
  short *psVar7;
  undefined4 *puVar8;
  bool bVar9;
  longlong lVar10;
  undefined4 uStack_44;
  int local_40;
  char local_3c [2];
  short local_3a [29];
  
  iVar3 = FUN_82214898();
  puVar8 = &uStack_44;
  puVar6 = (undefined4 *)(iVar3 + -4);
  lVar10 = 6;
  do {
    puVar6 = puVar6 + 1;
    puVar8 = puVar8 + 1;
    *puVar8 = *puVar6;
    lVar10 = lVar10 + -1;
  } while (lVar10 != 0);
  bVar9 = false;
  iVar3 = (int)param_1;
  if (((-1 < iVar3) && (iVar3 < 2)) && (param_2 != (int *)0x0)) {
    bVar9 = local_40 != *param_2;
    if (bVar9) {
      local_40 = *param_2;
      FUN_821fea08(local_3a);
    }
    iVar4 = 0;
    psVar7 = local_3a;
    psVar5 = (short *)((int)param_2 + 6);
    lVar10 = 8;
    do {
      sVar1 = *psVar5;
      sVar2 = *psVar7;
      if (sVar2 != sVar1) {
        bVar9 = true;
        *psVar7 = sVar1;
      }
      if (*psVar7 == 99) {
        iVar4 = iVar4 + 1;
      }
      psVar5 = psVar5 + 1;
      psVar7 = psVar7 + 1;
      lVar10 = lVar10 + -1;
    } while (lVar10 != 0);
    if (iVar4 == 8) {
      FUN_821fea08(local_3a,*param_2,sVar2,sVar1);
    }
    if (*(char *)(param_2 + 1) != local_3c[0]) {
      bVar9 = true;
      local_3c[0] = *(char *)(param_2 + 1);
    }
  }
  FUN_821fe8e0(param_1,local_40,local_3a,local_3c);
  puVar6 = &DAT_829aaa68;
  if (DAT_829b4ba4 == '\0') {
    if (iVar3 != 0) {
      if (iVar3 != 1) {
        return bVar9;
      }
      if (DAT_829b4a64 < 0) {
        return bVar9;
      }
      puVar6 = &DAT_829afa64;
    }
    puVar6 = puVar6 + 0x13f8;
    puVar8 = &uStack_44;
    lVar10 = 6;
    do {
      puVar8 = puVar8 + 1;
      puVar6 = puVar6 + 1;
      *puVar6 = *puVar8;
      lVar10 = lVar10 + -1;
    } while (lVar10 != 0);
  }
  return bVar9;
}



// ===================================================
// 8221555C  ->  FUN_82215500  (entree 82215500)
// ===================================================

undefined8 FUN_82215500(ulonglong param_1,undefined8 param_2)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  int iVar4;
  undefined8 uVar5;
  
  uVar5 = 0;
  if ((int)param_2 == -1) {
    param_2 = FUN_8239fde0();
  }
  if ((((-1 < (int)param_2) && ((int)param_2 < 4)) && (iVar4 = FUN_82214658(param_2), iVar4 != 0))
     && ((((int)param_2 == DAT_829b4a60 && (DAT_829b4a68 != '\0')) ||
         (((int)param_2 == DAT_829b4a64 && (DAT_829b4a69 != '\0')))))) {
    uVar3 = (uint)((param_1 & 0xffffffff) >> 3) & 0x1ffffffc;
    uVar2 = 1 << ((uint)param_1 & 0x1f);
    uVar1 = *(uint *)(uVar3 + iVar4);
    if ((uVar1 & uVar2) == 0) {
      if ((param_1 & 0xffffffff) < 0xc) {
        *(uint *)(uVar3 + iVar4) = uVar1 | uVar2;
      }
      FUN_823a65d8(param_2,param_1);
      uVar5 = 1;
    }
  }
  return uVar5;
}



