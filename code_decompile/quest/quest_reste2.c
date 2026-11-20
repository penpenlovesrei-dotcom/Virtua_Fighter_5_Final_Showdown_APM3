// ===================================================
// 822E8158  ->  FUN_822e8158  (entree 822e8158)
// ===================================================

/* WARNING: Function: __savegprlr_22 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_22 replaced with injection: x360_restgprlr */

void FUN_822e8158(int param_1,int param_2)

{
  uint uVar1;
  bool bVar2;
  undefined8 in_r0;
  char cVar3;
  uint uVar4;
  uint uVar5;
  int iVar6;
  int aiStack_70 [2];
  uint uStack_68;
  uint uStack_64;
  undefined1 uStack_60;
  undefined1 uStack_5f;
  undefined1 uStack_5e;
  undefined1 uStack_5d;
  uint uStack_5c;
  
  uVar4 = param_1 + 0x5c8;
  uStack_5c = *(uint *)(param_1 + 0x5d0);
  uStack_64 = *(uint *)(param_1 + 0x5cc);
  if (uStack_5c < uStack_64) {
    trapWord(0x1f,in_r0,0x16);
  }
  uStack_60 = (undefined1)(uVar4 >> 0x18);
  uStack_5f = (undefined1)(uVar4 >> 0x10);
  uStack_5e = (undefined1)(uVar4 >> 8);
  uStack_5d = (undefined1)uVar4;
  if (uStack_5c < uStack_64) {
    trapWord(0x1f,in_r0,0x16);
  }
  uStack_68 = uVar4;
  FUN_82318f58(&uStack_60,uVar4,CONCAT44(uVar4,uStack_64),CONCAT44(uVar4,uStack_5c));
  uVar5 = 0;
  cVar3 = FUN_822c8b30(0,&uStack_68,0,aiStack_70);
  do {
    if (cVar3 == '\0') {
      return;
    }
    if ((param_2 == aiStack_70[0]) && (cVar3 = FUN_822c8bb0(uVar5), cVar3 == '\0')) {
      iVar6 = param_1 + 0x578;
      if (0xff < uVar5) {
        FUN_822c5128(iVar6);
      }
      bVar2 = (1 << (uVar5 & 0x1f) & *(uint *)((uVar5 >> 3 & 0x1ffffffc) + iVar6)) != 0;
      uStack_60 = bVar2;
      if (bVar2) {
        if (0xff < uVar5) {
          FUN_822c5128(iVar6);
        }
        uVar1 = *(uint *)((uVar5 >> 3 & 0x1ffffffc) + iVar6);
        if (0xff < uVar5) {
          FUN_822c5128(param_1 + 0x598);
        }
        uStack_5f = 1;
        if (((1 << (uVar5 & 0x1f) & uVar1) == 0 ^ 1) ==
            ((uint)LZCOUNT(1 << (uVar5 & 0x1f) &
                           *(uint *)((uVar5 >> 3 & 0x1ffffffc) + param_1 + 0x598)) >> 5 ^ 1))
        goto LAB_822e82bc;
      }
      else {
LAB_822e82bc:
        uStack_5f = 0;
      }
      uStack_5e = (undefined1)uVar5;
      uStack_5c = uStack_68;
      if (!bVar2) {
        uStack_5c = 0x60ba;
      }
      FUN_82319818(uVar4,&uStack_60);
    }
    uVar5 = uVar5 + 1 & 0xff;
    cVar3 = FUN_822c8b30(uVar5,&uStack_68,0,aiStack_70);
  } while( true );
}



// ===================================================
// 822E8320  ->  FUN_822e8320  (entree 822e8320)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_822e8320(int param_1)

{
  int iVar1;
  int iVar2;
  char cVar3;
  int *piVar4;
  
  piVar4 = (int *)(param_1 + 0x818);
  iVar1 = *(int *)(param_1 + 0x818);
  iVar2 = FUN_822d1868();
  if (-1 < iVar2) {
    FUN_822d11a8();
    *(undefined4 *)(param_1 + 0x5bc) = 4;
    return;
  }
  iVar2 = FUN_822d1830();
  if (-1 < iVar2) {
    FUN_822d1198();
    *(undefined1 *)(param_1 + 0x828) = 0;
    if ((*(int *)(param_1 + 0x5cc) == 0) ||
       (*(int *)(param_1 + 0x5d0) - *(int *)(param_1 + 0x5cc) >> 3 == 0)) {
      *(undefined1 *)(param_1 + 0x828) = 1;
    }
    if (*(char *)((*(int *)(param_1 + 0x824) + 0xbb) * 8 + *(int *)(param_1 + 0x820) + param_1) ==
        '\x02') {
      *(undefined1 *)(param_1 + 0x828) = 1;
    }
    *(undefined4 *)(param_1 + 0x814) = 1;
    return;
  }
  cVar3 = FUN_822d0f88(piVar4,*(undefined4 *)(param_1 + 0x81c),0);
  if (cVar3 != '\0') {
    FUN_822d1188();
    *(undefined4 *)(param_1 + 0x820) = 0;
    *(undefined4 *)(param_1 + 0x824) = 0;
    FUN_822e8158(param_1,*piVar4);
    FUN_822e7600(param_1,*piVar4);
    if (iVar1 < *piVar4) {
      FUN_822f65f8(param_1 + 0xa08);
    }
    if (*piVar4 < iVar1) {
      FUN_822f65f8(param_1 + 0x9e4);
    }
  }
  return;
}



// ===================================================
// 822E8440  ->  FUN_822e8440  (entree 822e8440)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

undefined8 FUN_822e8440(int param_1)

{
  char cVar3;
  undefined8 uVar1;
  undefined4 uVar2;
  undefined8 uVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  undefined **ppuVar8;
  undefined4 uStack_70;
  undefined4 uStack_6c;
  undefined4 uStack_68;
  undefined4 uStack_60;
  undefined4 uStack_5c;
  undefined4 uStack_58;
  undefined4 uStack_50;
  undefined4 uStack_4c;
  undefined4 uStack_48;
  
  uVar4 = 0;
  switch(*(undefined4 *)(param_1 + 0x5bc)) {
  case 0:
    cVar3 = FUN_822e74d8(param_1);
    if (cVar3 == '\0') {
      FUN_822e8158(param_1,*(undefined4 *)(param_1 + 0x818));
      FUN_822e7600(param_1,*(undefined4 *)(param_1 + 0x818));
      iVar7 = param_1 + 0x600;
      FUN_822e3ad8(iVar7);
      FUN_821dc9b8(iVar7,6);
      FUN_822e3778(iVar7,0x1c,0);
      FUN_822e2f20(param_1 + 0x634);
      FUN_822c8aa0(param_1 + 0x634,0xffffffff82086130);
      *(undefined1 *)(param_1 + 0x6b5) = 0;
      FUN_822e2e98(param_1 + 0x6b8);
      FUN_822c8aa0(param_1 + 0x6b8,0xffffffff82086110);
      *(undefined1 *)(param_1 + 0x70d) = 0;
      *(undefined4 *)(param_1 + 0x5bc) = 1;
    }
    break;
  case 1:
    iVar7 = param_1 + 0x600;
    cVar3 = FUN_822e2dd8(iVar7);
    if (cVar3 != '\0') {
      if (*(char *)(param_1 + 0x829) == '\0') {
        *(undefined4 *)(param_1 + 0x5bc) = 2;
      }
      else {
        *(undefined4 *)(param_1 + 0x80c) = 2;
        *(undefined4 *)(param_1 + 0x810) = 0;
        *(undefined4 *)(param_1 + 0x5bc) = 3;
      }
      uStack_70 = DAT_82000a34;
      uStack_6c = DAT_82000a34;
      uStack_68 = DAT_82000a34;
      FUN_822e39c0(iVar7,param_1 + 0x9b4,0xffffffff820860fc,1);
      FUN_822e39c0(iVar7,param_1 + 0x9c0,0xffffffff820860e8,1);
      FUN_822e39c0(iVar7,param_1 + 0x9cc,0xffffffff820860d4,1);
      FUN_822e39c0(iVar7,param_1 + 0x9d8,0xffffffff820860b8,1);
      iVar6 = param_1 + 0x834;
      ppuVar8 = &PTR_s_p_emb_1a_c_82655088;
      do {
        iVar5 = 8;
        do {
          FUN_822e39c0(iVar7,iVar6,*ppuVar8,1);
          iVar5 = iVar5 + -1;
          ppuVar8 = ppuVar8 + 1;
          iVar6 = iVar6 + 0xc;
        } while (iVar5 != 0);
      } while ((int)ppuVar8 < -0x7d9aaef8);
      FUN_822e39c0(iVar7,&uStack_70,0xffffffff820860a0,1);
      uStack_60 = uStack_70;
      uStack_5c = uStack_6c;
      uStack_58 = uStack_68;
      FUN_822f66f0(param_1 + 0x9e4,2,7,&uStack_60);
      FUN_822e39c0(iVar7,&uStack_70,0xffffffff82086088,1);
      uStack_50 = uStack_70;
      uStack_4c = uStack_6c;
      uStack_48 = uStack_68;
      FUN_822f66f0(param_1 + 0xa08,3,7,&uStack_50);
      *(undefined1 *)(param_1 + 0x82b) = 1;
    }
    break;
  case 2:
    if (*(int *)(param_1 + 0x814) == 0) {
      FUN_822e8320(param_1);
    }
    else if (*(int *)(param_1 + 0x814) == 1) {
      FUN_822e79a8(param_1);
    }
    else {
      *(undefined4 *)(param_1 + 0x814) = 0;
    }
    break;
  case 3:
    FUN_822e7d68(param_1);
    break;
  case 4:
    iVar7 = param_1 + 0x600;
    cVar3 = FUN_822e2dd8(iVar7);
    if (cVar3 != '\0') {
      FUN_822fb5b8(param_1 + 0x82c);
      FUN_822fb5b8(param_1 + 0x830);
      FUN_822f6578(param_1 + 0x9e4);
      FUN_822f6578(param_1 + 0xa08);
      *(undefined1 *)(param_1 + 0x82b) = 0;
      FUN_822e37b8(iVar7);
    }
    cVar3 = FUN_822e2df0(iVar7);
    if (cVar3 != '\0') goto switchD_822e8478_default;
    break;
  default:
switchD_822e8478_default:
    uVar4 = 1;
  }
  FUN_822e4d70(param_1 + 0x600);
  FUN_822e70d0(param_1);
  if (*(int *)(param_1 + 0x814) == 0) {
    uVar1 = 0x128;
  }
  else {
    if (*(int *)(param_1 + 0x814) != 1) goto LAB_822e8790;
    uVar1 = 0x129;
  }
  uVar2 = FUN_82322798(uVar1);
  *(undefined4 *)(param_1 + 0x680) = uVar2;
LAB_822e8790:
  uVar2 = FUN_82322798(3);
  *(undefined4 *)(param_1 + 0x704) = uVar2;
  return uVar4;
}



// ===================================================
// 822EF340  ->  FUN_822ef340  (entree 822ef340)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_822ef340(int param_1)

{
  undefined8 uVar1;
  undefined4 auStack_40 [16];
  
  auStack_40[0] = 0x3b8;
  auStack_40[1] = 0x3bc;
  auStack_40[2] = 0x3c2;
  auStack_40[3] = 0x3c9;
  auStack_40[4] = 0x3ce;
  auStack_40[5] = 0x3d5;
  FUN_8223bc10(0xe);
  FUN_8223c130(8);
  FUN_8223beb8((double)*(float *)(param_1 + 0x590),(double)*(float *)(param_1 + 0x594));
  FUN_8223c048(0xffffffffffbff560);
  uVar1 = FUN_82322798(0x3a9);
  FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar1);
  FUN_8223beb8((double)*(float *)(param_1 + 0x59c),(double)*(float *)(param_1 + 0x5a0));
  if (*(int *)(param_1 + 0x91c) == 0) {
    uVar1 = 0xffffffffff6cbede;
  }
  else {
    uVar1 = 0xffffffffffffffff;
  }
  FUN_8223c048(uVar1);
  uVar1 = FUN_82322798(auStack_40[*(int *)(param_1 + 0x924)]);
  FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,uVar1);
  return;
}



// ===================================================
// 822EF430  ->  FUN_822ef430  (entree 822ef430)
// ===================================================

undefined8 FUN_822ef430(int param_1)

{
  uint uVar1;
  char cVar2;
  
  uVar1 = *(uint *)(param_1 + 0x584);
  if (uVar1 == 0) {
    FUN_82356c08();
    *(undefined4 *)(param_1 + 0x680) =
         *(undefined4 *)(&DAT_8208bc00 + (uint)*(byte *)(param_1 + 0x148) * 4);
    FUN_822c2a80();
    *(undefined4 *)(param_1 + 0x584) = 1;
  }
  else if (uVar1 == 1) {
    cVar2 = FUN_822c2848(*(undefined4 *)(param_1 + 0x680));
    if (cVar2 == '\0') {
      FUN_82356ca0();
      *(undefined4 *)(param_1 + 0x584) = 2;
      return 0;
    }
  }
  else if (uVar1 < 3) {
    return 0;
  }
  return 1;
}



// ===================================================
// 822EF740  ->  FUN_822ef740  (entree 822ef740)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_822ef740(int param_1)

