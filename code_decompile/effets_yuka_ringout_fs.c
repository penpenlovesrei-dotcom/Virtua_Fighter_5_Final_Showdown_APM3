// ===================================================
// 1800861A0  ->  FUN_1800861a0  (entree 1800861a0)
// ===================================================

void FUN_1800861a0(int param_1)

{
  int iVar1;
  int iVar2;
  longlong *plVar3;
  longlong lVar4;
  longlong lVar5;
  longlong lVar6;
  longlong lVar7;
  longlong lVar8;
  int *piVar9;
  longlong lVar10;
  
  lVar7 = (longlong)param_1;
  lVar8 = lVar7 * 0xdd8;
  plVar3 = (longlong *)FUN_1800f93f0(0x18);
  FUN_1802ff420(&DAT_1806f43b0 + lVar8,0,0xdd8);
  *(undefined4 *)(&DAT_1806f43c0 + lVar8) = 0xffffffff;
  *(undefined8 *)(&DAT_1806f43f8 + lVar7 * 0x376) = 0;
  (&DAT_1806f4400)[lVar7 * 0x376] = 0;
  piVar9 = (int *)(&DAT_1806f440c + lVar8);
  lVar7 = 0;
  while( true ) {
    lVar4 = FUN_1800f8c60();
    if (lVar4 == 0) {
      return;
    }
    lVar5 = 0;
    if (*(int *)(lVar4 + 0x1c) != 0) {
      lVar5 = lVar4 + 0x1c + (longlong)*(int *)(lVar4 + 0x1c);
    }
    lVar10 = 0;
    if (*(int *)(lVar4 + 0x24) != 0) {
      lVar10 = lVar4 + 0x24 + (longlong)*(int *)(lVar4 + 0x24);
    }
    lVar6 = 0;
    if (*(int *)(lVar5 + 0x18) != 0) {
      lVar6 = lVar5 + 0x18 + (longlong)*(int *)(lVar5 + 0x18);
    }
    if (*(int *)(lVar4 + 0x18) != 1) {
      return;
    }
    if (*(int *)(lVar4 + 0x20) != 1) {
      return;
    }
    if (*(int *)(lVar5 + 0x14) != 1) break;
    iVar1 = *(int *)(lVar5 + 0x24);
    piVar9[-1] = iVar1;
    *piVar9 = *(int *)(lVar6 + 0x34);
    lVar4 = 0;
    iVar2 = *(int *)(lVar6 + 0x38);
    if (iVar2 != 0) {
      lVar4 = lVar6 + 0x38 + (longlong)iVar2;
    }
    *(longlong *)(piVar9 + 3) = lVar4;
    *(undefined2 *)(piVar9 + 1) = *(undefined2 *)(&DAT_1806f43c4 + lVar8);
    *(int *)(&DAT_1806f43c4 + lVar8) = *(int *)(&DAT_1806f43c4 + lVar8) + iVar1;
    *(int *)(&DAT_1806f43c8 + lVar8) = *(int *)(&DAT_1806f43c8 + lVar8) + *piVar9 + 1;
    iVar1 = *(int *)(*plVar3 + (ulonglong)(*(uint *)(lVar10 + 0x18) >> 0x14) * 4);
    if (*(int *)(&DAT_1806f43c0 + lVar8) == -1) {
      *(int *)(&DAT_1806f43c0 + lVar8) = iVar1;
    }
    else if (*(int *)(&DAT_1806f43c0 + lVar8) != iVar1) {
      return;
    }
    lVar7 = lVar7 + 1;
    piVar9 = piVar9 + 6;
    if (0x8f < lVar7) {
      (&DAT_1806f43b0)[lVar8] = 1;
      return;
    }
  }
  return;
}



// ===================================================
// 180086300  ->  FUN_180086300  (entree 180086300)
// ===================================================

void FUN_180086300(int param_1)

