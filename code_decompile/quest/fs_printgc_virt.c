// ===================================================
// 18019ADB0  ->  FUN_18019adb0  (entree 18019adb0)
// ===================================================

undefined8 *
FUN_18019adb0(longlong param_1,undefined8 *param_2,uint param_3,short *param_4,longlong param_5)

{
  float fVar1;
  int iVar2;
  ulonglong uVar3;
  longlong lVar4;
  short sVar5;
  short sVar6;
  short *psVar7;
  short *psVar8;
  float fVar9;
  float fVar10;
  undefined1 auVar11 [64];
  float fVar12;
  float fVar13;
  float fVar14;
  undefined1 auVar15 [16];
  float fVar17;
  float fVar18;
  float fVar19;
  float local_res20;
  float fStackX_24;
  undefined1 local_208 [16];
  longlong local_1f8;
  short *local_1f0;
  undefined1 local_1e8 [12];
  int local_1dc;
  int local_1d8;
  float local_1d4;
  undefined8 local_1c0;
  undefined1 local_1b8 [4];
  undefined4 local_1b4;
  uint local_1a8;
  undefined4 local_1a0;
  undefined4 local_19c;
  undefined4 local_198;
  undefined4 local_194;
  float local_184;
  float local_180;
  undefined4 local_178;
  undefined4 local_174;
  undefined1 auVar16 [64];
  
  local_1c0 = 0xfffffffffffffffe;
  auVar11 = ZEXT1264(ZEXT812(0));
  local_res20 = 0.0;
  fVar12 = 0.0;
  fStackX_24 = 0.0;
  if ((param_3 & 0x200) != 0) {
    if ((*(float *)(param_1 + 0x38) < *(float *)(param_1 + 0x18)) ||
       (*(float *)(param_1 + 0x18) + *(float *)(param_1 + 0x20) <
        *(float *)(param_1 + 0x38) + *(float *)(*(longlong *)(param_1 + 0x48) + 0x28))) {
      *param_2 = 0;
      return param_2;
    }
  }
  local_208 = (undefined1  [16])0x0;
  psVar7 = (short *)0x0;
  local_1f8 = 0;
  local_1f0 = param_4 + (param_5 - (longlong)param_4 >> 1);
  FUN_18019ab60(local_208,0x100);
  fVar14 = *(float *)(param_1 + 0x34);
  fVar19 = *(float *)(param_1 + 0x38);
  fVar10 = *(float *)(*(longlong *)(param_1 + 0x48) + 0x2c);
  fVar18 = *(float *)(*(longlong *)(param_1 + 0x48) + 0x34) / fVar10;
  fVar17 = 0.0;
  fVar13 = 0.0;
  if ((param_3 & 0x200) != 0) {
    fVar13 = *(float *)(param_1 + 0x14) - fVar14;
    fVar17 = fVar13 / fVar10;
    fVar13 = (fVar13 + *(float *)(param_1 + 0x1c)) / fVar10;
  }
  auVar15._0_12_ = ZEXT812(0);
  auVar15._12_4_ = 0;
  auVar16 = ZEXT1664(auVar15);
  sVar6 = 0;
  psVar8 = psVar7;
  if (param_4 != param_4 + (param_5 - (longlong)param_4 >> 1)) {
    do {
      sVar5 = *param_4;
      iVar2 = FUN_180019ab0(sVar5);
      if (iVar2 != 0) {
        FUN_18019b3c0(*(undefined8 *)(param_1 + 0x48),local_1e8,sVar5);
        auVar15 = auVar16._0_16_;
        if (sVar6 != 0) {
          local_res20 = auVar11._0_4_ + fVar18;
          auVar11 = ZEXT464((uint)local_res20);
        }
        fVar10 = local_1d4;
        if (((param_3 & 0x200) == 0) ||
           ((fVar9 = auVar11._0_4_, fVar17 <= fVar9 && (local_1d4 + fVar9 <= fVar13)))) {
          if (sVar5 == 0x20) {
            psVar7 = (short *)0x0;
            psVar8 = param_4;
          }
          else if (psVar8 != (short *)0x0) {
            psVar7 = (short *)(ulonglong)((int)psVar7 + 1);
          }
          FUN_18019b4a0(local_208,param_3 & 0xe00,&local_res20,local_1e8,
                        *(undefined4 *)(param_1 + 8));
LAB_18019b046:
          auVar11 = ZEXT464((uint)(auVar11._0_4_ + fVar10));
        }
        else {
          if ((param_3 >> 0xb & 1) == 0) {
LAB_18019b003:
            if (fVar9 <= fVar13) goto LAB_18019b046;
            break;
          }
          if ((param_3 >> 0xc & 1) != 0) {
            if (sVar5 == 0x20) {
              param_4 = param_4 + 1;
              psVar7 = (short *)0x0;
              psVar8 = param_4;
            }
            else if (psVar8 != (short *)0x0) {
              if ((int)psVar7 != 0) {
                local_208._8_8_ = local_208._8_8_ + (longlong)psVar7 * -0x60;
              }
              psVar7 = (short *)0x0;
              param_4 = psVar8 + 1;
              psVar8 = param_4;
            }
          }
          lVar4 = *(longlong *)(param_1 + 0x48);
          fVar1 = *(float *)(lVar4 + 0x38) + *(float *)(lVar4 + 0x28);
          if (*(float *)(param_1 + 0x20) < fVar1 + fVar12) goto LAB_18019b003;
          auVar15 = vmaxss_avx(auVar11._0_16_,auVar15);
          auVar16 = ZEXT1664(auVar15);
          auVar11 = ZEXT1264(ZEXT812(0));
          fVar12 = fVar12 + fVar1 / *(float *)(lVar4 + 0x30);
          param_4 = param_4 + -1;
          sVar5 = 0;
          fStackX_24 = fVar12;
        }
        local_res20 = auVar11._0_4_;
      }
      sVar6 = sVar5;
      auVar15 = auVar16._0_16_;
      param_4 = param_4 + 1;
    } while (param_4 != local_1f0);
    fVar10 = auVar11._0_4_;
    if (auVar15._0_4_ < fVar10) goto LAB_18019b071;
  }
  fVar10 = auVar15._0_4_;
LAB_18019b071:
  fVar13 = DAT_180346d38;
  lVar4 = *(longlong *)(param_1 + 0x48);
  fVar10 = fVar10 * *(float *)(lVar4 + 0x2c);
  fVar12 = fVar12 * *(float *)(lVar4 + 0x30) + *(float *)(lVar4 + 0x28);
  local_res20 = fVar10;
  fStackX_24 = fVar12;
  if ((param_3 & 1) == 0) {
    if ((param_3 & 2) == 0) {
      if ((param_3 & 4) == 0) {
        if ((param_3 & 8) != 0) {
          fVar14 = fVar14 - fVar10 * DAT_180346d38;
        }
      }
      else if ((param_3 & 0x200) == 0) {
        FUN_18016aec0(local_1e8,*(undefined4 *)(param_1 + 0x2c));
        fVar14 = (float)local_1dc * fVar13 - fVar10 * fVar13;
      }
      else {
        fVar14 = (DAT_180346d38 * *(float *)(param_1 + 0x1c) + *(float *)(param_1 + 0x14)) -
                 fVar10 * DAT_180346d38;
      }
    }
    else {
      fVar14 = fVar14 - fVar10;
    }
  }
  else {
    *(float *)(param_1 + 0x34) = fVar10 + *(float *)(param_1 + 0x34);
  }
  if ((param_3 & 0x10) == 0) {
    if ((param_3 & 0x20) != 0) {
      fVar19 = fVar19 - fVar13 * *(float *)(*(longlong *)(param_1 + 0x48) + 0x28);
    }
  }
  else if ((param_3 & 0x200) == 0) {
    FUN_18016aec0(local_1e8,*(undefined4 *)(param_1 + 0x2c));
    fVar19 = (float)local_1d8 * fVar13 - fVar12 * fVar13;
  }
  else {
    fVar19 = (fVar13 * *(float *)(param_1 + 0x20) + *(float *)(param_1 + 0x18)) - fVar12 * fVar13;
  }
  if (local_208._0_8_ != local_208._8_8_) {
    FUN_180189880(local_1b8);
    lVar4 = *(longlong *)(param_1 + 0x48);
    local_1b4 = **(undefined4 **)(lVar4 + 8);
    local_178 = *(undefined4 *)(lVar4 + 0x2c);
    local_174 = *(undefined4 *)(lVar4 + 0x30);
    local_1a8 = *(uint *)(param_1 + 0x30) >> 3 & 2;
    local_198 = *(undefined4 *)(param_1 + 0x2c);
    local_19c = *(undefined4 *)(param_1 + 0x24);
    local_1a0 = *(undefined4 *)(param_1 + 0x28);
    local_194 = local_198;
    local_184 = fVar14;
    local_180 = fVar19;
    FUN_18018e620(local_1b8,local_208._0_8_,(longlong)(local_208._8_8_ - local_208._0_8_) / 0x18);
    FUN_180187c00(local_1b8);
  }
  *param_2 = CONCAT44(fStackX_24,local_res20);
  if (local_208._0_8_ != 0) {
    uVar3 = ((local_1f8 - local_208._0_8_) / 0x18) * 0x18;
    lVar4 = local_208._0_8_;
    if (0xfff < uVar3) {
      lVar4 = *(longlong *)(local_208._0_8_ + -8);
      if (0x1f < (local_208._0_8_ - lVar4) - 8U) {
                    /* WARNING: Subroutine does not return */
        FUN_180303af0(local_1f8 - local_208._0_8_,uVar3 + 0x27);
      }
    }
    FUN_1802fdd80(lVar4);
  }
  return param_2;
}



// ===================================================
// 180199FB0  ->  FUN_180199fb0  (entree 180199fb0)
// ===================================================

longlong FUN_180199fb0(uint param_1)

{
  uint uVar1;
  
  uVar1 = 0;
  if (param_1 < 3) {
    uVar1 = param_1;
  }
  return DAT_180750ff8 + (longlong)(int)uVar1 * 0x18 + 0x98;
}



