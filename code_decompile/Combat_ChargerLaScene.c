/* Combat_ChargerLaScene  --  VF5FS+0x1c4d60
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801c4d60.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


bool Combat_ChargerLaScene(int *param_1)

{
  char cVar1;
  int iVar2;
  undefined8 uVar3;
  
  switch(*param_1) {
  case 0:
    cVar1 = FUN_18018fb20("STAGE_TASK",0);
    if (cVar1 == '\0') {
      module_demander_identifiant(1);
      *param_1 = *param_1 + 1;
      return 0x27 < *param_1;
    }
    break;
  case 1:
    cVar1 = module_identifiant_en_attente();
    if (cVar1 == '\0') {
      FUN_1800d7130(1);
      *param_1 = *param_1 + 1;
      return 0x27 < *param_1;
    }
    break;
  case 2:
    iVar2 = FUN_1800d9020();
    if (iVar2 == 0) {
      *param_1 = 10;
      return 0x27 < *param_1;
    }
    break;
  case 10:
    uVar3 = FUN_1801c3830();
    FUN_1801c3350(uVar3,param_1 + 2,param_1 + 0x116c);
    *param_1 = *param_1 + 1;
    return 0x27 < *param_1;
  case 0xb:
    uVar3 = FUN_1801c3830();
    cVar1 = FUN_1800b5860(uVar3);
    if (cVar1 != '\0') {
      FUN_18019bd80();
      FUN_1801973d0(&DAT_180750dd0);
      FUN_1801b7060(1);
      FUN_180185da0(0,"rom/sound/bgm/vfes_bgm_cus.adx",0);
      *param_1 = *param_1 + 1;
      return 0x27 < *param_1;
    }
    break;
  case 0xc:
    uVar3 = FUN_1801c3830();
    cVar1 = FUN_180244ea0(uVar3);
    if (cVar1 == '\0') {
      *param_1 = 0x28;
      return 0x27 < *param_1;
    }
    break;
  case 0x28:
    FUN_180186d40(0);
  }
  return 0x27 < *param_1;
}
