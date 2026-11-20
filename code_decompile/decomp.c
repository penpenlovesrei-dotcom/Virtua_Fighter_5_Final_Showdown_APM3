// ===================================================
// 18019A740  ->  FUN_18019a740  (entree 18019a740)
// ===================================================

void FUN_18019a740(undefined4 *param_1,undefined4 param_2,undefined1 param_3,undefined1 param_4,
                  undefined1 param_5,undefined1 param_6,byte param_7,byte param_8,undefined4 param_9
                  )

{
  undefined4 *puVar1;
  uint uVar2;
  undefined4 local_res8;
  short local_resc;
  
  *(undefined1 *)((longlong)param_1 + 6) = param_5;
  *(undefined1 *)((longlong)param_1 + 7) = param_6;
  param_1[3] = param_9;
  *(byte *)(param_1 + 2) = param_7;
  *param_1 = param_2;
  *(undefined1 *)(param_1 + 1) = param_3;
  *(undefined1 *)((longlong)param_1 + 5) = param_4;
  *(byte *)((longlong)param_1 + 9) = param_8;
  param_1[5] = 0x100;
  param_1[6] = 0x10;
  param_1[4] = (float)param_7 / (float)param_8;
  if ((ulonglong)((*(longlong *)(param_1 + 0xc) - *(longlong *)(param_1 + 8)) / 6) < 0x100) {
    FUN_180199e50(param_1 + 8);
  }
  uVar2 = 0;
  do {
    puVar1 = *(undefined4 **)(param_1 + 10);
    local_res8 = CONCAT13((char)(uVar2 / (uint)param_1[6]),
                          CONCAT12((char)(uVar2 % (uint)param_1[6]),
                                   CONCAT11(*(char *)((longlong)param_1 + 9) != '\x01',1)));
    local_resc = (ushort)*(byte *)(param_1 + 1) << 8;
    if (*(undefined4 **)(param_1 + 0xc) == puVar1) {
      FUN_180199940(param_1 + 8,puVar1,&local_res8);
    }
    else {
      *puVar1 = local_res8;
      *(short *)(puVar1 + 1) = local_resc;
      *(longlong *)(param_1 + 10) = *(longlong *)(param_1 + 10) + 6;
    }
    uVar2 = uVar2 + 1;
  } while (uVar2 < 0x100);
  return;
}



