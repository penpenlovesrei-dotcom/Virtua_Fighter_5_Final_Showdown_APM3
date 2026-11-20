// ===================================================
// 1800B34D0  ->  FUN_1800b34d0  (entree 1800b34d0)
// ===================================================

void FUN_1800b34d0(longlong param_1,int *param_2)

{
  int iVar1;
  int iVar2;
  longlong lVar3;
  
  FUN_1800b56c0();
  *(undefined4 *)(param_1 + 0x10ac) = 2;
  *(undefined8 *)(param_1 + 0x10a0) = 0;
  *(undefined4 *)(param_1 + 0x10a8) = 0;
  *(undefined4 *)(param_1 + 0x10b0) = 0xffffffff;
  *(int *)(param_1 + 8) = *param_2;
  *(int *)(param_1 + 0xc) = param_2[1];
  *(int *)(param_1 + 0x10) = param_2[2];
  *(int *)(param_1 + 0x14) = param_2[3];
  *(int *)(param_1 + 0x1c) = param_2[5];
  *(int *)(param_1 + 0x24) = param_2[7];
  *(int *)(param_1 + 0x2c) = param_2[9];
  *(int *)(param_1 + 0x34) = param_2[0xb];
  *(int *)(param_1 + 0x18) = param_2[4];
  *(int *)(param_1 + 0x20) = param_2[6];
  *(int *)(param_1 + 0x28) = param_2[8];
  *(int *)(param_1 + 0x30) = param_2[10];
  *(int *)(param_1 + 0x38) = param_2[0xc];
  *(int *)(param_1 + 0x3c) = param_2[0xd];
  *(short *)(param_1 + 0x40) = (short)param_2[0xe];
  *(undefined2 *)(param_1 + 0x42) = *(undefined2 *)((longlong)param_2 + 0x3a);
  *(int *)(param_1 + 0x44) = param_2[0xf];
  *(int *)(param_1 + 0x48) = param_2[0x10];
  *(int *)(param_1 + 0x4c) = param_2[0x11];
  lVar3 = (longlong)param_2[0x10];
  iVar1 = *(int *)(&DAT_18034b208 + lVar3 * 4);
  *(int *)(param_1 + 0x50 + lVar3 * 4) = param_2[0x12];
  *(undefined4 *)(param_1 + 0x50 + (longlong)iVar1 * 4) = 0;
  *(undefined1 *)(lVar3 + 0x58 + param_1) = 0;
  iVar2 = *param_2;
  if (iVar2 == 0) {
    if ((char)param_2[0x13] == '\0') goto LAB_1800b35cc;
  }
  else if (iVar2 == 1) {
    if (param_2[0x12] != 0) goto LAB_1800b35cc;
  }
  else if ((iVar2 != 2) && (iVar2 != 3)) goto LAB_1800b35cc;
  *(undefined1 *)(lVar3 + 0x58 + param_1) = 1;
LAB_1800b35cc:
  *(undefined1 *)((longlong)iVar1 + 0x58 + param_1) = 1;
  *(undefined1 *)(param_1 + 0x5a) = 1;
  *(undefined1 *)(param_1 + 0x5b) = *(undefined1 *)((longlong)param_2 + 0x4d);
  *(undefined1 *)(param_1 + 0x5c) = *(undefined1 *)((longlong)param_2 + 0x4e);
  *(undefined1 *)(param_1 + 0x61) = *(undefined1 *)((longlong)param_2 + 0x4f);
  return;
}



