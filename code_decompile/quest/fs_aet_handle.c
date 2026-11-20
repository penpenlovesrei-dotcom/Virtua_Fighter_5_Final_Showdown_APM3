// ===================================================
// 180029A90  ->  FUN_180029a90  (entree 180029a90)
// ===================================================

undefined4
FUN_180029a90(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined4 uVar1;
  longlong lVar2;
  undefined4 local_128 [72];
  
  FUN_180028e90(local_128,param_1,param_3,param_4,0xfffffffffffffffe);
  lVar2 = FUN_180024250(DAT_18066b738,local_128[0]);
  local_128[0] = *(undefined4 *)(lVar2 + 0x28);
  uVar1 = FUN_180026790(DAT_18066b750,local_128);
  FUN_180029140(local_128);
  return uVar1;
}



// ===================================================
// 180171070  ->  FUN_180171070  (entree 180171070)
// ===================================================

undefined4 FUN_180171070(longlong param_1,int param_2)

{
  char cVar1;
  undefined4 uVar2;
  
  uVar2 = 1;
  if (*(char *)(param_1 + 0x138) != '\0') {
    return 1;
  }
  if (*(int *)(param_1 + 0x5c + (longlong)param_2 * 4) != 0) {
    cVar1 = FUN_180029770();
    uVar2 = 1;
    if (cVar1 == '\0') {
      uVar2 = 0;
    }
  }
  return uVar2;
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



