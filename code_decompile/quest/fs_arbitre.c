// ===================================================
// 1800DB4B0  ->  FUN_1800db4b0  (entree 1800db4b0)
// ===================================================

undefined4 FUN_1800db4b0(void)

{
  char cVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  undefined4 uVar5;
  undefined8 uVar6;
  longlong lVar7;
  undefined8 uVar8;
  longlong lVar9;
  ulonglong uVar10;
  undefined1 uVar11;
  undefined1 uVar12;
  
  uVar6 = FUN_1800b23a0();
  lVar7 = FUN_1800b23b0(uVar6);
  uVar8 = FUN_1800b24b0(uVar6);
  iVar2 = FUN_1800b4940(uVar8);
  iVar3 = FUN_1800244d0(uVar6);
  iVar4 = FUN_1800244d0(lVar7);
  if (iVar4 == 0) {
    if (iVar3 != iVar2) {
      cVar1 = FUN_1800b2590(lVar7);
      if (cVar1 != '\0') {
        uVar5 = FUN_1800b4840(lVar7);
        FUN_180048f90(iVar3,uVar5);
        FUN_180048fc0(iVar3,0);
        iVar2 = FUN_1800b48c0(lVar7);
        FUN_180049170(iVar3,iVar2 + 1);
        iVar2 = *(int *)(lVar7 + 0x45c);
        uVar5 = FUN_1800244d0(lVar7);
        FUN_18008b9b0(uVar5,0,iVar3,iVar2 != 0,0,0);
        return 0x14;
      }
      cVar1 = FUN_1800b1d30(uVar6,iVar3);
      if (cVar1 == '\0') {
        return 0x14;
      }
      return 0x13;
    }
    uVar5 = FUN_1800b4910(uVar8);
    FUN_1800b17c0(lVar7,uVar5);
    FUN_1800b27f0(uVar8);
    FUN_1800b1690(lVar7,uVar8);
    FUN_1800b2500(lVar7);
    cVar1 = FUN_1800b1d30(uVar6,*(undefined4 *)(&DAT_18034b208 + (longlong)iVar3 * 4));
    if (cVar1 == '\0') {
      cVar1 = FUN_1800b1d80(lVar7);
      iVar2 = FUN_18019c090();
      if (cVar1 != '\0') {
        if (iVar2 != 1) {
          FUN_1800b27a0(uVar6,iVar3);
        }
        uVar5 = FUN_1800b4840(lVar7);
        FUN_180048f90(iVar3,uVar5);
        FUN_180048fc0(iVar3,0);
        uVar5 = FUN_1800b48c0(lVar7);
        FUN_180049170(iVar3,uVar5);
        uVar5 = FUN_1800b48b0(lVar7);
        FUN_180049110(iVar3,uVar5);
        iVar2 = FUN_18019c090();
        if (iVar2 == 2) {
          return 0x14;
        }
        cVar1 = FUN_180007450();
        if ((cVar1 != '\0') && (iVar2 = FUN_18019c090(), iVar2 == 0)) {
          return 0x14;
        }
        iVar2 = *(int *)(lVar7 + 0x45c);
        uVar5 = FUN_1800244d0(lVar7);
        FUN_18008b9b0(uVar5,1,iVar3,iVar2 != 0,0,0);
        return 0x14;
      }
      if (((iVar2 == 2) && (cVar1 = FUN_1801d8700(), cVar1 == '\0')) &&
         (cVar1 = FUN_1801d4b30(), cVar1 == '\0')) {
        return 0x14;
      }
      goto LAB_1800db79d;
    }
  }
  else {
    if (iVar4 != 1) {
      return 0x13;
    }
    if (iVar3 != iVar2) {
      cVar1 = FUN_1800b1d30(uVar6,iVar3);
      if (cVar1 == '\0') {
        iVar2 = *(int *)(lVar7 + 0x45c);
        uVar5 = FUN_1800244d0(lVar7);
        FUN_18008b9b0(uVar5,0,iVar3,iVar2 != 0,0,0);
        return 0x14;
      }
      return 0x13;
    }
    uVar5 = FUN_1800b4910(uVar8);
    FUN_1800b17c0(lVar7,uVar5);
    FUN_1800b27f0(uVar8);
    FUN_1800b1690(lVar7,uVar8);
    FUN_1800b1850(lVar7,uVar8);
    FUN_1800b2500(lVar7);
    cVar1 = FUN_1800b1d30(uVar6,*(undefined4 *)(&DAT_18034b208 + (longlong)iVar3 * 4));
    if (cVar1 == '\0') {
      cVar1 = FUN_1800b1d80(lVar7);
      if (cVar1 != '\0') {
        FUN_1800b27a0(uVar6,iVar3);
        FUN_180048fc0(iVar3,0);
        uVar5 = FUN_1800b48c0(lVar7);
        FUN_180049170(iVar3,uVar5);
        lVar9 = FUN_180095510();
        uVar12 = 0;
        uVar11 = 0;
        if (lVar9 != 0) {
          if (((*(char *)(lVar9 + 0xbc) != '\0') && (*(char *)(lVar9 + 0xcb) == '\0')) ||
             (uVar12 = 0, *(char *)(lVar9 + 0xcc) != '\0')) {
            uVar12 = 1;
          }
          uVar11 = 0;
          if (*(char *)(lVar9 + 0xbd) != '\0') {
            uVar11 = 1;
          }
        }
        iVar2 = *(int *)(lVar7 + 0x45c);
        uVar5 = FUN_1800244d0(lVar7);
        FUN_18008b9b0(uVar5,1,iVar3,iVar2 != 0,uVar12,uVar11);
        iVar2 = FUN_18019c090();
        if (iVar2 != 3) {
          return 0x14;
        }
        FUN_1801a5f40(2);
        return 0x14;
      }
LAB_1800db79d:
      FUN_1800b1ab0(uVar8,0);
      FUN_180101970(DAT_18070fb10);
      FUN_1800ff970(DAT_18070fb10,0);
      cVar1 = FUN_1800cc240(iVar3);
      if (cVar1 != '\0') {
        return 0x13;
      }
      uVar10 = FUN_1800b48c0(lVar7);
      if ((uVar10 & 1) != 0) {
        _guard_check_icall(0xb4);
        return 0x13;
      }
      return 0x13;
    }
  }
  return 0x11;
}



