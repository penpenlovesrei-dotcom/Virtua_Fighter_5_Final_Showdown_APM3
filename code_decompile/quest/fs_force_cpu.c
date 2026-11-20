// ===================================================
// 1800ACD80  ->  FUN_1800acd80  (entree 1800acd80)
// ===================================================

undefined4 FUN_1800acd80(uint param_1,uint param_2)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if ((((DAT_1806f9c10 != 0) && (param_1 < 5)) && (param_2 < 8)) &&
     (uVar1 = 0, *(char *)(DAT_1806f9c10 + 0x9c) != '\0')) {
    uVar1 = *(undefined4 *)
             (*(longlong *)(DAT_1806f9c10 + 0xd0) +
             ((ulonglong)param_2 + (ulonglong)param_1 * 8) * 4);
  }
  return uVar1;
}



// ===================================================
// 18010ED40  ->  FUN_18010ed40  (entree 18010ed40)
// ===================================================

void FUN_18010ed40(int param_1,undefined2 param_2,int param_3)

{
  int iVar1;
  longlong lVar2;
  undefined *puVar3;
  
  puVar3 = &DAT_1803a55b0;
  iVar1 = 10;
  do {
    if (iVar1 == param_3) break;
    iVar1 = *(int *)(puVar3 + 8);
    puVar3 = puVar3 + 8;
  } while (iVar1 != 0x15);
  if (iVar1 != 0x15) {
    lVar2 = (longlong)param_1 * 0x1d28 + DAT_18070fc78;
    iVar1 = *(int *)(puVar3 + 4);
    FUN_180120510(lVar2);
    FUN_18010e540(lVar2);
    *(undefined2 *)(lVar2 + 0x1cf8) = param_2;
    *(undefined4 *)(lVar2 + 0x3c) = 0;
    *(undefined4 *)(lVar2 + 0x50) = 0;
    *(undefined4 *)(lVar2 + 0x58) = 1;
    *(undefined1 *)(lVar2 + 0x5e) = 0;
    if (-1 < iVar1) {
      FUN_18011d190(1,lVar2,iVar1);
    }
  }
  return;
}