{
  float fVar1;
  float fVar2;
  undefined8 uVar3;
  float *pfVar4;
  undefined8 uVar5;
  int iVar6;
  int iVar7;
  float *pfVar8;
  undefined4 *puVar9;
  double dVar10;
  undefined4 uStack_d0;
  undefined4 uStack_cc;
  undefined4 uStack_c8;
  float fStack_c0;
  float fStack_bc;
  float fStack_b8;
  float fStack_b0;
  float fStack_ac;
  float fStack_a8;
  undefined4 uStack_a0;
  undefined4 uStack_9c;
  float fStack_98;
  undefined1 auStack_90 [16];
  float afStack_80 [4];
  float fStack_70;
  float fStack_6c;
  float fStack_68;
  float fStack_64;
  float fStack_60;
  float fStack_5c;
  float fStack_58;
  float fStack_54;
  float fStack_50;
  float fStack_4c;
  float fStack_48;
  
  if (*(int *)(param_1 + 0x588) != 0) {
    uVar3 = FUN_822c29e8();
    FUN_822c29d8(2);
    FUN_822c2a08(9);
    dVar10 = (double)DAT_82000a34;
    afStack_80[0] = DAT_82000a34;
    iVar6 = *(int *)(param_1 + 0x924) * 0x10 + param_1;
    afStack_80[1] = DAT_82000a34;
    afStack_80[2] = DAT_82000a34;
    afStack_80[3] = DAT_82000a34;
    fStack_70 = DAT_82000a34;
    fStack_6c = DAT_82000a34;
    iVar7 = *(int *)(iVar6 + 0x8b0);
    fStack_68 = DAT_82000a34;
    fStack_64 = DAT_82000a34;
    fStack_60 = DAT_82000a34;
    fStack_5c = DAT_82000a34;
    fStack_58 = DAT_82000a34;
    fStack_54 = DAT_82000a34;
    fStack_50 = DAT_82000a34;
    fStack_4c = DAT_82000a34;
    fStack_48 = DAT_82000a34;
    if (iVar7 == 0) {
      iVar7 = 0;
    }
    else {
      iVar7 = *(int *)(iVar6 + 0x8b4) - iVar7;
      iVar7 = iVar7 / 0x14 + (iVar7 >> 0x1f);
      iVar7 = iVar7 - (iVar7 >> 0x1f);
    }
    pfVar8 = afStack_80;
    puVar9 = (undefined4 *)(param_1 + 0x5bc);
    iVar6 = 5;
    do {
      uStack_d0 = puVar9[-2];
      uStack_cc = puVar9[-1];
      uStack_c8 = *puVar9;
      pfVar4 = (float *)FUN_822f6658(auStack_90,&uStack_d0);
      iVar6 = iVar6 + -1;
      fVar1 = pfVar4[1];
      puVar9 = puVar9 + 3;
      fVar2 = pfVar4[2];
      *pfVar8 = *pfVar4;
      pfVar8[1] = fVar1;
      pfVar8[2] = fVar2;
      pfVar8 = pfVar8 + 3;
    } while (iVar6 != 0);
    if (*(int *)(param_1 + 0x91c) == 1) {
      if (*(int *)(param_1 + 0x58c) == 0) {
        FUN_822f69d8((undefined4 *)(param_1 + 0x58c),0x422,0xffffffff82088214,7,0x20000,0,0);
      }
      iVar6 = *(int *)(param_1 + 0x928) - *(int *)(param_1 + 0x92c);
      fStack_c0 = afStack_80[iVar6 * 3];
      fStack_bc = afStack_80[iVar6 * 3 + 1];
      fStack_b8 = afStack_80[iVar6 * 3 + 2];
      FUN_82166540(*(undefined4 *)(param_1 + 0x58c),&fStack_c0);
    }
    else if ((*(int *)(param_1 + 0x91c) == 0) && (*(int *)(param_1 + 0x58c) == 0)) {
      FUN_822f69d8(param_1 + 0x58c,0x422,0xffffffff82088224,7,0x20000,0,0);
    }
    puVar9 = (undefined4 *)(param_1 + 0x930);
    if (*(int *)(param_1 + 0x930) == 0) {
      fStack_a8 = (float)dVar10;
      fStack_b0 = afStack_80[0] + DAT_82015b00;
      fStack_ac = afStack_80[1] + DAT_820036d8;
      FUN_822f6768(puVar9,0xe2,0xffffffff82011310,&fStack_b0,8,0x20000,0xffffffff8200eb74);
      fStack_98 = (float)dVar10;
      uStack_a0 = DAT_8208bc68;
      uStack_9c = DAT_8208bc68;
      FUN_82166558(*puVar9,&uStack_a0);
      FUN_82166528(*puVar9,0);
    }
    uVar5 = 1;
    if (*(int *)(param_1 + 0x924) < 1) {
      uVar5 = 2;
    }
    FUN_821ccba8(param_1 + 0x638,uVar5);
    FUN_822f6830(param_1 + 0x638);
    uVar5 = 1;
    if (4 < *(int *)(param_1 + 0x924)) {
      uVar5 = 2;
    }
    FUN_821ccba8(param_1 + 0x65c,uVar5);
    FUN_822f6830(param_1 + 0x65c);
    uVar5 = 1;
    if (*(int *)(param_1 + 0x92c) < 1) {
      uVar5 = 2;
    }
    FUN_821ccba8(param_1 + 0x5f0,uVar5);
    FUN_822f6830(param_1 + 0x5f0);
    uVar5 = 1;
    if (iVar7 <= *(int *)(param_1 + 0x92c) + 5) {
      uVar5 = 2;
    }
    FUN_821ccba8(param_1 + 0x614,uVar5);
    FUN_822f6830(param_1 + 0x614);
    FUN_822c2a18();
    FUN_822c29d8(uVar3);
  }
  return;
}



// ===================================================
// 822F0820  ->  FUN_822f0820  (entree 822f0820)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_822f0820(longlong param_1,char *param_2)

{
  char cVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  char *pcVar4;
  undefined1 auStack_40 [8];
  undefined1 auStack_38 [8];
  undefined1 auStack_30 [48];
  
  param_1 = param_1 + 0xc0;
  puVar2 = (undefined8 *)FUN_8215c470(auStack_40,param_1);
  puVar3 = (undefined8 *)FUN_82245ee8(auStack_38,param_1);
  FUN_8215d158(auStack_30,param_1,*puVar3,*puVar2);
  pcVar4 = param_2;
  do {
    cVar1 = *pcVar4;
    pcVar4 = pcVar4 + 1;
  } while (cVar1 != '\0');
  FUN_82141840(param_1,param_2,pcVar4 + (-1 - (int)param_2));
  return;
}



// ===================================================
// 822F08A0  ->  FUN_822f08a0  (entree 822f08a0)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

void FUN_822f08a0(longlong param_1,char *param_2)

{
  char cVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  char *pcVar4;
  undefined1 auStack_40 [8];
  undefined1 auStack_38 [8];
  undefined1 auStack_30 [48];
  
  param_1 = param_1 + 0xdc;
  puVar2 = (undefined8 *)FUN_8215c470(auStack_40,param_1);
  puVar3 = (undefined8 *)FUN_82245ee8(auStack_38,param_1);
  FUN_8215d158(auStack_30,param_1,*puVar3,*puVar2);
  pcVar4 = param_2;
  do {
    cVar1 = *pcVar4;
    pcVar4 = pcVar4 + 1;
  } while (cVar1 != '\0');
  FUN_82141840(param_1,param_2,pcVar4 + (-1 - (int)param_2));
  return;
}



// ===================================================
// 822F0920  ->  FUN_822f0920  (entree 822f0920)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */
/* WARNING: Removing unreachable block (ram,0x822f0a80) */
/* WARNING: Removing unreachable block (ram,0x822f0a84) */
/* WARNING: Removing unreachable block (ram,0x822f0a94) */
/* WARNING: Removing unreachable block (ram,0x822f0aa8) */
/* WARNING: Removing unreachable block (ram,0x822f0b04) */

undefined8 FUN_822f0920(int param_1)

{
  uint uVar1;
  undefined8 in_r0;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined4 uVar4;
  uint *puVar5;
  uint uVar6;
  undefined4 *puVar7;
  undefined4 *puVar8;
  ulonglong uVar9;
  undefined4 *puVar10;
  int iVar11;
  int iStack_38;
  undefined4 *puStack_34;
  
  FUN_822f3068();
  uVar2 = FUN_821ccbb8();
  uVar3 = FUN_82235f28(0xffffffff827a99f8,uVar2);
  FUN_821de388(param_1 + 0x50,uVar3);
  FUN_822da898(uVar2);
  uVar4 = FUN_822dac40();
  *(undefined4 *)(param_1 + 0x578) = uVar4;
  uVar6 = 0;
  *(undefined4 *)(param_1 + 0x57c) = 0;
  *(undefined4 *)(param_1 + 0x584) = 0;
  *(undefined4 *)(param_1 + 0x588) = 0;
  *(undefined4 *)(param_1 + 0x92c) = 0;
  *(undefined4 *)(param_1 + 0x91c) = 0;
  *(undefined4 *)(param_1 + 0x920) = 0;
  *(undefined4 *)(param_1 + 0x924) = 0;
  *(undefined4 *)(param_1 + 0x928) = 0;
  *(undefined4 *)(param_1 + 0x930) = 0;
  *(undefined1 *)(param_1 + 0x935) = 0;
  *(undefined1 *)(param_1 + 0x936) = 0;
  *(undefined1 *)(param_1 + 0x937) = 0;
  *(undefined1 *)(param_1 + 0x934) = 1;
  uVar9 = (ulonglong)*(uint *)(param_1 + 0x180);
  if (uVar9 != 0) {
    do {
      uVar1 = (uint)uVar9;
      uVar9 = uVar9 >> 4;
      uVar6 = (int)(char)(&DAT_8264ff24)[uVar1 & 0xf] + uVar6;
    } while (uVar9 != 0);
    if (6 < uVar6) {
      if (*(byte *)(param_1 + 0x184) < 8) {
        *(undefined1 *)(param_1 + 0x934) = 0;
      }
      else {
        *(undefined1 *)(param_1 + 0x937) = 1;
      }
    }
  }
  if ((*(char *)(param_1 + 0x934) == '\0') && (*(char *)(param_1 + 0x937) == '\0')) {
    *(undefined1 *)(param_1 + 0x935) = 1;
  }
  puVar5 = (uint *)(param_1 + 0x8b4);
  iVar11 = 6;
  do {
    uVar6 = puVar5[-1];
    if (*puVar5 < uVar6) {
      trapWord(0x1f,in_r0,0x16);
      trapWord(0x1f,in_r0,0x16);
    }
    if (puVar5 == (uint *)0x8) {
      trapWord(0x1f,in_r0,0x16);
    }
    if (uVar6 != *puVar5) {
      *puVar5 = uVar6;
    }
    iVar11 = iVar11 + -1;
    puVar5 = puVar5 + 4;
  } while (iVar11 != 0);
  uVar6 = *(uint *)(param_1 + 0x910);
  if (*(uint *)(param_1 + 0x914) < uVar6) {
    trapWord(0x1f,in_r0,0x16);
    trapWord(0x1f,in_r0,0x16);
  }
  if (uVar6 != *(uint *)(param_1 + 0x914)) {
    *(uint *)(param_1 + 0x914) = uVar6;
  }
  iStack_38 = param_1 + 0x890;
  puVar10 = (undefined4 *)(param_1 + 0x894);
  uVar6 = *(uint *)(param_1 + 0x8a8);
  puVar7 = puVar10;
  if (0xf < uVar6) {
    puVar7 = *(undefined4 **)(param_1 + 0x894);
  }
  iVar11 = *(int *)(param_1 + 0x8a4);
  puVar7 = (undefined4 *)(iVar11 + (int)puVar7);
  if (puVar7 == (undefined4 *)0x0) {
LAB_822f0b7c:
    trapWord(0x1f,in_r0,0x16);
  }
  else {
    puVar8 = puVar10;
    if (0xf < uVar6) {
      puVar8 = (undefined4 *)*puVar10;
    }
    if (puVar7 < puVar8) goto LAB_822f0b7c;
    puVar8 = puVar10;
    if (0xf < uVar6) {
      puVar8 = (undefined4 *)*puVar10;
    }
    if ((undefined4 *)(iVar11 + (int)puVar8) < puVar7) goto LAB_822f0b7c;
  }
  puStack_34 = puVar10;
  if (0xf < uVar6) {
    puStack_34 = (undefined4 *)*puVar10;
  }
  if (puStack_34 != (undefined4 *)0x0) {
    puVar8 = puVar10;
    if (0xf < uVar6) {
      puVar8 = (undefined4 *)*puVar10;
    }
    if (puVar8 <= puStack_34) {
      if (0xf < uVar6) {
        puVar10 = (undefined4 *)*puVar10;
      }
      if (puStack_34 <= (undefined4 *)(iVar11 + (int)puVar10)) goto LAB_822f0bdc;
    }
  }
  trapWord(0x1f,in_r0,0x16);
LAB_822f0bdc:
  FUN_8215d158(&iStack_38,iStack_38,CONCAT44(iStack_38,puStack_34),CONCAT44(iStack_38,puVar7));
  *(undefined4 *)(param_1 + 0x58c) = 0;
  return 1;
}



