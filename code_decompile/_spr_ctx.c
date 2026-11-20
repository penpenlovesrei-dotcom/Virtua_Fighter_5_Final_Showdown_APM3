// ===================================================
// 18018C7D0  ->  FUN_18018c7d0  (entree 18018c7d0)
// ===================================================

void FUN_18018c7d0(longlong param_1,uint param_2)

{
  longlong lVar1;
  undefined4 *puVar2;
  uint uVar3;
  undefined1 auVar4 [16];
  undefined1 auVar5 [16];
  undefined1 auVar6 [16];
  undefined1 local_248 [16];
  undefined8 local_238;
  undefined **local_228;
  longlong local_220;
  undefined1 local_218 [16];
  undefined4 local_208;
  undefined1 local_200 [144];
  undefined1 local_170;
  undefined1 local_168;
  undefined7 uStack_167;
  undefined8 local_158;
  ulonglong local_150;
  undefined1 local_148 [16];
  undefined8 local_138;
  undefined4 local_130;
  uint local_128 [2];
  undefined1 local_120 [264];
  
  local_238 = 0xfffffffffffffffe;
  uVar3 = 0;
  if (param_2 != 0) {
    do {
      local_228 = SPRSET::vftable;
      FUN_1802161d0(local_200);
      local_158 = 0;
      local_150 = 0xf;
      local_168 = 0;
      local_220 = (ulonglong)uVar3 << 0x20;
      local_218 = (undefined1  [16])0x0;
      local_208 = 0;
      local_170 = 0;
      local_148 = (undefined1  [16])0x0;
      local_138 = 0;
      local_130 = 0;
      local_128[0] = uVar3;
      FUN_180189790(local_120,&local_228);
      lVar1 = FUN_180187ed0(param_1,local_128);
      FUN_180188690(param_1,local_248,0,lVar1 + 0x20,lVar1);
      FUN_180189b30(local_120);
      local_228 = SPRSET::vftable;
      local_220 = 0;
      local_218 = (undefined1  [16])0x0;
      local_208 = 0;
      local_170 = 0;
      if (0xf < local_150) {
        if (0xfff < local_150 + 1) {
          lVar1 = *(longlong *)(CONCAT71(uStack_167,local_168) + -8);
          if (0x1f < (CONCAT71(uStack_167,local_168) - lVar1) - 8U) {
                    /* WARNING: Subroutine does not return */
            FUN_180303af0(lVar1,local_150 + 0x28);
          }
        }
        FUN_1802fdd80();
      }
      local_158 = 0;
      local_150 = 0xf;
      local_168 = 0;
      FUN_1802163b0(local_200);
      uVar3 = uVar3 + 1;
    } while (uVar3 < param_2);
  }
  *(undefined4 *)(param_1 + 0x828) = 0;
  *(undefined4 *)(param_1 + 0x82c) = 0x11;
  puVar2 = (undefined4 *)FUN_18016b0c0();
  auVar6._0_12_ = ZEXT812(0);
  auVar6._12_4_ = 0;
  auVar4._8_8_ = 0;
  auVar4._0_8_ = *(ulonglong *)(puVar2 + 6);
  auVar4 = vcvtpd2ps_avx(auVar4);
  *(int *)(param_1 + 0x810) = auVar4._0_4_;
  *(undefined4 *)(param_1 + 0x814) = *puVar2;
  auVar5._0_4_ = (float)(int)puVar2[4];
  auVar5._4_8_ = SUB128(ZEXT812(0),4);
  auVar5._12_4_ = 0;
  auVar4 = vinsertps_avx(auVar6,auVar6,0x10);
  auVar4 = vinsertps_avx(auVar4,ZEXT416((uint)(float)(int)puVar2[3]),0x20);
  auVar4 = vinsertps_avx(auVar4,auVar5,0x30);
  *(undefined1 (*) [16])(param_1 + 0x818) = auVar4;
  return;
}



