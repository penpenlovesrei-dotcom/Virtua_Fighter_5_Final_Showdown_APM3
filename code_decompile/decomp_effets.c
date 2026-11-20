// ===================================================
// 18006B880  ->  FUN_18006b880  (entree 18006b880)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

ulonglong FUN_18006b880(longlong param_1)

{
  longlong lVar1;
  float fVar2;
  undefined1 auVar3 [16];
  bool bVar4;
  char cVar5;
  int iVar6;
  undefined4 uVar7;
  undefined8 uVar8;
  ulonglong uVar9;
  undefined8 uVar10;
  char *pcVar11;
  int iVar12;
  float extraout_XMM0_Da;
  undefined1 auVar13 [64];
  undefined1 auVar14 [16];
  undefined1 auVar15 [64];
  undefined8 local_res8;
  undefined4 local_168 [2];
  char *local_160;
  undefined1 local_158 [16];
  undefined4 local_148;
  undefined4 local_144;
  undefined4 local_140;
  undefined4 local_13c;
  undefined4 local_138;
  undefined4 local_134;
  undefined4 local_130;
  undefined1 local_12c;
  undefined8 local_128;
  undefined4 local_120;
  undefined8 local_11c;
  undefined4 local_114;
  undefined8 local_110;
  undefined4 local_108;
  undefined8 local_104;
  undefined4 local_fc;
  undefined4 local_f8;
  undefined8 local_f4;
  undefined8 uStack_ec;
  undefined8 local_e0;
  undefined1 local_d8 [16];
  undefined1 local_c0;
  undefined7 uStack_bf;
  undefined8 local_b0;
  ulonglong local_a8;
  undefined8 local_a0;
  undefined1 local_98 [16];
  undefined4 local_80;
  undefined1 local_78 [16];
  longlong local_68;
  undefined1 local_58;
  undefined8 local_48;
  
  local_48 = 0xfffffffffffffffe;
  bVar4 = true;
  auVar13 = ZEXT464(DAT_180346d3c);
  auVar15 = ZEXT1264(ZEXT812(0));
  iVar12 = 0;
  if ((*(char *)(param_1 + 0x70) != '\0') && (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0)) {
    local_res8 = 0;
    if ((*(code **)(DAT_180c3b6f0 + 0x1fe10) == (code *)0x0) ||
       (iVar6 = (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                          (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0xb,&local_res8), iVar6 != 1)) {
      if (((*(char *)(param_1 + 0x71) == '\0') && ((char)local_res8 == '\x02')) &&
         (fVar2 = *(float *)(param_1 + 0x68) - auVar13._0_4_, *(float *)(param_1 + 0x68) = fVar2,
         fVar2 < auVar15._0_4_)) {
        cVar5 = FUN_180029fb0();
        uVar10 = 4;
        if (cVar5 != '\0') {
          uVar10 = 2;
        }
        iVar6 = FUN_1801a2c10(uVar10);
        pcVar11 = "rom/sound/voice/sega441.adx";
        if (iVar6 < 0) {
          pcVar11 = "rom/sound/bgm/vfes_se_logo_sega.adx";
        }
        FUN_180185da0(0,pcVar11,0);
        *(undefined1 *)(param_1 + 0x71) = 1;
      }
      bVar4 = false;
    }
  }
  switch(*(undefined4 *)(param_1 + 0x58)) {
  case 0:
    FUN_180187ab0();
    cVar5 = (**(code **)(*DAT_180c3b6f8 + 0x1a0))();
    if (cVar5 == '\0') {
      if (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) == 0) {
        FUN_180187c50(0x266);
        FUN_180029c20(0x206);
      }
      else {
        if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
          (**(code **)(DAT_180c3b6f0 + 0x1fe10))(*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),9);
        }
        if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
          (**(code **)(DAT_180c3b6f0 + 0x1fe10))(*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0x28);
          *(undefined4 *)(param_1 + 0x58) = 1;
          break;
        }
      }
    }
    *(undefined4 *)(param_1 + 0x58) = 1;
    break;
  case 1:
    cVar5 = (**(code **)(*DAT_180c3b6f8 + 0x1a0))();
    if (cVar5 == '\0') {
      if (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0) {
        if (((*(code **)(DAT_180c3b6f0 + 0x1fe10) == (code *)0x0) ||
            (iVar12 = (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                                (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),10), iVar12 != 2)) &&
           ((*(code **)(DAT_180c3b6f0 + 0x1fe10) == (code *)0x0 ||
            (iVar12 = (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                                (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0x29), iVar12 != 2)))) {
          *(undefined4 *)(param_1 + 0x68) = 0x42700000;
          *(undefined1 *)(param_1 + 0x70) = 1;
          *(undefined4 *)(param_1 + 0x58) = 2;
        }
        break;
      }
      cVar5 = FUN_180187cc0(0x266);
      if ((cVar5 != '\0') || (cVar5 = FUN_180029d40(0x206), cVar5 != '\0')) break;
      local_e0 = 0;
      local_d8 = (undefined1  [16])0x0;
      local_b0 = 0;
      local_a8 = 0xf;
      local_c0 = 0;
      local_a0 = 0;
      local_98 = (undefined1  [16])0x0;
      local_78 = (undefined1  [16])0x0;
      local_68 = 0;
      local_160 = (char *)0x0;
      local_158 = (undefined1  [16])0x0;
      local_148 = DAT_180347cd8;
      local_144 = DAT_180347cd8;
      local_13c = 0xffffffff;
      local_138 = 0;
      local_134 = 7;
      local_130 = 9;
      local_120 = auVar15._0_4_;
      auVar14 = auVar15._0_16_;
      auVar3 = vunpcklps_avx(auVar14,auVar14);
      local_128 = auVar3._0_8_;
      auVar3 = vunpcklps_avx(auVar14,auVar14);
      local_11c = auVar3._0_8_;
      local_108 = auVar13._0_4_;
      auVar3 = vunpcklps_avx(auVar13._0_16_,auVar13._0_16_);
      local_110 = auVar3._0_8_;
      auVar3 = vunpcklps_avx(auVar14,auVar14);
      local_104 = auVar3._0_8_;
      local_f4 = _DAT_180348bb0;
      uStack_ec = _UNK_180348bb8;
      local_80 = 1;
      local_58 = 0;
      local_12c = 1;
      local_168[0] = 0x2a1;
      local_140 = 0x20000;
      local_114 = local_120;
      local_fc = local_120;
      local_f8 = local_108;
      iVar12 = FUN_1802447c0();
      local_158._0_8_ = "SEGA_s";
      if (iVar12 == 0) {
        local_160 = "logo_jpn";
        *(undefined4 *)(param_1 + 0x68) = 0x44214000;
      }
      else {
        local_160 = "logo_usu";
        *(undefined4 *)(param_1 + 0x68) = 0x43838000;
        if (iVar12 == 1) {
          local_158._0_8_ = "REATING_s";
        }
      }
      *(char **)(param_1 + 0x60) = local_160;
      local_158._8_8_ = "SEGA_e";
      if (DAT_180c3b701 == '\0') {
        local_158._8_8_ = "INFO_end";
      }
      uVar7 = FUN_180029a90(local_168);
      *(undefined4 *)(param_1 + 0x5c) = uVar7;
      if (local_78._0_8_ != 0) {
        uVar9 = local_68 - local_78._0_8_ & 0xfffffffffffffff8;
        if (0xfff < uVar9) {
          if (0x1f < (local_78._0_8_ - *(longlong *)(local_78._0_8_ + -8)) - 8U) {
                    /* WARNING: Subroutine does not return */
            FUN_180303af0(*(longlong *)(local_78._0_8_ + -8),uVar9 + 0x27);
          }
        }
        FUN_1802fdd80();
        local_78 = (undefined1  [16])0x0;
        local_68 = 0;
      }
      FUN_18000e060(&local_a0);
      if (0xf < local_a8) {
        if (0xfff < local_a8 + 1) {
          lVar1 = *(longlong *)(CONCAT71(uStack_bf,local_c0) + -8);
          if (0x1f < (CONCAT71(uStack_bf,local_c0) - lVar1) - 8U) {
                    /* WARNING: Subroutine does not return */
            FUN_180303af0(lVar1,local_a8 + 0x28);
          }
        }
        FUN_1802fdd80();
      }
      local_b0 = 0;
      local_a8 = 0xf;
      local_c0 = 0;
      FUN_180034fa0(&local_e0);
    }
    *(undefined4 *)(param_1 + 0x58) = 2;
    break;
  case 2:
    FUN_1801efb10();
    FUN_18019a730();
    FUN_180187c50(10);
    FUN_180187c50(0);
    FUN_180029c20(1);
    FUN_180187c50(0x263);
    FUN_180187c50(0x265);
    FUN_180029c20(0x205);
    FUN_180044540();
    *(undefined4 *)(param_1 + 0x58) = 3;
    break;
  case 3:
    cVar5 = FUN_1801efdd0();
    if ((((((cVar5 != '\0') || (cVar5 = FUN_18019a870(), cVar5 != '\0')) ||
          (cVar5 = FUN_180187cc0(10), cVar5 != '\0')) ||
         ((cVar5 = FUN_180187cc0(0), cVar5 != '\0' || (cVar5 = FUN_180029d40(1), cVar5 != '\0'))))
        || (cVar5 = FUN_180187cc0(0x263), cVar5 != '\0')) ||
       (((cVar5 = FUN_180187cc0(0x265), cVar5 != '\0' ||
         (cVar5 = FUN_180029d40(0x205), cVar5 != '\0')) || (cVar5 = FUN_180046800(), cVar5 != '\0'))
       )) break;
    cVar5 = (**(code **)(*DAT_180c3b6f8 + 0x1a0))();
    if (cVar5 == '\0') {
      *(undefined4 *)(param_1 + 0x58) = 4;
      FUN_1801bdb60(param_1 + 0x6c);
      break;
    }
    goto LAB_18006c344;
  case 4:
    FUN_1800f9c60(0x14,0x180000001);
    FUN_1800f9c60(0x15,1);
    FUN_18003c200("EFFEFFCMN");
    FUN_1800e7140(0x18);
    FUN_180159ed0(0x18);
    FUN_18008a0f0();
    FUN_180050740();
    FUN_18014be80();
    FUN_18003c200("STGCMN");
    FUN_18003c200("NAGE_VF4");
    FUN_180185a60("rom/sound/se_system.csb");
    FUN_180185a60("rom/sound/se_fd.csb");
    FUN_180185a60("rom/sound/se_satellite.csb");
    FUN_180185a60("rom/sound/se_cs.csb");
    if (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0) {
      FUN_180185a60("rom/sound/se_adam.csb");
    }
    _guard_check_icall();
    _guard_check_icall();
    FUN_180091ee0();
    FUN_180092550();
    _guard_check_icall();
    *(undefined4 *)(param_1 + 0x58) = 5;
    break;
  case 5:
    cVar5 = FUN_1800fb7e0(0x14,0x180000001);
    if ((((((cVar5 != '\0') || (cVar5 = FUN_1800fb7e0(0x15,1), cVar5 != '\0')) ||
          (cVar5 = FUN_18003c1d0("EFFEFFCMN"), cVar5 == '\0')) ||
         ((cVar5 = FUN_1800e5e50(0x18), cVar5 != '\0' ||
          (cVar5 = FUN_1801599d0(0x18), cVar5 != '\0')))) ||
        (((cVar5 = FUN_18008a220(), cVar5 != '\0' ||
          ((cVar5 = FUN_180050a30(), cVar5 != '\0' || (cVar5 = FUN_18014e420(), cVar5 != '\0')))) ||
         ((cVar5 = FUN_18003c1d0("STGCMN"), cVar5 == '\0' ||
          (((cVar5 = FUN_18003c1d0("NAGE_VF4"), cVar5 == '\0' ||
            (cVar5 = FUN_180186d70("rom/sound/se_system.csb"), cVar5 != '\0')) ||
           (cVar5 = FUN_180186d70("rom/sound/se_fd.csb"), cVar5 != '\0')))))))) ||
       ((((cVar5 = FUN_180186d70("rom/sound/se_satellite.csb"), cVar5 != '\0' ||
          (cVar5 = FUN_180186d70("rom/sound/se_cs.csb"), cVar5 != '\0')) ||
         ((*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0 &&
          (cVar5 = FUN_180186d70("rom/sound/se_adam.csb"), cVar5 != '\0')))) ||
        (((cVar5 = FUN_180007450(), cVar5 != '\0' || (cVar5 = FUN_1800932b0(), cVar5 != '\0')) ||
         (cVar5 = FUN_180007450(), cVar5 != '\0')))))) break;
    thunk_FUN_180217900();
    _guard_check_icall();
    _guard_check_icall();
    uVar10 = DAT_18070fb10;
    do {
      uVar8 = FUN_180091650(iVar12);
      FUN_180101ba0(uVar10,iVar12,uVar8);
      iVar12 = iVar12 + 1;
    } while (iVar12 < 0x15);
    FUN_1800d4610();
    iVar12 = FUN_180007440();
    if (iVar12 == 0) {
      *(undefined4 *)(param_1 + 0x58) = 6;
      break;
    }
    if (iVar12 == 2) {
      *(undefined4 *)(param_1 + 0x58) = 8;
      break;
    }
    if (iVar12 == 3) {
      *(undefined4 *)(param_1 + 0x58) = 10;
      break;
    }
    goto LAB_18006c344;
  case 6:
    FUN_180099390();
    FUN_1800af4b0();
    FUN_1800af640();
    FUN_180187c50(0x1d);
    FUN_180029c20(0xf1);
    FUN_180187c50(0x160);
    FUN_180029c20(0x12f);
    FUN_180187c50(0x12e);
    FUN_180029c20(0xf6);
    FUN_180187c50(299);
    FUN_180029c20(0xf2);
    FUN_1801b73b0();
    *(undefined4 *)(param_1 + 0x58) = 7;
    break;
  case 7:
    cVar5 = FUN_180187cc0(0x1d);
    if (((cVar5 != '\0') || (cVar5 = FUN_180029d40(0xf1), cVar5 != '\0')) ||
       ((((cVar5 = FUN_180187cc0(0x160), cVar5 != '\0' ||
          ((cVar5 = FUN_180029d40(0x12f), cVar5 != '\0' ||
           (cVar5 = FUN_180187cc0(0x12e), cVar5 != '\0')))) ||
         (cVar5 = FUN_180029d40(0xf6), cVar5 != '\0')) ||
        ((((cVar5 = FUN_180187cc0(299), cVar5 != '\0' ||
           (cVar5 = FUN_180029d40(0xf2), cVar5 != '\0')) ||
          (cVar5 = thunk_FUN_180217bf0(), cVar5 != '\0')) ||
         (cVar5 = FUN_1800af620(), cVar5 != '\0')))))) break;
    FUN_1800af9c0();
    if (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) == 0) {
      cVar5 = FUN_180029770(*(undefined4 *)(param_1 + 0x5c));
      if (cVar5 == '\0') break;
      FUN_1801be500(param_1 + 0x6c);
    }
    else if ((!bVar4) ||
            ((((cVar5 = (**(code **)*DAT_180c3b6f8)(), cVar5 == '\0' || (DAT_180c3bdd8 == 0)) ||
              ((*(char *)(DAT_180c3bdd8 + 0x18) == '\0' ||
               ((*(longlong *)(DAT_180c3bdd8 + 0x10) == 0 ||
                (cVar5 = FUN_1802c8b00(), cVar5 == '\0')))))) &&
             (*(int *)(param_1 + 0x74) = *(int *)(param_1 + 0x74) + -1, 0 < *(int *)(param_1 + 0x74)
             )))) break;
    goto LAB_18006c344;
  case 8:
    FUN_180187c50(0xc);
    FUN_180187c50(0x15);
    FUN_180029c20(0x85);
    FUN_180185a60("rom/sound/se_tv_cmn.csb");
    *(undefined4 *)(param_1 + 0x58) = 9;
    break;
  case 9:
    cVar5 = FUN_180187cc0(0xc);
    if ((((cVar5 != '\0') || (cVar5 = FUN_180187cc0(0x15), cVar5 != '\0')) ||
        (cVar5 = FUN_180029d40(0x85), cVar5 != '\0')) ||
       (cVar5 = FUN_180186d70("rom/sound/se_tv_cmn.csb"), cVar5 != '\0')) break;
    goto LAB_18006c344;
  case 10:
    FUN_180099390();
    FUN_1800993e0();
    FUN_180029c20(0x133);
    FUN_180187c50(0x28);
    FUN_180187c50(0xc);
    FUN_180185a60("rom/sound/se_terminal.csb");
    *(undefined4 *)(param_1 + 0x58) = 0xb;
    break;
  case 0xb:
    cVar5 = FUN_180029d40(0x133);
    if (((cVar5 != '\0') || (cVar5 = FUN_180187cc0(0x28), cVar5 != '\0')) ||
       ((cVar5 = FUN_180187cc0(0xc), cVar5 != '\0' ||
        ((cVar5 = FUN_180186d70("rom/sound/se_terminal.csb"), cVar5 != '\0' ||
         (cVar5 = thunk_FUN_180217bf0(), cVar5 != '\0')))))) break;
    FUN_18009c3d0();
LAB_18006c344:
    *(undefined4 *)(param_1 + 0x58) = 0xc;
  }
  uVar9 = DAT_180c3b6f0;
  if ((((*(longlong *)(DAT_180c3b6f0 + 0x1fe10) == 0) &&
       (auVar15._0_4_ < *(float *)(param_1 + 0x68))) && (*(int *)(param_1 + 0x5c) != 0)) &&
     (uVar9 = FUN_180029780(), *(float *)(param_1 + 0x68) < extraout_XMM0_Da)) {
    uVar9 = FUN_1801a2c10(6);
    if (-1 < (int)uVar9) {
      uVar9 = FUN_180185da0(0,"rom/sound/voice/sega441.adx",0);
    }
    *(undefined4 *)(param_1 + 0x68) = 0xbf800000;
  }
  return uVar9 & 0xffffffffffffff00;
}



