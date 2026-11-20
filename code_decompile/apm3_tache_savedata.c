// ===================================================
// 1801B6AD0  ->  FUN_1801b6ad0  (entree 1801b6ad0)
// ===================================================

void FUN_1801b6ad0(longlong param_1)

{
  *(undefined8 *)(param_1 + 0x58) = 0xc;
  *(undefined8 *)(param_1 + 0x60) = 0;
  *(undefined2 *)(param_1 + 0x68) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined2 *)(param_1 + 0x78) = 0;
  FUN_180014990(param_1 + 0x80);
  *(undefined8 *)(param_1 + 0x90) = 0;
  if (*(longlong *)(param_1 + 0x98) != 0) {
    FUN_1802fdd80(*(longlong *)(param_1 + 0x98),0x16c0);
    *(undefined8 *)(param_1 + 0x98) = 0;
  }
  *(undefined8 *)(param_1 + 0xa0) = 0;
  *(undefined8 *)(param_1 + 0xa8) = 0;
  *(undefined8 *)(param_1 + 0xb0) = 0;
  *(undefined8 *)(param_1 + 0xb8) = 0;
  *(undefined8 *)(param_1 + 0xc0) = 0;
  *(undefined8 *)(param_1 + 200) = 0;
  *(undefined8 *)(param_1 + 0xd0) = 0;
  *(undefined8 *)(param_1 + 0xd8) = 0;
  *(undefined8 *)(param_1 + 0xe0) = 0;
  *(undefined8 *)(param_1 + 0xe8) = 0;
  *(undefined8 *)(param_1 + 0xf0) = 0;
  *(undefined8 *)(param_1 + 0xf8) = 0;
  *(undefined8 *)(param_1 + 0x100) = 0;
  *(undefined8 *)(param_1 + 0x108) = 0;
  *(undefined8 *)(param_1 + 0x110) = 0;
  *(undefined8 *)(param_1 + 0x118) = 0;
  *(undefined8 *)(param_1 + 0x120) = 0;
  *(undefined8 *)(param_1 + 0x128) = 0;
  *(undefined8 *)(param_1 + 0x130) = 0;
  *(undefined8 *)(param_1 + 0x138) = 0;
  *(undefined1 *)(param_1 + 0x140) = 0;
  return;
}



// ===================================================
// 1801B6E61  ->  FUN_1801b6e40  (entree 1801b6e40)
// ===================================================

undefined8 FUN_1801b6e40(void)

{
  char cVar1;
  
  if (((*(char *)(DAT_180752148 + 0x68c1) != '\0') && (cVar1 = FUN_180029fb0(0,0), cVar1 != '\0'))
     && (cVar1 = FUN_180244ea0(&DAT_180752000), cVar1 == '\0')) {
    if ((*(char *)(DAT_180752148 + 0x68c4) != '\0') && (cVar1 = FUN_180029fb0(0,0), cVar1 == '\0'))
    {
      return 0;
    }
    cVar1 = FUN_180007450();
    if (cVar1 != '\0') {
      return 1;
    }
  }
  return 0;
}



// ===================================================
// 1801B7014  ->  FUN_1801b7010  (entree 1801b7010)
// ===================================================

bool FUN_1801b7010(void)

{
  char cVar1;
  
  cVar1 = FUN_180244ea0(&DAT_180752000);
  return cVar1 == '\0';
}



