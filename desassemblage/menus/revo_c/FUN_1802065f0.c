/* FUN_1802065f0  --  VF5FS+0x2065f0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1802065f0.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1802065f0(void)

{
  undefined8 *puVar1;
  
  puVar1 = (undefined8 *)FUN_1802ecd50(0x450,0x10);
  if (puVar1 != (undefined8 *)0x0) {
    FUN_1801de060(puVar1);
    *puVar1 = TaskMenuMulti::vftable;
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
    FUN_1800e4d00(puVar1 + 0x5b);
    puVar1[0x88] = 0;
    DAT_18079b168 = puVar1;
    return;
  }
  DAT_18079b168 = (undefined8 *)0x0;
  return;
}
