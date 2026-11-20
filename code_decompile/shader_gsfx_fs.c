// ===================================================
// 180250E32  ->  FUN_180250da0  (entree 180250da0)
// ===================================================

/* WARNING: Function: _alloca_probe replaced with injection: alloca_probe */

void FUN_180250da0(longlong param_1,int param_2,undefined4 param_3,int *param_4)

{
  longlong lVar1;
  uint uVar2;
  longlong lVar3;
  undefined4 uVar4;
  longlong lVar5;
  undefined8 uVar6;
  undefined1 local_8078 [8];
  undefined8 local_8070;
  undefined8 local_8068;
  undefined8 local_8040;
  undefined8 local_8038;
  undefined8 local_8030;
  undefined8 local_8028;
  undefined8 local_8020;
  undefined8 local_8018;
  int local_8008 [8190];
  undefined8 uStack_10;
  
  uStack_10 = 0x180250dc0;
  lVar3 = *(longlong *)(param_1 + 0x1020);
  if (lVar3 != 0) {
    lVar5 = FUN_180286370(param_4);
    if (lVar5 != 0) {
      param_3 = FUN_1802863a0(local_8008,0x8000,param_4);
      param_4 = local_8008;
    }
    if (param_2 == 0x447) {
      lVar5 = (ulonglong)*(uint *)(param_1 + 0xfd0) * 0x20;
      lVar1 = (ulonglong)*(uint *)(param_1 + 0xfd0) * 0x20 + lVar3;
      *(undefined4 *)(lVar5 + 4 + lVar3) = 0x447;
      if (*param_4 == 0x58465347) {
        uVar6 = FUN_180269490();
        *(undefined8 *)(lVar1 + 8) = uVar6;
      }
      else {
        uVar4 = FUN_180268710(param_4,0);
        *(undefined4 *)(lVar1 + 8) = uVar4;
      }
      local_8040 = 0;
      local_8038 = 0;
      local_8030 = 0;
      local_8028 = 0;
      local_8020 = 0;
      local_8018 = 0;
      *(undefined4 *)(lVar5 + 0x10 + lVar3) = param_3;
      FUN_1802695e0(local_8078,*(undefined4 *)(lVar5 + 8 + lVar3));
    }
    else {
      if (param_2 != 0x48b) {
        return;
      }
      uVar2 = *(uint *)(param_1 + 0xfd4);
      lVar5 = (ulonglong)uVar2 * 0x20;
      *(undefined4 *)(lVar5 + 4 + lVar3) = 0x48b;
      uVar4 = FUN_180269080(param_4,0);
      local_8040 = 0;
      local_8038 = 0;
      local_8030 = 0;
      local_8028 = 0;
      local_8020 = 0;
      local_8018 = 0;
      *(undefined4 *)((ulonglong)uVar2 * 0x20 + 8 + lVar3) = uVar4;
      *(undefined4 *)(lVar5 + 0x10 + lVar3) = param_3;
      FUN_1802695e0(local_8078,uVar4);
      local_8070 = local_8068;
    }
    *(undefined8 *)(lVar5 + 0x18 + lVar3) = local_8070;
  }
  return;
}



// ===================================================
// 1802694B3  ->  FUN_180269490  (entree 180269490)
// ===================================================

