/* FUN_1802ccab0  --  VF5FS+0x2ccab0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1802ccab0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined8 FUN_1802ccab0(longlong param_1)

{
  longlong *plVar1;
  bool bVar2;
  
  plVar1 = (longlong *)*DAT_180ea7608;
  bVar2 = plVar1 == (longlong *)0x0;
  if (!bVar2) {
    do {
      if (*plVar1 == param_1) break;
      plVar1 = (longlong *)plVar1[2];
    } while (plVar1 != (longlong *)0x0);
    bVar2 = plVar1 == (longlong *)0x0;
  }
  return CONCAT71((int7)((ulonglong)plVar1 >> 8),!bVar2);
}
