// ===================================================
// 822E3A48  ->  FUN_822e39c0  (entree 822e39c0)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

void FUN_822e39c0(int param_1,undefined4 *param_2,undefined8 param_3,char param_4)

{
  char cVar2;
  int iVar1;
  int iVar3;
  
  iVar1 = *(int *)(param_1 + 4);
  if (iVar1 != 0x38) {
    if (iVar1 == 0xb) {
      iVar1 = 10;
    }
    if (param_4 != '\0') {
      FUN_82158a20(param_1 + 0x1c);
    }
    if ((*(int *)(param_1 + 0x20) == 0) ||
       (iVar3 = *(int *)(param_1 + 0x24) - *(int *)(param_1 + 0x20),
       iVar3 = iVar3 / 0x6c + (iVar3 >> 0x1f), iVar3 == iVar3 >> 0x1f)) {
      iVar3 = *(int *)(&DAT_82085700 + iVar1 * 8);
      cVar2 = FUN_82144b30();
      if ((cVar2 == '\0') && (iVar3 == 0x416)) {
        iVar3 = 0x424;
      }
      FUN_821665d8(*(undefined4 *)(param_1 + 0x18));
      FUN_82166ad0(param_1 + 0x1c,iVar3,(&PTR_s_cmn_win_s_01_82085704)[iVar1 * 2],0,9,0);
    }
    iVar1 = FUN_82166778(param_1 + 0x1c,param_3);
    if ((iVar1 != 0) && (param_2 != (undefined4 *)0x0)) {
      *param_2 = *(undefined4 *)(iVar1 + 0x40);
      param_2[1] = *(undefined4 *)(iVar1 + 0x44);
      param_2[2] = *(undefined4 *)(iVar1 + 0x48);
    }
  }
  return;
}



// ===================================================
// 822E4CB8  ->  FUN_822e4bf0  (entree 822e4bf0)
// ===================================================

void FUN_822e4bf0(int param_1,ulonglong param_2)

{
  int iVar1;
  char cVar3;
  undefined4 uVar2;
  char *apcStack_f0 [5];
  char *pcStack_dc;
  char *pcStack_d8;
  char *pcStack_d4;
  int aiStack_d0 [5];
  undefined *puStack_bc;
  undefined4 uStack_b8;
  undefined4 uStack_b4;
  undefined4 uStack_a8;
  undefined4 uStack_a4;
  undefined4 uStack_9c;
  undefined4 uStack_94;
  undefined4 uStack_5c;
  
  apcStack_f0[0] = s_sta_s_82084c28;
  pcStack_dc = s_end_e_82084c00;
  pcStack_d8 = s_end_e_82084c00;
  apcStack_f0[1] = s_sta_e_82084c20;
  apcStack_f0[2] = s_neu_s_82084c18;
  aiStack_d0[1] = 0x10000;
  apcStack_f0[3] = s_neu_e_82084c10;
  apcStack_f0[4] = s_end_s_82084c08;
  pcStack_d4 = s_end_s_82084c08;
  aiStack_d0[0] = 0x20000;
  aiStack_d0[2] = 0x20000;
  aiStack_d0[3] = 0x20000;
  if (*(int *)(param_1 + 0x18) != 0) {
    FUN_821664c0();
  }
  FUN_82158008(aiStack_d0 + 4);
  uStack_9c = *(undefined4 *)(param_1 + 8);
  uStack_5c = *(undefined4 *)(param_1 + 0x14);
  iVar1 = (int)((param_2 & 0xffffffff) << 3);
  uStack_a8 = *(undefined4 *)((int)aiStack_d0 + (int)((param_2 & 0xffffffff) << 2));
  uStack_b8 = *(undefined4 *)((int)apcStack_f0 + iVar1);
  aiStack_d0[4] = *(int *)(&DAT_82085700 + *(int *)(param_1 + 4) * 8);
  uStack_a4 = 2;
  puStack_bc = (&PTR_s_cmn_win_s_01_82085704)[*(int *)(param_1 + 4) * 2];
  uStack_b4 = *(undefined4 *)((int)apcStack_f0 + iVar1 + 4);
  uStack_94 = 9;
  cVar3 = FUN_82144b30();
  if ((cVar3 == '\0') && (aiStack_d0[4] == 0x416)) {
    aiStack_d0[4] = 0x424;
  }
  uVar2 = FUN_82166cc0(aiStack_d0 + 4);
  *(undefined4 *)(param_1 + 0x18) = uVar2;
  if (((int)param_2 == 0) && (*(char *)(param_1 + 0xd) != '\0')) {
    FUN_822b3ac0(0xffffffff82085ae8);
  }
  FUN_82157f80(aiStack_d0 + 4);
  return;
}



// ===================================================
// 822E3AD8  ->  FUN_822e3ad8  (entree 822e3ad8)
// ===================================================

undefined8 FUN_822e3ad8(undefined4 *param_1)

{
  undefined8 in_r0;
  undefined4 *local_18;
  uint uStack_14;
  
  local_18 = param_1 + 7;
  param_1[5] = DAT_82000b08;
  *(undefined1 *)(param_1 + 3) = 1;
  param_1[1] = 0x38;
  param_1[2] = 8;
  *(undefined1 *)((int)param_1 + 0xd) = 1;
  *param_1 = 0;
  param_1[4] = 0;
  param_1[6] = 0;
  uStack_14 = param_1[8];
  if ((uint)param_1[9] < uStack_14) {
    trapWord(0x1f,in_r0,0x16);
    trapWord(0x1f,in_r0,0x16);
  }
  FUN_821589a0(&local_18,local_18,CONCAT44(local_18,uStack_14),CONCAT44(local_18,param_1[9]));
  return 1;
}



// ===================================================
// 821DC9B8  ->  FUN_821dc9b8  (entree 821dc9b8)
// ===================================================

void FUN_821dc9b8(int param_1,undefined4 param_2)

{
  *(undefined4 *)(param_1 + 8) = param_2;
  return;
}



