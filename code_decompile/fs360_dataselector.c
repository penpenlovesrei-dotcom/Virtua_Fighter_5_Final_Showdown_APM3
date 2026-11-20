// ===================================================
// 82239288  ->  FUN_82239288  (entree 82239288)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

undefined8 FUN_82239288(int param_1)

{
  byte bVar1;
  ulonglong uVar2;
  int iVar3;
  
  FUN_82217e18(param_1,0);
  FUN_82217f40(param_1);
  FUN_82238e78(param_1);
  FUN_823ad3a8(param_1 + 0x1fc,param_1,0xffffffff82011688);
  bVar1 = *(byte *)(param_1 + 0x5398) >> 6 & 1;
  *(byte *)(param_1 + 0x3c0) = bVar1;
  if (bVar1 == 0) {
    FUN_82217990(param_1 + 0x3e4);
  }
  iVar3 = param_1 + 0x428;
  FUN_823ad3a8(iVar3,param_1,0xffffffff8201167c);
  uVar2 = (~(ulonglong)*(byte *)(param_1 + 0x5398) & 0xffffffff) >> 6 & 1;
  *(char *)(param_1 + 0x5ec) = (char)uVar2;
  if (uVar2 == 0) {
    FUN_821c5dd8(*(undefined4 *)(param_1 + 0x62c));
    *(undefined4 *)(param_1 + 0x62c) = 0;
    FUN_82217990(param_1 + 0x600);
  }
  else {
    FUN_82239148(iVar3);
  }
  if ((*(byte *)(param_1 + 0x5398) & 0x40) == 0) {
    *(int *)(param_1 + 0x53a0) = iVar3;
  }
  else {
    *(int *)(param_1 + 0x53a0) = param_1 + 0x1fc;
  }
  *(undefined1 *)(param_1 + 0x53a4) = 0;
  *(undefined1 *)(param_1 + 0x53b4) = 0;
  *(undefined4 *)(param_1 + 0x53ac) = 0xffffffff;
  *(undefined4 *)(param_1 + 0x53a8) = 0x15;
  *(undefined4 *)(param_1 + 0x53b0) = 0xffffffff;
  *(undefined4 *)(param_1 + 0x1bc) = 0x12;
  *(undefined1 *)(param_1 + 0x1c0) = 1;
  return 1;
}



// ===================================================
// 822391E0  ->  FUN_822391e0  (entree 822391e0)
// ===================================================

undefined8 FUN_822391e0(int param_1)

{
  FUN_82239148();
  *(undefined4 *)(param_1 + 0x1bc) = 1;
  *(undefined1 *)(param_1 + 0x1c0) = 1;
  return 1;
}



