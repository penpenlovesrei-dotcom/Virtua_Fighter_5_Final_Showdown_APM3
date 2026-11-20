// ===================================================
// 180020DA2  ->  FUN_180020cc0  (entree 180020cc0)
// ===================================================

undefined8 *
FUN_180020cc0(undefined8 *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined8 *puVar1;
  longlong lVar2;
  longlong lVar3;
  undefined8 *puVar4;
  undefined8 uVar5;
  
  uVar5 = 0xfffffffffffffffe;
  *param_1 = AetObj::vftable;
  *(undefined8 *)((longlong)param_1 + 0x44) = 0;
  *(undefined8 *)((longlong)param_1 + 0x4c) = 0;
  *(undefined8 *)((longlong)param_1 + 0x54) = 0;
  *(undefined8 *)((longlong)param_1 + 0x5c) = 0;
  *(undefined8 *)((longlong)param_1 + 100) = 0;
  *(undefined8 *)((longlong)param_1 + 0x6c) = 0;
  param_1[0xf] = 0;
  param_1[0x10] = 0;
  *(undefined8 *)((longlong)param_1 + 0x94) = 0;
  FUN_180189880(param_1 + 0x14);
  puVar1 = param_1 + 0x32;
  *puVar1 = 0;
  param_1[0x33] = 0;
  param_1[0x34] = 0;
  puVar4 = param_1 + 0x36;
  param_1[0x38] = 0;
  param_1[0x39] = 0xf;
  *(undefined1 *)puVar4 = 0;
  param_1[0x3a] = 0;
  param_1[0x3b] = 0;
  param_1[0x3c] = 0;
  param_1[0x3f] = 0;
  param_1[0x40] = 0;
  param_1[0x41] = 0;
  *(undefined4 *)(param_1 + 1) = 0xffffffff;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  *(undefined4 *)(param_1 + 6) = 0;
  *(undefined4 *)((longlong)param_1 + 0x34) = 0xffffffff;
  *(undefined4 *)(param_1 + 7) = 0;
  *(undefined4 *)((longlong)param_1 + 0x3c) = 3;
  param_1[8] = 9;
  param_1[9] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[0xc] = 0;
  param_1[0xd] = 0;
  param_1[0xe] = 0;
  param_1[0xf] = 0;
  param_1[0x10] = 0;
  *(undefined4 *)(param_1 + 0x11) = 0;
  *(undefined4 *)((longlong)param_1 + 0x8c) = 9;
  *(undefined8 *)((longlong)param_1 + 0x94) = 0;
  *(undefined1 *)((longlong)param_1 + 0x9c) = 0;
  FUN_18018c6b0(param_1 + 0x14);
  *(undefined4 *)(param_1 + 0x31) = 0;
  FUN_18001a9d0(*puVar1,param_1[0x33],puVar1,param_4,uVar5);
  param_1[0x33] = *puVar1;
  param_1[0x38] = 0;
  if (0xf < (ulonglong)param_1[0x39]) {
    puVar4 = (undefined8 *)*puVar4;
  }
  *(undefined1 *)puVar4 = 0;
  lVar2 = param_1[0x3b];
  lVar3 = param_1[0x3a];
  if (lVar3 != lVar2) {
    do {
      FUN_18000df90(lVar3);
      lVar3 = lVar3 + 0x40;
    } while (lVar3 != lVar2);
    lVar3 = param_1[0x3a];
  }
  param_1[0x3b] = lVar3;
  *(undefined4 *)(param_1 + 0x3e) = 2;
  param_1[0x40] = param_1[0x3f];
  *(undefined1 *)(param_1 + 0x43) = 0;
  *(undefined1 *)(param_1 + 0x12) = 0;
  return param_1;
}



// ===================================================
// 1801EB365  ->  FUN_1801eaee0  (entree 1801eaee0)
// ===================================================

void FUN_1801eaee0(longlong param_1)

