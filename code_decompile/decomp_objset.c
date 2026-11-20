// ===================================================
// 1800f8a40  ->  FUN_1800f8a40  (entree 1800f8a40)
// ===================================================

void FUN_1800f8a40(undefined4 param_1)

{
  char cVar1;
  longlong lVar2;
  
  cVar1 = FUN_1800f75b0();
  if (cVar1 == '\0') {
    lVar2 = FUN_1800f9450(param_1);
    if ((((lVar2 != 0) && (*(char *)(lVar2 + 0x138) != '\0')) && (*(char *)(lVar2 + 0x90) != '\0'))
       && (*(char *)(lVar2 + 0x128) != '\0')) {
      FUN_180217900(lVar2,1);
      return;
    }
  }
  return;
}



// ===================================================
// 1800f9450  ->  FUN_1800f9450  (entree 1800f9450)
// ===================================================

int * FUN_1800f9450(int param_1)

{
  int *piVar1;
  longlong lVar2;
  int iVar3;
  int *piVar4;
  char cVar5;
  longlong lVar6;
  int *piVar7;
  int *piVar8;
  
  if (DAT_180644a40._4_4_ == param_1) {
    return DAT_18070fa98;
  }
  piVar7 = (int *)0x0;
  cVar5 = FUN_1800f75b0();
  iVar3 = DAT_180644a40._4_4_;
  piVar4 = DAT_18070fa98;
  if (cVar5 == '\0') {
    piVar1 = (int *)DAT_18070fa90[1];
    piVar8 = (int *)*DAT_18070fa90;
    lVar6 = (longlong)piVar1 - (longlong)piVar8 >> 9;
    while (lVar2 = lVar6, 0 < lVar2) {
      lVar6 = lVar2 >> 1;
      if (piVar8[lVar6 * 0x80] < param_1) {
        piVar8 = piVar8 + lVar6 * 0x80 + 0x80;
        lVar6 = lVar2 + (-1 - lVar6);
      }
    }
    if ((piVar8 == piVar1) || (param_1 < *piVar8)) {
      piVar8 = piVar1;
    }
    piVar7 = piVar8 + 2;
    iVar3 = param_1;
    piVar4 = piVar7;
    if (piVar8 == piVar1) {
      return (int *)0x0;
    }
  }
  DAT_18070fa98 = piVar4;
  DAT_180644a40._4_4_ = iVar3;
  return piVar7;
}



// ===================================================
// 1800f97e0  ->  FUN_1800f97e0  (entree 1800f97e0)
// ===================================================

void FUN_1800f97e0(void)

{
  longlong lVar1;
  longlong lVar2;
  undefined1 local_88 [128];
  
  lVar1 = DAT_18070fa88;
  if (*(char *)(DAT_18070fa88 + 0x90) == '\0') {
    FUN_1800133d0(local_88,"./rom/objset/",0x80);
    FUN_1800132f0(local_88,"obj_db.bin",0x80);
    FUN_180217e70(lVar1,local_88,0);
    FUN_180218210(lVar1);
    lVar2 = FUN_180217940(lVar1);
    *(longlong *)(lVar1 + 0x98) = lVar2;
    if (lVar2 != 0) {
      FUN_1800fa8a0(lVar2);
      FUN_1800f9a40(lVar1);
      *(undefined4 *)(lVar1 + 0xa0) = **(undefined4 **)(lVar1 + 0x98);
      *(undefined4 *)(lVar1 + 0xa4) = (*(undefined4 **)(lVar1 + 0x98))[1];
      *(undefined1 *)(lVar1 + 0x90) = 1;
    }
  }
  return;
}



// ===================================================
// 1800f9c60  ->  FUN_1800f9c60  (entree 1800f9c60)
// ===================================================

undefined8 FUN_1800f9c60(undefined4 param_1,char param_2)

