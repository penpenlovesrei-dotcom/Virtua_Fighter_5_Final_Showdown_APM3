/* FUN_1801c0100  --  VF5FS+0x1c0100
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801c0100.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined * FUN_1801c0100(void)

{
  char cVar1;
  undefined *puVar2;
  
  cVar1 = FUN_1802cd400(&DAT_180795c70,"RANKING");
  puVar2 = (undefined *)0x0;
  if (cVar1 != '\0') {
    puVar2 = &DAT_180795c70;
  }
  return puVar2;
}
