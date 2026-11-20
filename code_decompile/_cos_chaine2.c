// ===================================================
// 821DF8BC  ->  FUN_821df868  (entree 821df868)
// ===================================================

undefined8 FUN_821df868(undefined8 param_1)

{
  undefined8 uVar1;
  ulonglong uVar2;
  int iVar3;
  int iVar4;
  
  iVar4 = (int)param_1;
  if (((iVar4 == 0) || (iVar4 == 1)) && (DAT_82797cb4 == 0)) {
    uVar2 = FUN_82142ee0(0xbe8);
    if ((uVar2 & 0xffffffff) == 0) {
      iVar3 = 0;
    }
    else {
      iVar3 = FUN_821df780(uVar2,0);
    }
    DAT_82797cb4 = iVar3;
    *(int *)(iVar3 + 8) = iVar4;
    FUN_821dd578(iVar3,param_1,0,0);
    FUN_821d0098();
    uVar1 = 1;
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}



