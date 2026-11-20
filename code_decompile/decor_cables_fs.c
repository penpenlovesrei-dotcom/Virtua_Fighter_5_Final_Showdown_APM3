// ===================================================
// 18010B6CB  ->  FUN_18010b570  (entree 18010b570)
// ===================================================

void FUN_18010b570(longlong param_1)

{
  undefined1 auVar1 [16];
  char cVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  uint uVar6;
  undefined8 uVar7;
  longlong lVar8;
  undefined1 auVar9 [64];
  undefined4 uVar10;
  undefined4 local_res10;
  undefined4 local_res14;
  undefined8 in_stack_ffffffffffffffb0;
  ulonglong uVar11;
  
  uVar10 = (undefined4)((ulonglong)in_stack_ffffffffffffffb0 >> 0x20);
  lVar8 = ((longlong)*(int *)(&DAT_1803a50e0 + (longlong)*(int *)(DAT_18070fc68 + 0x15c) * 4) + 7) *
          0x38 + DAT_18070fc68;
  iVar3 = FUN_1800ec090(0xd);
  if (((((iVar3 == 0) && (iVar3 = FUN_1800ec090(0xf), iVar3 == 0)) &&
       (iVar3 = FUN_1800ec090(0xe), iVar3 == 0)) &&
      ((iVar3 = FUN_1800ec090(10), iVar3 == 0 && (iVar3 = FUN_1800ec090(0xc), iVar3 == 0)))) &&
     (iVar3 = FUN_1800ec090(0xb), iVar3 == 0)) {
    FUN_18010cca0(lVar8,0);
    FUN_18010b160(0x4000,0,0,0,0);
    FUN_18010d190(lVar8);
    return;
  }
  FUN_18010cca0(lVar8,0);
  FUN_180248bc0(0x800);
  uVar7 = *(undefined8 *)(lVar8 + 8);
  uVar4 = FUN_180195590(uVar7,0);
  uVar5 = FUN_180195840(uVar7,0);
  FUN_18024f500(0,0,uVar5,uVar4);
  FUN_180052090();
  FUN_1800d5020(0,1);
  FUN_1800881f0(0);
  FUN_1800881f0(1);
  FUN_1802541d0(0x100);
  FUN_18010d240(lVar8,1,0);
  FUN_1800f0c80("S_REFL");
  DAT_1807154a0._4_4_ = 1;
  uVar6 = FUN_18018f580();
  auVar1 = vpcmpeqd_avx(ZEXT416(uVar6),ZEXT416(10));
  auVar1 = vblendvps_avx(ZEXT416(DAT_18034fea4),ZEXT416(DAT_1803a5230),auVar1);
  local_res10 = auVar1._0_4_;
  uVar11 = CONCAT44(uVar10,local_res10);
  uVar10 = 0;
  FUN_180252990(0x48b,0x16,0,DAT_180347cd8,0,uVar11);
  iVar3 = FUN_1800ec090(0xd);
  if (iVar3 != 0) {
    FUN_1800ea4c0(0xd,0,0);
  }
  iVar3 = FUN_1800ec090(0xf);
  if (iVar3 != 0) {
    FUN_1800ea4c0(0xf,0,0);
  }
  iVar3 = FUN_1800ec090(0xe);
  if (iVar3 != 0) {
    FUN_1800ea4c0(0xe,0,0);
  }
  auVar9 = ZEXT464(DAT_180346d3c);
  uVar6 = 0;
  if (*(int *)(param_1 + 0x154) != 2) goto LAB_18010b89b;
  uVar7 = FUN_1801509b0();
  cVar2 = FUN_180150a30(uVar7,0);
  if ((cVar2 == '\0') || (iVar3 = FUN_180150840(uVar7,0), iVar3 != 0x14)) {
    cVar2 = FUN_180150a30(uVar7,1);
    uVar4 = (undefined4)(uVar11 >> 0x20);
    if (cVar2 != '\0') {
      iVar3 = FUN_180150840(uVar7,1);
      uVar4 = (undefined4)(uVar11 >> 0x20);
      if (iVar3 == 0x14) goto LAB_18010b7d7;
    }
  }
  else {
LAB_18010b7d7:
    FUN_18010ce60(DAT_18070fc68 + 0x1c0,0xf);
    FUN_180256d50(0x22c);
    uVar11 = uVar11 & 0xffffffff00000000;
    FUN_180256f20(0x11e,0,0,0,0,uVar11,0x200,0x100);
    uVar4 = (undefined4)(uVar11 >> 0x20);
  }
  DAT_1807154a0._4_4_ = 0;
  FUN_180252990(0x48b,0x16,0,auVar9._0_8_,uVar10,CONCAT44(uVar4,uVar10));
  iVar3 = FUN_1800ec090(10);
  if (iVar3 != 0) {
    FUN_1800ea4c0(10,0,0);
  }
  iVar3 = FUN_1800ec090(0xc);
  if (iVar3 != 0) {
    FUN_1800ea4c0(0xc,0,0);
  }
  iVar3 = FUN_1800ec090(0xb);
  if (iVar3 != 0) {
    FUN_1800ea4c0(0xb,0,0);
  }
LAB_18010b89b:
  DAT_1807154a0._4_4_ = 0;
  FUN_1800f0c80(0);
  FUN_1800d4830();
  FUN_180088150();
  FUN_180248ba0();
  FUN_18010d190(lVar8);
  if (*(int *)(param_1 + 0x1c) != 0) {
    do {
      local_res10 = auVar9._0_4_;
      local_res14 = local_res10;
      FUN_1800d06d0(lVar8,0,lVar8,0,*(undefined4 *)(param_1 + 0x20),&local_res10);
      uVar6 = uVar6 + 1;
    } while (uVar6 < *(uint *)(param_1 + 0x1c));
  }
  FUN_180007440();
  return;
}



