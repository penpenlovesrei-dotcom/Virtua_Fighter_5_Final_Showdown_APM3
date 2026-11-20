// ===================================================
// 1801DE7B0  ->  FUN_1801de7b0  (entree 1801de7b0)
// ===================================================

undefined8 FUN_1801de7b0(longlong param_1)

{
  char cVar1;
  int iVar2;
  
  if ((DAT_180c3b6f0 == 0) || (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) == 0)) {
    FUN_1801bc0b0(param_1);
    FUN_1801bc060(param_1 + 0x240);
    FUN_1801bc060(param_1 + 0x298);
    FUN_1801bc060(param_1 + 0x2f0);
    FUN_1802450a0(param_1 + 0x348);
    FUN_1802450a0(param_1 + 0x4c0);
    if (*(int *)(param_1 + 0x638) != 0) {
      FUN_180029be0();
      *(undefined4 *)(param_1 + 0x638) = 0;
    }
    if (*(longlong *)(param_1 + 0x650) != 0) {
      if (*(int *)(param_1 + 0x58) == 5) {
        *(undefined1 *)(param_1 + 0x63d) = 1;
        *(undefined1 *)(param_1 + 0x63f) = 0;
        return 1;
      }
      if (*(int *)(param_1 + 0x58) == 7) {
        *(undefined1 *)(param_1 + 0x63e) = 1;
      }
    }
    *(undefined1 *)(param_1 + 0x63f) = 0;
    return 1;
  }
  if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
    iVar2 = (**(code **)(DAT_180c3b6f0 + 0x1fe10))(*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0x4c);
    if (iVar2 == 1) {
      if (*(char *)(param_1 + 0x2a09) == '\0') {
        FUN_1801de560(param_1 + 0x2a00);
      }
      cVar1 = FUN_180197350(PTR_DAT_180409ff0);
      if (cVar1 == '\0') {
        FUN_1801973d0(PTR_DAT_180409ff0);
        FUN_1801973f0(PTR_DAT_180409ff0);
        FUN_180087420(0x49,_guard_check_icall);
        FUN_180087420(0x4a,FUN_1801e2a70);
        FUN_180087420(0x4b,_guard_check_icall);
        FUN_180087420(0x4c,FUN_1801e2a70);
        return 1;
      }
    }
  }
  return 0;
}



