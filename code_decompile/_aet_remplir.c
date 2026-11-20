// ===================================================
// 180027900  ->  FUN_180027900  (entree 180027900)
// ===================================================

undefined8 FUN_180027900(longlong param_1,longlong *param_2,uint *param_3)

{
  undefined8 *puVar1;
  undefined8 *puVar2;
  longlong lVar3;
  undefined8 *puVar4;
  undefined8 *puVar5;
  undefined8 *puVar6;
  int iVar7;
  undefined8 *puVar8;
  uint uVar9;
  undefined1 local_58 [12];
  int local_4c;
  int local_48;
  
  puVar8 = *(undefined8 **)(param_1 + 0x58);
  uVar9 = (int)*param_3 >> 0x10 & 0xffff;
  puVar1 = (undefined8 *)puVar8[1];
  puVar4 = puVar8;
  if (*(char *)((longlong)puVar8[1] + 0x19) == '\0') {
    do {
      if (*(int *)(puVar1 + 4) < (int)uVar9) {
        puVar2 = (undefined8 *)puVar1[2];
      }
      else {
        puVar2 = (undefined8 *)*puVar1;
        puVar4 = puVar1;
      }
      puVar1 = puVar2;
    } while (*(char *)((longlong)puVar2 + 0x19) == '\0');
    if ((puVar4 != puVar8) && (*(int *)(puVar4 + 4) <= (int)uVar9)) goto LAB_180027957;
  }
  puVar4 = puVar8;
LAB_180027957:
  puVar2 = (undefined8 *)0x0;
  puVar1 = puVar4 + 5;
  if (puVar4 == puVar8) {
    puVar1 = puVar2;
  }
  if ((((puVar1 != (undefined8 *)0x0) && (*(uint *)(puVar1 + 1) == uVar9)) &&
      (*(char *)(puVar1 + 0x16) != '\0')) &&
     (uVar9 = *param_3 & 0xffff, (int)uVar9 < *(int *)(puVar1 + 3))) {
    iVar7 = *(int *)(puVar1[2] + (ulonglong)uVar9 * 4);
    puVar8 = puVar2;
    if (iVar7 != 0) {
      puVar8 = (undefined8 *)(puVar1[2] + (ulonglong)uVar9 * 4 + (longlong)iVar7);
    }
    if (((((puVar8 != (undefined8 *)0x0) && (lVar3 = FUN_180028590(puVar8), lVar3 != 0)) &&
         ((puVar4 = puVar2, *(longlong *)(param_3 + 2) == 0 ||
          (puVar4 = (undefined8 *)FUN_1800244e0(puVar1,puVar8), puVar4 != (undefined8 *)0x0)))) &&
        ((puVar5 = puVar2, *(longlong *)(param_3 + 4) == 0 ||
         (puVar5 = (undefined8 *)FUN_180024630(puVar1,puVar4), puVar5 != (undefined8 *)0x0)))) &&
       ((puVar6 = puVar2, *(longlong *)(param_3 + 6) == 0 ||
        (puVar6 = (undefined8 *)FUN_180024630(puVar1,puVar4), puVar6 != (undefined8 *)0x0)))) {
      do {
        FUN_18016aec0(local_58,puVar2);
        if ((*(int *)((longlong)puVar8 + 0x14) == local_4c) &&
           (iVar7 = (int)puVar2, *(int *)(puVar8 + 3) == local_48)) break;
        uVar9 = (int)puVar2 + 1;
        puVar2 = (undefined8 *)(ulonglong)uVar9;
        iVar7 = 9;
      } while ((int)uVar9 < 0x11);
      (**(code **)(*param_2 + 8))(param_2,param_3,puVar8,lVar3,puVar4,puVar5,puVar6,iVar7);
      return 1;
    }
  }
  return 0;
}



