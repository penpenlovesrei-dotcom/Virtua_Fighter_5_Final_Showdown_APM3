// ===================================================
// 82146550  ->  FUN_82146550  (entree 82146550)
// ===================================================

undefined8 FUN_82146550(int param_1)

{
  if (*(int *)(param_1 + 0x100) != -1) {
    FUN_82546a10(*(int *)(param_1 + 0x100),0);
    FUN_8252ea08(*(undefined4 *)(param_1 + 0x100));
    *(undefined4 *)(param_1 + 0x100) = 0xffffffff;
  }
  if (*(int *)(param_1 + 0x234) != 0) {
    FUN_8220cda0(0xf);
    *(undefined4 *)(param_1 + 0x234) = 0;
  }
  if (*(int *)(param_1 + 0xb48) != 0) {
    FUN_82142f48();
    *(undefined4 *)(param_1 + 0xb48) = 0;
  }
  if (*(int *)(param_1 + 0xb4c) != 0) {
    FUN_82142f48();
    *(undefined4 *)(param_1 + 0xb4c) = 0;
  }
  if (*(int *)(param_1 + 0x11c) != 0) {
    FUN_8220cda0(0xf);
    *(undefined4 *)(param_1 + 0x11c) = 0;
  }
  return 1;
}



// ===================================================
// 82146B80  ->  FUN_82146b80  (entree 82146b80)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

undefined8 FUN_82146b80(int param_1)

{
  undefined4 uVar1;
  int iVar3;
  undefined8 uVar2;
  
  uVar1 = DAT_8264089c;
  *(undefined8 *)(param_1 + 0x68) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x78) = 0;
  *(undefined4 *)(param_1 + 0x80) = 0;
  FUN_8252e5f8(uVar1,0x800a,1);
  iVar3 = FUN_82546870(0x706,uVar1,1,0,param_1 + 0xf8,param_1 + 0xb8,(undefined8 *)(param_1 + 0x68),
                       param_1 + 0x100);
  if ((iVar3 == 0) || (uVar2 = 0, iVar3 == 0x3e5)) {
    uVar2 = 1;
  }
  return uVar2;
}



// ===================================================
// 82146C08  ->  FUN_82146c08  (entree 82146c08)
// ===================================================

undefined8 FUN_82146c08(int param_1)

{
  int iVar2;
  undefined8 uVar1;
  
  *(undefined8 *)(param_1 + 0x68) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x78) = 0;
  *(undefined4 *)(param_1 + 0x80) = 0;
  iVar2 = FUN_82546b68(*(undefined4 *)(param_1 + 0x100),*(undefined4 *)(param_1 + 0x84),
                       param_1 + 0x88,param_1 + 0xa8);
  if ((iVar2 == 0) || (uVar1 = 0, iVar2 == 0x3e5)) {
    uVar1 = 1;
  }
  return uVar1;
}



// ===================================================
// 82146C70  ->  FUN_82146c70  (entree 82146c70)
// ===================================================

undefined8 FUN_82146c70(int param_1)

{
  int iVar2;
  undefined8 uVar1;
  
  *(undefined8 *)(param_1 + 0x68) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x78) = 0;
  *(undefined4 *)(param_1 + 0x80) = 0;
  iVar2 = FUN_82546e38(*(undefined4 *)(param_1 + 0x100),0);
  if ((iVar2 == 0) || (uVar1 = 0, iVar2 == 0x3e5)) {
    uVar1 = 1;
  }
  return uVar1;
}



// ===================================================
// 82146CD0  ->  FUN_82146cd0  (entree 82146cd0)
// ===================================================

undefined8 FUN_82146cd0(int param_1)

{
  int iVar2;
  undefined8 uVar1;
  
  if (*(int *)(param_1 + 0x100) == -1) {
    return 0;
  }
  *(undefined8 *)(param_1 + 0x68) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x78) = 0;
  *(undefined4 *)(param_1 + 0x80) = 0;
  iVar2 = FUN_82546ed0(*(undefined4 *)(param_1 + 0x100));
  if ((iVar2 == 0) || (uVar1 = 0, iVar2 == 0x3e5)) {
    uVar1 = 1;
  }
  return uVar1;
}



// ===================================================
// 82146D50  ->  FUN_82146d50  (entree 82146d50)
// ===================================================

undefined8 FUN_82146d50(int param_1)

{
  int iVar2;
  undefined8 uVar1;
  
  if (*(int *)(param_1 + 0x100) == -1) {
    return 0;
  }
  *(undefined8 *)(param_1 + 0x68) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x78) = 0;
  *(undefined4 *)(param_1 + 0x80) = 0;
  iVar2 = FUN_82546cb8(*(undefined4 *)(param_1 + 0x100),*(undefined4 *)(param_1 + 0x84),
                       param_1 + 0x88);
  if ((iVar2 == 0) || (uVar1 = 0, iVar2 == 0x3e5)) {
    uVar1 = 1;
  }
  return uVar1;
}



// ===================================================
// 82146DD8  ->  FUN_82146dd8  (entree 82146dd8)
// ===================================================

undefined8 FUN_82146dd8(int param_1)

{
  int iVar2;
  undefined8 uVar1;
  
  if (*(int *)(param_1 + 0x100) == -1) {
    return 0;
  }
  *(undefined8 *)(param_1 + 0x68) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x78) = 0;
  *(undefined4 *)(param_1 + 0x80) = 0;
  iVar2 = FUN_82546a10(*(undefined4 *)(param_1 + 0x100));
  if ((iVar2 == 0) || (uVar1 = 0, iVar2 == 0x3e5)) {
    uVar1 = 1;
  }
  return uVar1;
}



// ===================================================
// 82146E58  ->  FUN_82146e58  (entree 82146e58)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_82146e58(int param_1)

{
  undefined4 uVar1;
  uint uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 *puVar5;
  
  iVar3 = *(int *)(param_1 + 0x110);
  *(uint *)(param_1 + 0x1e0) = *(uint *)(param_1 + 0x10c);
  *(int *)(param_1 + 0x1c8) = iVar3;
  *(undefined4 *)(param_1 + 0x1a0) = 0x20000003;
  *(undefined1 **)(param_1 + 0x1d0) = &DAT_10000002;
  *(undefined4 *)(param_1 + 0x200) = 0;
  *(undefined1 *)(param_1 + 0x1a8) = 2;
  *(undefined4 *)(param_1 + 0x1b8) = 0;
  *(undefined1 *)(param_1 + 0x1c0) = 0;
  *(undefined1 *)(param_1 + 0x1d8) = 1;
  *(undefined4 *)(param_1 + 0x1e8) = 0x10008011;
  *(ulonglong *)(param_1 + 0x1b0) = -(ulonglong)*(uint *)(param_1 + 0x10c);
  if ((*(uint *)(param_1 + 0x118) & 2) == 0) {
    uVar1 = 0;
  }
  else {
    uVar1 = *(undefined4 *)(param_1 + 0x120);
  }
  *(undefined4 *)(param_1 + 0x1f8) = uVar1;
  *(undefined1 *)(param_1 + 0x1f0) = 1;
  if (*(int *)(param_1 + 0x104) == 0) {
    *(undefined1 *)(param_1 + 0x160) = 2;
    *(undefined4 *)(param_1 + 0x170) = 0;
    *(int *)(param_1 + 0x180) = iVar3;
    *(undefined1 *)(param_1 + 0x178) = 0;
    *(ulonglong *)(param_1 + 0x168) = (ulonglong)*(uint *)(param_1 + 0x108);
    *(undefined4 *)(param_1 + 0x188) = 0x10008011;
    *(undefined4 *)(param_1 + 0x158) = 0x20000001;
    if ((*(uint *)(param_1 + 0x118) & 1) == 0) {
      uVar1 = 0;
    }
    else {
      uVar1 = *(undefined4 *)(param_1 + 0x120);
    }
    *(undefined4 *)(param_1 + 0x198) = uVar1;
    *(undefined1 *)(param_1 + 400) = 1;
    *(undefined4 *)(param_1 + 0x128) =
         *(undefined4 *)(&DAT_82000b20 + (*(int *)(param_1 + 0x114) * 0x13 + iVar3) * 8);
    *(undefined4 *)((*(int *)(param_1 + 0x200) + 0x19) * 0xc + param_1) = 3;
    *(int *)(*(int *)(param_1 + 0x200) * 0xc + param_1 + 0x130) = param_1 + 0x158;
    iVar3 = *(int *)(param_1 + 0x200) + 1;
    *(int *)(param_1 + 0x200) = iVar3;
    *(undefined4 *)(iVar3 * 0xc + param_1 + 0x128) =
         *(undefined4 *)(&DAT_82000bb0 + *(int *)(param_1 + 0x114) * 0x98);
    *(undefined4 *)((*(int *)(param_1 + 0x200) + 0x19) * 0xc + param_1) = 3;
    *(int *)(*(int *)(param_1 + 0x200) * 0xc + param_1 + 0x130) = param_1 + 0x158;
    iVar3 = *(int *)(param_1 + 0x200) + 1;
    *(int *)(param_1 + 0x200) = iVar3;
    *(undefined4 *)(iVar3 * 0xc + param_1 + 0x128) =
         *(undefined4 *)
          (&DAT_82000b24 + (*(int *)(param_1 + 0x114) * 0x13 + *(int *)(param_1 + 0x110)) * 8);
    *(undefined4 *)((*(int *)(param_1 + 0x200) + 0x19) * 0xc + param_1) = 4;
    *(int *)(*(int *)(param_1 + 0x200) * 0xc + param_1 + 0x130) = param_1 + 0x1a0;
    iVar3 = *(int *)(param_1 + 0x200) + 1;
    *(int *)(param_1 + 0x200) = iVar3;
    *(undefined4 *)(iVar3 * 0xc + param_1 + 0x128) =
         *(undefined4 *)(&DAT_82000bb4 + *(int *)(param_1 + 0x114) * 0x98);
  }
  else {
    if (*(int *)(param_1 + 0x104) != 1) goto LAB_821470f0;
    *(undefined4 *)(param_1 + 0x128) = *(undefined4 *)(&DAT_82000ce8 + iVar3 * 4);
  }
  *(undefined4 *)((*(int *)(param_1 + 0x200) + 0x19) * 0xc + param_1) = 4;
  *(int *)(*(int *)(param_1 + 0x200) * 0xc + param_1 + 0x130) = param_1 + 0x1a0;
  *(int *)(param_1 + 0x200) = *(int *)(param_1 + 0x200) + 1;
LAB_821470f0:
  uVar2 = 0;
  if (*(int *)(param_1 + 0x200) != 0) {
    puVar5 = (undefined4 *)(param_1 + 0x92c);
    puVar4 = (undefined4 *)(param_1 + 0x128);
    do {
      uVar1 = *puVar4;
      uVar2 = uVar2 + 1;
      *puVar5 = 1;
      puVar4 = puVar4 + 3;
      *(undefined2 *)(puVar5 + 1) = 1;
      puVar5[-1] = uVar1;
      puVar5 = puVar5 + 0x22;
    } while (uVar2 < *(uint *)(param_1 + 0x200));
  }
  return;
}