{
  float *pfVar1;
  int iVar2;
  int iVar3;
  float fVar4;
  float fVar5;
  uint uVar6;
  float *pfVar7;
  float *pfVar8;
  int iVar9;
  float *pfVar10;
  longlong lVar11;
  ulonglong uVar12;
  longlong lVar13;
  undefined4 *puVar14;
  float *pfVar15;
  float *pfVar16;
  ulonglong uVar17;
  float fVar18;
  undefined8 unaff_XMM6_Qa;
  undefined8 unaff_XMM6_Qb;
  float fVar19;
  undefined8 unaff_XMM7_Qa;
  undefined8 unaff_XMM7_Qb;
  
  lVar13 = (longlong)param_1;
  lVar11 = lVar13 * 0xdd8;
  if ((&DAT_1806f43b0)[lVar11] != '\0') {
    iVar2 = *(int *)(&DAT_1806f43c4 + lVar11);
    iVar3 = *(int *)(&DAT_1806f43c8 + lVar11);
    pfVar7 = (float *)FUN_180218410(1,(longlong)(iVar2 << 5),&DAT_180356ce0);
    if (pfVar7 != (float *)0x0) {
      lVar11 = FUN_180218410(0,(longlong)(iVar3 * 2),"INDEX_BUF",0);
      (&DAT_1806f43b8)[lVar13 * 0x1bb] = lVar11;
      if (lVar11 != 0) {
        FUN_180249fb0(1,&DAT_1806f43b4 + lVar13 * 0x376);
        FUN_180249bd0(0x2a9,(&DAT_1806f43b4)[lVar13 * 0x376]);
        uVar12 = 0;
        puVar14 = (undefined4 *)(&DAT_180356620 + lVar13 * 4);
        fVar18 = 0.0;
        pfVar15 = pfVar7;
        fVar19 = DAT_180356ce4;
        do {
          lVar11 = FUN_1800f8c60(*puVar14);
          if (lVar11 == 0) break;
          lVar13 = 0;
          if (*(int *)(lVar11 + 0x1c) != 0) {
            lVar13 = lVar11 + 0x1c + (longlong)*(int *)(lVar11 + 0x1c);
          }
          iVar3 = *(int *)(lVar13 + 0x24);
          iVar9 = (int)(uVar12 / 0xc);
          pfVar10 = (float *)0x0;
          fVar4 = (float)((int)uVar12 + iVar9 * -0xc) - fVar19;
          fVar5 = (float)iVar9 - fVar19;
          if (*(int *)(lVar13 + 0x28) != 0) {
            pfVar10 = (float *)(lVar13 + 0x28 + (longlong)*(int *)(lVar13 + 0x28));
          }
          pfVar8 = (float *)0x0;
          if (*(int *)(lVar13 + 0x2c) != 0) {
            pfVar8 = (float *)(lVar13 + 0x2c + (longlong)*(int *)(lVar13 + 0x2c));
          }
          pfVar16 = (float *)0x0;
          if (*(int *)(lVar13 + 0x38) != 0) {
            pfVar16 = (float *)(lVar13 + 0x38 + (longlong)*(int *)(lVar13 + 0x38));
          }
          iVar9 = 0;
          if (3 < iVar3) {
            uVar6 = (iVar3 - 4U >> 2) + 1;
            uVar17 = (ulonglong)uVar6;
            iVar9 = uVar6 * 4;
            do {
              *pfVar15 = fVar4 + *pfVar10;
              pfVar15[1] = fVar18 + pfVar10[1];
              pfVar15[2] = fVar5 + pfVar10[2];
              pfVar15[3] = *pfVar8;
              pfVar15[4] = pfVar8[1];
              pfVar15[5] = pfVar8[2];
              pfVar15[6] = *pfVar16;
              pfVar15[7] = pfVar16[1];
              pfVar15[8] = fVar4 + pfVar10[3];
              pfVar15[9] = fVar18 + pfVar10[4];
              pfVar15[10] = fVar5 + pfVar10[5];
              pfVar15[0xb] = pfVar8[3];
              pfVar15[0xc] = pfVar8[4];
              pfVar15[0xd] = pfVar8[5];
              pfVar15[0xe] = pfVar16[2];
              pfVar15[0xf] = pfVar16[3];
              pfVar15[0x10] = fVar4 + pfVar10[6];
              pfVar15[0x11] = fVar18 + pfVar10[7];
              pfVar15[0x12] = fVar5 + pfVar10[8];
              pfVar15[0x13] = pfVar8[6];
              pfVar15[0x14] = pfVar8[7];
              pfVar15[0x15] = pfVar8[8];
              pfVar15[0x16] = pfVar16[4];
              pfVar15[0x17] = pfVar16[5];
              pfVar15[0x18] = fVar4 + pfVar10[9];
              pfVar15[0x19] = fVar18 + pfVar10[10];
              pfVar15[0x1a] = fVar5 + pfVar10[0xb];
              pfVar10 = pfVar10 + 0xc;
              pfVar15[0x1b] = pfVar8[9];
              pfVar15[0x1c] = pfVar8[10];
              pfVar1 = pfVar8 + 0xb;
              pfVar8 = pfVar8 + 0xc;
              pfVar15[0x1d] = *pfVar1;
              pfVar15[0x1e] = pfVar16[6];
              pfVar1 = pfVar16 + 7;
              pfVar16 = pfVar16 + 8;
              pfVar15[0x1f] = *pfVar1;
              pfVar15 = pfVar15 + 0x20;
              uVar17 = uVar17 - 1;
            } while (uVar17 != 0);
          }
          if (iVar9 < iVar3) {
            uVar17 = (ulonglong)(uint)(iVar3 - iVar9);
            do {
              *pfVar15 = fVar4 + *pfVar10;
              pfVar15[1] = fVar18 + pfVar10[1];
              pfVar15[2] = fVar5 + pfVar10[2];
              pfVar10 = pfVar10 + 3;
              pfVar15[3] = *pfVar8;
              pfVar15[4] = pfVar8[1];
              pfVar15[5] = pfVar8[2];
              pfVar15[6] = *pfVar16;
              pfVar15[7] = pfVar16[1];
              pfVar15 = pfVar15 + 8;
              uVar17 = uVar17 - 1;
              pfVar8 = pfVar8 + 3;
              pfVar16 = pfVar16 + 2;
            } while (uVar17 != 0);
          }
          uVar6 = (int)uVar12 + 1;
          uVar12 = (ulonglong)uVar6;
          puVar14 = puVar14 + 3;
        } while ((int)uVar6 < 0x90);
        FUN_180249c60(0x2a9,(longlong)(iVar2 << 5),pfVar7,0x2b7,unaff_XMM7_Qa,unaff_XMM7_Qb,
                      unaff_XMM6_Qa,unaff_XMM6_Qb);
        FUN_180248c60(0x13);
        FUN_180249bd0(0x2a9,0);
        FUN_180218400(1,pfVar7);
      }
    }
  }
  return;
}



