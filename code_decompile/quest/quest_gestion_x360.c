// ===================================================
// 82300038  ->  FUN_82300038  (entree 82300038)
// ===================================================

undefined8 FUN_82300038(void)

{
  FUN_823029d8();
  FUN_822d09c0(0);
  FUN_822d0c30(2);
  return 1;
}



// ===================================================
// 82300070  ->  FUN_82300070  (entree 82300070)
// ===================================================

undefined8 FUN_82300070(void)

{
  FUN_82304870();
  return 1;
}



// ===================================================
// 82300098  ->  FUN_82300098  (entree 82300098)
// ===================================================

undefined8 FUN_82300098(void)

{
  FUN_82304888();
  return 1;
}



// ===================================================
// 823000C0  ->  FUN_823000c0  (entree 823000c0)
// ===================================================

undefined8 FUN_823000c0(void)

{
  FUN_82305290();
  return 1;
}



// ===================================================
// 823000E8  ->  FUN_823000e8  (entree 823000e8)
// ===================================================

undefined8 FUN_823000e8(void)

{
  FUN_823052a8();
  return 1;
}



// ===================================================
// 82300110  ->  FUN_82300110  (entree 82300110)
// ===================================================

undefined8 FUN_82300110(void)

{
  FUN_82301850();
  return 1;
}



// ===================================================
// 82300138  ->  FUN_82300138  (entree 82300138)
// ===================================================

undefined8 FUN_82300138(void)

{
  FUN_82301868();
  return 1;
}



// ===================================================
// 82300160  ->  FUN_82300160  (entree 82300160)
// ===================================================

undefined8 FUN_82300160(void)

{
  FUN_82302200();
  return 1;
}



// ===================================================
// 82300188  ->  FUN_82300188  (entree 82300188)
// ===================================================

undefined8 FUN_82300188(void)

{
  FUN_82302218();
  return 1;
}



// ===================================================
// 823001B0  ->  FUN_823001b0  (entree 823001b0)
// ===================================================

undefined8 FUN_823001b0(void)

{
  char cVar1;
  
  cVar1 = FUN_822fa098(0xffffffff82ac8510);
  if (cVar1 == '\0') {
    return 0;
  }
  FUN_822c29d8(0);
  FUN_82301e28();
  return 1;
}



// ===================================================
// 82300208  ->  FUN_82300208  (entree 82300208)
// ===================================================

undefined8 FUN_82300208(void)

{
  FUN_82301e60();
  FUN_822c29d8(2);
  return 1;
}



// ===================================================
// 82300248  ->  FUN_82300248  (entree 82300248)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

void FUN_82300248(void)

{
  undefined1 uVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  int iVar6;
  int iVar7;
  undefined8 uVar4;
  undefined8 uVar5;
  
  uVar2 = FUN_821dc920();
  uVar3 = FUN_821dc9c0();
  iVar6 = FUN_821dd318(uVar2,uVar3);
  iVar7 = FUN_82235f28(0xffffffff827a99f8,uVar3);
  uVar4 = FUN_821dca18(uVar2,uVar3);
  uVar1 = *(undefined1 *)(iVar7 + iVar6 + 0x1b8);
  uVar5 = FUN_821dd2f8(uVar2,uVar3);
  FUN_821dc940(uVar2,uVar3,uVar5,uVar1,iVar6,uVar4);
  return;
}



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
// 82300648  ->  FUN_82300648  (entree 82300648)
// ===================================================

undefined8 FUN_82300648(void)

{
  FUN_8230cb50();
  return 1;
}



// ===================================================
// 82300670  ->  FUN_82300670  (entree 82300670)
// ===================================================

undefined8 FUN_82300670(void)

{
  FUN_8230cbb0();
  return 1;
}



// ===================================================
// 82300698  ->  FUN_82300698  (entree 82300698)
// ===================================================

undefined8 FUN_82300698(void)

{
  FUN_8230b7a8();
  return 1;
}



// ===================================================
// 823006C0  ->  FUN_823006c0  (entree 823006c0)
// ===================================================

undefined8 FUN_823006c0(void)

{
  FUN_8230b7c0();
  return 1;
}



// ===================================================
// 823006E8  ->  FUN_823006e8  (entree 823006e8)
// ===================================================

undefined8 FUN_823006e8(void)

{
  FUN_82311720();
  return 1;
}



// ===================================================
// 82300710  ->  FUN_82300710  (entree 82300710)
// ===================================================

undefined8 FUN_82300710(void)