longlong FUN_180269490(int *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined4 *puVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  longlong lVar5;
  int *piVar6;
  longlong lVar7;
  longlong lVar8;
  undefined8 uVar9;
  
  lVar5 = DAT_180c4d590;
  uVar9 = 0xfffffffffffffffe;
  lVar7 = 0;
  lVar8 = lVar7;
  if ((*param_1 == 0x58465347) && (lVar8 = 0, 0x4ffff < (uint)param_1[2])) {
    puVar1 = (undefined4 *)(DAT_180c4d590 + 0x1c00);
    FUN_180286310();
    piVar6 = (int *)FUN_180269bd0(lVar5 + 0x16c8,param_1 + 4);
    if (piVar6 == (int *)0x0) {
      piVar6 = (int *)(**(code **)(**(longlong **)(DAT_180c4d590 + 0xb0) + 8))
                                (*(longlong **)(DAT_180c4d590 + 0xb0),0x40,0x10,param_4,uVar9);
      if (piVar6 != (int *)0x0) {
        *piVar6 = 1;
        piVar6[2] = 0;
        piVar6[3] = 0;
        uVar9 = *(undefined8 *)(param_1 + 6);
        uVar3 = *(undefined8 *)(param_1 + 8);
        uVar4 = *(undefined8 *)(param_1 + 10);
        *(undefined8 *)(piVar6 + 4) = *(undefined8 *)(param_1 + 4);
        *(undefined8 *)(piVar6 + 6) = uVar9;
        *(undefined8 *)(piVar6 + 8) = uVar3;
        *(undefined8 *)(piVar6 + 10) = uVar4;
        *(ulonglong *)(piVar6 + 0xc) = *(ulonglong *)(piVar6 + 0xc) & 0xffff000000000000;
        *(undefined2 *)((longlong)piVar6 + 0x36) = 0;
        *(ulonglong *)(piVar6 + 0xe) = *(ulonglong *)(piVar6 + 0xe) & 0xffff000000000000;
        *(undefined2 *)((longlong)piVar6 + 0x3e) = 0;
        lVar7 = FUN_180269750(piVar6,param_1);
        if ((lVar7 == 0) && (iVar2 = *piVar6, *piVar6 = iVar2 + -1, iVar2 + -1 == 0)) {
          FUN_1802691a0(piVar6);
          (**(code **)(**(longlong **)(DAT_180c4d590 + 0xb0) + 0x18))
                    (*(longlong **)(DAT_180c4d590 + 0xb0),piVar6);
        }
      }
    }
    else {
      LOCK();
      *piVar6 = *piVar6 + 1;
      UNLOCK();
      lVar7 = *(longlong *)(piVar6 + 2);
    }
    *puVar1 = 0;
    lVar8 = lVar7;
  }
  return lVar8;
}



// ===================================================
// 18027090E  ->  FUN_1802708e0  (entree 1802708e0)
// ===================================================

longlong * FUN_1802708e0(int *param_1,undefined8 param_2)

