/* FUN_1801909d0  --  VF5FS+0x1909d0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801909d0.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1801909d0(void)

{
  int iVar1;
  undefined4 *puVar2;
  int iVar3;
  undefined *puVar4;
  
  iVar1 = 0;
  puVar2 = &DAT_180749c28;
  iVar3 = 0;
  do {
    FUN_180007450(*puVar2,iVar3);
    iVar3 = iVar3 + 1;
    puVar2 = puVar2 + 0x21a;
  } while (iVar3 < 2);
  _guard_check_icall();
  FUN_1801a1af0();
  FUN_1801b2020();
  puVar4 = &g_entreeRoles;
  do {
    FUN_180190c40(puVar4,iVar1);
    iVar1 = iVar1 + 1;
    puVar4 = puVar4 + 0x868;
  } while (iVar1 < 2);
  return;
}
