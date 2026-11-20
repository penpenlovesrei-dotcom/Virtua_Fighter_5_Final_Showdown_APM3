/* FUN_1801bb3a0  --  VF5FS+0x1bb3a0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801bb3a0.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


longlong FUN_1801bb3a0(int param_1,int param_2,char param_3)

{
  longlong lVar1;
  longlong lVar2;
  char cVar3;
  
  lVar2 = DAT_180795c50;
  lVar1 = DAT_180795c48;
  if ((param_2 == 2) && (param_1 != 0)) {
    *(undefined4 *)(DAT_180795c50 + 0x3f4) = 2;
    *(int *)(lVar2 + 0x3f0) = param_1;
    cVar3 = FUN_1802cd400(lVar2,"OPTION CONTROL");
    if (cVar3 != '\0') {
      return DAT_180795c50;
    }
  }
  else {
    *(int *)(DAT_180795c48 + 0x1520) = param_1;
    DAT_180795c40 = param_2;
    if (param_3 != '\0') {
      *(undefined4 *)(lVar1 + 0xb8) = 0;
      *(undefined4 *)(lVar1 + 0x338) = 0;
    }
    cVar3 = FUN_1802cd400(lVar1,"OPTION");
    if (cVar3 != '\0') {
      return DAT_180795c48;
    }
  }
  return 0;
}
