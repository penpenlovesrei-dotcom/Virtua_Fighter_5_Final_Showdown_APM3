// ===================================================
// 180083895  ->  FUN_180082fb0  (entree 180082fb0)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_180082fb0(longlong param_1)

{
  float *pfVar1;
  char cVar2;
  int iVar3;
  longlong lVar4;
  undefined8 uVar5;
  ulonglong *puVar6;
  uint uVar7;
  uint *puVar8;
  longlong lVar9;
  float *pfVar10;
  uint uVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  undefined1 auVar15 [16];
  undefined1 auVar16 [16];
  undefined1 auVar17 [16];
  float fVar18;
  undefined1 auVar19 [16];
  float fVar20;
  undefined1 auVar21 [16];
  float fVar22;
  undefined4 uVar23;
  float fVar24;
  undefined1 auVar25 [64];
  undefined1 auVar26 [64];
  undefined4 uVar27;
  float fVar28;
  undefined1 auVar29 [64];
  undefined4 uVar30;
  float fVar31;
  float fVar32;
  float fVar33;
  undefined1 auVar34 [64];
  undefined1 auVar35 [64];
  undefined1 auVar36 [64];
  undefined1 auVar37 [64];
  float local_res8 [2];
  float local_res10;
  float local_res18;
  float local_res20;
  undefined8 local_1d8;
  float local_1d0;
  undefined8 local_1c8;
  float local_1c0;
  float local_1b8;
  float local_1b4;
  float local_1b0;
  float local_1a8;
  float local_1a4;
  float local_1a0;
  float local_198;
  float local_194;
  undefined8 local_190;
  float *local_188;
  undefined1 local_180 [16];
  float local_170;
  float local_16c;
  uint local_168;
  undefined1 local_158 [64];
  undefined8 local_118;
  undefined1 local_108 [16];
  undefined8 local_f8;
  
  local_118 = 0xfffffffffffffffe;
  uVar11 = 0;
  if (0 < *(int *)(param_1 + 0x210)) {
    do {
      if ((uVar11 < 0x3c) &&
         (puVar8 = &DAT_1806f21d0 + (longlong)(int)uVar11 * 0x18, puVar8 != (uint *)0x0)) {
        uVar7 = *puVar8;
        *puVar8 = (uVar7 & 0x20) * 2 | (uVar7 & 8) * 2 | uVar7 & 0xffffff84;
      }
      uVar11 = uVar11 + 1;
    } while ((int)uVar11 < *(int *)(param_1 + 0x210));
  }
  cVar2 = FUN_180041a80(param_1 + 0x140);
  auVar34 = ZEXT1264(ZEXT812(0));
  if ((cVar2 == '\0') || (cVar2 = FUN_180041180(param_1 + 0x140), cVar2 == '\0')) {
    cVar2 = FUN_180041a80(param_1 + 0x138);
    if ((cVar2 != '\0') &&
       ((cVar2 = FUN_180041180(param_1 + 0x138), cVar2 != '\0' &&
        (uVar11 = 0, 0 < *(int *)(param_1 + 0x210))))) {
      do {
        if (uVar11 < 0x3c) {
          lVar9 = (longlong)(int)uVar11;
          puVar8 = &DAT_1806f21d0 + lVar9 * 0x18;
          if ((puVar8 != (uint *)0x0) && (lVar4 = FUN_180044a90(param_1 + 0x138), lVar4 != 0)) {
            uVar30 = *(undefined4 *)(lVar4 + 0x2c);
            uVar27 = *(undefined4 *)(lVar4 + 0x1c);
            uVar23 = *(undefined4 *)(lVar4 + 0xc);
            local_1d0 = auVar34._0_4_;
            local_1d8 = CONCAT44(local_1d0,local_1d0);
            FUN_18006f150(lVar4,&local_1d8);
            (&DAT_1806f220c)[lVar9 * 0x18] = uVar23;
            (&DAT_1806f2210)[lVar9 * 0x18] = uVar27;
            (&DAT_1806f2214)[lVar9 * 0x18] = uVar30;
            (&DAT_1806f2218)[lVar9 * 0x18] = (float)local_1d8;
            (&DAT_1806f221c)[lVar9 * 0x18] = local_1d8._4_4_;
            (&DAT_1806f2220)[lVar9 * 0x18] = local_1d0;
            *puVar8 = *puVar8 | 0x20;
          }
        }
        uVar11 = uVar11 + 1;
      } while ((int)uVar11 < *(int *)(param_1 + 0x210));
    }
  }
  else {
    uVar11 = 0;
    if (0 < *(int *)(param_1 + 0x210)) {
      do {
        if (uVar11 < 0x3c) {
          lVar9 = (longlong)(int)uVar11;
          puVar8 = &DAT_1806f21d0 + lVar9 * 0x18;
          if ((puVar8 != (uint *)0x0) && (lVar4 = FUN_180044a90(param_1 + 0x140), lVar4 != 0)) {
            uVar30 = *(undefined4 *)(lVar4 + 0x2c);
            uVar27 = *(undefined4 *)(lVar4 + 0x1c);
            uVar23 = *(undefined4 *)(lVar4 + 0xc);
            local_1d0 = auVar34._0_4_;
            local_1d8 = CONCAT44(local_1d0,local_1d0);
            FUN_18006f150(lVar4,&local_1d8);
            (&DAT_1806f220c)[lVar9 * 0x18] = uVar23;
            (&DAT_1806f2210)[lVar9 * 0x18] = uVar27;
            (&DAT_1806f2214)[lVar9 * 0x18] = uVar30;
            (&DAT_1806f2218)[lVar9 * 0x18] = (float)local_1d8;
            (&DAT_1806f221c)[lVar9 * 0x18] = local_1d8._4_4_;
            (&DAT_1806f2220)[lVar9 * 0x18] = local_1d0;
            *puVar8 = *puVar8 | 8;
          }
        }
        uVar11 = uVar11 + 1;
      } while ((int)uVar11 < *(int *)(param_1 + 0x210));
    }
  }
  iVar3 = *(int *)(param_1 + 0x144);
  if ((iVar3 != 0) && (iVar3 != 4)) {
    uVar11 = 0;
    if (0 < *(int *)(param_1 + 0x210)) {
      do {
        if ((uVar11 < 0x3c) &&
           (puVar8 = &DAT_1806f21d0 + (longlong)(int)uVar11 * 0x18, puVar8 != (uint *)0x0)) {
          uVar7 = *puVar8;
          if ((uVar7 & 0x28) == 0) {
            uVar7 = uVar7 | 1;
            *puVar8 = uVar7;
          }
          if ((((byte)uVar7 & 0x18) == 0x18) || ((uVar7 & 0x20) != 0)) {
            *puVar8 = uVar7 | 1;
          }
        }
        uVar11 = uVar11 + 1;
      } while ((int)uVar11 < *(int *)(param_1 + 0x210));
      iVar3 = *(int *)(param_1 + 0x144);
    }
    if (iVar3 != 4) {
      return;
    }
  }
  local_180 = (undefined1  [16])0x0;
  uVar5 = FUN_1800827d0(local_180);
  local_180._0_8_ = uVar5;
  local_108 = (undefined1  [16])0x0;
  local_f8 = 0;
  local_1b8 = auVar34._0_4_;
  auVar29 = ZEXT464(DAT_180346d3c);
  local_168 = DAT_180346d3c;
  local_1b4 = local_1b8;
  local_1b0 = local_1b8;
  local_1a8 = local_1b8;
  local_1a4 = local_1b8;
  local_1a0 = local_1b8;
  local_170 = local_1b8;
  local_16c = local_1b8;
  FUN_180211a00(local_158);
  local_194 = (float)FUN_18018f600(1);
  local_194 = local_194 * DAT_180346d38;
  puVar6 = (ulonglong *)FUN_180051950(&local_1c8);
  auVar25 = ZEXT864(*puVar6);
  local_1d0 = *(float *)(puVar6 + 1);
  puVar6 = (ulonglong *)FUN_180051830(&local_1c8);
  local_1c8 = *puVar6;
  auVar19._8_8_ = 0;
  auVar19._0_8_ = local_1c8;
  local_1c0 = *(float *)(puVar6 + 1);
  fVar31 = local_1c0 - local_1d0;
  auVar15 = vshufps_avx(auVar25._0_16_,auVar25._0_16_,0x55);
  local_res20 = auVar15._0_4_;
  auVar15 = vshufps_avx(auVar19,auVar19,0x55);
  fVar12 = auVar15._0_4_ - local_res20;
  local_1d8._0_4_ = auVar25._0_4_;
  fVar24 = (float)local_1c8 - (float)local_1d8;
  local_1d8 = auVar25._0_8_;
  local_res18 = (float)FUN_18030381c(fVar12 * fVar12 + fVar24 * fVar24 + fVar31 * fVar31);
  local_res8[0] = auVar29._0_4_;
  if (DAT_180356580 <= (double)local_res18) {
    local_res18 = local_res8[0] / local_res18;
    local_res10 = fVar24 * local_res18;
    local_res8[0] = fVar12 * local_res18;
    local_res18 = fVar31 * local_res18;
  }
  else {
    local_res10 = auVar34._0_4_;
    local_res18 = local_res10;
  }
  auVar15._0_8_ = (double)local_1d0;
  auVar15._8_8_ = 0;
  auVar15 = vandpd_avx(auVar15,_DAT_180346d50);
  auVar21._0_4_ = (float)auVar15._0_8_;
  auVar21._4_12_ = auVar15._4_12_;
  auVar16._0_8_ = (double)(float)local_1d8;
  auVar16._8_8_ = 0;
  auVar15 = vandpd_avx(auVar16,_DAT_180346d50);
  auVar17._0_4_ = (float)auVar15._0_8_;
  auVar17._4_12_ = auVar15._4_12_;
  auVar15 = vmaxss_avx(auVar21,auVar17);
  local_198 = auVar15._0_4_;
  uVar11 = 0;
  if (0 < *(int *)(param_1 + 0x210)) {
    pfVar10 = (float *)(param_1 + 0x23c);
    fVar31 = DAT_180348aa4;
    do {
      pfVar1 = *(float **)(pfVar10 + -9);
      lVar9 = (longlong)(int)uVar11;
      lVar4 = lVar9 * 0x30;
      auVar35 = ZEXT1664(auVar34._0_16_);
      fVar12 = *pfVar10;
      auVar25 = ZEXT464((uint)fVar12);
      fVar24 = (float)local_1d8;
      local_188 = pfVar1;
      if (auVar34._0_4_ < fVar12) {
        fVar12 = (float)FUN_18030aa40(DAT_180356588,DAT_180356598 - fVar12);
        fVar13 = (float)FUN_18030eb80(auVar25._0_8_);
        auVar35 = ZEXT464((uint)(fVar13 * (fVar12 + fVar12)));
        *pfVar10 = auVar25._0_4_ - auVar29._0_4_;
      }
      fVar12 = *pfVar1;
      if (pfVar10[-7] != 0.0) {
        fVar12 = pfVar10[-6];
      }
      auVar25 = ZEXT464((uint)pfVar1[4]);
      auVar36 = ZEXT464((uint)pfVar1[3]);
      auVar37 = ZEXT464((uint)pfVar1[2]);
      fVar13 = local_1d0;
      FUN_180213910(local_158);
      FUN_180212eb0(local_158,fVar31 * pfVar1[6]);
      FUN_180214000(local_158,&local_170,&local_1a8);
      local_1c8 = CONCAT44(auVar34._0_4_,auVar34._0_4_);
      local_1c0 = DAT_180346d38;
      FUN_180213fa0(local_158,&local_1c8,&local_1b8);
      fVar13 = (auVar25._0_4_ + local_1b0) - fVar13;
      fVar32 = (auVar36._0_4_ + local_1b4) - local_res20;
      fVar24 = (auVar37._0_4_ + local_1b8) - fVar24;
      fVar14 = (float)FUN_18030381c(fVar24 * fVar24 + fVar32 * fVar32 + fVar13 * fVar13);
      fVar28 = auVar29._0_4_;
      auVar15 = auVar29._0_16_;
      fVar33 = auVar34._0_4_;
      fVar18 = fVar28;
      fVar20 = fVar33;
      fVar22 = fVar33;
      if (DAT_180356580 <= (double)fVar14) {
        fVar14 = fVar28 / fVar14;
        fVar18 = fVar32 * fVar14;
        fVar20 = fVar24 * fVar14;
        fVar22 = fVar13 * fVar14;
      }
      if (fVar18 * local_1a4 + fVar20 * local_1a8 + fVar22 * local_1a0 < fVar33) {
LAB_180083663:
        local_190 = 0;
LAB_180083670:
        auVar26 = ZEXT1664(auVar15);
LAB_180083677:
        if ((uVar11 < 0x3c) && (puVar8 = &DAT_1806f21d0 + lVar9 * 0x18, puVar8 != (uint *)0x0)) {
          uVar7 = ((int)pfVar10[-7] << 2 ^ *puVar8) & 4 ^ *puVar8;
          *puVar8 = uVar7;
          (&DAT_1806f21d8)[lVar9 * 0x18] = auVar26._0_4_;
          if (auVar26._0_4_ < DAT_180350efc) {
            *puVar8 = uVar7 | 2;
          }
          (&DAT_1806f21f4)[lVar9 * 0x18] = auVar35._0_4_ * fVar31;
        }
      }
      else {
        local_190 = 0x100000000;
        fVar24 = local_1a4 * local_res8[0] + local_1a8 * local_res10 + local_1a0 * local_res18;
        fVar24 = fVar24 * fVar24;
        auVar19 = vminss_avx(ZEXT416(DAT_18034af40),
                             ZEXT416((uint)((((fVar28 + local_198) - local_194) -
                                            fVar24 * fVar24 * DAT_1803480b8) * DAT_180356578)));
        if (*(int *)(param_1 + 0x14c) != 0) {
          auVar16 = vpcmpeqd_avx(ZEXT416((uint)pfVar10[-0x37]),ZEXT416(3));
          auVar19 = vblendvps_avx(auVar19,auVar15,auVar16);
        }
        if (*(int *)(param_1 + 0xd64) == 1) goto LAB_180083663;
        auVar15 = auVar19;
        if (*(int *)(param_1 + 0xd64) != 2) goto LAB_180083670;
        auVar26 = ZEXT1664(auVar34._0_16_);
        if (uVar11 < 0x3c) {
          puVar8 = &DAT_1806f21d0 + lVar9 * 0x18;
          if (puVar8 != (uint *)0x0) {
            *puVar8 = *puVar8 | 1;
          }
          goto LAB_180083677;
        }
      }
      fVar24 = auVar26._0_4_;
      if (DAT_180350efc <= fVar24) {
        if (*(int *)(param_1 + 0x14c) == 0) {
          FUN_18024bbc0();
          FUN_18024bdb0(auVar37._0_8_,auVar36._0_8_,auVar25._0_8_);
          pfVar1 = local_188;
          FUN_18024bc70(local_188[6],auVar34._0_8_,auVar29._0_8_,auVar34._0_8_);
          FUN_18024bc70(auVar35._0_8_,auVar29._0_8_,auVar34._0_8_,auVar34._0_8_);
          if (fVar24 < fVar28) {
            FUN_1800ed1d0(0x800);
            FUN_1800ecef0(fVar12,auVar26._0_8_);
            FUN_1800ed1d0(0);
          }
          else {
            FUN_1800ec460(fVar12);
          }
          FUN_18024bb70();
          if ((*(int *)(param_1 + 0x144) == 4) && (iVar3 = FUN_18018f580(), iVar3 == 0x27)) {
            FUN_18024bbc0();
            FUN_18024bdb0(auVar37._0_8_,
                          CONCAT44(auVar36._4_4_ ^ _UNK_180346d64,auVar36._0_4_ ^ DAT_180346d60),
                          auVar25._0_8_);
            FUN_18024bc70(pfVar1[6],auVar34._0_8_,auVar29._0_8_,auVar34._0_8_);
            FUN_18024bc70(auVar35._0_8_,auVar29._0_8_,auVar34._0_8_,auVar34._0_8_);
            FUN_1800ed1d0(0x80000200);
            FUN_1800ec460(0xb1f009d);
            FUN_1800ed1d0(0);
            FUN_18024bb70();
          }
        }
        else {
          FUN_180213910(local_158);
          FUN_180213180(local_158,auVar37._0_8_,auVar36._0_8_,auVar25._0_8_);
          FUN_180212eb0(local_158,fVar31 * local_188[6]);
          lVar9 = param_1 + 0x154 + lVar4;
          FUN_180046490(lVar9,1);
          FUN_180045fc0(lVar9,local_158);
          FUN_180046450(lVar9,auVar26._0_8_);
          FUN_180045f20(lVar9,fVar24 < fVar28);
          FUN_1800460d0(lVar9,1);
          cVar2 = FUN_180041a80(lVar4 + param_1 + 0x15c);
          if (cVar2 != '\0') {
            FUN_1800460d0(lVar4 + param_1 + 0x15c,1);
          }
        }
      }
      else if (*(int *)(param_1 + 0x14c) != 0) {
        FUN_180046490(param_1 + 0x154 + lVar4,0);
      }
      uVar11 = uVar11 + 1;
      pfVar10 = pfVar10 + 0xc;
    } while ((int)uVar11 < *(int *)(param_1 + 0x210));
  }
  FUN_180083960(local_180,local_res8,*(undefined8 *)local_180._0_8_);
  FUN_1802fdd80(local_180._0_8_,0x48);
  return;
}



