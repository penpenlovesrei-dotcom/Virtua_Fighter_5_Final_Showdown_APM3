// ===================================================
// 82214C08  ->  FUN_82214b48  (entree 82214b48)
// ===================================================

void FUN_82214b48(ulonglong param_1,undefined8 param_2)

{
  char cVar1;
  undefined8 uVar2;
  
  if ((int)param_2 < 0) {
    param_2 = FUN_8239fde0();
  }
  cVar1 = FUN_823a4988(param_2);
  if (cVar1 != '\0') {
    uVar2 = 0xffffffff829aaa68;
    if ((int)param_2 == DAT_829b4a60) {
      if (((param_1 & 0xff) != 0) && (DAT_829afa48 == 0)) {
        return;
      }
    }
    else {
      if ((int)param_2 != DAT_829b4a64) {
        return;
      }
      if (((param_1 & 0xff) != 0) && (DAT_829b4a44 == 0)) {
        return;
      }
      uVar2 = 0xffffffff829afa64;
    }
    FUN_823a35c8(param_2,uVar2,0x4ffc,param_1,0);
  }
  return;
}



// ===================================================
// 8221545C  ->  FUN_822153a8  (entree 822153a8)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_822153a8(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  char cVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  
  if ((int)param_3 < 0) {
    param_3 = FUN_8239fde0();
  }
  cVar1 = FUN_823a4988(param_3);
  if (cVar1 != '\0') {
    uVar3 = 0xffffffff829aaa68;
    if ((int)param_3 == DAT_829b4a60) {
      uVar2 = 0xffffffff82215228;
    }
    else {
      if ((int)param_3 != DAT_829b4a64) {
        return;
      }
      FUN_82214400(0xffffffff829afa64);
      param_1 = 0;
      uVar2 = 0xffffffff822152e0;
      uVar3 = 0xffffffff829afa64;
      DAT_829b4a70 = 0;
    }
    FUN_823a5d58(param_3,uVar3,0x4ffc,param_1,param_2,uVar2);
  }
  return;
}



