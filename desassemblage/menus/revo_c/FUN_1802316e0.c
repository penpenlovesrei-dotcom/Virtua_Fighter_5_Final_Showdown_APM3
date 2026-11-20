/* FUN_1802316e0  --  VF5FS+0x2316e0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1802316e0.
 * Vidée le 2026-11-09.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


char * FUN_1802316e0(uint param_1)

{
  int iVar1;
  char cVar2;
  char *pcVar3;
  int *piVar4;
  uint local_18 [2];
  char *local_10;
  
  if ((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) {
    if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
      local_18[0] = param_1;
      (**(code **)(DAT_180c8df28 + 0x1ff08))(*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0x87,local_18)
      ;
    }
    return local_10;
  }
  if ((DAT_18079bb50 == 0) || (0x5e3c < param_1)) {
    pcVar3 = (char *)0x0;
    if (param_1 - 0x5e3e < 0x45) {
      pcVar3 = "dummy";
    }
  }
  else {
    cVar2 = FUN_18000ba20();
    if ((cVar2 == '\0') && (param_1 < 0x31)) {
      param_1 = param_1 + 0x31;
    }
    piVar4 = (int *)(DAT_18079bb50 + (ulonglong)param_1 * 4);
    iVar1 = *piVar4;
    pcVar3 = (char *)0x0;
    if (iVar1 != 0) {
      return (char *)((longlong)piVar4 + (longlong)iVar1);
    }
  }
  return pcVar3;
}
