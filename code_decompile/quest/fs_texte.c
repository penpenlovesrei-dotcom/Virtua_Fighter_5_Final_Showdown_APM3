// ===================================================
// 1801BD131  ->  FUN_1801bd120  (entree 1801bd120)
// ===================================================

undefined8 FUN_1801bd120(longlong param_1)

{
  *(undefined1 *)(param_1 + 0x124) = 1;
  *(undefined8 *)(param_1 + 0xc0) = 0;
  *(undefined8 *)(param_1 + 0x198) = 0;
  *(undefined4 *)(param_1 + 0x1f8) = 0x13;
  *(undefined2 *)(param_1 + 0x1fc) = 0x101;
  *(undefined1 *)(param_1 + 0x125) = *(undefined1 *)(param_1 + 0x210);
  *(undefined4 *)(param_1 + 0x120) = *(undefined4 *)(param_1 + 0x214);
  FUN_180245830(param_1 + 0x68,"MENU_EXPLAIN");
  *(undefined1 *)(param_1 + 0x1fd) = *(undefined1 *)(param_1 + 0x211);
  *(undefined4 *)(param_1 + 0x1f8) = *(undefined4 *)(param_1 + 0x218);
  FUN_180245830(param_1 + 0x140,"MENU_CONTROL");
  *(undefined4 *)(param_1 + 0x224) = 0;
  *(undefined4 *)(param_1 + 0x22c) = 0;
  *(undefined1 *)(param_1 + 0x60) = 0;
  *(undefined1 *)(param_1 + 0x231) = 1;
  return 1;
}



