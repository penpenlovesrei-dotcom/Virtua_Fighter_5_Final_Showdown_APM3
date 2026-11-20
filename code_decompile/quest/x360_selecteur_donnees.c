// ===================================================
// 82307D48  ->  FUN_82307d48  (entree 82307d48)
// ===================================================

/* WARNING: Function: __savegprlr_16 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_16 replaced with injection: x360_restgprlr */

void FUN_82307d48(int param_1)

{
  uint uVar1;
  bool bVar2;
  char cVar10;
  undefined8 uVar3;
  int iVar8;
  undefined8 uVar4;
  longlong lVar5;
  ulonglong uVar6;
  int iVar9;
  longlong lVar7;
  undefined8 uVar11;
  ulonglong uVar12;
  int iVar13;
  int iVar14;
  longlong lVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  double dVar18;
  double dVar19;
  double dVar20;
  float fStack_170;
  float fStack_16c;
  float fStack_168;
  float fStack_160;
  float fStack_15c;
  float fStack_158;
  undefined1 auStack_150 [32];
  float fStack_130;
  float fStack_12c;
  undefined4 uStack_128;
  undefined4 uStack_124;
  undefined1 auStack_120 [288];
  
  cVar10 = FUN_822c80d0();
  if (((cVar10 == '\0') || (*(int *)(param_1 + 0x4c) < 0)) ||
     (bVar2 = true, 6 < *(int *)(param_1 + 0x4c))) {
    bVar2 = false;
  }
  if (!bVar2) {
    return;
  }
  dVar18 = (double)DAT_82000a34;
  fStack_170 = DAT_82000a34;
  fStack_16c = DAT_82000a34;
  fStack_168 = DAT_82000a34;
  uVar11 = 0xffffffffff808080;
  if (*(char *)(param_1 + 100) == '\0') {
    uVar11 = 0xffffffffffffffff;
  }
  uVar3 = FUN_822c29e8();
  FUN_822c29d8(2);
  FUN_822c2a08(9);
  iVar13 = param_1 + 0x68;
  cVar10 = FUN_822e2dd8(iVar13);
  if (cVar10 == '\0') goto LAB_823082cc;
  FUN_8223bc10(0xe);
  FUN_8223c048(0xffffffffffffffff);
  FUN_8223c130(9);
  FUN_82249520(auStack_150,0x20,0xffffffff8208dc6c,(ulonglong)*(uint *)(param_1 + 0x50) + 1);
  FUN_822e39c0(iVar13,&fStack_170,auStack_150,1);
  FUN_8223beb8((double)fStack_170,(double)fStack_16c);
  uVar17 = 0x54b;
  iVar8 = FUN_822fcdd8();
  if (iVar8 == 0) {
    uVar17 = 0x54c;
  }
  else {
    iVar8 = FUN_822fcdd8();
    if (iVar8 == 3) {
      uVar17 = 0x54e;
    }
    else {
      iVar8 = FUN_822fcdd8();
      if (iVar8 == 1) {
        uVar17 = 0x54d;
      }
    }
  }
  uVar4 = FUN_82322798(uVar17);
  FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar4);
  dVar19 = (double)DAT_82000b08;
  if (*(int *)(param_1 + 0x54) == 0) {
    FUN_82322798(uVar17);
    FUN_822e37e0((double)fStack_170,(double)fStack_16c,dVar19,param_1 + 0xc0);
  }
  dVar20 = (double)DAT_82000f1c;
  fStack_16c = (float)((double)fStack_16c + dVar20);
  FUN_8223beb8((double)fStack_170);
  uVar17 = 0xffffffffff808080;
  if (*(char *)(param_1 + 0x60) != '\0') {
    uVar17 = uVar11;
  }
  FUN_8223c048(uVar17);
  uVar17 = FUN_82322798(0x54a);
  FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar17);
  FUN_8223c048(uVar11);
  if (*(int *)(param_1 + 0x54) == 1) {
    FUN_82322798(0x54a);
    FUN_822e37e0((double)fStack_170,(double)fStack_16c,dVar19,param_1 + 0xc0);
  }
  uVar17 = FUN_8223c1b0();
  uVar4 = FUN_8223c1d8();
  FUN_82249520(auStack_150,0x20,0xffffffff8208dc54,(ulonglong)*(uint *)(param_1 + 0x50) + 1);
  FUN_822e39c0(iVar13,&fStack_170,auStack_150,0);
  uVar1 = *(uint *)(param_1 + 0x54);
  fStack_170 = fStack_170 - DAT_8208d01c;
  uVar6 = 2;
  if (1 < (int)uVar1) {
    uVar6 = (ulonglong)uVar1;
  }
  if ((int)uVar1 < 0x1e) {
    uVar12 = uVar6;
    if (((2 < (int)uVar1) && (uVar12 = uVar6 - 1, 3 < (int)uVar1)) &&
       (*(int *)(param_1 + 0x58) < (int)uVar1)) {
      uVar12 = uVar6 - 2;
    }
  }
  else {
    uVar12 = 0x1c;
  }
  iVar8 = (int)uVar12;
  iVar14 = iVar8 + 4;
  if (iVar8 < iVar14) {
    lVar7 = uVar12 - 2;
    do {
      FUN_8223beb8((double)fStack_170,(double)fStack_16c);
      lVar5 = FUN_82322798(0x548);
      uVar6 = FUN_822da8b8(*(undefined4 *)(param_1 + 0x50),lVar7);
      if (((uVar6 & 0xffffffff) != 0) && (cVar10 = FUN_821f6110(), cVar10 == '\0')) {
        lVar5 = uVar6 + 0xfd;
        FUN_8223c198(1);
        FUN_8223c1c0(1);
      }
      lVar15 = lVar7 + 1;
      FUN_82249520(auStack_120,0x80,0xffffffff8208dc48,lVar15,lVar5);
      uVar16 = uVar11;
      if (*(int *)(param_1 + 0x54) == (int)lVar7 + 2) {
        FUN_822e37e0((double)fStack_170,(double)fStack_16c,dVar19,param_1 + 0xc0);
      }
      else {
        iVar9 = FUN_82144c28();
        if (iVar9 < 0) {
          iVar9 = FUN_822da898(*(undefined4 *)(&DAT_820036c0 + *(int *)(param_1 + 0x50) * 4));
          uVar16 = 0xffffffffff808080;
          if ((int)lVar7 != iVar9) {
            uVar16 = uVar11;
          }
        }
      }
      FUN_8223c048(uVar16);
      FUN_8223fe30(0xffffffff82000f08,auStack_120);
      FUN_8223c198(uVar17);
      FUN_8223c1c0(uVar4);
      fStack_16c = (float)((double)fStack_16c + dVar20);
      lVar7 = lVar15;
    } while ((int)lVar15 + 2 < iVar14);
  }
  if (*(char *)(param_1 + 100) == '\0') {
    FUN_822e32b8(param_1 + 200,0xffffffffffffffff,2 < iVar8);
    uVar11 = 1;
    if (0x1f < iVar14) goto LAB_823081c8;
  }
  else {
    FUN_822e32b8(param_1 + 200,0xffffffffffffffff,0);
LAB_823081c8:
    uVar11 = 0;
  }
  FUN_822e32b8(param_1 + 200,1,uVar11);
  fStack_160 = (float)dVar18;
  fStack_15c = (float)dVar18;
  fStack_158 = (float)dVar18;
  FUN_82249520(auStack_150,0x20,0xffffffff8208dc2c,(ulonglong)*(uint *)(param_1 + 0x50) + 1);
  FUN_822e39c0(iVar13,&fStack_170,auStack_150,0);
  FUN_82249520(auStack_150,0x20,0xffffffff8208dc0c,(ulonglong)*(uint *)(param_1 + 0x50) + 1);
  FUN_822e39c0(iVar13,&fStack_160,auStack_150,0);
  FUN_822e53f8((double)fStack_170,(double)fStack_16c,(double)fStack_160,(double)fStack_15c,
               param_1 + 200);
  FUN_82249520(auStack_150,0x20,0xffffffff8208dbf4,(ulonglong)*(uint *)(param_1 + 0x50) + 1);
  FUN_822e39c0(iVar13,&fStack_170,auStack_150,0);
  FUN_8223beb8((double)fStack_170,(double)fStack_16c);
  FUN_8223c048(0xffffffffffffffff);
  uVar11 = FUN_82322798(0);
  FUN_8223fe30(0xffffffff82085944,0xffffffff82010300,uVar11);
