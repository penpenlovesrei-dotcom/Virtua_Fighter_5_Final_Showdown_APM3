/* Selecteur_EscalierChoix  --  VF5FS+0x17b280
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18017b280.
 * Vidée le 2026-11-13.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du binaire ci-dessus, gardée pour ne pas la refaire.
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
    iVar4 = FUN_1800b22c0(uVar7,0);
    uVar5 = FUN_1800b22e0(uVar7,0);
    uVar6 = FUN_1800b22f0(uVar7,0);
    if (iVar4 == 0x15) {
      FUN_18017e290(param_1 + 0x68,0);
    }
    else {
      FUN_18017ee50(param_1 + 0x68,0,iVar4,uVar5,uVar6);
    }
    if (*(char *)(param_1 + 0x5f) != '\0') {
      FUN_18017f070(param_1 + 0x68,0);
    }
    bVar1 = false;
    if (iVar4 != 0x15) {
      bVar1 = true;
    }
  }
  bVar2 = false;
  if (*(char *)(param_1 + 0x5e) != '\0') {
    iVar4 = FUN_1800b22c0(uVar7,1);
    uVar5 = FUN_1800b22e0(uVar7,1);
    uVar6 = FUN_1800b22f0(uVar7,1);
    if (iVar4 == 0x15) {
      FUN_18017e290(param_1 + 0x68,1);
    }
    else {
      FUN_18017ee50(param_1 + 0x68,1,iVar4,uVar5,uVar6);
    }
    if (*(char *)(param_1 + 0x60) != '\0') {
      FUN_18017f070(param_1 + 0x68,1);
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
    FUN_1801a3f20(&DAT_1807956d0);
    FUN_18017ba00();
    FUN_1802cd400(param_1 + 0x68,"SEL_CHARA");
    *(undefined4 *)(param_1 + 0x58) = 3;
LAB_18017b424:
    cVar3 = FUN_18017ee40(param_1 + 0x68);
    if (cVar3 == '\0') {
      return 0;
    }
    *(undefined4 *)(param_1 + 0x58) = 4;
LAB_18017b438:
    if ((*(char *)(param_1 + 0x62) == '\0') &&
       (((cVar3 = FUN_18017ed20(param_1 + 0x68), cVar3 != '\0' ||
         (cVar3 = FUN_1801846c0(param_1 + 0x3a0), cVar3 != '\0')) && (DAT_180c8de18 == '\0')))) {
      FUN_1801b34a0();
      *(undefined1 *)(param_1 + 0x62) = 1;
      FUN_1802ccb60(param_1 + 0x68);
      if ((*(char *)(param_1 + 99) != '\0') &&
         (*(code **)(g_singletonDuJeu_COUPE_LES_COUCHES_0_2_3_5_6_7_8_9 + 0x1ff08) != (code *)0x0))
      {
        (**(code **)(g_singletonDuJeu_COUPE_LES_COUCHES_0_2_3_5_6_7_8_9 + 0x1ff08))
                  (*(undefined8 *)(g_singletonDuJeu_COUPE_LES_COUCHES_0_2_3_5_6_7_8_9 + 0x1ff10),7,0
                  );
      }
      FUN_1800f0a50(DAT_1807598c0);
      *(undefined4 *)(param_1 + 0x58) = 0x11;
      return 0;
    }
    cVar3 = FUN_18017ed10(param_1 + 0x68);
    if (cVar3 != '\0') {
      return 0;
    }
  }
  else {
    if (iVar4 == 3) goto LAB_18017b424;
    if (iVar4 == 4) goto LAB_18017b438;
    if (iVar4 != 5) {
      if (iVar4 != 6) {
        *(undefined4 *)(param_1 + 0x58) = 2;
        return 0;
      }
      goto LAB_18017b4d5;
    }
  }
  *(undefined4 *)(param_1 + 0x58) = 6;
LAB_18017b4d5:
  *(undefined1 *)(param_1 + 0x5c) = 0;
  return 1;
}
