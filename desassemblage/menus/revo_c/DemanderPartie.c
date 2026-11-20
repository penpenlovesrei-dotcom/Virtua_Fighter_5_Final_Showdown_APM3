/* DemanderPartie  --  VF5FS+0x1aac20
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801aac20.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void DemanderPartie(int param_1,undefined6 *param_2,undefined1 param_3,char param_4)

{
  undefined4 uVar1;
  undefined8 uVar2;
  ulonglong uVar3;
  
  _DAT_180795934 = 0;
  DAT_180795936 = 0;
  _DAT_18079592c = (ulonglong)CONCAT16(param_3,*param_2);
  g_sorteDePartie = param_1;
  if (param_4 != '\0') {
    FUN_1801b39a0(0,1);
    FUN_1801b39a0(1,0);
  }
  uVar3 = (ulonglong)(param_4 != '\0');
  CreerObjetEntree(uVar3);
  if (param_1 - 4U < 2) {
    uVar1 = *(undefined4 *)(&DAT_1803759d8 + uVar3 * 4);
    uVar2 = LireObjetEntree();
    InscrireJoueur(uVar2,uVar1,1,0);
    if (param_1 == 5) goto LAB_1801aace2;
  }
  FUN_1801a4180(&DAT_1807956d0);
  FUN_1800da490(&DAT_18074fe70,3);
  if (param_1 != 0xb) {
    DemanderMode(2);
  }
LAB_1801aace2:
  if ((((DAT_180c8df28 != 0) && (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0)) &&
      (g_sorteDePartie == 4)) && (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0)) {
    (**(code **)(DAT_180c8df28 + 0x1ff08))(*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0xf7,0);
  }
  return;
}
