// ===================================================
// 8232295C  ->  FUN_82322900  (entree 82322900)
// ===================================================

void FUN_82322900(void)

{
  char cVar1;
  char *pcVar2;
  undefined4 *****pppppuVar3;
  char *pcVar4;
  undefined1 auStack_30 [4];
  undefined4 ****appppuStack_2c [4];
  undefined4 uStack_1c;
  uint uStack_18;
  
  uStack_18 = 0xf;
  uStack_1c = 0;
  appppuStack_2c[0] = (undefined4 ****)(uint)appppuStack_2c[0]._1_3_;
  pcVar2 = (char *)FUN_82144aa8();
  pcVar4 = pcVar2;
  do {
    cVar1 = *pcVar4;
    pcVar4 = pcVar4 + 1;
  } while (cVar1 != '\0');
  FUN_82141840(auStack_30,pcVar2,pcVar4 + (-1 - (int)pcVar2));
  FUN_8214c930(auStack_30,0xffffffff820b1588,0x10);
  pppppuVar3 = (undefined4 *****)appppuStack_2c[0];
  if (uStack_18 < 0x10) {
    pppppuVar3 = appppuStack_2c;
  }
  FUN_821cf6e8(0xffffffff82ad1c48,pppppuVar3,0xf);
  if (0xf < uStack_18) {
    thunk_FUN_82142f48(appppuStack_2c[0]);
  }
  return;
}



