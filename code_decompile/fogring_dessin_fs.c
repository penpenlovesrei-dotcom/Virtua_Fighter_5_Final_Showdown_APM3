// ===================================================
// 180072BA0  ->  FUN_180072ba0  (entree 180072ba0)
// ===================================================

void FUN_180072ba0(longlong param_1)

{
  longlong lVar1;
  
  if (*(int *)(param_1 + 0x58) != 0) {
    FUN_180248bc0(0xffffffff);
    FUN_18024a6a0(2);
    FUN_180247100(300);
    FUN_1802473b0(0x12d);
    FUN_180175970(0x2a);
    FUN_180252390();
    FUN_18024e900(0xac);
    FUN_18024f2d0(*(undefined4 *)(param_1 + 0x30));
    FUN_18024f2a0(0x311);
    FUN_18024e900(0x318);
    FUN_1802573a0(0x318,0x319,1);
    FUN_18024e900(0x2cd);
    lVar1 = FUN_1801957a0(*(undefined4 *)(param_1 + 0x1c));
    if (lVar1 != 0) {
      FUN_180256d50(0x21d);
      FUN_180256da0(*(undefined4 *)(lVar1 + 0x14),*(undefined4 *)(lVar1 + 0x10));
    }
    FUN_180247600(3,0x161,0x20,*(undefined8 *)(param_1 + 0x50));
    FUN_1802470a0(4,0x161,0x20,*(longlong *)(param_1 + 0x50) + 0xc);
    FUN_180247430(0xe);
    FUN_1802475b0(0xe,1,0x161,0,0x20,*(longlong *)(param_1 + 0x50) + 0x1c);
    FUN_180247230(2,0,*(undefined4 *)(param_1 + 0x58));
    FUN_180252530();
    FUN_180176960();
    FUN_18024a650();
    FUN_180248ba0();
  }
  return;
}



// ===================================================
// 1800729C0  ->  FUN_1800729c0  (entree 1800729c0)
// ===================================================

void FUN_1800729c0(char *param_1)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar3;
  longlong lVar4;
  undefined8 uVar5;
  undefined1 auVar6 [64];
  undefined4 local_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  
  FUN_1800f0ba0(0);
  if (*param_1 != '\0') {
    FUN_1800f0ba0(1);
    lVar4 = FUN_18010bef0(5);
    FUN_18010cca0(lVar4,0);
    FUN_180248bc0(0x800);
    uVar5 = *(undefined8 *)(lVar4 + 8);
    uVar1 = FUN_180195590(uVar5,0);
    uVar2 = FUN_180195840(uVar5,0);
    FUN_18024f500(0,0,uVar2,uVar1);
    uVar1 = *(undefined4 *)(param_1 + 0x40);
    auVar6 = ZEXT464(DAT_180346d3c);
    FUN_18024e3c0(uVar1,uVar1,uVar1,DAT_180346d3c);
    FUN_1802541d0(0x4100);
    iVar3 = FUN_1800ec090(0x16);
    if (iVar3 != 0) {
      FUN_1800ea4c0(0x16,0,0);
    }
    FUN_180248ba0();
    FUN_18010d190(lVar4);
    local_20 = DAT_18034b3ec;
    local_24 = DAT_18034b3ec;
    local_28 = DAT_18034b3ec;
    local_1c = auVar6._0_4_;
    FUN_180254610(*(undefined4 *)(*(longlong *)(lVar4 + 8) + 0x10),0,1);
    if (*(longlong *)(lVar4 + 0x10) != 0) {
      FUN_180254610(*(undefined4 *)(*(longlong *)(lVar4 + 0x10) + 0x10),0,1);
    }
    uVar5 = FUN_18010bef0(2);
    FUN_1800d1f30(uVar5,0,lVar4,0,&local_28);
    FUN_180254610(*(undefined4 *)(*(longlong *)(lVar4 + 8) + 0x10),0,0);
    if (*(longlong *)(lVar4 + 0x10) != 0) {
      FUN_180254610(*(undefined4 *)(*(longlong *)(lVar4 + 0x10) + 0x10),0,0);
    }
    lVar4 = FUN_18010bef0(2);
    FUN_18010ca10(*(undefined8 *)(lVar4 + 8));
    FUN_180007440();
  }
  return;
}



