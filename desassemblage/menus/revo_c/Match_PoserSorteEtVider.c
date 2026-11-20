/* Match_PoserSorteEtVider  --  VF5FS+0x1aabe0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801aabe0.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void Match_PoserSorteEtVider(undefined4 param_1,undefined1 param_2,char param_3)

{
  g_sorteDePartie = param_1;
  _DAT_18079592c = 0;
  DAT_180795934 = 0;
  DAT_180795936 = 0;
  DAT_180795935 = param_2;
  if (param_3 != '\0') {
    DemanderMode(7);
    return;
  }
  return;
}
