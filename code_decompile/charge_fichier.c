// ===================================================
// 180216620  ->  FUN_180216620  (entree 180216620)
// ===================================================

void FUN_180216620(int *param_1,char param_2)

{
  if ((*param_1 == 1) && (*(code **)(param_1 + 0xe) != (code *)0x0)) {
    (**(code **)(param_1 + 0xe))(*(undefined8 *)(param_1 + 0x14),*(undefined8 *)(param_1 + 0x1c));
  }
  FUN_180216a70(param_1);
  FUN_180216bb0(param_1);
  if (param_2 != '\0') {
    FUN_180216890();
  }
  return;
}



// ===================================================
// 180217BF0  ->  FUN_180217bf0  (entree 180217bf0)
// ===================================================

undefined1 FUN_180217bf0(longlong param_1)

{
  int iVar1;
  
  iVar1 = *(int *)(param_1 + 8);
  if (((iVar1 != 0) && (1 < iVar1 - 5U)) && ((*(char *)(param_1 + 0x88) == '\0' || (iVar1 != 0xf))))
  {
    return 1;
  }
  return 0;
}



