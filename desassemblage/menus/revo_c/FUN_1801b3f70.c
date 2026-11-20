/* FUN_1801b3f70  --  VF5FS+0x1b3f70
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801b3f70.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1801b3f70(void)

{
  undefined8 *puVar1;
  
  puVar1 = (undefined8 *)FUN_1802ecd50(0x4b0,0x10);
  if (puVar1 != (undefined8 *)0x0) {
    FUN_1801de060(puVar1);
    *puVar1 = _anon_6B24EAF8::TaskMenuTeam::vftable;
    puVar1[0x4a] = 0;
    puVar1[0x4b] = 0;
    *(undefined4 *)(puVar1 + 0x4c) = 0;
    puVar1[0x4d] = 0;
    *(undefined8 *)((longlong)puVar1 + 0x274) = 0;
    puVar1[0x54] = 0;
    puVar1[0x55] = 0;
    *(undefined4 *)(puVar1 + 0x56) = 0;
    puVar1[0x57] = 0;
    *(undefined8 *)((longlong)puVar1 + 0x2c4) = 0;
    puVar1[0x5e] = 0;
    puVar1[0x5f] = 0;
    FUN_1801dfb10();
    FUN_1802cc880(puVar1 + 0x60);
    *(undefined4 *)(puVar1 + 0x72) = 0;
    *(undefined2 *)((longlong)puVar1 + 0x394) = 0;
    puVar1[0x73] = 0;
    puVar1[0x74] = 0;
    *(undefined1 *)(puVar1 + 0x75) = 0;
    puVar1[0x76] = 0;
    *(undefined1 *)(puVar1 + 0x77) = 0;
    puVar1[0x7d] = 0;
    puVar1[0x7e] = 0;
    *(undefined4 *)(puVar1 + 0x7f) = 0;
    puVar1[0x80] = 0;
    *(undefined8 *)((longlong)puVar1 + 0x40c) = 0;
    puVar1[0x87] = 0;
    puVar1[0x88] = 0;
    *(undefined4 *)(puVar1 + 0x89) = 0;
    puVar1[0x8a] = 0;
    *(undefined8 *)((longlong)puVar1 + 0x45c) = 0;
    puVar1[0x60] = _anon_6B24EAF8::TaskClearInfo::vftable;
    FUN_1801aa1f0(puVar1 + 0x94);
    DAT_180795c38 = puVar1;
    return;
  }
  DAT_180795c38 = (undefined8 *)0x0;
  return;
}
