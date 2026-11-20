// ===================================================
// 18007AE10  ->  FUN_18007ae10  (entree 18007ae10)
// ===================================================

void FUN_18007ae10(undefined4 *param_1,int param_2)

{
  undefined4 *puVar1;
  undefined1 auVar2 [16];
  int iVar3;
  undefined8 uVar4;
  longlong lVar5;
  undefined4 *puVar6;
  longlong lVar7;
  undefined4 *puVar8;
  longlong lVar9;
  longlong *plVar10;
  ulonglong uVar11;
  undefined4 *puVar12;
  uint uVar13;
  undefined4 *puVar14;
  
  puVar8 = (undefined4 *)0x0;
  puVar6 = &DAT_1806432e0;
  if (param_2 != DAT_1806432e0) {
    puVar6 = puVar8;
  }
  if (param_2 == DAT_18064330c) {
    puVar6 = &DAT_18064330c;
  }
  else if (puVar6 == (undefined4 *)0x0) {
    return;
  }
  param_1[0x2c58] = puVar6[6];
  param_1[0x2c59] = puVar6[7];
  param_1[2] = puVar6[1];
  param_1[3] = puVar6[2];
  param_1[4] = puVar6[3];
  param_1[6] = puVar6[4];
  param_1[7] = puVar6[5];
  param_1[8] = 0xff000000;
  param_1[9] = puVar6[8];
  *(undefined1 *)(param_1 + 10) = *(undefined1 *)(puVar6 + 9);
  param_1[0xc] = puVar6[10];
  *param_1 = 0x3f800000;
  param_1[0x2c56] = 0;
  *(undefined1 *)(param_1 + 0x2c57) = 0;
  FUN_18010ca20(4,1);
  FUN_18010bdc0(0,&LAB_18007b470,param_1);
  iVar3 = 0xe;
  plVar10 = (longlong *)(param_1 + 0x2c44);
  param_1[0x2c42] = 0xe;
  lVar9 = 2;
  do {
    uVar11 = (ulonglong)iVar3;
    auVar2._8_8_ = 0;
    auVar2._0_8_ = uVar11;
    uVar4 = SUB168(ZEXT816(0x14) * auVar2,0);
    if (SUB168(ZEXT816(0x14) * auVar2,8) != 0) {
      uVar4 = 0xffffffffffffffff;
    }
    lVar5 = FUN_180218930(uVar4);
    if (lVar5 == 0) {
      lVar5 = 0;
    }
    else if (uVar11 != 0) {
      lVar7 = lVar5 + 0x10;
      do {
        *(undefined4 *)(lVar7 + -0x10) = 0xffffffff;
        *(undefined8 *)(lVar7 + -0xc) = 0;
        *(undefined8 *)(lVar7 + -4) = 0;
        lVar7 = lVar7 + 0x14;
        uVar11 = uVar11 - 1;
      } while (uVar11 != 0);
    }
    *plVar10 = lVar5;
    iVar3 = param_1[0x2c42];
    puVar6 = puVar8;
    puVar12 = puVar8;
    puVar14 = puVar8;
    if (0 < iVar3) {
      do {
        *(undefined4 *)((longlong)puVar6 + lVar5) =
             *(undefined4 *)((longlong)&DAT_180350e30 + (longlong)puVar12);
        puVar1 = puVar6 + 5;
        uVar13 = (int)puVar14 + 1;
        *(undefined4 *)((longlong)puVar6 + *plVar10 + 4) =
             *(undefined4 *)((longlong)&DAT_180350e68 + (longlong)puVar12);
        lVar5 = *plVar10;
        *(undefined8 *)(lVar5 + -0xc + (longlong)puVar1) = 0;
        *(undefined4 *)(lVar5 + -4 + (longlong)puVar1) = 0;
        iVar3 = param_1[0x2c42];
        puVar6 = puVar1;
        puVar12 = puVar12 + 1;
        puVar14 = (undefined4 *)(ulonglong)uVar13;
      } while ((int)uVar13 < iVar3);
    }
    plVar10 = plVar10 + 1;
    lVar9 = lVar9 + -1;
  } while (lVar9 != 0);
  *(undefined1 *)(param_1 + 1) = 0;
  param_1[0xb] = 0x3c;
  FUN_18007a4d0(param_1);
  lVar9 = FUN_18006f350();
  if (lVar9 != 0) {
    *(undefined4 *)(lVar9 + 0x328) = 1;
    *(uint *)(lVar9 + 0x32c) = (uint)(param_2 == 4);
  }
  return;
}



