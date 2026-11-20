// ===================================================
// 180261840  ->  FUN_180261840  (entree 180261840)
// ===================================================

void FUN_180261840(longlong param_1,longlong param_2,longlong param_3,longlong param_4,uint param_5)

{
  undefined1 auVar1 [16];
  int iVar2;
  int iVar3;
  undefined8 *puVar4;
  int iVar5;
  ulonglong uVar6;
  undefined4 *puVar7;
  int iVar8;
  int iVar9;
  int *piVar10;
  uint uVar11;
  undefined8 uVar12;
  undefined8 uVar13;
  undefined1 auVar14 [16];
  undefined1 auVar15 [16];
  undefined8 local_58;
  int iStack_50;
  int iStack_4c;
  int local_48;
  int iStack_44;
  
  uVar11 = 0;
  if (param_5 != 0) {
    piVar10 = (int *)(param_3 + 8);
    puVar7 = (undefined4 *)(param_1 + 0x1e18);
    do {
      if (param_2 == 0) {
        iStack_50 = *(int *)(param_1 + 0x1dc0);
        local_58._0_4_ = 0;
        iStack_4c = *(int *)(param_1 + 0x1dc4);
        uVar13 = *(undefined8 *)(param_1 + 0x1dc0);
        local_58._4_4_ = 0;
        local_58 = 0;
        uVar12 = local_58;
      }
      else {
        puVar4 = (undefined8 *)((param_2 - param_3) + -8 + (longlong)piVar10);
        uVar12 = *puVar4;
        uVar13 = puVar4[1];
        iStack_4c = (int)((ulonglong)uVar13 >> 0x20);
        iStack_50 = (int)uVar13;
        local_58._4_4_ = (int)((ulonglong)uVar12 >> 0x20);
        local_58._0_4_ = (int)uVar12;
      }
      puVar4 = (undefined8 *)((longlong)piVar10 + (param_1 - param_3) + 0x1dcc);
      *puVar4 = uVar12;
      puVar4[1] = uVar13;
      if (param_4 != 0) {
        puVar7[-1] = *(undefined4 *)(param_4 + (ulonglong)(uVar11 * 2) * 4);
        *puVar7 = *(undefined4 *)(param_4 + (ulonglong)(uVar11 * 2 + 1) * 4);
      }
      iVar9 = *(int *)(param_1 + 0x1dc0);
      iVar2 = 0;
      if (0 < (int)local_58) {
        iVar2 = (int)local_58;
      }
      iVar5 = iVar9;
      if (iVar2 < iVar9) {
        iVar5 = iVar2;
      }
      iVar2 = *(int *)(param_1 + 0x1dc4);
      iVar3 = 0;
      if (0 < iStack_50) {
        iVar3 = iStack_50;
      }
      if (iVar3 < iVar9) {
        iVar9 = iVar3;
      }
      iVar3 = 0;
      if (0 < local_58._4_4_) {
        iVar3 = local_58._4_4_;
      }
      iVar8 = iVar2;
      if (iVar3 < iVar2) {
        iVar8 = iVar3;
      }
      iVar3 = 0;
      if (0 < iStack_4c) {
        iVar3 = iStack_4c;
      }
      if (iVar3 < iVar2) {
        iVar2 = iVar3;
      }
      local_48 = iVar5;
      iStack_44 = iVar8;
      if (param_3 != 0) {
        iVar3 = iVar5;
        if (iVar5 < piVar10[-2]) {
          iVar3 = piVar10[-2];
        }
        local_48 = iVar9;
        if (iVar3 < iVar9) {
          local_48 = iVar3;
        }
        if (iVar5 < *piVar10) {
          iVar5 = *piVar10;
        }
        if (iVar5 < iVar9) {
          iVar9 = iVar5;
        }
        iVar5 = iVar8;
        if (iVar8 < piVar10[-1]) {
          iVar5 = piVar10[-1];
        }
        iStack_44 = iVar2;
        if (iVar5 < iVar2) {
          iStack_44 = iVar5;
        }
        if (iVar8 < piVar10[1]) {
          iVar8 = piVar10[1];
        }
        if (iVar8 < iVar2) {
          iVar2 = iVar8;
        }
      }
      uVar11 = uVar11 + 1;
      puVar7 = puVar7 + 2;
      puVar4 = (undefined8 *)((longlong)piVar10 + (param_1 - param_3) + 0x1e48);
      *puVar4 = CONCAT44(iStack_44,local_48);
      puVar4[1] = CONCAT44(iVar2,iVar9);
      piVar10 = piVar10 + 4;
    } while (uVar11 < param_5);
  }
  if (param_5 < 4) {
    puVar4 = (undefined8 *)(param_1 + 0x1ddc + (ulonglong)param_5 * 0x10);
    uVar6 = (ulonglong)(4 - param_5);
    do {
      puVar4[-1] = 0;
      *puVar4 = 0;
      *(undefined8 *)((longlong)puVar4 + 0x74) = 0;
      *(undefined8 *)((longlong)puVar4 + 0x7c) = 0;
      puVar4 = puVar4 + 2;
      uVar6 = uVar6 - 1;
    } while (uVar6 != 0);
  }
  auVar14._0_4_ = (float)(*(int *)(param_1 + 0x1ddc) - *(int *)(param_1 + 0x1dd4));
  auVar14._4_8_ = SUB128(ZEXT812(0),4);
  auVar14._12_4_ = 0;
  auVar15._0_4_ = (float)(*(int *)(param_1 + 0x1de0) - *(int *)(param_1 + 0x1dd8));
  auVar15._4_8_ = SUB128(ZEXT812(0),4);
  auVar15._12_4_ = 0;
  auVar1 = vinsertps_avx(auVar14,auVar15,0x10);
  auVar1 = vinsertps_avx(auVar1,ZEXT416((uint)(DAT_180346d3c / auVar14._0_4_)),0x20);
  auVar1 = vinsertps_avx(auVar1,ZEXT416((uint)(DAT_180346d3c / auVar15._0_4_)),0x30);
  *(undefined1 (*) [16])(param_1 + 0x1e40) = auVar1;
  *(uint *)(param_1 + 0x1dd0) = param_5;
  FUN_18026e0f0(*(undefined8 *)(param_1 + 0x18),(int *)(param_1 + 0x1dd4),param_5,param_1 + 0x1e14);
  FUN_18026e060(*(undefined8 *)(param_1 + 0x18),param_1 + 0x1e50,param_5);
  FUN_18025e830(param_1,DAT_180347cb0,DAT_180347cb0);
  return;
}



