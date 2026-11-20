// ===================================================
// 18019A8C0  ->  FUN_18019a8c0  (entree 18019a8c0)
// ===================================================

undefined8 * FUN_18019a8c0(undefined8 *param_1)

{
  *param_1 = app::PrintGC::vftable;
  *(undefined4 *)(param_1 + 1) = 0xffffffff;
  *(undefined4 *)((longlong)param_1 + 0xc) = 0xff808080;
  *(undefined1 *)(param_1 + 2) = 0;
  *(undefined8 *)((longlong)param_1 + 0x14) = 0;
  *(undefined8 *)((longlong)param_1 + 0x1c) = 0;
  *(undefined8 *)((longlong)param_1 + 0x24) = 7;
  *(undefined8 *)((longlong)param_1 + 0x2c) = 9;
  *(undefined8 *)((longlong)param_1 + 0x34) = 0;
  *(undefined8 *)((longlong)param_1 + 0x3c) = 0;
  param_1[9] = DAT_180751000;
  return param_1;
}



// ===================================================
// 18019A9D0  ->  FUN_18019a9d0  (entree 18019a9d0)
// ===================================================

undefined4 * FUN_18019a9d0(undefined4 *param_1)

{
  *param_1 = 0xffffffff;
  *(undefined8 *)(param_1 + 2) = 0;
  *(undefined8 *)(param_1 + 4) = 0;
  *(undefined8 *)(param_1 + 6) = 0;
  *(undefined8 *)(param_1 + 8) = 0;
  *(undefined8 *)(param_1 + 10) = 0;
  *(undefined8 *)(param_1 + 0xc) = 0;
  param_1[0xe] = 0;
  FUN_18019b6f0(param_1,0);
  return param_1;
}



// ===================================================
// 18019B6F0  ->  FUN_18019b6f0  (entree 18019b6f0)
// ===================================================

void FUN_18019b6f0(undefined4 *param_1,undefined4 param_2)

{
  byte bVar1;
  byte bVar2;
  short sVar3;
  longlong lVar4;
  longlong *plVar5;
  
  plVar5 = (longlong *)FUN_180199fb0(param_2);
  *param_1 = param_2;
  *(longlong *)(param_1 + 2) = *plVar5;
  bVar1 = *(byte *)(*plVar5 + 4);
  param_1[5] = (float)bVar1;
  bVar2 = *(byte *)(*plVar5 + 5);
  param_1[6] = (float)bVar2;
  param_1[7] = (float)*(byte *)(*plVar5 + 6);
  param_1[8] = (float)*(byte *)(*plVar5 + 7);
  sVar3 = *(short *)((longlong)plVar5 + 10);
  lVar4 = plVar5[1];
  param_1[10] = (float)(int)sVar3;
  param_1[9] = (float)(int)(short)lVar4;
  param_1[0xb] = (float)(int)(short)lVar4 / (float)bVar1;
  param_1[0xc] = (float)(int)sVar3 / (float)bVar2;
  param_1[0xd] = (float)(int)*(short *)((longlong)plVar5 + 0xc);
  sVar3 = *(short *)((longlong)plVar5 + 0xe);
  param_1[4] = 0;
  param_1[0xe] = (float)(int)sVar3;
  if (*(char *)(*plVar5 + 8) != *(char *)(*plVar5 + 9)) {
    param_1[4] = 1;
  }
  if (((char)plVar5[2] != '\0') && (*(char *)(*plVar5 + 0x38) != '\0')) {
    param_1[4] = 2;
  }
  return;
}



// ===================================================
// 18019B830  ->  FUN_18019b830  (entree 18019b830)
// ===================================================

void FUN_18019b830(longlong param_1,float param_2)

{
  *(float *)(param_1 + 0x24) = param_2;
  *(float *)(param_1 + 0x28) = param_2;
  *(float *)(param_1 + 0x30) = param_2 / *(float *)(param_1 + 0x18);
  *(float *)(param_1 + 0x2c) = param_2 / *(float *)(param_1 + 0x14);
  return;
}