// ===================================================
// 822F0C08  ->  FUN_822f0c08  (entree 822f0c08)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */
/* WARNING: Removing unreachable block (ram,0x822f0ca4) */
/* WARNING: Removing unreachable block (ram,0x822f0ca8) */
/* WARNING: Removing unreachable block (ram,0x822f0cb8) */
/* WARNING: Removing unreachable block (ram,0x822f0ccc) */
/* WARNING: Removing unreachable block (ram,0x822f0d28) */

undefined8 FUN_822f0c08(int param_1)

{
  uint uVar1;
  undefined8 in_r0;
  undefined8 uVar2;
  uint *puVar3;
  undefined4 *puVar4;
  undefined4 *puVar5;
  undefined4 *puVar6;
  int iVar7;
  int iStack_28;
  undefined4 *puStack_24;
  
  FUN_822f3068();
  uVar2 = FUN_821ccbb8();
  FUN_82236060(0xffffffff827a99f8,param_1 + 0x50,uVar2);
  puVar3 = (uint *)(param_1 + 0x8b4);
  iVar7 = 6;
  do {
    uVar1 = puVar3[-1];
    if (*puVar3 < uVar1) {
      trapWord(0x1f,in_r0,0x16);
      trapWord(0x1f,in_r0,0x16);
    }
    if (puVar3 == (uint *)0x8) {
      trapWord(0x1f,in_r0,0x16);
    }
    if (uVar1 != *puVar3) {
      *puVar3 = uVar1;
    }
    iVar7 = iVar7 + -1;
    puVar3 = puVar3 + 4;
  } while (iVar7 != 0);
  uVar1 = *(uint *)(param_1 + 0x910);
  if (*(uint *)(param_1 + 0x914) < uVar1) {
    trapWord(0x1f,in_r0,0x16);
    trapWord(0x1f,in_r0,0x16);
  }
  if (uVar1 != *(uint *)(param_1 + 0x914)) {
    *(uint *)(param_1 + 0x914) = uVar1;
  }
  iStack_28 = param_1 + 0x890;
  puVar6 = (undefined4 *)(param_1 + 0x894);
  uVar1 = *(uint *)(param_1 + 0x8a8);
  puVar4 = puVar6;
  if (0xf < uVar1) {
    puVar4 = *(undefined4 **)(param_1 + 0x894);
  }
  iVar7 = *(int *)(param_1 + 0x8a4);
  puVar4 = (undefined4 *)(iVar7 + (int)puVar4);
  if (puVar4 == (undefined4 *)0x0) {
LAB_822f0da0:
    trapWord(0x1f,in_r0,0x16);
  }
  else {
    puVar5 = puVar6;
    if (0xf < uVar1) {
      puVar5 = (undefined4 *)*puVar6;
    }
    if (puVar4 < puVar5) goto LAB_822f0da0;
    puVar5 = puVar6;
    if (0xf < uVar1) {
      puVar5 = (undefined4 *)*puVar6;
    }
    if ((undefined4 *)(iVar7 + (int)puVar5) < puVar4) goto LAB_822f0da0;
  }
  puStack_24 = puVar6;
  if (0xf < uVar1) {
    puStack_24 = (undefined4 *)*puVar6;
  }
  if (puStack_24 != (undefined4 *)0x0) {
    puVar5 = puVar6;
    if (0xf < uVar1) {
      puVar5 = (undefined4 *)*puVar6;
    }
    if (puVar5 <= puStack_24) {
      if (0xf < uVar1) {
        puVar6 = (undefined4 *)*puVar6;
      }
      if (puStack_24 <= (undefined4 *)(iVar7 + (int)puVar6)) goto LAB_822f0e00;
    }
  }
  trapWord(0x1f,in_r0,0x16);
LAB_822f0e00:
  FUN_8215d158(&iStack_28,iStack_28,CONCAT44(iStack_28,puStack_24),CONCAT44(iStack_28,puVar4));
  FUN_822c2888(*(undefined4 *)(param_1 + 0x680));
  *(undefined4 *)(param_1 + 0x584) = 3;
  FUN_822c7d50(param_1 + 0x6b0);
  FUN_822c7d50(param_1 + 0x734);
  return 1;
}



// ===================================================
// 822F0E48  ->  FUN_822f0e48  (entree 822f0e48)
// ===================================================

void FUN_822f0e48(int param_1,undefined4 param_2,char *param_3)

{
  char cVar1;
  char *pcVar2;
  
  *(undefined4 *)(param_1 + 0x888) = param_2;
  *(undefined4 *)(param_1 + 0x88c) = 0;
  pcVar2 = param_3;
  if (param_3 != (char *)0x0) {
    do {
      cVar1 = *pcVar2;
      pcVar2 = pcVar2 + 1;
    } while (cVar1 != '\0');
    FUN_82141840(param_1 + 0x890,param_3,pcVar2 + (-1 - (int)param_3));
  }
  *(undefined4 *)(param_1 + 0x57c) = 3;
  return;
}



// ===================================================
// 822F0EC0  ->  FUN_822f0ec0  (entree 822f0ec0)
// ===================================================

void FUN_822f0ec0(int param_1,uint param_2)

{
  undefined8 in_r0;
  uint uVar1;
  int iVar2;
  
  if (*(int *)(param_1 + 4) != 0) {
    iVar2 = *(int *)(param_1 + 8) - *(int *)(param_1 + 4);
    iVar2 = iVar2 / 0x14 + (iVar2 >> 0x1f);
    if (param_2 < (uint)(iVar2 - (iVar2 >> 0x1f))) goto LAB_822f0f14;
  }
  FUN_82234ec8();
LAB_822f0f14:
  if (*(uint *)(param_1 + 8) < *(uint *)(param_1 + 4)) {
    trapWord(0x1f,in_r0,0x16);
  }
  uVar1 = param_2 * 0x14 + *(uint *)(param_1 + 4);
  if ((*(uint *)(param_1 + 8) < uVar1) || (uVar1 < *(uint *)(param_1 + 4))) {
    trapWord(0x1f,in_r0,0x16);
  }
  if (*(uint *)(param_1 + 8) <= uVar1) {
    trapWord(0x1f,in_r0,0x16);
  }
  return;
}



// ===================================================
// 822F0F90  ->  FUN_822f0f90  (entree 822f0f90)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_822f0f90(int param_1,ulonglong param_2,ulonglong param_3,undefined4 *param_4)

{
  undefined4 uVar1;
  uint uVar2;
  undefined4 *puVar3;
  ulonglong uVar4;
  ulonglong uVar5;
  ulonglong uVar6;
  undefined4 *puVar10;
  longlong lVar7;
  undefined4 *puVar11;
  ulonglong uVar8;
  ulonglong uVar9;
  int iVar13;
  undefined4 *puVar14;
  int iVar15;
  ulonglong uVar12;
  uint uVar16;
  ulonglong uVar17;
  ulonglong uVar18;
  longlong lVar19;
  longlong lVar20;
  ulonglong uStack00000018;
  undefined1 uStack_60;
  undefined4 auStack_50 [20];
  
  puVar11 = auStack_50;
  lVar19 = 5;
  do {
    uVar1 = *param_4;
    param_4 = param_4 + 1;
    *puVar11 = uVar1;
    puVar11 = puVar11 + 1;
    lVar19 = lVar19 + -1;
  } while (lVar19 != 0);
  iVar13 = *(int *)(param_1 + 4);
  if (iVar13 == 0) {
    uVar4 = 0;
  }
  else {
    iVar15 = *(int *)(param_1 + 0xc) - iVar13;
    uVar16 = iVar15 / 0x14 + (iVar15 >> 0x1f);
    uVar4 = (longlong)(int)uVar16 + (ulonglong)(uVar16 >> 0x1f);
  }
  if ((param_3 & 0xffffffff) != 0) {
    if (iVar13 == 0) {
      lVar19 = 0;
    }
    else {
      iVar15 = *(int *)(param_1 + 8) - iVar13;
      uVar16 = iVar15 / 0x14 + (iVar15 >> 0x1f);
      lVar19 = (longlong)(int)uVar16 + (ulonglong)(uVar16 >> 0x1f);
    }
    uStack00000018 = param_2;
    if ((0xcccccccU - lVar19 & 0xffffffff) < (param_3 & 0xffffffff)) {
      FUN_822bc8f0();
      return;
    }
    if (iVar13 == 0) {
      lVar19 = 0;
    }
    else {
      iVar15 = *(int *)(param_1 + 8) - iVar13;
      uVar16 = iVar15 / 0x14 + (iVar15 >> 0x1f);
      lVar19 = (longlong)(int)uVar16 + (ulonglong)(uVar16 >> 0x1f);
    }
    if ((uVar4 & 0xffffffff) < (lVar19 + param_3 & 0xffffffff)) {
      uVar6 = (uVar4 & 0xffffffff) >> 1;
      uVar17 = 0;
      if ((uVar4 & 0xffffffff) <= (0xccccccc - uVar6 & 0xffffffff)) {
        uVar17 = uVar6 + uVar4;
      }
      if (iVar13 == 0) {
        lVar19 = 0;
      }
      else {
        iVar15 = *(int *)(param_1 + 8) - iVar13;
        uVar16 = iVar15 / 0x14 + (iVar15 >> 0x1f);
        lVar19 = (longlong)(int)uVar16 + (ulonglong)(uVar16 >> 0x1f);
      }
      if ((uVar17 & 0xffffffff) < (lVar19 + param_3 & 0xffffffff)) {
        if (iVar13 == 0) {
          lVar19 = 0;
        }
        else {
          iVar13 = *(int *)(param_1 + 8) - iVar13;
          uVar16 = iVar13 / 0x14 + (iVar13 >> 0x1f);
          lVar19 = (longlong)(int)uVar16 + (ulonglong)(uVar16 >> 0x1f);
        }
        uVar17 = lVar19 + param_3;
      }
      puVar3 = (undefined4 *)FUN_822915a8(uVar17,0);
      uVar18 = uStack00000018 & 0xffffffff;
      uVar6 = (ulonglong)*(uint *)(param_1 + 4);
      uVar4 = uVar6;
      puVar11 = puVar3;
      while (uVar4 != uVar18) {
        if (puVar11 != (undefined4 *)0x0) {
          lVar19 = 5;
          uVar4 = uVar6;
          puVar10 = puVar11;
          do {
            puVar14 = (undefined4 *)uVar4;
            uVar4 = uVar4 + 4;
            *puVar10 = *puVar14;
            puVar10 = puVar10 + 1;
            lVar19 = lVar19 + -1;
          } while (lVar19 != 0);
        }
        uVar6 = uVar6 + 0x14;
        puVar11 = puVar11 + 5;
        uVar4 = uVar6 & 0xffffffff;
      }
      uVar4 = FUN_822f05e0(param_1,puVar11,param_3,auStack_50);
      uVar16 = *(uint *)(param_1 + 8);
      if (uVar18 != uVar16) {
        lVar19 = uVar18 - uVar4;
        do {
          if ((uVar4 & 0xffffffff) != 0) {
            lVar7 = lVar19 + uVar4;
            lVar20 = 5;
            uVar6 = uVar4;
            do {
              puVar11 = (undefined4 *)lVar7;
              lVar7 = lVar7 + 4;
              *(undefined4 *)uVar6 = *puVar11;
              uVar6 = uVar6 + 4;
              lVar20 = lVar20 + -1;
            } while (lVar20 != 0);
          }
          uVar4 = uVar4 + 0x14;
        } while ((lVar19 + uVar4 & 0xffffffff) != (ulonglong)uVar16);
      }
      iVar13 = *(int *)(param_1 + 4);
      if (iVar13 == 0) {
        lVar19 = 0;
      }
      else {
        iVar15 = *(int *)(param_1 + 8) - iVar13;
        uVar16 = iVar15 / 0x14 + (iVar15 >> 0x1f);
        lVar19 = (longlong)(int)uVar16 + (ulonglong)(uVar16 >> 0x1f);
      }
      if (iVar13 != 0) {
        FUN_82142f48();
      }
      *(undefined4 **)(param_1 + 4) = puVar3;
      *(int *)(param_1 + 0xc) =
           (int)((uVar17 + (uVar17 & 0x3fffffff) * 4 & 0xffffffff) << 2) + (int)puVar3;
      *(int *)(param_1 + 8) =
           (int)((lVar19 + param_3 + (lVar19 + param_3 & 0x3fffffff) * 4 & 0xffffffff) << 2) +
           (int)puVar3;
      return;
    }
    uVar16 = *(uint *)(param_1 + 8);
    uVar4 = (ulonglong)uVar16;
    uStack00000018._4_4_ = (int)param_2;
    uVar6 = param_2 & 0xffffffff;
    uVar2 = (int)(uVar16 - uStack00000018._4_4_) / 0x14 +
            ((int)(uVar16 - uStack00000018._4_4_) >> 0x1f);
    if (((longlong)(int)uVar2 + (ulonglong)(uVar2 >> 0x1f) & 0xffffffff) < (param_3 & 0xffffffff)) {
      uVar17 = param_3 + (param_3 & 0x3fffffff) * 4 & 0x3fffffff;
      uVar18 = uVar17 * 4 + uVar6;
      if ((param_2 & 0xffffffff) != uVar4) {
        uVar5 = uVar18 + uVar17 * -4;
        do {
          if ((uVar18 & 0xffffffff) != 0) {
            lVar19 = 5;
            uVar8 = uVar18;
            uVar12 = uVar5;
            do {
              puVar11 = (undefined4 *)uVar12;
              uVar12 = uVar12 + 4;
              *(undefined4 *)uVar8 = *puVar11;
              uVar8 = uVar8 + 4;
              lVar19 = lVar19 + -1;
            } while (lVar19 != 0);
          }
          uVar5 = uVar5 + 0x14;
          uVar18 = uVar18 + 0x14;
        } while ((uVar5 & 0xffffffff) != uVar4);
      }
      iVar13 = *(int *)(param_1 + 8) - uStack00000018._4_4_;
      uVar16 = iVar13 / 0x14 + (iVar13 >> 0x1f);
      FUN_822f05e0(param_1,*(int *)(param_1 + 8),
                   param_3 - ((longlong)(int)uVar16 + (ulonglong)(uVar16 >> 0x1f)),auStack_50);
      lVar19 = uVar17 * 4 + (ulonglong)*(uint *)(param_1 + 8);
      uVar4 = lVar19 + uVar17 * -4;
      *(int *)(param_1 + 8) = (int)lVar19;
      if ((param_2 & 0xffffffff) != (uVar4 & 0xffffffff)) {
        do {
          puVar11 = auStack_50;
          lVar19 = 5;
          uVar17 = uVar6;
          do {
            uVar1 = *puVar11;
            puVar11 = puVar11 + 1;
            *(undefined4 *)uVar17 = uVar1;
            uVar17 = uVar17 + 4;
            lVar19 = lVar19 + -1;
          } while (lVar19 != 0);
          uVar6 = uVar6 + 0x14;
        } while ((uVar6 & 0xffffffff) != (uVar4 & 0xffffffff));
        return;
      }
    }
    else {
      uVar17 = param_3 + (param_3 & 0x3fffffff) * 4 & 0x3fffffff;
      uVar8 = uVar4 + uVar17 * -4;
      uVar18 = uVar4;
      for (uVar5 = uVar8; (uVar5 & 0xffffffff) != uVar4; uVar5 = uVar5 + 0x14) {
        if ((uVar18 & 0xffffffff) != 0) {
          lVar19 = 5;
          uVar12 = uVar18;
          uVar9 = uVar5;
          do {
            puVar11 = (undefined4 *)uVar9;
            uVar9 = uVar9 + 4;
            *(undefined4 *)uVar12 = *puVar11;
            uVar12 = uVar12 + 4;
            lVar19 = lVar19 + -1;
          } while (lVar19 != 0);
        }
        uVar18 = uVar18 + 0x14;
        uVar16 = (uint)uVar18;
      }
      *(uint *)(param_1 + 8) = uVar16;
      FUN_822efa68(uVar6,uVar8,uVar4,uStack_60,uStack_60,0);
      uVar4 = uVar17 * 4 + uVar6;
      if ((param_2 & 0xffffffff) != (uVar4 & 0xffffffff)) {
        do {
          puVar11 = auStack_50;
          lVar19 = 5;
          uVar17 = uVar6;
          do {
            uVar1 = *puVar11;
            puVar11 = puVar11 + 1;
            *(undefined4 *)uVar17 = uVar1;
            uVar17 = uVar17 + 4;
            lVar19 = lVar19 + -1;
          } while (lVar19 != 0);
          uVar6 = uVar6 + 0x14;
        } while ((uVar6 & 0xffffffff) != (uVar4 & 0xffffffff));
      }
    }
  }
  return;
}



