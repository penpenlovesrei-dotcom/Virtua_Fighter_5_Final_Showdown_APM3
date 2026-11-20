/* FUN_1801cfd80  --  VF5FS+0x1cfd80
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801cfd80.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1801cfd80(char param_1,int param_2)

{
  longlong lVar1;
  char cVar2;
  undefined8 uVar3;
  
  if (*(char *)(DAT_180796db0 + 0x1122c) != '\0') {
    cVar2 = FUN_1802cca00(&DAT_1807969a0);
    lVar1 = DAT_180796db0;
    if (cVar2 == '\0') {
      *(undefined1 *)(DAT_180796db0 + 0x11085) = 0;
      *(undefined4 *)(lVar1 + 0x11088) = 3;
      if (param_2 < 0) {
        param_2 = FUN_18000ba10();
      }
      cVar2 = FUN_180026620(param_2);
      if (((cVar2 != '\0') && (param_2 == *(int *)(DAT_180796db0 + 0x11080))) &&
         ((param_1 == '\0' || (*(int *)(DAT_180796db0 + 0x96a8) != 0)))) {
        FUN_1801d0320();
        uVar3 = FUN_1801dd040();
        FUN_1801dd060(uVar3);
        FUN_1801d62a0(&DAT_1807969a0,param_2,DAT_180796db0,param_1,&LAB_1801ce900);
      }
    }
  }
  return;
}