// ===================================================
// 82147138  ->  FUN_82147138  (entree 82147138)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

undefined8 FUN_82147138(int param_1)

{
  int iVar1;
  int iVar2;
  longlong *plVar3;
  int *piVar4;
  int *piVar5;
  int *piVar6;
  uint uVar7;
  int *piVar8;
  int *piVar9;
  int *piVar10;
  int *piVar11;
  int *piVar12;
  undefined4 *puVar13;
  int *piVar14;
  uint uVar15;
  int iVar16;
  int iVar17;
  int aiStack_70 [28];
  
  iVar17 = 0;
  if (*(int *)(param_1 + 0xb48) != 0) {
    piVar14 = (int *)(param_1 + 0x128);
    FUN_825ffd30(aiStack_70,piVar14,0x30);
    uVar15 = 0;
    if (*(int *)(param_1 + 0x200) != 0) {
      piVar8 = aiStack_70;
      piVar9 = (int *)(param_1 + 0x130);
      piVar11 = (int *)(param_1 + 300);
      iVar16 = iVar17;
      piVar10 = piVar14;
      do {
        iVar1 = *piVar8;
        uVar7 = 0;
        iVar2 = piVar8[2];
        *piVar11 = piVar8[1];
        *piVar10 = iVar1;
        *piVar9 = iVar2;
        iVar17 = iVar16 + 1;
        piVar4 = piVar11 + 3;
        piVar5 = piVar9 + 3;
        piVar6 = piVar10 + 3;
        if (**(int **)(param_1 + 0xb48) != 0) {
          piVar12 = (int *)(*(int **)(param_1 + 0xb48))[1];
          do {
            if ((((iVar1 == *piVar12) && (*(char *)(iVar2 + 8) == '\x02')) && (piVar12[2] == 1)) &&
               (((plVar3 = (longlong *)piVar12[3], *plVar3 == *(longlong *)(param_1 + 0x60) &&
                 (*(int *)(plVar3 + 1) != 0)) &&
                (iVar17 = iVar16, piVar4 = piVar11, piVar5 = piVar9, piVar6 = piVar10,
                *(longlong *)(iVar2 + 0x10) <= plVar3[2])))) break;
            uVar7 = uVar7 + 1;
            piVar12 = piVar12 + 4;
            iVar17 = iVar16 + 1;
            piVar4 = piVar11 + 3;
            piVar5 = piVar9 + 3;
            piVar6 = piVar10 + 3;
          } while (uVar7 < **(uint **)(param_1 + 0xb48));
        }
        piVar10 = piVar6;
        piVar9 = piVar5;
        piVar11 = piVar4;
        uVar15 = uVar15 + 1;
        piVar8 = piVar8 + 3;
        iVar16 = iVar17;
      } while (uVar15 < *(uint *)(param_1 + 0x200));
    }
    *(int *)(param_1 + 0x200) = iVar17;
    if (iVar17 != 0) {
      uVar15 = 0;
      puVar13 = (undefined4 *)(param_1 + 0x92c);
      do {
        iVar17 = *piVar14;
        uVar15 = uVar15 + 1;
        *puVar13 = 1;
        piVar14 = piVar14 + 3;
        *(undefined2 *)(puVar13 + 1) = 1;
        puVar13[-1] = iVar17;
        puVar13 = puVar13 + 0x22;
      } while (uVar15 < *(uint *)(param_1 + 0x200));
      return 1;
    }
  }
  return 0;
}



// ===================================================
// 821472C0  ->  FUN_821472c0  (entree 821472c0)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

bool FUN_821472c0(int param_1)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int *piVar5;
  int iVar6;
  int iVar7;
  
  iVar1 = *(int *)(param_1 + 0x200);
  iVar6 = 0;
  if (iVar1 != 0) {
    iVar2 = **(int **)(param_1 + 0xb48);
    iVar6 = 0;
    iVar3 = param_1;
    iVar7 = iVar1;
    do {
      if (iVar2 != 0) {
        piVar5 = (int *)(*(int **)(param_1 + 0xb48))[1];
        iVar4 = iVar2;
        do {
          if ((((*(int *)(iVar3 + 0x128) == *piVar5) &&
               (*(char *)(*(int *)(iVar3 + 0x130) + 8) == '\x02')) && (piVar5[2] == 1)) &&
             ((*(longlong *)piVar5[3] == *(longlong *)(param_1 + 0x60) &&
              (*(longlong *)(*(int *)(iVar3 + 0x130) + 0x10) == ((longlong *)piVar5[3])[2])))) {
            iVar6 = iVar6 + 1;
          }
          iVar4 = iVar4 + -1;
          piVar5 = piVar5 + 4;
        } while (iVar4 != 0);
      }
      iVar7 = iVar7 + -1;
      iVar3 = iVar3 + 0xc;
    } while (iVar7 != 0);
  }
  return iVar1 == iVar6;
}



// ===================================================
// 82147380  ->  FUN_82147380  (entree 82147380)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82147380(int param_1)

{
  int iVar2;
  undefined8 uVar1;
  uint uVar3;
  int *piVar4;
  longlong lVar5;
  
  uVar3 = 0;
  if (*(int *)(param_1 + 0x200) != 0) {
    piVar4 = (int *)(param_1 + 0x130);
    do {
      if (*(char *)(*piVar4 + 8) != '\x02') {
        return 0;
      }
      uVar3 = uVar3 + 1;
      piVar4[0x35] = piVar4[-2];
      *(undefined8 *)(piVar4 + 0x36) = *(undefined8 *)(*piVar4 + 0x10);
      piVar4 = piVar4 + 3;
    } while (uVar3 < *(uint *)(param_1 + 0x200));
  }
  lVar5 = ((ulonglong)*(uint *)(param_1 + 0x200) + 2 & 0x3fffffff) << 2;
  if (*(int *)(param_1 + 0x234) != 0) {
    FUN_8220cda0(0xf);
  }
  iVar2 = FUN_8220cf50(0xf,lVar5,0xffffffff82000e60);
  *(int *)(param_1 + 0x234) = iVar2;
  if (iVar2 == 0) {
    return 0;
  }
  *(undefined8 *)(param_1 + 0x68) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x78) = 0;
  *(undefined4 *)(param_1 + 0x80) = 0;
  iVar2 = FUN_825478e8(*(undefined4 *)(param_1 + 0x200),param_1 + 0x204,lVar5,
                       *(undefined4 *)(param_1 + 0x234));
  if ((iVar2 == 0) || (uVar1 = 0, iVar2 == 0x3e5)) {
    uVar1 = 1;
  }
  return uVar1;
}



// ===================================================
// 82147470  ->  FUN_82147470  (entree 82147470)
// ===================================================

void FUN_82147470(int param_1)

{
  int iVar1;
  bool bVar2;
  uint uVar3;
  int iVar4;
  int *piVar5;
  
  bVar2 = false;
  if ((*(int **)(param_1 + 0x234) != (int *)0x0) && (*(int *)(param_1 + 0x120) != 0)) {
    iVar4 = *(int *)(param_1 + 0x200);
    if (iVar4 == **(int **)(param_1 + 0x234)) {
      uVar3 = 0;
      if (iVar4 != 0) {
        iVar4 = 0;
        piVar5 = (int *)(param_1 + 0x130);
        do {
          if (*(uint *)(*(int *)(*(int *)(param_1 + 0x234) + 4) + iVar4) < 0x65) {
            bVar2 = true;
          }
          else {
            iVar1 = piVar5[-1] * 0x18 + *piVar5;
            if (*(int *)(iVar1 + -0x18) == 0x10008011) {
              *(undefined4 *)(iVar1 + -8) = 0;
            }
          }
          uVar3 = uVar3 + 1;
          iVar4 = iVar4 + 4;
          piVar5 = piVar5 + 3;
        } while (uVar3 < *(uint *)(param_1 + 0x200));
      }
    }
    else {
      uVar3 = 0;
      if (iVar4 != 0) {
        piVar5 = (int *)(param_1 + 0x130);
        do {
          iVar4 = piVar5[-1] * 0x18 + *piVar5;
          if (*(int *)(iVar4 + -0x18) == 0x10008011) {
            *(undefined4 *)(iVar4 + -8) = 0;
          }
          uVar3 = uVar3 + 1;
          piVar5 = piVar5 + 3;
        } while (uVar3 < *(uint *)(param_1 + 0x200));
      }
    }
  }
  if (!bVar2) {
    *(undefined4 *)(param_1 + 0x120) = 0;
  }
  return;
}



