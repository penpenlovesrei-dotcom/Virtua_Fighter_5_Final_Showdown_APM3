/* Selecteur_Pas  --  VF5FS+0x17ae30
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18017ae30.
 * Vidée le 2026-11-13.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du binaire ci-dessus, gardée pour ne pas la refaire.
 */


/* LE PAS DU SELECTEUR -- 20 phases dans [sel+0x58]   (SS 419.167, corrige 419.168)
   
   Creneau +0x10 de la 2e table virtuelle (0x428270). Table de sauts a
   0x17B228, indexee par [sel+0x58], 20 entrees :
      0 -> 0x17AEB6     1 -> 0x17AFA8     2..6   -> 0x17AFC6
      7..11 -> 0x17B18A    12..16 -> 0x17B19A
      17 -> 0x17B1A5    18 -> 0x17B1D1    19 -> 0x17B0CD
   
    0,1  montage : decharge l'ecran precedent, demande "SEL_COMMON", -> 2
    2..6 appelle Selecteur_EscalierChoix (0x17B280) :
           case 2 : les DEUX ports ont un personnage reel (!= 0x15) ?
                    OUI -> [sel+0x61] = 1 et phase 5
                    NON -> demande "SEL_CHARA" sur sel+0x68, phase 3
           case 3 : attend SEL_CHARA charge -> phase 4
           case 4 : L'ECRAN VIVANT. Rend 0 tant que SEL_CHARA tourne.
                    C'est un etat de REPOS, pas un mur.
           case 5 : -> phase 6
           case 6 : [sel+0x5c] = 0 et REND 1
         rend 0 -> ce pas rend 0, on reste.
         rend 1 -> LA DOUBLE PORTE, 0x17B006 :
           [sel+0x5d] (joueur 0 a rejoint) ET [sel+0x5e] (joueur 1 a rejoint)
           >>> ATTENTION : CETTE PORTE N'ANNULE RIEN. Corrige au 419.168.
               Elle ne choisit QUE l'habillage de la sortie.
           l'un des deux a 0 -> phase 12, PUIS 12..16 -> 17 -> 18 -> rend 1
                                (ni animation de verrouillage, ni choix de
                                 stage ; le match part quand meme)
           les deux a 1 :
               0x184680(sel+0x3A0)   lance le troisieme sous-objet (SEL_STAGE)
               bl = (0x40B70(0x41230()+8) != 0)
               si LireSorteDePartie() == 4 : bl = 0x1AA6E0()
               bl == 0        -> phase 17 (ni animation ni stage)
               [sel+0x61] == 0 -> phase 7  (stage, sans animation)
               [sel+0x61] != 0 -> phase 19 (animation puis stage)
    19   joue "chara_start" (evt 0x16A ou 0x16D) et "bg_light_change"
         (0x14B/0x14C) avec "loop_start"/"loop_end" -> phase 7
    7..11 Selecteur_EscalierStage (0x17B4F0) : LE CHOIX DU STAGE, pas une
         intro. Quand il rend 1 -> phase 17
    12..16 -> phase 17
    17   0x17E370 sur les trois sous-objets (table, sel+0x68, sel+0x3A0) -> 18
    18   0x2CCA00 sur les trois ; tous partis -> REND 1
   
   LE SEUL AVORTEMENT du selecteur est [sel+0x62], pose par les branches de
   TEMPS ECOULE de Selecteur_EscalierChoix (case 4) et de
   Selecteur_EscalierStage (case 9). SE19_SELECTOR_Phase1 le lit par
   Selecteur_TempsEcoule et appelle alors DemanderMode(5) = retour au MENU.
   
   ET LA VRAIE CONDITION DE DEPART est SelChara_TousLesParticipantsOntValide
   (0x17ED50), via Selecteur_ChoixConclus (0x17BB70) : tout port qui PARTICIPE
   doit avoir atteint l'etat 6. UN SEUL JOUEUR SUFFIT.
   
   Ce "rend 1" ne lance PAS le combat : il termine la TACHE. C'est
   SE19_SELECTOR_Phase1 (0xE2470) qui, voyant la tache partie, rend 1 a son
   tour, et la pompe commet alors le sous-etat deja arme = 20 MODE_SELECTOR
   (le montage du match), puis 21 VS. Voir MachineEtats_Commettre.
   
   ORACLE APM3 : FUN_18016C570, identique, mais le 3e sous-objet y est a
   sel+0x3B0 (et non +0x3A0) et la decompilation Ghidra y rend du C lisible
   avec tous les fallthrough du switch. */

undefined8 Selecteur_Pas(longlong param_1)

