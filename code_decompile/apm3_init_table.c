// ===================================================
// 1801C5CE4  ->  FUN_1801c5cb0  (entree 1801c5cb0)
// ===================================================

void FUN_1801c5cb0(undefined8 *param_1)

{
  longlong lVar1;
  longlong lVar2;
  
  lVar1 = (longlong)param_1 + 0x1a;
  *param_1 = 0;
  lVar2 = 0x96;
  param_1[1] = 0;
  *(undefined4 *)(param_1 + 2) = 0;
  *(undefined1 *)((longlong)param_1 + 0x14) = 0;
  do {
    *(undefined1 *)(lVar1 + -2) = 0;
    *(undefined2 *)(lVar1 + -1) = 0;
    *(undefined1 *)(lVar1 + 2) = 0;
    *(undefined8 *)(lVar1 + 6) = 0;
    *(undefined8 *)(lVar1 + 0xe) = 0;
    *(undefined8 *)(lVar1 + 0x16) = 0;
    *(undefined8 *)(lVar1 + 0x1e) = 0;
    *(undefined8 *)(lVar1 + 0x26) = 0;
    *(undefined8 *)(lVar1 + 0x2e) = 0;
    *(undefined8 *)(lVar1 + 0x36) = 0;
    *(undefined8 *)(lVar1 + 0x3e) = 0;
    *(undefined8 *)(lVar1 + 0x46) = 0;
    *(undefined8 *)(lVar1 + 0x4e) = 0;
    *(undefined8 *)(lVar1 + 0x56) = 0;
    *(undefined8 *)(lVar1 + 0x5e) = 0;
    FUN_1802ff420(lVar1 + 0x66,0,(lVar1 - (lVar1 + 0x66)) + 0x7b);
    lVar1 = lVar1 + 0x80;
    lVar2 = lVar2 + -1;
  } while (lVar2 != 0);
  return;
}



