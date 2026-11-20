// ===================================================
// 18016DA30  ->  FUN_18016da30  (entree 18016da30)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_18016da30(longlong param_1)

{
  longlong lVar1;
  undefined1 uVar2;
  char cVar3;
  char cVar4;
  char cVar5;
  char cVar6;
  int iVar7;
  undefined4 uVar8;
  longlong lVar9;
  int *piVar10;
  undefined8 uVar11;
  int iVar12;
  undefined *puVar13;
  ulonglong uVar14;
  char *pcVar15;
  float fVar16;
  undefined8 in_stack_ffffffffffffffb8;
  
  uVar8 = (undefined4)((ulonglong)in_stack_ffffffffffffffb8 >> 0x20);
  lVar1 = param_1 + 200;
  *(undefined1 *)(param_1 + 0x6b) = *(undefined1 *)(param_1 + 0x6a);
  uVar2 = FUN_1801724a0(lVar1,0);
  *(undefined1 *)(param_1 + 0x6a) = uVar2;
  *(undefined1 *)(param_1 + 0x9b) = *(undefined1 *)(param_1 + 0x9a);
  cVar3 = FUN_1801724a0(lVar1,1);
  uVar14 = 0;
  *(char *)(param_1 + 0x9a) = cVar3;
  if (((*(char *)(param_1 + 0x6a) != *(char *)(param_1 + 0x6b)) ||
      (cVar3 != *(char *)(param_1 + 0x9b))) && (*(int *)(param_1 + 0x58) != 2)) {
    *(undefined4 *)(param_1 + 0x58) = 0;
  }
  lVar9 = FUN_18016b0c0();
  iVar7 = *(int *)(param_1 + 0x58);
  iVar12 = (*(char *)(lVar9 + 0x20) != '\0') + 0x14b;
  if (iVar7 == 0) {
    if (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) == 0) {
      cVar3 = FUN_180187cc0(0x144);
      if (cVar3 != '\0') {
        return 0;
      }
      cVar3 = FUN_180029d40(0x112);
      if (cVar3 != '\0') {
        return 0;
      }
      uVar11 = CONCAT44(uVar8,1);
      FUN_180171e90(PTR_DAT_1803ffbd0,7,iVar12,"bg_light_in",uVar11,0x20000);
      uVar11 = CONCAT44((int)((ulonglong)uVar11 >> 0x20),9);
      FUN_180171e90(PTR_DAT_1803ffbd0,0xf,iVar12,"deco_tit_chara_in",uVar11,0x20000);
      uVar8 = (undefined4)((ulonglong)uVar11 >> 0x20);
      cVar3 = FUN_180007450();
      uVar11 = CONCAT44(uVar8,0xb);
      if (cVar3 == '\0') {
        FUN_180171e90(PTR_DAT_1803ffbd0,0x10,iVar12,"chara_icon_base_in",uVar11,0x20000);
        uVar8 = (undefined4)((ulonglong)uVar11 >> 0x20);
        pcVar15 = "chara_icon_name_in";
      }
      else {
        FUN_180171e90(PTR_DAT_1803ffbd0,0x10,iVar12,"chara_icon_base_in_dur",uVar11,0x20000);
        uVar8 = (undefined4)((ulonglong)uVar11 >> 0x20);
        pcVar15 = "chara_icon_name_in_dur";
      }
      FUN_180171e90(PTR_DAT_1803ffbd0,0x11,iVar12,pcVar15,CONCAT44(uVar8,0xf),0x20000);
    }
    FUN_180245830(lVar1,"SEL_CURSOR");
    if (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) == 0) {
      puVar13 = &DAT_1803ff0b0;
      cVar3 = '\x15';
    }
    else {
      *(undefined1 *)(param_1 + 0x1c8) = 1;
      puVar13 = &DAT_1803ff350;
      cVar3 = FUN_180007450();
      cVar3 = (cVar3 != '\0') + '\x14';
    }
    FUN_180173bd0(lVar1,puVar13,cVar3);
    cVar3 = FUN_180007450();
    if (cVar3 != '\0') {
      do {
        if (*(int *)((longlong)&DAT_1803ff5f0 + uVar14) == 0x15) break;
        FUN_180173f50(lVar1);
        uVar14 = uVar14 + 4;
      } while (uVar14 < 0x40);
    }
    cVar3 = FUN_180007450();
    if (cVar3 == '\0') {
      FUN_180173f50(lVar1,0x14);
    }
    *(undefined1 *)(param_1 + 0x6c) = 0;
    *(undefined4 *)(param_1 + 0x70) = 0;
    *(undefined8 *)(param_1 + 0x78) = 0;
    *(undefined8 *)(param_1 + 0x80) = 0;
    *(undefined8 *)(param_1 + 0x88) = 0;
    *(undefined1 *)(param_1 + 0x9c) = 0;
    *(undefined4 *)(param_1 + 0xa0) = 0;
    *(undefined8 *)(param_1 + 0xa8) = 0;
    *(undefined8 *)(param_1 + 0xb0) = 0;
    *(undefined8 *)(param_1 + 0xb8) = 0;
    DAT_180714940 = 0;
    DAT_180714944 = 0;
    _DAT_180714948 = 0x15;
    _DAT_180714950 = 0;
    _DAT_180714958 = 1;
    _DAT_180714960 = 0;
    DAT_180714964 = 1;
    DAT_180714968 = 1;
    DAT_18071496c = 0;
    _DAT_180714970 = 0x15;
    _DAT_180714978 = 0;
    _DAT_180714980 = 1;
    _DAT_180714988 = 0;
    DAT_18071498c = 1;
    *(undefined4 *)(param_1 + 0x58) = 1;
    return 0;
  }
  if (iVar7 == 1) {
    cVar3 = FUN_180244fc0(lVar1);
    if (cVar3 == '\0') {
      return 0;
    }
    FUN_180173f90(lVar1,0,0);
    FUN_180173f90(lVar1,1);
    *(undefined4 *)(param_1 + 0x58) = 2;
    return 0;
  }
  if (iVar7 != 2) {
    if (iVar7 == 3) {
      cVar3 = FUN_180173b80(lVar1);
      if (cVar3 != '\0') {
        return 0;
      }
      FUN_1802450a0(lVar1);
      cVar3 = FUN_1800cb400(0);
      if (cVar3 != '\0') {
        FUN_1800cb460(0);
      }
      cVar3 = FUN_1800cb400(1);
      if (cVar3 != '\0') {
        FUN_1800cb460(1);
      }
      FUN_180171e90(PTR_DAT_1803ffbd0,7,iVar12,"bg_light_change",CONCAT44(uVar8,1),0x20000);
      uVar8 = 0;
      FUN_180171f40(PTR_DAT_1803ffbd0,0xf,iVar12,"deco_tit_chara_out_stage_in",0,9,0x20000,
                    "cha_out_start","cha_out_end");
      cVar3 = FUN_180007450();
      uVar11 = CONCAT44(uVar8,0xb);
      if (cVar3 == '\0') {
        FUN_180171e90(PTR_DAT_1803ffbd0,0x10,iVar12,"chara_end",uVar11,0x20000);
        uVar8 = (undefined4)((ulonglong)uVar11 >> 0x20);
        pcVar15 = "chara_icon_name_out";
      }
      else {
        FUN_180171e90(PTR_DAT_1803ffbd0,0x10,iVar12,"chara_end_dur",uVar11,0x20000);
        uVar8 = (undefined4)((ulonglong)uVar11 >> 0x20);
        pcVar15 = "chara_icon_name_out_dur";
      }
      FUN_180171e90(PTR_DAT_1803ffbd0,0x11,iVar12,pcVar15,CONCAT44(uVar8,0xf),0x20000);
      FUN_180172210(PTR_DAT_1803ffbd0,DAT_180714940,4);
      FUN_180172210(PTR_DAT_1803ffbd0,DAT_180714968,4);
      *(undefined4 *)(param_1 + 0x58) = 4;
      return 0;
    }
    if (iVar7 != 4) {
      return 0;
    }
    fVar16 = (float)FUN_180171d20(PTR_DAT_1803ffbd0,0x11);
    if (DAT_18034b8b4 <= fVar16) {
      FUN_1801721d0(PTR_DAT_1803ffbd0,0x13);
      FUN_1801721d0(PTR_DAT_1803ffbd0,0x14);
    }
    cVar3 = FUN_1800cb400(0);
    if ((cVar3 != '\0') && (cVar3 = FUN_1800cb420(0), cVar3 == '\0')) {
      return 0;
    }
    cVar3 = FUN_1800cb400(1);
    if ((cVar3 != '\0') && (cVar3 = FUN_1800cb420(1), cVar3 == '\0')) {
      return 0;
    }
    cVar3 = FUN_180171070(PTR_DAT_1803ffbd0,0xf);
    if (cVar3 == '\0') {
      return 0;
    }
    cVar3 = FUN_180171070(PTR_DAT_1803ffbd0,0x10);
    if (cVar3 == '\0') {
      return 0;
    }
    cVar3 = FUN_180171070(PTR_DAT_1803ffbd0,0x11);
    if (cVar3 == '\0') {
      return 0;
    }
    return 1;
  }
  FUN_180173f90(lVar1,0,0);
  FUN_180173f90(lVar1,1);
  cVar3 = FUN_180171070(PTR_DAT_1803ffbd0,7);
  if (cVar3 != '\0') {
    FUN_180171e90(PTR_DAT_1803ffbd0,7,iVar12,"bg_light",CONCAT44(uVar8,1),0x10000);
  }
  lVar9 = param_1 + 0x1d0;
  cVar3 = FUN_180244f90(lVar9);
  if ((cVar3 == '\0') && ((DAT_180c3b701 == '\0' || (DAT_180c3b702 != '\0')))) {
    iVar7 = FUN_1801bce90(lVar9);
    if (iVar7 == 0) {
      return 0;
    }
    cVar3 = FUN_180244ea0(param_1);
    if (cVar3 == '\0') {
LAB_18016dddc:
      cVar3 = FUN_180244ea0(param_1);
      if (cVar3 == '\0') {
LAB_18016de0e:
        piVar10 = (int *)FUN_1800da7e0();
        if ((((*piVar10 != 7) || (cVar3 = FUN_180007450(0xffffffff), cVar3 == '\0')) &&
            (DAT_180c3b702 == '\0')) && (iVar7 = FUN_1801a2b90(), -1 < iVar7)) {
          FUN_1801bd950(lVar9);
          FUN_180245830(lVar9,"CANCEL_CAUTION");
          uVar11 = FUN_1801efd10(0x3f0);
          *(undefined8 *)(param_1 + 0x240) = uVar11;
          FUN_1801be920(lVar9,1);
          *(int *)(param_1 + 600) = iVar7;
          *(undefined1 *)(param_1 + 0x265) = 1;
        }
      }
      else if (*(char *)(param_1 + 0x98) == '\0') {
        uVar8 = FUN_1801a2380(1);
        cVar3 = FUN_1801a6d00(uVar8);
        if (cVar3 == '\0') goto LAB_18016de0e;
      }
    }
    else if (*(char *)(param_1 + 0x68) == '\0') {
      uVar8 = FUN_1801a2380(0);
      cVar3 = FUN_1801a6d00(uVar8);
      if (cVar3 == '\0') goto LAB_18016dddc;
    }
  }
  else {
    piVar10 = (int *)FUN_1800da7e0();
    if ((*piVar10 == 7) && (cVar3 = FUN_180007450(0xffffffff), cVar3 != '\0')) {
      FUN_1802450a0(lVar9);
    }
  }
  if (*(char *)(param_1 + 0x6a) != '\0') {
    FUN_18016e390(param_1,0);
  }
  if (*(char *)(param_1 + 0x9a) != '\0') {
    FUN_18016e390(param_1,1);
  }
  piVar10 = (int *)FUN_1800da7e0();
  if (((*piVar10 == 7) && (cVar3 = FUN_180007450(0xffffffff), cVar3 != '\0')) ||
     ((DAT_180c3b701 != '\0' && (DAT_180c3b702 == '\0')))) {
    cVar3 = FUN_180244ea0(param_1);
    if (cVar3 == '\0') {
LAB_18016df12:
      cVar3 = FUN_180244ea0(param_1);
      if (cVar3 == '\0') {
LAB_18016df4e:
        *(undefined2 *)(PTR_DAT_1803ffbd0 + 0x124) = 0x100;
        goto LAB_18016df5e;
      }
      if (*(char *)(param_1 + 0x98) == '\0') {
        uVar8 = FUN_1801a2380(1);
        cVar3 = FUN_1801a6d00(uVar8);
        if (cVar3 == '\0') goto LAB_18016df4e;
      }
    }
    else if (*(char *)(param_1 + 0x68) == '\0') {
      uVar8 = FUN_1801a2380(0);
      cVar3 = FUN_1801a6d00(uVar8);
      if (cVar3 == '\0') goto LAB_18016df12;
    }
    *(undefined2 *)(PTR_DAT_1803ffbd0 + 0x124) = 0x101;
  }
