// ===================================================
// 180085940  ->  FUN_180085940  (entree 180085940)
// ===================================================

undefined8 FUN_180085940(longlong param_1)

{
  undefined1 auVar1 [16];
  undefined1 auVar2 [32];
  
  FUN_180087550(0,&LAB_1800858a0,param_1,0);
  FUN_180087550(1,&LAB_1800858a0,param_1);
  FUN_180087550(9,&LAB_180085b00,param_1);
  FUN_180087550(10,FUN_180085a40,param_1);
  auVar1 = vpcmpeqd_avx(ZEXT416(*(uint *)(param_1 + 0x60)),ZEXT416(0x13));
  auVar1 = vblendvps_avx(ZEXT416(DAT_180350c00),ZEXT416(DAT_18034af50),auVar1);
  auVar1 = vshufps_avx(auVar1,auVar1,0);
  auVar2._16_16_ = auVar1;
  auVar2._0_16_ = auVar1;
  *(undefined1 (*) [32])(param_1 + 100) = auVar2;
  *(undefined4 *)(param_1 + 0x5c) = 0x1e;
  return 1;
}



// ===================================================
// 180085B10  ->  FUN_180085b10  (entree 180085b10)
// ===================================================

void FUN_180085b10(longlong param_1,undefined4 param_2)

{
  *(undefined4 *)(param_1 + 0x60) = param_2;
  return;
}



// ===================================================
// 1800856E0  ->  FUN_1800856e0  (entree 1800856e0)
// ===================================================

uint FUN_1800856e0(longlong param_1)

{
  float fVar1;
  float fVar2;
  float fVar3;
  uint uVar4;
  float fVar5;
  
  fVar3 = DAT_180356614;
  fVar2 = DAT_18034b3c0;
  fVar5 = *(float *)(param_1 + 0x68);
  fVar1 = *(float *)(param_1 + 100);
  if (fVar5 - fVar1 <= DAT_18034b3c0) {
    if (fVar5 - fVar1 < DAT_180356614) {
      fVar5 = fVar1 - DAT_18034b3c0;
    }
  }
  else {
    fVar5 = fVar1 + DAT_18034b3c0;
  }
  *(float *)(param_1 + 100) = fVar5;
  fVar5 = *(float *)(param_1 + 0x78);
  fVar1 = *(float *)(param_1 + 0x74);
  if (fVar5 - fVar1 <= fVar2) {
    if (fVar5 - fVar1 < fVar3) {
      fVar5 = fVar1 - fVar2;
    }
  }
  else {
    fVar5 = fVar1 + fVar2;
  }
  *(float *)(param_1 + 0x74) = fVar5;
  uVar4 = *(uint *)(param_1 + 0x5c);
  if (0 < (int)uVar4) {
    uVar4 = uVar4 - 1;
    *(uint *)(param_1 + 0x5c) = uVar4;
  }
  return uVar4 & 0xffffff00;
}



