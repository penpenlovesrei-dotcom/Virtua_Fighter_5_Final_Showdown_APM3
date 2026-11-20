// ===================================================
// 8230DC78  ->  FUN_8230dc78  (entree 8230dc78)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

void FUN_8230dc78(void)

{
  char cVar1;
  int *piVar2;
  char *pcVar5;
  undefined8 uVar3;
  int *piVar6;
  undefined8 uVar4;
  undefined4 *****pppppuVar7;
  char *pcVar8;
  int iVar9;
  undefined1 auStack_b0 [4];
  undefined4 ****appppuStack_ac [4];
  undefined4 uStack_9c;
  uint uStack_98;
  undefined1 auStack_90 [144];
  
  if (DAT_82acb928 == (int *)0x0) {
    FUN_821ccac8(auStack_90);
    uStack_9c = 0;
    uStack_98 = 0xf;
    appppuStack_ac[0] = (undefined4 ****)((uint)appppuStack_ac[0] & 0xffffff);
    pcVar5 = (char *)FUN_82144aa8();
    pcVar8 = pcVar5;
    do {
      cVar1 = *pcVar8;
      pcVar8 = pcVar8 + 1;
    } while (cVar1 != '\0');
    FUN_82141840(auStack_b0,pcVar5,pcVar8 + (-1 - (int)pcVar5));
    FUN_8214c930(auStack_b0,0xffffffff8208e274,0xb);
    pppppuVar7 = (undefined4 *****)appppuStack_ac[0];
    if (uStack_98 < 0x10) {
      pppppuVar7 = appppuStack_ac;
    }
    FUN_821cf6e8(auStack_90,pppppuVar7,0xf);
    FUN_821cf700(auStack_90);
    uVar3 = FUN_821ccb88(auStack_90);
    piVar6 = (int *)FUN_8220cf50(0xe,uVar3,0xffffffff8208e26c);
    DAT_82acb928 = piVar6;
    uVar3 = FUN_821ccb88(auStack_90);
    uVar4 = FUN_821ccb68(auStack_90);
    FUN_825ffd30(piVar6,uVar4,uVar3);
    FUN_821ce558(auStack_90,1);
    piVar2 = DAT_82acb928;
    iVar9 = 1000;
    do {
      iVar9 = iVar9 + -1;
      *piVar6 = *piVar6 + (int)piVar2;
      piVar6[1] = piVar6[1] + (int)piVar2;
      piVar6[2] = piVar6[2] + (int)piVar2;
      piVar6 = piVar6 + 0x24;
    } while (iVar9 != 0);
    FUN_8230d7d8(0xffffffff82acb930);
    if (0xf < uStack_98) {
      thunk_FUN_82142f48(appppuStack_ac[0]);
    }
    uStack_98 = 0xf;
    uStack_9c = 0;
    appppuStack_ac[0] = (undefined4 ****)((uint)appppuStack_ac[0] & 0xffffff);
    FUN_821ce520(auStack_90);
  }
  return;
}



