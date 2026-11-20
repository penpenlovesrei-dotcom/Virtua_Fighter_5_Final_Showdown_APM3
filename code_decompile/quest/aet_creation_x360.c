// ===================================================
// 82308640  ->  FUN_82308640  (entree 82308640)
// ===================================================

undefined8 FUN_82308640(int param_1,int param_2)

{
  undefined8 uVar1;
  
  if (*(int *)(param_2 * 8 + param_1 + 0x4c) != 0) {
    uVar1 = FUN_821665e8();
    return uVar1;
  }
  return 1;
}



// ===================================================
// 82166CC0  ->  FUN_82166cc0  (entree 82166cc0)
// ===================================================

undefined8 FUN_82166cc0(undefined8 param_1)

{
  int iVar2;
  undefined8 uVar1;
  undefined4 auStack_b0 [40];
  
  FUN_82166880(auStack_b0,param_1);
  iVar2 = FUN_8215d970(0xffffffff826f96e0,auStack_b0[0]);
  auStack_b0[0] = *(undefined4 *)(iVar2 + 0x20);
  uVar1 = FUN_82165590(0xffffffff826f8fa4,auStack_b0);
  FUN_82157f80(auStack_b0);
  return uVar1;
}



// ===================================================
// 82158008  ->  FUN_82158008  (entree 82158008)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined4 * FUN_82158008(undefined4 *param_1)

{
  float fVar1;
  undefined4 uVar2;
  double dVar3;
  
  fVar1 = DAT_82000a34;
  dVar3 = (double)DAT_82000a34;
  param_1[0xd] = DAT_82000a34;
  param_1[0xe] = fVar1;
  param_1[0xf] = fVar1;
  param_1[0x10] = fVar1;
  param_1[0x11] = fVar1;
  param_1[0x12] = fVar1;
  param_1[0x13] = fVar1;
  param_1[0x14] = fVar1;
  param_1[0x15] = fVar1;
  param_1[0x16] = fVar1;
  param_1[0x17] = fVar1;
  param_1[0x18] = fVar1;
  param_1[0x1a] = fVar1;
  param_1[0x1b] = fVar1;
  param_1[0x1c] = fVar1;
  param_1[0x1d] = fVar1;
  FUN_821d6240(param_1 + 0x1e);
  param_1[0x26] = 0;
  param_1[0x27] = 0xf;
  *(undefined1 *)(param_1 + 0x22) = 0;
  uVar2 = DAT_82001968;
  param_1[4] = DAT_82001968;
  param_1[9] = 3;
  param_1[5] = uVar2;
  param_1[10] = 9;
  uVar2 = DAT_82000b08;
  *param_1 = 0xffffffff;
  param_1[7] = 0xffffffff;
  param_1[0xd] = (float)dVar3;
  param_1[0xe] = (float)dVar3;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[0x19] = uVar2;
  param_1[6] = 0;
  param_1[8] = 0;
  param_1[0xf] = (float)dVar3;
  param_1[0x10] = (float)dVar3;
  param_1[0x11] = (float)dVar3;
  param_1[0x12] = (float)dVar3;
  param_1[0x13] = uVar2;
  param_1[0x14] = uVar2;
  param_1[0x15] = uVar2;
  param_1[0x16] = (float)dVar3;
  param_1[0x17] = (float)dVar3;
  param_1[0x18] = (float)dVar3;
  param_1[0x1a] = uVar2;
  param_1[0x1b] = uVar2;
  param_1[0x1c] = uVar2;
  param_1[0x1d] = uVar2;
  uVar2 = FUN_822c2a28();
  param_1[0xb] = uVar2;
  *(undefined1 *)(param_1 + 0xc) = 1;
  return param_1;
}



// ===================================================
// 822F6768  ->  FUN_822f6768  (entree 822f6768)
// ===================================================

/* WARNING: Function: __savegprlr_24 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_24 replaced with injection: x360_restgprlr */

void FUN_822f6768(int *param_1,undefined4 param_2,undefined4 param_3,undefined4 *param_4,
                 undefined4 param_5,undefined4 param_6,undefined4 param_7,undefined4 param_8)

{
  int iVar1;
  undefined4 uStack_f0;
  undefined4 uStack_ec;
  undefined4 uStack_e8;
  undefined4 uStack_e4;
  undefined4 uStack_d8;
  undefined4 uStack_d4;
  undefined4 uStack_cc;
  undefined4 uStack_c4;
  undefined4 uStack_bc;
  undefined4 uStack_b8;
  undefined4 uStack_b4;
  
  FUN_82158008(&uStack_f0);
  uStack_bc = *param_4;
  uStack_b8 = param_4[1];
  uStack_b4 = param_4[2];
  uStack_f0 = param_2;
  uStack_ec = param_3;
  uStack_e8 = param_7;
  uStack_e4 = param_8;
  uStack_d8 = param_6;
  uStack_cc = param_5;
  if (*param_1 != 0) {
    FUN_821664c0();
    *param_1 = 0;
  }
  uStack_d4 = 2;
  uStack_c4 = 9;
  iVar1 = FUN_82166cc0(&uStack_f0);
  *param_1 = iVar1;
  FUN_82157f80(&uStack_f0);
  return;
}



// ===================================================
// 82144B30  ->  FUN_82144b30  (entree 82144b30)
// ===================================================

undefined1 FUN_82144b30(void)

{
  return DAT_826f06ae;
}



// ===================================================
// 823163A0  ->  FUN_823163a0  (entree 823163a0)
// ===================================================

bool FUN_823163a0(uint param_1)

{
  return (1 << (param_1 & 0x3f) & DAT_82656b34) != 0;
}



// ===================================================
// 82316390  ->  FUN_82316390  (entree 82316390)
// ===================================================

void FUN_82316390(undefined8 param_1)

{
  FUN_82315960(0xffffffff82656b08,param_1);
  return;
}



// ===================================================
// 821665E8  ->  FUN_821665e8  (entree 821665e8)
// ===================================================

void FUN_821665e8(undefined8 param_1)

{
  FUN_8215d0e0(0xffffffff826f8fa4,param_1);
  return;
}



// ===================================================
// 82166540  ->  FUN_82166540  (entree 82166540)
// ===================================================

void FUN_82166540(undefined8 param_1,undefined8 param_2)

{
  FUN_8215ce00(0xffffffff826f8fa4,param_1,param_2);
  return;
}



// ===================================================
// 82166570  ->  FUN_82166570  (entree 82166570)
// ===================================================

void FUN_82166570(undefined8 param_1)

{
  FUN_8215ce90(0xffffffff826f8fa4,param_1);
  return;
}



