// ===================================================
// 18018B0C3  ->  FUN_18018b010  (entree 18018b010)
// ===================================================

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18018b010(int *param_1)

{
  undefined4 uVar1;
  int iVar2;
  int iVar3;
  char cVar4;
  uint uVar5;
  int iVar6;
  undefined8 *puVar7;
  undefined4 *puVar8;
  longlong lVar9;
  undefined8 uVar10;
  longlong lVar11;
  int iVar12;
  longlong *plVar13;
  ulonglong uVar14;
  int iVar15;
  int *piVar16;
  float fVar17;
  undefined1 auVar18 [64];
  undefined8 unaff_XMM7_Qa;
  undefined8 unaff_XMM7_Qb;
  undefined1 auVar19 [64];
  undefined8 unaff_XMM8_Qa;
  undefined8 unaff_XMM8_Qb;
  undefined1 auVar20 [64];
  undefined8 local_res8;
  float local_res10;
  float local_res14;
  undefined1 local_158 [32];
  undefined1 local_138 [16];
  longlong local_128;
  undefined8 local_120 [23];
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_58;
  undefined8 uStack_50;
  
  local_138._0_12_ = ZEXT812(0);
  local_138._12_4_ = 0;
  puVar7 = local_120 + 1;
  local_158 = ZEXT1232(ZEXT812(0));
  lVar9 = 4;
  do {
    puVar7[-1] = 0;
    *puVar7 = 0;
    puVar7[1] = 0;
    puVar7[2] = 0;
    puVar7 = puVar7 + 6;
    lVar9 = lVar9 + -1;
  } while (lVar9 != 0);
  if (*param_1 == 1) {
    return;
  }
  FUN_180247010(*(undefined1 *)((longlong)param_1 + 10),*(undefined1 *)((longlong)param_1 + 9),
                (char)param_1[2],*(undefined1 *)((longlong)param_1 + 0xb));
  fVar17 = 0.0;
  piVar16 = param_1;
  do {
    uVar1 = *(undefined4 *)(DAT_180719900 + 0x830);
    if (piVar16[8] != 0x11) {
      FUN_18016af60(piVar16 + 0xd,uVar1,piVar16 + 0xd);
      iVar6 = piVar16[8];
      local_res10 = fVar17;
      local_res14 = fVar17;
      puVar8 = (undefined4 *)FUN_18016b0c0();
      FUN_18016b0a0(&local_res10,*puVar8,iVar6);
      piVar16[0xf] = (int)(local_res14 * (float)piVar16[0xf]);
      piVar16[0x1f] = piVar16[0x1f];
      piVar16[0x23] = (int)(local_res14 * (float)piVar16[0x23]);
      if (*(longlong *)(piVar16 + 0x2e) != 0) {
        lVar11 = *(longlong *)(piVar16 + 0x2c);
        lVar9 = lVar11 + *(longlong *)(piVar16 + 0x2e) * 0x18;
        for (; lVar11 != lVar9; lVar11 = lVar11 + 0x18) {
          FUN_18016af60(lVar11,uVar1,lVar11,piVar16[8]);
        }
      }
    }
    if (piVar16[9] != 0x11) {
      local_res8 = CONCAT44(fVar17,fVar17);
      FUN_18016b0a0(&local_res8,uVar1);
      piVar16[0x10] = (int)((float)local_res8 * (float)piVar16[0x10]);
      piVar16[0x11] = (int)(local_res8._4_4_ * (float)piVar16[0x11]);
    }
    piVar16 = *(int **)(piVar16 + 0x38);
  } while (piVar16 != (int *)0x0);
  uVar5 = param_1[0x30];
  if ((uVar5 & 1) != 0) {
    FUN_18018aa60(param_1,local_158,0);
    uVar5 = param_1[0x30];
  }
  iVar6 = 0;
  if (((uVar5 & 2) != 0) && (iVar6 = 0, *(longlong *)(param_1 + 0x28) != 0)) {
    iVar6 = FUN_18018a740(param_1,&local_128,local_158);
  }
  if ((param_1[3] & 0x20000000U) == 0) {
    if (DAT_1807499b4 == '\0') {
      FUN_18024e900(0xac);
      DAT_1807499b4 = '\x01';
    }
    lVar9 = (longlong)param_1[4] * 0x10;
    cVar4 = FUN_18010bed0(10);
    if (((cVar4 == '\0') || (iVar15 = FUN_18010beb0(), iVar15 < 0xb)) || (1 < (uint)param_1[4])) {
      iVar15 = *(int *)(&DAT_18064955c + lVar9);
      iVar12 = *(int *)(&DAT_180649558 + lVar9);
      iVar3 = *(int *)(&DAT_180649554 + lVar9);
      iVar2 = *(int *)(&DAT_180649550 + lVar9);
      if (((DAT_1807499b8 != iVar2) || (DAT_1807499c0 != iVar3)) ||
         ((DAT_1807499bc != iVar12 || (DAT_1807499c4 != iVar15)))) {
        FUN_18024e370(iVar2,iVar3,iVar12,iVar15);
        DAT_1807499b8 = iVar2;
        DAT_1807499bc = iVar12;
        DAT_1807499c0 = iVar3;
        DAT_1807499c4 = iVar15;
      }
    }
    else {
      iVar15 = *(int *)(&DAT_180649554 + lVar9);
      iVar12 = *(int *)(&DAT_180649550 + lVar9);
      if (((DAT_1807499b8 != iVar12) || (DAT_1807499c0 != iVar15)) ||
         ((DAT_1807499bc != 1 || (DAT_1807499c4 != 0x20)))) {
        FUN_18024e370(iVar12,iVar15,1);
        DAT_1807499bc = 1;
        DAT_1807499c4 = 0x20;
        DAT_1807499b8 = iVar12;
        DAT_1807499c0 = iVar15;
      }
    }
  }
  else if (DAT_1807499b4 == '\x01') {
    FUN_18024e8d0(0xac);
    DAT_1807499b4 = '\0';
  }
  iVar15 = param_1[0x2b];
  if (iVar15 == 0) {
    param_1[0x2b] = 0x2f;
    if ((DAT_180749980 != 0x2f) || (DAT_1807499c8 != iVar6)) {
      if (iVar6 < 2) {
        if (iVar6 < 1) {
          DAT_180715460._0_4_ = 0;
          iVar15 = (int)DAT_180715460;
        }
        else {
          DAT_180715460._0_4_ = 1;
          DAT_180715458 = CONCAT44(1,(undefined4)DAT_180715458);
          iVar15 = (int)DAT_180715460;
        }
      }
      else {
        DAT_180715458 = 0;
        DAT_180715450 = 0;
        iVar15 = iVar6;
        if (((iVar6 != 2) && (iVar6 != 3)) && (iVar15 = (int)DAT_180715460, iVar6 == 4)) {
          iVar15 = iVar6;
        }
      }
      DAT_180715460._0_4_ = iVar15;
      FUN_180175970(0x2f);
      DAT_180749980 = 0x2f;
      DAT_1807499c8 = iVar6;
LAB_18018b411:
      FUN_180252390();
    }
  }
  else if (DAT_180749980 != iVar15) {
    FUN_180175970(iVar15);
    DAT_1807499c8 = -1;
    DAT_180749980 = iVar15;
    goto LAB_18018b411;
  }
  if (1 < iVar6) {
    lVar9 = (longlong)iVar6;
    iVar15 = 0x21d;
    auVar18 = ZEXT464(DAT_1804033c0);
    if (0 < iVar6) {
      local_58 = unaff_XMM7_Qa;
      uStack_50 = unaff_XMM7_Qb;
      plVar13 = &local_128;
      auVar19 = ZEXT464(DAT_1804033c4);
      local_68 = unaff_XMM8_Qa;
      uStack_60 = unaff_XMM8_Qb;
      iVar12 = 0x21d;
      auVar20 = ZEXT464(DAT_1804033bc);
      local_res8 = lVar9;
      do {
        if (DAT_180749984 != iVar12) {
          FUN_180256d50(iVar12);
          DAT_180749988 = iVar12 + -0x21d;
          DAT_180749984 = iVar12;
        }
        lVar11 = *plVar13;
        if (*(int *)(lVar11 + 0x14) == 0x39a) {
          FUN_18024e900(0x39a);
          FUN_180256da0(0x39a,*(undefined4 *)(*plVar13 + 0x10));
        }
        else {
          if ((&DAT_18074998c)[DAT_180749988] == '\0') {
            FUN_18024e900(0x11e);
            lVar11 = *plVar13;
            (&DAT_18074998c)[DAT_180749988] = 1;
          }
          iVar3 = *(int *)(lVar11 + 0x10);
          if ((&DAT_180749994)[DAT_180749988] != iVar3) {
            FUN_180256da0(0x11e,iVar3);
            (&DAT_180749994)[DAT_180749988] = iVar3;
          }
          FUN_180257560(0x11e,0x142,&DAT_1804033a0);
          FUN_1802575a0(0x11e,0x1b3,599);
          FUN_1802575a0(0x11e,0x1b4,599);
          FUN_180257360(0x1a4,0x1a2,auVar19._0_8_);
          FUN_180257360(0x1a4,0x265,auVar20._0_8_);
          FUN_180257360(0x1a4,0x266,auVar18._0_8_);
        }
        iVar12 = iVar12 + 1;
        plVar13 = plVar13 + 6;
        local_res8 = local_res8 + -1;
      } while (local_res8 != 0);
      local_res8 = 0;
    }
    iVar12 = 0;
    if (0 < iVar6) {
      do {
        FUN_180246fa0(iVar12 + 0x21d);
        FUN_1802473b0(0x12f);
        FUN_180247500(2,0x161,8,local_120 + (longlong)iVar12 * 6);
        iVar12 = iVar12 + 1;
      } while (iVar12 < iVar6);
    }
    FUN_180247600(3,0x161,0xc,local_158);
    FUN_180247230(9,0,4);
    iVar12 = 0;
    if (0 < iVar6) {
      do {
        FUN_180246fa0(iVar12 + 0x21d);
        FUN_180247100(0x12f);
        iVar12 = iVar12 + 1;
      } while (iVar12 < iVar6);
    }
    FUN_180246fa0(0x21d);
    FUN_1802473b0(0x12f);
    FUN_180247500(2,0x161,8,&DAT_180749950);
    FUN_180247600(3,0x161,0xc,&DAT_180749920);
    if (0 < iVar6) {
      plVar13 = &local_128;
      do {
        if (DAT_180749984 != iVar15) {
          FUN_180256d50(iVar15);
          DAT_180749988 = iVar15 + -0x21d;
          DAT_180749984 = iVar15;
        }
        if (*(int *)(*plVar13 + 0x14) == 0x39a) {
          FUN_180256da0(0x39a,0);
          FUN_18024e8d0(0x39a);
        }
        else {
          if ((&DAT_18074998c)[DAT_180749988] == '\x01') {
            FUN_18024e8d0(0x11e);
            (&DAT_18074998c)[DAT_180749988] = 0;
          }
          if ((&DAT_180749994)[DAT_180749988] != 0) {
            FUN_180256da0(0x11e,0);
            (&DAT_180749994)[DAT_180749988] = 0;
          }
          FUN_180257360(0x1a4,0x1a2,auVar18._0_8_);
        }
        iVar15 = iVar15 + 1;
        plVar13 = plVar13 + 6;
        lVar9 = lVar9 + -1;
      } while (lVar9 != 0);
    }
    goto LAB_18018bb8d;
  }
  if (0 < iVar6) {
    if (DAT_180749984 != 0x21d) {
      FUN_180256d50(0x21d);
      DAT_180749984 = 0x21d;
      DAT_180749988 = 0;
    }
    if (*(int *)(local_128 + 0x14) == 0x39a) {
      FUN_18024e900(0x39a);
      FUN_180256da0(0x39a,*(undefined4 *)(local_128 + 0x10));
    }
    else {
      if ((&DAT_18074998c)[DAT_180749988] == '\0') {
        FUN_18024e900(0x11e);
        (&DAT_18074998c)[DAT_180749988] = 1;
      }
      iVar6 = *(int *)(local_128 + 0x10);
      if ((&DAT_180749994)[DAT_180749988] != iVar6) {
        FUN_180256da0(0x11e,iVar6);
        (&DAT_180749994)[DAT_180749988] = iVar6;
      }
    }
    if (*(longlong *)(param_1 + 0x2e) == 0) {
      _DAT_180749950 = local_120[0];
      uRam0000000180749958 = local_120[1];
      uRam0000000180749960 = local_120[2];
      uRam0000000180749968 = local_120[3];
      _DAT_180749920 = local_158._0_8_;
      _DAT_180749928 = local_158._8_8_;
      _DAT_180749930 = local_158._16_8_;
      uRam0000000180749938 = local_158._24_8_;
      _DAT_180749940 = local_138._0_8_;
      uRam0000000180749948 = local_138._8_8_;
      FUN_180247230(9,0,4);
    }
    else {
      FUN_1802473b0(0x12d);
      FUN_180247600(3,0x161,0x18,*(undefined8 *)(param_1 + 0x2c));
      FUN_180247500(2,0x161,0x18,*(longlong *)(param_1 + 0x2c) + 0xc);
      FUN_1802470a0(4,0x15c,0x18,*(longlong *)(param_1 + 0x2c) + 0x14);
      FUN_180247230(9,0,param_1[0x2e]);
      FUN_180247600(3,0x161,0xc,&DAT_180749920);
      FUN_180247500(2,0x161,8,&DAT_180749950);
      FUN_180247100(0x12d);
    }
    if (*(int *)(local_128 + 0x14) == 0x39a) {
      FUN_180256da0(0x39a,0);
      FUN_18024e8d0(0x39a);
    }
    else {
      if ((&DAT_180749994)[DAT_180749988] != 0) {
        FUN_180256da0(0x11e,0);
        (&DAT_180749994)[DAT_180749988] = 0;
      }
      if ((&DAT_18074998c)[DAT_180749988] == '\x01') {
        FUN_18024e8d0(0x11e);
        (&DAT_18074998c)[DAT_180749988] = 0;
      }
    }
    goto LAB_18018bb8d;
  }
  if ((&DAT_18074998c)[DAT_180749988] == '\x01') {
    FUN_18024e8d0(0x11e);
    (&DAT_18074998c)[DAT_180749988] = 0;
  }
  iVar6 = *param_1;
  if (iVar6 == 2) {
    FUN_180247100(0x12f);
LAB_18018bafb:
    _DAT_180749920 = local_158._0_8_;
    _DAT_180749928 = CONCAT44(local_158._24_4_,local_158._8_4_);
    _DAT_180749930 = CONCAT44(local_138._0_4_,local_158._28_4_);
    FUN_180247230(3,0,2);
LAB_18018bb5f:
    FUN_1802473b0(0x12f);
  }
  else {
    if (iVar6 == 3) {
      FUN_180247100(0x12f);
      FUN_180247600(3,0x161,0xc,local_158);
      uVar10 = 9;
    }
    else {
      if (iVar6 != 4) {
        if (iVar6 == 6) {
          FUN_180247100(0x12f);
          if (*(ulonglong *)(param_1 + 0x2e) == 0) goto LAB_18018bafb;
          puVar7 = *(undefined8 **)(param_1 + 0x2c);
          for (uVar14 = *(ulonglong *)(param_1 + 0x2e) >> 1; uVar14 != 0; uVar14 = uVar14 - 1) {
            _DAT_180749920 = *puVar7;
            _DAT_180749928 = CONCAT44(*(undefined4 *)(puVar7 + 3),*(undefined4 *)(puVar7 + 1));
            _DAT_180749930 = *(undefined8 *)((longlong)puVar7 + 0x1c);
            FUN_180247230(3,0,2);
            puVar7 = puVar7 + 6;
          }
          goto LAB_18018bb5f;
        }
        goto LAB_18018bb69;
      }
      FUN_180247100(0x12f);
      FUN_180247600(3,0x161,0xc,local_158);
      uVar10 = 4;
    }
    FUN_180247230(uVar10,0,4);
    FUN_1802473b0(0x12f);
    FUN_180247600(3,0x161,0xc,&DAT_180749920);
  }
LAB_18018bb69:
  if ((&DAT_18074998c)[DAT_180749988] == '\0') {
    FUN_18024e900(0x11e);
    (&DAT_18074998c)[DAT_180749988] = 1;
  }
LAB_18018bb8d:
  FUN_180252530();
  return;
}



// ===================================================
// 180187C00  ->  FUN_180187c00  (entree 180187c00)
// ===================================================

void FUN_180187c00(int *param_1)

{
  longlong lVar1;
  
  if (*param_1 == 0) {
    lVar1 = FUN_18018c610(DAT_180719908,param_1[1]);
    param_1[1] = *(int *)(lVar1 + 0x28);
  }
  FUN_18018ca20(DAT_180719900,param_1);
  return;
}



