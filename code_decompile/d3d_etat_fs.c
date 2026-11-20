// ===================================================
// 180251551  ->  FUN_180251390  (entree 180251390)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_180251390(longlong param_1,ulonglong param_2)

{
  ushort uVar1;
  undefined8 uVar2;
  ulonglong uVar3;
  undefined1 auVar4 [16];
  longlong *plVar5;
  longlong lVar6;
  undefined8 *puVar7;
  longlong *plVar8;
  longlong lVar9;
  longlong *plVar10;
  uint uVar11;
  longlong *plVar12;
  longlong lVar13;
  uint local_dc;
  undefined8 local_d8;
  
  lVar13 = (param_2 & 0xffffffff) * 0x20 + *(longlong *)(param_1 + 0x1020);
  plVar5 = (longlong *)FUN_180253c90();
  uVar1 = *(ushort *)(lVar13 + 0x1a);
  lVar9 = *plVar5;
  if (((uVar1 & 4) != 0) &&
     (lVar6 = FUN_180251b70(param_1), *(longlong *)(lVar9 + 0xfb8) != *(longlong *)(lVar6 + 0x10)))
  {
    *(longlong *)(lVar9 + 0x1258) = lVar6;
    *(undefined8 *)(lVar9 + 0xfb8) = *(undefined8 *)(lVar6 + 0x10);
    (**(code **)(**(longlong **)(lVar9 + 0x18) + 0x38))
              (*(longlong **)(lVar9 + 0x18),2,1,*(longlong *)(lVar6 + 0x18) + 0x10);
  }
  if (((uVar1 & 0x20) != 0) &&
     (lVar6 = FUN_180252180(param_1), *(longlong *)(lVar9 + 0xfd0) != *(longlong *)(lVar6 + 0x10)))
  {
    *(longlong *)(lVar9 + 0x1270) = lVar6;
    *(undefined8 *)(lVar9 + 0xfd0) = *(undefined8 *)(lVar6 + 0x10);
    (**(code **)(**(longlong **)(lVar9 + 0x18) + 0x38))
              (*(longlong **)(lVar9 + 0x18),5,1,*(longlong *)(lVar6 + 0x18) + 0x10);
  }
  if (((uVar1 & 0x10) != 0) &&
     (lVar6 = FUN_180251920(param_1), *(longlong *)(lVar9 + 0xfc8) != *(longlong *)(lVar6 + 0x10)))
  {
    *(longlong *)(lVar9 + 0x1268) = lVar6;
    *(undefined8 *)(lVar9 + 0xfc8) = *(undefined8 *)(lVar6 + 0x10);
    (**(code **)(**(longlong **)(lVar9 + 0x18) + 0x38))
              (*(longlong **)(lVar9 + 0x18),4,1,*(longlong *)(lVar6 + 0x18) + 0x10);
  }
  if (((uVar1 & 8) != 0) &&
     (lVar6 = FUN_180251ac0(param_1), *(longlong *)(lVar9 + 0xfc0) != *(longlong *)(lVar6 + 0x10)))
  {
    *(longlong *)(lVar9 + 0x1260) = lVar6;
    *(undefined8 *)(lVar9 + 0xfc0) = *(undefined8 *)(lVar6 + 0x10);
    (**(code **)(**(longlong **)(lVar9 + 0x18) + 0x38))
              (*(longlong **)(lVar9 + 0x18),3,1,*(longlong *)(lVar6 + 0x18) + 0x10);
  }
  if ((uVar1 & 0x40) != 0) {
    lVar6 = *(longlong *)(param_1 + 0xe70);
    if (lVar6 == 0) {
      lVar6 = FUN_180253c90();
      puVar7 = (undefined8 *)FUN_180253c90();
      auVar4 = vinsertps_avx(_DAT_180350980,ZEXT416(*(uint *)(lVar6 + 0xd959c)),0);
      auVar4 = vinsertps_avx(auVar4,ZEXT416(*(uint *)(lVar6 + 0xd95a0)),0x10);
      auVar4 = vinsertps_avx(auVar4,ZEXT416(*(uint *)(lVar6 + 0xd95a4)),0x20);
      uVar2 = *puVar7;
      *(undefined1 (*) [16])(param_1 + 0xe20) = auVar4;
      auVar4 = vinsertps_avx(ZEXT416(*(uint *)(lVar6 + 0xd9598)),ZEXT416(*(uint *)(lVar6 + 0xd95a8))
                             ,0x10);
      auVar4 = vinsertps_avx(auVar4,ZEXT416(*(uint *)(lVar6 + 0xd95ac)),0x20);
      auVar4 = vinsertps_avx(auVar4,ZEXT416(*(uint *)(lVar6 + 0xd95b0)),0x30);
      *(undefined1 (*) [16])(param_1 + 0xe30) = auVar4;
      lVar6 = FUN_18025bee0(uVar2,6,2);
      *(longlong *)(param_1 + 0xe70) = lVar6;
    }
    if (*(longlong *)(lVar9 + 0xfd8) != *(longlong *)(lVar6 + 0x10)) {
      *(longlong *)(lVar9 + 0x1278) = lVar6;
      *(undefined8 *)(lVar9 + 0xfd8) = *(undefined8 *)(lVar6 + 0x10);
      (**(code **)(**(longlong **)(lVar9 + 0x18) + 0x38))
                (*(longlong **)(lVar9 + 0x18),6,1,*(longlong *)(lVar6 + 0x18) + 0x10);
    }
  }
  if (((uVar1 & 1) != 0) &&
     (lVar6 = FUN_18025bee0(lVar9,0,0x20,param_1 + 0x400),
     *(longlong *)(lVar9 + 0xfa8) != *(longlong *)(lVar6 + 0x10))) {
    *(longlong *)(lVar9 + 0x1248) = lVar6;
    *(undefined8 *)(lVar9 + 0xfa8) = *(undefined8 *)(lVar6 + 0x10);
    (**(code **)(**(longlong **)(lVar9 + 0x18) + 0x38))
              (*(longlong **)(lVar9 + 0x18),0,1,*(longlong *)(lVar6 + 0x18) + 0x10);
  }
  if (((uVar1 & 2) != 0) &&
     (lVar6 = FUN_18025bee0(lVar9,1,4,param_1 + 0x600),
     *(longlong *)(lVar9 + 0xfb0) != *(longlong *)(lVar6 + 0x10))) {
    *(longlong *)(lVar9 + 0x1250) = lVar6;
    *(undefined8 *)(lVar9 + 0xfb0) = *(undefined8 *)(lVar6 + 0x10);
    (**(code **)(**(longlong **)(lVar9 + 0x18) + 0x38))
              (*(longlong **)(lVar9 + 0x18),1,1,*(longlong *)(lVar6 + 0x18) + 0x10);
  }
  if ((uVar1 & 0x2200) == 0x2200) {
    FUN_1802617e0(lVar9,param_1 + 0xeb0,0x100);
    lVar9 = *(longlong *)(lVar9 + 0x38);
    uVar11 = (((((((((((((((*(byte *)(param_1 + 0xfbf) & 1) * 2 | *(byte *)(param_1 + 0xfbe) & 1) *
                          2 | *(byte *)(param_1 + 0xfbd) & 1) * 2 | *(byte *)(param_1 + 0xfbc) & 1)
                        * 2 | *(byte *)(param_1 + 0xfbb) & 1) * 2 | *(byte *)(param_1 + 0xfba) & 1)
                      * 2 | *(byte *)(param_1 + 0xfb9) & 1) * 2 | *(byte *)(param_1 + 0xfb8) & 1) *
                    2 | *(byte *)(param_1 + 0xfb7) & 1) * 2 | *(byte *)(param_1 + 0xfb6) & 1) * 2 |
                 *(byte *)(param_1 + 0xfb5) & 1) * 2 | *(byte *)(param_1 + 0xfb4) & 1) * 2 |
               *(byte *)(param_1 + 0xfb3) & 1) * 2 | *(byte *)(param_1 + 0xfb2) & 1) * 2 |
             *(byte *)(param_1 + 0xfb1) & 1) * 2 | *(byte *)(param_1 + 0xfb0) & 1 |
             *(uint *)(lVar9 + 0x420) & 0xffff0000;
    if (*(uint *)(lVar9 + 0x420) != uVar11) {
      *(uint *)(lVar9 + 0x420) = uVar11;
      *(ulonglong *)(lVar9 + 8) = *(ulonglong *)(lVar9 + 8) | 0x4000000000000;
      *(undefined8 *)(lVar9 + 0x80) = 0x1010d;
    }
    plVar5 = *(longlong **)(param_1 + 0x1070);
    plVar8 = (longlong *)0x0;
    local_dc = 0;
    plVar10 = plVar8;
    while (plVar12 = plVar8, plVar5 != (longlong *)0x0) {
      uVar3 = *(ulonglong *)((longlong)*(short *)((longlong)plVar5 + 0xe) + 0x10 + (longlong)plVar5)
      ;
      if (uVar3 < 0x40000004) {
        plVar12 = plVar5;
        if (0x40000002 < uVar3) break;
        (&local_d8)[(longlong)plVar10] = (&local_d8)[(longlong)plVar10] & 0xffff000000000000;
        (&local_d8)[(longlong)plVar10] =
             (&local_d8)[(longlong)plVar10] | (ulonglong)plVar5 & 0xffffffffffff;
        *(undefined2 *)((longlong)&local_d8 + (longlong)plVar10 * 8 + 6) = 1;
        lVar9 = plVar5[1];
      }
      else {
        (&local_d8)[(longlong)plVar10] = (&local_d8)[(longlong)plVar10] & 0xffff000000000000;
        (&local_d8)[(longlong)plVar10] =
             (&local_d8)[(longlong)plVar10] | (ulonglong)plVar5 & 0xffffffffffff;
        *(undefined2 *)((longlong)&local_d8 + (longlong)plVar10 * 8 + 6) = 0;
        lVar9 = *plVar5;
      }
      local_dc = local_dc + 1;
      plVar10 = (longlong *)(ulonglong)local_dc;
      plVar5 = (longlong *)((lVar9 << 0x10) >> 0x10);
    }
    if (plVar12 != (longlong *)0x0) {
      plVar8 = (longlong *)((longlong)*(short *)((longlong)plVar12 + 0xe) + (longlong)plVar12);
    }
    if (plVar8 == (longlong *)0x0) {
      lVar9 = FUN_180263610(0x40000003);
      FUN_18024f5b0(param_1 + 0x1070,0x40000003,lVar9);
    }
    else {
      lVar9 = plVar8[3];
    }
    *(uint *)(param_1 + 0xfc4) = *(uint *)(param_1 + 0xfc4) | 4;
    *(longlong *)(param_1 + 0xfe0) = lVar9;
  }
  uVar1 = *(ushort *)(lVar13 + 0x18);
  if (uVar1 != 0) {
    if ((uVar1 & 1) != 0) {
      FUN_180256b50(0x800);
      return;
    }
    if ((uVar1 & 8) != 0) {
      FUN_180256b50(0x803);
    }
  }
  return;
}