// ===================================================
// 180085F50  ->  FUN_180085f50  (entree 180085f50)
// ===================================================

void FUN_180085f50(longlong param_1,longlong param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined *puVar3;
  longlong lVar4;
  float fVar5;
  float fVar6;
  undefined1 auVar7 [64];
  undefined1 auVar8 [64];
  undefined1 auVar9 [64];
  undefined1 local_78 [112];
  
  uVar1 = *(undefined4 *)(param_2 + 0x2c);
  auVar7 = ZEXT464(*(uint *)(param_2 + 0x24));
  auVar8 = ZEXT464((uint)*(float *)(param_2 + 0x1c));
  auVar9 = ZEXT464(*(uint *)(param_2 + 0x20));
  fVar5 = floorf(*(float *)(param_2 + 0x1c));
  fVar6 = floorf(auVar7._0_4_);
  puVar3 = PTR_DAT_180643568;
  if ((((int)fVar5 + 6U < 0xc) && ((int)fVar6 + 6U < 0xc)) &&
     (iVar2 = (int)fVar5 + 6U + ((int)fVar6 + 6U) * 0xc, iVar2 != -1)) {
    lVar4 = (longlong)iVar2;
    iVar2 = *(int *)(PTR_DAT_180643568 + lVar4 * 0x14 + 4);
    if (iVar2 < 2) {
      *(int *)(PTR_DAT_180643568 + lVar4 * 0x14 + 4) = iVar2 + 1;
      *(undefined4 *)(puVar3 + (longlong)iVar2 * 4 + lVar4 * 0x14 + 0xc) = uVar1;
      if (*(int *)(param_1 + 0x58) == 0x496) {
        FUN_180211a00(local_78);
        FUN_180213910(local_78);
        FUN_180213180(local_78,auVar8._0_8_,auVar9._0_8_,auVar7._0_8_);
        FUN_180045fc0(param_1 + 0x5c,local_78);
        FUN_1800460d0(param_1 + 0x5c,1);
        FUN_1800463b0(param_1 + 0x5c,0);
        FUN_180046360(param_1 + 0x5c,0);
        FUN_180046230(param_1 + 0x5c,0);
      }
    }
  }
  return;
}



