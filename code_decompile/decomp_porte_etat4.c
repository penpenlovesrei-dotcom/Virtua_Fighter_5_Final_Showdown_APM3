// ===================================================
// 18006fa60  ->  FUN_18006fa60  (entree 18006fa60)
// ===================================================

void FUN_18006fa60(void)

{
  FUN_18006f380(&DAT_180642fe0);
  return;
}



// ===================================================
// 18006f620  ->  FUN_18006f620  (entree 18006f620)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18006f620(int param_1)

{
  int *piVar1;
  int iVar2;
  int *piVar3;
  int iVar4;
  
  iVar4 = 0;
  iVar2 = 0;
  piVar1 = &DAT_18034d510;
  do {
    if (*piVar1 == -1) break;
    FUN_1800f9c60(*piVar1,1);
    iVar2 = iVar2 + 1;
    piVar1 = piVar1 + 1;
  } while (iVar2 < 8);
  FUN_18003c200("EFFEFFCMN");
  piVar3 = (int *)(&DAT_18034d570 + (longlong)param_1 * 0x60);
  piVar1 = piVar3;
  do {
    if (*piVar1 == -1) {
      _DAT_180642fe0 = param_1;
      DAT_180642fe8 = piVar3;
      DAT_1806430b8 = 1;
      return;
    }
    FUN_1800f9c60(*piVar1,1);
    iVar4 = iVar4 + 1;
    piVar1 = piVar1 + 1;
  } while (iVar4 < 8);
  _DAT_180642fe0 = param_1;
  DAT_180642fe8 = piVar3;
  DAT_1806430b8 = 1;
  return;
}



// ===================================================
// 18006f9c0  ->  FUN_18006f9c0  (entree 18006f9c0)
// ===================================================

void FUN_18006f9c0(char param_1)

{
  longlong *plVar1;
  int iVar2;
  int iVar3;
  longlong *plVar4;
  
  if (((DAT_1806430bc != param_1) && (DAT_1806430bc = param_1, DAT_1806430b8 == 4)) &&
     (iVar3 = 0, 0 < DAT_180642ff0)) {
    plVar4 = &DAT_180643038;
    iVar2 = DAT_180642ff0;
    do {
      plVar1 = (longlong *)*plVar4;
      if (plVar1 != (longlong *)0x0) {
        (**(code **)(*plVar1 + 0x50))(plVar1,param_1);
        iVar2 = DAT_180642ff0;
        param_1 = DAT_1806430bc;
      }
      iVar3 = iVar3 + 1;
      plVar4 = plVar4 + 1;
    } while (iVar3 < iVar2);
  }
  return;
}



// ===================================================
// 18006f350  ->  FUN_18006f350  (entree 18006f350)
// ===================================================

undefined * FUN_18006f350(void)

{
  return &DAT_180677330;
}