{
  FUN_82311780();
  return 1;
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



// ===================================================
// 823007D0  ->  FUN_823007d0  (entree 823007d0)
// ===================================================

undefined8 FUN_823007d0(void)

{
  char cVar4;
  int iVar3;
  undefined8 uVar1;
  undefined8 uVar2;
  longlong lVar5;
  
  cVar4 = FUN_821d0720();
  if (cVar4 == '\0') {
    lVar5 = 0;
    do {
      iVar3 = FUN_821f1b50(lVar5);
      if ((iVar3 == 1) && (cVar4 = FUN_821f1c00(lVar5), cVar4 == '\0')) {
        FUN_821f1ca8(lVar5);
        FUN_821f1ce0(lVar5,0);
        FUN_821ed240(lVar5);
      }
      lVar5 = lVar5 + 1;
    } while ((int)lVar5 < 2);
    if (DAT_82ac921c == 1) {
      uVar1 = FUN_821dc920();
      uVar2 = FUN_821dc9c0();
      FUN_821dc978(uVar1,uVar2);
      FUN_8230b540();
      FUN_822cdda0(PTR_DAT_82084200);
      uVar1 = 0x51;
    }
    else {
      FUN_8220d1a8(4);
      uVar1 = 0x4d;
    }
    FUN_8220d1e0(uVar1);
    DAT_82ac921c = 0;
  }
  return 0;
}



// ===================================================
// 823008B8  ->  FUN_823008b8  (entree 823008b8)
// ===================================================

undefined8 FUN_823008b8(void)

{
  char cVar1;
  
  cVar1 = FUN_822d0c80(0);
  if (cVar1 == '\0') {
    FUN_821df868(1);
  }
  else {
    FUN_821df868(0);
  }
  FUN_8218dea0(cVar1 == '\0');
  return 1;
}



// ===================================================
// 82300910  ->  FUN_82300910  (entree 82300910)
// ===================================================

undefined8 FUN_82300910(void)

{
  undefined8 uVar1;
  undefined8 uVar2;
  
  uVar1 = FUN_821dc920();
  uVar2 = FUN_821dc9c0();
  FUN_821dd710(uVar1,uVar2);
  FUN_821dd4f0();
  return 1;
}



// ===================================================
// 82300960  ->  FUN_82300960  (entree 82300960)
// ===================================================

undefined8 FUN_82300960(void)

{
  int iVar1;
  
  iVar1 = FUN_8233ed90();
  FUN_8232d570(iVar1 == 2,0);
  return 1;
}



// ===================================================
// 82300998  ->  FUN_82300998  (entree 82300998)
// ===================================================

undefined8 FUN_82300998(void)

{
  FUN_8232c768();
  return 1;
}



// ===================================================
// 823009C0  ->  FUN_823009c0  (entree 823009c0)
// ===================================================

undefined8 FUN_823009c0(void)

{
  FUN_823a7598();
  return 1;
}



// ===================================================
// 823009E8  ->  FUN_823009e8  (entree 823009e8)
// ===================================================

undefined8 FUN_823009e8(void)

{
  char cVar1;
  
  cVar1 = FUN_8233f608();
  if (cVar1 != '\0') {
    FUN_8220d1a8(0x14);
    FUN_8220d1e0(0x5a);
  }
  return 0;
}



// ===================================================
// 82300A28  ->  FUN_82300a28  (entree 82300a28)
// ===================================================

undefined8 FUN_82300a28(void)

{
  char cVar2;
  undefined8 uVar1;
  undefined8 uVar3;
  
  cVar2 = FUN_822d0c80(0);
  if (cVar2 == '\0') {
    cVar2 = FUN_822d0c80(1);
    if (cVar2 == '\0') goto LAB_82300a8c;
    FUN_821df868(1);
    uVar1 = FUN_821dc920();
    uVar3 = 0;
  }
  else {
    FUN_821df868(0);
    uVar1 = FUN_821dc920();
    uVar3 = 1;
  }
  FUN_821dd578(uVar1,uVar3,0,0);
LAB_82300a8c:
  FUN_8218dea0(0);
  FUN_8218dea0(1);
  return 1;
}



// ===================================================
// 82300AB0  ->  FUN_82300ab0  (entree 82300ab0)
// ===================================================

undefined8 FUN_82300ab0(void)

{
  undefined8 uVar1;
  
  uVar1 = FUN_821dc920();
  FUN_821dd710(uVar1,0);
  FUN_821dd710(uVar1,1);
  FUN_821dd4f0();
  return 1;
}



// ===================================================
// 82300AF8  ->  FUN_82300af8  (entree 82300af8)
// ===================================================

undefined8 FUN_82300af8(void)

{
  FUN_8233f1a8();
  return 1;
}



// ===================================================
// 82300B28  ->  FUN_82300b28  (entree 82300b28)
// ===================================================

undefined8 FUN_82300b28(void)

{
  FUN_8233f4b8();
  return 1;
}



// ===================================================
// 82300B50  ->  FUN_82300b50  (entree 82300b50)
// ===================================================

undefined8 FUN_82300b50(void)

{
  FUN_823401b8();
  return 1;
}



// ===================================================
// 82300B78  ->  FUN_82300b78  (entree 82300b78)
// ===================================================

undefined8 FUN_82300b78(void)

{
  FUN_823401d0();
  return 1;
}



// ===================================================
// 82300BA0  ->  FUN_82300ba0  (entree 82300ba0)
// ===================================================

undefined8 FUN_82300ba0(void)

{
  FUN_8233f5d8();
  return 1;
}



// ===================================================
// 82300BC8  ->  FUN_82300bc8  (entree 82300bc8)
// ===================================================

undefined8 FUN_82300bc8(void)

{
  char cVar1;
  
  cVar1 = FUN_8233f608();
  if (cVar1 != '\0') {
    FUN_8220d1a8(4);
    FUN_8220d1e0(0x4d);
  }
  return 0;
}



// ===================================================
// 82300C08  ->  FUN_82300c08  (entree 82300c08)
// ===================================================

undefined8 FUN_82300c08(void)

{
  char cVar1;
  
  cVar1 = FUN_8233f608();
  if (cVar1 != '\0') {
    FUN_8220d1a8(0x15);
    FUN_8220d1e0(0x5e);
  }
  return 0;
}



// ===================================================
// 82300C48  ->  FUN_82300c48  (entree 82300c48)
// ===================================================

undefined8 FUN_82300c48(void)

{
  int iVar2;
  undefined8 uVar1;
  
  iVar2 = FUN_8220d178();
  iVar2 = *(int *)(iVar2 + 0x1c);
  if (100 < iVar2) {
    if (iVar2 < 0x67) {
      DAT_82ac9223 = 0;
      goto LAB_82300cd4;
    }
    if (iVar2 == 0x67) {
      uVar1 = FUN_82321f90();
      FUN_82322408(uVar1,1);
      FUN_822c8aa0(PTR_DAT_8200f3bc,0xffffffff8208d6d4);
    }
  }
  FUN_821dff70();
  FUN_8227ee78(PTR_DAT_826539c4);
  FUN_821df868(0);
  uVar1 = FUN_821dc920();
  FUN_821dd578(uVar1,1,0,0);
  FUN_8218dea0(0);
  FUN_8218dea0(1);
  DAT_82ac9223 = 1;
LAB_82300cd4:
  FUN_82145be0(0xffffffffffffffff,0xffffffffffffffff,0xffffffffffffffff);
  return 1;
}



// ===================================================
// 82300D08  ->  FUN_82300d08  (entree 82300d08)
// ===================================================

undefined8 FUN_82300d08(void)

{
  undefined8 uVar1;
  
  if (DAT_82ac9223 != '\0') {
    uVar1 = FUN_821dc920();
    FUN_821dd710(uVar1,0);
    FUN_821dd710(uVar1,1);
    FUN_821dd4f0();
    FUN_8227e210(PTR_DAT_826539c4);
    FUN_8227d988(PTR_DAT_826539c4);
    FUN_822c7d50(PTR_DAT_8200f3bc);
    FUN_821e0bc8();
    DAT_82ac9223 = '\0';
  }
  return 1;
}



// ===================================================
// 82300D98  ->  FUN_82300d98  (entree 82300d98)
// ===================================================

bool FUN_82300d98(void)

{
  char cVar1;
  
  cVar1 = FUN_821dfff0();
  return cVar1 == '\0';
}



// ===================================================
// 82300DC8  ->  FUN_82300dc8  (entree 82300dc8)
// ===================================================

undefined8 FUN_82300dc8(void)

{
  FUN_822e1b48();
  return 0;
}



// ===================================================
// 82300DF0  ->  FUN_82300df0  (entree 82300df0)
// ===================================================

undefined8 FUN_82300df0(void)

{
  char cVar1;
  
  cVar1 = FUN_821dfff0();
  if (cVar1 != '\0') {
    return 0;
  }
  FUN_822dda38();
  return 1;
}



// ===================================================
// 82300E40  ->  FUN_82300e40  (entree 82300e40)
// ===================================================

undefined8 FUN_82300e40(void)

{
  FUN_822ddb18();
  return 1;
}



// ===================================================
// 82300E70  ->  FUN_82300e70  (entree 82300e70)
// ===================================================

undefined8 FUN_82300e70(void)

{
  int iVar2;
  undefined8 uVar1;
  
  iVar2 = FUN_822dd4c8();
  uVar1 = FUN_821576d8(iVar2 != 1);
  FUN_822c8aa0(uVar1,0xffffffff8201d730);
  FUN_822cdd90(PTR_DAT_82084200);
  return 1;
}



// ===================================================
// 82300EC0  ->  FUN_82300ec0  (entree 82300ec0)
// ===================================================

undefined8 FUN_82300ec0(void)

{
  int iVar2;
  undefined8 uVar1;
  char cVar3;
  char acStack_20 [16];
  
  iVar2 = FUN_822dd4c8();
  uVar1 = FUN_821576d8(iVar2 != 1);
  acStack_20[0] = '\0';
  FUN_822c3910(acStack_20,0);
  if (((acStack_20[0] != '\0') && (iVar2 = FUN_822d0ca8(0x200), -1 < iVar2)) ||
     (cVar3 = FUN_822c80d0(uVar1), cVar3 == '\0')) {
    FUN_8220d1a8(4);
    FUN_8220d1e0(0x4b);
  }
  return 0;
}



// ===================================================
// 82300F58  ->  FUN_82300f58  (entree 82300f58)
// ===================================================

undefined8 FUN_82300f58(void)

{
  int iVar1;
  
  iVar1 = FUN_822dd4c8();
  FUN_821576d8(iVar1 != 1);
  FUN_822c7d50();
  return 1;
}



// ===================================================
// 82300F98  ->  FUN_82300f98  (entree 82300f98)
// ===================================================

undefined8 FUN_82300f98(void)

{
  int iVar1;
  char cVar2;
  
  FUN_822daef0();
  FUN_8221d010(0xffffffff82ac9225);
  iVar1 = FUN_822d0ca8(0x200);
  if ((-1 < iVar1) || (cVar2 = FUN_8221ccb0(0xffffffff82ac9225), cVar2 == '\0')) {
    FUN_8220d1a8(4);
    FUN_8220d1e0(0x4b);
  }
  return 0;
}



// ===================================================
// 82301008  ->  FUN_82301008  (entree 82301008)
// ===================================================

undefined8 FUN_82301008(void)

{
  FUN_8221cc80(0xffffffff82ac9225);
  return 1;
}



// ===================================================
// 82301038  ->  FUN_82301038  (entree 82301038)
// ===================================================

undefined8 FUN_82301038(void)

{
  char cVar2;
  undefined8 uVar1;
  
  cVar2 = FUN_822e16c8();
  if (cVar2 == '\0') {
    FUN_8220d1a8(4);
    uVar1 = 0x4c;
  }
  else {
    uVar1 = 0x68;
  }
  FUN_8220d1e0(uVar1);
  return 0;
}



// ===================================================
// 82301088  ->  FUN_82301088  (entree 82301088)
// ===================================================

undefined8 FUN_82301088(void)

{
  char cVar1;
  
  cVar1 = FUN_822dde98();
  if (cVar1 != '\0') {
    FUN_8220d1e0(0x67);
  }
  return 0;
}



// ===================================================
// 823010C8  ->  FUN_823010c8  (entree 823010c8)
// ===================================================

undefined8 FUN_823010c8(void)

{
  int *piVar1;
  
  piVar1 = (int *)FUN_8220d178();
  if ((*piVar1 == 0x16) && ((piVar1[7] == 0x67 || (piVar1[7] == 0x68)))) {
    return 1;
  }
  return 0;
}



// ===================================================
// 82301120  ->  FUN_82301120  (entree 82301120)
// ===================================================

bool FUN_82301120(void)

{
  char cVar3;
  undefined8 uVar1;
  undefined8 uVar2;
  
  cVar3 = FUN_821dfff0();
  if (cVar3 == '\0') {
    uVar1 = FUN_82336f48();
    uVar2 = FUN_821dcd60();
    uVar1 = FUN_82336f68(uVar1);
    FUN_823370c0(uVar1,uVar2);
    FUN_8233eda0(2);
    FUN_8232d570(1,1);
  }
  return cVar3 == '\0';
}



// ===================================================
// 823011A0  ->  FUN_823011a0  (entree 823011a0)
// ===================================================

undefined8 FUN_823011a0(void)

{
  FUN_8232c768();
  FUN_8233edc8();
  return 1;
}



// ===================================================
// 823011C8  ->  FUN_823011c8  (entree 823011c8)
// ===================================================

undefined8 FUN_823011c8(void)

{
  undefined4 uVar1;
  int iVar2;
  char cVar3;
  undefined1 auStack_80 [4];
  int iStack_7c;
  int iStack_78;
  undefined1 auStack_50 [4];
  undefined4 uStack_4c;
  uint uStack_38;
  undefined1 uStack_34;
  undefined1 uStack_33;
  float fStack_28;
  float fStack_24;
  undefined4 uStack_1c;
  
  FUN_8221d938(auStack_50);
  iVar2 = FUN_822dd4c8();
  if (iVar2 == 0) {
    FUN_822979c0(auStack_80,0x10);
    uStack_34 = 1;
    fStack_28 = (float)(longlong)iStack_7c;
    fStack_24 = (float)(longlong)iStack_78;
    FUN_82141840(auStack_50,0xffffffff8201d734,0x14);
    cVar3 = FUN_82144b40();
    if (cVar3 != '\0') {
      uStack_33 = 1;
    }
    cVar3 = FUN_82144b30();
    uVar1 = DAT_82003638;
joined_r0x82301308:
    DAT_82003638 = uVar1;
    if (cVar3 != '\0') goto LAB_82301400;
  }
  else {
    iVar2 = FUN_822dd4c8();
    if (iVar2 == 3) {
      FUN_822979c0(auStack_80,0x10);
      uStack_34 = 1;
      fStack_28 = (float)(longlong)iStack_7c;
      fStack_24 = (float)(longlong)iStack_78;
      FUN_82141840(auStack_50,0xffffffff8208d70c,0x10);
      cVar3 = FUN_82144b40();
      if (cVar3 != '\0') {
        uStack_33 = 1;
      }
      cVar3 = FUN_82144b30();
      uVar1 = DAT_82003638;
      goto joined_r0x82301308;
    }
    iVar2 = FUN_822dd4c8();
    if (iVar2 == 4) {
      FUN_822979c0(auStack_80,0x10);
      uStack_34 = 1;
      fStack_28 = (float)(longlong)iStack_7c;
      fStack_24 = (float)(longlong)iStack_78;
      FUN_82141840(auStack_50,0xffffffff8208d6f4,0x14);
      cVar3 = FUN_82144b40();
      if (cVar3 != '\0') {
        uStack_33 = 1;
      }
      goto LAB_82301400;
    }
    FUN_822979c0(auStack_80,0x10);
    uStack_34 = 0;
    fStack_28 = (float)(longlong)iStack_7c;
    fStack_24 = (float)(longlong)iStack_78;
    FUN_82141840(auStack_50,0xffffffff8208d6e0,0x10);
    uVar1 = DAT_8200365c;
  }
  uStack_1c = uVar1;
LAB_82301400:
  FUN_8221df90(0xffffffff82ac9225,auStack_50);
  if (0xf < uStack_38) {
    thunk_FUN_82142f48(uStack_4c);
  }
  return 1;
}



// ===================================================
// 82301480  ->  FUN_82301480  (entree 82301480)
// ===================================================

undefined8 FUN_82301480(int param_1)

{
  char cVar1;
  
  *(undefined4 **)(param_1 + 0x154) = &DAT_82ac8510;
  cVar1 = FUN_822fa900(0xffffffff82ac8510,0xffffffff8208d72c,0,DAT_82ac8568 == 0,1);
  if (cVar1 == '\0') {
    return 0;
  }
  FUN_822e36a8(param_1,0);
  FUN_822e38d8(param_1);
  *(undefined4 *)(param_1 + 0x144) = 3;
  *(undefined1 *)(param_1 + 0x148) = 0;
  return 1;
}



// ===================================================
// 82301520  ->  FUN_82301520  (entree 82301520)
// ===================================================

undefined8 FUN_82301520(int param_1)

{
  char cVar2;
  undefined8 uVar1;
  undefined4 auStack_20 [4];
  
  FUN_822e3618(param_1,0x1da0);
  FUN_822e3660(param_1,0x1da0);
  cVar2 = FUN_82148620();
  if (cVar2 == '\0') {
    return 0;
  }
  cVar2 = FUN_822fa080(*(undefined4 *)(param_1 + 0x154));
  if (cVar2 == '\0') {
    return 0;
  }
  if (*(int *)(param_1 + 0x4c) == 3) {
    FUN_82144c28();
    cVar2 = FUN_82144cb0();
    if (cVar2 == '\0') {
      *(undefined4 *)(param_1 + 0x4c) = 2;
      goto LAB_823015a0;
    }
  }
  FUN_822e33f8(param_1);
LAB_823015a0:
  auStack_20[0] = 0x12a;
  auStack_20[1] = 299;
  auStack_20[2] = 0x12d;
  auStack_20[3] = 0x12e;
  uVar1 = FUN_82322798(auStack_20[*(int *)(param_1 + 0x4c)]);
  FUN_822e3650(param_1,uVar1);
  FUN_822e3660(param_1,3);
  return 0;
}



// ===================================================
// 82301608  ->  FUN_82301608  (entree 82301608)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_82301608(int param_1)

{
  char cVar2;
  undefined8 uVar1;
  undefined8 uVar3;
  int iVar4;
  double dVar5;
  double dVar6;
  double dVar7;
  float fStack_78;
  float fStack_74;
  float fStack_70;
  undefined4 auStack_60 [24];
  
  cVar2 = FUN_822fa080(*(undefined4 *)(param_1 + 0x154));
  if (cVar2 != '\0') {
    auStack_60[0] = 0x3ef;
    fStack_78 = DAT_82000a34;
    fStack_74 = DAT_82000a34;
    fStack_70 = DAT_82000a34;
    auStack_60[1] = 0x3f0;
    auStack_60[2] = 0x3f2;
    auStack_60[3] = 0x3f3;
    FUN_822c2a08(9);
    FUN_822faa88(*(undefined4 *)(param_1 + 0x154),&fStack_78,0xffffffff8208d730,1);
    fStack_74 = fStack_74 - DAT_82084e7c;
    FUN_8223bc10(0xe);
    FUN_8223c130(9);
    iVar4 = 0;
    dVar5 = (double)DAT_82000b08;
    dVar6 = (double)DAT_82011814;
    do {
      uVar1 = FUN_82322798(auStack_60[iVar4]);
      uVar3 = 0xffffffffffffffff;
      if (iVar4 == 3) {
        FUN_82144c28();
        cVar2 = FUN_82144cb0();
        if (cVar2 == '\0') {
          uVar3 = 0xffffffffff7f7f7f;
        }
      }
      FUN_8223c048(uVar3);
      dVar7 = (double)(float)((double)(longlong)iVar4 * dVar6);
      FUN_8223beb8((double)fStack_78,(double)(float)(dVar7 + (double)fStack_74));
      FUN_8223bf98(1);
      FUN_8223fe30(0xffffffff82000f08,uVar1);
      if (iVar4 == *(int *)(param_1 + 0x4c)) {
        FUN_822e37e0((double)fStack_78,(double)(float)(dVar7 + (double)fStack_74),dVar5,
                     param_1 + 0x158);
      }
      iVar4 = iVar4 + 1;
    } while (iVar4 < 4);
    FUN_822c2a18();
  }
  return;
}



// ===================================================
// 823017B0  ->  FUN_823017b0  (entree 823017b0)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

longlong FUN_823017b0(int param_1,undefined8 param_2)

{
  char cVar1;
  longlong lVar2;
  
  lVar2 = 1;
  if (*(int *)(param_1 + 0x4c) == 3) {
    FUN_82144c28();
    cVar1 = FUN_82144cb0();
    if (cVar1 == '\0') {
      lVar2 = 0;
    }
  }
  if (lVar2 != 0) {
    FUN_822e35b0(param_1,param_2);
  }
  return lVar2;
}



// ===================================================
// 82301810  ->  FUN_82301810  (entree 82301810)
// ===================================================

void FUN_82301810(int param_1)

{
  thunk_FUN_822d11a8();
  FUN_822fa018(*(undefined4 *)(param_1 + 0x154),0);
  FUN_8220d1e0(0x43);
  return;
}



// ===================================================
// 82301878  ->  FUN_82301878  (entree 82301878)
// ===================================================

undefined8 FUN_82301878(int param_1)

{
  char cVar1;
  char cVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  char *pcVar5;
  char *pcVar6;
  
  uVar3 = 1;
  uVar4 = 0;
  *(undefined4 **)(param_1 + 0x154) = &DAT_82ac8510;
  if (DAT_82ac8568 != (char *)0x0) {
    pcVar5 = &DAT_8208d754;
    pcVar6 = DAT_82ac8568;
    do {
      cVar2 = *pcVar6;
      cVar1 = *pcVar5;
      if (cVar2 == '\0') break;
      pcVar6 = pcVar6 + 1;
      pcVar5 = pcVar5 + 1;
    } while (cVar2 == cVar1);
    if (cVar2 == cVar1) {
      uVar3 = 0;
      uVar4 = 1;
    }
  }
  cVar2 = FUN_822fa900(0xffffffff82ac8510,0xffffffff8208d72c,0xffffffff8208d750,uVar3,uVar4);
  if (cVar2 == '\0') {
    return 0;
  }
  FUN_822e36a8(param_1,0);
  FUN_822e38d8(param_1);
  *(undefined4 *)(param_1 + 0x144) = 3;
  *(undefined1 *)(param_1 + 0x148) = 0;
  FUN_822e3618(param_1,0x1da0);
  FUN_822e3660(param_1,0x1da0);
  FUN_822e3c10(param_1 + 0x158);
  return 1;
}



// ===================================================
// 82301980  ->  FUN_82301980  (entree 82301980)
// ===================================================

undefined8 FUN_82301980(int param_1)

{
  char cVar2;
  undefined8 uVar1;
  int iVar3;
  undefined4 auStack_30 [6];
  
  cVar2 = FUN_82148620();
  if (cVar2 == '\0') {
    return 0;
  }
  iVar3 = param_1 + 0x158;
  cVar2 = FUN_822c7b98(iVar3);
  if (cVar2 != '\0') {
    FUN_82144c28();
    cVar2 = FUN_82144cb0();
    if (cVar2 != '\0') {
      return 0;
    }
    FUN_822c7d50(iVar3);
    return 0;
  }
  uVar1 = FUN_822e2e38(iVar3);
  if ((int)uVar1 == 0) {
    FUN_822db8f8(uVar1,0,0xffffffffffffffff);
    FUN_822e3c10(iVar3);
    return 0;
  }
  FUN_822e3618(param_1,0x1da0);
  FUN_822e3660(param_1,0x1da0);
  cVar2 = FUN_822fa080(*(undefined4 *)(param_1 + 0x154));
  if (cVar2 == '\0') {
    return 0;
  }
  auStack_30[0] = 0x151;
  auStack_30[1] = 0x152;
  auStack_30[2] = 0x154;
  auStack_30[3] = 0x155;
  if (*(int *)(param_1 + 0x4c) != 2) {
    FUN_82144c28();
    cVar2 = FUN_82144cb0();
    if (cVar2 == '\0') {
      *(undefined4 *)(param_1 + 0x4c) = 2;
      goto LAB_82301a88;
    }
  }
  FUN_822e33f8(param_1);
LAB_82301a88:
  FUN_822e3618(param_1,auStack_30[*(int *)(param_1 + 0x4c)]);
  FUN_822e3660(param_1,3);
  return 0;
}



// ===================================================
// 82301AC8  ->  FUN_82301ac8  (entree 82301ac8)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

void FUN_82301ac8(int param_1)

{
  char cVar2;
  undefined8 uVar1;
  undefined4 *puVar3;
  undefined8 uVar4;
  int iVar5;
  double dVar6;
  double dVar7;
  double dVar8;
  float fStack_88;
  float fStack_84;
  float fStack_80;
  undefined4 uStack_70;
  undefined4 uStack_6c;
  undefined4 uStack_68;
  undefined4 uStack_64;
  
  cVar2 = FUN_822fa080(*(undefined4 *)(param_1 + 0x154));
  if (cVar2 != '\0') {
    uStack_70 = 0x53c;
    fStack_88 = DAT_82000a34;
    fStack_84 = DAT_82000a34;
    fStack_80 = DAT_82000a34;
    uStack_6c = 0x53d;
    uStack_68 = 0x53e;
    uStack_64 = 0x540;
    FUN_822c2a08(9);
    FUN_8223bc10(0xe);
    FUN_8223c130(9);
    FUN_822faa88(*(undefined4 *)(param_1 + 0x154),&fStack_88,0xffffffff8208d76c,1);
    FUN_8223beb8((double)fStack_88,(double)fStack_84);
    FUN_8223c048(0xffffffffffbff560);
    uVar1 = FUN_82322798(0x53b);
    FUN_8223fe30(0xffffffff8208476c,uVar1);
    FUN_8223c048(0xffffffffffffffff);
    FUN_822faa88(*(undefined4 *)(param_1 + 0x154),&fStack_88,0xffffffff8208d758,1);
    iVar5 = 0;
    puVar3 = &uStack_70;
    fStack_84 = fStack_84 - DAT_82084e7c;
    dVar6 = (double)DAT_82000b08;
    dVar7 = (double)DAT_82011814;
    do {
      uVar1 = FUN_82322798(*puVar3);
      uVar4 = 0xffffffffffffffff;
      if (iVar5 != 2) {
        FUN_82144c28();
        cVar2 = FUN_82144cb0();
        if (cVar2 == '\0') {
          uVar4 = 0xffffffffff7f7f7f;
        }
      }
      FUN_8223c048(uVar4);
      dVar8 = (double)(float)((double)(longlong)iVar5 * dVar7);
      FUN_8223beb8((double)fStack_88,(double)(float)(dVar8 + (double)fStack_84));
      FUN_8223bf98(1);
      FUN_8223fe30(0xffffffff82000f08,uVar1);
      if (iVar5 == *(int *)(param_1 + 0x4c)) {
        FUN_822e37e0((double)fStack_88,(double)(float)(dVar8 + (double)fStack_84),dVar6,
                     param_1 + 0x250);
      }
      iVar5 = iVar5 + 1;
      puVar3 = puVar3 + 1;
    } while (iVar5 < 4);
    FUN_822c2a18();
  }
  return;
}



// ===================================================
// 82301CC8  ->  FUN_82301cc8  (entree 82301cc8)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

longlong FUN_82301cc8(int param_1,undefined8 param_2)

{
  char cVar1;
  longlong lVar2;
  
  lVar2 = 1;
  if (*(int *)(param_1 + 0x4c) != 2) {
    FUN_82144c28();
    cVar1 = FUN_82144cb0();
    if (cVar1 == '\0') {
      lVar2 = 0;
    }
  }
  if (lVar2 != 0) {
    FUN_822e35b0(param_1,param_2);
  }
  return lVar2;
}



// ===================================================
// 82301D28  ->  FUN_82301d28  (entree 82301d28)
// ===================================================

void FUN_82301d28(int param_1)

{
  thunk_FUN_822d11a8();
  FUN_822fa018(*(undefined4 *)(param_1 + 0x154),0);
  FUN_8220d1e0(0x6d);
  return;
}



// ===================================================
// 82301D68  ->  FUN_82301d68  (entree 82301d68)
// ===================================================

void FUN_82301d68(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  
  FUN_822e35e0();
  switch(*(undefined4 *)(param_1 + 0x4c)) {
  case 0:
    FUN_822db258(0,0xffffffffffffffff);
    break;
  case 1:
    iVar2 = param_1 + 0x158;
    FUN_822e3c10(iVar2);
    FUN_822c8aa0(iVar2,0xffffffff82085024);
    FUN_822e2e28(iVar2,1);
    uVar1 = FUN_82322798(0x59d);
    *(undefined4 *)(param_1 + 0x1b8) = uVar1;
    break;
  case 2:
    FUN_8220d1e0(0x73);
    break;
  case 3:
    FUN_822db480();
  }
  return;
}



// ===================================================
// 82301E28  ->  FUN_82301e28  (entree 82301e28)
// ===================================================

void FUN_82301e28(void)

{
  FUN_823a7598();
  FUN_821586c8();
  FUN_822c8aa0(0xffffffff82ac95e4,0xffffffff8208d77c);
  return;
}



// ===================================================
// 82301E60  ->  FUN_82301e60  (entree 82301e60)
// ===================================================

void FUN_82301e60(void)

{
  FUN_821586e0();
  FUN_822c7d50(0xffffffff82ac95e4);
  return;
}



// ===================================================
// 82301E90  ->  FUN_82301e90  (entree 82301e90)
// ===================================================

undefined8 FUN_82301e90(int param_1)

{
  char cVar1;
  
  cVar1 = FUN_82158700();
  if (cVar1 == '\0') {
    return 0;
  }
  FUN_822e3698(param_1,0);
  FUN_822e36a0(param_1,1);
  FUN_822e38d8(param_1);
  FUN_822e3618(param_1,0x1da0);
  FUN_822e3c10(param_1 + 0x154);
  *(undefined1 *)(param_1 + 0x24c) = 0;
  return 1;
}



// ===================================================
// 82301F20  ->  FUN_82301f20  (entree 82301f20)
// ===================================================

void FUN_82301f20(int param_1)

{
  thunk_FUN_822d11a8();
  if (*(char *)(param_1 + 0x24c) != '\0') {
    FUN_822db258(1,0xffffffffffffffff);
  }
  FUN_8220d1e0(0x6d);
  return;
}



// ===================================================
// 82301F70  ->  FUN_82301f70  (entree 82301f70)
// ===================================================

void FUN_82301f70(int param_1)

{
  undefined8 uVar1;
  
  FUN_822e35e0();
  switch(*(undefined4 *)(param_1 + 0x4c)) {
  case 0:
    uVar1 = 0x6e;
    break;
  case 1:
    uVar1 = 0x6f;
    break;
  case 2:
    uVar1 = 0x71;
    break;
  case 3:
    uVar1 = 0x72;
    DAT_82ac93d4 = 0;
    break;
  default:
    goto switchD_82301fa8_default;
  }
  FUN_8220d1e0(uVar1);
switchD_82301fa8_default:
  return;
}



// ===================================================
// 82302000  ->  FUN_82302000  (entree 82302000)
// ===================================================

undefined8 FUN_82302000(int param_1)

{
  char cVar4;
  int iVar2;
  ulonglong uVar1;
  undefined4 uVar3;
  int iVar5;
  
  FUN_822e3660(param_1,0x1da0);
  iVar5 = param_1 + 0x154;
  cVar4 = FUN_822c7b98(iVar5);
  if (cVar4 == '\0') {
    iVar2 = FUN_822e2e38(iVar5);
    if (-1 < iVar2) {
      iVar2 = FUN_822e2e38(iVar5);
      if ((iVar2 == 0) && (uVar1 = FUN_82188ea8(), (uVar1 & 0xffffffff) != 0)) {
        FUN_8218a3c8(uVar1 + 0x4770);
        *(undefined1 *)(param_1 + 0x24c) = 1;
      }
      FUN_822e3c10(iVar5);
    }
    FUN_82158758(0);
    FUN_822e33f8(param_1);
    iVar2 = FUN_822d0ca8(0x100);
    if (-1 < iVar2) {
      FUN_822e3c10(iVar5);
      FUN_822c8aa0(iVar5,0xffffffff82085024);
      FUN_822e2e28(iVar5,1);
      uVar3 = FUN_82322798(0x603);
      *(undefined4 *)(param_1 + 0x1b4) = uVar3;
      FUN_82158758(1);
    }
  }
  FUN_822e3660(param_1,0x18);
  return 0;
}



// ===================================================
// 82302100  ->  FUN_82302100  (entree 82302100)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

int FUN_82302100(int param_1,ulonglong param_2)

{
  FUN_82154d98(param_1 + 0x154);
  FUN_822c73a8(param_1 + 0xdc);
  if (*(int *)(param_1 + 200) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 200) = 0;
  *(undefined4 *)(param_1 + 0xcc) = 0;
  *(undefined4 *)(param_1 + 0xd0) = 0;
  FUN_822c73a8(param_1 + 0x58);
  FUN_822c73a8(param_1);
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 82302180  ->  FUN_82302180  (entree 82302180)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

int FUN_82302180(int param_1,ulonglong param_2)

{
  FUN_82154d98(param_1 + 0x158);
  FUN_822c73a8(param_1 + 0xdc);
  if (*(int *)(param_1 + 200) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 200) = 0;
  *(undefined4 *)(param_1 + 0xcc) = 0;
  *(undefined4 *)(param_1 + 0xd0) = 0;
  FUN_822c73a8(param_1 + 0x58);
  FUN_822c73a8(param_1);
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 82302228  ->  FUN_82302228  (entree 82302228)
// ===================================================

undefined8 FUN_82302228(int *param_1)

{
  int iVar1;
  int *piVar2;
  
  FUN_822e36a8(param_1,0);
  FUN_822e38d8(param_1);
  piVar2 = (int *)FUN_822db050();
  iVar1 = *piVar2;
  param_1[0x55] = iVar1;
  param_1[0x56] = iVar1;
  param_1[0x51] = 1;
  *(undefined1 *)(param_1 + 0x52) = 0;
  param_1[0x13] = 0;
  FUN_822e3208(param_1 + 0x98);
  (**(code **)(*param_1 + 0x18))(param_1,0);
  param_1[0x57] = (int)&DAT_82ac8510;
  FUN_822fa900(0xffffffff82ac8510,0xffffffff8208d72c,0xffffffff8208d754,1,0);
  FUN_822e3c10(param_1 + 0x58);
  return 1;
}



// ===================================================
// 823022E0  ->  FUN_823022e0  (entree 823022e0)
// ===================================================

undefined8 FUN_823022e0(int param_1)

{
  char cVar2;
  int iVar1;
  undefined4 auStack_30 [6];
  
  cVar2 = FUN_822c7b98(param_1 + 0x160);
  if (cVar2 == '\0') {
    iVar1 = FUN_822e2e38(param_1 + 0x160);
    if (iVar1 == 0) {
      FUN_8220d1e0(0x72);
    }
    else {
      cVar2 = FUN_822fa080(*(undefined4 *)(param_1 + 0x15c));
      if (cVar2 != '\0') {
        FUN_822e33f8(param_1);
      }
    }
  }
  auStack_30[0] = 0x156;
  auStack_30[1] = 0x157;
  auStack_30[2] = 4;
  auStack_30[3] = 2;
  FUN_822e3618(param_1,auStack_30[*(int *)(param_1 + 0x4c)]);
  FUN_822e3660(param_1,auStack_30[*(int *)(param_1 + 0x4c) + 2]);
  return 0;
}



// ===================================================
// 823023B8  ->  FUN_823023b8  (entree 823023b8)
// ===================================================

undefined8 FUN_823023b8(int param_1)

{
  FUN_822e3968();
  FUN_822fa018(*(undefined4 *)(param_1 + 0x15c),0);
  FUN_822e3228(param_1 + 0x260);
  return 1;
}



// ===================================================
// 82302400  ->  FUN_82302400  (entree 82302400)
// ===================================================

/* WARNING: Function: __savegprlr_23 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_23 replaced with injection: x360_restgprlr */

void FUN_82302400(void)

{
  int iVar2;
  char cVar3;
  undefined8 uVar1;
  ulonglong uVar4;
  int iVar5;
  double dVar6;
  double dVar7;
  double dVar8;
  double dVar9;
  double dVar10;
  uint auStack_90 [2];
  float fStack_88;
  float fStack_84;
  float fStack_80;
  
  iVar2 = FUN_826018c4();
  cVar3 = FUN_822fa080(*(undefined4 *)(iVar2 + 0x15c));
  if (cVar3 != '\0') {
    dVar6 = (double)DAT_82000a34;
    fStack_88 = DAT_82000a34;
    fStack_84 = DAT_82000a34;
    fStack_80 = DAT_82000a34;
    auStack_90[0] = 0x542;
    auStack_90[1] = 0x546;
    FUN_822c2a08(9);
    FUN_8223bc10(0xe);
    FUN_8223c130(9);
    FUN_822faa88(*(undefined4 *)(iVar2 + 0x15c),&fStack_88,0xffffffff8208d840,1);
    FUN_8223beb8((double)fStack_88,(double)fStack_84);
    FUN_8223c048(0xffffffffffbff560);
    uVar1 = FUN_82322798(0x541);
    FUN_8223fe30(0xffffffff8208476c,uVar1);
    FUN_8223c048(0xffffffffffffffff);
    dVar7 = (double)FUN_822e4a08(iVar2);
    FUN_822faa88(*(undefined4 *)(iVar2 + 0x15c),&fStack_88,0xffffffff8208d830,0);
    dVar10 = (double)DAT_82000f1c;
    dVar9 = (double)DAT_82010304;
    iVar5 = 0;
    dVar8 = (double)DAT_82000b08;
    do {
      if (iVar5 == 1) {
        FUN_822faa88(*(undefined4 *)(iVar2 + 0x15c),&fStack_88,0xffffffff8208d820,0);
      }
      FUN_8223beb8((double)fStack_88,(double)fStack_84);
      uVar4 = (ulonglong)auStack_90[iVar5];
      if (iVar5 < 1) {
        uVar1 = FUN_82322798(uVar4);
        FUN_8223fe30(0xffffffff82000f08,uVar1);
        uVar1 = FUN_82322798(*(uint *)((iVar5 + 0x55) * 4 + iVar2) + uVar4 + 1);
        if (iVar5 == *(int *)(iVar2 + 0x4c)) {
          FUN_82322798(uVar4);
          FUN_822e37e0((double)fStack_88,(double)fStack_84,dVar8,iVar2 + 600);
          dVar6 = (double)fStack_84;
        }
        FUN_8223beb8((double)(float)(dVar7 - dVar9),(double)fStack_84);
        FUN_8223fe30(0xffffffff820117f8,uVar1);
      }
      else {
        uVar1 = FUN_82322798(uVar4);
        FUN_8223fe30(0xffffffff8208476c,uVar1);
        if (iVar5 == *(int *)(iVar2 + 0x4c)) {
          FUN_82322798(uVar4);
          FUN_822e37e0((double)fStack_88,(double)fStack_84,dVar8,iVar2 + 600);
        }
      }
      iVar5 = iVar5 + 1;
      fStack_84 = (float)((double)fStack_84 + dVar10);
    } while (iVar5 < 2);
    if (*(int *)(iVar2 + 0x4c) < 1) {
      FUN_822e5380((double)(float)(dVar7 - dVar9),dVar6);
      FUN_822c2a18();
      FUN_82601910();
      return;
    }
    FUN_822e3228(iVar2 + 0x260);
    FUN_822c2a18();
  }
  FUN_82601910();
  return;
}



// ===================================================
// 823026B0  ->  FUN_823026b0  (entree 823026b0)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_823026b0(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  int aiStack_30 [12];
  
  aiStack_30[0] = 1;
  if (param_2 != 0) {
    FUN_822e35b0();
    FUN_822e3228(param_1 + 0x260);
  }
  iVar1 = *(int *)(param_1 + 0x4c);
  if (iVar1 < 1) {
    iVar2 = aiStack_30[iVar1];
    *(undefined4 *)(param_1 + 0x50) = *(undefined4 *)((iVar1 + 0x55) * 4 + param_1);
    *(int *)(param_1 + 0x14c) = iVar2;
  }
  else {
    *(undefined4 *)(param_1 + 0x14c) = 0;
  }
  *(undefined1 *)(param_1 + 0x150) = 0;
  FUN_822e32b8(param_1 + 0x260,0xffffffffffffffff,0 < *(int *)(param_1 + 0x50));
  FUN_822e32b8(param_1 + 0x260,1,*(int *)(param_1 + 0x50) < aiStack_30[*(int *)(param_1 + 0x4c)]);
  return 1;
}



// ===================================================
// 82302778  ->  FUN_82302778  (entree 82302778)
// ===================================================

undefined8 FUN_82302778(int *param_1,undefined8 param_2)

{
  FUN_822e35b0();
  if (param_1[0x13] < 1) {
    param_1[param_1[0x13] + 0x55] = param_1[0x14];
    FUN_821ccba8(param_1 + 0x98,param_2);
    (**(code **)(*param_1 + 0x18))(param_1,0);
  }
  return 1;
}



// ===================================================
// 823027F8  ->  FUN_823027f8  (entree 823027f8)
// ===================================================

void FUN_823027f8(int param_1)

{
  byte bVar1;
  byte bVar2;
  undefined4 uVar3;
  byte *pbVar4;
  byte *pbVar5;
  int iVar6;
  
  thunk_FUN_822d11a8();
  pbVar5 = (byte *)(param_1 + 0x154);
  pbVar4 = (byte *)(param_1 + 0x158);
  do {
    bVar1 = *pbVar5;
    bVar2 = *pbVar4;
    if ((ulonglong)bVar1 - (ulonglong)bVar2 != 0) break;
    pbVar5 = pbVar5 + 1;
    pbVar4 = pbVar4 + 1;
  } while (pbVar5 != (byte *)(param_1 + 0x158));
  if ((int)((ulonglong)bVar1 - (ulonglong)bVar2) == 0) {
    FUN_8220d1e0(0x72);
  }
  else {
    iVar6 = param_1 + 0x160;
    FUN_822e3c10(iVar6);
    FUN_822c8aa0(iVar6,0xffffffff82085024);
    FUN_822e2e28(iVar6,1);
    uVar3 = FUN_82322798(0x5ff);
    *(undefined4 *)(param_1 + 0x1c0) = uVar3;
  }
  return;
}



// ===================================================
// 823028A0  ->  FUN_823028a0  (entree 823028a0)
// ===================================================

void FUN_823028a0(int param_1)

{
  byte bVar1;
  byte bVar2;
  byte *pbVar3;
  byte *pbVar4;
  
  if (*(int *)(param_1 + 0x4c) == 1) {
    FUN_822e35e0();
    pbVar4 = (byte *)(param_1 + 0x154);
    FUN_822db068(pbVar4);
    pbVar3 = (byte *)(param_1 + 0x158);
    do {
      bVar1 = *pbVar4;
      bVar2 = *pbVar3;
      if ((ulonglong)bVar1 - (ulonglong)bVar2 != 0) break;
      pbVar4 = pbVar4 + 1;
      pbVar3 = pbVar3 + 1;
    } while (pbVar4 != (byte *)(param_1 + 0x158));
    if ((int)((ulonglong)bVar1 - (ulonglong)bVar2) != 0) {
      FUN_822db258(1,0xffffffffffffffff);
    }
    FUN_8220d1e0(0x72);
  }
  return;
}



// ===================================================
// 82302938  ->  FUN_82302938  (entree 82302938)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

int FUN_82302938(int param_1,ulonglong param_2)

{
  FUN_82154d98(param_1 + 0x160);
  FUN_822c73a8(param_1 + 0xdc);
  if (*(int *)(param_1 + 200) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 200) = 0;
  *(undefined4 *)(param_1 + 0xcc) = 0;
  *(undefined4 *)(param_1 + 0xd0) = 0;
  FUN_822c73a8(param_1 + 0x58);
  FUN_822c73a8(param_1);
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 823029E8  ->  FUN_823029e8  (entree 823029e8)
// ===================================================

undefined8 FUN_823029e8(int param_1)

{
  char cVar1;
  
  if ((*(char *)(param_1 + 0x54) == '\0') && (cVar1 = FUN_822e2dd8(param_1 + 0x180), cVar1 != '\0'))
  {
    FUN_822d0c30(*(undefined4 *)(param_1 + 0x178));
    FUN_822e33f8(param_1);
  }
  FUN_822e4d70(param_1 + 0x180);
  return 0;
}



// ===================================================
// 82302A50  ->  FUN_82302a50  (entree 82302a50)
// ===================================================

bool FUN_82302a50(longlong param_1)

{
  char cVar1;
  longlong lVar2;
  
  lVar2 = param_1 + 0x180;
  FUN_822e37b8(lVar2);
  cVar1 = FUN_822e2df0(lVar2);
  if (cVar1 != '\0') {
    FUN_822e3968(param_1);
    FUN_822e3b78(lVar2);
    FUN_822e3228(param_1 + 0x1b4);
  }
  else {
    FUN_822e4d70(lVar2);
  }
  return cVar1 != '\0';
}



// ===================================================
// 82302AD0  ->  FUN_82302ad0  (entree 82302ad0)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82302ad0(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  
  *(undefined1 *)(param_1 + 0x17c) = 1;
  FUN_822e35b0();
  iVar3 = param_1 + 0x1b4;
  FUN_822e3228(iVar3);
  iVar1 = *(int *)(param_1 + 0x4c);
  if (iVar1 < 8) {
    uVar2 = *(undefined4 *)((iVar1 + 0x55) * 4 + param_1);
    *(undefined4 *)(param_1 + 0x14c) = 7;
    *(undefined1 *)(param_1 + 0x150) = 1;
    *(undefined4 *)(param_1 + 0x50) = uVar2;
    FUN_822e32b8(iVar3,0xffffffffffffffff,1);
    FUN_822e32b8(iVar3,1,1);
    return 1;
  }
  if (iVar1 == 8) {
    *(undefined4 *)(param_1 + 0x14c) = 1;
    *(undefined1 *)(param_1 + 0x150) = 0;
    *(int *)(param_1 + 0x50) = *(int *)(param_1 + 0x174);
    FUN_822e32b8(iVar3,0xffffffffffffffff,*(int *)(param_1 + 0x174) != 0);
    FUN_822e32b8(iVar3,1,*(int *)(param_1 + 0x174) == 0);
    return 1;
  }
  *(undefined4 *)(param_1 + 0x14c) = 0;
  *(undefined1 *)(param_1 + 0x150) = 0;
  return 1;
}



// ===================================================
// 82302BB8  ->  FUN_82302bb8  (entree 82302bb8)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82302bb8(int param_1,undefined8 param_2)

{
  int iVar1;
  
  FUN_822e35b0();
  iVar1 = *(int *)(param_1 + 0x4c);
  if (iVar1 < 8) {
    *(undefined4 *)((iVar1 + 0x55) * 4 + param_1) = *(undefined4 *)(param_1 + 0x50);
    FUN_821ccba8(param_1 + 0x1b4,param_2);
    return 1;
  }
  if (iVar1 == 8) {
    iVar1 = param_1 + 0x1b4;
    *(undefined4 *)(param_1 + 0x174) = *(undefined4 *)(param_1 + 0x50);
    FUN_821ccba8(iVar1,param_2);
    FUN_822e32b8(iVar1,0xffffffffffffffff,*(int *)(param_1 + 0x174) != 0);
    FUN_822e32b8(iVar1,1,*(int *)(param_1 + 0x174) == 0);
  }
  return 1;
}



// ===================================================
// 82302CF8  ->  FUN_82302cf8  (entree 82302cf8)
// ===================================================

void FUN_82302cf8(undefined8 param_1,undefined2 *param_2,int *param_3)

{
  undefined2 auStack_20 [12];
  
  auStack_20[0] = 99;
  auStack_20[1] = 7;
  auStack_20[2] = 8;
  auStack_20[3] = 9;
  auStack_20[4] = 100;
  auStack_20[5] = 0x66;
  auStack_20[6] = 0x65;
  auStack_20[7] = 0x67;
  *param_2 = auStack_20[*param_3];
  param_2[1] = auStack_20[param_3[1]];
  param_2[2] = auStack_20[param_3[2]];
  param_2[3] = auStack_20[param_3[3]];
  param_2[4] = auStack_20[param_3[4]];
  param_2[5] = auStack_20[param_3[5]];
  param_2[6] = auStack_20[param_3[6]];
  param_2[7] = auStack_20[param_3[7]];
  return;
}



// ===================================================
// 82302DE8  ->  FUN_82302de8  (entree 82302de8)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82302de8(int param_1)

{
  int iVar1;
  char cVar2;
  int iVar3;
  
  iVar1 = FUN_822db088(*(undefined4 *)(param_1 + 0x178));
  FUN_822e36a8(param_1,0);
  FUN_822e38d8(param_1);
  FUN_82302c60(param_1,param_1 + 0x154,iVar1);
  iVar3 = param_1 + 0x180;
  *(undefined4 *)(param_1 + 0x174) = *(undefined4 *)(iVar1 + 0x10);
  *(undefined1 *)(param_1 + 0x148) = 0;
  *(undefined4 *)(param_1 + 0x144) = 10;
  *(undefined4 *)(param_1 + 0x4c) = 10;
  *(undefined1 *)(param_1 + 0x54) = 0;
  *(undefined1 *)(param_1 + 0x17c) = 0;
  *(undefined1 *)(param_1 + 0x17d) = 0;
  *(undefined1 *)(param_1 + 0x17e) = 0;
  FUN_822e3ad8(iVar3);
  FUN_822e3778(iVar3,(*(int *)(param_1 + 0x178) != 0) + '\x10',0);
  cVar2 = FUN_822c80d0(0xffffffff82ac8510);
  FUN_822e2e00(iVar3,cVar2 == '\0');
  FUN_822e3208(param_1 + 0x1b4);
  return 1;
}



// ===================================================
// 82302EB8  ->  FUN_82302eb8  (entree 82302eb8)
// ===================================================

void FUN_82302eb8(int param_1)

{
  undefined1 uVar1;
  undefined1 auStack_30 [16];
  undefined4 uStack_20;
  
  if (*(char *)(param_1 + 0x54) == '\0') {
    if (*(int *)(param_1 + 0x4c) == 10) {
      FUN_822d1198();
      FUN_82302cf8(param_1,auStack_30,param_1 + 0x154);
      uStack_20 = *(undefined4 *)(param_1 + 0x174);
      if (*(char *)(param_1 + 0x17d) == '\0') {
        uVar1 = FUN_822db0c0(*(undefined4 *)(param_1 + 0x178),auStack_30);
        *(undefined1 *)(param_1 + 0x17d) = uVar1;
      }
      *(undefined1 *)(param_1 + 0x54) = 1;
    }
    else if (*(int *)(param_1 + 0x4c) == 9) {
      FUN_822d1198();
      FUN_822d1148(auStack_30);
      uStack_20 = 1;
      FUN_82302c60(param_1,param_1 + 0x154,auStack_30);
      *(undefined4 *)(param_1 + 0x174) = 1;
    }
  }
  return;
}



// ===================================================
// 82302F78  ->  FUN_82302f78  (entree 82302f78)
// ===================================================

/* WARNING: Function: __savegprlr_22 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_22 replaced with injection: x360_restgprlr */

void FUN_82302f78(int param_1)

{
  char cVar4;
  undefined8 uVar1;
  undefined8 uVar2;
  longlong lVar3;
  int iVar5;
  uint *puVar6;
  undefined4 *puVar7;
  int iVar8;
  int iVar9;
  double dVar10;
  double dVar11;
  double dVar12;
  float fStack_e0;
  float fStack_dc;
  float fStack_d8;
  float fStack_d0;
  float fStack_cc;
  float fStack_c8;
  undefined1 auStack_c0 [32];
  undefined4 auStack_a0 [40];
  
  iVar5 = param_1 + 0x180;
  cVar4 = FUN_822e2dd8(iVar5);
  if (cVar4 != '\0') {
    auStack_a0[0] = 0x448;
    auStack_a0[1] = 0x449;
    dVar10 = (double)DAT_82000a34;
    fStack_e0 = DAT_82000a34;
    fStack_dc = DAT_82000a34;
    fStack_d8 = DAT_82000a34;
    fStack_d0 = DAT_82000a34;
    auStack_a0[2] = 1099;
    fStack_cc = DAT_82000a34;
    fStack_c8 = DAT_82000a34;
    auStack_a0[3] = 0x44a;
    auStack_a0[4] = 0x44c;
    auStack_a0[5] = 0x44d;
    auStack_a0[6] = 0x44f;
    auStack_a0[7] = 0x450;
    auStack_a0[8] = 0x45d;
    auStack_a0[9] = 0x444;
    auStack_a0[10] = 0x461;
    dVar11 = dVar10;
    uVar1 = FUN_822c29e8();
    FUN_822c29d8(2);
    FUN_822c2a08(9);
    FUN_8223bc10(0xe);
    FUN_8223c130(9);
    FUN_8223c048(0xffffffffffffffff);
    FUN_82249520(auStack_c0,0x20,0xffffffff8208d8a4,(-(*(int *)(param_1 + 0x178) != 0) & 2U) + 2);
    FUN_822e39c0(iVar5,&fStack_e0,auStack_c0,1);
    FUN_82249520(auStack_c0,0x20,0xffffffff8208d8a4,(-(*(int *)(param_1 + 0x178) != 0) & 2U) + 3);
    FUN_822e39c0(iVar5,&fStack_d0,auStack_c0,0);
    puVar7 = auStack_a0;
    puVar6 = (uint *)(param_1 + 0x154);
    dVar12 = (double)DAT_82011308;
    iVar9 = 0;
    do {
      iVar8 = iVar9;
      FUN_8223beb8((double)fStack_e0,(double)fStack_dc);
      uVar2 = FUN_82322798(*puVar7);
      FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar2);
      FUN_8223beb8((double)fStack_d0,(double)fStack_cc);
      uVar2 = FUN_82322798((ulonglong)*puVar6 + 0x452);
      FUN_8223fe30(0xffffffff82085944,0xffffffff82000f88,uVar2);
      if (iVar8 == *(int *)(param_1 + 0x4c)) {
        dVar11 = (double)fStack_d0;
        dVar10 = (double)fStack_cc;
      }
      iVar9 = iVar8 + 1;
      fStack_dc = (float)((double)fStack_dc + dVar12);
      puVar7 = puVar7 + 1;
      fStack_cc = (float)((double)fStack_cc + dVar12);
      puVar6 = puVar6 + 1;
    } while (iVar9 < 4);
    FUN_82249520(auStack_c0,0x20,0xffffffff8208d8a4,(-(*(int *)(param_1 + 0x178) != 0) & 2U) + 6);
    FUN_822e39c0(iVar5,&fStack_e0,auStack_c0,0);
    FUN_82249520(auStack_c0,0x20,0xffffffff8208d8a4,(-(*(int *)(param_1 + 0x178) != 0) & 2U) + 7);
    FUN_822e39c0(iVar5,&fStack_d0,auStack_c0,0);
    if (iVar9 < 9) {
      puVar7 = auStack_a0 + iVar9;
      puVar6 = (uint *)((iVar8 + 0x56) * 4 + param_1);
      do {
        FUN_8223beb8((double)fStack_e0,(double)fStack_dc);
        uVar2 = FUN_82322798(*puVar7);
        FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar2);
        FUN_8223beb8((double)fStack_d0,(double)fStack_cc);
        if (iVar9 < 8) {
          lVar3 = (ulonglong)*puVar6 + 0x452;
        }
        else {
          lVar3 = (ulonglong)(*(int *)(param_1 + 0x174) == 0) + 0x45e;
        }
        uVar2 = FUN_82322798(lVar3);
        FUN_8223fe30(0xffffffff82085944,0xffffffff82000f88,uVar2);
        if (iVar9 == *(int *)(param_1 + 0x4c)) {
          dVar11 = (double)fStack_d0;
          dVar10 = (double)fStack_cc;
        }
        iVar9 = iVar9 + 1;
        fStack_dc = (float)((double)fStack_dc + dVar12);
        puVar7 = puVar7 + 1;
        fStack_cc = (float)((double)fStack_cc + dVar12);
        puVar6 = puVar6 + 1;
      } while (iVar9 < 9);
    }
    FUN_82249520(auStack_c0,0x20,0xffffffff8208d894,(*(int *)(param_1 + 0x178) != 0) + '\n');
    FUN_822e39c0(iVar5,&fStack_e0,auStack_c0,0);
    dVar12 = (double)DAT_82000f1c;
    FUN_8223beb8((double)fStack_e0,(double)(float)((double)fStack_dc - dVar12));
    if (iVar9 == *(int *)(param_1 + 0x4c)) {
      dVar11 = (double)fStack_e0;
      dVar10 = (double)(float)((double)fStack_dc - dVar12);
    }
    uVar2 = FUN_82322798(auStack_a0[iVar9]);
    FUN_8223fe30(0xffffffff82085944,0xffffffff82000f88,uVar2);
    if (iVar9 + 1 == *(int *)(param_1 + 0x4c)) {
      dVar11 = (double)fStack_e0;
      dVar10 = (double)fStack_dc;
    }
    uVar2 = FUN_82322798(auStack_a0[iVar9 + 1]);
    FUN_8223fe30(0xffffffff82085944,0xffffffff82000f88,uVar2);
    if (*(char *)(param_1 + 0x17e) == '\0') {
      FUN_822e3228(param_1 + 0x1b4);
    }
    else {
      iVar5 = *(int *)(param_1 + 0x4c);
      if (iVar5 < 8) {
        FUN_82322798((ulonglong)*(uint *)((iVar5 + 0x55) * 4 + param_1) + 0x452);
        FUN_822e5380(dVar11,dVar10,param_1 + 0x1b4);
      }
      else if (iVar5 < 9) {
        FUN_82322798((ulonglong)(*(int *)(param_1 + 0x174) == 0) + 0x45e);
        FUN_822e5380(dVar11,dVar10,param_1 + 0x1b4);
      }
      else {
        FUN_822e3228(param_1 + 0x1b4);
        dVar12 = (double)DAT_82000b08;
        FUN_82322798(auStack_a0[*(int *)(param_1 + 0x4c)]);
        FUN_822e37e0(dVar11,dVar10,dVar12,param_1 + 0x1ac);
      }
    }
    *(undefined1 *)(param_1 + 0x17e) = 0;
    FUN_822c2a18();
    FUN_822c29d8(uVar1);
  }
  return;
}



