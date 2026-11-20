// ===================================================
// 18007E420  ->  FUN_18007e420  (entree 18007e420)
// ===================================================

void FUN_18007e420(undefined4 *param_1)

{
  FUN_18024e5a0(1,0,0,0);
  FUN_180175870("SN_FOOT");
  FUN_180252390();
  FUN_18024a6a0(2);
  FUN_180247100(300);
  FUN_1802473b0(0x12d);
  FUN_18024e900(0x318);
  FUN_18024e900(0xac);
  FUN_18024e300(0x3d2);
  FUN_18024e330(1);
  FUN_180256d50(0x21d);
  FUN_180256da0(*(undefined4 *)(*(longlong *)(param_1 + 8) + 0x14),
                *(undefined4 *)(*(longlong *)(param_1 + 8) + 0x10));
  FUN_1802573a0(0x318,0x319,1);
  FUN_180247600(3,0x161,0,*(undefined8 *)(param_1 + 2));
  FUN_1802470a0(4,0x15c,0,*(undefined8 *)(param_1 + 4));
  FUN_18024f2d0(param_1[6]);
  FUN_1802573a0(0x318,0x319,1);
  FUN_18024e900(0x2cd);
  FUN_18024f2a0(0x311);
  FUN_180247430(0xe);
  FUN_1802475b0(0xe,1,0x161,0,4,*(undefined8 *)(param_1 + 10));
  FUN_180247230(2,0,*param_1);
  FUN_18024e8d0(0xac);
  FUN_1802573a0(0x318,0x319,0);
  FUN_18024f2d0(DAT_180346d3c);
  FUN_180256da0(*(undefined4 *)(*(longlong *)(param_1 + 8) + 0x14),0);
  FUN_18024e300(0x3ce);
  FUN_18024e330(1);
  FUN_18024e8d0(0x2cd);
  FUN_1802573a0(0x318,0x319,0);
  FUN_18024e8d0(0x318);
  FUN_18024a650();
  FUN_180252530();
  FUN_18024e5a0(1,1,1);
  FUN_180176960();
  return;
}



// ===================================================
// 18007E180  ->  FUN_18007e180  (entree 18007e180)
// ===================================================

