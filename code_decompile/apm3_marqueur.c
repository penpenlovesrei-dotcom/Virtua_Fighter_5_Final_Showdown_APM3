// ===================================================
// 1801B9D40  ->  FUN_1801b9d40  (entree 1801b9d40)
// ===================================================

void FUN_1801b9d40(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined1 *puVar3;
  undefined1 *puVar4;
  undefined4 local_28;
  undefined1 local_24 [2];
  undefined1 local_22 [26];
  
  iVar2 = 0;
  local_28 = 0;
  FUN_1801a3090(local_24);
  FUN_1801a23a0(local_22,0);
  do {
    if (iVar2 == param_1) {
      puVar4 = (undefined1 *)(DAT_180752148 + 0x5028);
      puVar3 = (undefined1 *)(DAT_180752148 + 0x502a);
      uVar1 = *(undefined4 *)(DAT_180752148 + 0x5024);
    }
    else {
      puVar4 = local_24;
      puVar3 = local_22;
      uVar1 = local_28;
    }
    FUN_1801a3180(iVar2,uVar1,puVar3,puVar4);
    iVar2 = iVar2 + 1;
  } while (iVar2 < 2);
  *(undefined1 *)(DAT_180752148 + 0x68c0) = 0;
  return;
}



// ===================================================
// 1801B69B0  ->  FUN_1801b69b0  (entree 1801b69b0)
// ===================================================

void FUN_1801b69b0(char param_1,undefined1 param_2)

{
  undefined8 *puVar1;
  ulonglong uVar2;
  ulonglong uVar3;
  
  uVar2 = 0;
  uVar3 = uVar2;
  do {
    FUN_1801a3180(uVar3 & 0xffffffff,*(undefined4 *)(uVar2 + 0x5024 + (longlong)DAT_180752148),
                  (longlong)DAT_180752148 + uVar2 + 0x502a,(longlong)DAT_180752148 + uVar2 + 0x5028)
    ;
    uVar3 = uVar3 + 1;
    uVar2 = uVar2 + 0x18;
  } while (uVar2 < 0x30);
  FUN_1801b8ff0();
  puVar1 = DAT_180752148;
  if (param_1 == '\0') {
    *(undefined4 *)(DAT_180752148 + 0xa04) = 0;
  }
  else {
    *(undefined1 *)((longlong)DAT_180752148 + 0x671c) = param_2;
    *puVar1 = 0;
    *(undefined4 *)(puVar1 + 1) = 0;
  }
  *(char *)((longlong)puVar1 + 0x671d) = param_1;
  FUN_1801b7c20();
  return;
}



