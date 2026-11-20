// ===================================================
// 18016D180  ->  FUN_18016d180  (entree 18016d180)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18016d180(void)

{
  undefined1 *puVar1;
  bool bVar2;
  ulonglong uVar3;
  char cVar4;
  int iVar5;
  size_t sVar6;
  undefined1 *puVar7;
  char *_Buf2;
  undefined8 in_R9;
  undefined8 uVar8;
  undefined8 local_30;
  undefined1 local_28;
  undefined7 uStack_27;
  size_t local_18;
  ulonglong uStack_10;
  
  uVar8 = 0xfffffffffffffffe;
  _Buf2 = "rom/sound/bgm/vf5fs_bgm_sel.adx";
  if ((DAT_180c3b6f0 != 0) &&
     (_Buf2 = "rom/sound/bgm/vfes_bgm_sel.adx", *(longlong *)(DAT_180c3b6f0 + 0x1fe10) == 0)) {
    _Buf2 = "rom/sound/bgm/vf5fs_bgm_sel.adx";
  }
  cVar4 = FUN_1801856a0(0);
  if (cVar4 != '\0') {
    local_18 = _DAT_1803478a0;
    uStack_10 = _UNK_1803478a8;
    local_28 = 0;
    local_30 = 0;
    FUN_180184f20(&local_30,0);
    uVar3 = uStack_10;
    sVar6 = 0xffffffffffffffff;
    do {
      sVar6 = sVar6 + 1;
    } while (_Buf2[sVar6] != '\0');
    puVar1 = (undefined1 *)CONCAT71(uStack_27,local_28);
    puVar7 = &local_28;
    if (0xf < uStack_10) {
      puVar7 = puVar1;
    }
    if ((local_18 == sVar6) && (iVar5 = memcmp(puVar7,_Buf2,local_18), iVar5 == 0)) {
      bVar2 = false;
    }
    else {
      bVar2 = true;
    }
    if (0xf < uVar3) {
      puVar7 = puVar1;
      if ((0xfff < uVar3 + 1) &&
         (puVar7 = *(undefined1 **)(puVar1 + -8),
         (undefined1 *)0x1f < puVar1 + (-8 - (longlong)puVar7))) {
                    /* WARNING: Subroutine does not return */
        FUN_180303af0();
      }
      FUN_1802fdd80(puVar7);
    }
    if (!bVar2) {
      return;
    }
  }
  FUN_180185da0(0,_Buf2,0,in_R9,uVar8);
  return;
}



