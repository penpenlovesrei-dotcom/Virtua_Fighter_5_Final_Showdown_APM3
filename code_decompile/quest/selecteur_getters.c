// ===================================================
// 18016FFF0  ->  FUN_18016fff0  (entree 18016fff0)
// ===================================================

undefined4 FUN_18016fff0(undefined8 param_1,int param_2)

{
  return *(undefined4 *)(&DAT_180714960 + (longlong)param_2 * 0x28);
}



// ===================================================
// 18016FFD0  ->  FUN_18016ffd0  (entree 18016ffd0)
// ===================================================

undefined4 FUN_18016ffd0(undefined8 param_1,int param_2,int param_3)

{
  return *(undefined4 *)(&DAT_180714950 + ((longlong)param_2 * 5 + (longlong)param_3) * 8);
}



// ===================================================
// 1800B6D80  ->  FUN_1800b6d80  (entree 1800b6d80)
// ===================================================

void FUN_1800b6d80(undefined8 param_1)

{
  FUN_1800b6d90(param_1,0);
  return;
}



