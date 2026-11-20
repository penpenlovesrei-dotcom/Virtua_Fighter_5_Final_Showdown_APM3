/* SelChara_PasGrillePort  --  VF5FS+0x181fe0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180181fe0.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void SelChara_PasGrillePort(longlong param_1,int param_2)

{
  char cVar1;
  uint uVar2;
  undefined4 uVar3;
  int iVar4;
  undefined8 *puVar5;
  longlong lVar6;
  uint *puVar7;
  uint uVar8;
  undefined8 *puVar9;
  ulonglong uVar10;
  undefined8 *puVar11;
  uint uVar12;
  uint uVar13;
  undefined8 *puVar14;
  char *pcVar15;
  byte bVar16;
  undefined8 *puVar17;
  uint uVar18;
  int local_res8;
  undefined4 local_res18;
  int local_res20;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined1 local_90 [16];
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined1 local_60 [16];
  
  puVar9 = (undefined8 *)0x0;
  puVar17 = (undefined8 *)0x0;
  pcVar15 = (char *)(((longlong)param_2 + 2) * 0x40 + param_1);
  if (*pcVar15 == '\0') {
    return;
  }
  if (*(int *)(pcVar15 + 0x20) == 6) {
    return;
  }
  if (*(int *)(pcVar15 + 0x20) == 7) {
    return;
  }
  if (*(int *)(pcVar15 + 0x28) == 6) {
    return;
  }
  if (*(longlong **)(pcVar15 + 8) == (longlong *)0x0) {
    return;
  }
  if (**(longlong **)(pcVar15 + 8) == 0) {
    return;
  }
  if (*(char *)((longlong)param_2 * 0x40 + 0x81 + param_1) == '\0') {
    return;
  }
  if (DAT_180759a59 != '\0') {
    return;
  }
  if (DAT_180759a5a != '\0') {
    return;
  }
  if (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0) {
    uStack_70 = 0;
    uStack_68 = 0;
    local_80 = 0xd;
    uStack_78 = 0xa000000;
    local_60 = (undefined1  [16])0x0;
    if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
      (**(code **)(DAT_180c8df28 + 0x1ff08))(*(undefined8 *)(DAT_180c8df28 + 0x1ff10),8,&local_80);
      if ((((uStack_78._3_1_ == '\v') && (param_2 == 1)) && (*(int *)(param_1 + 0xa0) != 6)) &&
         ((*(int *)(param_1 + 0xa0) != 7 && (*(int *)(param_1 + 0xa8) != 6)))) {
        return;
      }
    }
    if (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0) {
      uStack_70 = 0;
      uStack_68 = 0;
      uStack_78 = 0x10000;
      local_80 = (ulonglong)CONCAT14((char)param_2,0xd);
      local_60 = (undefined1  [16])0x0;
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))(*(undefined8 *)(DAT_180c8df28 + 0x1ff10),6,&local_80)
        ;
        if (uStack_78._2_1_ == '\0') {
          return;
        }
      }
    }
  }
  local_res8 = 0;
  local_res20 = 0;
  uVar12 = *(uint *)**(undefined8 **)(pcVar15 + 8);
  uVar2 = uVar12 & 0xff;
  uVar18 = ((uint *)**(undefined8 **)(pcVar15 + 8))[1];
  uVar8 = uVar18 & 0xff;
  uStack_a8 = 0;
  uStack_a0 = 0;
  uStack_98 = 0;
  local_90 = (undefined1  [16])0x0;
  local_b0 = (ulonglong)CONCAT21(CONCAT11((char)uVar18,(char)uVar12),(char)param_2) << 0x20;
  if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
    (**(code **)(DAT_180c8df28 + 0x1ff08))(*(undefined8 *)(DAT_180c8df28 + 0x1ff10),8,&local_b0);
    uVar8 = (uint)local_b0._6_1_;
    uVar2 = (uint)local_b0._5_1_;
  }
  puVar14 = puVar9;
  if (((uStack_a8._3_1_ == '\x01') &&
      ((puVar9 = (undefined8 *)0x1, puVar14 = puVar17, uVar2 != uVar12 || (uVar8 != uVar18)))) &&
     (puVar5 = *(undefined8 **)(param_1 + 0x58), uVar12 = uVar2, uVar18 = uVar8,
     puVar5 != (undefined8 *)0x0)) {
    uVar10 = 0;
    if (*(ulonglong *)(param_1 + 0x70) != 0) {
      do {
        puVar7 = (uint *)*puVar5;
        puVar14 = puVar17;
        if ((puVar7 == (uint *)0x0) ||
           (((*(char *)((longlong)puVar5 + 0x14) == '\0' && (*puVar7 == uVar2)) &&
            (puVar14 = puVar5, puVar7[1] == uVar8)))) break;
        uVar10 = uVar10 + 1;
        puVar5 = puVar5 + 3;
        puVar14 = puVar17;
      } while (uVar10 < *(ulonglong *)(param_1 + 0x70));
    }
  }
  cVar1 = (char)puVar9;
  uVar2 = Entree_SlotDuPort(param_2);
  local_res18 = 2;
  if (uVar2 < 2) {
    Entree_RestreindreAuSlot(uVar2);
    uVar8 = Entree_QuelSlotAValide();
    if (uVar8 == uVar2) {
      cVar1 = '\x01';
    }
    Entree_RestreindreAuSlot(2);
  }
  if (cVar1 != '\0') {
    *(undefined8 *)(pcVar15 + 0x18) = *(undefined8 *)(pcVar15 + 8);
    pcVar15[0x28] = '\x06';
    pcVar15[0x29] = '\0';
    pcVar15[0x2a] = '\0';
    pcVar15[0x2b] = '\0';
    if (puVar14 == (undefined8 *)0x0) {
      return;
    }
    *(undefined8 **)(pcVar15 + 0x18) = puVar14;
    return;
  }
  if (uStack_a8._3_1_ != '\x02') {
    if ((local_b0._5_1_ != uVar12) || (local_b0._6_1_ != uVar18)) {
      lVar6 = FUN_180182c50(param_1,local_b0._5_1_,local_b0._6_1_);
      if (lVar6 == 0) {
        return;
      }
      pcVar15[0x28] = '\x05';
      pcVar15[0x29] = '\0';
      pcVar15[0x2a] = '\0';
      pcVar15[0x2b] = '\0';
      *(longlong *)(pcVar15 + 0x18) = lVar6;
      return;
    }
  }
  uVar3 = Entree_SlotDuPort(param_2);
  cVar1 = Entree_EtatMaintenu(uVar3,0x10000000);
  if (cVar1 == '\0') {
    cVar1 = Entree_EtatMaintenu(uVar3,0x20000000);
    if (cVar1 == '\0') {
      cVar1 = Entree_EtatMaintenu(uVar3,0x40000000);
      if (cVar1 == '\0') {
        cVar1 = Entree_EtatMaintenu(uVar3,0x80000000);
        if (cVar1 == '\0') {
          pcVar15[0x30] = '\0';
          pcVar15[0x31] = '\0';
          pcVar15[0x32] = '\0';
          pcVar15[0x33] = '\0';
          pcVar15[0x34] = '\0';
          pcVar15[0x35] = '\0';
          pcVar15[0x36] = '\0';
          pcVar15[0x37] = '\0';
          return;
        }
        if (*(int *)(pcVar15 + 0x30) == -0x80000000) {
          iVar4 = *(int *)(pcVar15 + 0x34);
          if (iVar4 != 0) goto LAB_180182434;
          uVar3 = 10;
        }
        else {
          uVar3 = 0x14;
        }
        *(undefined4 *)(pcVar15 + 0x34) = uVar3;
        local_res8 = 1;
        local_res18 = 5;
        pcVar15[0x30] = '\0';
        pcVar15[0x31] = '\0';
        pcVar15[0x32] = '\0';
        pcVar15[0x33] = -0x80;
      }
      else {
        if (*(int *)(pcVar15 + 0x30) == 0x40000000) {
          iVar4 = *(int *)(pcVar15 + 0x34);
          if (iVar4 != 0) {
LAB_180182434:
            *(int *)(pcVar15 + 0x34) = iVar4 + -1;
            return;
          }
          uVar3 = 10;
        }
        else {
          uVar3 = 0x14;
        }
        *(undefined4 *)(pcVar15 + 0x34) = uVar3;
        pcVar15[0x30] = '\0';
        pcVar15[0x31] = '\0';
        pcVar15[0x32] = '\0';
        pcVar15[0x33] = '@';
        local_res8 = -1;
        local_res18 = 4;
      }
    }
    else {
      if (*(int *)(pcVar15 + 0x30) == 0x20000000) {
        iVar4 = *(int *)(pcVar15 + 0x34);
        if (iVar4 != 0) goto LAB_180182434;
        uVar3 = 10;
      }
      else {
        uVar3 = 0x14;
      }
      *(undefined4 *)(pcVar15 + 0x34) = uVar3;
      cVar1 = FUN_1802cb780();
      if ((cVar1 == '\0') || (*(char *)(param_1 + 0x101) == '\0')) {
        local_res20 = 1;
      }
      else {
        local_res8 = -1;
      }
      local_res18 = 3;
      pcVar15[0x30] = '\0';
      pcVar15[0x31] = '\0';
      pcVar15[0x32] = '\0';
      pcVar15[0x33] = ' ';
    }
  }
  else {
    if (*(int *)(pcVar15 + 0x30) == 0x10000000) {
      iVar4 = *(int *)(pcVar15 + 0x34);
      if (iVar4 != 0) goto LAB_180182434;
      uVar3 = 10;
    }
    else {
      uVar3 = 0x14;
    }
    *(undefined4 *)(pcVar15 + 0x34) = uVar3;
    cVar1 = FUN_1802cb780();
    if ((cVar1 == '\0') || (*(char *)(param_1 + 0x101) == '\0')) {
      local_res20 = -1;
    }
    else {
      local_res8 = 1;
    }
    pcVar15[0x30] = '\0';
    pcVar15[0x31] = '\0';
    pcVar15[0x32] = '\0';
    pcVar15[0x33] = '\x10';
  }
  uVar2 = 10;
  if (*(char *)(param_1 + 0x100) == '\0') goto LAB_180182589;
  uVar18 = uVar18 + local_res20;
  if (*(char *)(param_1 + 0x101) == '\0') {
    if ((int)uVar18 < 0) {
      uVar8 = 0;
      uVar18 = 1;
    }
    else {
      if ((int)uVar18 < 2) {
        uVar8 = (uint)(uVar18 != 1);
        if (uVar18 == 1) goto LAB_180182507;
      }
      else {
        uVar18 = 0;
        uVar8 = 1;
      }
      cVar1 = FUN_1801aa370();
      if (cVar1 == '\0') {
        uVar2 = 9;
      }
    }
LAB_180182507:
    uVar13 = uVar12 + local_res8;
    uVar12 = uVar2;
    if (local_res20 == 0) {
      if (((int)uVar8 <= (int)uVar13) && (uVar12 = uVar13, (int)uVar2 < (int)uVar13)) {
        uVar12 = uVar8;
      }
    }
    else {
      if ((int)uVar13 < (int)uVar8) {
        uVar13 = uVar8;
      }
      if ((int)uVar13 < (int)uVar2) {
        uVar12 = uVar13;
      }
    }
  }
  else {
    uVar2 = 1;
    if ((-1 < (int)uVar18) && (uVar2 = uVar18, 1 < (int)uVar18)) {
      uVar2 = 0;
    }
    uVar18 = uVar2;
    uVar12 = uVar12 + local_res8;
    if ((int)uVar12 < 0) {
      uVar12 = 10;
    }
    else if (10 < (int)uVar12) {
      uVar12 = 0;
    }
  }
  puVar9 = *(undefined8 **)(param_1 + 0x58);
  uVar10 = 0;
  if (((puVar9 != (undefined8 *)0x0) && (*(ulonglong *)(param_1 + 0x70) != 0)) &&
     (puVar7 = (uint *)*puVar9, puVar7 != (uint *)0x0)) {
    while (((*(char *)((longlong)puVar9 + 0x14) != '\0' || (*puVar7 != uVar12)) ||
           (puVar7[1] != uVar18))) {
      uVar10 = uVar10 + 1;
      puVar9 = puVar9 + 3;
      if ((*(ulonglong *)(param_1 + 0x70) <= uVar10) ||
         (puVar7 = (uint *)*puVar9, puVar7 == (uint *)0x0)) goto LAB_180182589;
    }
    if (puVar9 != (undefined8 *)0x0) {
      lVar6 = ((longlong)param_2 + 2) * 0x40;
      *(undefined4 *)(lVar6 + 0x28 + param_1) = local_res18;
      *(undefined8 **)(lVar6 + 0x18 + param_1) = puVar9;
      return;
    }
  }
LAB_180182589:
  if ((int)uVar18 < (int)*(uint *)(param_1 + 100)) {
    uVar18 = *(uint *)(param_1 + 0x6c);
  }
  else if (*(int *)(param_1 + 0x6c) < (int)uVar18) {
    uVar18 = *(uint *)(param_1 + 100);
  }
  uVar2 = 0xffffffff;
  if (local_res8 != 0) {
    do {
      uVar8 = uVar2;
      cVar1 = FUN_1802cb780();
      if ((cVar1 != '\0') && (*(char *)(param_1 + 0x101) != '\0')) {
        uVar2 = uVar18 + 1;
        if ((int)uVar2 < (int)*(uint *)(param_1 + 100)) {
          uVar2 = *(uint *)(param_1 + 0x6c);
        }
        else if (*(int *)(param_1 + 0x6c) < (int)uVar2) {
          uVar2 = *(uint *)(param_1 + 100);
        }
        puVar9 = *(undefined8 **)(param_1 + 0x58);
        uVar10 = 0;
        if ((puVar9 != (undefined8 *)0x0) && (*(ulonglong *)(param_1 + 0x70) != 0)) {
          puVar7 = (uint *)*puVar9;
          while (puVar7 != (uint *)0x0) {
            if (((*(char *)((longlong)puVar9 + 0x14) == '\0') && (*puVar7 == uVar12)) &&
               (puVar7[1] == uVar2)) goto LAB_180182817;
            uVar10 = uVar10 + 1;
            puVar9 = puVar9 + 3;
            if (*(ulonglong *)(param_1 + 0x70) <= uVar10) break;
            puVar7 = (uint *)*puVar9;
          }
        }
      }
      uVar10 = 0;
      uVar12 = local_res8 + uVar12;
      if ((int)uVar12 < (int)*(uint *)(param_1 + 0x60)) {
        uVar12 = *(uint *)(param_1 + 0x68);
      }
      else if (*(int *)(param_1 + 0x68) < (int)uVar12) {
        uVar12 = *(uint *)(param_1 + 0x60);
      }
      puVar9 = *(undefined8 **)(param_1 + 0x58);
      if ((puVar9 != (undefined8 *)0x0) && (*(ulonglong *)(param_1 + 0x70) != 0)) {
        puVar7 = (uint *)*puVar9;
        while (puVar7 != (uint *)0x0) {
          if (((*(char *)((longlong)puVar9 + 0x14) == '\0') && (*puVar7 == uVar12)) &&
             (puVar7[1] == uVar18)) goto LAB_180182817;
          uVar10 = uVar10 + 1;
          puVar9 = puVar9 + 3;
          if (*(ulonglong *)(param_1 + 0x70) <= uVar10) break;
          puVar7 = (uint *)*puVar9;
        }
      }
      if (local_res8 == 0) {
        local_res8 = 1;
      }
      if (local_res20 == 0) {
        local_res20 = 1;
      }
      uVar2 = uVar12;
      if ((-1 < (int)uVar8) && (uVar2 = uVar8, uVar8 == uVar12)) {
        uVar18 = local_res20 + uVar18;
        local_res8 = 0;
        if ((int)uVar18 < (int)*(uint *)(param_1 + 100)) {
          uVar18 = *(uint *)(param_1 + 0x6c);
        }
        else if (*(int *)(param_1 + 0x6c) < (int)uVar18) {
          uVar18 = *(uint *)(param_1 + 100);
        }
      }
    } while( true );
  }
  uVar2 = *(uint *)(param_1 + 0x68);
  puVar17 = *(undefined8 **)(param_1 + 0x58);
  uVar8 = uVar12;
  do {
    puVar9 = (undefined8 *)0x0;
    uVar8 = uVar8 + 1;
    uVar12 = uVar12 - 1;
    uVar13 = uVar8;
    if ((int)uVar2 < (int)uVar8) {
      uVar13 = uVar2;
    }
    bVar16 = (int)uVar2 < (int)uVar8;
    if (puVar17 != (undefined8 *)0x0) {
      puVar14 = puVar9;
      if ((*(undefined8 **)(param_1 + 0x70) != (undefined8 *)0x0) &&
         (puVar7 = (uint *)*puVar17, puVar5 = puVar17, puVar11 = puVar9, puVar7 != (uint *)0x0)) {
        while ((*(char *)((longlong)puVar5 + 0x14) != '\0' ||
               ((*puVar7 != uVar13 || (puVar14 = puVar5, puVar7[1] != uVar18))))) {
          puVar14 = puVar9;
          if ((*(undefined8 **)(param_1 + 0x70) <= (undefined8 *)((longlong)puVar11 + 1)) ||
             (puVar7 = (uint *)puVar5[3], puVar5 = puVar5 + 3,
             puVar11 = (undefined8 *)((longlong)puVar11 + 1), puVar7 == (uint *)0x0)) break;
        }
      }
      if (puVar14 != (undefined8 *)0x0) {
        lVar6 = ((longlong)param_2 + 2) * 0x40;
        *(undefined4 *)(lVar6 + 0x28 + param_1) = local_res18;
        *(undefined8 **)(lVar6 + 0x18 + param_1) = puVar14;
        return;
      }
    }
    uVar10 = 0;
    uVar13 = uVar12;
    if ((int)uVar12 < (int)*(uint *)(param_1 + 0x60)) {
      bVar16 = bVar16 + 1;
      uVar13 = *(uint *)(param_1 + 0x60);
    }
    if ((puVar17 != (undefined8 *)0x0) && (*(ulonglong *)(param_1 + 0x70) != 0)) {
      puVar7 = (uint *)*puVar17;
      puVar9 = puVar17;
      while (puVar7 != (uint *)0x0) {
        if (((*(char *)((longlong)puVar9 + 0x14) == '\0') && (*puVar7 == uVar13)) &&
           (puVar7[1] == uVar18)) {
LAB_180182817:
          lVar6 = ((longlong)param_2 + 2) * 0x40;
          *(undefined4 *)(lVar6 + 0x28 + param_1) = local_res18;
          *(undefined8 **)(lVar6 + 0x18 + param_1) = puVar9;
          return;
        }
        uVar10 = uVar10 + 1;
        puVar9 = puVar9 + 3;
        if (*(ulonglong *)(param_1 + 0x70) <= uVar10) break;
        puVar7 = (uint *)*puVar9;
      }
    }
    if (1 < bVar16) {
      return;
    }
  } while( true );
}
