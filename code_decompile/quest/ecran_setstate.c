// ===================================================
// 1800DA800  ->  FUN_1800da800  (entree 1800da800)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1800da800(int param_1,int param_2)

{
  longlong lVar1;
  ulonglong uVar2;
  int *piVar3;
  ulonglong uVar4;
  uint uVar5;
  ulonglong uVar6;
  
  uVar6 = 0;
  if (param_1 != 10) {
    lVar1 = (longlong)DAT_18070c4f0;
    _DAT_18070c4f8 = DAT_18070c4f0;
    DAT_18070c4f4 = 10;
    DAT_18070c4fc = 0;
    DAT_18070c500 = 0;
    _DAT_18070c504 = 0;
    DAT_18070c4f0 = param_1;
    FUN_180215580(10,"[%s]->[%s]\n",(&PTR_s_STARTUP_1803a0c80)[lVar1],
                  (&PTR_s_STARTUP_1803a0c80)[param_1]);
    uVar2 = uVar6;
    uVar4 = uVar6;
    do {
      if (*(int *)((longlong)&DAT_1803a0190 + uVar2) == DAT_18070c4f0) {
        if (uVar4 * 0x68 != -0x1803a0190) {
          DAT_18070c4f4 = *(undefined4 *)(&UNK_1803a01f0 + uVar4 * 0x68);
        }
        break;
      }
      uVar4 = uVar4 + 1;
      uVar2 = uVar2 + 0x68;
    } while (uVar2 < 0x410);
  }
  _DAT_18070c514 = DAT_18070c50c;
  DAT_18070c50c = 0x37;
  DAT_18070c510 = 0x37;
  DAT_18070c518 = 0;
  DAT_18070c51c = 0;
  _DAT_18070c520 = 0;
  uVar2 = uVar6;
  uVar4 = uVar6;
  while (*(int *)((longlong)&DAT_1803a0190 + uVar2) != DAT_18070c4f0) {
    uVar4 = uVar4 + 1;
    uVar2 = uVar2 + 0x68;
    if (0x40f < uVar2) {
      return;
    }
  }
  lVar1 = uVar4 * 0x68;
  if (lVar1 != -0x1803a0190) {
    piVar3 = (int *)(&UNK_1803a01b0 + lVar1);
    if (param_2 == 0x37) {
      DAT_18070c50c = *piVar3;
      DAT_18070c510 = *(undefined4 *)(&UNK_1803a01b4 + lVar1);
      return;
    }
    while (*piVar3 != 0x37) {
      uVar5 = (int)uVar6 + 1;
      if (*piVar3 == param_2) {
        DAT_18070c50c = param_2;
        DAT_18070c510 = *(undefined4 *)(&UNK_1803a01b0 + (longlong)(int)uVar5 * 4 + lVar1);
        DAT_18070c518 = 0;
        DAT_18070c51c = 0;
        _DAT_18070c520 = 0;
        return;
      }
      piVar3 = piVar3 + 1;
      uVar6 = (ulonglong)uVar5;
      if (0xe < (int)uVar5) {
        return;
      }
    }
  }
  return;
}



// ===================================================
// 1801DCE27  ->  FUN_1801dc620  (entree 1801dc620)
// ===================================================

undefined8 FUN_1801dc620(longlong param_1)

