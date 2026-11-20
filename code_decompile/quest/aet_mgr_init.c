// ===================================================
// 180021D70  ->  FUN_180021d70  (entree 180021d70)
// ===================================================

void FUN_180021d70(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  undefined8 *puVar3;
  longlong lVar4;
  undefined8 *puVar5;
  
  lVar4 = 0x10;
  puVar1 = (undefined8 *)FUN_18027ca60(0x818,0x10,param_3,param_4,0xfffffffffffffffe);
  if (puVar1 == (undefined8 *)0x0) {
    DAT_18066b750 = (undefined8 *)0x0;
    puVar1 = DAT_18066b750;
  }
  else {
    FUN_180244c80(puVar1);
    *puVar1 = AetMgr::vftable;
    puVar3 = puVar1 + 0xb;
    *puVar3 = 0;
    puVar1[0xc] = 0;
    uVar2 = FUN_180022100(puVar3);
    *puVar3 = uVar2;
    puVar3 = puVar1 + 0xd;
    *puVar3 = 0;
    puVar1[0xe] = 0;
    uVar2 = FUN_180022140(puVar3);
    *puVar3 = uVar2;
    puVar3 = puVar1 + 0xf;
    *puVar3 = 0;
    puVar1[0x10] = 0;
    uVar2 = FUN_180022180(puVar3,0,0);
    *puVar3 = uVar2;
    puVar5 = puVar1 + 0x12;
    puVar3 = puVar1 + 0x1b;
    do {
      FUN_180211a00(puVar5);
      puVar3[-1] = 0;
      *puVar3 = 0;
      puVar3[1] = 0;
      puVar3[2] = 0;
      *(undefined2 *)(puVar3 + 3) = 0;
      *(undefined1 *)((longlong)puVar3 + 0x1a) = 0;
      FUN_180213910(puVar5);
      puVar3[-1] = 0;
      *puVar3 = 0;
      puVar3[1] = 0;
      puVar3[2] = 0;
      *(undefined2 *)(puVar3 + 3) = 0xffff;
      *(undefined1 *)((longlong)puVar3 + 0x1a) = 0xff;
      *(undefined4 *)((longlong)puVar3 + 0x1c) = 0x3f800000;
      *(undefined4 *)(puVar3 + 4) = 9;
      puVar5 = puVar5 + 0xf;
      puVar3 = puVar3 + 0xf;
      lVar4 = lVar4 + -1;
    } while (lVar4 != 0);
  }
  DAT_18066b750 = puVar1;
  return;
}



