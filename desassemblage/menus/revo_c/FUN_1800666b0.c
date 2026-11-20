/* FUN_1800666b0  --  VF5FS+0x666b0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800666b0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1800666b0(void)

{
  char cVar1;
  int iVar2;
  undefined8 uVar3;
  
  FUN_1802cd400(&DAT_1806bacc0,"DATA_INITIALIZE");
  FUN_18003f1a0();
  FUN_180025df0();
  FUN_180026620();
  uVar3 = FUN_180132710();
  FUN_180026620(uVar3);
  FUN_180194570("rom/sound/se_adam.csb");
  FUN_180277a20();
  cVar1 = FUN_1801952b0("rom/sound/se_adam.csb");
  while (cVar1 != '\0') {
    FUN_1802f12a0(100);
    FUN_180277a20();
    cVar1 = FUN_1801952b0("rom/sound/se_adam.csb");
  }
  FUN_1802c4920();
  iVar2 = FUN_18000ba10();
  if (iVar2 == 2) {
    _guard_check_icall();
    return;
  }
  if (iVar2 != 3) {
    return;
  }
  _guard_check_icall();
  return;
}
