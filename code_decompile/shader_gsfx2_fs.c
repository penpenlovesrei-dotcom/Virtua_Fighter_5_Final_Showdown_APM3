// ===================================================
// 180269750  ->  FUN_180269750  (entree 180269750)
// ===================================================

int * FUN_180269750(longlong param_1,longlong param_2,undefined8 param_3,undefined8 param_4)

{
  ulonglong *puVar1;
  char cVar2;
  longlong lVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  uint uVar7;
  int *piVar9;
  LPCRITICAL_SECTION lpCriticalSection;
  int *piVar10;
  int *piVar11;
  char local_60 [40];
  int *piVar8;
  
  piVar10 = (int *)0x0;
  uVar7 = 0;
  uVar4 = FUN_180264d00(DAT_180c4d590 + 0x1970,param_1,param_3,param_4,0xfffffffffffffffe);
  if (uVar4 == 0) {
    return (int *)0x0;
  }
  lpCriticalSection = (LPCRITICAL_SECTION)(DAT_180c4d590 + 0x19c0);
  EnterCriticalSection(lpCriticalSection);
  piVar8 = piVar10;
  do {
    cVar2 = *(char *)((longlong)piVar8 + param_1 + 0x12);
    if (cVar2 == '\0') break;
    local_60[(longlong)piVar8] = cVar2;
    uVar5 = (int)piVar8 + 1;
    piVar8 = (int *)(ulonglong)uVar5;
  } while (uVar5 < 0x1e);
  local_60[(longlong)piVar8] = '\0';
  uVar5 = uVar7;
  if (*(int *)(param_2 + 0x34) != 0) {
    uVar5 = FUN_180268030((ulonglong)*(uint *)(param_2 + 0x30) + param_2,local_60);
    uVar7 = 0;
    if (uVar5 == 0) {
      uVar7 = 0x80004005;
    }
  }
  piVar8 = piVar10;
  if (*(int *)(param_2 + 0x3c) != 0) {
    uVar6 = FUN_180268a10((ulonglong)*(uint *)(param_2 + 0x38) + param_2,local_60);
    piVar8 = (int *)(ulonglong)uVar6;
    if (uVar6 == 0) {
      uVar7 = 0x80004005;
    }
  }
  if ((((*(int *)(param_2 + 0x44) == 0) && (piVar9 = piVar10, *(int *)(param_2 + 0x4c) == 0)) ||
      (piVar9 = (int *)FUN_1802708e0(param_2,local_60), piVar9 != (int *)0x0)) && (-1 < (int)uVar7))
  {
    piVar10 = (int *)((ulonglong)(ushort)((ushort)piVar8 ^ (ushort)uVar5) ^ (ulonglong)piVar8 |
                      (ulonglong)(uVar4 & 0xffff) << 0x20 | (ulonglong)piVar9 & 0xffff000000000000);
    *(int **)(param_1 + 8) = piVar10;
    FUN_180269a20(DAT_180c4d590 + 0x16c8,param_1);
  }
  else {
    if (uVar5 != 0) {
      uVar7 = (uVar5 & 0xffff) - 1;
      piVar11 = piVar10;
      if (uVar7 < *(uint *)(DAT_180c4d590 + 0x18a4)) {
        piVar11 = *(int **)(*(longlong *)(DAT_180c4d590 + 0x1890) + (ulonglong)uVar7 * 8);
      }
      *piVar11 = *piVar11 + -1;
      if (*piVar11 == 0) {
        FUN_180267e10(piVar11);
        (**(code **)(**(longlong **)(DAT_180c4d590 + 0xb0) + 0x18))
                  (*(longlong **)(DAT_180c4d590 + 0xb0),piVar11);
      }
    }
    if ((uint)piVar8 != 0) {
      uVar7 = ((uint)piVar8 >> 0x10) - 1;
      piVar8 = piVar10;
      if (uVar7 < *(uint *)(DAT_180c4d590 + 0x18c4)) {
        piVar8 = *(int **)(*(longlong *)(DAT_180c4d590 + 0x18b0) + (ulonglong)uVar7 * 8);
      }
      *piVar8 = *piVar8 + -1;
      if (*piVar8 == 0) {
        FUN_180268830(piVar8);
        (**(code **)(**(longlong **)(DAT_180c4d590 + 0xb0) + 0x18))
                  (*(longlong **)(DAT_180c4d590 + 0xb0),piVar8);
      }
    }
    if (piVar9 != (int *)0x0) {
      uVar7 = ((ushort)((ulonglong)piVar9 >> 0x30) & 0x3fff) - 1;
      piVar8 = piVar10;
      if (uVar7 < *(uint *)(DAT_180c4d590 + 0x1964)) {
        piVar8 = *(int **)(*(longlong *)(DAT_180c4d590 + 0x1950) + (ulonglong)uVar7 * 8);
      }
      *piVar8 = *piVar8 + -1;
      if (*piVar8 == 0) {
        FUN_180270660(piVar8);
        (**(code **)(**(longlong **)(DAT_180c4d590 + 0xb0) + 0x18))
                  (*(longlong **)(DAT_180c4d590 + 0xb0),piVar8);
      }
    }
    lVar3 = DAT_180c4d590;
    uVar4 = uVar4 - 1;
    if (uVar4 < *(uint *)(DAT_180c4d590 + 0x1984)) {
      uVar7 = uVar4 >> 6;
      *(undefined8 *)(*(longlong *)(DAT_180c4d590 + 0x1970) + (ulonglong)uVar4 * 8) = 0;
      puVar1 = (ulonglong *)(*(longlong *)(lVar3 + 0x1978) + (ulonglong)uVar7 * 8);
      *puVar1 = *puVar1 | 1L << ((ulonglong)(0x3f - (uVar4 & 0x3f)) & 0x3f);
      if (uVar7 < *(uint *)(lVar3 + 0x1988)) {
        *(uint *)(lVar3 + 0x1988) = uVar7;
      }
    }
  }
  LeaveCriticalSection(lpCriticalSection);
  return piVar10;
}



