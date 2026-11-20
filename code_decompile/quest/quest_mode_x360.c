// ===================================================
// 823002D8  ->  FUN_823002d8  (entree 823002d8)
// ===================================================

undefined8 FUN_823002d8(void)

{
  char cVar1;
  
  FUN_82356c08();
  FUN_821dff70();
  FUN_8230dc78();
  FUN_8230dae0();
  FUN_8227ee78(PTR_DAT_826539c4);
  FUN_82308490();
  cVar1 = FUN_822d0c80(0);
  if (cVar1 == '\0') {
    FUN_821df868(1);
  }
  else {
    FUN_821df868(0);
  }
  FUN_822da6b0(cVar1 != '\0',0x1e,0);
  DAT_82ac921c = 0;
  return 1;
}



// ===================================================
// 82300360  ->  FUN_82300360  (entree 82300360)
// ===================================================

undefined8 FUN_82300360(void)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  
  uVar1 = FUN_821dc920();
  uVar2 = FUN_821dc9c0();
  FUN_8218dea0();
  uVar3 = FUN_82315930();
  FUN_82315d00(uVar3,uVar2);
  FUN_8230db10();
  FUN_8231fe58();
  FUN_821dd710(uVar1,uVar2);
  FUN_822da6b0(0,0xffffffffffffffff,0);
  FUN_822da6b0(1,0xffffffffffffffff,0);
  FUN_821dd4f0();
  FUN_8227e210(PTR_DAT_826539c4);
  FUN_8227d988(PTR_DAT_826539c4);
  FUN_823084a8();
  FUN_8230d838();
  FUN_8230b540();
  FUN_821e0bc8();
  return 1;
}



// ===================================================
// 82300410  ->  FUN_82300410  (entree 82300410)
// ===================================================

undefined8 FUN_82300410(void)

