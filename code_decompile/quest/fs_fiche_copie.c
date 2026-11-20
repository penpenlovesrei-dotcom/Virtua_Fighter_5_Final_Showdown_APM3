// ===================================================
// 1800B3340  ->  FUN_1800b3340  (entree 1800b3340)
// ===================================================

void FUN_1800b3340(longlong param_1,int param_2,undefined8 param_3,undefined8 param_4)

{
  longlong lVar1;
  longlong lVar2;
  undefined8 uVar3;
  char cVar4;
  uint uVar5;
  ulonglong uVar6;
  longlong lVar7;
  longlong lVar8;
  
  uVar3 = DAT_18070fb10;
  lVar8 = (longlong)param_2;
  lVar7 = lVar8 * 0x5a0;
  lVar1 = lVar7 + param_1;
  FUN_180101840(DAT_18070fb10,lVar1 + 0x68,param_2,param_4,0xfffffffffffffffe);
  *(bool *)(lVar1 + 0x68) = *(int *)(param_1 + 0x34 + lVar8 * 4) == 1;
  *(undefined2 *)(lVar7 + 0x6b + param_1) = 0;
  lVar2 = lVar8 * 0x240 + param_1;
  FUN_180101880(uVar3,lVar2 + 0xba8,param_2);
  FUN_18010ea40(param_2,1);
  cVar4 = *(char *)(lVar1 + 0x68);
  if (((cVar4 == '\0') && (*(char *)(lVar7 + 0x5cb + param_1) == '\0')) &&
     (*(int *)(lVar2 + 0xbb0) == 0)) {
    if (*(int *)(param_1 + 8) == 0) {
      uVar5 = *(uint *)(param_1 + 0xc);
      uVar6 = (ulonglong)uVar5;
      if (uVar5 == 0) {
        uVar5 = 2;
      }
      else {
        if (uVar5 != 1) goto LAB_1800b342c;
        uVar5 = 1;
      }
    }
    else {
      if (*(int *)(param_1 + 8) != 1) goto LAB_1800b342c;
      uVar5 = 4;
      uVar6 = 0;
    }
    FUN_18010ea40(param_2,CONCAT71((int7)(uVar6 >> 8),(*(uint *)(lVar2 + 0xc00) & uVar5) != 0));
    cVar4 = *(char *)(lVar1 + 0x68);
  }
LAB_1800b342c:
  if ((cVar4 == '\0') &&
     (uVar5 = (uint)*(byte *)(*(int *)(param_1 + 0x24 + lVar8 * 4) + lVar7 + 0x2c8 + param_1),
     *(uint *)(param_1 + 0x1c + lVar8 * 4) != uVar5)) {
    *(uint *)(param_1 + 0x1c + lVar8 * 4) = uVar5;
  }
  return;
}



// ===================================================
// 1800ACD40  ->  FUN_1800acd40  (entree 1800acd40)
// ===================================================

undefined4 FUN_1800acd40(uint param_1,uint param_2)

{
  undefined4 uVar1;
  
  uVar1 = 0x15;
  if ((((DAT_1806f9c10 != 0) && (param_1 < 3)) && (param_2 < 8)) &&
     (*(char *)(DAT_1806f9c10 + 0x9c) != '\0')) {
    uVar1 = *(undefined4 *)
             (*(longlong *)(DAT_1806f9c10 + 0xb8) +
             ((ulonglong)param_2 + (longlong)(int)param_1 * 8) * 4);
  }
  return uVar1;
}



// ===================================================
// 1800B4600  ->  FUN_1800b4600  (entree 1800b4600)
// ===================================================

undefined4 FUN_1800b4600(longlong param_1)

{
  return *(undefined4 *)(param_1 + 0xc);
}



