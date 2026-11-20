// ===================================================
// 18025E0B4  ->  FUN_18025de00  (entree 18025de00)
// ===================================================

void FUN_18025de00(longlong param_1)

{
  undefined1 (*pauVar1) [16];
  undefined1 auVar2 [16];
  undefined1 auVar3 [16];
  undefined1 auVar4 [16];
  undefined1 auVar5 [16];
  int iVar6;
  longlong lVar7;
  undefined1 (*pauVar8) [16];
  ulonglong uVar9;
  ulonglong uVar10;
  undefined1 (*pauVar11) [16];
  undefined1 (*pauVar12) [16];
  ulonglong uVar13;
  ulonglong uVar14;
  ulonglong uVar15;
  uint uVar16;
  uint local_res8;
  longlong local_res20;
  undefined1 (*local_58) [16];
  undefined8 local_50;
  
  local_res8 = 0;
  local_res20 = 0;
  do {
    lVar7 = *(longlong *)(param_1 + 0x38);
    uVar15 = *(ulonglong *)(lVar7 + 8 + local_res20);
    if (uVar15 != 0) {
      do {
        lVar7 = 0x3f;
        if (uVar15 != 0) {
          for (; uVar15 >> lVar7 == 0; lVar7 = lVar7 + -1) {
          }
        }
        iVar6 = (int)lVar7;
        if (uVar15 == 0) {
          iVar6 = -1;
        }
        uVar15 = uVar15 & ~(1L << ((ulonglong)(0x3f - (0x3f - iVar6)) & 0x3f));
        uVar10 = *(ulonglong *)
                  (*(longlong *)(param_1 + 0x38) + 0x18 +
                  (ulonglong)(local_res8 * 0x40 + (0x3f - iVar6)) * 8);
        uVar16 = (uint)(uVar10 >> 0x10) & 0xfff;
        uVar9 = uVar10 >> 8;
        lVar7 = FUN_18026b040(*(undefined8 *)(param_1 + 0x28),uVar10 & 0xff,uVar16);
        FUN_180286310(lVar7 + 4);
        *(short *)(lVar7 + 0x16) = *(short *)(lVar7 + 0x16) + 1;
        local_58 = (undefined1 (*) [16])0x0;
        local_50 = 0;
        iVar6 = (**(code **)(**(longlong **)(param_1 + 0x18) + 0x70))
                          (*(longlong **)(param_1 + 0x18),
                           *(undefined8 *)(*(longlong *)(lVar7 + 0x18) + 0x10),0,4,0,&local_58);
        if ((-1 < iVar6) && (local_58 != (undefined1 (*) [16])0x0)) {
          pauVar11 = (undefined1 (*) [16])
                     (*(longlong *)(param_1 + 0x38) + 0x420 + (uVar10 >> 0x18 & 0xfffffff0));
          uVar13 = (ulonglong)uVar16;
          pauVar8 = local_58;
          if (3 < uVar13) {
            uVar14 = (ulonglong)(uVar16 >> 2);
            uVar13 = uVar13 + uVar14 * -4;
            pauVar12 = pauVar11;
            do {
              auVar2 = pauVar12[1];
              auVar3 = pauVar12[2];
              auVar4 = pauVar12[3];
              pauVar1 = pauVar8 + 3;
              pauVar11 = pauVar12 + 4;
              auVar5 = vmovntdq_avx(*pauVar12);
              *pauVar8 = auVar5;
              auVar2 = vmovntdq_avx(auVar2);
              pauVar8[1] = auVar2;
              auVar2 = vmovntdq_avx(auVar3);
              pauVar8[2] = auVar2;
              pauVar8 = pauVar8 + 4;
              auVar2 = vmovntdq_avx(auVar4);
              *pauVar1 = auVar2;
              uVar14 = uVar14 - 1;
              pauVar12 = pauVar11;
            } while (uVar14 != 0);
          }
          for (; uVar13 != 0; uVar13 = uVar13 - 1) {
            auVar2 = vmovntdq_avx(*pauVar11);
            *pauVar8 = auVar2;
            pauVar8 = pauVar8 + 1;
            pauVar11 = pauVar11 + 1;
          }
          (**(code **)(**(longlong **)(param_1 + 0x18) + 0x78))
                    (*(longlong **)(param_1 + 0x18),
                     *(undefined8 *)(*(longlong *)(lVar7 + 0x18) + 0x10),0);
        }
        uVar10 = (ulonglong)((uint)(uVar10 & 0xff) & 0xf);
        *(undefined4 *)(lVar7 + 4) = 0;
        if (((uVar9 & 1) != 0) &&
           (*(longlong *)(param_1 + 0xfa8 + uVar10 * 8) != *(longlong *)(lVar7 + 0x10))) {
          *(longlong *)(param_1 + 0x1248 + uVar10 * 8) = lVar7;
          *(undefined8 *)(param_1 + 0xfa8 + uVar10 * 8) = *(undefined8 *)(lVar7 + 0x10);
          (**(code **)(**(longlong **)(param_1 + 0x18) + 0x38))
                    (*(longlong **)(param_1 + 0x18),uVar10,1,*(longlong *)(lVar7 + 0x18) + 0x10);
        }
        if (((uVar9 & 2) != 0) &&
           (*(longlong *)(param_1 + 0x1018 + uVar10 * 8) != *(longlong *)(lVar7 + 0x10))) {
          *(longlong *)(param_1 + 0x12b8 + uVar10 * 8) = lVar7;
          *(undefined8 *)(param_1 + 0x1018 + uVar10 * 8) = *(undefined8 *)(lVar7 + 0x10);
          (**(code **)(**(longlong **)(param_1 + 0x18) + 0x80))
                    (*(longlong **)(param_1 + 0x18),uVar10,1,*(longlong *)(lVar7 + 0x18) + 0x10);
        }
        if (((uVar9 & 4) != 0) &&
           (*(longlong *)(param_1 + 0x1088 + uVar10 * 8) != *(longlong *)(lVar7 + 0x10))) {
          *(longlong *)(param_1 + 0x1328 + uVar10 * 8) = lVar7;
          *(undefined8 *)(param_1 + 0x1088 + uVar10 * 8) = *(undefined8 *)(lVar7 + 0x10);
          (**(code **)(**(longlong **)(param_1 + 0x18) + 0xb0))
                    (*(longlong **)(param_1 + 0x18),uVar10,1,*(longlong *)(lVar7 + 0x18) + 0x10);
        }
        if (((uVar9 & 0x10) != 0) &&
           (*(longlong *)(param_1 + 0x10f8 + uVar10 * 8) != *(longlong *)(lVar7 + 0x10))) {
          *(longlong *)(param_1 + 0x1398 + uVar10 * 8) = lVar7;
          *(undefined8 *)(param_1 + 0x10f8 + uVar10 * 8) = *(undefined8 *)(lVar7 + 0x10);
          (**(code **)(**(longlong **)(param_1 + 0x18) + 0x1f0))
                    (*(longlong **)(param_1 + 0x18),uVar10,1,*(longlong *)(lVar7 + 0x18) + 0x10);
        }
        if (((uVar9 & 0x20) != 0) &&
           (*(longlong *)(param_1 + 0x1168 + uVar10 * 8) != *(longlong *)(lVar7 + 0x10))) {
          *(longlong *)(param_1 + 0x1408 + uVar10 * 8) = lVar7;
          *(undefined8 *)(param_1 + 0x1168 + uVar10 * 8) = *(undefined8 *)(lVar7 + 0x10);
          (**(code **)(**(longlong **)(param_1 + 0x18) + 0x210))
                    (*(longlong **)(param_1 + 0x18),uVar10,1,*(longlong *)(lVar7 + 0x18) + 0x10);
        }
        if (((uVar9 & 8) != 0) &&
           (*(longlong *)(param_1 + 0x11d8 + uVar10 * 8) != *(longlong *)(lVar7 + 0x10))) {
          *(longlong *)(param_1 + 0x1478 + uVar10 * 8) = lVar7;
          *(undefined8 *)(param_1 + 0x11d8 + uVar10 * 8) = *(undefined8 *)(lVar7 + 0x10);
          (**(code **)(**(longlong **)(param_1 + 0x18) + 0x238))
                    (*(longlong **)(param_1 + 0x18),uVar10,1,*(longlong *)(lVar7 + 0x18) + 0x10);
        }
      } while (uVar15 != 0);
      lVar7 = *(longlong *)(param_1 + 0x38);
    }
    local_res8 = local_res8 + 1;
    local_res20 = local_res20 + 8;
  } while (local_res8 < 2);
  *(undefined8 *)(lVar7 + 0x10) = 0;
  *(undefined8 *)(*(longlong *)(param_1 + 0x38) + 8) = 0;
  return;
}



