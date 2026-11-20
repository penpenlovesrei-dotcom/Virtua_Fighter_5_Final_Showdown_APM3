// ===================================================
// 18025E830  ->  FUN_18025e830  (entree 18025e830)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18025e830(longlong param_1,float param_2,float param_3,float param_4,float param_5)

{
  longlong lVar1;
  undefined1 auVar2 [16];
  undefined1 auVar3 [16];
  float fVar4;
  float fVar5;
  float fVar6;
  undefined1 auVar7 [16];
  
  lVar1 = *(longlong *)(param_1 + 0x38);
  auVar2._4_8_ = SUB128(ZEXT812(0),4);
  auVar2._0_4_ = param_2 - DAT_180347cb0;
  auVar2._12_4_ = 0;
  auVar7._0_12_ = ZEXT812(0);
  auVar7._12_4_ = 0;
  auVar2 = vcmpss_avx(auVar7,auVar2,2);
  auVar2 = vblendvps_avx(ZEXT416((uint)param_2),
                         ZEXT416(SUB164(*(undefined1 (*) [16])(param_1 + 0x1e40),0)),auVar2);
  auVar7 = vcmpss_avx(auVar7,ZEXT416((uint)(param_3 - DAT_180347cb0)),2);
  auVar3 = vpermilps_avx(*(undefined1 (*) [16])(param_1 + 0x1e40),1);
  auVar7 = vblendvps_avx(ZEXT416((uint)param_3),ZEXT416(auVar3._0_4_),auVar7);
  auVar2 = vmaxss_avx(auVar2,ZEXT416(DAT_180346d3c));
  auVar7 = vmaxss_avx(auVar7,ZEXT416(DAT_180346d3c));
  auVar2 = vinsertps_avx(_DAT_180350990,auVar2,0);
  auVar2 = vinsertps_avx(auVar2,auVar7,0x10);
  auVar7 = vinsertps_avx(ZEXT416(0) << 0x40,ZEXT416((uint)(param_4 + param_4)),0x20);
  auVar7 = vinsertps_avx(auVar7,ZEXT416((uint)(param_5 * DAT_1803507f0)),0x30);
  auVar2 = vdivps_avx(_DAT_180348bb0,auVar2);
  auVar3 = vpslldq_avx(auVar2,8);
  fVar4 = auVar2._4_4_ * _UNK_180573164 + _UNK_180573174;
  fVar5 = auVar2._8_4_ * _UNK_180573168 + _UNK_180573178;
  fVar6 = auVar2._12_4_ * _UNK_18057316c + _UNK_18057317c;
  *(float *)(lVar1 + 0x640) =
       auVar2._0_4_ * _DAT_180573160 + _DAT_180573170 + auVar3._0_4_ * auVar7._0_4_;
  *(float *)(lVar1 + 0x644) = fVar4 + auVar3._4_4_ * auVar7._4_4_;
  *(float *)(lVar1 + 0x648) = fVar5 + auVar3._8_4_ * auVar7._8_4_;
  *(float *)(lVar1 + 0x64c) = fVar6 + auVar3._12_4_ * auVar7._12_4_;
  *(ulonglong *)(lVar1 + 8) = *(ulonglong *)(lVar1 + 8) | 0x8000000000000;
  *(undefined8 *)(lVar1 + 0x78) = 0x601f270c;
  return;
}



