// ===================================================
// 18018FBC0  ->  FUN_18018fbc0  (entree 18018fbc0)
// ===================================================

void FUN_18018fbc0(longlong param_1)

{
  longlong lVar1;
  ulonglong uVar2;
  ulonglong uVar3;
  undefined1 local_38 [16];
  undefined4 uStack_28;
  uint uStack_24;
  uint uStack_20;
  undefined4 uStack_1c;
  uint local_18;
  uint uStack_14;
  undefined4 uStack_10;
  uint uStack_c;
  
  uVar2 = 0;
  uVar3 = uVar2;
  do {
    if (*(int *)(param_1 + 0x5c) == *(int *)((longlong)&DAT_1806495f8 + uVar2)) {
      lVar1 = uVar3 * 0xc;
      if (lVar1 != -0x1806495f8) {
        uStack_24 = *(uint *)(lVar1 + 0x1806495fc);
        local_38._4_4_ = *(undefined4 *)(lVar1 + 0x180649600);
        local_38._12_4_ = uStack_24 ^ DAT_180346d60;
        local_38._8_4_ = local_38._12_4_;
        local_38._0_4_ = local_38._12_4_;
        uStack_28 = local_38._4_4_;
        uStack_20 = uStack_24;
        uStack_1c = local_38._4_4_;
        uStack_14 = uStack_24;
        local_18 = uStack_24;
        uStack_10 = local_38._4_4_;
        uStack_c = local_38._12_4_;
        FUN_18024a6a0(2);
        FUN_180247600(3,0x161,0,local_38);
        FUN_180247100(300);
        FUN_18024e5a0(0,0,0,0);
        FUN_180175970(0xe);
        FUN_180252390();
        FUN_180247230(9,0,4);
        FUN_180252530();
        FUN_180176960();
        FUN_18024e5a0(1,1,1);
        FUN_18024a650();
      }
      return;
    }
    uVar3 = uVar3 + 1;
    uVar2 = uVar2 + 0xc;
  } while (uVar2 < 0x18);
  return;
}



