// ===================================================
// 1801AB190  ->  FUN_1801ab190  (entree 1801ab190)
// ===================================================

undefined8 FUN_1801ab190(longlong param_1)

{
  int iVar1;
  char cVar2;
  undefined4 uVar3;
  int *piVar4;
  undefined8 *puVar5;
  undefined4 *puVar6;
  undefined8 uVar7;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  
  piVar4 = (int *)FUN_1800da7e0();
  iVar1 = *piVar4;
  FUN_1801be860(param_1,iVar1 != 4);
  FUN_1801be7e0(param_1,iVar1 != 4);
  FUN_1801bd120(param_1);
  *(undefined4 *)(param_1 + 0x58) = 0;
  if (DAT_1807513b8 != 1) {
    cVar2 = FUN_180007450();
    if (cVar2 == '\0') {
      uVar7 = 0x10;
      uVar3 = 3;
      goto LAB_1801ab1fd;
    }
  }
  uVar7 = 0xe;
  uVar3 = 1;
LAB_1801ab1fd:
  *(undefined4 *)(param_1 + 0x224) = uVar3;
  *(undefined1 *)(param_1 + 0x228) = 0;
  *(undefined4 *)(param_1 + 0x22c) =
       *(undefined4 *)(&DAT_180410d88 + (longlong)*(int *)(param_1 + 0x58) * 4);
  *(undefined1 *)(param_1 + 0x230) = 0;
  puVar5 = (undefined8 *)FUN_1801b8a30();
  puVar6 = (undefined4 *)FUN_1801b8980();
  *(undefined4 *)(param_1 + 0x240) = *(undefined4 *)((longlong)puVar5 + 4);
  *(undefined4 *)(param_1 + 0x244) = *(undefined4 *)puVar5;
  *(undefined4 *)(param_1 + 0x248) = *(undefined4 *)(puVar5 + 1);
  *(undefined4 *)(param_1 + 0x24c) = *puVar6;
  *(undefined4 *)(param_1 + 0x5c) =
       *(undefined4 *)(param_1 + 0x240 + (longlong)*(int *)(param_1 + 0x58) * 4);
  *(undefined8 *)(param_1 + 0x250) = *puVar5;
  *(undefined4 *)(param_1 + 600) = *(undefined4 *)(puVar5 + 1);
  *(undefined4 *)(param_1 + 0x311) = 0;
  FUN_1801bd0f0(param_1 + 0x31c);
  FUN_1801be850(param_1 + 0x31c,0xffffffff,0 < *(int *)(param_1 + 0x5c));
  FUN_1801be850(param_1 + 0x31c,1,
                *(int *)(param_1 + 0x5c) <
                *(int *)(&DAT_180410d88 + (longlong)*(int *)(param_1 + 0x58) * 4));
  FUN_1801bd0b0(param_1 + 0x260);
  FUN_1801bd0b0(param_1 + 0x2b8);
  FUN_1801be8e0(param_1 + 0x2b8,0xe);
  FUN_1801bda20(param_1 + 0x2b8,uVar7);
  local_18 = 0;
  local_14 = 0;
  local_10 = 0;
  cVar2 = FUN_1801bcd70(param_1 + 0x2b8,&local_18,"p_txt_01_lt",1,"neu_s");
  if (cVar2 != '\0') {
    FUN_1801be8d0(param_1 + 0x260,local_18,local_14);
    FUN_1801be8e0(param_1 + 0x260,0x10);
    FUN_1801bda20(param_1 + 0x260,0x1a);
  }
  *(undefined1 *)(param_1 + 0x310) = 0;
  return 1;
}



// ===================================================
// 1801AA140  ->  FUN_1801aa140  (entree 1801aa140)
// ===================================================

void FUN_1801aa140(longlong param_1)