{
  undefined8 uVar1;
  char cVar2;
  
  uVar1 = FUN_821dc920();
  cVar2 = FUN_821dfff0();
  if (cVar2 == '\0') {
    FUN_82356ca0();
    FUN_821fa038(PTR_DAT_82015b34,0);
    FUN_8229fb10(PTR_DAT_82655c08);
    cVar2 = FUN_821dc930(uVar1,0);
    if (cVar2 != '\0') {
      FUN_8229fb78(PTR_DAT_82655c08,0);
    }
    cVar2 = FUN_821dc930(uVar1,1);
    if (cVar2 != '\0') {
      FUN_8229fb78(PTR_DAT_82655c08,1);
    }
    uVar1 = 1;
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}



// ===================================================
// 823004C8  ->  FUN_823004c8  (entree 823004c8)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

undefined8 FUN_823004c8(void)

{
  undefined8 uVar1;
  char cVar8;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  char *pcVar7;
  
  uVar1 = FUN_821dc920();
  cVar8 = FUN_822c80d0(PTR_DAT_82655c08);
  if (cVar8 == '\0') {
    FUN_82237ce8(0xffffffff827a99f8);
    FUN_821dc9c0(uVar1);
    pcVar7 = (char *)FUN_8230b5b8();
    if ((pcVar7 != (char *)0x0) && (*pcVar7 == '\0')) {
      FUN_8230b6b8();
    }
    FUN_8230d270();
    FUN_823177c0();
    FUN_8231fe20();
    return 1;
  }
  FUN_82307010(0);
  cVar8 = FUN_823073e0();
  if (cVar8 == '\0') {
    FUN_82307010(1);
    cVar8 = FUN_823073e0();
    if (cVar8 == '\0') {
      cVar8 = FUN_822a0020(PTR_DAT_82655c08);
      if (cVar8 != '\0') {
        uVar2 = FUN_821dc9c0(uVar1);
        uVar3 = FUN_8229fc10(PTR_DAT_82655c08,uVar2);
        uVar4 = FUN_8229fc20(PTR_DAT_82655c08,uVar2);
        uVar5 = FUN_8229fc18(PTR_DAT_82655c08,uVar2,uVar4);
        uVar6 = FUN_8229fc28(PTR_DAT_82655c08,uVar2);
        FUN_821dc940(uVar1,uVar2,uVar3,uVar5,uVar4,uVar6);
      }
      return 0;
    }
  }
  DAT_82ac921c = 0;
  FUN_8220d1e0(0x59);
  return 0;
}



// ===================================================
// 82300618  ->  FUN_82300618  (entree 82300618)
// ===================================================

undefined8 FUN_82300618(void)

{
  thunk_FUN_822c7d50(PTR_DAT_82655c08);
  return 1;
}



// ===================================================
// 82320DB0  ->  FUN_82320db0  (entree 82320db0)
// ===================================================

undefined8 FUN_82320db0(void)

{
  int *piVar1;
  
  piVar1 = (int *)FUN_82308480();
  (**(code **)(*piVar1 + 0xc))();
  FUN_8230b540();
  FUN_82320300(DAT_82ad1618);
  FUN_822db740(DAT_82ad1618);
  return 1;
}



// ===================================================
// 8231FAB8  ->  FUN_8231fab8  (entree 8231fab8)
// ===================================================

undefined8 FUN_8231fab8(void)

{
  FUN_8220d1e0(0x57);
  return 0;
}



// ===================================================
// 82320E08  ->  FUN_82320e08  (entree 82320e08)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

undefined8 FUN_82320e08(void)

{
  char cVar6;
  undefined8 uVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  longlong lVar4;
  undefined8 uVar5;
  
  cVar6 = FUN_822ccf80(PTR_DAT_82084200);
  if (cVar6 == '\0') {
    FUN_821fa038(PTR_DAT_82015b34,3);
    FUN_8227e210(PTR_DAT_826539c4);
    uVar1 = FUN_821dc920();
    uVar2 = FUN_821dc9f8();
    uVar3 = FUN_821dc9c0(uVar1);
    FUN_821dd788(uVar1);
    lVar4 = FUN_821dd070(uVar2,uVar3);
    uVar5 = FUN_821dd308(uVar1,uVar3);
    uVar1 = FUN_821dd2f8(uVar1,uVar3);
    FUN_8218abe8(uVar3,uVar1,uVar5,lVar4 + 0x59);
    FUN_821e23b0(0xffffffff8208f4cc,uVar2);
    FUN_82305c30();
    FUN_821ca8c0(9,0xffffffff82320a68,0);
    FUN_821ca8c0(0xf,0xffffffff8231fae0,0);
    return 1;
  }
  return 0;
}



// ===================================================
// 8231FEB8  ->  FUN_8231feb8  (entree 8231feb8)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

undefined8 FUN_8231feb8(void)

{
  undefined1 uVar1;
  undefined4 uVar2;
  bool bVar3;
  bool bVar4;
  undefined1 uVar5;
  undefined8 uVar6;
  ulonglong uVar7;
  char cVar10;
  undefined8 uVar8;
  int iVar9;
  int iStack_50;
  undefined4 uStack_4c;
  
  FUN_821fa038(PTR_DAT_82015b34,3);
  uVar6 = FUN_821dc920();
  uVar7 = FUN_821cfbd0();
  cVar10 = FUN_821e3ba8();
  if (cVar10 != '\0') {
    cVar10 = FUN_823163c8();
    if (cVar10 == '\0') {
      FUN_821dc9f8(uVar6);
      iVar9 = FUN_821dd368();
      FUN_82315120(DAT_82ad162c,iVar9 != DAT_82ad1618);
      uVar8 = 0x54;
    }
    else {
      uVar8 = 0x55;
    }
    FUN_8220d1e0(uVar8);
  }
  cVar10 = FUN_821e3e90();
  if (cVar10 != '\0') {
    uVar8 = FUN_82315120(DAT_82ad162c,0);
    DAT_82ad162c = (undefined4)uVar8;
    FUN_8230ddf0(uVar8,0xffffffff82ad1634);
    uVar5 = DAT_82ad16ac;
    iVar9 = DAT_82ad1630;
    uVar2 = *(undefined4 *)(&DAT_820036c0 + DAT_82ad1618 * 4);
    uVar1 = (&DAT_82ad16ad)[DAT_82ad1630];
    FUN_821dd578(uVar6,uVar2,1,0);
    FUN_821dc940(uVar6,uVar2,uVar5,uVar1,iVar9,0);
    iVar9 = FUN_8230b5b8(DAT_82ad1618);
    if (iVar9 != 0) {
      iStack_50 = iVar9 + 0x74;
      uStack_4c = DAT_82ad162c;
      FUN_821d1798(&iStack_50,1);
    }
    FUN_8220d1e0(0x56);
  }
  cVar10 = FUN_821e3bb8();
  if (cVar10 == '\0') {
    return 0;
  }
  cVar10 = FUN_821e3c98();
  if (cVar10 == '\0') {
    return 0;
  }
  if ((uVar7 & 0xffffffff) == 0) {
LAB_82320038:
    bVar3 = false;
  }
  else {
    cVar10 = FUN_821cfe88(uVar7);
    bVar3 = true;
    if (cVar10 == '\0') goto LAB_82320038;
  }
  bVar4 = false;
  if (bVar3) {
    FUN_821cfe30(uVar7);
  }
  cVar10 = FUN_82315e20(0xffffffff82ad0628);
  if (cVar10 == '\0') {
    cVar10 = FUN_822c80d0(0xffffffff82ad0628);
    if (cVar10 == '\0') {
      bVar4 = true;
    }
    else {
      iVar9 = FUN_82315de0(0xffffffff82ad0628);
      if (iVar9 != -1) {
        if (iVar9 == 0) {
          if (bVar3) {
            FUN_821cfe48(uVar7);
            FUN_82315e78(0xffffffff82ad0628);
            goto LAB_82320100;
          }
        }
        else {
          iVar9 = FUN_823158c0(DAT_82ad0674);
          if (iVar9 == 0) {
            FUN_82317f88(DAT_82ad0674);
          }
          bVar4 = true;
        }
        FUN_82315e78(0xffffffff82ad0628);
      }
    }
  }
  else {
    cVar10 = FUN_821e3cc0();
    if (cVar10 != '\0') {
      FUN_82315e50(0xffffffff82ad0628);
    }
  }
LAB_82320100:
  if ((bVar3) && (bVar4)) {
    uVar8 = FUN_821cfd58(uVar7);
    FUN_821cfe48(uVar7);
    FUN_821dd578(uVar6,uVar8,1,1);
    FUN_821e3e80(1);
  }
  return 0;
}



// ===================================================
// 82320F08  ->  FUN_82320f08  (entree 82320f08)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

undefined8 FUN_82320f08(void)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  char cVar5;
  int iVar4;
  
  uVar2 = FUN_821dc920();
  uVar3 = FUN_821dc9f8();
  iVar1 = *(int *)(&DAT_820036c0 + DAT_82ad1618 * 4);
  cVar5 = FUN_821e3bb8();
  if (cVar5 == '\0') {
    iVar4 = FUN_821dde10(uVar3);
    DAT_82ad1730 = iVar4 + DAT_82ad1730;
  }
  uVar3 = FUN_8230b5b8(DAT_82ad1618);
  FUN_8230b5f8(uVar3,DAT_82ad1730);
  FUN_8230b660(uVar3);
  FUN_821ca9b8(9,0xffffffff82320a68,0);
  FUN_821ca9b8(0xf,0xffffffff8231fae0,0);
  FUN_821e2408();
  FUN_82305c48();
  (&DAT_827a9a09)[iVar1 * 0x528] = 0;
  FUN_821f1ce0(iVar1,0);
  FUN_821ed240(iVar1);
  iVar4 = FUN_8220d178();
  if (*(int *)(iVar4 + 0x20) != 0x56) {
    FUN_821fa038(PTR_DAT_82015b34,0);
    FUN_821dd710(uVar2,iVar1);
    cVar5 = FUN_821dc930(uVar2,DAT_82ad1618);
    if (cVar5 == '\0') {
      FUN_821dd578(uVar2,DAT_82ad1618,0,0);
    }
    FUN_821dc940(uVar2,DAT_82ad1618,DAT_82ad161c,DAT_82ad1620,DAT_82ad1624,DAT_82ad1628);
    FUN_821dc9b8(uVar2,DAT_82ad1618);
  }
  return 1;
}



