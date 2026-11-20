// ===================================================
// 180070DF0  ->  FUN_180070df0  (entree 180070df0)
// ===================================================

void FUN_180070df0(longlong *param_1,int param_2)

{
  char cVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  int iVar5;
  uint uVar6;
  undefined4 *puVar8;
  undefined4 *puVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  undefined1 local_res10 [8];
  undefined4 *puVar7;
  
  puVar8 = (undefined4 *)0x0;
  *(int *)((longlong)param_1 + 0x5c) = param_2;
  puVar2 = &DAT_1806430c0;
  if (param_2 != DAT_1806430c0) {
    puVar2 = puVar8;
  }
  puVar9 = &DAT_1806430d4;
  if (param_2 != DAT_1806430d4) {
    puVar9 = puVar2;
  }
  if (param_2 == DAT_1806430e8) {
    puVar9 = &DAT_1806430e8;
  }
  else if (puVar9 == (undefined4 *)0x0) {
    return;
  }
  (**(code **)(*param_1 + 0x58))(param_1,0);
  (**(code **)(*param_1 + 0x50))(param_1,*(undefined1 *)(puVar9 + 1));
  fVar12 = DAT_18034af44;
  fVar11 = DAT_18034a514;
  *(undefined4 *)(param_1 + 0xd) = 6;
  puVar2 = (undefined4 *)((longlong)param_1 + 0x8c);
  puVar4 = puVar8;
  do {
    iVar5 = (int)puVar4;
    if (0 < (int)param_1[0xd]) {
      fVar10 = (float)iVar5 * fVar12;
      puVar4 = puVar2;
      puVar7 = puVar8;
      do {
        puVar4[-7] = iVar5;
        puVar4[-6] = puVar9[2];
        puVar4[-5] = 0;
        puVar4[-4] = puVar9[4];
        *(undefined1 *)((longlong)puVar4 + -0x1f) = 1;
        *(undefined8 *)(puVar4 + -2) = 0;
        *puVar4 = 0;
        puVar3 = (undefined4 *)FUN_18003c370(local_res10,puVar9[3]);
        puVar4[-3] = *puVar3;
        cVar1 = FUN_180041a80(puVar4 + -3);
        if (cVar1 != '\0') {
          FUN_1800460d0(puVar4 + -3,0);
          FUN_180044830(puVar4 + -3);
        }
        *(undefined1 *)(puVar4 + -8) = 1;
        puVar4[-5] = (float)(int)puVar7 * fVar11 + fVar10;
        puVar4 = puVar4 + 9;
        uVar6 = (int)puVar7 + 1;
        puVar7 = (undefined4 *)(ulonglong)uVar6;
      } while ((int)uVar6 < (int)param_1[0xd]);
    }
    puVar4 = (undefined4 *)(ulonglong)(iVar5 + 1U);
    puVar2 = puVar2 + 0x36;
  } while ((int)(iVar5 + 1U) < 2);
  return;
}



// ===================================================
// 180071AF0  ->  FUN_180071af0  (entree 180071af0)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_180071af0(longlong param_1,int param_2)

{
  undefined8 uVar1;
  undefined4 *puVar2;
  
  _DAT_180677b08 = (undefined1 *)(param_1 + 0x58);
  *(undefined1 *)(param_1 + 0x60) = 1;
  *_DAT_180677b08 = 0;
  *(undefined4 *)(param_1 + 0x5c) = 0xffffffff;
  *(undefined8 *)(param_1 + 100) = 0;
  *(undefined8 *)(param_1 + 0x6c) = 0;
  *(undefined8 *)(param_1 + 0x74) = 0;
  *(undefined4 *)(param_1 + 0x8c) = 0x3f800000;
  *(undefined4 *)(param_1 + 0x90) = 0x3f800000;
  *(undefined4 *)(param_1 + 0x94) = 0x3f800000;
  *(undefined4 *)(param_1 + 0x98) = 0x3f800000;
  *(undefined8 *)(param_1 + 0x7c) = 0;
  *(undefined8 *)(param_1 + 0x84) = 0;
  puVar2 = &DAT_180643130;
  if (param_2 != DAT_180643130) {
    puVar2 = (undefined4 *)0x0;
  }
  if (param_2 == DAT_180643164) {
    puVar2 = &DAT_180643164;
  }
  else if (puVar2 == (undefined4 *)0x0) goto LAB_180071b91;
  *(int *)(param_1 + 0x5c) = param_2;
  *(undefined1 *)(param_1 + 0x60) = *(undefined1 *)(puVar2 + 1);
  *(undefined4 *)(param_1 + 0x70) = puVar2[10];
  *(undefined4 *)(param_1 + 0x74) = puVar2[0xb];
  *(undefined4 *)(param_1 + 0x78) = puVar2[0xc];
  uVar1 = *(undefined8 *)(puVar2 + 4);
  *(undefined8 *)(param_1 + 0x8c) = *(undefined8 *)(puVar2 + 2);
  *(undefined8 *)(param_1 + 0x94) = uVar1;
  uVar1 = *(undefined8 *)(puVar2 + 8);
  *(undefined8 *)(param_1 + 0x7c) = *(undefined8 *)(puVar2 + 6);
  *(undefined8 *)(param_1 + 0x84) = uVar1;
  *_DAT_180677b08 = 1;
LAB_180071b91:
  FUN_180040270("TaskEffectFogAnim::pre_init()\n");
  return;
}



