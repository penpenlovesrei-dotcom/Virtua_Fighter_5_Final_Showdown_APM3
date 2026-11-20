// ===================================================
// 18006FD66  ->  FUN_18006fc30  (entree 18006fc30)
// ===================================================

ulonglong FUN_18006fc30(longlong param_1)

{
  undefined1 auVar1 [16];
  double dVar2;
  float fVar3;
  int iVar4;
  int iVar5;
  undefined4 uVar6;
  uint uVar7;
  undefined8 uVar8;
  ulonglong uVar9;
  longlong lVar10;
  longlong lVar11;
  ulonglong uVar12;
  longlong lVar13;
  undefined4 *puVar14;
  longlong lVar15;
  float fVar16;
  undefined4 uVar17;
  undefined4 uVar18;
  undefined4 uVar19;
  undefined1 auVar20 [64];
  undefined1 auVar21 [64];
  undefined1 auVar22 [64];
  undefined4 local_128;
  undefined4 local_124;
  undefined4 local_120;
  undefined8 local_118;
  undefined8 uStack_110;
  undefined8 uStack_108;
  undefined8 uStack_100;
  undefined8 local_f8;
  undefined8 uStack_f0;
  undefined8 uStack_e8;
  undefined8 uStack_e0;
  undefined8 local_d8;
  undefined8 uStack_d0;
  undefined8 uStack_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  
  iVar5 = 0;
  auVar20 = ZEXT1264(ZEXT812(0));
  if ((*(char *)(param_1 + 0xb0) != '\0') && (0 < *(int *)(param_1 + 0xb4))) {
    lVar13 = *(longlong *)(param_1 + 0x68);
    if (lVar13 != lVar13 + *(longlong *)(param_1 + 0x58) * 4) {
      do {
        iVar4 = FUN_180041440(lVar13);
        if (iVar4 == 0x7f4) {
          if (*(int *)(param_1 + 0xb4) == 3) {
            FUN_1800460d0();
          }
          else {
            FUN_180046230(lVar13,auVar20._0_8_);
            FUN_1800463b0(lVar13,0);
            FUN_1800460d0(lVar13,1);
            if (*(int *)(param_1 + 0xb4) == 1) {
              FUN_180046360(lVar13,0);
              FUN_180045f70(lVar13);
            }
            else {
              FUN_180046360(lVar13);
            }
          }
        }
        lVar13 = lVar13 + 4;
      } while (lVar13 != *(longlong *)(param_1 + 0x68) + *(longlong *)(param_1 + 0x58) * 4);
    }
    *(undefined4 *)(param_1 + 0xb4) = 0;
  }
  FUN_180211a00(&local_d8);
  FUN_180213910(&local_d8);
  auVar21 = ZEXT1664(auVar20._0_16_);
  auVar22 = ZEXT1664(auVar20._0_16_);
  if (*(char *)(param_1 + 0xb1) != '\0') {
    fVar16 = (float)FUN_180191600();
    fVar16 = fVar16 + *(float *)(param_1 + 0xbc);
    *(float *)(param_1 + 0xbc) = fVar16;
    uVar8 = FUN_180088160(0);
    auVar1 = vmaxss_avx(auVar20._0_16_,ZEXT416((uint)((fVar16 - DAT_18034fea8) / DAT_18034fea8)));
    auVar1 = vminss_avx(ZEXT416(DAT_180346d3c),auVar1);
    FUN_1800881d0(uVar8,DAT_18034fea4 - auVar1._0_4_ * DAT_18034fea0);
    FUN_180211a00(&local_118);
    if (auVar20._0_4_ <= *(float *)(param_1 + 0xb8)) {
      iVar5 = (int)*(float *)(param_1 + 0xb8);
      fVar16 = (float)FUN_180191600();
      fVar3 = DAT_18034feac;
      fVar16 = fVar16 + *(float *)(param_1 + 0xb8);
      *(float *)(param_1 + 0xb8) = fVar16;
      if (fVar3 < fVar16) {
        *(undefined4 *)(param_1 + 0xb8) = 0;
      }
    }
    FUN_180213910(&local_118);
    FUN_180213180(&local_118,auVar20._0_8_,DAT_18034bbbc,auVar20._0_8_);
    if (*(int *)(param_1 + 0xc0) == 1) {
      local_d8 = local_118;
      uStack_d0 = uStack_110;
      uStack_c8 = uStack_108;
      uStack_c0 = uStack_100;
      local_b8 = local_f8;
      uStack_b0 = uStack_f0;
      uStack_a8 = uStack_e8;
      uStack_a0 = uStack_e0;
      auVar20 = ZEXT1664(auVar20._0_16_);
      fVar16 = (float)FUN_18030eb80();
      auVar21 = ZEXT464((uint)(fVar16 * DAT_18034fe98));
      dVar2 = (double)((float)(iVar5 % 0x168) * DAT_18034fe94) * DAT_18034a520;
      fVar16 = (float)FUN_18030eb80(CONCAT44((int)((ulonglong)dVar2 >> 0x20),(float)dVar2));
      auVar22 = ZEXT464((uint)(fVar16 * DAT_18034fe98));
    }
    lVar13 = *(longlong *)(param_1 + 0x68);
    if (lVar13 != lVar13 + *(longlong *)(param_1 + 0x58) * 4) {
      do {
        iVar5 = FUN_180041440(lVar13);
        if (iVar5 - 0x4e8U < 2) {
          FUN_180045fc0(lVar13,&local_118);
        }
        lVar13 = lVar13 + 4;
      } while (lVar13 != *(longlong *)(param_1 + 0x68) + *(longlong *)(param_1 + 0x58) * 4);
    }
    FUN_18018fd20(&local_118);
  }
  uVar9 = FUN_18006f350();
  if (uVar9 == 0) {
    uVar12 = 0;
  }
  else {
    lVar13 = *(longlong *)(param_1 + 0x68);
    fVar16 = DAT_18034b3dc;
    uVar12 = uVar9;
    if (lVar13 != lVar13 + *(longlong *)(param_1 + 0x58) * 4) {
      do {
        iVar5 = FUN_180041440(lVar13);
        if (iVar5 == 0x487) {
          *(undefined4 *)(uVar9 + 0x2e4) = 0;
          lVar10 = FUN_1801957a0(*(int *)(uVar9 + 0x2e8) + 0x1762);
          if (lVar10 != 0) {
            uVar6 = FUN_180254550(*(undefined4 *)(lVar10 + 0x10));
            *(undefined4 *)(uVar9 + 0x2e4) = uVar6;
          }
          *(int *)(uVar9 + 0x2e8) = *(int *)(uVar9 + 0x2e8) + 1;
          uVar7 = *(uint *)(uVar9 + 0x2e8);
          if (0x77 < *(uint *)(uVar9 + 0x2e8)) {
            uVar7 = 0;
          }
          *(uint *)(uVar9 + 0x2e8) = uVar7;
        }
        else if (iVar5 == 0x4e1) {
          *(undefined4 *)(uVar9 + 0x210) = 1;
          puVar14 = (undefined4 *)(uVar9 + 0x234);
          lVar15 = 4;
          lVar10 = 0;
          do {
            lVar11 = FUN_180044a90(lVar13,lVar10);
            if (lVar11 != 0) {
              uVar6 = *(undefined4 *)(lVar11 + 0xc);
              uVar17 = *(undefined4 *)(lVar11 + 0x1c);
              uVar18 = *(undefined4 *)(lVar11 + 0x2c);
              local_128 = auVar20._0_4_;
              local_124 = local_128;
              local_120 = local_128;
              FUN_18006f150(lVar11,&local_128);
              puVar14[-5] = 1;
              puVar14[-2] = uVar6;
              puVar14[-1] = uVar17;
              *puVar14 = uVar18;
              puVar14[1] = local_128;
              puVar14[3] = local_120;
              puVar14[2] = local_124;
              puVar14[4] = 0x3f800000;
              puVar14[5] = 0x3f800000;
              puVar14[6] = 0x3f800000;
            }
            lVar10 = lVar10 + 1;
            puVar14 = puVar14 + 0xc;
            lVar15 = lVar15 + -1;
          } while (lVar15 != 0);
        }
        else if (iVar5 == 0x4e8) {
          *(undefined4 *)(uVar9 + 0x3b8) = 1;
          *(undefined8 *)(uVar9 + 0x3cc) = 0;
          *(undefined8 *)(uVar9 + 0x3d4) = 0;
          *(undefined8 *)(uVar9 + 0x3dc) = 0;
          *(undefined4 *)(uVar9 + 0x3e4) = 0x3f800000;
          *(undefined4 *)(uVar9 + 1000) = 0x3f800000;
          *(undefined4 *)(uVar9 + 0x3ec) = 0x3f800000;
          *(undefined8 *)(uVar9 + 0x3c4) = 0;
          lVar10 = FUN_180044a90(lVar13,0);
          if (lVar10 != 0) {
            uVar6 = *(undefined4 *)(lVar10 + 0xc);
            uVar17 = *(undefined4 *)(lVar10 + 0x1c);
            uVar18 = *(undefined4 *)(lVar10 + 0x2c);
            uVar19 = auVar20._0_4_;
            FUN_18006f150(lVar10);
            *(undefined4 *)(uVar9 + 0x3cc) = uVar6;
            *(undefined4 *)(uVar9 + 0x3d0) = uVar17;
            *(undefined4 *)(uVar9 + 0x3d4) = uVar18;
            *(undefined4 *)(uVar9 + 0x3d8) = uVar19;
            *(undefined4 *)(uVar9 + 0x3e0) = uVar19;
            *(undefined4 *)(uVar9 + 0x3dc) = uVar19;
            *(float *)(uVar9 + 0x3c8) = auVar22._0_4_ * fVar16;
            *(float *)(uVar9 + 0x3c4) = auVar21._0_4_ * fVar16;
          }
        }
        else if (iVar5 == 0x7ed) {
          *(undefined4 *)(uVar9 + 0x2e4) = 0;
          lVar10 = FUN_1801957a0(*(int *)(uVar9 + 0x2e8) + 0x4694);
          if (lVar10 != 0) {
            uVar6 = FUN_180254550(*(undefined4 *)(lVar10 + 0x10));
            *(undefined4 *)(uVar9 + 0x2e4) = uVar6;
          }
          *(int *)(uVar9 + 0x2e8) = *(int *)(uVar9 + 0x2e8) + 1;
          if (0x77 < *(uint *)(uVar9 + 0x2e8)) {
            *(undefined4 *)(uVar9 + 0x2e8) = 0;
          }
        }
        lVar13 = lVar13 + 4;
        uVar12 = *(ulonglong *)(param_1 + 0x68);
      } while (lVar13 != uVar12 + *(longlong *)(param_1 + 0x58) * 4);
    }
    uVar12 = uVar12 & 0xffffffffffffff00;
  }
  return uVar12;
}



