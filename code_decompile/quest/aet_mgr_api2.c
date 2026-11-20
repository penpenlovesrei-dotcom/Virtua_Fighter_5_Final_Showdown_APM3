// ===================================================
// 180029790  ->  FUN_180029790  (entree 180029790)
// ===================================================

void FUN_180029790(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  longlong lVar1;
  undefined8 uVar2;
  undefined4 local_128 [72];
  
  uVar2 = 0xfffffffffffffffe;
  FUN_180028e90(local_128);
  lVar1 = FUN_180024250(DAT_18066b738,local_128[0]);
  local_128[0] = *(undefined4 *)(lVar1 + 0x28);
  FUN_180024970(DAT_18066b750,param_1,local_128,param_4,uVar2);
  FUN_180029140(local_128);
  return;
}



// ===================================================
// 1800297F0  ->  FUN_1800297f0  (entree 1800297f0)
// ===================================================

void FUN_1800297f0(undefined8 param_1,undefined4 param_2,undefined8 param_3,undefined4 param_4,
                  undefined4 param_5,undefined8 param_6,undefined4 param_7)

{
  longlong lVar1;
  undefined4 local_128 [2];
  undefined8 local_120;
  undefined8 local_118;
  undefined4 local_108;
  undefined4 local_100;
  undefined4 local_f0;
  
  FUN_180029000(local_128);
  lVar1 = FUN_180024250(DAT_18066b738,param_2);
  local_128[0] = *(undefined4 *)(lVar1 + 0x28);
  local_f0 = param_5;
  local_118 = param_6;
  local_108 = param_7;
  local_120 = param_3;
  local_100 = param_4;
  FUN_180024970(DAT_18066b750,param_1,local_128);
  FUN_180029140(local_128);
  return;
}



// ===================================================
// 1800298B0  ->  FUN_1800298b0  (entree 1800298b0)
// ===================================================

undefined4 * FUN_1800298b0(undefined8 *param_1,longlong param_2)

{
  char cVar1;
  char cVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  char *pcVar5;
  longlong lVar6;
  
  puVar4 = (undefined4 *)*param_1;
  do {
    if (puVar4 == (undefined4 *)param_1[1]) {
      return (undefined4 *)0x0;
    }
    pcVar5 = *(char **)(puVar4 + 0x1c);
    lVar6 = param_2 - (longlong)pcVar5;
    do {
      cVar1 = *pcVar5;
      cVar2 = pcVar5[lVar6];
      if (cVar1 != cVar2) break;
      pcVar5 = pcVar5 + 1;
    } while (cVar2 != '\0');
    if (cVar1 == cVar2) {
      puVar3 = (undefined4 *)FUN_180024600(DAT_18066b750);
      *puVar3 = *puVar4;
      puVar3[1] = puVar4[1];
      puVar3[2] = puVar4[2];
      puVar3[3] = puVar4[3];
      puVar3[4] = puVar4[4];
      puVar3[5] = puVar4[5];
      puVar3[6] = puVar4[6];
      puVar3[7] = puVar4[7];
      puVar3[8] = puVar4[8];
      puVar3[9] = puVar4[9];
      puVar3[10] = puVar4[10];
      puVar3[0xb] = puVar4[0xb];
      puVar3[0xc] = puVar4[0xc];
      puVar3[0xd] = puVar4[0xd];
      puVar3[0xe] = puVar4[0xe];
      puVar3[0xf] = puVar4[0xf];
      *(undefined8 *)(puVar3 + 0x10) = *(undefined8 *)(puVar4 + 0x10);
      puVar3[0x12] = puVar4[0x12];
      *(undefined8 *)(puVar3 + 0x13) = *(undefined8 *)(puVar4 + 0x13);
      puVar3[0x15] = puVar4[0x15];
      *(undefined8 *)(puVar3 + 0x16) = *(undefined8 *)(puVar4 + 0x16);
      *(undefined2 *)(puVar3 + 0x18) = *(undefined2 *)(puVar4 + 0x18);
      *(undefined1 *)((longlong)puVar3 + 0x62) = *(undefined1 *)((longlong)puVar4 + 0x62);
      puVar3[0x19] = puVar4[0x19];
      puVar3[0x1a] = puVar4[0x1a];
      *(undefined8 *)(puVar3 + 0x1c) = *(undefined8 *)(puVar4 + 0x1c);
      return puVar3;
    }
    puVar4 = puVar4 + 0x1e;
  } while( true );
}



// ===================================================
// 180029730  ->  FUN_180029730  (entree 180029730)
// ===================================================

void FUN_180029730(undefined4 param_1)

{
  longlong lVar1;
  
  lVar1 = FUN_1800248d0(DAT_18066b738,param_1);
  FUN_1800240c0(DAT_18066b750,*(undefined4 *)(lVar1 + 0x48));
  return;
}



