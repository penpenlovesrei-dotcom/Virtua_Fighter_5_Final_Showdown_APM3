// ===================================================
// 8230CB00  ->  FUN_8230cb00  (entree 8230cb00)
// ===================================================

undefined8 FUN_8230cb00(undefined8 param_1,ulonglong param_2)

{
  FUN_8230c998();
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 8230B7D0  ->  FUN_8230b7d0  (entree 8230b7d0)
// ===================================================

undefined8 FUN_8230b7d0(int param_1)

{
  char cVar1;
  
  *(undefined4 *)(param_1 + 0x54) = 0;
  *(undefined4 *)(param_1 + 0x50) = 0;
  *(undefined4 *)(param_1 + 0x4c) = 0;
  *(undefined4 *)(param_1 + 0x58) = 0;
  FUN_822e3ad8(param_1 + 0x238);
  FUN_821dc9b8(param_1 + 0x238,6);
  FUN_822e2f20(param_1 + 0x60);
  FUN_822c8aa0(param_1 + 0x60,0xffffffff8208e084);
  FUN_822e2e98(param_1 + 0xe4);
  FUN_822c8aa0(param_1 + 0xe4,0xffffffff8208e070);
  cVar1 = FUN_822b1638(0);
  if (cVar1 == '\0') {
    FUN_822b1540(0,0xffffffff8208e054);
  }
  return 1;
}



// ===================================================
// 8230C8A0  ->  FUN_8230c8a0  (entree 8230c8a0)
// ===================================================

undefined8 FUN_8230c8a0(int param_1)

{
  if (*(int *)(param_1 + 0x4c) != *(int *)(param_1 + 0x50)) {
    *(int *)(param_1 + 0x54) = *(int *)(param_1 + 0x4c);
    *(int *)(param_1 + 0x4c) = *(int *)(param_1 + 0x50);
    *(undefined4 *)(param_1 + 0x58) = 0;
  }
  switch(*(undefined4 *)(param_1 + 0x4c)) {
  case 0:
    FUN_8230c3a8(param_1);
    break;
  case 1:
    FUN_8230b8e0(param_1);
    break;
  case 2:
    FUN_8230bac8(param_1);
    break;
  case 3:
    FUN_8230bb68(param_1);
    break;
  case 4:
    FUN_8230bc08(param_1);
    break;
  case 5:
    FUN_8230bcc0(param_1);
    break;
  case 6:
    FUN_8230bdb8(param_1);
    break;
  case 7:
    FUN_8230c6d8(param_1);
  }
  FUN_822e4d70(param_1 + 0x238);
  return 0;
}



