/* FUN_1801cfeb0  --  VF5FS+0x1cfeb0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801cfeb0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


ulonglong FUN_1801cfeb0(void)

{
  char cVar1;
  char cVar2;
  char cVar3;
  char cVar4;
  char cVar5;
  char cVar6;
  char cVar7;
  char cVar8;
  char cVar9;
  char cVar10;
  char cVar11;
  char cVar12;
  int iVar13;
  longlong *plVar14;
  longlong lVar15;
  longlong lVar16;
  longlong lVar17;
  longlong lVar18;
  longlong *plVar19;
  int iVar20;
  int iVar21;
  int iVar22;
  longlong *_Buf1;
  longlong lVar23;
  bool bVar24;
  undefined4 local_res8 [2];
  int local_res10;
  undefined1 local_res14;
  undefined2 local_res15;
  undefined1 local_res17;
  int local_res18;
  int local_res20;
  longlong local_68;
  longlong local_58;
  
  plVar19 = DAT_180796db0;
  local_res15 = 0;
  local_res17 = 0;
  local_res8[0] = (undefined4)DAT_180796db0[0x12d6];
  local_res14 = 0;
  local_res10 = 0;
  FUN_1801b2150(0,0,local_res8,0,0);
  local_res14 = (undefined1)local_res8[0];
  if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
    (**(code **)(DAT_180c8df28 + 0x1ff08))
              (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xf1,&local_res10);
  }
  local_res14 = 0;
  local_res15 = 0;
  local_res17 = 0;
  local_res8[0] = *(undefined4 *)((longlong)plVar19 + 0x96f4);
  local_res10 = 1;
  FUN_1801b2150(1,0,local_res8,0,0);
  local_res14 = (undefined1)local_res8[0];
  if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
    (**(code **)(DAT_180c8df28 + 0x1ff08))
              (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xf1,&local_res10);
  }
  plVar14 = (longlong *)DAT_180796db0[0x2246];
  if (plVar14 != (longlong *)0x0) {
    local_58 = *plVar14 - *plVar19;
    if (local_58 == 0) {
      local_58 = (ulonglong)*(uint *)(plVar14 + 1) - (ulonglong)*(uint *)(plVar19 + 1);
    }
    iVar22 = *(int *)((longlong)plVar14 + 0xc);
    iVar13 = *(int *)((longlong)plVar19 + 0xc);
    local_res20 = memcmp(plVar14 + 2,plVar19 + 2,0x4b18);
    local_68 = plVar14[0x965] - plVar19[0x965];
    if ((local_68 == 0) && (local_68 = plVar14[0x966] - plVar19[0x966], local_68 == 0)) {
      local_68 = (ulonglong)*(uint *)(plVar14 + 0x967) - (ulonglong)*(uint *)(plVar19 + 0x967);
    }
    local_res18 = memcmp((void *)((longlong)plVar14 + 0x4b3c),(void *)((longlong)plVar19 + 0x4b3c),
                         0x450);
    lVar15 = *(longlong *)((longlong)plVar14 + 0x4f8c);
    lVar16 = *(longlong *)((longlong)plVar19 + 0x4f8c);
    local_res10 = memcmp((void *)((longlong)plVar14 + 0x4f94),(void *)((longlong)plVar19 + 0x4f94),
                         0x32);
    cVar1 = *(char *)((longlong)plVar14 + 0x4fc6);
    cVar2 = *(char *)((longlong)plVar14 + 0x4fc7);
    cVar3 = *(char *)((longlong)plVar14 + 0x4fcc);
    cVar4 = *(char *)((longlong)plVar14 + 0x9594);
    cVar5 = *(char *)((longlong)plVar14 + 0x9595);
    lVar17 = plVar14[0x9f9];
    cVar6 = *(char *)((longlong)plVar14 + 0x9596);
    lVar18 = plVar19[0x9f9];
    cVar7 = *(char *)((longlong)plVar19 + 0x4fc6);
    cVar8 = *(char *)((longlong)plVar19 + 0x4fc7);
    cVar9 = *(char *)((longlong)plVar19 + 0x4fcc);
    cVar10 = *(char *)((longlong)plVar19 + 0x9594);
    cVar11 = *(char *)((longlong)plVar19 + 0x9595);
    cVar12 = *(char *)((longlong)plVar19 + 0x9596);
    iVar20 = memcmp((void *)((longlong)plVar14 + 0x95d4),(void *)((longlong)plVar19 + 0x95d4),0x88);
    iVar21 = memcmp((void *)((longlong)plVar14 + 0x965c),(void *)((longlong)plVar19 + 0x965c),0x4c);
    lVar23 = 2;
    _Buf1 = plVar14 + 0x12d6;
    bVar24 = (((((((((((((((plVar14[0x12d5] != plVar19[0x12d5] || iVar21 != 0) || iVar20 != 0) ||
                         cVar6 != cVar12) || cVar5 != cVar11) || cVar4 != cVar10) || cVar3 != cVar9)
                     || (int)lVar17 != (int)lVar18) || cVar2 != cVar8) || cVar1 != cVar7) ||
                  local_res10 != 0) || lVar15 != lVar16) || local_res18 != 0) || local_68 != 0) ||
              local_res20 != 0) || iVar22 != iVar13) || local_58 != 0;
    do {
      iVar22 = memcmp(_Buf1,(void *)(((longlong)plVar19 - (longlong)plVar14) + (longlong)_Buf1),0x44
                     );
      _Buf1 = (longlong *)((longlong)_Buf1 + 0x44);
      bVar24 = (bool)(bVar24 | iVar22 != 0);
      lVar23 = lVar23 + -1;
    } while (lVar23 != 0);
    return (ulonglong)
           CONCAT11((char)((ushort)(short)plVar19[0x12eb] >> 8),
                    ((short)plVar14[0x12e7] != (short)plVar19[0x12eb] ||
                    *(short *)((longlong)plVar14 + 0x973a) != *(short *)((longlong)plVar19 + 0x975a)
                    ) | bVar24);
  }
  return (ulonglong)DAT_180796db0 & 0xffffffffffffff00;
}
