// ===================================================
// 18006F380  ->  FUN_18006f380  (entree 18006f380)
// ===================================================

undefined8 FUN_18006f380(undefined4 *param_1)

{
  longlong *plVar1;
  longlong lVar2;
  undefined *puVar3;
  bool bVar4;
  char cVar5;
  int iVar6;
  ulonglong uVar7;
  int iVar8;
  uint uVar9;
  ulonglong uVar10;
  longlong *plVar11;
  int *piVar12;
  
  iVar6 = param_1[0x36];
  if (iVar6 != 1) {
    if (iVar6 != 2) {
      if (iVar6 == 3) {
        if ((DAT_180677334 & 1) != 0) {
          return 1;
        }
        param_1[0x36] = 4;
      }
      return 0;
    }
    iVar6 = 0;
    bVar4 = false;
    iVar8 = 0;
    if (0 < (int)param_1[4]) {
      plVar11 = (longlong *)(param_1 + 0x16);
      do {
        if ((*plVar11 != 0) && (cVar5 = FUN_180244fc0(), cVar5 == '\0')) {
          bVar4 = true;
        }
        iVar8 = iVar8 + 1;
        plVar11 = plVar11 + 1;
      } while (iVar8 < (int)param_1[4]);
      if (bVar4) {
        return 1;
      }
      if (0 < (int)param_1[4]) {
        plVar11 = (longlong *)(param_1 + 0x16);
        do {
          plVar1 = (longlong *)*plVar11;
          if (plVar1 != (longlong *)0x0) {
            (**(code **)(*plVar1 + 0x50))(plVar1,*(undefined1 *)(param_1 + 0x37));
          }
          iVar6 = iVar6 + 1;
          plVar11 = plVar11 + 1;
        } while (iVar6 < (int)param_1[4]);
      }
    }
    param_1[0x36] = 3;
    return 1;
  }
  uVar7 = 0;
  piVar12 = &DAT_18034d510;
  uVar10 = uVar7;
  while (*piVar12 != -1) {
    cVar5 = FUN_1800fb7e0(*piVar12,1);
    if (cVar5 != '\0') {
      return 1;
    }
    uVar9 = (int)uVar10 + 1;
    uVar10 = (ulonglong)uVar9;
    piVar12 = piVar12 + 1;
    if (7 < (int)uVar9) {
      return 1;
    }
  }
  cVar5 = FUN_18003c1d0("EFFEFFCMN");
  uVar10 = uVar7;
  if (cVar5 == '\0') {
    return 1;
  }
  while (*(int *)(uVar10 + *(longlong *)(param_1 + 2)) != -1) {
    cVar5 = FUN_1800fb7e0(*(int *)(uVar10 + *(longlong *)(param_1 + 2)),1);
    if (cVar5 != '\0') {
      return 1;
    }
    uVar10 = uVar10 + 4;
    if (0x1f < (longlong)uVar10) {
      return 1;
    }
  }
  piVar12 = &DAT_18034d530;
  plVar11 = (longlong *)(param_1 + 0x16);
  do {
    iVar6 = *piVar12;
    if (iVar6 == -1) break;
    lVar2 = *(longlong *)(&DAT_180677270 + (longlong)iVar6 * 8);
    *plVar11 = lVar2;
    if (lVar2 != 0) {
      puVar3 = (&PTR_s_EFFECT_HIT_18034e4d0)[iVar6];
      *(int *)((longlong)(param_1 + -0x600d3547) + (longlong)piVar12) = iVar6;
      FUN_180245830(*plVar11,puVar3);
      (**(code **)(*(longlong *)*plVar11 + 0x38))((longlong *)*plVar11,*param_1);
      (**(code **)(*(longlong *)*plVar11 + 0x50))
                ((longlong *)*plVar11,*(undefined1 *)(param_1 + 0x37));
      FUN_180245a10(*plVar11,1);
    }
    uVar9 = (int)uVar7 + 1;
    uVar7 = (ulonglong)uVar9;
    plVar11 = plVar11 + 1;
    piVar12 = piVar12 + 1;
  } while ((int)uVar9 < 8);
  uVar9 = (uint)uVar7;
  param_1[4] = uVar9;
  if ((int)uVar9 < 0x10) {
    plVar11 = (longlong *)(param_1 + (longlong)(int)uVar9 * 2 + 0x16);
    piVar12 = param_1 + (longlong)(int)uVar9 + 5;
    do {
      uVar9 = (uint)uVar7;
      iVar6 = *(int *)(*(longlong *)(param_1 + 2) + 0x20 + (longlong)(int)(uVar9 - param_1[4]) * 4);
      if (iVar6 == -1) break;
      lVar2 = *(longlong *)(&DAT_180677270 + (longlong)iVar6 * 8);
      *plVar11 = lVar2;
      if (lVar2 != 0) {
        puVar3 = (&PTR_s_EFFECT_HIT_18034e4d0)[iVar6];
        *piVar12 = iVar6;
        FUN_180245830(*plVar11,puVar3);
        (**(code **)(*(longlong *)*plVar11 + 0x38))((longlong *)*plVar11,*param_1);
        (**(code **)(*(longlong *)*plVar11 + 0x50))
                  ((longlong *)*plVar11,*(undefined1 *)(param_1 + 0x37));
        FUN_180245a10(*plVar11,1);
      }
      uVar9 = uVar9 + 1;
      uVar7 = (ulonglong)uVar9;
      piVar12 = piVar12 + 1;
      plVar11 = plVar11 + 1;
    } while ((int)uVar9 < 0x10);
  }
  param_1[4] = uVar9;
  param_1[0x36] = 2;
  return 1;
}



