// ===================================================
// 1801B8A9D  ->  FUN_1801b8a80  (entree 1801b8a80)
// ===================================================

void FUN_1801b8a80(longlong param_1)

{
  undefined4 *puVar1;
  longlong lVar2;
  
  FUN_1801b9230();
  lVar2 = 2;
  *(undefined4 *)(param_1 + 0x4fd4) = 1;
  *(undefined4 *)(param_1 + 0x4fd0) = 2;
  puVar1 = (undefined4 *)(param_1 + 0x5024);
  *(undefined4 *)(param_1 + 0x4fe4) = 2;
  *(undefined4 *)(param_1 + 0x4ffc) = 2;
  *(undefined4 *)(param_1 + 0x4fd8) = 1;
  *(undefined4 *)(param_1 + 0x4fdc) = 1;
  *(undefined4 *)(param_1 + 0x4fe0) = 1;
  *(undefined4 *)(param_1 + 0x4fe8) = 1;
  *(undefined4 *)(param_1 + 0x4fec) = 1;
  *(undefined4 *)(param_1 + 0x4ff0) = 1;
  *(undefined8 *)(param_1 + 0x4ff4) = 1;
  *(undefined4 *)(param_1 + 0x5000) = 1;
  *(undefined4 *)(param_1 + 0x5004) = 1;
  *(undefined4 *)(param_1 + 0x5008) = 1;
  *(undefined8 *)(param_1 + 0x500c) = 1;
  *(undefined4 *)(param_1 + 0x5014) = 5;
  *(undefined8 *)(param_1 + 0x5018) = 5;
  *(undefined4 *)(param_1 + 0x5020) = 1;
  do {
    *puVar1 = 0;
    FUN_1801a3090(puVar1 + 1);
    FUN_1801a23a0((longlong)puVar1 + 6,*puVar1);
    puVar1 = puVar1 + 6;
    lVar2 = lVar2 + -1;
  } while (lVar2 != 0);
  FUN_1801b92d0(param_1 + 0x5058);
  return;
}



// ===================================================
// 1801B8CD3  ->  FUN_1801b8c40  (entree 1801b8c40)
// ===================================================

void FUN_1801b8c40(void)

