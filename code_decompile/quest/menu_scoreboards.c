// ===================================================
// 1801E3D86  ->  FUN_1801e36d0  (entree 1801e36d0)
// ===================================================

undefined8 FUN_1801e36d0(longlong param_1)

{
  bool bVar1;
  char cVar2;
  int iVar3;
  undefined4 uVar4;
  longlong lVar5;
  undefined8 *puVar6;
  undefined8 uVar7;
  longlong lVar8;
  char *pcVar9;
  undefined8 local_78;
  undefined4 local_70;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 local_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  undefined8 uStack_30;
  int local_28;
  
  cVar2 = FUN_1801b7010();
  if (cVar2 == '\0') {
    return 0;
  }
  if ((DAT_180c3b6f0 != 0) && (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0)) {
    FUN_180087550(0x49,_guard_check_icall,0);
    FUN_180087550(0x4a,FUN_1801e2a70,0);
    FUN_180087550(0x4b,_guard_check_icall,0);
    FUN_180087550(0x4c,FUN_1801e2a70,0);
    cVar2 = FUN_180029fb0();
    if (cVar2 == '\0') {
      lVar5 = FUN_1801b8a10();
      if (1 < *(byte *)(lVar5 + 0x4f95)) {
        *(undefined1 *)(lVar5 + 0x4f95) = 0;
      }
      puVar6 = (undefined8 *)FUN_1801b8a00();
      local_68 = *puVar6;
      uStack_60 = puVar6[1];
      uStack_58 = puVar6[2];
      uStack_50 = puVar6[3];
      local_48 = puVar6[4];
      uStack_40 = puVar6[5];
      uStack_38 = puVar6[6];
      uStack_30 = puVar6[7];
      local_28 = *(int *)(puVar6 + 8);
      if (local_28 != 0) {
        local_28 = 0;
        FUN_1801ba0a0(&local_68);
      }
      puVar6 = (undefined8 *)FUN_1801b8a30();
      local_78 = *puVar6;
      if (*(int *)(puVar6 + 1) != 0) {
        local_70 = 0;
        FUN_1801ba0d0(&local_78);
      }
    }
    if ((DAT_180c3b6f0 != 0) && (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0)) {
      local_78 = CONCAT44(local_78._4_4_,1);
      if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
        (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                  (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0xa4,&local_78);
      }
    }
    cVar2 = FUN_1801b7ab0();
    if (cVar2 != '\0') {
      *(undefined1 *)(param_1 + 0x63f) = 1;
    }
    FUN_1801b7c20();
    uVar7 = FUN_1801bb730();
    cVar2 = FUN_180007450(uVar7);
    if (cVar2 != '\0') {
      *(undefined1 *)(param_1 + 0x63f) = 1;
    }
    lVar5 = FUN_1801b8a20();
    if ((*(byte *)(lVar5 + 0x1e) & 1) != 0) {
      lVar8 = 0x20;
      if (*(ulonglong *)(lVar5 + 0x30) <= *(ulonglong *)(lVar5 + 0x60)) {
        lVar8 = 0x50;
      }
      lVar8 = FUN_1801b65f0(lVar8 + lVar5);
      *(ushort *)(lVar5 + 0x1e) = *(ushort *)(lVar5 + 0x1e) & 0xfffe;
      *(undefined1 *)(param_1 + 0x63f) = 1;
      if (lVar8 != 0) {
        cVar2 = (lVar8 != 1) + '\x01';
        goto LAB_1801e38a8;
      }
    }
    cVar2 = '\0';
LAB_1801e38a8:
    *(char *)(param_1 + 0x2a14) = cVar2;
    if (*(char *)(param_1 + 0x63f) != '\0') {
      FUN_1801b7960(1,0xffffffff);
    }
    *(undefined1 *)(param_1 + 0x63f) = 0;
    if (*(char *)(param_1 + 0x29fb) == '\0') {
      _guard_check_icall();
    }
    *(undefined2 *)(param_1 + 0x29f8) = 0;
    *(undefined1 *)(param_1 + 0x29fa) = 0;
    *(undefined1 *)(param_1 + 0x29fc) = 0;
    *(undefined4 *)(param_1 + 0x29e8) = 0x5140c;
    *(undefined2 *)(param_1 + 0x29ec) = 0;
    *(undefined1 *)(param_1 + 0x29ee) = 0;
    *(undefined8 *)(param_1 + 0x29f0) = 0;
    *(undefined8 *)(param_1 + 0x650) = 0;
    if ((DAT_180c3b6f0 != 0) && (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0)) {
      FUN_1801e2e80(param_1 + 0x2a00);
      FUN_180185da0(0,"rom/sound/bgm/vfes_bgm_mnu.adx",0);
      if ((*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) &&
         (iVar3 = (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                            (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0x4a,param_1 + 0x29e8),
         iVar3 == 1)) {
        if (*(char *)(param_1 + 0x29fb) == '\0') {
          return 1;
        }
        FUN_1801973d0(PTR_DAT_180409ff0);
        return 1;
      }
    }
    return 0;
  }
  FUN_1801be860(param_1,1);
  FUN_1801be870(param_1,10);
  FUN_1801be7e0(param_1,1);
  FUN_1801bd120(param_1);
  *(undefined4 *)(param_1 + 0x224) = 9;
  *(undefined1 *)(param_1 + 0x228) = 0;
  FUN_1801a3890(2);
  *(undefined8 *)(param_1 + 0x642) = 0;
  *(undefined2 *)(param_1 + 0x64a) = 0;
  cVar2 = FUN_180007450();
  if (cVar2 != '\0') {
    *(undefined1 *)(param_1 + 0x646) = 1;
    *(undefined2 *)(param_1 + 0x643) = 0x101;
  }
  *(undefined1 *)(param_1 + 0x64b) = 2;
  *(undefined1 *)(param_1 + 0x648) = 2;
  *(undefined4 *)(param_1 + 0x638) = 0;
  FUN_1801bd0b0(param_1 + 0x240);
  FUN_1801bd0b0(param_1 + 0x298);
  FUN_1801bd0b0(param_1 + 0x2f0);
  *(undefined1 *)(param_1 + 0x63c) = 0;
  *(undefined2 *)(param_1 + 0x640) = 0;
  if (*(char *)(param_1 + 0x63f) != '\0') {
    FUN_1801b7960(1,0xffffffff);
  }
  *(undefined1 *)(param_1 + 0x63f) = 0;
  *(undefined8 *)(param_1 + 0x650) = 0;
  bVar1 = true;
  cVar2 = FUN_180007450(0xffffffff);
  if (cVar2 != '\0') {
    uVar4 = FUN_180007440();
    cVar2 = FUN_180007450(uVar4);
    if (cVar2 == '\0') {
      FUN_1800da9a0(0);
      FUN_1800da9c0(3);
LAB_1801e3c30:
      *(undefined1 *)(param_1 + 0x641) = 1;
      FUN_1802450a0(param_1);
      return 1;
    }
    cVar2 = FUN_180007450();
    if (cVar2 == '\0') {
      cVar2 = FUN_180007450();
      if ((cVar2 != '\0') && (cVar2 = FUN_180007450(), cVar2 == '\0')) {
        *(undefined4 *)(DAT_180753820 + 0x58) = 1;
        *(undefined1 *)(DAT_180753820 + 0x60) = 1;
        FUN_1800da9a0(7);
        FUN_1801e4960(DAT_180753818,0);
        *(undefined4 *)(DAT_180753818 + 0x58) = 2;
        *(undefined1 *)(DAT_180753820 + 0x60) = 1;
        goto LAB_1801e3c30;
      }
      _guard_check_icall();
      FUN_1801e4960(DAT_180753818,0);
      *(undefined4 *)(DAT_180753818 + 0x58) = 2;
      *(undefined1 *)(DAT_180753820 + 0x60) = 1;
    }
    else {
      uVar7 = FUN_1801ac2c0(0,0);
      *(undefined8 *)(param_1 + 0x650) = uVar7;
      bVar1 = false;
    }
  }
  FUN_1801973d0(PTR_DAT_180409ff0);
  FUN_1801be8e0(param_1 + 0x240,7);
  FUN_1801bda20(param_1 + 0x240,0x2b);
  FUN_1801be8e0(param_1 + 0x298,1);
  FUN_1801bda20(param_1 + 0x298,0x2a);
  FUN_1801be8e0(param_1 + 0x2f0,0x19);
  FUN_1801bda20(param_1 + 0x2f0,0x2c);
  uVar4 = FUN_180029af0(0x2a3,"bg_base",1,0x10000,"neu_s","neu_e");
  *(undefined4 *)(param_1 + 0x638) = uVar4;
  if (*(longlong *)(param_1 + 0x650) != 0) goto LAB_1801e3e1a;
  if (*(char *)(DAT_180753820 + 0x60) != '\0') {
    cVar2 = FUN_180007450();
    if ((cVar2 == '\0') || (cVar2 = FUN_180007450(), cVar2 != '\0')) {
      lVar5 = DAT_180753820;
      *(undefined4 *)(DAT_180753820 + 0x58) = 0;
      *(undefined1 *)(lVar5 + 0x60) = 0;
      *(undefined1 *)(lVar5 + 0x2f4) = 0;
    }
    else {
      cVar2 = FUN_180245830(DAT_180753820,"MULTI MENU");
      if (cVar2 != '\0') {
        *(longlong *)(param_1 + 0x650) = DAT_180753820;
      }
    }
    goto LAB_1801e3e1a;
  }
  lVar5 = param_1 + 0x658;
  if (((((*(char *)(param_1 + 0x6b8) == '\0') && (*(char *)(param_1 + 0x9b8) == '\0')) &&
       (*(char *)(param_1 + 0xe98) == '\0')) &&
      ((*(char *)(param_1 + 0x1158) == '\0' && (iVar3 = FUN_1801a5620(), iVar3 != 2)))) &&
     (iVar3 = FUN_1801a5660(), iVar3 != 2)) {
    if (*(char *)(param_1 + 0x1a08) == '\0') {
      lVar5 = param_1 + 0x1cf0;
      if (((*(char *)(param_1 + 0x1d50) == '\0') && (*(char *)(param_1 + 0x2050) == '\0')) &&
         (cVar2 = FUN_18020f170(), cVar2 == '\0')) {
        lVar5 = param_1 + 9000;
        if ((((*(char *)(param_1 + 0x2388) == '\0') && (iVar3 = FUN_1801cfda0(), iVar3 != 2)) &&
            (cVar2 = FUN_1801c5c60(), cVar2 == '\0')) &&
           ((*(char *)(param_1 + 0x2688) == '\0' && (*(char *)(param_1 + 0x291a) == '\0')))) {
          if (*(char *)(param_1 + 0x63d) == '\0') {
            if (*(char *)(param_1 + 0x63e) != '\0') {
              uVar7 = FUN_1801ab3a0(0,0,0);
              *(undefined8 *)(param_1 + 0x650) = uVar7;
            }
          }
          else {
            uVar7 = FUN_1801b0120(0,0,0);
            *(undefined8 *)(param_1 + 0x650) = uVar7;
          }
          goto LAB_1801e3e1a;
        }
        pcVar9 = "TERMINAL MENU";
      }
      else {
        cVar2 = FUN_180007450();
        if (cVar2 != '\0') {
          FUN_1801e4a40(lVar5);
          goto LAB_1801e3deb;
        }
        pcVar9 = "TRAINING MENU";
      }
    }
    else {
      lVar5 = param_1 + 0x19a8;
      pcVar9 = "VERSUS MENU";
    }
  }
  else {
    cVar2 = FUN_180007450();
    if (cVar2 != '\0') {
      FUN_1801e48e0(lVar5);
LAB_1801e3deb:
      uVar7 = FUN_1801ac2c0(0,0);
      *(undefined8 *)(param_1 + 0x650) = uVar7;
      bVar1 = false;
      goto LAB_1801e3e1a;
    }
    pcVar9 = "ARCADE MENU";
  }
  cVar2 = FUN_180245830(lVar5,pcVar9);
  if (cVar2 != '\0') {
    *(longlong *)(param_1 + 0x650) = lVar5;
  }
LAB_1801e3e1a:
  *(undefined2 *)(param_1 + 0x63d) = 0;
  if (!bVar1) {
    return 1;
  }
  FUN_180185da0(0,"rom/sound/bgm/vf5b_tkv.adx",0);
  return 1;
}