// ===================================================
// 82147590  ->  FUN_82147590  (entree 82147590)
// ===================================================

undefined8 FUN_82147590(int param_1)

{
  int iVar2;
  undefined8 uVar1;
  
  if (*(int *)(param_1 + 0x100) == -1) {
    return 0;
  }
  *(undefined8 *)(param_1 + 0x68) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x78) = 0;
  *(undefined4 *)(param_1 + 0x80) = 0;
  iVar2 = FUN_82547150(*(undefined4 *)(param_1 + 0x100),*(undefined8 *)(param_1 + 0x60),
                       *(undefined4 *)(param_1 + 0x200),param_1 + 0x128);
  if ((iVar2 == 0) || (uVar1 = 0, iVar2 == 0x3e5)) {
    uVar1 = 1;
  }
  return uVar1;
}



// ===================================================
// 82147620  ->  FUN_82147620  (entree 82147620)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82147620(int param_1)

{
  uint uVar1;
  int iVar2;
  ulonglong uVar3;
  undefined4 uStack_30;
  undefined4 auStack_2c [11];
  
  if ((*(int *)(param_1 + 0x120) == 0) || (*(int *)(param_1 + 0x11c) == 0)) {
    return 0;
  }
  uVar1 = *(uint *)(param_1 + 0x124);
  uVar3 = (ulonglong)uVar1;
  if (*(uint *)(param_1 + 0x200) <= uVar3) {
    return 0;
  }
  iVar2 = *(int *)((int)((uVar3 + 0x19 + (uVar3 + 0x19 & 0x7fffffff) * 2 & 0xffffffff) << 2) +
                  param_1) * 0x18 +
          *(int *)((int)((uVar3 + ((ulonglong)uVar1 & 0x7fffffff) * 2 & 0xffffffff) << 2) + param_1
                  + 0x130);
  if ((*(int *)(iVar2 + -0x18) == 0x10008011) && (*(int *)(iVar2 + -8) != 0)) {
    uVar3 = (ulonglong)*(uint *)(param_1 + 0xb4c);
    uStack_30 = 0;
    if (uVar3 == 0) {
      uVar3 = FUN_82142ee0(0x400);
      *(int *)(param_1 + 0xb4c) = (int)uVar3;
      if ((uVar3 & 0xffffffff) == 0) {
        return 0;
      }
    }
    auStack_2c[0] = 0x400;
    uStack_30 = *(undefined4 *)(*(int *)(param_1 + 0x124) * 0xc + param_1 + 0x128);
    iVar2 = FUN_82547ac8(DAT_8264089c,1,&uStack_30,4,0xffffffff82000e64,uVar3,auStack_2c);
    if (iVar2 != 0) {
      return 0;
    }
    *(undefined8 *)(param_1 + 0x68) = 0;
    *(undefined8 *)(param_1 + 0x70) = 0;
    *(undefined8 *)(param_1 + 0x78) = 0;
    *(undefined4 *)(param_1 + 0x80) = 0;
    iVar2 = FUN_82547650(DAT_8264089c,*(undefined4 *)(param_1 + 0xb4c),
                         *(undefined4 *)(param_1 + 0x120),*(undefined4 *)(param_1 + 0x11c));
    *(int *)(param_1 + 0x124) = *(int *)(param_1 + 0x124) + 1;
    if (iVar2 != 0) {
      if (iVar2 != 0x3e5) {
        return 0;
      }
      return 1;
    }
  }
  else {
    *(uint *)(param_1 + 0x124) = uVar1 + 1;
  }
  return 1;
}



// ===================================================
// 821477A0  ->  FUN_821477a0  (entree 821477a0)
// ===================================================

undefined8 FUN_821477a0(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  ulonglong uVar3;
  undefined4 uStack_20;
  undefined4 uStack_1c;
  
  if ((*(int *)(param_1 + 0xb5c) != 0) && (*(int *)(param_1 + 0xb58) != 0)) {
    uVar3 = (ulonglong)*(uint *)(param_1 + 0xb4c);
    uStack_20 = 0;
    if (uVar3 == 0) {
      uVar3 = FUN_82142ee0(0x400);
      *(int *)(param_1 + 0xb4c) = (int)uVar3;
      if ((uVar3 & 0xffffffff) == 0) {
        return 0;
      }
    }
    uStack_20 = *(undefined4 *)(param_1 + 0x928);
    uStack_1c = 0x400;
    iVar1 = FUN_82547b80(*(undefined8 *)(param_1 + 0xb50),1,&uStack_20,4,0xffffffff82000e64,uVar3,
                         &uStack_1c);
    if (iVar1 == 0) {
      if (*(int *)(param_1 + 0x11c) != 0) {
        FUN_8220cda0(0xf);
        *(undefined4 *)(param_1 + 0x11c) = 0;
      }
      *(undefined4 *)(param_1 + 0x120) = *(undefined4 *)(param_1 + 0xb5c);
      uVar2 = FUN_8220cf50(0xf,*(undefined4 *)(param_1 + 0xb5c),0xffffffff82000e68);
      *(undefined4 *)(param_1 + 0x11c) = uVar2;
      *(undefined8 *)(param_1 + 0x68) = 0;
      *(undefined8 *)(param_1 + 0x70) = 0;
      *(undefined8 *)(param_1 + 0x78) = 0;
      *(undefined4 *)(param_1 + 0x80) = 0;
      iVar1 = FUN_82547370(DAT_8264089c,*(undefined4 *)(param_1 + 0xb4c),
                           *(undefined4 *)(param_1 + 0x120),*(undefined4 *)(param_1 + 0x11c),0x14,
                           param_1 + 0xb60);
      if ((iVar1 != 0) && (iVar1 != 0x3e5)) {
        return 0;
      }
      return 1;
    }
  }
  return 0;
}



// ===================================================
// 821478D8  ->  FUN_821478d8  (entree 821478d8)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

bool FUN_821478d8(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 auStack_30 [12];
  
  if (*(int *)(param_1 + 0xb48) != 0) {
    FUN_82142f48();
    *(undefined4 *)(param_1 + 0xb48) = 0;
  }
  auStack_30[0] = 0;
  iVar1 = FUN_8252e750(0,*(undefined4 *)(param_1 + 0x84),param_1 + 0x88,
                       *(undefined4 *)(param_1 + 0x200),param_1 + 0x928,auStack_30,0,0);
  if (iVar1 != 0x7a) {
    return false;
  }
  uVar2 = FUN_82142ee0(auStack_30[0]);
  *(undefined4 *)(param_1 + 0xb48) = uVar2;
  *(undefined8 *)(param_1 + 0x68) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x78) = 0;
  *(undefined4 *)(param_1 + 0x80) = 0;
  iVar1 = FUN_8252e750(0,*(undefined4 *)(param_1 + 0x84),param_1 + 0x88,
                       *(undefined4 *)(param_1 + 0x200),param_1 + 0x928,auStack_30,
                       *(undefined4 *)(param_1 + 0xb48));
  return iVar1 == 0x3e5;
}



// ===================================================
// 82147998  ->  FUN_82147998  (entree 82147998)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82147998(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  undefined4 auStack_30 [12];
  
  if (*(int *)(param_1 + 0xb48) != 0) {
    FUN_82142f48();
    *(undefined4 *)(param_1 + 0xb48) = 0;
  }
  puVar3 = (undefined4 *)(param_1 + 0x924);
  auStack_30[0] = 0;
  if (*(int *)(param_1 + 0x4c) == 0xb) {
    iVar1 = FUN_8252e898(0,*(undefined8 *)(param_1 + 0x60));
  }
  else {
    iVar1 = FUN_8252e838(0,*(undefined4 *)(param_1 + 0x920),0x13,1,param_1 + 0x928,auStack_30,puVar3
                        );
  }
  if (iVar1 != 0) {
    return 0;
  }
  uVar2 = FUN_82142ee0(auStack_30[0]);
  *(undefined4 *)(param_1 + 0xb48) = uVar2;
  *(undefined8 *)(param_1 + 0x68) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x78) = 0;
  *(undefined4 *)(param_1 + 0x80) = 0;
  iVar1 = FUN_82530098(*puVar3,*(undefined4 *)(param_1 + 0xb48),auStack_30[0],0);
  if (iVar1 != 0x3e5) {
    FUN_8252ea08(*puVar3);
    *puVar3 = 0xffffffff;
    return 0;
  }
  return 1;
}



// ===================================================
// 82147A78  ->  FUN_82147a78  (entree 82147a78)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

void FUN_82147a78(int param_1,int *param_2,undefined8 *param_3)

