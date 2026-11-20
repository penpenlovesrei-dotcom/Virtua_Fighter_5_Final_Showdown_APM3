// ===================================================
// 180172E24  ->  FUN_180172730  (entree 180172730)
// ===================================================

void FUN_180172730(longlong param_1,int param_2)

{
  uint7 uVar1;
  char cVar2;
  longlong lVar3;
  char *pcVar4;
  undefined1 uVar5;
  longlong lVar6;
  int iVar7;
  longlong lVar8;
  undefined8 local_res8;
  undefined8 local_res18;
  longlong *plVar9;
  undefined4 uVar10;
  undefined8 local_128;
  undefined8 local_120;
  undefined8 local_118;
  undefined8 local_110;
  undefined8 local_108;
  undefined8 local_100;
  longlong local_f8;
  undefined4 local_f0;
  longlong local_e8;
  undefined4 local_e0;
  char *local_d8 [4];
  char *local_b8;
  char *local_b0;
  char *local_a8;
  char *local_a0;
  char *local_98;
  char *local_90;
  char *local_88;
  char *local_80;
  char *local_78;
  char *local_70;
  char *local_68 [4];
  char *local_48;
  char *local_40;
  char *local_38;
  char *local_30;
  
  lVar6 = (longlong)param_2;
  local_d8[0] = "eff_choice_1p_nml_idle";
  local_res8 = 0;
  local_d8[1] = "eff_choice_2p_nml_idle";
  local_res18 = 0;
  local_a8 = "cursor_nml_out_1p_up";
  local_a0 = "cursor_nml_out_1p_dw";
  lVar8 = (lVar6 + 2) * 0x40 + param_1;
  local_98 = "cursor_nml_out_1p_lf";
  local_90 = "cursor_nml_out_1p_ri";
  local_88 = "cursor_nml_out_2p_up";
  local_80 = "cursor_nml_out_2p_dw";
  local_78 = "cursor_nml_out_2p_lf";
  local_70 = "cursor_nml_out_2p_ri";
  local_68[0] = "cursor_nml_in_1p_up";
  local_68[1] = "cursor_nml_in_1p_dw";
  local_68[2] = "cursor_nml_in_1p_lf";
  local_68[3] = "cursor_nml_in_1p_ri";
  local_48 = "cursor_nml_in_2p_up";
  local_40 = "cursor_nml_in_2p_dw";
  local_38 = "cursor_nml_in_2p_lf";
  local_30 = "cursor_nml_in_2p_ri";
  local_d8[2] = "eff_fix_1p_nml";
  local_d8[3] = "eff_fix_2p_nml";
  local_b8 = "eff_choice_1p_nml_crnt";
  local_b0 = "eff_choice_2p_nml_crnt";
  local_f8 = 0;
  local_f0 = 0;
  local_e8 = 0;
  local_e0 = 0;
  uVar5 = (undefined1)param_2;
  if (*(char *)(param_1 + 0x100) != '\0') {
    local_120 = 0;
    local_118 = 0;
    local_110 = 0;
    local_108 = 0;
    local_100 = 0;
    local_128._0_5_ = CONCAT14(uVar5,5);
    local_128 = (ulonglong)(uint5)local_128;
    if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
      (**(code **)(DAT_180c3b6f0 + 0x1fe10))(*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),6,&local_128);
    }
    if (local_120._2_1_ == '\0') {
      return;
    }
  }
  cVar2 = FUN_1801710b0(PTR_DAT_1803ffbd0,param_2,2);
  if (cVar2 == '\0') {
    return;
  }
  cVar2 = FUN_1801710b0(PTR_DAT_1803ffbd0,param_2,3);
  if (cVar2 == '\0') {
    return;
  }
  plVar9 = *(longlong **)(lVar8 + 8);
  if ((plVar9 != (longlong *)0x0) && (*plVar9 != 0)) {
    local_f8 = plVar9[1];
    local_f0 = (undefined4)plVar9[2];
    local_res8 = *(ulonglong *)*plVar9;
  }
  plVar9 = *(longlong **)(lVar8 + 0x10);
  if ((plVar9 != (longlong *)0x0) && (*plVar9 != 0)) {
    local_e8 = plVar9[1];
    local_e0 = (undefined4)plVar9[2];
    local_res18 = *(undefined8 *)*plVar9;
  }
  lVar3 = FUN_18016b0c0();
  iVar7 = (*(char *)(lVar3 + 0x20) != '\0') + 0x14b;
  switch(*(undefined4 *)(lVar8 + 0x20)) {
  case 1:
    if (*(char *)(param_1 + 0x100) != '\0') {
      return;
    }
    uVar10 = 0x10000;
    pcVar4 = local_d8[lVar6];
    goto LAB_180172f67;
  case 2:
    if (*(char *)(param_1 + 0x100) == '\0') {
      FUN_180172120(PTR_DAT_1803ffbd0,param_2,2,iVar7,local_d8[lVar6 * 4 + 6],&local_e8,0xd,0x20000)
      ;
      pcVar4 = local_68[lVar6 * 4 + 1];
LAB_180172dff:
      FUN_180172120(PTR_DAT_1803ffbd0,param_2,3,iVar7,pcVar4,&local_f8,0xd,0x20000);
    }
    else {
      local_118 = 0;
      local_110 = 0;
      local_108 = 0;
      local_100 = 0;
      local_128 = (local_res8 & 0xff) << 0x28;
      local_128._0_7_ = CONCAT16(local_res8._4_1_,(undefined6)local_128);
      local_128 = CONCAT17((undefined1)local_res18,(int7)local_128);
      local_120 = (ulonglong)local_res18._4_1_;
      local_128._0_5_ = CONCAT14(uVar5,3);
      if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
        (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                  (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),6,&local_128);
      }
      if (param_2 == 0) {
        uVar10 = FUN_180173aa0(param_1,0);
        FUN_180172300(uVar10);
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x100) == '\0') {
      FUN_180172120(PTR_DAT_1803ffbd0,param_2,2,iVar7,local_d8[lVar6 * 4 + 7],&local_e8,0xd,0x20000)
      ;
      pcVar4 = local_68[lVar6 * 4];
      goto LAB_180172dff;
    }
    local_118 = 0;
    local_110 = 0;
    local_108 = 0;
    local_100 = 0;
    local_128 = (local_res8 & 0xff) << 0x28;
    local_128._0_7_ = CONCAT16(local_res8._4_1_,(undefined6)local_128);
    local_128 = CONCAT17((undefined1)local_res18,(int7)local_128);
    local_120 = (ulonglong)local_res18._4_1_;
    local_128._0_5_ = CONCAT14(uVar5,3);
    if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
      (**(code **)(DAT_180c3b6f0 + 0x1fe10))(*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),6,&local_128);
    }
    if (param_2 == 0) {
      uVar10 = FUN_180173aa0(param_1,0);
      FUN_180172300(uVar10);
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x100) == '\0') {
      FUN_180172120(PTR_DAT_1803ffbd0,param_2,2,iVar7,local_d8[lVar6 * 4 + 8],&local_e8,0xd,0x20000)
      ;
      pcVar4 = local_68[lVar6 * 4 + 3];
      goto LAB_180172dff;
    }
    local_118 = 0;
    local_110 = 0;
    local_108 = 0;
    local_100 = 0;
    local_128 = (local_res8 & 0xff) << 0x28;
    local_128._0_7_ = CONCAT16(local_res8._4_1_,(undefined6)local_128);
    local_128 = CONCAT17((undefined1)local_res18,(int7)local_128);
    local_120 = (ulonglong)local_res18._4_1_;
    local_128._0_5_ = CONCAT14(uVar5,3);
    if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
      (**(code **)(DAT_180c3b6f0 + 0x1fe10))(*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),6,&local_128);
    }
    if (param_2 == 0) {
      uVar10 = FUN_180173aa0(param_1,0);
      FUN_180172300(uVar10);
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0x100) == '\0') {
      FUN_180172120(PTR_DAT_1803ffbd0,param_2,2,iVar7,local_d8[lVar6 * 4 + 9],&local_e8,0xd,0x20000)
      ;
      pcVar4 = local_68[lVar6 * 4 + 2];
      goto LAB_180172dff;
    }
    local_118 = 0;
    local_110 = 0;
    local_108 = 0;
    local_100 = 0;
    local_128 = (local_res8 & 0xff) << 0x28;
    local_128._0_7_ = CONCAT16(local_res8._4_1_,(undefined6)local_128);
    local_128 = CONCAT17((undefined1)local_res18,(int7)local_128);
    local_120 = (ulonglong)local_res18._4_1_;
    local_128._0_5_ = CONCAT14(uVar5,3);
    if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
      (**(code **)(DAT_180c3b6f0 + 0x1fe10))(*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),6,&local_128);
    }
    if (param_2 == 0) {
      uVar10 = FUN_180173aa0(param_1,0);
      FUN_180172300(uVar10);
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x100) != '\0') {
      local_120 = 0;
      local_118 = 0;
      local_110 = 0;
      local_108 = 0;
      local_100 = 0;
      local_128._0_7_ = (uint7)CONCAT11(local_res8._4_1_,(undefined1)local_res8) << 0x28;
      uVar1 = (uint7)(int7)local_128 >> 0x28;
      local_128._0_5_ = CONCAT14(uVar5,4);
      local_128 = CONCAT35((uint3)uVar1,(uint5)local_128);
      if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
        (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                  (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),6,&local_128);
      }
      if (param_2 == 0) {
        uVar10 = FUN_180173aa0(param_1,0);
        FUN_180172300(uVar10);
      }
      FUN_180185ab0("sy_select_kettei_B");
      return;
    }
    plVar9 = &local_f8;
    FUN_180172120(PTR_DAT_1803ffbd0,param_2,3,iVar7,local_d8[lVar6 + 2],plVar9,0xd,0x20000);
    FUN_180171e90(PTR_DAT_1803ffbd0,0x16,iVar7,"fix_beta_white_flash",7,
                  (ulonglong)plVar9 & 0xffffffff00000000);
    FUN_180185ab0("sy_select_kettei_B");
    return;
  case 7:
    if (*(char *)(param_1 + 0x100) != '\0') {
      return;
    }
    uVar10 = 0x20000;
    pcVar4 = local_d8[lVar6 + 4];
LAB_180172f67:
    FUN_180172120(PTR_DAT_1803ffbd0,param_2,2,iVar7,pcVar4,&local_f8,0xd,uVar10);
  default:
    goto switchD_1801729c0_default;
  }
  FUN_1801860b0(*(undefined4 *)(lVar8 + 0x2c));
  uVar10 = FUN_180185ab0("sy_cursor_move");
  *(undefined4 *)(lVar8 + 0x2c) = uVar10;
switchD_1801729c0_default:
  return;
}



