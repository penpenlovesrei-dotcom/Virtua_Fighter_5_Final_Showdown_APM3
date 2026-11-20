// ===================================================
// 180072130  ->  FUN_180072130  (entree 180072130)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_180072130(undefined1 *param_1,int param_2)

{
  float fVar1;
  float fVar2;
  float fVar3;
  undefined1 auVar4 [16];
  undefined1 auVar5 [16];
  float fVar6;
  undefined4 uVar7;
  int iVar8;
  undefined1 *puVar9;
  undefined8 uVar10;
  ulonglong uVar11;
  ulonglong uVar12;
  longlong lVar13;
  ulonglong uVar14;
  uint uVar15;
  ulonglong uVar16;
  float fVar17;
  float fVar18;
  float fVar19;
  float fVar20;
  float fVar21;
  float fVar22;
  float fVar23;
  float fVar24;
  float fVar25;
  
  uVar14 = 0;
  *param_1 = 1;
  *(undefined4 *)(param_1 + 0x58) = 0;
  *(undefined2 *)(param_1 + 0x2b8) = 0;
  *(undefined4 *)(param_1 + 4) = 0x3f800000;
  param_1[8] = 1;
  if (param_2 == DAT_1806431c8) {
    *param_1 = DAT_1806431cc;
    *(undefined4 *)(param_1 + 0xc) = DAT_1806431d4;
    *(undefined8 *)(param_1 + 0x10) = DAT_1806431d8;
    *(undefined4 *)(param_1 + 0x18) = DAT_1806431e0;
    *(undefined4 *)(param_1 + 0x1c) = DAT_1806431e4;
    uVar10 = uRam00000001806431f0;
    *(undefined8 *)(param_1 + 0x20) = _DAT_1806431e8;
    *(undefined8 *)(param_1 + 0x28) = uVar10;
    *(undefined4 *)(param_1 + 0x30) = DAT_1806431f8;
    uVar7 = DAT_1806431d0;
    *(undefined4 *)(param_1 + 0x38) = DAT_1806431d0;
    *(undefined4 *)(param_1 + 0x34) = uVar7;
    puVar9 = param_1 + 0x6c;
    *(undefined4 *)(param_1 + 0x3c) = DAT_1806431fc;
    *(undefined4 *)(param_1 + 0x40) = DAT_180643200;
    uVar16 = uVar14;
    do {
      iVar8 = (int)uVar16;
      *(int *)(puVar9 + -0x10) = iVar8;
      *(undefined8 *)(puVar9 + -0xc) = 0x8a;
      *(undefined8 *)(puVar9 + -4) = 0;
      *(int *)(puVar9 + 4) = iVar8;
      *(undefined8 *)(puVar9 + 8) = 0x84;
      *(undefined8 *)(puVar9 + 0x10) = 0;
      *(int *)(puVar9 + 0x18) = iVar8;
      *(undefined8 *)(puVar9 + 0x1c) = 0x49;
      *(undefined8 *)(puVar9 + 0x24) = 0;
      *(int *)(puVar9 + 0x2c) = iVar8;
      *(undefined8 *)(puVar9 + 0x30) = 0x66;
      *(undefined8 *)(puVar9 + 0x38) = 0;
      *(int *)(puVar9 + 0x40) = iVar8;
      uVar16 = (ulonglong)(iVar8 + 1U);
      *(undefined8 *)(puVar9 + 0x44) = 0;
      *(undefined8 *)(puVar9 + 0x4c) = 0;
      puVar9 = puVar9 + 100;
    } while ((int)(iVar8 + 1U) < 2);
    uVar16 = (ulonglong)*(int *)(param_1 + 0x34);
    auVar4._8_8_ = 0;
    auVar4._0_8_ = uVar16;
    uVar10 = SUB168(ZEXT816(0x2c) * auVar4,0);
    if (SUB168(ZEXT816(0x2c) * auVar4,8) != 0) {
      uVar10 = 0xffffffffffffffff;
    }
    uVar11 = FUN_180218930(uVar10);
    uVar12 = uVar14;
    if ((uVar11 != 0) && (uVar12 = uVar11, uVar16 != 0)) {
      lVar13 = uVar11 + 0x14;
      do {
        *(undefined8 *)(lVar13 + -0x14) = 0;
        *(undefined8 *)(lVar13 + -0xc) = 0;
        *(undefined8 *)(lVar13 + -4) = 0;
        *(undefined8 *)(lVar13 + 4) = 0;
        *(undefined4 *)(lVar13 + 0xc) = 0;
        lVar13 = lVar13 + 0x2c;
        uVar16 = uVar16 - 1;
      } while (uVar16 != 0);
    }
    *(ulonglong *)(param_1 + 0x48) = uVar12;
    auVar5._8_8_ = 0;
    auVar5._0_8_ = (longlong)*(int *)(param_1 + 0x34);
    uVar10 = SUB168(ZEXT816(0x20) * auVar5,0);
    if (SUB168(ZEXT816(0x20) * auVar5,8) != 0) {
      uVar10 = 0xffffffffffffffff;
    }
    uVar10 = FUN_180218930(uVar10);
    *(undefined8 *)(param_1 + 0x50) = uVar10;
    uVar16 = uVar14;
    fVar23 = DAT_180346d38;
    fVar24 = DAT_18035008c;
    fVar25 = DAT_1803480b8;
    if (0 < *(int *)(param_1 + 0x34)) {
      do {
        lVar13 = *(longlong *)(param_1 + 0x48);
        *(undefined8 *)(uVar16 + lVar13) = 0;
        *(undefined8 *)(uVar16 + 8 + lVar13) = 0;
        *(undefined4 *)(uVar16 + 0x10 + lVar13) = 0xbf800000;
        *(undefined8 *)(uVar16 + 0x14 + lVar13) = 0;
        *(undefined8 *)(uVar16 + 0x1c + lVar13) = 0;
        *(undefined4 *)(uVar16 + 0x24 + lVar13) = 0x3f800000;
        *(undefined4 *)(uVar16 + 0x28 + lVar13) = 0x3f800000;
        iVar8 = FUN_18030e650();
        fVar22 = (float)(iVar8 % 10000) * fVar24 * fVar25;
        iVar8 = FUN_18030e650();
        fVar21 = (float)(iVar8 % 10000) * fVar24 * fVar23;
        iVar8 = FUN_18030e650();
        fVar20 = fVar23 * *(float *)(param_1 + 0xc);
        fVar19 = (float)(iVar8 % 10000) * fVar24 * fVar23;
        iVar8 = FUN_18030e650();
        fVar17 = fVar23 * *(float *)(param_1 + 0xc);
        fVar18 = (float)(iVar8 % 10000) * fVar24 * fVar20;
        iVar8 = FUN_18030e650();
        fVar6 = (float)(iVar8 % 10000) * fVar24 * fVar17;
        lVar13 = *(longlong *)(param_1 + 0x48);
        fVar1 = *(float *)(param_1 + 0x30);
        fVar2 = *(float *)(param_1 + 0x18);
        fVar3 = *(float *)(param_1 + 0x10);
        *(undefined4 *)(uVar16 + 4 + lVar13) = 0x3f000000;
        uVar15 = (int)uVar14 + 1;
        uVar14 = (ulonglong)uVar15;
        *(float *)(uVar16 + lVar13) = (fVar6 + fVar6) - fVar17;
        *(float *)(uVar16 + 8 + lVar13) = (fVar18 + fVar18) - fVar20;
        *(float *)(uVar16 + 0xc + lVar13) = ((fVar19 + fVar19) - fVar23) + fVar3;
        *(float *)(uVar16 + 0x14 + lVar13) = ((fVar21 + fVar21) - fVar23) + fVar2;
        *(undefined4 *)(uVar16 + 0x10 + lVar13) = 0;
        *(float *)(uVar16 + 0x24 + lVar13) = ((fVar22 + fVar22) - fVar25) + fVar1;
        *(undefined4 *)(uVar16 + 0x28 + lVar13) = 0x3f800000;
        uVar16 = uVar16 + 0x2c;
      } while ((int)uVar15 < *(int *)(param_1 + 0x34));
    }
    FUN_18010ca20(4,1);
    FUN_18010bdc0(0,FUN_1800729c0,param_1);
  }
  return;
}



