// ===================================================
// 8214ACE8  ->  FUN_8214ace8  (entree 8214ace8)
// ===================================================

double FUN_8214ace8(double param_1)

{
  float fStack_20;
  float fStack_1c;
  float fStack_18;
  float fStack_14;
  
  fStack_14 = (float)param_1;
  fStack_20 = DAT_82000a34;
  fStack_1c = DAT_82000a34;
  fStack_18 = DAT_82000a34;
  FUN_82297be0(&fStack_20,9,&fStack_18,0x10);
  return (double)fStack_1c;
}



// ===================================================
// 822DC728  ->  FUN_822dc728  (entree 822dc728)
// ===================================================

void FUN_822dc728(undefined4 *param_1,undefined4 *param_2)

{
  double dVar1;
  
  if ((param_2 != (undefined4 *)0x0) && (param_1 != (undefined4 *)0x0)) {
    *param_1 = *param_2;
    dVar1 = (double)FUN_8214ace8((double)(float)param_2[1]);
    param_1[1] = (float)dVar1;
    param_1[2] = param_2[2];
  }
  return;
}



// ===================================================
// 82166598  ->  FUN_82166598  (entree 82166598)
// ===================================================

void FUN_82166598(undefined8 param_1)

{
  FUN_8215cf20(0xffffffff826f8fa4,param_1);
  return;
}



// ===================================================
// 8231FE78  ->  FUN_8231fe78  (entree 8231fe78)
// ===================================================

void FUN_8231fe78(void)

{
  DAT_82657140 = FUN_8231fcb8(0xffffffff8265713c,DAT_8265713c);
  return;
}



// ===================================================
// 82317860  ->  FUN_82317860  (entree 82317860)
// ===================================================

bool FUN_82317860(void)

{
  uint uVar1;
  
  uVar1 = FUN_82316270();
  return (uVar1 & DAT_82656b34) != 0;
}



// ===================================================
// 82315960  ->  FUN_82315960  (entree 82315960)
// ===================================================

ulonglong FUN_82315960(int param_1,int param_2)

{
  ulonglong uVar1;
  uint uVar2;
  int iVar3;
  
  uVar1 = 0;
  do {
    uVar2 = (uint)uVar1;
    if ((int)uVar2 < 0) {
      if (6 < (int)uVar2) goto LAB_82315988;
LAB_82315994:
      iVar3 = -1;
    }
    else if ((int)uVar2 < 7) {
      iVar3 = 0;
    }
    else {
LAB_82315988:
      iVar3 = 1;
      if (0xe < (int)uVar2) goto LAB_82315994;
    }
    if ((iVar3 == param_2) && ((1 << (uVar2 & 0x3f) & *(uint *)(param_1 + 0x2c)) != 0)) {
      return uVar1;
    }
    uVar1 = uVar1 + 1;
    if (0xe < (uVar1 & 0xffffffff)) {
      return 0xffffffffffffffff;
    }
  } while( true );
}



