// ===================================================
// 82239148  ->  FUN_82239148  (entree 82239148)
// ===================================================

void FUN_82239148(int param_1)

{
  undefined4 uVar1;
  undefined4 local_f0;
  char *local_ec;
  undefined4 local_e8;
  undefined4 local_e4;
  undefined4 local_d8;
  undefined4 local_d4;
  undefined4 local_cc;
  undefined4 local_90;
  
  if (*(int *)(param_1 + 0x204) == 0) {
    FUN_821c6270(&local_f0);
    local_e8 = 0;
    local_90 = DAT_82000830;
    local_f0 = 0x2a0;
    local_ec = s_cursor_tri_46_8200e1c0;
    local_cc = 0x10;
    local_d8 = 0x10000;
    local_e4 = 0;
    local_d4 = 2;
    uVar1 = FUN_821c6940(&local_f0);
    *(undefined4 *)(param_1 + 0x204) = uVar1;
    FUN_821c61a8(&local_f0);
  }
  return;
}



