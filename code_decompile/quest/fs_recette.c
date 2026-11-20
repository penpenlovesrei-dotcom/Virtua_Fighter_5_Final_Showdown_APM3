// ===================================================
// 180187AA0  ->  FUN_180187aa0  (entree 180187aa0)
// ===================================================

void FUN_180187aa0(void)

{
  FUN_18018c6a0(DAT_180719900);
  return;
}



// ===================================================
// 180187CB0  ->  FUN_180187cb0  (entree 180187cb0)
// ===================================================

void FUN_180187cb0(undefined4 param_1)

{
  FUN_18018e810(DAT_180719900,param_1);
  return;
}



// ===================================================
// 18019B800  ->  FUN_18019b800  (entree 18019b800)
// ===================================================

void FUN_18019b800(longlong param_1,undefined8 *param_2,undefined4 param_3)

{
  uint uVar1;
  undefined8 uVar2;
  undefined1 auVar3 [16];
  
  uVar1 = *(uint *)((longlong)param_2 + 4);
  *(undefined4 *)(param_1 + 0x3c) = *(undefined4 *)param_2;
  auVar3._8_8_ = 0;
  auVar3._0_8_ = *(ulonglong *)(param_1 + 0x3c);
  auVar3 = vinsertps_avx(auVar3,ZEXT416(uVar1),0x10);
  *(longlong *)(param_1 + 0x34) = auVar3._0_8_;
  *(longlong *)(param_1 + 0x3c) = auVar3._0_8_;
  *(undefined4 *)(param_1 + 0x2c) = param_3;
  *(undefined1 *)(param_1 + 0x10) = 1;
  uVar2 = param_2[1];
  *(undefined8 *)(param_1 + 0x14) = *param_2;
  *(undefined8 *)(param_1 + 0x1c) = uVar2;
  return;
}



// ===================================================
// 18019B870  ->  FUN_18019b870  (entree 18019b870)
// ===================================================

void FUN_18019b870(longlong param_1,int param_2)

{
  longlong lVar1;
  
  lVar1 = *(longlong *)(param_1 + 8);
  if (lVar1 != 0) {
    if (param_2 != 1) {
      if (param_2 != 2) goto LAB_18019b8a5;
      if (*(char *)(lVar1 + 0x38) != '\0') {
        *(undefined4 *)(param_1 + 0x10) = 2;
        return;
      }
    }
    if (*(char *)(lVar1 + 8) != *(char *)(lVar1 + 9)) {
      *(undefined4 *)(param_1 + 0x10) = 1;
      return;
    }
  }
LAB_18019b8a5:
  *(undefined4 *)(param_1 + 0x10) = 0;
  return;
}



// ===================================================
// 18019B300  ->  FUN_18019b300  (entree 18019b300)
// ===================================================

void FUN_18019b300(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined8 local_res18;
  undefined8 local_res20;
  
  local_res18 = param_3;
  local_res20 = param_4;
  FUN_18019b330(param_1,1,param_2,&local_res18);
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



