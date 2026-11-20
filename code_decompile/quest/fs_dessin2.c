// ===================================================
// 18019B330  ->  FUN_18019b330  (entree 18019b330)
// ===================================================

int FUN_18019b330(undefined8 param_1,undefined4 param_2)

{
  int iVar1;
  longlong lVar2;
  ulonglong uVar3;
  undefined1 local_808 [1024];
  undefined1 local_408 [1024];
  
  iVar1 = FUN_180017310(local_808,0x400);
  uVar3 = (ulonglong)iVar1;
  if (0x400 < uVar3) {
    uVar3 = 0x400;
  }
  lVar2 = FUN_180019d10(local_408,local_808,0x200,uVar3);
  if (lVar2 != -1) {
    FUN_18019ac70(param_1,param_2,local_408,lVar2);
  }
  return iVar1;
}