{
  char cVar1;
  int iVar2;
  longlong lVar3;
  undefined4 uVar4;
  undefined8 uVar5;
  char local_res8 [8];
  
  FUN_180181480(&DAT_180759920,0);
  if ((*(char *)(param_1 + 0x5d) != '\0') && (*(char *)(param_1 + 0x5e) != '\0')) {
    FUN_180181480(&DAT_180759920,1);
  }
  uVar5 = 0;
  if ((*(int *)(param_1 + 0x58) == 4) || (*(int *)(param_1 + 0x58) == 9)) {
    uVar5 = 1;
  }
  FUN_1801cf1f0(uVar5);
  switch(*(undefined4 *)(param_1 + 0x58)) {
  case 0:
    *(undefined1 *)(param_1 + 0x5c) = 1;
    cVar1 = FUN_180196130(0x26);
    if (cVar1 != '\0') {
      return 0;
    }
    cVar1 = FUN_1800262e0(0x113);
    if (cVar1 != '\0') {
      return 0;
    }
    lVar3 = FUN_180179e70();
    if (*(char *)(lVar3 + 0x20) == '\0') {
      cVar1 = FUN_180196130(0x15e);
      if (cVar1 != '\0') {
        return 0;
      }
      uVar5 = 0x12d;
    }
    else {
      cVar1 = FUN_180196130(0x161);
      if (cVar1 != '\0') {
        return 0;
      }
      uVar5 = 0x130;
    }
    cVar1 = FUN_1800262e0(uVar5);
    if (cVar1 != '\0') {
      return 0;
    }
    if (*(char *)(param_1 + 99) == '\0') {
      cVar1 = FUN_180196130(0x144);
      if (cVar1 != '\0') {
        return 0;
      }
      cVar1 = FUN_1800262e0(0x112);
      if (cVar1 != '\0') {
        return 0;
      }
    }
    else {
      local_res8[0] = '\0';
      if (*(code **)(g_singletonDuJeu_COUPE_LES_COUCHES_0_2_3_5_6_7_8_9 + 0x1ff08) == (code *)0x0) {
        return 0;
      }
      (**(code **)(g_singletonDuJeu_COUPE_LES_COUCHES_0_2_3_5_6_7_8_9 + 0x1ff08))
                (*(undefined8 *)(g_singletonDuJeu_COUPE_LES_COUCHES_0_2_3_5_6_7_8_9 + 0x1ff10),5,
                 local_res8);
      if (local_res8[0] == '\0') {
        return 0;
      }
    }
    FUN_1801aa3b0();
    FUN_18021f0f0();
    FUN_180195090();
    *(undefined4 *)(param_1 + 0x58) = 1;
  case 1:
    break;
  case 2:
  case 3:
  case 4:
  case 5:
  case 6:
    goto switchD_18017aeb4_caseD_2;
  case 0x13:
    lVar3 = FUN_180179e70();
    cVar1 = *(char *)(lVar3 + 0x20);
    uVar5 = 0x16a;
    if (cVar1 != '\0') {
      uVar5 = 0x16d;
    }
    FUN_180180df0(&DAT_180759920,0,uVar5,"chara_start",0,7,0x10000,"loop_start","loop_end");
    FUN_180180df0(&DAT_180759920,7,(cVar1 != '\0') + 0x14b,"bg_light_change",0,1,0x10000,
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
    *(undefined1 *)(param_1 + 0x5c) = 0;
    *(undefined4 *)(param_1 + 0x58) = 0x11;
  case 0x11:
    *(undefined1 *)(param_1 + 0x5c) = 0;
    FUN_18017e370(&DAT_180759920);
    FUN_18017e370(param_1 + 0x68);
    FUN_18017e370(param_1 + 0x3a0);
    *(undefined4 *)(param_1 + 0x58) = 0x12;
  case 0x12:
    *(undefined1 *)(param_1 + 0x5c) = 0;
    cVar1 = FUN_1802cca00(&DAT_180759920);
    if (cVar1 != '\0') {
      return 0;
    }
    cVar1 = FUN_1802cca00(param_1 + 0x68);
    if (cVar1 != '\0') {
      return 0;
    }
    cVar1 = FUN_1802cca00(param_1 + 0x3a0);
    if (cVar1 != '\0') {
      return 0;
    }
    return 1;
  default:
    goto switchD_18017aeb4_default;
  }
  *(undefined1 *)(param_1 + 0x5c) = 1;
  FUN_1802cd400(&DAT_180759920,"SEL_COMMON");
  *(undefined4 *)(param_1 + 0x58) = 2;
switchD_18017aeb4_caseD_2:
  *(undefined1 *)(param_1 + 0x5c) = 1;
  cVar1 = Selecteur_EscalierChoix(param_1);
  if (cVar1 == '\0') {
    return 0;
  }
  uVar4 = 7;
  if ((*(char *)(param_1 + 99) != '\0') &&
     (*(code **)(g_singletonDuJeu_COUPE_LES_COUCHES_0_2_3_5_6_7_8_9 + 0x1ff08) != (code *)0x0)) {
    (**(code **)(g_singletonDuJeu_COUPE_LES_COUCHES_0_2_3_5_6_7_8_9 + 0x1ff08))
              (*(undefined8 *)(g_singletonDuJeu_COUPE_LES_COUCHES_0_2_3_5_6_7_8_9 + 0x1ff10),7,0);
  }
  uVar5 = DAT_1807598c0;
  if ((*(char *)(param_1 + 0x5d) == '\0') || (*(char *)(param_1 + 0x5e) == '\0')) {
    *(undefined4 *)(param_1 + 0x58) = 0xc;
    FUN_1800f0a50(uVar5);
  }
  else {
    FUN_180184680(param_1 + 0x3a0);
    lVar3 = FUN_180041230();
    iVar2 = FUN_180040b70(lVar3 + 8);
    cVar1 = iVar2 != 0;
    iVar2 = LireSorteDePartie();
    if (iVar2 == 4) {
      cVar1 = FUN_1801aa6e0();
    }
    if (cVar1 == '\0') {
      uVar4 = 0x11;
    }
    else {
      cVar1 = FUN_1802cca00(param_1 + 0x68);
      if (cVar1 != '\0') {
        return 0;
      }
      if (*(char *)(param_1 + 0x61) != '\0') {
        FUN_1801a3f20(&DAT_1807956d0);
        FUN_18017ba00();
        *(undefined4 *)(param_1 + 0x58) = 0x13;
        _guard_check_icall(0x708);
        goto LAB_18017b0b2;
      }
    }
    *(undefined4 *)(param_1 + 0x58) = uVar4;
    _guard_check_icall(0x708);
  }
LAB_18017b0b2:
  FUN_180106fb0(DAT_180754a90);
  _guard_check_icall(900);
switchD_18017aeb4_default:
  return 0;
}
