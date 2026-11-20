// ===================================================
// 82322798  ->  FUN_82322798  (entree 82322798)
// ===================================================

undefined4 FUN_82322798(ulonglong param_1)

{
  char cVar2;
  undefined4 uVar1;
  
  if ((DAT_82ad1c40 == 0) || (0x1d9f < (int)param_1)) {
    uVar1 = 0;
  }
  else {
    cVar2 = FUN_82144b10();
    if ((cVar2 == '\0') && ((param_1 & 0xffffffff) < 0x2a)) {
      uVar1 = *(undefined4 *)((int)((param_1 + 0x2a & 0xffffffff) << 2) + DAT_82ad1c40);
    }
    else {
      uVar1 = *(undefined4 *)((int)((param_1 & 0xffffffff) << 2) + DAT_82ad1c40);
    }
  }
  return uVar1;
}



