// ===================================================
// 180187C50  ->  FUN_180187c50  (entree 180187c50)
// ===================================================

void FUN_180187c50(undefined4 param_1)

{
  longlong lVar1;
  longlong *plVar2;
  
  lVar1 = FUN_18018c420(DAT_180719908,param_1);
  plVar2 = (longlong *)(lVar1 + 0x28);
  if (0xf < *(ulonglong *)(lVar1 + 0x40)) {
    plVar2 = (longlong *)*plVar2;
  }
  lVar1 = FUN_18018c420(DAT_180719908,param_1);
  FUN_18018e5a0(DAT_180719900,*(undefined4 *)(lVar1 + 0x48),plVar2);
  return;
}



// ===================================================
// 18018DFE5  ->  FUN_18018dfb0  (entree 18018dfb0)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18018dfb0(longlong param_1,undefined8 param_2)

{
  ulonglong uVar1;
  char *pcVar2;
  size_t _Size;
  char cVar3;
  int iVar4;
  undefined8 ***pppuVar5;
  void *_Buf1;
  ulonglong uVar6;
  ulonglong *puVar7;
  undefined8 ****ppppuVar8;
  longlong lVar9;
  ulonglong uVar10;
  undefined1 *puVar11;
  char *pcVar12;
  undefined8 ****ppppuVar13;
  undefined8 ***local_d8;
  ulonglong uStack_d0;
  undefined1 local_c8 [16];
  ulonglong local_b8 [2];
  ulonglong local_a8;
  ulonglong uStack_a0;
  undefined1 local_98;
  undefined7 uStack_97;
  ulonglong local_88;
  ulonglong uStack_80;
  char local_78;
  undefined7 uStack_77;
  size_t local_68;
  ulonglong local_60;
  undefined1 local_58;
  undefined7 uStack_57;
  ulonglong local_48;
  ulonglong uStack_40;
  undefined8 local_38;
  
  local_38 = 0xfffffffffffffffe;
  if (*(int *)(param_1 + 0x20) < 1) {
    *(undefined4 *)(param_1 + 0x20) = 1;
    FUN_1800524e0(param_1 + 0xc0);
    local_48 = _DAT_1803478a0;
    uStack_40 = _UNK_1803478a8;
    local_58 = 0;
    FUN_1800524e0(&local_58,"./rom/2d/");
    local_68 = 0;
    uVar10 = 0xf;
    local_60 = 0xf;
    local_78 = '\0';
    FUN_1800524e0(&local_78,&DAT_18034c110);
    local_88 = _DAT_1803478a0;
    uStack_80 = _UNK_1803478a8;
    local_98 = 0;
    FUN_1800524e0(&local_98,".farc");
    FUN_18008bb50(local_b8,&local_58,param_2);
    local_c8 = (undefined1  [16])0x0;
    puVar7 = local_b8;
    if (0xf < uStack_a0) {
      puVar7 = (ulonglong *)CONCAT71(local_b8[0]._1_7_,(undefined1)local_b8[0]);
    }
    if (local_a8 < 0x10) {
      local_d8 = (undefined8 ***)*puVar7;
      uStack_d0 = puVar7[1];
    }
    else {
      uVar10 = local_a8 | 0xf;
      if (0x7fffffffffffffff < uVar10) {
        uVar10 = 0x7fffffffffffffff;
      }
      uVar1 = uVar10 + 1;
      if (uVar1 < 0x1000) {
        local_d8 = (undefined8 ****)0x0;
        if (uVar1 != 0) {
          local_d8 = (undefined8 ***)FUN_180218930(uVar1);
        }
      }
      else {
        uVar6 = uVar10 + 0x28;
        if (uVar10 + 0x28 <= uVar1) {
          uVar6 = 0xffffffffffffffff;
        }
        pppuVar5 = (undefined8 ***)FUN_180218930(uVar6);
        if (pppuVar5 == (undefined8 ***)0x0) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0();
        }
        local_d8 = (undefined8 ***)((longlong)pppuVar5 + 0x27U & 0xffffffffffffffe0);
        local_d8[-1] = pppuVar5;
      }
      FUN_180300010(local_d8,puVar7,local_a8 + 1);
    }
    _Size = local_68;
    ppppuVar8 = (undefined8 ****)0xffffffffffffffff;
    pcVar2 = (char *)CONCAT71(uStack_77,local_78);
    pcVar12 = &local_78;
    if (0xf < local_60) {
      pcVar12 = pcVar2;
    }
    ppppuVar13 = &local_d8;
    if (0xf < uVar10) {
      ppppuVar13 = (undefined8 ****)local_d8;
    }
    local_c8._8_8_ = uVar10;
    if ((local_68 <= local_a8) && (ppppuVar8 = (undefined8 ****)0x0, local_68 != 0)) {
      lVar9 = local_a8 - local_68;
      for (_Buf1 = (void *)FUN_1802ff380(ppppuVar13,(int)*pcVar12,lVar9 + 1); _Buf1 != (void *)0x0;
          _Buf1 = (void *)FUN_1802ff380((longlong)_Buf1 + 1,(int)*pcVar12,
                                        (longlong)ppppuVar13 + ((lVar9 + 1) - ((longlong)_Buf1 + 1))
                                       )) {
        iVar4 = memcmp(_Buf1,pcVar12,_Size);
        if (iVar4 == 0) {
          ppppuVar8 = (undefined8 ****)((longlong)_Buf1 - (longlong)ppppuVar13);
          goto LAB_18018e1c6;
        }
      }
      ppppuVar8 = (undefined8 ****)0xffffffffffffffff;
    }
LAB_18018e1c6:
    puVar11 = &local_98;
    if (0xf < uStack_80) {
      puVar11 = (undefined1 *)CONCAT71(uStack_97,local_98);
    }
    uVar10 = local_88;
    FUN_18018de10(&local_d8,ppppuVar8,_Size,puVar11,local_88);
    ppppuVar8 = &local_d8;
    if (0xf < (ulonglong)local_c8._8_8_) {
      ppppuVar8 = (undefined8 ****)local_d8;
    }
    cVar3 = FUN_180217860(ppppuVar8);
    if (cVar3 == '\0') {
      puVar7 = local_b8;
      if (0xf < uStack_a0) {
        puVar7 = (ulonglong *)CONCAT71(local_b8[0]._1_7_,(undefined1)local_b8[0]);
      }
      FUN_180217e70(param_1 + 0x28,puVar7,1);
      FUN_180218110(param_1 + 0x28,0,FUN_18018ea50,param_1);
    }
    else {
      FUN_18018c290(param_1);
      ppppuVar8 = &local_d8;
      if (0xf < (ulonglong)local_c8._8_8_) {
        ppppuVar8 = (undefined8 ****)local_d8;
      }
      FUN_180217c60(param_1 + 0x28,ppppuVar8,param_2,1,uVar10 & 0xffffffffffffff00,0);
      FUN_180218110(param_1 + 0x28,0,&LAB_18018e820,param_1);
      FUN_180218110(param_1 + 0x28,1,&LAB_18018e820,param_1);
      FUN_180218110(param_1 + 0x28,2,FUN_18018e830,param_1);
      FUN_18005c6a0(param_1 + 0x28,0x20);
    }
    *(undefined1 *)(param_1 + 0xb8) = 0;
    if (0xf < (ulonglong)local_c8._8_8_) {
      if (0xfff < local_c8._8_8_ + 1) {
        if (0x1f < (ulonglong)((longlong)local_d8 + (-8 - (longlong)local_d8[-1]))) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(local_d8[-1],local_c8._8_8_ + 0x28);
        }
      }
      FUN_1802fdd80();
    }
    local_c8._8_8_ = _UNK_1803478a8;
    local_c8._0_8_ = _DAT_1803478a0;
    local_d8 = (undefined8 ***)((ulonglong)local_d8 & 0xffffffffffffff00);
    if (0xf < uStack_a0) {
      if (0xfff < uStack_a0 + 1) {
        lVar9 = *(longlong *)(CONCAT71(local_b8[0]._1_7_,(undefined1)local_b8[0]) + -8);
        if (0x1f < (CONCAT71(local_b8[0]._1_7_,(undefined1)local_b8[0]) - lVar9) - 8U) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(lVar9,uStack_a0 + 0x28);
        }
      }
      FUN_1802fdd80();
    }
    local_a8 = _DAT_1803478a0;
    uStack_a0 = _UNK_1803478a8;
    local_b8[0]._0_1_ = 0;
    uVar10 = _DAT_1803478a0;
    if (0xf < uStack_80) {
      if (0xfff < uStack_80 + 1) {
        lVar9 = *(longlong *)(CONCAT71(uStack_97,local_98) + -8);
        if (0x1f < (CONCAT71(uStack_97,local_98) - lVar9) - 8U) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(lVar9,uStack_80 + 0x28);
        }
      }
      uVar10 = FUN_1802fdd80();
    }
    if (0xf < local_60) {
      pcVar12 = pcVar2;
      if (0xfff < local_60 + 1) {
        pcVar12 = *(char **)(pcVar2 + -8);
        if ((char *)0x1f < pcVar2 + (-8 - (longlong)pcVar12)) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(uVar10,local_60 + 0x28);
        }
      }
      FUN_1802fdd80(pcVar12);
    }
    if (0xf < uStack_40) {
      if (0xfff < uStack_40 + 1) {
        lVar9 = *(longlong *)(CONCAT71(uStack_57,local_58) + -8);
        if (0x1f < (CONCAT71(uStack_57,local_58) - lVar9) - 8U) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(lVar9,uStack_40 + 0x28);
        }
      }
      FUN_1802fdd80();
    }
  }
  else {
    *(int *)(param_1 + 0x20) = *(int *)(param_1 + 0x20) + 1;
  }
  return;
}