// ===================================================
// 822F13F0  ->  FUN_822f13f0  (entree 822f13f0)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_822f13f0(int param_1)

{
  int iVar1;
  int *piVar2;
  int *piVar3;
  
  if (*(int *)(param_1 + 0x910) != 0) {
    FUN_82142f48();
  }
  iVar1 = 5;
  *(undefined4 *)(param_1 + 0x910) = 0;
  *(undefined4 *)(param_1 + 0x914) = 0;
  *(undefined4 *)(param_1 + 0x918) = 0;
  piVar2 = (int *)(param_1 + 0x910);
  do {
    piVar3 = piVar2 + -4;
    if (*piVar3 != 0) {
      FUN_82142f48();
    }
    iVar1 = iVar1 + -1;
    *piVar3 = 0;
    piVar2[-3] = 0;
    piVar2[-2] = 0;
    piVar2 = piVar3;
  } while (-1 < iVar1);
  if (0xf < *(uint *)(param_1 + 0x8a8)) {
    thunk_FUN_82142f48(*(undefined4 *)(param_1 + 0x894));
  }
  *(undefined4 *)(param_1 + 0x8a4) = 0;
  *(undefined4 *)(param_1 + 0x8a8) = 0xf;
  *(undefined1 *)(param_1 + 0x894) = 0;
  FUN_82154d98(param_1 + 0x790);
  FUN_822c73a8(param_1 + 0x734);
  if (*(int *)(param_1 + 0x720) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 0x720) = 0;
  *(undefined4 *)(param_1 + 0x724) = 0;
  *(undefined4 *)(param_1 + 0x728) = 0;
  FUN_822c73a8(param_1 + 0x6b0);
  if (*(int *)(param_1 + 0x6a4) != 0) {
    FUN_82142f48();
  }
  *(undefined4 *)(param_1 + 0x6a4) = 0;
  *(undefined4 *)(param_1 + 0x6a8) = 0;
  *(undefined4 *)(param_1 + 0x6ac) = 0;
  FUN_823a7598(param_1 + 0x65c);
  FUN_823a7598(param_1 + 0x638);
  FUN_823a7598(param_1 + 0x614);
  FUN_823a7598(param_1 + 0x5f0);
  FUN_822c73a8(param_1);
  return;
}



// ===================================================
// 822F1510  ->  FUN_822f1510  (entree 822f1510)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_822f1510(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  char cVar5;
  undefined4 *puVar4;
  longlong lVar6;
  
  iVar1 = *(int *)(param_1 + 0x924);
  if (*(int *)(param_1 + 0x910) == 0) {
    lVar6 = 0;
  }
  else {
    lVar6 = (longlong)(*(int *)(param_1 + 0x914) - *(int *)(param_1 + 0x910) >> 2);
  }
  iVar3 = FUN_822d1868();
  if (-1 < iVar3) {
    *(undefined4 *)(param_1 + 0x88c) = 0;
    *(undefined4 *)(param_1 + 0x888) = 3;
    *(undefined4 *)(param_1 + 0x57c) = 3;
    return;
  }
  iVar3 = FUN_822d1830();
  if (iVar3 < 0) {
    if ((int)lVar6 != 0) {
      cVar5 = FUN_822d0f88((undefined4 *)(param_1 + 0x920),lVar6 + -1,0);
      if (cVar5 != '\0') {
        puVar4 = (undefined4 *)FUN_822ea420(param_1 + 0x90c,*(undefined4 *)(param_1 + 0x920));
        uVar2 = *puVar4;
        *(undefined4 *)(param_1 + 0x928) = 0;
        *(undefined4 *)(param_1 + 0x92c) = 0;
        *(undefined4 *)(param_1 + 0x924) = uVar2;
        FUN_822d1188();
        if (iVar1 < *(int *)(param_1 + 0x924)) {
          FUN_822f65f8(param_1 + 0x65c);
        }
        if (*(int *)(param_1 + 0x924) < iVar1) {
          FUN_822f65f8(param_1 + 0x638);
        }
        if (*(char *)(param_1 + 0x935) != '\0') {
          FUN_82166528(*(undefined4 *)(param_1 + 0x930),*(int *)(param_1 + 0x924) == 5);
        }
      }
    }
    return;
  }
  if ((*(int *)(param_1 + 0x924) == 5) && (*(char *)(param_1 + 0x935) == '\0')) {
    FUN_822b3ac0(0xffffffff820881ec);
    return;
  }
  *(undefined4 *)(param_1 + 0x91c) = 1;
  FUN_822d1198();
  return;
}



// ===================================================
// 822F1658  ->  FUN_822f1658  (entree 822f1658)
// ===================================================

/* WARNING: Function: __savegprlr_21 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_21 replaced with injection: x360_restgprlr */

void FUN_822f1658(void)

{
  undefined1 uVar1;
  undefined4 uVar2;
  int iVar3;
  bool bVar4;
  int iVar6;
  undefined4 *puVar7;
  undefined8 uVar5;
  int iVar8;
  undefined **ppuVar9;
  uint uVar10;
  double dVar11;
  double dVar12;
  double dVar13;
  double dVar14;
  double dVar15;
  double dVar16;
  double dVar17;
  double dVar18;
  undefined *puStack_150;
  undefined *puStack_14c;
  undefined *puStack_148;
  undefined **ppuStack_144;
  undefined4 auStack_140 [24];
  undefined1 auStack_e0 [224];
  
  iVar6 = FUN_826018b8();
  bVar4 = false;
  auStack_140[0] = 0x3b9;
  uVar1 = *(undefined1 *)(iVar6 + 0x148);
  auStack_140[1] = 0x3ba;
  auStack_140[4] = 0x3be;
  auStack_140[2] = 0x3bb;
  auStack_140[5] = 0x3bf;
  auStack_140[3] = 0x3bd;
  auStack_140[6] = 0x3c0;
  auStack_140[7] = 0x3c1;
  auStack_140[8] = 0x3c3;
  auStack_140[9] = 0x3c4;
  auStack_140[10] = 0x3c5;
  auStack_140[0xb] = 0x3ca;
  auStack_140[0xc] = 0x3cb;
  auStack_140[0xd] = 0x3cc;
  auStack_140[0xe] = 0x3cd;
  auStack_140[0xf] = 0x3c6;
  auStack_140[0x10] = 0x3c7;
  auStack_140[0x11] = 0x3cf;
  auStack_140[0x12] = 0x3d0;
  auStack_140[0x13] = 0x3d1;
  auStack_140[0x14] = 0x3d2;
  auStack_140[0x15] = 0x3d3;
  auStack_140[0x16] = 0x3d4;
  auStack_140[0x17] = 0x3c8;
  puVar7 = (undefined4 *)
           FUN_822f0ec0(*(int *)(iVar6 + 0x924) * 0x10 + iVar6 + 0x8ac,
                        *(undefined4 *)(iVar6 + 0x928));
  puStack_150 = DAT_8201180c;
  puStack_14c = (undefined *)DAT_82088098;
  dVar17 = (double)(*(float *)(iVar6 + 0x5ac) + DAT_82015b8c);
  dVar15 = (double)(*(float *)(iVar6 + 0x5a8) + DAT_82015b8c);
  dVar11 = (double)DAT_820636c4;
  dVar16 = (double)(float)(dVar17 + dVar11);
  dVar14 = (double)(float)(dVar16 + dVar11);
  dVar11 = (double)(float)(dVar14 + dVar11);
  if ((*(int *)(iVar6 + 0x91c) != 0) && (*(int *)(iVar6 + 0x924) != 5)) {
    iVar3 = *(int *)(iVar6 + 0x924) * 0x10 + iVar6;
    iVar8 = *(int *)(iVar3 + 0x8b0);
    if (iVar8 != 0) {
      iVar8 = *(int *)(iVar3 + 0x8b4) - iVar8;
      iVar8 = iVar8 / 0x14 + (iVar8 >> 0x1f);
      if (iVar8 != iVar8 >> 0x1f) goto LAB_822f17f4;
    }
  }
  bVar4 = true;
LAB_822f17f4:
  FUN_8223df90(*(undefined8 *)(iVar6 + 0x5a8),CONCAT44(DAT_8201180c,DAT_82088098),9,7,0);
  FUN_8223bc10(0xe);
  FUN_8223c048(0xffffffffffffffff);
  FUN_8223c130(8);
  FUN_8223beb8(dVar15,dVar17);
  FUN_8223c048(0xfffffffffff29600);
  uVar5 = FUN_82322798(0x3e2);
  FUN_8223fe30(0xffffffff82000f08,uVar5);
  dVar13 = (double)DAT_820035f0;
  dVar12 = (double)DAT_82088088;
  FUN_8223beb8((double)(float)((double)*(float *)(iVar6 + 0x5a8) + dVar12),
               (double)(float)(dVar17 + dVar13));
  FUN_8223c048(0xffffffffffffffff);
  if (!bVar4) {
    uVar5 = FUN_82322798(auStack_140[puVar7[1]]);
    FUN_8223fe30(0xffffffff82085944,0xffffffff82000f88,uVar5);
  }
  puStack_150 = &DAT_8200f32c;
  puStack_14c = &DAT_8200f330;
  puStack_148 = &DAT_8200f334;
  ppuStack_144 = &PTR_FUN_8200f338;
  FUN_8223beb8(dVar15,dVar16);
  FUN_8223c048(0xfffffffffff29600);
  uVar5 = FUN_82322798(0x3e3);
  FUN_8223fe30(0xffffffff82000f08,uVar5);
  FUN_8223c048(0xffffffffffffffff);
  if (!bVar4) {
    uVar10 = 0;
    ppuVar9 = &puStack_150;
    dVar16 = (double)DAT_8208bc6c;
    dVar17 = (double)DAT_820647b4;
    dVar18 = (double)DAT_82000f1c;
    do {
      if ((1 << (uVar10 & 0x3f) & puVar7[2]) != 0) {
        FUN_8223beb8((double)(float)((double)uVar10 * dVar18 + dVar17),dVar16);
        FUN_8223fe30(0xffffffff82000f08,*ppuVar9);
      }
      uVar10 = uVar10 + 1;
      ppuVar9 = ppuVar9 + 1;
    } while (uVar10 < 4);
  }
  FUN_8223beb8(dVar15,dVar14);
  FUN_8223c048(0xfffffffffff29600);
  uVar5 = FUN_82322798(0x3e4);
  FUN_8223fe30(0xffffffff82000f08,uVar5);
  FUN_8223beb8((double)(float)((double)*(float *)(iVar6 + 0x5a8) + dVar12),
               (double)(float)(dVar14 + dVar13));
  FUN_8223c048(0xffffffffffffffff);
  if (!bVar4) {
    uVar5 = FUN_82278ac0(uVar1,*puVar7);
    FUN_8223fe30(0xffffffff82088168,0xffffffff82000f88,uVar5);
  }
  uVar2 = *(undefined4 *)(iVar6 + 0x13c);
  FUN_8223beb8(dVar15,dVar11);
  FUN_8223c048(0xfffffffffff29600);
  uVar5 = FUN_82322798(0x3e5);
  FUN_8223fe30(0xffffffff82000f08,uVar5);
  FUN_8223beb8((double)(float)((double)*(float *)(iVar6 + 0x5a8) + dVar12),
               (double)(float)(dVar11 + dVar13));
  FUN_8223c048(0xffffffffffffffff);
  uVar5 = FUN_82322798(999);
  FUN_82249520(auStack_e0,0x40,uVar5,uVar2);
  FUN_8223fe30(0xffffffff82000f80,0xffffffff82000f88,auStack_e0);
  FUN_82601904();
  return;
}



