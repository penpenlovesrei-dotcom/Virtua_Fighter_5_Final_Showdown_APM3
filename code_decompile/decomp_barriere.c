// ===================================================
// 18018f680  ->  FUN_18018f680  (entree 18018f680)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18018f680(longlong param_1)

{
  undefined4 *puVar1;
  char cVar2;
  int iVar3;
  undefined4 uVar4;
  int iVar5;
  longlong lVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  longlong lVar9;
  ulonglong uVar10;
  ulonglong uVar11;
  uint uVar12;
  ulonglong uVar13;
  ulonglong uVar14;
  float fVar15;
  float fVar16;
  undefined4 local_c8;
  float local_c4;
  float local_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  float local_68;
  
  lVar6 = FUN_180178a60();
  uVar7 = FUN_1801053e0();
  local_b8 = _DAT_180408280;
  uStack_b0 = _UNK_180408288;
  uStack_a8 = _UNK_180408290;
  uStack_a0 = _UNK_180408298;
  local_98 = _DAT_180408260;
  uStack_90 = _UNK_180408268;
  uStack_88 = _UNK_180408270;
  uStack_80 = _UNK_180408278;
  local_78 = _DAT_180348bb0;
  uStack_70 = _UNK_180348bb8;
  local_68 = DAT_180346d3c;
  fVar16 = DAT_180346d3c;
  uVar8 = FUN_1801509b0();
  iVar3 = *(int *)(param_1 + 0x58);
  if (iVar3 == 1) {
    uVar10 = 0;
    fVar16 = 0.0;
    uVar11 = uVar10;
    do {
      iVar3 = FUN_180150840(uVar8,uVar11);
      if (((iVar3 != 0x15) && (lVar9 = FUN_180150a00(uVar8,uVar11), lVar9 != 0)) &&
         (lVar9 = FUN_180010090(lVar9), uVar13 = uVar10, uVar14 = uVar10, lVar9 != 0)) {
        do {
          iVar5 = FUN_18014d530(iVar3,*(undefined4 *)(uVar13 + lVar9));
          uVar14 = (ulonglong)(uint)((int)uVar14 + iVar5);
          uVar13 = uVar13 + 4;
        } while ((longlong)uVar13 < 0x60);
        fVar16 = fVar16 + (float)uVar14 * *(float *)((longlong)&local_b8 + (longlong)iVar3 * 4);
      }
      uVar12 = (int)uVar11 + 1;
      uVar11 = (ulonglong)uVar12;
    } while ((int)uVar12 < 2);
    DAT_18070fd74 = *(undefined1 *)(*(longlong *)(param_1 + 0x68) + 0xbc);
    FUN_18010ca50(*(undefined4 *)(*(longlong *)(param_1 + 0x68) + 0xb8));
    DAT_18070fd75 = *(undefined1 *)(*(longlong *)(param_1 + 0x68) + 0xbd);
    lVar9 = *(longlong *)(param_1 + 0x68);
    puVar1 = *(undefined4 **)(lVar9 + 0xc0);
    if (puVar1 != (undefined4 *)0x0) {
      FUN_18010ca20(2,1);
      FUN_18010ca40(*puVar1);
      FUN_18010ca30(puVar1[1],puVar1[2]);
      FUN_18010c9e0(1);
      lVar9 = *(longlong *)(param_1 + 0x68);
    }
    puVar1 = *(undefined4 **)(lVar9 + 200);
    if ((puVar1 != (undefined4 *)0x0) && (fVar16 < DAT_18034b438)) {
      FUN_18010ca20(3,1);
      FUN_18010ca60(*puVar1);
      FUN_18010c9f0(1);
    }
    if (((*(int *)(param_1 + 0x5c) == 0x28) || (*(int *)(param_1 + 0x5c) == 0x10)) && (lVar6 != 0))
    {
      *(undefined1 *)(lVar6 + 0x334) = 0;
    }
    FUN_1800f9c60(*(undefined4 *)(*(longlong *)(param_1 + 0x68) + 0x10),1);
    *(undefined4 *)(param_1 + 0x58) = 2;
  }
  else if (iVar3 == 2) {
    cVar2 = FUN_1800fb7e0(*(undefined4 *)(*(longlong *)(param_1 + 0x68) + 0x10),0);
    if (cVar2 == '\0') {
      FUN_1800d7130(*(undefined4 *)(param_1 + 0x5c));
      FUN_18005f100(*(undefined8 *)(*(longlong *)(param_1 + 0x68) + 0x48));
      FUN_18003c200(**(undefined8 **)(param_1 + 0x68));
      lVar6 = **(longlong **)(param_1 + 0x68);
      lVar9 = FUN_18006f350();
      if (lVar9 != 0) {
        uVar11 = 0;
        *(undefined4 *)(lVar9 + 0x790) = 0;
        if ((lVar6 != 0) && (iVar3 = FUN_180040f30(lVar6), 0 < iVar3)) {
          uVar10 = FUN_18003c180((longlong)iVar3);
          if (uVar10 != 0) {
            do {
              if ((*(uint *)(lVar9 + 0x790) < 8) &&
                 (lVar6 = FUN_18003c120((longlong)iVar3,uVar11), lVar6 != 0)) {
                uVar4 = FUN_180046620(lVar6);
                *(undefined4 *)(lVar9 + 0x7a0 + (ulonglong)*(uint *)(lVar9 + 0x790) * 4) = uVar4;
                *(int *)(lVar9 + 0x790) = *(int *)(lVar9 + 0x790) + 1;
              }
              uVar11 = uVar11 + 1;
            } while (uVar11 < uVar10);
          }
        }
      }
      FUN_18003c200(*(undefined8 *)(*(longlong *)(param_1 + 0x68) + 8));
      FUN_1801903d0(*(undefined4 *)(param_1 + 0x5c));
      *(undefined4 *)(param_1 + 0x58) = 3;
    }
  }
  else if (iVar3 == 3) {
    cVar2 = FUN_1800fb7e0(*(undefined4 *)(*(longlong *)(param_1 + 0x68) + 0x10),0);
    if (((((cVar2 == '\0') && (iVar3 = FUN_1800d9020(), iVar3 == 0)) &&
         (cVar2 = FUN_18005f720(), cVar2 == '\0')) &&
        (cVar2 = FUN_18003c1d0(**(undefined8 **)(param_1 + 0x68)), cVar2 != '\0')) &&
       (((lVar9 = FUN_18006f350(), lVar9 == 0 || ((*(byte *)(lVar9 + 4) & 2) == 0)) &&
        ((cVar2 = FUN_18003c1d0(*(undefined8 *)(*(longlong *)(param_1 + 0x68) + 8)), cVar2 != '\0'
         && (cVar2 = FUN_180190470(), cVar2 == '\0')))))) {
      if (*(int *)(*(longlong *)(param_1 + 0x68) + 0x40) != -1) {
        uVar8 = FUN_1801957a0();
        FUN_180105830(uVar7,uVar8);
      }
      if (lVar6 != 0) {
        FUN_180178e00(lVar6);
        *(undefined4 *)(lVar6 + 0x2dc) = *(undefined4 *)(*(longlong *)(param_1 + 0x68) + 0xe0);
      }
      FUN_18006f620(*(undefined4 *)(param_1 + 0x5c));
      FUN_18006f9c0(*(undefined1 *)(param_1 + 0x70));
      lVar6 = DAT_1807499d8;
      *(undefined4 *)(param_1 + 0x58) = 4;
      fVar15 = DAT_18034af74;
      if (*(longlong *)(lVar6 + 0x68) != 0) {
        fVar15 = *(float *)(*(longlong *)(lVar6 + 0x68) + 0xe4);
      }
      DAT_1807499d0 = fVar15 * DAT_180346d38;
      local_c0 = DAT_1807499d0 + fVar16;
      local_c8 = 0;
      local_c4 = fVar16;
      DAT_180649668 = FUN_18005e560(&local_c8,0,0xc000c700);
    }
  }
  else if ((iVar3 == 4) && (cVar2 = FUN_18006fa60(), cVar2 == '\0')) {
    FUN_1800f8a40(*(undefined4 *)(*(longlong *)(param_1 + 0x68) + 0x10));
    *(undefined4 *)(param_1 + 0x58) = 5;
  }
  return;
}