// ===================================================
// 823034A8  ->  FUN_823034a8  (entree 823034a8)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_823034a8(int param_1)

{
  if (*(int *)(param_1 + 0x1a0) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 0x1a0) = 0;
  *(undefined4 *)(param_1 + 0x1a4) = 0;
  *(undefined4 *)(param_1 + 0x1a8) = 0;
  FUN_822c73a8(param_1 + 0xdc);
  if (*(int *)(param_1 + 200) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 200) = 0;
  *(undefined4 *)(param_1 + 0xcc) = 0;
  *(undefined4 *)(param_1 + 0xd0) = 0;
  FUN_822c73a8(param_1 + 0x58);
  FUN_822c73a8(param_1);
  return;
}



// ===================================================
// 82303520  ->  FUN_82303520  (entree 82303520)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

void FUN_82303520(int param_1)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  int *piVar4;
  
  iVar1 = 1;
  iVar2 = param_1 + 0x4f4;
  piVar3 = (int *)(param_1 + 0x5bc);
  do {
    piVar4 = piVar3 + -0x74;
    iVar2 = iVar2 + -0x1d0;
    if (piVar3[-0x3e] != 0) {
      FUN_82142f48();
    }
    piVar3[-0x3e] = 0;
    piVar3[-0x3d] = 0;
    piVar3[-0x3c] = 0;
    FUN_822c73a8(piVar3 + -0x6f);
    if (*piVar4 != 0) {
      FUN_82142f48();
    }
    *piVar4 = 0;
    piVar3[-0x73] = 0;
    piVar3[-0x72] = 0;
    FUN_822c73a8(piVar3 + -0x90);
    FUN_822c73a8(iVar2);
    iVar1 = iVar1 + -1;
    piVar3 = piVar4;
  } while (-1 < iVar1);
  FUN_822c73a8(param_1 + 0xdc);
  if (*(int *)(param_1 + 200) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 200) = 0;
  *(undefined4 *)(param_1 + 0xcc) = 0;
  *(undefined4 *)(param_1 + 0xd0) = 0;
  FUN_822c73a8(param_1 + 0x58);
  FUN_822c73a8(param_1);
  return;
}



// ===================================================
// 823035E8  ->  FUN_823035e8  (entree 823035e8)
// ===================================================

undefined8 FUN_823035e8(undefined8 param_1,ulonglong param_2)

