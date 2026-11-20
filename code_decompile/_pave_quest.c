// ===================================================
// 8230A384  ->  FUN_8230a338  (entree 8230a338)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_8230a338(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                 undefined4 param_5)

{
  undefined4 uVar1;
  char *pcStack_130;
  undefined4 uStack_12c;
  undefined1 auStack_120 [4];
  uint uStack_11c;
  undefined4 uStack_10c;
  uint uStack_108;
  undefined1 auStack_100 [4];
  uint uStack_fc;
  undefined4 uStack_ec;
  uint uStack_e8;
  undefined4 uStack_e0;
  char *pcStack_dc;
  undefined4 uStack_d8;
  undefined4 uStack_d4;
  undefined4 uStack_c8;
  undefined4 uStack_c4;
  undefined4 uStack_bc;
  undefined4 uStack_b4;
  undefined1 auStack_68 [104];
  
  if (*(int *)(param_1 + 0xf4) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0xf4) = 0;
  }
  FUN_82158008(&uStack_e0);
  pcStack_dc = s_col_iconmove_82084ca0;
  pcStack_130 = s_p_col_txt_main_c_82084c8c;
  uStack_e0 = 0x423;
  uStack_c8 = 0x20000;
  uStack_bc = 6;
  uStack_c4 = 2;
  uStack_b4 = 9;
  uStack_12c = param_4;
  uStack_d8 = param_2;
  uStack_d4 = param_3;
  FUN_8214d890(auStack_120,&pcStack_130);
  FUN_82330798(&pcStack_130,auStack_68,auStack_120);
  if (0xf < uStack_108) {
    thunk_FUN_82142f48(uStack_11c);
  }
  uStack_10c = 0;
  uStack_11c = uStack_11c & 0xffffff;
  uStack_108 = 0xf;
  pcStack_130 = s_p_col_txt_sub_c_82084c7c;
  uStack_12c = param_5;
  FUN_8214d890(auStack_100,&pcStack_130);
  FUN_82330798(&pcStack_130,auStack_68,auStack_100);
  if (0xf < uStack_e8) {
    thunk_FUN_82142f48(uStack_fc);
  }
  uStack_e8 = 0xf;
  uStack_ec = 0;
  uStack_fc = uStack_fc & 0xffffff;
  uVar1 = FUN_82166cc0(&uStack_e0);
  *(undefined4 *)(param_1 + 0xf4) = uVar1;
  FUN_82157f80(&uStack_e0);
  return;
}