// ===================================================
// 822F1AB8  ->  FUN_822f1ab8  (entree 822f1ab8)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 * FUN_822f1ab8(undefined8 *param_1,int param_2,undefined8 param_3)

{
  undefined8 in_r0;
  int iVar1;
  uint uVar2;
  int iStack00000020;
  int iStack00000024;
  undefined8 uStack_30;
  
  uVar2 = *(uint *)(param_2 + 4);
  if (uVar2 != 0) {
    iVar1 = *(uint *)(param_2 + 8) - uVar2;
    iVar1 = iVar1 / 0x14 + (iVar1 >> 0x1f);
    if (iVar1 != iVar1 >> 0x1f) {
      if (*(uint *)(param_2 + 8) < uVar2) {
        trapWord(0x1f,in_r0,0x16);
      }
      iStack00000020 = (int)((ulonglong)param_3 >> 0x20);
      if ((iStack00000020 == 0) || (iStack00000020 != param_2)) {
        trapWord(0x1f,in_r0,0x16);
      }
      iStack00000024 = (int)param_3;
      iVar1 = (int)(iStack00000024 - uVar2) / 0x14 + ((int)(iStack00000024 - uVar2) >> 0x1f);
      iVar1 = iVar1 - (iVar1 >> 0x1f);
      goto LAB_822f1b4c;
    }
  }
  iVar1 = 0;
LAB_822f1b4c:
  _iStack00000020 = param_3;
  FUN_822f0f90(param_2,param_3,1);
  if (*(uint *)(param_2 + 8) < *(uint *)(param_2 + 4)) {
    trapWord(0x1f,in_r0,0x16);
  }
  uVar2 = iVar1 * 0x14 + *(uint *)(param_2 + 4);
  if ((*(uint *)(param_2 + 8) < uVar2) || (uVar2 < *(uint *)(param_2 + 4))) {
    trapWord(0x1f,in_r0,0x16);
  }
  uStack_30 = CONCAT44(param_2,uVar2);
  *param_1 = uStack_30;
  return param_1;
}



// ===================================================
// 822F1BC0  ->  FUN_822f1bc0  (entree 822f1bc0)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

void FUN_822f1bc0(int param_1)

{
  uint uVar1;
  int iVar3;
  int *piVar4;
  char cVar5;
  undefined8 uVar2;
  int iVar6;
  int iVar7;
  longlong lVar8;
  int iStack_80;
  int iStack_7c;
  undefined1 auStack_70 [4];
  undefined4 ***apppuStack_6c [5];
  uint uStack_58;
  undefined1 auStack_50 [4];
  undefined4 ***apppuStack_4c [5];
  uint uStack_38;
  
  iVar3 = *(int *)(param_1 + 0x924) * 0x10 + param_1;
  iVar7 = *(int *)(iVar3 + 0x8b0);
  if (iVar7 == 0) {
    lVar8 = 0;
  }
  else {
    iVar7 = *(int *)(iVar3 + 0x8b4) - iVar7;
    uVar1 = iVar7 / 0x14 + (iVar7 >> 0x1f);
    lVar8 = (longlong)(int)uVar1 + (ulonglong)(uVar1 >> 0x1f);
  }
  iVar7 = *(int *)(param_1 + 0x92c);
  iVar3 = FUN_822d1868();
  if (-1 < iVar3) {
    *(undefined4 *)(param_1 + 0x91c) = 0;
    FUN_822d11a8();
    return;
  }
  if ((int)lVar8 == 0) {
    return;
  }
  iVar3 = FUN_822d1830();
  if (-1 < iVar3) {
    piVar4 = (int *)FUN_822f0ec0(*(int *)(param_1 + 0x924) * 0x10 + param_1 + 0x8ac,
                                 *(undefined4 *)(param_1 + 0x928));
    if (*(int *)(param_1 + 0x924) == 5) {
      if (*(char *)(param_1 + 0x935) == '\0') {
        return;
      }
      if (*(char *)(param_1 + 0x936) != '\0') goto LAB_822f1d74;
      if ((uint)piVar4[3] <= *(uint *)(param_1 + 0x13c)) {
        uVar2 = FUN_82322798(0x3d5);
        FUN_82141968(auStack_50,uVar2);
        if (uStack_38 < 0x10) {
          apppuStack_4c[0] = apppuStack_4c;
        }
        FUN_822f0e48(param_1,0,apppuStack_4c[0]);
        FUN_821d62d0(auStack_50);
        return;
      }
    }
    else {
      iStack_7c = *piVar4;
      if (iStack_7c == 0) {
        return;
      }
      iStack_80 = param_1 + 0x188;
      cVar5 = FUN_821d1808(&iStack_80);
      if (cVar5 != '\0') {
LAB_822f1d74:
        FUN_822b3ac0(0xffffffff820881ec);
        return;
      }
      if ((uint)piVar4[3] <= *(uint *)(param_1 + 0x13c)) {
        FUN_82279be0(auStack_70,*(undefined1 *)(param_1 + 0x148),*piVar4);
        if (uStack_58 < 0x10) {
          apppuStack_6c[0] = apppuStack_6c;
        }
        FUN_822f0e48(param_1,0,apppuStack_6c[0]);
        FUN_821d62d0(auStack_70);
        return;
      }
    }
    *(undefined4 *)(param_1 + 0x88c) = 0;
    *(undefined4 *)(param_1 + 0x888) = 2;
    *(undefined4 *)(param_1 + 0x57c) = 3;
    return;
  }
  cVar5 = FUN_822d0e18((int *)(param_1 + 0x928),lVar8 + -1,0);
  if (cVar5 == '\0') {
    return;
  }
  FUN_822d1188();
  iVar3 = *(int *)(param_1 + 0x928);
  iVar6 = iVar3 - *(int *)(param_1 + 0x92c);
  if (iVar6 < 5) {
    if (-1 < iVar6) goto LAB_822f1dd4;
  }
  else {
    iVar3 = iVar3 + -4;
  }
  *(int *)(param_1 + 0x92c) = iVar3;
LAB_822f1dd4:
  if (iVar7 < *(int *)(param_1 + 0x92c)) {
    FUN_822f65f8(param_1 + 0x614);
  }
  if (*(int *)(param_1 + 0x92c) < iVar7) {
    FUN_822f65f8(param_1 + 0x5f0);
  }
  return;
}



// ===================================================
// 822F1E08  ->  FUN_822f1e08  (entree 822f1e08)
// ===================================================

/* WARNING: Function: __savegprlr_15 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_15 replaced with injection: x360_restgprlr */

void FUN_822f1e08(void)

{
  undefined1 uVar1;
  uint uVar2;
  undefined4 uVar3;
  int iVar4;
  ulonglong uVar5;
  int iVar8;
  uint *puVar9;
  undefined8 uVar6;
  longlong lVar7;
  int iVar10;
  ulonglong uVar11;
  char cVar12;
  int iVar13;
  int iVar14;
  int iVar15;
  int iVar16;
  double dVar17;
  double dVar18;
  double dVar19;
  double dVar20;
  uint uStack_11c;
  uint uStack_108;
  
  uVar5 = ZEXT48(&stack0x00000000);
  iVar8 = FUN_826018c0();
  uVar1 = *(undefined1 *)(iVar8 + 0x148);
  iVar13 = *(int *)(iVar8 + 0x924) * 0x10 + iVar8;
  iVar10 = *(int *)(iVar13 + 0x8b0);
  if (iVar10 == 0) {
    iVar10 = 0;
  }
  else {
    iVar10 = (*(int *)(iVar13 + 0x8b4) - iVar10) / 0x14;
  }
  iVar13 = -0x14c;
  if (iVar10 < 6) {
    iVar13 = -0x150;
  }
  iVar10 = *(int *)(&stack0x00000000 + iVar13);
  FUN_8223bc10(0xe);
  FUN_8223c130(8);
  if (*(int *)(iVar8 + 0x924) == 5) {
    if (*(char *)(iVar8 + 0x935) != '\0') {
      iVar10 = FUN_822f0ec0(iVar8 + 0x8fc,0);
      dVar17 = (double)DAT_82001bc8;
      FUN_8223beb8((double)(*(float *)(iVar8 + 0x5b4) + DAT_82003a50),
                   (double)(float)((double)*(float *)(iVar8 + 0x5b8) + dVar17));
      if (*(char *)(iVar8 + 0x936) == '\0') {
        if (*(int *)(iVar8 + 0x91c) == 1) {
          uVar6 = 0xffffffffff6cbede;
        }
        else {
          uVar6 = 0xffffffffffffffff;
        }
      }
      else {
        uVar6 = 0xffffffffff7f7f7f;
      }
      FUN_8223c048(uVar6);
      uVar6 = FUN_82322798(0x3d5);
      FUN_8223fe30(0xffffffff82000f08,uVar6);
      FUN_8223beb8((double)(*(float *)(iVar8 + 0x5b4) + DAT_82088160),
                   (double)(*(float *)(iVar8 + 0x5b8) + DAT_8208815c));
      if (*(char *)(iVar8 + 0x936) == '\0') {
        uVar3 = *(undefined4 *)(iVar10 + 0xc);
        uVar6 = FUN_82322798(999);
        FUN_82249520(uVar5 - 0x100,0x40,uVar6,uVar3);
        lVar7 = uVar5 - 0x100;
      }
      else {
        lVar7 = FUN_82322798(0x3e6);
      }
      FUN_8223fe30(0xffffffff82000f80,0xffffffff82010300,lVar7);
      dVar18 = (double)(float)((double)*(float *)(iVar8 + 0x5b8) + dVar17);
      dVar17 = (double)(*(float *)(iVar8 + 0x5b4) + DAT_8200a98c);
      FUN_822c2bc0(dVar17,dVar18,(double)(float)(dVar17 + (double)DAT_82000f18),
                   (double)(float)(dVar18 + (double)DAT_82000f18));
      FUN_8260190c();
      return;
    }
    FUN_8223bec0(uVar5 - 0x130,9);
    uVar6 = 0x3e9;
    if (*(char *)(iVar8 + 0x937) == '\0') {
      uVar6 = 1000;
    }
    uVar6 = FUN_82322798(uVar6);
    FUN_8223fe30(0xffffffff82000f08,uVar6);
  }
  else if (0 < iVar10) {
    dVar17 = (double)DAT_82088160;
    dVar18 = (double)DAT_8208815c;
    dVar19 = (double)DAT_82003a50;
    iVar13 = iVar8 + 0x188;
    dVar20 = (double)DAT_82001bc8;
    iVar15 = 0;
    do {
      iVar14 = iVar15 + *(int *)(iVar8 + 0x92c);
      puVar9 = (uint *)FUN_822f0ec0(*(int *)(iVar8 + 0x924) * 0x10 + iVar8 + 0x8ac,iVar14);
      uVar6 = FUN_82277e08(uVar1,*puVar9);
      if ((int)uVar6 == -1) {
        uVar6 = 0x15;
      }
      iVar4 = iVar15 * 0xc + iVar8;
      iVar16 = (iVar15 + 0x7a) * 0xc;
      FUN_823084e8(uVar6,8,uVar5 - 0x148,0);
      FUN_8223beb8((double)(float)((double)*(float *)(iVar4 + 0x5b4) + dVar19),
                   (double)(float)((double)*(float *)(iVar16 + iVar8) + dVar20));
      uVar2 = *puVar9;
      if (999 < uVar2) {
        FUN_822c5128(iVar13);
      }
      if ((1 << (uVar2 & 0x1f) & *(uint *)((uVar2 >> 3 & 0x1ffffffc) + iVar13)) == 0) {
        if ((iVar14 == *(int *)(iVar8 + 0x928)) && (*(int *)(iVar8 + 0x91c) == 1)) {
          uVar6 = 0xffffffffff6cbede;
        }
        else {
          uVar6 = 0xffffffffffffffff;
        }
      }
      else {
        uVar6 = 0xffffffffff7f7f7f;
      }
      FUN_8223c048(uVar6);
      FUN_82279be0(uVar5 - 0x120,uVar1,*puVar9);
      uVar11 = (ulonglong)uStack_11c;
      if (uStack_108 < 0x10) {
        uVar11 = uVar5 - 0x11c;
      }
      FUN_8223fe30(0xffffffff82000f08,uVar11);
      FUN_8223beb8((double)(float)((double)*(float *)(iVar4 + 0x5b4) + dVar17),
                   (double)(float)((double)*(float *)(iVar16 + iVar8) + dVar18));
      uVar2 = *puVar9;
      if (999 < uVar2) {
        FUN_822c5128(iVar13);
      }
      if ((1 << (uVar2 & 0x1f) & *(uint *)((uVar2 >> 3 & 0x1ffffffc) + iVar13)) == 0) {
        uVar2 = puVar9[3];
        uVar6 = FUN_82322798(999);
        FUN_82249520(uVar5 - 0x100,0x40,uVar6,uVar2);
        lVar7 = uVar5 - 0x100;
      }
      else {
        lVar7 = FUN_82322798(0x3e6);
      }
      FUN_8223fe30(0xffffffff82000f80,0xffffffff82010300,lVar7);
      if (0xf < uStack_108) {
        thunk_FUN_82142f48(uStack_11c);
      }
      cVar12 = (char)iVar15 + '\x01';
      uStack_108 = 0xf;
      iVar15 = (int)cVar12;
      uStack_11c = uStack_11c & 0xffffff;
    } while (cVar12 < iVar10);
    FUN_8260190c();
    return;
  }
  FUN_8260190c();
  return;
}



