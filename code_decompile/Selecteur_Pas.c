/* Selecteur_Pas  --  VF5FS+0x16c570
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18016c570.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* LE PAS DU SELECTEUR -- L'ORACLE  (SS 419.167)
   
   Ghidra rend ici du C lisible avec tous les fallthrough du switch, la ou le
   meme code dans REVO (0x18017AE30) ne se lit qu'en desassemblage par sa
   table de sauts. C'est donc CE corps-ci qui sert de reference.
   
   switch ([sel+0x58]) -- les fallthrough sont essentiels :
   
    case 0      montage, puis TOMBE dans case 1
    case 1      demande "SEL_COMMON", [sel+0x58] = 2, TOMBE dans case 2
    case 2..6   Selecteur_EscalierChoix(sel) :
                  rend 0 -> ce pas rend 0, on reste (phase 4 = l'ecran vivant)
                  rend 1 -> LA DOUBLE PORTE :
                    [sel+0x5d] && [sel+0x5e] (les deux joueurs inscrits) ?
                    non -> [sel+0x58] = 0xC, abandon
                    oui -> 0x175320(sel+0x3B0)   lance SEL_STAGE
                           c = (0x47DE0(0x484B0()+8) != 0)
                           si LireSorteDePartie() == 4 : c = 0x19C0B0()
                           !c              -> suivant = 0x11 (ni animation ni stage)
                           [sel+0x61] != 0 -> [sel+0x58] = 0x13 (animation puis stage)
                           sinon           -> suivant = 7 (stage, sans animation)
    case 0x13   joue "chara_start" (0x16A ou 0x16D) et "bg_light_change"
                (0x14B/0x14C), [sel+0x58] = 7, TOMBE dans case 7
    case 7..0xB Selecteur_EscalierStage(sel) : LE CHOIX DU STAGE, pas une
                intro. Rend 0 -> on reste.
    case 0xC..0x10  [sel+0x58] = 0x11, TOMBE
    case 0x11   arrete les trois sous-objets (table, sel+0x68, sel+0x3B0) -> 0x12
    case 0x12   attend que les trois soient partis -> REND 1
   
   Ce "rend 1" termine la TACHE, pas le sous-etat. SE17_SELECTOR_Phase1
   (0x1800DB270) le voit et rend 1 a son tour ; la pompe commet alors le
   sous-etat deja arme. Mode 2 = GAME, liste 17 SELECTOR -> 18 MODE_SELECTOR
   -> 19 VS -> 20 GAMEOVER.
   
   DIFFERENCES AVEC REVO, mesurees et non supposees :
     - 3e sous-objet a sel+0x3B0 ici, sel+0x3A0 dans REVO
     - APM3 a 10 modes (sentinelle 10) et 55 sous-etats (sentinelle 0x37) ;
       REVO en a 14 (sentinelle 0xE) et 73 (sentinelle 0x49)
     - REVO a insere les sous-etats CROSSPLAY_WARNING (3) et OFFLINE_WARNING
       (4), d'ou un decalage de +2 sur tous les sous-etats a partir de 3 :
       SELECTOR 17->19, MODE_SELECTOR 18->20, VS 19->21, GAMEOVER 20->22
     - et les modes WORLD_STAGE (3), RANK_MATCH (11), ROOM_MATCH (12),
       TOURNAMENT (13), d'ou MENU 4->5 et DATA_TEST 3->4. GAME reste 2.
     - APM3 a en plus 0x170930(sel+0x68, port), garde par [sel+0x5f] /
       [sel+0x60], que REVO n'appelle pas a cet endroit. */

undefined8 Selecteur_Pas(longlong param_1)