{
  short sVar1;
  uint uVar2;
  undefined4 uVar3;
  int iVar4;
  uint uVar5;
  uint *puVar6;
  undefined2 *puVar7;
  short *psVar8;
  uint *puVar9;
  longlong lVar10;
  int aiStack_40 [2];
  undefined8 auStack_38 [7];
  
  if ((param_2 != (int *)0x0) && (param_3 != (undefined8 *)0x0)) {
    puVar9 = (uint *)(param_2 + 10);
    lVar10 = 0xb;
    puVar6 = puVar9;
    do {
      *puVar6 = 0;
      puVar6 = puVar6 + 1;
      lVar10 = lVar10 + -1;
    } while (lVar10 != 0);
    *param_2 = *(int *)(param_3 + 1);
    *(undefined8 *)(param_2 + 2) = *param_3;
    FUN_822c4ba0(param_2 + 4,param_3 + 3,0x10);
    uVar5 = 0;
    if (*(int *)(param_1 + 0x104) == 2) {
      *(undefined8 *)(param_2 + 8) = param_3[2];
      if (*(int *)(param_3 + 5) != 0) {
        iVar4 = 0;
        do {
          puVar7 = (undefined2 *)(iVar4 + *(int *)((int)param_3 + 0x2c));
          switch(*puVar7) {
          case 1:
            param_2[0xc] = *(int *)(puVar7 + 8);
            break;
          case 2:
            param_2[0xd] = *(int *)(puVar7 + 8);
            break;
          case 3:
            param_2[0xe] = *(int *)(puVar7 + 8);
            break;
          case 4:
            param_2[0xf] = *(int *)(puVar7 + 8);
            break;
          case 5:
            param_2[0x10] = *(int *)(puVar7 + 8);
            break;
          case 6:
            param_2[0x11] = *(int *)(puVar7 + 8);
            break;
          case 7:
            param_2[0x12] = *(int *)(puVar7 + 8);
            break;
          case 8:
            param_2[0x13] = *(int *)(puVar7 + 8);
            break;
          case 9:
            uVar2 = *(uint *)(puVar7 + 8);
            *puVar9 = uVar2;
            if (0x10 < uVar2) {
              *puVar9 = 0x14;
            }
            break;
          case 10:
            param_2[0x14] = *(int *)(puVar7 + 8);
          }
          uVar5 = uVar5 + 1;
          iVar4 = iVar4 + 0x18;
        } while (uVar5 < *(uint *)(param_3 + 5));
      }
    }
    else if (*(int *)(param_1 + 0x92c) == 2) {
      *(undefined8 *)(param_2 + 8) = param_3[2];
      if (*(int *)(param_3 + 5) != 0) {
        iVar4 = 0;
        do {
          psVar8 = (short *)(iVar4 + *(int *)((int)param_3 + 0x2c));
          if (*psVar8 == 1) {
            uVar2 = *(uint *)(psVar8 + 8);
            *puVar9 = uVar2;
            if (0x10 < uVar2) {
              *puVar9 = 0x14;
            }
          }
          else if (*psVar8 == -6) {
            param_2[0xb] = *(int *)(psVar8 + 8);
          }
          uVar5 = uVar5 + 1;
          iVar4 = iVar4 + 0x18;
        } while (uVar5 < *(uint *)(param_3 + 5));
      }
    }
    else if (*(int *)(param_3 + 5) != 0) {
      iVar4 = 0;
      do {
        psVar8 = (short *)(iVar4 + *(int *)((int)param_3 + 0x2c));
        sVar1 = *psVar8;
        if (sVar1 == 1) {
          uVar2 = *(uint *)(psVar8 + 8);
          *puVar9 = uVar2;
          if (0x10 < uVar2) {
            *puVar9 = 0x14;
          }
        }
        else if (sVar1 == 2) {
          *(longlong *)(param_2 + 8) = (longlong)*(int *)(psVar8 + 8);
        }
        else if (sVar1 == -6) {
          param_2[0xb] = *(int *)(psVar8 + 8);
        }
        uVar5 = uVar5 + 1;
        iVar4 = iVar4 + 0x18;
      } while (uVar5 < *(uint *)(param_3 + 5));
    }
    if (100 < *param_2) {
      param_2[0xb] = 0;
    }
    uVar3 = DAT_8264089c;
    if (((param_2[0xb] != 0) && (*(longlong *)(param_2 + 2) != *(longlong *)(param_1 + 0x60))) &&
       (iVar4 = FUN_82140470(DAT_8264089c,0xf7), iVar4 == 0)) {
      iVar4 = FUN_82140470(uVar3,0xf6);
      if (iVar4 != 0) {
        auStack_38[0] = *(undefined8 *)(param_2 + 2);
        iVar4 = FUN_8252e6b8(uVar3,auStack_38,1,aiStack_40,0);
        if ((iVar4 == 0) && (aiStack_40[0] != 0)) {
          return;
        }
      }
      param_2[0xb] = 0;
    }
  }
  return;
}



// ===================================================
// 82147D98  ->  FUN_82147d98  (entree 82147d98)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_82147d98(int param_1)

{
  int *piVar1;
  int iVar2;
  uint uVar3;
  longlong *plVar4;
  int iVar5;
  
  piVar1 = *(int **)(param_1 + 0xb48);
  if (((piVar1 != (int *)0x0) && (*piVar1 == 1)) &&
     (piVar1 = (int *)piVar1[1], *(int *)(param_1 + 0x928) == *piVar1)) {
    uVar3 = 0;
    iVar2 = *(int *)(param_1 + 0x23c);
    *(int *)(param_1 + 0x238) = piVar1[1];
    if (piVar1[2] != 0) {
      iVar5 = 0;
      plVar4 = (longlong *)(param_1 + 0x248);
      do {
        if (*(int *)(piVar1[3] + iVar5 + 8) == 1) {
          FUN_82147a78(param_1,param_1 + 0x8c8);
        }
        if ((iVar2 == -1) &&
           (FUN_82147a78(param_1,plVar4 + -1,piVar1[3] + iVar5),
           *(longlong *)(param_1 + 0x60) == *plVar4)) {
          *(uint *)(param_1 + 0x23c) = uVar3;
        }
        uVar3 = uVar3 + 1;
        iVar5 = iVar5 + 0x30;
        plVar4 = plVar4 + 0xb;
      } while (uVar3 < (uint)piVar1[2]);
    }
  }
  return;
}



// ===================================================
// 82149B70  ->  FUN_82149b70  (entree 82149b70)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82149b70(int param_1)

{
  char cVar2;
  int iVar1;
  ulonglong uVar3;
  ulonglong uVar4;
  
  *(undefined4 *)(param_1 + 0x100) = 0xffffffff;
  *(undefined4 *)(param_1 + 0x924) = 0xffffffff;
  *(undefined8 *)(param_1 + 0x68) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x78) = 0;
  *(undefined4 *)(param_1 + 0x80) = 0;
  uVar3 = (ulonglong)DAT_8264089c;
  uVar4 = 0xffffffffffffffff;
  if (uVar3 < 4) {
    uVar4 = uVar3;
  }
  cVar2 = FUN_82144cb0(uVar4);
  if (cVar2 != '\0') {
    iVar1 = FUN_8252e8f8(uVar3,(undefined8 *)(param_1 + 0x60));
    if (iVar1 == 0) {
      *(undefined4 *)(param_1 + 0x84) = 0;
      *(undefined8 *)(param_1 + 0x88) = *(undefined8 *)(param_1 + 0x60);
      *(undefined4 *)((*(int *)(param_1 + 0x84) + 0x2a) * 4 + param_1) = 0;
      *(undefined1 *)(param_1 + 0x54) = 0;
      *(undefined1 *)(param_1 + 0x55) = 0;
      *(undefined4 *)(param_1 + 0x5c) = 0;
      *(undefined4 *)(param_1 + 0x58) = 0;
      *(int *)(param_1 + 0x84) = *(int *)(param_1 + 0x84) + 1;
      if (*(int *)(param_1 + 0x234) != 0) {
        FUN_8220cda0(0xf);
        *(undefined4 *)(param_1 + 0x234) = 0;
      }
      if (*(int *)(param_1 + 0xb48) != 0) {
        FUN_82142f48();
        *(undefined4 *)(param_1 + 0xb48) = 0;
      }
      if (*(int *)(param_1 + 0xb4c) != 0) {
        FUN_82142f48();
        *(undefined4 *)(param_1 + 0xb4c) = 0;
      }
      if (*(int *)(param_1 + 0x4c) == 0) {
        FUN_82146e58(param_1);
        *(undefined4 *)(param_1 + 0x124) = 0;
        *(undefined4 *)(param_1 + 0x50) = 0xe;
        return 1;
      }
      FUN_821448e0(param_1 + 0x238);
      *(undefined4 *)(param_1 + 0x50) = 0xe;
      return 1;
    }
  }
  *(undefined1 *)(param_1 + 0x55) = 0;
  FUN_822c7d50(param_1);
  return 1;
}



// ===================================================
// 82149CB8  ->  FUN_82149cb8  (entree 82149cb8)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