{
  ulonglong *puVar1;
  ulonglong uVar2;
  ulonglong uVar3;
  uint uVar4;
  longlong *plVar5;
  longlong *plVar6;
  int *piVar7;
  longlong *plVar8;
  longlong lVar9;
  longlong *plVar10;
  longlong *plVar11;
  longlong *plVar12;
  undefined2 local_res8;
  undefined2 uStackX_a;
  undefined2 uStackX_c;
  undefined2 uStackX_e;
  longlong local_res18;
  undefined8 uVar13;
  uint uStack_c4;
  undefined8 local_c0;
  
  lVar9 = DAT_180c4d590;
  uVar13 = 0xfffffffffffffffe;
  plVar8 = (longlong *)0x0;
  plVar10 = plVar8;
  if ((*param_1 == 0x58465347) && (plVar10 = (longlong *)0x0, 0x4ffff < (uint)param_1[2])) {
    local_res18 = 0;
    plVar5 = plVar8;
    if (param_1[0x11] != 0) {
      plVar5 = (longlong *)FUN_1802716a0((ulonglong)(uint)param_1[0x10] + (longlong)param_1);
    }
    plVar6 = plVar8;
    if (param_1[0x13] != 0) {
      uVar4 = param_1[0x12];
      plVar6 = (longlong *)
               FUN_180271c00((longlong)param_1 +
                             (ulonglong)*(uint *)((longlong)param_1 + (ulonglong)uVar4 + 0x10) +
                             (ulonglong)uVar4,param_2);
      local_res18 = FUN_180272160((longlong)param_1 +
                                  (ulonglong)*(uint *)((longlong)param_1 + (ulonglong)uVar4 + 0x18)
                                  + (ulonglong)uVar4,param_2);
    }
    local_res8 = SUB82(plVar5,0);
    uStackX_a = (undefined2)((ulonglong)plVar6 >> 0x10);
    uStackX_c = (undefined2)((ulonglong)local_res18 >> 0x20);
    uStackX_e = 0;
    uStack_c4 = 0;
    plVar10 = *(longlong **)(lVar9 + 0x16c0);
    plVar11 = plVar8;
    plVar12 = plVar8;
    if (plVar10 != (longlong *)0x0) {
      uVar3 = (ulonglong)CONCAT24(uStackX_c,CONCAT22(uStackX_a,local_res8));
      do {
        uVar2 = *(ulonglong *)
                 ((longlong)*(short *)((longlong)plVar10 + 0xe) + 0x10 + (longlong)plVar10);
        if (uVar3 < uVar2) {
          puVar1 = &local_c0 + (longlong)plVar12;
          *puVar1 = *puVar1 & 0xffff000000000000;
          *puVar1 = *puVar1 | (ulonglong)plVar10 & 0xffffffffffff;
          *(undefined2 *)((longlong)&local_c0 + (longlong)plVar12 * 8 + 6) = 0;
          lVar9 = *plVar10;
        }
        else {
          plVar11 = plVar10;
          if (uVar3 <= uVar2) break;
          puVar1 = &local_c0 + (longlong)plVar12;
          *puVar1 = *puVar1 & 0xffff000000000000;
          *puVar1 = *puVar1 | (ulonglong)plVar10 & 0xffffffffffff;
          *(undefined2 *)((longlong)&local_c0 + (longlong)plVar12 * 8 + 6) = 1;
          lVar9 = plVar10[1];
        }
        uStack_c4 = uStack_c4 + 1;
        plVar12 = (longlong *)(ulonglong)uStack_c4;
        plVar10 = (longlong *)((lVar9 << 0x10) >> 0x10);
        plVar11 = plVar8;
      } while (plVar10 != (longlong *)0x0);
    }
    plVar10 = plVar8;
    if (plVar11 != (longlong *)0x0) {
      plVar10 = (longlong *)((longlong)*(short *)((longlong)plVar11 + 0xe) + (longlong)plVar11);
    }
    if (plVar10 == (longlong *)0x0) {
      piVar7 = (int *)(**(code **)(**(longlong **)(DAT_180c4d590 + 0xb0) + 8))
                                (*(longlong **)(DAT_180c4d590 + 0xb0),0x40,0x10,plVar12,uVar13);
      plVar10 = plVar8;
      if (piVar7 != (int *)0x0) {
        *piVar7 = 1;
        piVar7[2] = 0;
        piVar7[3] = 0;
        piVar7[4] = 0;
        piVar7[5] = 0;
        piVar7[6] = 0;
        piVar7[7] = 0;
        piVar7[8] = 0;
        piVar7[9] = 0;
        piVar7[10] = 0;
        piVar7[0xb] = 0;
        *(ulonglong *)(piVar7 + 0xc) = *(ulonglong *)(piVar7 + 0xc) & 0xffff000000000000;
        *(undefined2 *)((longlong)piVar7 + 0x36) = 0;
        *(ulonglong *)(piVar7 + 0xe) = *(ulonglong *)(piVar7 + 0xe) & 0xffff000000000000;
        *(undefined2 *)((longlong)piVar7 + 0x3e) = 0;
        plVar10 = (longlong *)FUN_180270c50(piVar7,&local_res8);
        if ((plVar10 == (longlong *)0x0) && (*piVar7 = *piVar7 + -1, *piVar7 == 0)) {
          FUN_180270660(piVar7);
          (**(code **)(**(longlong **)(DAT_180c4d590 + 0xb0) + 0x18))
                    (*(longlong **)(DAT_180c4d590 + 0xb0),piVar7);
        }
      }
    }
    else {
      *(int *)plVar10 = (int)*plVar10 + 1;
      plVar10 = (longlong *)plVar10[1];
    }
    if (plVar5 != (longlong *)0x0) {
      uVar4 = ((uint)plVar5 & 0xffff) - 1;
      plVar5 = plVar8;
      if (uVar4 < *(uint *)(DAT_180c4d590 + 0x18e4)) {
        plVar5 = *(longlong **)(*(longlong *)(DAT_180c4d590 + 0x18d0) + (ulonglong)uVar4 * 8);
      }
      *(int *)plVar5 = (int)*plVar5 + -1;
      if ((int)*plVar5 == 0) {
        FUN_1802714c0(plVar5);
        (**(code **)(**(longlong **)(DAT_180c4d590 + 0xb0) + 0x18))
                  (*(longlong **)(DAT_180c4d590 + 0xb0),plVar5);
      }
    }
    if (plVar6 != (longlong *)0x0) {
      uVar4 = ((uint)((ulonglong)plVar6 >> 0x10) & 0xffff) - 1;
      plVar5 = plVar8;
      if (uVar4 < *(uint *)(DAT_180c4d590 + 0x1904)) {
        plVar5 = *(longlong **)(*(longlong *)(DAT_180c4d590 + 0x18f0) + (ulonglong)uVar4 * 8);
      }
      *(int *)plVar5 = (int)*plVar5 + -1;
      if ((int)*plVar5 == 0) {
        FUN_180271a20(plVar5);
        (**(code **)(**(longlong **)(DAT_180c4d590 + 0xb0) + 0x18))
                  (*(longlong **)(DAT_180c4d590 + 0xb0),plVar5);
      }
    }
    if (local_res18 != 0) {
      uVar4 = ((uint)((ulonglong)local_res18 >> 0x20) & 0xffff) - 1;
      if (uVar4 < *(uint *)(DAT_180c4d590 + 0x1924)) {
        plVar8 = *(longlong **)(*(longlong *)(DAT_180c4d590 + 0x1910) + (ulonglong)uVar4 * 8);
      }
      *(int *)plVar8 = (int)*plVar8 + -1;
      if ((int)*plVar8 == 0) {
        FUN_180271f80(plVar8);
        (**(code **)(**(longlong **)(DAT_180c4d590 + 0xb0) + 0x18))
                  (*(longlong **)(DAT_180c4d590 + 0xb0),plVar8);
      }
    }
  }
  return plVar10;
}



