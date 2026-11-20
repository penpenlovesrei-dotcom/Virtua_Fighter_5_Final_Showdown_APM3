// ===================================================
// 84B8A64  ->  FUN_084b8a64  (entree 084b8a64)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_084b8a64(int param_1)

{
  char cVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  longdouble lVar5;
  undefined4 uVar6;
  
  iVar3 = *(int *)(param_1 + 0x50);
  iVar4 = *(int *)(param_1 + 0x58);
  iVar2 = iVar4 + iVar3 * 4;
  while (iVar2 != iVar4) {
    cVar1 = FUN_08294526(iVar4);
    if (cVar1 == '\0') {
      return 0;
    }
    iVar3 = *(int *)(param_1 + 0x50);
    iVar4 = iVar4 + 4;
    iVar2 = *(int *)(param_1 + 0x58) + iVar3 * 4;
  }
  iVar4 = *(int *)(param_1 + 0x58);
  iVar2 = iVar4 + iVar3 * 4;
  do {
    if (iVar2 == iVar4) {
      if (*(char *)(param_1 + 0x9c) != '\0') {
        FUN_080aff74(0x19,FUN_084b86b0,param_1);
      }
      if ((*(char *)(param_1 + 0x9d) != '\0') || (*(char *)(param_1 + 0x9c) != '\0')) {
        FUN_080aff74(2,&LAB_084b86c8,param_1);
        FUN_080aff74(3,&LAB_084b86e6,param_1);
      }
      return 1;
    }
    iVar2 = FUN_082944e0(iVar4);
    if (iVar2 - 0x4e8U < 2) {
      lVar5 = (longdouble)FUN_082945fe(iVar4);
      FUN_082948da(iVar4,(float)lVar5 - _DAT_088353c8);
      FUN_082949f8(iVar4);
LAB_084b8ab1:
      FUN_08294852(iVar4,1);
      FUN_0829473a(iVar4,0);
      uVar6 = 1;
    }
    else {
      if (iVar2 != 0x7f4) goto LAB_084b8ab1;
      FUN_08294852(iVar4,0);
      FUN_0829473a(iVar4,1);
      uVar6 = 0;
    }
    FUN_082947ca(iVar4,uVar6);
    iVar4 = iVar4 + 4;
    iVar2 = *(int *)(param_1 + 0x58) + *(int *)(param_1 + 0x50) * 4;
  } while( true );
}



// ===================================================
// 84B87A8  ->  FUN_084b87a8  (entree 084b87a8)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_084b87a8(int param_1)

{
  int iVar1;
  int iVar2;
  longdouble lVar3;
  float fVar4;
  float fVar5;
  undefined1 local_5c [76];
  
  if ((*(char *)(param_1 + 0x9c) != '\0') && (0 < *(int *)(param_1 + 0xa0))) {
    iVar2 = *(int *)(param_1 + 0x58);
    iVar1 = iVar2 + *(int *)(param_1 + 0x50) * 4;
    while (iVar1 != iVar2) {
      iVar1 = FUN_082944e0(iVar2);
      if (iVar1 == 0x7f4) {
        if (*(int *)(param_1 + 0xa0) == 3) {
          FUN_082947ca(iVar2,0);
        }
        else {
          FUN_08294574(iVar2,0);
          FUN_0829473a(iVar2,0);
          FUN_082947ca(iVar2,1);
          if (*(int *)(param_1 + 0xa0) == 1) {
            FUN_08294852(iVar2,0);
            FUN_08294acc(iVar2,1);
          }
          else {
            FUN_08294852(iVar2,1);
          }
        }
      }
      iVar2 = iVar2 + 4;
      iVar1 = *(int *)(param_1 + 0x58) + *(int *)(param_1 + 0x50) * 4;
    }
    *(undefined4 *)(param_1 + 0xa0) = 0;
  }
  if (*(char *)(param_1 + 0x9d) == '\0') {
    return 0;
  }
  FUN_0809ad5a(local_5c);
  iVar1 = 0;
  if (DAT_08765870 <= *(float *)(param_1 + 0xa4)) {
    iVar1 = (int)*(float *)(param_1 + 0xa4);
    lVar3 = (longdouble)FUN_080cac34();
    fVar5 = (float)lVar3 + *(float *)(param_1 + 0xa4);
    fVar4 = 0.0;
    if (fVar5 <= DAT_088353c4) {
      fVar4 = fVar5;
    }
    *(float *)(param_1 + 0xa4) = fVar4;
  }
  lVar3 = (longdouble)
          fsin((longdouble)(float)((double)((float)(iVar1 % 0x200) * _DAT_0877aa00) * _DAT_0877aa08)
              );
  fVar5 = (float)lVar3 * DAT_08777f44;
  lVar3 = (longdouble)
          fsin((longdouble)(float)((double)((float)(iVar1 % 0x168) * _DAT_0877aa04) * _DAT_0877aa08)
              );
  fVar4 = DAT_08777f44 * (float)lVar3;
  FUN_0809e236(local_5c);
  FUN_0809f278(local_5c,0,0xbe4ccccd,0);
  FUN_0809f050(local_5c,fVar5);
  FUN_0809f250(local_5c,fVar4);
  iVar2 = *(int *)(param_1 + 0x58);
  iVar1 = iVar2 + *(int *)(param_1 + 0x50) * 4;
  while (iVar1 != iVar2) {
    iVar1 = FUN_082944e0(iVar2);
    if (iVar1 - 0x4e8U < 2) {
      FUN_08294b54(iVar2,local_5c);
    }
    iVar2 = iVar2 + 4;
    iVar1 = *(int *)(param_1 + 0x58) + *(int *)(param_1 + 0x50) * 4;
  }
  FUN_0810886e(local_5c);
  return 0;
}