undefined8 FUN_82149cb8(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  char cVar3;
  ulonglong uVar4;
  ulonglong uVar5;
  ulonglong uVar6;
  undefined8 uVar7;
  
  uVar7 = 0;
  if (*(char *)(param_1 + 0x54) == '\0') {
    uVar4 = (ulonglong)*(uint *)(param_1 + 0x58) + 1;
    uVar5 = (ulonglong)*(uint *)(param_1 + 0x5c) + 1;
    *(int *)(param_1 + 0x58) = (int)uVar4;
    *(int *)(param_1 + 0x5c) = (int)uVar5;
    uVar6 = (ulonglong)DAT_8264089c;
    if (3 < uVar6) {
      uVar6 = 0xffffffffffffffff;
    }
    cVar3 = FUN_82144cb0(uVar6);
    if ((cVar3 == '\0') || (cVar3 = FUN_82144d78(), cVar3 == '\0')) {
      *(undefined4 *)(param_1 + 0x4c) = 0xe;
    }
    switch(*(undefined4 *)(param_1 + 0x4c)) {
    case 0:
      cVar3 = FUN_821478d8(param_1);
      if (cVar3 != '\0') {
        *(undefined1 *)(param_1 + 0x54) = 1;
        *(undefined4 *)(param_1 + 0x50) = 1;
        return 0;
      }
      break;
    case 1:
      cVar3 = FUN_82146b80(param_1);
      if (cVar3 != '\0') {
        *(undefined1 *)(param_1 + 0x54) = 1;
        *(undefined4 *)(param_1 + 0x50) = 2;
        return 0;
      }
      break;
    case 2:
      cVar3 = FUN_82146c08(param_1);
      if (cVar3 != '\0') {
        *(undefined1 *)(param_1 + 0x54) = 1;
        *(undefined4 *)(param_1 + 0x50) = 3;
        return 0;
      }
      break;
    case 3:
      cVar3 = FUN_82146c70(param_1);
      if (cVar3 != '\0') {
        *(undefined1 *)(param_1 + 0x54) = 1;
        *(uint *)(param_1 + 0x50) = (-(uint)(*(int *)(param_1 + 0x120) != 0) & 0xfffffffe) + 6;
        return 0;
      }
      break;
    case 4:
      cVar3 = FUN_82147380(param_1);
      if (cVar3 != '\0') {
        *(undefined1 *)(param_1 + 0x54) = 1;
        *(undefined4 *)(param_1 + 0x50) = 6;
        return 0;
      }
      break;
    case 5:
      cVar3 = FUN_82147620(param_1);
      if (cVar3 != '\0') {
        *(undefined1 *)(param_1 + 0x54) = 1;
        *(uint *)(param_1 + 0x50) =
             6 - (uint)(*(uint *)(param_1 + 0x124) < *(uint *)(param_1 + 0x200));
        return 0;
      }
      break;
    case 6:
      cVar3 = FUN_82147590(param_1);
      if (cVar3 != '\0') {
        *(undefined1 *)(param_1 + 0x54) = 1;
        *(undefined4 *)(param_1 + 0x50) = 7;
        return 0;
      }
      break;
    case 7:
      cVar3 = FUN_82146cd0(param_1);
      if (cVar3 != '\0') {
        *(undefined1 *)(param_1 + 0x54) = 1;
        *(undefined4 *)(param_1 + 0x50) = 8;
        return 0;
      }
      break;
    case 8:
      cVar3 = FUN_82146d50(param_1);
      if (cVar3 != '\0') {
        *(undefined1 *)(param_1 + 0x54) = 1;
        *(undefined4 *)(param_1 + 0x50) = 9;
        return 0;
      }
      break;
    case 9:
      cVar3 = FUN_82146dd8(param_1);
      if (cVar3 != '\0') {
        *(undefined1 *)(param_1 + 0x54) = 1;
        *(undefined4 *)(param_1 + 0x50) = 10;
        return 0;
      }
      break;
    case 10:
      if (uVar5 == ((uVar5 & 0xffffffff) / 0x3c) * 0x3c) {
        cVar3 = FUN_821478d8(param_1);
        if (cVar3 != '\0') {
          *(undefined1 *)(param_1 + 0x54) = 1;
          *(undefined4 *)(param_1 + 0x50) = 10;
          return 0;
        }
      }
      else if ((uVar4 & 0xffffffff) < 0x385) {
        return 0;
      }
      break;
    case 0xb:
      cVar3 = FUN_82147998(param_1);
      if (cVar3 != '\0') {
        *(undefined1 *)(param_1 + 0x54) = 1;
        *(undefined4 *)(param_1 + 0x920) = 1;
        *(undefined4 *)(param_1 + 0x50) = 0xc;
        return 0;
      }
      break;
    case 0xc:
      cVar3 = FUN_82147998(param_1);
      if (cVar3 != '\0') {
        *(undefined4 *)(param_1 + 0x50) = 0xe;
        *(undefined1 *)(param_1 + 0x54) = 1;
        return 0;
      }
      break;
    case 0xd:
      cVar3 = FUN_821477a0(param_1);
      if (cVar3 != '\0') {
        *(undefined4 *)(param_1 + 0x50) = 0xe;
        *(undefined1 *)(param_1 + 0x54) = 1;
        return 0;
      }
      break;
    case 0xe:
      uVar7 = 1;
    default:
      return uVar7;
    }
    *(undefined4 *)(param_1 + 0x4c) = 0xe;
    return 0;
  }
  if (*(int *)(param_1 + 0x68) == 0x3e5) {
    return 0;
  }
  iVar2 = FUN_825375c0(param_1 + 0x68);
  if (-1 < iVar2) {
    iVar2 = *(int *)(param_1 + 0x4c);
    if (iVar2 == 0) {
      cVar3 = FUN_82147138(param_1);
      if (cVar3 == '\0') {
        *(undefined4 *)(param_1 + 0x50) = 0xe;
        *(undefined4 *)(param_1 + 0x50) = 0xe;
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x55) = 1;
        *(undefined4 *)(param_1 + 0x4c) = 0xe;
        return 0;
      }
    }
    else if (iVar2 == 4) {
      cVar3 = FUN_82147470(param_1);
      if (cVar3 != '\0') {
        *(undefined4 *)(param_1 + 0x124) = 0;
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined4 *)(param_1 + 0x50) = 5;
        *(undefined4 *)(param_1 + 0x50) = 0xe;
        *(undefined4 *)(param_1 + 0x4c) = 5;
        return 0;
      }
    }
    else {
      if (iVar2 == 9) {
        FUN_8252ea08(*(undefined4 *)(param_1 + 0x100));
        *(undefined4 *)(param_1 + 0x5c) = 0;
        *(undefined4 *)(param_1 + 0x58) = 0;
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined4 *)(param_1 + 0x100) = 0xffffffff;
        uVar1 = *(undefined4 *)(param_1 + 0x50);
        *(undefined4 *)(param_1 + 0x50) = 0xe;
        *(undefined4 *)(param_1 + 0x4c) = uVar1;
        return 0;
      }
      if (iVar2 == 10) {
        *(undefined4 *)(param_1 + 0x5c) = 0;
        cVar3 = FUN_821472c0(param_1);
        if (cVar3 != '\0') {
          *(undefined4 *)(param_1 + 0x50) = 0xe;
          *(undefined4 *)(param_1 + 0x50) = 0xe;
          *(undefined1 *)(param_1 + 0x54) = 0;
          *(undefined1 *)(param_1 + 0x55) = 1;
          *(undefined4 *)(param_1 + 0x4c) = 0xe;
          return 0;
        }
      }
      else {
        if (iVar2 == 0xb) {
          FUN_82147d98(param_1);
          FUN_8252ea08(*(undefined4 *)(param_1 + 0x924));
          *(undefined1 *)(param_1 + 0x54) = 0;
          *(undefined4 *)(param_1 + 0x924) = 0xffffffff;
          uVar1 = *(undefined4 *)(param_1 + 0x50);
          *(undefined4 *)(param_1 + 0x50) = 0xe;
          *(undefined4 *)(param_1 + 0x4c) = uVar1;
          return 0;
        }
        if (iVar2 == 0xc) {
          FUN_82147d98(param_1);
          *(undefined1 *)(param_1 + 0x55) = 1;
          FUN_8252ea08(*(undefined4 *)(param_1 + 0x924));
          *(undefined1 *)(param_1 + 0x54) = 0;
          *(undefined4 *)(param_1 + 0x924) = 0xffffffff;
          uVar1 = *(undefined4 *)(param_1 + 0x50);
          *(undefined4 *)(param_1 + 0x50) = 0xe;
          *(undefined4 *)(param_1 + 0x4c) = uVar1;
          return 0;
        }
        if (iVar2 == 0xd) {
          iVar2 = *(int *)(param_1 + 0x11c);
          cVar3 = FUN_82149660(iVar2,0x20070622);
          if ((cVar3 != '\0') && (*(uint *)(iVar2 + 0xc) <= *(uint *)(param_1 + 0xb5c))) {
            *(undefined1 *)(param_1 + 0x55) = 1;
            FUN_825ffd30(*(undefined4 *)(param_1 + 0xb58),iVar2 + 0x10,*(undefined4 *)(iVar2 + 0xc))
            ;
          }
        }
      }
    }
    uVar1 = *(undefined4 *)(param_1 + 0x50);
    *(undefined4 *)(param_1 + 0x50) = 0xe;
    *(undefined1 *)(param_1 + 0x54) = 0;
    *(undefined4 *)(param_1 + 0x4c) = uVar1;
    return 0;
  }
  *(undefined1 *)(param_1 + 0x54) = 0;
  *(undefined4 *)(param_1 + 0x4c) = 0xe;
  return 0;
}



// ===================================================
// 8214AD38  ->  FUN_8214ad38  (entree 8214ad38)
// ===================================================

void FUN_8214ad38(int param_1)

{
  undefined8 uVar1;
  uint uVar3;
  undefined8 uVar2;
  double dVar4;
  undefined1 uStack_130;
  undefined1 uStack_12f;
  undefined1 uStack_12e;
  undefined1 uStack_12d;
  float afStack_128 [6];
  float fStack_110;
  float fStack_10c;
  float fStack_108;
  float fStack_104;
  undefined1 auStack_100 [4];
  float fStack_fc;
  uint uStack_f4;
  undefined4 uStack_e4;
  float fStack_c4;
  float fStack_c0;
  float fStack_bc;
  
  uVar1 = FUN_822c29e8();
  FUN_822c29d8(2);
  FUN_822c2a08(9);
  if (*(int *)(param_1 + 0x4c) < 0xe) {
    afStack_128[1] = 6.81872e-42;
    afStack_128[2] = 6.82012e-42;
    FUN_822b99e8(auStack_100);
    uVar3 = FUN_822c6de8();
    fStack_fc = afStack_128[(uVar3 / 10) % 3];
    FUN_822977e0();
    afStack_128[1] = DAT_82000f18;
    dVar4 = (double)DAT_82000a34;
    afStack_128[2] = DAT_82000a34;
    fStack_c4 = afStack_128[0];
    fStack_c0 = DAT_82000f18;
    fStack_bc = DAT_82000a34;
    uStack_f4 = uStack_f4 | 0x400000;
    uStack_e4 = 0xe;
    uVar2 = FUN_82322798(0x5dc);
    fStack_110 = (float)dVar4;
    fStack_10c = (float)dVar4;
    fStack_108 = (float)dVar4;
    fStack_104 = (float)dVar4;
    FUN_8223bc10(0xe);
    FUN_8223c130(0xe);
    FUN_8223e5e0(uVar2,&fStack_110);
    fStack_c4 = fStack_c4 - fStack_108;
    fStack_10c = fStack_c0 - DAT_82001004;
    fStack_108 = fStack_108 + DAT_82001000;
    fStack_104 = (float)DAT_82000ffc;
    uStack_130 = 0;
    uStack_12f = 0;
    uStack_12e = 0;
    uStack_12d = 0x7f;
    fStack_110 = fStack_c4 - DAT_82000ff8;
    FUN_822c2c90(&fStack_110,9,0xe,&uStack_130,0);
    FUN_822c2940(auStack_100);
    FUN_8223beb8((double)(fStack_110 + DAT_82000ff4),(double)(fStack_10c + DAT_82000ff4));
    FUN_8223fe30(0xffffffff82000f08,uVar2);
  }
  FUN_822c2a18();
  FUN_822c29d8(uVar1);
  return;
}