LAB_18016df5e:
  cVar3 = FUN_1801724a0(lVar1,0);
  cVar4 = FUN_1801724a0(lVar1,1);
  cVar5 = FUN_180172450(lVar1,0);
  cVar6 = FUN_180172450(lVar1,1);
  if (cVar3 == '\0') {
    if (cVar4 == '\0') goto LAB_18016dfa0;
  }
  else {
    if (cVar5 == '\0') goto LAB_18016dfa0;
    if (cVar4 == '\0') goto LAB_18016e004;
  }
  if (cVar6 != '\0') {
LAB_18016e004:
    FUN_180172270(PTR_DAT_1803ffbd0,0);
    *(undefined4 *)(param_1 + 0x58) = 3;
    iVar7 = FUN_18019c090();
    if (iVar7 != 3) {
      return 0;
    }
    iVar7 = FUN_1801a2c10(0x200);
    if (iVar7 != 0) {
      return 0;
    }
    FUN_18019c3c0();
    return 0;
  }
LAB_18016dfa0:
  cVar3 = FUN_180244f90(lVar9);
  if ((cVar3 == '\0') || ((DAT_180c3b701 != '\0' && (DAT_180c3b702 == '\0')))) {
    if (*(char *)(param_1 + 0x6a) != '\0') {
      FUN_18016d370(&DAT_180714940);
    }
    if (*(char *)(param_1 + 0x9a) != '\0') {
      FUN_18016d370(&DAT_180714968);
    }
  }
  return 0;
}