// ===================================================
// 180105636  ->  FUN_180105600  (entree 180105600)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_180105600(int *param_1)

{
  undefined1 auVar1 [12];
  undefined1 auVar2 [12];
  int iVar3;
  int iVar4;
  longlong lVar5;
  int *piVar6;
  longlong lVar7;
  undefined *puVar8;
  undefined1 auVar9 [64];
  undefined4 local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined8 local_48;
  undefined8 uStack_40;
  undefined4 local_38;
  undefined4 local_34;
  
  iVar4 = 1;
  local_38 = 2;
  local_48 = _DAT_1803a4060;
  uStack_40 = _UNK_1803a4068;
  local_34 = 1;
  iVar3 = FUN_18018f580();
  puVar8 = &DAT_180644a78;
  if (iVar3 != 0x13) {
    puVar8 = &DAT_180644a68;
  }
  FUN_18024eab0(0xb7,&local_58);
  FUN_18024e3c0(0,0,0,0);
  iVar3 = *param_1;
  if (0 < iVar3) {
    piVar6 = param_1 + 0x189;
    lVar5 = 1;
    auVar9 = ZEXT464(DAT_180346d3c);
    do {
      if (iVar4 != iVar3 + -1) {
        FUN_18010cca0(param_1 + (longlong)iVar4 * 0xe + 6,0);
        lVar7 = lVar5 - ((ulonglong)(iVar4 == *param_1) + 1);
        FUN_180256d50(0x21d);
        FUN_180256da0(0x11e,param_1[lVar7 + 0x15b]);
        FUN_1802575a0(0x11e,0x1b1,0x1ac);
        FUN_1802575a0(0x11e,0x1b2,0x1ac);
        FUN_1802541d0(0x4000);
        FUN_18024f500(0,0,*piVar6,piVar6[9]);
        if (iVar4 < param_1[1] + -1) {
          DAT_1807154a8._4_4_ = 2;
        }
        else {
          DAT_1807154a8._4_4_ =
               *(undefined4 *)((longlong)&local_48 + (longlong)(iVar4 - param_1[1]) * 4 + 4);
          if ((param_1[2] != 0) && (iVar4 == param_1[1])) {
            DAT_1807154a8._4_4_ = 0;
          }
        }
        FUN_180175970(0x13);
        FUN_180252b00(0x48b,2,puVar8);
        auVar1._4_8_ = SUB128(ZEXT812(0),4);
        auVar1._0_4_ = (float)param_1[lVar7 + 0x1a3];
        auVar2._4_8_ = SUB128(ZEXT812(0),4);
        auVar2._0_4_ = (float)param_1[lVar7 + 0x19a];
        FUN_180104790(param_1,auVar2._0_8_,auVar1._0_8_,auVar9._0_8_,auVar9._0_4_,0);
        iVar3 = *param_1;
      }
      iVar4 = iVar4 + 1;
      lVar5 = lVar5 + 1;
      piVar6 = piVar6 + 1;
    } while (iVar4 <= iVar3);
  }
  FUN_18024e3c0(local_58,local_54,local_50,local_4c);
  return;
}



