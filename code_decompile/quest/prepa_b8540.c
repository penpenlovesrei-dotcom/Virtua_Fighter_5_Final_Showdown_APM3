// ===================================================
// 1800B8540  ->  FUN_1800b8540  (entree 1800b8540)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1800b8540(undefined8 param_1)

{
  ulonglong *puVar1;
  char cVar2;
  byte bVar3;
  undefined1 uVar4;
  undefined2 uVar5;
  undefined2 uVar6;
  short sVar7;
  int iVar8;
  undefined4 uVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  uint uVar13;
  int iVar14;
  uint uVar15;
  longlong lVar16;
  undefined8 *puVar17;
  longlong lVar18;
  longlong lVar19;
  longlong lVar20;
  undefined6 *puVar21;
  undefined8 uVar22;
  short *psVar23;
  int *piVar24;
  ulonglong uVar25;
  longlong lVar26;
  undefined8 local_res10;
  undefined4 local_res18;
  int local_res20;
  undefined4 in_stack_fffffffffffffc90;
  undefined8 local_368;
  undefined8 uStack_360;
  undefined8 uStack_358;
  undefined8 uStack_350;
  undefined8 local_348;
  undefined8 uStack_340;
  undefined8 local_338;
  undefined8 local_330;
  int local_328;
  undefined8 local_324;
  undefined4 local_31c;
  undefined4 local_318;
  undefined4 local_314;
  undefined1 local_310 [4];
  undefined1 local_30c;
  undefined4 local_308;
  undefined8 local_300;
  undefined8 local_2f8;
  undefined8 local_2f0;
  undefined8 local_2e8;
  longlong local_2e0;
  undefined8 local_2d8;
  undefined8 local_2d0;
  undefined1 local_2c8 [8];
  byte local_2c0;
  undefined4 local_2bc;
  byte local_2a8;
  byte local_2a7;
  undefined1 local_150 [272];
  
  uVar6 = (undefined2)((uint)in_stack_fffffffffffffc90 >> 0x10);
  local_2d0 = 0xfffffffffffffffe;
  lVar16 = FUN_1800b23b0();
  local_2d8 = FUN_1800b24b0(param_1);
  local_368 = _DAT_18039b420;
  uStack_360 = _UNK_18039b428;
  uStack_358 = _UNK_18039b430;
  uStack_350 = _UNK_18039b438;
  local_348 = _DAT_18039b3e0;
  uStack_340 = _UNK_18039b3e8;
  local_338 = 4;
  local_330 = 0;
  local_328 = 2;
  iVar12 = 0x29;
  local_324 = 0x29;
  local_31c = 0;
  iVar8 = FUN_1800b48c0(lVar16);
  local_368 = local_368 & 0xffffffff00000000;
  uVar9 = FUN_1800244d0(lVar16);
  local_368 = CONCAT44(uVar9,(undefined4)local_368);
  uStack_360 = uStack_360 & 0xffffffff00000000;
  local_res20 = FUN_1800244d0(param_1);
  lVar18 = (longlong)local_res20 * 4;
  iVar14 = *(int *)(&DAT_18034b208 + lVar18);
  lVar26 = (longlong)iVar14;
  piVar24 = (int *)((longlong)&uStack_360 + lVar18 + 4);
  local_res10 = piVar24;
  iVar10 = FUN_1800b23e0(param_1,local_res20);
  iVar11 = local_res20;
  *piVar24 = iVar10;
  piVar24 = (int *)((longlong)&uStack_358 + lVar18 + 4);
  iVar10 = FUN_1800b23f0(param_1,local_res20);
  *piVar24 = iVar10;
  uVar9 = FUN_1800b2400(param_1,iVar11);
  *(undefined4 *)((longlong)&uStack_350 + lVar18 + 4) = uVar9;
  uVar9 = FUN_1800b2410(param_1,iVar11);
  *(undefined4 *)((longlong)&local_348 + lVar18 + 4) = uVar9;
  *(undefined4 *)((longlong)&uStack_340 + lVar18 + 4) = 0;
  local_300 = 0xffffffffffffffff;
  local_30c = 0;
  local_308 = 0xffffffff;
  puVar17 = (undefined8 *)FUN_1800ff0b0();
  local_300 = *puVar17;
  local_2f8 = 0;
  local_2f0 = 0;
  local_2e8 = 0;
  FUN_180215590(local_310);
  lVar18 = FUN_180101820(DAT_18070fb10,iVar11);
  if (*(char *)(lVar18 + 1) != '\0') {
    _guard_check_icall(local_310,lVar18 + 0x410);
  }
  FUN_180094840();
  FUN_1800a2160();
  _guard_check_icall();
  cVar2 = FUN_180007450();
  if (cVar2 == '\0') {
    _guard_check_icall();
  }
  _guard_check_icall();
  _guard_check_icall(1);
  _guard_check_icall();
  FUN_18010eaf0();
  if (local_368._4_4_ == 0) {
    iVar11 = FUN_18019c090();
    if (iVar11 == 2) {
      cVar2 = FUN_1801d4a80();
      if (cVar2 != '\0') {
        FUN_1801d4560();
      }
      puVar21 = (undefined6 *)FUN_18019c080();
      local_res10 = (int *)CONCAT26(local_res10._6_2_,*puVar21);
      uVar6 = FUN_1801d4030(iVar8);
      local_res10._0_4_ = CONCAT22(uVar6,(undefined2)local_res10);
      cVar2 = FUN_1801d4990(8);
      if ((cVar2 == '\0') && (iVar11 = FUN_1801d3b60(iVar8), iVar11 != 8)) {
        uVar4 = FUN_1801d4270(iVar8);
        local_res10._0_6_ = CONCAT15(uVar4,(undefined5)local_res10);
      }
      else {
        local_res10._0_6_ = CONCAT15(1,(undefined5)local_res10);
      }
      uVar4 = FUN_1801d44e0(iVar8);
      local_res10._0_5_ = CONCAT14(uVar4,(undefined4)local_res10);
      FUN_18019c3a0(&local_res10);
      uVar6 = FUN_1801d3b20(iVar8);
      FUN_1800b5dd0(local_2c8);
      FUN_1801a53a0(local_2c8,uVar6);
      lVar18 = lVar26 * 4;
      *(uint *)((longlong)&uStack_360 + lVar18 + 4) = (uint)local_2c0;
      *(undefined4 *)((longlong)&uStack_358 + lVar18 + 4) = 0;
      *(undefined4 *)((longlong)&uStack_350 + lVar18 + 4) = 0;
      *(undefined4 *)((longlong)&local_348 + lVar18 + 4) = 0;
      *(undefined4 *)((longlong)&uStack_340 + lVar18 + 4) = 1;
      uVar9 = FUN_1801d3ff0(iVar8);
      FUN_18010ede0(iVar14,uVar9,local_2bc,local_150);
      FUN_180098430(local_2c8);
      iVar12 = FUN_1801d4460(iVar8);
    }
    else {
      uVar9 = FUN_1800b4600(lVar16);
      iVar11 = FUN_1800acd40(uVar9,iVar8);
      if (iVar11 == 0x15) {
        iVar11 = 9;
      }
      lVar18 = lVar26 * 4;
      *(int *)((longlong)&uStack_360 + lVar18 + 4) = iVar11;
      uVar9 = 0;
      if (iVar11 == *local_res10) {
        if (((*(uint *)(DAT_180c3b6f0 + 0x10) & 0x100) == 0) && (*piVar24 == 0)) {
          uVar9 = 1;
        }
      }
      else if ((iVar11 == 0x14) && (lVar19 = FUN_1800b23a0(), uVar9 = 0, lVar19 != 0)) {
        uVar22 = FUN_1800b23b0(lVar19);
        uVar9 = FUN_1800b22e0(uVar22);
      }
      *(undefined4 *)((longlong)&uStack_358 + lVar18 + 4) = uVar9;
      *(undefined4 *)((longlong)&uStack_350 + lVar18 + 4) = 0;
      *(undefined4 *)((longlong)&local_348 + lVar18 + 4) = 0;
      *(undefined4 *)((longlong)&uStack_340 + lVar18 + 4) = 1;
      lVar19 = FUN_1800484b0();
      uVar15 = FUN_180047de0(lVar19 + 0x60);
      uVar13 = FUN_18019c090();
      if (uVar13 < 2) {
        bVar3 = FUN_18019c060();
        uVar15 = (uint)bVar3;
      }
      uVar9 = FUN_1800acd80(uVar15,iVar8);
      FUN_18010ed40(iVar14,uVar9,*(undefined4 *)((longlong)&uStack_360 + lVar18 + 4));
      iVar12 = FUN_1800af400(*(undefined4 *)((longlong)&uStack_360 + lVar18 + 4));
      if ((iVar12 == 0x15) && (lVar18 = FUN_1800b23a0(), lVar18 != 0)) {
        uVar22 = FUN_1800b23b0(lVar18);
        iVar12 = FUN_1800b2330(uVar22);
      }
    }
  }
  else if (local_368._4_4_ == 1) {
    lVar18 = FUN_180095510();
    local_2e0 = lVar18;
    FUN_1800b1f20(lVar16);
    local_314 = FUN_1800b45a0(lVar16);
    iVar11 = FUN_1800b47c0(lVar16);
    local_318 = FUN_1800b47f0(lVar16,iVar8);
    uVar9 = FUN_1800b47a0(lVar16,iVar8);
    local_res18 = uVar9;
    uVar5 = FUN_1800b4780(lVar16,iVar8);
    local_res10 = (int *)CONCAT62(local_res10._2_6_,uVar5);
    lVar19 = FUN_1800b4620(lVar16,uVar5,uVar9);
    cVar2 = FUN_18009cbe0(local_res18);
    if (cVar2 == '\0') {
      if (lVar19 == 0) goto LAB_1800b8843;
    }
    else if (lVar19 == 0) {
LAB_1800b8843:
      FUN_1800b5dd0(local_2c8);
      FUN_1801a53a0(local_2c8,(ulonglong)local_res10 & 0xffff);
      lVar19 = lVar26 * 4;
      *(uint *)((longlong)&uStack_360 + lVar19 + 4) = (uint)local_2c0;
      *(uint *)((longlong)&uStack_358 + lVar19 + 4) = (uint)local_2a8;
      *(undefined4 *)((longlong)&uStack_350 + lVar19 + 4) = 0;
      cVar2 = FUN_18019c330();
      if (cVar2 != '\0') {
        *(uint *)((longlong)&uStack_358 + lVar19 + 4) = (uint)local_2a7;
        *(undefined4 *)((longlong)&uStack_350 + lVar19 + 4) = 1;
      }
      lVar20 = FUN_180101820(DAT_18070fb10,iVar14);
      uVar25 = 0;
      do {
        if (1999 < uVar25) {
                    /* WARNING: Subroutine does not return */
          FUN_1800934d0(lVar20 + 0x160);
        }
        puVar1 = (ulonglong *)(lVar20 + 0x160 + (uVar25 >> 6) * 8);
        *puVar1 = *puVar1 | 1L << ((uint)uVar25 & 0x3f);
        uVar25 = uVar25 + 1;
      } while (uVar25 < 2000);
      *(undefined4 *)((longlong)&local_348 + lVar19 + 4) = 0;
      *(undefined4 *)((longlong)&uStack_340 + lVar19 + 4) = 1;
      uVar9 = FUN_1800b4760(lVar16,iVar8);
      uVar9 = FUN_1800991e0(iVar8,iVar11,uVar9,*(undefined4 *)(lVar18 + 0xd0));
      FUN_18010ede0(iVar14,uVar9,local_2bc,local_150);
      FUN_180098430(local_2c8);
    }
    else {
      lVar20 = lVar26 * 4;
      *(uint *)((longlong)&uStack_360 + lVar20 + 4) = (uint)*(byte *)(lVar19 + 0x8b);
      *(uint *)((longlong)&uStack_358 + lVar20 + 4) = (uint)*(byte *)(lVar19 + 0xb2);
      *(undefined4 *)((longlong)&uStack_350 + lVar20 + 4) = 0;
      *(undefined4 *)((longlong)&local_348 + lVar20 + 4) = 0;
      *(undefined4 *)((longlong)&uStack_340 + lVar20 + 4) = 1;
      if (iVar11 == 9) {
        uVar9 = 0xffffffff;
      }
      else {
        uVar9 = FUN_1800b4760(lVar16,iVar8);
        uVar9 = FUN_1800991e0(iVar8,iVar11,uVar9,*(undefined4 *)(lVar18 + 0xd0));
      }
      FUN_18010ec90(iVar14,uVar9,lVar19 + 0x268);
    }
    iVar12 = FUN_1800b47d0(lVar16,iVar8);
    FUN_180095560(local_2e0,local_314,iVar11,local_318,local_res18,
                  CONCAT22(uVar6,(undefined2)local_res10));
  }
  lVar18 = FUN_1800484b0();
  if (local_368._4_4_ == 0) {
    iVar14 = FUN_180047de0(lVar18 + 0xa0);
    local_338 = CONCAT44(iVar14 * 0x3c,(undefined4)local_338);
    sVar7 = FUN_180047de0(lVar18 + 0x48);
    lVar18 = lVar18 + 0x38;
LAB_1800b8b81:
    local_330 = CONCAT62(CONCAT42(local_330._4_4_,sVar7 + 1),sVar7 + 1);
    uVar9 = FUN_180047de0(lVar18);
    local_330 = CONCAT44(uVar9,(undefined4)local_330);
  }
  else if (local_368._4_4_ == 1) {
    iVar14 = FUN_180047de0(lVar18 + 0xa8);
    local_338 = CONCAT44(iVar14 * 0x3c,(undefined4)local_338);
    sVar7 = FUN_180047de0(lVar18 + 0x88);
    lVar18 = lVar18 + 0x80;
    goto LAB_1800b8b81;
  }
  psVar23 = (short *)FUN_18019c080();
  uVar15 = FUN_18019c090();
  iVar14 = local_res20;
  if (uVar15 < 4) {
    local_338 = CONCAT44((uint)*(byte *)(psVar23 + 2) * 0x3c,(undefined4)local_338);
    local_330._0_4_ = CONCAT22(psVar23[1] + 1,*psVar23 + 1);
    local_330 = (ulonglong)CONCAT14(*(undefined1 *)((longlong)psVar23 + 5),(undefined4)local_330);
  }
  local_328 = local_res20;
  local_324 = CONCAT44(local_324._4_4_,iVar12);
  uVar9 = FUN_1800b4900(lVar16);
  local_324 = CONCAT44(uVar9,(undefined4)local_324);
  if (iVar8 == 0) {
    local_31c = CONCAT31(local_31c._1_3_,1);
    if (*(int *)(lVar16 + 0x45c) == 0) goto LAB_1800b8c07;
  }
  local_31c = local_31c & 0xffffff00;
LAB_1800b8c07:
  cVar2 = FUN_1800b2590(lVar16);
  if (cVar2 == '\0') {
    local_31c._0_2_ = CONCAT11(local_368._4_4_ != 1,(byte)local_31c);
  }
  else {
    local_31c._0_2_ = (ushort)(byte)local_31c;
  }
  uVar4 = FUN_1800b2680(lVar16);
  uVar22 = local_2d8;
  local_31c._0_3_ = CONCAT12(uVar4,(ushort)local_31c);
  FUN_1800b34d0(local_2d8,&local_368);
  FUN_1800b3340(uVar22,0);
  FUN_1800b3340(uVar22,1);
  FUN_1800b2280(uVar22,iVar14);
  FUN_1800b28d0(param_1);
  FUN_1800b1be0(uVar22);
  cVar2 = FUN_1800b25f0(lVar16);
  uVar4 = iVar8 != 0;
  if (cVar2 != '\0') {
    uVar4 = 2;
  }
  cVar2 = FUN_1800b2590(lVar16);
  if (cVar2 != '\0') {
    uVar4 = 3;
  }
  if (local_368._4_4_ == 0) {
    iVar14 = FUN_18019c090();
    if (iVar14 == 2) {
      FUN_1801974e0(PTR_DAT_180409ff0,uStack_360._4_1_,uStack_358 & 0xff,local_328);
    }
    else {
      FUN_180197480(PTR_DAT_180409ff0,*(undefined1 *)((longlong)&uStack_360 + lVar26 * 4 + 4),uVar4)
      ;
    }
  }
  else if (local_368._4_4_ == 1) {
    FUN_180197420(PTR_DAT_180409ff0,uStack_360._4_1_,uStack_358 & 0xff,uVar4,iVar8,local_328);
  }
  return;
}



