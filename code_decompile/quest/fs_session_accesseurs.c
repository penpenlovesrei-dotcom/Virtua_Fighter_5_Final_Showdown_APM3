// ===================================================
// 1800B23E0  ->  FUN_1800b23e0  (entree 1800b23e0)
// ===================================================

undefined4 FUN_1800b23e0(longlong param_1,int param_2)

{
  return *(undefined4 *)(param_1 + 0x28 + (longlong)param_2 * 4);
}



// ===================================================
// 1800B23F0  ->  FUN_1800b23f0  (entree 1800b23f0)
// ===================================================

undefined4 FUN_1800b23f0(longlong param_1,int param_2)

{
  return *(undefined4 *)(param_1 + 0x30 + (longlong)param_2 * 4);
}



// ===================================================
// 1800B2400  ->  FUN_1800b2400  (entree 1800b2400)
// ===================================================

undefined4 FUN_1800b2400(longlong param_1,int param_2)

{
  return *(undefined4 *)(param_1 + 0x38 + (longlong)param_2 * 4);
}



// ===================================================
// 1800B2410  ->  FUN_1800b2410  (entree 1800b2410)
// ===================================================

undefined4 FUN_1800b2410(longlong param_1,int param_2)

{
  return *(undefined4 *)(param_1 + 0x40 + (longlong)param_2 * 4);
}



// ===================================================
// 1800B48C0  ->  FUN_1800b48c0  (entree 1800b48c0)
// ===================================================

undefined4 FUN_1800b48c0(longlong param_1)

{
  return *(undefined4 *)(param_1 + 0x3f0);
}



// ===================================================
// 1800B2590  ->  FUN_1800b2590  (entree 1800b2590)
// ===================================================

ulonglong FUN_1800b2590(longlong param_1)

{
  ulonglong in_RAX;
  ulonglong uVar1;
  
  uVar1 = in_RAX & 0xffffffffffffff00;
  if ((*(int *)(param_1 + 8) == 0) && (uVar1 = 0, *(int *)(param_1 + 0x3f0) == 7)) {
    uVar1 = 1;
  }
  return uVar1;
}



// ===================================================
// 1800B2680  ->  FUN_1800b2680  (entree 1800b2680)
// ===================================================

ulonglong FUN_1800b2680(longlong param_1)

{
  int iVar1;
  ulonglong uVar2;
  
  if (*(int *)(param_1 + 8) == 0) {
    iVar1 = FUN_18019c090();
    if (iVar1 == 2) {
      iVar1 = FUN_1801d43c0();
      return (ulonglong)
             CONCAT31((int3)((uint)(iVar1 + -1) >> 8),*(int *)(param_1 + 0x3f0) == iVar1 + -1);
    }
    return (ulonglong)(*(int *)(param_1 + 0x3f0) == 7);
  }
  if (*(int *)(param_1 + 8) == 1) {
    uVar2 = FUN_1801a5b40(*(undefined4 *)(param_1 + 0x3f0));
    return uVar2;
  }
  return 0;
}



// ===================================================
// 1800B25F0  ->  FUN_1800b25f0  (entree 1800b25f0)
// ===================================================

undefined1 FUN_1800b25f0(longlong param_1)

{
  undefined1 uVar1;
  int iVar2;
  
  if (*(int *)(param_1 + 8) == 0) {
    iVar2 = FUN_18019c090();
    if (iVar2 != 2) {
      return *(int *)(param_1 + 0x3f0) == 6;
    }
    iVar2 = FUN_1801d43c0();
    if (*(int *)(param_1 + 0x3f0) == iVar2) {
      return true;
    }
  }
  else if (*(int *)(param_1 + 8) == 1) {
    uVar1 = FUN_1801a5b40(*(undefined4 *)(param_1 + 0x3f0));
    return uVar1;
  }
  return false;
}



// ===================================================
// 1800B4900  ->  FUN_1800b4900  (entree 1800b4900)
// ===================================================

undefined4 FUN_1800b4900(longlong param_1)

{
  return *(undefined4 *)(param_1 + 0x3f4);
}



// ===================================================
// 1800B47D0  ->  FUN_1800b47d0  (entree 1800b47d0)
// ===================================================

undefined4 FUN_1800b47d0(longlong param_1,uint param_2)

{
  if (param_2 < 10) {
    return *(undefined4 *)((ulonglong)param_2 * 0x5c + 0x1c + param_1);
  }
  return 0xffffffff;
}



// ===================================================
// 1800B4760  ->  FUN_1800b4760  (entree 1800b4760)
// ===================================================

undefined4 FUN_1800b4760(longlong param_1,uint param_2)

{
  if (param_2 < 10) {
    return *(undefined4 *)((ulonglong)param_2 * 0x5c + 0x70 + param_1);
  }
  return 0;
}



