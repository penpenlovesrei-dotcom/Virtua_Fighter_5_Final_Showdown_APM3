/* FUN_1800f07e0  --  VF5FS+0xf07e0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800f07e0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

ulonglong FUN_1800f07e0(undefined8 param_1,undefined1 (*param_2) [16])

{
  longlong lVar1;
  ulonglong uVar2;
  longlong lVar3;
  undefined1 (*pauVar4) [16];
  undefined1 (*pauVar5) [16];
  longlong lVar6;
  char *pcVar7;
  bool bVar8;
  
  lVar1 = (*(longlong *)*param_2 << 0x14) >> 0x14;
  lVar6 = lVar1 << 4;
  if (lVar1 == 0) {
    lVar6 = 0;
  }
  pauVar4 = (undefined1 (*) [16])(lVar6 + 4);
  if (lVar6 == 0) {
    pauVar4 = param_2;
  }
  pcVar7 = "bad locale name";
  vpcmpistri_avx(*pauVar4,_DAT_1803739f8,0x18);
  uVar2 = FUN_1802cca00(DAT_1807515d0,(longlong)DAT_1803739f8);
  if ((char)uVar2 == '\0') {
    FUN_1802cd400(DAT_1807515d0,"MOVIE");
    lVar6 = DAT_1807515d0;
    lVar3 = (*(longlong *)*param_2 << 0x14) >> 0x14;
    lVar1 = lVar3 << 4;
    if (lVar3 == 0) {
      lVar1 = 0;
    }
    pauVar4 = (undefined1 (*) [16])(lVar1 + 4);
    if (lVar1 == 0) {
      pauVar4 = param_2;
    }
    pauVar5 = pauVar4 + -1;
    bVar8 = pauVar5 != (undefined1 (*) [16])0x0;
    do {
      vpcmpistri_avx(pauVar5[1],*(undefined1 (*) [16])(pcVar7 + 0x10),0x18);
      pauVar5 = pauVar5 + 1;
      pcVar7 = pcVar7 + 0x10;
    } while (pauVar4 < (undefined1 (*) [16])0x10 && bVar8);
    if (pauVar4 >= (undefined1 (*) [16])0x10) {
      if ((undefined1 (*) [16])(DAT_1807515d0 + 0x58) != param_2) {
        pauVar4 = param_2;
        if (lVar1 != 0) {
          pauVar4 = (undefined1 (*) [16])(lVar1 + 4);
        }
        FUN_180012a10((undefined1 (*) [16])(DAT_1807515d0 + 0x58),pauVar4);
      }
      *(undefined1 *)(lVar6 + 0x60) = (*param_2)[8];
      *(undefined1 *)(lVar6 + 0x61) = (*param_2)[9];
      *(undefined1 *)(lVar6 + 0x62) = (*param_2)[10];
      *(undefined8 *)(lVar6 + 100) = *(undefined8 *)(*param_2 + 0xc);
      *(undefined8 *)(lVar6 + 0x6c) = *(undefined8 *)(param_2[1] + 4);
      *(undefined4 *)(lVar6 + 0x74) = *(undefined4 *)(param_2[1] + 0xc);
      *(undefined4 *)(lVar6 + 0x78) = *(undefined4 *)param_2[2];
      *(undefined4 *)(lVar6 + 0x7c) = *(undefined4 *)(param_2[2] + 4);
      pauVar5 = (undefined1 (*) [16])(ulonglong)*(uint *)(param_2[2] + 8);
      *(uint *)(lVar6 + 0x80) = *(uint *)(param_2[2] + 8);
      *(undefined4 *)(lVar6 + 0x108) = 0x3f800000;
    }
    return CONCAT71((int7)((ulonglong)pauVar5 >> 8),1);
  }
  return uVar2 & 0xffffffffffffff00;
}
