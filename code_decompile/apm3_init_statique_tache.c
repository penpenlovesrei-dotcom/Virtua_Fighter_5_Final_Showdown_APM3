// ===================================================
// 180004CAF  ->  FUN_180004ca0  (entree 180004ca0)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_180004ca0(void)

{
  undefined8 *puVar1;
  undefined8 *puVar2;
  longlong lVar3;
  
  FUN_180244c80(&DAT_180752000);
  _DAT_180752000 = TaskCsSystemSaveData::vftable;
  _DAT_180752058 = 0xc;
  _DAT_180752060 = 0;
  _DAT_180752068 = 0;
  _DAT_180752070 = 0;
  _DAT_180752078 = 0;
  FUN_180014870(&DAT_180752080);
  _DAT_180752090 = (undefined1  [16])0x0;
  lVar3 = 2;
  puVar1 = &DAT_1807520a0;
  do {
    puVar2 = puVar1;
    *puVar2 = 0;
    puVar2[1] = 0;
    puVar2[2] = 0;
    puVar2[3] = 0;
    puVar2[4] = 0;
    puVar2[5] = 0;
    puVar2[6] = 0;
    puVar2[7] = 0;
    lVar3 = lVar3 + -1;
    puVar1 = puVar2 + 8;
  } while (lVar3 != 0);
  puVar2[8] = 0;
  puVar2[9] = 0;
  puVar2[10] = 0;
  puVar2[0xb] = 0;
  DAT_180752140 = 0;
  atexit((_func_5014 *)&LAB_180344af0);
  return;
}



