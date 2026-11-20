// ===================================================
// 18016AEC0  ->  FUN_18016aec0  (entree 18016aec0)
// ===================================================

int * FUN_18016aec0(int *param_1,int param_2)

{
  float fVar1;
  float fVar2;
  longlong lVar3;
  
  *param_1 = param_2;
  param_1[1] = 0;
  param_1[2] = 0;
  if (param_2 != 0x11) {
    lVar3 = (longlong)param_2;
    fVar1 = (float)(&DAT_1803feb20)[lVar3 * 7];
    param_1[3] = (int)fVar1;
    fVar2 = (float)(&DAT_1803feb24)[lVar3 * 7];
    param_1[4] = (int)fVar2;
    *(double *)(param_1 + 6) = (double)(int)fVar1 / (double)(int)fVar2;
    *(undefined1 *)(param_1 + 8) = (&DAT_1803feb28)[lVar3 * 0x1c];
    return param_1;
  }
  param_1[3] = DAT_1806490dc;
  param_1[4] = DAT_1806490e0;
  *(undefined8 *)(param_1 + 6) = DAT_1806490e8;
  *(undefined1 *)(param_1 + 8) = DAT_1806490f0;
  return param_1;
}



