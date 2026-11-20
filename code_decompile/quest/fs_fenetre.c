// ===================================================
// 1801BC580  ->  FUN_1801bc580  (entree 1801bc580)
// ===================================================

void FUN_1801bc580(longlong param_1)

{
  int *piVar1;
  uint uVar2;
  undefined4 uVar3;
  longlong lVar4;
  ulonglong uVar5;
  undefined8 uVar6;
  undefined1 uVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  undefined1 auVar10 [64];
  ulonglong uVar11;
  undefined1 auVar12 [64];
  undefined4 uVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  undefined4 uVar18;
  float fVar19;
  undefined4 local_res8;
  undefined1 local_178 [8];
  undefined4 local_170;
  undefined1 local_168;
  int local_154;
  undefined4 local_14c;
  float local_144;
  float local_140;
  float local_13c;
  float local_138;
  undefined1 *local_130;
  float local_128;
  undefined4 local_124;
  undefined4 local_120;
  float local_118;
  float local_114;
  float local_110;
  float local_10c;
  undefined1 local_108 [40];
  float local_e0;
  undefined4 local_d4;
  float local_d0;
  undefined8 local_c8;
  
  local_c8 = 0xfffffffffffffffe;
  FUN_18019a8c0(local_178);
  FUN_18019a9d0(local_108);
  uVar13 = 0;
  auVar12 = ZEXT1264(ZEXT812(0));
  auVar10 = ZEXT1264(ZEXT812(0));
  fVar14 = 0.0;
  fVar16 = 0.0;
  fVar15 = 0.0;
  uVar3 = FUN_180187aa0();
  FUN_180187cb0(2);
  fVar19 = DAT_18034b410;
  uVar18 = DAT_1803480b8;
  fVar17 = DAT_180346d4c;
  piVar1 = (int *)(param_1 + 200);
  if ((*piVar1 != 3) || (*(longlong *)(param_1 + 0x70) == 0)) goto LAB_1801bcb29;
  uVar2 = *(uint *)(param_1 + 0xcc);
  if (uVar2 != 0x5a) {
    *(longlong *)(param_1 + 0xf0) = *(longlong *)(param_1 + 0xe8);
    if (*(longlong *)(param_1 + 0xe8) == *(longlong *)(param_1 + 0xe8)) {
      uVar9 = *(undefined4 *)(&DAT_18052e680 + (ulonglong)uVar2 * 0x18);
      uVar8 = FUN_180029780(*(undefined4 *)(param_1 + 0xd8));
      FUN_1800297f0(param_1 + 0xe8,uVar9,(&PTR_s_cmn_win_s_01_18052e688)[(ulonglong)uVar2 * 3],0,9,0
                    ,uVar8);
    }
    lVar4 = FUN_1800298b0(param_1 + 0xe8,"p_txt_01_lt");
    if (lVar4 != 0) {
      fVar14 = *(float *)(lVar4 + 100);
      auVar10 = ZEXT464((uint)(*(float *)(lVar4 + 0x44) + *(float *)(param_1 + 0x118)));
      auVar12 = ZEXT464((uint)(*(float *)(lVar4 + 0x40) + *(float *)(param_1 + 0x114)));
    }
  }
  uVar2 = *(uint *)(param_1 + 0xcc);
  if (uVar2 != 0x5a) {
    if (*(longlong *)(param_1 + 0xe8) == *(longlong *)(param_1 + 0xf0)) {
      uVar9 = *(undefined4 *)(&DAT_18052e680 + (ulonglong)uVar2 * 0x18);
      uVar8 = FUN_180029780(*(undefined4 *)(param_1 + 0xd8));
      FUN_1800297f0(param_1 + 0xe8,uVar9,(&PTR_s_cmn_win_s_01_18052e688)[(ulonglong)uVar2 * 3],0,9,0
                    ,uVar8);
    }
    lVar4 = FUN_1800298b0(param_1 + 0xe8,"p_txt_02_rb");
    if (lVar4 != 0) {
      fVar15 = *(float *)(lVar4 + 0x44) + *(float *)(param_1 + 0x118);
      fVar16 = *(float *)(lVar4 + 0x40) + *(float *)(param_1 + 0x114);
    }
  }
  local_114 = auVar10._0_4_;
  local_10c = fVar15 - local_114;
  local_118 = auVar12._0_4_ + *(float *)(param_1 + 0x80);
  local_110 = fVar16 - local_118;
  FUN_18019b6f0(local_108,1);
  FUN_18019b870(local_108,2);
  FUN_18019b830(local_108,DAT_18034af78);
  local_130 = local_108;
  local_154 = *(int *)(param_1 + 0x84) + 2;
  local_d4 = uVar18;
  local_d0 = fVar19;
  FUN_18019b800(local_178,&local_118,9);
  local_res8 = CONCAT13((char)(int)(fVar14 * fVar17),0xd0c8c6);
  local_170 = local_res8;
  FUN_18019b2e0(local_178,0x800,&DAT_180347cf8,*(undefined8 *)(param_1 + 0x70));
  uVar11 = auVar12._0_8_;
  local_168 = 0;
  uVar2 = *(uint *)(param_1 + 0xcc);
  uVar5 = (ulonglong)uVar2;
  if (*(int *)(param_1 + 0x60) == 0) {
    if (uVar2 != 0x5a) {
      if (*(longlong *)(param_1 + 0xe8) == *(longlong *)(param_1 + 0xf0)) {
        uVar9 = *(undefined4 *)(&DAT_18052e680 + uVar5 * 0x18);
        uVar8 = FUN_180029780(*(undefined4 *)(param_1 + 0xd8));
        FUN_1800297f0(param_1 + 0xe8,uVar9,(&PTR_s_cmn_win_s_01_18052e688)[uVar5 * 3],0,9,0,uVar8);
      }
      lVar4 = FUN_1800298b0(param_1 + 0xe8,"p_txt_ok_01_lt");
      if (lVar4 != 0) {
        fVar14 = *(float *)(lVar4 + 100);
        auVar10 = ZEXT464((uint)(*(float *)(lVar4 + 0x44) + *(float *)(param_1 + 0x118)));
        auVar12 = ZEXT464((uint)(*(float *)(lVar4 + 0x40) + *(float *)(param_1 + 0x114)));
      }
    }
    local_144 = auVar12._0_4_;
    if ((*piVar1 == 3) && (*(int *)(param_1 + 0xdc) != 0)) {
      local_124 = auVar10._0_4_;
      local_128 = local_144;
      local_120 = uVar13;
      FUN_180029d00(*(int *)(param_1 + 0xdc),&local_128);
      local_144 = auVar12._0_4_;
      *(undefined1 *)(param_1 + 0xe0) = 1;
    }
    local_140 = auVar10._0_4_;
    local_14c = 9;
    local_res8._3_1_ = (undefined1)(int)(fVar14 * fVar17);
    uVar6 = 0x10f;
    local_13c = local_144;
    local_138 = local_140;
LAB_1801bcaf6:
    local_res8 = CONCAT13(local_res8._3_1_,0x5b5bff);
  }
  else {
    if (uVar2 != 0x5a) {
      if (*(longlong *)(param_1 + 0xe8) == *(longlong *)(param_1 + 0xf0)) {
        uVar13 = *(undefined4 *)(&DAT_18052e680 + uVar5 * 0x18);
        uVar9 = FUN_180029780(*(undefined4 *)(param_1 + 0xd8));
        FUN_1800297f0(param_1 + 0xe8,uVar13,(&PTR_s_cmn_win_s_01_18052e688)[uVar5 * 3],0,9,0,uVar9);
      }
      lVar4 = FUN_1800298b0(param_1 + 0xe8,"p_txt_yes_01_lt");
      uVar11 = auVar12._0_8_;
      if (lVar4 != 0) {
        fVar14 = *(float *)(lVar4 + 100);
        auVar10 = ZEXT464((uint)(*(float *)(lVar4 + 0x44) + *(float *)(param_1 + 0x118)));
        uVar11 = (ulonglong)(uint)(*(float *)(lVar4 + 0x40) + *(float *)(param_1 + 0x114));
      }
    }
    local_144 = (float)uVar11;
    local_140 = auVar10._0_4_;
    local_14c = 9;
    local_13c = local_144;
    local_138 = local_140;
    if (*(int *)(param_1 + 100) != 0) {
      FUN_1801be470(piVar1,uVar11,local_140 + local_e0 + local_d0);
      local_res8._3_1_ = (undefined1)(int)(fVar14 * fVar17);
      local_res8 = CONCAT13(local_res8._3_1_,0xd0c8c6);
      local_170 = local_res8;
      uVar6 = FUN_1801efd10(0x10b);
      FUN_18019b300(local_178,&DAT_18039f5c4,uVar6);
      uVar6 = 0x10c;
      goto LAB_1801bcaf6;
    }
    FUN_1801be470(piVar1,uVar11,auVar10._0_8_);
    uVar7 = (undefined1)(int)(fVar14 * fVar17);
    local_res8 = CONCAT13(uVar7,0x5b5bff);
    local_170 = local_res8;
    uVar6 = FUN_1801efd10(0x10b);
    FUN_18019b300(local_178,&DAT_18039f5c4,uVar6);
    local_res8 = CONCAT13(uVar7,0xd0c8c6);
    uVar6 = 0x10c;
  }
  local_170 = local_res8;
  uVar6 = FUN_1801efd10(uVar6);
  FUN_18019b300(local_178,&DAT_180347cf8,uVar6);
LAB_1801bcb29:
  if (*(int *)(param_1 + 0x120) == 3) {
    uVar2 = *(uint *)(param_1 + 0x124);
    if (uVar2 != 0x5a) {
      *(longlong *)(param_1 + 0x148) = *(longlong *)(param_1 + 0x140);
      if (*(longlong *)(param_1 + 0x140) == *(longlong *)(param_1 + 0x140)) {
        uVar13 = *(undefined4 *)(&DAT_18052e680 + (ulonglong)uVar2 * 0x18);
        uVar9 = FUN_180029780(*(undefined4 *)(param_1 + 0x130));
        FUN_1800297f0(param_1 + 0x140,uVar13,(&PTR_s_cmn_win_s_01_18052e688)[(ulonglong)uVar2 * 3],0
                      ,9,0,uVar9);
      }
      lVar4 = FUN_1800298b0(param_1 + 0x140,"p_sousa_win_01_lt");
      if (lVar4 != 0) {
        fVar14 = *(float *)(lVar4 + 100);
        auVar10 = ZEXT464((uint)(*(float *)(lVar4 + 0x44) + *(float *)(param_1 + 0x170)));
      }
    }
    uVar2 = *(uint *)(param_1 + 0x124);
    if (uVar2 != 0x5a) {
      if (*(longlong *)(param_1 + 0x140) == *(longlong *)(param_1 + 0x148)) {
        uVar13 = *(undefined4 *)(&DAT_18052e680 + (ulonglong)uVar2 * 0x18);
        uVar9 = FUN_180029780(*(undefined4 *)(param_1 + 0x130));
        FUN_1800297f0(param_1 + 0x140,uVar13,(&PTR_s_cmn_win_s_01_18052e688)[(ulonglong)uVar2 * 3],0
                      ,9,0,uVar9);
      }
      lVar4 = FUN_1800298b0(param_1 + 0x140,"p_sousa_win_02_rb");
      if (lVar4 != 0) {
        fVar16 = *(float *)(lVar4 + 0x40) + *(float *)(param_1 + 0x16c);
      }
    }
    FUN_18019b6f0(local_108,1);
    FUN_18019b870(local_108,2);
    FUN_18019b830(local_108,DAT_18034af78);
    local_130 = local_108;
    local_154 = *(int *)(param_1 + 0x84) + 1;
    local_140 = auVar10._0_4_;
    local_14c = 9;
    local_res8 = CONCAT13((char)(int)(fVar14 * fVar17),0xd0c8c6);
    local_170 = local_res8;
    local_144 = fVar16;
    local_13c = fVar16;
    local_138 = local_140;
    local_d4 = uVar18;
    local_d0 = fVar19;
    uVar6 = FUN_1801efd10(0);
    FUN_18019b2e0(local_178,2,&DAT_180347cf8,uVar6);
  }
  FUN_180187cb0(uVar3);
  return;
}



