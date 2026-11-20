// ===================================================
// 1800D72A0  ->  FUN_1800d72a0  (entree 1800d72a0)
// ===================================================

undefined8 FUN_1800d72a0(undefined8 param_1,char *param_2)

{
  char cVar1;
  undefined1 *puVar2;
  undefined1 auVar3 [16];
  ulonglong uVar4;
  int iVar5;
  uint uVar6;
  char *pcVar7;
  undefined8 uVar8;
  uint uVar9;
  char *pcVar10;
  longlong lVar11;
  undefined1 *puVar12;
  longlong lVar13;
  longlong lVar14;
  char *pcVar15;
  uint uVar16;
  uint uVar17;
  char *pcVar18;
  bool bVar19;
  uint local_res10 [4];
  uint local_res20;
  uint local_298;
  undefined4 local_294;
  undefined4 local_290;
  undefined4 local_28c;
  undefined1 local_288 [4];
  undefined4 uStack_284;
  undefined4 uStack_280;
  undefined4 uStack_27c;
  undefined8 local_278;
  ulonglong local_270;
  undefined1 local_268;
  undefined7 uStack_267;
  longlong local_258;
  undefined8 local_250;
  undefined *local_248 [2];
  undefined1 local_238 [124];
  undefined4 local_1bc;
  undefined **local_1b8 [12];
  undefined8 local_158;
  undefined1 local_150 [24];
  char local_138 [256];
  
  local_158 = 0xfffffffffffffffe;
  uVar17 = 0;
  local_res20 = 0;
  FUN_180218880(local_150,0);
  uVar16 = local_res10[0];
  uVar6 = uVar17;
  do {
    pcVar18 = (char *)0x0;
    pcVar10 = pcVar18;
    pcVar7 = local_138;
    if (param_2 != (char *)0x0) {
      do {
        pcVar15 = pcVar7;
        cVar1 = *param_2;
        *pcVar15 = cVar1;
        param_2 = param_2 + 1;
        if ((cVar1 == '\0') || (cVar1 == '\n')) break;
        uVar9 = (int)pcVar10 + 1;
        pcVar10 = (char *)(ulonglong)uVar9;
        pcVar7 = pcVar15 + 1;
      } while ((int)uVar9 < 0xff);
      *pcVar15 = '\0';
      pcVar10 = pcVar18;
      do {
        pcVar7 = pcVar10;
        bVar19 = local_138[(longlong)pcVar7] == pcVar7[0x18039fc3c];
        if (!bVar19) goto LAB_1800d7369;
        pcVar10 = pcVar7 + 1;
      } while (pcVar7 + 1 != &DAT_00000004);
      bVar19 = local_138[(longlong)pcVar7] == pcVar7[0x18039fc3c];
LAB_1800d7369:
      pcVar10 = param_2;
      if (bVar19) {
        pcVar10 = pcVar18;
      }
    }
    if (pcVar10 == (char *)0x0) {
      FUN_180218900(local_150);
      return 0;
    }
    local_278 = 0;
    local_270 = 0xf;
    auVar3[0xf] = 0;
    auVar3._0_15_ = stack0xfffffffffffffd79;
    _local_288 = auVar3 << 8;
    lVar13 = -1;
    do {
      lVar14 = lVar13 + 1;
      lVar13 = lVar13 + 1;
    } while (local_138[lVar14] != '\0');
    FUN_180010a10(local_288,local_138);
    local_248[0] = &DAT_18034a508;
    local_res20 = uVar6 | 1;
    local_1b8[0] = std::basic_istream<char,std::char_traits<char>_>::vftable;
    local_1bc = 0x78;
    local_248[1] = (undefined *)0x0;
    FUN_1800112a0(local_1b8,local_238,0);
    *(undefined ***)((longlong)local_248 + (longlong)*(int *)(local_248[0] + 4)) =
         std::basic_istringstream<char,std::char_traits<char>,std::allocator<char>_>::vftable;
    *(int *)((longlong)&local_250 + (longlong)*(int *)(local_248[0] + 4) + 4) =
         *(int *)(local_248[0] + 4) + -0x90;
    FUN_180033370(local_238,local_288,1);
    if (0xf < local_270) {
      if (0xfff < local_270 + 1) {
        if (0x1f < (_local_288 - *(longlong *)(_local_288 + -8)) - 8U) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(*(longlong *)(_local_288 + -8),local_270 + 0x28);
        }
      }
      FUN_1802fdd80();
    }
    local_258 = 0;
    local_250 = 0xf;
    local_268 = 0;
    FUN_1800d5ac0(local_248,&local_268);
    uVar4 = local_250;
    lVar13 = local_258;
    puVar2 = (undefined1 *)CONCAT71(uStack_267,local_268);
    puVar12 = &local_268;
    if (0xf < local_250) {
      puVar12 = puVar2;
    }
    if ((local_258 == 0xb) && (iVar5 = memcmp(puVar12,"group_start",0xb), iVar5 == 0)) {
      local_res10[0] = uVar16;
      FUN_1800d5d50(local_248,local_res10);
      uVar16 = local_res10[0];
      uVar17 = local_res10[0];
    }
    puVar12 = &local_268;
    if (0xf < uVar4) {
      puVar12 = puVar2;
    }
    if (lVar13 == 4) {
      lVar14 = 0;
      do {
        lVar11 = lVar14 + 1;
        if (puVar12[lVar14] != (&DAT_18039fadc)[lVar14]) {
          uVar6 = -(uint)((byte)puVar12[lVar14] < (byte)(&DAT_18039fadc)[lVar14]) | 1;
          goto LAB_1800d751d;
        }
        lVar14 = lVar11;
      } while (lVar11 != 4);
      uVar6 = 0;
LAB_1800d751d:
      if (uVar6 == 0) {
        local_res10[0] = local_298;
        FUN_1800d5d50(local_248,local_res10);
        uVar6 = local_res10[0];
        local_298 = local_res10[0];
        uVar8 = FUN_180088160(uVar17);
        FUN_180088420(uVar8,uVar6);
      }
    }
    puVar12 = &local_268;
    if (0xf < uVar4) {
      puVar12 = puVar2;
    }
    if ((lVar13 == 7) && (iVar5 = memcmp(puVar12,"density",7), iVar5 == 0)) {
      FUN_1800d5f40(local_248,&local_294);
      uVar8 = FUN_180088160(uVar17);
      FUN_1800881c0(uVar8,local_294);
    }
    puVar12 = &local_268;
    if (0xf < uVar4) {
      puVar12 = puVar2;
    }
    if (lVar13 == 6) {
      lVar14 = 0;
      do {
        lVar11 = lVar14 + 1;
        if (puVar12[lVar14] != "linear"[lVar14]) {
          uVar6 = -(uint)((byte)puVar12[lVar14] < (byte)"linear"[lVar14]) | 1;
          goto LAB_1800d75dd;
        }
        lVar14 = lVar11;
      } while (lVar11 != 6);
      uVar6 = 0;
LAB_1800d75dd:
      if (uVar6 == 0) {
        FUN_1800d5f40(local_248,&local_290);
        FUN_1800d5f40(local_248,&local_28c);
        uVar8 = FUN_180088160(uVar17);
        FUN_180088400(uVar8,local_290);
        FUN_1800881d0(uVar8,local_28c);
      }
    }
    puVar12 = &local_268;
    if (0xf < uVar4) {
      puVar12 = puVar2;
    }
    if (lVar13 == 5) {
      lVar13 = 0;
      do {
        lVar14 = lVar13 + 1;
        if (puVar12[lVar13] != "color"[lVar13]) {
          uVar6 = -(uint)((byte)puVar12[lVar13] < (byte)"color"[lVar13]) | 1;
          goto LAB_1800d766e;
        }
        lVar13 = lVar14;
      } while (lVar14 != 5);
      uVar6 = 0;
LAB_1800d766e:
      if (uVar6 == 0) {
        _local_288 = ZEXT812(0);
        uStack_27c = 0;
        FUN_1800d5f40(local_248,local_288);
        FUN_1800d5f40(local_248,&uStack_284);
        FUN_1800d5f40(local_248,&uStack_280);
        FUN_1800d5f40(local_248,&uStack_27c);
        uVar8 = FUN_180088160(uVar17);
        FUN_1800881a0(uVar8,local_288,uStack_284,uStack_280,uStack_27c);
      }
    }
    if (0xf < uVar4) {
      puVar12 = puVar2;
      if ((0xfff < uVar4 + 1) &&
         (puVar12 = *(undefined1 **)(puVar2 + -8),
         (undefined1 *)0x1f < puVar2 + (-8 - (longlong)puVar12))) {
                    /* WARNING: Subroutine does not return */
        FUN_180303af0();
      }
      FUN_1802fdd80(puVar12);
    }
    *(undefined ***)((longlong)local_248 + (longlong)*(int *)(local_248[0] + 4)) =
         std::basic_istringstream<char,std::char_traits<char>,std::allocator<char>_>::vftable;
    *(int *)((longlong)&local_250 + (longlong)*(int *)(local_248[0] + 4) + 4) =
         *(int *)(local_248[0] + 4) + -0x90;
    FUN_18000de80(local_238);
    *(undefined ***)((longlong)local_248 + (longlong)*(int *)(local_248[0] + 4)) =
         std::basic_istream<char,std::char_traits<char>_>::vftable;
    *(int *)((longlong)&local_250 + (longlong)*(int *)(local_248[0] + 4) + 4) =
         *(int *)(local_248[0] + 4) + -0x18;
    local_1b8[0] = std::ios_base::vftable;
    std::ios_base::_Ios_base_dtor((ios_base *)local_1b8);
    param_2 = pcVar10;
    uVar6 = local_res20;
  } while( true );
}



