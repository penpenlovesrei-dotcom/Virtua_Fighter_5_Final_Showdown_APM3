// ===================================================
// 838C92A  ->  FUN_0838c92a  (entree 0838c92a)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_0838c92a(int param_1)

{
  char cVar1;
  int iVar2;
  int iVar3;
  longdouble lVar4;
  
  iVar2 = *(int *)(param_1 + 0x4c);
  iVar3 = *(int *)(param_1 + 0x54);
  if (iVar3 != iVar3 + iVar2 * 4) {
    do {
      cVar1 = FUN_081e35ee(iVar3);
      if (cVar1 == '\0') {
        return 0;
      }
      iVar2 = *(int *)(param_1 + 0x4c);
      iVar3 = iVar3 + 4;
    } while (iVar3 != *(int *)(param_1 + 0x54) + iVar2 * 4);
  }
  iVar3 = *(int *)(param_1 + 0x54);
  if (iVar3 != iVar3 + iVar2 * 4) {
    do {
      iVar2 = FUN_081e3552(iVar3);
      if (iVar2 - 0x364U < 2) {
        lVar4 = (longdouble)FUN_081e37de(iVar3);
        FUN_081e3afa(iVar3,(float)(lVar4 - (longdouble)_DAT_08600134));
        FUN_081e3c3c(iVar3);
      }
      FUN_081e3a50(iVar3,1);
      FUN_081e38f8(iVar3,0);
      iVar2 = iVar3 + 4;
      FUN_081e39a4(iVar3,1);
      iVar3 = iVar2;
    } while (iVar2 != *(int *)(param_1 + 0x54) + *(int *)(param_1 + 0x4c) * 4);
  }
  if (*(int *)(param_1 + 0x98) != 0) {
    FUN_080815c2(2,&LAB_0838c746,param_1);
    FUN_080815c2(3,&LAB_0838c75a,param_1);
  }
  return 1;
}



// ===================================================
// 838CA32  ->  FUN_0838ca32  (entree 0838ca32)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_0838ca32(int param_1)

{
  float fVar1;
  int iVar2;
  int iVar3;
  longdouble lVar4;
  longdouble lVar5;
  float fVar6;
  float fVar7;
  undefined1 local_5c [76];
  
  if (*(int *)(param_1 + 0x98) != 0) {
    FUN_08071492(local_5c);
    if (0.0 <= *(float *)(param_1 + 0x9c)) {
      iVar3 = (int)ROUND(*(float *)(param_1 + 0x9c));
      lVar4 = (longdouble)FUN_08096658();
      lVar5 = (longdouble)_DAT_08600138;
      lVar4 = lVar4 + (longdouble)*(float *)(param_1 + 0x9c);
      *(float *)(param_1 + 0x9c) = (float)lVar4;
      if (lVar5 < lVar4) {
        *(undefined4 *)(param_1 + 0x9c) = 0;
      }
    }
    else {
      iVar3 = 0;
    }
    fVar7 = (float)_DAT_08522748;
    fVar1 = _DAT_085359a0 * (float)(iVar3 % 0x168);
    fVar6 = sinf(_DAT_0853599c * (float)(iVar3 % 0x200) * fVar7);
    fVar6 = _DAT_08532fd8 * fVar6;
    fVar7 = sinf(fVar1 * fVar7);
    fVar7 = _DAT_08532fd8 * fVar7;
    FUN_08072af6(local_5c);
    FUN_08073562(local_5c,0,0xbe4ccccd,0);
    FUN_08073340(local_5c,fVar6);
    FUN_08073520(local_5c,fVar7);
    iVar3 = *(int *)(param_1 + 0x54);
    if (iVar3 != iVar3 + *(int *)(param_1 + 0x4c) * 4) {
      do {
        iVar2 = FUN_081e3552(iVar3);
        if (iVar2 - 0x364U < 2) {
          FUN_081e3ddc(iVar3,local_5c);
        }
        iVar3 = iVar3 + 4;
      } while (iVar3 != *(int *)(param_1 + 0x54) + *(int *)(param_1 + 0x4c) * 4);
    }
    FUN_080c7b4e(local_5c);
  }
  return 0;
}



// ===================================================
// 838C868  ->  FUN_0838c868  (entree 0838c868)
// ===================================================

void FUN_0838c868(int param_1,int param_2)

{
  int *piVar1;
  uint uVar2;
  undefined4 *puVar3;
  int *piVar4;
  char cVar5;
  int iVar6;
  int *piVar7;
  int aiStack_44 [13];
  
  aiStack_44[2] = param_2;
  iVar6 = FUN_0838c718();
  if ((iVar6 != 0) && (piVar7 = *(int **)(iVar6 + 4), piVar7 != (int *)0x0)) {
    if (param_2 == 8) {
      *(undefined4 *)(param_1 + 0x98) = 1;
    }
    iVar6 = *piVar7;
    piVar4 = aiStack_44 + 2;
    while ((iVar6 != -1 && (*(int *)(param_1 + 0x4c) != *(int *)(param_1 + 0x50)))) {
      piVar1 = aiStack_44 + 6;
      piVar4[1] = iVar6;
      *piVar4 = (int)piVar1;
      piVar4[-1] = 0x838c8b9;
      FUN_081e3330();
      piVar4[-1] = (int)piVar1;
                    /* try { // try from 0838c8bf to 0838c8e8 has its CatchHandler @ 0838c921 */
      piVar4[-2] = 0x838c8c4;
      cVar5 = FUN_081e3504();
      if (cVar5 != '\0') {
        piVar4[-1] = (int)piVar1;
        piVar4[-2] = 0x838c8e9;
        FUN_081e359a();
        iVar6 = *(int *)(param_1 + 0x4c);
        uVar2 = iVar6 + 1;
        if (uVar2 <= *(uint *)(param_1 + 0x50)) {
          *(uint *)(param_1 + 0x4c) = uVar2;
          puVar3 = (undefined4 *)(*(int *)(param_1 + 0x54) + iVar6 * 4);
          if (puVar3 != (undefined4 *)0x0) {
            *puVar3 = aiStack_44[6];
          }
        }
      }
      piVar7 = piVar7 + 1;
      iVar6 = *piVar7;
      piVar4 = piVar4 + -1;
    }
  }
  return;
}