// ===================================================
// 18018f04d  ->  FUN_18018f030  (entree 18018f030)
// ===================================================

void FUN_18018f030(longlong param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined8 uVar3;
  longlong lVar4;
  int iVar5;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  
  if ((*(int *)(param_1 + 0x58) == 5) && (*(char *)(param_1 + 0x70) != '\0')) {
    FUN_18024bbc0();
    FUN_18024bc70(*(undefined4 *)(param_1 + 0xb8),0,DAT_180346d3c,0);
    lVar4 = *(longlong *)(param_1 + 0x68);
    if ((*(int *)(lVar4 + 0x14) != -1) && (*(char *)(param_1 + 0x72) != '\0')) {
      FUN_1800ec460();
      lVar4 = *(longlong *)(param_1 + 0x68);
    }
    if ((*(int *)(lVar4 + 0x18) != -1) && (*(char *)(param_1 + 0x73) != '\0')) {
      FUN_1800ec460();
      lVar4 = *(longlong *)(param_1 + 0x68);
    }
    iVar1 = *(int *)(lVar4 + 0x20);
    if (iVar1 != -1) {
      iVar5 = 0;
      do {
        FUN_1800ed1c0(iVar5);
        uVar3 = FUN_180178a60();
        FUN_180178dd0(uVar3,iVar5);
        FUN_1800ed1d0(0x80000080);
        FUN_1800ec460(iVar1);
        iVar5 = iVar5 + 1;
      } while (iVar5 < 2);
      FUN_1800ed1d0(0);
      FUN_1800ec450(0);
      FUN_1800ed1c0(0);
      lVar4 = *(longlong *)(param_1 + 0x68);
    }
    iVar1 = *(int *)(lVar4 + 0x24);
    if (iVar1 != -1) {
      FUN_1800ed1d0(0x80000200);
      FUN_1800ec460(iVar1);
      FUN_1800ed1d0(0);
      lVar4 = *(longlong *)(param_1 + 0x68);
    }
    iVar1 = *(int *)(lVar4 + 0x28);
    if (iVar1 != -1) {
      FUN_1800ed1d0(0x80000400);
      FUN_1800ec460(iVar1);
      FUN_1800ed1d0(0);
    }
    if (*(int *)(DAT_1807499d8 + 0x5c) - 8U < 2) {
      FUN_1800ec7c0(FUN_18018fbc0,param_1,0x15);
    }
    if ((*(int *)(*(longlong *)(param_1 + 0x68) + 0x1c) != -1) &&
       (*(char *)(param_1 + 0x74) != '\0')) {
      uVar3 = FUN_18000fa90(param_1 + 0x78);
      FUN_18024b890(uVar3);
      FUN_1800ec460(*(undefined4 *)(*(longlong *)(param_1 + 0x68) + 0x1c));
    }
    FUN_18024bb70();
    if ((*(int *)(*(longlong *)(param_1 + 0x68) + 0x2c) != -1) &&
       (*(char *)(param_1 + 0x71) != '\0')) {
      uVar3 = FUN_1801053e0();
      uVar2 = *(undefined4 *)(*(longlong *)(param_1 + 0x68) + 0x10);
      local_18 = FUN_1800f92f0(uVar2,*(undefined4 *)(*(longlong *)(param_1 + 0x68) + 0x2c));
      local_14 = FUN_1800f92f0(uVar2,*(undefined4 *)(*(longlong *)(param_1 + 0x68) + 0x30));
      local_10 = FUN_1800f92f0(uVar2,*(undefined4 *)(*(longlong *)(param_1 + 0x68) + 0x34));
      FUN_180105380(uVar3,&local_18,*(undefined4 *)(*(longlong *)(param_1 + 0x68) + 0x38),
                    *(undefined4 *)(*(longlong *)(param_1 + 0x68) + 0x3c));
    }
    FUN_18010ca00(*(undefined1 *)(param_1 + 0x75));
  }
  return;
}



