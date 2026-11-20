// ===================================================
// 8239F8FC  ->  FUN_8239f8d8  (entree 8239f8d8)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

undefined8 FUN_8239f8d8(longlong param_1,undefined8 param_2)

{
  undefined8 uVar1;
  uint local_b0 [4];
  undefined4 local_a0;
  uint local_9c;
  uint local_90 [4];
  undefined4 local_80;
  uint local_7c;
  uint local_70 [4];
  undefined4 local_60;
  uint local_5c;
  uint local_50 [4];
  undefined4 local_40;
  uint local_3c;
  
  FUN_8239f850();
  local_60 = 0;
  local_5c = 0xf;
  local_70[0] = local_70[0] & 0xffffff;
  FUN_821a3170(local_70,0xffffffff820db020,0xd);
  FUN_822176c8(local_90);
  uVar1 = FUN_821c35b8(local_50,local_90,local_70);
  uVar1 = FUN_821a32a0(uVar1,param_2,0,0xffffffffffffffff);
  local_9c = 0xf;
  local_a0 = 0;
  local_b0[0] = local_b0[0] & 0xffffff;
  FUN_821a43e0(local_b0,uVar1);
  FUN_821a43e0(param_1 + 0x3c,local_b0);
  if (0xf < local_9c) {
    thunk_FUN_822d3528(local_b0[0]);
  }
  local_9c = 0xf;
  local_a0 = 0;
  local_b0[0] = local_b0[0] & 0xffffff;
  if (0xf < local_3c) {
    thunk_FUN_822d3528(local_50[0]);
  }
  local_3c = 0xf;
  local_40 = 0;
  local_50[0] = local_50[0] & 0xffffff;
  if (0xf < local_7c) {
    thunk_FUN_822d3528(local_90[0]);
  }
  local_7c = 0xf;
  local_80 = 0;
  local_90[0] = local_90[0] & 0xffffff;
  if (0xf < local_5c) {
    thunk_FUN_822d3528(local_70[0]);
  }
  return 0;
}



