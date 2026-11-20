// ===================================================
// 1800267B5  ->  FUN_180026790  (entree 180026790)
// ===================================================

undefined4 FUN_180026790(longlong param_1,undefined8 param_2)

{
  undefined8 *puVar1;
  char cVar2;
  longlong lVar3;
  undefined8 *puVar4;
  undefined8 *puVar5;
  undefined8 *puVar6;
  undefined4 uVar7;
  undefined1 local_470 [24];
  undefined1 local_458 [544];
  uint local_238 [2];
  undefined1 local_230 [552];
  
  FUN_180020cc0(local_458);
  cVar2 = FUN_180027900(param_1,local_458,param_2);
  if (cVar2 == '\0') {
    uVar7 = 0;
  }
  else {
    do {
      local_238[0] = *(int *)(param_1 + 0x88) + 1;
      *(uint *)(param_1 + 0x88) = local_238[0];
      puVar1 = *(undefined8 **)(param_1 + 0x68);
      cVar2 = *(char *)((longlong)puVar1[1] + 0x19);
      puVar6 = puVar1;
      puVar5 = (undefined8 *)puVar1[1];
      while (cVar2 == '\0') {
        if (*(uint *)(puVar5 + 4) < local_238[0]) {
          puVar4 = (undefined8 *)puVar5[2];
          puVar5 = puVar6;
        }
        else {
          puVar4 = (undefined8 *)*puVar5;
        }
        puVar6 = puVar5;
        puVar5 = puVar4;
        cVar2 = *(char *)((longlong)puVar4 + 0x19);
      }
      if ((puVar6 == puVar1) || (local_238[0] < *(uint *)(puVar6 + 4))) {
        puVar6 = puVar1;
      }
    } while ((puVar6 != puVar1) || (local_238[0] == 0));
    FUN_1800208b0(local_230,local_458);
    lVar3 = FUN_18001a7a0(param_1 + 0x68,local_238);
    FUN_18001bc00(param_1 + 0x68,local_470,0,lVar3 + 0x20,lVar3);
    FUN_180021420(local_230);
    uVar7 = *(undefined4 *)(param_1 + 0x88);
  }
  FUN_180021420(local_458);
  return uVar7;
}



