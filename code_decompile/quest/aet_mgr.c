// ===================================================
// 180024430  ->  FUN_180024430  (entree 180024430)
// ===================================================

undefined8 FUN_180024430(longlong param_1,uint param_2)

{
  undefined8 *puVar1;
  char cVar2;
  undefined8 *puVar3;
  undefined8 *puVar4;
  undefined8 *puVar5;
  longlong *plVar6;
  undefined8 uVar7;
  
  cVar2 = FUN_180244ea0();
  if (cVar2 == '\0') {
    return 0;
  }
  puVar1 = *(undefined8 **)(param_1 + 0x68);
  puVar3 = (undefined8 *)puVar1[1];
  puVar5 = puVar1;
  if (*(char *)((longlong)puVar1[1] + 0x19) == '\0') {
    do {
      if (*(uint *)(puVar3 + 4) < param_2) {
        puVar4 = (undefined8 *)puVar3[2];
      }
      else {
        puVar4 = (undefined8 *)*puVar3;
        puVar5 = puVar3;
      }
      puVar3 = puVar4;
    } while (*(char *)((longlong)puVar4 + 0x19) == '\0');
    if ((puVar5 != puVar1) && (*(uint *)(puVar5 + 4) <= param_2)) goto LAB_180024484;
  }
  puVar5 = puVar1;
LAB_180024484:
  plVar6 = puVar5 + 5;
  if (puVar5 == puVar1) {
    plVar6 = (longlong *)0x0;
  }
  if (plVar6 == (longlong *)0x0) {
    return 0;
  }
                    /* WARNING: Could not recover jumptable at 0x0001800244a6. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  uVar7 = (**(code **)(*plVar6 + 0x90))(plVar6);
  return uVar7;
}



// ===================================================
// 180024600  ->  FUN_180024600  (entree 180024600)
// ===================================================

longlong FUN_180024600(longlong param_1)

{
  uint uVar1;
  uint uVar2;
  
  uVar1 = *(uint *)(param_1 + 0x810);
  uVar2 = uVar1 + 1;
  if (0xf < uVar2) {
    uVar2 = 0;
  }
  *(uint *)(param_1 + 0x810) = uVar2;
  return (ulonglong)uVar1 * 0x78 + 0x90 + param_1;
}



// ===================================================
// 180024970  ->  FUN_180024970  (entree 180024970)
// ===================================================

void FUN_180024970(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined8 uVar1;
  undefined **local_238 [68];
  undefined8 local_18;
  
  uVar1 = 0xfffffffffffffffe;
  FUN_180020cc0(local_238);
  local_238[0] = AetLyo::vftable;
  local_18 = param_2;
  FUN_180027900(param_1,local_238,param_3,param_4,uVar1);
  FUN_180023650(local_238);
  local_238[0] = AetLyo::vftable;
  FUN_180021420(local_238);
  return;
}



// ===================================================
// 1800272E0  ->  FUN_1800272e0  (entree 1800272e0)
// ===================================================

void FUN_1800272e0(longlong param_1,uint param_2)

{
  longlong *plVar1;
  undefined8 *puVar2;
  longlong *plVar3;
  longlong lVar4;
  undefined8 *puVar5;
  undefined8 *puVar6;
  longlong *plVar7;
  undefined8 uVar8;
  longlong *plVar9;
  undefined8 *puVar10;
  longlong *plVar11;
  longlong *plVar12;
  undefined8 *local_res8;
  
  puVar2 = *(undefined8 **)(param_1 + 0x68);
  puVar5 = (undefined8 *)puVar2[1];
  puVar10 = puVar2;
  if (*(char *)((longlong)puVar2[1] + 0x19) == '\0') {
    do {
      if (*(uint *)(puVar5 + 4) < param_2) {
        puVar6 = (undefined8 *)puVar5[2];
      }
      else {
        puVar6 = (undefined8 *)*puVar5;
        puVar10 = puVar5;
      }
      puVar5 = puVar6;
    } while (*(char *)((longlong)puVar6 + 0x19) == '\0');
    if ((puVar10 != puVar2) && (*(uint *)(puVar10 + 4) <= param_2)) goto LAB_18002731b;
  }
  puVar10 = puVar2;
LAB_18002731b:
  if (puVar10 != puVar2) {
    plVar9 = *(longlong **)(param_1 + 0x78);
    plVar1 = (longlong *)(param_1 + 0x78);
    plVar7 = (longlong *)*plVar9;
    plVar11 = plVar9;
    plVar12 = plVar9;
    local_res8 = puVar10;
    if (plVar7 != plVar9) {
      do {
        plVar3 = (longlong *)*plVar7;
        plVar12 = plVar11;
        if (((undefined8 *)plVar7[2] == puVar10) &&
           (plVar12 = plVar7, (undefined8 **)(plVar7 + 2) != &local_res8)) {
          *(longlong **)plVar7[1] = plVar3;
          *(longlong *)(*plVar7 + 8) = plVar7[1];
          *(longlong *)(param_1 + 0x80) = *(longlong *)(param_1 + 0x80) + -1;
          FUN_1802fdd80(plVar7,0x18);
          plVar12 = plVar11;
        }
        plVar9 = (longlong *)*plVar1;
        plVar7 = plVar3;
        plVar11 = plVar12;
      } while (plVar3 != plVar9);
    }
    if (plVar12 != plVar9) {
      *(longlong *)plVar12[1] = *plVar12;
      *(longlong *)(*plVar12 + 8) = plVar12[1];
      *(longlong *)(param_1 + 0x80) = *(longlong *)(param_1 + 0x80) + -1;
      FUN_1802fdd80(plVar12,0x18);
    }
    lVar4 = *plVar1;
    puVar2 = *(undefined8 **)(lVar4 + 8);
    uVar8 = FUN_18001a770(plVar1,lVar4,puVar2,&local_res8);
    if (*(longlong *)(param_1 + 0x80) == 0xaaaaaaaaaaaaaa9) {
                    /* WARNING: Subroutine does not return */
      FUN_1802fbd0c("list<T> too long");
    }
    *(longlong *)(param_1 + 0x80) = *(longlong *)(param_1 + 0x80) + 1;
    *(undefined8 *)(lVar4 + 8) = uVar8;
    *puVar2 = uVar8;
  }
  return;
}



