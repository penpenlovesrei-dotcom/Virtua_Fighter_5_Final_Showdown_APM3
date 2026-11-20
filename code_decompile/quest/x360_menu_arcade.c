// ===================================================
// 82313F50  ->  FUN_82313ea8  (entree 82313ea8)
// ===================================================

/* WARNING: Function: __savegprlr_14 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_14 replaced with injection: x360_restgprlr */

void FUN_82313ea8(void)

{
  undefined4 uVar1;
  undefined1 uVar2;
  int iVar6;
  char cVar9;
  undefined8 uVar3;
  int iVar7;
  undefined8 uVar4;
  undefined8 uVar5;
  int iVar8;
  undefined1 *puVar10;
  undefined2 *puVar11;
  int iVar12;
  undefined4 *puVar13;
  ulonglong uVar14;
  ulonglong uVar15;
  longlong lVar16;
  double dVar17;
  double dVar18;
  double dVar19;
  double dVar20;
  double dVar21;
  double dVar22;
  double dVar23;
  double dVar24;
  double dVar25;
  float local_250;
  float local_24c;
  float local_248;
  int local_240;
  undefined4 local_23c;
  undefined4 local_230 [8];
  float local_210 [9];
  float local_1ec;
  float local_1e8;
  undefined1 local_1e0 [31];
  undefined1 local_1c1 [40];
  undefined1 local_199 [49];
  undefined1 local_168;
  undefined2 local_164 [48];
  undefined4 local_104;
  undefined1 local_f0;
  
  iVar6 = FUN_826018b4();
  iVar12 = iVar6 + 0x564;
  cVar9 = FUN_822e2dd8(iVar12);
  if ((cVar9 != '\0') && (*(int *)(iVar6 + 0xdc) != 4)) {
    dVar19 = (double)DAT_82000a34;
    local_250 = DAT_82000a34;
    local_24c = DAT_82000a34;
    local_248 = DAT_82000a34;
    uVar3 = FUN_822c29e8();
    iVar7 = FUN_8230b5b8(*(undefined4 *)(iVar6 + 0x5c));
    local_210[0] = 7.39886e-43;
    local_210[1] = 7.41287e-43;
    local_210[2] = 7.42688e-43;
    local_210[3] = 7.44089e-43;
    local_210[4] = 7.45491e-43;
    local_210[5] = 7.46892e-43;
    local_210[6] = 7.48293e-43;
    local_210[7] = 7.49695e-43;
    local_230[0] = 0x24d;
    local_230[1] = 0x24e;
    local_230[2] = 0x24f;
    local_230[3] = 0x251;
    local_230[4] = 0x252;
    FUN_822c29d8(2);
    FUN_822c2a08(9);
    FUN_8223bc10(0xe);
    FUN_8223c130(9);
    FUN_8223c048(0xffffffffffffffff);
    FUN_822e39c0(iVar12,&local_250,0xffffffff8208e704,1);
    FUN_8223beb8((double)local_250,(double)local_24c);
    uVar4 = FUN_82322798(local_210[*(int *)(iVar6 + 0x4c)]);
    FUN_8223fe30(0xffffffff8208476c,uVar4);
    puVar13 = (undefined4 *)(iVar6 + 100);
    dVar21 = (double)DAT_82000f0c;
    dVar20 = (double)DAT_8208e6f8;
    dVar25 = (double)DAT_8200651c;
    dVar24 = (double)DAT_8208e6fc;
    dVar23 = (double)DAT_82001e60;
    dVar22 = (double)DAT_8208e700;
    uVar15 = 0;
    do {
      uVar14 = uVar15;
      cVar9 = FUN_823163a0(*(undefined4 *)(iVar6 + 0x4c));
      if (cVar9 == '\0') {
        puVar10 = local_1e0;
        lVar16 = 0x1f;
        do {
          *puVar10 = 0;
          puVar10 = puVar10 + 1;
          lVar16 = lVar16 + -1;
        } while (lVar16 != 0);
        puVar10 = local_1c1;
        lVar16 = 0x28;
        do {
          *puVar10 = 0;
          puVar10 = puVar10 + 1;
          lVar16 = lVar16 + -1;
        } while (lVar16 != 0);
        puVar10 = local_199;
        lVar16 = 0x28;
        do {
          *puVar10 = 0;
          puVar10 = puVar10 + 1;
          lVar16 = lVar16 + -1;
        } while (lVar16 != 0);
        puVar11 = local_164;
        lVar16 = 0x30;
        do {
          *puVar11 = 0;
          puVar11 = puVar11 + 1;
          lVar16 = lVar16 + -1;
        } while (lVar16 != 0);
        local_104 = 0;
        FUN_8230ddf0(*puVar13,local_1e0);
        FUN_82249520(local_210,0x20,0xffffffff8208e6e0,uVar14 + 1);
        FUN_822e39c0(iVar12,&local_250,local_210,0);
        FUN_8223beb8((double)(float)((double)local_250 + dVar20),
                     (double)(float)((double)local_24c + dVar21));
        FUN_8223c130(9);
        FUN_8223c048(0xffffffffffffffff);
        uVar4 = FUN_8223c198(1);
        uVar5 = FUN_8223c1c0(1);
        FUN_8223fe30(0xffffffff82000f08,local_1e0);
        FUN_8223c198(uVar4);
        FUN_8223c1c0(uVar5);
        if (iVar7 != 0) {
          local_23c = *puVar13;
          local_240 = iVar7 + 0xf4;
          cVar9 = FUN_821d1808(&local_240);
          if (cVar9 != '\0') {
            FUN_8223c048(0xffffffffffffff00);
            FUN_8223fe30(0xffffffff82000f80,0xffffffff82010300,0xffffffff820117c8);
          }
        }
        uVar2 = local_168;
        dVar18 = (double)(float)((double)local_24c + dVar25);
        dVar17 = (double)(float)((double)local_250 + dVar24);
        uVar4 = FUN_82308480();
        FUN_82309ba0(dVar17,dVar18,uVar4,uVar14,uVar2,1,9);
        FUN_821dc920();
        iVar8 = FUN_821dc9c0();
        uVar2 = local_f0;
        dVar18 = (double)(float)((double)local_24c + dVar23);
        dVar17 = (double)(float)((double)local_250 + dVar22);
        uVar1 = *(undefined4 *)(&DAT_820036c0 + iVar8 * 4);
        uVar4 = FUN_82308480();
        FUN_82309e20(dVar17,dVar18,uVar4,uVar14,uVar1,uVar2,9);
        if ((int)uVar14 == *(int *)(iVar6 + 0x50)) {
          dVar18 = (double)local_24c;
          dVar17 = (double)local_250;
          uVar4 = FUN_82308480();
          FUN_8230a1c0(dVar17,dVar18,uVar4,0,9);
        }
      }
      uVar15 = uVar14 + 1;
      puVar13 = puVar13 + 9;
    } while ((int)uVar15 < 3);
    FUN_8223c130(9);
    FUN_8223c048(0xffffffffffffffff);
    FUN_822e39c0(iVar12,&local_250,0xffffffff8208e6c8,0);
    cVar9 = FUN_823163a0(*(undefined4 *)(iVar6 + 0x4c));
    dVar20 = (double)DAT_8208e6c4;
    if (cVar9 == '\0') {
      FUN_8223beb8((double)(float)((double)local_250 + dVar20),
                   (double)(float)((double)local_24c + dVar21));
      uVar4 = FUN_82322798(0x250);
      FUN_8223fe30(0xffffffff8208476c,uVar4);
      FUN_8223beb8((double)(float)((double)local_250 + dVar20),(double)(local_24c + DAT_82063418));
      uVar4 = FUN_82322798(*(undefined4 *)((int)local_230 + (int)((uVar15 & 0xffffffff) << 2)));
      FUN_8223fe30(0xffffffff8208476c,uVar4);
    }
    else {
      local_210[8] = (float)((double)local_250 + dVar20);
      uVar1 = *(undefined4 *)(iVar6 + 0x4c);
      local_1e8 = (float)dVar19;
      local_1ec = local_24c + DAT_8208e6c0;
      uVar4 = FUN_82308480();
      FUN_82309ff8(uVar4,uVar1,1,9,local_210 + 8);
    }
    if ((int)uVar15 == *(int *)(iVar6 + 0x50)) {
      dVar21 = (double)local_24c;
      dVar19 = (double)local_250;
      uVar4 = FUN_82308480();
      FUN_8230a1c0(dVar19,dVar21,uVar4,1,9);
    }
    FUN_822e39c0(iVar12,&local_250,0xffffffff8208e6a8,0);
    FUN_8223beb8((double)(float)((double)local_250 + dVar20),(double)(local_24c + DAT_82054e74));
    uVar4 = FUN_82322798(*(undefined4 *)((int)local_230 + (int)((uVar14 + 2 & 0xffffffff) << 2)));
    FUN_8223fe30(0xffffffff8208476c,uVar4);
    if ((int)(uVar14 + 2) == *(int *)(iVar6 + 0x50)) {
      dVar20 = (double)local_24c;
      dVar19 = (double)local_250;
      uVar4 = FUN_82308480();
      FUN_8230a1c0(dVar19,dVar20,uVar4,0,9);
    }
    FUN_822c2a18();
    FUN_822c29d8(uVar3);
  }
  FUN_82601900();
  return;
}



