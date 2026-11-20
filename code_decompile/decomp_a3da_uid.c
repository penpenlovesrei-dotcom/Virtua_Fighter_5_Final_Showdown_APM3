// ===================================================
// 180042B30  ->  FUN_180042b30  (entree 180042b30)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_180042b30(longlong param_1,undefined8 param_2,undefined1 (*param_3) [16])

{
  char *pcVar1;
  undefined1 auVar2 [16];
  ulonglong uVar3;
  undefined4 uVar4;
  uint uVar5;
  int iVar6;
  ulonglong uVar7;
  longlong lVar8;
  ulonglong *puVar9;
  ulonglong *puVar10;
  longlong lVar11;
  char *pcVar12;
  ulonglong uVar13;
  ulonglong uVar14;
  longlong *plVar15;
  ulonglong uVar16;
  ulonglong uVar17;
  undefined4 uVar18;
  char *pcVar19;
  char *pcVar20;
  ulonglong local_b0;
  char *pcStack_a8;
  char *local_a0;
  ulonglong local_98;
  char *pcStack_90;
  char *pcStack_88;
  ulonglong uStack_80;
  longlong local_78;
  longlong lStack_70;
  char *pcStack_68;
  ulonglong uStack_60;
  
  auVar2 = *param_3;
  local_a0 = *(char **)param_3[1];
  pcStack_a8 = (char *)vpextrq_avx(auVar2,1);
  if (pcStack_a8 != local_a0) {
    lVar8 = (longlong)".name" - (longlong)pcStack_a8;
    do {
      if (pcStack_a8[lVar8] == '\0') break;
      *pcStack_a8 = pcStack_a8[lVar8];
      pcStack_a8 = pcStack_a8 + 1;
    } while (pcStack_a8 != local_a0);
  }
  local_b0 = auVar2._0_8_;
  FUN_180031a20(param_2,&local_98,&local_b0);
  puVar10 = (ulonglong *)(param_1 + 0x1f8);
  if (puVar10 == &local_98) {
    if (0xf < uStack_80) {
      if (0xfff < uStack_80 + 1) {
        if (0x1f < (local_98 - *(longlong *)(local_98 - 8)) - 8) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(*(longlong *)(local_98 - 8),uStack_80 + 0x28);
        }
      }
      FUN_1802fdd80();
    }
  }
  else {
    FUN_18000de20(puVar10);
    *puVar10 = local_98;
    *(char **)(param_1 + 0x200) = pcStack_90;
    *(char **)(param_1 + 0x208) = pcStack_88;
    *(ulonglong *)(param_1 + 0x210) = uStack_80;
  }
  auVar2 = *param_3;
  local_a0 = *(char **)param_3[1];
  pcStack_a8 = (char *)vpextrq_avx(auVar2,1);
  if (pcStack_a8 != local_a0) {
    lVar8 = (longlong)".uid_name" - (longlong)pcStack_a8;
    do {
      if (pcStack_a8[lVar8] == '\0') break;
      *pcStack_a8 = pcStack_a8[lVar8];
      pcStack_a8 = pcStack_a8 + 1;
    } while (pcStack_a8 != local_a0);
  }
  local_b0 = auVar2._0_8_;
  FUN_180031a20(param_2,&local_98,&local_b0);
  puVar10 = (ulonglong *)(param_1 + 0x218);
  if (puVar10 == &local_98) {
    if (0xf < uStack_80) {
      if (0xfff < uStack_80 + 1) {
        if (0x1f < (local_98 - *(longlong *)(local_98 - 8)) - 8) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(*(longlong *)(local_98 - 8),uStack_80 + 0x28);
        }
      }
      FUN_1802fdd80();
    }
  }
  else {
    FUN_18000de20(puVar10);
    *puVar10 = local_98;
    *(char **)(param_1 + 0x220) = pcStack_90;
    *(char **)(param_1 + 0x228) = pcStack_88;
    *(ulonglong *)(param_1 + 0x230) = uStack_80;
  }
  puVar9 = puVar10;
  if (0xf < *(ulonglong *)(param_1 + 0x230)) {
    puVar9 = (ulonglong *)*puVar10;
  }
  uVar4 = FUN_1800f8b50(puVar9);
  *(undefined4 *)(param_1 + 0x2e0) = uVar4;
  puVar9 = puVar10;
  if (0xf < *(ulonglong *)(param_1 + 0x230)) {
    puVar9 = (ulonglong *)*puVar10;
  }
  lVar8 = FUN_1800124b0(puVar9,*(undefined8 *)(param_1 + 0x228),0,"_REFLECT",8);
  *(bool *)(param_1 + 0x2e4) = lVar8 != -1;
  if (0xf < *(ulonglong *)(param_1 + 0x230)) {
    puVar10 = (ulonglong *)*puVar10;
  }
  lVar8 = FUN_1800124b0(puVar10,*(undefined8 *)(param_1 + 0x228),0,"_REFRACT",8);
  *(bool *)(param_1 + 0x2e5) = lVar8 != -1;
  FUN_180042960(param_1,param_2,param_3);
  auVar2 = *param_3;
  pcVar1 = *(char **)param_3[1];
  pcVar12 = (char *)vpextrq_avx(auVar2,1);
  if (pcVar12 != pcVar1) {
    lVar8 = (longlong)".child." - (longlong)pcVar12;
    do {
      if (pcVar12[lVar8] == '\0') break;
      *pcVar12 = pcVar12[lVar8];
      pcVar12 = pcVar12 + 1;
    } while (pcVar12 != pcVar1);
  }
  local_b0 = auVar2._0_8_;
  pcStack_a8 = pcVar12;
  if (pcVar12 != pcVar1) {
    do {
      if (pcStack_a8[(longlong)"length" - (longlong)pcVar12] == '\0') break;
      *pcStack_a8 = pcStack_a8[(longlong)"length" - (longlong)pcVar12];
      pcStack_a8 = pcStack_a8 + 1;
    } while (pcStack_a8 != pcVar1);
  }
  uVar7 = local_b0;
  pcVar19 = pcVar12;
  pcVar20 = pcVar1;
  local_a0 = pcVar1;
  lVar8 = FUN_180011060(param_2,&local_b0);
  uVar14 = 0;
  uVar5 = 0;
  if (lVar8 != 0) {
    uVar5 = FUN_180014840(lVar8,10);
  }
  uVar16 = (ulonglong)uVar5;
  if ((uVar5 != 0) && (FUN_18002ec10(param_1 + 0x2c8,uVar16,param_1 + 0x2c8), uVar16 != 0)) {
    uVar13 = uVar14;
    uVar17 = uVar14;
    do {
      local_98 = uVar7;
      pcStack_90 = pcVar19;
      pcStack_88 = pcVar20;
      iVar6 = FUN_1800172b0(pcVar12,(longlong)pcVar1 - (longlong)pcVar12,&DAT_180347ce8,
                            uVar13 & 0xffffffff);
      pcStack_a8 = pcVar12 + iVar6;
      local_b0 = local_98;
      FUN_180031a20(param_2,&local_78,&local_b0);
      plVar15 = (longlong *)(*(longlong *)(param_1 + 0x2c8) + uVar17);
      if (plVar15 == &local_78) {
        if (0xf < uStack_60) {
          if (0xfff < uStack_60 + 1) {
            lVar8 = *(longlong *)(CONCAT71(local_78._1_7_,(undefined1)local_78) + -8);
            if (0x1f < (CONCAT71(local_78._1_7_,(undefined1)local_78) - lVar8) - 8U) {
                    /* WARNING: Subroutine does not return */
              FUN_180303af0(lVar8,uStack_60 + 0x28);
            }
          }
          FUN_1802fdd80();
        }
      }
      else {
        uVar3 = plVar15[3];
        if (0xf < uVar3) {
          lVar8 = *plVar15;
          lVar11 = lVar8;
          if (0xfff < uVar3 + 1) {
            lVar11 = *(longlong *)(lVar8 + -8);
            if (0x1f < (lVar8 - lVar11) - 8U) {
                    /* WARNING: Subroutine does not return */
              FUN_180303af0(lVar8 - lVar11,uVar3 + 0x28);
            }
          }
          FUN_1802fdd80(lVar11);
        }
        *plVar15 = CONCAT71(local_78._1_7_,(undefined1)local_78);
        plVar15[1] = lStack_70;
        plVar15[2] = (longlong)pcStack_68;
        plVar15[3] = uStack_60;
      }
      uVar13 = uVar13 + 1;
      uVar17 = uVar17 + 0x20;
    } while (uVar13 < uVar16);
  }
  pcStack_68 = _DAT_1803478a0;
  uStack_60 = _UNK_1803478a8;
  local_78._0_1_ = 0;
  auVar2 = *param_3;
  local_a0 = *(char **)param_3[1];
  pcStack_a8 = (char *)vpextrq_avx(auVar2,1);
  if (pcStack_a8 != local_a0) {
    lVar8 = (longlong)&DAT_18034a1cc - (longlong)pcStack_a8;
    do {
      if (pcStack_a8[lVar8] == '\0') break;
      *pcStack_a8 = pcStack_a8[lVar8];
      pcStack_a8 = pcStack_a8 + 1;
    } while (pcStack_a8 != local_a0);
  }
  local_b0 = auVar2._0_8_;
  plVar15 = (longlong *)FUN_180011060(param_2,&local_b0);
  if (plVar15 == (longlong *)0x0) {
    FUN_18000d770(&local_98,&local_78);
  }
  else {
    pcStack_88 = _DAT_1803478a0;
    uStack_80 = _UNK_1803478a8;
    local_98 = local_98 & 0xffffffffffffff00;
    FUN_180010a10(&local_98,*plVar15,plVar15[1] - *plVar15);
  }
  puVar10 = (ulonglong *)(param_1 + 0x240);
  if (puVar10 == &local_98) {
    if (0xf < uStack_80) {
      if (0xfff < uStack_80 + 1) {
        if (0x1f < (local_98 - *(longlong *)(local_98 - 8)) - 8) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(*(longlong *)(local_98 - 8),uStack_80 + 0x28);
        }
      }
      FUN_1802fdd80();
    }
  }
  else {
    uVar7 = *(ulonglong *)(param_1 + 600);
    if (0xf < uVar7) {
      uVar16 = *puVar10;
      uVar13 = uVar16;
      if (0xfff < uVar7 + 1) {
        uVar13 = *(ulonglong *)(uVar16 - 8);
        if (0x1f < (uVar16 - uVar13) - 8) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(uVar16 - uVar13,uVar7 + 0x28);
        }
      }
      FUN_1802fdd80(uVar13);
    }
    *(undefined8 *)(param_1 + 600) = 0xf;
    *puVar10 = local_98;
    *(char **)(param_1 + 0x248) = pcStack_90;
    *(char **)(param_1 + 0x250) = pcStack_88;
    *(ulonglong *)(param_1 + 600) = uStack_80;
  }
  if (0xf < uStack_60) {
    if (0xfff < uStack_60 + 1) {
      lVar8 = *(longlong *)(CONCAT71(local_78._1_7_,(undefined1)local_78) + -8);
      if (0x1f < (CONCAT71(local_78._1_7_,(undefined1)local_78) - lVar8) - 8U) {
                    /* WARNING: Subroutine does not return */
        FUN_180303af0(lVar8,uStack_60 + 0x28);
      }
    }
    FUN_1802fdd80();
  }
  auVar2 = *param_3;
  local_a0 = *(char **)param_3[1];
  pcStack_a8 = (char *)vpextrq_avx(auVar2,1);
  if (pcStack_a8 != local_a0) {
    lVar8 = (longlong)".pat_offset" - (longlong)pcStack_a8;
    do {
      if (pcStack_a8[lVar8] == '\0') break;
      *pcStack_a8 = pcStack_a8[lVar8];
      pcStack_a8 = pcStack_a8 + 1;
    } while (pcStack_a8 != local_a0);
  }
  local_b0 = auVar2._0_8_;
  lVar8 = FUN_180011060(param_2,&local_b0);
  uVar4 = 0;
  if (lVar8 == 0) {
    uVar18 = 0;
  }
  else {
    uVar18 = FUN_1800147e0(lVar8);
  }
  *(undefined4 *)(param_1 + 0x260) = uVar18;
  pcStack_68 = _DAT_1803478a0;
  uStack_60 = _UNK_1803478a8;
  local_78._0_1_ = 0;
  auVar2 = *param_3;
  local_a0 = *(char **)param_3[1];
  pcStack_a8 = (char *)vpextrq_avx(auVar2,1);
  if (pcStack_a8 != local_a0) {
    lVar8 = (longlong)".morph" - (longlong)pcStack_a8;
    do {
      if (pcStack_a8[lVar8] == '\0') break;
      *pcStack_a8 = pcStack_a8[lVar8];
      pcStack_a8 = pcStack_a8 + 1;
    } while (pcStack_a8 != local_a0);
  }
  local_b0 = auVar2._0_8_;
  plVar15 = (longlong *)FUN_180011060(param_2,&local_b0);
  if (plVar15 == (longlong *)0x0) {
    FUN_18000d770(&local_98,&local_78);
  }
  else {
    pcStack_88 = _DAT_1803478a0;
    uStack_80 = _UNK_1803478a8;
    local_98 = local_98 & 0xffffffffffffff00;
    FUN_180010a10(&local_98,*plVar15,plVar15[1] - *plVar15);
  }
  puVar10 = (ulonglong *)(param_1 + 0x270);
  if (puVar10 == &local_98) {
    if (0xf < uStack_80) {
      if (0xfff < uStack_80 + 1) {
        if (0x1f < (local_98 - *(longlong *)(local_98 - 8)) - 8) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(*(longlong *)(local_98 - 8),uStack_80 + 0x28);
        }
      }
      FUN_1802fdd80();
    }
  }
  else {
    uVar7 = *(ulonglong *)(param_1 + 0x288);
    if (0xf < uVar7) {
      uVar16 = *puVar10;
      uVar13 = uVar16;
      if (0xfff < uVar7 + 1) {
        uVar13 = *(ulonglong *)(uVar16 - 8);
        if (0x1f < (uVar16 - uVar13) - 8) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(uVar16 - uVar13,uVar7 + 0x28);
        }
      }
      FUN_1802fdd80(uVar13);
    }
    *(undefined8 *)(param_1 + 0x288) = 0xf;
    *puVar10 = local_98;
    *(char **)(param_1 + 0x278) = pcStack_90;
    *(char **)(param_1 + 0x280) = pcStack_88;
    *(ulonglong *)(param_1 + 0x288) = uStack_80;
  }
  if (0xf < uStack_60) {
    if (0xfff < uStack_60 + 1) {
      lVar8 = *(longlong *)(CONCAT71(local_78._1_7_,(undefined1)local_78) + -8);
      if (0x1f < (CONCAT71(local_78._1_7_,(undefined1)local_78) - lVar8) - 8U) {
                    /* WARNING: Subroutine does not return */
        FUN_180303af0(lVar8,uStack_60 + 0x28);
      }
    }
    FUN_1802fdd80();
  }
  auVar2 = *param_3;
  local_a0 = *(char **)param_3[1];
  pcStack_a8 = (char *)vpextrq_avx(auVar2,1);
  if (pcStack_a8 != local_a0) {
    lVar8 = (longlong)".morph_offset" - (longlong)pcStack_a8;
    do {
      if (pcStack_a8[lVar8] == '\0') break;
      *pcStack_a8 = pcStack_a8[lVar8];
      pcStack_a8 = pcStack_a8 + 1;
    } while (pcStack_a8 != local_a0);
  }
  local_b0 = auVar2._0_8_;
  lVar8 = FUN_180011060(param_2,&local_b0);
  if (lVar8 != 0) {
    uVar4 = FUN_1800147e0(lVar8);
  }
  *(undefined4 *)(param_1 + 0x290) = uVar4;
  auVar2 = *param_3;
  pcVar1 = *(char **)param_3[1];
  pcVar12 = (char *)vpextrq_avx(auVar2,1);
  if (pcVar12 != pcVar1) {
    lVar8 = (longlong)".tex_pat" - (longlong)pcVar12;
    do {
      if (pcVar12[lVar8] == '\0') break;
      *pcVar12 = pcVar12[lVar8];
      pcVar12 = pcVar12 + 1;
    } while (pcVar12 != pcVar1);
  }
  local_b0 = auVar2._0_8_;
  if (pcVar12 != pcVar1) {
    lVar8 = (longlong)&DAT_180346d24 - (longlong)pcVar12;
    do {
      if (pcVar12[lVar8] == '\0') break;
      *pcVar12 = pcVar12[lVar8];
      pcVar12 = pcVar12 + 1;
    } while (pcVar12 != pcVar1);
  }
  local_98 = local_b0;
  pcStack_a8 = pcVar12;
  if (pcVar12 != pcVar1) {
    do {
      if (pcStack_a8[(longlong)"length" - (longlong)pcVar12] == '\0') break;
      *pcStack_a8 = pcStack_a8[(longlong)"length" - (longlong)pcVar12];
      pcStack_a8 = pcStack_a8 + 1;
    } while (pcStack_a8 != pcVar1);
  }
  plVar15 = (longlong *)(param_1 + 0x298);
  pcVar19 = pcVar1;
  uVar16 = local_b0;
  pcVar20 = pcVar12;
  local_a0 = pcVar1;
  pcStack_90 = pcVar12;
  lVar8 = FUN_180011060(param_2,&local_b0);
  uVar7 = uVar14;
  if (lVar8 != 0) {
    uVar7 = FUN_180014840(lVar8,10);
  }
  uVar13 = uVar7 & 0xffffffff;
  if (((int)uVar7 != 0) && (FUN_18002ed90(plVar15,uVar13,plVar15), uVar13 != 0)) {
    uVar7 = uVar14;
    do {
      pcStack_a8 = pcVar20;
      local_b0 = uVar16;
      local_a0 = pcVar19;
      iVar6 = FUN_1800172b0(pcVar12,(longlong)pcVar1 - (longlong)pcVar12,&DAT_180347ce8,
                            uVar7 & 0xffffffff);
      pcStack_a8 = pcVar12 + iVar6;
      FUN_180043510(*plVar15 + uVar14,param_2,&local_b0);
      uVar7 = uVar7 + 1;
      uVar14 = uVar14 + 0x58;
    } while (uVar7 < uVar13);
  }
  return 1;
}