{
  int iVar1;
  char cVar2;
  undefined1 uVar3;
  undefined4 uVar4;
  undefined8 uVar5;
  ulonglong uVar6;
  int iVar7;
  longlong lVar8;
  ulonglong uVar9;
  ulonglong uVar10;
  bool bVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  undefined1 auVar16 [64];
  undefined1 auVar17 [64];
  undefined4 uVar18;
  undefined1 auVar19 [64];
  float fVar20;
  undefined4 local_res8;
  undefined4 local_res10;
  undefined4 local_res18;
  undefined4 local_res20;
  uint local_178;
  float local_174;
  float local_170;
  uint local_168 [4];
  undefined1 local_158 [8];
  undefined4 local_150;
  undefined4 local_134;
  undefined4 local_12c;
  uint local_124;
  float local_120;
  uint local_11c;
  float local_118;
  undefined1 *local_110;
  int local_108 [4];
  undefined1 local_f8 [40];
  float local_d0;
  undefined4 local_c4;
  float local_c0;
  undefined8 local_b8;
  
  local_b8 = 0xfffffffffffffffe;
  local_108[0] = 0x30c;
  local_108[1] = 0x2f6;
  local_108[2] = 0x322;
  local_108[3] = 0x32a;
  local_178 = 0;
  local_174 = 0.0;
  local_170 = 0.0;
  local_168[0] = 0;
  local_168[1] = 0;
  local_168[2] = 0;
  FUN_18019a8c0(local_158);
  FUN_18019a9d0(local_f8);
  uVar4 = FUN_180187aa0();
  FUN_180187cb0(2);
  cVar2 = FUN_1801bda10(param_1 + 0x260);
  uVar6 = 0;
  auVar16 = ZEXT464(DAT_18034af78);
  fVar13 = DAT_18034b410;
  fVar15 = DAT_180346d4c;
  uVar18 = DAT_1803480b8;
  if (cVar2 != '\0') {
    FUN_1801bcd70(param_1 + 0x260,&local_178,"p_small_head_lt",1,0);
    FUN_18019b6f0(local_f8,1);
    FUN_18019b870(local_f8,2);
    FUN_18019b830(local_f8,auVar16._0_8_);
    local_110 = local_f8;
    local_134 = 0x12;
    local_11c = local_178;
    local_118 = local_174;
    local_124 = local_178;
    local_120 = local_174;
    local_12c = 9;
    local_res8 = CONCAT13((char)(int)(fVar15 * local_170),0x39b7ff);
    local_150 = local_res8;
    local_c4 = uVar18;
    local_c0 = fVar13;
    uVar5 = FUN_1801efd10(0x2f3);
    FUN_18019b300(local_158,uVar5);
  }
  cVar2 = FUN_1801bda10(param_1 + 0x2b8);
  if (cVar2 != '\0') {
    FUN_1801bcd70(param_1 + 0x2b8,&local_178,"p_txt_01_lt",1,0);
    FUN_1801bcd70(param_1 + 0x2b8,local_168,"p_txt_03_rt",0,0);
    FUN_18019b6f0(local_f8,1);
    FUN_18019b870(local_f8,2);
    FUN_18019b830(local_f8,auVar16._0_8_);
    local_c4 = uVar18;
    local_c0 = fVar13;
    local_110 = local_f8;
    local_134 = 0x12;
    auVar19 = ZEXT464((uint)local_174);
    fVar13 = local_d0 + fVar13;
    auVar16 = ZEXT464((uint)(fVar13 + local_174));
    auVar17 = ZEXT464(local_178);
    uVar9 = uVar6;
    uVar10 = uVar6;
    fVar20 = DAT_180346d38;
    fVar12 = local_d0;
    if (-1 < *(int *)(param_1 + 0x224)) {
      do {
        iVar7 = (int)uVar6;
        if (*(char *)(param_1 + 0x311 + uVar9) == '\0') {
          if (iVar7 == *(int *)(param_1 + 0x58)) {
            FUN_1801be470(param_1 + 0x2b8,auVar17._0_8_,auVar16._0_8_,fVar12);
            auVar19 = ZEXT464((uint)(local_d0 * fVar20 + auVar16._0_4_));
            fVar12 = local_d0;
          }
          fVar14 = auVar16._0_4_;
          if ((longlong)uVar9 < 4) {
            local_124 = auVar17._0_4_;
            local_12c = 9;
            uVar3 = (undefined1)(int)(fVar15 * local_170);
            if (iVar7 == *(int *)(param_1 + 0x58)) {
              local_res8 = CONCAT13(uVar3,0x5b5bff);
              local_150 = local_res8;
            }
            else {
              local_res10 = CONCAT13(uVar3,0xd0c8c6);
              local_150 = local_res10;
            }
            iVar1 = local_108[uVar9];
            local_120 = fVar14;
            local_11c = local_124;
            local_118 = fVar14;
            uVar5 = FUN_1801efd10(iVar1);
            FUN_18019b300(local_158,&DAT_180347cf8,uVar5);
            uVar6 = FUN_1801efd10(*(int *)(param_1 + 0x240 + uVar9 * 4) + 1 + iVar1);
            bVar11 = iVar7 != *(int *)(param_1 + 0x58);
            if (!bVar11) {
              uVar10 = uVar6;
            }
            local_11c = local_168[0];
            local_120 = auVar16._0_4_;
            local_124 = local_168[0];
            local_12c = 9;
            uVar3 = (undefined1)(int)(fVar15 * local_170);
            if (bVar11) {
              local_res20 = CONCAT13(uVar3,0xd0c8c6);
              local_150 = local_res20;
            }
            else {
              local_res18 = CONCAT13(uVar3,0x5b5bff);
              local_150 = local_res18;
            }
            local_118 = local_120;
            FUN_18019b2e0(local_158,2,&DAT_180347cf8,uVar6);
            fVar14 = auVar16._0_4_;
            fVar12 = local_d0;
          }
          auVar16 = ZEXT464((uint)(fVar14 + fVar13));
        }
        uVar6 = (ulonglong)(iVar7 + 1U);
        uVar9 = uVar9 + 1;
      } while ((int)(iVar7 + 1U) <= *(int *)(param_1 + 0x224));
      if (uVar10 != 0) {
        lVar8 = -1;
        do {
          lVar8 = lVar8 + 1;
        } while (*(char *)(uVar10 + lVar8) != '\0');
        FUN_18019b8b0(local_158,&local_res8,uVar10,lVar8,DAT_180347cd8);
        FUN_1801be070(param_1 + 0x31c,local_168[0],auVar19._0_8_,4,0x12,local_res8);
        goto LAB_1801aa5cf;
      }
    }
    FUN_1801be4b0(param_1 + 0x31c);
  }
LAB_1801aa5cf:
  FUN_180187cb0(uVar4);
  return;
}



