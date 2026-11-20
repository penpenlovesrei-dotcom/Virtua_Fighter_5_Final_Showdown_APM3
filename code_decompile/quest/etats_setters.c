// ===================================================
// 1800DA9A0  ->  FUN_1800da9a0  (entree 1800da9a0)
// ===================================================

void FUN_1800da9a0(undefined4 param_1)

{
  DAT_18070c4f4 = param_1;
  DAT_18070c500 = 1;
  DAT_18070c51c = 0;
  return;
}



// ===================================================
// 1800DA932  ->  FUN_1800da800  (entree 1800da800)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1800da800(int param_1,int param_2)

{
  longlong lVar1;
  ulonglong uVar2;
  int *piVar3;
  ulonglong uVar4;
  uint uVar5;
  ulonglong uVar6;
  
  uVar6 = 0;
  if (param_1 != 10) {
    lVar1 = (longlong)DAT_18070c4f0;
    _DAT_18070c4f8 = DAT_18070c4f0;
    DAT_18070c4f4 = 10;
    DAT_18070c4fc = 0;
    DAT_18070c500 = 0;
    _DAT_18070c504 = 0;
    DAT_18070c4f0 = param_1;
    FUN_180215580(10,"[%s]->[%s]\n",(&PTR_s_STARTUP_1803a0c80)[lVar1],
                  (&PTR_s_STARTUP_1803a0c80)[param_1]);
    uVar2 = uVar6;
    uVar4 = uVar6;
    do {
      if (*(int *)((longlong)&DAT_1803a0190 + uVar2) == DAT_18070c4f0) {
        if (uVar4 * 0x68 != -0x1803a0190) {
          DAT_18070c4f4 = *(undefined4 *)(&UNK_1803a01f0 + uVar4 * 0x68);
        }
        break;
      }
      uVar4 = uVar4 + 1;
      uVar2 = uVar2 + 0x68;
    } while (uVar2 < 0x410);
  }
  _DAT_18070c514 = DAT_18070c50c;
  DAT_18070c50c = 0x37;
  DAT_18070c510 = 0x37;
  DAT_18070c518 = 0;
  DAT_18070c51c = 0;
  _DAT_18070c520 = 0;
  uVar2 = uVar6;
  uVar4 = uVar6;
  while (*(int *)((longlong)&DAT_1803a0190 + uVar2) != DAT_18070c4f0) {
    uVar4 = uVar4 + 1;
    uVar2 = uVar2 + 0x68;
    if (0x40f < uVar2) {
      return;
    }
  }
  lVar1 = uVar4 * 0x68;
  if (lVar1 != -0x1803a0190) {
    piVar3 = (int *)(&UNK_1803a01b0 + lVar1);
    if (param_2 == 0x37) {
      DAT_18070c50c = *piVar3;
      DAT_18070c510 = *(undefined4 *)(&UNK_1803a01b4 + lVar1);
      return;
    }
    while (*piVar3 != 0x37) {
      uVar5 = (int)uVar6 + 1;
      if (*piVar3 == param_2) {
        DAT_18070c50c = param_2;
        DAT_18070c510 = *(undefined4 *)(&UNK_1803a01b0 + (longlong)(int)uVar5 * 4 + lVar1);
        DAT_18070c518 = 0;
        DAT_18070c51c = 0;
        _DAT_18070c520 = 0;
        return;
      }
      piVar3 = piVar3 + 1;
      uVar6 = (ulonglong)uVar5;
      if (0xe < (int)uVar5) {
        return;
      }
    }
  }
  return;
}



// ===================================================
// 1800DA8A2  ->  FUN_1800da800  (entree 1800da800)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1800da800(int param_1,int param_2)

{
  longlong lVar1;
  ulonglong uVar2;
  int *piVar3;
  ulonglong uVar4;
  uint uVar5;
  ulonglong uVar6;
  
  uVar6 = 0;
  if (param_1 != 10) {
    lVar1 = (longlong)DAT_18070c4f0;
    _DAT_18070c4f8 = DAT_18070c4f0;
    DAT_18070c4f4 = 10;
    DAT_18070c4fc = 0;
    DAT_18070c500 = 0;
    _DAT_18070c504 = 0;
    DAT_18070c4f0 = param_1;
    FUN_180215580(10,"[%s]->[%s]\n",(&PTR_s_STARTUP_1803a0c80)[lVar1],
                  (&PTR_s_STARTUP_1803a0c80)[param_1]);
    uVar2 = uVar6;
    uVar4 = uVar6;
    do {
      if (*(int *)((longlong)&DAT_1803a0190 + uVar2) == DAT_18070c4f0) {
        if (uVar4 * 0x68 != -0x1803a0190) {
          DAT_18070c4f4 = *(undefined4 *)(&UNK_1803a01f0 + uVar4 * 0x68);
        }
        break;
      }
      uVar4 = uVar4 + 1;
      uVar2 = uVar2 + 0x68;
    } while (uVar2 < 0x410);
  }
  _DAT_18070c514 = DAT_18070c50c;
  DAT_18070c50c = 0x37;
  DAT_18070c510 = 0x37;
  DAT_18070c518 = 0;
  DAT_18070c51c = 0;
  _DAT_18070c520 = 0;
  uVar2 = uVar6;
  uVar4 = uVar6;
  while (*(int *)((longlong)&DAT_1803a0190 + uVar2) != DAT_18070c4f0) {
    uVar4 = uVar4 + 1;
    uVar2 = uVar2 + 0x68;
    if (0x40f < uVar2) {
      return;
    }
  }
  lVar1 = uVar4 * 0x68;
  if (lVar1 != -0x1803a0190) {
    piVar3 = (int *)(&UNK_1803a01b0 + lVar1);
    if (param_2 == 0x37) {
      DAT_18070c50c = *piVar3;
      DAT_18070c510 = *(undefined4 *)(&UNK_1803a01b4 + lVar1);
      return;
    }
    while (*piVar3 != 0x37) {
      uVar5 = (int)uVar6 + 1;
      if (*piVar3 == param_2) {
        DAT_18070c50c = param_2;
        DAT_18070c510 = *(undefined4 *)(&UNK_1803a01b0 + (longlong)(int)uVar5 * 4 + lVar1);
        DAT_18070c518 = 0;
        DAT_18070c51c = 0;
        _DAT_18070c520 = 0;
        return;
      }
      piVar3 = piVar3 + 1;
      uVar6 = (ulonglong)uVar5;
      if (0xe < (int)uVar5) {
        return;
      }
    }
  }
  return;
}



