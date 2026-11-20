/* FUN_180231570  --  VF5FS+0x231570
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180231570.
 * Vidée le 2026-11-09.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_180231570(void)

{
  undefined *puVar1;
  int iVar2;
  undefined1 (*pauVar3) [16];
  longlong lVar4;
  int iVar5;
  longlong lVar6;
  longlong *plVar7;
  undefined1 auVar8 [64];
  longlong local_res8 [4];
  undefined *local_48 [4];
  undefined *local_28;
  undefined *local_20;
  
  if (((DAT_180c8df28 == 0) || (*(longlong *)(DAT_180c8df28 + 0x1ff08) == 0)) &&
     (DAT_18079bb50 == 0)) {
    plVar7 = local_res8;
    FUN_18000e180(plVar7,"string_array");
    iVar5 = (int)plVar7;
    local_48[0] = &DAT_18055c108;
    local_48[1] = &DAT_18055c10c;
    local_48[2] = &DAT_18055c10c;
    local_48[3] = &DAT_18055c10c;
    local_28 = &DAT_18055c10c;
    local_20 = &DAT_18055c10c;
    iVar2 = FUN_1802cb4a0();
    if (5 < iVar2) {
      iVar2 = 1;
    }
    puVar1 = local_48[iVar2];
    auVar8 = ZEXT1664(_DAT_180373c70);
    pauVar3 = (undefined1 (*) [16])(puVar1 + -0x10);
    do {
      pauVar3 = pauVar3 + 1;
      vpcmpistri_avx(_DAT_180373c70,*pauVar3,0x14);
    } while (pauVar3 != (undefined1 (*) [16])0x0);
    iVar2 = (int)local_res8;
    FUN_180010a70(SUB168(*pauVar3,0),puVar1,iVar5 - (int)puVar1);
    pauVar3 = (undefined1 (*) [16])0x180376544;
    do {
      pauVar3 = pauVar3 + 1;
      vpcmpistri_avx(auVar8._0_16_,*pauVar3,0x14);
    } while (pauVar3 != (undefined1 (*) [16])0x0);
    FUN_180010a70(SUB168(*pauVar3,0),&DAT_180376554,iVar2 + 0x7fc89aac);
    lVar4 = (local_res8[0] << 0x14) >> 0x14;
    lVar6 = lVar4 << 4;
    if (lVar4 == 0) {
      lVar6 = 0;
    }
    if (lVar6 == 0) {
      plVar7 = local_res8;
    }
    else {
      plVar7 = (longlong *)(lVar6 + 4);
    }
    FUN_180278e80(&DAT_18079b800,"rom_200/string_array.farc",plVar7,1,0,0);
    if (local_res8[0] << 0x14 != 0) {
      FUN_180279c00((local_res8[0] << 0x14) >> 0x10);
    }
  }
  return;
}
