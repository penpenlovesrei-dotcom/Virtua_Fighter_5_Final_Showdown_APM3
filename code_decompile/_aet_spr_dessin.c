// ===================================================
// 180023BAA  ->  FUN_180023930  (entree 180023930)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_180023930(longlong param_1,undefined8 *param_2,longlong param_3,ulonglong param_4,
                  float param_5)

{
  uint uVar1;
  int iVar2;
  uint *puVar3;
  char *pcVar4;
  longlong lVar5;
  longlong lVar6;
  char *pcVar7;
  uint *puVar8;
  char *pcVar9;
  float fVar10;
  float fVar11;
  undefined1 extraout_var [56];
  undefined1 extraout_var_00 [56];
  undefined1 auVar12 [16];
  undefined1 auVar13 [16];
  undefined4 local_128;
  uint local_124;
  uint local_120;
  uint local_11c;
  undefined4 local_118;
  undefined4 local_114;
  undefined4 local_110;
  undefined4 local_10c;
  undefined4 local_108;
  undefined4 local_104;
  undefined8 local_100;
  undefined4 local_f8;
  undefined8 local_f4;
  undefined4 local_ec;
  undefined8 local_e8;
  undefined4 local_e0;
  undefined8 local_dc;
  undefined4 local_d4;
  undefined8 uStack_d0;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined1 local_80;
  undefined1 local_7f;
  undefined4 local_7c;
  undefined8 local_78;
  undefined8 local_70;
  undefined4 local_68;
  undefined8 local_64;
  undefined4 local_5c;
  undefined8 local_58;
  undefined8 uStack_50;
  undefined8 local_48;
  
  pcVar7 = (char *)0x0;
  pcVar9 = pcVar7;
  if (*(int *)(param_3 + 0x18) != 0) {
    pcVar9 = (char *)(param_3 + 0x18 + (longlong)*(int *)(param_3 + 0x18));
  }
  FUN_180189880(&local_128);
  fVar10 = DAT_180346d4c;
  pcVar4 = pcVar7;
  if (*(int *)(pcVar9 + 0x10) != 0) {
    pcVar4 = pcVar9 + (longlong)*(int *)(pcVar9 + 0x10) + 0x10;
  }
  local_124 = *(uint *)(pcVar4 + (param_4 & 0xffffffff) * 8 + 4);
  puVar3 = *(uint **)(param_1 + 0x200);
  puVar8 = *(uint **)(param_1 + 0x1f8);
  lVar6 = (longlong)puVar3 - (longlong)puVar8 >> 3;
  while (lVar5 = lVar6, 0 < lVar5) {
    lVar6 = lVar5 >> 1;
    if (puVar8[lVar6 * 2] < local_124) {
      puVar8 = puVar8 + lVar6 * 2 + 2;
      lVar6 = lVar5 + (-1 - lVar6);
    }
  }
  if ((puVar8 == puVar3) || (local_124 < *puVar8)) {
    puVar8 = puVar3;
  }
  if ((puVar8 != puVar3) && (puVar8[1] != 0xffffffff)) {
    local_124 = puVar8[1];
  }
  local_c8 = *param_2;
  uStack_c0 = param_2[1];
  uStack_b8 = param_2[2];
  uStack_b0 = param_2[3];
  local_a8 = param_2[4];
  uStack_a0 = param_2[5];
  uStack_98 = param_2[6];
  uStack_90 = param_2[7];
  local_114 = *(undefined4 *)(param_1 + 0x34);
  local_110 = *(undefined4 *)(param_1 + 0x38);
  local_10c = *(undefined4 *)(param_1 + 0x3c);
  local_120 = (((int)(longlong)(param_5 * *(float *)(param_1 + 0x84) * DAT_180346d4c) << 8 |
               (uint)(longlong)(DAT_180346d4c * *(float *)(param_1 + 0x78)) & 0xff) << 8 |
              (uint)(longlong)(DAT_180346d4c * *(float *)(param_1 + 0x7c)) & 0xff) << 8 |
              (uint)(longlong)(DAT_180346d4c * *(float *)(param_1 + 0x80)) & 0xff;
  local_108 = *(undefined4 *)(param_1 + 0x8c);
  uVar1 = *(uint *)(param_1 + 0x30);
  if ((uVar1 >> 0x12 & 1) != 0) {
    local_11c = local_11c | 0x10000;
  }
  if ((uVar1 >> 0x13 & 1) != 0) {
    local_11c = local_11c | 0x20000;
  }
  if ((uVar1 >> 0x15 & 1) != 0) {
    local_11c = local_11c | 0x10000000;
  }
  iVar2 = *(int *)(param_3 + 0x28);
  pcVar4 = pcVar7;
  pcVar9 = pcVar7;
  if (iVar2 != 0) {
    pcVar4 = (char *)(longlong)iVar2;
    pcVar9 = (char *)(longlong)iVar2 + param_3 + 0x28;
  }
  if (*pcVar9 == '\a') {
    local_118 = 1;
  }
  pcVar9 = pcVar7;
  if (iVar2 != 0) {
    pcVar9 = pcVar4 + param_3 + 0x28;
  }
  if (*pcVar9 == '\x05') {
    local_118 = 2;
  }
  if (iVar2 != 0) {
    pcVar7 = pcVar4 + param_3 + 0x28;
  }
  if (*pcVar7 == '\x06') {
    local_118 = 3;
  }
  local_104 = local_108;
  if (*(char *)(param_1 + 0x9c) == '\0') {
    pcVar4 = pcVar4 + param_3 + 0x2a;
    if (iVar2 == 0) {
      pcVar4 = (char *)0x2;
    }
    if (*pcVar4 == '\0') {
      fVar10 = (float)FUN_180211bf0(&local_c8);
      auVar12._0_8_ = (double)fVar10;
      auVar12._8_8_ = extraout_var._0_8_;
      auVar13 = vandpd_avx(auVar12,_DAT_180346d50);
      if (DAT_180346d34 < (float)auVar13._0_8_) {
        FUN_180187c00(&local_128);
      }
    }
    else {
      *(float *)(param_1 + 0x188) = param_5;
      *(undefined1 *)(param_1 + 0x9c) = 1;
      FUN_18018c6b0((undefined4 *)(param_1 + 0xa0));
      *(undefined4 *)(param_1 + 0xa0) = local_128;
      *(uint *)(param_1 + 0xa4) = local_124;
      *(uint *)(param_1 + 0xa8) = local_120;
      *(uint *)(param_1 + 0xac) = local_11c;
      *(undefined4 *)(param_1 + 0xb0) = local_118;
      *(undefined4 *)(param_1 + 0xb4) = local_114;
      *(undefined4 *)(param_1 + 0xb8) = local_110;
      *(undefined4 *)(param_1 + 0xbc) = local_10c;
      *(undefined4 *)(param_1 + 0xc0) = local_108;
      *(undefined4 *)(param_1 + 0xc4) = local_104;
      *(undefined8 *)(param_1 + 200) = local_100;
      *(undefined4 *)(param_1 + 0xd0) = local_f8;
      *(undefined8 *)(param_1 + 0xd4) = local_f4;
      *(undefined4 *)(param_1 + 0xdc) = local_ec;
      *(undefined8 *)(param_1 + 0xe0) = local_e8;
      *(undefined4 *)(param_1 + 0xe8) = local_e0;
      *(undefined8 *)(param_1 + 0xec) = local_dc;
      *(undefined4 *)(param_1 + 0xf4) = local_d4;
      *(undefined8 *)(param_1 + 0xf8) = uStack_d0;
      *(undefined8 *)(param_1 + 0x100) = local_c8;
      *(undefined8 *)(param_1 + 0x108) = uStack_c0;
      *(undefined8 *)(param_1 + 0x110) = uStack_b8;
      *(undefined8 *)(param_1 + 0x118) = uStack_b0;
      *(undefined8 *)(param_1 + 0x120) = local_a8;
      *(undefined8 *)(param_1 + 0x128) = uStack_a0;
      *(undefined8 *)(param_1 + 0x130) = uStack_98;
      *(undefined4 *)(param_1 + 0x138) = (undefined4)uStack_90;
      *(undefined4 *)(param_1 + 0x13c) = uStack_90._4_4_;
      *(undefined8 *)(param_1 + 0x140) = local_88;
      *(undefined1 *)(param_1 + 0x148) = local_80;
      *(undefined1 *)(param_1 + 0x149) = local_7f;
      *(undefined4 *)(param_1 + 0x14c) = local_7c;
      *(undefined8 *)(param_1 + 0x150) = local_78;
      *(undefined8 *)(param_1 + 0x158) = local_70;
      *(undefined4 *)(param_1 + 0x160) = local_68;
      *(undefined8 *)(param_1 + 0x164) = local_64;
      *(undefined4 *)(param_1 + 0x16c) = local_5c;
      *(undefined8 *)(param_1 + 0x180) = local_48;
      *(undefined8 *)(param_1 + 0x170) = local_58;
      *(undefined8 *)(param_1 + 0x178) = uStack_50;
    }
  }
  else {
    *(undefined1 *)(param_1 + 0x9c) = 0;
    fVar11 = (float)FUN_180211bf0(&local_c8);
    auVar13._0_8_ = (double)fVar11;
    auVar13._8_8_ = extraout_var_00._0_8_;
    auVar13 = vandpd_avx(auVar13,_DAT_180346d50);
    if (DAT_180346d34 < (float)auVar13._0_8_) {
      *(uint *)(param_1 + 0xa8) =
           (((int)(longlong)
                  (param_5 * *(float *)(param_1 + 0x84) * *(float *)(param_1 + 0x188) * fVar10) << 8
            | (uint)(longlong)(fVar10 * *(float *)(param_1 + 0x78)) & 0xff) << 8 |
           (uint)(longlong)(fVar10 * *(float *)(param_1 + 0x7c)) & 0xff) << 8 |
           (uint)(longlong)(fVar10 * *(float *)(param_1 + 0x80)) & 0xff;
      lVar6 = FUN_180187c00(param_1 + 0xa0);
      lVar5 = FUN_180187c00(&local_128);
      if ((lVar5 != 0) && (lVar6 != 0)) {
        FUN_18018e5f0(lVar5,lVar6);
      }
    }
  }
  return;
}



