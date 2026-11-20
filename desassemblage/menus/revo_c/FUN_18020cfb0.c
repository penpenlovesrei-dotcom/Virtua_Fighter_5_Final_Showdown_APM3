/* FUN_18020cfb0  --  VF5FS+0x20cfb0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18020cfb0.
 * Vidée le 2026-11-09.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_18020cfb0(longlong param_1)

{
  char cVar1;
  undefined4 uVar2;
  uint uVar3;
  undefined8 uVar4;
  ulonglong uVar5;
  int iVar6;
  ulonglong uVar7;
  float fVar8;
  float fVar9;
  undefined1 auVar10 [64];
  undefined1 auVar11 [64];
  undefined4 uVar12;
  float fVar13;
  float fVar14;
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
  float local_90;
  
  local_128[0] = 0x2a3;
  local_128[1] = 0x2a4;
  local_128[2] = 0x2a5;
  local_138 = 0;
  local_134 = 0.0;
  local_130 = 0.0;
  FUN_1801a79f0(local_118);
  FUN_1801a7b00(local_c8);
  uVar2 = FUN_180195e10();
  FUN_180196120(2);
  cVar1 = FUN_1801e0460(param_1 + 0x230);
  uVar5 = 0;
  auVar10 = ZEXT464(0x42000000);
  uVar12 = 0x40400000;
  fVar8 = 4.0;
  fVar14 = 255.0;
  if (cVar1 != '\0') {
    FUN_1801df7c0(param_1 + 0x230,&local_138,"p_small_head_lt",1,0);
    FUN_1801a8890(local_c8,1);
    FUN_1801a8a10(local_c8,2);
    FUN_1801a89d0(local_c8,auVar10._0_8_);
    local_d0 = local_c8;
    local_f4 = 0x12;
    local_dc = local_138;
    local_d8 = local_134;
    local_e4 = local_138;
    local_e0 = local_134;
    local_ec = 9;
    local_res8 = CONCAT13((char)(int)(fVar14 * local_130),0x39b7ff);
    local_110 = local_res8;
    local_94 = uVar12;
    local_90 = fVar8;
    uVar4 = FUN_1802316e0(0x2a2);
    FUN_1801a86c0(local_118,uVar4);
  }
  cVar1 = FUN_1801e0460(param_1 + 0x280);
  if (cVar1 != '\0') {
    FUN_1801df7c0(param_1 + 0x280,&local_138,"p_txt_01_lt",1,0);
    FUN_1801a8890(local_c8,1);
    FUN_1801a8a10(local_c8,2);
    FUN_1801a89d0(local_c8,auVar10._0_8_);
    local_94 = uVar12;
    local_90 = fVar8;
    local_d0 = local_c8;
    local_f4 = 0x12;
    fVar8 = fVar8 + local_a0;
    auVar10 = ZEXT464(local_138);
    fVar9 = fVar8 + local_134;
    if (-1 < *(int *)(param_1 + 0x214)) {
      fVar13 = 0.5;
      uVar7 = uVar5;
      do {
        auVar11 = ZEXT464((uint)fVar9);
        fVar9 = local_130;
        if (*(char *)(param_1 + 0x2d3 + uVar5) == '\0') {
          if (uVar5 == 0) {
            cVar1 = FUN_1801cf0c0();
            if (cVar1 == '\0') goto LAB_18020d20e;
          }
        }
        else {
LAB_18020d20e:
          fVar9 = fVar9 * fVar13;
        }
        iVar6 = (int)uVar7;
        if (iVar6 == *(int *)(param_1 + 0x58)) {
          FUN_1801e1080(param_1 + 0x280,auVar10._0_8_,auVar11._0_8_,local_a0);
        }
        local_dc = auVar10._0_4_;
        local_d8 = auVar11._0_4_;
        local_e4 = auVar10._0_4_;
        local_e0 = auVar11._0_4_;
        local_ec = 9;
        uVar3 = 0x5b5bff;
        if (iVar6 != *(int *)(param_1 + 0x58)) {
          uVar3 = 0xd0c8c6;
        }
        local_110 = (int)(fVar9 * fVar14) << 0x18 | uVar3;
        uVar4 = FUN_1802316e0(local_128[uVar5]);
        FUN_1801a86c0(local_118,&DAT_1803758c0,uVar4);
        fVar9 = auVar11._0_4_ + fVar8;
        uVar7 = (ulonglong)(iVar6 + 1U);
        uVar5 = uVar5 + 1;
      } while ((int)(iVar6 + 1U) <= *(int *)(param_1 + 0x214));
    }
  }
  FUN_180196120(uVar2);
  return;
}
