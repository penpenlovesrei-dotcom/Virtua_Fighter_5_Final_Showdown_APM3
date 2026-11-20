// ===================================================
// 82309054  ->  FUN_82308c90  (entree 82308c90)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */
/* WARNING: Restarted to delay deadcode elimination for space: stack */

void FUN_82308c90(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar6;
  undefined8 uVar3;
  int iVar7;
  undefined8 uVar4;
  int iVar8;
  undefined8 uVar5;
  ulonglong uVar9;
  ulonglong uVar10;
  uint uVar11;
  undefined8 uVar12;
  double dVar13;
  double dVar14;
  double dVar15;
  double dVar16;
  double dVar17;
  float afStack_140 [2];
  undefined8 uStack_138;
  float fStack_130;
  float fStack_12c;
  float fStack_128;
  undefined8 uStack_120;
  float fStack_118;
  float fStack_114;
  float fStack_110;
  float fStack_108;
  float fStack_104;
  float fStack_100;
  float fStack_f8;
  float fStack_f4;
  float fStack_f0;
  float fStack_e8;
  float fStack_e4;
  float fStack_e0;
  undefined1 auStack_d0 [32];
  undefined1 auStack_b0 [32];
  undefined1 auStack_90 [144];
  
  iVar6 = FUN_826018c0();
  if (((*(int *)(iVar6 + 0x7c) != 0) && (*(char *)(iVar6 + 0x81) != '\0')) &&
     (*(int *)(iVar6 + 0x84) != 0)) {
    FUN_821dc920();
    uVar3 = FUN_821dc9c0();
    iVar7 = FUN_82235f28(0xffffffff827a99f8,uVar3);
    dVar17 = (double)DAT_82000a34;
    fStack_130 = DAT_82000a34;
    fStack_12c = DAT_82000a34;
    fStack_128 = DAT_82000a34;
    uStack_138 = 0x82084b888208be8c;
    uVar2 = *(undefined4 *)((int)&uStack_138 + (uint)*(byte *)(iVar6 + 0x80) * 4);
    FUN_8223bc10(0xe);
    FUN_8223c130(6);
    uVar12 = FUN_821665d8(*(undefined4 *)(iVar6 + 0x7c));
    FUN_82308b78(iVar6,&fStack_130,afStack_140,0x423,uVar2,0xffffffff8208be7c);
    dVar13 = (double)DAT_82000f14;
    FUN_8223beb8((double)fStack_130,(double)(float)((double)fStack_12c - dVar13));
    dVar14 = (double)afStack_140[0];
    dVar16 = (double)DAT_82001afc;
    iVar8 = (int)(longlong)(dVar14 * dVar16);
    uStack_138 = CONCAT44(iVar8,uStack_138._4_4_);
    FUN_8223c048(iVar8 << 0x18 | 0xffffff);
    uVar3 = FUN_8223c198(1);
    uVar4 = FUN_8223c1c0(1);
    FUN_8223fe30(0xffffffff82000f08,iVar7 + 0x59);
    FUN_8223c198(uVar3);
    FUN_8223c1c0(uVar4);
    uVar11 = *(uint *)(iVar7 + 0x100);
    uVar10 = (ulonglong)uVar11;
    uVar9 = (ulonglong)*(uint *)(iVar7 + 0x104);
    fStack_118 = fStack_130;
    fStack_114 = fStack_12c;
    fStack_110 = fStack_128;
    iVar8 = FUN_82144a98();
    if (iVar8 == 0) {
      uVar3 = FUN_82322798(0x18c);
      FUN_82249520(auStack_b0,0x20,uVar3,uVar10);
      uVar3 = 0x18d;
    }
    else {
      uVar3 = FUN_82322798(0x18e);
      FUN_82249520(auStack_b0,0x20,uVar3,uVar10);
      uVar3 = 399;
    }
    uVar3 = FUN_82322798(uVar3);
    FUN_82249520(auStack_d0,0x20,uVar3,uVar9);
    FUN_82308b78(uVar12,iVar6,&fStack_130,afStack_140,0x423,uVar2,0xffffffff8208be68);
    FUN_8223beb8((double)fStack_130,(double)fStack_12c);
    iVar8 = (int)(longlong)((double)afStack_140[0] * dVar16);
    uStack_138 = CONCAT44(iVar8,uStack_138._4_4_);
    FUN_8223c048(iVar8 << 0x18 | 0xffffff);
    FUN_8223fe30(0xffffffff820847fc,auStack_b0,auStack_d0);
    uVar10 = uVar9 + uVar10;
    dVar15 = dVar17;
    if (uVar10 != 0) {
      iVar8 = (int)(((float)uVar11 / (float)(uVar10 & 0xffffffff)) * DAT_82003edc * DAT_82003edc);
      uStack_138._4_4_ = (undefined4)uVar10;
      uStack_138 = CONCAT44(iVar8,uStack_138._4_4_);
      uStack_120 = (longlong)iVar8;
      dVar15 = (double)((float)uStack_120 * DAT_82003a3c);
    }
    FUN_82308b78(uVar12,iVar6,&fStack_130,afStack_140,0x423,uVar2,0xffffffff8208be54);
    iVar8 = (int)(longlong)((double)afStack_140[0] * dVar16);
    uStack_138 = CONCAT44(iVar8,uStack_138._4_4_);
    uVar11 = iVar8 << 0x18 | 0xffffff;
    FUN_8223beb8((double)fStack_130,(double)fStack_12c);
    FUN_8223c048(uVar11);
    if ((dVar15 <= dVar17) || (uVar9 != 0)) {
      uVar3 = FUN_82322798(0x191);
      uVar4 = FUN_82322798(400);
      FUN_8223fe30(0xffffffff8208be3c,uVar4,dVar15,uVar3);
    }
    else {
      uVar4 = FUN_82322798(0x191);
      uVar3 = DAT_820117f0;
      uVar5 = FUN_82322798(400);
      FUN_8223fe30(0xffffffff8208be48,uVar5,uVar3,uVar4);
    }
    if (*(char *)(iVar6 + 0x80) == '\0') {
      uVar3 = 0xffffffff8208dccc;
    }
    else {
      uVar3 = 0xffffffff8208be2c;
    }
    FUN_82308b78(uVar12,iVar6,&fStack_130,afStack_140,0x423,uVar2,uVar3);
    uVar1 = *(undefined4 *)(iVar7 + 0xec);
    uVar3 = FUN_82322798(999);
    FUN_82249520(auStack_90,0x20,uVar3,uVar1);
    dVar17 = (double)fStack_130;
    dVar16 = (double)fStack_12c;
    uStack_120 = CONCAT44(fStack_130,fStack_12c);
    dVar15 = (double)DAT_8208be28;
    uStack_138 = CONCAT44(DAT_8208be28,DAT_82011804);
    FUN_8223df90(uStack_120,uStack_138,9,5,0);
    FUN_8223beb8((double)(float)((double)(float)(dVar17 + dVar15) - (double)DAT_82000f0c),
                 (double)(float)(dVar16 + (double)DAT_82000f0c));
    FUN_8223c048(uVar11);
    FUN_8223fe30(0xffffffff82000f80,0xffffffff82010300,auStack_90);
    if (*(int *)(iVar6 + 0x84) != 0) {
      FUN_82308b78(uVar12,iVar6,&fStack_130,afStack_140,0x423,uVar2,0xffffffff8208be18);
      FUN_822dc728(&fStack_130,&fStack_130);
      fStack_108 = fStack_130;
      fStack_104 = fStack_12c;
      fStack_100 = fStack_128;
      FUN_82166540(*(undefined4 *)(iVar6 + 0x84),&fStack_108);
      FUN_82166570((double)afStack_140[0],*(undefined4 *)(iVar6 + 0x84));
    }
    if (*(int *)(iVar6 + 0xa4) != 0) {
      FUN_82308b78(uVar12,iVar6,&fStack_130,afStack_140,0x423,uVar2,0xffffffff8208be08);
      fStack_f8 = fStack_130;
      fStack_f4 = fStack_12c;
      fStack_f0 = fStack_128;
      FUN_82166540(*(undefined4 *)(iVar6 + 0xa4),&fStack_f8);
      FUN_82166570((double)afStack_140[0],*(undefined4 *)(iVar6 + 0xa4));
    }
    if (*(int *)(iVar6 + 0xac) != 0) {
      FUN_82308b78(uVar12,iVar6,&fStack_130,afStack_140,0x423,uVar2,0xffffffff8208bdf8);
      fStack_e4 = (float)((double)fStack_12c - dVar13);
      fStack_e8 = fStack_130;
      fStack_e0 = fStack_128;
      FUN_82166540(*(undefined4 *)(iVar6 + 0xac),&fStack_e8);
      FUN_82166570((double)afStack_140[0],*(undefined4 *)(iVar6 + 0xac));
    }
    if (*(char *)(iVar7 + 0x423) != '\0') {
      fStack_118 = fStack_118 + DAT_8200649c;
      fStack_114 = fStack_114 + DAT_82003a50;
      FUN_82308670(dVar14,iVar6,*(char *)(iVar7 + 0x423) + -1,&fStack_118);
    }
  }
  FUN_8260190c();
  return;
}



