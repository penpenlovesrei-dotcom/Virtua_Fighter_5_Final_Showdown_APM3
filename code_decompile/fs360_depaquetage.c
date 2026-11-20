// ===================================================
// 82215228  ->  FUN_82215228  (entree 82215228)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_82215228(char param_1,char param_2)

{
  ulonglong uVar1;
  ulonglong uVar2;
  ulonglong uVar3;
  
  FUN_821fe8e0(0,DAT_829afa4c,0xffffffff829afa52,0xffffffff829afa50);
  FUN_822146f0();
  if (param_1 == '\0') {
    DAT_829afa48 = 0;
  }
  else {
    DAT_829b4a68 = param_2;
    if (param_2 != '\0') {
      uVar3 = 0;
      uVar2 = 1;
      uVar1 = 0;
      do {
        if ((*(uint *)((int)&DAT_829aaa68 + ((uint)uVar1 & 0x1ffffffc)) & uVar2) != 0) {
          FUN_823a65d8(DAT_829b4a60,uVar3);
        }
        uVar3 = uVar3 + 1;
        uVar2 = (uVar2 & 0x7fffffff) << 1 | uVar2 >> 0x1f;
        uVar1 = (uVar3 & 0xffffffff) >> 3;
      } while ((uVar3 & 0xffffffff) < 0xc);
      return;
    }
  }
  return;
}



// ===================================================
// 822152E0  ->  FUN_822152e0  (entree 822152e0)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_822152e0(char param_1,char param_2)

{
  ulonglong uVar1;
  ulonglong uVar2;
  ulonglong uVar3;
  
  if (param_1 == '\0') {
    DAT_829b4a44 = 0;
  }
  else {
    FUN_821fe8e0(1,DAT_829b4a48,0xffffffff829b4a4e,0xffffffff829b4a4c);
    DAT_829b4a69 = param_2;
    if (param_2 != '\0') {
      uVar3 = 0;
      uVar2 = 1;
      uVar1 = 0;
      do {
        if ((*(uint *)((int)&DAT_829afa64 + ((uint)uVar1 & 0x1ffffffc)) & uVar2) != 0) {
          FUN_823a65d8(DAT_829b4a64,uVar3);
        }
        uVar3 = uVar3 + 1;
        uVar2 = (uVar2 & 0x7fffffff) << 1 | uVar2 >> 0x1f;
        uVar1 = (uVar3 & 0xffffffff) >> 3;
      } while ((uVar3 & 0xffffffff) < 0xc);
      return;
    }
  }
  return;
}



// ===================================================
// 82214400  ->  FUN_82214400  (entree 82214400)
// ===================================================

void FUN_82214400(int param_1)

{
  FUN_82214380();
  *(undefined4 *)(param_1 + 0x4f98) = 1;
  *(undefined4 *)(param_1 + 0x4f9c) = 1;
  *(undefined4 *)(param_1 + 0x4f94) = 2;
  *(undefined4 *)(param_1 + 0x4fa0) = 1;
  *(undefined4 *)(param_1 + 0x4fa4) = 1;
  *(undefined4 *)(param_1 + 0x4fa8) = 2;
  *(undefined4 *)(param_1 + 0x4fac) = 1;
  *(undefined4 *)(param_1 + 0x4fb0) = 1;
  *(undefined4 *)(param_1 + 0x4fb4) = 1;
  *(undefined4 *)(param_1 + 0x4fb8) = 0;
  *(undefined4 *)(param_1 + 0x4fbc) = 0;
  *(undefined4 *)(param_1 + 0x4fc0) = 2;
  *(undefined4 *)(param_1 + 0x4fc4) = 1;
  *(undefined4 *)(param_1 + 0x4fc8) = 1;
  *(undefined4 *)(param_1 + 0x4fcc) = 1;
  *(undefined4 *)(param_1 + 0x4fd0) = 1;
  *(undefined4 *)(param_1 + 0x4fd4) = 5;
  *(undefined4 *)(param_1 + 0x4fd8) = 5;
  *(undefined4 *)(param_1 + 0x4fdc) = 0;
  *(undefined4 *)(param_1 + 0x4fe0) = 1;
  *(undefined4 *)(param_1 + 0x4fe4) = 0;
  FUN_821fd9b0(param_1 + 0x4fe8);
  FUN_821fea08(param_1 + 0x4fea,*(undefined4 *)(param_1 + 0x4fe4));
  return;
}