// ===================================================
// 821D04D8  ->  FUN_821d04d8  (entree 821d04d8)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_821d04d8(int param_1)

{
  undefined1 uVar1;
  int iVar3;
  undefined8 uVar2;
  undefined4 uVar4;
  
  *(undefined4 *)(param_1 + 0x20c) = 0xffffffff;
  if (((*(int *)(param_1 + 0x4c) < 2) && (*(int *)(param_1 + 0x50) != 0)) &&
     (iVar3 = FUN_821dc920(), iVar3 != 0)) {
    uVar1 = *(undefined1 *)(param_1 + 0x210);
    uVar2 = FUN_821dc9f8();
    FUN_823a7598(*(undefined4 *)(param_1 + 0x4c),*(undefined4 *)(param_1 + 0x50),uVar2,uVar1,
                 param_1 + 0x54);
    uVar4 = FUN_82143758(0xffffffff8200b288,param_1 + 0x54,0x1b8,0);
    *(undefined4 *)(param_1 + 0x20c) = uVar4;
  }
  return 1;
}



// ===================================================
// 821D0568  ->  FUN_821d0568  (entree 821d0568)
// ===================================================

bool FUN_821d0568(int param_1)

{
  int iVar1;
  
  if (*(int *)(param_1 + 0x20c) < 0) {
    return true;
  }
  iVar1 = FUN_82143758(*(int *)(param_1 + 0x20c),0,0);
  return iVar1 < 1;
}



// ===================================================
// 821D1000  ->  FUN_821d1000  (entree 821d1000)
// ===================================================

undefined8 FUN_821d1000(undefined8 param_1,ulonglong param_2)

{
  FUN_822c73a8();
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 821E3CC0  ->  FUN_821e3cc0  (entree 821e3cc0)
// ===================================================

bool FUN_821e3cc0(void)

{
  char cVar1;
  
  cVar1 = FUN_822c80d0(0xffffffff82797e80);
  return DAT_82797f0c == 3 || cVar1 == '\0';
}



// ===================================================
// 82247170  ->  FUN_82247170  (entree 82247170)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 * FUN_82247170(undefined4 *param_1,undefined8 param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  longlong lVar4;
  undefined4 uStack_20;
  int iStack_1c;
  undefined4 uStack_18;
  undefined4 uStack_14;
  
  if ((int)param_2 < 0) {
    uStack_20 = 999;
    param_1[1] = 99;
    param_1[2] = 0x3b;
    param_1[3] = 99;
  }
  else {
    uVar1 = FUN_826062c0(param_2,0x3c);
    uStack_20 = (undefined4)((ulonglong)uVar1 >> 0x20);
    uVar2 = FUN_826062c0(uStack_20,0x3c);
    uStack_18 = (undefined4)((ulonglong)uVar2 >> 0x20);
    uVar3 = FUN_826062c0(uStack_18,0x3c);
    iStack_1c = (int)uVar1;
    uStack_14 = (undefined4)uVar2;
    lVar4 = (longlong)iStack_1c;
    iStack_1c = (int)uVar3;
    uStack_20 = (undefined4)((ulonglong)uVar3 >> 0x20);
    param_1[2] = uStack_14;
    param_1[1] = iStack_1c;
    param_1[3] = (int)((float)lVar4 * _DAT_820102e0);
  }
  *param_1 = uStack_20;
  return param_1;
}



// ===================================================
// 82277E08  ->  FUN_82277e08  (entree 82277e08)
// ===================================================

ulonglong FUN_82277e08(void)

{
  int iVar1;
  ulonglong uVar2;
  
  uVar2 = 0xffffffffffffffff;
  iVar1 = FUN_82276ad8();
  if (iVar1 != 0) {
    return (ulonglong)*(uint *)(iVar1 + 0x40);
  }
  return uVar2;
}



// ===================================================
// 82278670  ->  FUN_82278670  (entree 82278670)
// ===================================================

ulonglong FUN_82278670(undefined8 param_1)

{
  int iVar1;
  ulonglong uVar2;
  
  uVar2 = 0xffffffffffffffff;
  iVar1 = FUN_82276750();
  if ((iVar1 != 0) && (iVar1 = FUN_82277dc8(param_1), iVar1 != -1)) {
    return (ulonglong)(uint)(&DAT_8205f660)[iVar1];
  }
  return uVar2;
}



// ===================================================
// 822CF438  ->  FUN_822cf438  (entree 822cf438)
// ===================================================

bool FUN_822cf438(void)

{
  char cVar1;
  
  cVar1 = FUN_822c80d0(0xffffffff829c9c00);
  return cVar1 == '\0';
}



// ===================================================
// 822E41E0  ->  FUN_822e41e0  (entree 822e41e0)
// ===================================================

void FUN_822e41e0(longlong param_1)

{
  FUN_822e3b78(param_1 + 0x50);
  FUN_822c7d50(param_1);
  return;
}



// ===================================================
// 822E70D0  ->  FUN_822e70d0  (entree 822e70d0)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_822e70d0(int param_1)

{
  undefined8 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined8 uVar4;
  undefined4 uStack_50;
  undefined4 uStack_4c;
  undefined4 uStack_48;
  undefined4 uStack_40;
  undefined4 uStack_3c;
  undefined4 uStack_38;
  undefined1 auStack_30 [48];
  
  if (*(char *)(param_1 + 0x82b) != '\0') {
    uVar1 = FUN_822c29e8();
    FUN_822c29d8(2);
    FUN_822c2a08(9);
    if (*(int *)(param_1 + 0x814) == 0) {
      if (*(int *)(param_1 + 0x82c) == 0) {
        FUN_822f69d8(param_1 + 0x82c,0x422,0xffffffff82086030,7,0x10000,0xffffffff82084bc4,
                     0xffffffff82084bcc);
      }
      iVar2 = param_1 + 0x830;
    }
    else {
      if (*(char *)(param_1 + 0x828) == '\0') {
        if (*(int *)(param_1 + 0x830) == 0) {
          FUN_822f69d8((undefined4 *)(param_1 + 0x830),0x422,0xffffffff82086024,7,0x10000,
                       0xffffffff82084bc4,0xffffffff82084bcc);
        }
        puVar3 = (undefined4 *)
                 ((*(int *)(param_1 + 0x824) * 8 + *(int *)(param_1 + 0x820) + 0xaf) * 0xc + param_1
                 );
        uStack_50 = *puVar3;
        uStack_4c = puVar3[1];
        uStack_48 = puVar3[2];
        puVar3 = (undefined4 *)FUN_822f6658(auStack_30,&uStack_50);
        uStack_40 = *puVar3;
        uStack_3c = puVar3[1];
        uStack_38 = puVar3[2];
        FUN_82166540(*(undefined4 *)(param_1 + 0x830),&uStack_40);
      }
      else {
        FUN_822fb5b8(param_1 + 0x830);
      }
      iVar2 = param_1 + 0x82c;
    }
    FUN_822fb5b8(iVar2);
    uVar4 = 1;
    if (*(int *)(param_1 + 0x818) < 1) {
      uVar4 = 2;
    }
    FUN_821ccba8(param_1 + 0x9e4,uVar4);
    FUN_822f6830(param_1 + 0x9e4);
    uVar4 = 1;
    if (*(int *)(param_1 + 0x81c) <= *(int *)(param_1 + 0x818)) {
      uVar4 = 2;
    }
    FUN_821ccba8(param_1 + 0xa08,uVar4);
    FUN_822f6830(param_1 + 0xa08);
    FUN_822c2a18();
    FUN_822c29d8(uVar1);
  }
  return;
}



// ===================================================
// 822E7288  ->  FUN_822e7288  (entree 822e7288)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_822e7288(int param_1)

{
  undefined8 uVar1;
  undefined4 auStack_60 [24];
  
  auStack_60[0] = 0x23b;
  auStack_60[1] = 0x23c;
  auStack_60[2] = 0x23d;
  auStack_60[3] = 0x23e;
  auStack_60[4] = 0x23f;
  auStack_60[5] = 0x240;
  auStack_60[6] = 0x241;
  auStack_60[7] = 0x242;
  auStack_60[8] = 0x243;
  auStack_60[9] = 0x244;
  auStack_60[10] = 0x245;
  auStack_60[0xb] = 0x246;
  auStack_60[0xc] = 0x247;
  auStack_60[0xd] = 0x248;
  FUN_8223bc10(0xe);
  FUN_8223c130(7);
  FUN_8223beb8((double)*(float *)(param_1 + 0x9b4),(double)*(float *)(param_1 + 0x9b8));
  FUN_8223c048(0xffffffffffbff560);
  uVar1 = FUN_82322798(0x3ec);
  FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar1);
  FUN_8223beb8((double)*(float *)(param_1 + 0x9c0),(double)*(float *)(param_1 + 0x9c4));
  if (*(int *)(param_1 + 0x814) == 0) {
    uVar1 = 0xffffffffff6cbede;
  }
  else {
    uVar1 = 0xffffffffffffffff;
  }
  FUN_8223c048(uVar1);
  uVar1 = FUN_82322798(auStack_60[*(int *)(param_1 + 0x818)]);
  FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar1);
  return;
}