LAB_823082cc:
  cVar10 = FUN_822e2dd8(param_1 + 0x94);
  if (cVar10 != '\0') {
    if ((*(char *)(param_1 + 0x61) == '\0') && (cVar10 = FUN_822fde60(), cVar10 == '\0')) {
      uVar6 = (ulonglong)*(uint *)(param_1 + 0x50) ^ 1;
    }
    else {
      uVar6 = (ulonglong)*(uint *)(param_1 + 0x50);
    }
    FUN_82249520(auStack_150,0x20,0xffffffff8208dbdc,uVar6 + 1);
    FUN_822e39c0(param_1 + 0x94,&fStack_170,auStack_150,1);
    FUN_8223bc10(0xe);
    FUN_8223c130(9);
    FUN_8223c048(0xffffffffffffffff);
    fStack_130 = fStack_170;
    fStack_12c = fStack_16c;
    uStack_128 = DAT_82011844;
    uStack_124 = DAT_8208dbd8;
    FUN_8223bec0(&fStack_130,9);
    if (*(char *)(param_1 + 0x61) == '\0') {
      cVar10 = FUN_822fde60();
      if (cVar10 == '\0') {
        lVar7 = ((ulonglong)(*(int *)(param_1 + 0x50) == 0) ^ 1) + 0x556;
      }
      else {
        lVar7 = 0x558;
      }
    }
    else {
      lVar7 = 0x553;
    }
    uVar11 = FUN_82322798(lVar7);
    FUN_8223fe30(0xffffffff82000f08,uVar11);
  }
  FUN_822c2a18();
  FUN_822c29d8(uVar3);
  return;
}