// ===================================================
// 1802716CD  ->  FUN_1802716a0  (entree 1802716a0)
// ===================================================

/* WARNING: Type propagation algorithm not settling */

ulonglong FUN_1802716a0(int *param_1)

{
  ulonglong *puVar1;
  int iVar2;
  int iVar3;
  ushort uVar4;
  uint uVar5;
  int iVar6;
  longlong *plVar7;
  longlong *plVar8;
  uint *puVar9;
  uint uVar10;
  longlong *plVar11;
  ulonglong uVar12;
  longlong *plVar13;
  longlong lVar14;
  longlong *plVar15;
  longlong lVar16;
  uint uStack_b4;
  undefined8 local_b0;
  
  plVar11 = (longlong *)0x0;
  if (*param_1 != 0x53475347) {
    return 0;
  }
  if ((uint)param_1[2] < 0x50001) {
    return 0;
  }
  lVar16 = 0x10;
  uStack_b4 = 0;
  plVar7 = *(longlong **)(DAT_180c4d590 + 0x16a0);
  plVar8 = plVar11;
  while (plVar15 = plVar11, plVar7 != (longlong *)0x0) {
    puVar9 = (uint *)(param_1 + 8);
    plVar13 = plVar11;
    while( true ) {
      uVar10 = *puVar9;
      uVar5 = uVar10 >> 0x18 | (uVar10 & 0xff0000) >> 8 | (uVar10 & 0xff00) << 8 | uVar10 << 0x18;
      uVar10 = *(uint *)((longlong)plVar7 +
                         ((longlong)*(short *)((longlong)plVar7 + 0xe) - (longlong)param_1) + 0x58 +
                        (longlong)puVar9);
      uVar10 = uVar10 >> 0x18 | (uVar10 & 0xff0000) >> 8 | (uVar10 & 0xff00) << 8 | uVar10 << 0x18;
      if (uVar10 >= uVar5 && uVar10 != uVar5) break;
      if (uVar10 < uVar5) {
        puVar1 = &local_b0 + (longlong)plVar8;
        *puVar1 = *puVar1 & 0xffff000000000000;
        *puVar1 = *puVar1 | (ulonglong)plVar7 & 0xffffffffffff;
        *(undefined2 *)((longlong)&local_b0 + (longlong)plVar8 * 8 + 6) = 1;
        lVar14 = plVar7[1];
        goto LAB_1802717b4;
      }
      uVar10 = (int)plVar13 + 1;
      plVar13 = (longlong *)(ulonglong)uVar10;
      puVar9 = puVar9 + 1;
      plVar15 = plVar7;
      if (3 < uVar10) goto LAB_1802717ce;
    }
    puVar1 = &local_b0 + (longlong)plVar8;
    *puVar1 = *puVar1 & 0xffff000000000000;
    *puVar1 = *puVar1 | (ulonglong)plVar7 & 0xffffffffffff;
    *(undefined2 *)((longlong)&local_b0 + (longlong)plVar8 * 8 + 6) = 0;
    lVar14 = *plVar7;
LAB_1802717b4:
    uStack_b4 = uStack_b4 + 1;
    plVar8 = (longlong *)(ulonglong)uStack_b4;
    plVar7 = (longlong *)((lVar14 << 0x10) >> 0x10);
  }
LAB_1802717ce:
  plVar7 = plVar11;
  if (plVar15 != (longlong *)0x0) {
    plVar7 = (longlong *)((longlong)*(short *)((longlong)plVar15 + 0xe) + (longlong)plVar15);
  }
  if (plVar7 != (longlong *)0x0) {
    *(int *)plVar7 = (int)*plVar7 + 1;
    return plVar7[2];
  }
  plVar8 = (longlong *)
           (**(code **)(**(longlong **)(DAT_180c4d590 + 0xb0) + 8))
                     (*(longlong **)(DAT_180c4d590 + 0xb0),0xb0,0x10,plVar15,0xfffffffffffffffe);
  plVar7 = plVar11;
  if (plVar8 != (longlong *)0x0) {
    *plVar8 = 1;
    plVar8[1] = 0;
    plVar8[2] = 0;
    plVar7 = plVar8 + 3;
    do {
      FUN_18000fa90(plVar7);
      plVar7 = (longlong *)((longlong)plVar7 + 4);
      lVar16 = lVar16 + -1;
    } while (lVar16 != 0);
    plVar8[0xb] = 0;
    *(int *)(plVar8 + 0xc) = 0;
    plVar8[0xd] = plVar8[0xd] & 0xffff000000000000;
    *(undefined2 *)((longlong)plVar8 + 0x6e) = 0;
    plVar8[0xe] = plVar8[0xe] & 0xffff000000000000;
    *(undefined2 *)((longlong)plVar8 + 0x76) = 0;
    plVar8[0xf] = 0;
    plVar8[0x10] = 0;
    *(int *)(plVar8 + 0x11) = -1;
    plVar8[0x12] = 0;
    plVar8[0x13] = 0;
    plVar8[0x14] = 0;
    plVar8[0x15] = 0;
    plVar7 = plVar8;
  }
  if (plVar7 == (longlong *)0x0) {
    return 0;
  }
  uVar4 = FUN_180264d00(DAT_180c4d590 + 0x18d0,plVar7);
  uVar12 = (ulonglong)uVar4;
  if (uVar12 != 0) {
    plVar7[2] = uVar12;
    plVar7[1] = *(longlong *)(param_1 + 4);
    iVar6 = param_1[9];
    iVar2 = param_1[10];
    iVar3 = param_1[0xb];
    *(int *)(plVar7 + 0xf) = param_1[8];
    *(int *)((longlong)plVar7 + 0x7c) = iVar6;
    *(int *)(plVar7 + 0x10) = iVar2;
    *(int *)((longlong)plVar7 + 0x84) = iVar3;
    *(int *)((longlong)plVar7 + 4) = param_1[0xc];
    if ((*(ulonglong *)(param_1 + 4) & 0xf00000000) != 0) {
      do {
        *(int *)((longlong)plVar7 + (longlong)plVar11 * 4 + 0x18) = param_1[(longlong)(plVar11 + 2)]
        ;
        plVar11 = (longlong *)(ulonglong)((int)plVar11 + 1);
      } while (plVar11 < (longlong *)
                         (ulonglong)((uint)((ulonglong)*(undefined8 *)(param_1 + 4) >> 0x20) & 0xf))
      ;
    }
    iVar6 = FUN_18026ff50(plVar7 + 0xb,(ulonglong)(uint)param_1[6] + (longlong)param_1,param_1[7],0)
    ;
    lVar16 = DAT_180c4d590;
    if (iVar6 < 0) {
      uVar10 = uVar4 - 1;
      if (uVar10 < *(uint *)(DAT_180c4d590 + 0x18e4)) {
        uVar5 = uVar10 >> 6;
        *(undefined8 *)(*(longlong *)(DAT_180c4d590 + 0x18d0) + (ulonglong)uVar10 * 8) = 0;
        puVar1 = (ulonglong *)(*(longlong *)(lVar16 + 0x18d8) + (ulonglong)uVar5 * 8);
        *puVar1 = *puVar1 | 1L << ((ulonglong)(0x3f - (uVar10 & 0x3f)) & 0x3f);
        if (uVar5 < *(uint *)(lVar16 + 0x18e8)) {
          *(uint *)(lVar16 + 0x18e8) = uVar5;
        }
      }
      plVar7[2] = 0;
      goto LAB_1802719c5;
    }
    FUN_180268ee0(DAT_180c4d590 + 0x16a0,plVar7);
  }
  if (uVar12 != 0) {
    return uVar12;
  }
LAB_1802719c5:
  *(int *)plVar7 = (int)*plVar7 + -1;
  if ((int)*plVar7 == 0) {
    FUN_1802714c0(plVar7);
    (**(code **)(**(longlong **)(DAT_180c4d590 + 0xb0) + 0x18))
              (*(longlong **)(DAT_180c4d590 + 0xb0),plVar7);
  }
  return 0;
}



