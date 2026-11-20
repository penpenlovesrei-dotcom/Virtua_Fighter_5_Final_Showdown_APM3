// ===================================================
// 8222C43C  ->  FUN_8222c408  (entree 8222c408)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_8222c408(int param_1,byte param_2)

{
  undefined1 uVar1;
  uint uVar2;
  int iVar5;
  ulonglong uVar3;
  undefined8 uVar4;
  byte bVar6;
  
  iVar5 = FUN_822146a8();
  iVar5 = iVar5 + 0x10;
  uVar2 = (uint)param_2;
  bVar6 = *(char *)(uVar2 + iVar5) + 1;
  *(byte *)(uVar2 + iVar5) = bVar6;
  if (0x96 < bVar6) {
    *(undefined1 *)(uVar2 + iVar5) = 1;
  }
  uVar1 = *(undefined1 *)(uVar2 + iVar5);
  iVar5 = FUN_822146a8();
  iVar5 = iVar5 + param_1 * 0x80;
  uVar3 = FUN_82340db8(uVar2,0);
  if ((uVar3 & 0xffffffff) != 0) {
    *(undefined1 *)(iVar5 + 0x2c) = 0;
    FUN_826d8c40(iVar5 + 0x30,uVar3,0x60);
  }
  uVar4 = FUN_82332878(uVar2);
  FUN_8230c328(iVar5 + 0x90,0x15,0xffffffff82010ac4,uVar4,uVar1);
  *(byte *)(iVar5 + 0x29) = param_2;
  *(undefined1 *)(iVar5 + 0x28) = 1;
  return;
}



// ===================================================
// 8222E2E4  ->  FUN_8222e2d0  (entree 8222e2d0)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_8222e2d0(ulonglong param_1)

{
  longlong lVar1;
  longlong lVar2;
  int iVar3;
  undefined4 *puVar4;
  longlong lVar5;
  longlong lVar6;
  
  if ((-1 < (int)param_1) && ((int)param_1 < 0x96)) {
    lVar5 = param_1 + 1;
    if ((int)lVar5 < 0x96) {
      lVar6 = (param_1 & 0x1ffffff) << 7;
      do {
        lVar1 = FUN_822146a8();
        lVar2 = FUN_822146a8();
        FUN_826d8c40(lVar1 + lVar6 + 0x28,lVar2 + lVar6 + 0xa8,0x80);
        lVar5 = lVar5 + 1;
        lVar6 = lVar6 + 0x80;
      } while ((int)lVar5 < 0x96);
    }
    iVar3 = FUN_822146a8();
    *(undefined1 *)(iVar3 + 0x4aa8) = 0;
    *(undefined1 *)(iVar3 + 0x4aa9) = 0;
    lVar5 = 0x18;
    *(undefined1 *)(iVar3 + 0x4aac) = 0;
    puVar4 = (undefined4 *)(iVar3 + 0x4aac);
    do {
      puVar4 = puVar4 + 1;
      *puVar4 = 0;
      lVar5 = lVar5 + -1;
    } while (lVar5 != 0);
    FUN_826d9660(iVar3 + 0x4b10,0,(undefined1 *)(iVar3 + 0x4aa8) + (0x7d - (iVar3 + 0x4b10)));
  }
  return;
}



// ===================================================
// 8223785C  ->  FUN_822377d8  (entree 822377d8)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_822377d8(int *param_1,char param_2)

{
  int iVar1;
  char cVar3;
  char *pcVar2;
  ulonglong uVar4;
  
  uVar4 = 0;
  *param_1 = 0;
  cVar3 = FUN_821f7d00(param_2);
  if (cVar3 != '\0') {
    do {
      pcVar2 = (char *)FUN_8222c4c0(uVar4);
      if ((*pcVar2 != '\0') && (pcVar2[1] == param_2)) {
        iVar1 = *param_1;
        *(char *)(param_1 + iVar1 * 0x21 + 1) = (char)uVar4;
        FUN_826d8c40(param_1 + iVar1 * 0x21 + 2,pcVar2,0x80);
        *param_1 = *param_1 + 1;
      }
      uVar4 = uVar4 + 1;
    } while ((uVar4 & 0xffffffff) < 0x96);
  }
  return;
}



