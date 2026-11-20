// ===================================================
// 822C29E8  ->  FUN_822c29e8  (entree 822c29e8)
// ===================================================

void FUN_822c29e8(void)

{
  FUN_822b8530(0xffffffff8294ff30);
  return;
}



// ===================================================
// 822C29D8  ->  FUN_822c29d8  (entree 822c29d8)
// ===================================================

void FUN_822c29d8(undefined8 param_1)

{
  FUN_822b8528(0xffffffff8294ff30,param_1);
  return;
}



// ===================================================
// 822C2A08  ->  FUN_822c2a08  (entree 822c2a08)
// ===================================================

void FUN_822c2a08(undefined8 param_1)

{
  FUN_822b85e8(0xffffffff8294ff30,param_1);
  return;
}



// ===================================================
// 822C2A18  ->  FUN_822c2a18  (entree 822c2a18)
// ===================================================

void FUN_822c2a18(void)

{
  FUN_822b85f8(0xffffffff8294ff30);
  return;
}



// ===================================================
// 8223BC10  ->  FUN_8223bc10  (entree 8223bc10)
// ===================================================

void FUN_8223bc10(int param_1)

{
  short sVar1;
  short sVar2;
  short sVar3;
  short sVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  int iVar7;
  int iVar8;
  
  iVar7 = DAT_827aa9f0;
  uVar6 = DAT_82001bc8;
  uVar5 = DAT_82000b08;
  iVar8 = param_1 * 0x1c;
  *(undefined4 *)(DAT_827aa9f0 + 0x18) = DAT_82000b08;
  *(undefined4 *)(iVar7 + 0x1c) = uVar5;
  *(int *)(iVar7 + 0x58) = param_1;
  *(undefined4 *)(iVar7 + 0x50) = uVar6;
  *(undefined4 *)(iVar7 + 0x54) = 0;
  *(undefined4 *)(iVar7 + 0x40) = 0;
  uVar5 = DAT_82000a34;
  *(undefined4 *)(iVar7 + 0x3c) = 0xff000000;
  *(undefined4 *)(iVar7 + 0x44) = uVar5;
  *(int *)(iVar7 + 0x74) = iVar8 + -0x7d9af120;
  *(undefined4 *)(iVar7 + 0x48) = 0;
  *(undefined4 *)(iVar7 + 0x38) = 0xffffffff;
  sVar1 = *(short *)(&DAT_82650ee8 + iVar8);
  *(float *)(iVar7 + 0x2c) = (float)(longlong)sVar1;
  sVar2 = *(short *)(&DAT_82650eea + iVar8);
  *(float *)(iVar7 + 0x28) = (float)(longlong)sVar2;
  sVar3 = *(short *)(&DAT_82650eec + iVar8);
  *(float *)(iVar7 + 0x30) = (float)(longlong)sVar3;
  sVar4 = *(short *)(&DAT_82650eee + iVar8);
  *(float *)(iVar7 + 0x20) = (float)((double)(longlong)sVar3 / (double)(longlong)sVar1);
  *(float *)(iVar7 + 0x34) = (float)(longlong)sVar4;
  *(float *)(iVar7 + 0x24) = (float)((double)(longlong)sVar4 / (double)(longlong)sVar2);
  iVar8 = *(int *)(&DAT_82650ee4 + iVar8);
  *(undefined1 *)(iVar7 + 0x5c) = 0;
  *(undefined1 *)(iVar7 + 0x7c) = 0;
  *(undefined1 *)(iVar7 + 0x7e) = 0;
  *(undefined1 *)(iVar7 + 0x7f) = 0;
  *(int *)(iVar7 + 0x70) = iVar8;
  *(undefined1 *)(iVar7 + 0x80) = 0;
  *(bool *)(iVar7 + 0x7d) = iVar8 != 0;
  if (param_1 == 0xe) {
    iVar8 = FUN_82144a98();
    if (iVar8 == 0) {
      *(undefined1 *)(iVar7 + 0x7d) = 0;
    }
    else {
      *(undefined1 *)(iVar7 + 0x7e) = 1;
      *(undefined1 *)(iVar7 + 0x7f) = 1;
    }
  }
  return;
}



// ===================================================
// 8223C130  ->  FUN_8223c130  (entree 8223c130)
// ===================================================

void FUN_8223c130(int param_1)

{
  *(float *)(DAT_827aa9f0 + 0x50) = (float)(longlong)param_1;
  return;
}



// ===================================================
// 8223C048  ->  FUN_8223c048  (entree 8223c048)
// ===================================================

undefined4 FUN_8223c048(undefined4 param_1)

{
  undefined4 uVar1;
  
  uVar1 = *(undefined4 *)(DAT_827aa9f0 + 0x38);
  *(undefined4 *)(DAT_827aa9f0 + 0x38) = param_1;
  return uVar1;
}



// ===================================================
// 8223BEB8  ->  FUN_8223beb8  (entree 8223beb8)
// ===================================================

void FUN_8223beb8(void)

{
  FUN_8223bd80();
  return;
}



// ===================================================
// 8223FE30  ->  FUN_8223fe30  (entree 8223fe30)
// ===================================================

/* WARNING: Restarted to delay deadcode elimination for space: stack */

void FUN_8223fe30(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                 undefined8 param_5,undefined8 param_6,undefined8 param_7,undefined8 param_8)

{
  undefined8 uStack00000018;
  undefined8 uStack00000020;
  undefined8 uStack00000028;
  undefined8 uStack00000030;
  undefined8 uStack00000038;
  undefined8 uStack00000040;
  undefined8 uStack00000048;
  
  uStack00000018 = param_2;
  uStack00000020 = param_3;
  uStack00000028 = param_4;
  uStack00000030 = param_5;
  uStack00000038 = param_6;
  uStack00000040 = param_7;
  uStack00000048 = param_8;
  FUN_8223fba0(param_1,&stack0x00000018);
  FUN_8223fb20(param_1,&stack0x00000018);
  return;
}



