/* FUN_1802079e0  --  VF5FS+0x2079e0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1802079e0.
 * Vidée le 2026-11-10.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* WARNING: Removing unreachable block (ram,0x000180208868) */
/* WARNING: Removing unreachable block (ram,0x00018020886b) */

ulonglong FUN_1802079e0(longlong param_1)

{
  int *piVar1;
  undefined2 *puVar2;
  char cVar3;
  byte bVar4;
  undefined1 uVar5;
  char cVar6;
  char cVar7;
  char cVar8;
  undefined4 uVar9;
  int iVar10;
  longlong lVar11;
  ulonglong uVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  longlong lVar15;
  longlong lVar16;
  undefined8 *puVar17;
  char *pcVar18;
  longlong *plVar19;
  undefined1 (*pauVar20) [16];
  bool bVar21;
  uint local_res8;
  char local_resc;
  undefined4 local_108;
  undefined4 local_104;
  undefined8 local_100;
  undefined4 local_f8;
  undefined4 local_f4;
  ulonglong local_f0;
  undefined8 local_e8;
  undefined2 local_e0;
  undefined4 local_d8 [4];
  undefined4 *local_c8;
  ulonglong uStack_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  ulonglong local_a8;
  undefined8 uStack_a0;
  longlong lStack_98;
  longlong lStack_90;
  longlong local_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 local_48;
  undefined8 local_38;
  longlong local_30;
  
  cVar3 = FUN_1801d1c70();
  if ((((cVar3 == '\0') && (cVar3 = FUN_1801d1c80(), cVar3 == '\0')) &&
      (cVar3 = FUN_1801ceef0(), cVar3 != '\0')) && (cVar3 = FUN_1801cf0c0(), cVar3 != '\0')) {
    FUN_1801d5a50(1);
    FUN_1801d5a70(1);
    lVar11 = FUN_1801d1ae0();
    bVar4 = FUN_180212d00(*(undefined1 *)(lVar11 + 0x1bd1),1);
    *(undefined1 *)(param_1 + 0x3024) = 1;
    if ((bVar4 & 0x20) == 0) {
      if ((bVar4 & 0x10) == 0) {
        if ((bVar4 & 8) == 0) {
          if ((bVar4 & 4) == 0) {
            if ((bVar4 & 2) == 0) {
              *(byte *)(param_1 + 0x3026) = bVar4 & 1;
            }
            else {
              *(undefined1 *)(param_1 + 0x3026) = 2;
            }
          }
          else {
            *(undefined1 *)(param_1 + 0x3026) = 3;
          }
        }
        else {
          *(undefined1 *)(param_1 + 0x3026) = 4;
        }
      }
      else {
        *(undefined1 *)(param_1 + 0x3026) = 5;
      }
    }
    else {
      *(undefined1 *)(param_1 + 0x3026) = 6;
    }
    FUN_1801cfd80(1,0xffffffff);
  }
  cVar3 = FUN_1801ceef0();
  lVar11 = param_1 + 0x27c0;
  if (*(char *)(param_1 + 0x27d8) != cVar3) {
    uVar5 = FUN_1801ceef0();
    *(undefined1 *)(param_1 + 0x27d8) = uVar5;
  }
  if (*(longlong *)(param_1 + 0x608) != 0) {
    cVar3 = FUN_1802cb570();
    if (cVar3 != '\0') {
      FUN_1802ccb60(*(undefined8 *)(param_1 + 0x608));
    }
    uVar12 = FUN_1802cca00(*(undefined8 *)(param_1 + 0x608));
    if ((char)uVar12 == '\0') {
      *(undefined8 *)(param_1 + 0x608) = 0;
      cVar3 = FUN_1802cb570();
      if (cVar3 == '\0') {
        FUN_18020e9b0(param_1 + 0x28e8);
      }
      *(undefined2 *)(param_1 + 0x28c4) = 0x1311;
      *(undefined4 *)(param_1 + 0x28c9) = 5;
      *(undefined2 *)(param_1 + 0x28cd) = 0;
      *(undefined1 *)(param_1 + 0x28cf) = 0;
      *(undefined8 *)(param_1 + 0x28d2) = 0;
      if (((DAT_180c8df28 == 0) || (*(longlong *)(DAT_180c8df28 + 0x1ff08) == 0)) ||
         ((*(code **)(DAT_180c8df28 + 0x1ff08) == (code *)0x0 ||
          (uVar12 = (**(code **)(DAT_180c8df28 + 0x1ff08))
                              (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0x50), (int)uVar12 != 1))))
      goto LAB_180207b7d;
    }
    goto LAB_180208b81;
  }
LAB_180207b7d:
  if (*(char *)(param_1 + 0x28dd) == '\0') {
    uVar12 = FUN_18021bc00(&local_res8);
    if ((char)uVar12 != '\0') goto LAB_180208b81;
    *(undefined1 *)(param_1 + 0x28dd) = 1;
    FUN_180218530(lVar11,param_1 + 0x27b0);
    FUN_1801a3f20(&DAT_1807956d0);
  }
  if ((DAT_180c8df28 == 0) || (*(longlong *)(DAT_180c8df28 + 0x1ff08) == 0)) {
    uVar12 = 0;
    FUN_1801de430(param_1 + 0x230);
    FUN_1801de430(param_1 + 0x280);
    FUN_1801de430(param_1 + 0x2d0);
    FUN_1801e15d0(param_1,0x5e3d);
    if (*(char *)(param_1 + 0x5f4) != '\0') {
      iVar10 = FUN_1801df8e0(param_1 + 0x488);
      if (iVar10 < 0) {
        return 0;
      }
      *(undefined1 *)(param_1 + 0x5f4) = 0;
      if (iVar10 == 0) {
        if (*(int *)(param_1 + 0x58) != 9) {
          return 0;
        }
        *(undefined1 *)(param_1 + 0x60) = 1;
        FUN_180206bd0(param_1);
        *(undefined1 *)(param_1 + 0x5f9) = 1;
        return 0;
      }
    }
    FUN_1801e1660(param_1,0x5e3d);
    cVar3 = FUN_1801e0420(param_1);
    if ((((cVar3 == '\0') && (cVar3 = FUN_1801e0410(param_1 + 0x230), cVar3 != '\0')) &&
        (cVar3 = FUN_1801e0410(param_1 + 0x280), cVar3 != '\0')) &&
       (((cVar3 = FUN_1801e0410(param_1 + 0x2d0), cVar3 != '\0' &&
         (cVar3 = FUN_1802ccab0(param_1 + 800), cVar3 == '\0')) &&
        (cVar3 = FUN_1802ccab0(param_1 + 0x488), cVar3 == '\0')))) {
      if ((*(char *)(param_1 + 0x60) != '\0') && (*(int *)(param_1 + 0x58) == 9)) {
        FUN_18019e6c0();
        return 1;
      }
      FUN_1800e1b00(0);
      FUN_1800e1b20(5);
      uVar12 = 1;
    }
    if (*(char *)(param_1 + 0x5f9) != '\0') {
      return uVar12;
    }
    cVar3 = FUN_180026620();
    if (cVar3 == '\0') {
      return uVar12;
    }
    cVar3 = FUN_1801c5290();
    if (cVar3 != '\0') {
      return uVar12;
    }
    if (*(char *)(param_1 + 0x5f8) != '\0') {
      *(undefined1 *)(param_1 + 0x5f8) = 0;
      cVar3 = FUN_18000ba20();
      if (cVar3 != '\0') {
        local_res8 = CONCAT31(local_res8._1_3_,1);
        FUN_180081c50(0x2e,&local_res8);
        return 1;
      }
    }
    if (*(longlong *)(param_1 + 0x608) != 0) {
      cVar3 = FUN_1802ccab0();
      if (cVar3 != '\0') {
        return uVar12;
      }
      *(undefined8 *)(param_1 + 0x608) = 0;
      if ((*(int *)(param_1 + 0x58) == 9) && (cVar3 = FUN_1801bbaf0(), cVar3 != '\0')) {
        *(undefined1 *)(param_1 + 0x60) = 1;
        FUN_1801de400(param_1);
        FUN_1801de320(param_1 + 0x230);
        FUN_1801de320(param_1 + 0x280);
        FUN_1801de320(param_1 + 0x2d0);
        FUN_1802ccb60(param_1 + 800);
        FUN_1802ccb60(param_1 + 0x488);
        *(undefined1 *)(param_1 + 0x5f9) = 1;
      }
      _guard_check_icall(0xffffffff);
      cVar3 = FUN_180194240(0);
      if (cVar3 == '\0') {
        FUN_180194aa0(0,"rom/sound/bgm/vf5b_tkv.adx",0);
      }
    }
    local_108 = 0x62;
    local_104 = 99;
    local_100 = 0x6600000065;
    local_f8 = 0x67;
    local_f4 = 0x68;
    local_f0 = 0x6a00000069;
    local_e8._4_4_ = 0x6e;
    cVar3 = FUN_18000ba20();
    uVar9 = 0x6b;
    if (cVar3 == '\0') {
      uVar9 = 0x6d;
    }
    local_e8 = CONCAT44(local_e8._4_4_,uVar9);
    FUN_1801e1660(param_1,(&local_108)[*(int *)(param_1 + 0x58)]);
    cVar3 = FUN_1802ccab0(param_1 + 800);
    if (cVar3 != '\0') {
      return uVar12;
    }
    FUN_1801de510(param_1);
    FUN_1801e15d0(param_1,0);
    return uVar12;
  }
  if (*(char *)(param_1 + 0x28df) == '\0') {
    if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
      (**(code **)(DAT_180c8df28 + 0x1ff08))
                (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xfc,param_1 + 0x28df);
    }
    if (*(char *)(param_1 + 0x28df) != '\0') {
      *(undefined1 *)(param_1 + 0x3023) = 1;
    }
  }
  if (*(char *)(param_1 + 0x3023) == '\x01') {
    FUN_1802230d0();
    local_res8 = CONCAT31(local_res8._1_3_,1);
    if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
      (**(code **)(DAT_180c8df28 + 0x1ff08))
                (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xfe,&local_res8);
    }
    *(char *)(param_1 + 0x3023) = *(char *)(param_1 + 0x3023) + '\x01';