// ===================================================
// 180085D60  ->  FUN_180085d60  (entree 180085d60)
// ===================================================

void FUN_180085d60(int *param_1)

{
  short sVar1;
  int iVar2;
  undefined4 uVar3;
  undefined8 uVar4;
  undefined *puVar5;
  char cVar6;
  short sVar7;
  short *psVar8;
  short *psVar9;
  uint *puVar10;
  longlong lVar11;
  longlong lVar12;
  int iVar13;
  int iVar14;
  uint uVar15;
  short *psVar16;
  longlong lVar17;
  
  iVar2 = *param_1;
  lVar12 = (longlong)iVar2;
  lVar17 = lVar12 * 0xdd8;
  cVar6 = FUN_18024a180((&DAT_1806f43b4)[lVar12 * 0x376]);
  if (cVar6 != '\0') {
    FUN_1802473b0(299);
    FUN_1802473b0(300);
    FUN_180249bd0(0x2a9,(&DAT_1806f43b4)[lVar12 * 0x376]);
    FUN_180247600(3,0x161,0x20);
    FUN_1802474a0(0x161,0x20,0xc);
    if (*(int *)(&DAT_1806f43c0 + lVar17) != -1) {
      FUN_180246fa0(0x21d);
      FUN_1802473b0(0x12f);
      FUN_180247500(2,0x161,0x20);
    }
    puVar5 = PTR_DAT_180643568;
    psVar9 = (short *)(&DAT_1806f43b8)[lVar12 * 0x1bb];
    iVar14 = 0;
    iVar13 = 0;
    lVar11 = 0;
    puVar10 = (uint *)(&DAT_1806f440c + lVar17);
    do {
      psVar16 = *(short **)(puVar10 + 3);
      if (*(int *)(puVar5 + lVar11 + 4) == iVar2) {
        uVar15 = 0;
        psVar8 = psVar9;
        if (*puVar10 != 0) {
          do {
            sVar1 = *psVar16;
            psVar16 = psVar16 + 1;
            psVar9 = psVar8 + 1;
            sVar7 = -1;
            if (sVar1 != -1) {
              sVar7 = (short)puVar10[1] + sVar1;
            }
            *psVar8 = sVar7;
            uVar15 = uVar15 + 1;
            psVar8 = psVar9;
          } while (uVar15 < *puVar10);
        }
        *psVar9 = -1;
        psVar9 = psVar9 + 1;
        iVar13 = iVar13 + 1 + *puVar10;
        iVar14 = iVar14 + puVar10[-1];
      }
      puVar10 = puVar10 + 6;
      lVar11 = lVar11 + 0x14;
    } while (lVar11 < 0xb40);
    *(int *)(&DAT_1806f43d0 + lVar17) = iVar13;
    *(int *)(&DAT_1806f43cc + lVar17) = iVar14;
    FUN_180245d70(CONCAT71((int7)((ulonglong)psVar9 >> 8),1));
    sVar1 = *(short *)(&DAT_1806f43c4 + lVar17);
    uVar4 = (&DAT_1806f43b8)[lVar12 * 0x1bb];
    uVar3 = *(undefined4 *)(&DAT_1806f43d0 + lVar17);
    FUN_180252390();
    FUN_180247370(7,0,sVar1 + -1,uVar3,0x15e,uVar4);
    FUN_180252530();
    FUN_180245d70(0);
    FUN_180249bd0(0x2a9,0);
    FUN_180247100(0x12f);
    FUN_180247100(300);
  }
  return;
}



// ===================================================
// 1800794D0  ->  FUN_1800794d0  (entree 1800794d0)
// ===================================================

void FUN_1800794d0(int *param_1)

