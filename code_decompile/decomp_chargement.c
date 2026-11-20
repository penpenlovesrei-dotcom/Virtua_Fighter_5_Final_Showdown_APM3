// ===================================================
// 1800f7330  ->  FUN_1800f7330  (entree 1800f7330)
// ===================================================

void FUN_1800f7330(longlong param_1)

{
  if (*(longlong *)(param_1 + 0x148) != 0) {
    FUN_180218400(1);
    *(undefined8 *)(param_1 + 0x148) = 0;
  }
  if (*(longlong *)(param_1 + 0x140) != 0) {
    FUN_180218400(1);
    *(undefined8 *)(param_1 + 0x140) = 0;
  }
  return;
}



// ===================================================
// 1800f7390  ->  FUN_1800f7390  (entree 1800f7390)
// ===================================================

void FUN_1800f7390(longlong param_1,undefined8 *param_2)

{
  longlong lVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  
  if ((*(longlong *)(param_1 + 0x130) != 0) &&
     (*(int *)(*(longlong *)(param_1 + 0x130) + 0x20) != 0)) {
    iVar2 = *(int *)((longlong)param_2 + 4);
    *(int *)(param_1 + 0x178) = iVar2;
    lVar1 = (longlong)iVar2 * 4;
    puVar4 = (undefined8 *)FUN_180218410(1,lVar1 + 0xc,"TMP_TEXDATA_HEADER");
    *(undefined8 **)(param_1 + 0x140) = puVar4;
    uVar3 = param_2[1];
    *puVar4 = *param_2;
    puVar4[1] = uVar3;
    FUN_180218400(1,param_2);
    if (1 < *(int *)(param_1 + 0x178)) {
      FUN_180218110(param_1 + 0x98,2,FUN_1800f74a0,param_1);
      *(longlong *)(param_1 + 0x108) = *(longlong *)(param_1 + 0x140) + 0x10;
      FUN_18005c6a0(param_1 + 0x98,lVar1 + -4);
      return;
    }
    FUN_1800f74a0(param_1,0);
    return;
  }
  FUN_180218110(param_1 + 0x98,2,0);
  return;
}



// ===================================================
// 18005f807  ->  FUN_18005f720  (entree 18005f720)
// ===================================================

ulonglong FUN_18005f720(void)

{
  longlong lVar1;
  ulonglong in_RAX;
  longlong lVar2;
  int *piVar3;
  int iVar4;
  longlong lVar5;
  ulonglong uVar6;
  
  lVar1 = DAT_180676ac8;
  if (*(char *)(DAT_180676ac8 + 0x90) == '\0') {
    in_RAX = FUN_180217bf0(DAT_180676ac8);
    if ((char)in_RAX != '\0') {
      return 1;
    }
  }
  if (*(char *)(lVar1 + 0x90) != '\0') {
    return in_RAX & 0xffffffffffffff00;
  }
  lVar2 = FUN_180217940(lVar1);
  if (lVar2 != 0) {
    piVar3 = (int *)(lVar2 + 8);
    if (*(int *)(lVar2 + 8) != 0) {
      iVar4 = 0;
      lVar5 = *(int *)(lVar2 + 8) + lVar2;
      if (lVar5 != 0) {
        iVar4 = (int)lVar5 - (int)piVar3;
      }
      *piVar3 = iVar4;
    }
    lVar5 = 0;
    if (*piVar3 != 0) {
      lVar5 = (longlong)piVar3 + (longlong)*piVar3;
    }
    if (0 < (int)*(uint *)(lVar2 + 0x24)) {
      piVar3 = (int *)(lVar5 + 0x10);
      uVar6 = (ulonglong)*(uint *)(lVar2 + 0x24);
      do {
        iVar4 = *piVar3;
        if ((iVar4 != 0) && ((longlong)iVar4 + (longlong)piVar3 != 0)) {
          lVar5 = iVar4 + lVar2;
          iVar4 = 0;
          if (lVar5 != 0) {
            iVar4 = (int)lVar5 - (int)piVar3;
          }
          *piVar3 = iVar4;
        }
        piVar3 = piVar3 + 0x17;
        uVar6 = uVar6 - 1;
      } while (uVar6 != 0);
    }
    if (*(int *)(lVar2 + 4) == 0x3f2) {
      FUN_18005f200(lVar2);
    }
  }
  FUN_180217900(lVar1,1);
  *(undefined1 *)(lVar1 + 0x90) = 1;
  return 0;
}



// ===================================================
// 1800930d9  ->  FUN_180093060  (entree 180093060)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

byte FUN_180093060(longlong param_1)

