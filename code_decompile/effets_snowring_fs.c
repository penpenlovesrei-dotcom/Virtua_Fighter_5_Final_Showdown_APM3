// ===================================================
// 18007D820  ->  FUN_18007d820  (entree 18007d820)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18007d820(undefined1 *param_1,int param_2)

{
  undefined4 uVar1;
  undefined1 auVar2 [16];
  float fVar3;
  float fVar4;
  int iVar5;
  undefined8 uVar6;
  longlong lVar7;
  ulonglong uVar8;
  longlong lVar9;
  longlong *plVar10;
  undefined4 *puVar11;
  uint uVar12;
  undefined8 local_38;
  undefined8 uStack_30;
  ulonglong uVar13;
  
  if (param_2 == DAT_180643450) {
    *(undefined4 *)(param_1 + 0xc) = DAT_180643454;
    *(undefined4 *)(param_1 + 0x10) = DAT_180643458;
    fVar4 = DAT_180346d3c;
    fVar3 = DAT_18064345c * DAT_180346d38;
    *(undefined4 *)(param_1 + 0x18) = 0xff000000;
    *(float *)(param_1 + 0x14) = fVar4 / fVar3;
    *(undefined4 *)(param_1 + 0x1c) = DAT_180643460;
    *(undefined4 *)(param_1 + 0x20) = DAT_180643464;
    *(undefined4 *)(param_1 + 0x24) = DAT_180643468;
    *(undefined4 *)(param_1 + 0x28) = DAT_18064346c;
    *(undefined4 *)(param_1 + 0x2c) = DAT_180643470;
    *(undefined4 *)(param_1 + 0x30) = DAT_180643474;
    *(undefined4 *)(param_1 + 8) = DAT_180643478;
    FUN_18010ca20(4,1);
    FUN_18010bdc0(0,&LAB_18007df90,param_1);
    iVar5 = 0x10;
    *(undefined4 *)(param_1 + 0x19d0) = 0x10;
    plVar10 = (longlong *)(param_1 + 0x19d8);
    lVar9 = 2;
    do {
      uVar8 = (ulonglong)iVar5;
      auVar2._8_8_ = 0;
      auVar2._0_8_ = uVar8;
      uVar6 = SUB168(ZEXT816(0x10) * auVar2,0);
      if (SUB168(ZEXT816(0x10) * auVar2,8) != 0) {
        uVar6 = 0xffffffffffffffff;
      }
      lVar7 = FUN_180218930(uVar6);
      if (lVar7 == 0) {
        lVar7 = 0;
      }
      else if (uVar8 != 0) {
        puVar11 = (undefined4 *)(lVar7 + 0xc);
        do {
          puVar11[-3] = 0xffffffff;
          *(undefined8 *)(puVar11 + -2) = 0;
          *puVar11 = 0;
          puVar11 = puVar11 + 4;
          uVar8 = uVar8 - 1;
        } while (uVar8 != 0);
      }
      *plVar10 = lVar7;
      iVar5 = *(int *)(param_1 + 0x19d0);
      if (0 < iVar5) {
        puVar11 = &DAT_180350ff0;
        uVar8 = 0;
        uVar13 = 0;
        do {
          uVar1 = *puVar11;
          puVar11 = puVar11 + 1;
          *(undefined4 *)(uVar8 + lVar7) = uVar1;
          uVar8 = uVar8 + 0x10;
          lVar7 = *plVar10;
          uVar12 = (int)uVar13 + 1;
          uVar13 = (ulonglong)uVar12;
          *(undefined8 *)(lVar7 + -0xc + uVar8) = 0;
          *(undefined4 *)(lVar7 + -4 + uVar8) = 0;
          iVar5 = *(int *)(param_1 + 0x19d0);
        } while ((int)uVar12 < iVar5);
      }
      plVar10 = plVar10 + 1;
      lVar9 = lVar9 + -1;
    } while (lVar9 != 0);
    *(undefined4 *)(param_1 + 1) = 0x1000001;
    FUN_180087550(4,&LAB_18007d660,param_1,0);
    *param_1 = 1;
    lVar9 = FUN_18010bef0(5);
    if ((lVar9 != 0) && (lVar7 = FUN_1801957a0(*(undefined4 *)(param_1 + 0x20)), lVar7 != 0)) {
      FUN_18010cca0(lVar9,0);
      local_38 = _DAT_180348bb0;
      uStack_30 = _UNK_180348bb8;
      FUN_1800d1fa0(*(undefined4 *)(*(longlong *)(lVar9 + 8) + 0x10),0,*(undefined4 *)(lVar7 + 0x10)
                    ,0,&local_38);
      FUN_18010d190(lVar9);
    }
  }
  return;
}



