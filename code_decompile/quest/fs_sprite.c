// ===================================================
// 180187B10  ->  FUN_180187b10  (entree 180187b10)
// ===================================================

void FUN_180187b10(undefined8 param_1,undefined8 param_2,float param_3,float param_4,
                  undefined4 param_5,undefined4 param_6,undefined4 param_7,undefined4 param_8)

{
  undefined1 auVar1 [16];
  undefined1 auVar2 [16];
  undefined1 in_ZMM0 [64];
  undefined1 in_ZMM1 [64];
  undefined1 auVar3 [64];
  undefined1 auVar4 [64];
  undefined4 local_138 [2];
  undefined4 local_130;
  uint local_12c;
  undefined4 local_120;
  undefined4 local_11c;
  undefined4 local_118;
  undefined4 local_114;
  undefined8 local_104;
  undefined4 local_fc;
  
  auVar4 = ZEXT1664(in_ZMM1._0_16_);
  auVar3 = ZEXT1664(in_ZMM0._0_16_);
  FUN_180189880(local_138);
  local_fc = 0;
  local_120 = param_8;
  local_118 = param_5;
  local_114 = param_5;
  auVar1 = vunpcklps_avx(ZEXT416((uint)(param_3 - auVar3._0_4_)),
                         ZEXT416((uint)(param_4 - auVar4._0_4_)));
  local_11c = param_6;
  auVar2 = vunpcklps_avx(auVar3._0_16_,auVar4._0_16_);
  local_130 = param_7;
  local_138[0] = 2;
  local_104 = auVar2._0_8_;
  FUN_18018e7c0(local_138,auVar1._0_8_);
  local_12c = local_12c | 0x8000000;
  FUN_18018ca20(DAT_180719900,local_138);
  return;
}



// ===================================================
// 1801065A0  ->  FUN_1801065a0  (entree 1801065a0)
// ===================================================

void FUN_1801065a0(undefined4 *param_1,undefined4 *param_2)

{
  undefined4 uVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined4 local_res8;
  undefined4 local_resc;
  undefined4 local_res10;
  undefined4 local_res14;
  undefined4 local_88;
  undefined4 local_84;
  undefined4 local_80;
  undefined4 local_78;
  undefined4 local_74;
  undefined4 local_70;
  
  uVar2 = *param_1;
  uVar3 = param_1[1];
  uVar4 = param_1[2];
  uVar5 = *param_2;
  uVar6 = param_2[1];
  uVar7 = param_2[2];
  uVar1 = FUN_180007880(&DAT_180644a88);
  local_res10 = 0;
  local_res14 = 0;
  local_res8 = 0;
  local_resc = 0;
  local_88 = uVar2;
  local_84 = uVar3;
  local_80 = uVar4;
  local_78 = uVar5;
  local_74 = uVar6;
  local_70 = uVar7;
  FUN_18006ccc0(&local_res10,&local_88,1);
  FUN_18006ccc0(&local_res8,&local_78,1);
  FUN_180187b10(local_res10,local_res14,local_res8,local_resc,0x11,0x1d,uVar1,0);
  return;
}



