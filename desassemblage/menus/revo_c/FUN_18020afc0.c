/* FUN_18020afc0  --  VF5FS+0x20afc0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18020afc0.
 * Vidée le 2026-11-09.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_18020afc0(longlong param_1)

{
  char cVar1;
  undefined4 uVar2;
  uint uVar3;
  undefined8 uVar4;
  int iVar5;
  ulonglong uVar6;
  ulonglong uVar7;
  float fVar8;
  undefined1 auVar9 [64];
  undefined1 auVar10 [64];
  float fVar11;
  float fVar12;
  float fVar13;
  undefined4 local_res8;
  uint local_138;
  float local_134;
  float local_130;
  undefined4 local_128 [4];
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
  
  local_128[0] = 0x1a2;
  local_128[1] = 0x1a3;
  local_128[2] = 0x1a4;
  local_128[3] = 0x1a5;
  local_138 = 0;
  local_134 = 0.0;
  local_130 = 0.0;
  FUN_1801a79f0(local_118);
  FUN_1801a7b00(local_c8);
  uVar2 = FUN_180195e10();
  FUN_180196120(2);
  uVar6 = 0;
  cVar1 = FUN_1801df7c0(param_1 + 0x230,&local_138,"head_tit_ct",1,0);
  auVar9 = ZEXT464(0x42000000);
  fVar12 = 255.0;
  if (cVar1 != '\0') {
    FUN_1801a8890(local_c8,2);
    FUN_1801a89d0(local_c8,auVar9._0_8_);
    local_d0 = local_c8;
    local_f4 = 0x12;
    local_dc = local_138;
    local_d8 = local_134;
    local_e4 = local_138;
    local_e0 = local_134;
    local_ec = 9;
    local_res8 = CONCAT13((char)(int)(fVar12 * local_130),0x39b7ff);
    local_110 = local_res8;
    uVar4 = FUN_1802316e0(0x17a);
    FUN_1801a86c0(local_118,uVar4);
  }
  cVar1 = FUN_1801e0460(param_1 + 0x280);
  if (cVar1 != '\0') {
    FUN_1801df7c0(param_1 + 0x280,&local_138,"p_txt_01_lt",1,0);
    FUN_1801a8890(local_c8,1);
    FUN_1801a8a10(local_c8,2);
    FUN_1801a89d0(local_c8,auVar9._0_8_);
    local_94 = 0x40400000;
    local_90 = 0x40800000;
    local_d0 = local_c8;
    local_f4 = 0x12;
    fVar13 = local_a0 + 4.0;
    auVar9 = ZEXT464(local_138);
    if (-1 < *(int *)(param_1 + 0x214)) {
      fVar11 = 0.5;
      uVar7 = uVar6;
      fVar8 = local_134;
      do {
        auVar10 = ZEXT464((uint)fVar8);
        fVar8 = local_130;
        if (*(char *)(param_1 + 0x2d1 + uVar7) == '\0') {
          if (uVar7 == 3) {
            cVar1 = FUN_1801aa970();
            if (cVar1 == '\0') goto LAB_18020b1ff;
          }
        }
        else {
LAB_18020b1ff:
          fVar8 = fVar8 * fVar11;
        }
        iVar5 = (int)uVar6;
        if (iVar5 == *(int *)(param_1 + 0x58)) {
          FUN_1801e1080(param_1 + 0x280,auVar9._0_8_,auVar10._0_8_,local_a0);
        }
        local_dc = auVar9._0_4_;
        local_d8 = auVar10._0_4_;
        local_e4 = auVar9._0_4_;
        local_e0 = auVar10._0_4_;
        local_ec = 9;
        uVar3 = 0x5b5bff;
        if (iVar5 != *(int *)(param_1 + 0x58)) {
          uVar3 = 0xd0c8c6;
        }
        local_110 = (int)(fVar8 * fVar12) << 0x18 | uVar3;
        uVar4 = FUN_1802316e0(local_128[uVar7]);
        FUN_1801a86c0(local_118,&DAT_1803758c0,uVar4);
        fVar8 = auVar10._0_4_ + fVar13;
        uVar6 = (ulonglong)(iVar5 + 1U);
        uVar7 = uVar7 + 1;
      } while ((int)(iVar5 + 1U) <= *(int *)(param_1 + 0x214));
    }
  }
  FUN_180196120(uVar2);
  return;
}