{
  undefined8 *puVar1;
  longlong lVar2;
  undefined1 (*pauVar3) [16];
  longlong lVar4;
  longlong lVar5;
  undefined4 *puVar6;
  longlong lVar7;
  longlong lVar8;
  
  FUN_1801b8a80(DAT_180752148);
  lVar4 = DAT_180752148;
  *(undefined4 *)(DAT_180752148 + 0x6718) = 0xffffffff;
  *(undefined2 *)(lVar4 + 0x671c) = 1;
  lVar7 = 0;
  *(undefined4 *)(lVar4 + 0x6720) = 0;
  *(undefined1 *)(lVar4 + 0x6724) = 0;
  FUN_1801b8ff0();
  lVar4 = DAT_180752148;
  *(undefined4 *)(DAT_180752148 + 0x68c0) = 0x100;
  *(undefined1 *)(lVar4 + 0x68c4) = 0;
  *(undefined8 *)(lVar4 + 0x68c8) = 0;
  lVar2 = FUN_180218930(0x5058);
  lVar4 = lVar7;
  if (lVar2 != 0) {
    FUN_1801b9230(lVar2);
    lVar4 = 2;
    *(undefined4 *)(lVar2 + 0x4fd0) = 2;
    *(undefined4 *)(lVar2 + 0x4fd4) = 1;
    *(undefined4 *)(lVar2 + 0x4fd8) = 1;
    *(undefined4 *)(lVar2 + 0x4fdc) = 1;
    *(undefined4 *)(lVar2 + 0x4fe0) = 1;
    *(undefined4 *)(lVar2 + 0x4fe4) = 2;
    *(undefined4 *)(lVar2 + 0x4fe8) = 1;
    *(undefined4 *)(lVar2 + 0x4fec) = 1;
    *(undefined4 *)(lVar2 + 0x4ff0) = 1;
    *(undefined8 *)(lVar2 + 0x4ff4) = 1;
    *(undefined4 *)(lVar2 + 0x4ffc) = 2;
    *(undefined4 *)(lVar2 + 0x5000) = 1;
    *(undefined4 *)(lVar2 + 0x5004) = 1;
    *(undefined4 *)(lVar2 + 0x5008) = 1;
    *(undefined8 *)(lVar2 + 0x500c) = 1;
    *(undefined4 *)(lVar2 + 0x5014) = 5;
    *(undefined8 *)(lVar2 + 0x5018) = 5;
    *(undefined4 *)(lVar2 + 0x5020) = 1;
    puVar6 = (undefined4 *)(lVar2 + 0x5024);
    do {
      *puVar6 = 0;
      FUN_1801a3090(puVar6 + 1);
      FUN_1801a23a0((longlong)puVar6 + 6,*puVar6);
      puVar6 = puVar6 + 6;
      lVar4 = lVar4 + -1;
    } while (lVar4 != 0);
    *(undefined4 *)(lVar2 + 0x5054) = 0;
    lVar4 = lVar2;
  }
  lVar2 = DAT_180752148;
  *(longlong *)(DAT_180752148 + 0x68c8) = lVar4;
  if (lVar4 != 0) {
    FUN_1801b7c20();
  }
  *(undefined8 *)(lVar2 + 0x68d0) = 0;
  FUN_180087550(0x2e,FUN_1801ba100,0);
  FUN_180087550(0x2f,&LAB_1801b8fe0,0);
  FUN_180087550(0x3a,FUN_1801ba550,0);
  FUN_180087550(0x47,FUN_1801b9130,0);
  FUN_180087550(0x4f,FUN_1801b6a80,0);
  FUN_180215f70(DAT_180752148 + 0x67b8,&DAT_1804137f0);
  lVar4 = FUN_180218930(0x1a778);
  if (lVar4 != 0) {
    lVar7 = lVar4 + 0x10;
    lVar5 = 0x10;
    lVar8 = 0x10;
    lVar2 = lVar7;
    do {
      *(undefined8 *)(lVar2 + -0x10) = 0;
      *(undefined8 *)(lVar2 + -8) = 0;
      FUN_1801b92d0(lVar2);
      lVar2 = lVar2 + 0x16d0;
      lVar8 = lVar8 + -1;
    } while (lVar8 != 0);
    *(undefined1 *)(lVar4 + 0x183d0) = 0;
    *(undefined1 *)(lVar4 + 0x1a59e) = 0;
    *(undefined1 *)(lVar4 + 0x1a5c6) = 0;
    *(undefined1 *)(lVar4 + 0x1a5ee) = 0;
    *(undefined1 *)(lVar4 + 0x1a616) = 0;
    *(undefined1 *)(lVar4 + 0x1a63e) = 0;
    *(undefined1 *)(lVar4 + 0x1a666) = 0;
    *(undefined1 *)(lVar4 + 0x1a68e) = 0;
    *(undefined1 *)(lVar4 + 0x1a6b6) = 0;
    *(undefined1 *)(lVar4 + 0x1a6de) = 0;
    *(undefined1 *)(lVar4 + 0x1a706) = 0;
    puVar1 = (undefined8 *)(lVar4 + 0x1a718);
    *puVar1 = 0;
    *(undefined8 *)(lVar4 + 0x1a720) = 0;
    *(undefined8 *)(lVar4 + 0x1a728) = 0;
    *(undefined8 *)(lVar4 + 0x1a730) = 0;
    *(undefined8 *)(lVar4 + 0x1a738) = 0;
    pauVar3 = (undefined1 (*) [16])FUN_180218930(0x10);
    *puVar1 = pauVar3;
    *pauVar3 = (undefined1  [16])0x0;
    *(undefined8 **)*puVar1 = puVar1;
    *(undefined4 *)(lVar4 + 0x1a740) = 0;
    *(undefined4 *)(lVar4 + 0x1a74c) = 0;
    *(undefined8 *)(lVar4 + 0x1a750) = 0;
    do {
      *(undefined8 *)(lVar7 + -0x10) = 0;
      *(undefined8 *)(lVar7 + -8) = 0;
      FUN_1801b92d0(lVar7);
      lVar7 = lVar7 + 0x16d0;
      lVar5 = lVar5 + -1;
    } while (lVar5 != 0);
    FUN_1801b92d0(lVar4 + 0x16d00);
    FUN_1801b9790(lVar4 + 0x183c0);
    lVar7 = lVar4;
  }
  DAT_180752150 = lVar7;
  if (lVar7 != 0) {
    *(longlong *)(lVar7 + 0x1a758) = lVar7 + 0x183c0;
    *(undefined1 *)(lVar7 + 0x1a768) = 0;
    *(undefined4 *)(lVar7 + 0x1a74c) = 0;
    *(undefined1 *)(lVar7 + 0x1a748) = 1;
  }
  return;
}



