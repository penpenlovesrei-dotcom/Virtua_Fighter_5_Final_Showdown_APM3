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



// ===================================================
// 180085760  ->  FUN_180085760  (entree 180085760)
// ===================================================

undefined1 FUN_180085760(longlong param_1)

{
  FUN_180087420(0,&LAB_1800858a0,param_1);
  FUN_180087420(1,&LAB_1800858a0,param_1);
  FUN_180087420(9,&LAB_180085b00,param_1);
  FUN_180087420(10,FUN_180085a40,param_1);
  *(undefined4 *)(param_1 + 100) = 0x3a83126f;
  *(undefined4 *)(param_1 + 0x68) = 0x3a83126f;
  *(undefined4 *)(param_1 + 0x6c) = 0x3a83126f;
  *(undefined4 *)(param_1 + 0x70) = 0x3a83126f;
  *(undefined4 *)(param_1 + 0x74) = 0x3a83126f;
  *(undefined4 *)(param_1 + 0x78) = 0x3a83126f;
  *(undefined4 *)(param_1 + 0x7c) = 0x3a83126f;
  *(undefined4 *)(param_1 + 0x80) = 0x3a83126f;
  *(undefined4 *)(param_1 + 0x60) = 0xffffffff;
  return 1;
}



// ===================================================
// 180085800  ->  FUN_180085800  (entree 180085800)
// ===================================================

void FUN_180085800(longlong param_1)

{
  undefined8 uVar1;
  longlong lVar2;
  longlong lVar3;
  
  if (*(char *)(param_1 + 0x58) != '\0') {
    uVar1 = FUN_1801509b0();
    lVar2 = FUN_1801509e0(uVar1,0);
    lVar3 = FUN_1801509e0(uVar1,1);
    if (lVar2 != 0) {
      if (*(int *)(param_1 + 0x5c) < 1) {
        *(undefined4 *)(lVar2 + 0xe0) = *(undefined4 *)(param_1 + 100);
      }
      else {
        *(undefined4 *)(lVar2 + 0xe0) = 0x3f000000;
      }
    }
    if (lVar3 != 0) {
      if (0 < *(int *)(param_1 + 0x5c)) {
        *(undefined4 *)(lVar3 + 0xe0) = 0x3f000000;
        return;
      }
      *(undefined4 *)(lVar3 + 0xe0) = *(undefined4 *)(param_1 + 0x74);
    }
  }
  return;
}



// ===================================================
// 180085BA0  ->  FUN_180085ba0  (entree 180085ba0)
// ===================================================

void FUN_180085ba0(longlong param_1)

{
  *(undefined4 *)(param_1 + 0x68) = *(undefined4 *)(param_1 + 0x6c);
  *(undefined4 *)(param_1 + 100) = *(undefined4 *)(param_1 + 0x6c);
  *(undefined4 *)(param_1 + 0x78) = *(undefined4 *)(param_1 + 0x7c);
  *(undefined4 *)(param_1 + 0x74) = *(undefined4 *)(param_1 + 0x7c);
  return;
}



// ===================================================
// 180085B70  ->  FUN_180085b70  (entree 180085b70)
// ===================================================

void FUN_180085b70(longlong param_1)

{
  *(undefined4 *)(param_1 + 0x68) = *(undefined4 *)(param_1 + 0x70);
  *(undefined4 *)(param_1 + 100) = *(undefined4 *)(param_1 + 0x70);
  *(undefined4 *)(param_1 + 0x78) = *(undefined4 *)(param_1 + 0x80);
  *(undefined4 *)(param_1 + 0x74) = *(undefined4 *)(param_1 + 0x80);
  return;
}



// ===================================================
// 1800858A0  ->  FUN_1800858a0  (entree 1800858a0)
// ===================================================

void FUN_1800858a0(longlong param_1,char *param_2)

{
  int iVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  longlong lVar5;
  
  fVar4 = DAT_18034b8a8;
  fVar3 = DAT_18034b3ec;
  fVar2 = DAT_180346d3c;
  lVar5 = (longlong)*param_2;
  iVar1 = *(int *)(param_1 + 0x60);
  if (iVar1 != 4) {
    if (iVar1 == 8) {
      fVar3 = *(float *)(param_1 + 0x68 + lVar5 * 0x10) + DAT_18034a514;
      *(float *)(param_1 + 0x68 + lVar5 * 0x10) = fVar3;
      if (fVar3 <= fVar2) {
        return;
      }
      *(undefined4 *)(param_1 + 0x68 + lVar5 * 0x10) = 0x3f800000;
      return;
    }
    if (iVar1 != 0x13) {
      if (iVar1 != 0x15) {
        return;
      }
      fVar2 = *(float *)(param_1 + 0x68 + lVar5 * 0x10) + DAT_180356610;
      *(float *)(param_1 + 0x68 + lVar5 * 0x10) = fVar2;
      if (fVar2 <= fVar4) {
        return;
      }
      *(undefined4 *)(param_1 + 0x68 + lVar5 * 0x10) = 0x3f19999a;
      return;
    }
  }
  fVar2 = *(float *)(param_1 + 0x68 + lVar5 * 0x10) + DAT_18034a514;
  *(float *)(param_1 + 0x68 + lVar5 * 0x10) = fVar2;
  if (fVar3 < fVar2) {
    *(undefined4 *)(param_1 + 0x68 + lVar5 * 0x10) = 0x3f4ccccd;
  }
  return;
}



// ===================================================
// 180085A40  ->  FUN_180085a40  (entree 180085a40)
// ===================================================

void FUN_180085a40(longlong param_1)

{
  undefined1 auVar1 [16];
  float fVar2;
  char cVar3;
  char cVar4;
  undefined8 uVar5;
  undefined1 auVar6 [16];
  undefined1 auVar7 [16];
  
  uVar5 = FUN_1801509b0();
  cVar3 = FUN_1801501c0(uVar5,0);
  cVar4 = FUN_1801501c0(uVar5,1);
  fVar2 = DAT_18034b8a8;
  auVar7 = ZEXT416(DAT_180346d3c);
  if ((cVar3 != '\0') && ((*(int *)(param_1 + 0x60) - 8U < 3 || (*(int *)(param_1 + 0x60) == 0x17)))
     ) {
    auVar6 = ZEXT416((uint)(DAT_18034b8a8 + *(float *)(param_1 + 0x68)));
    auVar1 = vcmpss_avx(auVar7,auVar6,1);
    auVar1 = vblendvps_avx(auVar6,auVar7,auVar1);
    *(int *)(param_1 + 0x68) = auVar1._0_4_;
  }
  *(undefined4 *)(param_1 + 0x70) = *(undefined4 *)(param_1 + 0x68);
  if ((cVar4 != '\0') && ((*(int *)(param_1 + 0x60) - 8U < 3 || (*(int *)(param_1 + 0x60) == 0x17)))
     ) {
    auVar6 = ZEXT416((uint)(fVar2 + *(float *)(param_1 + 0x78)));
    auVar1 = vcmpss_avx(auVar7,auVar6,1);
    auVar7 = vblendvps_avx(auVar6,auVar7,auVar1);
    *(int *)(param_1 + 0x78) = auVar7._0_4_;
  }
  *(undefined4 *)(param_1 + 0x80) = *(undefined4 *)(param_1 + 0x78);
  return;
}



