// ===================================================
// 8230AF08  ->  FUN_8230af08  (entree 8230af08)
// ===================================================

void FUN_8230af08(int param_1,int param_2)

{
  undefined1 uVar1;
  undefined1 uVar2;
  
  uVar2 = *(undefined1 *)((param_2 + 10) * 8 + param_1);
  uVar1 = *(undefined1 *)(param_2 * 8 + param_1 + 0x51);
  switch(param_2) {
  case 0:
    FUN_82309310(param_1,1);
    return;
  case 1:
    FUN_82309408(param_1,uVar1);
    return;
  case 2:
  case 8:
  case 9:
  case 10:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x11:
  case 0x12:
  case 0x13:
  case 0x14:
  case 0x15:
    return;
  case 3:
    FUN_82309590();
    return;
  case 4:
    FUN_82309868();
    return;
  case 5:
    FUN_823096f0(param_1,uVar2,1);
    return;
  case 6:
    FUN_8230ab68();
    return;
  case 7:
    FUN_82309a00(param_1,0,uVar2,uVar1,5);
    return;
  case 0xb:
    FUN_82309c38();
    return;
  case 0xc:
    FUN_82309d58(param_1,0,uVar2,uVar1,6);
    return;
  case 0x10:
    FUN_8230ac50(param_1,1);
    return;
  case 0x16:
    FUN_8230a5c8(param_1,0xffffffffffffffff);
    return;
  default:
    return;
  }
}



// ===================================================
// 82308568  ->  FUN_82308568  (entree 82308568)
// ===================================================

undefined8 FUN_82308568(int param_1)

{
  int iVar1;
  undefined1 *puVar2;
  
  iVar1 = 0x19;
  puVar2 = (undefined1 *)(param_1 + 0x50);
  do {
    iVar1 = iVar1 + -1;
    *(undefined4 *)(puVar2 + -4) = 0;
    *puVar2 = 0;
    puVar2[1] = 0;
    puVar2 = puVar2 + 8;
  } while (iVar1 != 0);
  *(undefined4 *)(param_1 + 0x134) = 0;
  return 1;
}



// ===================================================
// 8230B488  ->  FUN_8230b488  (entree 8230b488)
// ===================================================

void FUN_8230b488(void)

{
  FUN_8230b008(0xffffffff82acb334);
  return;
}



// ===================================================
// 8230B4B0  ->  FUN_8230b4b0  (entree 8230b4b0)
// ===================================================

void FUN_8230b4b0(void)

{
  FUN_8230b108(0xffffffff82acb32c);
  return;
}



// ===================================================
// 8230B4C0  ->  FUN_8230b4c0  (entree 8230b4c0)
// ===================================================

void FUN_8230b4c0(void)

{
  FUN_8230b2f8(0xffffffff82acb32c);
  return;
}



// ===================================================
// 82166880  ->  FUN_82166880  (entree 82166880)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined4 * FUN_82166880(undefined4 *param_1,undefined4 *param_2)

{
  *param_1 = *param_2;
  param_1[1] = param_2[1];
  param_1[2] = param_2[2];
  param_1[3] = param_2[3];
  param_1[4] = param_2[4];
  param_1[5] = param_2[5];
  param_1[6] = param_2[6];
  param_1[7] = param_2[7];
  param_1[8] = param_2[8];
  param_1[9] = param_2[9];
  param_1[10] = param_2[10];
  param_1[0xb] = param_2[0xb];
  *(undefined1 *)(param_1 + 0xc) = *(undefined1 *)(param_2 + 0xc);
  param_1[0xd] = param_2[0xd];
  param_1[0xe] = param_2[0xe];
  param_1[0xf] = param_2[0xf];
  param_1[0x10] = param_2[0x10];
  param_1[0x11] = param_2[0x11];
  param_1[0x12] = param_2[0x12];
  param_1[0x13] = param_2[0x13];
  param_1[0x14] = param_2[0x14];
  param_1[0x15] = param_2[0x15];
  param_1[0x16] = param_2[0x16];
  param_1[0x17] = param_2[0x17];
  param_1[0x18] = param_2[0x18];
  param_1[0x19] = param_2[0x19];
  param_1[0x1a] = param_2[0x1a];
  param_1[0x1b] = param_2[0x1b];
  param_1[0x1c] = param_2[0x1c];
  param_1[0x1d] = param_2[0x1d];
  FUN_821d6240(param_1 + 0x1e);
  FUN_82160ee0(param_1 + 0x1e,param_2 + 0x1e);
  param_1[0x27] = 0xf;
  param_1[0x26] = 0;
  *(undefined1 *)(param_1 + 0x22) = 0;
  FUN_82141730(param_1 + 0x21,param_2 + 0x21,0,0xffffffffffffffff);
  return param_1;
}



