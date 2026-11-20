// ===================================================
// 18003c200  ->  FUN_18003c200  (entree 18003c200)
// ===================================================

void FUN_18003c200(longlong param_1)

{
  longlong lVar1;
  
  if (param_1 != 0) {
    lVar1 = FUN_180040e70();
    if ((lVar1 != 0) &&
       (*(int *)(lVar1 + 0xd8) = *(int *)(lVar1 + 0xd8) + 1, *(int *)(lVar1 + 0xd8) == 1)) {
      FUN_180038600(lVar1);
      return;
    }
  }
  return;
}



// ===================================================
// 1800C3570  ->  FUN_1800c3570  (entree 1800c3570)
// ===================================================

int FUN_1800c3570(int param_1,int param_2,byte *param_3,char param_4,int *param_5,int param_6)

{
  byte bVar1;
  bool bVar2;
  char cVar3;
  uint uVar4;
  int iVar5;
  undefined8 uVar6;
  ulonglong uVar7;
  ulonglong uVar8;
  longlong lVar9;
  longlong *plVar10;
  undefined8 *puVar11;
  longlong lVar12;
  byte *pbVar13;
  int *piVar14;
  ulonglong uVar15;
  ulonglong uVar16;
  ulonglong uVar17;
  char *pcVar18;
  uint uVar19;
  uint *puVar20;
  undefined4 uStack_6d8;
  byte abStack_6d4 [4];
  int aiStack_6d0 [350];
  longlong local_158;
  undefined8 *local_150;
  undefined8 *local_148;
  char *local_140;
  ulonglong local_138;
  undefined8 local_130;
  longlong local_128;
  longlong local_120;
  undefined8 local_118;
  byte local_108 [4];
  byte abStack_104 [4];
  int local_100 [11];
  byte abStack_d4 [4];
  int aiStack_d0 [36];
  
  local_118 = 0xfffffffffffffffe;
  uVar17 = 0;
  *param_5 = 0;
  puVar20 = (uint *)&DAT_18039d3d0;
  uVar6 = FUN_1801509b0();
  uVar4 = FUN_180150840(uVar6,param_1);
  uVar15 = uVar17;
  do {
    uVar19 = (uint)uVar15;
    if (uVar19 == uVar4) break;
    puVar20 = puVar20 + 0xc;
    uVar19 = *puVar20;
    uVar15 = (ulonglong)uVar19;
  } while (uVar19 != 0x15);
  if (uVar19 == 0x15) {
    return -1;
  }
  if (uVar4 == 0x14) {
    if (param_6 == 0xf) {
      puVar20 = (uint *)&DAT_18039d7f0;
    }
    else if (param_6 - 0x15U < 5) {
      puVar20 = (uint *)&DAT_18039d7c0;
    }
  }
  local_158 = 0;
  local_148 = (undefined8 *)0x0;
  local_150 = (undefined8 *)0x0;
  FUN_1800c2b20(&local_158,0x10);
  bVar2 = false;
  pbVar13 = local_108;
  puVar11 = local_150;
  uVar15 = uVar17;
  do {
    pbVar13[0] = 0xff;
    pbVar13[1] = 0xff;
    pbVar13[2] = 0xff;
    pbVar13[3] = 0xff;
    pbVar13[4] = (byte)uVar15;
    pbVar13[8] = 0;
    pbVar13[9] = 0;
    pbVar13[10] = 0;
    pbVar13[0xb] = 0;
    if (!bVar2) {
      iVar5 = *(int *)(*(longlong *)(puVar20 + (longlong)param_2 * 2 + 2) + uVar15 * 4);
      if (iVar5 == -1) {
        bVar2 = true;
      }
      else {
        *(int *)pbVar13 = iVar5;
        if (local_148 == puVar11) {
          FUN_1800c2910(&local_158,puVar11,pbVar13);
          puVar11 = local_150;
        }
        else {
          *puVar11 = *(undefined8 *)pbVar13;
          *(undefined4 *)(puVar11 + 1) = 0;
          local_150 = (undefined8 *)((longlong)local_150 + 0xc);
          puVar11 = local_150;
        }
      }
    }
    uVar15 = uVar15 + 1;
    pbVar13 = pbVar13 + 0xc;
  } while (uVar15 < 4);
  local_138 = 0;
  local_120 = FUN_1800b23a0();
  local_140 = (char *)0x0;
  if (local_120 != 0) {
    uVar6 = FUN_1800b24b0(local_120);
    local_140 = (char *)FUN_1800b2450(uVar6,param_1);
  }
  uVar7 = FUN_18008e900();
  uVar15 = uVar17;
  uVar8 = uVar17;
  if ((ulonglong)(longlong)(int)uVar4 < uVar7) {
    uVar8 = FUN_18008e8e0(uVar4);
    uVar15 = FUN_18008e8c0(uVar4);
    local_138 = uVar15;
  }
  uVar6 = FUN_1801509b0();
  local_130 = FUN_180150a00(uVar6,param_1);
  uVar7 = uVar17;
  do {
    uVar6 = local_130;
    lVar9 = (longlong)(char)uVar7 + 4;
    lVar12 = lVar9 * 0xc;
    pbVar13 = abStack_104 + lVar12 + -4;
    local_128 = lVar12;
    pbVar13[0] = 0xff;
    pbVar13[1] = 0xff;
    pbVar13[2] = 0xff;
    pbVar13[3] = 0xff;
    abStack_104[lVar12] = (char)uVar7 + 4;
    if (((local_140 != (char *)0x0) && (uVar15 != 0)) && (uVar8 != 0)) {
      piVar14 = (int *)(uVar15 + 0x28);
      uVar16 = uVar17;
      pcVar18 = local_140;
      do {
        if (((*piVar14 == (int)uVar7) && (piVar14[1] == (uint)(param_2 != 0))) &&
           (((*(ulonglong *)(pcVar18 + (ulonglong)((uint)piVar14[-10] >> 6) * 8 + 0x160) >>
              ((byte)piVar14[-10] & 0x3f) & 1) != 0 &&
            (cVar3 = FUN_18014a9c0(uVar6), pcVar18 = local_140, uVar6 = local_130, cVar3 != '\0'))))
        {
          plVar10 = (longlong *)(piVar14 + -8);
          if (0xf < *(ulonglong *)(piVar14 + -2)) {
            plVar10 = (longlong *)*plVar10;
          }
          iVar5 = FUN_180046620(plVar10);
          pcVar18 = local_140;
          uVar6 = local_130;
          if (iVar5 != -1) {
            *(int *)pbVar13 = iVar5;
            uVar15 = local_138;
            *(undefined4 *)((longlong)local_100 + local_128) =
                 *(undefined4 *)(local_138 + uVar16 * 0x30);
            if (local_148 == local_150) {
              FUN_1800c2910(&local_158,local_150,pbVar13);
            }
            else {
              *local_150 = *(undefined8 *)pbVar13;
              *(int *)(local_150 + 1) = local_100[lVar9 * 3];
              local_150 = (undefined8 *)((longlong)local_150 + 0xc);
            }
            break;
          }
        }
        uVar16 = uVar16 + 1;
        piVar14 = piVar14 + 0xc;
        uVar15 = local_138;
      } while (uVar16 < uVar8);
    }
    uVar4 = (int)uVar7 + 1;
    uVar7 = (ulonglong)uVar4;
  } while ((int)uVar4 < 0xc);
  iVar5 = FUN_18019c090();
  if (((iVar5 == 3) && (param_2 == 0)) && (*local_140 != '\0')) {
    uVar6 = FUN_1800b24b0(local_120);
    iVar5 = FUN_1800b4940(uVar6);
    uVar15 = uVar17;
    if (iVar5 == param_1) {
      do {
        lVar12 = (longlong)(char)uVar15 + 4;
        iVar5 = *(int *)(abStack_104 + lVar12 * 0xc + -4);
        if (iVar5 != -1) {
          *param_3 = abStack_104[lVar12 * 0xc];
          *param_5 = local_100[lVar12 * 3];
          goto LAB_1800c3a8b;
        }
        uVar15 = uVar15 + 1;
      } while (uVar15 < 0xc);
    }
  }
  if ((param_4 != '\0') && (*param_3 < 4)) {
    uVar6 = FUN_180190a50(param_1 != 0);
    do {
      if ((*param_3 == ((char)uVar17 + 4U & 3)) &&
         ((((cVar3 = FUN_180190b80(uVar6,9), cVar3 != '\0' && (uVar17 < 4)) ||
           ((cVar3 = FUN_180190b80(uVar6,7), cVar3 != '\0' && (uVar17 - 4 < 4)))) ||
          ((cVar3 = FUN_180190b80(uVar6,8), cVar3 != '\0' && (7 < uVar17)))))) {
        lVar12 = (longlong)(char)uVar17 + 4;
        iVar5 = *(int *)(abStack_104 + lVar12 * 0xc + -4);
        if (iVar5 != -1) {
          *param_3 = abStack_104[lVar12 * 0xc];
          *param_5 = local_100[lVar12 * 3];
          goto LAB_1800c3a8b;
        }
      }
      uVar17 = uVar17 + 1;
    } while (uVar17 < 0xc);
  }
  bVar1 = *param_3;
  if (bVar1 < 0x10) {
    iVar5 = *(int *)(abStack_104 + (longlong)(char)bVar1 * 0xc + -4);
    if (iVar5 != -1) {
      *param_5 = local_100[(longlong)(char)bVar1 * 3];
      goto LAB_1800c3a8b;
    }
    *param_3 = 0xff;
  }
  lVar12 = ((longlong)local_150 - local_158) / 6 + ((longlong)local_150 - local_158 >> 0x3f);
  uVar15 = (lVar12 >> 1) - (lVar12 >> 0x3f);
  if (uVar15 == 0) {
    *param_3 = 0xff;
    iVar5 = -1;
  }
  else {
    uVar4 = FUN_180244bb0(5);
    piVar14 = (int *)(local_158 + ((ulonglong)uVar4 % uVar15 & 0xffffffff) * 0xc);
    iVar5 = *piVar14;
    *param_3 = *(byte *)(piVar14 + 1);
    *param_5 = piVar14[2];
  }
LAB_1800c3a8b:
  if (local_158 != 0) {
    uVar15 = (((longlong)local_148 - local_158) / 0xc) * 0xc;
    lVar12 = local_158;
    if (0xfff < uVar15) {
      lVar12 = *(longlong *)(local_158 + -8);
      if (0x1f < (local_158 - lVar12) - 8U) {
                    /* WARNING: Subroutine does not return */
        FUN_180303af0((longlong)local_148 - local_158,uVar15 + 0x27);
      }
    }
    FUN_1802fdd80(lVar12);
  }
  return iVar5;
}



