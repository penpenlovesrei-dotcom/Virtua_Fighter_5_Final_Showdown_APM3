// ===================================================
// 18010BEF0  ->  FUN_18010bef0  (entree 18010bef0)
// ===================================================

longlong FUN_18010bef0(int param_1)

{
  return ((longlong)
          *(int *)(&DAT_1803a50e0 +
                  ((longlong)*(int *)(DAT_18070fc68 + 0x15c + (longlong)param_1 * 4) +
                  (longlong)param_1 * 3) * 4) + 7) * 0x38 + DAT_18070fc68;
}



// ===================================================
// 18024F2D0  ->  FUN_18024f2d0  (entree 18024f2d0)
// ===================================================

void FUN_18024f2d0(undefined4 param_1)

{
  longlong lVar1;
  
  lVar1 = FUN_180253c90();
  *(uint *)(lVar1 + 0xd8bd4) = *(uint *)(lVar1 + 0xd8bd4) | 2;
  *(undefined4 *)(lVar1 + 0xd9598) = param_1;
  return;
}



// ===================================================
// 180247230  ->  FUN_180247230  (entree 180247230)
// ===================================================

void FUN_180247230(undefined4 param_1,undefined4 param_2,int param_3)

{
  longlong lVar1;
  longlong lVar2;
  longlong lVar3;
  undefined8 uVar4;
  char cVar5;
  undefined4 uVar6;
  byte *pbVar7;
  
  lVar2 = FUN_180253c90();
  lVar1 = lVar2 + 0x757e0;
  if (0 < param_3) {
    lVar3 = FUN_180253c90();
    uVar6 = FUN_180245ea0(lVar1,param_1,param_3);
    pbVar7 = (byte *)FUN_1802498e0(lVar3 + 0x4a8,0x2a9);
    if (pbVar7 == (byte *)0x0) {
      cVar5 = FUN_180245f30(lVar1,lVar2 + 0x757e8,param_3);
      if (cVar5 == '\0') {
        return;
      }
      uVar4 = FUN_180246890(lVar1,lVar2 + 0x757e8);
      *(uint *)(lVar3 + 0xd8b14) = *(uint *)(lVar3 + 0xd8b14) | 4;
      *(undefined8 *)(lVar3 + 0xd8b30) = uVar4;
    }
    else if ((*pbVar7 & 0x10) == 0) {
      uVar4 = FUN_180246960(lVar1,lVar2 + 0x757e8);
      FUN_180250c50(lVar3 + 0xd7b50,uVar4);
    }
    FUN_180246750(lVar1,uVar6,param_2,param_3);
  }
  return;
}



// ===================================================
// 18024E900  ->  FUN_18024e900  (entree 18024e900)
// ===================================================

void FUN_18024e900(undefined4 param_1)

{
  longlong lVar1;
  
  lVar1 = FUN_180253c90();
  FUN_18024dd20(lVar1 + 0xd8bd0,param_1,1);
  return;
}



// ===================================================
// 1802573A0  ->  FUN_1802573a0  (entree 1802573a0)
// ===================================================

void FUN_1802573a0(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  longlong lVar1;
  undefined4 local_res18 [4];
  
  local_res18[0] = param_3;
  lVar1 = FUN_180253c90();
  FUN_180256600(lVar1 + 0xe3cc8,param_1,param_2,local_res18);
  return;
}