// ===================================================
// 822F2300  ->  FUN_822f2300  (entree 822f2300)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

void FUN_822f2300(int param_1)

{
  uint uVar1;
  char cVar6;
  int iVar3;
  undefined4 *puVar4;
  undefined8 uVar2;
  undefined4 uVar5;
  byte bVar7;
  int iVar8;
  int iStack_30;
  undefined4 uStack_2c;
  
  uVar1 = *(uint *)(param_1 + 0x88c);
  if (uVar1 != 0) {
    if (uVar1 == 1) {
      iVar3 = FUN_822e2e38(param_1 + 0x790);
      if (iVar3 == -1) {
        return;
      }
      *(undefined4 *)(param_1 + 0x88c) = 2;
      if (iVar3 == 0) {
        if (*(int *)(param_1 + 0x888) == 3) {
          *(undefined4 *)(param_1 + 0x580) = 4;
          return;
        }
        if (*(int *)(param_1 + 0x888) == 0) {
          puVar4 = (undefined4 *)
                   FUN_822f0ec0(*(int *)(param_1 + 0x924) * 0x10 + param_1 + 0x8ac,
                                *(undefined4 *)(param_1 + 0x928));
          if (*(int *)(param_1 + 0x924) == 5) {
            *(undefined1 *)(param_1 + 0x936) = 1;
            *(undefined4 *)(param_1 + 0x180) = 0;
            *(undefined2 *)(param_1 + 0x186) = 0;
            bVar7 = *(char *)(param_1 + 0x184) + 1;
            *(byte *)(param_1 + 0x184) = bVar7;
            if (8 < bVar7) {
              *(undefined1 *)(param_1 + 0x184) = 8;
            }
          }
          else {
            uStack_2c = *puVar4;
            iStack_30 = param_1 + 0x188;
            FUN_821d1798(&iStack_30,1);
            if (*(int *)(param_1 + 0x578) != 0) {
              uStack_2c = *puVar4;
              iStack_30 = *(int *)(param_1 + 0x578);
              FUN_821d1798(&iStack_30,1);
            }
            cVar6 = FUN_82310238(param_1 + 0x50,*(undefined1 *)(param_1 + 0x148),0);
            if (cVar6 != '\0') {
              FUN_822db578(0x12,0xffffffffffffffff);
            }
          }
          iVar3 = puVar4[3];
          *(undefined4 *)(param_1 + 0x888) = 1;
          *(undefined4 *)(param_1 + 0x88c) = 0;
          *(undefined4 *)(param_1 + 0x57c) = 3;
          *(int *)(param_1 + 0x13c) = *(int *)(param_1 + 0x13c) - iVar3;
          return;
        }
      }
      *(undefined4 *)(param_1 + 0x580) = 2;
      return;
    }
    if (2 < uVar1) {
      return;
    }
    cVar6 = FUN_822c80d0(param_1 + 0x790);
    if (cVar6 != '\0') {
      return;
    }
    *(undefined4 *)(param_1 + 0x57c) = *(undefined4 *)(param_1 + 0x580);
    return;
  }
  iVar3 = param_1 + 0x790;
  cVar6 = FUN_822c80d0(iVar3);
  if (cVar6 != '\0') {
    return;
  }
  FUN_822e3c10(iVar3);
  FUN_822c8aa0(iVar3,0xffffffff8208bc88);
  iVar8 = *(int *)(param_1 + 0x888);
  if (iVar8 == 0) {
    FUN_822e2e28(iVar3,1);
    if (*(uint *)(param_1 + 0x8a8) < 0x10) {
      iVar8 = param_1 + 0x894;
    }
    else {
      iVar8 = *(int *)(param_1 + 0x894);
    }
    uVar2 = FUN_82322798(0x5f9);
    FUN_82249520(0xffffffff82ac69b8,0x80,uVar2,iVar8);
    *(undefined **)(param_1 + 0x7f0) = &DAT_82ac69b8;
    FUN_822f0820(iVar3,0xffffffff8208bc78);
    FUN_822f08a0(iVar3,0xffffffff820881ec);
    *(undefined4 *)(param_1 + 0x88c) = 1;
    return;
  }
  if (iVar8 == 1) {
    uVar2 = 0x5fa;
  }
  else if (iVar8 == 2) {
    uVar2 = 0x5fb;
  }
  else {
    if (iVar8 != 3) goto LAB_822f2588;
    FUN_822e2e28(iVar3,1);
    uVar2 = 0x5fc;
  }
  uVar5 = FUN_82322798(uVar2);
  *(undefined4 *)(param_1 + 0x7f0) = uVar5;
LAB_822f2588:
  *(undefined4 *)(param_1 + 0x88c) = 1;
  return;
}



// ===================================================
// 822F2598  ->  FUN_822f2598  (entree 822f2598)
// ===================================================

void FUN_822f2598(int param_1,undefined4 *param_2)

{
  uint uVar1;
  undefined4 *puVar2;
  undefined4 uVar3;
  undefined8 in_r0;
  int iVar4;
  undefined4 *puVar5;
  int iVar6;
  longlong lVar7;
  int iStack_10;
  uint uStack_c;
  
  uVar1 = *(uint *)(param_1 + 4);
  if ((uVar1 != 0) &&
     (iVar4 = *(int *)(param_1 + 8) - uVar1, iVar4 = iVar4 / 0x14 + (iVar4 >> 0x1f),
     iVar6 = *(int *)(param_1 + 0xc) - uVar1, iVar6 = iVar6 / 0x14 + (iVar6 >> 0x1f),
     (uint)(iVar4 - (iVar4 >> 0x1f)) < (uint)(iVar6 - (iVar6 >> 0x1f)))) {
    puVar2 = *(undefined4 **)(param_1 + 8);
    if (puVar2 != (undefined4 *)0x0) {
      lVar7 = 5;
      puVar5 = puVar2;
      do {
        uVar3 = *param_2;
        param_2 = param_2 + 1;
        *puVar5 = uVar3;
        puVar5 = puVar5 + 1;
        lVar7 = lVar7 + -1;
      } while (lVar7 != 0);
    }
    *(undefined4 **)(param_1 + 8) = puVar2 + 5;
    return;
  }
  uStack_c = *(uint *)(param_1 + 8);
  if (uStack_c < uVar1) {
    trapWord(0x1f,in_r0,0x16);
  }
  iStack_10 = param_1;
  FUN_822f1ab8(&iStack_10,param_1,CONCAT44(param_1,uStack_c));
  return;
}



// ===================================================
// 822F27C8  ->  FUN_822f27c8  (entree 822f27c8)
// ===================================================

undefined8 FUN_822f27c8(undefined8 param_1,ulonglong param_2)

{
  FUN_822f13f0();
  if ((param_2 & 1) != 0) {
    FUN_82142f48(param_1);
  }
  return param_1;
}



// ===================================================
// 822F2818  ->  FUN_822f2818  (entree 822f2818)
// ===================================================

/* WARNING: Function: __savegprlr_20 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_20 replaced with injection: x360_restgprlr */
/* WARNING: Removing unreachable block (ram,0x822f2898) */
/* WARNING: Removing unreachable block (ram,0x822f289c) */
/* WARNING: Removing unreachable block (ram,0x822f28ac) */
/* WARNING: Removing unreachable block (ram,0x822f28c0) */
/* WARNING: Removing unreachable block (ram,0x822f291c) */

void FUN_822f2818(int param_1,int param_2)

{
  byte bVar1;
  int iVar2;
  uint uVar3;
  int *piVar4;
  uint uVar5;
  bool bVar6;
  undefined8 in_r0;
  int iVar7;
  char cVar10;
  int iVar8;
  undefined4 *puVar9;
  int *piVar11;
  uint uVar12;
  int iVar13;
  uint *puVar14;
  uint auStack_90 [4];
  int iStack_80;
  uint uStack_7c;
  uint uStack_78;
  int iStack_74;
  uint uStack_70;
  
  puVar14 = (uint *)(param_1 + 0x8b4);
  iVar7 = 6;
  do {
    uVar12 = puVar14[-1];
    if (*puVar14 < uVar12) {
      trapWord(0x1f,in_r0,0x16);
      trapWord(0x1f,in_r0,0x16);
    }
    if (puVar14 == (uint *)0x8) {
      trapWord(0x1f,in_r0,0x16);
    }
    if (uVar12 != *puVar14) {
      *puVar14 = uVar12;
    }
    iVar7 = iVar7 + -1;
    puVar14 = puVar14 + 4;
  } while (iVar7 != 0);
  uVar12 = *(uint *)(param_1 + 0x910);
  if (*(uint *)(param_1 + 0x914) < uVar12) {
    trapWord(0x1f,in_r0,0x16);
    trapWord(0x1f,in_r0,0x16);
  }
  if (uVar12 != *(uint *)(param_1 + 0x914)) {
    *(uint *)(param_1 + 0x914) = uVar12;
  }
  iVar7 = FUN_82276750(param_2);
  if (((iVar7 != 0) && (*(int *)(iVar7 + 8) != 0)) &&
     (piVar4 = (int *)(&PTR_DAT_82655288)[param_2], piVar4 != (int *)0x0)) {
    iVar13 = 0;
    iVar8 = *piVar4;
    piVar11 = piVar4;
    while (iVar8 != 0) {
      iVar8 = *piVar11;
      iVar2 = piVar11[1];
      puVar14 = (uint *)(iVar8 * 0x50 + *(int *)(iVar7 + 8));
      cVar10 = FUN_8227a3a0(param_2,iVar8);
      if (((cVar10 == '\0') && ((*puVar14 & 0x80000000) == 0)) && ((*puVar14 & 1) == 0)) {
        uStack_7c = puVar14[7];
        uStack_70 = puVar14[0x12];
        uVar12 = puVar14[0xe];
        bVar6 = (uVar12 & 1) == 0;
        uStack_78 = (uint)bVar6;
        if ((uVar12 & 2) == 0) {
          uStack_78 = bVar6 | 2;
        }
        if ((uVar12 & 4) == 0) {
          uStack_78 = uStack_78 | 4;
        }
        if ((uVar12 & 8) == 0) {
          uStack_78 = uStack_78 | 8;
        }
        iStack_80 = iVar8;
        iStack_74 = iVar2;
        iVar8 = FUN_82278670(param_2,iVar8);
        FUN_822f2598(iVar8 * 0x10 + param_1 + 0x8ac,&iStack_80);
      }
      iVar13 = iVar13 + 1;
      piVar11 = piVar4 + iVar13 * 2;
      iVar8 = *piVar11;
    }
    puVar14 = (uint *)(param_1 + 0x8b0);
    iVar7 = 6;
    do {
      uVar12 = *puVar14;
      if ((uVar12 != 0) &&
         (uVar3 = puVar14[1], iVar8 = (int)(uVar3 - uVar12) / 0x14 + ((int)(uVar3 - uVar12) >> 0x1f)
         , iVar8 != iVar8 >> 0x1f)) {
        if (uVar3 < uVar12) {
          trapWord(0x1f,in_r0,0x16);
          trapWord(0x1f,in_r0,0x16);
        }
        if (puVar14 == (uint *)0x4) {
          trapWord(0x1f,in_r0,0x16);
        }
        uVar5 = (int)(uVar3 - uVar12) / 0x14 + ((int)(uVar3 - uVar12) >> 0x1f);
        FUN_822f06b8(uVar12,uVar3,(longlong)(int)uVar5 + (ulonglong)(uVar5 >> 0x1f),
                     0xffffffff822ef300);
      }
      iVar7 = iVar7 + -1;
      puVar14 = puVar14 + 4;
    } while (iVar7 != 0);
    iStack_80 = 0;
    uStack_7c = 0;
    uStack_78 = 0;
    iStack_74 = 0;
    uStack_70 = 0;
    if (*(char *)(param_1 + 0x935) != '\0') {
      bVar1 = *(byte *)(param_1 + 0x184);
      uVar12 = (uint)bVar1;
      if (bVar1 == 0) {
        uVar12 = 1;
      }
      else if (6 < bVar1) {
        uVar12 = 7;
      }
      iStack_74 = *(int *)(&DAT_826552dc + uVar12 * 4);
    }
    FUN_822f2598(param_1 + 0x8fc,&iStack_80);
    auStack_90[0] = 0;
    do {
      uVar12 = auStack_90[0];
      iVar8 = auStack_90[0] * 0x10 + param_1;
      iVar7 = *(int *)(iVar8 + 0x8b0);
      if ((iVar7 != 0) &&
         (iVar7 = *(int *)(iVar8 + 0x8b4) - iVar7, iVar7 = iVar7 / 0x14 + (iVar7 >> 0x1f),
         iVar7 != iVar7 >> 0x1f)) {
        FUN_82220058(param_1 + 0x90c,auStack_90);
      }
      auStack_90[0] = uVar12 + 1;
    } while (auStack_90[0] < 6);
    puVar9 = (undefined4 *)FUN_822ea420(param_1 + 0x90c,0);
    *(undefined4 *)(param_1 + 0x924) = *puVar9;
  }
  return;
}