{
  longlong lVar1;
  char cVar2;
  longlong lVar3;
  longlong lVar4;
  undefined1 *puVar5;
  undefined1 *puVar6;
  undefined8 uVar7;
  undefined1 local_108 [128];
  undefined1 local_88 [128];
  
  cVar2 = FUN_1800f75b0();
  if (((cVar2 != '\0') || (lVar3 = FUN_1800f9450(param_1), lVar3 == 0)) ||
     (*(char *)(lVar3 + 500) != '\0')) {
    return 1;
  }
  if (0 < *(int *)(lVar3 + 0x1f0)) {
    *(int *)(lVar3 + 0x1f0) = *(int *)(lVar3 + 0x1f0) + 1;
    return 1;
  }
  lVar4 = FUN_1800f91b0(param_1,2);
  puVar5 = (undefined1 *)FUN_1800f91b0(param_1,0);
  puVar6 = (undefined1 *)FUN_1800f91b0(param_1,1);
  if (puVar5 == (undefined1 *)0x0) {
    return 1;
  }
  if (puVar6 == (undefined1 *)0x0) {
    return 1;
  }
  if (lVar4 != 0) {
    FUN_1800133d0(local_88,"./rom/objset/",0x80);
    FUN_1800132f0(local_88,lVar4,0x80);
  }
  FUN_1800133d0(local_108,"./rom/objset/",0x80);
  FUN_1800132f0(local_108,puVar5,0x80);
  if (param_2 == '\0') {
    *(undefined1 *)(lVar3 + 0x138) = 0;
    cVar2 = FUN_1801b6eb0(puVar5);
    if (cVar2 == '\0') {
      if (lVar4 != 0) {
        FUN_180217c60(lVar3,local_88,puVar5,0,0,0);
        goto LAB_1800f9e13;
      }
      puVar5 = local_108;
    }
    uVar7 = 0;
LAB_1800f9e0e:
    FUN_180217e70(lVar3,puVar5,uVar7);
  }
  else {
    *(undefined1 *)(lVar3 + 0x138) = 1;
    cVar2 = FUN_1801b6eb0(puVar5);
    if (cVar2 != '\0') {
      uVar7 = 1;
      goto LAB_1800f9e0e;
    }
    if (lVar4 == 0) {
      uVar7 = 1;
      puVar5 = local_108;
      goto LAB_1800f9e0e;
    }
    FUN_180217c60(lVar3,local_88,puVar5,1,0,0);
  }
LAB_1800f9e13:
  FUN_1800133d0(local_108,"./rom/objset/",0x80);
  FUN_1800132f0(local_108,puVar6,0x80);
  lVar1 = lVar3 + 0x98;
  cVar2 = FUN_1801b6eb0(puVar6);
  if (cVar2 == '\0') {
    if (lVar4 != 0) {
      FUN_180217c60(lVar1,local_88,puVar6,1,0,0);
      FUN_18005c6a0(lVar1,0x10);
      FUN_180218110(lVar1,0,FUN_1800f7330,lVar3);
      FUN_180218110(lVar1,1,FUN_1800f7330,lVar3);
      FUN_180218110(lVar1,2,FUN_1800f7390,lVar3);
      goto LAB_1800f9ee1;
    }
    puVar6 = local_108;
  }
  FUN_180217e70(lVar1,puVar6,1);
LAB_1800f9ee1:
  FUN_180218120(lVar1,4);
  *(undefined4 *)(lVar3 + 0x1f0) = 1;
  *(undefined1 *)(lVar3 + 0x90) = 0;
  *(undefined1 *)(lVar3 + 0x128) = 0;
  return 0;
}



// ===================================================
// 1800fa8a0  ->  FUN_1800fa8a0  (entree 1800fa8a0)
// ===================================================

void FUN_1800fa8a0(int *param_1)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  longlong lVar5;
  int *piVar6;
  
  piVar1 = param_1 + 2;
  if (param_1[2] != 0) {
    iVar2 = 0;
    lVar5 = (longlong)param_1[2] + (longlong)param_1;
    if (lVar5 != 0) {
      iVar2 = (int)lVar5 - (int)piVar1;
    }
    *piVar1 = iVar2;
  }
  iVar2 = 0;
  if (0 < *param_1) {
    do {
      lVar5 = 0;
      if (*piVar1 != 0) {
        lVar5 = (longlong)piVar1 + (longlong)*piVar1;
      }
      piVar6 = (int *)(lVar5 + (longlong)iVar2 * 0x24);
      iVar4 = *(int *)(lVar5 + (longlong)iVar2 * 0x24);
      if (iVar4 != 0) {
        iVar3 = 0;
        lVar5 = (longlong)iVar4 + (longlong)param_1;
        if (lVar5 != 0) {
          iVar3 = (int)lVar5 - (int)piVar6;
        }
        *piVar6 = iVar3;
      }
      if (piVar6[2] != 0) {
        iVar4 = 0;
        lVar5 = (longlong)piVar6[2] + (longlong)param_1;
        if (lVar5 != 0) {
          iVar4 = (int)lVar5 - (int)(piVar6 + 2);
        }
        piVar6[2] = iVar4;
      }
      if (piVar6[3] != 0) {
        iVar4 = 0;
        lVar5 = (longlong)piVar6[3] + (longlong)param_1;
        if (lVar5 != 0) {
          iVar4 = (int)lVar5 - (int)(piVar6 + 3);
        }
        piVar6[3] = iVar4;
      }
      if (piVar6[4] != 0) {
        iVar4 = 0;
        lVar5 = (longlong)piVar6[4] + (longlong)param_1;
        if (lVar5 != 0) {
          iVar4 = (int)lVar5 - (int)(piVar6 + 4);
        }
        piVar6[4] = iVar4;
      }
      iVar2 = iVar2 + 1;
    } while (iVar2 < *param_1);
  }
  piVar1 = param_1 + 4;
  if (param_1[4] != 0) {
    iVar2 = 0;
    lVar5 = (longlong)param_1[4] + (longlong)param_1;
    if (lVar5 != 0) {
      iVar2 = (int)lVar5 - (int)piVar1;
    }
    *piVar1 = iVar2;
  }
  iVar2 = 0;
  if (0 < param_1[3]) {
    do {
      lVar5 = 0;
      if (*piVar1 != 0) {
        lVar5 = (longlong)piVar1 + (longlong)*piVar1;
      }
      piVar6 = (int *)((longlong)iVar2 * 8 + 4 + lVar5);
      if (*piVar6 != 0) {
        iVar4 = 0;
        lVar5 = (longlong)*piVar6 + (longlong)param_1;
        if (lVar5 != 0) {
          iVar4 = (int)lVar5 - (int)piVar6;
        }
        *piVar6 = iVar4;
      }
      iVar2 = iVar2 + 1;
    } while (iVar2 < param_1[3]);
  }
  return;
}



