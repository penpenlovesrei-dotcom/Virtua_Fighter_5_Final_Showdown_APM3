/* FUN_18020dc80  --  VF5FS+0x20dc80
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18020dc80.
 * Vidée le 2026-11-09.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_18020dc80(longlong param_1)

{
  longlong lVar1;
  char cVar2;
  undefined8 uVar3;
  char *pcVar4;
  size_t sVar5;
  uint uVar6;
  char *pcVar7;
  int *piVar8;
  int iVar9;
  char *_Str;
  float fVar10;
  undefined1 extraout_var [56];
  float fVar11;
  undefined1 auVar12 [64];
  undefined1 auVar13 [64];
  float fVar14;
  float fVar15;
  undefined1 auVar16 [64];
  float fVar17;
  undefined8 local_res8;
  undefined4 local_res10;
  uint local_168;
  float local_164;
  float local_160;
  uint local_158 [4];
  undefined1 local_148 [8];
  uint local_140;
  undefined4 local_124;
  undefined4 local_11c;
  uint local_114;
  float local_110;
  uint local_10c;
  float local_108;
  undefined1 *local_100;
  int local_f8 [8];
  undefined1 local_d8 [40];
  float local_b0;
  undefined4 local_a4;
  undefined4 local_a0;
  
  local_f8[0] = 0x1b1;
  local_f8[1] = 0x1ad;
  local_f8[2] = 0x1cf;
  local_f8[3] = 0x1d4;
  local_f8[4] = 0x1d9;
  local_168 = 0;
  local_164 = 0.0;
  local_160 = 0.0;
  local_158[0] = 0;
  local_158[1] = 0;
  local_158[2] = 0;
  FUN_1801a79f0(local_148);
  FUN_1801a7b00(local_d8);
  local_res10 = FUN_180195e10();
  FUN_180196120(2);
  pcVar4 = (char *)0x0;
  cVar2 = FUN_1801df7c0(param_1 + 0x248,&local_168,"head_tit_ct",1,0);
  auVar12 = ZEXT464(0x42000000);
  fVar14 = 255.0;
  if (cVar2 != '\0') {
    FUN_1801a8890(local_d8,2);
    FUN_1801a89d0(local_d8,auVar12._0_8_);
    local_100 = local_d8;
    local_124 = 0x12;
    local_10c = local_168;
    local_108 = local_164;
    local_114 = local_168;
    local_110 = local_164;
    local_11c = 9;
    local_res8._0_4_ = CONCAT13((char)(int)(fVar14 * local_160),0x39b7ff);
    local_140 = (uint)local_res8;
    uVar3 = FUN_1802316e0(0x17b);
    FUN_1801a86c0(local_148,uVar3);
  }
  lVar1 = param_1 + 0x298;
  cVar2 = FUN_1801e0460(lVar1);
  if (cVar2 != '\0') {
    FUN_1801df7c0(lVar1,&local_168,"p_txt_01_lt",1,0);
    FUN_1801df7c0(lVar1,local_158,"p_txt_03_rt",0,0);
    FUN_1801a8890(local_d8,1);
    FUN_1801a8a10(local_d8,2);
    FUN_1801a89d0(local_d8,auVar12._0_8_);
    auVar12 = ZEXT464(0x40400000);
    uVar3 = auVar12._0_8_;
    local_a4 = 0x40400000;
    local_a0 = 0x40800000;
    local_100 = local_d8;
    local_124 = 0x12;
    auVar16 = ZEXT464((uint)local_164);
    fVar17 = local_b0 + 4.0;
    auVar13 = ZEXT464(local_168);
    if (-1 < *(int *)(param_1 + 0x214)) {
      piVar8 = local_f8;
      pcVar7 = (char *)(param_1 + 0x2ea);
      local_res8 = param_1 - (longlong)local_f8;
      fVar15 = 0.5;
      _Str = pcVar4;
      fVar11 = local_164;
      fVar10 = local_b0;
      do {
        iVar9 = (int)pcVar4;
        if ((iVar9 == *(int *)(param_1 + 0x58)) && (*(char *)(param_1 + 0x2e9) != '\0')) {
          FUN_1801e1080(param_1 + 0x298,auVar13._0_8_,fVar11,fVar10);
          auVar12 = ZEXT464((uint)(local_b0 * fVar15));
          auVar16 = ZEXT464((uint)(local_b0 * fVar15 + fVar11));
          fVar10 = local_b0;
        }
        if (iVar9 < 5) {
          if ((*pcVar7 != '\0') || (fVar10 = local_160, *(char *)(param_1 + 0x2e9) == '\0')) {
            fVar10 = fVar15 * local_160;
          }
          local_114 = auVar13._0_4_;
          local_11c = 9;
          if ((iVar9 == *(int *)(param_1 + 0x58)) && (*(char *)(param_1 + 0x2e9) != '\0')) {
            uVar6 = (int)(fVar10 * fVar14) << 0x18;
            local_140 = uVar6 | 0x5b5bff;
          }
          else {
            uVar6 = (int)(fVar10 * fVar14) << 0x18;
            local_140 = uVar6 | 0xd0c8c6;
          }
          local_110 = fVar11;
          local_10c = local_114;
          local_108 = fVar11;
          uVar3 = FUN_1802316e0(*piVar8);
          FUN_1801a86c0(local_148,&DAT_1803758c0,uVar3);
          pcVar4 = (char *)FUN_1802316e0(*(int *)(local_res8 + 0x230 + (longlong)piVar8) + 1 +
                                         *piVar8);
          local_11c = 9;
          local_10c = local_158[0];
          local_114 = local_158[0];
          if ((iVar9 == *(int *)(param_1 + 0x58)) &&
             (_Str = pcVar4, *(char *)(param_1 + 0x2e9) != '\0')) {
            local_140 = uVar6 | 0x5b5bff;
          }
          else {
            local_140 = uVar6 | 0xd0c8c6;
          }
          local_110 = fVar11;
          local_108 = fVar11;
          auVar12._0_8_ = FUN_1801a86a0(local_148,2,&DAT_1803758c0,pcVar4);
          auVar12._8_56_ = extraout_var;
          fVar10 = local_b0;
        }
        uVar3 = auVar12._0_8_;
        fVar11 = fVar11 + fVar17;
        pcVar4 = (char *)(ulonglong)(iVar9 + 1U);
        pcVar7 = pcVar7 + 1;
        piVar8 = piVar8 + 1;
      } while ((int)(iVar9 + 1U) <= *(int *)(param_1 + 0x214));
      if ((_Str != (char *)0x0) && (*(char *)(param_1 + 0x2e9) != '\0')) {
        sVar5 = strlen(_Str);
        FUN_1801a8a60(local_148,&local_res8,_Str,sVar5,0xbf800000);
        FUN_1801e0c60(param_1 + 0x2f0,local_158[0],auVar16._0_8_,4,0x12,(uint)local_res8);
        goto LAB_18020e0f3;
      }
    }
    FUN_1801e10c0(uVar3);
  }
LAB_18020e0f3:
  FUN_180196120(local_res10);
  return;
}