{
  FUN_823034a8();
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 82303638  ->  FUN_82303638  (entree 82303638)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

undefined4 * FUN_82303638(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  double dVar4;
  
  FUN_822e4b58();
  puVar2 = param_1 + 0x55;
  iVar1 = 1;
  puVar3 = param_1 + 0xbd;
  dVar4 = (double)DAT_82000a34;
  *param_1 = &PTR_FUN_8208d8e8;
  do {
    FUN_822e4b58(puVar2);
    *puVar2 = &PTR_FUN_8208d8bc;
    iVar1 = iVar1 + -1;
    puVar3[9] = (float)dVar4;
    puVar3[10] = (float)dVar4;
    *puVar3 = 0;
    puVar3[1] = 0;
    puVar2 = puVar2 + 0x74;
    puVar3[2] = 0;
    *(undefined1 *)(puVar3 + 5) = 0;
    puVar3[6] = 0;
    puVar3 = puVar3 + 0x74;
  } while (-1 < iVar1);
  return param_1;
}



// ===================================================
// 823036C8  ->  FUN_823036c8  (entree 823036c8)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

undefined8 FUN_823036c8(int param_1)

{
  char cVar2;
  int iVar1;
  int iVar3;
  
  *(undefined4 **)(param_1 + 0x4f8) = &DAT_82ac8510;
  cVar2 = FUN_822fa900(0xffffffff82ac8510,0xffffffff8208d72c,0xffffffff8208d920,1,0);
  FUN_822e36a8(param_1,cVar2 == '\0');
  *(undefined4 *)(param_1 + 0x4fc) = 0;
  FUN_822e38d8(param_1);
  iVar1 = *(int *)(param_1 + 0x4f4);
  if (-1 < iVar1) {
    if (0 < iVar1) {
      iVar3 = 1;
      goto LAB_82303760;
    }
    iVar3 = iVar1;
    if (-1 < iVar1) goto LAB_82303760;
  }
  iVar3 = 0;
LAB_82303760:
  if (iVar3 == iVar1) {
    param_1 = iVar1 * 0x1d0 + param_1;
    *(int *)(param_1 + 0x2cc) = iVar1;
    FUN_822c8aa0(param_1 + 0x154,0xffffffff8208d910);
    return 1;
  }
  *(undefined4 *)(param_1 + 0x4f4) = 2;
  *(undefined4 *)(param_1 + 0x2cc) = 0;
  FUN_822c8aa0(param_1 + 0x154,0xffffffff8208d910);
  *(undefined4 *)(param_1 + 0x49c) = 1;
  FUN_822c8aa0(param_1 + 0x324,0xffffffff8208d910);
  iVar1 = FUN_82144c28();
  if (-1 < iVar1) {
    *(undefined4 *)(param_1 + 0x50) = 0;
    *(undefined4 *)(param_1 + 0x14c) = 1;
    *(undefined1 *)(param_1 + 0x150) = 0;
  }
  return 1;
}



// ===================================================
// 823037E8  ->  FUN_823037e8  (entree 823037e8)
// ===================================================

void FUN_823037e8(int param_1)

{
  FUN_822c7d50(param_1 + 0x154);
  FUN_822c7d50(param_1 + 0x324);
  FUN_822fa018(*(undefined4 *)(param_1 + 0x4f8),0);
  FUN_821664c0(*(undefined4 *)(param_1 + 0x4fc));
  FUN_822e3968(param_1);
  return;
}



// ===================================================
// 82303840  ->  FUN_82303840  (entree 82303840)
// ===================================================

void FUN_82303840(int param_1)

{
  char cVar2;
  undefined8 uVar1;
  float local_20;
  float local_1c;
  float local_18;
  
  cVar2 = FUN_822fa080(*(undefined4 *)(param_1 + 0x4f8));
  if (cVar2 != '\0') {
    local_20 = DAT_82000a34;
    local_1c = DAT_82000a34;
    local_18 = DAT_82000a34;
    FUN_822c2a08(9);
    FUN_8223bc10(0xe);
    FUN_8223c130(9);
    FUN_822faa88(*(undefined4 *)(param_1 + 0x4f8),&local_20,0xffffffff8208d924,1);
    FUN_8223beb8((double)local_20,(double)local_1c);
    FUN_8223c048(0xffffffffffbff560);
    uVar1 = FUN_82322798(0x446);
    FUN_8223fe30(0xffffffff8208476c,uVar1);
    FUN_822c2a18();
  }
  return;
}



// ===================================================
// 82303900  ->  FUN_82303900  (entree 82303900)
// ===================================================

void FUN_82303900(int param_1)

{
  if ((*(int *)(param_1 + 0x14c) != 0) && (*(char *)(param_1 + 0x54) == '\0')) {
    thunk_FUN_822d11a8();
    *(undefined4 *)(param_1 + 0x14c) = 0;
    *(undefined1 *)(param_1 + 0x150) = 0;
    *(undefined1 *)(param_1 + 0x1a8) = 1;
    *(undefined1 *)(param_1 + 0x378) = 1;
  }
  return;
}



// ===================================================
// 82303980  ->  FUN_82303980  (entree 82303980)
// ===================================================

undefined8 FUN_82303980(undefined8 param_1,ulonglong param_2)

{
  FUN_82303520();
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 823039D0  ->  FUN_823039d0  (entree 823039d0)
// ===================================================

void FUN_823039d0(int param_1,int param_2)

{
  char cVar2;
  undefined4 uVar1;
  undefined8 uVar3;
  double dVar4;
  float local_e0;
  float local_dc;
  float local_d8;
  float local_d0;
  float local_cc;
  float local_c8;
  undefined4 local_c0;
  char *local_bc;
  undefined4 local_a8;
  undefined4 local_a4;
  undefined4 local_9c;
  undefined4 local_94;
  float local_8c;
  float local_88;
  float local_84;
  
  cVar2 = FUN_822fa080(*(undefined4 *)(param_1 + 0x4f8));
  if (cVar2 != '\0') {
    if (*(int *)(param_1 + 0x4fc) != 0) {
      FUN_821664c0();
    }
    local_e0 = DAT_82000a34;
    local_dc = DAT_82000a34;
    local_d8 = DAT_82000a34;
    if (param_2 == 0) {
      uVar3 = 0xffffffff8208d950;
    }
    else {
      uVar3 = 0xffffffff8208d93c;
    }
    FUN_822faa88(*(undefined4 *)(param_1 + 0x4f8),&local_e0,uVar3,1);
    dVar4 = (double)FUN_8214ace8((double)local_dc);
    local_dc = (float)dVar4;
    FUN_82158008(&local_c0);
    local_d0 = local_e0;
    local_cc = local_dc;
    local_c8 = local_d8;
    local_c0 = 0x417;
    local_bc = s_cs_dark_8208d934;
    local_9c = 10;
    local_a8 = 0x20000;
    local_8c = local_e0;
    local_88 = local_dc;
    local_84 = local_d8;
    local_a4 = 2;
    local_94 = 9;
    uVar1 = FUN_82166cc0(&local_c0);
    *(undefined4 *)(param_1 + 0x4fc) = uVar1;
    FUN_82157f80(&local_c0);
  }
  return;
}



// ===================================================
// 82303AF8  ->  FUN_82303af8  (entree 82303af8)
// ===================================================

/* WARNING: Function: __savegprlr_24 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_24 replaced with injection: x360_restgprlr */

undefined8 FUN_82303af8(int param_1,undefined1 *param_2)

{
  bool bVar1;
  bool bVar2;
  bool bVar3;
  char cVar4;
  undefined1 uVar5;
  ulonglong uVar6;
  char *pcVar7;
  
  bVar1 = false;
  bVar2 = false;
  bVar3 = false;
  uVar5 = 0;
  uVar6 = 0;
  pcVar7 = (char *)(param_1 + 0x1a8);
  do {
    cVar4 = FUN_822c7b98(pcVar7 + -0x54);
    if (cVar4 != '\0') {
      bVar1 = true;
      if (*pcVar7 == '\0') {
        if (pcVar7[0x128] != '\0') {
          bVar3 = true;
        }
      }
      else {
        if (pcVar7[0x129] != '\0') {
          uVar5 = 1;
        }
        bVar2 = true;
        if (*(int *)(param_1 + 0x14c) == 0) {
          FUN_823039d0(param_1,uVar6);
        }
      }
    }
    uVar6 = uVar6 + 1;
    pcVar7 = pcVar7 + 0x1d0;
  } while ((uVar6 & 0xffffffff) < 2);
  if (param_2 != (undefined1 *)0x0) {
    *param_2 = uVar5;
  }
  if (*(int *)(param_1 + 0x14c) != 0) {
    return 0;
  }
  if ((bVar1) && ((!bVar2 || (bVar3)))) {
    return 0;
  }
  return 1;
}



// ===================================================
// 82303C10  ->  FUN_82303c10  (entree 82303c10)
// ===================================================

undefined8 FUN_82303c10(int param_1)

{
  char cVar1;
  undefined8 uVar2;
  
  FUN_822e3618(param_1,0x1da0);
  FUN_822e3660(param_1,0x1da0);
  if (*(int *)(param_1 + 0x14c) == 0) {
    if (1 < *(int *)(param_1 + 0x4f4)) {
      return 0;
    }
    *(undefined1 *)(*(int *)(param_1 + 0x4f4) * 0x1d0 + param_1 + 0x2d2) = 1;
  }
  else {
    cVar1 = FUN_822e2dd8(param_1 + 0x2d4);
    if (cVar1 == '\0') {
      return 0;
    }
    cVar1 = FUN_822e2dd8(param_1 + 0x4a4);
    if (cVar1 == '\0') {
      return 0;
    }
    if (*(char *)(param_1 + 0x54) == '\0') {
      if (*(int *)(param_1 + 0x4fc) == 0) {
        FUN_823039d0(param_1,*(uint *)(param_1 + 0x50) ^ 1);
      }
      FUN_822d09c0(0);
      FUN_822d0c30(2);
      FUN_822e33f8(param_1);
      FUN_822c7e30(param_1 + 0x154);
      FUN_822c7e30(param_1 + 0x324);
      FUN_822e3618(param_1,0x140);
      uVar2 = 3;
      goto LAB_82303d54;
    }
    *(undefined1 *)(*(int *)(param_1 + 0x50) * 0x1d0 + param_1 + 0x2d2) = 1;
    if (*(char *)(*(int *)(param_1 + 0x50) * 0x1d0 + param_1 + 0x1a8) != '\0') {
      *(undefined4 *)(param_1 + 0x14c) = 0;
      *(undefined1 *)(param_1 + 0x150) = 0;
      return 0;
    }
    FUN_822d09c0();
    FUN_822c7ff0(*(int *)(param_1 + 0x50) * 0x1d0 + param_1 + 0x154);
  }
  FUN_822e3618(param_1,0x13e);
  uVar2 = 0;
LAB_82303d54:
  FUN_822e3660(param_1,uVar2);
  return 0;
}



// ===================================================
// 82303D78  ->  FUN_82303d78  (entree 82303d78)
// ===================================================

undefined8 FUN_82303d78(int param_1,undefined8 param_2)

{
  undefined8 uVar1;
  
  if ((*(int *)(param_1 + 0x14c) == 0) || (*(char *)(param_1 + 0x54) != '\0')) {
    uVar1 = 1;
  }
  else {
    FUN_823039d0(param_1,*(uint *)(param_1 + 0x50) ^ 1);
    uVar1 = FUN_822e35b0(param_1,param_2);
  }
  return uVar1;
}



// ===================================================
// 82303E10  ->  FUN_82303e10  (entree 82303e10)
// ===================================================

undefined8 FUN_82303e10(int *param_1)

{
  undefined8 uVar1;
  
  FUN_822e36a8(param_1,0);
  FUN_822e38d8(param_1);
  uVar1 = FUN_822dac80();
  FUN_825ffd30(param_1 + 0x55,uVar1,0x30);
  FUN_825ffd30(param_1 + 0x61,param_1 + 0x55,0x30);
  *(undefined1 *)(param_1 + 0x52) = 0;
  param_1[0x51] = 0xd;
  param_1[0x13] = 0;
  FUN_822e3208(param_1 + 0xec);
  (**(code **)(*param_1 + 0x18))(param_1,0);
  param_1[0x6d] = (int)&DAT_82ac8510;
  FUN_822fa900(0xffffffff82ac8510,0xffffffff8208d72c,0xffffffff8208d970,1,0);
  FUN_822e3c10(param_1 + 0x6e);
  FUN_822e3c10(param_1 + 0xac);
  return 1;
}



// ===================================================
// 82303EE8  ->  FUN_82303ee8  (entree 82303ee8)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82303ee8(int param_1)

{
  char cVar3;
  int iVar1;
  int iVar2;
  undefined4 local_90 [36];
  
  cVar3 = FUN_822c7b98(param_1 + 0x1b8);
  if (cVar3 == '\0') {
    iVar1 = FUN_822e2e38(param_1 + 0x1b8);
    if (iVar1 == 0) {
      FUN_8220d1e0(0x6d);
    }
    else {
      iVar1 = param_1 + 0x2b0;
      cVar3 = FUN_822c7b98(iVar1);
      if (cVar3 == '\0') {
        iVar2 = FUN_822e2e38(iVar1);
        if (-1 < iVar2) {
          iVar2 = FUN_822e2e38(iVar1);
          if (iVar2 == 0) {
            *(undefined4 *)(param_1 + 0x154) = 2;
            *(undefined4 *)(param_1 + 0x15c) = 2;
            *(undefined4 *)(param_1 + 0x160) = 2;
            *(undefined4 *)(param_1 + 0x164) = 2;
            *(undefined4 *)(param_1 + 0x16c) = 2;
            *(undefined4 *)(param_1 + 0x158) = 1;
            *(undefined4 *)(param_1 + 0x168) = 0;
            *(undefined4 *)(param_1 + 0x170) = 2;
            *(undefined4 *)(param_1 + 0x174) = 2;
            *(undefined4 *)(param_1 + 0x178) = 2;
            *(undefined4 *)(param_1 + 0x17c) = 1;
            *(undefined4 *)(param_1 + 0x180) = 0;
          }
          FUN_822e3c10(iVar1);
        }
        cVar3 = FUN_822fa080(*(undefined4 *)(param_1 + 0x1b4));
        if (cVar3 != '\0') {
          FUN_822e33f8(param_1);
        }
      }
    }
  }
  local_90[0x1a] = 2;
  local_90[0x1b] = 2;
  local_90[0] = 0x130;
  local_90[1] = 0x131;
  local_90[2] = 0x132;
  local_90[3] = 0x133;
  local_90[4] = 0x134;
  local_90[5] = 0x135;
  local_90[6] = 0x136;
  local_90[7] = 0x137;
  local_90[8] = 0x138;
  local_90[9] = 0x139;
  local_90[10] = 0x13a;
  local_90[0xb] = 0x13b;
  local_90[0xc] = 0x13c;
  local_90[0xd] = 0x13d;
  local_90[0xe] = 4;
  local_90[0xf] = 4;
  local_90[0x10] = 4;
  local_90[0x11] = 4;
  local_90[0x12] = 4;
  local_90[0x13] = 4;
  local_90[0x14] = 4;
  local_90[0x15] = 4;
  local_90[0x16] = 4;
  local_90[0x17] = 4;
  local_90[0x18] = 4;
  local_90[0x19] = 4;
  FUN_822e3618(param_1,local_90[*(int *)(param_1 + 0x4c)]);
  FUN_822e3660(param_1,local_90[*(int *)(param_1 + 0x4c) + 0xe]);
  return 0;
}



// ===================================================
// 823040B0  ->  FUN_823040b0  (entree 823040b0)
// ===================================================

undefined8 FUN_823040b0(int param_1)

{
  FUN_822e3968();
  FUN_822fa018(*(undefined4 *)(param_1 + 0x1b4),0);
  FUN_822e3228(param_1 + 0x3b0);
  return 1;
}



// ===================================================
// 823040F8  ->  FUN_823040f8  (entree 823040f8)
// ===================================================

/* WARNING: Function: __savegprlr_19 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_19 replaced with injection: x360_restgprlr */

void FUN_823040f8(void)

{
  int iVar2;
  char cVar3;
  undefined8 uVar1;
  int iVar4;
  ulonglong uVar5;
  double dVar6;
  double dVar7;
  double dVar8;
  double dVar9;
  double dVar10;
  double dVar11;
  double dVar12;
  double dVar13;
  float fStack_f0;
  float fStack_ec;
  float fStack_e8;
  uint auStack_e0 [56];
  
  iVar2 = FUN_826018c0();
  cVar3 = FUN_822fa080(*(undefined4 *)(iVar2 + 0x1b4));
  if (cVar3 != '\0') {
    dVar6 = (double)DAT_82000a34;
    fStack_f0 = DAT_82000a34;
    fStack_ec = DAT_82000a34;
    fStack_e8 = DAT_82000a34;
    auStack_e0[0] = 0x3f7;
    auStack_e0[1] = 0x3fd;
    auStack_e0[2] = 0x403;
    auStack_e0[3] = 0x408;
    auStack_e0[4] = 0x411;
    auStack_e0[5] = 0x41a;
    auStack_e0[6] = 0x421;
    auStack_e0[7] = 0x427;
    auStack_e0[8] = 0x42c;
    auStack_e0[9] = 0x435;
    auStack_e0[10] = 0x43e;
    auStack_e0[0xb] = 0x441;
    auStack_e0[0xc] = 0x444;
    auStack_e0[0xd] = 0x445;
    FUN_822c2a08(9);
    FUN_8223bc10(0xe);
    FUN_8223c130(9);
    FUN_822faa88(*(undefined4 *)(iVar2 + 0x1b4),&fStack_f0,0xffffffff8208d9c4,1);
    FUN_8223beb8((double)fStack_f0,(double)fStack_ec);
    FUN_8223c048(0xffffffffffbff560);
    uVar1 = FUN_82322798(0x3f5);
    FUN_8223fe30(0xffffffff8208476c,uVar1);
    FUN_8223c048(0xffffffffffffffff);
    dVar7 = (double)FUN_822e4a08(iVar2);
    iVar4 = 0;
    dVar13 = (double)DAT_82084cb4;
    dVar12 = (double)DAT_82000f1c;
    dVar11 = (double)DAT_82000b08;
    dVar10 = (double)DAT_82010304;
    dVar9 = dVar7;
    do {
      dVar8 = (double)fStack_ec;
      if (iVar4 == 0) {
        FUN_822faa88(dVar7,dVar8,*(undefined4 *)(iVar2 + 0x1b4),&fStack_f0,0xffffffff8208d974,0);
        FUN_8223beb8((double)fStack_f0,(double)fStack_ec);
        uVar1 = FUN_82322798(0x3f6);
        FUN_8223fe30(0xffffffff82000f08,uVar1);
        FUN_822faa88(*(undefined4 *)(iVar2 + 0x1b4),&fStack_f0,0xffffffff8208d984,0);
        fStack_ec = (float)((double)fStack_ec - dVar13);
      }
      else if (iVar4 == 6) {
        FUN_822faa88(dVar7,dVar8,*(undefined4 *)(iVar2 + 0x1b4),&fStack_f0,0xffffffff8208d994,0);
        FUN_8223beb8((double)fStack_f0,(double)fStack_ec);
        uVar1 = FUN_82322798(0x420);
        FUN_8223fe30(0xffffffff82000f08,uVar1);
        FUN_822faa88(*(undefined4 *)(iVar2 + 0x1b4),&fStack_f0,0xffffffff8208d9a4,0);
        fStack_ec = (float)((double)fStack_ec - dVar13);
      }
      else if (iVar4 == 0xc) {
        FUN_822faa88(dVar7,dVar8,*(undefined4 *)(iVar2 + 0x1b4),&fStack_f0,0xffffffff8208d9b4,0);
        fStack_ec = (float)((double)fStack_ec - dVar12);
      }
      FUN_8223beb8((double)fStack_f0);
      uVar5 = (ulonglong)auStack_e0[iVar4];
      if (iVar4 < 0xc) {
        uVar1 = FUN_82322798(uVar5);
        FUN_8223fe30(0xffffffff82000f08,uVar1);
        uVar1 = FUN_82322798(*(uint *)((iVar4 + 0x55) * 4 + iVar2) + uVar5 + 1);
        if (iVar4 == *(int *)(iVar2 + 0x4c)) {
          FUN_82322798(uVar5);
          FUN_822e37e0((double)fStack_f0,(double)fStack_ec,dVar11,iVar2 + 0x3a8);
          dVar6 = (double)fStack_ec;
        }
        FUN_8223beb8((double)(float)(dVar9 - dVar10),(double)fStack_ec);
        dVar7 = (double)FUN_8223fe30(0xffffffff820117f8,uVar1);
      }
      else {
        uVar1 = FUN_82322798(uVar5);
        dVar7 = (double)FUN_8223fe30(0xffffffff8208476c,uVar1);
        if (iVar4 == *(int *)(iVar2 + 0x4c)) {
          FUN_82322798(uVar5);
          dVar7 = (double)FUN_822e37e0((double)fStack_f0,(double)fStack_ec,dVar11,iVar2 + 0x3a8);
        }
      }
      iVar4 = iVar4 + 1;
      fStack_ec = (float)((double)fStack_ec + dVar12);
    } while (iVar4 < 0xe);
    if (*(int *)(iVar2 + 0x4c) < 0xc) {
      FUN_822e5380((double)(float)(dVar9 - dVar10),dVar6);
      FUN_822c2a18();
      FUN_8260190c();
      return;
    }
    FUN_822e3228(iVar2 + 0x3b0);
    FUN_822c2a18();
  }
  FUN_8260190c();
  return;
}



// ===================================================
// 823044E0  ->  FUN_823044e0  (entree 823044e0)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

undefined8 FUN_823044e0(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  int aiStack_60 [24];
  
  aiStack_60[3] = 7;
  aiStack_60[0] = 4;
  aiStack_60[1] = 4;
  aiStack_60[2] = 3;
  aiStack_60[4] = 7;
  aiStack_60[5] = 1;
  aiStack_60[6] = 4;
  aiStack_60[7] = 3;
  aiStack_60[8] = 7;
  aiStack_60[9] = 7;
  aiStack_60[10] = 1;
  aiStack_60[0xb] = 1;
  if (param_2 != 0) {
    FUN_822e35b0();
    FUN_822e3228(param_1 + 0x3b0);
  }
  iVar1 = *(int *)(param_1 + 0x4c);
  if (iVar1 < 0xc) {
    iVar2 = aiStack_60[iVar1];
    *(undefined4 *)(param_1 + 0x50) = *(undefined4 *)((iVar1 + 0x55) * 4 + param_1);
    *(int *)(param_1 + 0x14c) = iVar2;
  }
  else {
    *(undefined4 *)(param_1 + 0x14c) = 0;
  }
  *(undefined1 *)(param_1 + 0x150) = 0;
  FUN_822e32b8(param_1 + 0x3b0,0xffffffffffffffff,0 < *(int *)(param_1 + 0x50));
  FUN_822e32b8(param_1 + 0x3b0,1,*(int *)(param_1 + 0x50) < aiStack_60[*(int *)(param_1 + 0x4c)]);
  return 1;
}



// ===================================================
// 823045E0  ->  FUN_823045e0  (entree 823045e0)
// ===================================================

undefined8 FUN_823045e0(int *param_1,undefined8 param_2)

{
  FUN_822e35b0();
  if (param_1[0x13] < 0xc) {
    param_1[param_1[0x13] + 0x55] = param_1[0x14];
    FUN_821ccba8(param_1 + 0xec,param_2);
    (**(code **)(*param_1 + 0x18))(param_1,0);
  }
  return 1;
}



// ===================================================
// 82304660  ->  FUN_82304660  (entree 82304660)
// ===================================================

void FUN_82304660(int param_1)

{
  byte bVar1;
  byte bVar2;
  undefined4 uVar3;
  byte *pbVar4;
  byte *pbVar5;
  int iVar6;
  
  thunk_FUN_822d11a8();
  pbVar5 = (byte *)(param_1 + 0x154);
  pbVar4 = (byte *)(param_1 + 0x184);
  do {
    bVar1 = *pbVar5;
    bVar2 = *pbVar4;
    if ((ulonglong)bVar1 - (ulonglong)bVar2 != 0) break;
    pbVar5 = pbVar5 + 1;
    pbVar4 = pbVar4 + 1;
  } while (pbVar5 != (byte *)(param_1 + 0x184));
  if ((int)((ulonglong)bVar1 - (ulonglong)bVar2) == 0) {
    FUN_8220d1e0(0x6d);
  }
  else {
    iVar6 = param_1 + 0x1b8;
    FUN_822e3c10(iVar6);
    FUN_822c8aa0(iVar6,0xffffffff82085024);
    FUN_822e2e28(iVar6,1);
    uVar3 = FUN_82322798(0x5ff);
    *(undefined4 *)(param_1 + 0x218) = uVar3;
  }
  return;
}



// ===================================================
// 82304708  ->  FUN_82304708  (entree 82304708)
// ===================================================

void FUN_82304708(int param_1)

{
  byte bVar1;
  byte bVar2;
  undefined4 uVar3;
  byte *pbVar4;
  byte *pbVar5;
  int iVar6;
  
  if (*(int *)(param_1 + 0x4c) == 0xd) {
    FUN_822e35e0();
    pbVar5 = (byte *)(param_1 + 0x154);
    FUN_822dac98(pbVar5);
    pbVar4 = (byte *)(param_1 + 0x184);
    do {
      bVar1 = *pbVar5;
      bVar2 = *pbVar4;
      if ((ulonglong)bVar1 - (ulonglong)bVar2 != 0) break;
      pbVar5 = pbVar5 + 1;
      pbVar4 = pbVar4 + 1;
    } while (pbVar5 != (byte *)(param_1 + 0x184));
    if ((int)((ulonglong)bVar1 - (ulonglong)bVar2) != 0) {
      FUN_822db258(1,0xffffffffffffffff);
    }
    FUN_8220d1e0(0x6d);
  }
  else if (*(int *)(param_1 + 0x4c) == 0xc) {
    FUN_822e35e0(param_1);
    iVar6 = param_1 + 0x2b0;
    FUN_822e3c10(iVar6);
    FUN_822c8aa0(iVar6,0xffffffff82085024);
    FUN_822e2e28(iVar6,1);
    uVar3 = FUN_82322798(0x600);
    *(undefined4 *)(param_1 + 0x310) = uVar3;
  }
  return;
}



// ===================================================
// 823047E8  ->  FUN_823047e8  (entree 823047e8)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

int FUN_823047e8(int param_1,ulonglong param_2)

{
  FUN_82154d98(param_1 + 0x2b0);
  FUN_82154d98(param_1 + 0x1b8);
  FUN_822c73a8(param_1 + 0xdc);
  if (*(int *)(param_1 + 200) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 200) = 0;
  *(undefined4 *)(param_1 + 0xcc) = 0;
  *(undefined4 *)(param_1 + 0xd0) = 0;
  FUN_822c73a8(param_1 + 0x58);
  FUN_822c73a8(param_1);
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 82304898  ->  FUN_82304898  (entree 82304898)
// ===================================================

undefined8 FUN_82304898(int *param_1)

{
  int *piVar1;
  
  FUN_822e36a8(param_1,0);
  FUN_822e38d8(param_1);
  piVar1 = (int *)FUN_822dada0();
  param_1[0x55] = *piVar1;
  param_1[0x56] = piVar1[1];
  param_1[0x57] = piVar1[2];
  param_1[0x58] = param_1[0x55];
  param_1[0x59] = param_1[0x56];
  param_1[0x5a] = param_1[0x57];
  param_1[0x51] = 4;
  *(undefined1 *)(param_1 + 0x52) = 0;
  param_1[0x13] = 0;
  param_1[0x56] = param_1[0x56] + 0xf;
  param_1[0x57] = param_1[0x57] + 0xf;
  FUN_822e3208(param_1 + 0xda);
  (**(code **)(*param_1 + 0x18))(param_1,0);
  param_1[0x5b] = (int)&DAT_82ac8510;
  FUN_822fa900(0xffffffff82ac8510,0xffffffff8208d72c,0xffffffff8208da10,1,0);
  FUN_822e3c10(param_1 + 0x5c);
  FUN_822e3c10(param_1 + 0x9a);
  return 1;
}



// ===================================================
// 82304990  ->  FUN_82304990  (entree 82304990)
// ===================================================

undefined8 FUN_82304990(int param_1)

{
  char cVar3;
  int iVar1;
  int iVar2;
  undefined4 auStack_40 [10];
  
  cVar3 = FUN_822c7b98(param_1 + 0x170);
  if (cVar3 == '\0') {
    iVar1 = FUN_822e2e38(param_1 + 0x170);
    if (iVar1 == 0) {
      FUN_822db7e0(param_1 + 0x160);
      FUN_8220d1e0(0x6d);
    }
    else {
      iVar1 = param_1 + 0x268;
      cVar3 = FUN_822c7b98(iVar1);
      if (cVar3 == '\0') {
        iVar2 = FUN_822e2e38(iVar1);
        if (-1 < iVar2) {
          iVar2 = FUN_822e2e38(iVar1);
          if (iVar2 == 0) {
            *(undefined4 *)(param_1 + 0x154) = 0;
            *(undefined4 *)(param_1 + 0x15c) = 0;
            *(undefined4 *)(param_1 + 0x158) = 0;
            FUN_822db7e0();
            *(int *)(param_1 + 0x158) = *(int *)(param_1 + 0x158) + 0xf;
            *(int *)(param_1 + 0x15c) = *(int *)(param_1 + 0x15c) + 0xf;
          }
          FUN_822e3c10(iVar1);
        }
        cVar3 = FUN_822fa080(*(undefined4 *)(param_1 + 0x16c));
        if (cVar3 != '\0') {
          FUN_822e33f8(param_1);
        }
      }
    }
  }
  auStack_40[0] = 0x141;
  auStack_40[1] = 0x143;
  auStack_40[2] = 0x144;
  auStack_40[3] = 0x145;
  auStack_40[4] = 0x146;
  auStack_40[5] = 4;
  auStack_40[6] = 4;
  auStack_40[7] = 4;
  auStack_40[8] = 2;
  auStack_40[9] = 2;
  FUN_822e3618(param_1,auStack_40[*(int *)(param_1 + 0x4c)]);
  FUN_822e3660(param_1,auStack_40[*(int *)(param_1 + 0x4c) + 5]);
  return 0;
}



// ===================================================
// 82304B00  ->  FUN_82304b00  (entree 82304b00)
// ===================================================

undefined8 FUN_82304b00(int param_1)

{
  FUN_822e3968();
  FUN_822fa018(*(undefined4 *)(param_1 + 0x16c),0);
  FUN_822e3228(param_1 + 0x368);
  return 1;
}



// ===================================================
// 82304B48  ->  FUN_82304b48  (entree 82304b48)
// ===================================================

/* WARNING: Function: __savegprlr_22 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_22 replaced with injection: x360_restgprlr */

void FUN_82304b48(void)

{
  double dVar1;
  uint uVar2;
  int iVar4;
  char cVar5;
  undefined8 uVar3;
  int iVar6;
  ulonglong uVar7;
  double dVar8;
  double dVar9;
  double dVar10;
  double dVar11;
  double dVar12;
  double dVar13;
  float fStack_b0;
  float fStack_ac;
  float fStack_a8;
  uint auStack_a0 [40];
  
  iVar4 = FUN_826018c0();
  cVar5 = FUN_822fa080(*(undefined4 *)(iVar4 + 0x16c));
  if (cVar5 != '\0') {
    dVar8 = (double)DAT_82000a34;
    fStack_b0 = DAT_82000a34;
    fStack_ac = DAT_82000a34;
    fStack_a8 = DAT_82000a34;
    auStack_a0[0] = 0x47e;
    auStack_a0[1] = 0x4ab;
    auStack_a0[2] = 0x4cb;
    auStack_a0[3] = 0x4eb;
    auStack_a0[4] = 0x4ec;
    FUN_822c2a08(9);
    FUN_8223bc10(0xe);
    FUN_8223c130(9);
    FUN_822faa88(*(undefined4 *)(iVar4 + 0x16c),&fStack_b0,0xffffffff8208da40,1);
    FUN_8223beb8((double)fStack_b0,(double)fStack_ac);
    FUN_8223c048(0xffffffffffbff560);
    uVar3 = FUN_82322798(0x47d);
    FUN_8223fe30(0xffffffff8208476c,uVar3);
    FUN_8223c048(0xffffffffffffffff);
    dVar9 = (double)FUN_822e4a08(iVar4);
    FUN_822faa88(*(undefined4 *)(iVar4 + 0x16c),&fStack_b0,0xffffffff8208da2c,0);
    dVar10 = (double)DAT_82000f1c;
    dVar12 = (double)DAT_82011814;
    dVar13 = (double)DAT_82010304;
    iVar6 = 0;
    dVar11 = (double)DAT_82000b08;
    do {
      if (iVar6 == 3) {
        FUN_822faa88(*(undefined4 *)(iVar4 + 0x16c),&fStack_b0,0xffffffff8208da14,0);
      }
      FUN_8223beb8((double)fStack_b0,(double)fStack_ac);
      if (iVar6 < 3) {
        FUN_8223c048(0xffffffffffffffff);
        cVar5 = FUN_82144b20();
        if ((cVar5 != '\0') && (iVar6 != 0)) {
          FUN_8223c048(0xffffffffff808080);
        }
        uVar7 = (ulonglong)auStack_a0[iVar6];
        uVar3 = FUN_82322798(uVar7);
        FUN_8223fe30(0xffffffff82000f08,uVar3);
        if (iVar6 == *(int *)(iVar4 + 0x4c)) {
          FUN_82322798(uVar7);
          FUN_822e37e0((double)fStack_b0,(double)fStack_ac,dVar11,iVar4 + 0x360);
          dVar8 = (double)fStack_ac;
        }
        uVar3 = FUN_82322798(*(uint *)((iVar6 + 0x55) * 4 + iVar4) + uVar7 + 1);
        cVar5 = FUN_82144b20();
        if ((cVar5 != '\0') && (iVar6 != 0)) {
          uVar3 = 0xffffffff8208da24;
        }
        FUN_8223beb8((double)(float)(dVar9 - dVar13),(double)fStack_ac);
        FUN_8223fe30(0xffffffff820117f8,uVar3);
        FUN_8223c048(0xffffffffffffffff);
        dVar1 = (double)fStack_ac + dVar12;
      }
      else {
        uVar2 = auStack_a0[iVar6];
        uVar3 = FUN_82322798(uVar2);
        FUN_8223fe30(0xffffffff8208476c,uVar3);
        if (iVar6 == *(int *)(iVar4 + 0x4c)) {
          FUN_82322798(uVar2);
          FUN_822e37e0((double)fStack_b0,(double)fStack_ac,dVar11,iVar4 + 0x360);
        }
        dVar1 = (double)fStack_ac + dVar10;
      }
      fStack_ac = (float)dVar1;
      iVar6 = iVar6 + 1;
    } while (iVar6 < 5);
    if (*(int *)(iVar4 + 0x4c) < 3) {
      FUN_822e5380((double)(float)(dVar9 - dVar13),dVar8);
      FUN_822c2a18();
      FUN_8260190c();
      return;
    }
    FUN_822e3228(iVar4 + 0x368);
    FUN_822c2a18();
  }
  FUN_8260190c();
  return;
}



// ===================================================
// 82304E98  ->  FUN_82304e98  (entree 82304e98)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82304e98(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  char cVar3;
  int aiStack_30 [12];
  
  aiStack_30[0] = 1;
  aiStack_30[1] = 0x1e;
  aiStack_30[2] = 0x1e;
  if (param_2 != 0) {
    FUN_822e35b0();
    FUN_822e3228(param_1 + 0x368);
  }
  cVar3 = FUN_82144b20();
  if (cVar3 != '\0') {
    if (*(int *)(param_1 + 0x4c) == 1) {
      *(undefined4 *)(param_1 + 0x4c) = 3;
    }
    else if (*(int *)(param_1 + 0x4c) == 2) {
      *(undefined4 *)(param_1 + 0x4c) = 0;
    }
  }
  iVar1 = *(int *)(param_1 + 0x4c);
  if (iVar1 < 3) {
    iVar2 = aiStack_30[iVar1];
    *(undefined4 *)(param_1 + 0x50) = *(undefined4 *)((iVar1 + 0x55) * 4 + param_1);
    *(int *)(param_1 + 0x14c) = iVar2;
  }
  else {
    *(undefined4 *)(param_1 + 0x14c) = 0;
  }
  *(undefined1 *)(param_1 + 0x150) = 0;
  FUN_822e32b8(param_1 + 0x368,0xffffffffffffffff,0 < *(int *)(param_1 + 0x50));
  FUN_822e32b8(param_1 + 0x368,1,*(int *)(param_1 + 0x50) < aiStack_30[*(int *)(param_1 + 0x4c)]);
  return 1;
}



// ===================================================
// 82304FA0  ->  FUN_82304fa0  (entree 82304fa0)
// ===================================================

undefined8 FUN_82304fa0(int *param_1,undefined8 param_2)

{
  int iStack_30;
  int iStack_2c;
  int iStack_28;
  
  FUN_822e35b0();
  if (param_1[0x13] < 3) {
    param_1[param_1[0x13] + 0x55] = param_1[0x14];
    FUN_821ccba8(param_1 + 0xda,param_2);
    (**(code **)(*param_1 + 0x18))(param_1,0);
    iStack_2c = param_1[0x56] + -0xf;
    iStack_30 = param_1[0x55];
    iStack_28 = param_1[0x57] + -0xf;
    FUN_822db7e0(&iStack_30);
  }
  return 1;
}



// ===================================================
// 82305048  ->  FUN_82305048  (entree 82305048)
// ===================================================

void FUN_82305048(int param_1)

{
  byte bVar1;
  byte bVar2;
  undefined4 uVar3;
  byte *pbVar4;
  byte *pbVar5;
  int iVar6;
  undefined4 uStack_30;
  int iStack_2c;
  int iStack_28;
  byte abStack_24 [12];
  
  thunk_FUN_822d11a8();
  pbVar5 = (byte *)&uStack_30;
  pbVar4 = (byte *)(param_1 + 0x160);
  iStack_2c = *(int *)(param_1 + 0x158) + -0xf;
  uStack_30 = *(undefined4 *)(param_1 + 0x154);
  iStack_28 = *(int *)(param_1 + 0x15c) + -0xf;
  do {
    bVar1 = *pbVar5;
    bVar2 = *pbVar4;
    if ((ulonglong)bVar1 - (ulonglong)bVar2 != 0) break;
    pbVar5 = pbVar5 + 1;
    pbVar4 = pbVar4 + 1;
  } while (pbVar5 != abStack_24);
  if ((int)((ulonglong)bVar1 - (ulonglong)bVar2) == 0) {
    FUN_8220d1e0(0x6d);
  }
  else {
    iVar6 = param_1 + 0x170;
    FUN_822e3c10(iVar6);
    FUN_822c8aa0(iVar6,0xffffffff82085024);
    FUN_822e2e28(iVar6,1);
    uVar3 = FUN_82322798(0x5ff);
    *(undefined4 *)(param_1 + 0x1d0) = uVar3;
  }
  return;
}



// ===================================================
// 82305110  ->  FUN_82305110  (entree 82305110)
// ===================================================

void FUN_82305110(int param_1)

{
  byte bVar1;
  byte bVar2;
  undefined4 uVar3;
  byte *pbVar4;
  byte *pbVar5;
  int iVar6;
  undefined4 uStack_30;
  int iStack_2c;
  int iStack_28;
  byte abStack_24 [12];
  
  if (*(int *)(param_1 + 0x4c) == 4) {
    FUN_822e35e0();
    iStack_2c = *(int *)(param_1 + 0x158) + -0xf;
    uStack_30 = *(undefined4 *)(param_1 + 0x154);
    iStack_28 = *(int *)(param_1 + 0x15c) + -0xf;
    FUN_822db7e0(&uStack_30);
    pbVar5 = (byte *)&uStack_30;
    pbVar4 = (byte *)(param_1 + 0x160);
    do {
      bVar1 = *pbVar5;
      bVar2 = *pbVar4;
      if ((ulonglong)bVar1 - (ulonglong)bVar2 != 0) break;
      pbVar5 = pbVar5 + 1;
      pbVar4 = pbVar4 + 1;
    } while (pbVar5 != abStack_24);
    if ((int)((ulonglong)bVar1 - (ulonglong)bVar2) != 0) {
      FUN_822db258(1,0xffffffffffffffff);
    }
    FUN_8220d1e0(0x6d);
  }
  else if (*(int *)(param_1 + 0x4c) == 3) {
    FUN_822e35e0(param_1);
    iVar6 = param_1 + 0x268;
    FUN_822e3c10(iVar6);
    FUN_822c8aa0(iVar6,0xffffffff82085024);
    FUN_822e2e28(iVar6,1);
    uVar3 = FUN_82322798(0x601);
    *(undefined4 *)(param_1 + 0x2c8) = uVar3;
  }
  return;
}



// ===================================================
// 82305208  ->  FUN_82305208  (entree 82305208)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

int FUN_82305208(int param_1,ulonglong param_2)

{
  FUN_82154d98(param_1 + 0x268);
  FUN_82154d98(param_1 + 0x170);
  FUN_822c73a8(param_1 + 0xdc);
  if (*(int *)(param_1 + 200) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 200) = 0;
  *(undefined4 *)(param_1 + 0xcc) = 0;
  *(undefined4 *)(param_1 + 0xd0) = 0;
  FUN_822c73a8(param_1 + 0x58);
  FUN_822c73a8(param_1);
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 823052B8  ->  FUN_823052b8  (entree 823052b8)
// ===================================================

undefined8 FUN_823052b8(int *param_1)

{
  int *piVar1;
  
  FUN_822e36a8(param_1,0);
  FUN_822e38d8(param_1);
  piVar1 = (int *)FUN_822dae30();
  param_1[0x55] = *piVar1;
  param_1[0x56] = piVar1[1];
  param_1[0x57] = piVar1[2];
  param_1[0x58] = piVar1[3];
  param_1[0x59] = param_1[0x55];
  param_1[0x5a] = param_1[0x56];
  param_1[0x5b] = param_1[0x57];
  param_1[0x5c] = param_1[0x58];
  param_1[0x51] = 5;
  *(undefined1 *)(param_1 + 0x52) = 0;
  param_1[0x13] = 0;
  FUN_822e3208(param_1 + 0xdc);
  (**(code **)(*param_1 + 0x18))(param_1,0);
  param_1[0x5d] = (int)&DAT_82ac8510;
  FUN_822fa900(0xffffffff82ac8510,0xffffffff8208d72c,0xffffffff8208da8c,1,0);
  FUN_822e3c10(param_1 + 0x5e);
  FUN_822e3c10(param_1 + 0x9c);
  return 1;
}



// ===================================================
// 823053A8  ->  FUN_823053a8  (entree 823053a8)
// ===================================================

undefined8 FUN_823053a8(int param_1)

{
  char cVar3;
  int iVar1;
  int iVar2;
  int aiStack_50 [14];
  
  cVar3 = FUN_822c7b98(param_1 + 0x178);
  if (cVar3 == '\0') {
    iVar1 = FUN_822e2e38(param_1 + 0x178);
    if (iVar1 == 0) {
      FUN_822db810(param_1 + 0x164);
      FUN_8220d1e0(0x6d);
    }
    else {
      iVar1 = param_1 + 0x270;
      cVar3 = FUN_822c7b98(iVar1);
      if (cVar3 == '\0') {
        iVar2 = FUN_822e2e38(iVar1);
        if (-1 < iVar2) {
          iVar2 = FUN_822e2e38(iVar1);
          if (iVar2 == 0) {
            *(undefined4 *)(param_1 + 0x158) = 0x14;
            *(undefined4 *)(param_1 + 0x154) = 0;
            *(undefined4 *)(param_1 + 0x15c) = 0x14;
            *(undefined4 *)(param_1 + 0x160) = 0x14;
            FUN_822db810();
          }
          FUN_822e3c10(iVar1);
        }
        cVar3 = FUN_822fa080(*(undefined4 *)(param_1 + 0x174));
        if (cVar3 != '\0') {
          FUN_822e33f8(param_1);
        }
      }
    }
  }
  aiStack_50[0] = 0x14a;
  aiStack_50[1] = 0x14c;
  aiStack_50[2] = 0x14d;
  aiStack_50[3] = 0x14e;
  aiStack_50[4] = 0x14f;
  aiStack_50[5] = 0x150;
  aiStack_50[6] = 4;
  aiStack_50[7] = 4;
  aiStack_50[8] = 4;
  aiStack_50[9] = 4;
  aiStack_50[10] = 2;
  aiStack_50[0xb] = 2;
  if (*(int *)(param_1 + 0x4c) == 0) {
    aiStack_50[0] = *(int *)(param_1 + 0x154) + 0x14a;
  }
  FUN_822e3618(param_1,aiStack_50[*(int *)(param_1 + 0x4c)]);
  FUN_822e3660(param_1,aiStack_50[*(int *)(param_1 + 0x4c) + 6]);
  return 0;
}



// ===================================================
// 82305540  ->  FUN_82305540  (entree 82305540)
// ===================================================

undefined8 FUN_82305540(int param_1)

{
  FUN_822e3968();
  FUN_822fa018(*(undefined4 *)(param_1 + 0x174),0);
  FUN_822e3228(param_1 + 0x370);
  return 1;
}



// ===================================================
// 82305588  ->  FUN_82305588  (entree 82305588)
// ===================================================

/* WARNING: Function: __savegprlr_23 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_23 replaced with injection: x360_restgprlr */

void FUN_82305588(void)

{
  double dVar1;
  int iVar3;
  char cVar4;
  undefined8 uVar2;
  int iVar5;
  ulonglong uVar6;
  double dVar7;
  double dVar8;
  double dVar9;
  double dVar10;
  double dVar11;
  double dVar12;
  float fStack_b0;
  float fStack_ac;
  float fStack_a8;
  uint auStack_a0 [40];
  
  iVar3 = FUN_826018c0();
  cVar4 = FUN_822fa080(*(undefined4 *)(iVar3 + 0x174));
  if (cVar4 != '\0') {
    dVar7 = (double)DAT_82000a34;
    fStack_b0 = DAT_82000a34;
    fStack_ac = DAT_82000a34;
    fStack_a8 = DAT_82000a34;
    auStack_a0[0] = 0x4f4;
    auStack_a0[1] = 0x4f7;
    auStack_a0[2] = 0x50d;
    auStack_a0[3] = 0x523;
    auStack_a0[4] = 0x539;
    auStack_a0[5] = 0x53a;
    FUN_822c2a08(9);
    FUN_8223bc10(0xe);
    FUN_8223c130(9);
    FUN_822faa88(*(undefined4 *)(iVar3 + 0x174),&fStack_b0,0xffffffff8208dab4,1);
    FUN_8223beb8((double)fStack_b0,(double)fStack_ac);
    FUN_8223c048(0xffffffffffbff560);
    uVar2 = FUN_82322798(0x4ed);
    FUN_8223fe30(0xffffffff8208476c,uVar2);
    FUN_8223c048(0xffffffffffffffff);
    dVar8 = (double)FUN_822e4a08(iVar3);
    FUN_822faa88(*(undefined4 *)(iVar3 + 0x174),&fStack_b0,0xffffffff8208daa0,0);
    dVar9 = (double)DAT_82000f1c;
    dVar11 = (double)DAT_82011814;
    dVar12 = (double)DAT_82010304;
    iVar5 = 0;
    dVar10 = (double)DAT_82000b08;
    do {
      if (iVar5 == 4) {
        FUN_822faa88(*(undefined4 *)(iVar3 + 0x174),&fStack_b0,0xffffffff8208da90,0);
      }
      FUN_8223beb8((double)fStack_b0,(double)fStack_ac);
      uVar6 = (ulonglong)auStack_a0[iVar5];
      if (iVar5 < 4) {
        uVar2 = FUN_82322798(uVar6);
        FUN_8223fe30(0xffffffff82000f08,uVar2);
        uVar2 = FUN_82322798(*(uint *)((iVar5 + 0x55) * 4 + iVar3) + uVar6 + 1);
        if (iVar5 == *(int *)(iVar3 + 0x4c)) {
          FUN_82322798(uVar6);
          FUN_822e37e0((double)fStack_b0,(double)fStack_ac,dVar10,iVar3 + 0x368);
          dVar7 = (double)fStack_ac;
        }
        FUN_8223beb8((double)(float)(dVar8 - dVar12),(double)fStack_ac);
        FUN_8223fe30(0xffffffff820117f8,uVar2);
        dVar1 = (double)fStack_ac + dVar11;
      }
      else {
        uVar2 = FUN_82322798(uVar6);
        FUN_8223fe30(0xffffffff8208476c,uVar2);
        if (iVar5 == *(int *)(iVar3 + 0x4c)) {
          FUN_82322798(uVar6);
          FUN_822e37e0((double)fStack_b0,(double)fStack_ac,dVar10,iVar3 + 0x368);
        }
        dVar1 = (double)fStack_ac + dVar9;
      }
      fStack_ac = (float)dVar1;
      iVar5 = iVar5 + 1;
    } while (iVar5 < 6);
    if (*(int *)(iVar3 + 0x4c) < 4) {
      FUN_822e5380((double)(float)(dVar8 - dVar12),dVar7);
      FUN_822c2a18();
      FUN_8260190c();
      return;
    }
    FUN_822e3228(iVar3 + 0x370);
    FUN_822c2a18();
  }
  FUN_8260190c();
  return;
}



// ===================================================
// 82305868  ->  FUN_82305868  (entree 82305868)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82305868(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  int aiStack_30 [12];
  
  aiStack_30[0] = 1;
  aiStack_30[1] = 0x14;
  aiStack_30[2] = 0x14;
  aiStack_30[3] = 0x14;
  if (param_2 != 0) {
    FUN_822e35b0();
    FUN_822e3228(param_1 + 0x370);
  }
  iVar1 = *(int *)(param_1 + 0x4c);
  if (iVar1 < 4) {
    iVar2 = aiStack_30[iVar1];
    *(undefined4 *)(param_1 + 0x50) = *(undefined4 *)((iVar1 + 0x55) * 4 + param_1);
    *(int *)(param_1 + 0x14c) = iVar2;
  }
  else {
    *(undefined4 *)(param_1 + 0x14c) = 0;
  }
  *(undefined1 *)(param_1 + 0x150) = 0;
  FUN_822e32b8(param_1 + 0x370,0xffffffffffffffff,0 < *(int *)(param_1 + 0x50));
  FUN_822e32b8(param_1 + 0x370,1,*(int *)(param_1 + 0x50) < aiStack_30[*(int *)(param_1 + 0x4c)]);
  return 1;
}



// ===================================================
// 82305940  ->  FUN_82305940  (entree 82305940)
// ===================================================

undefined8 FUN_82305940(int *param_1,undefined8 param_2)

{
  FUN_822e35b0();
  if (param_1[0x13] < 4) {
    param_1[param_1[0x13] + 0x55] = param_1[0x14];
    FUN_821ccba8(param_1 + 0xdc,param_2);
    (**(code **)(*param_1 + 0x18))(param_1,0);
    FUN_822db810(param_1 + 0x55);
  }
  return 1;
}



// ===================================================
// 823059C8  ->  FUN_823059c8  (entree 823059c8)
// ===================================================

void FUN_823059c8(int param_1)

{
  byte bVar1;
  byte bVar2;
  undefined4 uVar3;
  byte *pbVar4;
  byte *pbVar5;
  int iVar6;
  
  thunk_FUN_822d11a8();
  pbVar5 = (byte *)(param_1 + 0x154);
  pbVar4 = (byte *)(param_1 + 0x164);
  do {
    bVar1 = *pbVar5;
    bVar2 = *pbVar4;
    if ((ulonglong)bVar1 - (ulonglong)bVar2 != 0) break;
    pbVar5 = pbVar5 + 1;
    pbVar4 = pbVar4 + 1;
  } while (pbVar5 != (byte *)(param_1 + 0x164));
  if ((int)((ulonglong)bVar1 - (ulonglong)bVar2) == 0) {
    FUN_8220d1e0(0x6d);
  }
  else {
    iVar6 = param_1 + 0x178;
    FUN_822e3c10(iVar6);
    FUN_822c8aa0(iVar6,0xffffffff82085024);
    FUN_822e2e28(iVar6,1);
    uVar3 = FUN_82322798(0x5ff);
    *(undefined4 *)(param_1 + 0x1d8) = uVar3;
  }
  return;
}



// ===================================================
// 82305A70  ->  FUN_82305a70  (entree 82305a70)
// ===================================================

void FUN_82305a70(int param_1)

{
  byte bVar1;
  byte bVar2;
  undefined4 uVar3;
  byte *pbVar4;
  byte *pbVar5;
  int iVar6;
  
  if (*(int *)(param_1 + 0x4c) == 5) {
    FUN_822e35e0();
    pbVar5 = (byte *)(param_1 + 0x154);
    FUN_822db810(pbVar5);
    pbVar4 = (byte *)(param_1 + 0x164);
    do {
      bVar1 = *pbVar5;
      bVar2 = *pbVar4;
      if ((ulonglong)bVar1 - (ulonglong)bVar2 != 0) break;
      pbVar5 = pbVar5 + 1;
      pbVar4 = pbVar4 + 1;
    } while (pbVar5 != (byte *)(param_1 + 0x164));
    if ((int)((ulonglong)bVar1 - (ulonglong)bVar2) != 0) {
      FUN_822db258(1,0xffffffffffffffff);
    }
    FUN_8220d1e0(0x6d);
  }
  else if (*(int *)(param_1 + 0x4c) == 4) {
    FUN_822e35e0(param_1);
    iVar6 = param_1 + 0x270;
    FUN_822e3c10(iVar6);
    FUN_822c8aa0(iVar6,0xffffffff82085024);
    FUN_822e2e28(iVar6,1);
    uVar3 = FUN_82322798(0x602);
    *(undefined4 *)(param_1 + 0x2d0) = uVar3;
  }
  return;
}



// ===================================================
// 82305B50  ->  FUN_82305b50  (entree 82305b50)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

int FUN_82305b50(int param_1,ulonglong param_2)

{
  FUN_82154d98(param_1 + 0x270);
  FUN_82154d98(param_1 + 0x178);
  FUN_822c73a8(param_1 + 0xdc);
  if (*(int *)(param_1 + 200) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 200) = 0;
  *(undefined4 *)(param_1 + 0xcc) = 0;
  *(undefined4 *)(param_1 + 0xd0) = 0;
  FUN_822c73a8(param_1 + 0x58);
  FUN_822c73a8(param_1);
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 82305BD8  ->  FUN_82305bd8  (entree 82305bd8)
// ===================================================

undefined1 FUN_82305bd8(void)

{
  char cVar2;
  int iVar1;
  
  cVar2 = FUN_823010c8();
  if (cVar2 != '\0') {
    return 2;
  }
  FUN_821dc920();
  FUN_821dc9f8();
  iVar1 = FUN_821dc9c0();
  return iVar1 == 2;
}



// ===================================================
// 82305C78  ->  FUN_82305c78  (entree 82305c78)
// ===================================================

undefined8 FUN_82305c78(int param_1)

{
  int iVar2;
  char cVar4;
  undefined4 uVar3;
  undefined8 uVar1;
  char cVar5;
  uint uVar6;
  double dVar7;
  
  iVar2 = FUN_822fcdd8();
  if (iVar2 == 2) {
    cVar4 = FUN_822d0c80(1);
  }
  else {
    uVar1 = FUN_821dc920();
    cVar5 = FUN_821dc930(uVar1,0);
    uVar1 = FUN_821dc920();
    cVar4 = FUN_821dc930(uVar1,1);
    if ((cVar5 != '\0') && (cVar4 != '\0')) {
      uVar6 = 2;
      goto LAB_82305cb4;
    }
  }
  uVar6 = cVar4 == '\0' ^ 1;
LAB_82305cb4:
  *(uint *)(param_1 + 0x54) = uVar6;
  FUN_822d0c30(uVar6);
  *(undefined4 *)(param_1 + 0x50) = 0xffffffff;
  *(undefined4 *)(param_1 + 0x4c) = 0;
  dVar7 = (double)FUN_822c6f78();
  *(float *)(param_1 + 0x58) = (float)dVar7;
  *(undefined4 *)(param_1 + 0x5c) = 0;
  *(undefined1 *)(param_1 + 0x248) = 0;
  FUN_822e2e98(param_1 + 0xf4);
  uVar3 = FUN_82322798(0);
  *(undefined4 *)(param_1 + 0x140) = uVar3;
  return 1;
}



// ===================================================
// 82305D50  ->  FUN_82305d50  (entree 82305d50)
// ===================================================

undefined8 FUN_82305d50(int param_1)

{
  *(undefined4 *)(param_1 + 0x4c) = 0;
  *(undefined1 *)(param_1 + 0x248) = 0;
  FUN_822d0c30(*(undefined4 *)(param_1 + 0x54));
  FUN_822c6d60((double)*(float *)(param_1 + 0x58));
  FUN_822c7d50(param_1 + 0xf4);
  return 1;
}



// ===================================================
// 82305DA0  ->  FUN_82305da0  (entree 82305da0)
// ===================================================

undefined8 FUN_82305da0(undefined8 param_1)

{
  char cVar2;
  undefined8 uVar1;
  
  cVar2 = FUN_822c80d0();
  if (cVar2 != '\0') {
    return 0;
  }
  uVar1 = FUN_822c8aa0(param_1,0xffffffff8208db0c);
  return uVar1;
}



// ===================================================
// 82305E00  ->  FUN_82305e00  (entree 82305e00)
// ===================================================

undefined8 FUN_82305e00(longlong param_1)

{
  char cVar2;
  undefined8 uVar1;
  
  cVar2 = FUN_822c80d0();
  if (cVar2 == '\0') {
    return 0;
  }
  uVar1 = FUN_822e37b8(param_1 + 0x5c);
  return uVar1;
}



// ===================================================
// 82305E58  ->  FUN_82305e58  (entree 82305e58)
// ===================================================

undefined8 FUN_82305e58(int param_1)

{
  undefined4 auStack_20 [2];
  
  auStack_20[0] = 10;
  auStack_20[1] = 0xb;
  FUN_822e3ad8(param_1 + 0x5c);
  FUN_822e3778(param_1 + 0x5c,auStack_20[*(int *)(param_1 + 0x4c)],0);
  *(undefined4 *)(param_1 + 0x54) = 0;
  *(undefined1 *)(param_1 + 0x90) = 0;
  *(undefined1 *)(param_1 + 0x91) = 0;
  *(undefined1 *)(param_1 + 0x92) = 0;
  *(undefined1 *)(param_1 + 0x93) = 0;
  if (*(int *)(param_1 + 0x58) == 2) {
    *(undefined1 *)(param_1 + 0x92) = 1;
  }
  return 1;
}



// ===================================================
// 82305EF0  ->  FUN_82305ef0  (entree 82305ef0)
// ===================================================

void FUN_82305ef0(int param_1)

{
  char cVar2;
  int iVar1;
  
  *(undefined4 *)(param_1 + 0x54) = 0;
  do {
    cVar2 = FUN_822d0e18((int *)(param_1 + 0x50),3,0);
    if (cVar2 == '\0') break;
  } while (*(char *)(*(int *)(param_1 + 0x50) + param_1 + 0x90) != '\0');
  if (cVar2 == '\0') {
    iVar1 = FUN_822d1830();
    if (-1 < iVar1) {
      FUN_822d1198();
      *(undefined4 *)(param_1 + 0x54) = 1;
    }
  }
  else {
    FUN_822d1188();
  }
  return;
}



// ===================================================
// 82305F88  ->  FUN_82305f88  (entree 82305f88)
// ===================================================

void FUN_82305f88(ulonglong param_1)

{
  undefined **ppuStack_20;
  undefined4 uStack_1c;
  
  if (((param_1 & 0xffffffff) != 0) &&
     (trapWord(6,param_1,0), 0xffffffff / (param_1 & 0xffffffff) < 0x20)) {
    uStack_1c = 0;
    ppuStack_20 = &PTR_FUN_82000a28;
    FUN_82144880(&ppuStack_20);
    ppuStack_20 = &PTR_FUN_82000a18;
  }
  FUN_82142ee0((param_1 & 0x7ffffff) << 5);
  return;
}



// ===================================================
// 82306000  ->  FUN_82306000  (entree 82306000)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

undefined4 FUN_82306000(int param_1)

{
  char cVar3;
  int iVar1;
  int iVar2;
  undefined4 uVar4;
  
  uVar4 = *(undefined4 *)(param_1 + 0x4c);
  if ((*(int *)(param_1 + 0xb4) != 0) && (iVar2 = *(int *)(param_1 + 0xb0), -1 < iVar2)) {
    cVar3 = FUN_822c80d0(param_1 + 0x60);
    if (cVar3 == '\0') {
      cVar3 = '\0';
    }
    else {
      cVar3 = FUN_822e37b8(param_1 + 0xbc);
    }
    if (cVar3 != '\0') {
      iVar1 = FUN_82305bd8(param_1);
      if (iVar1 == 1) {
        iVar2 = iVar2 + 4;
      }
      else if (iVar1 == 2) {
        iVar2 = iVar2 + 8;
      }
      switch(iVar2) {
      case 1:
        return 3;
      case 2:
        return 5;
      case 3:
        return 0xf;
      default:
        uVar4 = 7;
        break;
      case 5:
        return 9;
      case 6:
        return 0xb;
      case 7:
        iVar2 = FUN_822fcdd8();
        if (iVar2 == 1) {
          return 0xf;
        }
        return 0x11;
      case 9:
        return 0xd;
      case 0xb:
        return 0x11;
      }
    }
  }
  return uVar4;
}



// ===================================================
// 82306160  ->  FUN_82306160  (entree 82306160)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

bool FUN_82306160(longlong param_1)

{
  char cVar1;
  longlong lVar2;
  
  lVar2 = param_1 + 0x5c;
  FUN_822e4d70(lVar2);
  cVar1 = FUN_822e2dd8(lVar2);
  if (cVar1 != '\0') {
    FUN_82305ef0(param_1);
    return false;
  }
  cVar1 = FUN_822e2df0(lVar2);
  return cVar1 != '\0';
}



// ===================================================
// 823061D0  ->  FUN_823061d0  (entree 823061d0)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

undefined8 FUN_823061d0(int param_1)

{
  bool bVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  uint uVar5;
  undefined4 uVar6;
  longlong lVar4;
  int iVar7;
  char cVar8;
  undefined8 uVar9;
  double dVar10;
  undefined4 auStack_60 [4];
  undefined4 uStack_50;
  undefined1 uStack_4c;
  undefined1 uStack_4b;
  undefined1 uStack_4a;
  float fStack_48;
  float fStack_44;
  float fStack_40;
  undefined2 uStack_3c;
  undefined2 uStack_3a;
  
  uVar2 = FUN_821dc920();
  uVar9 = 0;
  switch(*(undefined4 *)(param_1 + 0x4c)) {
  case 0:
    cVar8 = FUN_821e3c78();
    if (cVar8 != '\0') {
      lVar4 = 0;
      *(undefined4 *)(param_1 + 0x50) = 0xffffffff;
      do {
        cVar8 = FUN_822d0c80(lVar4);
        if (((cVar8 != '\0') && (iVar7 = FUN_822d0c08(lVar4), -1 < iVar7)) &&
           (cVar8 = FUN_822d0798(lVar4), cVar8 == '\0')) {
          *(int *)(param_1 + 0x50) = (int)lVar4;
          break;
        }
        lVar4 = lVar4 + 1;
      } while ((int)lVar4 < 2);
      if (*(int *)(param_1 + 0x50) < 0) {
        uVar6 = FUN_822d0ca8(0x200);
        *(undefined4 *)(param_1 + 0x50) = uVar6;
      }
      if (-1 < *(int *)(param_1 + 0x50)) {
        uVar6 = FUN_82305bd8(param_1);
        *(undefined4 *)(param_1 + 0xb0) = 0;
        *(undefined4 *)(param_1 + 0xb8) = uVar6;
        *(undefined4 *)(param_1 + 0xac) = *(undefined4 *)(param_1 + 0x50);
        dVar10 = (double)FUN_822c6f78();
        *(float *)(param_1 + 0x58) = (float)dVar10;
        FUN_822c6d60((double)DAT_82000a34);
        FUN_821ca7f8(0x24,0);
        FUN_822d0c30(*(undefined4 *)(param_1 + 0x50));
        *(undefined4 *)(param_1 + 0x4c) = 1;
      }
    }
    break;
  case 1:
    cVar8 = FUN_82305da0(param_1 + 0x60);
    if (cVar8 != '\0') {
      FUN_822c8aa0(param_1 + 0xf4,0xffffffff8208db2c);
      *(undefined4 *)(param_1 + 0x4c) = 2;
    }
    break;
  case 2:
    iVar7 = FUN_822d0ca8(0x200);
    if (iVar7 < 0) {
      uVar6 = FUN_82306000(param_1);
      *(undefined4 *)(param_1 + 0x4c) = uVar6;
    }
    else {
      cVar8 = FUN_82305e00(param_1 + 0x60);
      if (cVar8 != '\0') {
        FUN_822d11a8();
        *(undefined4 *)(param_1 + 0x4c) = 7;
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x248) == '\0') {
      lVar4 = 0;
      iVar7 = param_1 + 0x24c;
      do {
        FUN_8233c520(iVar7,lVar4);
        lVar4 = lVar4 + 1;
        iVar7 = iVar7 + 0x10c;
      } while ((int)lVar4 < 2);
      *(undefined1 *)(param_1 + 0x248) = 1;
    }
    iVar7 = *(int *)(param_1 + 0x50);
    if ((iVar7 == 0) || (iVar7 == 1)) {
      iVar7 = iVar7 * 0x10c + param_1;
      *(undefined4 *)(iVar7 + 0x298) = 2;
      FUN_822c8ab8(iVar7 + 0x24c,0xffffffff8208daf4,0);
      *(undefined4 *)(param_1 + 0x4c) = 4;
    }
    break;
  case 4:
    iVar7 = *(int *)(param_1 + 0x50) * 0x10c + param_1;
    cVar8 = FUN_822c80d0(iVar7 + 0x24c);
    if ((cVar8 == '\0') && (*(int *)(iVar7 + 0x2b4) != 3)) {
      *(undefined4 *)(param_1 + 0x4c) = 1;
    }
    break;
  case 5:
    FUN_823029b8(*(undefined4 *)(param_1 + 0x50));
    *(undefined4 *)(param_1 + 0x4c) = 6;
    break;
  case 6:
    cVar8 = FUN_82303c00(0);
    if (cVar8 != '\0') {
      FUN_823029d8();
      *(undefined4 *)(param_1 + 0x4c) = 1;
    }
    break;
  case 7:
    *(undefined4 *)(param_1 + 0x5c) = 10;
    *(undefined4 *)(param_1 + 0x4c) = 8;
  case 8:
    lVar4 = (ulonglong)*(uint *)(param_1 + 0x5c) - 1;
    *(int *)(param_1 + 0x5c) = (int)lVar4;
    if (lVar4 < 1) {
      *(undefined4 *)(param_1 + 0x5c) = 0;
      FUN_822c6d60((double)*(float *)(param_1 + 0x58));
      FUN_821ca7f8(0x25,0);
      FUN_822d0c30(*(undefined4 *)(param_1 + 0x54));
      FUN_822c7d50(param_1 + 0xf4);
      *(undefined4 *)(param_1 + 0x4c) = 0;
    }
    break;
  case 9:
    FUN_822c7d50(param_1 + 0xf4);
    *(undefined4 *)(param_1 + 0x4c) = 10;
  case 10:
    cVar8 = FUN_822c8178(param_1 + 0x60);
    if (cVar8 == '\0') {
      FUN_822c6d60((double)*(float *)(param_1 + 0x58));
      FUN_821ca7f8(0x25,0);
      FUN_822d0c30(*(undefined4 *)(param_1 + 0x54));
      uVar3 = FUN_8227f378();
      bVar1 = true;
      uStack_4b = 0;
      uStack_4a = 0;
      uStack_3c = 0;
      uStack_50 = 2;
      uStack_4c = 1;
      fStack_48 = DAT_82000a34;
      fStack_44 = DAT_82000a34;
      fStack_40 = DAT_82000a34;
      uStack_3a = 0xc9;
      FUN_8227f9d0();
      FUN_8227f480(uVar3,&uStack_50,&uStack_50);
      FUN_8227fa28(uVar3,1);
      iVar7 = FUN_821dc9f8(uVar2);
      uVar6 = *(undefined4 *)(iVar7 + 0xae0);
      cVar8 = FUN_822e1490();
      if (cVar8 == '\0') {
        auStack_60[0] = 0;
        FUN_822912a8(uVar6,auStack_60);
        uVar3 = FUN_822912d0(uVar6);
        cVar8 = FUN_821e1bf8(uVar2,auStack_60[0],uVar3,1);
        if (cVar8 == '\0') {
          bVar1 = false;
        }
      }
      if (bVar1) {
        FUN_821ca7f8(0x12,0);
        FUN_822b1610(0);
        FUN_822b1610(1);
        FUN_822b1b10();
        FUN_821ed240(0);
        FUN_821ed240(1);
        FUN_8220cc10();
        FUN_82291330(uVar6,0);
        FUN_821e3f58();
        *(undefined4 *)(param_1 + 0x4c) = 0;
      }
      else {
        *(undefined4 *)(param_1 + 0x4c) = 0x11;
      }
    }
    break;
  case 0xb:
    FUN_822ddf28();
    *(undefined4 *)(param_1 + 0x4c) = 0xc;
    break;
  case 0xc:
    cVar8 = FUN_822ddf40();
    if (cVar8 != '\0') {
      FUN_822ddf78();
      *(undefined4 *)(param_1 + 0x4c) = 1;
    }
    break;
  case 0xd:
    FUN_822c7d50(param_1 + 0xf4);
    *(undefined4 *)(param_1 + 0x4c) = 0xe;
  case 0xe:
    cVar8 = FUN_822c8178(param_1 + 0x60);
    if (cVar8 == '\0') {
      FUN_822c6d60((double)*(float *)(param_1 + 0x58));
      FUN_821dc9f0(uVar2);
      FUN_821dc8b8();
      FUN_821da3b0(PTR_DAT_8200f3bc);
      FUN_8220d1e0(0x67);
    }
    break;
  case 0xf:
    iVar7 = param_1 + 0x150;
    cVar8 = FUN_822c80d0(iVar7);
    if (cVar8 == '\0') {
      uVar5 = FUN_822fcdd8();
      if (uVar5 == 0) {
        lVar4 = 0x5c8;
      }
      else if (uVar5 == 1) {
        lVar4 = FUN_82305bd8(param_1);
        lVar4 = (-(ulonglong)(lVar4 != 0) & 2) + 0x5cd;
      }
      else if (uVar5 < 3) {
        cVar8 = FUN_823178a0(0);
        if (cVar8 == '\0') {
          cVar8 = FUN_823178a0(1);
          lVar4 = (-(ulonglong)(cVar8 != '\0') & 3) + 0x5e2;
        }
        else {
          lVar4 = 0x5e4;
        }
      }
      else {
        lVar4 = 0x5cc;
      }
      FUN_822e3c10(iVar7);
      FUN_822e2e28(iVar7,1);
      uVar6 = FUN_82322798(lVar4);
      *(undefined4 *)(param_1 + 0x1b0) = uVar6;
      FUN_822c8aa0(iVar7,0xffffffff8208db18);
      *(undefined4 *)(param_1 + 0x4c) = 0x10;
    }
    break;
  case 0x10:
    lVar4 = FUN_822e2e38(param_1 + 0x150);
    if ((int)lVar4 != -1) {
      *(uint *)(param_1 + 0x4c) = (-(uint)(lVar4 != 0) & 0xfffffff0) + 0x11;
    }
    break;
  case 0x11:
    FUN_821dc9f8(uVar2);
    iVar7 = FUN_821dc9c0();
    if (iVar7 == 1) {
      iVar7 = FUN_821dc9c0(uVar2);
      FUN_8218dea0(*(undefined4 *)(&DAT_820036c0 + iVar7 * 4));
      FUN_821899a8();
    }
    FUN_821ed240(0);
    FUN_821ed240(1);
    iVar7 = FUN_822fcdd8();
    if (iVar7 == 2) {
      cVar8 = FUN_823163c8();
      if (cVar8 != '\0') {
        FUN_82316380();
        FUN_82317f88();
      }
      uVar2 = 0x54;
    }
    else {
      if (iVar7 == 4) {
        FUN_8220d1a8(4);
        cVar8 = FUN_822dcef8();
        if (cVar8 == '\0') {
          cVar8 = FUN_823010c8();
          if (cVar8 == '\0') {
            FUN_8220d1e0(0x48);
          }
          else {
            FUN_8220d1e0(0x4c);
          }
        }
        else {
          FUN_8220d1e0(0x4a);
        }
        break;
      }
      uVar2 = 0x14;
      DAT_827a9a09 = 0;
      DAT_827a9f31 = 0;
    }
    FUN_8220d1e0(uVar2);
    uVar9 = 1;
  }
  if (*(int *)(param_1 + 0x4c) != 2) {
    FUN_822c7d50(param_1 + 0xf4);
  }
  return uVar9;
}



// ===================================================
// 823068C0  ->  FUN_823068c0  (entree 823068c0)
// ===================================================

/* WARNING: Function: __savegprlr_24 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_24 replaced with injection: x360_restgprlr */

void FUN_823068c0(void)

{
  int iVar3;
  char cVar5;
  undefined8 uVar1;
  int iVar4;
  undefined8 uVar2;
  float fVar6;
  int iVar7;
  double dVar8;
  double dVar9;
  double dVar10;
  double dVar11;
  double dVar12;
  double dVar13;
  float fStack_d0;
  float fStack_cc;
  float fStack_c8;
  float fStack_c4;
  float fStack_c0;
  float fStack_bc;
  int aiStack_b0 [44];
  
  iVar3 = FUN_826018c0();
  iVar7 = iVar3 + 0x5c;
  cVar5 = FUN_822e2dd8(iVar7);
  if (cVar5 != '\0') {
    uVar1 = FUN_822c29e8();
    FUN_822c29d8(2);
    FUN_822c2a08(9);
    FUN_8223bc10(0xe);
    FUN_8223c130(9);
    aiStack_b0[0] = 0x1a6;
    aiStack_b0[3] = 0x1a9;
    aiStack_b0[4] = 0x1af;
    aiStack_b0[6] = 0x1ad;
    aiStack_b0[7] = 0x1a9;
    aiStack_b0[1] = 0x1a7;
    aiStack_b0[8] = 0x1af;
    aiStack_b0[2] = 0x1a8;
    aiStack_b0[5] = 0x1b0;
    aiStack_b0[9] = 0x1b0;
    aiStack_b0[10] = 0x1da0;
    aiStack_b0[0xb] = 0x1b4;
    iVar4 = FUN_822fcdd8();
    if (iVar4 == 0) {
      aiStack_b0[3] = 0x1b2;
    }
    else if (iVar4 == 1) {
      aiStack_b0[7] = 0x1b3;
      aiStack_b0[3] = 0x1b3;
    }
    else if (iVar4 == 2) {
      aiStack_b0[3] = 0x1aa;
      cVar5 = FUN_823178a0(1);
      if (cVar5 != '\0') {
        aiStack_b0[3] = 0x1ac;
      }
    }
    else if (iVar4 == 4) {
      cVar5 = FUN_822dcef8();
      aiStack_b0[7] = (-(uint)(cVar5 != '\0') & 0xfffffffd) + 0x1b1;
    }
    dVar11 = (double)DAT_8208db4c;
    fStack_d0 = DAT_82000a34;
    fStack_cc = DAT_82000a34;
    fStack_c8 = DAT_82000a34;
    fStack_c4 = DAT_82000a34;
    fStack_c0 = DAT_82000a34;
    fStack_bc = DAT_82000a34;
    FUN_822e39c0(iVar7,&fStack_d0,0xffffffff8208db50,1);
    FUN_822e39c0(iVar7,&fStack_c4,0xffffffff8208db3c,1);
    dVar9 = (double)DAT_82011814;
    iVar7 = 0;
    dVar10 = (double)DAT_82000b08;
    dVar8 = (double)DAT_82000f0c;
    do {
      if (*(char *)(iVar3 + 0x90 + iVar7) == '\0') {
        uVar2 = FUN_82322798(aiStack_b0[*(int *)(iVar3 + 0x58) * 4 + iVar7]);
        FUN_8223c048(0xffffffffffffffff);
        if (iVar7 == 3) {
          dVar12 = (double)fStack_c0 - dVar8;
          fVar6 = fStack_c4;
        }
        else {
          dVar12 = (double)fStack_cc + dVar11;
          fVar6 = fStack_d0;
        }
        dVar13 = (double)(float)dVar12;
        dVar12 = (double)fVar6;
        FUN_8223beb8(dVar12,dVar13);
        FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar2);
        if (iVar7 == *(int *)(iVar3 + 0x50)) {
          FUN_822e37e0(dVar12,dVar13,dVar10,iVar3 + 0x88);
        }
      }
      iVar7 = iVar7 + 1;
      dVar11 = (double)(float)(dVar11 + dVar9);
    } while (iVar7 < 4);
    FUN_822c2a18();
    FUN_822c29d8(uVar1);
  }
  FUN_8260190c();
  return;
}



// ===================================================
// 82306B78  ->  FUN_82306b78  (entree 82306b78)
// ===================================================

void FUN_82306b78(undefined4 *param_1,undefined4 *param_2)

{
  for (; param_1 != param_2; param_1 = param_1 + 8) {
    (**(code **)*param_1)(param_1,0);
  }
  return;
}



// ===================================================
// 82306BE0  ->  FUN_82306be0  (entree 82306be0)
// ===================================================

void FUN_82306be0(int param_1)

{
  undefined8 in_r0;
  int iStack_18;
  uint uStack_14;
  
  iStack_18 = param_1 + 0x54;
  *(undefined1 *)(param_1 + 0x84) = 0;
  *(undefined4 *)(param_1 + 0x50) = 0;
  uStack_14 = *(uint *)(param_1 + 0x58);
  if (*(uint *)(param_1 + 0x5c) < uStack_14) {
    trapWord(0x1f,in_r0,0x16);
    trapWord(0x1f,in_r0,0x16);
  }
  FUN_82258c38(&iStack_18,iStack_18,CONCAT44(iStack_18,uStack_14),
               CONCAT44(iStack_18,*(uint *)(param_1 + 0x5c)));
  iStack_18 = param_1 + 0x74;
  uStack_14 = *(uint *)(param_1 + 0x7c);
  if (uStack_14 < *(uint *)(param_1 + 0x78)) {
    trapWord(0x1f,in_r0,0x16);
    trapWord(0x1f,in_r0,0x16);
  }
  FUN_82258c38(&iStack_18,iStack_18,CONCAT44(iStack_18,*(uint *)(param_1 + 0x78)),
               CONCAT44(iStack_18,uStack_14));
  return;
}



// ===================================================
// 82306CA0  ->  FUN_82306ca0  (entree 82306ca0)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_82306ca0(undefined4 *param_1)

{
  undefined1 uStack_30;
  
  *param_1 = &PTR_FUN_8208db64;
  FUN_82306be0();
  FUN_822c73a8(param_1 + 0x2c);
  if (param_1[0x29] != 0) {
    FUN_82306b78(param_1[0x29],param_1[0x2a],param_1 + 0x28,uStack_30);
    FUN_82142f48(param_1[0x29]);
  }
  param_1[0x29] = 0;
  param_1[0x2a] = 0;
  param_1[0x2b] = 0;
  if (param_1[0x1e] != 0) {
    FUN_82142f48();
  }
  param_1[0x1e] = 0;
  param_1[0x1f] = 0;
  param_1[0x20] = 0;
  if (param_1[0x16] != 0) {
    FUN_82142f48();
  }
  param_1[0x16] = 0;
  param_1[0x17] = 0;
  param_1[0x18] = 0;
  FUN_822c73a8(param_1);
  return;
}



// ===================================================
// 82306D50  ->  FUN_82306d50  (entree 82306d50)
// ===================================================

undefined8 FUN_82306d50(undefined8 param_1,ulonglong param_2)

{
  FUN_82306ca0();
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 82306DA0  ->  FUN_82306da0  (entree 82306da0)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_82306da0(int param_1)

{
  int iVar1;
  int iVar2;
  
  iVar1 = 1;
  iVar2 = param_1 + 0x464;
  do {
    iVar2 = iVar2 + -0x10c;
    FUN_82306ca0(iVar2);
    iVar1 = iVar1 + -1;
  } while (-1 < iVar1);
  FUN_82154d98(param_1 + 0x150);
  FUN_822c73a8(param_1 + 0xf4);
  if (*(int *)(param_1 + 0xdc) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 0xdc) = 0;
  *(undefined4 *)(param_1 + 0xe0) = 0;
  *(undefined4 *)(param_1 + 0xe4) = 0;
  FUN_822c73a8(param_1 + 0x60);
  FUN_822c73a8(param_1);
  return;
}



// ===================================================
// 82306E20  ->  FUN_82306e20  (entree 82306e20)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined4 * FUN_82306e20(undefined4 *param_1)

{
  undefined4 *puVar1;
  
  FUN_822c7c68();
  puVar1 = param_1 + 0x2c;
  *param_1 = &PTR_FUN_8208db64;
  param_1[0x16] = 0;
  param_1[0x17] = 0;
  param_1[0x18] = 0;
  param_1[0x1e] = 0;
  param_1[0x1f] = 0;
  param_1[0x20] = 0;
  param_1[0x29] = 0;
  param_1[0x2a] = 0;
  param_1[0x2b] = 0;
  FUN_822c7c68(puVar1);
  *puVar1 = &PTR_FUN_82000eb4;
  FUN_82306be0(param_1);
  param_1[0x19] = 0;
  param_1[0x1a] = 0;
  param_1[0x1b] = 0;
  param_1[0x1c] = 0;
  param_1[0x13] = 2;
  FUN_822e2e98(puVar1);
  param_1[0x22] = 0;
  return param_1;
}



// ===================================================
// 82306EB8  ->  FUN_82306eb8  (entree 82306eb8)
// ===================================================

/* WARNING: Function: __savegprlr_23 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_23 replaced with injection: x360_restgprlr */

undefined4 * FUN_82306eb8(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  
  FUN_822c7c68();
  *param_1 = &PTR_FUN_8208db9c;
  FUN_822c7c68(param_1 + 0x18);
  param_1[0x18] = &PTR_FUN_8208db80;
  param_1[0x37] = 0;
  param_1[0x38] = 0;
  param_1[0x39] = 0;
  FUN_822c7c68(param_1 + 0x3d);
  param_1[0x3d] = &PTR_FUN_82000eb4;
  FUN_821569c0(param_1 + 0x54);
  puVar2 = param_1 + 0x93;
  iVar1 = 1;
  puVar3 = param_1 + 0xaa;
  do {
    FUN_822c7c68(puVar2);
    *puVar2 = &PTR_FUN_8208db64;
    puVar3[-1] = 0;
    *puVar3 = 0;
    puVar3[1] = 0;
    puVar3[7] = 0;
    puVar3[8] = 0;
    puVar3[9] = 0;
    puVar3[0x12] = 0;
    puVar3[0x13] = 0;
    puVar3[0x14] = 0;
    FUN_822c7c68(puVar3 + 0x15);
    puVar3[0x15] = &PTR_FUN_82000eb4;
    FUN_82306be0(puVar2);
    puVar3[-4] = 2;
    puVar3[2] = 0;
    puVar3[3] = 0;
    puVar3[4] = 0;
    puVar3[5] = 0;
    FUN_822e2e98(puVar3 + 0x15);
    iVar1 = iVar1 + -1;
    puVar3[0xb] = 0;
    puVar2 = puVar2 + 0x43;
    puVar3 = puVar3 + 0x43;
  } while (-1 < iVar1);
  return param_1;
}



// ===================================================
// 82306FC0  ->  FUN_82306fc0  (entree 82306fc0)
// ===================================================

undefined8 FUN_82306fc0(undefined8 param_1,ulonglong param_2)

{
  FUN_82306da0();
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 82307028  ->  FUN_82307028  (entree 82307028)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

undefined8 FUN_82307028(int param_1)

{
  uint uVar1;
  int iVar2;
  char cVar4;
  int iVar3;
  int iVar5;
  
  *(undefined4 *)(param_1 + 0x4c) = 0;
  uVar1 = FUN_822da898(*(undefined4 *)(param_1 + 0x50));
  iVar2 = FUN_822fcdd8();
  if ((iVar2 == 1) && (cVar4 = FUN_822fde60(), cVar4 == '\0')) {
    iVar2 = uVar1 + 2;
    if (0x1d < uVar1) {
      iVar2 = 0;
    }
  }
  else {
    iVar2 = FUN_822da6b0(*(undefined4 *)(param_1 + 0x50),0,0);
    iVar2 = iVar2 + 2;
  }
  *(int *)(param_1 + 0x54) = iVar2;
  *(int *)(param_1 + 0x58) = iVar2;
  FUN_822d0828(*(undefined4 *)(param_1 + 0x50));
  *(undefined4 *)(param_1 + 0x5c) = 0;
  *(undefined1 *)(param_1 + 0x61) = 0;
  *(undefined1 *)(param_1 + 0x60) = 1;
  iVar2 = FUN_822fcdd8();
  if (iVar2 != 2) {
    if (iVar2 != 5) goto LAB_823070d0;
    *(undefined1 *)(param_1 + 0x61) = 1;
  }
  *(undefined1 *)(param_1 + 0x60) = 0;
LAB_823070d0:
  if (*(char *)(param_1 + 0x62) != '\0') {
    *(undefined4 *)(param_1 + 0x4c) = 8;
    FUN_822da6b0(*(undefined4 *)(param_1 + 0x50),0xffffffffffffffff,0);
  }
  iVar5 = param_1 + 0x68;
  *(undefined1 *)(param_1 + 99) = 0;
  FUN_822e3ad8(iVar5);
  FUN_822e2e20(iVar5,0);
  iVar2 = param_1 + 0x94;
  FUN_822e3ad8(iVar2);
  FUN_822e2e20(iVar2,0);
  if (*(char *)(param_1 + 0x62) == '\0') {
    iVar3 = FUN_822d0c08(*(undefined4 *)(param_1 + 0x50));
    if (iVar3 < 0) {
      FUN_822e3778(iVar2,(*(int *)(param_1 + 0x50) == 0) + '\x14',0);
      *(undefined4 *)(param_1 + 0x4c) = 4;
      FUN_822e3278(param_1 + 200);
      return 1;
    }
    cVar4 = FUN_822dab40(*(undefined4 *)(param_1 + 0x50));
    if (cVar4 == '\0') {
      *(undefined4 *)(param_1 + 0x4c) = 8;
      FUN_822da6b0(*(undefined4 *)(param_1 + 0x50),0xffffffffffffffff,0);
    }
    else {
      FUN_822e3778(iVar5,(*(int *)(param_1 + 0x50) != 0) + '\x12');
      if ((*(char *)(param_1 + 0x61) != '\0') || (cVar4 = FUN_822fde60(), cVar4 != '\0')) {
        FUN_822e3778(iVar2,(*(int *)(param_1 + 0x50) != 0) + '\x14',0);
        FUN_822e3278(param_1 + 200);
        return 1;
      }
    }
  }
  FUN_822e3278(param_1 + 200);
  return 1;
}



// ===================================================
// 82307228  ->  FUN_82307228  (entree 82307228)
// ===================================================

undefined8 FUN_82307228(int param_1)

{
  FUN_822e3b78(param_1 + 0x68);
  FUN_822e3b78(param_1 + 0x94);
  FUN_822e32e0(param_1 + 200);
  *(undefined1 *)(param_1 + 0x62) = 0;
  FUN_822d0828(*(undefined4 *)(param_1 + 0x50));
  return 1;
}



// ===================================================
// 82307298  ->  FUN_82307298  (entree 82307298)
// ===================================================

void FUN_82307298(int param_1)

{
  char cVar1;
  
  cVar1 = FUN_822c80d0();
  if (cVar1 != '\0') {
    FUN_822d0828(*(undefined4 *)(param_1 + 0x50));
    *(undefined1 *)(param_1 + 99) = 0;
    *(undefined4 *)(param_1 + 0x4c) = 6;
  }
  return;
}



// ===================================================
// 823072E8  ->  FUN_823072e8  (entree 823072e8)
// ===================================================

bool FUN_823072e8(int param_1)

{
  char cVar1;
  bool bVar2;
  
  cVar1 = FUN_822c80d0();
  if (cVar1 == '\0') {
    bVar2 = true;
  }
  else {
    bVar2 = 6 < *(int *)(param_1 + 0x4c);
  }
  return bVar2;
}



// ===================================================
// 82307348  ->  FUN_82307348  (entree 82307348)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82307348(int param_1)

{
  bool bVar1;
  char cVar3;
  int iVar2;
  undefined8 uVar4;
  
  uVar4 = 0;
  bVar1 = false;
  cVar3 = FUN_822c80d0();
  if ((cVar3 == '\0') || (6 < *(int *)(param_1 + 0x4c))) {
    bVar1 = true;
  }
  if (bVar1) {
    return 1;
  }
  if (((*(char *)(param_1 + 99) != '\0') &&
      (iVar2 = FUN_822da8b8(*(undefined4 *)(param_1 + 0x50),(ulonglong)*(uint *)(param_1 + 0x54) - 2
                           ), iVar2 != 0)) && (cVar3 = FUN_821f6110(), cVar3 == '\0')) {
    uVar4 = 1;
  }
  return uVar4;
}



// ===================================================
// 823073E0  ->  FUN_823073e0  (entree 823073e0)
// ===================================================

bool FUN_823073e0(int param_1)

{
  char cVar1;
  
  cVar1 = FUN_822c80d0();
  if (cVar1 == '\0') {
    return false;
  }
  return *(int *)(param_1 + 0x4c) == 9;
}



// ===================================================
// 82307440  ->  FUN_82307440  (entree 82307440)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

undefined8 FUN_82307440(int param_1)

{
  uint uVar1;
  char cVar3;
  int iVar2;
  uint uVar4;
  undefined8 uVar5;
  uint *puVar6;
  
  uVar5 = 0;
  if (*(char *)(param_1 + 100) != '\0') {
    return 0;
  }
  puVar6 = (uint *)(param_1 + 0x54);
  uVar1 = *(uint *)(param_1 + 0x54);
  cVar3 = FUN_822d0e18(puVar6,0x1f,0);
  if (cVar3 != '\0') {
    if ((*(char *)(param_1 + 0x60) != '\0') || (*puVar6 != 1)) goto LAB_82307574;
    uVar4 = 2;
    if ((int)(1 - uVar1) < 1) {
      uVar4 = 0;
    }
    goto LAB_82307570;
  }
  iVar2 = FUN_822d1868();
  if (-1 < iVar2) {
    *puVar6 = 0;
    goto LAB_82307574;
  }
  iVar2 = FUN_822d0ca8(0x40);
  if (iVar2 < 0) {
    iVar2 = FUN_822d0ca8(0x80);
    if (iVar2 < 0) {
      iVar2 = FUN_822d0ca8(0x10);
      if (iVar2 < 0) {
        iVar2 = FUN_822d0ca8(0x20);
        if (iVar2 < 0) goto LAB_82307574;
LAB_8230756c:
        uVar4 = 0x1f;
      }
      else {
        uVar4 = 2;
      }
    }
    else {
      uVar4 = *puVar6 + 4;
      if ((int)uVar4 < 2) goto LAB_82307504;
      if (0x1e < (int)uVar4) goto LAB_8230756c;
      if ((int)uVar4 < 2) {
        uVar4 = 2;
      }
    }
  }
  else {
    uVar4 = *puVar6 - 4;
    if (1 < (int)uVar4) {
      if (0x1e < (int)uVar4) goto LAB_8230756c;
      if (1 < (int)uVar4) goto LAB_82307570;
    }
LAB_82307504:
    uVar4 = 2;
  }
LAB_82307570:
  *puVar6 = uVar4;
LAB_82307574:
  uVar4 = *puVar6;
  if (uVar1 != uVar4) {
    if ((int)uVar4 < 2) {
      FUN_822da6b0(*(undefined4 *)(param_1 + 0x50),0xffffffffffffffff,0);
    }
    else {
      iVar2 = FUN_822da6b0(*(undefined4 *)(param_1 + 0x50),(ulonglong)uVar4 - 2,
                           (ulonglong)uVar4 - (ulonglong)uVar1);
      *puVar6 = iVar2 + 2;
    }
    *(uint *)(param_1 + 0x58) = uVar1;
    if (uVar1 != *puVar6) {
      FUN_822d1188();
      if (1 < *(int *)(param_1 + 0x58)) {
        uVar5 = 0xffffffffffffffff;
        if (*(int *)(param_1 + 0x58) <= (int)*puVar6) {
          uVar5 = 1;
        }
        FUN_822e32d8(param_1 + 200,uVar5);
      }
      if (1 < (int)*puVar6) {
        *(undefined4 *)(param_1 + 0x5c) = 0xf;
      }
      uVar5 = 1;
    }
  }
  return uVar5;
}



// ===================================================
// 82307610  ->  FUN_82307610  (entree 82307610)
// ===================================================

void FUN_82307610(int param_1)

{
  char cVar2;
  int iVar1;
  undefined4 uVar3;
  
  cVar2 = FUN_822e2dd8(param_1 + 0x68);
  if (cVar2 == '\0') {
    return;
  }
  if (1 < *(int *)(param_1 + 0x54)) {
    cVar2 = FUN_821f1cc8(*(undefined4 *)(param_1 + 0x50));
    if (cVar2 == '\0') {
      return;
    }
    cVar2 = FUN_821f1c00(*(undefined4 *)(param_1 + 0x50));
    if (cVar2 != '\0') {
      return;
    }
    iVar1 = FUN_822d0ca8(0x100);
    if ((((-1 < iVar1) && (*(char *)(param_1 + 99) != '\0')) && (*(char *)(param_1 + 0x61) != '\0'))
       && ((iVar1 = FUN_822da8b8(*(undefined4 *)(param_1 + 0x50),
                                 (ulonglong)*(uint *)(param_1 + 0x54) - 2), iVar1 != 0 &&
           (cVar2 = FUN_821f6110(), cVar2 == '\0')))) {
      FUN_822d1198();
      *(undefined4 *)(param_1 + 0x4c) = 1;
      return;
    }
  }
  cVar2 = FUN_82307440(param_1);
  if (cVar2 != '\0') {
    FUN_82307298(param_1);
    return;
  }
  iVar1 = FUN_822d1830();
  if (iVar1 < 0) {
    return;
  }
  iVar1 = *(int *)(param_1 + 0x4c);
  if (*(int *)(param_1 + 0x54) == 0) {
    uVar3 = 9;
  }
  else if (*(int *)(param_1 + 0x54) == 1) {
    uVar3 = 8;
  }
  else {
    if (*(char *)(param_1 + 99) == '\0') goto LAB_8230773c;
    uVar3 = 7;
  }
  *(undefined4 *)(param_1 + 0x4c) = uVar3;
LAB_8230773c:
  if (iVar1 != *(int *)(param_1 + 0x4c)) {
    FUN_822d1198();
    FUN_822e37b8(param_1 + 0x68);
    FUN_822e37b8(param_1 + 0x94);
    FUN_822e32e0(param_1 + 200);
  }
  return;
}



// ===================================================
// 82307780  ->  FUN_82307780  (entree 82307780)
// ===================================================

void FUN_82307780(int param_1)

{
  char cVar1;
  longlong lVar2;
  
  FUN_822d0828(*(undefined4 *)(param_1 + 0x50));
  lVar2 = (ulonglong)*(uint *)(param_1 + 0x5c) - 1;
  *(undefined1 *)(param_1 + 99) = 0;
  if (lVar2 < 0) {
    lVar2 = 0;
  }
  *(int *)(param_1 + 0x5c) = (int)lVar2;
  if (((int)lVar2 < 1) && (cVar1 = FUN_821f1cc8(*(undefined4 *)(param_1 + 0x50)), cVar1 == '\0')) {
    if (1 < *(int *)(param_1 + 0x54)) {
      FUN_821f1870(*(undefined4 *)(param_1 + 0x50));
    }
    FUN_822e3778(param_1 + 0x68,(*(int *)(param_1 + 0x50) != 0) + '\x12',0);
    if ((*(char *)(param_1 + 0x61) != '\0') || (cVar1 = FUN_822fde60(), cVar1 != '\0')) {
      FUN_822e3778(param_1 + 0x94,(*(int *)(param_1 + 0x50) != 0) + '\x14',0);
    }
    *(undefined4 *)(param_1 + 0x4c) = 0;
  }
  else {
    FUN_82307440(param_1);
  }
  return;
}



// ===================================================
// 82307870  ->  FUN_82307870  (entree 82307870)
// ===================================================

void FUN_82307870(int param_1)

{
  char cVar3;
  int iVar2;
  undefined8 uVar1;
  
  cVar3 = FUN_822e2dd8(param_1 + 0x94);
  if (cVar3 != '\0') {
    FUN_822d0a70();
    iVar2 = FUN_822d0c08(*(undefined4 *)(param_1 + 0x50));
    if (-1 < iVar2) {
      FUN_822b3840(0,0xffffffff8201d710);
      FUN_822e37b8(param_1 + 0x94);
      FUN_822d0c08(*(undefined4 *)(param_1 + 0x50));
      cVar3 = FUN_82144cb0();
      if (cVar3 != '\0') {
        uVar1 = FUN_822d0c08(*(undefined4 *)(param_1 + 0x50));
        FUN_822db8f8(0,0,uVar1);
      }
      *(undefined4 *)(param_1 + 0x4c) = 5;
    }
  }
  return;
}



// ===================================================
// 82307920  ->  FUN_82307920  (entree 82307920)
// ===================================================

void FUN_82307920(int param_1)

{
  char cVar1;
  undefined4 uVar2;
  
  cVar1 = thunk_FUN_82148620();
  if (cVar1 != '\0') {
    FUN_822d0c08(*(undefined4 *)(param_1 + 0x50));
    cVar1 = FUN_82144cb0();
    if ((cVar1 == '\0') || (cVar1 = FUN_822dab40(*(undefined4 *)(param_1 + 0x50)), cVar1 == '\0')) {
      FUN_822da6b0(*(undefined4 *)(param_1 + 0x50),0xffffffffffffffff,0);
      uVar2 = 8;
    }
    else {
      uVar2 = 6;
    }
    *(undefined4 *)(param_1 + 0x4c) = uVar2;
  }
  return;
}



// ===================================================
// 823079A8  ->  FUN_823079a8  (entree 823079a8)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_823079a8(int param_1)

{
  byte *pbVar1;
  char cVar4;
  int iVar2;
  int iVar3;
  byte *pbVar5;
  
  cVar4 = FUN_822e2df0(param_1 + 0x68);
  if (cVar4 != '\0') {
    cVar4 = FUN_82298a58((&PTR_DAT_8206345c)[*(int *)(param_1 + 0x50)]);
    if (cVar4 != '\0') {
      iVar2 = thunk_FUN_821f4fc0(*(undefined4 *)(param_1 + 0x50),0);
      iVar3 = FUN_822dab70(*(undefined4 *)(param_1 + 0x50));
      if ((iVar2 != 0) && (iVar3 != 0)) {
        pbVar5 = (byte *)(iVar2 + 0x16d);
        do {
          pbVar1 = pbVar5 + (-0x16d - iVar2);
          pbVar5[-1] = pbVar1[iVar3 + (uint)*(byte *)(iVar2 + 0x2c) * 0x7d] | pbVar5[-1];
          *pbVar5 = pbVar1[iVar3 + (uint)*(byte *)(iVar2 + 0x2c) * 0x7d + 1] | *pbVar5;
          pbVar5[1] = pbVar1[iVar3 + (uint)*(byte *)(iVar2 + 0x2c) * 0x7d + 2] | pbVar5[1];
          pbVar5[2] = pbVar1[iVar3 + (uint)*(byte *)(iVar2 + 0x2c) * 0x7d + 3] | pbVar5[2];
          pbVar5[3] = pbVar1[iVar3 + (uint)*(byte *)(iVar2 + 0x2c) * 0x7d + 4] | pbVar5[3];
          pbVar5 = pbVar5 + 5;
        } while (pbVar5 + (-0x16d - iVar2) < (byte *)0x7d);
      }
      *(undefined4 *)(param_1 + 0x4c) = 8;
    }
  }
  return;
}



// ===================================================
// 82307AE0  ->  FUN_82307ae0  (entree 82307ae0)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82307ae0(int param_1)

{
  bool bVar1;
  char cVar3;
  int iVar2;
  undefined8 uVar4;
  
  FUN_822d0c30(*(undefined4 *)(param_1 + 0x50));
  uVar4 = 10;
  if (*(int *)(param_1 + 0x54) < 2) {
    uVar4 = 99;
  }
  FUN_822d0810(*(undefined4 *)(param_1 + 0x50),uVar4);
  *(undefined1 *)(param_1 + 100) = 0;
  iVar2 = *(int *)(&DAT_820036c0 + *(int *)(param_1 + 0x50) * 4);
  cVar3 = FUN_822c80d0(&DAT_82acb004 + iVar2 * 0x3d);
  if (cVar3 == '\0') {
    bVar1 = false;
  }
  else if ((*(int *)(&DAT_82acb050 + iVar2 * 0xf4) == 4) ||
          (bVar1 = false, *(int *)(&DAT_82acb050 + iVar2 * 0xf4) == 5)) {
    bVar1 = true;
  }
  if (bVar1) {
    *(undefined1 *)(param_1 + 100) = 1;
  }
  FUN_822e4d70(param_1 + 0x68);
  FUN_822e4d70(param_1 + 0x94);
  switch(*(undefined4 *)(param_1 + 0x4c)) {
  case 0:
    FUN_82307610(param_1);
    return 0;
  case 1:
    FUN_822e3c10(0xffffffff82acaf0c);
    FUN_822c8aa0(0xffffffff82acaf0c,0xffffffff8208dbd0);
    FUN_822e2e28(0xffffffff82acaf0c,1);
    DAT_82acaf6c = FUN_82322798(0x5f7);
    *(undefined4 *)(param_1 + 0x4c) = 2;
    return 0;
  case 2:
    cVar3 = FUN_822c7b98(0xffffffff82acaf0c);
    if (cVar3 == '\0') {
      iVar2 = FUN_822e2e38(0xffffffff82acaf0c);
      if (iVar2 != 0) {
        *(undefined4 *)(param_1 + 0x4c) = 0;
        return 0;
      }
      FUN_822d0828(*(undefined4 *)(param_1 + 0x50));
      FUN_822daa70(*(undefined4 *)(param_1 + 0x50));
      FUN_822e3c10(0xffffffff82acaf0c);
      FUN_822c8aa0(0xffffffff82acaf0c,0xffffffff8208dbc4);
      DAT_82acaf6c = FUN_82322798(0x5f8);
      *(undefined4 *)(param_1 + 0x4c) = 3;
      return 0;
    }
    break;
  case 3:
    FUN_822d0828(*(undefined4 *)(param_1 + 0x50));
    cVar3 = FUN_822c7b98(0xffffffff82acaf0c);
    if (cVar3 == '\0') {
      FUN_82307298(param_1);
    }
    break;
  case 4:
    FUN_82307870(param_1);
    return 0;
  case 5:
    FUN_82307920(param_1);
    return 0;
  case 6:
    FUN_82307780(param_1);
    return 0;
  case 7:
    FUN_823079a8(param_1);
    return 0;
  }
  return 0;
}



// ===================================================
// 82307D48  ->  FUN_82307d48  (entree 82307d48)
// ===================================================

/* WARNING: Function: __savegprlr_16 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_16 replaced with injection: x360_restgprlr */

void FUN_82307d48(int param_1)

{
  uint uVar1;
  bool bVar2;
  char cVar10;
  undefined8 uVar3;
  int iVar8;
  undefined8 uVar4;
  longlong lVar5;
  ulonglong uVar6;
  int iVar9;
  longlong lVar7;
  undefined8 uVar11;
  ulonglong uVar12;
  int iVar13;
  int iVar14;
  longlong lVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  double dVar18;
  double dVar19;
  double dVar20;
  float fStack_170;
  float fStack_16c;
  float fStack_168;
  float fStack_160;
  float fStack_15c;
  float fStack_158;
  undefined1 auStack_150 [32];
  float fStack_130;
  float fStack_12c;
  undefined4 uStack_128;
  undefined4 uStack_124;
  undefined1 auStack_120 [288];
  
  cVar10 = FUN_822c80d0();
  if (((cVar10 == '\0') || (*(int *)(param_1 + 0x4c) < 0)) ||
     (bVar2 = true, 6 < *(int *)(param_1 + 0x4c))) {
    bVar2 = false;
  }
  if (!bVar2) {
    return;
  }
  dVar18 = (double)DAT_82000a34;
  fStack_170 = DAT_82000a34;
  fStack_16c = DAT_82000a34;
  fStack_168 = DAT_82000a34;
  uVar11 = 0xffffffffff808080;
  if (*(char *)(param_1 + 100) == '\0') {
    uVar11 = 0xffffffffffffffff;
  }
  uVar3 = FUN_822c29e8();
  FUN_822c29d8(2);
  FUN_822c2a08(9);
  iVar13 = param_1 + 0x68;
  cVar10 = FUN_822e2dd8(iVar13);
  if (cVar10 == '\0') goto LAB_823082cc;
  FUN_8223bc10(0xe);
  FUN_8223c048(0xffffffffffffffff);
  FUN_8223c130(9);
  FUN_82249520(auStack_150,0x20,0xffffffff8208dc6c,(ulonglong)*(uint *)(param_1 + 0x50) + 1);
  FUN_822e39c0(iVar13,&fStack_170,auStack_150,1);
  FUN_8223beb8((double)fStack_170,(double)fStack_16c);
  uVar17 = 0x54b;
  iVar8 = FUN_822fcdd8();
  if (iVar8 == 0) {
    uVar17 = 0x54c;
  }
  else {
    iVar8 = FUN_822fcdd8();
    if (iVar8 == 3) {
      uVar17 = 0x54e;
    }
    else {
      iVar8 = FUN_822fcdd8();
      if (iVar8 == 1) {
        uVar17 = 0x54d;
      }
    }
  }
  uVar4 = FUN_82322798(uVar17);
  FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar4);
  dVar19 = (double)DAT_82000b08;
  if (*(int *)(param_1 + 0x54) == 0) {
    FUN_82322798(uVar17);
    FUN_822e37e0((double)fStack_170,(double)fStack_16c,dVar19,param_1 + 0xc0);
  }
  dVar20 = (double)DAT_82000f1c;
  fStack_16c = (float)((double)fStack_16c + dVar20);
  FUN_8223beb8((double)fStack_170);
  uVar17 = 0xffffffffff808080;
  if (*(char *)(param_1 + 0x60) != '\0') {
    uVar17 = uVar11;
  }
  FUN_8223c048(uVar17);
  uVar17 = FUN_82322798(0x54a);
  FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar17);
  FUN_8223c048(uVar11);
  if (*(int *)(param_1 + 0x54) == 1) {
    FUN_82322798(0x54a);
    FUN_822e37e0((double)fStack_170,(double)fStack_16c,dVar19,param_1 + 0xc0);
  }
  uVar17 = FUN_8223c1b0();
  uVar4 = FUN_8223c1d8();
  FUN_82249520(auStack_150,0x20,0xffffffff8208dc54,(ulonglong)*(uint *)(param_1 + 0x50) + 1);
  FUN_822e39c0(iVar13,&fStack_170,auStack_150,0);
  uVar1 = *(uint *)(param_1 + 0x54);
  fStack_170 = fStack_170 - DAT_8208d01c;
  uVar6 = 2;
  if (1 < (int)uVar1) {
    uVar6 = (ulonglong)uVar1;
  }
  if ((int)uVar1 < 0x1e) {
    uVar12 = uVar6;
    if (((2 < (int)uVar1) && (uVar12 = uVar6 - 1, 3 < (int)uVar1)) &&
       (*(int *)(param_1 + 0x58) < (int)uVar1)) {
      uVar12 = uVar6 - 2;
    }
  }
  else {
    uVar12 = 0x1c;
  }
  iVar8 = (int)uVar12;
  iVar14 = iVar8 + 4;
  if (iVar8 < iVar14) {
    lVar7 = uVar12 - 2;
    do {
      FUN_8223beb8((double)fStack_170,(double)fStack_16c);
      lVar5 = FUN_82322798(0x548);
      uVar6 = FUN_822da8b8(*(undefined4 *)(param_1 + 0x50),lVar7);
      if (((uVar6 & 0xffffffff) != 0) && (cVar10 = FUN_821f6110(), cVar10 == '\0')) {
        lVar5 = uVar6 + 0xfd;
        FUN_8223c198(1);
        FUN_8223c1c0(1);
      }
      lVar15 = lVar7 + 1;
      FUN_82249520(auStack_120,0x80,0xffffffff8208dc48,lVar15,lVar5);
      uVar16 = uVar11;
      if (*(int *)(param_1 + 0x54) == (int)lVar7 + 2) {
        FUN_822e37e0((double)fStack_170,(double)fStack_16c,dVar19,param_1 + 0xc0);
      }
      else {
        iVar9 = FUN_82144c28();
        if (iVar9 < 0) {
          iVar9 = FUN_822da898(*(undefined4 *)(&DAT_820036c0 + *(int *)(param_1 + 0x50) * 4));
          uVar16 = 0xffffffffff808080;
          if ((int)lVar7 != iVar9) {
            uVar16 = uVar11;
          }
        }
      }
      FUN_8223c048(uVar16);
      FUN_8223fe30(0xffffffff82000f08,auStack_120);
      FUN_8223c198(uVar17);
      FUN_8223c1c0(uVar4);
      fStack_16c = (float)((double)fStack_16c + dVar20);
      lVar7 = lVar15;
    } while ((int)lVar15 + 2 < iVar14);
  }
  if (*(char *)(param_1 + 100) == '\0') {
    FUN_822e32b8(param_1 + 200,0xffffffffffffffff,2 < iVar8);
    uVar11 = 1;
    if (0x1f < iVar14) goto LAB_823081c8;
  }
  else {
    FUN_822e32b8(param_1 + 200,0xffffffffffffffff,0);
LAB_823081c8:
    uVar11 = 0;
  }
  FUN_822e32b8(param_1 + 200,1,uVar11);
  fStack_160 = (float)dVar18;
  fStack_15c = (float)dVar18;
  fStack_158 = (float)dVar18;
  FUN_82249520(auStack_150,0x20,0xffffffff8208dc2c,(ulonglong)*(uint *)(param_1 + 0x50) + 1);
  FUN_822e39c0(iVar13,&fStack_170,auStack_150,0);
  FUN_82249520(auStack_150,0x20,0xffffffff8208dc0c,(ulonglong)*(uint *)(param_1 + 0x50) + 1);
  FUN_822e39c0(iVar13,&fStack_160,auStack_150,0);
  FUN_822e53f8((double)fStack_170,(double)fStack_16c,(double)fStack_160,(double)fStack_15c,
               param_1 + 200);
  FUN_82249520(auStack_150,0x20,0xffffffff8208dbf4,(ulonglong)*(uint *)(param_1 + 0x50) + 1);
  FUN_822e39c0(iVar13,&fStack_170,auStack_150,0);
  FUN_8223beb8((double)fStack_170,(double)fStack_16c);
  FUN_8223c048(0xffffffffffffffff);
  uVar11 = FUN_82322798(0);
  FUN_8223fe30(0xffffffff82085944,0xffffffff82010300,uVar11);
LAB_823082cc:
  cVar10 = FUN_822e2dd8(param_1 + 0x94);
  if (cVar10 != '\0') {
    if ((*(char *)(param_1 + 0x61) == '\0') && (cVar10 = FUN_822fde60(), cVar10 == '\0')) {
      uVar6 = (ulonglong)*(uint *)(param_1 + 0x50) ^ 1;
    }
    else {
      uVar6 = (ulonglong)*(uint *)(param_1 + 0x50);
    }
    FUN_82249520(auStack_150,0x20,0xffffffff8208dbdc,uVar6 + 1);
    FUN_822e39c0(param_1 + 0x94,&fStack_170,auStack_150,1);
    FUN_8223bc10(0xe);
    FUN_8223c130(9);
    FUN_8223c048(0xffffffffffffffff);
    fStack_130 = fStack_170;
    fStack_12c = fStack_16c;
    uStack_128 = DAT_82011844;
    uStack_124 = DAT_8208dbd8;
    FUN_8223bec0(&fStack_130,9);
    if (*(char *)(param_1 + 0x61) == '\0') {
      cVar10 = FUN_822fde60();
      if (cVar10 == '\0') {
        lVar7 = ((ulonglong)(*(int *)(param_1 + 0x50) == 0) ^ 1) + 0x556;
      }
      else {
        lVar7 = 0x558;
      }
    }
    else {
      lVar7 = 0x553;
    }
    uVar11 = FUN_82322798(lVar7);
    FUN_8223fe30(0xffffffff82000f08,uVar11);
  }
  FUN_822c2a18();
  FUN_822c29d8(uVar3);
  return;
}



// ===================================================
// 82308400  ->  FUN_82308400  (entree 82308400)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

int FUN_82308400(int param_1,ulonglong param_2)

{
  if (*(int *)(param_1 + 0xb4) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 0xb4) = 0;
  *(undefined4 *)(param_1 + 0xb8) = 0;
  *(undefined4 *)(param_1 + 0xbc) = 0;
  if (*(int *)(param_1 + 0x88) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 0x88) = 0;
  *(undefined4 *)(param_1 + 0x8c) = 0;
  *(undefined4 *)(param_1 + 0x90) = 0;
  FUN_822c73a8(param_1);
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 823084E8  ->  FUN_823084e8  (entree 823084e8)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_823084e8(undefined4 param_1,undefined4 param_2,undefined4 *param_3,undefined4 param_4)

{
  undefined1 auStack_110 [4];
  undefined4 uStack_10c;
  undefined4 uStack_104;
  undefined4 uStack_f4;
  undefined4 uStack_f0;
  undefined4 uStack_ec;
  undefined4 uStack_d4;
  undefined4 uStack_d0;
  undefined4 uStack_cc;
  
  FUN_822b99e8(auStack_110);
  uStack_d4 = *param_3;
  uStack_d0 = param_3[1];
  uStack_cc = param_3[2];
  uStack_f0 = 9;
  uStack_ec = 9;
  uStack_10c = param_1;
  uStack_104 = param_4;
  uStack_f4 = param_2;
  FUN_822c2940(auStack_110);
  return;
}



// ===================================================
// 823085A0  ->  FUN_823085a0  (entree 823085a0)
// ===================================================

void FUN_823085a0(int param_1,int param_2)

{
  undefined8 uVar1;
  
  if (param_2 == 0x10) {
    FUN_823085a0(param_1,6);
    FUN_823085a0(param_1,7);
    FUN_823085a0(param_1,0xb);
    uVar1 = 0xc;
  }
  else {
    if (param_2 != 1) goto LAB_82308600;
    uVar1 = 2;
  }
  FUN_823085a0(param_1,uVar1);
LAB_82308600:
  param_1 = param_2 * 8 + param_1;
  if (*(int *)(param_1 + 0x4c) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0x4c) = 0;
  }
  return;
}



// ===================================================
// 82308670  ->  FUN_82308670  (entree 82308670)
// ===================================================

void FUN_82308670(double param_1,undefined8 param_2,undefined8 param_3,undefined4 *param_4)

{
  undefined4 uStack_11c;
  undefined4 uStack_118;
  undefined4 uStack_114;
  undefined4 uStack_110;
  undefined1 auStack_100 [4];
  undefined4 uStack_fc;
  uint uStack_f8;
  undefined4 uStack_f4;
  undefined4 uStack_e4;
  undefined4 uStack_e0;
  undefined4 uStack_dc;
  undefined4 uStack_c4;
  undefined4 uStack_c0;
  undefined4 uStack_bc;
  
  FUN_822b99e8(auStack_100);
  FUN_822c8b30(param_3,&uStack_11c,0,0);
  uStack_118 = *param_4;
  uStack_114 = param_4[1];
  uStack_110 = param_4[2];
  uStack_fc = uStack_11c;
  uStack_e0 = 9;
  uStack_dc = 9;
  uStack_e4 = 6;
  uStack_f4 = 0x400000;
  uStack_f8 = (int)(longlong)(param_1 * (double)DAT_82001afc) << 0x18 | 0xffffff;
  uStack_c4 = uStack_118;
  uStack_c0 = uStack_114;
  uStack_bc = uStack_110;
  FUN_822c2940(auStack_100);
  return;
}



// ===================================================
// 82308758  ->  FUN_82308758  (entree 82308758)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

void FUN_82308758(int param_1)

{
  int iVar1;
  float *pfVar2;
  int *piVar3;
  int iVar4;
  double dVar5;
  double dVar6;
  double dVar7;
  double dVar8;
  int aiStack_60 [2];
  float fStack_58;
  float fStack_54;
  float fStack_50;
  
  piVar3 = aiStack_60;
  pfVar2 = (float *)(param_1 + 0x114);
  iVar1 = 2;
  aiStack_60[0] = 0x12;
  aiStack_60[1] = 0x13;
  dVar5 = (double)DAT_82000a34;
  do {
    iVar4 = *piVar3 * 8 + param_1;
    dVar7 = dVar5;
    if (*(int *)(iVar4 + 0x4c) != 0) {
      if ((*(byte *)(iVar4 + 0x53) & 0x80) == 0) {
        FUN_823085a0(param_1);
        dVar7 = dVar5;
      }
      else {
        dVar6 = dVar5;
        dVar8 = dVar5;
        if (pfVar2 != (float *)0x0) {
          dVar8 = (double)*pfVar2;
          dVar6 = (double)FUN_8214ace8((double)pfVar2[1]);
          dVar5 = (double)pfVar2[2];
        }
        fStack_58 = (float)dVar8;
        fStack_54 = (float)dVar6;
        fStack_50 = (float)dVar5;
        FUN_82166540(*(undefined4 *)(iVar4 + 0x4c),&fStack_58);
      }
    }
    iVar1 = iVar1 + -1;
    pfVar2 = pfVar2 + 3;
    piVar3 = piVar3 + 1;
    *(byte *)(iVar4 + 0x53) = *(byte *)(iVar4 + 0x53) & 0x7f;
    dVar5 = dVar7;
  } while (iVar1 != 0);
  return;
}



// ===================================================
// 82308838  ->  FUN_82308838  (entree 82308838)
// ===================================================

/* WARNING: Function: __savegprlr_22 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_22 replaced with injection: x360_restgprlr */

void FUN_82308838(int param_1)

{
  undefined1 uVar1;
  uint uVar2;
  int iVar4;
  undefined8 uVar3;
  int iVar5;
  int *piVar6;
  uint *puVar7;
  float *pfVar8;
  double dVar9;
  double dVar10;
  double dVar11;
  int aiStack_80 [32];
  
  piVar6 = aiStack_80;
  puVar7 = (uint *)(param_1 + 300);
  aiStack_80[0] = 0x12;
  dVar9 = (double)DAT_82054e74;
  pfVar8 = (float *)(param_1 + 0x114);
  iVar5 = 2;
  aiStack_80[1] = 0x13;
  do {
    if (*(int *)(*piVar6 * 8 + param_1 + 0x4c) != 0) {
      uVar1 = *(undefined1 *)((*piVar6 + 10) * 8 + param_1);
      iVar4 = FUN_823158c0(uVar1);
      if (iVar4 == 0) {
        uVar2 = *puVar7;
        dVar11 = (double)*pfVar8;
        dVar10 = (double)pfVar8[1];
        FUN_8223bc10(0xe);
        FUN_8223c130((ulonglong)uVar2 + 1);
        FUN_8223c048(0xffffffffffffffff);
        FUN_8223beb8(dVar11,dVar10);
        FUN_8223c198(1);
        uVar3 = FUN_823158f8(uVar1);
        FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar3);
        FUN_8223beb8(dVar11,(double)(float)(dVar10 + dVar9));
        FUN_8223c198(1);
        uVar3 = FUN_82322798(0x27a);
        FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar3);
      }
    }
    iVar5 = iVar5 + -1;
    pfVar8 = pfVar8 + 3;
    piVar6 = piVar6 + 1;
    puVar7 = puVar7 + 1;
  } while (iVar5 != 0);
  return;
}



