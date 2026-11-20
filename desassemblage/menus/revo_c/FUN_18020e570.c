/* FUN_18020e570  --  VF5FS+0x20e570
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18020e570.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_18020e570(undefined8 param_1,undefined1 *param_2)

{
  char cVar1;
  undefined4 uVar2;
  undefined8 uVar3;
  
  *(undefined1 *)(DAT_18079b160 + 0x2909) = 1;
  *param_2 = 1;
  cVar1 = FUN_180227f40(2);
  if (cVar1 == '\0') {
    *param_2 = 2;
    return;
  }
  uVar2 = FUN_1801da4e0();
  uVar3 = FUN_1801da490();
  FUN_180227fb0(2,uVar3,uVar2);
  return;
}
