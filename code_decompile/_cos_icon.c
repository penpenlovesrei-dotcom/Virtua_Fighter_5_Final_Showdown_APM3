// ===================================================
// 822CD93C  ->  FUN_822cd5a8  (entree 822cd5a8)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

void FUN_822cd5a8(int param_1,ulonglong param_2)

{
  char cVar1;
  float fVar2;
  bool bVar3;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  ulonglong uVar4;
  char *pcVar9;
  int iVar10;
  undefined4 uVar11;
  uint uVar12;
  char **ppcVar13;
  char *pcVar14;
  undefined8 uVar15;
  char *apcStack_210 [12];
  undefined1 auStack_1e0 [4];
  int iStack_1dc;
  undefined4 uStack_1d8;
  undefined4 uStack_1d4;
  int aiStack_1d0 [4];
  undefined1 auStack_1c0 [4];
  uint uStack_1bc;
  undefined4 uStack_1ac;
  uint uStack_1a8;
  char *pcStack_1a4;
  char *apcStack_1a0 [4];
  int iStack_190;
  char *pcStack_18c;
  undefined4 uStack_188;
  undefined4 uStack_184;
  undefined4 uStack_178;
  undefined4 uStack_16c;
  undefined1 auStack_118 [40];
  undefined1 auStack_f0 [240];
  
  apcStack_210[1] = s_pr_personal_pla_1p_match_8208432c;
  apcStack_210[0] = s_matching_1p_82084320;
  iVar7 = (int)param_2;
  apcStack_210[8] = s_h_info_txt_2p_lt_8208430c;
  apcStack_210[9] = s_h_info_bar_2p_lt_820842f8;
  iVar8 = iVar7 * 0x14 + param_1;
  iVar10 = iVar7 * 0x28 + param_1;
  iStack_1dc = 0;
  *(undefined1 *)(iVar8 + 0xa8) = 0;
  *(undefined1 *)(iVar8 + 0xd0) = 0;
  apcStack_210[7] = s_pr_personal_pla_2p_match_820842dc;
  *(undefined1 *)(iVar10 + 0xf8) = 0;
  *(undefined1 *)(iVar10 + 0x10c) = 0;
  uStack_1d8 = 0;
  uStack_1d4 = 0;
  apcStack_210[0xb] = s_h_pr_txt_2p_low_lt_820842c8;
  apcStack_210[2] = s_h_info_txt_1p_lt_820842b4;
  apcStack_210[3] = s_h_info_bar_1p_lt_820842a0;
  apcStack_210[4] = s_h_pr_txt_1p_up_lt_8208428c;
  apcStack_210[5] = s_h_pr_txt_1p_low_lt_82084278;
  apcStack_210[6] = s_matching_2p_8208426c;
  apcStack_210[10] = s_h_pr_txt_2p_up_lt_82084258;
  if (*(int *)(((-(uint)(param_2 != 0) & 4) + 0x1b) * 4 + param_1) != 0) {
    FUN_821665d8();
    iVar6 = (int)((param_2 + (param_2 & 0x7fffffff) * 2 & 0x1fffffff) << 3);
    FUN_82166ad0(auStack_1e0,0xe2,*(undefined4 *)((int)apcStack_210 + iVar6),0x20000,9,0);
    iVar5 = FUN_82166778(auStack_1e0,*(undefined4 *)((int)apcStack_210 + iVar6 + 8));
    if (iVar5 != 0) {
      *(undefined1 *)(iVar8 + 0xa8) = 1;
      *(undefined4 *)(iVar8 + 0xac) = *(undefined4 *)(iVar5 + 0x40);
      *(undefined4 *)(iVar8 + 0xb0) = *(undefined4 *)(iVar5 + 0x44);
      *(undefined4 *)
       ((int)((param_2 + 9 + (param_2 + 9 & 0x3fffffff) * 4 & 0xffffffff) << 2) + param_1) =
           *(undefined4 *)(iVar5 + 100);
      *(undefined4 *)(iVar8 + 0xb8) = *(undefined4 *)(iVar5 + 0x60);
    }
    iVar6 = FUN_82166778(auStack_1e0,*(undefined4 *)((int)apcStack_210 + iVar6 + 0xc));
    if (iVar6 != 0) {
      *(undefined1 *)(iVar8 + 0xd0) = 1;
      *(undefined4 *)(iVar8 + 0xd4) = *(undefined4 *)(iVar6 + 0x40);
      *(undefined4 *)(iVar8 + 0xd8) = *(undefined4 *)(iVar6 + 0x44);
      *(undefined4 *)
       ((int)((param_2 + 0xb + (param_2 + 0xb & 0x3fffffff) * 4 & 0xffffffff) << 2) + param_1) =
           *(undefined4 *)(iVar6 + 100);
      *(undefined4 *)(iVar8 + 0xe0) = *(undefined4 *)(iVar6 + 0x60);
    }
    iVar6 = FUN_822977e0();
    if (*(char *)(iVar6 + 0x20) == '\0') {
      fVar2 = DAT_8200f3dc;
      if (iVar7 == 0) {
        fVar2 = DAT_8200f3e0;
      }
      *(float *)(iVar8 + 0xac) = fVar2 + *(float *)(iVar8 + 0xac);
      *(float *)(iVar8 + 0xd4) = fVar2 + *(float *)(iVar8 + 0xd4);
    }
  }
  if (*(int *)(((-(uint)(param_2 != 0) & 4) + 0x1c) * 4 + param_1) != 0) {
    uVar15 = FUN_821665d8();
    iVar7 = FUN_822977e0();
    iVar8 = (int)((param_2 + (param_2 & 0x7fffffff) * 2 & 0x1fffffff) << 3);
    FUN_82166ad0(uVar15,auStack_1e0,
                 (-(ulonglong)(*(char *)(iVar7 + 0x20) != '\0') & 0xfffffffffffffd4f) + 0x393,
                 *(undefined4 *)((int)apcStack_210 + iVar8 + 4),0x20000,9,0);
    iVar7 = FUN_82166778(auStack_1e0,*(undefined4 *)((int)apcStack_210 + iVar8 + 0x10));
    if (iVar7 != 0) {
      *(undefined1 *)(iVar10 + 0xf8) = 1;
      *(undefined4 *)(iVar10 + 0xfc) = *(undefined4 *)(iVar7 + 0x40);
      *(undefined4 *)(iVar10 + 0x100) = *(undefined4 *)(iVar7 + 0x44);
      *(undefined4 *)(iVar10 + 0x104) = *(undefined4 *)(iVar7 + 100);
      *(undefined4 *)(iVar10 + 0x108) = *(undefined4 *)(iVar7 + 0x60);
    }
    iVar8 = FUN_82166778(auStack_1e0,*(undefined4 *)((int)apcStack_210 + iVar8 + 0x14));
    if (iVar8 != 0) {
      *(undefined1 *)(iVar10 + 0x10c) = 1;
      *(undefined4 *)(iVar10 + 0x110) = *(undefined4 *)(iVar8 + 0x40);
      *(undefined4 *)(iVar10 + 0x114) = *(undefined4 *)(iVar8 + 0x44);
      *(undefined4 *)
       ((int)((param_2 + 7 + (param_2 + 7 & 0x3fffffff) * 4 & 0xffffffff) << 3) + param_1) =
           *(undefined4 *)(iVar8 + 100);
      *(undefined4 *)(iVar10 + 0x11c) = *(undefined4 *)(iVar8 + 0x60);
    }
  }
  iVar8 = FUN_822c5e70();
  if (iVar8 != 2) {
    uVar4 = FUN_821dc920();
    pcVar9 = (char *)0x0;
    iVar8 = 0;
    bVar3 = false;
    if ((uVar4 & 0xffffffff) != 0) {
      pcVar9 = (char *)FUN_821dd308(uVar4,param_2);
      iVar8 = FUN_821dd318(uVar4,param_2);
      iVar10 = (int)((param_2 + 0x52 & 0xffffffff) << 2);
      if (*(char **)(iVar10 + param_1) != pcVar9) {
        bVar3 = true;
        *(char **)(iVar10 + param_1) = pcVar9;
      }
    }
    if (bVar3) {
      apcStack_210[0] = (char *)0x0;
      apcStack_210[3] = (char *)0x1;
      pcVar14 = (char *)0x1b82;
      aiStack_1d0[0] = 9;
      apcStack_1a0[0] = s_p_cos_icon_1p_lt_82084244;
      apcStack_210[1] = (char *)0x1b82;
      apcStack_1a0[1] = s_p_cos_icon_2p_lt_82084230;
      uVar12 = 0;
      aiStack_1d0[1] = 0xd;
      apcStack_210[2] = (char *)0x1b86;
      apcStack_210[4] = (char *)0x1b83;
      apcStack_210[5] = (char *)0x1b87;
      apcStack_210[6] = (char *)0x2;
      apcStack_210[7] = (char *)0x1b84;
      apcStack_210[8] = (char *)0x1b88;
      apcStack_210[9] = (char *)0x3;
      apcStack_210[10] = (char *)0x1b85;
      apcStack_210[0xb] = (char *)0x1b89;
      ppcVar13 = apcStack_210;
      do {
        if (*ppcVar13 == pcVar9) {
          pcVar14 = ppcVar13[1];
          if (iVar8 == 1) {
            pcVar14 = ppcVar13[2];
          }
          break;
        }
        uVar12 = uVar12 + 1;
        ppcVar13 = ppcVar13 + 3;
      } while (uVar12 < 4);
      FUN_82158008(&iStack_190);
      iVar10 = FUN_822977e0();
      uStack_188 = 0;
      uStack_184 = 0;
      uStack_1ac = 0;
      uStack_1bc = uStack_1bc & 0xffffff;
      iVar8 = (int)((param_2 & 0xffffffff) << 2);
      iStack_190 = (-(uint)(*(char *)(iVar10 + 0x20) != '\0') & 0xffffff54) + 0x2c4;
      uStack_16c = 10;
      pcStack_18c = *(char **)((int)apcStack_1a0 + iVar8);
      uStack_178 = 0x20000;
      uStack_1a8 = 0xf;
      pcVar9 = pcStack_18c;
      do {
        cVar1 = *pcVar9;
        pcVar9 = pcVar9 + 1;
      } while (cVar1 != '\0');
      FUN_82141840(auStack_1c0,pcStack_18c,pcVar9 + (-1 - (int)pcStack_18c));
      pcStack_1a4 = pcVar14;
      FUN_82330798(apcStack_1a0,auStack_118,auStack_1c0);
      if (0xf < uStack_1a8) {
        thunk_FUN_82142f48(uStack_1bc);
      }
      uStack_1a8 = 0xf;
      uStack_1ac = 0;
      uStack_1bc = uStack_1bc & 0xffffff;
      uVar15 = FUN_82166880(auStack_f0,&iStack_190);
      iVar8 = (*(int *)((int)aiStack_1d0 + iVar8) + 0x14) * 4;
      if (*(int *)(iVar8 + param_1) != 0) {
        FUN_821664c0();
        *(undefined4 *)(iVar8 + param_1) = 0;
      }
      uVar11 = FUN_82166cc0(uVar15);
      *(undefined4 *)(iVar8 + param_1) = uVar11;
      FUN_82157f80(uVar15);
      FUN_82157f80(&iStack_190);
    }
  }
  if (iStack_1dc != 0) {
    FUN_82142f48();
  }
  return;
}



