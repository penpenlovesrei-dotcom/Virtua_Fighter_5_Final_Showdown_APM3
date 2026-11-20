/* FUN_1801b3e40  --  VF5FS+0x1b3e40
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801b3e40.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1801b3e40(void)

{
  undefined8 *puVar1;
  
  puVar1 = (undefined8 *)FUN_1802ecd50(0x330,0x10);
  if (puVar1 != (undefined8 *)0x0) {
    FUN_1801de060(puVar1);
    *puVar1 = _anon_6B24EAF8::TaskMenuSetting::vftable;
    FUN_1801aa1f0(puVar1 + 0x46);
    puVar1[0x4e] = 0;
    puVar1[0x4f] = 0;
    *(undefined4 *)(puVar1 + 0x50) = 0;
    puVar1[0x51] = 0;
    *(undefined8 *)((longlong)puVar1 + 0x294) = 0;
    puVar1[0x58] = 0;
    puVar1[0x59] = 0;
    *(undefined4 *)(puVar1 + 0x5a) = 0;
    puVar1[0x5b] = 0;
    *(undefined8 *)((longlong)puVar1 + 0x2e4) = 0;
    puVar1[0x62] = 0;
    puVar1[99] = 0;
    FUN_1801dfb10((longlong)puVar1 + 0x2f4);
    puVar1[100] = 0;
    FUN_1801dfb90((longlong)puVar1 + 0x2f4);
    DAT_180795c30 = puVar1;
    return;
  }
  DAT_180795c30 = (undefined8 *)0x0;
  return;
}