// ===================================================
// 82308978  ->  FUN_82308978  (entree 82308978)
// ===================================================

void FUN_82308978(int param_1,undefined1 param_2)

{
  if (*(int *)(param_1 + 0xec) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0xec) = 0;
  }
  *(undefined1 *)(param_1 + 0xf1) = param_2;
  return;
}



// ===================================================
// 823089C8  ->  FUN_823089c8  (entree 823089c8)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_823089c8(int *param_1)

{
  char cVar1;
  
  if (*param_1 != 0) {
    if ((*(char *)((int)param_1 + 5) == '\x02') && (cVar1 = FUN_821665e8(), cVar1 != '\0')) {
      if (*param_1 != 0) {
        FUN_821664c0();
        *param_1 = 0;
      }
      *(undefined1 *)((int)param_1 + 5) = 0xff;
    }
    if (*(char *)((int)param_1 + 7) == '\0') {
      if (*param_1 != 0) {
        FUN_821664c0();
        *param_1 = 0;
      }
      *(undefined1 *)((int)param_1 + 5) = 0xff;
    }
    *(undefined1 *)((int)param_1 + 7) = 0;
    return;
  }
  *(undefined1 *)((int)param_1 + 7) = 0;
  return;
}



// ===================================================
// 82308A60  ->  FUN_82308a60  (entree 82308a60)
// ===================================================