{
  undefined4 uVar1;
  longlong lVar2;
  undefined1 auVar3 [16];
  char cVar4;
  byte bVar5;
  int iVar6;
  undefined8 uVar7;
  longlong lVar8;
  undefined8 *puVar9;
  ulonglong uVar10;
  longlong lVar11;
  uint uVar12;
  undefined4 uVar14;
  undefined1 auVar15 [64];
  float fVar16;
  float fVar17;
  undefined4 uVar18;
  undefined1 auVar19 [64];
  undefined1 auVar20 [64];
  undefined1 local_res10 [8];
  float local_f8;
  float fStack_f4;
  float local_f0;
  float local_e8;
  float local_e4;
  float local_e0;
  undefined1 local_d8 [176];
  ulonglong uVar13;
  
  uVar10 = 0;
  if (0 < *param_1) {
    auVar19 = ZEXT464(DAT_18034b3ec);
    auVar20 = ZEXT464(DAT_180346d38);
    auVar15 = ZEXT1264(ZEXT812(0));
    uVar13 = uVar10;
    fVar16 = DAT_180350e00;
    fVar17 = DAT_180350dfc;
    uVar18 = DAT_18034a514;
    do {
      lVar2 = *(longlong *)(param_1 + 2);
      local_f8 = auVar15._0_4_;
      if (*(int *)(uVar10 + 4 + lVar2) == 0) {
        fStack_f4 = local_f8;
        local_f0 = local_f8;
        local_e8 = local_f8;
        local_e4 = local_f8;
        local_e0 = local_f8;
        uVar7 = FUN_1801509b0();
        lVar8 = FUN_1801509c0(uVar7,*(undefined4 *)(uVar10 + lVar2));
        if ((lVar8 != 0) &&
           (lVar8 = FUN_1800e0280(lVar8,(longlong)*(int *)(uVar10 + 0xc + lVar2)), lVar8 != 0)) {
          local_f0 = *(float *)(lVar8 + 0x2c);
          fStack_f4 = *(float *)(lVar8 + 0x1c);
          local_f8 = *(float *)(lVar8 + 0xc);
          uVar7 = FUN_1801509b0();
          cVar4 = FUN_1801501e0(uVar7,*(undefined4 *)(uVar10 + lVar2));
          if (((cVar4 != '\0') &&
              ((((iVar6 = FUN_18018f580(), iVar6 != 9 || (local_f8 <= fVar16)) ||
                (fVar17 <= local_f8)) || ((local_f0 <= fVar16 || (fVar17 <= local_f0)))))) &&
             (iVar6 = FUN_18005dce0(&local_e8,local_res10,&local_f8,lVar2 + 0x14 + uVar10,uVar18,
                                    0x2000), iVar6 != -1)) {
            bVar5 = FUN_1800533a0();
            auVar3 = vpcmpeqd_avx(ZEXT116(bVar5),ZEXT416(0));
            auVar3 = vblendvps_avx(auVar20._0_16_,auVar19._0_16_,auVar3);
            lVar8 = lVar2 + 0x10 + uVar10;
            uVar14 = auVar3._0_4_;
            cVar4 = FUN_180041a80(lVar8);
            if (cVar4 != '\0') {
              FUN_180211a00(local_d8);
              FUN_180213910(local_d8);
              FUN_180213180(local_d8,local_e8,local_e4 + *(float *)(uVar10 + 0x48 + lVar2),local_e0)
              ;
              FUN_180213140(local_d8,uVar14,uVar14,uVar14);
              FUN_180045fc0(lVar8,local_d8);
              FUN_1800460d0(lVar8,1);
              FUN_1800463b0(lVar8,0);
              FUN_180046360(lVar8,0);
              FUN_180045f70(lVar8,1);
              FUN_180046230(lVar8,auVar15._0_8_);
              lVar8 = FUN_18006f350();
              if (lVar8 != 0) {
                iVar6 = *(int *)(lVar8 + 0x108);
                lVar11 = (longlong)iVar6;
                if (iVar6 < 4) {
                  *(int *)(lVar8 + 0x108) = iVar6 + 1;
                  *(undefined4 *)(lVar8 + 0x110 + lVar11 * 0x28) =
                       *(undefined4 *)(uVar10 + 8 + lVar2);
                  uVar1 = *(undefined4 *)(uVar10 + 0x4c + lVar2);
                  *(float *)(lVar8 + 0x114 + lVar11 * 0x28) = local_e8;
                  *(undefined4 *)(lVar8 + 0x118 + lVar11 * 0x28) = uVar1;
                  *(float *)(lVar8 + 0x11c + lVar11 * 0x28) = local_e0;
                  *(undefined8 *)(lVar8 + 0x120 + lVar11 * 0x28) = 0;
                  *(undefined4 *)(lVar8 + 0x128 + lVar11 * 0x28) = 0;
                  *(undefined4 *)(lVar8 + 300 + lVar11 * 0x28) = uVar14;
                  *(undefined4 *)(lVar8 + 0x130 + lVar11 * 0x28) = uVar14;
                  *(undefined4 *)(lVar8 + 0x134 + lVar11 * 0x28) = uVar14;
                }
              }
              puVar9 = (undefined8 *)(lVar2 + 0x28 + uVar10);
              if (puVar9[2] != 0) {
                if (0xf < (ulonglong)puVar9[3]) {
                  puVar9 = (undefined8 *)*puVar9;
                }
                FUN_1801644a0(puVar9);
              }
            }
            *(undefined4 *)(uVar10 + 4 + lVar2) = 1;
          }
          *(ulonglong *)(uVar10 + 0x14 + lVar2) = CONCAT44(fStack_f4,local_f8);
          *(float *)(uVar10 + 0x1c + lVar2) = local_f0;
        }
      }
      uVar12 = (int)uVar13 + 1;
      uVar13 = (ulonglong)uVar12;
      uVar10 = uVar10 + 0x50;
    } while ((int)uVar12 < *param_1);
  }
  return;
}