{
  longlong lVar1;
  byte bVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined8 *puVar5;
  int iVar6;
  byte bVar7;
  longlong lVar8;
  char *pcVar9;
  undefined1 local_138;
  undefined7 uStack_137;
  undefined8 local_128;
  ulonglong uStack_120;
  undefined8 local_118;
  int iStack_10c;
  longlong local_108 [2];
  undefined1 local_f8 [128];
  undefined **local_78 [12];
  
  local_118 = 0xfffffffffffffffe;
  bVar7 = 0;
  iVar6 = 0;
  pcVar9 = (char *)(param_1 + 0x91);
  do {
    if ((pcVar9[-1] == '\0') && (*pcVar9 != '\0')) {
      bVar2 = FUN_180217bf0((longlong)iVar6 * 0xf8 + param_1);
      if (bVar2 == 0) {
        lVar8 = (longlong)iVar6 * 0xf8 + param_1;
        *(undefined1 *)(lVar8 + 0x90) = 1;
        if ((iVar6 - 8U & 0xfffffffd) == 0) {
          FUN_180092d30(param_1,iVar6);
          puVar5 = (undefined8 *)(lVar8 + 0x98);
          *(undefined8 *)(lVar8 + 0xc0) = *(undefined8 *)(lVar8 + 0xb8);
          *(undefined8 *)(lVar8 + 0xd0) = 0;
          *(undefined8 *)(lVar8 + 0xe0) = *(undefined8 *)(lVar8 + 0xd8);
          *(undefined8 *)(lVar8 + 0xa8) = 0;
          if (0xf < *(ulonglong *)(lVar8 + 0xb0)) {
            puVar5 = (undefined8 *)*puVar5;
          }
          *(undefined1 *)puVar5 = 0;
        }
        else {
          uVar3 = FUN_180217940(lVar8);
          uVar4 = FUN_180217be0(lVar8);
          local_128 = _DAT_1803478a0;
          uStack_120 = _UNK_1803478a8;
          local_138 = 0;
          FUN_180010a10(&local_138,uVar3,uVar4);
          FUN_18008c1b0(local_108,&local_138,1);
          if (0xf < uStack_120) {
            if (0xfff < uStack_120 + 1) {
              lVar1 = *(longlong *)(CONCAT71(uStack_137,local_138) + -8);
              if (0x1f < (CONCAT71(uStack_137,local_138) - lVar1) - 8U) {
                    /* WARNING: Subroutine does not return */
                FUN_180303af0(lVar1,uStack_120 + 0x28);
              }
            }
            FUN_1802fdd80();
          }
          puVar5 = (undefined8 *)(lVar8 + 0x98);
          FUN_180011410(puVar5,local_108);
          *(undefined ***)((longlong)local_108 + (longlong)*(int *)(local_108[0] + 4)) =
               std::basic_istringstream<char,std::char_traits<char>,std::allocator<char>_>::vftable;
          *(int *)((longlong)&iStack_10c + (longlong)*(int *)(local_108[0] + 4)) =
               *(int *)(local_108[0] + 4) + -0x90;
          FUN_18000de80(local_f8);
          *(undefined ***)((longlong)local_108 + (longlong)*(int *)(local_108[0] + 4)) =
               std::basic_istream<char,std::char_traits<char>_>::vftable;
          *(int *)((longlong)&iStack_10c + (longlong)*(int *)(local_108[0] + 4)) =
               *(int *)(local_108[0] + 4) + -0x18;
          local_78[0] = std::ios_base::vftable;
          std::ios_base::_Ios_base_dtor((ios_base *)local_78);
          FUN_180092690(param_1,iVar6);
          *(undefined8 *)(lVar8 + 0xc0) = *(undefined8 *)(lVar8 + 0xb8);
          *(undefined8 *)(lVar8 + 0xd0) = 0;
          *(undefined8 *)(lVar8 + 0xe0) = *(undefined8 *)(lVar8 + 0xd8);
          *(undefined8 *)(lVar8 + 0xa8) = 0;
          if (0xf < *(ulonglong *)(lVar8 + 0xb0)) {
            puVar5 = (undefined8 *)*puVar5;
          }
          *(undefined1 *)puVar5 = 0;
        }
        FUN_18008e750(lVar8 + 0x98);
        FUN_180217900(lVar8,1);
        return 1;
      }
      bVar7 = bVar7 | bVar2;
    }
    iVar6 = iVar6 + 1;
    pcVar9 = pcVar9 + 0xf8;
  } while (iVar6 < 0xe);
  return bVar7;
}



// ===================================================
// 180218110  ->  FUN_180218110  (entree 180218110)
// ===================================================

void FUN_180218110(longlong param_1,int param_2,undefined8 param_3,undefined8 param_4)

{
  *(undefined8 *)(param_1 + 0x30 + (longlong)param_2 * 8) = param_3;
  *(undefined8 *)(param_1 + 0x48 + (longlong)param_2 * 8) = param_4;
  return;
}



// ===================================================
// 180218120  ->  FUN_180218120  (entree 180218120)
// ===================================================

void FUN_180218120(longlong param_1,undefined4 param_2)

{
  *(undefined4 *)(param_1 + 4) = param_2;
  return;
}



