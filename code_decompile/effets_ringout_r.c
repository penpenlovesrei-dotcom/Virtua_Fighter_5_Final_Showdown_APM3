// ===================================================
// 84C5554  ->  FUN_084c5554  (entree 084c5554)
// ===================================================

void FUN_084c5554(int param_1,undefined4 param_2)

{
  FUN_084c52f4(param_1 + 0x50);
  FUN_084c5480(param_1 + 0x50,param_2);
  FUN_08055c96();
  return;
}



// ===================================================
// 84C5480  ->  FUN_084c5480  (entree 084c5480)
// ===================================================

void FUN_084c5480(int *param_1,int param_2)

{
  char cVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  char *pcVar5;
  undefined4 local_24;
  int local_20;
  int local_1c;
  
  iVar4 = 0;
  iVar2 = 0;
  while (*(int *)((int)&DAT_0883ac00 + iVar2) != param_2) {
    iVar4 = iVar4 + 1;
    iVar2 = iVar2 + 0x14;
    if (2 < iVar4) {
      return;
    }
  }
  if (iVar2 == -0x883ac00) {
    return;
  }
  local_20 = 0;
  if (*param_1 < 1) {
    return;
  }
  local_1c = 0;
  do {
    iVar4 = local_1c + param_1[1];
    *(undefined4 *)(iVar4 + 0x20) = *(undefined4 *)(&UNK_0883ac0c + iVar2);
    if (*(int *)(iVar4 + 8) == 0) {
      local_24 = *(undefined4 *)(&UNK_0883ac04 + iVar2);
      iVar3 = -1;
      pcVar5 = *(char **)(&UNK_0883ac10 + iVar2);
      do {
        if (iVar3 == 0) break;
        iVar3 = iVar3 + -1;
        cVar1 = *pcVar5;
        pcVar5 = pcVar5 + 1;
      } while (cVar1 != '\0');
      std::string::assign((char *)(iVar4 + 0x24),(uint)*(char **)(&UNK_0883ac10 + iVar2));
    }
    else {
      local_24 = *(undefined4 *)(&UNK_0883ac08 + iVar2);
    }
    FUN_084c4ba0(iVar4,local_24);
    local_20 = local_20 + 1;
    local_1c = local_1c + 0x28;
    if (*param_1 <= local_20) {
      return;
    }
  } while( true );
}



// ===================================================
// 84C52F4  ->  FUN_084c52f4  (entree 084c52f4)
// ===================================================

void FUN_084c52f4(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  int iVar3;
  undefined4 *puVar4;
  int iVar5;
  int iVar6;
  
  iVar6 = 5;
  FUN_084c51b0(param_1);
  *param_1 = 6;
  puVar2 = operator_new__(0xf4);
  puVar4 = puVar2 + 1;
  *puVar2 = 6;
  puVar2 = puVar4;
  do {
                    /* try { // try from 084c5345 to 084c5349 has its CatchHandler @ 084c5397 */
    FUN_084c526a(puVar2);
    puVar2 = puVar2 + 10;
    iVar6 = iVar6 + -1;
  } while (iVar6 != -1);
  param_1[1] = puVar4;
  iVar6 = 0;
  if (puVar4 == (undefined4 *)0x0) {
    *param_1 = 0;
  }
  else {
    while( true ) {
      iVar5 = 0;
      while( true ) {
        iVar3 = iVar6 * 3 + iVar5;
        iVar1 = iVar5 * 8;
        iVar5 = iVar5 + 1;
        FUN_084c5020(puVar4 + iVar3 * 10,iVar6,&DAT_0883ac3c + iVar1);
        if (2 < iVar5) break;
        puVar4 = (undefined4 *)param_1[1];
      }
      iVar6 = iVar6 + 1;
      if (1 < iVar6) break;
      puVar4 = (undefined4 *)param_1[1];
    }
  }
  return;
}



// ===================================================
// 84C4C44  ->  FUN_084c4c44  (entree 084c4c44)
// ===================================================