void FUN_82308a60(int *param_1)

{
  if (*param_1 != 0) {
    FUN_821664c0();
    *param_1 = 0;
  }
  *param_1 = 0;
  *(undefined1 *)((int)param_1 + 6) = 0;
  *(undefined1 *)((int)param_1 + 7) = 0;
  *(undefined1 *)((int)param_1 + 5) = 0xff;
  *(undefined1 *)(param_1 + 1) = 0xff;
  return;
}



// ===================================================
// 82308AC0  ->  FUN_82308ac0  (entree 82308ac0)
// ===================================================

void FUN_82308ac0(int *param_1,int param_2)

{
  int iVar1;
  
  if (*param_1 != 0) {
    FUN_821664c0();
    *param_1 = 0;
  }
  *(undefined4 *)(param_2 + 0x1c) = 2;
  *(undefined4 *)(param_2 + 0x2c) = 9;
  iVar1 = FUN_82166cc0(param_2);
  *param_1 = iVar1;
  return;
}



// ===================================================
// 82308B28  ->  FUN_82308b28  (entree 82308b28)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

undefined8 FUN_82308b28(int param_1)

{
  undefined1 *puVar1;
  ulonglong uVar2;
  
  puVar1 = (undefined1 *)(param_1 + 0x51);
  uVar2 = 0;
  do {
    FUN_823085a0(param_1,uVar2);
    uVar2 = uVar2 + 1;
    puVar1[-1] = 0;
    *puVar1 = 0;
    puVar1 = puVar1 + 8;
  } while ((uVar2 & 0xffffffff) < 0x19);
  *(undefined4 *)(param_1 + 0x134) = 0;
  return 1;
}



