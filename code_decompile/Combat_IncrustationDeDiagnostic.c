/* Combat_IncrustationDeDiagnostic  --  VF5FS+0xbc1d0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800bc1d0.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void Combat_IncrustationDeDiagnostic(longlong param_1)

{
  longlong lVar1;
  undefined8 uVar2;
  char cVar3;
  int iVar4;
  
  cVar3 = FUN_180007450();
  if (cVar3 == '\0') {
    if (*(int *)(param_1 + 0x6dc) == 8) {
      iVar4 = FUN_1801915e0(1);
      if (30000 < iVar4) {
        FUN_1801087b0(0x38);
        FUN_1801080f0(0,0x42480000,9);
        FUN_180108880(0xffff0000);
        FUN_180108200(&DAT_180346d24,1);
      }
    }
    lVar1 = LireObjetEntree();
    if (lVar1 != 0) {
      uVar2 = LireObjetEntree();
      lVar1 = FUN_1800b24b0(uVar2);
      if (*(longlong *)(lVar1 + 0x1090) != 0) {
        cVar3 = FUN_180166ed0();
        if (cVar3 == '\0') {
          FUN_1801087b0(0x38);
          FUN_1801080f0(0,0x42940000,9);
          FUN_180108880(0xff00ff00);
          FUN_180108200(&DAT_180346d24,1);
          return;
        }
      }
    }
  }
  return;
}
