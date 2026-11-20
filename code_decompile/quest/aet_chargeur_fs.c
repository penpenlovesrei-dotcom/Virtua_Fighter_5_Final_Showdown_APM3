// ===================================================
// 180027600  ->  FUN_180027600  (entree 180027600)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_180027600(undefined8 param_1)

{
  longlong lVar1;
  undefined8 uVar2;
  undefined1 *puVar3;
  undefined1 local_30;
  undefined7 uStack_2f;
  longlong local_20;
  ulonglong uStack_18;
  
  local_20 = _DAT_1803478a0;
  uStack_18 = _UNK_1803478a8;
  local_30 = 0;
  FUN_180010a10(&local_30,"./rom/2d/",9);
  if (uStack_18 - local_20 < 10) {
    FUN_18000bff0(&local_30,10,0,"aet_db.bin",10);
  }
  else {
    puVar3 = &local_30;
    if (0xf < uStack_18) {
      puVar3 = (undefined1 *)CONCAT71(uStack_2f,local_30);
    }
    puVar3 = puVar3 + local_20;
    local_20 = local_20 + 10;
    FUN_180300010(puVar3,"aet_db.bin",10);
    puVar3[10] = 0;
  }
  puVar3 = &local_30;
  if (0xf < uStack_18) {
    puVar3 = (undefined1 *)CONCAT71(uStack_2f,local_30);
  }
  FUN_180217e70(param_1,puVar3,0);
  FUN_180218210(param_1);
  uVar2 = FUN_180217940(param_1);
  FUN_1800268a0(param_1,uVar2);
  FUN_180217900(param_1,1);
  if (0xf < uStack_18) {
    if (0xfff < uStack_18 + 1) {
      lVar1 = *(longlong *)(CONCAT71(uStack_2f,local_30) + -8);
      if (0x1f < (CONCAT71(uStack_2f,local_30) - lVar1) - 8U) {
                    /* WARNING: Subroutine does not return */
        FUN_180303af0(lVar1,uStack_18 + 0x28);
      }
    }
    FUN_1802fdd80();
  }
  return;
}



// ===================================================
// 180027740  ->  FUN_180027740  (entree 180027740)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_180027740(longlong param_1,int param_2,longlong param_3)

{
  undefined8 *puVar1;
  longlong lVar2;
  undefined8 *puVar3;
  undefined8 *puVar4;
  longlong *plVar5;
  undefined8 *puVar6;
  undefined1 *puVar7;
  ulonglong uVar8;
  undefined1 local_30;
  undefined7 uStack_2f;
  longlong local_20;
  ulonglong uStack_18;
  
  local_20 = _DAT_1803478a0;
  uStack_18 = _UNK_1803478a8;
  local_30 = 0;
  FUN_180010a10(&local_30,"./rom/2d/",9);
  uVar8 = 0xffffffffffffffff;
  do {
    uVar8 = uVar8 + 1;
  } while (*(char *)(param_3 + uVar8) != '\0');
  if (uStack_18 - local_20 < uVar8) {
    FUN_18000bff0(&local_30,uVar8,0,param_3,uVar8);
  }
  else {
    puVar7 = &local_30;
    if (0xf < uStack_18) {
      puVar7 = (undefined1 *)CONCAT71(uStack_2f,local_30);
    }
    puVar7 = puVar7 + local_20;
    local_20 = local_20 + uVar8;
    FUN_180300010(puVar7,param_3,uVar8);
    puVar7[uVar8] = 0;
  }
  puVar1 = *(undefined8 **)(param_1 + 0x58);
  puVar3 = (undefined8 *)puVar1[1];
  puVar6 = puVar1;
  if (*(char *)((longlong)puVar1[1] + 0x19) == '\0') {
    do {
      if (*(int *)(puVar3 + 4) < param_2) {
        puVar4 = (undefined8 *)puVar3[2];
      }
      else {
        puVar4 = (undefined8 *)*puVar3;
        puVar6 = puVar3;
      }
      puVar3 = puVar4;
    } while (*(char *)((longlong)puVar4 + 0x19) == '\0');
    if ((puVar6 != puVar1) && (*(int *)(puVar6 + 4) <= param_2)) goto LAB_180027834;
  }
  puVar6 = puVar1;
LAB_180027834:
  plVar5 = puVar6 + 5;
  if (puVar6 == puVar1) {
    plVar5 = (longlong *)0x0;
  }
  puVar7 = &local_30;
  if (0xf < uStack_18) {
    puVar7 = (undefined1 *)CONCAT71(uStack_2f,local_30);
  }
  (**(code **)(*plVar5 + 8))(plVar5,puVar7);
  if (0xf < uStack_18) {
    if (0xfff < uStack_18 + 1) {
      lVar2 = *(longlong *)(CONCAT71(uStack_2f,local_30) + -8);
      if (0x1f < (CONCAT71(uStack_2f,local_30) - lVar2) - 8U) {
                    /* WARNING: Subroutine does not return */
        FUN_180303af0(lVar2,uStack_18 + 0x28);
      }
    }
    FUN_1802fdd80();
  }
  return;
}



