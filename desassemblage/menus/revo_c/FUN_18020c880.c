/* FUN_18020c880  --  VF5FS+0x20c880
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18020c880.
 * Vidée le 2026-11-09.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_18020c880(longlong param_1)

{
  char cVar1;
  undefined4 uVar2;
  undefined8 uVar3;
  uint uVar4;
  char *pcVar5;
  int iVar6;
  undefined4 *puVar7;
  float fVar8;
  undefined1 auVar9 [64];
  float fVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  undefined4 local_res10;
  float local_198;
  uint local_194;
  float local_190;
  undefined4 local_188;
  undefined4 local_184;
  undefined4 local_180;
  undefined1 local_178 [8];
  uint local_170;
  undefined4 local_154;
  undefined4 local_14c;
  float local_144;
  uint local_140;
  float local_13c;
  uint local_138;
  undefined1 *local_130;
  undefined4 local_128 [9];
  undefined4 local_104;
  undefined1 local_f8 [40];
  float local_d0;
  undefined4 local_c0;
  
  if ((DAT_180c8df28 == 0) || (*(longlong *)(DAT_180c8df28 + 0x1ff08) == 0)) {
    local_128[0] = 0x17a;
    local_128[1] = 0x17b;
    local_128[2] = 0x17d;
    local_128[3] = 0x17e;
    local_128[4] = 0x17f;
    local_128[5] = 0x181;
    local_128[6] = 0x182;
    local_128[7] = 0x183;
    local_104 = 0x186;
    cVar1 = FUN_18000ba20();
    local_128[8] = 0x184;
    if (cVar1 == '\0') {
      local_128[8] = 0x185;
    }
    local_198 = 0.0;
    local_194 = 0;
    local_190 = 0.0;
    local_188 = 0;
    local_184 = 0;
    local_180 = 0;
    FUN_1801a79f0(local_178);
    FUN_1801a7b00(local_f8);
    uVar2 = FUN_180195e10();
    FUN_180196120(2);
    cVar1 = FUN_1801e0460(param_1 + 0x230);
    iVar6 = 0;
    fVar13 = 255.0;
    if (cVar1 != '\0') {
      FUN_1801df7c0(param_1 + 0x230,&local_198,"p_main_head_lt",1,0);
      FUN_1801a8890(local_f8,2);
      local_130 = local_f8;
      local_154 = 8;
      local_13c = local_198;
      local_138 = local_194;
      local_144 = local_198;
      local_140 = local_194;
      local_14c = 9;
      local_res10 = CONCAT13((char)(int)(fVar13 * local_190),0x39b7ff);
      local_170 = local_res10;
      uVar3 = FUN_1802316e0(0x179);
      FUN_1801a86c0(local_178,uVar3);
    }
    cVar1 = FUN_1801e0460(param_1 + 0x280);
    if (cVar1 != '\0') {
      FUN_1801df7c0(param_1 + 0x280,&local_198,"p_menutxt_PS3_lt",1,0);
      FUN_1801df7c0(param_1 + 0x280,&local_188,"p_menutxt_02_rb",0,0);
      FUN_1801a8890(local_f8,2);
      FUN_1801a89d0(local_f8,0x42000000);
      local_c0 = 0x41000000;
      local_130 = local_f8;
      local_154 = 0xc;
      fVar15 = local_d0 + 8.0;
      auVar9 = ZEXT464(local_194);
      if (-1 < *(int *)(param_1 + 0x214)) {
        pcVar5 = (char *)(param_1 + 0x5fa);
        puVar7 = local_128;
        fVar11 = 0.5;
        fVar12 = 10.0;
        fVar14 = 6.0;
        fVar10 = local_198;
        do {
          if (*pcVar5 != '\x02') {
            uVar3 = FUN_1802316e0(*puVar7);
            fVar8 = local_190;
            if (*pcVar5 == '\x01') {
              fVar8 = fVar11 * local_190;
            }
            if (iVar6 == *(int *)(param_1 + 0x58)) {
              FUN_1801e1080(param_1 + 0x280,fVar10 - fVar12,auVar9._0_8_,local_d0);
            }
            local_144 = fVar10 - fVar14;
            local_140 = auVar9._0_4_;
            local_14c = 9;
            uVar4 = (int)(fVar8 * fVar13) << 0x18;
            local_170 = 0x5a;
            if (iVar6 != *(int *)(param_1 + 0x58)) {
              local_170 = 0x75716e;
            }
            local_170 = local_170 | uVar4;
            local_13c = local_144;
            local_138 = local_140;
            FUN_1801a86c0(local_178,&DAT_1803758c0,uVar3);
            local_140 = auVar9._0_4_;
            local_14c = 9;
            local_170 = 0x5b5bff;
            if (iVar6 != *(int *)(param_1 + 0x58)) {
              local_170 = 0xd0c8c6;
            }
            local_170 = local_170 | uVar4;
            local_144 = fVar10;
            local_13c = fVar10;
            local_138 = local_140;
            FUN_1801a86c0(local_178,&DAT_1803758c0,uVar3);
            auVar9 = ZEXT464((uint)(auVar9._0_4_ + fVar15));
          }
          iVar6 = iVar6 + 1;
          puVar7 = puVar7 + 1;
          pcVar5 = pcVar5 + 1;
        } while (iVar6 <= *(int *)(param_1 + 0x214));
      }
    }
    FUN_180196120(uVar2);
  }
  return;
}