// ===================================================
// 82308B78  ->  FUN_82308b78  (entree 82308b78)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

void FUN_82308b78(undefined8 param_1,undefined8 param_2,undefined4 *param_3,undefined4 *param_4,
                 undefined8 param_5,undefined8 param_6,undefined8 param_7)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 ***pppuStack_50;
  int iStack_4c;
  undefined4 uStack_48;
  undefined4 uStack_44;
  undefined4 ***pppuStack_40;
  undefined4 uStack_3c;
  
  pppuStack_50 = &pppuStack_50;
  pppuStack_40 = &pppuStack_50;
  uStack_3c = 0;
  iStack_4c = 0;
  uStack_48 = 0;
  uStack_44 = 0;
  FUN_821589a0(&pppuStack_40,&pppuStack_50,ZEXT48(pppuStack_40) << 0x20,ZEXT48(pppuStack_50) << 0x20
              );
  FUN_82166ad0(param_1,&pppuStack_50,param_5,param_6,0,9,0);
  iVar2 = FUN_82166778(&pppuStack_50,param_7);
  uVar1 = DAT_82000a34;
  if (iVar2 == 0) {
    if (param_3 != (undefined4 *)0x0) {
      *param_3 = DAT_82000a34;
      param_3[1] = uVar1;
      param_3[2] = uVar1;
    }
    uVar1 = DAT_82000b08;
    if (param_4 == (undefined4 *)0x0) goto LAB_82308c74;
  }
  else {
    if (param_3 != (undefined4 *)0x0) {
      *param_3 = *(undefined4 *)(iVar2 + 0x40);
      param_3[1] = *(undefined4 *)(iVar2 + 0x44);
      param_3[2] = *(undefined4 *)(iVar2 + 0x48);
    }
    if (param_4 == (undefined4 *)0x0) goto LAB_82308c74;
    uVar1 = *(undefined4 *)(iVar2 + 0x60);
  }
  *param_4 = uVar1;
LAB_82308c74:
  if (iStack_4c != 0) {
    FUN_82142f48();
  }
  return;
}



// ===================================================
// 82308C90  ->  FUN_82308c90  (entree 82308c90)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */
/* WARNING: Restarted to delay deadcode elimination for space: stack */

void FUN_82308c90(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar6;
  undefined8 uVar3;
  int iVar7;
  undefined8 uVar4;
  int iVar8;
  undefined8 uVar5;
  ulonglong uVar9;
  ulonglong uVar10;
  uint uVar11;
  undefined8 uVar12;
  double dVar13;
  double dVar14;
  double dVar15;
  double dVar16;
  double dVar17;
  float afStack_140 [2];
  undefined8 uStack_138;
  float fStack_130;
  float fStack_12c;
  float fStack_128;
  undefined8 uStack_120;
  float fStack_118;
  float fStack_114;
  float fStack_110;
  float fStack_108;
  float fStack_104;
  float fStack_100;
  float fStack_f8;
  float fStack_f4;
  float fStack_f0;
  float fStack_e8;
  float fStack_e4;
  float fStack_e0;
  undefined1 auStack_d0 [32];
  undefined1 auStack_b0 [32];
  undefined1 auStack_90 [144];
  
  iVar6 = FUN_826018c0();
  if (((*(int *)(iVar6 + 0x7c) != 0) && (*(char *)(iVar6 + 0x81) != '\0')) &&
     (*(int *)(iVar6 + 0x84) != 0)) {
    FUN_821dc920();
    uVar3 = FUN_821dc9c0();
    iVar7 = FUN_82235f28(0xffffffff827a99f8,uVar3);
    dVar17 = (double)DAT_82000a34;
    fStack_130 = DAT_82000a34;
    fStack_12c = DAT_82000a34;
    fStack_128 = DAT_82000a34;
    uStack_138 = 0x82084b888208be8c;
    uVar2 = *(undefined4 *)((int)&uStack_138 + (uint)*(byte *)(iVar6 + 0x80) * 4);
    FUN_8223bc10(0xe);
    FUN_8223c130(6);
    uVar12 = FUN_821665d8(*(undefined4 *)(iVar6 + 0x7c));
    FUN_82308b78(iVar6,&fStack_130,afStack_140,0x423,uVar2,0xffffffff8208be7c);
    dVar13 = (double)DAT_82000f14;
    FUN_8223beb8((double)fStack_130,(double)(float)((double)fStack_12c - dVar13));
    dVar14 = (double)afStack_140[0];
    dVar16 = (double)DAT_82001afc;
    iVar8 = (int)(longlong)(dVar14 * dVar16);
    uStack_138 = CONCAT44(iVar8,uStack_138._4_4_);
    FUN_8223c048(iVar8 << 0x18 | 0xffffff);
    uVar3 = FUN_8223c198(1);
    uVar4 = FUN_8223c1c0(1);
    FUN_8223fe30(0xffffffff82000f08,iVar7 + 0x59);
    FUN_8223c198(uVar3);
    FUN_8223c1c0(uVar4);
    uVar11 = *(uint *)(iVar7 + 0x100);
    uVar10 = (ulonglong)uVar11;
    uVar9 = (ulonglong)*(uint *)(iVar7 + 0x104);
    fStack_118 = fStack_130;
    fStack_114 = fStack_12c;
    fStack_110 = fStack_128;
    iVar8 = FUN_82144a98();
    if (iVar8 == 0) {
      uVar3 = FUN_82322798(0x18c);
      FUN_82249520(auStack_b0,0x20,uVar3,uVar10);
      uVar3 = 0x18d;
    }
    else {
      uVar3 = FUN_82322798(0x18e);
      FUN_82249520(auStack_b0,0x20,uVar3,uVar10);
      uVar3 = 399;
    }
    uVar3 = FUN_82322798(uVar3);
    FUN_82249520(auStack_d0,0x20,uVar3,uVar9);
    FUN_82308b78(uVar12,iVar6,&fStack_130,afStack_140,0x423,uVar2,0xffffffff8208be68);
    FUN_8223beb8((double)fStack_130,(double)fStack_12c);
    iVar8 = (int)(longlong)((double)afStack_140[0] * dVar16);
    uStack_138 = CONCAT44(iVar8,uStack_138._4_4_);
    FUN_8223c048(iVar8 << 0x18 | 0xffffff);
    FUN_8223fe30(0xffffffff820847fc,auStack_b0,auStack_d0);
    uVar10 = uVar9 + uVar10;
    dVar15 = dVar17;
    if (uVar10 != 0) {
      iVar8 = (int)(((float)uVar11 / (float)(uVar10 & 0xffffffff)) * DAT_82003edc * DAT_82003edc);
      uStack_138._4_4_ = (undefined4)uVar10;
      uStack_138 = CONCAT44(iVar8,uStack_138._4_4_);
      uStack_120 = (longlong)iVar8;
      dVar15 = (double)((float)uStack_120 * DAT_82003a3c);
    }
    FUN_82308b78(uVar12,iVar6,&fStack_130,afStack_140,0x423,uVar2,0xffffffff8208be54);
    iVar8 = (int)(longlong)((double)afStack_140[0] * dVar16);
    uStack_138 = CONCAT44(iVar8,uStack_138._4_4_);
    uVar11 = iVar8 << 0x18 | 0xffffff;
    FUN_8223beb8((double)fStack_130,(double)fStack_12c);
    FUN_8223c048(uVar11);
    if ((dVar15 <= dVar17) || (uVar9 != 0)) {
      uVar3 = FUN_82322798(0x191);
      uVar4 = FUN_82322798(400);
      FUN_8223fe30(0xffffffff8208be3c,uVar4,dVar15,uVar3);
    }
    else {
      uVar4 = FUN_82322798(0x191);
      uVar3 = DAT_820117f0;
      uVar5 = FUN_82322798(400);
      FUN_8223fe30(0xffffffff8208be48,uVar5,uVar3,uVar4);
    }
    if (*(char *)(iVar6 + 0x80) == '\0') {
      uVar3 = 0xffffffff8208dccc;
    }
    else {
      uVar3 = 0xffffffff8208be2c;
    }
    FUN_82308b78(uVar12,iVar6,&fStack_130,afStack_140,0x423,uVar2,uVar3);
    uVar1 = *(undefined4 *)(iVar7 + 0xec);
    uVar3 = FUN_82322798(999);
    FUN_82249520(auStack_90,0x20,uVar3,uVar1);
    dVar17 = (double)fStack_130;
    dVar16 = (double)fStack_12c;
    uStack_120 = CONCAT44(fStack_130,fStack_12c);
    dVar15 = (double)DAT_8208be28;
    uStack_138 = CONCAT44(DAT_8208be28,DAT_82011804);
    FUN_8223df90(uStack_120,uStack_138,9,5,0);
    FUN_8223beb8((double)(float)((double)(float)(dVar17 + dVar15) - (double)DAT_82000f0c),
                 (double)(float)(dVar16 + (double)DAT_82000f0c));
    FUN_8223c048(uVar11);
    FUN_8223fe30(0xffffffff82000f80,0xffffffff82010300,auStack_90);
    if (*(int *)(iVar6 + 0x84) != 0) {
      FUN_82308b78(uVar12,iVar6,&fStack_130,afStack_140,0x423,uVar2,0xffffffff8208be18);
      FUN_822dc728(&fStack_130,&fStack_130);
      fStack_108 = fStack_130;
      fStack_104 = fStack_12c;
      fStack_100 = fStack_128;
      FUN_82166540(*(undefined4 *)(iVar6 + 0x84),&fStack_108);
      FUN_82166570((double)afStack_140[0],*(undefined4 *)(iVar6 + 0x84));
    }
    if (*(int *)(iVar6 + 0xa4) != 0) {
      FUN_82308b78(uVar12,iVar6,&fStack_130,afStack_140,0x423,uVar2,0xffffffff8208be08);
      fStack_f8 = fStack_130;
      fStack_f4 = fStack_12c;
      fStack_f0 = fStack_128;
      FUN_82166540(*(undefined4 *)(iVar6 + 0xa4),&fStack_f8);
      FUN_82166570((double)afStack_140[0],*(undefined4 *)(iVar6 + 0xa4));
    }
    if (*(int *)(iVar6 + 0xac) != 0) {
      FUN_82308b78(uVar12,iVar6,&fStack_130,afStack_140,0x423,uVar2,0xffffffff8208bdf8);
      fStack_e4 = (float)((double)fStack_12c - dVar13);
      fStack_e8 = fStack_130;
      fStack_e0 = fStack_128;
      FUN_82166540(*(undefined4 *)(iVar6 + 0xac),&fStack_e8);
      FUN_82166570((double)afStack_140[0],*(undefined4 *)(iVar6 + 0xac));
    }
    if (*(char *)(iVar7 + 0x423) != '\0') {
      fStack_118 = fStack_118 + DAT_8200649c;
      fStack_114 = fStack_114 + DAT_82003a50;
      FUN_82308670(dVar14,iVar6,*(char *)(iVar7 + 0x423) + -1,&fStack_118);
    }
  }
  FUN_8260190c();
  return;
}



// ===================================================
// 823092A8  ->  FUN_823092a8  (entree 823092a8)
// ===================================================

void FUN_823092a8(undefined8 param_1)

{
  undefined8 uVar1;
  
  uVar1 = FUN_822c29e8();
  FUN_822c29d8(2);
  FUN_822c2a08(9);
  FUN_82308c90(param_1);
  FUN_82308838(param_1);
  FUN_822c2a18();
  FUN_822c29d8(uVar1);
  return;
}



// ===================================================
// 82309310  ->  FUN_82309310  (entree 82309310)
// ===================================================

void FUN_82309310(int param_1,int param_2)

{
  char cVar2;
  undefined4 uVar1;
  char *apcStack_d0 [4];
  int iStack_c0;
  undefined *puStack_bc;
  char *pcStack_b8;
  char *pcStack_b4;
  undefined4 uStack_a8;
  undefined4 uStack_a4;
  undefined4 uStack_9c;
  undefined4 uStack_94;
  
  if (*(int *)(param_1 + 0x4c) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0x4c) = 0;
  }
  apcStack_d0[0] = s_sta_s_82084c28;
  apcStack_d0[1] = s_sta_e_82084c20;
  apcStack_d0[2] = s_sta_e_82084c20;
  apcStack_d0[3] = s_sta_e_82084c20;
  FUN_82158008(&iStack_c0);
  cVar2 = FUN_82144b30();
  puStack_bc = &DAT_8208dce4;
  iStack_c0 = (-(uint)(cVar2 != '\0') & 0xfffffff2) + 0x426;
  uStack_9c = 8;
  uStack_a8 = 0x20000;
  uStack_a4 = 2;
  uStack_94 = 9;
  pcStack_b8 = apcStack_d0[param_2 * 2];
  pcStack_b4 = apcStack_d0[param_2 * 2 + 1];
  uVar1 = FUN_82166cc0(&iStack_c0);
  *(char *)(param_1 + 0x51) = (char)param_2;
  *(undefined4 *)(param_1 + 0x4c) = uVar1;
  FUN_82157f80(&iStack_c0);
  return;
}



// ===================================================
// 82309408  ->  FUN_82309408  (entree 82309408)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_82309408(int param_1,int param_2)

{
  char cVar2;
  undefined4 uVar1;
  char *apcStack_1a0 [4];
  undefined4 uStack_190;
  undefined4 uStack_18c;
  int iStack_180;
  char *pcStack_17c;
  char *pcStack_178;
  char *pcStack_174;
  char *pcStack_168;
  undefined4 uStack_164;
  undefined4 uStack_15c;
  undefined4 uStack_154;
  int iStack_e0;
  char *pcStack_dc;
  undefined4 uStack_c8;
  undefined4 uStack_c4;
  undefined4 uStack_bc;
  undefined4 uStack_b4;
  
  FUN_823085a0(param_1,2);
  if (*(int *)(param_1 + 0x54) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0x54) = 0;
  }
  if (*(int *)(param_1 + 0x5c) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0x5c) = 0;
  }
  apcStack_1a0[0] = s_sta_s_82084c28;
  apcStack_1a0[3] = s_neu_e_82084c10;
  apcStack_1a0[1] = s_neu_s_82084c18;
  apcStack_1a0[2] = s_neu_s_82084c18;
  uStack_190 = 0x20000;
  uStack_18c = 0x10000;
  FUN_82158008(&iStack_180);
  cVar2 = FUN_82144b30();
  pcStack_168 = apcStack_1a0[param_2 + 4];
  iStack_180 = (-(uint)(cVar2 != '\0') & 0xfffffff2) + 0x426;
  pcStack_178 = apcStack_1a0[param_2 * 2];
  pcStack_174 = apcStack_1a0[param_2 * 2 + 1];
  uStack_15c = 1;
  uStack_164 = 2;
  pcStack_17c = s_map_base_8208dcf8;
  uStack_154 = 9;
  uVar1 = FUN_82166cc0(&iStack_180);
  *(undefined4 *)(param_1 + 0x54) = uVar1;
  *(char *)(param_1 + 0x59) = (char)param_2;
  if (param_2 == 1) {
    FUN_82158008(&iStack_e0);
    cVar2 = FUN_82144b30();
    uStack_c8 = 0x20000;
    uStack_c4 = 2;
    uStack_b4 = 9;
    pcStack_dc = s_map_home_txt_8208dce8;
    iStack_e0 = (-(uint)(cVar2 != '\0') & 0xfffffff2) + 0x426;
    uStack_bc = 5;
    uVar1 = FUN_82166cc0(&iStack_e0);
    *(undefined1 *)(param_1 + 0x61) = 1;
    *(undefined4 *)(param_1 + 0x5c) = uVar1;
    FUN_82157f80(&iStack_e0);
  }
  FUN_82157f80(&iStack_180);
  return;
}



// ===================================================
// 82309590  ->  FUN_82309590  (entree 82309590)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_82309590(int param_1,int param_2)

{
  char cVar2;
  undefined4 uVar1;
  char *apcStack_100 [4];
  char *pcStack_f0;
  char *pcStack_ec;
  char *pcStack_e8;
  char *pcStack_e4;
  char *pcStack_e0;
  char *pcStack_dc;
  int iStack_d0;
  char *pcStack_cc;
  char *pcStack_c8;
  char *pcStack_c4;
  undefined4 uStack_b8;
  undefined4 uStack_b4;
  undefined4 uStack_ac;
  undefined4 uStack_a4;
  
  if (*(int *)(param_1 + 100) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 100) = 0;
  }
  if (param_2 == 0) {
    *(undefined1 *)(param_1 + 0x68) = 0;
    return;
  }
  if ((param_2 == 8) && (cVar2 = FUN_823163a0(0xe), cVar2 != '\0')) {
    param_2 = 9;
  }
  apcStack_100[0] = (char *)0x0;
  pcStack_dc = s_bg_01_dom_02_8208dd68;
  apcStack_100[1] = s_bg_01_swn_8208dd5c;
  apcStack_100[2] = s_bg_01_sws_8208dd50;
  apcStack_100[3] = s_bg_01_swr_8208dd44;
  pcStack_f0 = s_bg_01_csd_8208dd38;
  pcStack_ec = s_bg_01_csb_8208dd2c;
  pcStack_e8 = s_bg_01_sac_8208dd20;
  pcStack_e4 = s_bg_01_sae_8208dd14;
  pcStack_e0 = s_bg_01_dom_01_8208dd04;
  FUN_82158008(&iStack_d0);
  cVar2 = FUN_82144b30();
  pcStack_cc = apcStack_100[param_2];
  iStack_d0 = (-(uint)(cVar2 != '\0') & 0xfffffff2) + 0x426;
  pcStack_c8 = s_sta_s_82084c28;
  pcStack_c4 = s_sta_e_82084c20;
  uStack_a4 = 9;
  uStack_b8 = 0x20000;
  uStack_ac = 2;
  uStack_b4 = 2;
  uVar1 = FUN_82166cc0(&iStack_d0);
  *(char *)(param_1 + 0x68) = (char)param_2;
  *(undefined4 *)(param_1 + 100) = uVar1;
  FUN_82157f80(&iStack_d0);
  return;
}



// ===================================================
// 823096F0  ->  FUN_823096f0  (entree 823096f0)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

void FUN_823096f0(int param_1,int param_2,ulonglong param_3)

{
  int iVar1;
  char cVar3;
  undefined4 uVar2;
  char *apcStack_130 [8];
  char *apcStack_110 [4];
  char *pcStack_100;
  char *pcStack_fc;
  char *pcStack_f8;
  char *pcStack_f4;
  char *pcStack_f0;
  int iStack_e0;
  char *pcStack_dc;
  undefined4 uStack_d8;
  undefined4 uStack_d4;
  undefined4 uStack_c8;
  undefined4 uStack_c4;
  undefined4 uStack_bc;
  undefined4 uStack_b4;
  
  if (*(int *)(param_1 + 0x74) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0x74) = 0;
  }
  apcStack_110[0] = s_ic_hom_8208ddb8;
  apcStack_130[3] = s_neu_e_82084c10;
  apcStack_110[1] = s_ic_swn_8208ddb0;
  apcStack_110[2] = s_ic_sws_8208dda8;
  apcStack_110[3] = s_ic_swr_8208dda0;
  pcStack_100 = s_ic_csd_8208dd98;
  pcStack_fc = s_ic_csb_8208dd90;
  pcStack_f8 = s_ic_sac_8208dd88;
  pcStack_f4 = s_ic_sae_8208dd80;
  pcStack_f0 = s_ic_dom_8208dd78;
  apcStack_130[0] = s_sta_s_82084c28;
  apcStack_130[1] = s_neu_s_82084c18;
  apcStack_130[2] = s_neu_s_82084c18;
  apcStack_130[4] = (char *)0x20000;
  apcStack_130[5] = (char *)0x10000;
  FUN_82158008(&iStack_e0);
  cVar3 = FUN_82144b30();
  iVar1 = (int)((param_3 & 0xffffffff) << 3);
  pcStack_dc = apcStack_110[param_2];
  uStack_c8 = *(undefined4 *)((int)apcStack_130 + (int)((param_3 & 0xffffffff) << 2) + 0x10);
  iStack_e0 = (-(uint)(cVar3 != '\0') & 0xfffffff2) + 0x426;
  uStack_bc = 2;
  uStack_c4 = 2;
  uStack_b4 = 9;
  uStack_d8 = *(undefined4 *)((int)apcStack_130 + iVar1);
  uStack_d4 = *(undefined4 *)((int)apcStack_130 + iVar1 + 4);
  uVar2 = FUN_82166cc0(&iStack_e0);
  *(char *)(param_1 + 0x78) = (char)param_2;
  *(char *)(param_1 + 0x79) = (char)param_3;
  *(undefined4 *)(param_1 + 0x74) = uVar2;
  FUN_82157f80(&iStack_e0);
  return;
}



// ===================================================
// 82309868  ->  FUN_82309868  (entree 82309868)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_82309868(int param_1,int param_2,ulonglong param_3)

{
  int iVar1;
  char cVar3;
  undefined4 uVar2;
  char *apcStack_140 [5];
  char *pcStack_12c;
  undefined4 auStack_128 [6];
  char *apcStack_110 [4];
  char *pcStack_100;
  char *pcStack_fc;
  char *pcStack_f8;
  char *pcStack_f4;
  char *pcStack_f0;
  int iStack_e0;
  char *pcStack_dc;
  undefined4 uStack_d8;
  undefined4 uStack_d4;
  undefined4 uStack_c8;
  undefined4 uStack_c4;
  undefined4 uStack_bc;
  undefined4 uStack_b4;
  
  if (*(int *)(param_1 + 0x6c) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0x6c) = 0;
  }
  if ((param_2 == 7) && (cVar3 = FUN_823163a0(0xe), cVar3 != '\0')) {
    param_2 = 8;
  }
  apcStack_110[0] = s_zoom_swn_8208de20;
  apcStack_110[1] = s_zoom_sws_8208de14;
  apcStack_110[2] = s_zoom_swr_8208de08;
  apcStack_110[3] = s_zoom_csd_8208ddfc;
  pcStack_100 = s_zoom_csb_8208ddf0;
  pcStack_fc = s_zoom_sac_8208dde4;
  pcStack_f8 = s_zoom_sae_8208ddd8;
  pcStack_f4 = s_zoom_dom_01_8208ddcc;
  auStack_128[1] = 2;
  pcStack_f0 = s_zoom_dom_02_8208ddc0;
  apcStack_140[0] = s_sta_s_82084c28;
  pcStack_12c = s_sta_s_82084c28;
  apcStack_140[1] = s_sta_e_82084c20;
  apcStack_140[2] = s_sta_e_82084c20;
  apcStack_140[3] = s_sta_e_82084c20;
  apcStack_140[4] = s_sta_e_82084c20;
  auStack_128[0] = 7;
  auStack_128[2] = 7;
  FUN_82158008(&iStack_e0);
  cVar3 = FUN_82144b30();
  uStack_c4 = 2;
  iVar1 = (int)((param_3 & 0xffffffff) << 3);
  pcStack_dc = apcStack_110[param_2];
  uStack_bc = *(undefined4 *)((int)auStack_128 + (int)((param_3 & 0xffffffff) << 2));
  iStack_e0 = (-(uint)(cVar3 != '\0') & 0xfffffff2) + 0x426;
  uStack_c8 = 0x20000;
  uStack_b4 = 9;
  uStack_d8 = *(undefined4 *)((int)apcStack_140 + iVar1);
  uStack_d4 = *(undefined4 *)((int)apcStack_140 + iVar1 + 4);
  uVar2 = FUN_82166cc0(&iStack_e0);
  *(char *)(param_1 + 0x70) = (char)param_2;
  *(char *)(param_1 + 0x71) = (char)param_3;
  *(undefined4 *)(param_1 + 0x6c) = uVar2;
  FUN_82157f80(&iStack_e0);
  return;
}



// ===================================================
// 82309A00  ->  FUN_82309a00  (entree 82309a00)
// ===================================================

/* WARNING: Function: __savegprlr_18 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_18 replaced with injection: x360_restgprlr */

void FUN_82309a00(int param_1,ulonglong param_2,int param_3,undefined1 param_4,undefined4 param_5)

{
  int iVar1;
  undefined4 uVar2;
  undefined *apuStack_180 [4];
  undefined *puStack_170;
  undefined *puStack_16c;
  undefined *puStack_168;
  undefined *puStack_164;
  undefined *puStack_160;
  undefined *puStack_15c;
  undefined *puStack_158;
  undefined *puStack_154;
  undefined *puStack_150;
  undefined *puStack_14c;
  undefined *puStack_148;
  undefined *puStack_144;
  undefined *puStack_140;
  undefined *puStack_13c;
  undefined *puStack_138;
  undefined *puStack_134;
  undefined *puStack_130;
  undefined4 uStack_120;
  char *pcStack_11c;
  undefined *puStack_118;
  undefined *puStack_114;
  undefined4 uStack_108;
  undefined4 uStack_104;
  undefined4 uStack_fc;
  undefined4 uStack_f4;
  
  FUN_823085a0(param_1,param_2 + 7);
  puStack_160 = &DAT_82003f4c;
  puStack_15c = &DAT_82003f48;
  puStack_158 = &DAT_82003f98;
  puStack_154 = &DAT_82003f90;
  puStack_150 = &DAT_82003f88;
  puStack_14c = &DAT_82003f7c;
  puStack_148 = &DAT_82003f68;
  puStack_144 = &DAT_82003f44;
  apuStack_180[0] = &DAT_82003f58;
  puStack_140 = &DAT_82003f40;
  apuStack_180[1] = &DAT_82003f94;
  apuStack_180[2] = &DAT_82003f8c;
  apuStack_180[3] = &DAT_82003f84;
  puStack_170 = &DAT_82003f70;
  puStack_16c = &DAT_82003f5c;
  puStack_168 = &DAT_82003f54;
  puStack_164 = &DAT_82003f50;
  puStack_13c = &DAT_82003f58;
  puStack_138 = &DAT_82003f58;
  puStack_134 = &DAT_82003f58;
  puStack_130 = &DAT_82003f58;
  FUN_82158008(&uStack_120);
  uStack_120 = 0x423;
  if ((param_2 & 0xffffffff) == 0) {
    pcStack_11c = s_chara_face_82084c44;
  }
  else {
    pcStack_11c = s_chara_face_store_8208de2c;
  }
  iVar1 = (int)((param_2 & 0xffffffff) << 3) + param_1;
  puStack_118 = apuStack_180[param_3];
  uStack_108 = 0x20000;
  uStack_104 = 2;
  uStack_f4 = 9;
  puStack_114 = puStack_118;
  uStack_fc = param_5;
  uVar2 = FUN_82166cc0(&uStack_120);
  *(undefined1 *)(iVar1 + 0x89) = param_4;
  *(undefined4 *)(iVar1 + 0x84) = uVar2;
  *(char *)((int)((param_2 + 0x11 & 0xffffffff) << 3) + param_1) = (char)param_3;
  FUN_82157f80(&uStack_120);
  return;
}



// ===================================================
// 82309BA0  ->  FUN_82309ba0  (entree 82309ba0)
// ===================================================

void FUN_82309ba0(double param_1,undefined8 param_2,int param_3,ulonglong param_4,uint param_5)

{
  int iVar1;
  double dVar2;
  float fStack_30;
  float fStack_2c;
  undefined4 uStack_28;
  
  iVar1 = (int)((param_4 & 0xffffffff) << 3) + param_3;
  if ((*(int *)(iVar1 + 0x8c) == 0) ||
     (*(byte *)((int)((param_4 + 0x12 & 0xffffffff) << 3) + param_3) != param_5)) {
    FUN_82309a00(param_3,param_4 + 1);
    dVar2 = (double)FUN_8214ace8(param_2);
    fStack_30 = (float)param_1;
    fStack_2c = (float)dVar2;
    uStack_28 = DAT_82000a34;
    FUN_82166540(*(undefined4 *)(iVar1 + 0x8c),&fStack_30);
  }
  return;
}



// ===================================================
// 82309C38  ->  FUN_82309c38  (entree 82309c38)
// ===================================================

