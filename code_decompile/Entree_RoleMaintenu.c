/* Entree_RoleMaintenu  --  VF5FS+0x190b80
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180190b80.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined8 Entree_RoleMaintenu(longlong param_1,int param_2)

{
  ulonglong uVar1;
  
  if ((ulonglong)(longlong)param_2 < 99) {
    uVar1 = *(ulonglong *)(param_1 + 0x20 + ((ulonglong)(longlong)param_2 >> 6) * 8);
    return CONCAT71((int7)(uVar1 >> 8),(uVar1 >> ((byte)param_2 & 0x3f) & 1) != 0);
  }
                    /* WARNING: Subroutine does not return */
  FUN_1800934d0(param_1 + 0x20);
}
