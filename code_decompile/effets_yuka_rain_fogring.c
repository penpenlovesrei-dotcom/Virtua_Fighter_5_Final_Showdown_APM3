// ===================================================
// 1800860C0  ->  FUN_1800860c0  (entree 1800860c0)
// ===================================================

undefined1 FUN_1800860c0(longlong param_1)

{
  undefined4 *puVar1;
  char cVar2;
  undefined4 *puVar3;
  longlong lVar4;
  int iVar5;
  
  cVar2 = FUN_180044640(param_1 + 0x5c);
  if (cVar2 == '\0') {
    return 0;
  }
  FUN_180087550(0,FUN_180085f50,param_1,0);
  FUN_180087550(1,FUN_180085f50,param_1);
  puVar1 = (undefined4 *)PTR_DAT_180643568;
  iVar5 = 0;
  lVar4 = 0x90;
  *(undefined4 *)PTR_DAT_180643568 = 0;
  puVar3 = (undefined4 *)((longlong)puVar1 + 0x10);
  do {
    puVar1[1] = 0;
    *(undefined8 *)(puVar3 + -2) = 0xffffffffffffffff;
    *puVar3 = 0xffffffff;
    puVar3 = puVar3 + 5;
    puVar1[5] = 0xffffffff;
    lVar4 = lVar4 + -1;
    puVar1 = puVar1 + 5;
  } while (lVar4 != 0);
  do {
    FUN_1800861a0(iVar5);
    FUN_180086300(iVar5);
    iVar5 = iVar5 + 1;
  } while (iVar5 < 3);
  return 1;
}



// ===================================================
// 180085C00  ->  FUN_180085c00  (entree 180085c00)
// ===================================================

undefined1 FUN_180085c00(longlong param_1)

{
  char cVar1;
  undefined4 *puVar2;
  longlong lVar3;
  
  puVar2 = &DAT_1806f43b4;
  lVar3 = 3;
  do {
    cVar1 = FUN_18024a180(*puVar2);
    if (cVar1 != '\0') {
      FUN_180249e50(1,puVar2);
    }
    FUN_180218400(0,*(undefined8 *)(puVar2 + 1));
    puVar2 = puVar2 + 0x376;
    lVar3 = lVar3 + -1;
  } while (lVar3 != 0);
  if (*(int *)(param_1 + 0x58) != -1) {
    FUN_180087420(0,FUN_180085f50,param_1);
    FUN_180087420(1,FUN_180085f50,param_1);
    FUN_18003d840(param_1 + 0x5c);
    *(undefined4 *)(param_1 + 0x58) = 0xffffffff;
    FUN_18003d840(param_1 + 0x5c);
    *(undefined1 *)(param_1 + 0x60) = 1;
  }
  return 1;
}



// ===================================================
// 180085CB0  ->  FUN_180085cb0  (entree 180085cb0)
// ===================================================

void FUN_180085cb0(longlong param_1)

{
  undefined4 *puVar1;
  longlong lVar2;
  undefined *puVar3;
  int *piVar4;
  
  if (*(char *)(param_1 + 0x60) != '\0') {
    puVar1 = &DAT_1806f43fc;
    lVar2 = 3;
    puVar3 = &DAT_180643570;
    piVar4 = &DAT_180643558;
    do {
      if ((*piVar4 != 0) && (*(char *)(puVar1 + -0x13) != '\0')) {
        FUN_18024bbc0();
        FUN_18024bdb0(puVar1[-1],*puVar1,puVar1[1]);
        FUN_1800ec520(0x180000,FUN_180085d60,puVar3);
        FUN_18024bb70();
      }
      puVar3 = puVar3 + 4;
      piVar4 = piVar4 + 1;
      puVar1 = puVar1 + 0x376;
      lVar2 = lVar2 + -1;
    } while (lVar2 != 0);
  }
  return;
}



// ===================================================
// 180086660  ->  FUN_180086660  (entree 180086660)
// ===================================================

void FUN_180086660(longlong param_1)

{
  char cVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined1 local_res8 [32];
  
  *(undefined4 *)(param_1 + 0x58) = 0x496;
  puVar2 = (undefined4 *)FUN_18003c370(local_res8,0x496);
  puVar3 = (undefined4 *)(param_1 + 0x5c);
  *puVar3 = *puVar2;
  cVar1 = FUN_180041a80(puVar3);
  if (cVar1 != '\0') {
    FUN_1800460d0(puVar3,0);
    FUN_180044830(puVar3);
    return;
  }
  return;
}



// ===================================================
// 180086730  ->  FUN_180086730  (entree 180086730)
// ===================================================

void FUN_180086730(longlong *param_1,int param_2)

