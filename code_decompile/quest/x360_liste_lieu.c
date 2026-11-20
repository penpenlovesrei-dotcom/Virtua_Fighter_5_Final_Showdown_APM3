// ===================================================
// 8230E018  ->  FUN_8230e018  (entree 8230e018)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

void FUN_8230e018(ulonglong param_1,int param_2,uint param_3)

{
  uint uVar1;
  byte *pbVar2;
  byte *pbVar3;
  uint auStack_50 [20];
  
  if ((param_1 & 0xffffffff) != 0) {
    pbVar3 = &DAT_82acd874;
    auStack_50[0] = 0;
    pbVar2 = (byte *)(DAT_82acb928 + 0x88);
    do {
      uVar1 = auStack_50[0];
      if (((param_2 == 0) ||
          ((1 << (*pbVar3 & 0x1f) & *(uint *)((*pbVar3 >> 3 & 0x1ffffffc) + param_2)) != 0)) &&
         ((param_3 == 0 || ((1 << (*pbVar2 & 0x3f) & param_3) != 0)))) {
        FUN_82220058(param_1,auStack_50);
      }
      auStack_50[0] = uVar1 + 1;
      pbVar2 = pbVar2 + 0x90;
      pbVar3 = pbVar3 + 8;
    } while (auStack_50[0] < 1000);
  }
  return;
}



