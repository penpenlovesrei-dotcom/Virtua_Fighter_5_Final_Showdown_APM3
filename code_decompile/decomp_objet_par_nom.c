// ===================================================
// 1800f8b50  ->  FUN_1800f8b50  (entree 1800f8b50)
// ===================================================

undefined4 FUN_1800f8b50(byte *param_1)

{
  byte bVar1;
  uint uVar2;
  byte *pbVar3;
  longlong *plVar4;
  uint uVar5;
  longlong lVar6;
  longlong *plVar7;
  longlong lVar8;
  longlong lVar9;
  
  uVar5 = 0;
  plVar7 = *(longlong **)(DAT_18070fa88 + 0xd0);
  plVar4 = *(longlong **)(DAT_18070fa88 + 200);
  lVar8 = (longlong)plVar7 - (longlong)plVar4 >> 4;
  if (0 < lVar8) {
    do {
      lVar9 = lVar8 >> 1;
      pbVar3 = (byte *)plVar4[lVar9 * 2];
      if ((pbVar3 != (byte *)0x0) && (param_1 != (byte *)0x0)) {
        lVar6 = (longlong)param_1 - (longlong)pbVar3;
        do {
          bVar1 = *pbVar3;
          if (bVar1 != pbVar3[lVar6]) {
            uVar2 = -(uint)(bVar1 < pbVar3[lVar6]) | 1;
            goto LAB_1800f8bc9;
          }
          pbVar3 = pbVar3 + 1;
        } while (bVar1 != 0);
        uVar2 = 0;
LAB_1800f8bc9:
        if ((int)uVar2 < 0) {
          plVar4 = plVar4 + lVar9 * 2 + 2;
          lVar9 = lVar8 + (-1 - lVar9);
        }
      }
      lVar8 = lVar9;
    } while (0 < lVar9);
    plVar7 = *(longlong **)(DAT_18070fa88 + 0xd0);
  }
  if (plVar4 != plVar7) {
    if ((param_1 == (byte *)0x0) || (*plVar4 == 0)) goto LAB_1800f8c25;
    lVar8 = *plVar4 - (longlong)param_1;
    do {
      bVar1 = *param_1;
      if (bVar1 != param_1[lVar8]) {
        uVar5 = -(uint)(bVar1 < param_1[lVar8]) | 1;
        break;
      }
      param_1 = param_1 + 1;
    } while (bVar1 != 0);
    if (-1 < (int)uVar5) goto LAB_1800f8c25;
  }
  plVar4 = plVar7;
LAB_1800f8c25:
  if (plVar4 == *(longlong **)(DAT_18070fa88 + 0xd0)) {
    return 0xffffffff;
  }
  return (int)plVar4[1];
}