{
  char cVar1;
  int iVar2;
  longlong lVar3;
  undefined4 uVar4;
  undefined8 uVar5;
  char local_res8 [8];
  
  FUN_180172290(&DAT_180714990,0);
  if ((*(char *)(param_1 + 0x5d) != '\0') && (*(char *)(param_1 + 0x5e) != '\0')) {
    FUN_180172290(&DAT_180714990,1);
  }
  uVar5 = 0;
  if ((*(int *)(param_1 + 0x58) == 4) || (*(int *)(param_1 + 0x58) == 9)) {
    uVar5 = 1;
  }
  FUN_1801b7060(uVar5);
  switch(*(undefined4 *)(param_1 + 0x58)) {
  case 0:
    *(undefined1 *)(param_1 + 0x5c) = 1;
    cVar1 = FUN_180187cc0(0x26);
    if (cVar1 != '\0') {
      return 0;
    }
    cVar1 = FUN_180029d40(0x113);
    if (cVar1 != '\0') {
      return 0;
    }
    lVar3 = FUN_18016b0c0();
    if (*(char *)(lVar3 + 0x20) == '\0') {
      cVar1 = FUN_180187cc0(0x15e);
      if (cVar1 != '\0') {
        return 0;
      }
      uVar5 = 0x12d;
    }
    else {
      cVar1 = FUN_180187cc0(0x161);
      if (cVar1 != '\0') {
        return 0;
      }
      uVar5 = 0x130;
    }
    cVar1 = FUN_180029d40(uVar5);
    if (cVar1 != '\0') {
      return 0;
    }
    if (*(char *)(param_1 + 99) == '\0') {
      cVar1 = FUN_180187cc0(0x144);
      if (cVar1 != '\0') {
        return 0;
      }
      cVar1 = FUN_180029d40(0x112);
      if (cVar1 != '\0') {
        return 0;
      }
    }
    else {
      if (*(code **)(module_execute_info_courant + 0x1fe10) == (code *)0x0) {
        return 0;
      }
      local_res8[0] = cVar1;
      (**(code **)(module_execute_info_courant + 0x1fe10))
                (*(undefined8 *)(module_execute_info_courant + 0x1fe18),5,local_res8);
      if (local_res8[0] == '\0') {
        return 0;
      }
    }
    FUN_18019bd80();
    FUN_1801e5930();
    FUN_180186a00();
    *(undefined4 *)(param_1 + 0x58) = 1;
  case 1:
    break;
  case 2:
  case 3:
  case 4:
  case 5:
  case 6:
    goto switchD_18016c5f4_caseD_2;
  case 0x13:
    lVar3 = FUN_18016b0c0();
    cVar1 = *(char *)(lVar3 + 0x20);
    uVar5 = 0x16a;
    if (cVar1 != '\0') {
      uVar5 = 0x16d;
    }
    FUN_180171f40(&DAT_180714990,0,uVar5,"chara_start",0,7,0x10000,"loop_start","loop_end");
    FUN_180171f40(&DAT_180714990,7,(cVar1 != '\0') + 0x14b,"bg_light_change",0,1,0x10000,
                  "loop_start","loop_end");
    *(undefined4 *)(param_1 + 0x58) = 7;
  case 7:
  case 8:
  case 9:
  case 10:
  case 0xb:
    *(undefined1 *)(param_1 + 0x5c) = 0;
    cVar1 = Selecteur_EscalierStage(param_1);
    if (cVar1 == '\0') {
      return 0;
    }
  case 0xc:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x10:
    *(undefined4 *)(param_1 + 0x58) = 0x11;
  case 0x11:
    *(undefined1 *)(param_1 + 0x5c) = 0;
    FUN_18016ff00(&DAT_180714990);
    FUN_18016ff00(param_1 + 0x68);
    FUN_18016ff00(param_1 + 0x3b0);
    *(undefined4 *)(param_1 + 0x58) = 0x12;
  case 0x12:
    *(undefined1 *)(param_1 + 0x5c) = 0;
    cVar1 = FUN_180244ea0(&DAT_180714990);
    if (cVar1 != '\0') {
      return 0;
    }
    cVar1 = FUN_180244ea0(param_1 + 0x68);
    if (cVar1 != '\0') {
      return 0;
    }
    cVar1 = FUN_180244ea0(param_1 + 0x3b0);
    if (cVar1 != '\0') {
      return 0;
    }
    return 1;
  default:
    goto switchD_18016c5f4_default;
  }
  *(undefined1 *)(param_1 + 0x5c) = 1;
  FUN_180245830(&DAT_180714990,"SEL_COMMON");
  *(undefined4 *)(param_1 + 0x58) = 2;
switchD_18016c5f4_caseD_2:
  *(undefined1 *)(param_1 + 0x5c) = 1;
  cVar1 = Selecteur_EscalierChoix(param_1);
  if (cVar1 == '\0') {
    return 0;
  }
  uVar4 = 7;
  if ((*(char *)(param_1 + 99) != '\0') &&
     (*(code **)(module_execute_info_courant + 0x1fe10) != (code *)0x0)) {
    (**(code **)(module_execute_info_courant + 0x1fe10))
              (*(undefined8 *)(module_execute_info_courant + 0x1fe18),7,0);
  }
  uVar5 = DAT_180714930;
  if ((*(char *)(param_1 + 0x5d) == '\0') || (*(char *)(param_1 + 0x5e) == '\0')) {
    *(undefined4 *)(param_1 + 0x58) = 0xc;
    FUN_1800e89a0(uVar5);
  }
  else {
    FUN_180175320(param_1 + 0x3b0);
    lVar3 = FUN_1800484b0();
    iVar2 = FUN_180047de0(lVar3 + 8);
    cVar1 = iVar2 != 0;
    iVar2 = LireSorteDePartie();
    if (iVar2 == 4) {
      cVar1 = FUN_18019c0b0();
    }
    if (cVar1 == '\0') {
      uVar4 = 0x11;
    }
    else {
      cVar1 = FUN_180244ea0(param_1 + 0x68);
      if (cVar1 != '\0') {
        return 0;
      }
      if (*(char *)(param_1 + 0x61) != '\0') {
        FUN_1801973d0(&DAT_180750dd0);
        FUN_18016d180();
        *(undefined4 *)(param_1 + 0x58) = 0x13;
        _guard_check_icall(0x708);
        goto LAB_18016c7ef;
      }
    }
    *(undefined4 *)(param_1 + 0x58) = uVar4;
    _guard_check_icall(0x708);
  }
LAB_18016c7ef:
  FUN_1801018a0(DAT_18070fb10);
  _guard_check_icall(900);
switchD_18016c5f4_default:
  return 0;
}
