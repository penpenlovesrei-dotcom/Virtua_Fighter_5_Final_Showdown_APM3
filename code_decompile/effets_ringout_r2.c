// ===================================================
// 84C4E30  ->  FUN_084c4e30  (entree 084c4e30)
// ===================================================

void FUN_084c4e30(undefined4 *param_1)

{
  char cVar1;
  undefined4 uVar2;
  int iVar3;
  undefined1 local_40 [4];
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  
  local_2c = 0;
  local_28 = 0;
  local_24 = 0;
  local_3c = 0;
  local_38 = 0;
  local_34 = 0;
  if (param_1[1] == 0) {
    uVar2 = FUN_081f582c();
    iVar3 = FUN_081f67d8(uVar2,*param_1);
    if (iVar3 != 0) {
      iVar3 = FUN_082141c2(iVar3,param_1[3]);
      if (iVar3 != 0) {
        local_28 = *(undefined4 *)(iVar3 + 0x1c);
        local_2c = *(undefined4 *)(iVar3 + 0xc);
        local_24 = *(undefined4 *)(iVar3 + 0x2c);
        uVar2 = FUN_081f582c();
        cVar1 = FUN_081f6524(uVar2,*param_1);
        if (cVar1 != '\0') {
          iVar3 = FUN_0817293c(&local_3c,local_40,&local_2c,param_1 + 5,0x3dcccccd,0x2000);
          if (iVar3 != -1) {
            cVar1 = FUN_0810bf60();
            uVar2 = 0x3f4ccccd;
            if (cVar1 != '\0') {
              uVar2 = DAT_0876456c;
            }
            FUN_084c4d20(param_1,&local_3c,uVar2);
            param_1[1] = 1;
          }
        }
        param_1[5] = local_2c;
        param_1[6] = local_28;
        param_1[7] = local_24;
        return;
      }
    }
  }
  return;
}



// ===================================================
// 84C5020  ->  FUN_084c5020  (entree 084c5020)
// ===================================================

void FUN_084c5020(undefined4 *param_1,undefined4 param_2,undefined4 *param_3)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  FUN_084c4ffe(param_1);
  uVar1 = *param_3;
  uVar2 = param_3[1];
  *param_1 = param_2;
  param_1[2] = uVar1;
  param_1[1] = 0;
  param_1[3] = uVar2;
  param_1[5] = 0;
  param_1[6] = 0;
  param_1[7] = 0;
  return;
}



// ===================================================
// 84C4D20  ->  FUN_084c4d20  (entree 084c4d20)
// ===================================================

void FUN_084c4d20(int param_1,undefined4 *param_2,undefined4 param_3)

{
  char cVar1;
  int iVar2;
  undefined1 *puVar3;
  undefined1 local_5c [76];
  
  iVar2 = param_1 + 0x10;
  cVar1 = FUN_08294494(iVar2);
  if ((cVar1 != '\0') && (param_2 != (undefined4 *)0x0)) {
    FUN_0809ad5a(local_5c);
    FUN_0809e236(local_5c);
    FUN_0809f278(local_5c,*param_2,param_2[1],param_2[2]);
    FUN_0809ee78(local_5c,param_3,param_3,param_3);
    FUN_08294b54(iVar2,local_5c);
    FUN_082947ca(iVar2,1);
    FUN_0829473a(iVar2,0);
    FUN_08294852(iVar2,0);
    FUN_08294acc(iVar2,1);
    FUN_08294574(iVar2,0);
    puVar3 = &DAT_087667ff;
    iVar2 = std::string::compare((char *)(param_1 + 0x24));
    if (iVar2 != 0) {
      FUN_081dfe3e(*(undefined4 *)(param_1 + 0x24),puVar3);
    }
  }
  return;
}