LAB_180207c66:
    *(undefined1 *)(param_1 + 0x28fb) = 1;
    cVar3 = FUN_180222e00();
    if (cVar3 == '\0') {
      FUN_180222e10();
      local_res8 = local_res8 & 0xffffff00;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xfe,&local_res8);
      }
      *(undefined1 *)(param_1 + 0x3023) = 0;
      *(undefined1 *)(param_1 + 0x28df) = 0;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))(*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xfd,0);
      }
    }
  }
  else if (*(char *)(param_1 + 0x3023) == '\x02') goto LAB_180207c66;
  cVar3 = FUN_1802cb570();
  if ((cVar3 != '\0') || (*(char *)(param_1 + 0x28f9) == '\0')) {
    local_108 = 1;
    local_104 = 0x141400;
    local_100 = 0x10000;
    local_f8 = 0x2000001;
    local_f4 = 0x10000;
    local_f0 = 0x500;
    local_e8 = 0;
    local_e0 = 0;
    uVar13 = FUN_1801d1b00();
    uVar14 = FUN_1801d1ab0();
    FUN_1801d5460(&local_108,0,0,uVar14,uVar13,0);
    uVar13 = FUN_1801d1ab0();
    FUN_1801d5410(&local_108,uVar13);
    cVar3 = FUN_1801aaa40(0);
    if (((cVar3 == '\0') &&
        (((cVar3 = FUN_1801aaa40(1), cVar3 == '\0' && (cVar3 = FUN_1801aaa40(2), cVar3 == '\0')) &&
         (cVar3 = FUN_1801aaa40(3), cVar3 == '\0')))) && (cVar3 = FUN_1801aaa40(4), cVar3 == '\0'))
    {
      cVar3 = FUN_1801aaa40(6);
      local_108 = local_108 & 0xffffff00;
      if (cVar3 != '\0') goto LAB_180207dc6;
    }
    else {
LAB_180207dc6:
      local_108 = CONCAT31(local_108._1_3_,1);
    }
    cVar3 = FUN_1801aaa40(0);
    if (((cVar3 == '\0') && (cVar3 = FUN_1801aaa40(1), cVar3 == '\0')) &&
       ((cVar3 = FUN_1801aaa40(4), cVar3 == '\0' && (cVar3 = FUN_1801aaa40(6), cVar3 == '\0')))) {
LAB_180207e0c:
      local_108._0_2_ = (ushort)(byte)local_108;
    }
    else {
      cVar3 = FUN_1801d1a90();
      local_108._0_2_ = CONCAT11(1,(byte)local_108);
      if (cVar3 != '\0') goto LAB_180207e0c;
    }
    cVar3 = FUN_1801aaa40(0);
    if (((cVar3 == '\0') && (cVar3 = FUN_1801aaa40(1), cVar3 == '\0')) &&
       (cVar3 = FUN_1801aaa40(2), cVar3 == '\0')) {
LAB_180207e44:
      local_108._0_3_ = (uint3)(ushort)local_108;
    }
    else {
      cVar3 = FUN_1801d1aa0();
      local_108._0_3_ = CONCAT12(1,(ushort)local_108);
      if (cVar3 != '\0') goto LAB_180207e44;
    }
    local_f0 = local_f0 & 0xffffffffffffff00;
    lVar15 = FUN_1801d1ae0();
    lVar16 = *(longlong *)(lVar15 + 0x68);
    bVar21 = true;
    if (lVar16 != 0) {
      uVar12 = FUN_1801c5cc0();
      bVar21 = true;
      if (uVar12 <= lVar16 + 0x2a30U) {
        uVar12 = FUN_1801cdfe0(lVar15 + 0x58);
        bVar21 = uVar12 < 3;
      }
    }
    uVar13 = local_100;
    local_100._5_3_ = SUB83(uVar13,5);
    local_100._0_5_ =
         CONCAT14(*(undefined1 *)(param_1 + 0x3022),
                  CONCAT13(*(undefined1 *)(param_1 + 0x3021),CONCAT12(bVar21,(undefined2)local_100))
                 );
    uVar5 = FUN_1801d1af0();
    uVar13 = local_e8;
    local_e8._0_4_ = CONCAT13(uVar5,(undefined3)local_e8);
    local_e8._7_1_ = SUB81(uVar13,7);
    local_e8 = CONCAT26(CONCAT11(local_e8._7_1_,*(undefined1 *)(param_1 + 0x3026)),
                        CONCAT15(*(undefined1 *)(param_1 + 0x3025),
                                 CONCAT14(*(undefined1 *)(param_1 + 0x3024),(undefined4)local_e8)));
    uVar5 = FUN_180267210();
    local_e0 = CONCAT11(uVar5,(undefined1)local_e0);
    *(undefined2 *)(param_1 + 0x3021) = 0;
    *(undefined2 *)(param_1 + 0x3024) = 0;
    *(undefined1 *)(param_1 + 0x3026) = 0;
    local_c8 = &local_108;
    uStack_b8 = CONCAT71((int7)(uStack_b8 >> 8),DAT_180647160) & 0xffffffffffffff;
    uVar5 = FUN_180206a20(param_1);
    uStack_b8._0_2_ = CONCAT11(uVar5,(undefined1)uStack_b8);
    uStack_b0._0_7_ = CONCAT16(*(undefined1 *)(param_1 + 0x28e1),(undefined6)uStack_b0);
    uVar5 = FUN_1802c5230();
    uStack_b8._0_3_ = CONCAT12(uVar5,(undefined2)uStack_b8);
    uStack_c0 = FUN_1802c5050();
    lStack_90 = param_1 + 0x2898;
    lStack_98 = lVar11;
    lVar16 = FUN_1801d1ae0();
    *(byte *)(param_1 + 0x27d5) = *(byte *)(lVar16 + 0x22) >> 1 & 1;
    uVar5 = FUN_180220ba0();
    *(undefined1 *)(param_1 + 0x27ce) = uVar5;
    if (*(char *)(param_1 + 0x27d5) == '\0') {
      *(undefined1 *)(param_1 + 0x27d1) = 0;
    }
    local_resc = '\0';
    local_res8 = 7;
    if (((*(code **)(DAT_180c8df28 + 0x1ff08) == (code *)0x0) ||
        ((**(code **)(DAT_180c8df28 + 0x1ff08))
                   (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0x17d,&local_res8), local_resc == '\0')
        ) && (lVar16 = FUN_1801d1ab0(), *(char *)(lVar16 + 0x4b) != '\0')) {
      uVar5 = 1;
    }
    else {
      *(undefined1 *)(param_1 + 0x27cb) = 1;
      uVar5 = 0;
    }
    *(undefined1 *)(param_1 + 0x27cc) = uVar5;
    uStack_b0._0_3_ = (uint3)(byte)uStack_b0;
    local_a8 = 0;
    piVar1 = (int *)(param_1 + 0x28e8);
    iVar10 = *(int *)(param_1 + 0x28ec);
    if (((iVar10 == 0) && (*piVar1 == 3 || *piVar1 == 4)) && (*(longlong *)(param_1 + 0x3010) == 0))
    {
      uStack_b8._0_4_ = CONCAT13(1,(uint3)uStack_b8);
LAB_180208033:
      uVar5 = 0;
    }
    else {
      uStack_b8._0_4_ = (uint)(uint3)uStack_b8;
      if (iVar10 != 3 && iVar10 != 4) goto LAB_180208033;
      uVar5 = 1;
    }
    uVar13 = uStack_b8;
    uStack_b8._6_2_ = SUB82(uVar13,6);
    uStack_b8._0_6_ = (uint6)CONCAT14(uVar5,(uint)uStack_b8);
    local_88 = param_1 + 0x2910;
    uVar5 = FUN_180217fd0(iVar10,param_1);
    uStack_b8 = CONCAT17(uVar5,(undefined7)uStack_b8);
    lVar16 = FUN_180217fc0();
    uStack_b0 = CONCAT71(uStack_b0._1_7_,*(char *)(lVar16 + 1) == '\0');
    uVar5 = FUN_1802cb570();
    uStack_b8._0_7_ = CONCAT16(uVar5,(uint6)uStack_b8);
    if (*(char *)(param_1 + 0x2909) == '\0') {
      cVar3 = FUN_1801a3ef0(&DAT_1807956d0);
      uStack_b0._0_4_ = (uint)(uint3)uStack_b0;
      if (cVar3 == '\0') goto LAB_18020809a;
    }
    else {
LAB_18020809a:
      uStack_b0._0_4_ = CONCAT13(1,(uint3)uStack_b0);
    }
    uVar5 = FUN_1802cb780();
    uStack_b0._0_5_ = CONCAT14(uVar5,(uint)uStack_b0);
    uVar5 = FUN_1802194c0();
    uStack_b0._0_6_ = CONCAT15(uVar5,(undefined5)uStack_b0);
    uStack_a0._0_4_ = 0;
    uVar9 = FUN_18022fad0();
    uStack_a0 = CONCAT44(uStack_a0._4_4_,uVar9);
    bVar4 = FUN_180206a20(param_1);
    *(byte *)(lStack_98 + 0x17) = bVar4 ^ 1;
    FUN_1801d1c90();
    if ((*(code **)(DAT_180c8df28 + 0x1ff08) == (code *)0x0) ||
       (iVar10 = (**(code **)(DAT_180c8df28 + 0x1ff08))
                           (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0x51,&local_c8), iVar10 != 1))
    {
      if (*(char *)(param_1 + 0x28cf) != '\0') {
        FUN_180266fb0(*(undefined4 *)(lStack_90 + 0x28));
        FUN_180211420(param_1);
        *(undefined1 *)(param_1 + 0x28cf) = 0;
      }
      cVar3 = FUN_1802cb570();
      if (cVar3 == '\0') {
        if (((*piVar1 == 0) && (cVar3 = FUN_180194240(0), cVar3 == '\0')) &&
           (*(char *)(param_1 + 0x28df) == '\0')) {
          FUN_180194aa0(0,"rom/sound/bgm/vfes_bgm_mnu.adx",0);
        }
        cVar6 = FUN_1802cb570();
        cVar3 = uStack_b8._5_1_;
        if (*(char *)(param_1 + 0x2908) == '\0') {
          if (cVar6 != '\0') goto LAB_180208a9e;
          FUN_18020e9b0(piVar1);
        }
        cVar7 = FUN_1801cf090();
        cVar8 = FUN_1801cef40();
        if (cVar7 == '\0') {
          if (cVar8 != '\0') goto LAB_180208a61;
        }
        else {
          FUN_1800e1b00(0);
          FUN_1800e1b20(5);
LAB_180208a61:
          FUN_1801951a0();
          FUN_1801951d0(0);
          FUN_1801951d0(1);
          FUN_1801951d0(2);
        }
        if ((cVar3 != '\0') || (*(char *)(param_1 + 0x28fb) != '\0')) {
          FUN_180211030(piVar1);
          FUN_180211220(piVar1,cVar6);
        }
      }
LAB_180208a9e:
      uVar12 = FUN_1802cb570();
      bVar4 = 0;
      if (*(char *)(param_1 + 0x27cd) != '\0') {
        bVar4 = (byte)uVar12 ^ 1;
      }
      if (bVar4 != 0) goto LAB_180208b81;
      if (*(char *)(param_1 + 0x28de) == '\0') {
        if (*(char *)(param_1 + 0x27d3) != '\0') {
          if (*(char *)(param_1 + 0x27d2) == '\0') {
            uVar5 = *(undefined1 *)(*(longlong *)(param_1 + 0x27c0) + 1);
          }
          else {
            uVar5 = *(undefined1 *)(param_1 + 0x27d1);
          }
          uVar12 = FUN_1801ee690(0,uVar5,0,1);
          *(undefined1 *)(param_1 + 0x27cd) = 0;
          *(undefined1 *)(param_1 + 0x28de) = 1;
          goto LAB_180208b60;
        }
      }
      else {
        uVar12 = FUN_1801edd30(0,param_1 + 0x27b0);
        iVar10 = (int)uVar12;
        if (iVar10 != 0) {
          *(undefined1 *)(param_1 + 0x27d3) = 0;
          *(undefined1 *)(param_1 + 0x28de) = 0;
          *(bool *)(param_1 + 0x27cd) = 0 < iVar10;
        }
        if (*(char *)(param_1 + 0x27d4) != '\0') {
          uVar13 = thunk_FUN_1801fa270(0);
          *(undefined1 *)(param_1 + 0x27d3) = 0;
          *(undefined1 *)(param_1 + 0x28de) = 0;
          uVar12 = CONCAT71((int7)((ulonglong)uVar13 >> 8),0 < iVar10);
          *(bool *)(param_1 + 0x27cd) = 0 < iVar10;
LAB_180208b60:
          *(undefined1 *)(param_1 + 0x27d4) = 0;
        }
      }
      if (*(char *)(param_1 + 0x27d5) != '\0') {
        *(undefined1 *)(param_1 + 0x27d5) = 0;
        uVar12 = FUN_1801d1ae0();
        *(ushort *)(uVar12 + 0x22) = *(ushort *)(uVar12 + 0x22) | 2;
      }
      goto LAB_180208b81;
    }
    switch(*(undefined1 *)(param_1 + 0x28c4)) {
    case 0:
      uVar13 = 3;
      break;
    case 1:
      uVar13 = 4;
      break;
    case 2:
      uVar13 = 9;
      break;
    case 3:
      uVar13 = 2;
      break;
    case 4:
      uVar13 = 1;
      break;
    case 5:
      uVar13 = 5;
      break;
    default:
      uVar13 = 0;
      break;
    case 8:
      uVar13 = 6;
      break;
    case 9:
      uVar13 = 7;
      break;
    case 0xc:
      uVar13 = 8;
    }
    FUN_1801a4030(&DAT_1807956d0,uVar13);
  }
  uVar12 = FUN_18020a2b0(param_1 + 0x28e8);
  if (((char)uVar12 == '\0') || (uVar12 = FUN_1800ba920(), (char)uVar12 != '\0'))
  goto LAB_180208b81;
  puVar2 = (undefined2 *)(param_1 + 0x28c4);
  DAT_180647160 = *(undefined1 *)puVar2;
  switch(*(undefined1 *)puVar2) {
  case 0:
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      local_d8[0] = 2;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xbc,local_d8);
      }
    }
    FUN_1802104e0(param_1,0);
    FUN_18021a450(lVar11,param_1 + 0x27b0);
    FUN_1800e1b00(0xb);
    uVar12 = 1;
    break;
  case 1:
    if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
      (**(code **)(DAT_180c8df28 + 0x1ff08))(*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xd5,0);
    }
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      local_d8[0] = 3;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xbc,local_d8);
      }
    }
    FUN_1802104e0(param_1,1);
    FUN_1800e1b00(0xc);
    uVar12 = 1;
    break;
  case 2:
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      local_d8[0] = 4;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xbc,local_d8);
      }
    }
    FUN_1802104e0(param_1,2);
    FUN_1800e1b00(0xd);
    uVar12 = 1;
    break;
  case 3:
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      local_d8[0] = 6;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xbc,local_d8);
      }
    }
    FUN_1801aa1d0(&local_res8,*(undefined2 *)(param_1 + 0x28d2),*(undefined2 *)(param_1 + 0x28d4),
                  *(undefined1 *)(param_1 + 0x28cb),*(undefined1 *)(param_1 + 0x28ca));
    cVar3 = *(char *)(param_1 + 0x28cc);
    FUN_180263ee0();
    FUN_1801aad60(4,&local_res8,cVar3);
    iVar10 = FUN_1801b2460(1);
    if (iVar10 < 0) {
      FUN_1801b3960(1);
    }
    puVar17 = (undefined8 *)FUN_1801d1ab0();
    local_c8 = (undefined4 *)*puVar17;
    uStack_c0 = puVar17[1];
    uStack_a0 = puVar17[5];
    lStack_98 = puVar17[6];
    lStack_90 = puVar17[7];
    local_88 = puVar17[8];
    uStack_80 = puVar17[9];
    uStack_78 = puVar17[10];
    uStack_70 = puVar17[0xb];
    local_68 = puVar17[0xc];
    uStack_60 = puVar17[0xd];
    uStack_58 = puVar17[0xe];
    uStack_50 = puVar17[0xf];
    local_48 = puVar17[0x10];
    uStack_b8._0_4_ = (uint)puVar17[2];
    uStack_b8 = (ulonglong)CONCAT14(*(undefined1 *)(param_1 + 0x28d6),(uint)uStack_b8);
    uStack_b0 = (ulonglong)
                CONCAT14(*(undefined1 *)(param_1 + 0x28d8),(uint)*(byte *)(param_1 + 0x28d7));
    local_a8 = (ulonglong)CONCAT14(cVar3 != '\0',(uint)*(byte *)(param_1 + 0x28d9));
    FUN_1801d5920(&local_c8);
    uVar12 = 1;
    break;
  case 4:
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      local_d8[0] = 5;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xbc,local_d8);
      }
    }
    FUN_1801aa1d0(&local_res8,*(undefined2 *)(param_1 + 0x28d2),*(undefined2 *)(param_1 + 0x28d4),
                  *(undefined1 *)(param_1 + 0x28cb),*(undefined1 *)(param_1 + 0x28ca));
    bVar4 = *(byte *)(param_1 + 0x28c9);
    FUN_1801aac20(0,&local_res8,bVar4,0);
    lVar11 = FUN_1801d1ab0();
    uStack_b0 = *(undefined8 *)(lVar11 + 0x18);
    local_a8 = *(undefined8 *)(lVar11 + 0x20);
    uStack_a0 = *(undefined8 *)(lVar11 + 0x28);
    lStack_98 = *(undefined8 *)(lVar11 + 0x30);
    lStack_90 = *(undefined8 *)(lVar11 + 0x38);
    local_88 = *(undefined8 *)(lVar11 + 0x40);
    uStack_80 = *(undefined8 *)(lVar11 + 0x48);
    uStack_78 = *(undefined8 *)(lVar11 + 0x50);
    uStack_70 = *(undefined8 *)(lVar11 + 0x58);
    local_68 = *(undefined8 *)(lVar11 + 0x60);
    uStack_60 = *(undefined8 *)(lVar11 + 0x68);
    uStack_58 = *(undefined8 *)(lVar11 + 0x70);
    uStack_50 = *(undefined8 *)(lVar11 + 0x78);
    local_48 = *(undefined8 *)(lVar11 + 0x80);
    local_c8 = (undefined4 *)(ulonglong)CONCAT14(*(undefined1 *)(param_1 + 0x28d6),(uint)bVar4);
    uStack_c0 = (ulonglong)
                CONCAT14(*(undefined1 *)(param_1 + 0x28d8),(uint)*(byte *)(param_1 + 0x28d7));
    uStack_b8._4_4_ = (undefined4)((ulonglong)*(undefined8 *)(lVar11 + 0x10) >> 0x20);
    uStack_b8 = CONCAT44(uStack_b8._4_4_,(uint)*(byte *)(param_1 + 0x28d9));
    FUN_1801d5920(&local_c8);
    uVar12 = 1;
    break;
  case 5:
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      local_d8[0] = 7;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xbc,local_d8);
      }
    }
    FUN_180260950(*(undefined1 *)(param_1 + 0x28c5));
    FUN_1802608b0(1);
    FUN_1801aabe0(6,0,1);
    uVar12 = 1;
    break;
  case 6:
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      local_d8[0] = 7;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xbc,local_d8);
      }
    }
    FUN_180262890(*(undefined1 *)(param_1 + 0x28c6));
    FUN_1801aabe0(9,0,1);
    uVar12 = 1;
    break;
  case 7:
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      local_d8[0] = 7;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xbc,local_d8);
      }
    }
    FUN_180240470(*(undefined1 *)(param_1 + 0x28c7));
    FUN_1802404d0(*(undefined1 *)(param_1 + 0x28c8));
    FUN_1801aabe0(10,0,1);
    uVar12 = 1;
    break;
  case 8:
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      local_d8[0] = 7;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xbc,local_d8);
      }
    }
    FUN_1801aabe0(7,*(char *)(param_1 + 0x28cd) == '\0',1);
    uVar12 = 1;
    break;
  case 9:
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      local_d8[0] = 7;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xbc,local_d8);
      }
    }
    FUN_1801aabe0(8,0,1);
    uVar12 = 1;
    break;
  case 10:
    uVar13 = FUN_1801c0100(0,0,1);
    *(undefined8 *)(param_1 + 0x608) = uVar13;
    cVar3 = FUN_180194240(0);
    if (cVar3 == '\0') {
      uVar12 = FUN_180194aa0(0,"rom/sound/bgm/vfes_bgm_mnu.adx",0);
      return uVar12 & 0xffffffffffffff00;
    }
    local_30 = 0;
    local_38 = 0;
    uVar12 = FUN_180193f00(&local_38,0);
    if ((char)uVar12 != '\0') {
      lVar16 = (local_30 << 0x14) >> 0x14;
      lVar11 = lVar16 << 4;
      if (lVar16 == 0) {
        lVar11 = 0;
      }
      plVar19 = (longlong *)(lVar11 + 4);
      if (lVar11 == 0) {
        plVar19 = &local_30;
      }
      pauVar20 = (undefined1 (*) [16])(plVar19 + -2);
      pcVar18 = "MAIN MENU";
      do {
        pauVar20 = pauVar20 + 1;
        pcVar18 = (char *)((longlong)pcVar18 + 0x10);
        vpcmpistri_avx(*pauVar20,*(undefined1 (*) [16])pcVar18,0x18);
      } while( true );
    }
    if (local_30 << 0x14 != 0) {
      uVar12 = FUN_180279c00((local_30 << 0x14) >> 0x10);
    }
    goto LAB_180208b81;
  default:
    uVar12 = FUN_18020e9b0(param_1 + 0x28e8);
    *puVar2 = 0x1311;
    *(undefined4 *)(param_1 + 0x28c9) = 5;
    *(undefined2 *)(param_1 + 0x28cd) = 0;
    *(undefined1 *)(param_1 + 0x28cf) = 0;
    *(undefined8 *)(param_1 + 0x28d2) = 0;
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      uVar12 = 0;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        uVar12 = (**(code **)(DAT_180c8df28 + 0x1ff08))
                           (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0x50,puVar2);
        return uVar12 & 0xffffffffffffff00;
      }
    }
LAB_180208b81:
    uVar12 = uVar12 & 0xffffffffffffff00;
    break;
  case 0xc:
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      local_d8[0] = 8;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xbc,local_d8);
      }
    }
    FUN_1800e1b00(6);
    FUN_1800e1b20(0x29);
    uVar12 = 1;
    break;
  case 0xe:
    FUN_1800e1b00(6);
    FUN_1800e1b20(0x2a);
    uVar12 = 1;
    break;
  case 0xf:
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      local_d8[0] = 10;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xbc,local_d8);
      }
    }
    if (*(char *)(param_1 + 0x28ce) == '\0') {
      uVar12 = (ulonglong)*(uint *)(param_1 + 0x28c0);
      FUN_180267d60(uVar12);
      uVar12 = uVar12 & 0xffffffffffffff00;
    }
    else {
      uVar12 = 1;
    }
    FUN_180267020(uVar12);
    FUN_1800e1b00(3);
    FUN_1800e1b20(0x17);
    uVar12 = 1;
    break;
  case 0x10:
    PostQuitMessage(0);
    uVar12 = 1;
  }
  return uVar12;
}