// ===================================================
// 18007DF90  ->  thunk_FUN_18007dfa0  (entree 18007df90)
// ===================================================

void thunk_FUN_18007dfa0(void)

{
  FUN_18007dfa0();
  return;
}



// ===================================================
// 18007D7B0  ->  FUN_18007d7b0  (entree 18007d7b0)
// ===================================================

void FUN_18007d7b0(longlong param_1)

{
  if (((*(char *)(param_1 + 0x5c) != '\0') && (*(char *)(param_1 + 0x68) != '\0')) &&
     (*(char *)(param_1 + 0x69) == '\x01')) {
    FUN_18007e180(param_1 + 0x68);
    if (0 < *(int *)(param_1 + 0x608)) {
      FUN_1800ec7c0(FUN_18007e420,(int *)(param_1 + 0x608),0x16);
    }
    FUN_1800ec520(*(undefined4 *)(param_1 + 0x98),FUN_18007e5f0,0);
    return;
  }
  return;
}



// ===================================================
// 18007DD00  ->  FUN_18007dd00  (entree 18007dd00)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18007dd00(longlong param_1)

{
  longlong lVar1;
  undefined1 auVar2 [16];
  undefined1 auVar3 [16];
  undefined1 auVar4 [32];
  undefined1 auVar5 [32];
  longlong lVar6;
  longlong lVar7;
  longlong lVar8;
  int iVar9;
  int iVar10;
  undefined1 auVar11 [16];
  undefined1 auVar12 [64];
  undefined1 auVar13 [64];
  undefined1 local_88 [32];
  undefined1 local_68 [32];
  undefined1 local_48 [16];
  
  lVar6 = FUN_18010bef0(6);
  lVar1 = *(longlong *)(lVar6 + 8);
  lVar7 = FUN_1801957a0(*(undefined4 *)(param_1 + 0x28));
  if ((lVar7 != 0) && (lVar8 = FUN_1801957a0(*(undefined4 *)(param_1 + 0x2c)), lVar8 != 0)) {
    FUN_1800d5020(0,1);
    FUN_180256d50(0x21d);
    FUN_180256da0(*(undefined4 *)(lVar7 + 0x14),*(undefined4 *)(lVar7 + 0x10));
    FUN_180256d50(0x21e);
    FUN_180256da0(*(undefined4 *)(lVar8 + 0x14),*(undefined4 *)(lVar8 + 0x10));
    FUN_180248bc0(0x800);
    FUN_180052090();
    iVar10 = (int)*(short *)(lVar1 + 0xc);
    iVar9 = (int)*(short *)(lVar1 + 0xe);
    FUN_18024b790(0x17b);
    FUN_18024bbc0();
    FUN_18024b650();
    FUN_180257840(0,(double)iVar10,0,(double)iVar9);
    FUN_18024b790(0x17a);
    FUN_18024bbc0();
    FUN_18024f500(0,0,iVar10,iVar9);
    FUN_18010cca0(lVar6,0);
    FUN_180175970(0x1f);
    local_48._0_12_ = ZEXT812(0);
    local_48._12_4_ = 0;
    local_88 = ZEXT1232(ZEXT812(0));
    auVar12 = ZEXT1264(CONCAT84(SUB128(ZEXT812(0),4),(float)iVar10));
    auVar13 = ZEXT1264(CONCAT84(SUB128(ZEXT812(0),4),(float)iVar9));
    local_68 = local_88;
    FUN_180215c50();
    auVar4 = local_68;
    auVar11._0_12_ = ZEXT812(0);
    auVar11._12_4_ = 0;
    auVar2 = vunpcklps_avx(auVar11,auVar13._0_16_);
    local_68._0_8_ = auVar2._0_8_;
    auVar5 = local_68;
    auVar3 = vunpcklps_avx(auVar11,auVar11);
    local_68._20_12_ = auVar4._20_12_;
    local_68._0_12_ = auVar5._0_12_;
    local_68._12_8_ = auVar3._0_8_;
    auVar3 = vunpcklps_avx(auVar12._0_16_,auVar11);
    local_68._8_4_ = 0;
    local_68._20_4_ = 0;
    local_68._24_8_ = auVar3._0_8_;
    auVar2 = vunpcklps_avx(auVar12._0_16_,auVar13._0_16_);
    auVar3._8_8_ = 0;
    auVar3._0_8_ = auVar2._0_8_;
    local_48 = auVar3 << 0x20;
    local_88._8_8_ = _UNK_1803510a8;
    local_88._0_8_ = _DAT_1803510a0;
    local_88._16_8_ = _UNK_1803510b0;
    local_88._24_8_ = _UNK_1803510b8;
    FUN_18018eb00(local_68,local_88,1);
    FUN_18010d190(lVar6);
    FUN_180176960();
    FUN_18024bb70();
    FUN_18024b790(0x17b);
    FUN_18024bb70();
    FUN_18024b790(0x17a);
    FUN_180256d50(0x21e);
    FUN_180256da0(*(undefined4 *)(lVar8 + 0x14),0);
    FUN_180256d50(0x21d);
    FUN_180256da0(*(undefined4 *)(lVar7 + 0x14),0);
    FUN_180256d50(0x21d);
    FUN_180248ba0();
  }
  return;
}