// ===================================================
// 82166778  ->  FUN_82166778  (entree 82166778)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82166778(int param_1,char *param_2)

{
  char cVar1;
  char cVar2;
  uint uVar3;
  uint uVar4;
  undefined8 in_r0;
  undefined8 uVar5;
  char *pcVar6;
  char *pcVar7;
  uint uVar8;
  
  uVar3 = *(uint *)(param_1 + 4);
  uVar4 = *(uint *)(param_1 + 8);
  uVar8 = uVar3;
  if (uVar4 < uVar3) {
    trapWord(0x1f,in_r0,0x16);
  }
  do {
    if (uVar4 < uVar3) {
      trapWord(0x1f,in_r0,0x16);
    }
    if (param_1 == 0) {
      trapWord(0x1f,in_r0,0x16);
    }
    if (uVar8 == uVar4) {
      return 0;
    }
    if (param_1 == 0) {
      trapWord(0x1f,in_r0,0x16);
    }
    if (*(uint *)(param_1 + 8) <= uVar8) {
      trapWord(0x1f,in_r0,0x16);
    }
    pcVar7 = *(char **)(uVar8 + 0x68);
    pcVar6 = param_2;
    do {
      cVar1 = *pcVar7;
      cVar2 = *pcVar6;
      if (cVar1 == '\0') break;
      pcVar7 = pcVar7 + 1;
      pcVar6 = pcVar6 + 1;
    } while (cVar1 == cVar2);
    if (cVar1 == cVar2) {
      uVar5 = FUN_8215a480(0xffffffff826f8fa4);
      if (*(uint *)(param_1 + 8) <= uVar8) {
        trapWord(0x1f,in_r0,0x16);
      }
      FUN_82158778(uVar5,uVar8);
      return uVar5;
    }
    if (*(uint *)(param_1 + 8) <= uVar8) {
      trapWord(0x1f,in_r0,0x16);
    }
    uVar8 = uVar8 + 0x6c;
  } while( true );
}



// ===================================================
// 82166AD0  ->  FUN_82166ad0  (entree 82166ad0)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_82166ad0(double param_1,undefined8 param_2,undefined8 param_3,undefined4 param_4,
                 undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  int iVar1;
  undefined4 uStack_e0;
  undefined4 uStack_dc;
  undefined4 uStack_d8;
  float fStack_d0;
  undefined4 uStack_c8;
  undefined4 uStack_b8;
  
  FUN_82158008(&uStack_e0);
  iVar1 = FUN_8215d970(0xffffffff826f96e0,param_3);
  uStack_e0 = *(undefined4 *)(iVar1 + 0x20);
  fStack_d0 = (float)param_1;
  uStack_dc = param_4;
  uStack_d8 = param_7;
  uStack_c8 = param_5;
  uStack_b8 = param_6;
  FUN_821630e0(0xffffffff826f8fa4,param_2,&uStack_e0);
  FUN_82157f80(&uStack_e0);
  return;
}



// ===================================================
// 8215D0E0  ->  FUN_8215d0e0  (entree 8215d0e0)
// ===================================================

undefined8 FUN_8215d0e0(undefined8 param_1,undefined8 param_2)

{
  char cVar3;
  undefined8 uVar1;
  int *piVar2;
  
  cVar3 = FUN_822c80d0();
  if (cVar3 == '\0') {
    uVar1 = 1;
  }
  else {
    piVar2 = (int *)FUN_8215c9d0(param_1,param_2);
    if (piVar2 == (int *)0x0) {
      uVar1 = 0;
    }
    else {
      uVar1 = (**(code **)(*piVar2 + 0x48))();
    }
  }
  return uVar1;
}



