// ===================================================
// 82308480  ->  FUN_82308480  (entree 82308480)
// ===================================================

undefined8 FUN_82308480(void)

{
  return 0xffffffff82acb1f0;
}



// ===================================================
// 82309310  ->  FUN_82309310  (entree 82309310)
// ===================================================

void FUN_82309310(int param_1,int param_2)

{
  char cVar2;
  undefined4 uVar1;
  char *apcStack_d0 [4];
  int iStack_c0;
  undefined *puStack_bc;
  char *pcStack_b8;
  char *pcStack_b4;
  undefined4 uStack_a8;
  undefined4 uStack_a4;
  undefined4 uStack_9c;
  undefined4 uStack_94;
  
  if (*(int *)(param_1 + 0x4c) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0x4c) = 0;
  }
  apcStack_d0[0] = s_sta_s_82084c28;
  apcStack_d0[1] = s_sta_e_82084c20;
  apcStack_d0[2] = s_sta_e_82084c20;
  apcStack_d0[3] = s_sta_e_82084c20;
  FUN_82158008(&iStack_c0);
  cVar2 = FUN_82144b30();
  puStack_bc = &DAT_8208dce4;
  iStack_c0 = (-(uint)(cVar2 != '\0') & 0xfffffff2) + 0x426;
  uStack_9c = 8;
  uStack_a8 = 0x20000;
  uStack_a4 = 2;
  uStack_94 = 9;
  pcStack_b8 = apcStack_d0[param_2 * 2];
  pcStack_b4 = apcStack_d0[param_2 * 2 + 1];
  uVar1 = FUN_82166cc0(&iStack_c0);
  *(char *)(param_1 + 0x51) = (char)param_2;
  *(undefined4 *)(param_1 + 0x4c) = uVar1;
  FUN_82157f80(&iStack_c0);
  return;
}



// ===================================================
// 82309868  ->  FUN_82309868  (entree 82309868)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_82309868(int param_1,int param_2,ulonglong param_3)

{
  int iVar1;
  char cVar3;
  undefined4 uVar2;
  char *apcStack_140 [5];
  char *pcStack_12c;
  undefined4 auStack_128 [6];
  char *apcStack_110 [4];
  char *pcStack_100;
  char *pcStack_fc;
  char *pcStack_f8;
  char *pcStack_f4;
  char *pcStack_f0;
  int iStack_e0;
  char *pcStack_dc;
  undefined4 uStack_d8;
  undefined4 uStack_d4;
  undefined4 uStack_c8;
  undefined4 uStack_c4;
  undefined4 uStack_bc;
  undefined4 uStack_b4;
  
  if (*(int *)(param_1 + 0x6c) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0x6c) = 0;
  }
  if ((param_2 == 7) && (cVar3 = FUN_823163a0(0xe), cVar3 != '\0')) {
    param_2 = 8;
  }
  apcStack_110[0] = s_zoom_swn_8208de20;
  apcStack_110[1] = s_zoom_sws_8208de14;
  apcStack_110[2] = s_zoom_swr_8208de08;
  apcStack_110[3] = s_zoom_csd_8208ddfc;
  pcStack_100 = s_zoom_csb_8208ddf0;
  pcStack_fc = s_zoom_sac_8208dde4;
  pcStack_f8 = s_zoom_sae_8208ddd8;
  pcStack_f4 = s_zoom_dom_01_8208ddcc;
  auStack_128[1] = 2;
  pcStack_f0 = s_zoom_dom_02_8208ddc0;
  apcStack_140[0] = s_sta_s_82084c28;
  pcStack_12c = s_sta_s_82084c28;
  apcStack_140[1] = s_sta_e_82084c20;
  apcStack_140[2] = s_sta_e_82084c20;
  apcStack_140[3] = s_sta_e_82084c20;
  apcStack_140[4] = s_sta_e_82084c20;
  auStack_128[0] = 7;
  auStack_128[2] = 7;
  FUN_82158008(&iStack_e0);
  cVar3 = FUN_82144b30();
  uStack_c4 = 2;
  iVar1 = (int)((param_3 & 0xffffffff) << 3);
  pcStack_dc = apcStack_110[param_2];
  uStack_bc = *(undefined4 *)((int)auStack_128 + (int)((param_3 & 0xffffffff) << 2));
  iStack_e0 = (-(uint)(cVar3 != '\0') & 0xfffffff2) + 0x426;
  uStack_c8 = 0x20000;
  uStack_b4 = 9;
  uStack_d8 = *(undefined4 *)((int)apcStack_140 + iVar1);
  uStack_d4 = *(undefined4 *)((int)apcStack_140 + iVar1 + 4);
  uVar2 = FUN_82166cc0(&iStack_e0);
  *(char *)(param_1 + 0x70) = (char)param_2;
  *(char *)(param_1 + 0x71) = (char)param_3;
  *(undefined4 *)(param_1 + 0x6c) = uVar2;
  FUN_82157f80(&iStack_e0);
  return;
}



// ===================================================
// 8230A5C8  ->  FUN_8230a5c8  (entree 8230a5c8)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_8230a5c8(int param_1,int param_2)

{
  char cVar1;
  int *piVar2;
  int iStack_d0;
  char *pcStack_cc;
  undefined4 uStack_b8;
  undefined4 uStack_ac;
  undefined1 uStack_a0;
  
  piVar2 = (int *)(param_1 + 0xfc);
  if (*(int *)(param_1 + 0xfc) == 0) {
    if (*piVar2 != 0) {
      FUN_821664c0();
      *piVar2 = 0;
    }
    FUN_82158008(&iStack_d0);
    cVar1 = FUN_82144b30();
    uStack_a0 = 0;
    pcStack_cc = s_map_aero_8208df68;
    iStack_d0 = (-(uint)(cVar1 != '\0') & 0xfffffff2) + 0x426;
    uStack_b8 = 0x10000;
    uStack_ac = 4;
    FUN_82308ac0(piVar2,&iStack_d0);
    if (-1 < param_2) {
      *(int *)(param_1 + 0x134) = param_2;
    }
    FUN_82157f80(&iStack_d0);
  }
  return;
}



// ===================================================
// 823085A0  ->  FUN_823085a0  (entree 823085a0)
// ===================================================

void FUN_823085a0(int param_1,int param_2)

{
  undefined8 uVar1;
  
  if (param_2 == 0x10) {
    FUN_823085a0(param_1,6);
    FUN_823085a0(param_1,7);
    FUN_823085a0(param_1,0xb);
    uVar1 = 0xc;
  }
  else {
    if (param_2 != 1) goto LAB_82308600;
    uVar1 = 2;
  }
  FUN_823085a0(param_1,uVar1);
LAB_82308600:
  param_1 = param_2 * 8 + param_1;
  if (*(int *)(param_1 + 0x4c) != 0) {
    FUN_821664c0();
    *(undefined4 *)(param_1 + 0x4c) = 0;
  }
  return;
}



// ===================================================
// 8231FE78  ->  FUN_8231fe78  (entree 8231fe78)
// ===================================================

void FUN_8231fe78(void)

{
  DAT_82657140 = FUN_8231fcb8(0xffffffff8265713c,DAT_8265713c);
  return;
}