void FUN_18007e180(longlong param_1)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  char cVar6;
  longlong lVar7;
  undefined8 uVar8;
  longlong lVar9;
  ulonglong uVar10;
  uint uVar11;
  ulonglong uVar12;
  ulonglong uVar13;
  longlong *plVar14;
  ulonglong uVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  float fVar19;
  float fVar20;
  
  *(longlong *)(param_1 + 0x78) = param_1 + 0xa0;
  uVar13 = 0;
  *(undefined4 *)(param_1 + 0x70) = 0;
  *(longlong *)(param_1 + 0x80) = param_1 + 0x3a0;
  *(undefined4 *)(param_1 + 0x88) = *(undefined4 *)(param_1 + 0x1c);
  *(longlong *)(param_1 + 0x98) = param_1 + 0x4a0;
  lVar7 = FUN_1801957a0(*(undefined4 *)(param_1 + 0x24));
  *(longlong *)(param_1 + 0x90) = lVar7;
  if (lVar7 != 0) {
    plVar14 = (longlong *)(param_1 + 0x19d8);
    uVar15 = uVar13;
    fVar20 = DAT_18034b3c4;
    do {
      uVar8 = FUN_1801509b0();
      lVar7 = FUN_180150920(uVar8,uVar15);
      if (lVar7 != 0) {
        uVar8 = FUN_1801509b0();
        cVar6 = FUN_1801508a0(uVar8,uVar15);
        if (cVar6 != '\0') {
          uVar8 = FUN_1801509b0();
          lVar7 = FUN_1801509c0(uVar8,uVar15);
          if ((lVar7 != 0) && (uVar10 = uVar13, uVar12 = uVar13, 0 < *(int *)(param_1 + 0x19d0))) {
            do {
              lVar9 = FUN_1800e0280(lVar7,(longlong)*(int *)(*plVar14 + uVar10));
              fVar1 = *(float *)(lVar9 + 0x1c);
              fVar2 = *(float *)(lVar9 + 0xc);
              fVar3 = *(float *)(lVar9 + 0x2c);
              if (fVar1 - *(float *)(param_1 + 0x10) < *(float *)(param_1 + 0xc)) {
                lVar9 = *plVar14;
                fVar16 = fVar2 - *(float *)(lVar9 + 4 + uVar10);
                fVar4 = fVar1 - *(float *)(lVar9 + 8 + uVar10);
                fVar5 = fVar3 - *(float *)(lVar9 + 0xc + uVar10);
                fVar17 = fVar1;
                fVar18 = fVar2;
                fVar19 = fVar3;
                fVar16 = (float)FUN_18030381c(fVar16 * fVar16 + fVar4 * fVar4 + fVar5 * fVar5);
                if ((fVar20 < fVar16) && (*(int *)(param_1 + 0x70) < 0x40)) {
                  *(float *)(*(longlong *)(param_1 + 0x78) +
                            (longlong)*(int *)(param_1 + 0x70) * 0xc) =
                       fVar18 * *(float *)(param_1 + 0x14);
                  *(float *)(*(longlong *)(param_1 + 0x78) + 4 +
                            (longlong)*(int *)(param_1 + 0x70) * 0xc) = fVar17;
                  *(float *)(*(longlong *)(param_1 + 0x78) + 8 +
                            (longlong)*(int *)(param_1 + 0x70) * 0xc) =
                       fVar19 * *(float *)(param_1 + 0x14);
                  *(undefined4 *)
                   (*(longlong *)(param_1 + 0x80) + (longlong)*(int *)(param_1 + 0x70) * 4) = 0;
                  *(undefined4 *)
                   (*(longlong *)(param_1 + 0x98) + (longlong)*(int *)(param_1 + 0x70) * 4) =
                       *(undefined4 *)(param_1 + 0x1c);
                  *(int *)(param_1 + 0x70) = *(int *)(param_1 + 0x70) + 1;
                }
              }
              lVar9 = *plVar14;
              uVar11 = (int)uVar12 + 1;
              *(ulonglong *)(lVar9 + 4 + uVar10) = CONCAT44(fVar1,fVar2);
              *(float *)(lVar9 + 0xc + uVar10) = fVar3;
              uVar10 = uVar10 + 0x10;
              uVar12 = (ulonglong)uVar11;
            } while ((int)uVar11 < *(int *)(param_1 + 0x19d0));
          }
        }
      }
      uVar11 = (int)uVar15 + 1;
      uVar15 = (ulonglong)uVar11;
      plVar14 = plVar14 + 1;
    } while ((int)uVar11 < 2);
    if (0 < *(int *)(param_1 + 0x70)) {
      FUN_1800ec7c0(FUN_18007e420,param_1 + 0x70,0x16);
    }
  }
  return;
}



// ===================================================
// 18007E5F0  ->  FUN_18007e5f0  (entree 18007e5f0)
// ===================================================

void FUN_18007e5f0(void)

{
  longlong lVar1;
  longlong *plVar2;
  undefined8 uVar3;
  
  plVar2 = (longlong *)FUN_1800f06c0();
  if (plVar2 != (longlong *)0x0) {
    uVar3 = FUN_18010bef0(6);
    FUN_18010ce60(uVar3,4);
    FUN_1800f2470(plVar2);
    lVar1 = *plVar2;
    FUN_1800f0cb0(*(undefined4 *)(lVar1 + 0x2c),*(undefined4 *)(lVar1 + 0x34),
                  *(undefined2 *)(lVar1 + 0x54),*(undefined2 *)(lVar1 + 0x56),
                  *(undefined4 *)(lVar1 + 0x30),*(undefined4 *)(lVar1 + 0x58));
    FUN_1800f2060(plVar2);
    FUN_18010d3b0(uVar3);
  }
  return;
}



