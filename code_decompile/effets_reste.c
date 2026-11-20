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



// ===================================================
// 180080a10  ->  FUN_180080a10  (entree 180080a10)
// ===================================================

void FUN_180080a10(undefined1 *param_1,int param_2)

{
  undefined8 *puVar1;
  undefined4 uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  char cVar5;
  int iVar6;
  undefined4 *puVar7;
  uint uVar8;
  undefined4 *puVar9;
  undefined4 *puVar10;
  undefined4 *puVar11;
  
  puVar9 = (undefined4 *)0x0;
  FUN_1800805a0();
  puVar7 = &DAT_180643490;
  if (param_2 != DAT_180643490) {
    puVar7 = puVar9;
  }
  puVar11 = &DAT_1806434c8;
  if (param_2 != DAT_1806434c8) {
    puVar11 = puVar7;
  }
  if (param_2 == DAT_180643500) {
    puVar11 = &DAT_180643500;
  }
  else if (puVar11 == (undefined4 *)0x0) {
    return;
  }
  *(int *)(param_1 + 4) = param_2;
  param_1[8] = *(undefined1 *)(puVar11 + 1);
  cVar5 = FUN_180080d40(param_1 + 0x10,puVar11[2],puVar11[3],*(undefined1 *)(puVar11 + 0xd),
                        *(undefined1 *)((longlong)puVar11 + 0x35));
  if (cVar5 != '\0') {
    uVar2 = puVar11[5];
    *(undefined4 *)(param_1 + 0xf4) = uVar2;
    puVar7 = puVar9;
    puVar10 = puVar9;
    if (0 < *(int *)(param_1 + 0x20)) {
      do {
        uVar8 = (int)puVar7 + 1;
        *(undefined4 *)(*(longlong *)(param_1 + 0x28) + -0x14 + (longlong)(puVar10 + 0x1c)) = uVar2;
        puVar7 = (undefined4 *)(ulonglong)uVar8;
        puVar10 = puVar10 + 0x1c;
      } while ((int)uVar8 < *(int *)(param_1 + 0x20));
    }
    uVar3 = *(undefined8 *)(puVar11 + 9);
    uVar4 = *(undefined8 *)(puVar11 + 0xb);
    *(undefined8 *)(param_1 + 0xe0) = uVar3;
    *(undefined8 *)(param_1 + 0xe8) = uVar4;
    puVar7 = puVar9;
    puVar10 = puVar9;
    if (0 < *(int *)(param_1 + 0x30)) {
      do {
        uVar8 = (int)puVar10 + 1;
        puVar1 = (undefined8 *)((longlong)puVar7 + *(longlong *)(param_1 + 0x38) + 8);
        *puVar1 = uVar3;
        puVar1[1] = uVar4;
        puVar7 = puVar7 + 0x2a;
        puVar10 = (undefined4 *)(ulonglong)uVar8;
      } while ((int)uVar8 < *(int *)(param_1 + 0x30));
    }
    uVar2 = puVar11[4];
    iVar6 = *(int *)(param_1 + 0x30);
    *(undefined4 *)(param_1 + 0xf0) = uVar2;
    puVar7 = puVar9;
    puVar10 = puVar9;
    if (0 < iVar6) {
      do {
        uVar8 = (int)puVar10 + 1;
        *(undefined4 *)((longlong)puVar7 + *(longlong *)(param_1 + 0x38) + 0x18) = uVar2;
        iVar6 = *(int *)(param_1 + 0x30);
        puVar7 = puVar7 + 0x2a;
        puVar10 = (undefined4 *)(ulonglong)uVar8;
      } while ((int)uVar8 < iVar6);
    }
    puVar7 = puVar9;
    puVar10 = puVar9;
    if (0 < *(int *)(param_1 + 0x20)) {
      do {
        uVar8 = (int)puVar10 + 1;
        *(undefined4 *)(*(longlong *)(param_1 + 0x28) + -0x44 + (longlong)(puVar7 + 0x1c)) = uVar2;
        puVar7 = puVar7 + 0x1c;
        puVar10 = (undefined4 *)(ulonglong)uVar8;
      } while ((int)uVar8 < *(int *)(param_1 + 0x20));
      iVar6 = *(int *)(param_1 + 0x30);
    }
    uVar2 = puVar11[8];
    puVar7 = puVar9;
    puVar10 = puVar9;
    if (0 < iVar6) {
      do {
        uVar8 = (int)puVar10 + 1;
        *(undefined4 *)((longlong)puVar7 + *(longlong *)(param_1 + 0x38) + 0xa0) = uVar2;
        puVar7 = puVar7 + 0x2a;
        puVar10 = (undefined4 *)(ulonglong)uVar8;
      } while ((int)uVar8 < *(int *)(param_1 + 0x30));
    }
    *(undefined4 *)(param_1 + 0xf8) = uVar2;
    iVar6 = *(int *)(param_1 + 0x20);
    uVar2 = puVar11[6];
    puVar7 = puVar9;
    puVar10 = puVar9;
    if (0 < iVar6) {
      do {
        uVar8 = (int)puVar10 + 1;
        *(undefined4 *)(*(longlong *)(param_1 + 0x28) + -0xc + (longlong)(puVar7 + 0x1c)) = uVar2;
        iVar6 = *(int *)(param_1 + 0x20);
        puVar7 = puVar7 + 0x1c;
        puVar10 = (undefined4 *)(ulonglong)uVar8;
      } while ((int)uVar8 < iVar6);
    }
    if ((param_1[0x40] != '\0') && (puVar7 = puVar9, puVar10 = puVar9, 0 < *(int *)(param_1 + 0xa0))
       ) {
      do {
        uVar8 = (int)puVar10 + 1;
        *(undefined4 *)((longlong)puVar7 + *(longlong *)(param_1 + 0xa8) + 100) = uVar2;
        puVar7 = puVar7 + 0x1c;
        puVar10 = (undefined4 *)(ulonglong)uVar8;
      } while ((int)uVar8 < *(int *)(param_1 + 0xa0));
      iVar6 = *(int *)(param_1 + 0x20);
    }
    uVar2 = puVar11[7];
    puVar7 = puVar9;
    puVar11 = puVar9;
    if (0 < iVar6) {
      do {
        uVar8 = (int)puVar11 + 1;
        *(undefined4 *)(*(longlong *)(param_1 + 0x28) + -8 + (longlong)(puVar7 + 0x1c)) = uVar2;
        puVar7 = puVar7 + 0x1c;
        puVar11 = (undefined4 *)(ulonglong)uVar8;
      } while ((int)uVar8 < *(int *)(param_1 + 0x20));
    }
    if ((param_1[0x40] != '\0') && (puVar7 = puVar9, 0 < *(int *)(param_1 + 0xa0))) {
      do {
        uVar8 = (int)puVar7 + 1;
        *(undefined4 *)((longlong)puVar9 + *(longlong *)(param_1 + 0xa8) + 0x68) = uVar2;
        puVar9 = puVar9 + 0x1c;
        puVar7 = (undefined4 *)(ulonglong)uVar8;
      } while ((int)uVar8 < *(int *)(param_1 + 0xa0));
    }
    *param_1 = 1;
  }
  return;
}



// ===================================================
// 180076B00  ->  FUN_180076b00  (entree 180076b00)
// ===================================================

void FUN_180076b00(longlong param_1,undefined4 param_2)

{
  *(undefined4 *)(param_1 + 0x58) = param_2;
  return;
}



