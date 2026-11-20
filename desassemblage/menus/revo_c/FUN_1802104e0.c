/* FUN_1802104e0  --  VF5FS+0x2104e0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1802104e0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1802104e0(undefined8 param_1,char param_2)

{
  char local_res10 [24];
  
  if ((((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) &&
      ((param_2 == '\0' || ((param_2 == '\x01' || (param_2 == '\x02')))))) &&
     (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0)) {
    local_res10[0] = param_2;
    (**(code **)(DAT_180c8df28 + 0x1ff08))
              (*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xd6,local_res10);
  }
  return;
}
