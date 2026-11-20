// ===================================================
// 18025C201  ->  FUN_18025c190  (entree 18025c190)
// ===================================================

void FUN_18025c190(longlong param_1,longlong param_2)

{
  longlong lVar1;
  longlong *plVar2;
  ulonglong uVar3;
  ulonglong uVar4;
  ulonglong uVar5;
  uint uVar6;
  uint uVar7;
  longlong lVar8;
  ulonglong uVar9;
  int iVar10;
  ulonglong uVar11;
  ulonglong uVar12;
  uint *puVar13;
  ulonglong uVar14;
  uint uVar15;
  uint *puVar16;
  ulonglong uVar17;
  ulonglong uVar18;
  ulonglong uVar19;
  ulonglong uVar20;
  ulonglong local_res8;
  int local_res18;
  undefined8 local_178;
  uint uStack_170;
  ulonglong local_168;
  ulonglong local_160;
  longlong local_150;
  undefined8 local_148 [16];
  longlong alStack_c8 [17];
  
  uVar9 = *(ulonglong *)(param_1 + 8);
  uVar12 = 0;
  *(undefined8 *)(param_1 + 8) = 0;
  *(longlong *)(param_1 + 0xec8) = param_2;
  local_150 = -1;
  local_res18 = -1;
  if ((*(ushort *)(param_2 + 0xe) >> 0xe & 1) != 0) {
    lVar1 = *(longlong *)(param_2 + 0x18);
    (**(code **)(**(longlong **)(param_1 + 0x18) + 0xb8))
              (*(longlong **)(param_1 + 0x18),*(undefined8 *)(lVar1 + 0x58),0,0);
    uVar4 = *(ulonglong *)(lVar1 + 8);
    puVar16 = (uint *)(lVar1 + 0x18);
    uVar15 = (uint)(uVar4 >> 0x20) & 0xf;
    if ((uVar4 & 0xf00000000) != 0) {
      do {
        uVar15 = uVar15 - 1;
        uVar7 = *puVar16 >> 4;
        puVar13 = (uint *)(param_1 + 0x268 + (ulonglong)(*puVar16 & 0xf) * 0x10);
        uVar6 = *puVar13;
        puVar13[2] = uVar7 & 7;
        if ((uVar6 & 0x10) == 0) {
          uVar6 = uVar6 & 0xfffffff8 | (uVar7 & 7) >> 2 | (uVar7 & 1) << 2 | uVar7 & 2;
          *puVar13 = uVar6;
        }
        uVar6 = (*puVar16 * 2 ^ uVar6) & 0x700 ^ uVar6;
        *puVar13 = uVar6;
        uVar6 = (*puVar16 * 2 ^ uVar6) & 0x3800 ^ uVar6;
        *puVar13 = uVar6;
        uVar6 = (*puVar16 * 2 ^ uVar6) & 0x1c000 ^ uVar6;
        *puVar13 = uVar6;
        uVar7 = (*puVar16 << 5 ^ uVar6) & 0x1ffffff ^ *puVar16 << 5;
        *puVar13 = uVar7;
        uVar6 = *puVar16;
        puVar16 = puVar16 + 1;
        *puVar13 = (uVar6 * 2 ^ uVar7) & 0x1e0000 ^ uVar7;
      } while (uVar15 != 0);
      uVar4 = (ulonglong)*(uint *)(lVar1 + 8);
    }
    if ((uVar9 & 0xffff0000) != 0 || (uVar4 & 0xffff) != 0) {
      local_res8 = 0;
      uVar17 = -1;
      uVar19 = (uVar9 & 0xffff0000 | (uVar4 & 0xffff) << 0x10) >> 0x10;
      iVar10 = -1;
      local_168 = 0;
      uVar9 = uVar9 & 0xffffffff0000ffff;
      local_160 = -1;
      uVar4 = uVar12;
      uVar3 = uVar12;
      uVar20 = uVar12;
      if (uVar19 != 0) {
        do {
          uVar11 = 0;
          if (uVar19 != 0) {
            for (; (uVar19 >> uVar11 & 1) == 0; uVar11 = uVar11 + 1) {
            }
          }
          uVar11 = uVar11 & 0xffffffff;
          if (uVar19 == 0) {
            uVar11 = 0x40;
          }
          lVar8 = uVar11 * 0x10 + param_1;
          lVar1 = *(longlong *)(param_1 + 0x1ae8 + uVar11 * 8);
          local_178 = *(longlong *)(lVar8 + 0x268);
          uStack_170 = (uint)*(undefined8 *)(lVar8 + 0x270);
          if ((lVar1 != 0) && ((*(uint *)(lVar1 + 0x18) & 0xf0000000) == 0x10000000)) {
            local_178._4_4_ = (undefined4)((ulonglong)local_178 >> 0x20);
            local_178 = CONCAT44(local_178._4_4_,
                                 uStack_170 >> 2 & 1 | (uStack_170 & 1) << 2 |
                                 (uint)local_178 & 0xfe1fffe8 | uStack_170 & 2);
          }
          if (*(longlong *)(lVar8 + 0xa58) != local_178) {
            *(longlong *)(lVar8 + 0xa58) = local_178;
            *(uint *)(lVar8 + 0xa60) = uStack_170;
            if (uVar17 != local_178) {
              local_160 = local_178;
              uVar3 = FUN_18026c2a0();
              uVar20 = local_res8;
              local_168 = uVar3;
            }
            uVar17 = uVar4;
            uVar5 = local_res8;
            if ((iVar10 != (int)uVar11 + -1) &&
               (uVar17 = uVar12, uVar3 = local_168, uVar20 = uVar11, uVar5 = uVar11, (int)uVar4 != 0
               )) {
              plVar2 = *(longlong **)(param_1 + 0x18);
              uVar14 = uVar12;
              uVar18 = uVar4;
              do {
                *(undefined8 *)((longlong)local_148 + uVar14) =
                     **(undefined8 **)((longlong)alStack_c8 + uVar14);
                uVar18 = uVar18 - 1;
                uVar14 = uVar14 + 8;
              } while (uVar18 != 0);
              (**(code **)(*plVar2 + 0x100))(plVar2,local_res8,uVar4,local_148);
            }
            local_res8 = uVar5;
            uVar4 = (ulonglong)((int)uVar17 + 1);
            alStack_c8[uVar17] = uVar3 + 0x10;
            uVar17 = local_160;
            iVar10 = (int)uVar11;
          }
          uVar19 = uVar19 & ~(1L << (uVar11 & 0x3f));
        } while (uVar19 != 0);
        if ((int)uVar4 != 0) {
          plVar2 = *(longlong **)(param_1 + 0x18);
          uVar3 = uVar12;
          uVar17 = uVar4;
          do {
            *(undefined8 *)((longlong)local_148 + uVar3) =
                 **(undefined8 **)((longlong)alStack_c8 + uVar3);
            uVar17 = uVar17 - 1;
            uVar3 = uVar3 + 8;
          } while (uVar17 != 0);
          (**(code **)(*plVar2 + 0x100))(plVar2,uVar20,uVar4,local_148);
        }
      }
    }
  }
  if (*(short *)(param_2 + 0xe) < 0) {
    lVar1 = *(longlong *)(param_2 + 0x20);
    (**(code **)(**(longlong **)(param_1 + 0x18) + 0x1e0))
              (*(longlong **)(param_1 + 0x18),*(undefined8 *)(lVar1 + 0x58),0,0);
    uVar4 = *(ulonglong *)(lVar1 + 8);
    puVar16 = (uint *)(lVar1 + 0x18);
    uVar15 = (uint)(uVar4 >> 0x20) & 0xf;
    if ((uVar4 & 0xf00000000) != 0) {
      do {
        uVar15 = uVar15 - 1;
        uVar7 = *puVar16 >> 4;
        puVar13 = (uint *)(param_1 + 0x368 + (ulonglong)(*puVar16 & 0xf) * 0x10);
        uVar6 = *puVar13;
        puVar13[2] = uVar7 & 7;
        if ((uVar6 & 0x10) == 0) {
          uVar6 = uVar6 & 0xfffffff8 | (uVar7 & 7) >> 2 | (uVar7 & 1) << 2 | uVar7 & 2;
          *puVar13 = uVar6;
        }
        uVar6 = (*puVar16 * 2 ^ uVar6) & 0x700 ^ uVar6;
        *puVar13 = uVar6;
        uVar6 = (*puVar16 * 2 ^ uVar6) & 0x3800 ^ uVar6;
        *puVar13 = uVar6;
        uVar6 = (*puVar16 * 2 ^ uVar6) & 0x1c000 ^ uVar6;
        *puVar13 = uVar6;
        uVar7 = (*puVar16 << 5 ^ uVar6) & 0x1ffffff ^ *puVar16 << 5;
        *puVar13 = uVar7;
        uVar6 = *puVar16;
        puVar16 = puVar16 + 1;
        *puVar13 = (uVar6 * 2 ^ uVar7) & 0x1e0000 ^ uVar7;
      } while (uVar15 != 0);
      uVar4 = (ulonglong)*(uint *)(lVar1 + 8);
    }
    if ((uVar9 & 0xffff00000000) != 0 || (uVar4 & 0xffff) != 0) {
      local_res8 = 0;
      uVar17 = -1;
      uVar19 = (uVar9 & 0xffff00000000 | (uVar4 & 0xffff) << 0x20) >> 0x20;
      iVar10 = -1;
      local_160 = 0;
      uVar9 = uVar9 & 0xffff0000ffffffff;
      local_168 = -1;
      uVar4 = uVar12;
      uVar3 = uVar12;
      uVar20 = uVar12;
      if (uVar19 != 0) {
        do {
          uVar11 = 0;
          if (uVar19 != 0) {
            for (; (uVar19 >> uVar11 & 1) == 0; uVar11 = uVar11 + 1) {
            }
          }
          uVar11 = uVar11 & 0xffffffff;
          if (uVar19 == 0) {
            uVar11 = 0x40;
          }
          lVar8 = uVar11 * 0x10 + param_1;
          lVar1 = *(longlong *)(param_1 + 0x1b68 + uVar11 * 8);
          local_178 = *(longlong *)(lVar8 + 0x368);
          uStack_170 = (uint)*(undefined8 *)(lVar8 + 0x370);
          if ((lVar1 != 0) && ((*(uint *)(lVar1 + 0x18) & 0xf0000000) == 0x10000000)) {
            local_178._4_4_ = (undefined4)((ulonglong)local_178 >> 0x20);
            local_178 = CONCAT44(local_178._4_4_,
                                 uStack_170 >> 2 & 1 | (uStack_170 & 1) << 2 |
                                 (uint)local_178 & 0xfe1fffe8 | uStack_170 & 2);
          }
          if (*(longlong *)(lVar8 + 0xb58) != local_178) {
            *(longlong *)(lVar8 + 0xb58) = local_178;
            *(uint *)(lVar8 + 0xb60) = uStack_170;
            if (uVar17 != local_178) {
              local_168 = local_178;
              uVar3 = FUN_18026c2a0();
              uVar20 = local_res8;
              local_160 = uVar3;
            }
            uVar17 = uVar4;
            uVar5 = local_res8;
            if ((iVar10 != (int)uVar11 + -1) &&
               (uVar17 = uVar12, uVar3 = local_160, uVar20 = uVar11, uVar5 = uVar11, (int)uVar4 != 0
               )) {
              plVar2 = *(longlong **)(param_1 + 0x18);
              uVar14 = uVar12;
              uVar18 = uVar4;
              do {
                *(undefined8 *)((longlong)local_148 + uVar14) =
                     **(undefined8 **)((longlong)alStack_c8 + uVar14);
                uVar18 = uVar18 - 1;
                uVar14 = uVar14 + 8;
              } while (uVar18 != 0);
              (**(code **)(*plVar2 + 0x1e8))(plVar2,local_res8,uVar4,local_148);
            }
            local_res8 = uVar5;
            uVar4 = (ulonglong)((int)uVar17 + 1);
            alStack_c8[uVar17] = uVar3 + 0x10;
            uVar17 = local_168;
            iVar10 = (int)uVar11;
          }
          uVar19 = uVar19 & ~(1L << (uVar11 & 0x3f));
        } while (uVar19 != 0);
        if ((int)uVar4 != 0) {
          plVar2 = *(longlong **)(param_1 + 0x18);
          uVar3 = uVar12;
          uVar17 = uVar4;
          do {
            *(undefined8 *)((longlong)local_148 + uVar3) =
                 **(undefined8 **)((longlong)alStack_c8 + uVar3);
            uVar17 = uVar17 - 1;
            uVar3 = uVar3 + 8;
          } while (uVar17 != 0);
          (**(code **)(*plVar2 + 0x1e8))(plVar2,uVar20,uVar4,local_148);
        }
      }
    }
    lVar1 = *(longlong *)(param_2 + 0x28);
    (**(code **)(**(longlong **)(param_1 + 0x18) + 0x200))
              (*(longlong **)(param_1 + 0x18),*(undefined8 *)(lVar1 + 0x58),0,0);
    uVar4 = *(ulonglong *)(lVar1 + 8);
    puVar16 = (uint *)(lVar1 + 0x18);
    uVar15 = (uint)(uVar4 >> 0x20) & 0xf;
    if ((uVar4 & 0xf00000000) != 0) {
      do {
        uVar15 = uVar15 - 1;
        uVar7 = *puVar16 >> 4;
        puVar13 = (uint *)(param_1 + 0x468 + (ulonglong)(*puVar16 & 0xf) * 0x10);
        uVar6 = *puVar13;
        puVar13[2] = uVar7 & 7;
        if ((uVar6 & 0x10) == 0) {
          uVar6 = uVar6 & 0xfffffff8 | (uVar7 & 7) >> 2 | (uVar7 & 1) << 2 | uVar7 & 2;
          *puVar13 = uVar6;
        }
        uVar6 = (*puVar16 * 2 ^ uVar6) & 0x700 ^ uVar6;
        *puVar13 = uVar6;
        uVar6 = (*puVar16 * 2 ^ uVar6) & 0x3800 ^ uVar6;
        *puVar13 = uVar6;
        uVar6 = (*puVar16 * 2 ^ uVar6) & 0x1c000 ^ uVar6;
        *puVar13 = uVar6;
        uVar7 = (*puVar16 << 5 ^ uVar6) & 0x1ffffff ^ *puVar16 << 5;
        *puVar13 = uVar7;
        uVar6 = *puVar16;
        puVar16 = puVar16 + 1;
        *puVar13 = (uVar6 * 2 ^ uVar7) & 0x1e0000 ^ uVar7;
      } while (uVar15 != 0);
      uVar4 = (ulonglong)*(uint *)(lVar1 + 8);
    }
    if ((uVar9 & 0xffff000000000000) != 0 || uVar4 << 0x30 != 0) {
      uVar20 = (uVar9 | uVar4 << 0x30) >> 0x30;
      local_res8 = 0;
      uVar9 = uVar12;
      uVar4 = uVar12;
      uVar3 = uVar12;
      if (uVar20 != 0) {
        do {
          uVar17 = 0;
          if (uVar20 != 0) {
            for (; (uVar20 >> uVar17 & 1) == 0; uVar17 = uVar17 + 1) {
            }
          }
          uVar17 = uVar17 & 0xffffffff;
          if (uVar20 == 0) {
            uVar17 = 0x40;
          }
          lVar8 = uVar17 * 0x10 + param_1;
          lVar1 = *(longlong *)(param_1 + 0x1be8 + uVar17 * 8);
          local_178 = *(longlong *)(lVar8 + 0x468);
          uStack_170 = (uint)*(undefined8 *)(lVar8 + 0x470);
          if ((lVar1 != 0) && ((*(uint *)(lVar1 + 0x18) & 0xf0000000) == 0x10000000)) {
            local_178._4_4_ = (undefined4)((ulonglong)local_178 >> 0x20);
            local_178 = CONCAT44(local_178._4_4_,
                                 uStack_170 >> 2 & 1 | (uStack_170 & 1) << 2 |
                                 (uint)local_178 & 0xfe1fffe8 | uStack_170 & 2);
          }
          uVar19 = uVar3;
          if (*(longlong *)(lVar8 + 0xc58) != local_178) {
            *(longlong *)(lVar8 + 0xc58) = local_178;
            *(uint *)(lVar8 + 0xc60) = uStack_170;
            if (local_150 != local_178) {
              local_150 = local_178;
              uVar4 = FUN_18026c2a0();
              local_res8 = uVar4;
            }
            uVar11 = uVar9;
            if ((local_res18 != (int)uVar17 + -1) &&
               (uVar11 = uVar12, uVar4 = local_res8, uVar19 = uVar17, (int)uVar9 != 0)) {
              plVar2 = *(longlong **)(param_1 + 0x18);
              uVar5 = uVar12;
              uVar14 = uVar9;
              do {
                *(undefined8 *)((longlong)local_148 + uVar5) =
                     **(undefined8 **)((longlong)alStack_c8 + uVar5);
                uVar14 = uVar14 - 1;
                uVar5 = uVar5 + 8;
              } while (uVar14 != 0);
              (**(code **)(*plVar2 + 0x208))(plVar2,uVar3,uVar9,local_148);
            }
            uVar9 = (ulonglong)((int)uVar11 + 1);
            alStack_c8[uVar11] = uVar4 + 0x10;
            local_res18 = (int)uVar17;
          }
          uVar20 = uVar20 & ~(1L << (uVar17 & 0x3f));
          uVar3 = uVar19;
        } while (uVar20 != 0);
        if ((int)uVar9 != 0) {
          plVar2 = *(longlong **)(param_1 + 0x18);
          uVar4 = uVar9;
          do {
            *(undefined8 *)((longlong)local_148 + uVar12) =
                 **(undefined8 **)((longlong)alStack_c8 + uVar12);
            uVar4 = uVar4 - 1;
            uVar12 = uVar12 + 8;
          } while (uVar4 != 0);
          (**(code **)(*plVar2 + 0x208))(plVar2,uVar19,uVar9,local_148);
        }
      }
    }
  }
  return;
}



