// ===================================================
// 81BC29C  ->  FUN_081bbee4  (entree 081bbee4)
// ===================================================

void FUN_081bbee4(int param_1,int param_2)

{
  uint uVar1;
  bool bVar2;
  undefined2 uVar3;
  short sVar4;
  int iVar5;
  int iVar6;
  undefined2 *puVar7;
  undefined2 *puVar8;
  int *piVar9;
  _List_node_base *p_Var10;
  int iVar11;
  int iVar12;
  int iVar13;
  longdouble lVar14;
  float local_b0;
  undefined4 local_94;
  uint local_90;
  undefined1 local_8c [32];
  undefined2 local_6c [8];
  undefined4 local_5c;
  undefined2 local_4c;
  undefined2 uStack_4a;
  short local_3c;
  undefined2 uStack_3a;
  int local_2c;
  
  local_94 = *(uint *)(param_1 + 0x398);
  local_90 = *(uint *)(param_1 + 0x39c) | 2;
  *(byte *)(param_2 + 0x2c9) = *(byte *)(param_2 + 0x2c9) | 8;
  FUN_081793e6(*(undefined4 *)(param_2 + 0x52f8),0);
  if ((local_90 & 0x40) != 0) goto LAB_081bbff3;
  if ((local_90 & 0x100) == 0) {
    local_94 = 2;
    uVar1 = *(uint *)(param_2 + 0x638);
    if (((uVar1 & 0x400) == 0) && ((uVar1 & 0x20000) == 0)) goto LAB_081bbff3;
    if (*(int *)(param_1 + 0x6a0) == 0xc || *(int *)(param_1 + 0x6a0) == 0xe) goto LAB_081bc266;
    if (((*(float *)(param_2 + 0x4d0) < *(float *)(param_2 + 0x894)) && ((uVar1 & 0x800) == 0)) &&
       (-1 < *(char *)(param_2 + 0x2c8))) {
      if ((*(byte *)(param_2 + 0x63d) & 1) != 0) {
        local_94 = 0x40;
        local_90 = local_90 | 0x40;
      }
      goto LAB_081bbff3;
    }
  }
  else {
    if (((*(byte *)(param_2 + 0x629) & 4) == 0) ||
       ((uVar1 = *(uint *)(param_2 + 0x638), (uVar1 & 0x400) == 0 && ((uVar1 & 0x20000) == 0))))
    goto LAB_081bbff3;
    if ((*(int *)(param_1 + 0x6a0) == 0xc) ||
       ((*(int *)(param_1 + 0x6a0) == 0xe && ((uVar1 & 0x800) != 0)))) {
LAB_081bc266:
      local_94 = 0x4000;
      local_90 = local_90 | 0x4000;
      goto LAB_081bbff3;
    }
    if (((*(float *)(param_2 + 0x4d0) < *(float *)(param_2 + 0x894)) &&
        ((*(byte *)(param_2 + 0x639) & 8) == 0)) && (-1 < *(char *)(param_2 + 0x2c8))) {
      if ((local_94 & 0x200) == 0) {
        local_94 = 2;
      }
      goto LAB_081bbff3;
    }
  }
  local_94 = 0x8000;
LAB_081bbff3:
  *(uint *)(param_1 + 0x388) = local_94;
  *(uint *)(param_1 + 0x398) = local_94;
  *(uint *)(param_1 + 0x38c) = local_90;
  *(uint *)(param_1 + 0x39c) = local_90;
  iVar5 = FUN_081bab9e(param_2,param_1 + 0x61c,&local_94,&local_90);
  iVar6 = FUN_081d5c9c(iVar5);
  puVar7 = (undefined2 *)FUN_081d5f84(iVar5,0,0x23);
  local_2c._0_2_ = 0;
                    /* try { // try from 081bc079 to 081bc07d has its CatchHandler @ 081bc285 */
  puVar8 = (undefined2 *)FUN_081b6a4a(param_1);
  if (((iVar5 == 0xc30) && (*(int *)(param_1 + 0x6c0) - 8U < 2)) || (puVar7 == (undefined2 *)0x0)) {
    if (local_94._1_1_ < '\0') {
      local_b0 = *(float *)(puVar8 + 10);
      uVar3 = *puVar8;
    }
    else {
      local_b0 = *(float *)(puVar8 + 0xc);
      uVar3 = puVar8[1];
      if ((((local_90 & 0x40) == 0) && ((*(byte *)(param_2 + 0x63d) & 1) == 0)) &&
         ((*(byte *)(iVar6 + 0xc) & 0x80) == 0)) {
        if ((*(byte *)(param_2 + 0x63a) & 0x80) == 0) {
          if ((local_90 & 4) != 0) {
            local_b0 = *(float *)(puVar8 + 0x10);
            uVar3 = puVar8[3];
          }
        }
        else {
          local_b0 = *(float *)(puVar8 + 0x12);
          uVar3 = puVar8[4];
        }
      }
      else {
        local_b0 = *(float *)(puVar8 + 0xe);
        uVar3 = puVar8[2];
      }
      local_b0 = *(float *)(param_2 + 0x3c0) * local_b0;
    }
  }
  else {
    local_b0 = *(float *)(puVar7 + 2);
    uVar3 = *puVar7;
  }
  local_2c = CONCAT22(local_2c._2_2_,uVar3);
  local_3c = 0xd60;
  _local_4c = CONCAT22(uStack_4a,0x870);
  bVar2 = false;
  if (((*(byte *)(param_2 + 0x647) & 1) != 0) && (local_94._1_1_ < '\0')) {
    piVar9 = *(int **)(param_2 + 0x410);
    if (piVar9 != (int *)(param_2 + 0x410)) {
      do {
        if (piVar9[2] == *(int *)(param_2 + 0x61c)) goto LAB_081bc131;
        piVar9 = (int *)*piVar9;
      } while (piVar9 != (int *)(param_2 + 0x410));
    }
    bVar2 = true;
                    /* try { // try from 081bc115 to 081bc130 has its CatchHandler @ 081bc443 */
    p_Var10 = operator_new(0xc);
    *(int *)(p_Var10 + 8) = *(int *)(param_2 + 0x61c);
    std::_List_node_base::hook(p_Var10);
  }
LAB_081bc131:
  sVar4 = (short)local_2c;
  if (((*(short *)(param_2 + 0x3f8) < 3) || ((*(byte *)(iVar6 + 0xe) & 0x80) != 0)) || (bVar2)) {
    *(undefined1 *)(param_2 + 0x40c) = 0;
  }
  else {
    *(undefined1 *)(param_2 + 0x40c) = 1;
    if (local_94._1_1_ < '\0') {
      local_3c = (short)_local_4c;
    }
    local_5c = CONCAT22(local_5c._2_2_,0xc200);
    if (sVar4 < -0x3e00) {
      local_5c = (uint)local_5c._2_2_ << 0x10;
    }
    iVar12 = (int)(short)(*(short *)(param_2 + 0x3f8) + -2);
    iVar11 = 0;
    iVar13 = local_2c;
    if (0 < iVar12) {
      do {
        iVar13 = (int)(short)iVar13 - (int)local_3c;
        if ((short)iVar13 < (short)local_5c) {
          iVar13 = local_5c;
        }
        iVar11 = iVar11 + 1;
        sVar4 = (short)iVar13;
        local_2c = CONCAT22(local_2c._2_2_,sVar4);
      } while (iVar11 < iVar12);
    }
  }
  if (0x3e00 < sVar4) {
    local_2c = CONCAT22(local_2c._2_2_,0x3e00);
  }
  *(float *)(param_2 + 0x3c0) = local_b0;
  local_6c[0] = (undefined2)local_2c;
                    /* try { // try from 081bc193 to 081bc197 has its CatchHandler @ 081bc372 */
  FUN_081b8492(param_2,param_1,local_6c);
  if ((*(byte *)(iVar6 + 0xd) & 1) != 0) {
    *(short *)(param_2 + 0x418) = *(short *)(param_2 + 0x418) + 1;
  }
  lVar14 = (longdouble)FUN_081b75e6(param_1,param_2);
                    /* try { // try from 081bc1ca to 081bc217 has its CatchHandler @ 081bc443 */
  FUN_081f409c(param_2,(float)lVar14);
  FUN_081b98ec(param_1,param_2,(float)lVar14);
  FUN_081f3af4(local_8c,8);
  FUN_081f4034(param_2,8,iVar5,local_8c,0);
  return;
}



