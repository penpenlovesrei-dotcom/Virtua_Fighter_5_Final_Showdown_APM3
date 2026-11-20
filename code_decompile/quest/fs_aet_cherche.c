// ===================================================
// 180172020  ->  FUN_180172020  (entree 180172020)
// ===================================================

void FUN_180172020(longlong param_1,int param_2,int param_3,undefined4 param_4,undefined8 param_5,
                  undefined8 *param_6,undefined4 param_7,undefined4 param_8,undefined8 param_9,
                  undefined8 param_10)

{
  undefined4 uVar1;
  undefined4 local_128 [2];
  undefined8 local_120;
  undefined8 local_118;
  undefined8 local_110;
  undefined4 local_100;
  undefined4 local_f4;
  undefined8 local_e8;
  undefined4 local_e0;
  
  FUN_180029000(local_128);
  local_120 = param_5;
  local_f4 = param_7;
  local_100 = param_8;
  local_118 = param_9;
  local_110 = param_10;
  if (param_6 != (undefined8 *)0x0) {
    local_e8 = *param_6;
    local_e0 = *(undefined4 *)(param_6 + 1);
  }
  local_128[0] = param_4;
  if (*(char *)(param_1 + 0x138) == '\0') {
    param_1 = param_1 + ((longlong)param_2 * 0xb + (longlong)param_3) * 4;
    if (*(int *)(param_1 + 0xc0) != 0) {
      FUN_180029be0();
      *(undefined4 *)(param_1 + 0xc0) = 0;
    }
    uVar1 = FUN_180029a90(local_128);
    *(undefined4 *)(param_1 + 0xc0) = uVar1;
  }
  FUN_180029140(local_128);
  return;
}



// ===================================================
// 1801722A0  ->  FUN_1801722a0  (entree 1801722a0)
// ===================================================

undefined1 FUN_1801722a0(byte param_1)

{
  undefined4 local_38;
  uint uStack_34;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 local_20;
  undefined8 local_18;
  undefined8 local_10;
  
  local_30 = 0;
  local_28 = 0;
  local_20 = 0;
  local_18 = 0;
  local_10 = 0;
  _local_38 = CONCAT44((uint)param_1,5);
  if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
    (**(code **)(DAT_180c3b6f0 + 0x1fe10))(*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),6,&local_38);
  }
  return local_30._2_1_;
}



// ===================================================
// 1801724B0  ->  FUN_1801724b0  (entree 1801724b0)
// ===================================================

undefined1 FUN_1801724b0(undefined8 param_1)

{
  FUN_180173110(param_1,0);
  FUN_180173110(param_1,1);
  FUN_1801724e0(param_1);
  return 0;
}



// ===================================================
// 180172120  ->  FUN_180172120  (entree 180172120)
// ===================================================

void FUN_180172120(void)

{
  FUN_180172020();
  return;
}