// ===================================================
// 82320A68  ->  FUN_82320a68  (entree 82320a68)
// ===================================================

/* WARNING: Function: __savegprlr_24 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_24 replaced with injection: x360_restgprlr */

void FUN_82320a68(void)

{
  undefined8 uVar1;
  undefined8 uVar2;
  int iVar6;
  int iVar7;
  undefined8 uVar3;
  undefined8 uVar4;
  int iVar8;
  char cVar9;
  ulonglong uVar5;
  int iStack_5a0;
  int iStack_59c;
  int aiStack_590 [8];
  undefined1 auStack_570 [249];
  undefined1 uStack_477;
  undefined2 uStack_476;
  undefined1 uStack_474;
  undefined1 uStack_473;
  undefined1 uStack_472;
  undefined1 uStack_471;
  undefined4 uStack_470;
  undefined4 uStack_46c;
  byte bStack_14d;
  
  uVar1 = FUN_821dc920();
  uVar2 = FUN_821dc9f8();
  iVar6 = FUN_821ccbb8();
  iVar6 = *(int *)(&DAT_820036c0 + iVar6 * 4);
  iVar7 = FUN_821dd368(uVar2);
  uVar3 = FUN_821dd370(uVar2);
  uVar4 = FUN_82315930();
  iVar8 = FUN_821dde10(uVar2);
  DAT_82ad1730 = iVar8 + DAT_82ad1730;
  cVar9 = FUN_821e3bb8();
  if (cVar9 != '\0') {
    FUN_821df900(uVar2);
    FUN_821dd080(uVar2,1);
    FUN_821d05f8(DAT_82ad1618,0);
    FUN_821df480(auStack_570);
    FUN_822360c8(0xffffffff827a99f8,auStack_570,*(undefined4 *)(&DAT_820036c0 + DAT_82ad1618 * 4));
    DAT_82ad171c = uStack_470;
    DAT_82ad1720 = uStack_46c;
    DAT_82ad1724 = uStack_477;
    DAT_82ad1726 = uStack_476;
    DAT_82ad1728 = uStack_474;
    DAT_82ad1729 = uStack_473;
    DAT_82ad172a = uStack_472;
    DAT_82ad172b = uStack_471;
    FUN_8230db40(DAT_82ad162c,0xffffffff82ad1634);
    FUN_82315a10(uVar4);
    if (iVar7 == DAT_82ad1618) {
      if (bStack_14d != 0) {
        FUN_822da898();
        iVar7 = FUN_822dac40();
        if (iVar7 != 0) {
          iStack_5a0 = iVar7 + 0x7d;
          iStack_59c = bStack_14d - 1;
          FUN_823178e0(&iStack_5a0,1);
        }
      }
      if (iVar6 == DAT_82ad1618) {
        FUN_821dc9f0(uVar1);
        uVar5 = FUN_824d4820();
        if (9 < (uVar5 & 0xffffffff)) {
          for (iVar7 = (-(uint)(0x13 < uVar5) & 2) + 1; iVar7 != 0; iVar7 = iVar7 + -1) {
            FUN_82315a10(uVar4);
          }
        }
      }
      cVar9 = FUN_823159d0(uVar4);
      if ((cVar9 == '\0') && (DAT_82ad172c < 999)) {
        DAT_82ad172c = DAT_82ad172c + 1;
      }
      iVar7 = FUN_8230b5b8(DAT_82ad1618);
      if (iVar7 != 0) {
        iStack_5a0 = iVar7 + 0xf4;
        iStack_59c = DAT_82ad162c;
        FUN_821d1798(&iStack_5a0,1);
        if (*(uint *)(iVar7 + 4) < DAT_82ad172c) {
          *(uint *)(iVar7 + 4) = DAT_82ad172c;
        }
      }
      cVar9 = FUN_82310098(DAT_82ad1618,DAT_82ad1714,0);
      if (cVar9 != '\0') {
        aiStack_590[0] = 8;
        aiStack_590[1] = 9;
        aiStack_590[2] = 6;
        aiStack_590[3] = 4;
        aiStack_590[4] = 5;
        aiStack_590[5] = 3;
        aiStack_590[6] = 7;
        aiStack_590[7] = 0x20;
        if (aiStack_590[DAT_82ad1714] != 0x20) {
          FUN_822db578(aiStack_590[DAT_82ad1714],0xffffffffffffffff);
        }
      }
    }
    else {
      DAT_82ad172c = 0;
    }
    FUN_821ed930();
    if ((int)uVar3 == iVar6) {
      FUN_821e0448(uVar3);
    }
  }
  return;
}



