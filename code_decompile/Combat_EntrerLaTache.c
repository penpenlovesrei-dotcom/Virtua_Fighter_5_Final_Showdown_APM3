/* Combat_EntrerLaTache  --  VF5FS+0xbc5e0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800bc5e0.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* ORACLE : LE JUMEAU APM3 DE `Combat_EntrerLaTache` DE REVO (0x1800BD8A0).
   Trouve par les renvois vers la chaine "STAGE" en `0x18039B858`. SS 419.179.
   
   Creneau +0x10 de la table de tache `0x18039B7F8`, qui a la MEME FORME que celle
   de REVO (`0x1803C3F48`), creneau par creneau : descripteur, ?, entree, machine
   a etats, sortie, incrustation de diagnostic, deux souches. HUIT creneaux, et
   AUCUN N'EST UN DESSIN -- des deux cotes.
   
   Correspondance des champs (APM3 -> REVO) :
       vue              +0x6C8 -> +0x6F0
       objet de scene   +0x6E8 -> +0x728
       etat de la macro +0x6DC -> +0x720
       decor charge     +0x71A -> +0x75A
   
   Correspondance des appels :
       Combat_ObjetDeScene  FUN_1801509B0 -> FUN_18015B7A0  (singleton global)
       ouvrir le decor      FUN_18018FB20 -> Scene3D_Ouvrir (0x19CCE0)
       personnage/costume   FUN_1800B4590 / FUN_1800B45B0
                                          -> FUN_1800B4760 / FUN_1800B4770
       inscrire un combattant  FUN_180150450 -> Combat_InscrireCombattantDansLaScene
       constante DEUX       FUN_18005F850 -> FUN_180057890   (les deux `return 2;`)
       reserver la reserve  FUN_1801631E0 -> Rendu_ReserverReserveA
       couleur              FUN_18016B420(0xff003040) -> FUN_18017A190(0xff003040)
       evenement de fin     FUN_180087260(0x44) -> FUN_180081C50(0x46)
   
   UNE SEULE DIFFERENCE DE FOND dans tout le corps : REVO reserve une SECONDE
   reserve de rendu (`Rendu_ReserverReserveB`, 0x18016D5E0) qu'APM3 n'a pas, et la
   libere symetriquement dans la sortie. Tout le reste est identique.
   
   PORTEE DE L'ORACLE. Deux binaires independants montent le combat de la meme
   facon. Le montage de REVO n'a donc rien qui manque, et le combat vide du banc
   est un probleme de DESSIN, pas de montage. */

undefined8 Combat_EntrerLaTache(longlong param_1)