// ===================================================
// 18025D895  ->  FUN_18025ceb0  (entree 18025ceb0)
// ===================================================

void FUN_18025ceb0(ulonglong *param_1)

{
  ushort uVar1;
  longlong *plVar2;
  ulonglong uVar3;
  ulonglong uVar4;
  longlong lVar5;
  uint uVar6;
  uint uVar7;
  ulonglong uVar8;
  ulonglong *puVar9;
  ulonglong uVar10;
  uint uVar11;
  uint uVar12;
  ulonglong *puVar13;
  uint *puVar14;
  ulonglong uVar15;
  ulonglong uVar16;
  ulonglong uVar17;
  ulonglong uVar18;
  ulonglong uVar19;
  ulonglong uVar20;
  ulonglong uVar21;
  ulonglong uVar22;
  uint local_res8;
  uint local_res10;
  ulonglong local_168;
  undefined8 local_160;
  uint uStack_158;
  ulonglong local_150;
  undefined8 local_148 [16];
  longlong alStack_c8 [17];
  
  lVar5 = DAT_180c4d590;
  uVar19 = *param_1;
  if (uVar19 == 0) goto LAB_18025dde1;
  uVar8 = 0;
  *param_1 = 0;
  if ((uVar19 & 0xffffffff07f0) != 0) {
    if (((uVar19 & 0x10) != 0) && (uVar1 = (ushort)param_1[0x1d0], (ushort)param_1[0x1d1] != uVar1))
    {
      *(ushort *)(param_1 + 0x1d1) = uVar1;
      uVar20 = uVar8;
      if (uVar1 - 1 < *(uint *)(lVar5 + 0x18a4)) {
        uVar20 = *(ulonglong *)(*(longlong *)(lVar5 + 0x1890) + (ulonglong)(uVar1 - 1) * 8);
      }
      param_1[0x1d6] = uVar20;
      (**(code **)(*(longlong *)param_1[3] + 0x58))
                ((longlong *)param_1[3],*(undefined8 *)(uVar20 + 0x38),0,0);
      uVar20 = param_1[0x1d6];
      uVar3 = *(ulonglong *)(uVar20 + 8);
      puVar14 = *(uint **)(uVar20 + 0x58);
      uVar11 = (uint)(uVar3 >> 0x20) & 0xf;
      if ((uVar3 & 0xf00000000) != 0) {
        do {
          uVar11 = uVar11 - 1;
          uVar7 = *puVar14 >> 4;
          puVar13 = param_1 + (ulonglong)(*puVar14 & 0xf) * 2 + 0x2d;
          uVar6 = (uint)*puVar13;
          *(uint *)(puVar13 + 1) = uVar7 & 7;
          if ((uVar6 & 0x10) == 0) {
            uVar6 = uVar6 & 0xfffffff8 | (uVar7 & 7) >> 2 | (uVar7 & 1) << 2 | uVar7 & 2;
            *(uint *)puVar13 = uVar6;
          }
          uVar6 = (*puVar14 * 2 ^ uVar6) & 0x700 ^ uVar6;
          *(uint *)puVar13 = uVar6;
          uVar6 = (*puVar14 * 2 ^ uVar6) & 0x3800 ^ uVar6;
          *(uint *)puVar13 = uVar6;
          uVar6 = (*puVar14 * 2 ^ uVar6) & 0x1c000 ^ uVar6;
          *(uint *)puVar13 = uVar6;
          uVar7 = (*puVar14 << 5 ^ uVar6) & 0x1ffffff ^ *puVar14 << 5;
          *(uint *)puVar13 = uVar7;
          uVar6 = *puVar14;
          puVar14 = puVar14 + 1;
          *(uint *)puVar13 = (uVar6 * 2 ^ uVar7) & 0x1e0000 ^ uVar7;
        } while (uVar11 != 0);
        uVar3 = (ulonglong)*(uint *)(uVar20 + 8);
      }
      uVar11 = (uint)*(ushort *)((longlong)param_1 + 0x6b4);
      if (*(ushort *)((longlong)param_1 + 0x6b4) != 0) {
        puVar13 = param_1 + 0xd7;
        do {
          uVar11 = uVar11 - 1;
          uVar7 = (uint)*puVar13 >> 4;
          puVar9 = param_1 + (ulonglong)((uint)*puVar13 & 0xf) * 2 + 0x2d;
          uVar6 = (uint)*puVar9;
          *(uint *)(puVar9 + 1) = uVar7 & 7;
          if ((uVar6 & 0x10) == 0) {
            uVar6 = uVar6 & 0xfffffff8 | (uVar7 & 7) >> 2 | (uVar7 & 1) << 2 | uVar7 & 2;
            *(uint *)puVar9 = uVar6;
          }
          uVar6 = ((uint)*puVar13 * 2 ^ uVar6) & 0x700 ^ uVar6;
          *(uint *)puVar9 = uVar6;
          uVar6 = ((uint)*puVar13 * 2 ^ uVar6) & 0x3800 ^ uVar6;
          *(uint *)puVar9 = uVar6;
          uVar6 = ((uint)*puVar13 * 2 ^ uVar6) & 0x1c000 ^ uVar6;
          *(uint *)puVar9 = uVar6;
          uVar6 = ((uint)*puVar13 << 5 ^ uVar6) & 0x1ffffff ^ (uint)*puVar13 << 5;
          *(uint *)puVar9 = uVar6;
          uVar20 = *puVar13;
          puVar13 = (ulonglong *)((longlong)puVar13 + 4);
          *(uint *)puVar9 = ((uint)uVar20 * 2 ^ uVar6) & 0x1e0000 ^ uVar6;
        } while (uVar11 != 0);
      }
      uVar19 = uVar19 & 0xfffffffffffffeff | (uVar3 & 0xffff) << 0x20;
      *(int *)((longlong)param_1 + 0xe5c) = (int)param_1[0xd6];
      *(undefined4 *)((longlong)param_1 + 0xea4) =
           *(undefined4 *)(*(longlong *)(param_1[0x1d6] + 0x20) + 4);
    }
    uVar20 = uVar19;
    if (((uVar19 >> 8 & 1) != 0) &&
       (uVar20 = uVar19 & 0xfffffffffffffeff,
       *(int *)((longlong)param_1 + 0xe5c) != (int)param_1[0xd6])) {
      uVar19 = param_1[0x1d6];
      uVar3 = *(ulonglong *)(uVar19 + 8);
      puVar14 = *(uint **)(uVar19 + 0x58);
      uVar11 = (uint)(uVar3 >> 0x20) & 0xf;
      if ((uVar3 & 0xf00000000) != 0) {
        do {
          uVar11 = uVar11 - 1;
          uVar7 = *puVar14 >> 4;
          puVar13 = param_1 + (ulonglong)(*puVar14 & 0xf) * 2 + 0x2d;
          uVar6 = (uint)*puVar13;
          *(uint *)(puVar13 + 1) = uVar7 & 7;
          if ((uVar6 & 0x10) == 0) {
            uVar6 = uVar6 & 0xfffffff8 | (uVar7 & 7) >> 2 | (uVar7 & 1) << 2 | uVar7 & 2;
            *(uint *)puVar13 = uVar6;
          }
          uVar6 = (*puVar14 * 2 ^ uVar6) & 0x700 ^ uVar6;
          *(uint *)puVar13 = uVar6;
          uVar6 = (*puVar14 * 2 ^ uVar6) & 0x3800 ^ uVar6;
          *(uint *)puVar13 = uVar6;
          uVar6 = (*puVar14 * 2 ^ uVar6) & 0x1c000 ^ uVar6;
          *(uint *)puVar13 = uVar6;
          uVar7 = (*puVar14 << 5 ^ uVar6) & 0x1ffffff ^ *puVar14 << 5;
          *(uint *)puVar13 = uVar7;
          uVar6 = *puVar14;
          puVar14 = puVar14 + 1;
          *(uint *)puVar13 = (uVar6 * 2 ^ uVar7) & 0x1e0000 ^ uVar7;
        } while (uVar11 != 0);
        uVar3 = (ulonglong)*(uint *)(uVar19 + 8);
      }
      uVar11 = (uint)*(ushort *)((longlong)param_1 + 0x6b4);
      uVar20 = uVar20 | (uVar3 & 0xffff) << 0x20;
      if (*(ushort *)((longlong)param_1 + 0x6b4) != 0) {
        puVar13 = param_1 + 0xd7;
        do {
          uVar11 = uVar11 - 1;
          uVar7 = (uint)*puVar13 >> 4;
          puVar9 = param_1 + (ulonglong)((uint)*puVar13 & 0xf) * 2 + 0x2d;
          uVar6 = (uint)*puVar9;
          *(uint *)(puVar9 + 1) = uVar7 & 7;
          if ((uVar6 & 0x10) == 0) {
            uVar6 = uVar6 & 0xfffffff8 | (uVar7 & 7) >> 2 | (uVar7 & 1) << 2 | uVar7 & 2;
            *(uint *)puVar9 = uVar6;
          }
          uVar6 = ((uint)*puVar13 * 2 ^ uVar6) & 0x700 ^ uVar6;
          *(uint *)puVar9 = uVar6;
          uVar6 = ((uint)*puVar13 * 2 ^ uVar6) & 0x3800 ^ uVar6;
          *(uint *)puVar9 = uVar6;
          uVar6 = ((uint)*puVar13 * 2 ^ uVar6) & 0x1c000 ^ uVar6;
          *(uint *)puVar9 = uVar6;
          uVar6 = ((uint)*puVar13 << 5 ^ uVar6) & 0x1ffffff ^ (uint)*puVar13 << 5;
          *(uint *)puVar9 = uVar6;
          uVar19 = *puVar13;
          puVar13 = (ulonglong *)((longlong)puVar13 + 4);
          *(uint *)puVar9 = ((uint)uVar19 * 2 ^ uVar6) & 0x1e0000 ^ uVar6;
        } while (uVar11 != 0);
      }
      *(int *)((longlong)param_1 + 0xe5c) = (int)param_1[0xd6];
    }
    if ((char)uVar20 < '\0') {
      uVar19 = param_1[0x1d3];
      if (uVar19 == 0) {
        uVar19 = *(ulonglong *)(param_1[0x1d6] + 0x18);
        param_1[0x1d3] = uVar19;
      }
      *(undefined4 *)(param_1 + 0x1d4) = *(undefined4 *)(uVar19 + 4);
    }
    uVar19 = param_1[0x1d4];
    if (param_1[0x1d5] != uVar19) {
      param_1[0x1d5] = uVar19;
      uVar19 = FUN_18026e6f0(uVar19,param_1[0x1d3],param_1[0x1d6]);
      param_1[0x1d7] = uVar19;
      (**(code **)(*(longlong *)param_1[3] + 0x88))
                ((longlong *)param_1[3],*(undefined8 *)(uVar19 + 0x30));
    }
    if ((uVar20 & 0x20) == 0) {
LAB_18025d5e2:
      if (((uVar20 >> 9 & 1) != 0) &&
         (uVar20 = uVar20 & 0xfffffffffffffdff, (int)param_1[0x1cb] != (int)param_1[0xcd])) {
        uVar19 = param_1[0x1d8];
        uVar3 = *(ulonglong *)(uVar19 + 8);
        puVar14 = (uint *)(uVar19 + 0x18);
        uVar11 = (uint)(uVar3 >> 0x20) & 0xf;
        if ((uVar3 & 0xf00000000) != 0) {
          do {
            uVar11 = uVar11 - 1;
            uVar7 = *puVar14 >> 4;
            uVar12 = *puVar14 & 0xf;
            uVar6 = (uint)param_1[(ulonglong)uVar12 * 2 + 0xd];
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xe) = uVar7 & 7;
            if ((uVar6 & 0x10) == 0) {
              uVar6 = (uVar7 & 7) >> 2 | uVar6 & 0xfffffff8 | (uVar7 & 1) << 2 | uVar7 & 2;
              *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            }
            uVar6 = (*puVar14 * 2 ^ uVar6) & 0x700 ^ uVar6;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar6 = (*puVar14 * 2 ^ uVar6) & 0x3800 ^ uVar6;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar6 = (*puVar14 * 2 ^ uVar6) & 0x1c000 ^ uVar6;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar7 = (*puVar14 << 5 ^ uVar6) & 0x1ffffff ^ *puVar14 << 5;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar7;
            uVar6 = *puVar14;
            puVar14 = puVar14 + 1;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) =
                 (uVar6 * 2 ^ uVar7) & 0x1e0000 ^ uVar7;
          } while (uVar11 != 0);
          uVar3 = (ulonglong)*(uint *)(uVar19 + 8);
        }
        uVar11 = (uint)*(ushort *)((longlong)param_1 + 0x66c);
        uVar20 = uVar20 | (uVar3 & 0xffff) << 0x10;
        if (*(ushort *)((longlong)param_1 + 0x66c) != 0) {
          puVar13 = param_1 + 0xce;
          do {
            uVar11 = uVar11 - 1;
            uVar7 = (uint)*puVar13 >> 4;
            uVar12 = (uint)*puVar13 & 0xf;
            uVar6 = (uint)param_1[(ulonglong)uVar12 * 2 + 0xd];
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xe) = uVar7 & 7;
            if ((uVar6 & 0x10) == 0) {
              uVar6 = (uVar7 & 7) >> 2 | uVar6 & 0xfffffff8 | (uVar7 & 1) << 2 | uVar7 & 2;
              *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            }
            uVar6 = ((uint)*puVar13 * 2 ^ uVar6) & 0x700 ^ uVar6;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar6 = ((uint)*puVar13 * 2 ^ uVar6) & 0x3800 ^ uVar6;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar6 = ((uint)*puVar13 * 2 ^ uVar6) & 0x1c000 ^ uVar6;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar6 = ((uint)*puVar13 << 5 ^ uVar6) & 0x1ffffff ^ (uint)*puVar13 << 5;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar19 = *puVar13;
            puVar13 = (ulonglong *)((longlong)puVar13 + 4);
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) =
                 ((uint)uVar19 * 2 ^ uVar6) & 0x1e0000 ^ uVar6;
          } while (uVar11 != 0);
        }
        *(int *)(param_1 + 0x1cb) = (int)param_1[0xcd];
      }
    }
    else {
      uVar1 = *(ushort *)((longlong)param_1 + 0xe82);
      if ((*(ushort *)((longlong)param_1 + 0xe8a) != uVar1) || ((uVar20 >> 9 & 1) != 0)) {
        *(ushort *)((longlong)param_1 + 0xe8a) = uVar1;
        uVar19 = uVar8;
        if (uVar1 - 1 < *(uint *)(lVar5 + 0x18c4)) {
          uVar19 = *(ulonglong *)(*(longlong *)(lVar5 + 0x18b0) + (ulonglong)(uVar1 - 1) * 8);
        }
        param_1[0x1d8] = uVar19;
        (**(code **)(*(longlong *)param_1[3] + 0x48))
                  ((longlong *)param_1[3],*(undefined8 *)(uVar19 + 0x58),0,0);
        uVar19 = param_1[0x1d8];
        uVar3 = *(ulonglong *)(uVar19 + 8);
        puVar14 = (uint *)(uVar19 + 0x18);
        uVar11 = (uint)(uVar3 >> 0x20) & 0xf;
        if ((uVar3 & 0xf00000000) != 0) {
          do {
            uVar11 = uVar11 - 1;
            uVar7 = *puVar14 >> 4;
            uVar12 = *puVar14 & 0xf;
            uVar6 = (uint)param_1[(ulonglong)uVar12 * 2 + 0xd];
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xe) = uVar7 & 7;
            if ((uVar6 & 0x10) == 0) {
              uVar6 = (uVar7 & 7) >> 2 | uVar6 & 0xfffffff8 | (uVar7 & 1) << 2 | uVar7 & 2;
              *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            }
            uVar6 = (*puVar14 * 2 ^ uVar6) & 0x700 ^ uVar6;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar6 = (*puVar14 * 2 ^ uVar6) & 0x3800 ^ uVar6;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar6 = (*puVar14 * 2 ^ uVar6) & 0x1c000 ^ uVar6;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar7 = (*puVar14 << 5 ^ uVar6) & 0x1ffffff ^ *puVar14 << 5;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar7;
            uVar6 = *puVar14;
            puVar14 = puVar14 + 1;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) =
                 (uVar6 * 2 ^ uVar7) & 0x1e0000 ^ uVar7;
          } while (uVar11 != 0);
          uVar3 = (ulonglong)*(uint *)(uVar19 + 8);
        }
        uVar11 = (uint)*(ushort *)((longlong)param_1 + 0x66c);
        if (*(ushort *)((longlong)param_1 + 0x66c) != 0) {
          puVar13 = param_1 + 0xce;
          do {
            uVar11 = uVar11 - 1;
            uVar7 = (uint)*puVar13 >> 4;
            uVar12 = (uint)*puVar13 & 0xf;
            uVar6 = (uint)param_1[(ulonglong)uVar12 * 2 + 0xd];
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xe) = uVar7 & 7;
            if ((uVar6 & 0x10) == 0) {
              uVar6 = (uVar7 & 7) >> 2 | uVar6 & 0xfffffff8 | (uVar7 & 1) << 2 | uVar7 & 2;
              *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            }
            uVar6 = ((uint)*puVar13 * 2 ^ uVar6) & 0x700 ^ uVar6;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar6 = ((uint)*puVar13 * 2 ^ uVar6) & 0x3800 ^ uVar6;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar6 = ((uint)*puVar13 * 2 ^ uVar6) & 0x1c000 ^ uVar6;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar6 = ((uint)*puVar13 << 5 ^ uVar6) & 0x1ffffff ^ (uint)*puVar13 << 5;
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) = uVar6;
            uVar19 = *puVar13;
            puVar13 = (ulonglong *)((longlong)puVar13 + 4);
            *(uint *)(param_1 + (ulonglong)uVar12 * 2 + 0xd) =
                 ((uint)uVar19 * 2 ^ uVar6) & 0x1e0000 ^ uVar6;
          } while (uVar11 != 0);
        }
        uVar20 = uVar20 & 0xfffffffffffffdff | (uVar3 & 0xffff) << 0x10;
        *(int *)(param_1 + 0x1cb) = (int)param_1[0xcd];
        goto LAB_18025d5e2;
      }
    }
    if (((uVar20 & 0x40) != 0) &&
       (*(short *)((longlong)param_1 + 0xe8e) != *(short *)((longlong)param_1 + 0xe86))) {
      if (*(short *)((longlong)param_1 + 0xe86) == 0) {
        param_1[0x1d9] = 0;
        uVar19 = 0;
      }
      else {
        uVar19 = param_1[0x1d0] >> 0x30;
        uVar11 = ((ushort)(param_1[0x1d0] >> 0x30) & 0x3fff) - 1;
        uVar3 = uVar8;
        if (uVar11 < *(uint *)(lVar5 + 0x1964)) {
          uVar3 = *(ulonglong *)(*(longlong *)(lVar5 + 0x1950) + (ulonglong)uVar11 * 8);
        }
        param_1[0x1d9] = uVar3;
        if (uVar3 != 0) {
          FUN_18025c190(param_1);
          uVar19 = (ulonglong)*(ushort *)((longlong)param_1 + 0xe86);
        }
      }
      uVar11 = ~(uint)(uVar19 >> 0xe) & (uint)(*(ushort *)((longlong)param_1 + 0xe8e) >> 0xe);
      if ((uVar11 & 1) != 0) {
        (**(code **)(*(longlong *)param_1[3] + 0xb8))((longlong *)param_1[3],0,0,0);
      }
      if ((uVar11 & 2) != 0) {
        (**(code **)(*(longlong *)param_1[3] + 0x1e0))((longlong *)param_1[3],0,0,0);
        (**(code **)(*(longlong *)param_1[3] + 0x200))((longlong *)param_1[3],0,0,0);
      }
      *(undefined2 *)((longlong)param_1 + 0xe8e) = *(undefined2 *)((longlong)param_1 + 0xe86);
    }
    uVar19 = uVar20 & 0xffffffffffffff0f;
    if ((uVar20 & 0xffff00000000) != 0) {
      local_res10 = 0xffffffff;
      uVar17 = 0xffffffffffffffff;
      uVar22 = uVar20 >> 0x20 & 0xffff;
      local_res8 = 0;
      uVar19 = uVar20 & 0xffff0000ffffff0f;
      local_150 = 0;
      local_168 = 0xffffffffffffffff;
      uVar20 = uVar8;
      uVar3 = uVar8;
      uVar4 = uVar8;
      if (uVar22 != 0) {
        do {
          uVar21 = 0;
          if (uVar22 != 0) {
            for (; (uVar22 >> uVar21 & 1) == 0; uVar21 = uVar21 + 1) {
            }
          }
          uVar21 = uVar21 & 0xffffffff;
          if (uVar22 == 0) {
            uVar21 = 0x40;
          }
          uVar11 = (uint)uVar21;
          local_160 = param_1[uVar21 * 2 + 0x2d];
          uStack_158 = (uint)param_1[uVar21 * 2 + 0x2e];
          if ((param_1[uVar21 + 0x33d] != 0) &&
             ((*(uint *)(param_1[uVar21 + 0x33d] + 0x18) & 0xf0000000) == 0x10000000)) {
            local_160._4_4_ = (undefined4)(local_160 >> 0x20);
            local_160 = CONCAT44(local_160._4_4_,
                                 uStack_158 >> 2 & 1 | (uStack_158 & 1) << 2 |
                                 (uint)local_160 & 0xfe1fffe8 | uStack_158 & 2);
          }
          if (param_1[uVar21 * 2 + 299] != local_160) {
            param_1[uVar21 * 2 + 299] = local_160;
            *(uint *)(param_1 + uVar21 * 2 + 300) = uStack_158;
            if (uVar17 != local_160) {
              local_168 = local_160;
              uVar3 = FUN_18026c2a0();
              uVar4 = (ulonglong)local_res8;
              local_150 = uVar3;
            }
            uVar17 = uVar20;
            uVar6 = local_res8;
            if ((local_res10 != uVar11 - 1) &&
               (uVar17 = uVar8, uVar3 = local_150, uVar4 = uVar21, uVar6 = uVar11, (int)uVar20 != 0)
               ) {
              plVar2 = (longlong *)param_1[3];
              uVar15 = uVar8;
              uVar18 = uVar20;
              do {
                *(undefined8 *)((longlong)local_148 + uVar15) =
                     **(undefined8 **)((longlong)alStack_c8 + uVar15);
                uVar18 = uVar18 - 1;
                uVar15 = uVar15 + 8;
              } while (uVar18 != 0);
              (**(code **)(*plVar2 + 0xd0))(plVar2,local_res8,uVar20,local_148);
            }
            local_res8 = uVar6;
            uVar20 = (ulonglong)((int)uVar17 + 1);
            alStack_c8[uVar17] = uVar3 + 0x10;
            uVar17 = local_168;
            local_res10 = uVar11;
          }
          uVar22 = uVar22 & ~(1L << (uVar21 & 0x3f));
        } while (uVar22 != 0);
        if ((int)uVar20 != 0) {
          plVar2 = (longlong *)param_1[3];
          uVar3 = uVar8;
          uVar17 = uVar20;
          do {
            *(undefined8 *)((longlong)local_148 + uVar3) =
                 **(undefined8 **)((longlong)alStack_c8 + uVar3);
            uVar17 = uVar17 - 1;
            uVar3 = uVar3 + 8;
          } while (uVar17 != 0);
          (**(code **)(*plVar2 + 0xd0))(plVar2,uVar4,uVar20,local_148);
        }
      }
    }
    if ((uVar19 & 0xffff0000) != 0) {
      local_res10 = 0xffffffff;
      uVar20 = uVar19 >> 0x10 & 0xffff;
      local_res8 = 0;
      uVar19 = uVar19 & 0xffffffff0000ffff;
      local_168 = 0;
      if (uVar20 != 0) {
        uVar22 = 0xffffffffffffffff;
        uVar3 = uVar8;
        uVar4 = uVar8;
        uVar17 = uVar8;
        do {
          uVar21 = 0;
          if (uVar20 != 0) {
            for (; (uVar20 >> uVar21 & 1) == 0; uVar21 = uVar21 + 1) {
            }
          }
          uVar21 = uVar21 & 0xffffffff;
          if (uVar20 == 0) {
            uVar21 = 0x40;
          }
          uVar11 = (uint)uVar21;
          local_160 = param_1[uVar21 * 2 + 0xd];
          uStack_158 = (uint)param_1[uVar21 * 2 + 0xe];
          if ((param_1[uVar21 + 0x34d] != 0) &&
             ((*(uint *)(param_1[uVar21 + 0x34d] + 0x18) & 0xf0000000) == 0x10000000)) {
            local_160._4_4_ = (undefined4)(local_160 >> 0x20);
            local_160 = CONCAT44(local_160._4_4_,
                                 uStack_158 >> 2 & 1 | (uStack_158 & 1) << 2 |
                                 (uint)local_160 & 0xfe1fffe8 | uStack_158 & 2);
          }
          if (param_1[uVar21 * 2 + 0x10b] != local_160) {
            param_1[uVar21 * 2 + 0x10b] = local_160;
            *(uint *)(param_1 + uVar21 * 2 + 0x10c) = uStack_158;
            uVar15 = uVar17;
            if (uVar22 != local_160) {
              uVar4 = FUN_18026c2a0();
              uVar15 = (ulonglong)local_res8;
              uVar22 = local_160;
              local_168 = uVar4;
            }
            uVar18 = uVar3;
            uVar17 = uVar15;
            if ((local_res10 != uVar11 - 1) &&
               (uVar18 = uVar8, uVar4 = local_168, uVar17 = uVar21, local_res8 = uVar11,
               (int)uVar3 != 0)) {
              plVar2 = (longlong *)param_1[3];
              uVar10 = uVar3;
              uVar16 = uVar8;
              do {
                *(undefined8 *)((longlong)local_148 + uVar16) =
                     **(undefined8 **)((longlong)alStack_c8 + uVar16);
                uVar10 = uVar10 - 1;
                uVar16 = uVar16 + 8;
              } while (uVar10 != 0);
              (**(code **)(*plVar2 + 0x50))(plVar2,uVar15,uVar3,local_148);
            }
            uVar3 = (ulonglong)((int)uVar18 + 1);
            alStack_c8[uVar18] = uVar4 + 0x10;
            local_res10 = uVar11;
          }
          uVar20 = uVar20 & ~(1L << (uVar21 & 0x3f));
        } while (uVar20 != 0);
        if ((int)uVar3 != 0) {
          plVar2 = (longlong *)param_1[3];
          uVar20 = uVar3;
          do {
            *(undefined8 *)((longlong)local_148 + uVar8) =
                 **(undefined8 **)((longlong)alStack_c8 + uVar8);
            uVar20 = uVar20 - 1;
            uVar8 = uVar8 + 8;
          } while (uVar20 != 0);
          (**(code **)(*plVar2 + 0x50))(plVar2,uVar17,uVar3,local_148);
        }
      }
    }
  }
  if (uVar19 != 0) {
    if (((uVar19 & 1) != 0) && (param_1[0x106] != param_1[8])) {
      lVar5 = FUN_180267650();
      param_1[0x106] = param_1[8];
      *(int *)(param_1 + 0x107) = (int)param_1[9];
      *(undefined4 *)((longlong)param_1 + 0x83c) = *(undefined4 *)((longlong)param_1 + 0x4c);
      (**(code **)(*(longlong *)param_1[3] + 0x158))
                ((longlong *)param_1[3],*(undefined8 *)(lVar5 + 0x10));
    }
    if (((uVar19 & 2) != 0) && (param_1[0x108] != param_1[10])) {
      param_1[0x108] = param_1[10];
      lVar5 = FUN_18026b490(param_1[10]);
      (**(code **)(*(longlong *)param_1[3] + 0x118))
                ((longlong *)param_1[3],**(undefined8 **)(lVar5 + 0x18),0,0xffffffff);
    }
    if ((uVar19 & 0xc) != 0) {
      if (param_1[0x109] == param_1[0xb]) {
        if ((int)param_1[0x1ce] != (int)param_1[0x103]) {
          *(int *)(param_1 + 0x1ce) = (int)param_1[0x103];
          (**(code **)(*(longlong *)param_1[3] + 0x120))
                    ((longlong *)param_1[3],*(undefined8 *)(param_1[0x1cf] + 0x10));
        }
      }
      else {
        param_1[0x109] = param_1[0xb];
        *(int *)(param_1 + 0x10a) = (int)param_1[0xc];
        *(int *)(param_1 + 0x1ce) = (int)param_1[0x103];
        uVar19 = FUN_180267a10(param_1[0xb]);
        param_1[0x1cf] = uVar19;
        (**(code **)(*(longlong *)param_1[3] + 0x120))
                  ((longlong *)param_1[3],*(undefined8 *)(uVar19 + 0x10),(int)param_1[0x103]);
      }
    }
  }
