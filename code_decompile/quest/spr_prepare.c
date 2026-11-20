// ===================================================
// 180187AB0  ->  FUN_180187ab0  (entree 180187ab0)
// ===================================================

void FUN_180187ab0(void)

{
  FUN_18018c7d0(DAT_180719900,
                (*(longlong *)(DAT_180719908 + 0x98) - *(longlong *)(DAT_180719908 + 0x90)) / 0x58);
  return;
}



// ===================================================
// 18018E5A0  ->  FUN_18018e5a0  (entree 18018e5a0)
// ===================================================

void FUN_18018e5a0(longlong *param_1,uint param_2,undefined8 param_3)

{
  undefined8 *puVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  undefined8 *puVar4;
  
  puVar1 = (undefined8 *)*param_1;
  puVar2 = (undefined8 *)puVar1[1];
  puVar4 = puVar1;
  if (*(char *)((longlong)puVar1[1] + 0x19) == '\0') {
    do {
      if (*(uint *)(puVar2 + 4) < param_2) {
        puVar3 = (undefined8 *)puVar2[2];
      }
      else {
        puVar3 = (undefined8 *)*puVar2;
        puVar4 = puVar2;
      }
      puVar2 = puVar3;
    } while (*(char *)((longlong)puVar3 + 0x19) == '\0');
    if ((puVar4 != puVar1) && (*(uint *)(puVar4 + 4) <= param_2)) goto LAB_18018e5d5;
  }
  puVar4 = puVar1;
LAB_18018e5d5:
  puVar2 = puVar4 + 5;
  if (puVar4 == puVar1) {
    puVar2 = (undefined8 *)0x0;
  }
  FUN_18018dfb0(puVar2,param_3);
  return;
}



