// ===================================================
// 180176829  ->  FUN_1801767d0  (entree 1801767d0)
// ===================================================

/* WARNING: Function: _alloca_probe replaced with injection: alloca_probe */

void FUN_1801767d0(undefined4 param_1,undefined8 param_2,int param_3,undefined1 param_4)

{
  ulonglong uVar1;
  undefined8 uVar2;
  undefined1 local_8098 [144];
  undefined1 local_8008 [32760];
  undefined8 uStack_10;
  
  uStack_10 = 0x1801767dc;
  uVar2 = 0xfffffffffffffffe;
  FUN_1802161d0(local_8098);
  FUN_180217c60(local_8098,"w64/shader_pxd_w64.farc",param_2,1,param_4,0,uVar2);
  FUN_180218210(local_8098);
  uVar1 = FUN_180217be0(local_8098);
  if (uVar1 + 1 < 0x8001) {
    uVar2 = FUN_180217940(local_8098);
    FUN_180300010(local_8008,uVar2,uVar1);
    local_8008[uVar1] = 0;
    if (param_3 == 0) {
      FUN_180252680(0x48b,param_1);
      uVar2 = 0x48b;
    }
    else {
      FUN_180252680(0x447,param_1);
      uVar2 = 0x447;
    }
    FUN_180252950(uVar2,uVar1 & 0xffffffff,local_8008);
  }
  else {
    FUN_1801d8720("\'%s\' too large shader code.\n",param_2);
  }
  FUN_180217900(local_8098,1);
  FUN_1802163b0(local_8098);
  return;
}