// ===================================================
// 82320150  ->  FUN_82320150  (entree 82320150)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_82320150(longlong param_1)

{
  undefined1 uVar1;
  uint uVar2;
  undefined1 uVar3;
  undefined8 uVar4;
  undefined4 uVar6;
  ulonglong uVar5;
  int iVar7;
  char cVar8;
  int iStack_40;
  undefined4 uStack_3c;
  
  uVar4 = FUN_821dc920();
  DAT_82ad1618 = FUN_821dc9c0();
  DAT_82ad161c = FUN_821dd2f8(uVar4);
  DAT_82ad1620 = FUN_821dd308(uVar4,DAT_82ad1618);
  DAT_82ad1624 = FUN_821dd318(uVar4,DAT_82ad1618);
  DAT_82ad1628 = FUN_821dca18(uVar4,DAT_82ad1618);
  DAT_82ad172c = 0;
  uVar6 = FUN_822d0d60(0x100);
  DAT_82ad1630 = (uint)LZCOUNT((int)LZCOUNT(uVar6)) >> 5 ^ 1;
  if ((int)param_1 == -1) {
    uVar5 = FUN_822499e8(0);
    param_1 = uVar5 + ((uVar5 & 0xffffffff) / 1000) * -1000;
  }
  DAT_82ad162c = (undefined4)param_1;
  FUN_8230ddf0(param_1,0xffffffff82ad1634);
  uVar3 = DAT_82ad16ac;
  uVar2 = DAT_82ad1630;
  uVar6 = *(undefined4 *)(&DAT_820036c0 + DAT_82ad1618 * 4);
  uVar1 = (&DAT_82ad16ad)[DAT_82ad1630];
  FUN_821dd578(uVar4,uVar6,1,0);
  FUN_821dc940(uVar4,uVar6,uVar3,uVar1,uVar2,0);
  iVar7 = FUN_8230b5b8(DAT_82ad1618);
  if (iVar7 != 0) {
    iStack_40 = iVar7 + 0x74;
    uStack_3c = DAT_82ad162c;
    FUN_821d1798(&iStack_40,1);
  }
  cVar8 = FUN_823163c8();
  if (cVar8 == '\0') {
    FUN_821dc9c8();
    uVar4 = FUN_821dc9f0(uVar4);
    iVar7 = FUN_82312590();
    FUN_82551720(uVar4);
    if (iVar7 != 0) {
      do {
        FUN_821dcc48(uVar4);
        iVar7 = iVar7 + -1;
      } while (iVar7 != 0);
      return;
    }
  }
  else {
    FUN_821dc9f0(uVar4);
    FUN_82551720();
  }
  return;
}



// ===================================================
// 82300738  ->  FUN_82300738  (entree 82300738)
// ===================================================

undefined8 FUN_82300738(void)

{
  char cVar1;
  
  cVar1 = FUN_822cf428();
  if (cVar1 != '\0') {
    FUN_822cf410();
  }
  return 1;
}



// ===================================================
// 82300770  ->  FUN_82300770  (entree 82300770)
// ===================================================

undefined8 FUN_82300770(void)

{
  char cVar1;
  
  cVar1 = FUN_822cf438();
  if (cVar1 != '\0') {
    FUN_8220d1e0(0x54);
  }
  return 0;
}



// ===================================================
// 823007A8  ->  FUN_823007a8  (entree 823007a8)
// ===================================================

undefined8 FUN_823007a8(void)

{
  FUN_822cf470();
  return 1;
}