// ===================================================
// 822F2BC8  ->  FUN_822f2bc8  (entree 822f2bc8)
// ===================================================

void FUN_822f2bc8(int param_1)

{
  undefined8 uVar1;
  
  if ((*(int *)(param_1 + 0x584) == 2) && (*(int *)(param_1 + 0x588) != 0)) {
    uVar1 = FUN_822c29e8();
    FUN_822c29d8(2);
    FUN_822c2a08(9);
    FUN_822ef340(param_1);
    FUN_822f1e08(param_1);
    FUN_822f1658(param_1);
    FUN_822c2a18();
    FUN_822c29d8(uVar1);
  }
  return;
}



// ===================================================
// 822F2C50  ->  FUN_822f2c50  (entree 822f2c50)
// ===================================================

void FUN_822f2c50(int param_1)

{
  int iVar1;
  
  iVar1 = *(int *)(param_1 + 0x91c);
  if (iVar1 == 0) {
    FUN_822f1510(param_1);
  }
  else if (iVar1 == 1) {
    FUN_822f1bc0();
  }
  if (iVar1 != *(int *)(param_1 + 0x91c)) {
    FUN_822fb5b8(param_1 + 0x58c);
  }
  return;
}



// ===================================================
// 822F2CB8  ->  FUN_822f2cb8  (entree 822f2cb8)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_822f2cb8(int param_1)

{
  char cVar2;
  undefined4 uVar1;
  undefined8 uVar3;
  int iVar4;
  undefined4 uStack_70;
  undefined4 uStack_6c;
  undefined4 uStack_68;
  undefined4 uStack_60;
  undefined4 uStack_5c;
  undefined4 uStack_58;
  undefined4 uStack_50;
  undefined4 uStack_4c;
  undefined4 uStack_48;
  undefined4 uStack_40;
  undefined4 uStack_3c;
  undefined4 uStack_38;
  undefined4 uStack_30;
  undefined4 uStack_2c;
  undefined4 uStack_28;
  
  uVar3 = 0;
  switch(*(undefined4 *)(param_1 + 0x57c)) {
  case 0:
    cVar2 = FUN_822ef430(param_1);
    if (cVar2 == '\0') {
      FUN_822f2818(param_1,*(undefined1 *)(param_1 + 0x148));
      iVar4 = param_1 + 0x684;
      FUN_822e3ad8(iVar4);
      FUN_821dc9b8(iVar4,6);
      FUN_822e3778(iVar4,0x1b,0);
      FUN_822e2f20(param_1 + 0x6b0);
      FUN_822c8aa0(param_1 + 0x6b0,0xffffffff8208bd5c);
      *(undefined1 *)(param_1 + 0x731) = 0;
      FUN_822e2e98(param_1 + 0x734);
      FUN_822c8aa0(param_1 + 0x734,0xffffffff8208bd40);
      *(undefined1 *)(param_1 + 0x789) = 0;
      *(undefined4 *)(param_1 + 0x57c) = 1;
    }
    break;
  case 1:
    iVar4 = param_1 + 0x684;
    cVar2 = FUN_822e2dd8(iVar4);
    if (cVar2 != '\0') {
      FUN_822e39c0(iVar4,param_1 + 0x590,0xffffffff82088330,1);
      FUN_822e39c0(iVar4,param_1 + 0x59c,0xffffffff82088344,1);
      FUN_822e39c0(iVar4,param_1 + 0x5a8,0xffffffff8208bd24,1);
      FUN_822e39c0(iVar4,param_1 + 0x5b4,0xffffffff820882e8,1);
      FUN_822e39c0(iVar4,param_1 + 0x5c0,0xffffffff820882d4,1);
      FUN_822e39c0(iVar4,param_1 + 0x5cc,0xffffffff820882c0,1);
      FUN_822e39c0(iVar4,param_1 + 0x5d8,0xffffffff820882ac,1);
      FUN_822e39c0(iVar4,param_1 + 0x5e4,0xffffffff82088298,1);
      uStack_70 = DAT_82000a34;
      uStack_6c = DAT_82000a34;
      uStack_68 = DAT_82000a34;
      FUN_822e39c0(iVar4,&uStack_70,0xffffffff8208bd0c,1);
      uStack_60 = uStack_70;
      uStack_5c = uStack_6c;
      uStack_58 = uStack_68;
      FUN_822f66f0(param_1 + 0x5f0,0,7,&uStack_60);
      FUN_822e39c0(iVar4,&uStack_70,0xffffffff8208bcf4,1);
      uStack_50 = uStack_70;
      uStack_4c = uStack_6c;
      uStack_48 = uStack_68;
      FUN_822f66f0(param_1 + 0x614,1,7,&uStack_50);
      FUN_822e39c0(iVar4,&uStack_70,0xffffffff8208bcdc,1);
      uStack_40 = uStack_70;
      uStack_3c = uStack_6c;
      uStack_38 = uStack_68;
      FUN_822f66f0(param_1 + 0x638,2,7,&uStack_40);
      FUN_822e39c0(iVar4,&uStack_70,0xffffffff8208bcc0,1);
      uStack_30 = uStack_70;
      uStack_2c = uStack_6c;
      uStack_28 = uStack_68;
      FUN_822f66f0(param_1 + 0x65c,3,7,&uStack_30);
      *(undefined4 *)(param_1 + 0x588) = 1;
      *(undefined4 *)(param_1 + 0x57c) = 2;
    }
    break;
  case 2:
    FUN_822f2c50(param_1);
    break;
  case 3:
    FUN_822f2300(param_1);
    break;
  case 4:
    iVar4 = param_1 + 0x684;
    cVar2 = FUN_822e2dd8(iVar4);
    if (cVar2 != '\0') {
      FUN_822fb5b8(param_1 + 0x58c);
      FUN_822fb5b8(param_1 + 0x930);
      FUN_822f6578(param_1 + 0x5f0);
      FUN_822f6578(param_1 + 0x614);
      FUN_822f6578(param_1 + 0x638);
      FUN_822f6578(param_1 + 0x65c);
      *(undefined4 *)(param_1 + 0x588) = 0;
      FUN_822e37b8(iVar4);
    }
    cVar2 = FUN_822e2df0(iVar4);
    if (cVar2 == '\0') break;
  default:
    uVar3 = 1;
  }
  FUN_822e4d70(param_1 + 0x684);
  FUN_822ef740(param_1);
  uVar1 = FUN_82322798(0x123);
  *(undefined4 *)(param_1 + 0x6fc) = uVar1;
  uVar1 = FUN_82322798(3);
  *(undefined4 *)(param_1 + 0x780) = uVar1;
  return uVar3;
}



// ===================================================
// 8252E750  ->  FUN_8252e750  (entree 8252e750)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

ulonglong FUN_8252e750(undefined4 param_1,int param_2,undefined4 param_3,ulonglong param_4,
                      int param_5,uint *param_6,undefined4 param_7,ulonglong param_8)

{
  ulonglong uVar1;
  int iVar3;
  longlong lVar2;
  int *piVar4;
  uint uVar5;
  undefined4 uStack_60;
  int iStack_5c;
  undefined4 uStack_58;
  int iStack_54;
  int iStack_50;
  uint uStack_4c;
  undefined4 uStack_48;
  
  iStack_54 = (int)param_4;
  uVar5 = (param_2 * 0x34 + 0x10) * iStack_54 + 8;
  if ((param_4 & 0xffffffff) != 0) {
    piVar4 = (int *)(param_5 + 4);
    do {
      iVar3 = *piVar4;
      param_4 = param_4 - 1;
      piVar4 = piVar4 + 0x22;
      uVar5 = param_2 * iVar3 * 0x1c + uVar5;
    } while (param_4 != 0);
  }
  uStack_4c = *param_6;
  if (uStack_4c < uVar5) {
    uVar1 = 0x7a;
    *param_6 = uVar5;
  }
  else {
    uStack_60 = param_1;
    iStack_5c = param_2;
    uStack_58 = param_3;
    iStack_50 = param_5;
    uStack_48 = param_7;
    iVar3 = FUN_8262f15c(0xfb,0xb0021,param_8,&uStack_60,0x1c);
    if (iVar3 < 0) {
      uVar1 = 0x65b;
    }
    else if ((param_8 & 0xffffffff) == 0) {
      lVar2 = FUN_8253ba78();
      uVar1 = -(ulonglong)(lVar2 != 0) & 0x65b;
    }
    else {
      uVar1 = 0x3e5;
    }
  }
  return uVar1;
}



// ===================================================
// 8252E838  ->  FUN_8252e838  (entree 8252e838)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

void FUN_8252e838(undefined8 param_1,undefined4 param_2,undefined8 param_3,undefined8 param_4,
                 undefined8 param_5,undefined8 param_6,undefined8 param_7)

{
  int iVar1;
  
  iVar1 = FUN_8253ba98();
  if (iVar1 == 0) {
    FUN_8262f1bc(param_1,1,param_2,param_3,param_4,param_5,param_6,param_7);
  }
  return;
}



// ===================================================
// 8252E898  ->  FUN_8252e898  (entree 8252e898)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

void FUN_8252e898(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                 undefined8 param_5,undefined8 param_6,undefined8 param_7)

{
  int iVar1;
  
  iVar1 = FUN_8253ba98();
  if (iVar1 == 0) {
    FUN_8262f1bc(param_1,0,param_2,param_3,param_4,param_5,param_6,param_7);
  }
  return;
}



// ===================================================
// 82547370  ->  FUN_82547370  (entree 82547370)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

ulonglong FUN_82547370(undefined4 param_1,undefined8 param_2,undefined4 param_3,undefined8 param_4,
                      undefined8 param_5,undefined8 param_6,int param_7)

{
  int iVar1;
  ulonglong uVar2;
  ulonglong uVar3;
  longlong lVar4;
  undefined4 uStack00000014;
  undefined4 uStack00000024;
  uint uStack_2a0;
  uint uStack_29c;
  int iStack_298;
  int iStack_294;
  undefined4 uStack_290;
  undefined4 uStack_28c;
  undefined4 uStack_288;
  int iStack_284;
  undefined1 auStack_280 [8];
  undefined8 uStack_278;
  undefined8 uStack_270;
  undefined8 uStack_268;
  undefined8 uStack_260;
  undefined1 auStack_250 [512];
  undefined4 uStack_50;
  
  uStack_50 = 0;
  iStack_298 = 0;
  uStack_29c = 0;
  uStack00000014 = param_1;
  uStack00000024 = param_3;
  iVar1 = FUN_82547d58(0xd01,&uStack_2a0);
  if ((-1 < iVar1) && (iVar1 = FUN_82547de0(uStack_2a0,0,2,0,&uStack_29c,0,0), -1 < iVar1)) {
    uVar2 = (ulonglong)uStack_29c;
    iVar1 = FUN_82547d58(0xc01,&uStack_2a0);
    if ((-1 < iVar1) && (iVar1 = FUN_82547de0(uStack_2a0,0,2,0,&uStack_29c,0,0), -1 < iVar1)) {
      uVar3 = (ulonglong)uStack_29c;
      iVar1 = FUN_82547d58(0xe01,&uStack_2a0);
      if ((-1 < iVar1) && (iVar1 = FUN_82547de0(uStack_2a0,0,3,0x100,&uStack_29c,0,0), -1 < iVar1))
      {
        lVar4 = uVar2 + 0x1c0 + uVar3 + (ulonglong)uStack_29c;
        iVar1 = FUN_82547d58(0xe11,&uStack_2a0);
        if ((-1 < iVar1) &&
           ((iVar1 = FUN_82547de0(uStack_2a0,5,0,lVar4,&uStack_29c,0,0), -1 < iVar1 &&
            (iVar1 = FUN_8262fd7c(0,uStack_29c,&iStack_298), -1 < iVar1)))) {
          iStack_284 = FUN_82600518(param_2);
          iStack_284 = iStack_284 + 1;
          uStack_28c = (undefined4)param_4;
          iVar1 = FUN_82547e80(0xe11,uStack_2a0,5,lVar4,iStack_298,uStack_29c,param_6,param_5);
          if (-1 < iVar1) {
            FUN_82547210(auStack_250,&stack0x00000014);
            FUN_82547210(auStack_250,param_2);
            FUN_82547210(auStack_250,&stack0x00000024);
            FUN_82547210(auStack_250,param_4);
            FUN_82547210(auStack_250,&iStack_284);
            FUN_82547210(auStack_250,&uStack_28c);
            iVar1 = FUN_82547f68(0,0,uStack_2a0,5,0,auStack_250,uStack_288,&uStack_290);
            if (-1 < iVar1) {
              *(undefined4 *)(iStack_294 + 0x1c) = uStack_290;
              uStack_278 = 0;
              uStack_270 = 0;
              uStack_268 = 0;
              uStack_260 = 0;
              iVar1 = FUN_8262f15c(0xfc,uStack_2a0 & 0xffff | 0x50000,param_7,auStack_280,0x28);
              if (-1 < iVar1) {
                if (param_7 != 0) {
                  return 0x3e5;
                }
                lVar4 = FUN_8253ba78();
                return -(ulonglong)(lVar4 != 0) & 0x65b;
              }
            }
          }
        }
      }
    }
  }
  if (param_7 == 0) {
    FUN_8253ba28();
  }
  else {
    *(int *)(param_7 + 0x18) = iVar1;
  }
  if (iStack_298 != 0) {
    FUN_8262fd6c();
  }
  return 0x65b;
}