{
  undefined4 *puVar1;
  byte bVar2;
  char cVar3;
  undefined1 uVar4;
  int iVar5;
  longlong lVar6;
  undefined1 *puVar7;
  longlong lVar8;
  ulonglong uVar9;
  undefined8 uVar10;
  undefined8 *puVar11;
  undefined4 uVar12;
  undefined1 local_res8 [8];
  undefined4 local_98;
  undefined1 local_94;
  undefined1 local_93;
  undefined1 local_92;
  undefined1 local_91;
  undefined1 local_90;
  undefined1 local_8f;
  undefined1 local_8e;
  undefined8 local_8d;
  undefined2 local_85;
  undefined4 *local_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  ulonglong uStack_60;
  undefined8 local_58;
  undefined8 uStack_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined4 local_38;
  
  if (*(longlong *)(param_1 + 0x650) == 0) {
LAB_1801dc6c2:
    if (*(char *)(param_1 + 0x29fb) == '\0') {
      cVar3 = FUN_180029fb0(local_res8);
      if (cVar3 != '\0') goto LAB_1801dce33;
      *(undefined1 *)(param_1 + 0x29fb) = 1;
      _guard_check_icall(param_1 + 0x2990,param_1 + 0x2980);
      FUN_1801973d0(PTR_DAT_180409ff0);
    }
    if ((DAT_180c3b6f0 == 0) || (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) == 0)) {
      uVar10 = 0;
      FUN_1801bbb10(param_1 + 0x240);
      FUN_1801bbb10(param_1 + 0x298);
      FUN_1801bbb10(param_1 + 0x2f0);
      FUN_1801be800(param_1,0x5a0c);
      if (*(char *)(param_1 + 0x63c) != '\0') {
        iVar5 = FUN_1801bce90(param_1 + 0x4c0);
        if (iVar5 < 0) {
          return 0;
        }
        *(undefined1 *)(param_1 + 0x63c) = 0;
        if (iVar5 == 0) {
          if (*(int *)(param_1 + 0x58) != 9) {
            return 0;
          }
          *(undefined1 *)(param_1 + 0x60) = 1;
          FUN_1801db8b0(param_1);
          *(undefined1 *)(param_1 + 0x641) = 1;
          return 0;
        }
      }
      FUN_1801be880(param_1,0x5a0c);
      cVar3 = FUN_1801bd9d0(param_1);
      if (((cVar3 == '\0') && (cVar3 = FUN_1801bd9c0(param_1 + 0x240), cVar3 != '\0')) &&
         ((cVar3 = FUN_1801bd9c0(param_1 + 0x298), cVar3 != '\0' &&
          (((cVar3 = FUN_1801bd9c0(param_1 + 0x2f0), cVar3 != '\0' &&
            (cVar3 = FUN_180244f90(param_1 + 0x348), cVar3 == '\0')) &&
           (cVar3 = FUN_180244f90(param_1 + 0x4c0), cVar3 == '\0')))))) {
        if ((*(char *)(param_1 + 0x60) != '\0') && (*(int *)(param_1 + 0x58) == 9)) {
          FUN_180191770();
          return 1;
        }
        FUN_1800da9a0(0);
        FUN_1800da9c0(3);
        uVar10 = 1;
      }
      if (*(char *)(param_1 + 0x641) != '\0') {
        return uVar10;
      }
      cVar3 = FUN_180029fb0();
      if (cVar3 == '\0') {
        return uVar10;
      }
      cVar3 = FUN_180007450();
      if (cVar3 != '\0') {
        return uVar10;
      }
      if (*(char *)(param_1 + 0x640) != '\0') {
        *(undefined1 *)(param_1 + 0x640) = 0;
        cVar3 = FUN_180007450();
        if (cVar3 != '\0') {
          local_res8[0] = 1;
          FUN_180087260(0x2e,local_res8);
          return 1;
        }
      }
      if (*(longlong *)(param_1 + 0x650) != 0) {
        cVar3 = FUN_180244f90();
        if (cVar3 != '\0') {
          return uVar10;
        }
        *(undefined8 *)(param_1 + 0x650) = 0;
        if ((*(int *)(param_1 + 0x58) == 9) && (cVar3 = FUN_1801abc00(), cVar3 != '\0')) {
          *(undefined1 *)(param_1 + 0x60) = 1;
          FUN_1801bbae0(param_1);
          FUN_1801bba20(param_1 + 0x240);
          FUN_1801bba20(param_1 + 0x298);
          FUN_1801bba20(param_1 + 0x2f0);
          FUN_1802450a0(param_1 + 0x348);
          FUN_1802450a0(param_1 + 0x4c0);
          *(undefined1 *)(param_1 + 0x641) = 1;
        }
        _guard_check_icall(0xffffffff);
        cVar3 = FUN_1801856a0(0);
        if (cVar3 == '\0') {
          FUN_180185da0(0,"rom/sound/bgm/vf5b_tkv.adx",0);
        }
      }
      local_78 = (undefined4 *)0x6300000062;
      uStack_70 = 0x6600000065;
      uStack_68 = (longlong *)0x6800000067;
      uStack_60 = 0x6a00000069;
      local_58._4_4_ = 0x6e;
      cVar3 = FUN_180007450();
      uVar12 = 0x6b;
      if (cVar3 == '\0') {
        uVar12 = 0x6d;
      }
      local_58 = CONCAT44(local_58._4_4_,uVar12);
      FUN_1801be880(param_1,*(undefined4 *)
                             ((longlong)&local_78 + (longlong)*(int *)(param_1 + 0x58) * 4));
      cVar3 = FUN_180244f90(param_1 + 0x348);
      if (cVar3 != '\0') {
        return uVar10;
      }
      FUN_1801bbbe0(param_1);
      FUN_1801be800(param_1,0);
      return uVar10;
    }
    if (*(char *)(param_1 + 0x2a09) == '\0') {
      local_92 = 0;
      local_8d = 5;
      local_85 = 0;
      uVar4 = FUN_180029fb0();
      local_98 = CONCAT31(local_98._1_3_,uVar4);
      cVar3 = FUN_180029fb0();
      if (cVar3 == '\0') {
LAB_1801dc75a:
        local_98._0_2_ = (ushort)(byte)local_98;
      }
      else {
        cVar3 = FUN_1801b89e0();
        local_98._0_2_ = CONCAT11(1,(byte)local_98);
        if (cVar3 != '\0') goto LAB_1801dc75a;
      }
      cVar3 = FUN_180029fb0();
      if (cVar3 == '\0') {
LAB_1801dc774:
        local_98 = local_98 & 0xffff;
      }
      else {
        cVar3 = FUN_1801b89f0();
        local_98 = (uint)CONCAT12(1,(ushort)local_98);
        if (cVar3 != '\0') goto LAB_1801dc774;
      }
      lVar6 = FUN_1801b8a30();
      local_94 = *(undefined1 *)(lVar6 + 4);
      puVar7 = (undefined1 *)FUN_1801b8a30();
      local_93 = *puVar7;
      lVar6 = FUN_1801b8a30();
      local_91 = *(undefined1 *)(lVar6 + 8);
      lVar6 = FUN_1801b8a00();
      local_90 = *(undefined1 *)(lVar6 + 0x40);
      lVar8 = FUN_1801b8a20();
      local_8f = true;
      lVar6 = *(longlong *)(lVar8 + 0x60);
      if ((lVar6 != 0) && (uVar9 = FUN_18022c0b0(), uVar9 <= lVar6 + 0x2a30U)) {
        uVar9 = FUN_1801b65f0(lVar8 + 0x50);
        local_8f = uVar9 < 3;
      }
      local_8e = *(undefined1 *)(param_1 + 0x2a14);
      puVar7 = (undefined1 *)FUN_1801b8a00();
      local_8d = CONCAT71(local_8d._1_7_,*puVar7);
      lVar6 = FUN_1801b8a00();
      local_8d._0_2_ = CONCAT11(*(undefined1 *)(lVar6 + 4),(undefined1)local_8d);
      lVar6 = FUN_1801b8a00();
      local_8d._0_3_ = CONCAT12(*(undefined1 *)(lVar6 + 8),(undefined2)local_8d);
      lVar6 = FUN_1801b8a00();
      local_8d._0_4_ = CONCAT13(*(undefined1 *)(lVar6 + 0xc),(undefined3)local_8d);
      lVar6 = FUN_1801b8a00();
      local_8d._0_5_ = CONCAT14(*(undefined1 *)(lVar6 + 0x10),(undefined4)local_8d);
      lVar6 = FUN_1801b8a00();
      local_8d._0_6_ = CONCAT15(*(undefined1 *)(lVar6 + 0x14),(undefined5)local_8d);
      lVar6 = FUN_1801b8a00();
      local_8d._0_7_ = CONCAT16(*(undefined1 *)(lVar6 + 0x18),(undefined6)local_8d);
      lVar6 = FUN_1801b8a00();
      local_8d = CONCAT17(*(undefined1 *)(lVar6 + 0x1c),(undefined7)local_8d);
      lVar6 = FUN_1801b8a00();
      local_85 = CONCAT11(local_85._1_1_,*(undefined1 *)(lVar6 + 0x20));
      lVar6 = FUN_1801b8a00();
      uVar9 = uStack_70;
      iVar5 = *(int *)(lVar6 + 0x24);
      local_78 = &local_98;
      *(undefined1 *)(param_1 + 0x2a14) = 0;
      local_85 = CONCAT11(iVar5 != 0,(undefined1)local_85);
      uStack_70 = CONCAT71(uStack_70._1_7_,DAT_18064bb28);
      uVar10 = uStack_70;
      cVar3 = *(char *)(param_1 + 0x29f8);
      uStack_70._5_3_ = SUB83(uVar9,5);
      uStack_70._0_5_ = (uint5)(uint)uVar10;
      *(undefined1 *)(param_1 + 0x29f8) = 1;
      if ((cVar3 == '\0') && (cVar3 = FUN_180007450(), cVar3 == '\0')) {
        *(undefined1 *)(param_1 + 0x29f9) = 1;
      }
      if ((((*(char *)(param_1 + 0x29fa) == '\0') && (*(char *)(param_1 + 0x29f9) == '\0')) ||
          (cVar3 = FUN_180007450(), cVar3 != '\0')) || (*(char *)(param_1 + 0x29f9) == '\0')) {
        cVar3 = FUN_180007450();
        if (cVar3 == '\0') {
          *(undefined1 *)(param_1 + 0x29fa) = 1;
          uVar4 = 0;
        }
        else {
          uVar4 = 1;
        }
      }
      else {
        if (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0) {
          *(undefined2 *)(param_1 + 0x3dc) = 0x100;
          *(undefined8 *)(param_1 + 0x3e0) = 0;
          *(undefined4 *)(param_1 + 0x3d8) = 1;
          uVar10 = FUN_1801efd10(0x3fb);
          *(undefined8 *)(param_1 + 0x3e0) = uVar10;
        }
        *(undefined2 *)(param_1 + 0x29f9) = 0x100;
        uVar4 = 0;
      }
      uStack_70._0_2_ = CONCAT11(uVar4,(undefined1)uStack_70);
      lVar6 = FUN_1801b8a20();
      *(byte *)(param_1 + 0x29e3) = *(byte *)(lVar6 + 0x1e) >> 1 & 1;
      uStack_68 = (longlong *)(param_1 + 0x2990);
      uVar4 = FUN_1801e67a0();
      *(undefined1 *)(param_1 + 0x299c) = uVar4;
      uVar9 = uStack_70 >> 0x18;
      uStack_70._0_3_ = CONCAT12(*(int *)(param_1 + 0x2a00) - 3U < 2,(undefined2)uStack_70);
      uStack_70 = CONCAT53((int5)uVar9,(undefined3)uStack_70) & 0xffffffff00ffffff;
      if ((*(code **)(DAT_180c3b6f0 + 0x1fe10) == (code *)0x0) ||
         (iVar5 = (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                            (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0x4b,&local_78), iVar5 != 1))
      {
        if ((*(int *)(param_1 + 0x2a00) == 0) && (cVar3 = FUN_1801856a0(0), cVar3 == '\0')) {
          FUN_180185da0(0,"rom/sound/bgm/vfes_bgm_mnu.adx",0);
        }
        FUN_1801dbbd0(param_1 + 0x2a00,uStack_70._3_1_);
        if (*(char *)(param_1 + 0x29fc) == '\0') {
          if (*(char *)(param_1 + 0x29e1) != '\0') {
            if (*(char *)(param_1 + 0x29e0) == '\0') {
              uVar4 = *(undefined1 *)(*(longlong *)(param_1 + 0x2990) + 1);
            }
            else {
              uVar4 = *(undefined1 *)(param_1 + 0x29df);
            }
            thunk_FUN_1801d07a0(0,uVar4,0,1);
            *(undefined1 *)(param_1 + 0x29e2) = 0;
            *(undefined1 *)(param_1 + 0x299b) = 0;
            *(undefined1 *)(param_1 + 0x29fc) = 1;
          }
        }
        else {
          iVar5 = FUN_1801c34e0(0,param_1 + 0x2980);
          if (iVar5 != 0) {
            *(undefined1 *)(param_1 + 0x29e1) = 0;
            *(undefined1 *)(param_1 + 0x29fc) = 0;
            *(bool *)(param_1 + 0x299b) = 0 < iVar5;
          }
          if (*(char *)(param_1 + 0x29e2) != '\0') {
            thunk_FUN_1801cedb0(0);
            *(undefined2 *)(param_1 + 0x29e1) = 0;
            *(undefined1 *)(param_1 + 0x29fc) = 0;
            *(bool *)(param_1 + 0x299b) = 0 < iVar5;
          }
        }
        if (*(char *)(param_1 + 0x29e3) != '\0') {
          *(undefined1 *)(param_1 + 0x29e3) = 0;
          lVar6 = FUN_1801b8a20();
          *(ushort *)(lVar6 + 0x1e) = *(ushort *)(lVar6 + 0x1e) | 2;
          return 0;
        }
        goto LAB_1801dce33;
      }
      FUN_1801973f0(PTR_DAT_180409ff0);
    }
    cVar3 = FUN_1801de560(param_1 + 0x2a00);
    if ((cVar3 == '\0') || (cVar3 = FUN_1800ba090(), cVar3 != '\0')) goto LAB_1801dce33;
    puVar1 = (undefined4 *)(param_1 + 0x29e8);
    DAT_18064bb28 = *(undefined1 *)puVar1;
    switch(*(undefined1 *)puVar1) {
    case 3:
      if ((DAT_180c3b6f0 != 0) && (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0)) {
        local_98 = 6;
        if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
          (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                    (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0xa4,&local_98);
        }
      }
      FUN_18019bbe0(local_res8,*(undefined2 *)(param_1 + 0x29f0),*(undefined2 *)(param_1 + 0x29f2),
                    *(undefined1 *)(param_1 + 0x29ec),*(undefined1 *)(param_1 + 0x29eb));
      cVar3 = *(char *)(param_1 + 0x29ed);
      FUN_180210e50();
      FUN_18019c520(4,local_res8,cVar3);
      iVar5 = FUN_1801a2330(1);
      if (iVar5 < 0) {
        FUN_1801a3830(1);
      }
      puVar11 = (undefined8 *)FUN_1801b8a00();
      local_78 = (undefined4 *)*puVar11;
      uStack_70 = puVar11[1];
      uStack_50 = puVar11[5];
      uStack_48 = puVar11[6];
      uStack_40 = puVar11[7];
      local_38 = *(undefined4 *)(puVar11 + 8);
      uStack_68._0_4_ = (undefined4)puVar11[2];
      uStack_68 = (longlong *)
                  (ulonglong)CONCAT14(*(undefined1 *)(param_1 + 0x29f4),(undefined4)uStack_68);
      uStack_60 = (ulonglong)
                  CONCAT14(*(undefined1 *)(param_1 + 0x29f6),(uint)*(byte *)(param_1 + 0x29f5));
      local_58 = (ulonglong)CONCAT14(cVar3 != '\0',(uint)*(byte *)(param_1 + 0x29f7));
      FUN_1801ba0a0(&local_78);
      uVar10 = 1;
      break;
    case 4:
      if ((DAT_180c3b6f0 != 0) && (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0)) {
        local_98 = 5;
        if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
          (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                    (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0xa4,&local_98);
        }
      }
      FUN_18019bbe0(local_res8,*(undefined2 *)(param_1 + 0x29f0),*(undefined2 *)(param_1 + 0x29f2),
                    *(undefined1 *)(param_1 + 0x29ec),*(undefined1 *)(param_1 + 0x29eb));
      bVar2 = *(byte *)(param_1 + 0x29ea);
      FUN_18019c420(0,local_res8,bVar2,0);
      lVar6 = FUN_1801b8a00();
      uStack_60 = *(undefined8 *)(lVar6 + 0x18);
      local_58 = *(undefined8 *)(lVar6 + 0x20);
      uStack_50 = *(undefined8 *)(lVar6 + 0x28);
      uStack_48 = *(undefined8 *)(lVar6 + 0x30);
      uStack_40 = *(undefined8 *)(lVar6 + 0x38);
      local_38 = *(undefined4 *)(lVar6 + 0x40);
      uStack_70 = (ulonglong)
                  CONCAT14(*(undefined1 *)(param_1 + 0x29f6),(uint)*(byte *)(param_1 + 0x29f5));
      uStack_68 = (longlong *)
                  CONCAT44((int)((ulonglong)*(undefined8 *)(lVar6 + 0x10) >> 0x20),
                           (uint)*(byte *)(param_1 + 0x29f7));
      local_78 = (undefined4 *)(ulonglong)CONCAT14(*(undefined1 *)(param_1 + 0x29f4),(uint)bVar2);
      FUN_1801ba0a0(&local_78);
      uVar10 = 1;
      break;
    case 5:
      if ((DAT_180c3b6f0 != 0) && (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0)) {
        local_98 = 7;
        if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
          (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                    (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0xa4,&local_98);
        }
      }
      FUN_18020f6b0(*(undefined1 *)(param_1 + 0x29e9));
      FUN_18020f5c0(1);
      FUN_18019c3d0(6,0,1);
      uVar10 = 1;
      break;
    case 6:
      if ((DAT_180c3b6f0 != 0) && (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0)) {
        local_98 = 7;
        if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
          (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                    (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0xa4,&local_98);
        }
      }
      FUN_18019c3d0(7,*(char *)(param_1 + 0x29ee) == '\0',1);
      uVar10 = 1;
      break;
    case 7:
      if ((DAT_180c3b6f0 != 0) && (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0)) {
        local_98 = 7;
        if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
          (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                    (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0xa4,&local_98);
        }
      }
      FUN_18019c3d0(8,0,1);
      uVar10 = 1;
      break;
    case 8:
      uVar10 = FUN_1801b0120(0,0,1);
      *(undefined8 *)(param_1 + 0x650) = uVar10;
      goto LAB_1801dce33;
    default:
      FUN_1801e2e80(param_1 + 0x2a00);
      *puVar1 = 0x5140c;
      *(undefined2 *)(param_1 + 0x29ec) = 0;
      *(undefined1 *)(param_1 + 0x29ee) = 0;
      *(undefined8 *)(param_1 + 0x29f0) = 0;
      if ((((DAT_180c3b6f0 != 0) && (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0)) &&
          (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0)) &&
         (iVar5 = (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                            (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0x4a,puVar1), iVar5 == 1))
      goto LAB_1801dce33;
    case 0:
    case 1:
    case 2:
      uVar10 = 1;
      break;
    case 10:
      if ((DAT_180c3b6f0 != 0) && (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0)) {
        local_98 = 8;
        if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
          (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                    (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0xa4,&local_98);
        }
      }
      FUN_1800da9a0(5);
      FUN_1800da9c0(0x25);
      uVar10 = 1;
    }
  }
  else {
    cVar3 = FUN_180244ea0();
    if (cVar3 == '\0') {
      *(undefined8 *)(param_1 + 0x650) = 0;
      FUN_1801e2e80(param_1 + 0x2a00);
      *(undefined4 *)(param_1 + 0x29e8) = 0x5140c;
      *(undefined2 *)(param_1 + 0x29ec) = 0;
      *(undefined1 *)(param_1 + 0x29ee) = 0;
      *(undefined8 *)(param_1 + 0x29f0) = 0;
      if ((((DAT_180c3b6f0 == 0) || (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) == 0)) ||
          (*(code **)(DAT_180c3b6f0 + 0x1fe10) == (code *)0x0)) ||
         (iVar5 = (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                            (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0x4a), iVar5 != 1))
      goto LAB_1801dc6c2;
    }
LAB_1801dce33:
    uVar10 = 0;
  }
  return uVar10;
}



