/* Selecteur_EscalierChoix  --  VF5FS+0x16c9c0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18016c9c0.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined8 Selecteur_EscalierChoix(longlong param_1)

{
  bool bVar1;
  bool bVar2;
  char cVar3;
  int iVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined8 uVar7;
  
  uVar7 = LireObjetEntree();
  bVar1 = false;
  if (*(char *)(param_1 + 0x5d) != '\0') {
    iVar4 = FUN_1800b23e0(uVar7,0);
    uVar5 = FUN_1800b2400(uVar7,0);
    uVar6 = FUN_1800b2410(uVar7,0);
    if (iVar4 == 0x15) {
      FUN_18016fdf0(param_1 + 0x68,0);
    }
    else {
      FUN_180170750(param_1 + 0x68,0,iVar4,uVar5,uVar6);
    }
    if (*(char *)(param_1 + 0x5f) != '\0') {
      FUN_180170930(param_1 + 0x68,0);
    }
    bVar1 = false;
    if (iVar4 != 0x15) {
      bVar1 = true;
    }
  }
  bVar2 = false;
  if (*(char *)(param_1 + 0x5e) != '\0') {
    iVar4 = FUN_1800b23e0(uVar7,1);
    uVar5 = FUN_1800b2400(uVar7,1);
    uVar6 = FUN_1800b2410(uVar7,1);
    if (iVar4 == 0x15) {
      FUN_18016fdf0(param_1 + 0x68,1);
    }
    else {
      FUN_180170750(param_1 + 0x68,1,iVar4,uVar5,uVar6);
    }
    if (*(char *)(param_1 + 0x60) != '\0') {
      FUN_180170930(param_1 + 0x68,1);
    }
    bVar2 = false;
    if (iVar4 != 0x15) {
      bVar2 = true;
    }
  }
  iVar4 = *(int *)(param_1 + 0x58);
  if (iVar4 == 2) {
    if ((bVar1) && (bVar2)) {
      *(undefined1 *)(param_1 + 0x61) = 1;
      *(undefined4 *)(param_1 + 0x58) = 5;
      return 0;
    }
    FUN_1801973d0(&DAT_180750dd0);
    FUN_18016d180();
    FUN_180245830(param_1 + 0x68,"SEL_CHARA");
    *(undefined4 *)(param_1 + 0x58) = 3;
LAB_18016cb64:
    cVar3 = FUN_180170740(param_1 + 0x68);
    if (cVar3 == '\0') {
      return 0;
    }
    *(undefined4 *)(param_1 + 0x58) = 4;
LAB_18016cb78:
    if ((*(char *)(param_1 + 0x62) == '\0') &&
       (((cVar3 = FUN_180170620(param_1 + 0x68), cVar3 != '\0' ||
         (cVar3 = FUN_180175360(param_1 + 0x3b0), cVar3 != '\0')) && (DAT_180c3b701 == '\0')))) {
      FUN_1801a3020();
      *(undefined1 *)(param_1 + 0x62) = 1;
      FUN_1802450a0(param_1 + 0x68);
      if ((*(char *)(param_1 + 99) != '\0') &&
         (*(code **)(module_execute_info_courant + 0x1fe10) != (code *)0x0)) {
        (**(code **)(module_execute_info_courant + 0x1fe10))
                  (*(undefined8 *)(module_execute_info_courant + 0x1fe18),7);
      }
      FUN_1800e89a0(DAT_180714930);
      *(undefined4 *)(param_1 + 0x58) = 0x11;
      return 0;
    }
    cVar3 = FUN_180170610(param_1 + 0x68);
    if (cVar3 != '\0') {
      return 0;
    }
  }
  else {
    if (iVar4 == 3) goto LAB_18016cb64;
    if (iVar4 == 4) goto LAB_18016cb78;
    if (iVar4 != 5) {
      if (iVar4 != 6) {
        *(undefined4 *)(param_1 + 0x58) = 2;
        return 0;
      }
      goto LAB_18016cc14;
    }
  }
  *(undefined4 *)(param_1 + 0x58) = 6;
LAB_18016cc14:
  *(undefined1 *)(param_1 + 0x5c) = 0;
  return 1;
}
