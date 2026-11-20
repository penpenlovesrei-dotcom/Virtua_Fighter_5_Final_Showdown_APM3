// ===================================================
// 1800A78A0  ->  FUN_1800a78a0  (entree 1800a78a0)
// ===================================================

undefined8 FUN_1800a78a0(void)

{
  undefined8 uVar1;
  
  uVar1 = 2;
  if (*(char *)(DAT_1806f9a18 + 0x6d8) != '\0') {
    if (*(int *)(DAT_1806f9a18 + 0x6d0) == 0) {
      return 0;
    }
    uVar1 = 2;
    if (*(int *)(DAT_1806f9a18 + 0x6d0) == 1) {
      uVar1 = 1;
    }
  }
  return uVar1;
}



