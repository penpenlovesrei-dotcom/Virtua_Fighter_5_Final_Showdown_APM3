// ===================================================
// 180019AB0  ->  FUN_180019ab0  (entree 180019ab0)
// ===================================================

undefined8 FUN_180019ab0(ushort param_1)

{
  undefined8 uVar1;
  
  uVar1 = 0;
  if ((0x1f < param_1) && (param_1 != 0x7f)) {
    uVar1 = 1;
  }
  return uVar1;
}



// ===================================================
// 18019B3C0  ->  FUN_18019b3c0  (entree 18019b3c0)
// ===================================================

float * FUN_18019b3c0(longlong param_1,float *param_2,undefined2 param_3)

{
  float fVar1;
  byte bVar2;
  longlong lVar3;
  
  lVar3 = FUN_180199fd0(*(undefined8 *)(param_1 + 8),param_3);
  param_2[0] = 0.0;
  param_2[1] = 0.0;
  param_2[2] = 0.0;
  param_2[3] = 0.0;
  bVar2 = *(byte *)(lVar3 + 3);
  fVar1 = *(float *)(param_1 + 0x20);
  *param_2 = (float)*(byte *)(lVar3 + 2) * *(float *)(param_1 + 0x1c);
  param_2[1] = (float)bVar2 * fVar1;
  *(undefined8 *)(param_2 + 2) = *(undefined8 *)(param_1 + 0x14);
  if (*(char *)(lVar3 + 1) != '\0') {
    param_2[2] = param_2[2] * DAT_180346d38;
  }
  param_2[4] = 0.0;
  param_2[5] = param_2[2];
  if (*(int *)(param_1 + 0x10) == 2) {
    param_2[4] = (float)*(byte *)(lVar3 + 4);
    param_2[5] = (float)*(byte *)(lVar3 + 5);
  }
  return param_2;
}



// ===================================================
// 18019B4A0  ->  FUN_18019b4a0  (entree 18019b4a0)
// ===================================================

void FUN_18019b4a0(longlong param_1,uint param_2,float *param_3,float *param_4,undefined4 param_5)

{
  undefined8 *puVar1;
  float fVar2;
  float fVar3;
  undefined4 uVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float local_c8;
  float fStack_c4;
  undefined4 uStack_c0;
  float fStack_bc;
  float local_b8;
  undefined1 uStack_b4;
  undefined1 uStack_b3;
  undefined1 uStack_b2;
  undefined1 uStack_b1;
  
  fVar2 = *param_4;
  fVar3 = param_4[1];
  fVar7 = *param_3 - param_4[4];
  fVar8 = param_3[1];
  fVar9 = param_4[2];
  uStack_b3 = (undefined1)((uint)param_5 >> 8);
  uStack_b4 = (undefined1)param_5;
  uStack_b2 = (undefined1)((uint)param_5 >> 0x10);
  uStack_b1 = (undefined1)((uint)param_5 >> 0x18);
  fVar10 = param_4[3];
  fVar5 = fVar9;
  fVar6 = fVar10;
  if ((param_2 >> 10 & 1) != 0) {
    fVar2 = fVar2 + DAT_180346d38;
    fVar3 = fVar3 + DAT_180346d38;
    fVar5 = fVar9 + DAT_180347cd8;
    fVar6 = fVar10 + DAT_180347cd8;
  }
  puVar1 = *(undefined8 **)(param_1 + 8);
  uVar4 = 0;
  uStack_c0 = 0;
  if (*(undefined8 **)(param_1 + 0x10) == puVar1) {
    local_c8 = fVar7;
    fStack_c4 = fVar8;
    fStack_bc = fVar2;
    local_b8 = fVar3;
    FUN_1801067c0(*param_3,puVar1,&local_c8);
    puVar1 = *(undefined8 **)(param_1 + 8);
  }
  else {
    *puVar1 = CONCAT44(fVar8,fVar7);
    puVar1[1] = (ulonglong)(uint)fVar2 << 0x20;
    puVar1[2] = CONCAT17(uStack_b1,CONCAT16(uStack_b2,CONCAT15(uStack_b3,CONCAT14(uStack_b4,fVar3)))
                        );
    *(longlong *)(param_1 + 8) = *(longlong *)(param_1 + 8) + 0x18;
    puVar1 = *(undefined8 **)(param_1 + 8);
  }
  fVar9 = fVar9 + fVar7;
  fVar5 = fVar5 + fVar2;
  if (*(undefined8 **)(param_1 + 0x10) == puVar1) {
    local_c8 = fVar9;
    fStack_c4 = fVar8;
    uStack_c0 = uVar4;
    fStack_bc = fVar5;
    local_b8 = fVar3;
    FUN_1801067c0(param_1,puVar1,&local_c8);
  }
  else {
    *puVar1 = CONCAT44(fVar8,fVar9);
    puVar1[1] = CONCAT44(fVar5,uVar4);
    puVar1[2] = CONCAT17(uStack_b1,CONCAT16(uStack_b2,CONCAT15(uStack_b3,CONCAT14(uStack_b4,fVar3)))
                        );
    *(longlong *)(param_1 + 8) = *(longlong *)(param_1 + 8) + 0x18;
  }
  puVar1 = *(undefined8 **)(param_1 + 8);
  fVar10 = fVar10 + fVar8;
  fVar6 = fVar6 + fVar3;
  if (*(undefined8 **)(param_1 + 0x10) == puVar1) {
    local_c8 = fVar9;
    fStack_c4 = fVar10;
    uStack_c0 = uVar4;
    fStack_bc = fVar5;
    local_b8 = fVar6;
    FUN_1801067c0(param_1,puVar1,&local_c8);
  }
  else {
    *puVar1 = CONCAT44(fVar10,fVar9);
    puVar1[1] = CONCAT44(fVar5,uVar4);
    puVar1[2] = CONCAT17(uStack_b1,CONCAT16(uStack_b2,CONCAT15(uStack_b3,CONCAT14(uStack_b4,fVar6)))
                        );
    *(longlong *)(param_1 + 8) = *(longlong *)(param_1 + 8) + 0x18;
  }
  puVar1 = *(undefined8 **)(param_1 + 8);
  if (*(undefined8 **)(param_1 + 0x10) == puVar1) {
    local_c8 = fVar7;
    fStack_c4 = fVar10;
    uStack_c0 = uVar4;
    fStack_bc = fVar2;
    local_b8 = fVar6;
    FUN_1801067c0(param_1,puVar1,&local_c8);
  }
  else {
    *puVar1 = CONCAT44(fVar10,fVar7);
    puVar1[1] = CONCAT44(fVar2,uVar4);
    puVar1[2] = CONCAT17(uStack_b1,CONCAT16(uStack_b2,CONCAT15(uStack_b3,CONCAT14(uStack_b4,fVar6)))
                        );
    *(longlong *)(param_1 + 8) = *(longlong *)(param_1 + 8) + 0x18;
  }
  return;
}