LAB_18025dde1:
  FUN_18025de00(param_1);
  return;
}



// ===================================================
// 18025FC78  ->  FUN_18025fc10  (entree 18025fc10)
// ===================================================

void FUN_18025fc10(ulonglong *param_1)

{
  ulonglong uVar1;
  ushort uVar2;
  
  *param_1 = *param_1 | 0xf0;
  uVar1 = param_1[0x1d9];
  param_1[0x1d0] = 0;
  param_1[0x1d1] = 0;
  param_1[0x1d3] = 0;
  param_1[0x1d6] = 0;
  param_1[0x1d8] = 0;
  if (uVar1 != 0) {
    uVar2 = *(ushort *)(uVar1 + 0xe);
    if ((uVar2 >> 0xe & 1) != 0) {
      (**(code **)(*(longlong *)param_1[3] + 0xb8))((longlong *)param_1[3],0,0,0);
      uVar2 = *(ushort *)(uVar1 + 0xe);
    }
    if ((short)uVar2 < 0) {
      (**(code **)(*(longlong *)param_1[3] + 0x1e0))((longlong *)param_1[3],0,0,0);
      (**(code **)(*(longlong *)param_1[3] + 0x200))((longlong *)param_1[3],0,0,0);
    }
    param_1[0x1d9] = 0;
  }
  param_1[0x1d7] = 0;
  param_1[0x1d5] = 0;
  param_1[0x1d2] = 0;
  if (param_1[0x1da] != 0) {
    (**(code **)(*(longlong *)param_1[3] + 0x228))((longlong *)param_1[3],0,0,0);
    param_1[0x1da] = 0;
  }
  param_1[0xcd] = 0x48674bc7;
  param_1[0xd6] = 0x48674bc7;
  param_1[0xdf] = 0x48674bc7;
  param_1[0xe8] = 0x48674bc7;
  param_1[0xf1] = 0x48674bc7;
  param_1[0xfa] = 0x48674bc7;
  *(int *)(param_1 + 0x1cb) = (int)param_1[0xcd];
  *(int *)((longlong)param_1 + 0xe5c) = (int)param_1[0xd6];
  *(int *)(param_1 + 0x1cc) = (int)param_1[0xdf];
  *(int *)((longlong)param_1 + 0xe64) = (int)param_1[0xe8];
  *(int *)(param_1 + 0x1cd) = (int)param_1[0xf1];
  *(int *)((longlong)param_1 + 0xe6c) = (int)param_1[0xfa];
  return;
}



