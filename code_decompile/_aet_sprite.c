// ===================================================
// 180026530  ->  FUN_180026530  (entree 180026530)
// ===================================================

void FUN_180026530(longlong *param_1,undefined8 param_2,longlong param_3,float param_4,float param_5
                  )

{
  float fVar1;
  int iVar2;
  longlong lVar3;
  ulonglong uVar4;
  longlong lVar5;
  double dVar6;
  double dVar7;
  double dVar8;
  double dVar9;
  double dVar10;
  
  iVar2 = *(int *)(param_3 + 0x18);
  lVar5 = 0;
  if (iVar2 != 0) {
    lVar5 = param_3 + 0x18 + (longlong)iVar2;
  }
  if (*(uint *)(lVar5 + 0xc) < 2) {
    if (*(uint *)(lVar5 + 0xc) != 0) {
                    /* WARNING: Could not recover jumptable at 0x000180026722. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(*param_1 + 0xd0))(param_1,param_2,param_3,0);
      return;
    }
    lVar5 = param_1[0x33] - param_1[0x32] >> 0x3f;
    if ((param_1[0x33] - param_1[0x32]) / 0x28 + lVar5 != lVar5) {
                    /* WARNING: Could not recover jumptable at 0x00018002677b. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(*param_1 + 200))(param_1,param_2,param_3,param_5);
      return;
    }
  }
  else {
    fVar1 = *(float *)(lVar5 + 8);
    dVar7 = (double)(fVar1 * param_4) + DAT_180348aa8;
    uVar4 = (ulonglong)dVar7;
    if ((*(byte *)(param_3 + 0x14) & 8) == 0) {
      (**(code **)(*param_1 + 0xd0))
                (param_1,(double)(fVar1 * param_4),fVar1,uVar4 & 0xffffffff,param_5);
    }
    else {
      dVar8 = DAT_180346d40;
      if (fVar1 <= DAT_180346d3c) {
        dVar9 = dVar7 - (double)(uVar4 & 0xffffffff);
      }
      else {
        dVar9 = DAT_180346d40 - DAT_180346d40 / (double)fVar1;
        if (0.0 <= dVar7 - DAT_180346d40) {
          lVar3 = *param_1;
          dVar6 = (double)FUN_18030d380(dVar9);
          (**(code **)(lVar3 + 0xd0))
                    (param_1,param_2,param_3,(int)uVar4 + -1,(float)(dVar6 * (double)param_5));
        }
      }
      lVar3 = *param_1;
      dVar10 = (double)param_5;
      dVar6 = (double)FUN_18030ce00(dVar9);
      (**(code **)(lVar3 + 0xd0))
                (param_1,param_2,param_3,uVar4 & 0xffffffff,(float)(dVar6 * dVar10));
      if (dVar7 + dVar8 < (double)*(uint *)(lVar5 + 0xc)) {
        lVar5 = *param_1;
        dVar7 = (double)FUN_18030d380(dVar9);
        (**(code **)(lVar5 + 0xd0))(param_1,param_2,param_3,(int)uVar4 + 1,(float)(dVar7 * dVar10));
      }
    }
  }
  return;
}



