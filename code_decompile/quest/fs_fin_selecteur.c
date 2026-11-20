// ===================================================
// 1800DB399  ->  FUN_1800db270  (entree 1800db270)
// ===================================================

undefined4 FUN_1800db270(void)

{
  undefined8 uVar1;
  char cVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  int iVar7;
  
  uVar1 = FUN_1800b23a0();
  FUN_1800d41e0(PTR_DAT_18039f560,3);
  if (DAT_18070c528 != 1) {
    cVar2 = FUN_180244ea0(DAT_180714928);
    if (cVar2 != '\0') {
      cVar2 = FUN_18016d330(DAT_180714928);
      if (cVar2 == '\0') {
        cVar2 = FUN_18016c540(DAT_180714928,0);
        if ((cVar2 != '\0') && (cVar2 = FUN_1800b6d80(0), cVar2 != '\0')) {
          FUN_1800b2fa0(uVar1,0,1);
          FUN_18016cf00(DAT_180714928,0);
        }
        cVar2 = FUN_18016c540(DAT_180714928,1);
        if (cVar2 == '\0') {
          return 0;
        }
        cVar2 = FUN_1800b6d80(1);
        if (cVar2 == '\0') {
          return 0;
        }
        FUN_1800b2fa0(uVar1,1,1,0);
        FUN_18016cf00(DAT_180714928,1);
        return 0;
      }
      iVar7 = 0;
      do {
        uVar3 = FUN_18016cf50(DAT_180714928,iVar7);
        uVar4 = FUN_18016cf30(DAT_180714928,iVar7);
        uVar5 = FUN_18016cf20(DAT_180714928,iVar7,uVar4);
        uVar6 = FUN_18016cf40(DAT_180714928,iVar7);
        FUN_1800b2f80(uVar1,iVar7,uVar3,uVar5,uVar4,uVar6);
        iVar7 = iVar7 + 1;
      } while (iVar7 < 2);
    }
    DAT_18070c528 = 1;
  }
  cVar2 = FUN_180244ea0(DAT_180714928);
  if (cVar2 == '\0') {
    if ((DAT_180c3b701 == '\0') && (cVar2 = FUN_18016d360(DAT_180714928), cVar2 != '\0')) {
      FUN_180186d40(0);
      FUN_1800da9a0(4);
      return 1;
    }
    cVar2 = FUN_180007450();
    if ((cVar2 == '\0') && (cVar2 = FUN_180007450(), cVar2 == '\0')) {
      if (*(char *)(DAT_18070fb10 + 0x19) != '\0') {
        uVar1 = FUN_180101820(DAT_18070fb10,0);
        _guard_check_icall(0,uVar1,0x4b0);
      }
      if (*(char *)(DAT_18070fb10 + 0x5b9) != '\0') {
        uVar1 = FUN_180101820(DAT_18070fb10,1);
        _guard_check_icall(1,uVar1,0x4b0);
      }
      return 1;
    }
  }
  return 0;
}



