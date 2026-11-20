/* Selecteur_EscalierStage  --  VF5FS+0x16cc30
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18016cc30.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined8 Selecteur_EscalierStage(longlong param_1)

{
  char cVar1;
  int iVar2;
  undefined4 uVar3;
  undefined8 uVar4;
  
  iVar2 = *(int *)(param_1 + 0x58);
  if (iVar2 == 7) {
LAB_18016cc6c:
    FUN_180245830(param_1 + 0x3b0,"SEL_STAGE");
    *(undefined4 *)(param_1 + 0x58) = 8;
LAB_18016cc86:
    cVar1 = FUN_180170740(param_1 + 0x3b0);
    if (cVar1 == '\0') {
      return 0;
    }
    if (*(char *)(param_1 + 0x5d) == '\0') {
      uVar3 = 1;
    }
    else if (*(char *)(param_1 + 0x5e) == '\0') {
      uVar3 = 0;
    }
    else {
      uVar4 = LireObjetEntree();
      iVar2 = FUN_1800244d0(uVar4);
      if ((*(uint *)(&DAT_18034b208 + (longlong)iVar2 * 4) < 2) &&
         (*(char *)((longlong)(int)*(uint *)(&DAT_18034b208 + (longlong)iVar2 * 4) + 0x5f + param_1)
          != '\0')) {
        uVar4 = LireObjetEntree();
        uVar3 = FUN_1800244d0(uVar4);
      }
      else {
        uVar4 = LireObjetEntree();
        iVar2 = FUN_1800244d0(uVar4);
        uVar3 = *(undefined4 *)(&DAT_18034b208 + (longlong)iVar2 * 4);
      }
    }
    FUN_1801748b0(param_1 + 0x3b0,uVar3);
    *(undefined4 *)(param_1 + 0x58) = 9;
  }
  else {
    if (iVar2 == 8) goto LAB_18016cc86;
    if (iVar2 != 9) {
      if (iVar2 == 10) goto LAB_18016cdbd;
      if (iVar2 == 0xb) {
        return 1;
      }
      *(undefined4 *)(param_1 + 0x58) = 7;
      goto LAB_18016cc6c;
    }
  }
  if ((*(char *)(param_1 + 0x62) == '\0') &&
     (((cVar1 = FUN_180170620(param_1 + 0x68), cVar1 != '\0' ||
       (cVar1 = FUN_180175360(param_1 + 0x3b0), cVar1 != '\0')) && (DAT_180c3b701 == '\0')))) {
    FUN_1801a3020();
    *(undefined1 *)(param_1 + 0x62) = 1;
    FUN_1802450a0(param_1 + 0x3b0);
    if ((*(char *)(param_1 + 99) != '\0') &&
       (*(code **)(module_execute_info_courant + 0x1fe10) != (code *)0x0)) {
      (**(code **)(module_execute_info_courant + 0x1fe10))
                (*(undefined8 *)(module_execute_info_courant + 0x1fe18),7);
    }
    FUN_1800e89a0(DAT_180714930);
    *(undefined4 *)(param_1 + 0x58) = 0x11;
    return 0;
  }
  cVar1 = FUN_180170610(param_1 + 0x3b0);
  if (cVar1 != '\0') {
    return 0;
  }
LAB_18016cdbd:
  *(undefined4 *)(param_1 + 0x58) = 0xb;
  return 1;
}
