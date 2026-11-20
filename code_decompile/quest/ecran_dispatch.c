// ===================================================
// 1800DA550  ->  FUN_1800da550  (entree 1800da550)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1800da550(void)

{
  bool bVar1;
  char cVar2;
  int iVar3;
  ulonglong uVar4;
  int *piVar5;
  undefined4 uVar6;
  ulonglong uVar7;
  ulonglong uVar8;
  
  iVar3 = FUN_180007440(PTR_DAT_180346c80);
  if (iVar3 != 0) {
    _guard_check_icall(iVar3);
  }
  if (DAT_18070c500 == '\0') {
    if ((DAT_18070c51c != '\0') && (DAT_18070c51d != '\0')) {
      cVar2 = FUN_180244f20();
      if (cVar2 != '\0') goto LAB_1800da7c8;
      uVar6 = 10;
      iVar3 = DAT_18070c510;
      goto LAB_1800da5de;
    }
  }
  else {
    if ((DAT_18070c501 != '\0') && (DAT_18070c51d != '\0')) {
      cVar2 = FUN_180244f20();
      if (cVar2 != '\0') goto LAB_1800da7c8;
      uVar6 = DAT_18070c4f4;
      iVar3 = 0x37;
      if (DAT_18070c51c != '\0') {
        iVar3 = DAT_18070c510;
      }
LAB_1800da5de:
      FUN_1800da800(uVar6,iVar3);
      DAT_18070c51d = '\0';
      DAT_18070c501 = '\0';
    }
    if ((DAT_18070c500 != '\0') && (DAT_18070c51d != '\0')) {
      DAT_18070c4fc = 2;
    }
  }
  uVar8 = 0;
  uVar4 = uVar8;
  uVar7 = uVar8;
  while (*(int *)((longlong)&DAT_1803a0190 + uVar4) != DAT_18070c4f0) {
    uVar7 = uVar7 + 1;
    uVar4 = uVar4 + 0x68;
    if (0x40f < uVar4) {
      _DAT_18070c504 = _DAT_18070c504 + 1;
      return;
    }
  }
  if (uVar7 * 0x68 == -0x1803a0190) goto LAB_1800da7c8;
  cVar2 = DAT_18070c4fc != 1;
  if ((code *)(&PTR_FUN_1803a0198)[uVar7 * 0xd + (longlong)DAT_18070c4fc] != (code *)0x0) {
    cVar2 = (*(code *)(&PTR_FUN_1803a0198)[uVar7 * 0xd + (longlong)DAT_18070c4fc])();
  }
  if (cVar2 == '\0') {
LAB_1800da6c8:
    if (DAT_18070c4fc == 0) goto LAB_1800da7c8;
  }
  else if (DAT_18070c4fc == 0) {
    DAT_18070c4fc = 1;
  }
  else if (DAT_18070c4fc == 1) {
    DAT_18070c4fc = 2;
  }
  else {
    if (DAT_18070c4fc != 2) goto LAB_1800da6c8;
    if (DAT_18070c500 == '\0') {
      DAT_18070c500 = '\x01';
      DAT_18070c51c = '\x01';
    }
    DAT_18070c501 = '\x01';
  }
  if (DAT_18070c51d == '\0') {
    if ((DAT_18070c500 != '\0') || (DAT_18070c51c != '\0')) {
      DAT_18070c518 = 2;
    }
    piVar5 = &DAT_1803a05a0;
    bVar1 = false;
    do {
      if (*piVar5 == DAT_18070c50c) {
        if (((uVar8 & 0x7ffffffffffffff) == 0x7fffffff3fe2fd3) ||
           (((DAT_18070c518 != 3 &&
             ((code *)(&PTR_FUN_1803a05a8)[uVar8 * 4 + (longlong)DAT_18070c518] != (code *)0x0)) &&
            (cVar2 = (*(code *)(&PTR_FUN_1803a05a8)[uVar8 * 4 + (longlong)DAT_18070c518])(),
            cVar2 == '\0')))) break;
        if (DAT_18070c518 == 0) {
          DAT_18070c518 = 1;
          break;
        }
        if (DAT_18070c518 == 1) {
          DAT_18070c518 = 2;
        }
        else if (DAT_18070c518 == 2) {
          bVar1 = true;
          break;
        }
        _DAT_18070c520 = _DAT_18070c520 + 1;
        goto LAB_1800da7c8;
      }
      uVar8 = uVar8 + 1;
      piVar5 = piVar5 + 8;
    } while (uVar8 < 0x37);
    _DAT_18070c520 = _DAT_18070c520 + 1;
    if (bVar1) {
      if (((DAT_18070c500 == '\0') && (DAT_18070c51c == '\0')) &&
         (DAT_18070c51c = '\x01', DAT_18070c510 == 0x37)) {
        DAT_18070c500 = '\x01';
        DAT_18070c510 = 0x37;
      }
      DAT_18070c51d = '\x01';
    }
  }
LAB_1800da7c8:
  _DAT_18070c504 = _DAT_18070c504 + 1;
  return;
}