{
  char cVar1;
  undefined1 uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  int iVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  undefined8 uVar9;
  longlong lVar10;
  longlong lVar11;
  uint uVar12;
  uint in_stack_ffffffffffffff38;
  undefined4 local_b8;
  undefined1 local_b4;
  undefined2 local_b3;
  undefined4 local_b0;
  undefined4 local_ac;
  undefined4 local_a8;
  undefined4 local_a4;
  undefined8 local_a0;
  undefined1 local_98 [128];
  
  local_a0 = 0xfffffffffffffffe;
  uVar9 = Combat_ObjetDeScene();
  *(undefined8 *)(param_1 + 0x6e8) = uVar9;
  *(undefined1 *)(param_1 + 0x6d0) = 0;
  uVar12 = 0;
  *(undefined4 *)(param_1 + 0x6d4) = 0;
  *(undefined1 *)(param_1 + 0x6d8) = 0;
  *(undefined4 *)(param_1 + 0x740) = 0;
  *(undefined1 *)(param_1 + 0x6f0) = 0;
  *(undefined4 *)(param_1 + 0x6f8) = 2;
  *(undefined4 *)(param_1 + 0x6f4) = 2;
  *(undefined1 *)(param_1 + 0x719) = 0;
  *(undefined1 *)(param_1 + 0x725) = 1;
  *(undefined4 *)(param_1 + 0x6dc) = 0;
  cVar1 = FUN_180197350(&DAT_180750dd0);
  if (cVar1 == '\0') {
    if (*(char *)(param_1 + 0x71a) == '\0') {
      if (DAT_180c3b701 == '\0') {
        FUN_18019c340();
      }
      cVar1 = FUN_18018fb20("STAGE",0);
      if (cVar1 == '\0') {
        uVar3 = FUN_1800b48d0(*(undefined8 *)(param_1 + 0x6c8));
        module_demander_identifiant(uVar3);
        FUN_18018fdc0(0,1);
        *(undefined1 *)(param_1 + 0x71a) = 1;
      }
    }
    else {
      cVar1 = module_identifiant_en_attente();
      if (cVar1 == '\0') {
        _guard_check_icall();
        local_b3 = 0;
        local_b0 = 0;
        local_ac = 0;
        local_a8 = 0;
        local_a4 = 0xdd0000;
        local_b8 = 0;
        local_b4 = 1;
        uVar3 = FUN_1800b45b0(*(undefined8 *)(param_1 + 0x6c8),0);
        uVar4 = FUN_1800b4590(*(undefined8 *)(param_1 + 0x6c8),0);
        FUN_180150450(*(undefined8 *)(param_1 + 0x6e8),uVar4,&local_b8,uVar3);
        uVar3 = FUN_1800b45b0(*(undefined8 *)(param_1 + 0x6c8),1);
        uVar4 = FUN_1800b4590(*(undefined8 *)(param_1 + 0x6c8),1);
        FUN_180150450(*(undefined8 *)(param_1 + 0x6e8),uVar4,&local_b8,uVar3);
        do {
          cVar1 = FUN_1800b1b90(*(undefined8 *)(param_1 + 0x6c8),uVar12);
          if (((cVar1 != '\0') ||
              (cVar1 = FUN_1800b1d00(*(undefined8 *)(param_1 + 0x6c8),uVar12), cVar1 != '\0')) ||
             (cVar1 = FUN_1800b1d40(*(undefined8 *)(param_1 + 0x6c8),uVar12), cVar1 != '\0')) {
            lVar10 = FUN_1800b2450(*(undefined8 *)(param_1 + 0x6c8),uVar12);
            cVar1 = FUN_1800b1d00(*(undefined8 *)(param_1 + 0x6c8),uVar12);
            if ((cVar1 == '\0') &&
               (cVar1 = FUN_1800b1d40(*(undefined8 *)(param_1 + 0x6c8),uVar12), cVar1 == '\0')) {
              iVar5 = FUN_1800b45c0(*(undefined8 *)(param_1 + 0x6c8),uVar12);
              in_stack_ffffffffffffff38 = in_stack_ffffffffffffff38 & 0xffffff00;
              FUN_1801512d0(*(undefined8 *)(param_1 + 0x6e8),uVar12,
                            (longlong)iVar5 * 0x30 + 0x262 + lVar10,lVar10,in_stack_ffffffffffffff38
                           );
            }
            else {
              FUN_180199220(local_98);
              FUN_180199700(local_98,lVar10);
              iVar5 = FUN_1800b45c0(*(undefined8 *)(param_1 + 0x6c8),uVar12);
              FUN_1801513a0(*(undefined8 *)(param_1 + 0x6e8),uVar12,
                            (longlong)iVar5 * 0x30 + 0x262 + lVar10,local_98);
              FUN_1801992e0(local_98);
            }
          }
          uVar12 = uVar12 + 1;
        } while (uVar12 < 2);
        uVar3 = FUN_1800b45f0(*(undefined8 *)(param_1 + 0x6c8),0);
        lVar10 = FUN_180150920(*(undefined8 *)(param_1 + 0x6e8),0);
        *(undefined4 *)(lVar10 + 0x18) = uVar3;
        uVar3 = FUN_1800b45f0(*(undefined8 *)(param_1 + 0x6c8),1);
        lVar10 = FUN_180150920(*(undefined8 *)(param_1 + 0x6e8),1);
        *(undefined4 *)(lVar10 + 0x18) = uVar3;
        uVar9 = Constante_Rend2(*(undefined8 *)(param_1 + 0x6e8));
        Rendu_ReserverReserveA(uVar9);
        FUN_18016b420(0xff003040);
        FUN_180051a10();
        FUN_180055460(0);
        _guard_check_icall();
        FUN_1800b5a60();
        uVar3 = FUN_1800b4590(*(undefined8 *)(param_1 + 0x6c8),1);
        uVar4 = FUN_1800b4590(*(undefined8 *)(param_1 + 0x6c8),0);
        uVar6 = FUN_1800b4860(*(undefined8 *)(param_1 + 0x6c8));
        uVar7 = FUN_1800b4600(*(undefined8 *)(param_1 + 0x6c8));
        uVar8 = FUN_1800244d0(*(undefined8 *)(param_1 + 0x6c8));
        FUN_1800a0680(uVar8,uVar7,uVar6,uVar4,uVar3);
        cVar1 = FUN_1800b5800(*(undefined8 *)(param_1 + 0x6c8));
        if (((cVar1 != '\0') ||
            (cVar1 = FUN_1800b5820(*(undefined8 *)(param_1 + 0x6c8)), cVar1 != '\0')) ||
           ((iVar5 = FUN_1800244d0(*(undefined8 *)(param_1 + 0x6c8)), iVar5 == 3 ||
            (iVar5 = FUN_1800244d0(*(undefined8 *)(param_1 + 0x6c8)), iVar5 == 1)))) {
          _guard_check_icall();
        }
        _guard_check_icall();
        FUN_180185f40(0,0,0x3c);
        *(undefined8 *)(param_1 + 0x728) = 0;
        *(undefined8 *)(param_1 + 0x730) = 0;
        lVar10 = FUN_180095510();
        uVar2 = *(undefined1 *)(lVar10 + 0x108);
        iVar5 = FUN_1800b4580(*(undefined8 *)(param_1 + 0x6c8));
        *(undefined1 *)((longlong)iVar5 + 0x736 + param_1) = uVar2;
        *(undefined1 *)(param_1 + 0x738) = 0;
        *(undefined4 *)(param_1 + 0x73c) = 0;
        *(undefined8 *)(param_1 + 0x6dc) = 1;
        *(undefined8 *)(param_1 + 0x71c) = 0;
        *(undefined1 *)(param_1 + 0x724) = 0;
        iVar5 = LireSorteDePartie();
        if (iVar5 == 2) {
          FUN_1801da220();
        }
        lVar10 = module_execute_info_courant;
        if (module_execute_info_courant != 0) {
          uVar2 = FUN_1800b4590(*(undefined8 *)(param_1 + 0x6c8),0);
          *(undefined1 *)(lVar10 + 0x1fc50) = 1;
          *(undefined1 *)(lVar10 + 0x1fc54) = uVar2;
          uVar2 = FUN_1800b4590(*(undefined8 *)(param_1 + 0x6c8),1);
          *(undefined1 *)(lVar10 + 0x1fd48) = 1;
          *(undefined1 *)(lVar10 + 0x1fd4c) = uVar2;
          lVar11 = FUN_18021d210();
          cVar1 = *(char *)(lVar11 + 0x3747);
          *(undefined1 *)(lVar10 + 0x1fbe6) = 1;
          *(bool *)(lVar10 + 0x1fbea) = cVar1 == '\x01';
        }
        FUN_180087260(0x44,module_execute_info_courant);
        return 1;
      }
    }
  }
  return 0;
}