// ===================================================
// 82307AE0  ->  FUN_82307ae0  (entree 82307ae0)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82307ae0(int param_1)

{
  bool bVar1;
  char cVar3;
  int iVar2;
  undefined8 uVar4;
  
  FUN_822d0c30(*(undefined4 *)(param_1 + 0x50));
  uVar4 = 10;
  if (*(int *)(param_1 + 0x54) < 2) {
    uVar4 = 99;
  }
  FUN_822d0810(*(undefined4 *)(param_1 + 0x50),uVar4);
  *(undefined1 *)(param_1 + 100) = 0;
  iVar2 = *(int *)(&DAT_820036c0 + *(int *)(param_1 + 0x50) * 4);
  cVar3 = FUN_822c80d0(&DAT_82acb004 + iVar2 * 0x3d);
  if (cVar3 == '\0') {
    bVar1 = false;
  }
  else if ((*(int *)(&DAT_82acb050 + iVar2 * 0xf4) == 4) ||
          (bVar1 = false, *(int *)(&DAT_82acb050 + iVar2 * 0xf4) == 5)) {
    bVar1 = true;
  }
  if (bVar1) {
    *(undefined1 *)(param_1 + 100) = 1;
  }
  FUN_822e4d70(param_1 + 0x68);
  FUN_822e4d70(param_1 + 0x94);
  switch(*(undefined4 *)(param_1 + 0x4c)) {
  case 0:
    FUN_82307610(param_1);
    return 0;
  case 1:
    FUN_822e3c10(0xffffffff82acaf0c);
    FUN_822c8aa0(0xffffffff82acaf0c,0xffffffff8208dbd0);
    FUN_822e2e28(0xffffffff82acaf0c,1);
    DAT_82acaf6c = FUN_82322798(0x5f7);
    *(undefined4 *)(param_1 + 0x4c) = 2;
    return 0;
  case 2:
    cVar3 = FUN_822c7b98(0xffffffff82acaf0c);
    if (cVar3 == '\0') {
      iVar2 = FUN_822e2e38(0xffffffff82acaf0c);
      if (iVar2 != 0) {
        *(undefined4 *)(param_1 + 0x4c) = 0;
        return 0;
      }
      FUN_822d0828(*(undefined4 *)(param_1 + 0x50));
      FUN_822daa70(*(undefined4 *)(param_1 + 0x50));
      FUN_822e3c10(0xffffffff82acaf0c);
      FUN_822c8aa0(0xffffffff82acaf0c,0xffffffff8208dbc4);
      DAT_82acaf6c = FUN_82322798(0x5f8);
      *(undefined4 *)(param_1 + 0x4c) = 3;
      return 0;
    }
    break;
  case 3:
    FUN_822d0828(*(undefined4 *)(param_1 + 0x50));
    cVar3 = FUN_822c7b98(0xffffffff82acaf0c);
    if (cVar3 == '\0') {
      FUN_82307298(param_1);
    }
    break;
  case 4:
    FUN_82307870(param_1);
    return 0;
  case 5:
    FUN_82307920(param_1);
    return 0;
  case 6:
    FUN_82307780(param_1);
    return 0;
  case 7:
    FUN_823079a8(param_1);
    return 0;
  }
  return 0;
}



// ===================================================
// 823084E8  ->  FUN_823084e8  (entree 823084e8)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_823084e8(undefined4 param_1,undefined4 param_2,undefined4 *param_3,undefined4 param_4)

{
  undefined1 auStack_110 [4];
  undefined4 uStack_10c;
  undefined4 uStack_104;
  undefined4 uStack_f4;
  undefined4 uStack_f0;
  undefined4 uStack_ec;
  undefined4 uStack_d4;
  undefined4 uStack_d0;
  undefined4 uStack_cc;
  
  FUN_822b99e8(auStack_110);
  uStack_d4 = *param_3;
  uStack_d0 = param_3[1];
  uStack_cc = param_3[2];
  uStack_f0 = 9;
  uStack_ec = 9;
  uStack_10c = param_1;
  uStack_104 = param_4;
  uStack_f4 = param_2;
  FUN_822c2940(auStack_110);
  return;
}



