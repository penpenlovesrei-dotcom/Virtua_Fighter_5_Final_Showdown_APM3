// ===================================================
// 1800236BA  ->  FUN_180023650  (entree 180023650)
// ===================================================

void FUN_180023650(longlong *param_1)

{
  int iVar1;
  longlong lVar2;
  int *piVar3;
  longlong lVar4;
  float fVar5;
  float fVar6;
  undefined8 uVar7;
  undefined1 auVar9 [16];
  uint uVar10;
  uint uVar11;
  undefined4 uVar12;
  uint uVar13;
  float fVar14;
  uint uVar15;
  undefined4 uVar16;
  undefined4 uVar17;
  undefined4 local_res8;
  undefined4 local_resc;
  undefined4 local_res10;
  undefined4 local_res14;
  float local_c8;
  float fStack_c4;
  undefined4 local_b8;
  undefined4 local_b4;
  float local_b0;
  undefined1 local_a8 [144];
  longlong lVar8;
  
  if ((*(byte *)(param_1 + 6) & 8) == 0) {
    local_res10 = *(undefined4 *)((longlong)param_1 + 0x44);
    local_res14 = (undefined4)param_1[9];
    uVar10 = 0;
    uVar12 = 0;
    local_res8 = 0;
    local_resc = 0;
    FUN_18016af60(&local_res8,*(undefined4 *)((longlong)param_1 + 0x8c),&local_res10,(int)param_1[8]
                 );
    uVar11 = *(uint *)(param_1 + 0xe);
    local_b8 = local_res8;
    local_b0 = *(float *)((longlong)param_1 + 0x4c);
    local_b4 = local_resc;
    lVar8 = param_1[0xd];
    if ((*(uint *)(param_1 + 6) & 0x100000) == 0) {
      uVar12 = 0;
      fStack_c4 = (float)((ulonglong)lVar8 >> 0x20);
      local_c8 = (float)lVar8;
      fVar5 = local_b0;
    }
    else {
      fVar5 = (float)*(uint *)(param_1[2] + 0x14);
      auVar9._0_4_ = (float)*(uint *)(param_1[2] + 0x18);
      auVar9._4_12_ = ZEXT812(0);
      lVar8 = auVar9._0_8_;
      fStack_c4 = auVar9._0_4_ * DAT_180346d38;
      local_c8 = fVar5 * DAT_180346d38;
      uVar11 = uVar10;
    }
    uVar17 = 0;
    uVar16 = 0;
    fVar14 = DAT_180346d38;
    FUN_180211a00(fVar5,lVar8);
    FUN_180213820(local_a8,&local_b8);
    FUN_180212d80(local_a8,(int)param_1[10]);
    FUN_180212eb0(local_a8,*(undefined4 *)((longlong)param_1 + 0x54));
    FUN_180213020(local_a8,*(float *)(param_1 + 0xb) * *(float *)((longlong)param_1 + 0x94) *
                           *(float *)(param_1 + 0x13));
    FUN_180213140(local_a8,*(float *)((longlong)param_1 + 0x5c) *
                           *(float *)((longlong)param_1 + 0x94),
                  *(float *)(param_1 + 0xc) * *(float *)(param_1 + 0x13),
                  *(undefined4 *)((longlong)param_1 + 100));
    uVar15 = 0;
    uVar10 = DAT_180346d60;
    FUN_180213180(local_a8,CONCAT44(uVar16,(uint)local_c8 ^ DAT_180346d60),
                  CONCAT44(uVar17,(uint)fStack_c4 ^ DAT_180346d60),
                  CONCAT44(uVar12,uVar11 ^ DAT_180346d60));
    lVar8 = param_1[2];
    iVar1 = *(int *)(lVar8 + 0x1c);
    if ((iVar1 != 0) && (lVar8 + 0x1c + (longlong)iVar1 != 0)) {
      fVar6 = (float)FUN_18001a3c0((longlong)iVar1 + 0x1c + lVar8,(int)param_1[0x11]);
      lVar4 = 0;
      fVar5 = (float)*(uint *)(lVar8 + 0x14) * fVar14;
      iVar1 = *(int *)(lVar8 + 0x1c);
      fVar6 = fVar6 - fVar5;
      uVar11 = 0;
      lVar2 = lVar4;
      if (iVar1 != 0) {
        lVar2 = lVar8 + 0x1c + (longlong)iVar1;
      }
      lVar8 = param_1[2];
      fVar5 = (float)FUN_18001a3c0(lVar2 + 8,(int)param_1[0x11],fVar5);
      piVar3 = (int *)(lVar8 + 0x1c);
      fVar14 = (float)*(uint *)(lVar8 + 0x18) * fVar14;
      iVar1 = *piVar3;
      fVar5 = fVar5 - fVar14;
      uVar13 = 0;
      if (iVar1 != 0) {
        lVar4 = (longlong)piVar3 + (longlong)iVar1;
      }
      uVar7 = FUN_18001a3c0(lVar4 + 0x10,(int)param_1[0x11],fVar14);
      FUN_180213180(local_a8,CONCAT44(uVar11 ^ uVar15,(uint)fVar6 ^ uVar10),
                    CONCAT44(uVar13 ^ uVar15,(uint)fVar5 ^ uVar10),
                    CONCAT44((uint)((ulonglong)uVar7 >> 0x20) ^ uVar15,(uint)uVar7 ^ uVar10));
    }
    if (param_1[4] != 0) {
      (**(code **)(*param_1 + 0xb8))(param_1,local_a8,param_1[4],(int)param_1[0x11]);
      return;
    }
    (**(code **)(*param_1 + 0xa8))(param_1,local_a8,param_1[3],(int)param_1[0x11],DAT_180346d3c);
  }
  return;
}



