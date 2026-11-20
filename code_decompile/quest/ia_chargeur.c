// ===================================================
// 82250588  ->  FUN_82250588  (entree 82250588)
// ===================================================

void FUN_82250588(int param_1)

{
  undefined4 ****ppppuVar1;
  undefined1 auStack_d0 [4];
  undefined4 ***apppuStack_cc [5];
  uint uStack_b8;
  undefined1 auStack_b0 [4];
  uint uStack_ac;
  undefined4 uStack_9c;
  uint uStack_98;
  undefined1 auStack_90 [4];
  undefined1 auStack_8c [72];
  undefined **appuStack_44 [13];
  
  if (*(int *)(param_1 + 0x5c) != -1) {
    if (*(int *)(param_1 + 0x58) != -1) {
      FUN_821ce558(param_1,1);
      *(undefined4 *)(param_1 + 0x58) = 0xffffffff;
    }
    *(undefined4 *)(param_1 + 0x58) = *(undefined4 *)(param_1 + 0x5c);
    FUN_82141968(auStack_d0,0xffffffff82053ffc);
    FUN_8214c930(auStack_d0,0xffffffff82053ff0,8);
    FUN_821774a0(auStack_90,2,1);
    FUN_822486b8(auStack_90,*(undefined4 *)(param_1 + 0x58));
    FUN_8216e918(auStack_b0,auStack_8c);
    FUN_8214c598(auStack_d0,auStack_b0,0,0xffffffffffffffff);
    if (0xf < uStack_98) {
      thunk_FUN_82142f48(uStack_ac);
    }
    uStack_98 = 0xf;
    uStack_9c = 0;
    uStack_ac = uStack_ac & 0xffffff;
    FUN_8214c930(auStack_d0,0xffffffff82004330,4);
    ppppuVar1 = (undefined4 ****)apppuStack_cc[0];
    if (uStack_b8 < 0x10) {
      ppppuVar1 = apppuStack_cc;
    }
    FUN_821cf6e8(param_1,ppppuVar1,0xe);
    FUN_821ccb20(param_1,0,0xffffffff8224feb8,param_1);
    FUN_82169fb8(appuStack_44);
    appuStack_44[0] = &PTR_FUN_82001db4;
    FUN_8258d128(appuStack_44);
    if (0xf < uStack_b8) {
      thunk_FUN_82142f48(apppuStack_cc[0]);
    }
  }
  return;
}



