// ===================================================
// 18019AC70  ->  FUN_18019ac70  (entree 18019ac70)
// ===================================================

void FUN_18019ac70(longlong *param_1,uint param_2,short *param_3,longlong param_4)

{
  short *psVar1;
  float fVar2;
  uint uVar3;
  bool bVar4;
  ulonglong uVar5;
  longlong lVar6;
  short *psVar7;
  ulonglong uVar8;
  undefined1 local_res8 [8];
  
  psVar1 = param_3 + param_4;
  if (((param_2 >> 9 & 1) == 0) && ((char)param_1[2] != '\0')) {
    param_2 = param_2 | 0x200;
  }
  lVar6 = param_1[9];
  if ((((*(float *)(lVar6 + 0x24) == *(float *)(lVar6 + 0x14)) &&
       (*(float *)(lVar6 + 0x28) == *(float *)(lVar6 + 0x18))) ||
      (*(float *)(lVar6 + 0x14) != *(float *)(lVar6 + 0x1c))) ||
     (*(float *)(lVar6 + 0x18) != *(float *)(lVar6 + 0x20))) {
    bVar4 = false;
  }
  else {
    bVar4 = true;
  }
  uVar3 = param_2 | 0x400;
  if (!bVar4) {
    uVar3 = param_2;
  }
  do {
    if (param_3 == psVar1) {
      return;
    }
    uVar8 = (longlong)psVar1 - (longlong)param_3 >> 1;
    psVar7 = param_3;
    for (uVar5 = uVar8; uVar5 != 0; uVar5 = uVar5 - 1) {
      if (*psVar7 == 10) goto LAB_18019ad23;
      psVar7 = psVar7 + 1;
    }
    psVar7 = (short *)0x0;
LAB_18019ad23:
    if (psVar7 == (short *)0x0) {
      (**(code **)(*param_1 + 8))(param_1,local_res8,uVar3,param_3,param_3 + uVar8);
      return;
    }
    lVar6 = (**(code **)(*param_1 + 8))();
    uVar5 = ((longlong)psVar7 - (longlong)param_3 >> 1) + 1;
    fVar2 = *(float *)(lVar6 + 4);
    *(undefined4 *)((longlong)param_1 + 0x34) = *(undefined4 *)((longlong)param_1 + 0x3c);
    fVar2 = fVar2 + *(float *)(param_1[9] + 0x38) + *(float *)(param_1 + 7);
    *(float *)(param_1 + 7) = fVar2;
    *(float *)(param_1 + 8) = fVar2;
    if (uVar8 <= uVar5) {
      return;
    }
    param_3 = param_3 + uVar5;
  } while( true );
}



