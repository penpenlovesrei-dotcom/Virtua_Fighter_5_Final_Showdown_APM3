// ===================================================
// 18016CF50  ->  FUN_18016cf50  (entree 18016cf50)
// ===================================================

void FUN_18016cf50(longlong param_1)

{
  FUN_180170010(param_1 + 0x68);
  return;
}



// ===================================================
// 18016CF30  ->  FUN_18016cf30  (entree 18016cf30)
// ===================================================

void FUN_18016cf30(longlong param_1)

{
  FUN_18016fff0(param_1 + 0x68);
  return;
}



// ===================================================
// 18016CF20  ->  FUN_18016cf20  (entree 18016cf20)
// ===================================================

void FUN_18016cf20(longlong param_1)

{
  FUN_18016ffd0(param_1 + 0x68);
  return;
}



// ===================================================
// 18016CF40  ->  FUN_18016cf40  (entree 18016cf40)
// ===================================================

void FUN_18016cf40(longlong param_1)

{
  FUN_180007440(param_1 + 0x68);
  return;
}



// ===================================================
// 1800B2F80  ->  FUN_1800b2f80  (entree 1800b2f80)
// ===================================================

void FUN_1800b2f80(longlong param_1,int param_2,undefined4 param_3,undefined4 param_4,
                  undefined4 param_5,undefined4 param_6)

{
  longlong lVar1;
  
  lVar1 = (longlong)param_2;
  *(undefined4 *)(param_1 + 0x38 + lVar1 * 4) = param_5;
  *(undefined4 *)(param_1 + 0x40 + lVar1 * 4) = param_6;
  *(undefined4 *)(param_1 + 0x28 + lVar1 * 4) = param_3;
  *(undefined4 *)(param_1 + 0x30 + lVar1 * 4) = param_4;
  return;
}



// ===================================================
// 1800B2FA0  ->  FUN_1800b2fa0  (entree 1800b2fa0)
// ===================================================

ulonglong FUN_1800b2fa0(longlong param_1,uint param_2,int param_3,uint param_4)

{
  char cVar1;
  ulonglong in_RAX;
  longlong lVar2;
  undefined4 uVar3;
  longlong lVar4;
  byte bVar5;
  
  lVar4 = (longlong)(int)param_2;
  if (1 < param_2) {
    return in_RAX & 0xffffffffffffff00;
  }
  bVar5 = 0;
  if (*(char *)(lVar4 + 0xc + param_1) == '\0') {
    uVar3 = 0;
    if (param_2 != 0) {
      if (param_2 != 1) goto LAB_1800b30da;
      uVar3 = 1;
    }
    lVar2 = FUN_18005f830(uVar3);
    if ((lVar2 != 0) && (cVar1 = FUN_180029fb0(lVar2), cVar1 != '\0')) {
      *(undefined1 *)(lVar4 + 0xc + param_1) = 1;
      *(undefined4 *)(param_1 + 0x28 + lVar4 * 4) = 0x15;
      *(undefined4 *)(param_1 + 0x30 + lVar4 * 4) = 0xffffffff;
      bVar5 = 1;
      *(undefined4 *)(param_1 + 0x38 + lVar4 * 4) = 0xffffffff;
      *(undefined4 *)(param_1 + 0x40 + lVar4 * 4) = 0xffffffff;
      *(undefined1 *)(lVar4 + 0x48 + param_1) = 0;
      _guard_check_icall(param_4 == 1,1);
      if (param_3 == 0) {
        if (param_4 == 0) {
          _guard_check_icall(PTR_DAT_180346c80,param_2,0);
          FUN_1800491a0(param_2);
        }
        else if (param_4 == 1) {
          _guard_check_icall(PTR_DAT_180346c80,param_2);
          _guard_check_icall(PTR_DAT_180346c80,param_2,1);
          FUN_180048950(param_2);
        }
      }
      else if ((param_3 == 1) && (param_4 < 3)) {
        _guard_check_icall(PTR_DAT_180346c80,param_2,0);
        FUN_1800491a0(param_2);
        FUN_1800488e0();
      }
    }
  }
LAB_1800b30da:
  return (ulonglong)bVar5;
}