// ===================================================
// 822E73B8  ->  FUN_822e73b8  (entree 822e73b8)
// ===================================================

void FUN_822e73b8(int param_1)

{
  undefined8 uVar1;
  double dVar2;
  
  dVar2 = (double)((float)(longlong)(int)(*(float *)(param_1 + 0x5b8) * DAT_82001948) * DAT_8201da2c
                  );
  FUN_8223bc10(0xe);
  FUN_8223c130(7);
  FUN_8223c048(0xfffffffffff29600);
  FUN_8223beb8((double)(*(float *)(param_1 + 0x9d8) - DAT_820636c4),
               (double)*(float *)(param_1 + 0x9dc));
  uVar1 = FUN_82322798(0x3ee);
  FUN_8223fe30(0xffffffff82000f80,0xffffffff82010300,uVar1);
  FUN_8223c048(0xffffffffffffffff);
  FUN_8223beb8((double)*(float *)(param_1 + 0x9d8),(double)*(float *)(param_1 + 0x9dc));
  uVar1 = FUN_82322798(0x191);
  FUN_8223fe30(0xffffffff82086040,0xffffffff82010300,dVar2,uVar1);
  return;
}



// ===================================================
// 822E74D8  ->  FUN_822e74d8  (entree 822e74d8)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

undefined8 FUN_822e74d8(int param_1)

{
  uint uVar1;
  bool bVar2;
  char cVar3;
  int *piVar4;
  int iVar5;
  int iVar6;
  
  uVar1 = *(uint *)(param_1 + 0x5c4);
  if (uVar1 == 0) {
    FUN_82356c08();
    iVar6 = 0;
    iVar5 = 0x106;
    do {
      FUN_822c2a80(iVar5);
      iVar6 = iVar6 + 1;
      iVar5 = (&DAT_82085fdc)[iVar6];
    } while (iVar5 != -1);
    *(undefined4 *)(param_1 + 0x5c4) = 1;
    return 1;
  }
  if (uVar1 == 1) {
    bVar2 = false;
    piVar4 = &DAT_82085fdc;
    iVar5 = 0;
    do {
      cVar3 = FUN_822c2848(*piVar4);
      if (cVar3 != '\0') {
        bVar2 = true;
        break;
      }
      iVar5 = iVar5 + 1;
      piVar4 = &DAT_82085fdc + iVar5;
    } while (*piVar4 != -1);
    if (bVar2) {
      return 1;
    }
    FUN_82356ca0();
    *(undefined4 *)(param_1 + 0x5c4) = 2;
  }
  else if (2 < uVar1) {
    return 1;
  }
  return 0;
}



// ===================================================
// 822E75B8  ->  FUN_822e75b8  (entree 822e75b8)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_822e75b8(int param_1)

{
  int iVar1;
  int iVar2;
  
  iVar2 = 0;
  iVar1 = 0x106;
  do {
    FUN_822c2888(iVar1);
    iVar2 = iVar2 + 1;
    iVar1 = (&DAT_82085fdc)[iVar2];
  } while (iVar1 != -1);
  *(undefined4 *)(param_1 + 0x5c4) = 3;
  return;
}



// ===================================================
// 822E76A0  ->  FUN_822e76a0  (entree 822e76a0)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_822e76a0(int param_1)

{
  FUN_823a7598(param_1 + 0xa08);
  FUN_823a7598(param_1 + 0x9e4);
  FUN_82154d98(param_1 + 0x714);
  FUN_822c73a8(param_1 + 0x6b8);
  if (*(int *)(param_1 + 0x6a4) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 0x6a4) = 0;
  *(undefined4 *)(param_1 + 0x6a8) = 0;
  *(undefined4 *)(param_1 + 0x6ac) = 0;
  FUN_822c73a8(param_1 + 0x634);
  if (*(int *)(param_1 + 0x620) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 0x620) = 0;
  *(undefined4 *)(param_1 + 0x624) = 0;
  *(undefined4 *)(param_1 + 0x628) = 0;
  if (*(int *)(param_1 + 0x5cc) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 0x5cc) = 0;
  *(undefined4 *)(param_1 + 0x5d0) = 0;
  *(undefined4 *)(param_1 + 0x5d4) = 0;
  FUN_822c73a8(param_1);
  return;
}



// ===================================================
// 822E7750  ->  FUN_822e7750  (entree 822e7750)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

undefined8 FUN_822e7750(int param_1)

{
  undefined8 in_r0;
  undefined8 uVar1;
  int iVar3;
  undefined8 uVar2;
  char cVar4;
  undefined4 *puVar5;
  int iVar6;
  undefined4 uVar7;
  int iStack_48;
  uint uStack_44;
  
  FUN_822f3068();
  uVar1 = FUN_821ccbb8();
  FUN_822da898();
  iVar3 = FUN_822dac40();
  uVar2 = FUN_82235f28(0xffffffff827a99f8,uVar1);
  FUN_821de388(param_1 + 0x50,uVar2);
  iVar6 = 7;
  puVar5 = (undefined4 *)(param_1 + 0x594);
  do {
    iVar6 = iVar6 + -1;
    *puVar5 = 0;
    puVar5 = puVar5 + -1;
  } while (-1 < iVar6);
  iVar6 = 7;
  puVar5 = (undefined4 *)(param_1 + 0x5b4);
  do {
    iVar6 = iVar6 + -1;
    *puVar5 = 0;
    puVar5 = puVar5 + -1;
  } while (-1 < iVar6);
  *(undefined1 *)(param_1 + 0x829) = 0;
  cVar4 = FUN_823103c8(uVar1,param_1 + 0x5b8);
  *(char *)(param_1 + 0x82a) = cVar4;
  if (iVar3 != 0) {
    if ((cVar4 != '\0') && (*(char *)(iVar3 + 0xc2) == '\0')) {
      *(undefined1 *)(iVar3 + 0xc2) = 1;
      *(undefined1 *)(param_1 + 0x829) = 1;
      FUN_825ffc10(iVar3 + 0x7d,0xff,0x20);
    }
    FUN_825ffd30(param_1 + 0x578,iVar3 + 0x7d,0x20);
    FUN_825ffd30(param_1 + 0x598,iVar3 + 0x9d,0x20);
    FUN_825ffd30(iVar3 + 0x9d,iVar3 + 0x7d,0x20);
  }
  *(undefined4 *)(param_1 + 0x5bc) = 0;
  *(undefined4 *)(param_1 + 0x5c4) = 0;
  *(undefined1 *)(param_1 + 0x82b) = 0;
  uVar7 = 0xc;
  *(undefined4 *)(param_1 + 0x814) = 0;
  *(undefined4 *)(param_1 + 0x818) = 0;
  *(undefined4 *)(param_1 + 0x820) = 0;
  *(undefined4 *)(param_1 + 0x824) = 0;
  *(undefined1 *)(param_1 + 0x828) = 0;
  if (*(char *)(param_1 + 0x82a) != '\0') {
    uVar7 = 0xd;
  }
  iStack_48 = param_1 + 0x5c8;
  *(undefined4 *)(param_1 + 0x81c) = uVar7;
  uStack_44 = *(uint *)(param_1 + 0x5cc);
  if (*(uint *)(param_1 + 0x5d0) < uStack_44) {
    trapWord(0x1f,in_r0,0x16);
    trapWord(0x1f,in_r0,0x16);
  }
  FUN_82318f58(&iStack_48,iStack_48,CONCAT44(iStack_48,uStack_44),
               CONCAT44(iStack_48,*(uint *)(param_1 + 0x5d0)));
  *(undefined4 *)(param_1 + 0x82c) = 0;
  *(undefined4 *)(param_1 + 0x830) = 0;
  return 1;
}



// ===================================================
// 822E78F8  ->  FUN_822e78f8  (entree 822e78f8)
// ===================================================

undefined8 FUN_822e78f8(int param_1)

{
  undefined8 in_r0;
  undefined8 uVar1;
  int iStack_18;
  uint uStack_14;
  
  FUN_822f3068();
  uVar1 = FUN_821ccbb8();
  FUN_82236060(0xffffffff827a99f8,param_1 + 0x50,uVar1);
  iStack_18 = param_1 + 0x5c8;
  uStack_14 = *(uint *)(param_1 + 0x5cc);
  if (*(uint *)(param_1 + 0x5d0) < uStack_14) {
    trapWord(0x1f,in_r0,0x16);
    trapWord(0x1f,in_r0,0x16);
  }
  FUN_82318f58(&iStack_18,iStack_18,CONCAT44(iStack_18,uStack_14),
               CONCAT44(iStack_18,*(uint *)(param_1 + 0x5d0)));
  FUN_822e75b8(param_1);
  FUN_822e3b78(param_1 + 0x600);
  FUN_822c7d50(param_1 + 0x634);
  FUN_822c7d50(param_1 + 0x6b8);
  return 1;
}



// ===================================================
// 822E79A8  ->  FUN_822e79a8  (entree 822e79a8)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_822e79a8(int param_1)