{
  byte bVar1;
  uint *puVar2;
  float fVar3;
  
  puVar2 = (uint *)FUN_18013a370(*(undefined8 *)(param_1 + 0x10));
  switch(*(undefined4 *)(param_1 + 0x20)) {
  case 0:
  case 1:
  case 0xb:
  case 0xc:
  case 0x11:
  case 0x12:
    if ((*(byte *)(param_1 + 0x35) & 0x20) != 0) {
      if (*(int *)(param_1 + 0x40) != 0) {
        *(byte *)(param_1 + 0x35) = *(byte *)(param_1 + 0x35) | 0x20;
        *(undefined8 *)(param_1 + 0x40) = 0;
        *(undefined8 *)(param_1 + 0x48) = 0;
        *(undefined8 *)(param_1 + 0x50) = 0xffffffffffffffff;
        if (*(int *)(param_1 + 0x5c) != 0) {
          FUN_180029c80(*(int *)(param_1 + 0x5c),0);
          FUN_180029be0(*(undefined4 *)(param_1 + 0x5c));
          *(undefined4 *)(param_1 + 0x58) = 0xffffffff;
          *(undefined8 *)(param_1 + 0x5c) = 0;
          *(undefined8 *)(param_1 + 100) = 0;
        }
      }
      *(undefined4 *)(param_1 + 0x40) = 0;
      return;
    }
    break;
  case 2:
    bVar1 = *(byte *)(param_1 + 0x35);
    if ((bVar1 & 0x20) != 0) {
      if (*(int *)(param_1 + 0x40) != 2) {
        bVar1 = bVar1 | 0x20;
        *(undefined8 *)(param_1 + 0x40) = 0;
        *(byte *)(param_1 + 0x35) = bVar1;
        *(undefined8 *)(param_1 + 0x48) = 0;
        *(undefined8 *)(param_1 + 0x50) = 0xffffffffffffffff;
        if (*(int *)(param_1 + 0x5c) != 0) {
          FUN_180029c80(*(int *)(param_1 + 0x5c),0);
          FUN_180029be0(*(undefined4 *)(param_1 + 0x5c));
          *(undefined4 *)(param_1 + 0x58) = 0xffffffff;
          *(undefined8 *)(param_1 + 0x5c) = 0;
          *(undefined8 *)(param_1 + 100) = 0;
          bVar1 = *(byte *)(param_1 + 0x35);
        }
      }
      *(byte *)(param_1 + 0x35) = bVar1 & 0xdf;
      *(undefined4 *)(param_1 + 0x40) = 2;
      return;
    }
    break;
  case 3:
    bVar1 = *(byte *)(param_1 + 0x35);
    if ((bVar1 & 0x20) != 0) {
      if (*(int *)(param_1 + 0x40) != 3) {
        bVar1 = bVar1 | 0x20;
        *(undefined8 *)(param_1 + 0x40) = 0;
        *(byte *)(param_1 + 0x35) = bVar1;
        *(undefined8 *)(param_1 + 0x48) = 0;
        *(undefined8 *)(param_1 + 0x50) = 0xffffffffffffffff;
        if (*(int *)(param_1 + 0x5c) != 0) {
          FUN_180029c80(*(int *)(param_1 + 0x5c),0);
          FUN_180029be0(*(undefined4 *)(param_1 + 0x5c));
          *(undefined4 *)(param_1 + 0x58) = 0xffffffff;
          *(undefined8 *)(param_1 + 0x5c) = 0;
          *(undefined8 *)(param_1 + 100) = 0;
          bVar1 = *(byte *)(param_1 + 0x35);
        }
      }
      *(byte *)(param_1 + 0x35) = bVar1 & 0xdf;
      *(undefined4 *)(param_1 + 0x40) = 3;
      return;
    }
    break;
  case 4:
    if ((-1 < *(char *)(param_1 + 0x35)) &&
       ((((byte)(*puVar2 >> 0xb) | (byte)(*puVar2 >> 10)) & 1) == 0)) {
      FUN_1801ea490(param_1,DAT_18034a51c);
      bVar1 = *(byte *)(param_1 + 0x35);
      if ((bVar1 & 0x20) != 0) {
        if (*(int *)(param_1 + 0x40) != 4) {
          bVar1 = bVar1 | 0x20;
          *(undefined8 *)(param_1 + 0x40) = 0;
          *(byte *)(param_1 + 0x35) = bVar1;
          *(undefined8 *)(param_1 + 0x48) = 0;
          *(undefined8 *)(param_1 + 0x50) = 0xffffffffffffffff;
          if (*(int *)(param_1 + 0x5c) != 0) {
            FUN_180029c80(*(int *)(param_1 + 0x5c),0);
            FUN_180029be0(*(undefined4 *)(param_1 + 0x5c));
            *(undefined4 *)(param_1 + 0x58) = 0xffffffff;
            *(undefined8 *)(param_1 + 0x5c) = 0;
            *(undefined8 *)(param_1 + 100) = 0;
            bVar1 = *(byte *)(param_1 + 0x35);
          }
        }
        *(byte *)(param_1 + 0x35) = bVar1 & 0xdf;
        *(undefined4 *)(param_1 + 0x40) = 4;
        return;
      }
    }
    break;
  case 5:
    if ((-1 < *(char *)(param_1 + 0x35)) &&
       ((((byte)(*puVar2 >> 0xb) | (byte)(*puVar2 >> 10)) & 1) == 0)) {
      FUN_1801ea490(param_1,DAT_180350f00);
      bVar1 = *(byte *)(param_1 + 0x35);
      if ((bVar1 & 0x20) != 0) {
        if (*(int *)(param_1 + 0x40) != 5) {
          bVar1 = bVar1 | 0x20;
          *(undefined8 *)(param_1 + 0x40) = 0;
          *(byte *)(param_1 + 0x35) = bVar1;
          *(undefined8 *)(param_1 + 0x48) = 0;
          *(undefined8 *)(param_1 + 0x50) = 0xffffffffffffffff;
          if (*(int *)(param_1 + 0x5c) != 0) {
            FUN_180029c80(*(int *)(param_1 + 0x5c),0);
            FUN_180029be0(*(undefined4 *)(param_1 + 0x5c));
            *(undefined4 *)(param_1 + 0x58) = 0xffffffff;
            *(undefined8 *)(param_1 + 0x5c) = 0;
            *(undefined8 *)(param_1 + 100) = 0;
            bVar1 = *(byte *)(param_1 + 0x35);
          }
        }
        *(byte *)(param_1 + 0x35) = bVar1 & 0xdf;
        *(undefined4 *)(param_1 + 0x40) = 5;
        return;
      }
    }
    break;
  case 6:
    bVar1 = *(byte *)(param_1 + 0x35);
    if ((bVar1 & 0x20) != 0) {
      if (*(int *)(param_1 + 0x40) != 6) {
        bVar1 = bVar1 | 0x20;
        *(undefined8 *)(param_1 + 0x40) = 0;
        *(byte *)(param_1 + 0x35) = bVar1;
        *(undefined8 *)(param_1 + 0x48) = 0;
        *(undefined8 *)(param_1 + 0x50) = 0xffffffffffffffff;
        if (*(int *)(param_1 + 0x5c) != 0) {
          FUN_180029c80(*(int *)(param_1 + 0x5c),0);
          FUN_180029be0(*(undefined4 *)(param_1 + 0x5c));
          *(undefined4 *)(param_1 + 0x58) = 0xffffffff;
          *(undefined8 *)(param_1 + 0x5c) = 0;
          *(undefined8 *)(param_1 + 100) = 0;
          bVar1 = *(byte *)(param_1 + 0x35);
        }
      }
      *(byte *)(param_1 + 0x35) = bVar1 & 0xdf;
      *(undefined4 *)(param_1 + 0x40) = 6;
      return;
    }
    break;
  case 7:
    bVar1 = *(byte *)(param_1 + 0x35);
    if ((bVar1 & 0x20) != 0) {
      if (*(int *)(param_1 + 0x40) != 7) {
        bVar1 = bVar1 | 0x20;
        *(undefined8 *)(param_1 + 0x40) = 0;
        *(byte *)(param_1 + 0x35) = bVar1;
        *(undefined8 *)(param_1 + 0x48) = 0;
        *(undefined8 *)(param_1 + 0x50) = 0xffffffffffffffff;
        if (*(int *)(param_1 + 0x5c) != 0) {
          FUN_180029c80(*(int *)(param_1 + 0x5c),0);
          FUN_180029be0(*(undefined4 *)(param_1 + 0x5c));
          *(undefined4 *)(param_1 + 0x58) = 0xffffffff;
          *(undefined8 *)(param_1 + 0x5c) = 0;
          *(undefined8 *)(param_1 + 100) = 0;
          bVar1 = *(byte *)(param_1 + 0x35);
        }
      }
      *(byte *)(param_1 + 0x35) = bVar1 & 0xdf;
      *(undefined4 *)(param_1 + 0x40) = 7;
      return;
    }
    break;
  case 8:
    bVar1 = *(byte *)(param_1 + 0x35);
    if ((bVar1 & 0x20) != 0) {
      if (*(int *)(param_1 + 0x40) != 8) {
        bVar1 = bVar1 | 0x20;
        *(undefined8 *)(param_1 + 0x40) = 0;
        *(byte *)(param_1 + 0x35) = bVar1;
        *(undefined8 *)(param_1 + 0x48) = 0;
        *(undefined8 *)(param_1 + 0x50) = 0xffffffffffffffff;
        if (*(int *)(param_1 + 0x5c) != 0) {
          FUN_180029c80(*(int *)(param_1 + 0x5c),0);
          FUN_180029be0(*(undefined4 *)(param_1 + 0x5c));
          *(undefined4 *)(param_1 + 0x58) = 0xffffffff;
          *(undefined8 *)(param_1 + 0x5c) = 0;
          *(undefined8 *)(param_1 + 100) = 0;
          bVar1 = *(byte *)(param_1 + 0x35);
        }
      }
      *(byte *)(param_1 + 0x35) = bVar1 & 0xdf;
      *(undefined4 *)(param_1 + 0x40) = 8;
      return;
    }
    break;
  case 9:
    FUN_1801ea920(param_1);
    FUN_1801ebfa0(param_1);
    return;
  case 10:
    FUN_1801ea920(param_1);
    return;
  case 0xe:
    FUN_1801ed570(param_1);
  case 0xd:
    if ((((*(byte *)(param_1 + 0x36) & 1) == 0) &&
        (fVar3 = (float)FUN_18013a1c0(*(undefined8 *)(param_1 + 0x10)), DAT_180350160 < fVar3)) &&
       (bVar1 = *(byte *)(param_1 + 0x35), (bVar1 & 0x20) != 0)) {
      if (*(int *)(param_1 + 0x40) != 0xd) {
        bVar1 = bVar1 | 0x20;
        *(undefined8 *)(param_1 + 0x40) = 0;
        *(byte *)(param_1 + 0x35) = bVar1;
        *(undefined8 *)(param_1 + 0x48) = 0;
        *(undefined8 *)(param_1 + 0x50) = 0xffffffffffffffff;
        if (*(int *)(param_1 + 0x5c) != 0) {
          FUN_180029c80(*(int *)(param_1 + 0x5c),0);
          FUN_180029be0(*(undefined4 *)(param_1 + 0x5c));
          *(undefined4 *)(param_1 + 0x58) = 0xffffffff;
          *(undefined8 *)(param_1 + 0x5c) = 0;
          *(undefined8 *)(param_1 + 100) = 0;
          bVar1 = *(byte *)(param_1 + 0x35);
        }
      }
      *(byte *)(param_1 + 0x35) = bVar1 & 0xdf;
      *(undefined4 *)(param_1 + 0x40) = 0xd;
      return;
    }
    break;
  case 0xf:
    *(undefined4 *)(param_1 + 0x88) = 4;
    FUN_1801ebb90(param_1);
    return;
  case 0x10:
    if ((-1 < *(char *)(param_1 + 0x35)) &&
       ((((byte)(*puVar2 >> 0xb) | (byte)(*puVar2 >> 10)) & 1) == 0)) {
      FUN_1801ea490(param_1,DAT_18034a51c);
      bVar1 = *(byte *)(param_1 + 0x35);
      if ((bVar1 & 0x20) != 0) {
        if (*(int *)(param_1 + 0x40) != 0x20) {
          bVar1 = bVar1 | 0x20;
          *(undefined8 *)(param_1 + 0x40) = 0;
          *(byte *)(param_1 + 0x35) = bVar1;
          *(undefined8 *)(param_1 + 0x48) = 0;
          *(undefined8 *)(param_1 + 0x50) = 0xffffffffffffffff;
          if (*(int *)(param_1 + 0x5c) != 0) {
            FUN_180029c80(*(int *)(param_1 + 0x5c),0);
            FUN_180029be0(*(undefined4 *)(param_1 + 0x5c));
            *(undefined4 *)(param_1 + 0x58) = 0xffffffff;
            *(undefined8 *)(param_1 + 0x5c) = 0;
            *(undefined8 *)(param_1 + 100) = 0;
            bVar1 = *(byte *)(param_1 + 0x35);
          }
        }
        *(undefined4 *)(param_1 + 0x40) = 0x20;
        *(byte *)(param_1 + 0x35) = bVar1 & 0xdf;
      }
    }
  }
  return;
}



