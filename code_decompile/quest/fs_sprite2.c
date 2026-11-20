// ===================================================
// 180173700  ->  FUN_180173700  (entree 180173700)
// ===================================================

void FUN_180173700(longlong param_1)

{
  longlong lVar1;
  bool bVar2;
  longlong *plVar3;
  longlong lVar4;
  undefined1 local_f8 [4];
  undefined4 local_f4;
  undefined4 local_ec;
  undefined4 local_dc;
  undefined4 local_d8;
  undefined4 local_d4;
  undefined8 local_c4;
  undefined4 local_bc;
  
  plVar3 = (longlong *)(param_1 + 0x88);
  lVar4 = 2;
  do {
    if ((char)plVar3[6] != '\0') {
      bVar2 = false;
      lVar1 = *plVar3;
      if (((int)plVar3[3] == 1) || ((int)plVar3[3] - 6U < 2)) {
        bVar2 = true;
      }
      if ((lVar1 != 0) && (bVar2)) {
        FUN_180189880(local_f8);
        local_c4 = *(undefined8 *)(lVar1 + 8);
        local_bc = *(undefined4 *)(lVar1 + 0x10);
        local_f4 = 0xd4b6;
        local_d8 = 9;
        local_d4 = 9;
        local_dc = 0xd;
        local_ec = 0x400000;
        FUN_180187c00();
      }
    }
    plVar3 = plVar3 + 8;
    lVar4 = lVar4 + -1;
  } while (lVar4 != 0);
  return;
}



