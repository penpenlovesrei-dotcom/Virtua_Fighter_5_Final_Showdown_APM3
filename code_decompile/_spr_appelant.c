// ===================================================
// 18010872E  ->  FUN_180108320  (entree 180108320)
// ===================================================

ulonglong FUN_180108320(ushort param_1)

{
  longlong lVar1;
  longlong lVar2;
  undefined4 *puVar3;
  int iVar4;
  float *pfVar5;
  int iVar6;
  uint uVar7;
  ulonglong uVar8;
  ushort uVar9;
  ulonglong uVar10;
  undefined1 auVar11 [16];
  undefined1 auVar12 [16];
  undefined1 auVar13 [64];
  undefined1 auVar14 [16];
  float fVar16;
  float fVar18;
  float fVar19;
  ushort local_res8 [4];
  float local_res10 [2];
  float local_res18;
  float local_res1c;
  undefined1 local_168 [4];
  undefined4 local_164;
  float local_160;
  uint local_15c;
  uint local_158;
  float local_150;
  undefined4 local_14c;
  float local_148;
  float local_144;
  float local_134;
  float local_130;
  float local_128;
  float local_124;
  float local_110;
  undefined1 local_c0 [4];
  undefined4 local_bc;
  undefined1 auVar15 [64];
  undefined1 auVar17 [64];
  
  local_res8[0] = param_1;
  FUN_1801073f0();
  auVar13 = ZEXT464((uint)DAT_180346d3c);
  local_res10[0] = DAT_180346d3c;
  uVar8 = FUN_180107480(local_res8[0],local_res10);
  uVar10 = uVar8 & 0xffffffff;
  iVar4 = (int)uVar8;
  if (2 < iVar4 - 1U) {
    iVar6 = FUN_180019ad0(local_res8[0]);
    if ((iVar6 != 0) || (iVar6 = FUN_180019ab0(local_res8[0]), pfVar5 = DAT_18070fb38, iVar6 == 0))
    {
      return uVar10;
    }
    fVar16 = (float)*(byte *)((longlong)DAT_18070fb38 + 0x3b) / DAT_180346d4c;
    auVar17 = ZEXT1264(CONCAT84(SUB128(ZEXT812(0),4),fVar16));
    if (iVar4 - 4U < 2) {
      fVar16 = fVar16 * local_res10[0] * DAT_180346d4c;
      DAT_18070fb38[0xe] = (float)((uint)DAT_18070fb38[0xe] & 0xffffff);
      pfVar5[0xe] = (float)((uint)pfVar5[0xe] | (int)fVar16 << 0x18);
    }
    lVar1 = *(longlong *)(pfVar5 + 0x20);
    FUN_180189880(local_168);
    lVar2 = *(longlong *)(lVar1 + 0x20);
    fVar16 = 0.0;
    local_res18 = 0.0;
    local_res1c = 0.0;
    if (lVar2 == 0) {
      uVar9 = local_res8[0] - *(short *)(lVar1 + 0x18);
      puVar3 = *(undefined4 **)(DAT_18070fb38 + 0x20);
      fVar18 = (float)(uVar9 & 0xf);
      fVar19 = (float)(uVar9 >> 4 & 0xf);
      if (*(longlong *)(DAT_18070fb38 + 0x1e) != 0) {
        fVar16 = (float)(int)*(char *)(*(longlong *)(DAT_18070fb38 + 0x1e) +
                                      (ulonglong)local_res8[0] * 2) * DAT_18070fb38[6] *
                 DAT_18070fb38[8];
      }
      local_158 = (uint)DAT_18070fb38[0x10] >> 3 & 2;
      local_160 = DAT_18070fb38[0xe];
      local_110 = DAT_18070fb38[0x11];
      local_148 = DAT_18070fb38[0x22];
      local_144 = DAT_18070fb38[0x22];
      local_128 = DAT_18070fb38[8] * DAT_18070fb38[6];
      local_124 = DAT_18070fb38[9] * DAT_18070fb38[7];
      local_130 = DAT_18070fb38[1];
      local_164 = *puVar3;
      local_15c = local_15c | 2;
      local_134 = *DAT_18070fb38 - fVar16;
      auVar14._0_4_ = (float)(int)*(short *)(puVar3 + 4);
      auVar14._4_8_ = SUB128(ZEXT812(0),4);
      auVar14._12_4_ = 0;
      auVar15 = ZEXT1664(auVar14);
      auVar11._0_4_ = (float)(int)*(short *)((longlong)puVar3 + 0x12);
      auVar11._4_8_ = SUB128(ZEXT812(0),4);
      auVar11._12_4_ = 0;
      auVar13 = ZEXT1664(auVar11);
      auVar11 = vunpcklps_avx(auVar14,auVar11);
      FUN_18018e7c0(local_168,auVar11._0_8_);
      FUN_18018e780(local_168,fVar18 * auVar15._0_4_,fVar19 * auVar13._0_4_,auVar15._0_8_,
                    auVar13._0_4_);
    }
    else {
      uVar7 = FUN_1801070f0(local_res8[0],lVar2,&local_res18);
      if (-1 < (int)uVar7) {
        auVar11 = vpcmpgtd_avx(ZEXT416(uVar7),ZEXT416(1));
        lVar1 = *(longlong *)(DAT_18070fb38 + 0x20);
        auVar11 = vblendvps_avx(ZEXT416(DAT_180346d38),auVar13._0_16_,auVar11);
        local_158 = (uint)DAT_18070fb38[0x10] >> 3 & 2;
        local_160 = DAT_18070fb38[0xe];
        local_110 = DAT_18070fb38[0x11];
        local_148 = DAT_18070fb38[0x22];
        local_144 = DAT_18070fb38[0x22];
        local_128 = DAT_18070fb38[8] * DAT_18070fb38[6];
        local_124 = DAT_18070fb38[9] * DAT_18070fb38[7];
        local_134 = *DAT_18070fb38;
        local_130 = DAT_18070fb38[1];
        local_164 = *(undefined4 *)
                     (*(longlong *)(*(longlong *)(lVar1 + 0x20) + 8) + (longlong)(int)uVar7 * 4);
        local_15c = local_15c | 2;
        if (DAT_18070fb38[0x16] == 8.40779e-44) {
          local_bc = 0x2d;
        }
        auVar12._0_4_ = (float)(int)*(short *)(lVar1 + 0x12);
        auVar12._4_8_ = SUB128(ZEXT812(0),4);
        auVar12._12_4_ = 0;
        auVar13 = ZEXT1664(auVar12);
        fVar16 = (float)(int)*(short *)(lVar1 + 0x10) * auVar11._0_4_;
        auVar15 = ZEXT464((uint)fVar16);
        auVar11 = vunpcklps_avx(ZEXT416((uint)fVar16),auVar12);
        FUN_18018e7c0(local_168,auVar11._0_8_);
        FUN_18018e780(local_168,auVar15._0_4_ * local_res18,auVar13._0_4_ * local_res1c,
                      auVar15._0_8_,auVar13._0_4_);
      }
    }
    local_14c = (undefined4)(longlong)pfVar5[0x14];
    local_150 = pfVar5[0x15];
    if (pfVar5[0x16] == 8.54792e-44) {
      FUN_18001a1c0(local_c0,local_res8,1);
      FUN_180187af0(local_168);
      fVar16 = auVar17._0_4_;
    }
    else {
      FUN_180187c00(local_168);
      fVar16 = auVar17._0_4_;
    }
    pfVar5 = DAT_18070fb38;
    uVar8 = uVar10;
    if (iVar4 - 4U < 2) {
      fVar16 = fVar16 * DAT_180346d4c;
      DAT_18070fb38[0xe] = (float)((uint)DAT_18070fb38[0xe] & 0xffffff);
      pfVar5[0xe] = (float)((uint)pfVar5[0xe] | (int)fVar16 << 0x18);
    }
  }
  return uVar8;
}