// ===================================================
// 180079A30  ->  FUN_180079a30  (entree 180079a30)
// ===================================================

void FUN_180079a30(longlong param_1,int param_2)

{
  int *piVar1;
  longlong lVar2;
  char cVar3;
  undefined8 *puVar4;
  int *piVar5;
  undefined4 *puVar6;
  int iVar7;
  undefined8 *puVar8;
  undefined8 *puVar9;
  uint uVar10;
  undefined8 *puVar11;
  longlong lVar12;
  undefined4 uVar13;
  undefined4 *puVar14;
  undefined8 local_res8;
  
  piVar1 = (int *)(param_1 + 0x58);
  FUN_180079890(piVar1);
  *piVar1 = 6;
  local_res8 = 6;
  puVar4 = (undefined8 *)FUN_180218930(0x1e8);
  puVar9 = (undefined8 *)0x0;
  puVar8 = puVar9;
  if (puVar4 != (undefined8 *)0x0) {
    *puVar4 = 6;
    _eh_vector_constructor_iterator_(puVar4 + 1,0x50,6,FUN_180079390,FUN_180079420);
    puVar8 = puVar4 + 1;
  }
  *(undefined8 **)(param_1 + 0x60) = puVar8;
  puVar4 = puVar9;
  puVar11 = puVar9;
  if (puVar8 == (undefined8 *)0x0) {
    *piVar1 = 0;
  }
  else {
    do {
      puVar6 = &DAT_180350c90;
      do {
        lVar12 = *(longlong *)(param_1 + 0x60);
        FUN_18003d840(lVar12 + 0x10 + (longlong)puVar11);
        *(undefined8 *)((longlong)puVar11 + lVar12) = 0;
        *(undefined4 *)((longlong)puVar11 + lVar12 + 8) = 0;
        *(undefined4 *)((longlong)puVar11 + lVar12 + 0xc) = 0xffffffff;
        *(undefined8 *)((longlong)puVar11 + lVar12 + 0x14) = 0;
        *(undefined8 *)((longlong)puVar11 + lVar12 + 0x1c) = 0;
        FUN_1800524e0(lVar12 + 0x28 + (longlong)puVar11,&PTR_180347568);
        *(undefined4 *)((longlong)puVar11 + lVar12 + 0x48) = 0;
        *(int *)((longlong)puVar11 + lVar12) = (int)puVar4;
        *(undefined4 *)((longlong)puVar11 + lVar12 + 4) = 0;
        *(undefined4 *)((longlong)puVar11 + lVar12 + 8) = *puVar6;
        *(undefined4 *)((longlong)puVar11 + lVar12 + 0xc) = puVar6[1];
        *(undefined8 *)((longlong)puVar11 + lVar12 + 0x14) = 0;
        *(undefined4 *)((longlong)puVar11 + lVar12 + 0x1c) = 0;
        puVar11 = puVar11 + 10;
        puVar6 = puVar6 + 2;
      } while ((longlong)puVar6 < 0x180350ca8);
      uVar10 = (int)puVar4 + 1;
      puVar4 = (undefined8 *)(ulonglong)uVar10;
    } while ((int)uVar10 < 2);
  }
  piVar5 = &DAT_180350c10;
  puVar8 = puVar9;
  do {
    iVar7 = (int)puVar8;
    if (*piVar5 == param_2) {
      lVar12 = (longlong)iVar7 * 0x20;
      if ((lVar12 != -0x180350c10) && (puVar8 = puVar9, 0 < *piVar1)) {
        do {
          lVar2 = *(longlong *)(param_1 + 0x60);
          *(undefined4 *)((longlong)puVar9 + lVar2 + 0x20) =
               *(undefined4 *)(&DAT_180350c1c + lVar12);
          *(undefined4 *)((longlong)puVar9 + lVar2 + 0x48) =
               *(undefined4 *)(&DAT_180350c28 + lVar12);
          *(undefined4 *)((longlong)puVar9 + lVar2 + 0x4c) =
               *(undefined4 *)(&DAT_180350c2c + lVar12);
          if (*(int *)((longlong)puVar9 + lVar2 + 8) == 0) {
            uVar13 = *(undefined4 *)(&DAT_180350c14 + lVar12);
            FUN_1800524e0(lVar2 + 0x28 + (longlong)puVar9,
                          (&PTR_s_fd_vfv_landing_water_180350c20)[(longlong)iVar7 * 4]);
          }
          else {
            uVar13 = *(undefined4 *)(&DAT_180350c18 + lVar12);
          }
          puVar14 = (undefined4 *)(lVar2 + 0x10 + (longlong)puVar9);
          FUN_18003d840(puVar14);
          puVar6 = (undefined4 *)FUN_18003c370(&local_res8,uVar13);
          *puVar14 = *puVar6;
          cVar3 = FUN_180041a80(puVar14);
          if (cVar3 != '\0') {
            FUN_1800460d0(puVar14,0);
            FUN_180044830(puVar14);
          }
          uVar10 = (int)puVar8 + 1;
          puVar9 = puVar9 + 10;
          puVar8 = (undefined8 *)(ulonglong)uVar10;
        } while ((int)uVar10 < *piVar1);
      }
      break;
    }
    puVar8 = (undefined8 *)(ulonglong)(iVar7 + 1);
    piVar5 = piVar5 + 8;
  } while ((longlong)piVar5 < 0x180350c90);
  FUN_180040270("TaskEffectRingoutSplash::pre_init()\n");
  return;
}



