// ===================================================
// 821DF7C0  ->  FUN_821df780  (entree 821df780)
// ===================================================

undefined4 * FUN_821df780(undefined4 *param_1,undefined1 param_2)

{
  *param_1 = &PTR_FUN_8200f6e8;
  param_1[0xc] = &PTR_FUN_8200f6d8;
  FUN_821dc8b8();
  FUN_821df6e0(param_1 + 0x2a);
  FUN_821dd458(param_1);
  *(undefined1 *)(param_1 + 0x2f9) = param_2;
  return param_1;
}