// ===================================================
// 18007D1F0  ->  FUN_18007d1f0  (entree 18007d1f0)
// ===================================================

void FUN_18007d1f0(longlong *param_1,int param_2)

{
  int iVar1;
  
  if (DAT_1806f2168 != (undefined4 *)0x0) {
    (**(code **)(*param_1 + 0x18))();
  }
  DAT_1806f2168 = &DAT_180643340;
  iVar1 = DAT_180643340;
  while( true ) {
    if (iVar1 == -1) {
      DAT_1806f2168 = (undefined4 *)0x0;
      return;
    }
    if (param_2 == iVar1) break;
    iVar1 = DAT_1806f2168[0x16];
    DAT_1806f2168 = DAT_1806f2168 + 0x16;
  }
  if (DAT_1806f2198 == 0) {
    DAT_1806f2198 = FUN_180218410(0,(longlong)(int)DAT_1806f2168[3] << 6,"a_malloc",0x10);
  }
  if (DAT_1806f21a0 == 0) {
    DAT_1806f21a0 = FUN_180218410(0,0x30000,"a_malloc",0x10);
  }
  if (DAT_1806f21a8 == 0) {
    DAT_1806f21a8 = FUN_180218410(0,0x30000,"a_malloc",0x10);
  }
  FUN_180249fb0(1,&DAT_1806f218c);
  return;
}



// ===================================================
// 180081960  ->  FUN_180081960  (entree 180081960)
// ===================================================

void FUN_180081960(longlong *param_1,undefined4 param_2)

{
  (**(code **)(*param_1 + 0x58))(param_1,0);
  FUN_180080a10(param_1 + 0xc,param_2);
  DAT_1806f21c0 = param_1 + 0xc;
  FUN_180040270("TaskEffectSplash::pre_init()\n");
  return;
}



// ===================================================
// 180082610  ->  FUN_180082610  (entree 180082610)
// ===================================================

void FUN_180082610(longlong param_1,int param_2)

{
  undefined4 *puVar1;
  char cVar2;
  longlong lVar3;
  longlong lVar4;
  undefined4 *puVar5;
  undefined1 local_res10 [8];
  
  if (param_2 == 0xd) {
    puVar5 = &DAT_180351b98;
  }
  else {
    if (param_2 != 0x18) {
      return;
    }
    puVar5 = &DAT_180351bb8;
  }
  lVar3 = param_1 + 0x58;
  param_1 = param_1 - (longlong)puVar5;
  lVar4 = 7;
  do {
    puVar1 = (undefined4 *)FUN_18003c370(local_res10,*puVar5);
    *(undefined4 *)(param_1 + 0x58 + (longlong)puVar5) = *puVar1;
    cVar2 = FUN_180041a80(lVar3);
    if (cVar2 != '\0') {
      FUN_180044830(lVar3);
    }
    lVar3 = lVar3 + 4;
    puVar5 = puVar5 + 1;
    lVar4 = lVar4 + -1;
  } while (lVar4 != 0);
  return;
}



// ===================================================
// 1800770A0  ->  FUN_1800770a0  (entree 1800770a0)
// ===================================================

void FUN_1800770a0(longlong param_1,int param_2)

{
  int iVar1;
  char cVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  longlong lVar5;
  undefined4 *puVar6;
  undefined1 local_res10 [8];
  
  iVar1 = *(int *)(&DAT_180350820 + (longlong)param_2 * 4);
  *(int *)(param_1 + 0x58) = iVar1;
  if (iVar1 != -1) {
    lVar5 = 2;
    puVar4 = (undefined4 *)(param_1 + 0x5c);
    puVar6 = puVar4;
    do {
      puVar3 = (undefined4 *)FUN_18003c370(local_res10,*(undefined4 *)(param_1 + 0x58));
      *puVar6 = *puVar3;
      cVar2 = FUN_180041a80(puVar4);
      if (cVar2 != '\0') {
        FUN_1800460d0(puVar4,0);
        FUN_180044830(puVar4);
      }
      puVar4 = puVar4 + 1;
      puVar6 = puVar6 + 1;
      lVar5 = lVar5 + -1;
    } while (lVar5 != 0);
  }
  return;
}



// ===================================================
// 1800713E0  ->  FUN_1800713e0  (entree 1800713e0)
// ===================================================

void FUN_1800713e0(longlong param_1,int param_2)

{
  int iVar1;
  char cVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  longlong lVar5;
  undefined4 *puVar6;
  undefined1 local_res10 [8];
  
  iVar1 = *(int *)(&DAT_18034ff20 + (longlong)param_2 * 4);
  *(int *)(param_1 + 0x58) = iVar1;
  if (iVar1 != -1) {
    lVar5 = 2;
    puVar4 = (undefined4 *)(param_1 + 0x5c);
    puVar6 = puVar4;
    do {
      puVar3 = (undefined4 *)FUN_18003c370(local_res10,*(undefined4 *)(param_1 + 0x58));
      *puVar6 = *puVar3;
      cVar2 = FUN_180041a80(puVar4);
      if (cVar2 != '\0') {
        FUN_1800460d0(puVar4,0);
        FUN_180044830(puVar4);
      }
      puVar4 = puVar4 + 1;
      puVar6 = puVar6 + 1;
      lVar5 = lVar5 + -1;
    } while (lVar5 != 0);
  }
  return;
}



