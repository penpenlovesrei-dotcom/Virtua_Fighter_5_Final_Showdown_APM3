/* FUN_180081c50  --  VF5FS+0x81c50
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180081c50.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_180081c50(int param_1,undefined8 param_2)

{
  longlong *plVar1;
  int iVar2;
  longlong lVar3;
  longlong local_410 [129];
  
  if (((DAT_180c8df28 != 0) && (param_1 != -1)) &&
     (*(code **)(DAT_180c8df28 + 0x20348) != (code *)0x0)) {
    (**(code **)(DAT_180c8df28 + 0x20348))(param_1);
  }
  iVar2 = 0;
  if ((DAT_18073aa10 == 1) && (*(int *)(&DAT_18073aa20 + (longlong)param_1 * 0x10) == 1)) {
    lVar3 = *(longlong *)(&DAT_18073aa28 + (longlong)param_1 * 0x10);
    if (lVar3 != 0) {
      plVar1 = local_410 + 1;
      do {
        if ((*(longlong *)(lVar3 + 0x18) != 0) && (*(char *)(lVar3 + 0x20) != '\0')) {
          iVar2 = iVar2 + 1;
          *plVar1 = lVar3;
          plVar1 = plVar1 + 1;
        }
        lVar3 = *(longlong *)(lVar3 + 8);
      } while (lVar3 != 0);
    }
    lVar3 = (longlong)iVar2;
    if (iVar2 != 0) {
      plVar1 = local_410 + lVar3;
      do {
        (**(code **)(*plVar1 + 0x18))(*(undefined8 *)(*plVar1 + 0x10),param_2);
        plVar1 = plVar1 + -1;
        lVar3 = lVar3 + -1;
      } while (lVar3 != 0);
    }
  }
  return;
}