// ===================================================
// 180261757  ->  FUN_180261700  (entree 180261700)
// ===================================================

void FUN_180261700(ulonglong *param_1)

{
  ulonglong uVar1;
  ushort uVar2;
  
  *param_1 = *param_1 | 0x70;
  uVar1 = param_1[0x1d9];
  param_1[0x1d1] = 0;
  param_1[0x1d6] = 0;
  param_1[0x1d8] = 0;
  if (uVar1 != 0) {
    uVar2 = *(ushort *)(uVar1 + 0xe);
    if ((uVar2 >> 0xe & 1) != 0) {
      (**(code **)(*(longlong *)param_1[3] + 0xb8))((longlong *)param_1[3],0,0,0);
      uVar2 = *(ushort *)(uVar1 + 0xe);
    }
    if ((short)uVar2 < 0) {
      (**(code **)(*(longlong *)param_1[3] + 0x1e0))((longlong *)param_1[3],0,0,0);
      (**(code **)(*(longlong *)param_1[3] + 0x200))((longlong *)param_1[3],0,0,0);
    }
    param_1[0x1d9] = 0;
  }
  *(undefined4 *)((longlong)param_1 + 0xe94) = 0;
  if (param_1[0x1da] != 0) {
    (**(code **)(*(longlong *)param_1[3] + 0x228))((longlong *)param_1[3],0,0,0);
    param_1[0x1da] = 0;
  }
  return;
}



