// ===================================================
// 180027AE0  ->  FUN_180027ae0  (entree 180027ae0)
// ===================================================

void FUN_180027ae0(longlong param_1,undefined4 *param_2,longlong param_3,undefined8 param_4,
                  longlong param_5,uint *param_6,float *param_7,undefined4 param_8)

{
  longlong *plVar1;
  longlong lVar2;
  float fVar3;
  float fVar4;
  uint uVar5;
  undefined8 uVar6;
  uint uVar7;
  longlong *plVar8;
  longlong lVar9;
  longlong lVar10;
  ulonglong uVar11;
  ulonglong uVar12;
  longlong lVar13;
  ulonglong uVar14;
  undefined1 auVar15 [16];
  undefined1 auVar16 [16];
  undefined1 auVar17 [16];
  
  fVar4 = DAT_180346d3c;
  uVar7 = *(uint *)(param_3 + 4);
  *(uint *)(param_1 + 0x28) = uVar7;
  fVar3 = *(float *)(param_3 + 8) - fVar4;
  *(float *)(param_1 + 0x2c) = fVar3;
  if (param_5 != 0) {
    uVar7 = *(uint *)(param_5 + 4);
    *(uint *)(param_1 + 0x28) = uVar7;
    fVar3 = *(float *)(param_5 + 8) - fVar4;
    *(float *)(param_1 + 0x2c) = fVar3;
  }
  if (param_6 != (uint *)0x0) {
    uVar7 = *param_6;
    *(uint *)(param_1 + 0x28) = uVar7;
  }
  auVar15 = ZEXT416(uVar7);
  if (param_7 != (float *)0x0) {
    fVar3 = *param_7;
    *(float *)(param_1 + 0x2c) = fVar3;
  }
  auVar16 = ZEXT416((uint)fVar3);
  fVar3 = (float)param_2[8];
  if (0.0 <= fVar3) {
    auVar15 = vcmpss_avx(ZEXT416((uint)fVar3),ZEXT416(*(uint *)(param_3 + 4)),1);
    auVar15 = vblendvps_avx(ZEXT416((uint)fVar3),ZEXT416(*(uint *)(param_3 + 4)),auVar15);
    auVar17 = vcmpss_avx(auVar15,ZEXT416(*(uint *)(param_3 + 8)),1);
    auVar15 = vblendvps_avx(ZEXT416(*(uint *)(param_3 + 8)),auVar15,auVar17);
    *(int *)(param_1 + 0x28) = auVar15._0_4_;
  }
  fVar3 = (float)param_2[9];
  if (0.0 <= fVar3) {
    auVar16 = vcmpss_avx(ZEXT416((uint)fVar3),ZEXT416(*(uint *)(param_3 + 4)),1);
    auVar16 = vblendvps_avx(ZEXT416((uint)fVar3),ZEXT416(*(uint *)(param_3 + 4)),auVar16);
    auVar17 = vcmpss_avx(auVar16,ZEXT416(*(uint *)(param_3 + 8)),1);
    auVar16 = vblendvps_avx(ZEXT416(*(uint *)(param_3 + 8)),auVar16,auVar17);
    *(int *)(param_1 + 0x2c) = auVar16._0_4_;
  }
  uVar7 = param_2[10] & 0xffff0000;
  *(uint *)(param_1 + 0x30) = uVar7;
  auVar17 = auVar16;
  if (auVar16._0_4_ < auVar15._0_4_) {
    uVar7 = uVar7 | 2;
    *(uint *)(param_1 + 0x30) = uVar7;
    *(float *)(param_1 + 0x28) = auVar16._0_4_;
    *(float *)(param_1 + 0x2c) = auVar15._0_4_;
    auVar17 = auVar15;
    auVar15 = auVar16;
  }
  uVar5 = DAT_180347cd8;
  auVar16 = vpcmpeqd_avx(ZEXT416(uVar7 & 2),ZEXT416(0));
  auVar15 = vblendvps_avx(auVar17,auVar15,auVar16);
  *(int *)(param_1 + 0x88) = auVar15._0_4_;
  auVar15 = vpcmpeqd_avx(ZEXT416(uVar7 & 0x40000),SUB6416(ZEXT464(0),0));
  auVar15 = vblendvps_avx(ZEXT416(uVar5),ZEXT416((uint)fVar4),auVar15);
  *(int *)(param_1 + 0x94) = auVar15._0_4_;
  auVar15 = vpcmpeqd_avx(ZEXT416(uVar7 & 0x80000),ZEXT416(0));
  auVar15 = vblendvps_avx(ZEXT416(uVar5),ZEXT416((uint)fVar4),auVar15);
  *(int *)(param_1 + 0x98) = auVar15._0_4_;
  *(undefined4 *)(param_1 + 8) = *param_2;
  *(longlong *)(param_1 + 0x20) = param_5;
  *(longlong *)(param_1 + 0x10) = param_3;
  *(undefined8 *)(param_1 + 0x18) = param_4;
  *(undefined4 *)(param_1 + 0x34) = param_2[0xb];
  *(undefined4 *)(param_1 + 0x38) = param_2[0xc];
  *(undefined4 *)(param_1 + 0x3c) = param_2[0xd];
  *(undefined4 *)(param_1 + 0x40) = param_2[0xe];
  *(undefined8 *)(param_1 + 0x44) = *(undefined8 *)(param_2 + 0x10);
  *(undefined4 *)(param_1 + 0x4c) = param_2[0x12];
  *(undefined8 *)(param_1 + 0x50) = *(undefined8 *)(param_2 + 0x13);
  *(undefined4 *)(param_1 + 0x58) = param_2[0x15];
  *(undefined8 *)(param_1 + 0x5c) = *(undefined8 *)(param_2 + 0x16);
  *(undefined4 *)(param_1 + 100) = param_2[0x18];
  *(undefined8 *)(param_1 + 0x68) = *(undefined8 *)(param_2 + 0x19);
  *(undefined4 *)(param_1 + 0x70) = param_2[0x1b];
  *(undefined4 *)(param_1 + 0x74) = param_2[0x1c];
  uVar6 = *(undefined8 *)(param_2 + 0x1f);
  *(undefined8 *)(param_1 + 0x78) = *(undefined8 *)(param_2 + 0x1d);
  *(undefined8 *)(param_1 + 0x80) = uVar6;
  *(undefined4 *)(param_1 + 0x8c) = param_8;
  *(undefined1 *)(param_1 + 0x90) = *(undefined1 *)(param_2 + 0xf);
  *(undefined1 *)(param_1 + 0x9c) = 0;
  *(undefined4 *)(param_1 + 0x188) = 0;
  FUN_180021690(param_1 + 400,param_2 + 0x22);
  plVar8 = (longlong *)(param_2 + 0x2a);
  *(undefined1 *)(param_1 + 0x1a8) = *(undefined1 *)(param_2 + 0x28);
  if ((longlong *)(param_1 + 0x1b0) != plVar8) {
    if (0xf < *(ulonglong *)(param_2 + 0x30)) {
      plVar8 = (longlong *)*plVar8;
    }
    FUN_180010a10(param_1 + 0x1b0,plVar8,*(undefined8 *)(param_2 + 0x2e));
  }
  plVar8 = (longlong *)(param_1 + 0x1d0);
  if (plVar8 != (longlong *)(param_2 + 0x32)) {
    lVar2 = *(longlong *)(param_2 + 0x34);
    lVar10 = *(longlong *)(param_2 + 0x32);
    lVar9 = *plVar8;
    lVar13 = *(longlong *)(param_1 + 0x1d8);
    uVar11 = lVar2 - lVar10 >> 6;
    uVar12 = lVar13 - lVar9 >> 6;
    uVar14 = *(longlong *)(param_1 + 0x1e0) - lVar9 >> 6;
    if (uVar14 < uVar11) {
      if (0x3ffffffffffffff < uVar11) {
                    /* WARNING: Subroutine does not return */
        FUN_180010340();
      }
      uVar12 = uVar11;
      if ((uVar14 <= 0x3ffffffffffffff - (uVar14 >> 1)) &&
         (uVar12 = (uVar14 >> 1) + uVar14, uVar12 < uVar11)) {
        uVar12 = uVar11;
      }
      if (lVar9 != 0) {
        if (lVar9 != lVar13) {
          do {
            FUN_18000df90(lVar9);
            lVar9 = lVar9 + 0x40;
          } while (lVar9 != lVar13);
          lVar9 = *plVar8;
        }
        FUN_180010d20(plVar8,lVar9,uVar14);
      }
      FUN_180022050(plVar8,uVar12);
      uVar6 = FUN_18000c390(plVar8,lVar10,lVar2,*plVar8);
      *(undefined8 *)(param_1 + 0x1d8) = uVar6;
    }
    else if (uVar12 < uVar11) {
      lVar13 = uVar12 * 0x40 + lVar10;
      FUN_18001a930(lVar10,lVar13,lVar9);
      uVar6 = FUN_18000c390(plVar8,lVar13,lVar2,*(undefined8 *)(param_1 + 0x1d8));
      *(undefined8 *)(param_1 + 0x1d8) = uVar6;
    }
    else {
      FUN_18001a930(lVar10,lVar2,lVar9);
      lVar2 = *(longlong *)(param_1 + 0x1d8);
      lVar9 = uVar11 * 0x40 + lVar9;
      for (lVar10 = lVar9; lVar10 != lVar2; lVar10 = lVar10 + 0x40) {
        FUN_18000df90(lVar10);
      }
      *(longlong *)(param_1 + 0x1d8) = lVar9;
    }
  }
  *(undefined1 *)(param_1 + 0x1e8) = *(undefined1 *)(param_2 + 0x38);
  plVar1 = (longlong *)(param_1 + 0x1f8);
  *(undefined4 *)(param_1 + 0x1f0) = param_2[0x3a];
  if (plVar1 != (longlong *)(param_2 + 0x3c)) {
    FUN_18001a5e0(plVar1,*(longlong *)(param_2 + 0x3c),*(undefined8 *)(param_2 + 0x3e),
                  (undefined1)param_8);
  }
  *(undefined1 *)(param_1 + 0x210) = *(undefined1 *)(param_2 + 0x42);
  *(undefined1 *)(param_1 + 0x218) = *(undefined1 *)(param_2 + 0x44);
  FUN_18001fd00(*(longlong *)(param_1 + 400),*(undefined8 *)(param_1 + 0x198),
                (*(longlong *)(param_1 + 0x198) - *(longlong *)(param_1 + 400)) / 0x28,0);
  FUN_1800200b0(*plVar8,*(longlong *)(param_1 + 0x1d8),*(longlong *)(param_1 + 0x1d8) - *plVar8 >> 6
                ,0);
  FUN_18001fa10(*plVar1,*(longlong *)(param_1 + 0x200),*(longlong *)(param_1 + 0x200) - *plVar1 >> 3
                ,0);
  return;
}



