// ===================================================
// 1800B23A0  ->  FUN_1800b23a0  (entree 1800b23a0)
// ===================================================

undefined8 FUN_1800b23a0(void)

{
  return DAT_1806f9c18;
}



// ===================================================
// 1800B3620  ->  FUN_1800b3620  (entree 1800b3620)
// ===================================================

undefined1 FUN_1800b3620(uint param_1)

{
  char cVar1;
  longlong lVar2;
  longlong lVar3;
  undefined8 uVar4;
  longlong lVar5;
  
  lVar5 = (longlong)(int)param_1;
  if ((param_1 < 2) && (DAT_1806f9c18 == 0)) {
    lVar2 = FUN_180218930(0x16e0);
    if (lVar2 == 0) {
      lVar2 = 0;
    }
    else {
      lVar2 = FUN_1800afa70(lVar2,0);
    }
    DAT_1806f9c18 = lVar2;
    if (lVar2 != 0) {
      *(uint *)(lVar2 + 8) = param_1;
      if ((param_1 < 2) && (*(char *)(lVar5 + 0xc + lVar2) == '\0')) {
        if (param_1 == 0) {
          uVar4 = 0;
        }
        else {
          if (param_1 != 1) goto LAB_1800b3710;
          uVar4 = 1;
        }
        lVar3 = FUN_18005f830(uVar4);
        if (lVar3 != 0) {
          cVar1 = FUN_180029fb0(lVar3);
          if (cVar1 != '\0') {
            *(undefined1 *)(lVar5 + 0xc + lVar2) = 1;
            *(undefined4 *)(lVar2 + 0x28 + lVar5 * 4) = 0x15;
            *(undefined4 *)(lVar2 + 0x30 + lVar5 * 4) = 0xffffffff;
            *(undefined4 *)(lVar2 + 0x38 + lVar5 * 4) = 0xffffffff;
            *(undefined4 *)(lVar2 + 0x40 + lVar5 * 4) = 0xffffffff;
            *(undefined1 *)(lVar5 + 0x48 + lVar2) = 0;
            _guard_check_icall(0,1);
            _guard_check_icall(PTR_DAT_180346c80,param_1,0);
            FUN_1800491a0(param_1);
          }
        }
      }
LAB_1800b3710:
      FUN_18008b210();
      return 1;
    }
  }
  return 0;
}



