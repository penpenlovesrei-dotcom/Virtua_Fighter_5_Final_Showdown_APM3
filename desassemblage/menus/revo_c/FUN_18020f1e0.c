/* FUN_18020f1e0  --  VF5FS+0x20f1e0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18020f1e0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined8 FUN_18020f1e0(longlong param_1)

{
  bool bVar1;
  char cVar2;
  byte bVar3;
  int iVar4;
  undefined4 uVar5;
  undefined8 uVar6;
  longlong *plVar7;
  longlong lVar8;
  longlong lVar9;
  char *pcVar10;
  undefined4 local_28 [4];
  
  cVar2 = FUN_1801cf0c0();
  if (cVar2 == '\0') {
    return 0;
  }
  if ((DAT_180c8df28 == 0) || (*(longlong *)(DAT_180c8df28 + 0x1ff08) == 0)) {
    FUN_1801e1640(param_1,1);
    FUN_1801e1650(param_1,10);
    FUN_1801e15b0(param_1,1);
    FUN_1801dfbc0(param_1);
    *(undefined4 *)(param_1 + 0x214) = 9;
    *(undefined1 *)(param_1 + 0x218) = 0;
    FUN_1801b3a20(2);
    *(undefined8 *)(param_1 + 0x5fa) = 0;
    *(undefined2 *)(param_1 + 0x602) = 0;
    cVar2 = FUN_18000ba20();
    if (cVar2 != '\0') {
      *(undefined1 *)(param_1 + 0x5fe) = 1;
      *(undefined2 *)(param_1 + 0x5fb) = 0x101;
    }
    *(undefined1 *)(param_1 + 0x603) = 2;
    *(undefined1 *)(param_1 + 0x600) = 2;
    *(undefined4 *)(param_1 + 0x5f0) = 0;
    FUN_1801dfb30(param_1 + 0x230);
    FUN_1801dfb30(param_1 + 0x280);
    FUN_1801dfb30(param_1 + 0x2d0);
    *(undefined1 *)(param_1 + 0x5f4) = 0;
    *(undefined2 *)(param_1 + 0x5f8) = 0;
    if (*(char *)(param_1 + 0x5f7) != '\0') {
      FUN_1801cfd80(1,0xffffffff);
    }
    *(undefined1 *)(param_1 + 0x5f7) = 0;
    *(undefined8 *)(param_1 + 0x608) = 0;
    bVar1 = true;
    cVar2 = FUN_18000ba20(0xffffffff);
    if (cVar2 != '\0') {
      uVar5 = FUN_18000ba10();
      cVar2 = FUN_18000ba20(uVar5);
      if (cVar2 == '\0') {
        FUN_1800e1b00(0);
        FUN_1800e1b20(5);
LAB_18020f8b1:
        *(undefined1 *)(param_1 + 0x5f9) = 1;
        FUN_1802ccb60(param_1);
        return 1;
      }
      cVar2 = FUN_18000ba20();
      if (cVar2 == '\0') {
        cVar2 = thunk_FUN_1802c5110();
        if ((cVar2 != '\0') && (cVar2 = FUN_18000ba20(), cVar2 == '\0')) {
          *(undefined4 *)(DAT_18079b168 + 0x58) = 1;
          *(undefined1 *)(DAT_18079b168 + 0x60) = 1;
          FUN_1800e1b00(8);
          FUN_180210c40(DAT_18079b160,0);
          *(undefined4 *)(DAT_18079b160 + 0x58) = 2;
          *(undefined1 *)(DAT_18079b168 + 0x60) = 1;
          goto LAB_18020f8b1;
        }
        _guard_check_icall();
        FUN_180210c40(DAT_18079b160,0);
        *(undefined4 *)(DAT_18079b160 + 0x58) = 2;
        *(undefined1 *)(DAT_18079b168 + 0x60) = 1;
      }
      else {
        uVar6 = FUN_1801bc1a0(0,0);
        *(undefined8 *)(param_1 + 0x608) = uVar6;
        bVar1 = false;
      }
    }
    FUN_1801a3f20(&DAT_1807956d0);
    FUN_1801e16c0(param_1 + 0x230,7);
    FUN_1801e0470(param_1 + 0x230,0x2b);
    FUN_1801e16c0(param_1 + 0x280,1);
    FUN_1801e0470(param_1 + 0x280,0x2a);
    FUN_1801e16c0(param_1 + 0x2d0,0x19);
    FUN_1801e0470(param_1 + 0x2d0,0x2c);
    uVar5 = FUN_180025eb0(0x2a3,"bg_base",1,0x10000,"neu_s","neu_e");
    *(undefined4 *)(param_1 + 0x5f0) = uVar5;
    if (*(longlong *)(param_1 + 0x608) == 0) {
      if (*(char *)(DAT_18079b168 + 0x60) == '\0') {
        if (((((*(char *)(param_1 + 0x670) == '\0') && (*(char *)(param_1 + 0x950) == '\0')) &&
             (*(char *)(param_1 + 0xde8) == '\0')) &&
            ((*(char *)(param_1 + 0x1078) == '\0' && (iVar4 = FUN_1801b5750(), iVar4 != 2)))) &&
           (iVar4 = FUN_1801b5790(), iVar4 != 2)) {
          lVar9 = param_1 + 0x1878;
          if (*(char *)(param_1 + 0x18d8) == '\0') {
            if (((*(char *)(param_1 + 0x1c00) == '\0') && (*(char *)(param_1 + 0x1ee0) == '\0')) &&
               (cVar2 = FUN_1802603d0(), cVar2 == '\0')) {
              if ((((*(char *)(param_1 + 0x21f8) == '\0') && (iVar4 = FUN_1801fb550(), iVar4 != 2))
                  && (cVar2 = FUN_1801f0460(), cVar2 == '\0')) &&
                 ((*(char *)(param_1 + 0x24d8) == '\0' && (*(char *)(param_1 + 0x274a) == '\0')))) {
                if (*(char *)(param_1 + 0x5f5) == '\0') {
                  if (*(char *)(param_1 + 0x5f6) != '\0') {
                    uVar6 = FUN_1801bb3a0(0,0,0);
                    *(undefined8 *)(param_1 + 0x608) = uVar6;
                  }
                }
                else {
                  uVar6 = FUN_1801c0100(0,0,0);
                  *(undefined8 *)(param_1 + 0x608) = uVar6;
                }
                goto LAB_18020fac7;
              }
              lVar9 = param_1 + 0x2198;
              pcVar10 = "TERMINAL MENU";
            }
            else {
              lVar9 = param_1 + 0x1ba0;
              cVar2 = FUN_18000ba20();
              if (cVar2 != '\0') {
                FUN_180210d20(lVar9);
                goto LAB_18020fa6f;
              }
              pcVar10 = "TRAINING MENU";
            }
          }
          else {
            pcVar10 = "VERSUS MENU";
          }
        }
        else {
          lVar9 = param_1 + 0x610;
          cVar2 = FUN_18000ba20();
          if (cVar2 != '\0') {
            FUN_180210bd0(lVar9);
LAB_18020fa6f:
            uVar6 = FUN_1801bc1a0(0,0);
            *(undefined8 *)(param_1 + 0x608) = uVar6;
            *(undefined2 *)(param_1 + 0x5f5) = 0;
            return 1;
          }
          pcVar10 = "ARCADE MENU";
        }
        cVar2 = FUN_1802cd400(lVar9,pcVar10);
        if (cVar2 != '\0') {
          *(longlong *)(param_1 + 0x608) = lVar9;
        }
      }
      else {
        cVar2 = FUN_1802c5110(1);
        if ((cVar2 == '\0') || (cVar2 = FUN_18000ba20(), cVar2 != '\0')) {
          lVar9 = DAT_18079b168;
          *(undefined4 *)(DAT_18079b168 + 0x58) = 0;
          *(undefined1 *)(lVar9 + 0x60) = 0;
          *(undefined1 *)(lVar9 + 0x2d4) = 0;
        }
        else {
          cVar2 = FUN_1802cd400(DAT_18079b168,"MULTI MENU");
          if (cVar2 != '\0') {
            *(longlong *)(param_1 + 0x608) = DAT_18079b168;
          }
        }
      }
    }
LAB_18020fac7:
    *(undefined2 *)(param_1 + 0x5f5) = 0;
    if (bVar1) {
      FUN_180194aa0(0,"rom/sound/bgm/vf5b_tkv.adx",0);
    }
    return 1;
  }
  FUN_180267920();
  FUN_180211420(param_1);
  *(undefined4 *)(param_1 + 0x28c0) = 0;
  FUN_180081fe0(0x4b,_guard_check_icall,0,0);
  FUN_180081fe0(0x4c,FUN_18020e540,param_1,0);
  FUN_180081fe0(0x4d,_guard_check_icall,0,0);
  FUN_180081fe0(0x4e,FUN_18020e540,0,0);
  FUN_180081fe0(0x55,_guard_check_icall,0,0);
  FUN_180081fe0(0x56,FUN_18020e540,0,0);
  FUN_180081fe0(0x53,_guard_check_icall,0,0);
  FUN_180081fe0(0x54,FUN_18020e520,0,0);
  FUN_180081fe0(0x5e,FUN_18020e570,0,0);
  FUN_180081fe0(0x3a,&LAB_18020e5c0,param_1,0);
  FUN_180081fe0(0x4f,_guard_check_icall,0,0);
  FUN_180081fe0(0x50,FUN_18020e540,0,0);
  FUN_180210d50();
  if (DAT_180c8df28 != 0) {
    if ((*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0) &&
       (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0)) {
      (**(code **)(DAT_180c8df28 + 0x1ff08))(*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xd8,0);
    }
    if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
      local_28[0] = 1;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))
                  (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xbc,local_28);
      }
    }
  }
  cVar2 = FUN_1801cfeb0();
  if (cVar2 != '\0') {
    *(undefined1 *)(param_1 + 0x5f7) = 1;
  }
  FUN_1801d0320();
  uVar6 = FUN_1801dd040();
  cVar2 = FUN_1801dd050(uVar6);
  if (cVar2 != '\0') {
    *(undefined1 *)(param_1 + 0x5f7) = 1;
  }
  plVar7 = (longlong *)FUN_1801d1ae0();
  if ((*(byte *)((longlong)plVar7 + 0x22) & 1) == 0) {
LAB_18020f465:
    cVar2 = '\0';
  }
  else {
    lVar9 = 0x28;
    if ((ulonglong)plVar7[7] <= (ulonglong)plVar7[0xd]) {
      lVar9 = 0x58;
    }
    lVar9 = FUN_1801cdfe0(lVar9 + (longlong)plVar7);
    *(ushort *)((longlong)plVar7 + 0x22) = *(ushort *)((longlong)plVar7 + 0x22) & 0xfffe;
    if (*plVar7 == 1) {
      *plVar7 = 0;
    }
    lVar8 = FUN_1801d1a80();
    if (lVar8 != 0) {
      *(ushort *)(lVar8 + 0x22) = *(ushort *)(lVar8 + 0x22) & 0xfffe;
    }
    *(undefined1 *)(param_1 + 0x5f7) = 1;
    if (lVar9 == 0) goto LAB_18020f465;
    cVar2 = (lVar9 != 1) + '\x01';
  }
  pcVar10 = (char *)(param_1 + 0x5f7);
  *(char *)(param_1 + 0x3021) = cVar2;
  lVar9 = FUN_1801d1ae0();
  if ((char)*(ushort *)(lVar9 + 0x22) < '\0') {
    *(ushort *)(lVar9 + 0x22) = *(ushort *)(lVar9 + 0x22) & 0xff7f;
    lVar9 = FUN_1801d1a80();
    if (lVar9 != 0) {
      *(ushort *)(lVar9 + 0x22) = *(ushort *)(lVar9 + 0x22) & 0xff7f;
    }
    *pcVar10 = '\x01';
    *(undefined1 *)(param_1 + 0x3021) = 3;
  }
  lVar9 = FUN_1801d1ae0();
  bVar3 = FUN_180212d00(*(undefined1 *)(lVar9 + 0x1bd1),0);
  if (bVar3 == 0) {
    cVar2 = *pcVar10;
LAB_18020f50a:
    *(undefined1 *)(param_1 + 0x3022) = 0;
    if (cVar2 == '\0') goto LAB_18020f521;
  }
  else {
    *pcVar10 = '\x01';
    if ((bVar3 & 0x20) == 0) {
      if ((bVar3 & 0x10) == 0) {
        if ((bVar3 & 8) == 0) {
          if ((bVar3 & 4) == 0) {
            if ((bVar3 & 2) == 0) {
              cVar2 = '\x01';
              if ((bVar3 & 1) == 0) goto LAB_18020f50a;
              *(undefined1 *)(param_1 + 0x3022) = 1;
            }
            else {
              *(undefined1 *)(param_1 + 0x3022) = 2;
            }
          }
          else {
            *(undefined1 *)(param_1 + 0x3022) = 3;
          }
        }
        else {
          *(undefined1 *)(param_1 + 0x3022) = 4;
        }
      }
      else {
        *(undefined1 *)(param_1 + 0x3022) = 5;
      }
    }
    else {
      *(undefined1 *)(param_1 + 0x3022) = 6;
    }
  }
  FUN_1801cfd80(1,0xffffffff);
LAB_18020f521:
  *(undefined1 *)(param_1 + 0x5f7) = 0;
  if (*(char *)(param_1 + 0x28dd) == '\0') {
    FUN_18021ba60();
  }
  FUN_18021baf0();
  FUN_18021bb70();
  *(undefined4 *)(param_1 + 0x28d8) = 0;
  *(undefined2 *)(param_1 + 0x28c4) = 0x1311;
  *(undefined4 *)(param_1 + 0x28c9) = 5;
  *(undefined2 *)(param_1 + 0x28cd) = 0;
  *(undefined1 *)(param_1 + 0x28cf) = 0;
  *(undefined4 *)(param_1 + 0x28d2) = 0;
  *(undefined2 *)(param_1 + 0x28d6) = 0;
  *(undefined8 *)(param_1 + 0x608) = 0;
  *(undefined1 *)(param_1 + 0x28dc) = 0;
  *(undefined4 *)(param_1 + 0x28de) = 0;
  *(undefined1 *)(param_1 + 0x3023) = 0;
  cVar2 = FUN_1802cb570();
  if (cVar2 == '\0') {
    FUN_18020e9b0(param_1 + 0x28e8);
  }
  lVar9 = FUN_1800e1940();
  if ((*(int *)(lVar9 + 8) != 6) || (*(int *)(lVar9 + 0x24) != 0x2a)) {
    FUN_180194aa0(0,"rom/sound/bgm/vfes_bgm_mnu.adx",0);
  }
  iVar4 = *(int *)(lVar9 + 0x24);
  if ((iVar4 == 0x2a) || (iVar4 == 0x2b)) {
    DAT_180647160 = 0xe;
  }
  if ((*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) &&
     (iVar4 = (**(code **)(DAT_180c8df28 + 0x1ff08))
                        (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0x50,param_1 + 0x28c4), iVar4 == 1
     )) {
    if (*(char *)(param_1 + 0x28dd) != '\0') {
      FUN_1801a3f20(&DAT_1807956d0);
    }
    FUN_1801b39c0(0x16);
    return 1;
  }
  return 0;
}
