// ===================================================
// 1801B8BB0  ->  FUN_1801b8bb0  (entree 1801b8bb0)
// ===================================================

undefined1 FUN_1801b8bb0(longlong param_1)

{
  longlong lVar1;
  
  *(undefined2 *)(param_1 + 0x78) = 0;
  FUN_180014990(param_1 + 0x80);
  *(undefined8 *)(param_1 + 0x90) = 0;
  lVar1 = FUN_180218930(0x16c0);
  if (lVar1 == 0) {
    lVar1 = 0;
  }
  else {
    FUN_1802ff420(lVar1,0,0x16c0);
  }
  *(longlong *)(param_1 + 0x98) = lVar1;
  if (lVar1 == 0) {
    *(undefined4 *)(param_1 + 0x58) = 0xb;
    return 1;
  }
  FUN_1801b92d0(lVar1);
  return 1;
}



// ===================================================
// 1801B7FD0  ->  FUN_1801b7fd0  (entree 1801b7fd0)
// ===================================================

undefined8 FUN_1801b7fd0(longlong param_1)

{
  byte bVar1;
  short sVar2;
  longlong lVar3;
  ulonglong uVar4;
  char cVar5;
  int iVar6;
  uint uVar7;
  longlong *plVar8;
  undefined8 uVar9;
  undefined4 uVar10;
  longlong lVar11;
  ulonglong *puVar12;
  bool bVar13;
  char local_res8 [8];
  char local_res10;
  undefined8 in_stack_ffffffffffffffc0;
  
  uVar10 = (undefined4)((ulonglong)in_stack_ffffffffffffffc0 >> 0x20);
  uVar9 = 0;
  switch(*(undefined4 *)(param_1 + 0x58)) {
  case 0:
    cVar5 = FUN_180029fb0(0);
    if (cVar5 == '\0') {
      return 0;
    }
    uVar9 = FUN_1801bb730();
    _guard_check_icall(uVar9);
    cVar5 = FUN_180029fb0(0xffffffff);
    *(bool *)(param_1 + 0x140) = cVar5 == '\0';
    if ((cVar5 == '\0') && (*(longlong *)(param_1 + 0x98) != 0)) {
      FUN_1801b92d0();
      FUN_180029fb0(*(undefined8 *)(param_1 + 0x98),0x16c0,0x21040415,1,0);
      *(undefined4 *)(param_1 + 0x58) = 1;
      return 0;
    }
    goto LAB_1801b80d4;
  case 1:
    local_res8[0] = '\0';
    if (*(longlong *)(param_1 + 0x98) != 0) {
      cVar5 = FUN_180029fb0(local_res8,0);
      if (cVar5 == '\0') {
        return 0;
      }
      if ((local_res8[0] != '\0') && (**(longlong **)(param_1 + 0x98) != 0)) {
        FUN_180300010(*(longlong *)(param_1 + 0x60) + 0x5058,*(longlong **)(param_1 + 0x98),0x16c0);
      }
    }
LAB_1801b80d4:
    *(undefined4 *)(param_1 + 0x58) = 2;
    return 0;
  case 2:
    lVar3 = *(longlong *)(param_1 + 0x60);
    iVar6 = FUN_1801b88a0(lVar3 + 0x5058,0);
    lVar11 = lVar3 + 0x5144 + (longlong)iVar6 * 0xd0;
    if (lVar11 != 0) {
      bVar1 = *(byte *)(lVar11 + 0x18);
      sVar2 = *(short *)(lVar11 + 0x14);
      uVar7 = FUN_1801b6640();
      bVar13 = *(byte *)(lVar3 + 0x64a1) < bVar1;
      if ((*(byte *)(lVar3 + 0x64a1) == bVar1) &&
         (bVar13 = *(uint *)(lVar3 + 0x64a4) < uVar7, *(uint *)(lVar3 + 0x64a4) == uVar7)) {
        if (*(short *)(lVar3 + 0x64a2) == sVar2) goto LAB_1801b818d;
        bVar13 = *(short *)(lVar3 + 0x64a2) < sVar2;
      }
      if (bVar13) {
        *(char *)(lVar3 + 0x64a0) = (char)iVar6;
        *(byte *)(lVar3 + 0x64a1) = bVar1;
        *(short *)(lVar3 + 0x64a2) = sVar2;
        *(uint *)(lVar3 + 0x64a4) = uVar7;
      }
    }
LAB_1801b818d:
    uVar9 = FUN_1801bb730();
    _guard_check_icall(uVar9);
    uVar9 = FUN_1801bb730();
    _guard_check_icall(uVar9);
    FUN_180029fb0(*(longlong *)(param_1 + 0x60) + 0x5058,0x16c0,0x21040415,1,0);
    *(undefined4 *)(param_1 + 0x58) = 3;
    return 0;
  case 3:
    local_res8[0] = '\0';
    cVar5 = FUN_180029fb0(local_res8,0);
    lVar3 = DAT_180752148;
    if (cVar5 != '\0') {
      if ((local_res8[0] == '\0') && (*(longlong *)(DAT_180752148 + 0x68d0) != 0)) {
        FUN_180300010(*(longlong *)(param_1 + 0x60) + 0x5058,*(longlong *)(DAT_180752148 + 0x68d0),
                      0x16c0);
      }
      if (*(longlong *)(lVar3 + 0x68d0) != 0) {
        FUN_1802fdd80();
        *(undefined8 *)(DAT_180752148 + 0x68d0) = 0;
      }
      FUN_180007450(*(undefined4 *)(param_1 + 0x5c),*(undefined8 *)(param_1 + 0x60),0x6718,
                    *(undefined1 *)(param_1 + 0x69),&LAB_1801b7400,CONCAT44(uVar10,0x21040415));
      *(undefined4 *)(param_1 + 0x58) = 4;
      return 0;
    }
    break;
  case 4:
    cVar5 = FUN_180029fb0();
    if (cVar5 != '\0') {
      if (*(char *)(param_1 + 0x140) != '\0') {
        *(undefined8 *)(param_1 + 0xa0) = 0;
        *(undefined8 *)(param_1 + 0xa8) = 0;
        *(undefined8 *)(param_1 + 0xb0) = 0;
        *(undefined8 *)(param_1 + 0xb8) = 0;
        *(undefined8 *)(param_1 + 0xc0) = 0;
        *(undefined8 *)(param_1 + 200) = 0;
        *(undefined8 *)(param_1 + 0xd0) = 0;
        *(undefined8 *)(param_1 + 0xd8) = 0;
        *(undefined8 *)(param_1 + 0xe0) = 0;
        *(undefined8 *)(param_1 + 0xe8) = 0;
        *(undefined8 *)(param_1 + 0xf0) = 0;
        *(undefined8 *)(param_1 + 0xf8) = 0;
        *(undefined8 *)(param_1 + 0x100) = 0;
        *(undefined8 *)(param_1 + 0x108) = 0;
        *(undefined8 *)(param_1 + 0x110) = 0;
        *(undefined8 *)(param_1 + 0x118) = 0;
        *(undefined8 *)(param_1 + 0x120) = 0;
        *(undefined8 *)(param_1 + 0x128) = 0;
        *(undefined8 *)(param_1 + 0x130) = 0;
        *(undefined8 *)(param_1 + 0x138) = 0;
        FUN_180007450((undefined8 *)(param_1 + 0xa0),1,0x14);
      }
      *(undefined4 *)(param_1 + 0x58) = 5;
      return 0;
    }
    break;
  case 5:
    local_res8[0] = '\0';
    cVar5 = FUN_180029fb0(local_res8,0);
    if (cVar5 != '\0') {
      plVar8 = (longlong *)FUN_1800148e0(param_1 + 0x80,local_res8);
      lVar3 = *plVar8;
      if (lVar3 < 0x2dc6c1) {
        uVar9 = 1000000;
        *(undefined4 *)(param_1 + 0x58) = 6;
        if (1000000 < lVar3) {
          uVar9 = 3000000;
        }
        *(undefined8 *)(param_1 + 0x90) = uVar9;
        return 0;
      }
      *(undefined4 *)(param_1 + 0x58) = 6;
      *(undefined8 *)(param_1 + 0x90) = 0;
      return 0;
    }
    break;
  case 6:
    plVar8 = (longlong *)FUN_1800148e0(param_1 + 0x80,local_res8);
    if (*(longlong *)(param_1 + 0x90) <= *plVar8) {
LAB_1801b83ff:
      *(undefined4 *)(param_1 + 0x58) = 0xb;
      return 0;
    }
    break;
  case 7:
    uVar9 = FUN_1801bb730();
    _guard_check_icall(uVar9);
    FUN_180007450(*(undefined4 *)(param_1 + 0x5c),*(undefined8 *)(param_1 + 0x60),0x6718,
                  *(undefined1 *)(param_1 + 0x68),*(undefined1 *)(param_1 + 0x69),&LAB_1801b7400,
                  0x21040415);
    if (*(longlong *)(param_1 + 0x98) != 0) {
      FUN_1801b92d0();
      FUN_180029fb0(*(undefined8 *)(param_1 + 0x98),0x16c0,0x21040415,1,0);
    }
    *(undefined4 *)(param_1 + 0x58) = 8;
    return 0;
  case 8:
    cVar5 = FUN_180029fb0();
    if (cVar5 != '\0') {
      local_res8[0] = '\0';
      if (*(longlong *)(param_1 + 0x98) != 0) {
        cVar5 = FUN_180029fb0(local_res8,0);
        if (cVar5 == '\0') {
          return 0;
        }
        if (local_res8[0] != '\0') {
          uVar4 = **(ulonglong **)(param_1 + 0x98);
          if ((uVar4 != 0) &&
             (puVar12 = (ulonglong *)(*(longlong *)(param_1 + 0x60) + 0x5058), *puVar12 <= uVar4)) {
            FUN_180300010(puVar12,*(ulonglong **)(param_1 + 0x98),0x16c0);
          }
        }
      }
      uVar9 = FUN_1801bb730();
      _guard_check_icall(uVar9);
      uVar9 = FUN_1801bb730();
      _guard_check_icall(uVar9);
      cVar5 = FUN_180007450(param_1 + 0xa0,1,0x14);
      uVar10 = 0xb;
      if (cVar5 != '\0') {
        uVar10 = 9;
      }
      *(undefined4 *)(param_1 + 0x58) = uVar10;
      return 0;
    }
    break;
  case 9:
    local_res8[0] = '\0';
    local_res10 = '\0';
    cVar5 = FUN_180029fb0(local_res8);
    if (cVar5 != '\0') {
      if (local_res8[0] != '\0') {
        if (local_res10 == '\0') {
          *(undefined8 *)(param_1 + 0xa0) = 0;
          *(undefined8 *)(param_1 + 0xa8) = 0;
          *(undefined8 *)(param_1 + 0xb0) = 0;
          *(undefined8 *)(param_1 + 0xb8) = 0;
          *(undefined8 *)(param_1 + 0xc0) = 0;
          *(undefined8 *)(param_1 + 200) = 0;
          *(undefined8 *)(param_1 + 0xd0) = 0;
          *(undefined8 *)(param_1 + 0xd8) = 0;
          *(undefined8 *)(param_1 + 0xe0) = 0;
          *(undefined8 *)(param_1 + 0xe8) = 0;
          *(undefined8 *)(param_1 + 0xf0) = 0;
          *(undefined8 *)(param_1 + 0xf8) = 0;
          *(undefined8 *)(param_1 + 0x100) = 0;
          *(undefined8 *)(param_1 + 0x108) = 0;
          *(undefined8 *)(param_1 + 0x110) = 0;
          *(undefined8 *)(param_1 + 0x118) = 0;
          *(undefined8 *)(param_1 + 0x120) = 0;
          *(undefined8 *)(param_1 + 0x128) = 0;
          *(undefined8 *)(param_1 + 0x130) = 0;
          *(undefined8 *)(param_1 + 0x138) = 0;
          FUN_180007450(param_1 + 0xa0,1,0x14);
          *(undefined4 *)(param_1 + 0x58) = 10;
          return 0;
        }
        uVar9 = FUN_1801bb730();
        _guard_check_icall(uVar9,param_1 + 0xa0);
      }
      goto LAB_1801b83ff;
    }
    break;
  case 10:
    local_res8[0] = '\0';
    cVar5 = FUN_180029fb0(local_res8,0);
    if (cVar5 != '\0') {
      *(undefined4 *)(param_1 + 0x58) = 0xb;
      return 0;
    }
    break;
  default:
    uVar9 = 1;
  }
  return uVar9;
}



// ===================================================
// 1801B8760  ->  FUN_1801b8760  (entree 1801b8760)
// ===================================================

undefined8 FUN_1801b8760(longlong param_1)

{
  if (*(longlong *)(param_1 + 0x98) != 0) {
    FUN_1802fdd80(*(longlong *)(param_1 + 0x98),0x16c0);
    *(undefined8 *)(param_1 + 0x98) = 0;
  }
  if ((*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0) &&
     (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0)) {
    (**(code **)(DAT_180c3b6f0 + 0x1fe10))(*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0x8b,0);
  }
  if (*(code **)(param_1 + 0x70) != (code *)0x0) {
    (**(code **)(param_1 + 0x70))(*(undefined1 *)(param_1 + 0x78),*(undefined1 *)(param_1 + 0x79));
  }
  FUN_1801b6ad0(param_1);
  return 1;
}



