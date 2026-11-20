/* FUN_18020d2f0  --  VF5FS+0x20d2f0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18020d2f0.
 * Vidée le 2026-11-09.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_18020d2f0(longlong param_1)

{
  char cVar1;
  undefined4 uVar2;
  uint uVar3;
  undefined8 uVar4;
  int iVar5;
  char *pcVar6;
  undefined4 *puVar7;
  undefined4 uVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  undefined1 auVar12 [64];
  float fVar13;
  float fVar14;
  undefined4 local_res8;
  uint local_138;
  float local_134;
  float local_130;
  undefined4 local_128 [4];
  undefined1 local_118 [40];
  float local_f0;
  undefined4 local_e4;
  float local_e0;
  undefined1 local_d8 [8];
  uint local_d0;
  undefined4 local_b4;
  undefined4 local_ac;
  uint local_a4;
  float local_a0;
  uint local_9c;
  float local_98;
  undefined1 *local_90;
  
  local_128[0] = 0x1c1;
  local_128[1] = 0x1c2;
  local_128[2] = 0x1c3;
  local_138 = 0;
  local_134 = 0.0;
  local_130 = 0.0;
  FUN_1801a79f0(local_d8);
  FUN_1801a7b00(local_118);
  uVar2 = FUN_180195e10();
  FUN_180196120(2);
  cVar1 = FUN_1801e0460(param_1 + 0x230);
  if (cVar1 == '\0') {
    uVar4 = 0;
  }
  else {
    iVar5 = 0;
    FUN_1801df7c0(param_1 + 0x230,&local_138,"p_small_head_lt",1,0);
    FUN_1801a8890(local_118,1);
    FUN_1801a8a10(local_118,2);
    FUN_1801a89d0(local_118,0x42000000);
    uVar8 = 0x40400000;
    local_e4 = 0x40400000;
    fVar11 = 4.0;
    local_e0 = 4.0;
    local_90 = local_118;
    local_b4 = 0x12;
    local_9c = local_138;
    local_98 = local_134;
    local_a4 = local_138;
    local_a0 = local_134;
    local_ac = 9;
    fVar14 = 255.0;
    local_res8 = CONCAT13((char)(int)(local_130 * 255.0),0x39b7ff);
    local_d0 = local_res8;
    uVar4 = FUN_1802316e0(0x1a3);
    FUN_1801a86c0(local_d8,uVar4);
    FUN_1801df7c0(param_1 + 0x230,&local_138,"p_txt_01_lt",0,0);
    FUN_1801a8890(local_118,1);
    FUN_1801a8a10(local_118,2);
    FUN_1801a89d0(local_118,0x42000000);
    local_e4 = uVar8;
    local_e0 = fVar11;
    local_90 = local_118;
    local_b4 = 0x12;
    fVar11 = local_f0 + fVar11;
    auVar12 = ZEXT464(local_138);
    if (-1 < *(int *)(param_1 + 0x214)) {
      puVar7 = local_128;
      pcVar6 = (char *)(param_1 + 0x281);
      fVar13 = 0.5;
      fVar9 = local_134;
      do {
        fVar10 = local_130;
        if (*pcVar6 != '\0') {
          fVar10 = local_130 * fVar13;
        }
        if (iVar5 == *(int *)(param_1 + 0x58)) {
          FUN_1801e1080(param_1 + 0x230,auVar12._0_8_,fVar9);
        }
        local_9c = auVar12._0_4_;
        local_98 = fVar9;
        local_a4 = auVar12._0_4_;
        local_a0 = fVar9;
        local_ac = 9;
        uVar3 = 0x5b5bff;
        if (iVar5 != *(int *)(param_1 + 0x58)) {
          uVar3 = 0xd0c8c6;
        }
        local_d0 = (int)(fVar10 * fVar14) << 0x18 | uVar3;
        uVar4 = FUN_1802316e0(*puVar7);
        FUN_1801a86c0(local_d8,&DAT_1803758c0,uVar4);
        fVar9 = fVar9 + fVar11;
        iVar5 = iVar5 + 1;
        pcVar6 = pcVar6 + 1;
        puVar7 = puVar7 + 1;
      } while (iVar5 <= *(int *)(param_1 + 0x214));
    }
    FUN_18020e140(param_1,local_d8,local_118);
    uVar4 = 1;
  }
  FUN_180026200(*(undefined4 *)(param_1 + 0x284),uVar4);
  FUN_180196120(uVar2);
  return;
}