{
  int iVar1;
  longlong lVar2;
  undefined *puVar3;
  longlong lVar4;
  int *piVar5;
  longlong lVar6;
  int iVar7;
  int *piVar8;
  longlong lVar9;
  
  puVar3 = PTR_DAT_180643568;
  lVar9 = 0;
  lVar2 = -(longlong)PTR_DAT_180643568;
  lVar6 = 0x90;
  piVar8 = (int *)(PTR_DAT_180643568 + 4);
  do {
    iVar1 = *piVar8;
    if (0 < iVar1) {
      iVar7 = piVar8[4];
      if (iVar7 == -1) {
        *(int *)(puVar3 + (longlong)piVar8 + lVar2 + 0x10) = iVar1;
        iVar7 = iVar1;
      }
      else {
        *(int *)(puVar3 + (longlong)piVar8 + lVar2) = iVar7;
      }
      lVar4 = (longlong)iVar7;
      if (0 < iVar7) {
        piVar5 = (int *)(puVar3 + (lVar4 + 2 + lVar9) * 4);
        do {
          iVar7 = iVar7 + -1;
          if ((*piVar5 < 0) || (*piVar5 < param_2)) break;
          *piVar8 = iVar7;
          lVar4 = lVar4 + -1;
          piVar5 = piVar5 + -1;
        } while (0 < lVar4);
      }
    }
    piVar8 = piVar8 + 5;
    lVar9 = lVar9 + 5;
    lVar6 = lVar6 + -1;
    if (lVar6 == 0) {
                    /* WARNING: Could not recover jumptable at 0x0001800867f7. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(*param_1 + 0x60))(param_1);
      return;
    }
  } while( true );
}



// ===================================================
// 180086700  ->  FUN_180086700  (entree 180086700)
// ===================================================

void FUN_180086700(void)

{
  int *piVar1;
  int *piVar2;
  longlong lVar3;
  
  lVar3 = 0x90;
  piVar2 = (int *)PTR_DAT_180643568;
  do {
    piVar1 = piVar2 + 5;
    if (*piVar1 != -1) {
      piVar2[1] = *piVar1;
      *piVar1 = -1;
    }
    lVar3 = lVar3 + -1;
    piVar2 = piVar1;
  } while (lVar3 != 0);
  return;
}



// ===================================================
// 180086800  ->  FUN_180086800  (entree 180086800)
// ===================================================

void FUN_180086800(longlong param_1,undefined1 param_2)

{
  char cVar1;
  
  cVar1 = FUN_180041a80(param_1 + 0x5c);
  if (cVar1 != '\0') {
    FUN_180046490(param_1 + 0x5c,param_2);
  }
  *(undefined1 *)(param_1 + 0x60) = param_2;
  return;
}



// ===================================================
// 180072580  ->  FUN_180072580  (entree 180072580)
// ===================================================

undefined1 FUN_180072580(void)

{
  FUN_180040270("TaskEffectFogRing::init()\n");
  return 1;
}



// ===================================================
// 180071F50  ->  FUN_180071f50  (entree 180071f50)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

longlong FUN_180071f50(longlong param_1)

{
  uint uVar1;
  float fVar2;
  float *pfVar3;
  float *pfVar4;
  int iVar5;
  float fVar6;
  undefined1 auVar7 [16];
  undefined1 auVar8 [64];
  float local_38;
  float fStack_34;
  float fStack_30;
  
  fVar6 = (float)(**(code **)(**(longlong **)(param_1 + 0x318) + 8))();
  fVar2 = fVar6 * DAT_18034ff14;
  auVar8 = ZEXT464((uint)fVar2);
  *(float *)(param_1 + 0x5c) = fVar6;
  auVar7._0_8_ = (double)fVar2;
  auVar7._8_8_ = 0;
  auVar7 = vandpd_avx(auVar7,_DAT_180346d50);
  if (DAT_180346d34 < (float)auVar7._0_8_) {
    FUN_180071bc0(param_1 + 0x58,fVar2);
    FUN_1800725a0(param_1 + 0x58,auVar8._0_8_);
  }
  fVar6 = DAT_180350090;
  uVar1 = *(uint *)(param_1 + 0x90);
  iVar5 = 0;
  pfVar4 = *(float **)(param_1 + 0xa0);
  pfVar3 = *(float **)(param_1 + 0xa8);
  fVar2 = *(float *)(param_1 + 0x94);
  if (0 < (int)uVar1) {
    fStack_30 = (float)*(undefined8 *)(param_1 + 0x80);
    fStack_34 = (float)((ulonglong)*(undefined8 *)(param_1 + 0x78) >> 0x20);
    local_38 = (float)*(undefined8 *)(param_1 + 0x78);
    do {
      *pfVar3 = fVar6 * *pfVar4;
      pfVar3[1] = fVar6 * pfVar4[1];
      pfVar3[2] = fVar6 * pfVar4[2];
      pfVar3[3] = local_38;
      pfVar3[4] = fStack_34;
      pfVar3[5] = fStack_30;
      pfVar3[6] = fVar2 * pfVar4[10];
      iVar5 = iVar5 + 1;
      pfVar3[7] = pfVar4[9];
      pfVar3 = pfVar3 + 8;
      uVar1 = *(uint *)(param_1 + 0x90);
      pfVar4 = pfVar4 + 0xb;
    } while (iVar5 < (int)uVar1);
  }
  *(uint *)(param_1 + 0xb0) = uVar1;
  *(undefined1 *)(param_1 + 0x60) = 0;
  return (ulonglong)(uVar1 >> 8) << 8;
}



// ===================================================
// 180072080  ->  FUN_180072080  (entree 180072080)
// ===================================================

undefined1 FUN_180072080(longlong param_1)

{
  if (*(longlong *)(param_1 + 0xa0) != 0) {
    FUN_180218960();
    *(undefined8 *)(param_1 + 0xa0) = 0;
  }
  if (*(longlong *)(param_1 + 0xa8) != 0) {
    FUN_180218960();
    *(undefined8 *)(param_1 + 0xa8) = 0;
  }
  FUN_18010ca20(4);
  FUN_18010be60(0);
  FUN_1800f0ba0(0);
  DAT_180677b10 = 0;
  FUN_180040270("TaskEffectFogRing::dest()\n");
  return 1;
}



// ===================================================
// 180072100  ->  FUN_180072100  (entree 180072100)
// ===================================================

void FUN_180072100(longlong param_1)

{
  if (*(char *)(param_1 + 0x58) != '\0') {
    FUN_1800ec7c0(FUN_180072ba0,param_1 + 0x58,0x16);
    return;
  }
  return;
}



// ===================================================
// 180072B60  ->  FUN_180072b60  (entree 180072b60)
// ===================================================

void FUN_180072b60(longlong *param_1,undefined4 param_2)

{
  (**(code **)(*param_1 + 0x58))(param_1,0);
  FUN_180072130(param_1 + 0xb,param_2);
  DAT_180677b10 = param_1 + 0xb;
  return;
}



// ===================================================
// 180079170  ->  FUN_180079170  (entree 180079170)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_180079170(longlong *param_1)

{
  longlong lVar1;
  
  (**(code **)(*param_1 + 0x58))(param_1,0);
  _DAT_18067cdf4 = DAT_180346d3c;
  _DAT_180681c78 = 5000;
  lVar1 = 0x180681c8c;
  do {
    *(undefined8 *)(lVar1 + -0xc) = 0;
    *(undefined8 *)(lVar1 + -4) = 0;
    *(undefined4 *)(lVar1 + 4) = 0;
    *(undefined4 *)(lVar1 + 8) = 0xbf800000;
    *(undefined4 *)(lVar1 + 0xc) = 0;
    *(undefined4 *)(lVar1 + 0x10) = 0x3f800000;
    *(undefined4 *)(lVar1 + 0x14) = 0x3f800000;
    lVar1 = lVar1 + 0x24;
  } while (lVar1 < 0x1806adbac);
  FUN_1802ff420(&DAT_1806adba0,0,280000);
  _DAT_18067cdfc = _DAT_180643284;
  uRam000000018067ce04 = uRam000000018064328c;
  _DAT_18067ce1c = DAT_180643294;
  _DAT_18067ce0c = _DAT_180643298;
  uRam000000018067ce14 = uRam00000001806432a0;
  _DAT_18067ce34 = DAT_1806432bc;
  _DAT_18067ce20 = _DAT_1806432a8;
  uRam000000018067ce28 = uRam00000001806432b0;
  _DAT_18067cdf8 = DAT_180643280;
  _DAT_18067ce40 = DAT_1806432c8;
  _DAT_18067ce50 = DAT_1806432d8;
  _DAT_18067ce30 = DAT_1806432b8;
  _DAT_18067ce3c = DAT_1806432c4;
  _DAT_18067ce44 = DAT_1806432cc;
  _DAT_18067ce4c = DAT_1806432d4;
  FUN_180040270("TaskEffectRain::init()\n");
  return 1;
}



// ===================================================
// 180078E00  ->  FUN_180078e00  (entree 180078e00)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

ulonglong FUN_180078e00(longlong param_1)

{
  ulonglong uVar1;
  
  _DAT_18067cdf4 = (**(code **)(**(longlong **)(param_1 + 0x58) + 8))();
  uVar1 = FUN_180078bb0(&DAT_18067cdf0);
  return uVar1 & 0xffffffffffffff00;
}



// ===================================================
// 180078E30  ->  FUN_180078e30  (entree 180078e30)
// ===================================================

undefined1 FUN_180078e30(void)

{
  FUN_180040270("TaskEffectRain::dest()\n");
  return 1;
}



// ===================================================
// 180078E50  ->  FUN_180078e50  (entree 180078e50)
// ===================================================

void FUN_180078e50(void)

{
  if ((DAT_18067cdf0 != '\0') && (0 < DAT_180681c7c)) {
    FUN_1800ec7c0(FUN_1800792c0,&DAT_18067cdf0,1);
    return;
  }
  return;
}



// ===================================================
// 180079370  ->  FUN_180079370  (entree 180079370)
// ===================================================

void FUN_180079370(undefined8 param_1,undefined1 param_2)

{
  DAT_18067cdf0 = param_2;
  return;
}