// ===================================================
// 180079890  ->  FUN_180079890  (entree 180079890)
// ===================================================

void FUN_180079890(int *param_1)

{
  __uint64 *p_Var1;
  longlong lVar2;
  void *pvVar3;
  uint uVar4;
  ulonglong uVar6;
  ulonglong uVar5;
  
  pvVar3 = *(void **)(param_1 + 2);
  uVar5 = 0;
  if (pvVar3 != (void *)0x0) {
    uVar6 = uVar5;
    if (0 < *param_1) {
      do {
        lVar2 = *(longlong *)(param_1 + 2);
        FUN_18003d840(lVar2 + 0x10 + uVar6);
        *(undefined8 *)(uVar6 + lVar2) = 0;
        *(undefined4 *)(uVar6 + 8 + lVar2) = 0;
        *(undefined4 *)(uVar6 + 0xc + lVar2) = 0xffffffff;
        *(undefined8 *)(uVar6 + 0x14 + lVar2) = 0;
        *(undefined8 *)(uVar6 + 0x1c + lVar2) = 0;
        FUN_1800524e0(lVar2 + 0x28 + uVar6,&PTR_180347568);
        *(undefined4 *)(uVar6 + 0x48 + lVar2) = 0;
        uVar4 = (int)uVar5 + 1;
        uVar5 = (ulonglong)uVar4;
        uVar6 = uVar6 + 0x50;
      } while ((int)uVar4 < *param_1);
      pvVar3 = *(void **)(param_1 + 2);
    }
    if (pvVar3 != (void *)0x0) {
      p_Var1 = (__uint64 *)((longlong)pvVar3 + -8);
      _eh_vector_destructor_iterator_(pvVar3,0x50,*p_Var1,FUN_180079420);
      FUN_1802fdd80(p_Var1,*p_Var1 * 0x50 + 8);
    }
  }
  *param_1 = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  return;
}