// ===================================================
// 1800725A0  ->  FUN_1800725a0  (entree 1800725a0)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1800725a0(longlong param_1,float param_2)

{
  float fVar1;
  float fVar2;
  float fVar3;
  bool bVar4;
  float *pfVar5;
  float *pfVar6;
  longlong lVar7;
  float *pfVar8;
  int iVar9;
  float fVar10;
  undefined1 auVar11 [16];
  undefined1 auVar12 [16];
  float fVar13;
  undefined1 auVar14 [16];
  undefined1 auVar15 [16];
  undefined1 auVar16 [16];
  float fVar17;
  float fVar18;
  float fVar19;
  float fVar20;
  undefined1 auVar21 [64];
  float fVar22;
  undefined1 auVar23 [64];
  undefined1 auVar24 [64];
  undefined1 auVar25 [64];
  float fVar26;
  float fVar27;
  undefined1 auVar28 [64];
  
  pfVar6 = *(float **)(param_1 + 0x48);
  iVar9 = 0;
  auVar25 = ZEXT464((uint)DAT_180346d3c);
  fVar1 = DAT_1806431a8 * param_2;
  fVar2 = param_2 * DAT_1806431bc;
  fVar3 = DAT_1806431c0 * param_2;
  fVar26 = *(float *)(param_1 + 0xc) * DAT_180346d38 + DAT_180346d3c;
  auVar28 = ZEXT464((uint)fVar26);
  if (0 < *(int *)(param_1 + 0x38)) {
    pfVar8 = pfVar6 + 8;
    auVar21 = ZEXT1664(CONCAT412(_UNK_180346d6c,
                                 CONCAT48(_UNK_180346d68,
                                          CONCAT44(_UNK_180346d64,(uint)fVar26 ^ DAT_180346d60))));
    auVar23 = ZEXT864(DAT_180346d50);
    auVar24 = ZEXT1264(ZEXT812(0));
    fVar26 = DAT_180348ab0;
    fVar27 = DAT_18034a510;
    do {
      lVar7 = (longlong)*(int *)(param_1 + 0x124);
      if (0 < lVar7) {
        pfVar5 = (float *)(param_1 + 0x134);
        do {
          auVar14._8_8_ = 0;
          auVar14._0_8_ = *(ulonglong *)pfVar6;
          fVar19 = (float)*(ulonglong *)pfVar6 - pfVar5[-2];
          auVar14 = vshufps_avx(auVar14,auVar14,0x55);
          fVar20 = auVar14._0_4_ - pfVar5[-1];
          fVar22 = pfVar6[2] - *pfVar5;
          fVar10 = fVar19 * fVar19 + fVar20 * fVar20 + fVar22 * fVar22;
          fVar13 = auVar25._0_4_ + pfVar5[1];
          if (fVar10 <= fVar13 * fVar13) {
            fVar13 = auVar24._0_4_;
            if (pfVar5[-3] == 0.0) {
              auVar16._8_8_ = 0;
              auVar16._0_8_ = *(ulonglong *)(pfVar5 + 3);
              fVar18 = pfVar5[6];
              auVar14 = vshufps_avx(auVar16,auVar16,0x55);
              fVar17 = (float)*(ulonglong *)(pfVar5 + 3) * fVar18;
              fVar13 = auVar14._0_4_ * fVar18;
              fVar18 = pfVar5[5] * fVar18;
            }
            else {
              fVar17 = fVar13;
              fVar18 = fVar13;
              if (pfVar5[-3] == 1.4013e-45) {
                if (fVar27 <= fVar10) {
                  auVar15._0_4_ = auVar25._0_4_ / fVar10;
                  auVar15._4_12_ = auVar25._4_12_;
                  auVar14 = vminss_avx(auVar15,auVar25._0_16_);
                  auVar21 = ZEXT1664(auVar14);
                  fVar10 = (float)FUN_18030381c(fVar10);
                  if (fVar10 != auVar24._0_4_) {
                    fVar10 = auVar25._0_4_ / fVar10;
                    fVar19 = fVar10 * fVar19;
                    fVar20 = fVar10 * fVar20;
                    fVar22 = fVar10 * fVar22;
                  }
                  fVar18 = auVar21._0_4_ * pfVar5[6];
                  fVar17 = fVar19 * fVar18;
                  fVar13 = fVar20 * fVar18;
                  fVar18 = fVar22 * fVar18;
                }
                else {
                  fVar17 = pfVar5[6];
                  fVar13 = fVar17 * fVar13;
                  fVar18 = fVar13;
                }
              }
            }
            pfVar8[-2] = fVar17 * param_2 * fVar26 + pfVar8[-2];
            *pfVar8 = fVar18 * param_2 * fVar26 + *pfVar8;
            pfVar8[-1] = fVar13 * param_2 * fVar26 + pfVar8[-1];
          }
          pfVar5 = pfVar5 + 10;
          lVar7 = lVar7 + -1;
        } while (lVar7 != 0);
        auVar21 = ZEXT1664(CONCAT412(auVar28._12_4_ ^ _UNK_180346d6c,
                                     CONCAT48(auVar28._8_4_ ^ _UNK_180346d68,
                                              CONCAT44(auVar28._4_4_ ^ _UNK_180346d64,
                                                       auVar28._0_4_ ^ DAT_180346d60))));
        auVar23 = ZEXT864(DAT_180346d50);
      }
      fVar10 = pfVar8[-2];
      fVar13 = *pfVar8;
      fVar19 = (fVar10 + pfVar8[-5]) * param_2 + *pfVar6;
      fVar20 = (fVar13 + pfVar8[-3]) * param_2 + pfVar8[-6];
      auVar11._0_8_ = (double)fVar10;
      auVar11._8_8_ = 0;
      auVar14 = vandpd_avx(auVar11,auVar23._0_16_);
      pfVar8[-1] = 0.0;
      *pfVar6 = fVar19;
      pfVar8[-6] = fVar20;
      bVar4 = fVar27 < (float)auVar14._0_8_;
      if (bVar4) {
        fVar10 = fVar10 - fVar10 * fVar1;
        pfVar8[-2] = fVar10;
      }
      auVar12._0_8_ = (double)fVar13;
      auVar12._8_8_ = 0;
      auVar14 = vandpd_avx(auVar12,auVar23._0_16_);
      if ((float)auVar14._0_8_ <= fVar27) {
        if (bVar4) goto LAB_18007288f;
        auVar16 = ZEXT416((uint)(fVar3 + pfVar8[2]));
        auVar14 = vcmpss_avx(auVar16,auVar25._0_16_,1);
        auVar14 = vblendvps_avx(auVar25._0_16_,auVar16,auVar14);
        fVar10 = auVar14._0_4_;
      }
      else {
        fVar13 = fVar13 - fVar13 * fVar1;
        *pfVar8 = fVar13;
LAB_18007288f:
        auVar16 = ZEXT416((uint)(pfVar8[2] -
                                (fVar10 * fVar10 + auVar24._0_4_ + fVar13 * fVar13) * fVar2));
        auVar14 = vcmpss_avx(auVar24._0_16_,auVar16,1);
        auVar14 = vblendvps_avx(auVar24._0_16_,auVar16,auVar14);
        fVar10 = auVar14._0_4_;
      }
      pfVar8[2] = fVar10;
      if (auVar21._0_4_ <= fVar19) {
        auVar14 = vcmpss_avx(auVar28._0_16_,ZEXT416((uint)fVar19),1);
        auVar14 = vblendvps_avx(ZEXT416((uint)fVar19),auVar21._0_16_,auVar14);
        *pfVar6 = auVar14._0_4_;
      }
      else {
        *pfVar6 = auVar28._0_4_;
      }
      if (auVar21._0_4_ <= fVar20) {
        auVar14 = vcmpss_avx(auVar28._0_16_,ZEXT416((uint)fVar20),1);
        auVar14 = vblendvps_avx(ZEXT416((uint)fVar20),auVar21._0_16_,auVar14);
        pfVar8[-6] = auVar14._0_4_;
      }
      else {
        pfVar8[-6] = auVar28._0_4_;
      }
      iVar9 = iVar9 + 1;
      pfVar6 = pfVar6 + 0xb;
      pfVar8 = pfVar8 + 0xb;
    } while (iVar9 < *(int *)(param_1 + 0x38));
  }
  return;
}



