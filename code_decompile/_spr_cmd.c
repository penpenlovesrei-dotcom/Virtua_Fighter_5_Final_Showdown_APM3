// ===================================================
// 18018CA20  ->  FUN_18018ca20  (entree 18018ca20)
// ===================================================

undefined8 * FUN_18018ca20(longlong *param_1,longlong param_2)

{
  longlong lVar1;
  longlong lVar2;
  int iVar3;
  undefined8 *puVar4;
  undefined8 uVar5;
  uint uVar6;
  int iVar7;
  uint uVar8;
  undefined8 *puVar9;
  undefined8 *puVar10;
  undefined8 *puVar11;
  undefined8 *puVar12;
  short sVar13;
  longlong *plVar14;
  ulonglong uVar15;
  short sVar16;
  uint uVar17;
  int iVar18;
  undefined1 auVar19 [16];
  undefined1 auVar20 [16];
  undefined1 auVar21 [16];
  undefined1 auVar22 [16];
  float fVar23;
  float fVar24;
  
  iVar18 = *(int *)(param_2 + 0x14);
  if (iVar18 == -1) {
    iVar18 = (int)param_1[0x105];
  }
  puVar9 = (undefined8 *)0x0;
  if (*(uint *)(param_2 + 4) == 0xffffffff) {
    lVar1 = *(longlong *)(param_2 + 0xa0);
    FUN_18018c9b0(param_1 + (((longlong)*(int *)(param_2 + 0x18) + (longlong)iVar18) * 0x20 +
                            (ulonglong)*(uint *)(param_2 + 0x1c) + 1) * 2);
    lVar2 = *(longlong *)
             (param_1[(((longlong)*(int *)(param_2 + 0x18) + (longlong)iVar18) * 0x20 +
                      (ulonglong)*(uint *)(param_2 + 0x1c) + 1) * 2] + 8);
    puVar12 = (undefined8 *)(lVar2 + 0x10);
    if (lVar1 != 0) {
      lVar1 = *(longlong *)(lVar2 + 0xb0);
      uVar6 = *(uint *)(lVar2 + 0xd0);
      sVar16 = *(short *)(lVar1 + 0xc);
      sVar13 = *(short *)(lVar1 + 0xe);
      auVar19._0_4_ = (float)(int)sVar16;
      auVar19._4_8_ = SUB128(ZEXT812(0),4);
      auVar19._12_4_ = 0;
      auVar20._0_4_ = (float)(int)sVar13;
      auVar20._4_8_ = SUB128(ZEXT812(0),4);
      auVar20._12_4_ = 0;
      if ((uVar6 & 1) == 0) {
        auVar19 = vunpcklps_avx(auVar19,auVar20);
        *(longlong *)(lVar2 + 0xd4) = auVar19._0_8_;
        uVar6 = uVar6 | 1;
        *(undefined4 *)(lVar2 + 0xdc) = 0;
        *(uint *)(lVar2 + 0xd0) = uVar6;
        sVar13 = *(short *)(lVar1 + 0xe);
        sVar16 = *(short *)(lVar1 + 0xc);
      }
      if ((uVar6 & 2) == 0) {
        *(float *)(lVar2 + 0xec) = (float)(int)sVar13;
        *(float *)(lVar2 + 0xe8) = (float)(int)sVar16;
        *(undefined8 *)(lVar2 + 0xe0) = 0;
        *(uint *)(lVar2 + 0xd0) = uVar6 | 2;
      }
    }
    goto LAB_18018ce31;
  }
  puVar11 = (undefined8 *)*param_1;
  uVar6 = *(uint *)(param_2 + 4) >> 0x10 & 0xfff;
  puVar12 = (undefined8 *)puVar11[1];
  puVar10 = puVar11;
  if (*(char *)((longlong)puVar11[1] + 0x19) == '\0') {
    do {
      if (*(uint *)(puVar12 + 4) < uVar6) {
        puVar4 = (undefined8 *)puVar12[2];
      }
      else {
        puVar4 = (undefined8 *)*puVar12;
        puVar10 = puVar12;
      }
      puVar12 = puVar4;
    } while (*(char *)((longlong)puVar4 + 0x19) == '\0');
    if ((puVar10 == puVar11) || (uVar6 < *(uint *)(puVar10 + 4))) goto LAB_18018caa8;
  }
  else {
LAB_18018caa8:
    puVar10 = puVar11;
  }
  puVar4 = puVar10 + 5;
  if (puVar10 == puVar11) {
    puVar4 = puVar9;
  }
  puVar12 = puVar9;
  if ((puVar4 != (undefined8 *)0x0) &&
     (puVar12 = (undefined8 *)0x0, *(char *)(puVar4 + 0x17) != '\0')) {
    plVar14 = param_1 + ((ulonglong)*(uint *)(param_2 + 0x1c) + 1 +
                        ((longlong)*(int *)(param_2 + 0x18) + (longlong)iVar18) * 0x20) * 2;
    lVar1 = *plVar14;
    puVar12 = *(undefined8 **)(lVar1 + 8);
    uVar5 = FUN_180187cf0(plVar14,lVar1,puVar12,param_2);
    if (plVar14[1] == 0x108421084210841) {
                    /* WARNING: Subroutine does not return */
      FUN_1802fbd0c("list<T> too long");
    }
    plVar14[1] = plVar14[1] + 1;
    *(undefined8 *)(lVar1 + 8) = uVar5;
    *puVar12 = uVar5;
    lVar1 = *(longlong *)
             (param_1[((ulonglong)*(uint *)(param_2 + 0x1c) + 1 +
                      ((longlong)*(int *)(param_2 + 0x18) + (longlong)iVar18) * 0x20) * 2] + 8);
    puVar12 = (undefined8 *)(lVar1 + 0x10);
    uVar6 = *(uint *)(lVar1 + 0x14);
    uVar17 = uVar6 & 0xf0000000;
    if (uVar17 == 0x10000000) {
      plVar14 = puVar10 + 8;
      if (puVar10 == puVar11) {
        plVar14 = (longlong *)&DAT_00000018;
      }
      uVar5 = *(undefined8 *)(*plVar14 + (ulonglong)(uVar6 & 0xffff) * 8);
    }
    else {
      plVar14 = puVar10 + 7;
      if (puVar10 == puVar11) {
        plVar14 = (longlong *)&DAT_00000010;
      }
      iVar3 = *(int *)(*plVar14 + 0x10);
      puVar4 = puVar9;
      if (iVar3 != 0) {
        puVar4 = (undefined8 *)(*plVar14 + 0x10 + (longlong)iVar3);
      }
      plVar14 = puVar10 + 8;
      if (puVar10 == puVar11) {
        plVar14 = (longlong *)&DAT_00000018;
      }
      uVar5 = *(undefined8 *)
               (*plVar14 + (longlong)*(int *)(puVar4 + (ulonglong)(uVar6 & 0xffff) * 5) * 8);
    }
    *(undefined8 *)(lVar1 + 0xb0) = uVar5;
    if (uVar17 == 0x10000000) {
      fVar23 = 0.0;
      fVar24 = 0.0;
      lVar2 = *(longlong *)(*plVar14 + (ulonglong)(uVar6 & 0xffff) * 8);
      iVar3 = (int)*(short *)(lVar2 + 0xe);
      iVar7 = (int)*(short *)(lVar2 + 0xc);
    }
    else {
      uVar15 = (ulonglong)(uVar6 & 0xffff);
      plVar14 = puVar10 + 7;
      if (puVar10 == puVar11) {
        plVar14 = (longlong *)&DAT_00000010;
      }
      iVar3 = *(int *)(*plVar14 + 0x10);
      puVar4 = puVar9;
      if (iVar3 != 0) {
        puVar4 = (undefined8 *)(*plVar14 + 0x10 + (longlong)iVar3);
      }
      fVar23 = (float)(int)*(float *)(puVar4 + uVar15 * 5 + 3);
      fVar24 = (float)(int)*(float *)((longlong)puVar4 + uVar15 * 0x28 + 0x1c);
      iVar3 = (int)*(float *)((longlong)puVar4 + uVar15 * 0x28 + 0x24);
      iVar7 = (int)*(float *)(puVar4 + uVar15 * 5 + 4);
    }
    auVar21._0_4_ = (float)iVar7;
    auVar21._4_8_ = SUB128(ZEXT812(0),4);
    auVar21._12_4_ = 0;
    uVar8 = *(uint *)(lVar1 + 0xd0);
    auVar22._0_4_ = (float)iVar3;
    auVar22._4_8_ = SUB128(ZEXT812(0),4);
    auVar22._12_4_ = 0;
    if ((uVar8 & 1) == 0) {
      uVar8 = uVar8 | 1;
      auVar19 = vunpcklps_avx(auVar21,auVar22);
      *(longlong *)(lVar1 + 0xd4) = auVar19._0_8_;
      *(undefined4 *)(lVar1 + 0xdc) = 0;
      *(uint *)(lVar1 + 0xd0) = uVar8;
    }
    if ((uVar8 & 2) == 0) {
      *(uint *)(lVar1 + 0xd0) = uVar8 | 2;
      *(float *)(lVar1 + 0xe0) = fVar23;
      *(float *)(lVar1 + 0xe4) = fVar24;
      *(float *)(lVar1 + 0xe8) = auVar21._0_4_;
      *(float *)(lVar1 + 0xec) = auVar22._0_4_;
    }
    if (*(int *)(lVar1 + 0x34) != 0x11) {
      if (uVar17 == 0x10000000) {
        *(undefined4 *)(lVar1 + 0x34) = 9;
      }
      else {
        plVar14 = puVar10 + 7;
        if (puVar10 == puVar11) {
          plVar14 = (longlong *)&DAT_00000010;
        }
        iVar3 = *(int *)(*plVar14 + 0x1c);
        puVar11 = puVar9;
        if (iVar3 != 0) {
          puVar11 = (undefined8 *)(*plVar14 + 0x1c + (longlong)iVar3);
        }
        *(undefined4 *)(lVar1 + 0x34) =
             *(undefined4 *)((longlong)puVar11 + (ulonglong)(uVar6 & 0xffff) * 8 + 4);
      }
    }
  }
LAB_18018ce31:
  if (puVar12 != (undefined8 *)0x0) {
    lVar1 = *(longlong *)
             (param_1[((ulonglong)*(uint *)(param_2 + 0x1c) + 1 +
                      ((longlong)*(int *)(param_2 + 0x18) + (longlong)iVar18) * 0x20) * 2] + 8);
    lVar2 = *(longlong *)(lVar1 + 0xb0);
    if ((lVar2 != 0) && (*(longlong *)(lVar1 + 200) != 0)) {
      sVar16 = *(short *)(lVar2 + 0xe);
      puVar11 = puVar9;
      fVar23 = DAT_180346d3c / (float)(int)sVar16;
      fVar24 = DAT_180346d3c / (float)(int)*(short *)(lVar2 + 0xc);
      if (*(int *)(lVar2 + 0x14) == 0x39a) {
        fVar23 = DAT_180346d3c;
        fVar24 = DAT_180346d3c;
      }
      do {
        puVar11 = (undefined8 *)((longlong)puVar11 + 1);
        *(float *)((longlong)puVar9 + *(longlong *)(lVar1 + 0xc0) + 0xc) =
             fVar24 * *(float *)((longlong)puVar9 + *(longlong *)(lVar1 + 0xc0) + 0xc);
        *(float *)((longlong)puVar9 + *(longlong *)(lVar1 + 0xc0) + 0x10) =
             ((float)(int)sVar16 - *(float *)((longlong)puVar9 + *(longlong *)(lVar1 + 0xc0) + 0x10)
             ) * fVar23;
        puVar9 = puVar9 + 3;
      } while (puVar11 < *(undefined8 **)(lVar1 + 200));
    }
  }
  return puVar12;
}