// ===================================================
// 180269BD0  ->  FUN_180269bd0  (entree 180269bd0)
// ===================================================

longlong FUN_180269bd0(undefined8 *param_1,ushort *param_2)

{
  int iVar1;
  ulonglong *puVar2;
  uint uVar3;
  ulonglong uVar5;
  longlong *plVar6;
  ulonglong uVar7;
  longlong *plVar8;
  longlong *plVar9;
  longlong lVar10;
  longlong *plVar11;
  undefined8 local_98;
  longlong *plVar4;
  
  plVar8 = (longlong *)*param_1;
  plVar6 = (longlong *)0x0;
  plVar11 = plVar6;
  iVar1 = 0;
  do {
    plVar9 = plVar6;
    if (plVar8 == (longlong *)0x0) {
LAB_180269ce2:
      if (plVar9 != (longlong *)0x0) {
        return (longlong)*(short *)((longlong)plVar9 + 0xe) + (longlong)plVar9;
      }
      return 0;
    }
    puVar2 = (ulonglong *)((longlong)*(short *)((longlong)plVar8 + 0xe) + 0x10 + (longlong)plVar8);
    if ((uint)(ushort)*puVar2 == (uint)*param_2) {
      lVar10 = (longlong)param_2 - (longlong)puVar2;
      plVar4 = plVar6;
      while( true ) {
        uVar5 = *(ulonglong *)((longlong)puVar2 + lVar10);
        uVar7 = *puVar2;
        uVar5 = uVar5 >> 0x38 | (uVar5 & 0xff000000000000) >> 0x28 |
                (uVar5 & 0xff0000000000) >> 0x18 | (uVar5 & 0xff00000000) >> 8 |
                (uVar5 & 0xff000000) << 8 | (uVar5 & 0xff0000) << 0x18 | (uVar5 & 0xff00) << 0x28 |
                uVar5 << 0x38;
        uVar7 = uVar7 >> 0x38 | (uVar7 & 0xff000000000000) >> 0x28 |
                (uVar7 & 0xff0000000000) >> 0x18 | (uVar7 & 0xff00000000) >> 8 |
                (uVar7 & 0xff000000) << 8 | (uVar7 & 0xff0000) << 0x18 | (uVar7 & 0xff00) << 0x28 |
                uVar7 << 0x38;
        if (uVar5 < uVar7) break;
        if (uVar7 < uVar5) goto LAB_180269c9f;
        uVar3 = (int)plVar4 + 1;
        plVar4 = (longlong *)(ulonglong)uVar3;
        puVar2 = puVar2 + 1;
        plVar9 = plVar8;
        if (3 < uVar3) goto LAB_180269ce2;
      }
LAB_180269c75:
      (&local_98)[(longlong)plVar11] = (&local_98)[(longlong)plVar11] & 0xffff000000000000;
      (&local_98)[(longlong)plVar11] =
           (&local_98)[(longlong)plVar11] | (ulonglong)plVar8 & 0xffffffffffff;
      *(undefined2 *)((longlong)&local_98 + (longlong)plVar11 * 8 + 6) = 0;
      lVar10 = *plVar8;
    }
    else {
      if (0 < (int)((uint)(ushort)*puVar2 - (uint)*param_2)) goto LAB_180269c75;
LAB_180269c9f:
      (&local_98)[(longlong)plVar11] = (&local_98)[(longlong)plVar11] & 0xffff000000000000;
      (&local_98)[(longlong)plVar11] =
           (&local_98)[(longlong)plVar11] | (ulonglong)plVar8 & 0xffffffffffff;
      *(undefined2 *)((longlong)&local_98 + (longlong)plVar11 * 8 + 6) = 1;
      lVar10 = plVar8[1];
    }
    plVar11 = (longlong *)(ulonglong)(iVar1 + 1);
    plVar8 = (longlong *)((lVar10 << 0x10) >> 0x10);
    iVar1 = iVar1 + 1;
  } while( true );
}



