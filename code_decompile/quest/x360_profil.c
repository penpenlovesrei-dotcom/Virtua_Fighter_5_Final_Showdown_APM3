// ===================================================
// 821DC9C0  ->  FUN_821dc9c0  (entree 821dc9c0)
// ===================================================

undefined4 FUN_821dc9c0(int param_1)

{
  return *(undefined4 *)(param_1 + 8);
}



// ===================================================
// 8230B5B8  ->  FUN_8230b5b8  (entree 8230b5b8)
// ===================================================

ulonglong FUN_8230b5b8(void)

{
  ulonglong uVar1;
  
  FUN_822da898();
  uVar1 = FUN_822dac40();
  if ((uVar1 & 0xffffffff) == 0) {
    return uVar1;
  }
  return uVar1 + 0xc0;
}