void FUN_82309c38(int param_1,uint param_2)

{
  undefined4 uVar1;
  undefined *apuStack_e0 [4];
  undefined *puStack_d0;
  undefined *puStack_cc;
  undefined *puStack_c8;
  undefined4 uStack_c0;
  char *pcStack_bc;
  undefined *puStack_b8;
  undefined *puStack_b4;
  undefined4 uStack_a8;
  undefined4 uStack_a4;
  undefined4 uStack_9c;
  undefined4 uStack_94;
  
  if (*(int *)(param_1 + 0xa4) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0xa4) = 0;
  }
  if (param_2 < 7) {
    apuStack_e0[0] = &DAT_8200eb74;
    apuStack_e0[1] = &DAT_820023f4;
    apuStack_e0[2] = &DAT_820033c0;
    apuStack_e0[3] = &DAT_820033c4;
    puStack_d0 = &DAT_820033c8;
    puStack_cc = &DAT_820033cc;
    puStack_c8 = &DAT_8200eb78;
    FUN_82158008(&uStack_c0);
    if (5 < param_2) {
      param_2 = 6;
    }
    pcStack_bc = s_ogen_base_8201130f + 1;
    puStack_b8 = apuStack_e0[param_2];
    uStack_c0 = 0xe2;
    uStack_9c = 6;
    uStack_a8 = 0x20000;
    uStack_a4 = 2;
    uStack_94 = 9;
    puStack_b4 = puStack_b8;
    uVar1 = FUN_82166cc0(&uStack_c0);
    *(char *)(param_1 + 0xa8) = (char)param_2;
    *(undefined4 *)(param_1 + 0xa4) = uVar1;
    FUN_82157f80(&uStack_c0);
  }
  return;
}



// ===================================================
// 82309D58  ->  FUN_82309d58  (entree 82309d58)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

void FUN_82309d58(int param_1,ulonglong param_2,int param_3,undefined8 param_4,undefined4 param_5)

{
  undefined4 uVar1;
  char *apcStack_e0 [4];
  undefined4 uStack_d0;
  char *pcStack_cc;
  undefined4 uStack_c8;
  undefined4 uStack_c4;
  undefined4 uStack_b8;
  undefined4 uStack_b4;
  undefined4 uStack_ac;
  undefined4 uStack_a4;
  
  FUN_823085a0(param_1,param_2 + 0xc);
  apcStack_e0[0] = s_dan_icon1p_8200ff28;
  apcStack_e0[1] = s_dan_icon2p_8200ff1c;
  FUN_82158008(&uStack_d0);
  uStack_d0 = 0xe2;
  pcStack_cc = apcStack_e0[param_3];
  uStack_b8 = 0x20000;
  uStack_ac = param_5;
  uStack_c8 = FUN_821d4680(param_4);
  uStack_c4 = FUN_821d4680(param_4);
  uStack_b4 = 2;
  uStack_a4 = 9;
  uVar1 = FUN_82166cc0(&uStack_d0);
  *(undefined4 *)((int)((param_2 & 0xffffffff) << 3) + param_1 + 0xac) = uVar1;
  *(char *)((int)((param_2 + 0x16 & 0xffffffff) << 3) + param_1) = (char)param_4;
  FUN_82157f80(&uStack_d0);
  return;
}



// ===================================================
// 82309E20  ->  FUN_82309e20  (entree 82309e20)
// ===================================================

void FUN_82309e20(double param_1,double param_2,int param_3,ulonglong param_4,undefined8 param_5,
                 char param_6)

{
  int iVar1;
  float fStack_30;
  float fStack_2c;
  undefined4 uStack_28;
  
  iVar1 = (int)((param_4 & 0xffffffff) << 3) + param_3;
  if ((*(int *)(iVar1 + 0xb4) != 0) &&
     (*(char *)((int)((param_4 + 0x17 & 0xffffffff) << 3) + param_3) == param_6)) {
    return;
  }
  FUN_82309d58(param_3,param_4 + 1);
  fStack_30 = (float)param_1;
  fStack_2c = (float)param_2;
  uStack_28 = DAT_82000a34;
  FUN_82166540(*(undefined4 *)(iVar1 + 0xb4),&fStack_30);
  return;
}



// ===================================================
// 82309EB0  ->  FUN_82309eb0  (entree 82309eb0)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_82309eb0(int param_1,int param_2,ulonglong param_3)

{
  int iVar1;
  undefined4 uVar2;
  char *apcStack_110 [8];
  char *apcStack_f0 [5];
  char *pcStack_dc;
  undefined4 uStack_d0;
  char *pcStack_cc;
  undefined4 uStack_c8;
  undefined4 uStack_c4;
  undefined4 uStack_b8;
  undefined4 uStack_b4;
  undefined4 uStack_ac;
  undefined4 uStack_a4;
  
  if (*(int *)(param_1 + 0xd4) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0xd4) = 0;
  }
  apcStack_110[0] = s_shutter_8208de80;
  pcStack_dc = s_sta_e_82084c20;
  apcStack_110[1] = s_shutter_filnal_8208de70;
  apcStack_110[3] = (char *)0x2;
  apcStack_f0[0] = s_sta_s_82084c28;
  apcStack_f0[2] = s_sta_s_82084c28;
  apcStack_f0[1] = &DAT_8208de68;
  apcStack_f0[3] = &DAT_8208de68;
  apcStack_f0[4] = &DAT_8208de68;
  apcStack_110[2] = (char *)0xf;
  apcStack_110[4] = (char *)0xf;
  FUN_82158008(&uStack_d0);
  uStack_b4 = 2;
  iVar1 = (int)((param_3 & 0xffffffff) << 3);
  pcStack_cc = apcStack_110[param_2];
  uStack_d0 = 0x423;
  uStack_ac = *(undefined4 *)((int)apcStack_110 + (int)((param_3 & 0xffffffff) << 2) + 8);
  uStack_b8 = 0x20000;
  uStack_a4 = 9;
  uStack_c8 = *(undefined4 *)((int)apcStack_f0 + iVar1);
  uStack_c4 = *(undefined4 *)((int)apcStack_f0 + iVar1 + 4);
  uVar2 = FUN_82166cc0(&uStack_d0);
  *(undefined4 *)(param_1 + 0xd4) = uVar2;
  *(char *)(param_1 + 0xd8) = (char)param_2;
  *(char *)(param_1 + 0xd9) = (char)param_3;
  if ((param_3 & 0xffffffff) == 0) {
    FUN_822b3ac0(0xffffffff8208de54);
    FUN_82157f80(&uStack_d0);
    return;
  }
  if ((param_3 & 0xffffffff) == 1) {
    FUN_822b3ac0(0xffffffff8208de40);
  }
  FUN_82157f80(&uStack_d0);
  return;
}



// ===================================================
// 82309FF8  ->  FUN_82309ff8  (entree 82309ff8)
// ===================================================

/* WARNING: Function: __savegprlr_21 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_21 replaced with injection: x360_restgprlr */

void FUN_82309ff8(int param_1,uint param_2,ulonglong param_3,undefined8 param_4,undefined4 *param_5)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  double dVar4;
  char *apcStack_c0 [3];
  float fStack_b4;
  undefined4 uStack_b0;
  char *apcStack_a0 [4];
  char *pcStack_90;
  char *pcStack_8c;
  char *pcStack_88;
  char *pcStack_84;
  char *pcStack_80;
  char *pcStack_7c;
  char *pcStack_78;
  char *pcStack_74;
  char *pcStack_70;
  char *pcStack_6c;
  char *pcStack_68;
  
  uVar1 = (int)param_3 == 0 ^ 1;
  iVar2 = (uVar1 + 0x12) * 8 + param_1;
  puVar3 = (undefined4 *)(((int)param_3 + 0x17) * 0xc + param_1);
  *(byte *)(iVar2 + 0x53) = *(byte *)(iVar2 + 0x53) | 0x80;
  *puVar3 = *param_5;
  puVar3[1] = param_5[1];
  puVar3[2] = param_5[2];
  if (*(int *)(iVar2 + 0x4c) != 0) {
    if (*(byte *)((uVar1 + 0x1c) * 8 + param_1) == param_2) {
      return;
    }
    FUN_823085a0(param_1,uVar1 + 0x12);
  }
  apcStack_c0[2] = (char *)*param_5;
  dVar4 = (double)FUN_8214ace8((double)(float)param_5[1]);
  uStack_b0 = param_5[2];
  fStack_b4 = (float)dVar4;
  pcStack_80 = s_logo_amateur_8208df18;
  apcStack_a0[0] = s_logo_normal_8208df0c;
  apcStack_a0[1] = s_logo_normal_8208df0c;
  apcStack_a0[2] = s_logo_normal_8208df0c;
  apcStack_a0[3] = s_logo_normal_8208df0c;
  pcStack_90 = s_logo_normal_8208df0c;
  pcStack_8c = s_logo_normal_8208df0c;
  pcStack_88 = s_logo_normal_8208df0c;
  pcStack_70 = s_logo_masters_8208dec0;
  pcStack_84 = s_logo_beginner_8208defc;
  pcStack_7c = s_logo_challeng_8208deec;
  pcStack_78 = s_logo_champion_8208dedc;
  pcStack_74 = s_logo_climax_8208ded0;
  pcStack_6c = s_logo_world_8208deb4;
  pcStack_68 = s_logo_final_8208dea8;
  apcStack_c0[1] = s_compe_logo_s_8208de98;
  apcStack_c0[0] = s_compe_logo_m_8208de88;
  FUN_822f6768(iVar2 + 0x4c,0x423,
               *(undefined4 *)((int)apcStack_c0 + (int)((param_3 & 0xffffffff) << 2)),
               apcStack_c0 + 2,param_4,0x20000,apcStack_a0[param_2]);
  *(char *)(iVar2 + 0x52) = (char)param_3;
  *(char *)((uVar1 + 0x1c) * 8 + param_1) = (char)param_2;
  *puVar3 = *param_5;
  puVar3[1] = param_5[1];
  puVar3[2] = param_5[2];
  *(int *)((int)((param_3 + 0x4b & 0xffffffff) << 2) + param_1) = (int)param_4;
  return;
}



// ===================================================
// 8230A1C0  ->  FUN_8230a1c0  (entree 8230a1c0)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_8230a1c0(double param_1,undefined8 param_2,int param_3,int param_4,undefined4 param_5)

{
  undefined4 uVar1;
  double dVar2;
  char *apcStack_100 [4];
  char *apcStack_f0 [4];
  char *pcStack_e0;
  char *pcStack_dc;
  undefined4 uStack_d0;
  char *pcStack_cc;
  char *pcStack_c8;
  char *pcStack_c4;
  undefined4 uStack_b8;
  undefined4 uStack_b4;
  undefined4 uStack_ac;
  undefined4 uStack_a4;
  char *pcStack_9c;
  float fStack_98;
  undefined4 uStack_94;
  
  if ((*(int *)(param_3 + 0xec) == 0) && (*(char *)(param_3 + 0xf1) != '\0')) {
    apcStack_100[0] = s_btn_cursor_a_8208df58;
    apcStack_f0[0] = (char *)0x0;
    apcStack_100[1] = s_btn_cursor_b_8208df48;
    apcStack_100[2] = s_btn_cursor_c_8208df38;
    apcStack_100[3] = s_btn_cursor_d_8208df28;
    apcStack_f0[1] = (char *)0x0;
    apcStack_f0[2] = s_loop_s_82084bc4;
    apcStack_f0[3] = s_loop_e_82084bcc;
    pcStack_e0 = s_hit_s_820852a4;
    pcStack_dc = s_hit_e_8208528c;
    FUN_82158008(&uStack_d0);
    pcStack_cc = apcStack_100[param_4];
    uStack_d0 = 0x423;
    uStack_b8 = 0x10000;
    if (*(char *)(param_3 + 0xf1) != '\x01') {
      uStack_b8 = 0x20000;
    }
    apcStack_100[0] = (char *)(float)param_1;
    uStack_ac = param_5;
    dVar2 = (double)FUN_8214ace8(param_2);
    apcStack_100[1] = (char *)(float)dVar2;
    apcStack_100[2] = (char *)DAT_82000a34;
    pcStack_9c = apcStack_100[0];
    uStack_94 = DAT_82000a34;
    uStack_b4 = 2;
    uStack_a4 = 9;
    pcStack_c8 = apcStack_f0[(uint)*(byte *)(param_3 + 0xf1) * 2];
    pcStack_c4 = apcStack_f0[(uint)*(byte *)(param_3 + 0xf1) * 2 + 1];
    fStack_98 = (float)apcStack_100[1];
    uVar1 = FUN_82166cc0(&uStack_d0);
    *(char *)(param_3 + 0xf0) = (char)param_4;
    *(undefined4 *)(param_3 + 0xec) = uVar1;
    FUN_82157f80(&uStack_d0);
  }
  return;
}



// ===================================================
// 8230A338  ->  FUN_8230a338  (entree 8230a338)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_8230a338(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                 undefined4 param_5)

{
  undefined4 uVar1;
  char *pcStack_130;
  undefined4 uStack_12c;
  undefined1 auStack_120 [4];
  uint uStack_11c;
  undefined4 uStack_10c;
  uint uStack_108;
  undefined1 auStack_100 [4];
  uint uStack_fc;
  undefined4 uStack_ec;
  uint uStack_e8;
  undefined4 uStack_e0;
  char *pcStack_dc;
  undefined4 uStack_d8;
  undefined4 uStack_d4;
  undefined4 uStack_c8;
  undefined4 uStack_c4;
  undefined4 uStack_bc;
  undefined4 uStack_b4;
  undefined1 auStack_68 [104];
  
  if (*(int *)(param_1 + 0xf4) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0xf4) = 0;
  }
  FUN_82158008(&uStack_e0);
  pcStack_dc = s_col_iconmove_82084ca0;
  pcStack_130 = s_p_col_txt_main_c_82084c8c;
  uStack_e0 = 0x423;
  uStack_c8 = 0x20000;
  uStack_bc = 6;
  uStack_c4 = 2;
  uStack_b4 = 9;
  uStack_12c = param_4;
  uStack_d8 = param_2;
  uStack_d4 = param_3;
  FUN_8214d890(auStack_120,&pcStack_130);
  FUN_82330798(&pcStack_130,auStack_68,auStack_120);
  if (0xf < uStack_108) {
    thunk_FUN_82142f48(uStack_11c);
  }
  uStack_10c = 0;
  uStack_11c = uStack_11c & 0xffffff;
  uStack_108 = 0xf;
  pcStack_130 = s_p_col_txt_sub_c_82084c7c;
  uStack_12c = param_5;
  FUN_8214d890(auStack_100,&pcStack_130);
  FUN_82330798(&pcStack_130,auStack_68,auStack_100);
  if (0xf < uStack_e8) {
    thunk_FUN_82142f48(uStack_fc);
  }
  uStack_e8 = 0xf;
  uStack_ec = 0;
  uStack_fc = uStack_fc & 0xffffff;
  uVar1 = FUN_82166cc0(&uStack_e0);
  *(undefined4 *)(param_1 + 0xf4) = uVar1;
  FUN_82157f80(&uStack_e0);
  return;
}



// ===================================================
// 8230A470  ->  FUN_8230a470  (entree 8230a470)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */
/* WARNING: Removing unreachable block (ram,0x8230a550) */
/* WARNING: Removing unreachable block (ram,0x8230a558) */

void FUN_8230a470(undefined8 param_1)

{
  undefined8 uVar1;
  int iVar4;
  undefined8 uVar2;
  ulonglong uVar3;
  ulonglong uVar5;
  uint uVar6;
  uint uVar7;
  undefined *apuStack_50 [4];
  undefined4 auStack_40 [16];
  
  auStack_40[0] = 0x1b82;
  apuStack_50[0] = &DAT_82063c1c;
  apuStack_50[1] = &DAT_82063c18;
  auStack_40[1] = 0x1b86;
  auStack_40[2] = 0x1b83;
  auStack_40[3] = 0x1b87;
  auStack_40[4] = 0x1b84;
  auStack_40[5] = 0x1b88;
  auStack_40[6] = 0x1b85;
  auStack_40[7] = 0x1b89;
  FUN_821dc920();
  uVar1 = FUN_821dc9c0();
  iVar4 = FUN_82235f28(0xffffffff827a99f8,uVar1);
  uVar2 = FUN_821dc920();
  uVar3 = FUN_821dd318(uVar2,uVar1);
  uVar7 = (uint)*(byte *)(iVar4 + 0x1b9);
  uVar6 = (uint)*(byte *)(iVar4 + 0x1b8);
  if (3 < *(byte *)(iVar4 + 0x1b9)) {
    uVar7 = 4;
  }
  if (3 < *(byte *)(iVar4 + 0x1b8)) {
    uVar6 = 4;
  }
  iVar4 = (int)uVar3;
  if (iVar4 < 0) {
    uVar5 = 0;
  }
  else {
    uVar5 = uVar3;
    if (1 < iVar4) {
      uVar5 = 2;
    }
  }
  if (iVar4 < 0) {
    uVar3 = 0;
  }
  else if (1 < iVar4) {
    uVar3 = 2;
  }
  FUN_8230a338(param_1,*(undefined4 *)((int)apuStack_50 + (int)((uVar3 & 0xffffffff) << 2)),
               *(undefined4 *)((int)apuStack_50 + (int)((uVar5 & 0xffffffff) << 2)),
               auStack_40[uVar6 * 2],auStack_40[uVar7 * 2 + 1]);
  return;
}



// ===================================================
// 8230A5C8  ->  FUN_8230a5c8  (entree 8230a5c8)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_8230a5c8(int param_1,int param_2)

{
  char cVar1;
  int *piVar2;
  int iStack_d0;
  char *pcStack_cc;
  undefined4 uStack_b8;
  undefined4 uStack_ac;
  undefined1 uStack_a0;
  
  piVar2 = (int *)(param_1 + 0xfc);
  if (*(int *)(param_1 + 0xfc) == 0) {
    if (*piVar2 != 0) {
      FUN_821664c0();
      *piVar2 = 0;
    }
    FUN_82158008(&iStack_d0);
    cVar1 = FUN_82144b30();
    uStack_a0 = 0;
    pcStack_cc = s_map_aero_8208df68;
    iStack_d0 = (-(uint)(cVar1 != '\0') & 0xfffffff2) + 0x426;
    uStack_b8 = 0x10000;
    uStack_ac = 4;
    FUN_82308ac0(piVar2,&iStack_d0);
    if (-1 < param_2) {
      *(int *)(param_1 + 0x134) = param_2;
    }
    FUN_82157f80(&iStack_d0);
  }
  return;
}



// ===================================================
// 8230A678  ->  FUN_8230a678  (entree 8230a678)
// ===================================================

/* WARNING: Function: __savegprlr_21 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_21 replaced with injection: x360_restgprlr */

void FUN_8230a678(int param_1,int param_2,ulonglong param_3)

{
  char *pcVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  char cVar5;
  int iVar6;
  int iVar7;
  double dVar8;
  float fStack_b0;
  float fStack_ac;
  float fStack_a8;
  undefined4 auStack_a0 [4];
  char *apcStack_90 [5];
  char *pcStack_7c;
  char *pcStack_78;
  char *pcStack_74;
  
  dVar8 = (double)DAT_82000a34;
  fStack_b0 = DAT_82000a34;
  fStack_ac = DAT_82000a34;
  fStack_a8 = DAT_82000a34;
  iVar7 = (param_2 == 7) + 0x17;
  FUN_823085a0(param_1,iVar7);
  pcStack_78 = s_p_eff_compe_sae_8208dfa0;
  pcStack_74 = s_p_eff_compe_dom_8208df90;
  pcVar1 = apcStack_90[param_2];
  auStack_a0[0] = 0x10000;
  apcStack_90[0] = s_nml_s_8208df88;
  auStack_a0[1] = 0x20000;
  apcStack_90[1] = s_nml_e_8208df80;
  apcStack_90[2] = s_sta_s_82084c28;
  apcStack_90[3] = s_sta_e_82084c20;
  apcStack_90[4] = s_neu_s_82084c18;
  pcStack_7c = s_neu_e_82084c10;
  auStack_a0[2] = 0x10000;
  cVar5 = FUN_82144b30();
  FUN_82308b78(dVar8,param_1,&fStack_b0,0,
               ((-(ulonglong)(cVar5 != '\0') & 0xfffffffe) << 0x20 |
               -(ulonglong)(cVar5 != '\0') & 0xfffffff2) + 0x426,0,pcVar1);
  dVar8 = (double)FUN_8214ace8((double)fStack_ac);
  iVar6 = (int)((param_3 & 0xffffffff) << 3);
  fStack_ac = (float)dVar8;
  uVar2 = *(undefined4 *)((int)apcStack_90 + iVar6 + 4);
  uVar3 = *(undefined4 *)((int)apcStack_90 + iVar6);
  iVar6 = iVar7 * 8 + param_1;
  uVar4 = *(undefined4 *)((int)auStack_a0 + (int)((param_3 & 0xffffffff) << 2));
  cVar5 = FUN_82144b30();
  FUN_822f6768(iVar6 + 0x4c,
               ((-(ulonglong)(cVar5 != '\0') & 0xfffffffe) << 0x20 |
               -(ulonglong)(cVar5 != '\0') & 0xfffffff2) + 0x426,0xffffffff8208df74,&fStack_b0,3,
               uVar4,uVar3,uVar2);
  *(char *)(iVar6 + 0x51) = (char)param_3;
  *(char *)(((param_2 == 7) + 0x21) * 8 + param_1) = (char)param_2;
  return;
}



// ===================================================
// 8230A858  ->  FUN_8230a858  (entree 8230a858)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_8230a858(int param_1,int param_2,undefined8 param_3)

{
  char cVar2;
  undefined8 uVar1;
  undefined8 uVar3;
  
  cVar2 = FUN_82317860(0);
  if (cVar2 != '\0') {
    uVar1 = FUN_82316390(0);
    uVar3 = param_3;
    if (param_2 != (int)uVar1) {
      if ((*(int *)(param_1 + 0x104) != 0) && (*(char *)(param_1 + 0x109) == '\0'))
      goto LAB_8230a8c4;
      uVar3 = 0;
    }
    FUN_8230a678(param_1,uVar1,uVar3);
  }
LAB_8230a8c4:
  cVar2 = FUN_82317860(1);
  if (cVar2 != '\0') {
    if (param_2 == 7) {
      FUN_8230a678(param_1,7,param_3);
      return;
    }
    if ((*(int *)(param_1 + 0x10c) == 0) || (*(char *)(param_1 + 0x111) != '\0')) {
      FUN_8230a678(param_1,7,0);
    }
  }
  return;
}



// ===================================================
// 8230A928  ->  FUN_8230a928  (entree 8230a928)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_8230a928(int param_1)

{
  int iVar1;
  int iVar2;
  char cVar3;
  int iVar4;
  int *piVar5;
  int aiStack_30 [12];
  
  piVar5 = aiStack_30;
  iVar4 = 2;
  aiStack_30[0] = 0x17;
  aiStack_30[1] = 0x18;
  do {
    iVar1 = *piVar5;
    iVar2 = iVar1 * 8 + param_1;
    if (((*(int *)(iVar2 + 0x4c) != 0) && (*(char *)(iVar2 + 0x51) == '\x01')) &&
       (cVar3 = FUN_821665e8(), cVar3 != '\0')) {
      FUN_8230a678(param_1,*(undefined1 *)((iVar1 + 10) * 8 + param_1),2);
    }
    iVar4 = iVar4 + -1;
    piVar5 = piVar5 + 1;
  } while (iVar4 != 0);
  return;
}



// ===================================================
// 8230A9D8  ->  FUN_8230a9d8  (entree 8230a9d8)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

void FUN_8230a9d8(int *param_1,char param_2,undefined8 param_3,undefined8 param_4,char param_5)

{
  int iVar1;
  undefined4 auStack_80 [4];
  char *apcStack_70 [4];
  char *apcStack_60 [4];
  char *pcStack_50;
  char *pcStack_4c;
  
  *(undefined1 *)((int)param_1 + 7) = 1;
  if (*(char *)((int)param_1 + 6) != '\0') {
    if (param_5 != '\0') {
      param_5 = '\x02';
    }
    *(undefined1 *)((int)param_1 + 6) = 0;
  }
  if ((*(char *)((int)param_1 + 5) != '\x02') || (param_5 != '\x01')) {
    if ((param_5 == '\x01') && (*(char *)((int)param_1 + 5) == '\x01')) {
      if (*param_1 != 0) {
        return;
      }
    }
    else if (*param_1 != 0) {
      FUN_821664c0();
      *param_1 = 0;
    }
    *(char *)((int)param_1 + 5) = param_5;
    apcStack_60[3] = s_loop_e_82084bcc;
    apcStack_70[0] = s_vertical_arrow_up_820852c0;
    apcStack_70[1] = s_vertical_arrow_down_820852ac;
    pcStack_50 = s_hit_s_820852a4;
    pcStack_4c = s_hit_e_8208528c;
    auStack_80[0] = 0x20000;
    apcStack_70[2] = s_side_arrow_left_82085294;
    apcStack_70[3] = s_side_arrow_right_82085278;
    apcStack_60[0] = s_unactive_s_8208526c;
    apcStack_60[1] = s_unactive_e_82085260;
    apcStack_60[2] = s_loop_s_82084bc4;
    auStack_80[1] = 0x10000;
    auStack_80[2] = 0x20000;
    FUN_822dc728(param_3,param_3);
    iVar1 = (int)*(char *)((int)param_1 + 5);
    FUN_822f6768(param_1,0x423,apcStack_70[param_2],param_3,param_4,auStack_80[iVar1],
                 apcStack_60[iVar1 * 2],apcStack_60[iVar1 * 2 + 1]);
  }
  return;
}



// ===================================================
// 8230AB68  ->  FUN_8230ab68  (entree 8230ab68)
// ===================================================

/* WARNING: Function: __savegprlr_20 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_20 replaced with injection: x360_restgprlr */

void FUN_8230ab68(int param_1,int param_2,int param_3)

{
  char *apcStack_a0 [4];
  undefined4 uStack_90;
  char *apcStack_80 [4];
  char *pcStack_70;
  char *pcStack_6c;
  
  if (*(int *)(param_1 + 0x7c) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0x7c) = 0;
  }
  apcStack_a0[2] = (char *)DAT_82000a34;
  apcStack_a0[3] = (char *)DAT_82000a34;
  pcStack_70 = s_end_s_82084c08;
  uStack_90 = DAT_82000a34;
  pcStack_6c = s_end_e_82084c00;
  apcStack_a0[0] = s_player_info_win_1p_82084b88;
  apcStack_a0[1] = s_player_info_win_2p_8208be8c;
  apcStack_80[0] = s_sta_s_82084c28;
  apcStack_80[1] = s_sta_e_82084c20;
  apcStack_80[2] = s_neu_s_82084c18;
  apcStack_80[3] = s_neu_s_82084c18;
  FUN_822f6768((undefined4 *)(param_1 + 0x7c),0x423,apcStack_a0[param_2],apcStack_a0 + 2,5,0x20000,
               apcStack_80[param_3 * 2],apcStack_80[param_3 * 2 + 1]);
  *(char *)(param_1 + 0x80) = (char)param_2;
  *(char *)(param_1 + 0x81) = (char)param_3;
  return;
}



// ===================================================
// 8230AC50  ->  FUN_8230ac50  (entree 8230ac50)
// ===================================================

/* WARNING: Function: __savegprlr_23 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_23 replaced with injection: x360_restgprlr */

void FUN_8230ac50(int param_1,int param_2)

{
  undefined8 uVar1;
  int iVar2;
  longlong lVar3;
  uint uVar4;
  
  FUN_821dc920();
  uVar1 = FUN_821dc9c0();
  iVar2 = FUN_82235f28(0xffffffff827a99f8,uVar1);
  lVar3 = 0;
  uVar4 = 0;
  do {
    if (9 < uVar4) {
      FUN_822c5128(iVar2 + 0x130);
    }
    if ((1 << (uVar4 & 0x1f) & *(uint *)((uVar4 >> 3 & 0x1ffffffc) + iVar2 + 0x130)) != 0) {
      lVar3 = lVar3 + 1;
    }
    uVar4 = uVar4 + 1;
  } while (uVar4 < 8);
  if (param_2 == 0) {
    FUN_8230ab68(param_1,uVar1,0);
    if (*(int *)(param_1 + 0x84) != 0) {
      FUN_821664c0();
      *(undefined4 *)(param_1 + 0x84) = 0;
    }
    if (*(int *)(param_1 + 0xa4) != 0) {
      FUN_821664c0();
      *(undefined4 *)(param_1 + 0xa4) = 0;
    }
    if (*(int *)(param_1 + 0xac) != 0) {
      FUN_821664c0();
      *(undefined4 *)(param_1 + 0xac) = 0;
      return;
    }
  }
  else {
    if (param_2 != 1) {
      FUN_8230ab68(param_1,uVar1,1);
    }
    else {
      FUN_8230ab68(param_1,uVar1,1);
    }
    FUN_82309a00(param_1,0,*(undefined1 *)(iVar2 + 0xf8),param_2 == 1,5);
    FUN_82309c38(param_1,lVar3);
    FUN_82309d58(param_1,0,uVar1,*(undefined1 *)(iVar2 + 0xf9),6);
  }
  return;
}



// ===================================================
// 8230AD98  ->  FUN_8230ad98  (entree 8230ad98)
// ===================================================

undefined8 FUN_8230ad98(int param_1)

{
  char cVar1;
  int iVar2;
  
  if (((*(char *)(param_1 + 0x79) == '\0') && (*(int *)(param_1 + 0x74) != 0)) &&
     (cVar1 = FUN_821665e8(), cVar1 != '\0')) {
    FUN_823096f0(param_1,*(undefined1 *)(param_1 + 0x78),1);
  }
  if (((*(char *)(param_1 + 0x71) == '\x02') && (*(int *)(param_1 + 0x6c) != 0)) &&
     ((cVar1 = FUN_821665e8(), cVar1 != '\0' && (*(int *)(param_1 + 0x6c) != 0)))) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0x6c) = 0;
  }
  if (((*(char *)(param_1 + 0x81) == '\0') && (*(int *)(param_1 + 0x7c) != 0)) &&
     (cVar1 = FUN_821665e8(), cVar1 != '\0')) {
    FUN_8230ac50(param_1,0xffffffffffffffff);
  }
  if ((((*(int *)(param_1 + 0xd4) != 0) && (*(char *)(param_1 + 0xd9) == '\x02')) &&
      (cVar1 = FUN_821665e8(), cVar1 != '\0')) && (*(int *)(param_1 + 0xd4) != 0)) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0xd4) = 0;
  }
  FUN_82308758(param_1);
  FUN_8230a928(param_1);
  iVar2 = *(int *)(param_1 + 0x134) + 1;
  *(int *)(param_1 + 0x134) = iVar2;
  if (0xdac < iVar2) {
    *(undefined4 *)(param_1 + 0x134) = 0;
  }
  if (*(int *)(param_1 + 0xfc) != 0) {
    FUN_82166598((double)(longlong)*(int *)(param_1 + 0x134));
  }
  return 0;
}



