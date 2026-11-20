/* FUN_18020d640  --  VF5FS+0x20d640
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18020d640.
 * Vidée le 2026-11-09.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_18020d640(longlong param_1)

{
  char cVar1;
  undefined4 uVar2;
  undefined8 uVar3;
  int iVar4;
  ulonglong uVar5;
  ulonglong uVar6;
  float fVar7;
  undefined1 auVar8 [64];
  undefined1 auVar9 [64];
  float fVar10;
  float fVar11;
  float fVar12;
  undefined4 local_res8;
  undefined4 local_res10 [2];
  uint local_128;
  float local_124;
  float local_120;
  undefined1 local_118 [8];
  uint local_110;
  undefined4 local_f4;
  undefined4 local_ec;
  uint local_e4;
  float local_e0;
  uint local_dc;
  float local_d8;
  undefined1 *local_d0;
  undefined1 local_c8 [40];
  float local_a0;
  undefined4 local_94;
  undefined4 local_90;
  
  local_res10[0] = 0x2a1;
  local_res10[1] = 0x2a2;
  local_128 = 0;
  local_124 = 0.0;
  local_120 = 0.0;
  FUN_1801a79f0(local_118);
  FUN_1801a7b00(local_c8);
  uVar2 = FUN_180195e10();
  FUN_180196120(2);
  uVar5 = 0;
  cVar1 = FUN_1801df7c0(param_1 + 0x230,&local_128,"head_tit_ct",1,0);
  auVar8 = ZEXT464(0x42000000);
  fVar11 = 255.0;
  if (cVar1 != '\0') {
    FUN_1801a8890(local_c8,2);
    FUN_1801a89d0(local_c8,auVar8._0_8_);
    local_d0 = local_c8;
    local_f4 = 0x12;
    local_dc = local_128;
    local_d8 = local_124;
    local_e4 = local_128;
    local_e0 = local_124;
    local_ec = 9;
    local_res8 = CONCAT13((char)(int)(fVar11 * local_120),0x39b7ff);
    local_110 = local_res8;
    uVar3 = FUN_1802316e0(0x17f);
    FUN_1801a86c0(local_118,uVar3);
  }
  cVar1 = FUN_1801e0460(param_1 + 0x280);
  if (cVar1 != '\0') {
    FUN_1801df7c0(param_1 + 0x280,&local_128,"p_txt_01_lt",1,0);
    FUN_1801a8890(local_c8,1);
    FUN_1801a8a10(local_c8,2);
    FUN_1801a89d0(local_c8,auVar8._0_8_);
    local_94 = 0x40400000;
    local_90 = 0x40800000;
    local_d0 = local_c8;
    local_f4 = 0x12;
    fVar12 = local_a0 + 4.0;
    auVar8 = ZEXT464(local_128);
    if (-1 < *(int *)(param_1 + 0x214)) {
      fVar10 = 0.5;
      uVar6 = uVar5;
      fVar7 = local_124;
      do {
        auVar9 = ZEXT464((uint)fVar7);
        fVar7 = local_120;
        if (*(char *)(param_1 + 0x2d1 + uVar6) == '\0') {
          if (uVar6 == 0) {
            cVar1 = FUN_1801aa9b0();
            if (cVar1 != '\0') {
              cVar1 = FUN_1801cf0c0();
              if (cVar1 != '\0') goto LAB_18020d87c;
            }
            goto LAB_18020d877;
          }
        }
        else {
LAB_18020d877:
          fVar7 = fVar7 * fVar10;
        }
LAB_18020d87c:
        iVar4 = (int)uVar5;
        if (iVar4 == *(int *)(param_1 + 0x58)) {
          FUN_1801e1080(param_1 + 0x280,auVar8._0_8_,auVar9._0_8_,local_a0);
        }
        local_e4 = auVar8._0_4_;
        local_e0 = auVar9._0_4_;
        local_ec = 9;
        local_110 = 0x5b5bff;
        if (iVar4 != *(int *)(param_1 + 0x58)) {
          local_110 = 0xd0c8c6;
        }
        local_110 = (int)(fVar7 * fVar11) << 0x18 | local_110;
        local_dc = local_e4;
        local_d8 = local_e0;
        uVar3 = FUN_1802316e0(local_res10[uVar6]);
        FUN_1801a86c0(local_118,&DAT_1803758c0,uVar3);
        fVar7 = auVar9._0_4_ + fVar12;
        uVar5 = (ulonglong)(iVar4 + 1U);
        uVar6 = uVar6 + 1;
      } while ((int)(iVar4 + 1U) <= *(int *)(param_1 + 0x214));
    }
  }
  FUN_180196120(uVar2);
  return;
}