{
  int iVar1;
  char *pcVar2;
  char cVar3;
  char cVar4;
  byte bVar5;
  int *piVar6;
  int *piVar7;
  
  iVar1 = FUN_822d1868();
  if (-1 < iVar1) {
    FUN_822d11a8();
    *(undefined1 *)(param_1 + 0x828) = 0;
    *(undefined4 *)(param_1 + 0x814) = 0;
    return;
  }
  iVar1 = FUN_822d1830();
  if (iVar1 < 0) {
    if ((*(int *)(param_1 + 0x5cc) != 0) &&
       (*(int *)(param_1 + 0x5d0) - *(int *)(param_1 + 0x5cc) >> 3 != 0)) {
      piVar7 = (int *)(param_1 + 0x824);
      piVar6 = (int *)(param_1 + 0x820);
      bVar5 = 0;
      while( true ) {
        cVar3 = FUN_822d0e18(piVar7,4,1);
        bVar5 = bVar5 + 1;
        cVar4 = *(char *)((*piVar7 + 0xbb) * 8 + param_1 + *piVar6);
        if (100 < bVar5) break;
        if ((cVar3 == '\0') || (cVar4 != '\0')) goto LAB_822e7b00;
      }
      cVar4 = '\x01';
      *piVar6 = 0;
      *piVar7 = 0;
LAB_822e7b00:
      if (cVar3 != '\0') {
        FUN_822d1188();
        if (cVar4 == '\x01') {
          *(undefined1 *)(param_1 + 0x828) = 0;
        }
        else if (cVar4 == '\x02') {
          *(undefined1 *)(param_1 + 0x828) = 1;
        }
      }
      if (*(char *)(param_1 + 0x828) == '\0') {
        bVar5 = 0;
        while( true ) {
          cVar4 = FUN_822d0f88(piVar6,7,1);
          bVar5 = bVar5 + 1;
          if (100 < bVar5) break;
          if ((cVar4 == '\0') || (*(char *)((*piVar7 + 0xbb) * 8 + param_1 + *piVar6) == '\x01'))
          goto LAB_822e7b9c;
        }
        *piVar6 = 0;
        *piVar7 = 0;
LAB_822e7b9c:
        if (cVar4 != '\0') {
          FUN_822d1188();
        }
      }
    }
  }
  else {
    if (*(char *)(param_1 + 0x828) != '\0') {
      if (*(char *)(param_1 + 0x473) == '\0') {
        FUN_822d11a8();
        return;
      }
      *(undefined4 *)(param_1 + 0x80c) = 1;
      *(undefined4 *)(param_1 + 0x810) = 0;
      *(undefined4 *)(param_1 + 0x5bc) = 3;
      return;
    }
    FUN_822d1198();
    pcVar2 = (char *)FUN_8226cd70(param_1 + 0x5c8,
                                  ((ulonglong)*(uint *)(param_1 + 0x824) & 0x1fffffff) * 8 +
                                  (ulonglong)*(uint *)(param_1 + 0x820));
    if (*pcVar2 != '\0') {
      *(undefined4 *)(param_1 + 0x80c) = 0;
      *(undefined4 *)(param_1 + 0x810) = 0;
      *(undefined4 *)(param_1 + 0x5bc) = 3;
      return;
    }
  }
  return;
}



// ===================================================
// 822E7BB8  ->  FUN_822e7bb8  (entree 822e7bb8)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_822e7bb8(int param_1)

{
  int iVar2;
  undefined8 uVar1;
  int iVar3;
  uint uVar4;
  
  if (*(int *)(param_1 + 0x5cc) == 0) {
    iVar3 = 0;
  }
  else {
    iVar3 = *(int *)(param_1 + 0x5d0) - *(int *)(param_1 + 0x5cc) >> 3;
  }
  uVar4 = 0;
  if (0 < iVar3) {
    do {
      iVar2 = FUN_8226cd70(param_1 + 0x5c8,uVar4);
      FUN_823084e8(*(undefined4 *)(iVar2 + 4),7,
                   ((uVar4 & 0xfffffff8) + (uVar4 & 7) + 0xaf) * 0xc + param_1,0x400000);
      uVar4 = uVar4 + 1;
    } while ((int)uVar4 < iVar3);
  }
  uVar1 = FUN_82322798(0x3ed);
  FUN_8223bc10(0xe);
  FUN_8223beb8((double)*(float *)(param_1 + 0x9cc),(double)*(float *)(param_1 + 0x9d0));
  FUN_8223c130(7);
  FUN_8223c048(0xffffffffffffffff);
  FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar1);
  if (*(char *)(param_1 + 0x828) != '\0') {
    FUN_822e37e0((double)*(float *)(param_1 + 0x9cc),(double)*(float *)(param_1 + 0x9d0),
                 (double)DAT_82000b08,param_1 + 0x62c);
  }
  return;
}



// ===================================================
// 822E7CD0  ->  FUN_822e7cd0  (entree 822e7cd0)
// ===================================================

void FUN_822e7cd0(int param_1)

{
  char cVar2;
  int iVar1;
  undefined4 uStack_20;
  undefined4 uStack_1c;
  undefined4 uStack_18;
  
  cVar2 = FUN_822e2dd8(param_1 + 0x784);
  if ((cVar2 != '\0') && (*(int *)(param_1 + 0x80c) == 0)) {
    iVar1 = FUN_8226cd70(param_1 + 0x5c8,
                         ((ulonglong)*(uint *)(param_1 + 0x824) & 0x1fffffff) * 8 +
                         (ulonglong)*(uint *)(param_1 + 0x820));
    uStack_20 = DAT_8208604c;
    uStack_1c = DAT_82006bb8;
    uStack_18 = DAT_82000a34;
    FUN_823084e8(*(undefined4 *)(iVar1 + 4),0xe,&uStack_20,0);
  }
  return;
}



// ===================================================
// 822E7D68  ->  FUN_822e7d68  (entree 822e7d68)
// ===================================================

void FUN_822e7d68(int param_1)

{
  uint uVar1;
  char cVar5;
  int iVar3;
  undefined8 uVar2;
  undefined4 uVar4;
  
  uVar1 = *(uint *)(param_1 + 0x810);
  if (uVar1 != 0) {
    if (uVar1 != 1) {
      if (2 < uVar1) {
        return;
      }
      cVar5 = FUN_822c80d0(param_1 + 0x714);
      if (cVar5 != '\0') {
        return;
      }
      *(undefined4 *)(param_1 + 0x5bc) = *(undefined4 *)(param_1 + 0x5c0);
      return;
    }
    iVar3 = FUN_822e2e38(param_1 + 0x714);
    if (iVar3 == -1) {
      return;
    }
    if (iVar3 == 0) {
      switch(*(undefined4 *)(param_1 + 0x80c)) {
      case 0:
        iVar3 = FUN_8226cd70(param_1 + 0x5c8,
                             ((ulonglong)*(uint *)(param_1 + 0x824) & 0x1fffffff) * 8 +
                             (ulonglong)*(uint *)(param_1 + 0x820));
        cVar5 = *(char *)(iVar3 + 2);
        *(undefined4 *)(param_1 + 0x810) = 2;
        *(undefined4 *)(param_1 + 0x5c0) = 4;
        *(char *)(param_1 + 0x473) = cVar5 + '\x01';
        return;
      case 1:
        *(undefined4 *)(param_1 + 0x810) = 2;
        *(undefined1 *)(param_1 + 0x473) = 0;
        *(undefined4 *)(param_1 + 0x5c0) = 4;
        return;
      case 2:
        break;
      case 3:
        *(undefined4 *)(param_1 + 0x810) = 2;
        *(undefined4 *)(param_1 + 0x5c0) = 4;
        return;
      default:
switchD_822e7df4_default:
        *(undefined4 *)(param_1 + 0x810) = 2;
        return;
      }
    }
    *(undefined4 *)(param_1 + 0x5c0) = 2;
    goto switchD_822e7df4_default;
  }
  iVar3 = param_1 + 0x714;
  cVar5 = FUN_822c80d0(iVar3);
  if (cVar5 != '\0') {
    return;
  }
  FUN_822e3c10(iVar3);
  FUN_822c8aa0(iVar3,0xffffffff82086050);
  switch(*(undefined4 *)(param_1 + 0x80c)) {
  case 0:
    FUN_822e2e28(iVar3,1);
    uVar2 = 0x5f5;
    *(undefined4 *)(param_1 + 0x760) = 3;
    break;
  case 1:
    FUN_822e2e28(iVar3,1);
    uVar2 = 0x5f6;
    break;
  case 2:
    uVar2 = 0x5f4;
    break;
  case 3:
    FUN_822e2e28(iVar3,1);
    uVar2 = 0x5fd;
    break;
  default:
    goto switchD_822e7ec0_default;
  }
  uVar4 = FUN_82322798(uVar2);
  *(undefined4 *)(param_1 + 0x774) = uVar4;
switchD_822e7ec0_default:
  *(undefined4 *)(param_1 + 0x810) = 1;
  return;
}



// ===================================================
// 822E7F48  ->  FUN_822e7f48  (entree 822e7f48)
// ===================================================

void FUN_822e7f48(int param_1)

{
  undefined8 uVar1;
  
  if (*(char *)(param_1 + 0x82b) != '\0') {
    uVar1 = FUN_822c29e8();
    FUN_822c29d8(2);
    FUN_822c2a08(9);
    FUN_822e7288(param_1);
    FUN_822e7bb8(param_1);
    FUN_822e73b8(param_1);
    FUN_822e7cd0(param_1);
    FUN_822c2a18();
    FUN_822c29d8(uVar1);
  }
  return;
}



// ===================================================
// 822E8108  ->  FUN_822e8108  (entree 822e8108)
// ===================================================

undefined8 FUN_822e8108(undefined8 param_1,ulonglong param_2)

{
  FUN_822e76a0();
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



