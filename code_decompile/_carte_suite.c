// ===================================================
// 82308838  ->  FUN_82308838  (entree 82308838)
// ===================================================

/* WARNING: Function: __savegprlr_22 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_22 replaced with injection: x360_restgprlr */

void FUN_82308838(int param_1)

{
  undefined1 uVar1;
  uint uVar2;
  int iVar4;
  undefined8 uVar3;
  int iVar5;
  int *piVar6;
  uint *puVar7;
  float *pfVar8;
  double dVar9;
  double dVar10;
  double dVar11;
  int aiStack_80 [32];
  
  piVar6 = aiStack_80;
  puVar7 = (uint *)(param_1 + 300);
  aiStack_80[0] = 0x12;
  dVar9 = (double)DAT_82054e74;
  pfVar8 = (float *)(param_1 + 0x114);
  iVar5 = 2;
  aiStack_80[1] = 0x13;
  do {
    if (*(int *)(*piVar6 * 8 + param_1 + 0x4c) != 0) {
      uVar1 = *(undefined1 *)((*piVar6 + 10) * 8 + param_1);
      iVar4 = FUN_823158c0(uVar1);
      if (iVar4 == 0) {
        uVar2 = *puVar7;
        dVar11 = (double)*pfVar8;
        dVar10 = (double)pfVar8[1];
        FUN_8223bc10(0xe);
        FUN_8223c130((ulonglong)uVar2 + 1);
        FUN_8223c048(0xffffffffffffffff);
        FUN_8223beb8(dVar11,dVar10);
        FUN_8223c198(1);
        uVar3 = FUN_823158f8(uVar1);
        FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar3);
        FUN_8223beb8(dVar11,(double)(float)(dVar10 + dVar9));
        FUN_8223c198(1);
        uVar3 = FUN_82322798(0x27a);
        FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar3);
      }
    }
    iVar5 = iVar5 + -1;
    pfVar8 = pfVar8 + 3;
    piVar6 = piVar6 + 1;
    puVar7 = puVar7 + 1;
  } while (iVar5 != 0);
  return;
}



