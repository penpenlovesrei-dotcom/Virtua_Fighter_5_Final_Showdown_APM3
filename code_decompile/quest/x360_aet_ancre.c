// ===================================================
// 82166778  ->  FUN_82166778  (entree 82166778)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82166778(int param_1,char *param_2)

{
  char cVar1;
  char cVar2;
  uint uVar3;
  uint uVar4;
  undefined8 in_r0;
  undefined8 uVar5;
  char *pcVar6;
  char *pcVar7;
  uint uVar8;
  
  uVar3 = *(uint *)(param_1 + 4);
  uVar4 = *(uint *)(param_1 + 8);
  uVar8 = uVar3;
  if (uVar4 < uVar3) {
    trapWord(0x1f,in_r0,0x16);
  }
  do {
    if (uVar4 < uVar3) {
      trapWord(0x1f,in_r0,0x16);
    }
    if (param_1 == 0) {
      trapWord(0x1f,in_r0,0x16);
    }
    if (uVar8 == uVar4) {
      return 0;
    }
    if (param_1 == 0) {
      trapWord(0x1f,in_r0,0x16);
    }
    if (*(uint *)(param_1 + 8) <= uVar8) {
      trapWord(0x1f,in_r0,0x16);
    }
    pcVar7 = *(char **)(uVar8 + 0x68);
    pcVar6 = param_2;
    do {
      cVar1 = *pcVar7;
      cVar2 = *pcVar6;
      if (cVar1 == '\0') break;
      pcVar7 = pcVar7 + 1;
      pcVar6 = pcVar6 + 1;
    } while (cVar1 == cVar2);
    if (cVar1 == cVar2) {
      uVar5 = FUN_8215a480(0xffffffff826f8fa4);
      if (*(uint *)(param_1 + 8) <= uVar8) {
        trapWord(0x1f,in_r0,0x16);
      }
      FUN_82158778(uVar5,uVar8);
      return uVar5;
    }
    if (*(uint *)(param_1 + 8) <= uVar8) {
      trapWord(0x1f,in_r0,0x16);
    }
    uVar8 = uVar8 + 0x6c;
  } while( true );
}



// ===================================================
// 82166AD0  ->  FUN_82166ad0  (entree 82166ad0)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_82166ad0(double param_1,undefined8 param_2,undefined8 param_3,undefined4 param_4,
                 undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  int iVar1;
  undefined4 uStack_e0;
  undefined4 uStack_dc;
  undefined4 uStack_d8;
  float fStack_d0;
  undefined4 uStack_c8;
  undefined4 uStack_b8;
  
  FUN_82158008(&uStack_e0);
  iVar1 = FUN_8215d970(0xffffffff826f96e0,param_3);
  uStack_e0 = *(undefined4 *)(iVar1 + 0x20);
  fStack_d0 = (float)param_1;
  uStack_dc = param_4;
  uStack_d8 = param_7;
  uStack_c8 = param_5;
  uStack_b8 = param_6;
  FUN_821630e0(0xffffffff826f8fa4,param_2,&uStack_e0);
  FUN_82157f80(&uStack_e0);
  return;
}



