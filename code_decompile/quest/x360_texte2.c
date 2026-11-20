// ===================================================
// 822C8910  ->  FUN_822c8910  (entree 822c8910)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */
/* WARNING: Removing unreachable block (ram,0x822c898c) */

undefined8 FUN_822c8910(int param_1,undefined4 param_2,int param_3,undefined4 param_4)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  int iVar3;
  undefined8 in_r0;
  char cVar6;
  int iVar4;
  int *piVar5;
  int iVar7;
  undefined8 uVar8;
  undefined4 uVar9;
  int *piVar10;
  
  iVar3 = DAT_829c649c;
  uVar8 = 0;
  *(undefined4 *)(param_1 + 0x14) = 0;
  puVar1 = *(undefined4 **)(iVar3 + 4);
  for (puVar2 = (undefined4 *)*puVar1; (puVar2 != puVar1 && (puVar2[2] != param_1));
      puVar2 = (undefined4 *)*puVar2) {
  }
  if (iVar3 == 0) {
    trapWord(0x1f,in_r0,0x16);
  }
  if ((puVar2 == puVar1) && (cVar6 = FUN_822c73c0(param_1,1), cVar6 != '\0')) {
    *(undefined4 *)(param_1 + 4) = param_4;
    *(undefined4 *)(param_1 + 8) = param_2;
    uVar9 = (undefined4)uVar8;
    *(undefined4 *)(param_1 + 0xc) = uVar9;
    *(undefined4 *)(param_1 + 0x10) = uVar9;
    *(undefined4 *)(param_1 + 0x18) = uVar9;
    *(undefined4 *)(param_1 + 0x1c) = uVar9;
    if (param_1 + 0x22 != param_3) {
      iVar4 = FUN_826015f0(param_3,0,0xffffffffffffffff);
      iVar7 = iVar4 - param_3;
      if (iVar4 == 0) {
        iVar7 = -1;
      }
      FUN_82158868(param_1 + 0x22,param_3,0x20,iVar7);
    }
    *(undefined4 *)(param_1 + 0x14) = 1;
    FUN_822c7468(param_1);
    iVar4 = *(int *)(iVar3 + 4);
    iVar7 = *(int *)(iVar4 + 4);
    piVar5 = (int *)FUN_82142ee0(0xc);
    if (piVar5 != (int *)0x0) {
      *piVar5 = iVar4;
    }
    piVar10 = piVar5 + 1;
    if (piVar10 != (int *)0x0) {
      *piVar10 = iVar7;
    }
    if (piVar5 + 2 != (int *)0x0) {
      piVar5[2] = param_1;
    }
    FUN_82205280(iVar3,1);
    *(int **)(iVar4 + 4) = piVar5;
    *(int **)*piVar10 = piVar5;
    return 1;
  }
  return uVar8;
}



