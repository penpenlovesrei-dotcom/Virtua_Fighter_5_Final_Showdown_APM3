/* FUN_1801b5750  --  VF5FS+0x1b5750
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801b5750.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


char FUN_1801b5750(void)

{
  char cVar1;
  
  cVar1 = FUN_1802ccab0(DAT_180795c30);
  if (cVar1 != '\0') {
    return '\0';
  }
  return (*(char *)(DAT_180795c30 + 0x60) != '\0') + '\x01';
}