// ===================================================
// 18007DAB0  ->  FUN_18007dab0  (entree 18007dab0)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18007dab0(longlong param_1)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar3;
  longlong lVar4;
  longlong lVar5;
  undefined4 local_res8;
  undefined4 local_resc;
  undefined8 in_stack_ffffffffffffffa8;
  uint uVar6;
  undefined8 local_38;
  undefined8 uStack_30;
  undefined8 local_28;
  undefined8 uStack_20;
  
  uVar6 = (uint)((ulonglong)in_stack_ffffffffffffffa8 >> 0x20);
  lVar4 = FUN_18010bef0(6);
  lVar5 = FUN_1801957a0(*(undefined4 *)(param_1 + 0x28));
  if (lVar5 != 0) {
    uVar1 = *(undefined4 *)(lVar5 + 0x10);
    uVar2 = *(undefined4 *)(*(longlong *)(lVar4 + 8) + 0x10);
    FUN_18010cca0(param_1 + 0x38,0);
    if ((*(char *)(param_1 + 4) == '\0') || (iVar3 = *(int *)(param_1 + 8), iVar3 == 0)) {
      local_28 = _DAT_180348bb0;
      uStack_20 = _UNK_180348bb8;
      FUN_1800d1fa0(uVar1,0,uVar2,0,&local_28);
    }
    else if (iVar3 == 1) {
      local_28 = 0;
      uStack_20 = 0;
      local_res8 = DAT_180346d3c;
      local_resc = DAT_180346d3c;
      local_38 = _DAT_180348bb0;
      uStack_30 = _UNK_180348bb8;
      FUN_1800d0770(uVar1,0,uVar2,0,(ulonglong)uVar6 << 0x20,&local_res8,&local_38,&local_28);
    }
    else if (iVar3 == 2) {
      local_28 = 0;
      uStack_20 = 0;
      local_res8 = DAT_180346d3c;
      local_resc = DAT_180346d3c;
      local_38 = _DAT_180348bb0;
      uStack_30 = _UNK_180348bb8;
      FUN_1800d0770(uVar1,0,uVar2,0,CONCAT44(uVar6,1),&local_res8,&local_38,&local_28);
    }
    else if (iVar3 == 3) {
      local_28 = 0;
      uStack_20 = 0;
      local_res8 = DAT_180346d3c;
      local_resc = DAT_180346d3c;
      local_38 = _DAT_180348bb0;
      uStack_30 = _UNK_180348bb8;
      FUN_1800d0770(uVar1,0,uVar2,0,CONCAT44(uVar6,2),&local_res8,&local_38,&local_28);
    }
    else if (iVar3 == 4) {
      local_38 = 0;
      uStack_30 = 0;
      local_res8 = DAT_180346d3c;
      local_resc = DAT_180346d3c;
      local_28 = _DAT_180348bb0;
      uStack_20 = _UNK_180348bb8;
      FUN_1800d0770(uVar1,0,uVar2,0,CONCAT44(uVar6,3),&local_res8,&local_28,&local_38);
    }
    FUN_18010d190(param_1 + 0x38);
  }
  return;
}



