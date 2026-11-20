// ===================================================
// 180245EA0  ->  FUN_180245ea0  (entree 180245ea0)
// ===================================================

undefined8 FUN_180245ea0(undefined8 param_1,undefined4 param_2,int param_3)

{
  undefined8 uVar1;
  
  switch(param_2) {
  case 2:
    return 1;
  case 3:
    return 2;
  default:
    return 4;
  case 5:
    return 3;
  case 7:
    return 5;
  case 8:
    return 0xe;
  case 9:
    return 0xf;
  case 0xb:
    break;
  }
  uVar1 = 0xf;
  if (param_3 != 4) {
    uVar1 = 4;
  }
  return uVar1;
}



// ===================================================
// 180246750  ->  FUN_180246750  (entree 180246750)
// ===================================================

void FUN_180246750(undefined8 param_1,int param_2,undefined4 param_3,ulonglong param_4)

{
  longlong lVar1;
  longlong lVar2;
  undefined8 uVar3;
  longlong *plVar4;
  longlong lVar5;
  int iVar6;
  
  uVar3 = FUN_180253c90();
  FUN_180253c60(uVar3);
  plVar4 = (longlong *)FUN_180253c90();
  lVar1 = *plVar4;
  if (param_2 - 0xeU < 2) {
    lVar5 = 0x1480;
    if (param_2 == 0xf) {
      lVar5 = 0x1478;
    }
    lVar5 = *(longlong *)(lVar5 + DAT_180c4d590);
    lVar2 = *(longlong *)(lVar5 + 0x10);
    if ((*(longlong *)(lVar1 + 0xf98) != lVar2) || (*(int *)(lVar1 + 4000) != 0)) {
      *(longlong *)(lVar1 + 0xf98) = lVar2;
      *(undefined4 *)(lVar1 + 4000) = 0;
      (**(code **)(**(longlong **)(lVar1 + 0x18) + 0x98))
                (*(longlong **)(lVar1 + 0x18),*(undefined8 *)(*(longlong *)(lVar5 + 0x18) + 0x10),
                 0x39);
    }
    if (*(int *)(lVar1 + 0xe74) != 4) {
      *(undefined4 *)(lVar1 + 0xe74) = 4;
      (**(code **)(**(longlong **)(lVar1 + 0x18) + 0xc0))(*(longlong **)(lVar1 + 0x18),4);
    }
    if (param_2 == 0xf) {
      iVar6 = ((uint)(param_4 >> 1) & 0x7fffffff) + (int)param_4;
    }
    else {
      iVar6 = ((int)param_4 + -2) * 3;
    }
    FUN_18025ceb0(lVar1);
    (**(code **)(**(longlong **)(lVar1 + 0x18) + 0x60))
              (*(longlong **)(lVar1 + 0x18),iVar6,0,param_3);
  }
  else {
    if (*(int *)(lVar1 + 0xe74) != param_2) {
      *(int *)(lVar1 + 0xe74) = param_2;
      (**(code **)(**(longlong **)(lVar1 + 0x18) + 0xc0))(*(longlong **)(lVar1 + 0x18),param_2);
    }
    FUN_18025ceb0(lVar1);
    (**(code **)(**(longlong **)(lVar1 + 0x18) + 0x68))
              (*(longlong **)(lVar1 + 0x18),param_4 & 0xffffffff,param_3);
  }
  return;
}