undefined4 FUN_084c4c44(int *param_1)

{
  char cVar1;
  int iVar2;
  int iVar3;
  
  iVar3 = 0;
  if (0 < *param_1) {
    iVar2 = 0;
    do {
      cVar1 = FUN_084c4c0e(param_1[1] + iVar2);
      if (cVar1 == '\0') {
        return 0;
      }
      iVar3 = iVar3 + 1;
      iVar2 = iVar2 + 0x28;
    } while (iVar3 < *param_1);
  }
  return 1;
}



// ===================================================
// 84C4C0E  ->  FUN_084c4c0e  (entree 084c4c0e)
// ===================================================

undefined1 FUN_084c4c0e(int param_1)

{
  char cVar1;
  undefined1 uVar2;
  
  cVar1 = FUN_08294494(param_1 + 0x10);
  if (cVar1 == '\0') {
    return 0;
  }
  uVar2 = FUN_08294526(param_1 + 0x10);
  return uVar2;
}



// ===================================================
// 84C4F7C  ->  FUN_084c4f7c  (entree 084c4f7c)
// ===================================================

undefined4 FUN_084c4f7c(int param_1)

{
  FUN_084c4f46(param_1 + 0x50);
  return 0;
}



// ===================================================
// 84C4B84  ->  FUN_084c4b84  (entree 084c4b84)
// ===================================================

void FUN_084c4b84(void)

{
  FUN_084c4b7a();
  return;
}



// ===================================================
// 84C4B92  ->  FUN_084c4b92  (entree 084c4b92)
// ===================================================

void FUN_084c4b92(void)

{
  FUN_084c4b44();
  return;
}



// ===================================================
// 84C4BA0  ->  FUN_084c4ba0  (entree 084c4ba0)
// ===================================================

void FUN_084c4ba0(int param_1,undefined4 param_2)

{
  int iVar1;
  char cVar2;
  undefined4 local_1c [4];
  
  iVar1 = param_1 + 0x10;
  FUN_082a3d10(iVar1);
  FUN_0829a0e4(local_1c,param_2);
  *(undefined4 *)(param_1 + 0x10) = local_1c[0];
  cVar2 = FUN_08294494(iVar1);
  if (cVar2 == '\0') {
    return;
  }
  FUN_082947ca(iVar1,0);
  FUN_0829786c(iVar1);
  return;
}



// ===================================================
// 84C4F46  ->  FUN_084c4f46  (entree 084c4f46)
// ===================================================

void FUN_084c4f46(int *param_1)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar3 = 0;
  if (0 < *param_1) {
    iVar2 = 0;
    do {
      iVar3 = iVar3 + 1;
      iVar1 = param_1[1] + iVar2;
      iVar2 = iVar2 + 0x28;
      FUN_084c4e30(iVar1);
    } while (iVar3 < *param_1);
  }
  return;
}



// ===================================================
// 84C4FFE  ->  FUN_084c4ffe  (entree 084c4ffe)
// ===================================================

void FUN_084c4ffe(int param_1)

{
  FUN_082a3d10(param_1 + 0x10);
  FUN_084c4f94();
  return;
}



// ===================================================
// 84C506C  ->  FUN_084c506c  (entree 084c506c)
// ===================================================

void FUN_084c506c(int param_1)

{
  allocator *paVar1;
  int iVar2;
  
                    /* try { // try from 084c5081 to 084c5085 has its CatchHandler @ 084c50a4 */
  FUN_084c4ffe(param_1);
  paVar1 = (allocator *)(*(int *)(param_1 + 0x24) + -0xc);
  if (paVar1 != (allocator *)&std::string::_Rep::_S_empty_rep_storage) {
                    /* try { // try from 084c50cd to 084c50d1 has its CatchHandler @ 084c50e4 */
    iVar2 = __gnu_cxx::__exchange_and_add((int *)(*(int *)(param_1 + 0x24) + -4),-1);
    if (iVar2 < 1) {
      std::string::_Rep::_M_destroy(paVar1);
    }
  }
  return;
}



