// ===================================================
// 1800B6D90  ->  FUN_1800b6d90  (entree 1800b6d90)
// ===================================================

undefined8 FUN_1800b6d90(int param_1,int param_2)

{
  char cVar1;
  int iVar2;
  undefined8 uVar3;
  longlong lVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  
  uVar6 = 0;
  uVar3 = FUN_180190a50();
  lVar4 = FUN_1800b23a0();
  if ((((lVar4 == 0) || (cVar1 = FUN_1800b1d30(lVar4,param_1), cVar1 == '\0')) &&
      (cVar1 = FUN_180194290(PTR_DAT_180409610,param_1), cVar1 != '\0')) &&
     (((cVar1 = FUN_180007450(PTR_DAT_180346c80), cVar1 == '\0' &&
       (cVar1 = FUN_180007450(PTR_DAT_180346c80), cVar1 == '\0')) ||
      ((param_2 == 1 &&
       ((lVar4 = FUN_18008b0c0(), lVar4 == 0 || (cVar1 = FUN_18008ab50(lVar4), cVar1 != '\0'))))))))
  {
    if (param_1 == 0) {
      uVar5 = 0;
    }
    else {
      if (param_1 != 1) {
        return 0;
      }
      uVar5 = 1;
    }
    lVar4 = FUN_18005f830(uVar5);
    if (lVar4 != 0) {
      _guard_check_icall(lVar4,param_2);
      cVar1 = FUN_180029fb0(lVar4);
      if (cVar1 != '\0') {
        if (((param_2 == 1) && (lVar4 = FUN_18008b0c0(), lVar4 != 0)) &&
           (iVar2 = FUN_18008b110(lVar4), iVar2 == 0)) {
          uVar5 = 2;
          if (DAT_180c3b703 != '\0') {
            uVar5 = 0x10;
          }
          cVar1 = FUN_180190bc0(uVar3,uVar5);
          if (cVar1 != '\0') {
            if ((DAT_180c3b701 == '\0') || ((*(uint *)(DAT_180c3b6f0 + 0x10) & 2) != 0)) {
              *(uint *)(DAT_180c3b6f0 + 0x10) = *(uint *)(DAT_180c3b6f0 + 0x10) | 4;
              uVar6 = 1;
            }
            else {
              *(uint *)(DAT_180c3b6f0 + 0x10) = *(uint *)(DAT_180c3b6f0 + 0x10) | 8;
            }
          }
        }
        else {
          cVar1 = FUN_180190bc0(uVar3,2);
          if (cVar1 != '\0') {
            uVar6 = 1;
          }
        }
      }
    }
  }
  return uVar6;
}



// ===================================================
// 1800DC890  ->  FUN_1800dc890  (entree 1800dc890)
// ===================================================

undefined4 FUN_1800dc890(void)

{
  undefined8 uVar1;
  char cVar2;
  undefined4 uVar3;
  int iVar4;
  undefined8 uVar5;
  
  FUN_1801b7060(0);
  cVar2 = FUN_180197350(PTR_DAT_180409ff0);
  if (cVar2 != '\0') {
    return 0;
  }
  FUN_1800d41e0(PTR_DAT_18039f560,3);
  FUN_18014ef10(PTR_DAT_1806487b0);
  cVar2 = FUN_180007450();
  if (cVar2 != '\0') {
    return 0;
  }
  uVar5 = FUN_1800b23a0();
  uVar1 = FUN_1800b24b0(uVar5);
  uVar3 = FUN_1800244d0(uVar5);
  FUN_1800b3100(uVar5);
  _guard_check_icall();
  iVar4 = FUN_1800244d0(uVar1);
  if (iVar4 == 0) {
    uVar5 = FUN_1800b2450(uVar1,uVar3);
    _guard_check_icall(uVar3,uVar5,0,0);
    uVar5 = FUN_1800b2450(uVar1,uVar3);
  }
  else {
    if (iVar4 != 1) goto LAB_1800dc9ce;
    uVar5 = FUN_1800b2450(uVar1,0);
    _guard_check_icall(0,uVar5,0,0);
    uVar5 = FUN_1800b2450(uVar1,1);
    _guard_check_icall(1,uVar5,0);
    uVar5 = FUN_1800b2450(uVar1,0);
    _guard_check_icall(0,uVar5,0,0xffffffff,0);
    uVar5 = FUN_1800b2450(uVar1,1);
    uVar3 = 1;
  }
  _guard_check_icall(uVar3,uVar5,0,0xffffffff,0);
LAB_1800dc9ce:
  FUN_1800b7000();
  FUN_1800bd070("GAME_VS",uVar1);
  _guard_check_icall();
  FUN_180087550(9,FUN_1800dbd60,0);
  FUN_180087550(0xf,FUN_1800dc520,0);
  FUN_180087550(0x10,FUN_1800dbb90,0);
  uVar1 = FUN_1801bb730();
  _guard_check_icall(uVar1);
  if (DAT_180c3b701 == '\0') {
    FUN_1801e93c0();
  }
  return 1;
}