// ===================================================
// 180071BC0  ->  FUN_180071bc0  (entree 180071bc0)
// ===================================================

void FUN_180071bc0(longlong param_1,float param_2)

{
  float fVar1;
  float fVar2;
  undefined4 uVar3;
  char cVar4;
  longlong lVar5;
  longlong lVar6;
  longlong lVar7;
  int *piVar8;
  int *piVar9;
  longlong lVar10;
  int iVar11;
  undefined1 auVar12 [16];
  undefined1 extraout_var [56];
  float fVar13;
  undefined8 uVar14;
  undefined1 in_ZMM7 [64];
  undefined1 auVar15 [64];
  undefined1 auVar16 [64];
  undefined1 auVar17 [64];
  undefined1 auVar18 [64];
  float local_b8;
  float fStack_b4;
  float local_b0;
  undefined8 local_a8;
  float local_a0;
  undefined4 local_90;
  undefined1 local_48 [16];
  
  iVar11 = 0;
  auVar17 = ZEXT1264(ZEXT812(0));
  local_a8 = 0;
  local_a0 = 0.0;
  local_b8 = 0.0;
  fStack_b4 = 0.0;
  local_b0 = 0.0;
  *(undefined4 *)(param_1 + 0x124) = 0;
  lVar5 = FUN_1801509b0();
  if (lVar5 != 0) {
    piVar8 = (int *)(param_1 + 0x60);
    local_48 = in_ZMM7._0_16_;
    auVar18 = ZEXT464(DAT_180346d3c);
    do {
      lVar6 = FUN_180150920(lVar5,iVar11);
      if (((lVar6 != 0) && (cVar4 = FUN_1801508a0(lVar5,iVar11), cVar4 != '\0')) &&
         (lVar6 = FUN_1801509c0(lVar5,iVar11), lVar6 != 0)) {
        lVar10 = 5;
        piVar9 = piVar8;
        do {
          lVar7 = FUN_1800e0280(lVar6,(longlong)*piVar9);
          if (lVar7 != 0) {
            fVar13 = *(float *)(lVar7 + 0x1c);
            fVar1 = *(float *)(lVar7 + 0x2c);
            auVar12._4_4_ = (int)((ulonglong)local_a8 >> 0x20);
            auVar12._0_4_ = *(float *)(lVar7 + 0xc);
            auVar12._8_8_ = 0;
            auVar12 = vinsertps_avx(auVar12,ZEXT416((uint)fVar13),0x10);
            local_a8 = auVar12._0_8_;
            auVar15 = ZEXT1664(auVar12);
            local_a0 = fVar1;
            uVar14 = local_a8;
            if (*(char *)(param_1 + 8) == '\0') {
              local_b0 = auVar18._0_4_ / param_2;
              local_b8 = (*(float *)(lVar7 + 0xc) - (float)piVar9[1]) * local_b0;
              fStack_b4 = (fVar13 - (float)piVar9[2]) * local_b0;
              local_b0 = (fVar1 - (float)piVar9[3]) * local_b0;
              auVar16._0_8_ =
                   FUN_18030381c(local_b8 * local_b8 + fStack_b4 * fStack_b4 + local_b0 * local_b0);
              uVar3 = DAT_1806431b4;
              uVar14 = auVar15._0_8_;
              auVar16._8_56_ = extraout_var;
              auVar12 = vminss_avx(ZEXT416(DAT_1806431a0),auVar16._0_16_);
              auVar16 = ZEXT1664(auVar12);
              if (*piVar9 == 0) {
                if (((fVar13 < DAT_1806431b8) && (DAT_1806431b8 <= (float)piVar9[2])) &&
                   (lVar7 = (longlong)*(int *)(param_1 + 0x124), *(int *)(param_1 + 0x124) < 10)) {
                  fVar13 = DAT_1806431b0 * DAT_1806431b0;
                  *(float *)(param_1 + 0x138 + lVar7 * 0x28) = DAT_1806431b0;
                  auVar12 = vunpcklps_avx(auVar17._0_16_,auVar18._0_16_);
                  local_90 = auVar17._0_4_;
                  *(longlong *)(param_1 + 0x140 + lVar7 * 0x28) = auVar12._0_8_;
                  *(undefined8 *)(param_1 + 300 + lVar7 * 0x28) = uVar14;
                  *(undefined4 *)(param_1 + 0x148 + lVar7 * 0x28) = local_90;
                  *(float *)(param_1 + 0x13c + lVar7 * 0x28) = fVar13;
                  *(undefined4 *)(param_1 + 0x14c + lVar7 * 0x28) = uVar3;
                  *(undefined4 *)(param_1 + 0x128 + lVar7 * 0x28) = 1;
                  *(float *)(param_1 + 0x134 + lVar7 * 0x28) = fVar1;
LAB_180071eb0:
                  *(int *)(param_1 + 0x124) = *(int *)(param_1 + 0x124) + 1;
                }
              }
              else if ((DAT_180643198 <= auVar12._0_4_) &&
                      (lVar7 = (longlong)*(int *)(param_1 + 0x124), *(int *)(param_1 + 0x124) < 10))
              {
                FUN_18004b7d0(&local_b8);
                fVar13 = auVar16._0_4_ * DAT_1806431ac;
                fVar2 = DAT_1806431a4 * DAT_1806431a4;
                *(float *)(param_1 + 0x138 + lVar7 * 0x28) = DAT_1806431a4;
                *(ulonglong *)(param_1 + 0x140 + lVar7 * 0x28) = CONCAT44(fStack_b4,local_b8);
                uVar14 = auVar15._0_8_;
                *(undefined8 *)(param_1 + 300 + lVar7 * 0x28) = uVar14;
                *(float *)(param_1 + 0x148 + lVar7 * 0x28) = local_b0;
                *(float *)(param_1 + 0x13c + lVar7 * 0x28) = fVar2;
                *(float *)(param_1 + 0x14c + lVar7 * 0x28) = fVar13;
                *(undefined4 *)(param_1 + 0x128 + lVar7 * 0x28) = 1;
                *(float *)(param_1 + 0x134 + lVar7 * 0x28) = fVar1;
                goto LAB_180071eb0;
              }
            }
            *(undefined8 *)(piVar9 + 1) = uVar14;
            piVar9[3] = (int)fVar1;
          }
          piVar9 = piVar9 + 5;
          lVar10 = lVar10 + -1;
        } while (lVar10 != 0);
      }
      piVar8 = piVar8 + 0x19;
      iVar11 = iVar11 + 1;
    } while (iVar11 < 2);
  }
  return;
}



