/* FUN_18020a2b0  --  VF5FS+0x20a2b0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18020a2b0.
 * Vidée le 2026-11-10.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined8 FUN_18020a2b0(int *param_1)

{
  char cVar1;
  undefined8 uVar2;
  
  if (*(char *)((longlong)param_1 + 0x12) != '\0') {
    return 1;
  }
  *(undefined1 *)((longlong)param_1 + 0x11) = 1;
  FUN_1801da220();
  if (param_1[1] == 3) {
    cVar1 = FUN_1801a3e70(&DAT_1807956d0);
    if (cVar1 != '\0') {
      return 0;
    }
  }
  if (param_1[1] - 4U < 2) {
    cVar1 = FUN_1800ba780();
    if ((cVar1 != '\0') || (cVar1 = FUN_1800ba8a0(), cVar1 != '\0')) goto LAB_18020a3de;
    FUN_1801d9270();
  }
  param_1[1] = 0;
  if (*param_1 == 3) {
    cVar1 = FUN_1801a3e70(&DAT_1807956d0);
    if (cVar1 != '\0') {
      return 0;
    }
  }
  if (*param_1 - 4U < 2) {
    cVar1 = FUN_1800ba780();
    if ((cVar1 != '\0') || (cVar1 = FUN_1800ba8a0(), cVar1 != '\0')) {
LAB_18020a3de:
      FUN_1801d91b0();
      return 0;
    }
    FUN_1801d9270();
  }
  *param_1 = 0;
  cVar1 = thunk_FUN_1800ba920();
  if (cVar1 != '\0') {
    return 0;
  }
  FUN_1802a15d0();
  if ((char)param_1[4] != '\0') {
    uVar2 = FUN_1800b21e0();
    FUN_1800b26d0(uVar2,0);
    FUN_1800b26d0(uVar2,1);
    FUN_1800b2110();
    FUN_1801597b0(PTR_DAT_180643220);
    FUN_180159630(PTR_DAT_180643220);
    FUN_1802ccb60(&DAT_18073d970);
    *(undefined1 *)(param_1 + 4) = 0;
  }
  FUN_1801aab20();
  FUN_1801cf1f0(1);
  *(undefined1 *)((longlong)param_1 + 0x12) = 1;
  return 1;
}
