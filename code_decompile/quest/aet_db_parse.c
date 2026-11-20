// ===================================================
// 1800268A0  ->  FUN_1800268a0  (entree 1800268a0)
// ===================================================

void FUN_1800268a0(longlong param_1,int *param_2)

{
  int *piVar1;
  int *piVar2;
  longlong *plVar3;
  longlong *plVar4;
  longlong *plVar5;
  longlong *plVar6;
  uint *puVar7;
  longlong lVar8;
  ulonglong uVar9;
  int iVar10;
  int iVar11;
  int *piVar12;
  int *piVar13;
  longlong lVar14;
  ulonglong uVar15;
  ulonglong uVar16;
  longlong lVar17;
  longlong lVar18;
  uint uVar19;
  ulonglong uVar20;
  longlong *plVar21;
  uint local_118;
  undefined4 uStack_114;
  uint local_110;
  undefined4 uStack_10c;
  undefined1 local_108 [8];
  ulonglong local_100;
  ulonglong local_f8;
  undefined1 local_f0;
  undefined7 uStack_ef;
  uint local_e8;
  undefined8 local_e0;
  ulonglong local_d8;
  uint local_d0;
  uint local_cc;
  uint local_c8;
  uint local_c0;
  undefined4 uStack_bc;
  undefined1 local_b8 [8];
  undefined8 local_b0;
  ulonglong local_a8;
  uint local_a0;
  undefined1 local_98 [32];
  uint local_78;
  uint local_74;
  longlong *local_70;
  int *local_68;
  uint *local_60;
  uint *local_58;
  undefined8 local_50;
  
  local_50 = 0xfffffffffffffffe;
  piVar1 = param_2 + 1;
  uVar20 = 0;
  iVar11 = 0;
  if (*piVar1 != 0) {
    lVar8 = (longlong)*piVar1 + (longlong)param_2;
    iVar10 = iVar11;
    if (lVar8 != 0) {
      iVar10 = (int)lVar8 - (int)piVar1;
    }
    *piVar1 = iVar10;
  }
  piVar2 = param_2 + 3;
  if (*piVar2 != 0) {
    lVar8 = (longlong)*piVar2 + (longlong)param_2;
    if (lVar8 != 0) {
      iVar11 = (int)lVar8 - (int)piVar2;
    }
    *piVar2 = iVar11;
  }
  iVar11 = *param_2;
  iVar10 = 0;
  uVar15 = uVar20;
  uVar16 = uVar20;
  if (0 < iVar11) {
    do {
      uVar9 = uVar20;
      if (*piVar1 != 0) {
        uVar9 = (longlong)piVar1 + (longlong)*piVar1;
      }
      piVar13 = (int *)(uVar9 + 4 + uVar15);
      if (*piVar13 != 0) {
        lVar8 = (longlong)*piVar13 + (longlong)param_2;
        iVar11 = iVar10;
        if (lVar8 != 0) {
          iVar11 = (int)lVar8 - (int)piVar13;
        }
        *piVar13 = iVar11;
      }
      uVar9 = uVar20;
      if (*piVar1 != 0) {
        uVar9 = (longlong)piVar1 + (longlong)*piVar1;
      }
      piVar13 = (int *)(uVar9 + 8 + uVar15);
      if (*piVar13 != 0) {
        lVar8 = (longlong)*piVar13 + (longlong)param_2;
        iVar11 = iVar10;
        if (lVar8 != 0) {
          iVar11 = (int)lVar8 - (int)piVar13;
        }
        *piVar13 = iVar11;
      }
      uVar19 = (int)uVar16 + 1;
      iVar11 = *param_2;
      uVar15 = uVar15 + 0x14;
      uVar16 = (ulonglong)uVar19;
    } while ((int)uVar19 < iVar11);
  }
  piVar13 = param_2 + 2;
  uVar15 = uVar20;
  uVar16 = uVar20;
  if (0 < *piVar13) {
    do {
      uVar9 = uVar20;
      if (*piVar2 != 0) {
        uVar9 = (longlong)piVar2 + (longlong)*piVar2;
      }
      piVar12 = (int *)(uVar9 + 4 + uVar16);
      if (*piVar12 != 0) {
        lVar8 = (longlong)*piVar12 + (longlong)param_2;
        iVar11 = iVar10;
        if (lVar8 != 0) {
          iVar11 = (int)lVar8 - (int)piVar12;
        }
        *piVar12 = iVar11;
      }
      uVar19 = (int)uVar15 + 1;
      uVar15 = (ulonglong)uVar19;
      uVar16 = uVar16 + 0xc;
    } while ((int)uVar19 < *piVar13);
    iVar11 = *param_2;
  }
  uVar20 = (ulonglong)iVar11;
  plVar3 = (longlong *)(param_1 + 0x90);
  local_68 = piVar13;
  if ((ulonglong)((*(longlong *)(param_1 + 0xa0) - *plVar3) / 0x58) < uVar20) {
    if (0x2e8ba2e8ba2e8ba < uVar20) {
                    /* WARNING: Subroutine does not return */
      FUN_180010340();
    }
    FUN_180022b30(plVar3,uVar20);
    iVar11 = *param_2;
  }
  uVar20 = (ulonglong)iVar11;
  plVar4 = (longlong *)(param_1 + 0xb0);
  if ((ulonglong)((*(longlong *)(param_1 + 0xc0) - *plVar4) / 0x58) < uVar20) {
    if (0x2e8ba2e8ba2e8ba < uVar20) {
                    /* WARNING: Subroutine does not return */
      FUN_180010340();
    }
    FUN_180022b30(plVar4,uVar20);
  }
  iVar11 = *piVar13;
  uVar20 = (ulonglong)iVar11;
  plVar5 = (longlong *)(param_1 + 0xd0);
  if ((ulonglong)((*(longlong *)(param_1 + 0xe0) - *plVar5) / 0x38) < uVar20) {
    if (0x492492492492492 < uVar20) {
                    /* WARNING: Subroutine does not return */
      FUN_180010340();
    }
    FUN_180022bc0(plVar5,uVar20);
    iVar11 = *piVar13;
  }
  uVar20 = (ulonglong)iVar11;
  plVar6 = (longlong *)(param_1 + 0xf0);
  if ((ulonglong)((*(longlong *)(param_1 + 0x100) - *plVar6) / 0x50) < uVar20) {
    if (0x333333333333333 < uVar20) {
                    /* WARNING: Subroutine does not return */
      FUN_180010340();
    }
    FUN_180022c50(plVar6,uVar20);
    iVar11 = *piVar13;
  }
  uVar20 = (ulonglong)iVar11;
  plVar21 = (longlong *)(param_1 + 0x110);
  local_70 = plVar21;
  if ((ulonglong)((*(longlong *)(param_1 + 0x120) - *plVar21) / 0x38) < uVar20) {
    if (0x492492492492492 < uVar20) {
                    /* WARNING: Subroutine does not return */
      FUN_180010340();
    }
    FUN_180022bc0(plVar21,uVar20);
  }
  lVar8 = 0;
  iVar11 = 0;
  if (0 < *param_2) {
    do {
      lVar14 = 0;
      local_100 = 0;
      local_f8 = 0xf;
      local_110 = local_110 & 0xffffff00;
      local_e0 = 0;
      local_d8 = 0xf;
      local_f0 = 0;
      iVar10 = *piVar1;
      lVar17 = lVar14;
      if (iVar10 != 0) {
        lVar17 = (longlong)piVar1 + (longlong)iVar10;
      }
      local_118 = *(uint *)(lVar8 + lVar17);
      lVar17 = (longlong)iVar10;
      if (iVar10 == 0) {
        lVar17 = lVar14;
      }
      lVar17 = (longlong)param_2 + lVar17 + 8;
      if (iVar10 == 0) {
        lVar17 = 4;
      }
      iVar10 = *(int *)(lVar17 + lVar8);
      if (iVar10 != 0) {
        lVar14 = lVar17 + lVar8 + (longlong)iVar10;
      }
      lVar17 = -1;
      do {
        lVar17 = lVar17 + 1;
      } while (*(char *)(lVar14 + lVar17) != '\0');
      FUN_180010a10(&local_110);
      lVar14 = 0;
      lVar17 = lVar14;
      if (*piVar1 != 0) {
        lVar17 = (longlong)piVar1 + (longlong)*piVar1;
      }
      piVar13 = (int *)(lVar17 + 8 + lVar8);
      iVar10 = *piVar13;
      lVar17 = lVar14;
      if (iVar10 != 0) {
        lVar17 = (longlong)piVar13 + (longlong)iVar10;
      }
      lVar18 = -1;
      do {
        lVar18 = lVar18 + 1;
      } while (*(char *)(lVar17 + lVar18) != '\0');
      FUN_180010a10(&local_f0);
      iVar10 = *piVar1;
      lVar17 = lVar14;
      if (iVar10 != 0) {
        lVar17 = (longlong)piVar1 + (longlong)iVar10;
      }
      local_d0 = *(uint *)(lVar8 + 0xc + lVar17);
      lVar17 = (longlong)iVar10;
      if (iVar10 == 0) {
        lVar17 = lVar14;
      }
      lVar17 = (longlong)param_2 + lVar17 + 0x14;
      if (iVar10 == 0) {
        lVar17 = 0x10;
      }
      local_cc = *(uint *)(lVar17 + lVar8);
      local_c8 = local_118;
      local_60 = &local_c0;
      local_c0 = local_118;
      FUN_18000d770(local_b8,&local_110);
      FUN_18000d770(local_98,&local_f0);
      uVar19 = local_d0;
      local_78 = local_d0;
      local_74 = local_cc;
      puVar7 = *(uint **)(param_1 + 0x98);
      if (*(uint **)(param_1 + 0xa0) == puVar7) {
        FUN_18001aa60(plVar3);
      }
      else {
        *puVar7 = local_c8;
        local_58 = puVar7 + 2;
        *local_58 = local_c0;
        FUN_18000d770(puVar7 + 4,local_b8);
        FUN_18000d770(puVar7 + 0xc,local_98);
        puVar7[0x14] = local_78;
        puVar7[0x15] = local_74;
        *(longlong *)(param_1 + 0x98) = *(longlong *)(param_1 + 0x98) + 0x58;
      }
      FUN_180021560(&local_c0);
      local_c8 = uVar19;
      local_60 = &local_c0;
      local_c0 = local_118;
      FUN_18000d770(local_b8,&local_110);
      FUN_18000d770(local_98,&local_f0);
      local_78 = local_d0;
      local_74 = local_cc;
      puVar7 = *(uint **)(param_1 + 0xb8);
      if (*(uint **)(param_1 + 0xc0) == puVar7) {
        FUN_18001aa60(plVar4);
      }
      else {
        *puVar7 = local_c8;
        puVar7[2] = local_c0;
        FUN_18000d770(puVar7 + 4,local_b8);
        FUN_18000d770(puVar7 + 0xc,local_98);
        puVar7[0x14] = local_78;
        puVar7[0x15] = local_74;
        *(longlong *)(param_1 + 0xb8) = *(longlong *)(param_1 + 0xb8) + 0x58;
      }
      FUN_180021560(&local_c0);
      if (0xf < local_d8) {
        if (0xfff < local_d8 + 1) {
          lVar17 = *(longlong *)(CONCAT71(uStack_ef,local_f0) + -8);
          if (0x1f < (CONCAT71(uStack_ef,local_f0) - lVar17) - 8U) {
                    /* WARNING: Subroutine does not return */
            FUN_180303af0(lVar17,local_d8 + 0x28);
          }
        }
        FUN_1802fdd80();
      }
      if (0xf < local_f8) {
        if (0xfff < local_f8 + 1) {
          lVar17 = *(longlong *)(CONCAT44(uStack_10c,local_110) + -8);
          if (0x1f < (CONCAT44(uStack_10c,local_110) - lVar17) - 8U) {
                    /* WARNING: Subroutine does not return */
            FUN_180303af0(lVar17,local_f8 + 0x28);
          }
        }
        FUN_1802fdd80();
      }
      iVar11 = iVar11 + 1;
      lVar8 = lVar8 + 0x14;
      plVar21 = local_70;
    } while (iVar11 < *param_2);
  }
  uVar15 = 0;
  uVar20 = uVar15;
  if (0 < param_2[2]) {
    do {
      lVar17 = 0;
      local_b0 = 0;
      local_a8 = 0xf;
      local_c0 = local_c0 & 0xffffff00;
      iVar11 = *piVar2;
      lVar8 = lVar17;
      if (iVar11 != 0) {
        lVar8 = (longlong)piVar2 + (longlong)iVar11;
      }
      local_c8 = *(uint *)(lVar8 + uVar15);
      lVar8 = (longlong)iVar11;
      if (iVar11 == 0) {
        lVar8 = lVar17;
      }
      lVar8 = (longlong)param_2 + lVar8 + 0x10;
      if (iVar11 == 0) {
        lVar8 = 4;
      }
      iVar11 = *(int *)(lVar8 + uVar15);
      if (iVar11 != 0) {
        lVar17 = (longlong)(lVar8 + uVar15) + (longlong)iVar11;
      }
      lVar8 = -1;
      do {
        lVar8 = lVar8 + 1;
      } while (*(char *)(lVar17 + lVar8) != '\0');
      FUN_180010a10(&local_c0);
      lVar8 = 0;
      if (*piVar2 != 0) {
        lVar8 = (longlong)piVar2 + (longlong)*piVar2;
      }
      local_a0 = *(uint *)(lVar8 + 8 + uVar15);
      local_118 = local_c8;
      local_110 = local_c8;
      FUN_18000d770(local_108,&local_c0);
      local_e8 = local_a0;
      puVar7 = *(uint **)(param_1 + 0xd8);
      if (*(uint **)(param_1 + 0xe0) == puVar7) {
        FUN_18001ac10(plVar5);
      }
      else {
        *puVar7 = local_118;
        puVar7[2] = local_110;
        FUN_18000d770(puVar7 + 4,local_108);
        puVar7[0xc] = local_e8;
        *(longlong *)(param_1 + 0xd8) = *(longlong *)(param_1 + 0xd8) + 0x38;
      }
      FUN_180021610(&local_110);
      FUN_18000d770(&local_118,&local_c0);
      local_f8 = CONCAT44(local_f8._4_4_,local_c8);
      FUN_18000d770(&local_f0,&local_c0);
      uVar19 = local_a0;
      local_d0 = local_a0;
      lVar8 = *(longlong *)(param_1 + 0xf8);
      if (*(longlong *)(param_1 + 0x100) == lVar8) {
        FUN_18001adc0(plVar6,lVar8);
      }
      else {
        FUN_18000d770(lVar8,&local_118);
        local_58 = (uint *)(lVar8 + 0x20);
        *local_58 = (uint)local_f8;
        FUN_18000d770(lVar8 + 0x28,&local_f0);
        *(uint *)(lVar8 + 0x48) = local_d0;
        *(longlong *)(param_1 + 0xf8) = *(longlong *)(param_1 + 0xf8) + 0x50;
      }
      FUN_180021610(&local_f8);
      if (0xf < local_100) {
        if (0xfff < local_100 + 1) {
          lVar8 = *(longlong *)(CONCAT44(uStack_114,local_118) + -8);
          if (0x1f < (CONCAT44(uStack_114,local_118) - lVar8) - 8U) {
                    /* WARNING: Subroutine does not return */
            FUN_180303af0(lVar8,local_100 + 0x28);
          }
        }
        FUN_1802fdd80();
      }
      local_118 = uVar19;
      local_110 = local_c8;
      FUN_18000d770(local_108,&local_c0);
      local_e8 = local_a0;
      puVar7 = (uint *)plVar21[1];
      if ((uint *)plVar21[2] == puVar7) {
        FUN_18001ac10(plVar21);
      }
      else {
        *puVar7 = local_118;
        puVar7[2] = local_110;
        FUN_18000d770(puVar7 + 4,local_108);
        puVar7[0xc] = local_e8;
        plVar21[1] = plVar21[1] + 0x38;
      }
      FUN_180021610(&local_110);
      if (0xf < local_a8) {
        if (0xfff < local_a8 + 1) {
          lVar8 = *(longlong *)(CONCAT44(uStack_bc,local_c0) + -8);
          if (0x1f < (CONCAT44(uStack_bc,local_c0) - lVar8) - 8U) {
                    /* WARNING: Subroutine does not return */
            FUN_180303af0(lVar8,local_a8 + 0x28);
          }
        }
        FUN_1802fdd80();
      }
      uVar19 = (int)uVar20 + 1;
      uVar15 = uVar15 + 0xc;
      uVar20 = (ulonglong)uVar19;
    } while ((int)uVar19 < *local_68);
  }
  FUN_18001f320(*plVar3,*(longlong *)(param_1 + 0x98),
                (*(longlong *)(param_1 + 0x98) - *plVar3) / 0x58,0);
  FUN_18001f320(*plVar4,*(longlong *)(param_1 + 0xb8),
                (*(longlong *)(param_1 + 0xb8) - *plVar4) / 0x58,0);
  FUN_18001f6d0(*plVar5,*(undefined8 *)(param_1 + 0xd8),
                (*(longlong *)(param_1 + 0xd8) - *plVar5) / 0x38,0);
  FUN_18001ff30(*plVar6,*(longlong *)(param_1 + 0xf8),
                (*(longlong *)(param_1 + 0xf8) - *plVar6) / 0x50,0);
  FUN_18001f6d0(*plVar21,plVar21[1],(plVar21[1] - *plVar21) / 0x38,0);
  return;
}



