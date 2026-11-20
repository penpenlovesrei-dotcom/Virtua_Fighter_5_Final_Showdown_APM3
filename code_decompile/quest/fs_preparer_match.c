// ===================================================
// 180209DB0  ->  FUN_180209db0  (entree 180209db0)
// ===================================================

undefined8 FUN_180209db0(longlong param_1)

{
  int iVar1;
  char cVar2;
  int iVar3;
  int iVar4;
  undefined4 uVar5;
  uint uVar6;
  undefined4 uVar7;
  undefined8 *puVar8;
  longlong lVar9;
  undefined8 uVar10;
  undefined8 *puVar11;
  undefined8 *puVar12;
  
  if (((*(longlong *)(DAT_180c3b6f0 + 0x1fe10) == 0) ||
      (*(code **)(DAT_180c3b6f0 + 0x1fe10) == (code *)0x0)) ||
     (iVar3 = (**(code **)(DAT_180c3b6f0 + 0x1fe10))(*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0x34),
     iVar3 != 2)) {
    *(undefined4 *)(param_1 + 0x80) = 2;
    *(undefined4 *)(param_1 + 0x84) = 2;
    puVar12 = (undefined8 *)0x0;
    *(undefined4 *)(param_1 + 0x8c) = 0;
    puVar8 = (undefined8 *)FUN_18027ca60(0x60);
    puVar11 = puVar12;
    if (puVar8 != (undefined8 *)0x0) {
      FUN_1802ff420(puVar8,0,0x60);
      FUN_180244c80(puVar8);
      *puVar8 = TrnImplSelect::vftable;
      puVar11 = puVar8;
    }
    *(undefined8 **)(param_1 + 0x60) = puVar11;
    puVar8 = (undefined8 *)FUN_18027ca60(0x68);
    puVar11 = puVar12;
    if (puVar8 != (undefined8 *)0x0) {
      FUN_180244c80(puVar8);
      *puVar8 = TrnImplMenu::vftable;
      puVar8[0xb] = 0;
      *(undefined4 *)(puVar8 + 0xc) = 0;
      puVar11 = puVar8;
    }
    *(undefined8 **)(param_1 + 0x68) = puVar11;
    puVar8 = (undefined8 *)FUN_18027ca60(0x58);
    puVar11 = puVar12;
    if (puVar8 != (undefined8 *)0x0) {
      FUN_1802ff420(puVar8,0,0x58);
      FUN_180244c80(puVar8);
      *puVar8 = TrnImplVs::vftable;
      puVar11 = puVar8;
    }
    *(undefined8 **)(param_1 + 0x70) = puVar11;
    puVar8 = (undefined8 *)FUN_18027ca60(0x58);
    puVar11 = puVar12;
    if (puVar8 != (undefined8 *)0x0) {
      FUN_1802ff420(puVar8,0,0x58);
      FUN_180244c80(puVar8);
      *puVar8 = TrnImplOver::vftable;
      puVar11 = puVar8;
    }
    *(undefined8 **)(param_1 + 0x78) = puVar11;
    uVar5 = 0;
    *(undefined4 *)(param_1 + 0x80) = 0;
    if ((*(int *)(param_1 + 0x58) != 1) && (*(int *)(param_1 + 0x58) != 2)) {
      *(undefined4 *)(param_1 + 0x84) = 1;
    }
    iVar4 = 0x15;
    puVar11 = puVar12;
    iVar3 = 0x15;
    uVar7 = uVar5;
    if ((*(char *)(param_1 + 0x5c) != '\0') &&
       (lVar9 = FUN_1800b23a0(), puVar11 = (undefined8 *)0x0, iVar3 = 0x15, lVar9 != 0)) {
      cVar2 = FUN_1800b1d30(lVar9,0);
      puVar11 = puVar12;
      iVar4 = 0x15;
      uVar5 = 0;
      if (cVar2 != '\0') {
        iVar4 = FUN_1800b23e0(lVar9,0);
        uVar5 = FUN_1800b2400(lVar9,0);
        uVar6 = FUN_1800b23f0(lVar9,0);
        puVar11 = (undefined8 *)(ulonglong)uVar6;
      }
      cVar2 = FUN_1800b1d30(lVar9,1);
      iVar3 = 0x15;
      uVar7 = 0;
      if (cVar2 != '\0') {
        iVar3 = FUN_1800b23e0(lVar9,1);
        uVar7 = FUN_1800b2400(lVar9,1);
        uVar6 = FUN_1800b23f0(lVar9,1);
        puVar12 = (undefined8 *)(ulonglong)uVar6;
      }
      FUN_1800b2290();
    }
    FUN_1800b3620(*(undefined4 *)(param_1 + 0x80));
    FUN_1800489e0(*(undefined4 *)(param_1 + 0x80));
    iVar1 = *(int *)(param_1 + 0x84);
    if (iVar1 != 2) {
      uVar10 = FUN_1800b23a0();
      FUN_1800b2fa0(uVar10,iVar1,0,0);
      FUN_1800489e0(*(undefined4 *)(param_1 + 0x84));
    }
    if ((*(char *)(param_1 + 0x5c) != '\0') && (iVar4 != 0x15)) {
      uVar10 = FUN_1800b23a0();
      FUN_1800b2f80(uVar10,0,iVar4,puVar11,uVar5,0);
      if (iVar3 != 0x15) {
        uVar10 = FUN_1800b23a0();
        FUN_1800b2f80(uVar10,1,iVar3,puVar12,uVar7,0);
        if (*(int *)(param_1 + 0x88) != -1) {
          *(undefined4 *)(param_1 + 0x8c) = 2;
        }
      }
    }
    uVar10 = 1;
  }
  else {
    uVar10 = 0;
  }
  return uVar10;
}