// ===================================================
// 18007D660  ->  FUN_18007d660  (entree 18007d660)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18007d660(char *param_1)

{
  longlong lVar1;
  longlong lVar2;
  undefined8 uStack_18;
  undefined8 uStack_10;
  
  if (param_1 != (char *)0x0) {
    if (((*param_1 != '\0') && (lVar1 = FUN_18010bef0(5), lVar1 != 0)) &&
       (lVar2 = FUN_1801957a0(*(undefined4 *)(param_1 + 0x20)), lVar2 != 0)) {
      FUN_18010cca0(lVar1,0);
      uStack_18 = _DAT_180348bb0;
      uStack_10 = _UNK_180348bb8;
      FUN_1800d1fa0(*(undefined4 *)(*(longlong *)(lVar1 + 8) + 0x10),0,*(undefined4 *)(lVar2 + 0x10)
                    ,0,&uStack_18);
      FUN_18010d190(lVar1);
    }
    return;
  }
  return;
}



// ===================================================
// 18007DFA0  ->  FUN_18007dfa0  (entree 18007dfa0)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18007dfa0(char *param_1)

{
  undefined8 uVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  int iVar4;
  longlong lVar5;
  longlong lVar6;
  longlong lVar7;
  undefined8 uVar8;
  undefined8 local_58;
  undefined8 uStack_50;
  undefined8 local_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  undefined8 uStack_30;
  undefined4 local_28;
  undefined4 local_24;
  
  if ((*param_1 != '\0') && (param_1[1] != '\0')) {
    lVar5 = FUN_18010bef0(5);
    lVar6 = FUN_18010bef0(2);
    uVar1 = *(undefined8 *)(lVar6 + 8);
    FUN_18010cca0(lVar5,0);
    FUN_18010d240(lVar5,1,0);
    FUN_180248bc0(0x800);
    uVar8 = *(undefined8 *)(lVar5 + 8);
    uVar2 = FUN_180195590(uVar8,0);
    uVar3 = FUN_180195840(uVar8,0);
    FUN_18024f500(0,0,uVar3,uVar2);
    FUN_180052090();
    iVar4 = FUN_1800ec090(0x16);
    if (iVar4 != 0) {
      FUN_1800ea4c0(0x16,0,0);
    }
    FUN_180248ba0();
    FUN_18010d190(lVar5);
    local_48 = _DAT_180351080;
    uStack_40 = _UNK_180351088;
    uStack_38 = _UNK_180351090;
    uStack_30 = _UNK_180351098;
    local_24 = DAT_180347cd8;
    local_28 = 0;
    lVar6 = FUN_18010bef0(5);
    lVar7 = FUN_1801957a0(*(undefined4 *)(param_1 + 0x28));
    if (lVar7 != 0) {
      FUN_18010cb20(param_1 + 0x38,*(undefined4 *)(lVar7 + 0x10),0,0);
      FUN_18010cca0(param_1 + 0x38,0);
      FUN_180175970(0x20);
      FUN_1800d2cb0(*(undefined4 *)(lVar7 + 0x10),*(undefined4 *)(*(longlong *)(lVar6 + 8) + 0x10),5
                    ,&local_48);
      FUN_180176960();
      FUN_18010d190(param_1 + 0x38);
    }
    local_58 = _DAT_180348bb0;
    uStack_50 = _UNK_180348bb8;
    uVar8 = FUN_18010bef0(2);
    FUN_1800d1f30(uVar8,0,lVar5,0,&local_58);
    FUN_18007dd00(param_1);
    FUN_18007dab0(param_1);
    FUN_18010ca10(uVar1);
    FUN_180007440();
  }
  return;
}



