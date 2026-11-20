// ===================================================
// 18018BBD0  ->  FUN_18018bbd0  (entree 18018bbd0)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18018bbd0(longlong param_1,int param_2,int param_3)

{
  int iVar1;
  int *piVar2;
  undefined4 *puVar3;
  longlong *plVar4;
  longlong *plVar5;
  int iVar6;
  longlong *plVar7;
  longlong lVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  undefined1 auVar13 [16];
  undefined1 auVar14 [64];
  float local_res8;
  float local_resc;
  float local_res20;
  float local_res24;
  float local_c8;
  float local_c4;
  undefined1 local_c0 [8];
  float fStack_b8;
  undefined4 local_b0 [3];
  int local_a4;
  int local_a0;
  
  DAT_180749980 = 0x31;
  _DAT_180749984 = 0x21d;
  DAT_1807499b4 = 0;
  DAT_1807499b8 = 1;
  _DAT_1807499bc = 1;
  DAT_1807499c4 = 0;
  DAT_1807499c8 = 0xffffffff;
  _DAT_18074998c = 0;
  _DAT_180749994 = 0;
  _DAT_18074999c = 0;
  _DAT_1807499a4 = 0;
  _DAT_1807499ac = 0;
  FUN_18024e8d0(0x11e);
  FUN_18024e8d0(0xac);
  FUN_180256d50(0x21d);
  FUN_180256da0(0x11e,0);
  FUN_18024e370(DAT_1807499b8,DAT_1807499c0,_DAT_1807499bc & 0xffffffff,DAT_1807499c4);
  if ((&DAT_18074998c)[DAT_180749988] == '\0') {
    FUN_18024e900(0x11e);
    (&DAT_18074998c)[DAT_180749988] = 1;
  }
  if (DAT_180749984 != 0x21d) {
    FUN_180256d50(0x21d);
    _DAT_180749984 = 0x21d;
  }
  FUN_18024bbc0();
  FUN_18024b650();
  FUN_18024a6a0(2);
  FUN_180247100(300);
  FUN_1802473b0(299);
  FUN_1802473b0(0x12f);
  FUN_180247600(3,0x161,0xc,&DAT_180749920);
  FUN_180247500(2,0x161,8,&DAT_180749950);
  FUN_180248bc0(0x800);
  if (param_3 == 0x11) {
    piVar2 = (int *)FUN_18016b0c0();
    param_3 = *piVar2;
  }
  FUN_18016aec0(local_b0,param_3);
  *(undefined4 *)(param_1 + 0x830) = local_b0[0];
  if (param_2 != 1) {
    auVar14 = ZEXT464((uint)((float)local_a4 * DAT_180346d38));
    fVar11 = (float)local_a0 * DAT_180346d38;
    fVar9 = (float)FUN_180051740();
    fVar12 = (fVar11 * *(float *)(param_1 + 0x810) * DAT_18034af40) / fVar9;
    fVar10 = (fVar11 * DAT_18034af40) / fVar9;
    FUN_18024b790(0x17b);
    FUN_18024b650();
    FUN_18024b410((double)(float)((uint)fVar12 ^ DAT_180346d60),(double)fVar12,(double)fVar10,
                  (double)(float)((uint)fVar10 ^ DAT_180346d60),_DAT_1804033d0,_UNK_1804033d8);
    FUN_1802575e0((double)auVar14._0_4_,(double)fVar11,(double)fVar9,(double)auVar14._0_4_,
                  (double)fVar11,0,0,DAT_180346d40,0);
    FUN_18024b790(0x17a);
    FUN_18024b650();
  }
  iVar6 = *(int *)(param_1 + 0x814);
  piVar2 = (int *)FUN_18016b0c0();
  if (iVar6 == *piVar2) {
    iVar6 = *(int *)(param_1 + 0x830);
    auVar13._0_4_ = (float)local_a0;
    auVar13._4_8_ = SUB128(ZEXT812(0),4);
    auVar13._12_4_ = 0;
    iVar1 = iVar6;
    fVar11 = 0.0;
    fVar9 = 0.0;
    fVar10 = (float)local_a4;
  }
  else {
    _local_c0 = *(undefined1 (*) [16])(param_1 + 0x818);
    iVar1 = *(int *)(param_1 + 0x830);
    auVar13 = vshufps_avx(_local_c0,_local_c0,0xff);
    fVar11 = (float)local_c0._0_4_;
    fVar9 = (float)local_c0._4_4_;
    fVar10 = fStack_b8;
  }
  auVar14 = ZEXT1664(auVar13);
  local_res20 = 0.0;
  local_res24 = 0.0;
  local_c8 = 0.0;
  local_c4 = 0.0;
  local_res8 = fVar11;
  local_resc = fVar9;
  FUN_18016af60(&local_res20,iVar1,&local_res8,iVar6);
  local_res8 = fVar10 + fVar11;
  local_resc = auVar14._0_4_ + fVar9;
  FUN_18016af60(&local_c8,*(undefined4 *)(param_1 + 0x830),&local_res8,iVar6);
  if (param_2 != 1) {
    FUN_18024f500((int)local_res20,(int)local_res24,(int)(local_c8 - local_res20),
                  (int)(local_c4 - local_res24));
  }
  iVar6 = 0x11;
  if ((param_2 == 1) && (*(int *)(param_1 + 0x82c) != 0x11)) {
    piVar2 = (int *)FUN_18016b0c0();
    iVar6 = *piVar2;
    puVar3 = (undefined4 *)FUN_18016b0c0();
    *puVar3 = *(undefined4 *)(param_1 + 0x82c);
  }
  lVar8 = 0x20;
  plVar5 = (longlong *)((longlong)param_2 * 0x200 + 0x10 + param_1);
  do {
    plVar4 = (longlong *)*plVar5;
    plVar7 = (longlong *)*plVar4;
    if (plVar7 != plVar4) {
      do {
        thunk_FUN_18018b010(plVar7 + 2);
        plVar7 = (longlong *)*plVar7;
      } while (plVar7 != plVar4);
      plVar4 = (longlong *)*plVar5;
      plVar7 = (longlong *)*plVar4;
    }
    *plVar4 = (longlong)plVar4;
    *(longlong *)(*plVar5 + 8) = *plVar5;
    plVar5[1] = 0;
    if (plVar7 != (longlong *)*plVar5) {
      do {
        plVar4 = (longlong *)*plVar7;
        FUN_1802fdd80(plVar7,0xf8);
        plVar7 = plVar4;
      } while (plVar4 != (longlong *)*plVar5);
    }
    plVar5 = plVar5 + 2;
    lVar8 = lVar8 + -1;
  } while (lVar8 != 0);
  if ((param_2 == 1) && (iVar6 != 0x11)) {
    piVar2 = (int *)FUN_18016b0c0();
    *piVar2 = iVar6;
  }
  FUN_180248ba0();
  FUN_18024a650();
  if (DAT_180749984 == 0x21d) {
  }
  else {
    FUN_180256d50(0x21d);
    _DAT_180749984 = 0x21d;
    DAT_180749988 = 0;
  }
  if ((&DAT_18074998c)[DAT_180749988] == '\x01') {
    FUN_18024e8d0(0x11e);
    (&DAT_18074998c)[DAT_180749988] = 0;
  }
  if ((((DAT_1807499b8 != 1) || (DAT_1807499c0 != 0)) || (DAT_1807499bc != 1)) ||
     (DAT_1807499c4 != 0)) {
    FUN_18024e370(1,0,1,0);
    DAT_1807499b8 = 1;
    _DAT_1807499bc = 1;
    DAT_1807499c4 = 0;
  }
  FUN_180246fc0(DAT_180346d3c,DAT_180346d3c,DAT_180346d3c,DAT_180346d3c);
  FUN_180176960();
  FUN_18024bb70();
  return;
}



