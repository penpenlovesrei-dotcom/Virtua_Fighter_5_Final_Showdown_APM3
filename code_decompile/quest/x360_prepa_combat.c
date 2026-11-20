// ===================================================
// 82320300  ->  FUN_82320300  (entree 82320300)
// ===================================================

/* WARNING: Function: __savegprlr_15 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_15 replaced with injection: x360_restgprlr */

void FUN_82320300(int param_1)

{
  float fVar1;
  ushort uVar2;
  int iVar3;
  ulonglong uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  uint uVar10;
  uint *puVar11;
  int iVar12;
  char cVar13;
  undefined8 uVar8;
  ulonglong uVar9;
  undefined4 *puVar14;
  undefined1 *puVar15;
  undefined1 *puVar16;
  undefined1 *puVar17;
  int iVar18;
  ushort *puVar19;
  longlong lVar20;
  double dVar21;
  double dVar22;
  double dVar23;
  undefined4 uStack_bf0;
  undefined4 uStack_bec;
  uint auStack_be8 [10];
  float fStack_bc0;
  float fStack_bbc;
  int iStack_bb8;
  undefined2 uStack_bb4;
  undefined4 uStack_bb0;
  undefined4 uStack_bac;
  undefined4 uStack_ba8;
  undefined4 uStack_ba4;
  undefined1 uStack_ba0;
  undefined1 uStack_b9f;
  undefined4 auStack_b90 [16];
  undefined4 auStack_b50 [20];
  undefined1 uStack_b00;
  undefined1 uStack_aff;
  undefined1 auStack_aa7 [40];
  undefined1 auStack_a7f [40];
  undefined1 auStack_a57 [55];
  undefined2 uStack_a20;
  undefined1 uStack_a08;
  undefined1 uStack_a07;
  undefined2 uStack_a06;
  undefined1 uStack_a04;
  undefined1 uStack_a03;
  undefined1 uStack_a02;
  undefined1 uStack_a01;
  undefined4 uStack_a00;
  undefined4 uStack_9fc;
  undefined4 uStack_9d0;
  uint auStack_9c8 [31];
  undefined4 uStack_94c;
  undefined1 uStack_948;
  undefined1 uStack_947;
  ushort auStack_946 [24];
  undefined1 auStack_916 [569];
  undefined1 uStack_6dd;
  undefined1 auStack_5d0 [1488];
  
  uVar5 = FUN_821dc920();
  uVar6 = FUN_821dc9f0();
  uVar7 = FUN_821dc9f8(uVar5);
  auStack_b50[3] = 5;
  iVar3 = *(int *)(&DAT_820036c0 + param_1 * 4);
  auStack_b50[2] = 4;
  auStack_b50[4] = 6;
  auStack_b90[0] = 0x15;
  auStack_b50[5] = 7;
  auStack_b50[6] = 8;
  auStack_b50[7] = 9;
  auStack_b50[8] = 10;
  auStack_b50[9] = 0xb;
  auStack_b50[10] = 0xc;
  auStack_b50[0xb] = 0xd;
  auStack_b50[0xc] = 0xe;
  auStack_b50[0xd] = 0xf;
  auStack_b50[0xe] = 0x10;
  auStack_b50[0xf] = 0x11;
  auStack_b50[0x10] = 0x12;
  auStack_b50[0x11] = 0x13;
  auStack_b50[0x12] = 0x14;
  auStack_b90[1] = 0x16;
  auStack_b90[2] = 0x17;
  auStack_b90[3] = 0x18;
  auStack_b90[4] = 0x1c;
  auStack_b90[5] = 0x1d;
  auStack_b90[6] = 0x1e;
  auStack_b90[7] = 0x1f;
  auStack_b90[8] = 0x20;
  auStack_b90[9] = 0x21;
  auStack_b90[10] = 0x22;
  auStack_b90[0xb] = 0x23;
  auStack_b90[0xc] = 0x24;
  uVar10 = FUN_822c6de8();
  auStack_b50[0] = auStack_b90[uVar10 & 3];
  uVar10 = FUN_822c6de8();
  auStack_b50[1] = auStack_b90[uVar10 % 9 + 4];
  puVar11 = (uint *)FUN_822dac30();
  if ((*puVar11 >> 1 & 1) == 0) {
    iVar12 = FUN_822c6de8();
    auStack_b50[1] = auStack_b90[iVar12 + 1U & 3];
  }
  (&DAT_827a9a09)[iVar3 * 0x528] = 1;
  FUN_821f1ce0(iVar3,1);
  auStack_be8[0] = 0x15;
  auStack_be8[1] = 0x15;
  auStack_be8[8] = 4;
  auStack_be8[9] = 4;
  uStack_bf0 = 1;
  dVar22 = (double)DAT_82000b08;
  fStack_bc0 = DAT_82000b08;
  iStack_bb8 = 0;
  fStack_bbc = DAT_82000b08;
  uStack_bb4 = 0;
  uStack_bb0 = 0;
  uStack_bac = 2;
  auStack_be8[2] = 0xffffffff;
  auStack_be8[3] = 0xffffffff;
  auStack_be8[4] = 0xffffffff;
  auStack_be8[5] = 0xffffffff;
  auStack_be8[6] = 0xffffffff;
  auStack_be8[7] = 0xffffffff;
  uStack_ba4 = 0;
  uStack_ba0 = 0;
  uStack_b9f = 0;
  uStack_bec = 0;
  uStack_ba8 = 0x25;
  FUN_821d10e0();
  FUN_821d49d0();
  FUN_821df480(auStack_5d0);
  FUN_821df480(&uStack_b00);
  if (param_1 == 0) {
    puVar16 = auStack_5d0;
    puVar17 = &uStack_b00;
  }
  else {
    puVar17 = auStack_5d0;
    puVar16 = &uStack_b00;
  }
  FUN_822360c8(0xffffffff827a99f8,auStack_5d0,param_1);
  FUN_822360c8(0xffffffff827a99f8,&uStack_b00,iVar3);
  uStack_b00 = 0;
  uStack_aff = 1;
  puVar15 = auStack_aa7;
  lVar20 = 0x1f;
  do {
    *puVar15 = 0;
    puVar15 = puVar15 + 1;
    lVar20 = lVar20 + -1;
  } while (lVar20 != 0);
  FUN_822c4ba0(auStack_aa7,0xffffffff82ad1634,0x1f);
  puVar15 = auStack_a7f;
  lVar20 = 0x28;
  do {
    *puVar15 = 0;
    puVar15 = puVar15 + 1;
    lVar20 = lVar20 + -1;
  } while (lVar20 != 0);
  FUN_822c4ba0(auStack_a7f,0xffffffff82ad1653,0x28);
  puVar15 = auStack_a57;
  lVar20 = 0x28;
  do {
    *puVar15 = 0;
    puVar15 = puVar15 + 1;
    lVar20 = lVar20 + -1;
  } while (lVar20 != 0);
  FUN_822c4ba0(auStack_a57,0xffffffff82ad167b,0x28);
  uStack_a20 = DAT_82ad16a4;
  uStack_6dd = DAT_82ad16a6;
  uStack_a08 = DAT_82ad16ac;
  uStack_948 = DAT_82ad16ad;
  uStack_947 = DAT_82ad16ae;
  FUN_826001b8(auStack_946,0xffffffff82ad16b0,0x30);
  FUN_826001b8(auStack_916,0xffffffff82ad16e0,0x30);
  uStack_9d0 = DAT_82ad1710;
  uStack_a00 = DAT_82ad171c;
  uStack_9fc = DAT_82ad1720;
  uStack_a07 = DAT_82ad1724;
  uStack_a06 = DAT_82ad1726;
  uStack_a04 = DAT_82ad1728;
  uStack_a03 = DAT_82ad1729;
  uStack_a02 = DAT_82ad172a;
  uStack_a01 = DAT_82ad172b;
  iVar12 = FUN_8230b5b8(param_1);
  dVar23 = (double)DAT_82ad16a8;
  if ((iVar12 != 0) &&
     ((fVar1 = DAT_82022658, *(int *)(iVar12 + 8) == 1 ||
      (fVar1 = DAT_820035b0, *(int *)(iVar12 + 8) == 2)))) {
    dVar23 = (double)(float)(dVar23 + (double)fVar1);
  }
  cVar13 = FUN_823163c8();
  if ((cVar13 == '\0') && (iVar12 = FUN_821dc9c0(uVar5), iVar12 != DAT_82ad1618)) {
    uVar10 = FUN_824d4820(uVar6);
    if (uVar10 < 0x14) {
      if (uVar10 < 10) {
        if (uVar10 < 2) goto LAB_82320758;
        dVar21 = (double)DAT_82003a3c;
      }
      else {
        dVar21 = (double)DAT_82002398;
      }
    }
    else {
      dVar21 = (double)DAT_8201da2c;
    }
    dVar23 = (double)(float)(dVar23 + dVar21);
  }
LAB_82320758:
  dVar21 = (double)DAT_82000a34;
  if ((dVar23 < dVar21) || ((dVar23 < dVar22 && (dVar22 = dVar23, dVar23 < dVar21)))) {
    dVar22 = dVar21;
  }
  if (DAT_82ad1718 == -1) {
    FUN_8224d778(dVar22,0);
  }
  else {
    FUN_8224d7e8(1,iVar3);
  }
  iVar12 = 0x1f;
  puVar14 = &uStack_94c;
  do {
    iVar12 = iVar12 + -1;
    *puVar14 = 0;
    puVar14 = puVar14 + -1;
  } while (-1 < iVar12);
  puVar19 = auStack_946;
  iVar12 = 2;
  do {
    iVar18 = 0x18;
    do {
      uVar2 = *puVar19;
      if (uVar2 != 0) {
        if (999 < uVar2) {
          FUN_822c5128(auStack_9c8);
        }
        uVar10 = uVar2 >> 3 & 0x1ffffffc;
        *(uint *)((int)auStack_9c8 + uVar10) =
             1 << (uVar2 & 0x1f) | *(uint *)((int)auStack_9c8 + uVar10);
      }
      iVar18 = iVar18 + -1;
      puVar19 = puVar19 + 1;
    } while (iVar18 != 0);
    iVar12 = iVar12 + -1;
  } while (iVar12 != 0);
  FUN_821d1a38(&uStack_b00);
  FUN_82236060(0xffffffff827a99f8,&uStack_b00,iVar3);
  FUN_82237dd0(0xffffffff827a99f8,1);
  uVar8 = FUN_824d4820(uVar6);
  cVar13 = FUN_821d5610(puVar16,puVar17,uVar8,1);
  if (cVar13 == '\0') {
    cVar13 = FUN_821d24c0(puVar16,puVar17,1);
    if (cVar13 != '\0') {
      uStack_bec = 2;
    }
  }
  else {
    uStack_bec = 1;
  }
  FUN_82143748(param_1,auStack_5d0);
  uVar10 = FUN_821dd2f8(uVar5,param_1);
  auStack_be8[param_1] = uVar10;
  uVar10 = FUN_821dd308(uVar5,param_1);
  auStack_be8[param_1 + 2] = uVar10;
  uVar10 = FUN_821dd318(uVar5,param_1);
  auStack_be8[param_1 + 4] = uVar10;
  uVar10 = FUN_821dca18(uVar5,param_1);
  auStack_be8[param_1 + 6] = uVar10;
  auStack_be8[param_1 + 8] = 0;
  uVar10 = FUN_821dd2f8(uVar5,iVar3);
  auStack_be8[iVar3] = uVar10;
  uVar10 = FUN_821dd308(uVar5,iVar3);
  auStack_be8[iVar3 + 2] = uVar10;
  uVar10 = FUN_821dd318(uVar5,iVar3);
  auStack_be8[iVar3 + 4] = uVar10;
  uVar10 = FUN_821dca18(uVar5,iVar3);
  auStack_be8[iVar3 + 6] = uVar10;
  auStack_be8[iVar3 + 8] = 1;
  iStack_bb8 = 0xa8c;
  uStack_bb4 = 0xc9;
  uStack_bb0 = 3;
  cVar13 = FUN_823163c8();
  if (cVar13 != '\0') {
    FUN_82316380();
    iStack_bb8 = FUN_82316438();
    iStack_bb8 = iStack_bb8 * 0x3c;
    FUN_82316380();
    uStack_bb0 = FUN_823163e8();
  }
  uVar9 = FUN_822499e8(0);
  uVar9 = uVar9 & 0xff;
  uVar4 = uVar9 * 0xaf286bcb >> 0x20;
  uStack_ba8 = *(undefined4 *)
                ((int)auStack_b50 +
                (int)((uVar9 + (((uVar9 - uVar4 & 0xffffffff) >> 1) + uVar4 >> 4) * -0x13 &
                      0xffffffff) << 2));
  uStack_bac = FUN_821dc9c0(uVar5);
  uStack_ba4 = FUN_824d4820(uVar6);
  uStack_ba0 = 0;
  uStack_b9f = 0;
  FUN_821dcd98(uVar7,&uStack_bf0);
  DAT_82ad1730 = 0;
  FUN_822cde60(PTR_DAT_82084200,auStack_be8[0] & 0xff,auStack_be8[1] & 0xff,uStack_bac);
  return;
}



// ===================================================
// 822DB740  ->  FUN_822db740  (entree 822db740)
// ===================================================

void FUN_822db740(undefined4 param_1)

{
  DAT_82ac347c = param_1;
  return;
}



// ===================================================
// 8230B540  ->  FUN_8230b540  (entree 8230b540)
// ===================================================

void FUN_8230b540(void)

{
  FUN_822c2888(0x178);
  FUN_82166380(0x151);
  FUN_822b2958(0xffffffff8208e014);
  DAT_82acb334 = 0;
  FUN_8230b2f8(0xffffffff82acb32c);
  FUN_822c2888(0x172);
  FUN_82166380(0x14b);
  FUN_822b2958(0xffffffff8208e02c);
  DAT_82acb330 = 0;
  return;
}



// ===================================================
// 82308480  ->  FUN_82308480  (entree 82308480)
// ===================================================

undefined8 FUN_82308480(void)

{
  return 0xffffffff82acb1f0;
}



