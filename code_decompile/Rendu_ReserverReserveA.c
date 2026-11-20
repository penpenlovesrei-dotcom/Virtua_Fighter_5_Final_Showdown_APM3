/* Rendu_ReserverReserveA  --  VF5FS+0x1631e0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801631e0.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void Rendu_ReserverReserveA(int param_1)

{
  int *piVar1;
  undefined8 uVar2;
  ulonglong uVar3;
  ulonglong uVar4;
  longlong lVar5;
  longlong *plVar6;
  longlong lVar7;
  ulonglong uVar8;
  undefined1 local_res10 [8];
  undefined8 uVar9;
  longlong local_60;
  longlong local_58;
  undefined1 local_48 [16];
  longlong local_38;
  longlong local_30;
  longlong local_28;
  longlong local_20;
  
  uVar9 = 0xfffffffffffffffe;
  if ((*(char *)((longlong)DAT_180713fe0 + 6) == '\0') || (*DAT_180713fe0 != param_1)) {
    FUN_1801626f0(DAT_180713fd8);
    *(undefined8 *)(DAT_180713fe0 + 0x14) = *(undefined8 *)(DAT_180713fe0 + 0x12);
    uVar2 = FUN_180162070(local_48,0x2d0,local_res10);
    FUN_1801621b0(&local_60,(longlong)param_1,uVar2,local_res10,uVar9);
    if (local_48._0_8_ != 0) {
      uVar3 = ((local_38 - local_48._0_8_) / 0x1c0) * 0x1c0;
      lVar7 = local_48._0_8_;
      if (0xfff < uVar3) {
        lVar7 = *(longlong *)(local_48._0_8_ + -8);
        if (0x1f < (local_48._0_8_ - lVar7) - 8U) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(local_38 - local_48._0_8_,uVar3 + 0x27);
        }
      }
      FUN_1802fdd80(lVar7);
      local_48 = (undefined1  [16])0x0;
      local_38 = 0;
    }
    FUN_180162240(&local_30,(longlong)param_1,local_res10);
    if (DAT_180713fd8 != &local_60) {
      FUN_1801619b0(DAT_180713fd8,local_60,local_58,local_res10[0]);
    }
    piVar1 = DAT_180713fe0;
    plVar6 = (longlong *)(DAT_180713fe0 + 0x12);
    if (plVar6 != &local_30) {
      uVar3 = local_28 - local_30 >> 6;
      lVar7 = *plVar6;
      uVar4 = *(longlong *)(DAT_180713fe0 + 0x14) - lVar7 >> 6;
      uVar8 = *(longlong *)(DAT_180713fe0 + 0x16) - lVar7 >> 6;
      if (uVar8 < uVar3) {
        if (0x3ffffffffffffff < uVar3) {
                    /* WARNING: Subroutine does not return */
          FUN_180010340();
        }
        uVar4 = uVar3;
        if ((uVar8 <= 0x3ffffffffffffff - (uVar8 >> 1)) &&
           (uVar4 = (uVar8 >> 1) + uVar8, uVar4 < uVar3)) {
          uVar4 = uVar3;
        }
        if (lVar7 != 0) {
          FUN_180010d20(plVar6,lVar7);
        }
        FUN_180022050(plVar6,uVar4);
        uVar9 = FUN_18007f8f0(plVar6,local_30,local_28,*plVar6);
        *(undefined8 *)(piVar1 + 0x14) = uVar9;
      }
      else if (uVar4 < uVar3) {
        lVar5 = uVar4 * 0x40 + local_30;
        FUN_180161df0(local_30,lVar5,lVar7);
        uVar9 = FUN_18007f8f0(plVar6,lVar5,local_28,*(undefined8 *)(piVar1 + 0x14));
        *(undefined8 *)(piVar1 + 0x14) = uVar9;
      }
      else {
        FUN_180161df0(local_30,local_28,lVar7);
        *(ulonglong *)(piVar1 + 0x14) = uVar3 * 0x40 + lVar7;
      }
    }
    uVar9 = FUN_180162ec0();
    piVar1 = DAT_180713fe0;
    *DAT_180713fe0 = param_1;
    *(undefined1 *)((longlong)piVar1 + 6) = 1;
    for (; local_60 != local_58; local_60 = local_60 + 0x18) {
      uVar9 = FUN_1801625b0(local_60);
    }
    if (local_30 != 0) {
      uVar3 = local_20 - local_30 & 0xffffffffffffffc0;
      lVar7 = local_30;
      if (0xfff < uVar3) {
        lVar7 = *(longlong *)(local_30 + -8);
        if (0x1f < (local_30 - lVar7) - 8U) {
                    /* WARNING: Subroutine does not return */
          FUN_180303af0(uVar9,uVar3 + 0x27);
        }
      }
      FUN_1802fdd80(lVar7);
    }
    FUN_180162630(&local_60);
  }
  return;
}