// ===================================================
// 82313448  ->  FUN_823130b8  (entree 823130b8)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

void FUN_823130b8(int param_1)

{
  int iVar2;
  char cVar6;
  undefined8 uVar1;
  uint uVar3;
  uint uVar4;
  undefined4 uVar5;
  undefined1 *puVar7;
  undefined1 *puVar8;
  undefined2 *puVar9;
  int iVar11;
  int *piVar12;
  ulonglong uVar10;
  longlong lVar13;
  int local_1e0 [4];
  undefined4 local_1d0 [8];
  undefined1 local_1b0 [31];
  undefined1 local_191 [40];
  undefined1 local_169 [53];
  undefined2 local_134 [48];
  undefined4 local_d4;
  undefined1 local_b0 [176];
  
  switch(*(undefined4 *)(param_1 + 0xdc)) {
  case 0:
    iVar11 = param_1 + 0x564;
    FUN_822e3ad8(iVar11);
    iVar2 = param_1 + 0x590;
    FUN_822e3ad8(iVar2);
    FUN_822e2e20(iVar2,0);
    if (*(int *)(param_1 + 0xd8) == 3) {
      FUN_822e3778(iVar11,0x2a,1);
      cVar6 = FUN_823163a0(*(undefined4 *)(param_1 + 0x4c));
      if (cVar6 != '\0') {
        uVar1 = 1;
LAB_82313180:
        FUN_822e3778(iVar2,0x2c,uVar1);
      }
    }
    else {
      FUN_822e3778(iVar11,0x2a,0);
      cVar6 = FUN_823163a0(*(undefined4 *)(param_1 + 0x4c));
      if (cVar6 != '\0') {
        uVar1 = 0;
        goto LAB_82313180;
      }
    }
    FUN_82312920(param_1 + 0x460,*(undefined4 *)(param_1 + 0x5c));
    uVar1 = FUN_82308480();
    FUN_82308978(uVar1,1);
    FUN_822e2f20(param_1 + 0x484);
    FUN_822c8aa0(param_1 + 0x484,0xffffffff8208e584);
    *(undefined4 *)(param_1 + 0xdc) = 1;
    break;
  case 1:
    cVar6 = FUN_822e2dd8(param_1 + 0x564);
    if (cVar6 != '\0') {
      *(undefined4 *)(param_1 + 0xdc) = 2;
    }
    break;
  case 2:
    piVar12 = (int *)(param_1 + 0x50);
    if (*(int *)(param_1 + 0x50) < 3) {
      cVar6 = FUN_823163a0(*(undefined4 *)(param_1 + 0x4c));
      if (cVar6 != '\0') {
        uVar1 = FUN_82308480();
        FUN_823085a0(uVar1,0x14);
        iVar2 = *piVar12;
        *piVar12 = 3;
        *(int *)(param_1 + 0x54) = iVar2;
        goto LAB_82313228;
      }
      iVar2 = FUN_822d0ca8(0x2000);
      if (iVar2 < 0) {
        cVar6 = FUN_822d0e18(piVar12,2,0);
        if (cVar6 == '\0') goto LAB_82313228;
        FUN_822d1188();
        uVar1 = FUN_82308480();
        FUN_823085a0(uVar1,0x14);
        *(undefined4 *)(param_1 + 0xcc) = 0;
      }
      else {
        FUN_822d1188();
        uVar1 = FUN_82308480();
        FUN_823085a0(uVar1,0x14);
        *(int *)(param_1 + 0x54) = *piVar12;
        *piVar12 = 4;
      }
    }
    else {
      cVar6 = FUN_823163a0(*(undefined4 *)(param_1 + 0x4c));
      if (cVar6 == '\0') {
        iVar2 = FUN_822d0ca8(0xffffffffffff8000);
        if (iVar2 < 0) goto LAB_82313228;
        FUN_822d1188();
        uVar1 = FUN_82308480();
        FUN_823085a0(uVar1,0x14);
        *piVar12 = *(int *)(param_1 + 0x54);
      }
      else {
        local_1e0[0] = *piVar12 + -3;
        cVar6 = FUN_822d0e18(local_1e0,1,0);
        if (cVar6 == '\0') {
LAB_82313228:
          iVar2 = FUN_822d1868();
          if (iVar2 < 0) {
            iVar2 = FUN_822d1830();
            if (-1 < iVar2) {
              FUN_822d1198();
              uVar1 = FUN_82308480();
              FUN_82308978(uVar1,2);
              *(undefined1 *)(param_1 + 0x464) = 1;
              *(undefined4 *)(param_1 + 0xdc) = 3;
            }
          }
          else {
            FUN_822d11a8();
            FUN_8220d1e0(0x52);
            *(undefined1 *)(param_1 + 0x464) = 1;
          }
        }
        else {
          FUN_822d1188();
          uVar1 = FUN_82308480();
          FUN_823085a0(uVar1,0x14);
          *piVar12 = local_1e0[0] + 3;
        }
      }
    }
    break;
  case 3:
    uVar1 = FUN_82308480();
    cVar6 = FUN_82308640(uVar1,0x14);
    if (cVar6 != '\0') {
      uVar10 = 0;
      *(undefined4 *)(param_1 + 0xdc) = 4;
      do {
        uVar1 = FUN_82308480();
        FUN_82308660(uVar1,uVar10);
        uVar1 = FUN_82308480();
        FUN_82308668(uVar1,uVar10);
        uVar10 = uVar10 + 1;
      } while ((uVar10 & 0xffffffff) < 3);
      uVar1 = FUN_82308480();
      FUN_82308978(uVar1,0);
      FUN_82312408(param_1 + 0x460);
      iVar2 = *(int *)(param_1 + 0x50);
      if (iVar2 != 3) {
        if (iVar2 != 4) {
          cVar6 = FUN_82317860(0);
          if (cVar6 != '\0') {
            FUN_82316390(0);
            FUN_82317f88();
          }
          uVar1 = FUN_82308480();
          FUN_823085a0(uVar1,0x10);
          *(int *)(param_1 + 0x58) = *(int *)(param_1 + 0x50);
          FUN_82320150(*(undefined4 *)(*(int *)(param_1 + 0x50) * 0x24 + param_1 + 100));
          FUN_8220d1e0(0x56);
          FUN_822b1610(0);
          break;
        }
        iVar2 = 2;
      }
      *(int *)(param_1 + 0xd4) = iVar2;
    }
  }
  if (*(int *)(param_1 + 0xdc) != 4) {
    FUN_823129a0(param_1 + 0x460);
  }
  iVar2 = *(int *)(param_1 + 0x50);
  local_1d0[0] = 0x92;
  local_1d0[1] = 0x93;
  local_1d0[2] = 0x94;
  local_1d0[3] = 0x96;
  local_1d0[4] = 0x99;
  if (2 < iVar2) {
    uVar5 = FUN_82322798(local_1d0[iVar2]);
    *(undefined4 *)(param_1 + 0x4d0) = uVar5;
    uVar5 = FUN_82322798(0xc);
    *(undefined4 *)(param_1 + 0x554) = uVar5;
    return;
  }
  local_b0[0] = 0;
  iVar2 = iVar2 * 0x24 + param_1;
  if ((1 < *(int *)(iVar2 + 0x80)) &&
     (iVar11 = *(int *)(param_1 + 0xcc) / 0x3c + (*(int *)(param_1 + 0xcc) >> 0x1f),
     (iVar11 - (iVar11 >> 0x1f) & 1U) == 0)) {
    puVar8 = local_1b0;
    lVar13 = 0x1f;
    do {
      *puVar8 = 0;
      puVar8 = puVar8 + 1;
      lVar13 = lVar13 + -1;
    } while (lVar13 != 0);
    puVar8 = local_191;
    lVar13 = 0x28;
    do {
      *puVar8 = 0;
      puVar8 = puVar8 + 1;
      lVar13 = lVar13 + -1;
    } while (lVar13 != 0);
    puVar8 = local_169;
    lVar13 = 0x28;
    do {
      *puVar8 = 0;
      puVar8 = puVar8 + 1;
      lVar13 = lVar13 + -1;
    } while (lVar13 != 0);
    puVar9 = local_134;
    lVar13 = 0x30;
    do {
      *puVar9 = 0;
      puVar9 = puVar9 + 1;
      lVar13 = lVar13 + -1;
    } while (lVar13 != 0);
    local_d4 = 0;
    FUN_8230ddf0(*(undefined4 *)(iVar2 + 100),local_1b0);
    uVar1 = FUN_82322798(0x95);
    uVar3 = FUN_825ffcb0(uVar1,0xffffffff82000f08);
    uVar1 = FUN_82322798(0x95);
    uVar4 = FUN_825ffcb0(uVar1,0xffffffff82003ed8);
    if (uVar3 < uVar4) {
      puVar7 = local_1b0;
      puVar8 = *(undefined1 **)(*(int *)(param_1 + 0x50) * 0x24 + param_1 + 0x80);
      uVar1 = FUN_82322798(0x95);
    }
    else {
      if (uVar3 <= uVar4) goto LAB_823135f4;
      puVar8 = local_1b0;
      puVar7 = *(undefined1 **)(*(int *)(param_1 + 0x50) * 0x24 + param_1 + 0x80);
      uVar1 = FUN_82322798(0x95);
    }
    FUN_82249520(local_b0,0x80,uVar1,puVar7,puVar8);
  }
LAB_823135f4:
  uVar1 = FUN_82322798(local_1d0[*(int *)(param_1 + 0x50)]);
  FUN_82249520(0xffffffff82acfed0,0x100,0xffffffff8208e624,uVar1,0xffffffff8208e62c,local_b0);
  *(undefined1 *)(param_1 + 0x507) = 1;
  *(undefined **)(param_1 + 0x4d0) = &DAT_82acfed0;
  uVar5 = FUN_82322798(0xc);
  *(undefined4 *)(param_1 + 0x554) = uVar5;
  return;
}



