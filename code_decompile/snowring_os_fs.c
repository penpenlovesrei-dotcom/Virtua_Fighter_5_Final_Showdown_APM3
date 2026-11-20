// ===================================================
// 1800E0280  ->  FUN_1800e0280  (entree 1800e0280)
// ===================================================

longlong FUN_1800e0280(longlong param_1,ulonglong param_2)

{
  if ((*(longlong *)(param_1 + 0x30) != 0) &&
     (param_2 < (ulonglong)(*(longlong *)(param_1 + 0x40) - *(longlong *)(param_1 + 0x38) >> 6))) {
    return *(longlong *)(param_1 + 0x30) + param_2 * 0x40;
  }
  return 0;
}



// ===================================================
// 1801509C0  ->  FUN_1801509c0  (entree 1801509c0)
// ===================================================

undefined8 FUN_1801509c0(undefined8 param_1,int param_2)

{
  return *(undefined8 *)((longlong)param_2 * 0x5d68 + 0x28 + DAT_180713e30);
}



// ===================================================
// 1801509B0  ->  FUN_1801509b0  (entree 1801509b0)
// ===================================================

undefined8 FUN_1801509b0(void)

{
  return DAT_180713e80;
}



// ===================================================
// 180150920  ->  FUN_180150920  (entree 180150920)
// ===================================================

longlong FUN_180150920(undefined8 param_1,int param_2)

{
  if ((&DAT_180713e50)[(longlong)param_2 * 6] != -1) {
    return (longlong)param_2 * 0x5d68 + DAT_180713e30;
  }
  return 0;
}



