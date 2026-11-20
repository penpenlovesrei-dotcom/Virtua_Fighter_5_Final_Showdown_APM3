// ===================================================
// 8230A5B4  ->  FUN_8230a470  (entree 8230a470)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */
/* WARNING: Removing unreachable block (ram,0x8230a550) */
/* WARNING: Removing unreachable block (ram,0x8230a558) */

void FUN_8230a470(undefined8 param_1)

{
  undefined8 uVar1;
  int iVar4;
  undefined8 uVar2;
  ulonglong uVar3;
  ulonglong uVar5;
  uint uVar6;
  uint uVar7;
  undefined *apuStack_50 [4];
  undefined4 auStack_40 [16];
  
  auStack_40[0] = 0x1b82;
  apuStack_50[0] = &DAT_82063c1c;
  apuStack_50[1] = &DAT_82063c18;
  auStack_40[1] = 0x1b86;
  auStack_40[2] = 0x1b83;
  auStack_40[3] = 0x1b87;
  auStack_40[4] = 0x1b84;
  auStack_40[5] = 0x1b88;
  auStack_40[6] = 0x1b85;
  auStack_40[7] = 0x1b89;
  FUN_821dc920();
  uVar1 = FUN_821dc9c0();
  iVar4 = FUN_82235f28(0xffffffff827a99f8,uVar1);
  uVar2 = FUN_821dc920();
  uVar3 = FUN_821dd318(uVar2,uVar1);
  uVar7 = (uint)*(byte *)(iVar4 + 0x1b9);
  uVar6 = (uint)*(byte *)(iVar4 + 0x1b8);
  if (3 < *(byte *)(iVar4 + 0x1b9)) {
    uVar7 = 4;
  }
  if (3 < *(byte *)(iVar4 + 0x1b8)) {
    uVar6 = 4;
  }
  iVar4 = (int)uVar3;
  if (iVar4 < 0) {
    uVar5 = 0;
  }
  else {
    uVar5 = uVar3;
    if (1 < iVar4) {
      uVar5 = 2;
    }
  }
  if (iVar4 < 0) {
    uVar3 = 0;
  }
  else if (1 < iVar4) {
    uVar3 = 2;
  }
  FUN_8230a338(param_1,*(undefined4 *)((int)apuStack_50 + (int)((uVar3 & 0xffffffff) << 2)),
               *(undefined4 *)((int)apuStack_50 + (int)((uVar5 & 0xffffffff) << 2)),
               auStack_40[uVar6 * 2],auStack_40[uVar7 * 2 + 1]);
  return;
}