// ===================================================
// 82547650  ->  FUN_82547650  (entree 82547650)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

ulonglong FUN_82547650(undefined4 param_1,undefined8 param_2,undefined4 param_3,undefined8 param_4,
                      int param_5)

{
  int iVar1;
  ulonglong uVar2;
  longlong lVar3;
  undefined4 uStack00000014;
  undefined4 uStack00000024;
  uint uStack_290;
  uint uStack_28c;
  int iStack_288;
  int iStack_284;
  undefined4 uStack_280;
  undefined4 uStack_27c;
  undefined4 uStack_278;
  int iStack_274;
  undefined1 auStack_270 [8];
  undefined8 uStack_268;
  undefined8 uStack_260;
  undefined8 uStack_258;
  undefined8 uStack_250;
  undefined1 auStack_240 [512];
  undefined4 uStack_40;
  
  uStack_40 = 0;
  iStack_288 = 0;
  uStack_28c = 0;
  uStack00000014 = param_1;
  uStack00000024 = param_3;
  iVar1 = FUN_82547d58(0xd01,&uStack_290);
  if ((-1 < iVar1) && (iVar1 = FUN_82547de0(uStack_290,0,2,0,&uStack_28c,0,0), -1 < iVar1)) {
    uVar2 = (ulonglong)uStack_28c;
    iVar1 = FUN_82547d58(0xe02,&uStack_290);
    if ((-1 < iVar1) && (iVar1 = FUN_82547de0(uStack_290,0,3,0x100,&uStack_28c,0,0), -1 < iVar1)) {
      lVar3 = uVar2 + 0x30 + (ulonglong)uStack_28c;
      iVar1 = FUN_82547d58(0xe13,&uStack_290);
      if (((-1 < iVar1) && (iVar1 = FUN_82547de0(uStack_290,5,0,lVar3,&uStack_28c,0,0), -1 < iVar1))
         && (iVar1 = FUN_8262fd7c(0,uStack_28c,&iStack_288), -1 < iVar1)) {
        iStack_274 = FUN_82600518(param_2);
        iStack_274 = iStack_274 + 1;
        uStack_27c = (undefined4)param_4;
        iVar1 = FUN_82547e80(0xe13,uStack_290,5,lVar3,iStack_288,uStack_28c,0,0);
        if (-1 < iVar1) {
          FUN_82547210(auStack_240,&stack0x00000014);
          FUN_82547210(auStack_240,param_2);
          FUN_82547210(auStack_240,&stack0x00000024);
          FUN_82547210(auStack_240,param_4);
          FUN_82547210(auStack_240,&iStack_274);
          FUN_82547210(auStack_240,&uStack_27c);
          iVar1 = FUN_82547f68(0,0,uStack_290,5,0,auStack_240,uStack_278,&uStack_280);
          if (-1 < iVar1) {
            *(undefined4 *)(iStack_284 + 0x1c) = uStack_280;
            uStack_268 = 0;
            uStack_260 = 0;
            uStack_258 = 0;
            uStack_250 = 0;
            iVar1 = FUN_8262f15c(0xfc,uStack_290 & 0xffff | 0x50000,param_5,auStack_270,0x28);
            if (-1 < iVar1) {
              if (param_5 != 0) {
                return 0x3e5;
              }
              lVar3 = FUN_8253ba78();
              return -(ulonglong)(lVar3 != 0) & 0x65b;
            }
          }
        }
      }
    }
  }
  if (param_5 == 0) {
    FUN_8253ba28();
  }
  else {
    *(int *)(param_5 + 0x18) = iVar1;
  }
  if (iStack_288 != 0) {
    FUN_8262fd6c();
  }
  return 0x65b;
}



// ===================================================
// 825478E8  ->  FUN_825478e8  (entree 825478e8)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

ulonglong FUN_825478e8(undefined4 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                      int param_5)

{
  int iVar2;
  longlong lVar1;
  undefined4 uStack00000014;
  uint uStack_290;
  undefined4 uStack_28c;
  int iStack_288;
  int iStack_284;
  undefined4 uStack_280;
  undefined4 uStack_27c;
  undefined4 auStack_278 [2];
  undefined1 auStack_270 [8];
  undefined8 uStack_268;
  undefined8 uStack_260;
  undefined8 uStack_258;
  undefined8 uStack_250;
  undefined1 auStack_240 [512];
  undefined4 uStack_40;
  
  uStack_40 = 0;
  iStack_288 = 0;
  uStack_28c = 0;
  uStack00000014 = param_1;
  iVar2 = FUN_82547d58(0x704,&uStack_290);
  if (((-1 < iVar2) && (iVar2 = FUN_82547de0(uStack_290,0,0,0,&uStack_28c,0,0), -1 < iVar2)) &&
     (iVar2 = FUN_8262fd7c(0,uStack_28c,&iStack_288), -1 < iVar2)) {
    auStack_278[0] = FUN_8262fd8c(7);
    iVar2 = FUN_82547e80(0x704,uStack_290,0,0,iStack_288,uStack_28c,param_4,param_3);
    if (-1 < iVar2) {
      FUN_82547210(auStack_240,&stack0x00000014);
      FUN_82547210(auStack_240,param_2);
      FUN_82547210(auStack_240,auStack_278);
      iVar2 = FUN_82547f68(0,0,uStack_290,0,0,auStack_240,uStack_27c,&uStack_280);
      if (-1 < iVar2) {
        *(undefined4 *)(iStack_284 + 0x1c) = uStack_280;
        uStack_268 = 0;
        uStack_260 = 0;
        uStack_258 = 0;
        uStack_250 = 0;
        iVar2 = FUN_8262f15c(0xfc,uStack_290 & 0xffff | 0x50000,param_5,auStack_270,0x28);
        if (-1 < iVar2) {
          if (param_5 != 0) {
            return 0x3e5;
          }
          lVar1 = FUN_8253ba78();
          return -(ulonglong)(lVar1 != 0) & 0x65b;
        }
      }
    }
  }
  if (param_5 == 0) {
    FUN_8253ba28();
  }
  else {
    *(int *)(param_5 + 0x18) = iVar2;
  }
  if (iStack_288 != 0) {
    FUN_8262fd6c();
  }
  return 0x65b;
}



// ===================================================
// 82547AC8  ->  FUN_82547ac8  (entree 82547ac8)
// ===================================================

undefined8
FUN_82547ac8(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
            undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  int iVar2;
  undefined8 uVar1;
  undefined4 auStack_40 [2];
  undefined8 uStack_38;
  undefined4 uStack_30;
  undefined4 uStack_2c;
  undefined4 uStack_28;
  undefined4 uStack_24;
  undefined4 uStack_20;
  undefined4 uStack_1c;
  
  uStack_38 = 0;
  auStack_40[0] = param_1;
  uStack_30 = param_2;
  uStack_2c = param_3;
  uStack_28 = param_4;
  uStack_24 = param_5;
  uStack_20 = param_6;
  uStack_1c = param_7;
  iVar2 = FUN_8262fd5c(0xfc,0x58035,auStack_40,0);
  if (iVar2 < 0) {
    if (iVar2 == -0x7ff8ffa9) {
      uVar1 = 0x57;
    }
    else {
      uVar1 = 0x7a;
      if (iVar2 != -0x7ff8ff86) {
        uVar1 = 0x65b;
      }
    }
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}



// ===================================================
// 82547B80  ->  FUN_82547b80  (entree 82547b80)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8
FUN_82547b80(undefined8 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
            undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  int iVar2;
  undefined8 uVar1;
  undefined4 auStack_50 [2];
  undefined8 uStack_48;
  undefined4 uStack_40;
  undefined4 uStack_3c;
  undefined4 uStack_38;
  undefined4 uStack_34;
  undefined4 uStack_30;
  undefined4 uStack_2c;
  
  auStack_50[0] = 0xfe;
  uStack_48 = param_1;
  uStack_40 = param_2;
  uStack_3c = param_3;
  uStack_38 = param_4;
  uStack_34 = param_5;
  uStack_30 = param_6;
  uStack_2c = param_7;
  iVar2 = FUN_8262fd5c(0xfc,0x58035,auStack_50,0);
  if (iVar2 < 0) {
    if (iVar2 == -0x7ff8ffa9) {
      uVar1 = 0x57;
    }
    else {
      uVar1 = 0x7a;
      if (iVar2 != -0x7ff8ff86) {
        uVar1 = 0x65b;
      }
    }
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}



// ===================================================
// 82547F68  ->  FUN_82547f68  (entree 82547f68)
// ===================================================

/* WARNING: Function: __savegprlr_24 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_24 replaced with injection: x360_restgprlr */

longlong FUN_82547f68(int param_1,uint param_2,undefined8 param_3,ulonglong param_4,
                     undefined8 param_5,undefined8 param_6,undefined8 param_7,undefined4 *param_8)

{
  longlong lVar1;
  int aiStack_50 [20];
  
  aiStack_50[0] = 0;
  if (param_2 < 0x440) {
    if (param_1 != 0) {
      return -0x7ff8ff86;
    }
    lVar1 = FUN_8262fd7c(0,0x440,aiStack_50);
    param_1 = aiStack_50[0];
    if (lVar1 < 0) goto LAB_82548020;
  }
  lVar1 = FUN_82548790(param_1,0xffffffff82ccdb48,param_3,param_5,param_6,param_7,*param_8,
                       (~param_4 & 0xffffffff) >> 2 & 1);
  if ((-1 < lVar1) && (lVar1 = FUN_825490a0(param_1), -1 < lVar1)) {
    *param_8 = *(undefined4 *)(param_1 + 0x14);
  }
LAB_82548020:
  if (aiStack_50[0] != 0) {
    FUN_8262fd6c();
  }
  return lVar1;
}



// ===================================================
// 82548638  ->  FUN_82548638  (entree 82548638)
// ===================================================

/* WARNING: Function: __savegprlr_28 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_28 replaced with injection: x360_restgprlr */

longlong FUN_82548638(int param_1,int param_2,undefined8 param_3,int param_4)

{
  longlong lVar1;
  undefined2 uStack_40;
  undefined2 uStack_3e;
  uint uStack_3c;
  uint uStack_38;
  
  *(int *)(param_1 + 0x14) = param_2;
  lVar1 = FUN_825484d8(param_2,param_3,&uStack_40);
  if (-1 < lVar1) {
    if (param_4 != 0) {
      uStack_3e = uStack_40;
      uStack_38 = uStack_3c;
    }
    lVar1 = 0;
    FUN_825490d0(param_1,(ulonglong)*(uint *)(param_2 + 0x34) + (ulonglong)uStack_38,uStack_3e,
                 uStack_3e,1);
  }
  return lVar1;
}



// ===================================================
// 82548790  ->  FUN_82548790  (entree 82548790)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

longlong FUN_82548790(undefined4 *param_1,undefined8 param_2,undefined8 param_3,undefined4 param_4,
                     undefined4 param_5,undefined8 param_6,undefined8 param_7,undefined8 param_8)

{
  longlong lVar1;
  longlong lVar2;
  
  *param_1 = (int)param_2;
  param_1[1] = param_5;
  lVar1 = FUN_82548638(param_1 + 7,param_2,param_3,1);
  if (lVar1 < 0) {
    *param_1 = 0;
    param_1[1] = 0;
    param_1[7] = 0;
    param_1[8] = 0;
    param_1[9] = 0;
    param_1[10] = 0;
    param_1[2] = 0;
    param_1[3] = 0;
    param_1[4] = 0;
    param_1[5] = 0;
    param_1[0x10e] = 0;
  }
  else {
    param_1[0x10e] = param_4;
    FUN_825490d0(param_1 + 2,param_6,param_7,param_7,param_8);
    param_1 = param_1 + 0xe;
    lVar2 = 0x40;
    do {
      *param_1 = 0;
      lVar2 = lVar2 + -1;
      param_1[1] = 0;
      *(undefined8 *)(param_1 + 2) = 0;
      param_1 = param_1 + 4;
    } while (lVar2 != 0);
  }
  return lVar1;
}



// ===================================================
// 825490A0  ->  FUN_825490a0  (entree 825490a0)
// ===================================================

void FUN_825490a0(undefined8 param_1)

{
  undefined4 auStack_10 [4];
  
  auStack_10[0] = 0;
  FUN_825488d8(param_1,0,auStack_10);
  return;
}



