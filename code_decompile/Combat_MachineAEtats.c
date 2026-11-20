/* Combat_MachineAEtats  --  VF5FS+0xba1a0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800ba1a0.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


ulonglong Combat_MachineAEtats(longlong param_1)

{
  byte bVar1;
  char cVar2;
  undefined1 uVar3;
  undefined1 uVar4;
  undefined1 uVar5;
  undefined1 uVar6;
  undefined1 uVar7;
  undefined2 uVar8;
  undefined2 uVar9;
  int iVar10;
  undefined4 uVar11;
  undefined4 uVar12;
  int iVar13;
  longlong lVar14;
  undefined8 uVar15;
  undefined8 uVar16;
  ulonglong uVar17;
  char *pcVar18;
  undefined1 local_res8;
  uint3 local_res9;
  undefined1 uStackX_c;
  undefined2 local_resd;
  undefined2 in_stack_ffffffffffffffb8;
  
  uVar7 = (undefined1)((ushort)in_stack_ffffffffffffffb8 >> 8);
  cVar2 = FUN_1800b9e10();
  if (((cVar2 == '\0') && (*(char *)(param_1 + 0x724) != '\0')) && (*(int *)(param_1 + 0x6dc) == 8))
  {
    *(undefined4 *)(param_1 + 0x6dc) = 0xd;
    *(undefined1 *)(param_1 + 0x724) = 0;
  }
  FUN_1800b99d0(param_1);
  switch(*(undefined4 *)(param_1 + 0x6dc)) {
  case 1:
    cVar2 = FUN_1800becc0(param_1);
    if (cVar2 == '\0') break;
  case 2:
    FUN_1800bde30(param_1);
    break;
  case 3:
    iVar13 = *(int *)(param_1 + 0x6f4);
    cVar2 = FUN_1800c2c30(param_1 + 0x648);
    if (cVar2 != '\0') {
      FUN_1801973d0(&DAT_180750dd0);
      *(undefined1 *)(param_1 + 0x719) = 1;
      FUN_18006f8a0(2,0,1);
      FUN_18006f8a0(1,3);
    }
    cVar2 = FUN_1800b9c50(param_1);
    if (cVar2 != '\0') {
      FUN_1802450a0(param_1 + 0x648);
    }
    cVar2 = FUN_180244ea0(param_1 + 0x648);
    if (cVar2 != '\0') break;
    FUN_180087260(3);
    if ((*(char *)(param_1 + 0x718) == '\0') &&
       (cVar2 = FUN_1800b1b80(*(undefined8 *)(param_1 + 0x6c8),iVar13), cVar2 != '\0')) {
      uVar3 = FUN_1800c57a0(iVar13);
      uVar11 = FUN_1800b48d0(*(undefined8 *)(param_1 + 0x6c8));
      uVar8 = CONCAT11(uVar7,uVar3);
      FUN_1800c3c60((longlong)iVar13 * 0x80 + 0x3c8 + param_1,iVar13,4,uVar11,uVar8);
      uVar7 = (undefined1)((ushort)uVar8 >> 8);
    }
    *(undefined4 *)(param_1 + 0x6dc) = 4;
  case 4:
    iVar13 = *(int *)(param_1 + 0x6f8);
    lVar14 = param_1 + 0x3c8 + (longlong)*(int *)(param_1 + 0x6f4) * 0x80;
    cVar2 = FUN_1800c2c30(lVar14);
    if (cVar2 != '\0') {
      FUN_1801973d0(&DAT_180750dd0);
      *(undefined1 *)(param_1 + 0x719) = 0;
      FUN_18006f8a0(2,0,2);
      FUN_18006f8a0(1,3);
    }
    cVar2 = FUN_1800b9c50(param_1);
    if (cVar2 != '\0') {
      FUN_1802450a0(lVar14);
    }
    cVar2 = FUN_180244ea0(lVar14);
    if (cVar2 == '\0') {
      if ((*(char *)(param_1 + 0x718) == '\0') &&
         (cVar2 = FUN_1800b1b80(*(undefined8 *)(param_1 + 0x6c8),iVar13), cVar2 != '\0')) {
        uVar3 = FUN_1800c57a0(iVar13);
        uVar11 = FUN_1800b48d0(*(undefined8 *)(param_1 + 0x6c8));
        FUN_1800c3c60((longlong)iVar13 * 0x80 + 0x3c8 + param_1,iVar13,4,uVar11,
                      CONCAT11(uVar7,uVar3));
      }
      *(undefined4 *)(param_1 + 0x6dc) = 5;
switchD_1800ba220_caseD_5:
      cVar2 = FUN_1800bd8c0(param_1);
      if (cVar2 != '\0') {
switchD_1800ba220_caseD_6:
        FUN_1800be300(param_1);
      }
    }
    break;
  case 5:
    goto switchD_1800ba220_caseD_5;
  case 6:
    goto switchD_1800ba220_caseD_6;
  case 7:
    if (DAT_1806436c0 != '\0') {
      FUN_180052df0();
    }
    FUN_180151120(*(undefined8 *)(param_1 + 0x6e8),3);
    if (*(longlong *)(*(longlong *)(param_1 + 0x6c8) + 0x1090) != 0) {
      FUN_180167cb0();
    }
    if (*(int *)(param_1 + 0x6d4) == 0) {
      FUN_180151120(*(undefined8 *)(param_1 + 0x6e8),4);
      FUN_180087260(6);
      FUN_180163e80();
      FUN_180185f40(0,0xffffffe2,0x3c);
      *(undefined4 *)(param_1 + 0x6dc) = 8;
    }
    break;
  case 8:
    uVar15 = FUN_1800b2440(*(undefined8 *)(param_1 + 0x6c8));
    if (DAT_1806436c0 != '\0') {
      FUN_180052df0();
    }
    lVar14 = *(longlong *)(param_1 + 0x6c8);
    if (*(longlong *)(lVar14 + 0x1090) != 0) {
      FUN_180167cb0(*(longlong *)(lVar14 + 0x1090));
      lVar14 = *(longlong *)(param_1 + 0x6c8);
    }
    FUN_1800b2580(lVar14);
    FUN_1800b1f10(uVar15);
    iVar13 = FUN_1800b45a0(uVar15);
    if (iVar13 == 600) {
      FUN_180087260(7);
    }
    cVar2 = FUN_180150170(*(undefined8 *)(param_1 + 0x6e8),0);
    if ((cVar2 != '\0') &&
       (cVar2 = FUN_180150170(*(undefined8 *)(param_1 + 0x6e8),1), cVar2 != '\0')) {
      cVar2 = FUN_1800b1e50(uVar15);
      if (cVar2 == '\0') break;
      FUN_1801514a0(*(undefined8 *)(param_1 + 0x6e8));
    }
    FUN_180087260(8);
    uVar8 = FUN_1801508e0(*(undefined8 *)(param_1 + 0x6e8),0);
    uVar9 = FUN_1801508e0(*(undefined8 *)(param_1 + 0x6e8),1);
    uVar3 = FUN_180150170(*(undefined8 *)(param_1 + 0x6e8),0);
    uVar4 = FUN_180150170(*(undefined8 *)(param_1 + 0x6e8),1);
    uVar5 = FUN_1801501c0(*(undefined8 *)(param_1 + 0x6e8),0);
    uVar6 = FUN_1801501c0(*(undefined8 *)(param_1 + 0x6e8),1);
    uVar7 = FUN_1800b1fb0(*(undefined8 *)(param_1 + 0x6c8),uVar3,uVar4,uVar5,CONCAT11(uVar7,uVar6),
                          uVar8,uVar9);
    *(undefined1 *)(param_1 + 0x6d8) = uVar7;
    FUN_180185f40(0,0,0x3c);
    *(undefined4 *)(param_1 + 0x6dc) = 9;
    break;
  case 9:
    if (DAT_1806436c0 != '\0') {
      FUN_180052df0();
    }
    lVar14 = *(longlong *)(param_1 + 0x6c8);
    if (*(longlong *)(lVar14 + 0x1090) != 0) {
      FUN_180167cb0(*(longlong *)(lVar14 + 0x1090));
      lVar14 = *(longlong *)(param_1 + 0x6c8);
    }
    uVar15 = FUN_1800b2440(lVar14);
    iVar13 = FUN_1800b47c0(uVar15);
    if (*(int *)(&DAT_18034b208 + (longlong)iVar13 * 4) != 2) {
      lVar14 = FUN_180150920(*(undefined8 *)(param_1 + 0x6e8));
      *(byte *)(lVar14 + 0x442) = *(byte *)(lVar14 + 0x442) | 1;
    }
    FUN_1800a9d80(&DAT_1806f9bb0);
    if (*(char *)(param_1 + 0x6d8) != '\0') {
      FUN_1800a9f00(&DAT_1806f9bb0);
      iVar13 = FUN_1800244d0(*(undefined8 *)(param_1 + 0x6c8));
      if ((iVar13 == 1) && (iVar13 = FUN_1800b4600(*(undefined8 *)(param_1 + 0x6c8)), iVar13 == 1))
      {
        iVar13 = FUN_1800b4580(*(undefined8 *)(param_1 + 0x6c8));
        iVar10 = FUN_1800b4810(*(undefined8 *)(param_1 + 0x6c8));
        if (iVar13 == iVar10) {
          uVar11 = FUN_1800b4580(*(undefined8 *)(param_1 + 0x6c8));
          uVar11 = FUN_180007440(uVar11);
          *(undefined4 *)(param_1 + 0x70c) = uVar11;
        }
      }
      if (*(int *)(param_1 + 0x704) == 0) {
        uVar11 = FUN_1800b4940(*(undefined8 *)(param_1 + 0x6c8));
        iVar13 = FUN_180007440(uVar11);
        if (iVar13 != 0) {
          *(int *)(param_1 + 0x704) = iVar13;
        }
      }
    }
    FUN_1800c5cb0(param_1 + 0x6d8);
    FUN_180087260(9);
    if (*(char *)(param_1 + 0x6d8) != '\0') {
      _guard_check_icall();
    }
    FUN_180245830(param_1 + 0x110,"DISP_JUDGE");
    *(undefined4 *)(param_1 + 0x6d4) = 0xb5;
    *(undefined4 *)(param_1 + 0x6dc) = 10;
    goto LAB_1800babf1;
  case 10:
    if (DAT_1806436c0 != '\0') {
      FUN_180052df0();
    }
    if (*(longlong *)(*(longlong *)(param_1 + 0x6c8) + 0x1090) != 0) {
      FUN_180167cb0();
    }
    if ((module_execute_info_courant == 0) ||
       (*(longlong *)(module_execute_info_courant + 0x1fe10) == 0)) {
      if (*(int *)(param_1 + 0x6d4) != 0) break;
    }
    else {
      if (*(int *)(param_1 + 0x6d4) != 0) break;
      FUN_180163d20(0xffffffff);
    }
    FUN_180029be0(*(undefined4 *)(param_1 + 0x70c));
    *(undefined4 *)(param_1 + 0x70c) = 0;
    _guard_check_icall();
    FUN_180053330();
    FUN_1801ba8c0();
    FUN_180151120(*(undefined8 *)(param_1 + 0x6e8),1);
    FUN_1800c5fe0();
    *(undefined4 *)(param_1 + 0x6dc) = 0xb;
    FUN_180087260(10,0);
    break;
  case 0xb:
    FUN_180087260(0xb);
    FUN_18006f300();
    FUN_180051a10();
    uVar15 = FUN_1800b2440(*(undefined8 *)(param_1 + 0x6c8));
    uVar8 = FUN_1800b45d0(uVar15,1);
    uVar15 = FUN_1800b2440(*(undefined8 *)(param_1 + 0x6c8));
    uVar9 = FUN_1800b45d0(uVar15,0);
    uVar11 = FUN_1800b4870(*(undefined8 *)(param_1 + 0x6c8),1);
    uVar12 = FUN_1800b4870(*(undefined8 *)(param_1 + 0x6c8),0);
    FUN_180150f50(*(undefined8 *)(param_1 + 0x6e8),uVar12,uVar11,uVar9,uVar8);
    *(undefined4 *)(param_1 + 0x6d4) = 0xf0;
    FUN_180163e50();
    if ((module_execute_info_courant == 0) ||
       (*(longlong *)(module_execute_info_courant + 0x1fe10) == 0)) {
      FUN_180245830(param_1 + 400,"DISP_REPLAY");
    }
    if (*(char *)(param_1 + 0x6d8) != '\0') {
      iVar13 = FUN_1800244d0(*(undefined8 *)(param_1 + 0x6c8));
      if ((iVar13 == 1) || (cVar2 = FUN_1800b5800(*(undefined8 *)(param_1 + 0x6c8)), cVar2 != '\0'))
      {
        _guard_check_icall();
      }
      if (*(int *)(param_1 + 0x704) != 0) {
        uVar11 = FUN_1800b4940(*(undefined8 *)(param_1 + 0x6c8));
        iVar13 = FUN_180007440(uVar11);
        if (iVar13 != 0) {
          FUN_180029be0(*(undefined4 *)(param_1 + 0x704));
          *(int *)(param_1 + 0x704) = iVar13;
        }
      }
    }
    FUN_180164b50();
    *(undefined4 *)(param_1 + 0x6dc) = 0xc;
    break;
  case 0xc:
    FUN_1800bdaf0(param_1);
    break;
  case 0xd:
    FUN_180087260(0xd);
    lVar14 = LireObjetEntree();
    if (lVar14 == 0) {
      iVar13 = 0xf0;
    }
    else {
      uVar15 = LireObjetEntree();
      lVar14 = FUN_1800b24b0(uVar15);
      iVar13 = 0xf0;
      lVar14 = *(longlong *)(lVar14 + 0x1090);
      if (lVar14 != 0) {
        iVar13 = (*(int *)(lVar14 + 0x148) - *(int *)(lVar14 + 0x144)) + 0x1e;
      }
    }
    FUN_180163d20(iVar13);
    FUN_180053330();
    FUN_180151120(*(undefined8 *)(param_1 + 0x6e8),1);
    FUN_18006f300();
    FUN_180051a10();
    uVar15 = FUN_1800b2440(*(undefined8 *)(param_1 + 0x6c8));
    uVar8 = FUN_1800b45d0(uVar15,1);
    uVar15 = FUN_1800b2440(*(undefined8 *)(param_1 + 0x6c8));
    uVar9 = FUN_1800b45d0(uVar15,0);
    uVar11 = FUN_1800b4870(*(undefined8 *)(param_1 + 0x6c8),1);
    uVar12 = FUN_1800b4870(*(undefined8 *)(param_1 + 0x6c8),0);
    FUN_180150f50(*(undefined8 *)(param_1 + 0x6e8),uVar12,uVar11,uVar9,uVar8);
    FUN_180163e20();
    FUN_180164b50();
    _guard_check_icall();
    _guard_check_icall();
    _guard_check_icall();
    *(undefined4 *)(param_1 + 0x6dc) = 0xe;
    break;
  case 0xe:
    cVar2 = FUN_1801630b0();
    if (cVar2 == '\0') {
      FUN_180087260(0xe);
      *(undefined4 *)(param_1 + 0x6dc) = 0x1a;
    }
    break;
  case 0xf:
    FUN_1800be520(param_1);
    break;
  case 0x10:
    cVar2 = FUN_180244ea0(param_1 + 0x1f0);
    if ((*(int *)(param_1 + 0x290) != 5) && (cVar2 != '\0')) break;
    cVar2 = FUN_1800b1d70(*(undefined8 *)(param_1 + 0x6c8));
    if ((cVar2 != '\0') && (iVar13 = FUN_1800244d0(*(undefined8 *)(param_1 + 0x6c8)), iVar13 == 0))
    {
      iVar13 = FUN_1800b4580(*(undefined8 *)(param_1 + 0x6c8));
      iVar10 = FUN_1800b4940(*(undefined8 *)(param_1 + 0x6c8));
      if (iVar13 != iVar10) {
        lVar14 = FUN_18008b0c0();
        FUN_1802450a0(param_1 + 0x1f0);
        FUN_1800c56c0();
        iVar13 = LireSorteDePartie();
        if (iVar13 == 2) {
          *(undefined4 *)(param_1 + 0x6dc) = 0x1a;
        }
        else if ((lVar14 == 0) || (cVar2 = FUN_18008b2c0(lVar14), cVar2 == '\0')) {
          FUN_1802450a0(param_1 + 0x4c8);
          *(undefined4 *)(param_1 + 0x6dc) = 0x15;
        }
        else {
          *(undefined4 *)(param_1 + 0x6dc) = 0x11;
        }
        goto LAB_1800babf1;
      }
    }
    *(undefined4 *)(param_1 + 0x6dc) = 0x1a;
    if (DAT_180c3b702 != '\0') {
      iVar13 = 0;
      do {
        uVar15 = LireObjetEntree();
        cVar2 = FUN_1800b1d30(uVar15,iVar13);
        if (cVar2 == '\0') {
          InscrireJoueur(uVar15,iVar13,1,1);
        }
        else {
          FUN_1800b2770();
          iVar10 = FUN_1800cc260(iVar13);
          if ((iVar10 == 1) && (cVar2 = FUN_1800cc220(iVar13), cVar2 == '\0')) {
            FUN_1800cc2d0(iVar13);
            FUN_1800cc2f0(iVar13,0);
            FUN_1800cb110(iVar13);
          }
        }
        iVar13 = iVar13 + 1;
      } while (iVar13 < 2);
      DemanderSousEtat(0x11);
    }
LAB_1800babf1:
    iVar13 = LireSorteDePartie();
    if (iVar13 == 2) {
      FUN_1801da1f0();
    }
    break;
  case 0x11:
    uVar15 = FUN_18008b0c0();
    if ((module_execute_info_courant == 0) ||
       (pcVar18 = "rom/sound/bgm/vfes_bgm_con.adx",
       *(longlong *)(module_execute_info_courant + 0x1fe10) == 0)) {
      pcVar18 = "rom/sound/bgm/vf5fs_lp_cnt.adx";
    }
    FUN_180185da0(0,pcVar18,0);
    FUN_18006f8a0(2,0,2);
    FUN_18006f8a0(1,3);
    FUN_18008abe0(uVar15);
    FUN_180245830(param_1 + 0x298,"DISP_CONTINUE");
    *(undefined4 *)(param_1 + 0x6dc) = 0x12;
    if (((module_execute_info_courant == 0) || (cVar2 = FUN_18021d190(), cVar2 == '\0')) ||
       (lVar14 = FUN_18021a6e0(), *(char *)(lVar14 + 0x13) != '\0')) break;
    local_res9 = (uint3)(byte)local_res9;
    local_resd = 0;
    local_res8 = 5;
    lVar14 = FUN_1802194c0();
    bVar1 = *(byte *)(lVar14 + 0xb);
    lVar14 = FUN_18021d210();
    if ((int)(uint)bVar1 < *(int *)(lVar14 + 0x3818)) {
      lVar14 = FUN_18021d210();
      uVar7 = *(undefined1 *)(lVar14 + 0x3818);
    }
    else {
      lVar14 = FUN_1802194c0();
      uVar7 = *(undefined1 *)(lVar14 + 0xb);
    }
    _local_res9 = CONCAT31(stack0x0000000a,uVar7);
    lVar14 = FUN_1802194c0();
    _local_res9 = CONCAT13(*(undefined1 *)(lVar14 + 0xb),local_res9);
    goto LAB_1800bae12;
  case 0x12:
    cVar2 = FUN_180244ea0(param_1 + 0x298);
    if (cVar2 != '\0') break;
    FUN_1802450a0(param_1 + 0x4c8);
    *(undefined4 *)(param_1 + 0x6dc) = 0x15;
    goto LAB_1800badf1;
  case 0x13:
    FUN_1802450a0(param_1 + 0x4c8);
    uVar11 = FUN_1800b48d0(*(undefined8 *)(param_1 + 0x6c8));
    uVar12 = FUN_1800b4810(*(undefined8 *)(param_1 + 0x6c8));
    FUN_1800c3c60(param_1 + 0x5c8,uVar12,2,uVar11,CONCAT11(uVar7,0xff));
    *(undefined4 *)(param_1 + 0x6dc) = 0x14;
    break;
  case 0x14:
    cVar2 = FUN_180244ea0(param_1 + 0x5c8);
    if ((cVar2 != '\0') ||
       (((module_execute_info_courant != 0 &&
         (*(code **)(module_execute_info_courant + 0x1fe10) != (code *)0x0)) &&
        (iVar13 = (**(code **)(module_execute_info_courant + 0x1fe10))
                            (*(undefined8 *)(module_execute_info_courant + 0x1fe18),0x9a,0),
        iVar13 == 2)))) break;
    FUN_18006f8a0(2,0,0);
    FUN_18006f8a0(1,3,1);
    *(undefined4 *)(param_1 + 0x6dc) = 0x1a;
LAB_1800badf1:
    if (module_execute_info_courant != 0) {
      _local_res9 = 0;
      local_resd = 0;
      local_res8 = 0;
LAB_1800bae12:
      if (*(code **)(module_execute_info_courant + 0x1fe10) != (code *)0x0) {
        (**(code **)(module_execute_info_courant + 0x1fe10))
                  (*(undefined8 *)(module_execute_info_courant + 0x1fe18),0x2b,&local_res8);
      }
    }
    break;
  case 0x15:
    FUN_180087260(0x10);
    FUN_180245830(param_1 + 0x300,"DISP_GAME_OVER");
    uVar11 = FUN_1800b4600(*(undefined8 *)(param_1 + 0x6c8));
    *(undefined4 *)(param_1 + 0x35c) = uVar11;
    uVar11 = FUN_1800b48d0(*(undefined8 *)(param_1 + 0x6c8));
    uVar12 = FUN_1800b4810(*(undefined8 *)(param_1 + 0x6c8));
    FUN_1800c3c60(param_1 + 0x548,uVar12,3,uVar11,CONCAT11(uVar7,0xff));
    *(undefined4 *)(param_1 + 0x6dc) = 0x16;
    break;
  case 0x16:
    cVar2 = FUN_1800b9e10();
    if (((cVar2 == '\0') && (cVar2 = FUN_180007450(), cVar2 == '\0')) &&
       (cVar2 = FUN_180007450(), cVar2 == '\0')) {
      uVar15 = Entree_RolesDuPort(0);
      uVar16 = Entree_RolesDuPort(1);
      cVar2 = Entree_RoleFront(uVar15,0x62);
      if (((cVar2 == '\0') && (cVar2 = Entree_RoleFront(uVar16,0x62), cVar2 == '\0')) &&
         ((cVar2 = FUN_180244ea0(param_1 + 0x548), cVar2 != '\0' ||
          ((*(int *)(param_1 + 0x360) != 0 || (cVar2 = FUN_1801856a0(0), cVar2 != '\0')))))) {
        cVar2 = FUN_180244ea0(param_1 + 0x548);
        if ((((cVar2 == '\0') && (module_execute_info_courant != 0)) &&
            (*(longlong *)(module_execute_info_courant + 0x1fe10) != 0)) &&
           (*(code **)(module_execute_info_courant + 0x1fe10) != (code *)0x0)) {
          (**(code **)(module_execute_info_courant + 0x1fe10))
                    (*(undefined8 *)(module_execute_info_courant + 0x1fe18),0x9c,0);
        }
      }
      else {
        FUN_1802450a0(param_1 + 0x548);
        FUN_18006f8a0(2,0,0);
        FUN_18006f8a0(1,3,1);
        FUN_180087260(0x11);
        *(undefined4 *)(param_1 + 0x6dc) = 0x1a;
      }
    }
    break;
  case 0x17:
    FUN_1800be050(param_1);
    break;
  case 0x18:
    cVar2 = FUN_1800d4180(&DAT_18070afd0);
    if (cVar2 != '\0') {
      FUN_1800d41f0(&DAT_18070afd0);
    }
    FUN_180186d10();
    FUN_180186d40(1);
    FUN_180186d40(2);
    FUN_1800a9d10(&DAT_1806f9bb0);
    cVar2 = FUN_180244ea0(DAT_1806f9c50 + 0x368);
    if (cVar2 == '\0') {
      *(undefined4 *)(param_1 + 0x6dc) = 0x19;
    }
    break;
  case 0x19:
    cVar2 = FUN_1800d4180(&DAT_18070afd0);
    if (cVar2 != '\0') {
      FUN_1800d41f0(&DAT_18070afd0);
    }
    FUN_180186d10();
    FUN_180087880();
    *(undefined4 *)(param_1 + 0x6dc) = 0x1a;
    break;
  case 0x1a:
    iVar13 = LireSorteDePartie();
    if (((iVar13 != 4) && (iVar13 = LireSorteDePartie(), iVar13 != 3)) &&
       (cVar2 = FUN_1801bac30(), cVar2 == '\0')) {
      FUN_180186d40(0);
      FUN_180186d40(1);
      FUN_180186d40(2);
    }
    if (((*(char *)(param_1 + 0x6f0) == '\0') && (*(longlong *)(param_1 + 0x6c8) != 0)) &&
       ((lVar14 = *(longlong *)(*(longlong *)(param_1 + 0x6c8) + 0x1090), lVar14 != 0 &&
        (*(char *)(lVar14 + 0xf1d) != '\0')))) {
      FUN_180167eb0();
    }
    *(undefined1 *)(param_1 + 0x6f0) = 1;
    iVar13 = LireSorteDePartie();
    if (iVar13 == 2) {
      FUN_1801d8730();
    }
  }
  if ((*(int *)(param_1 + 0x6d4) != 0) && (*(char *)(param_1 + 0x6d0) == '\0')) {
    *(int *)(param_1 + 0x6d4) = *(int *)(param_1 + 0x6d4) + -1;
  }
  if (0 < *(int *)(param_1 + 0x714)) {
    *(int *)(param_1 + 0x714) = *(int *)(param_1 + 0x714) + -1;
  }
  uVar17 = module_remplir_rapport(param_1);
  return uVar17 & 0xffffffffffffff00;
}