// ===================================================
// 180270C50  ->  FUN_180270c50  (entree 180270c50)
// ===================================================

undefined8 FUN_180270c50(longlong param_1,uint *param_2)

{
  ulonglong *puVar1;
  short sVar2;
  int *piVar3;
  undefined8 uVar4;
  ulonglong uVar5;
  longlong lVar6;
  ushort uVar7;
  int iVar8;
  uint uVar9;
  uint uVar10;
  ulonglong *puVar11;
  undefined8 uVar12;
  ushort uVar13;
  uint uVar14;
  ulonglong *puVar15;
  ulonglong uVar16;
  undefined8 *local_a8;
  undefined4 local_a0;
  uint local_9c;
  undefined8 local_98;
  
  uVar16 = 0;
  iVar8 = FUN_180264d00(DAT_180c4d590 + 0x1950,param_1);
  if (iVar8 == 0) {
    return 0;
  }
  uVar10 = *param_2;
  uVar14 = (uVar10 & 0xffff) - 1;
  uVar9 = uVar10 >> 0x10;
  if ((uVar14 < *(uint *)(DAT_180c4d590 + 0x18e4)) &&
     (piVar3 = *(int **)(*(longlong *)(DAT_180c4d590 + 0x18d0) + (ulonglong)uVar14 * 8),
     uVar9 = uVar10 >> 0x10, piVar3 != (int *)0x0)) {
    *piVar3 = *piVar3 + 1;
    *(int **)(param_1 + 0x18) = piVar3;
    uVar9 = (uint)*(ushort *)((longlong)param_2 + 2);
  }
  if ((uVar9 - 1 < *(uint *)(DAT_180c4d590 + 0x1904)) &&
     (piVar3 = *(int **)(*(longlong *)(DAT_180c4d590 + 0x18f0) + (ulonglong)(uVar9 - 1) * 8),
     piVar3 != (int *)0x0)) {
    *piVar3 = *piVar3 + 1;
    *(int **)(param_1 + 0x20) = piVar3;
  }
  uVar10 = (ushort)param_2[1] - 1;
  if ((uVar10 < *(uint *)(DAT_180c4d590 + 0x1924)) &&
     (piVar3 = *(int **)(*(longlong *)(DAT_180c4d590 + 0x1910) + (ulonglong)uVar10 * 8),
     piVar3 != (int *)0x0)) {
    *piVar3 = *piVar3 + 1;
    *(int **)(param_1 + 0x28) = piVar3;
  }
  puVar1 = (ulonglong *)(param_1 + 0x30);
  *(undefined8 *)(param_1 + 0x10) = *(undefined8 *)param_2;
  uVar10 = *param_2;
  *(short *)(param_1 + 8) = (short)uVar10;
  sVar2 = *(short *)((longlong)param_2 + 2);
  *(short *)(param_1 + 10) = sVar2;
  *(short *)(param_1 + 0xc) = (short)param_2[1];
  uVar7 = (ushort)((short)uVar10 != 0);
  uVar13 = uVar7 | 2;
  if (sVar2 == 0) {
    uVar13 = uVar7;
  }
  *(ushort *)(param_1 + 0xe) = uVar13 << 0xe | (ushort)iVar8 & 0x3fff;
  lVar6 = DAT_180c4d590;
  uVar4 = *(undefined8 *)(param_1 + 8);
  *puVar1 = *puVar1 & 0xffff000000000000;
  *(ulonglong *)(param_1 + 0x38) = *(ulonglong *)(param_1 + 0x38) & 0xffff000000000000;
  *(undefined2 *)(param_1 + 0x36) = 0;
  *(short *)(param_1 + 0x3e) = (short)param_1 - (short)puVar1;
  if (*(ulonglong **)(lVar6 + 0x16c0) == (ulonglong *)0x0) {
    *(ulonglong **)(lVar6 + 0x16c0) = puVar1;
  }
  else {
    local_a8 = &local_98;
    local_9c = 0;
    local_a0 = 0x10;
    puVar15 = *(ulonglong **)(lVar6 + 0x16c0);
    uVar10 = local_9c;
    do {
      while (local_9c = uVar10, puVar11 = puVar15,
            uVar5 = *(ulonglong *)
                     ((longlong)*(short *)((longlong)puVar11 + 0xe) + 0x10 + (longlong)puVar11),
            uVar5 <= *(ulonglong *)(param_1 + 0x10)) {
        if (*(ulonglong *)(param_1 + 0x10) <= uVar5) {
          return uVar4;
        }
        local_a8[uVar16] = local_a8[uVar16] & 0xffff000000000000;
        local_a8[uVar16] = local_a8[uVar16] | (ulonglong)puVar11 & 0xffffffffffff;
        *(undefined2 *)((longlong)&local_98 + uVar16 * 8 + 6) = 1;
        uVar16 = (ulonglong)(local_9c + 1);
        uVar5 = puVar11[1];
        puVar15 = (ulonglong *)((longlong)(uVar5 << 0x10) >> 0x10);
        uVar10 = local_9c + 1;
        if (puVar15 == (ulonglong *)0x0) {
          puVar11[1] = ((ulonglong)puVar1 ^ uVar5) & 0xffffffffffff ^ uVar5;
          goto LAB_180270eb2;
        }
      }
      local_a8[uVar16] = local_a8[uVar16] & 0xffff000000000000;
      local_a8[uVar16] = local_a8[uVar16] | (ulonglong)puVar11 & 0xffffffffffff;
      *(undefined2 *)((longlong)&local_98 + uVar16 * 8 + 6) = 0;
      uVar16 = (ulonglong)(local_9c + 1);
      uVar5 = *puVar11;
      puVar15 = (ulonglong *)((longlong)(uVar5 << 0x10) >> 0x10);
      uVar10 = local_9c + 1;
    } while (puVar15 != (ulonglong *)0x0);
    *puVar11 = ((ulonglong)puVar1 ^ uVar5) & 0xffffffffffff ^ uVar5;
LAB_180270eb2:
    local_9c = local_9c + 1;
    uVar12 = FUN_180262650(lVar6 + 0x16c0,*(undefined8 *)(lVar6 + 0x16c0),&local_a8);
    *(undefined8 *)(lVar6 + 0x16c0) = uVar12;
  }
  return uVar4;
}