// ===================================================
// 84B8D66  ->  FUN_084b8d66  (entree 084b8d66)
// ===================================================

void FUN_084b8d66(int param_1,int param_2)

{
  uint uVar1;
  undefined4 *puVar2;
  int iVar3;
  char cVar4;
  int iVar5;
  int *piVar6;
  int *piVar7;
  int aiStack_54 [9];
  int local_30;
  undefined4 local_2c [7];
  
  piVar6 = &DAT_088351c0;
  iVar5 = DAT_088351c0;
  while( true ) {
    if (iVar5 == -1) {
      return;
    }
    if (iVar5 == param_2) break;
    piVar6 = piVar6 + 2;
    iVar5 = *piVar6;
  }
  if (piVar6 == (int *)0x0) {
    return;
  }
  piVar6 = (int *)piVar6[1];
  if (piVar6 == (int *)0x0) {
    return;
  }
  if (param_2 == 8) {
    *(undefined1 *)(param_1 + 0x9d) = 1;
  }
  else if (param_2 == 0x27) {
    *(undefined1 *)(param_1 + 0x9c) = 1;
  }
  iVar5 = *piVar6;
  if (iVar5 == -1) {
    return;
  }
  local_30 = param_1 + 0x50;
  piVar7 = aiStack_54 + 2;
  do {
    if (*(int *)(param_1 + 0x50) == *(int *)(local_30 + 4)) {
      return;
    }
    piVar7[1] = iVar5;
    *piVar7 = (int)local_2c;
    piVar7[-1] = 0x84b8dd7;
    FUN_0829a0e4();
    piVar7[-1] = (int)local_2c;
                    /* try { // try from 084b8ddd to 084b8de1 has its CatchHandler @ 084b8dfb */
    piVar7[-2] = 0x84b8de2;
    cVar4 = FUN_08294494();
    if (cVar4 != '\0') {
      piVar7[-1] = (int)local_2c;
                    /* try { // try from 084b8e0f to 084b8e13 has its CatchHandler @ 084b8dfb */
      piVar7[-2] = 0x84b8e14;
      FUN_0829786c();
      iVar5 = *(int *)(param_1 + 0x50);
      uVar1 = iVar5 + 1;
      if (uVar1 <= *(uint *)(local_30 + 4)) {
        iVar3 = *(int *)(local_30 + 8);
        *(uint *)(param_1 + 0x50) = uVar1;
        puVar2 = (undefined4 *)(iVar3 + iVar5 * 4);
        if (puVar2 != (undefined4 *)0x0) {
          *puVar2 = local_2c[0];
        }
      }
    }
    piVar6 = piVar6 + 1;
    iVar5 = *piVar6;
    piVar7 = piVar7 + -1;
  } while (iVar5 != -1);
  return;
}



// ===================================================
// 84B8CE4  ->  FUN_084b8ce4  (entree 084b8ce4)
// ===================================================

undefined4 FUN_084b8ce4(int param_1)

{
  if (*(char *)(param_1 + 0x9c) != '\0') {
    FUN_080b0016(0x19,FUN_084b86b0,param_1);
  }
  if ((*(char *)(param_1 + 0x9d) != '\0') || (*(char *)(param_1 + 0x9c) != '\0')) {
    FUN_080b0016(2,&LAB_084b86c8,param_1);
    FUN_080b0016(3,&LAB_084b86e6,param_1);
  }
  FUN_084b8c72(param_1);
  return 1;
}



// ===================================================
// 84B8C22  ->  FUN_084b8c22  (entree 084b8c22)
// ===================================================

void FUN_084b8c22(int param_1,undefined1 param_2)

{
  int iVar1;
  
  iVar1 = *(int *)(param_1 + 0x58);
  if (iVar1 + *(int *)(param_1 + 0x50) * 4 != iVar1) {
    do {
      FUN_08294cfe(iVar1,param_2);
      iVar1 = iVar1 + 4;
    } while (*(int *)(param_1 + 0x58) + *(int *)(param_1 + 0x50) * 4 != iVar1);
  }
  return;
}



// ===================================================
// 84B8BE0  ->  FUN_084b8be0  (entree 084b8be0)
// ===================================================

void FUN_084b8be0(int param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  
  iVar1 = *(int *)(param_1 + 0x58) + *(int *)(param_1 + 0x50) * 4;
  iVar2 = *(int *)(param_1 + 0x58);
  while (iVar1 != iVar2) {
    FUN_082946ce(iVar2,param_2);
    iVar2 = iVar2 + 4;
    iVar1 = *(int *)(param_1 + 0x58) + *(int *)(param_1 + 0x50) * 4;
  }
  return;
}



