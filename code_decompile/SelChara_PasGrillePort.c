/* SelChara_PasGrillePort  --  VF5FS+0x173110
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180173110.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* LE PAS PAR PORT DE LA GRILLE -- ORACLE DE REVO 0x181FE0 (SS 419.170)
   
   grille = selchara + 0xC8 ; rec = grille + (port+2)*0x40.
   Sorties precoces identiques a REVO, a une pres : APM3 appelle
   SelChara_PortAValide(grille, port) la ou REVO deplie les trois tests
   (+0x20 == 6, == 7, +0x28 == 6). Meme semantique.
   
   LA SEULE VRAIE DIVERGENCE EST LA BANQUE D'ENTREE QU'IL LIT.
   
   APM3 lit la COUCHE DE ROLES :
       obj = Entree_RolesDuPort(port) = g_entreeRoles + port*0x868
       VALIDER   : Entree_RoleFront(obj, 9 | 7 | 8 | 0xB)   -> rec[0x28] = 6
       DIRECTIONS: Entree_RoleMaintenu(obj, 3 | 4 | 5 | 6)
                   (3 HAUT, 4 BAS, 5 GAUCHE, 6 DROITE)
       obj+0x00 = jeu de bits FRONT, obj+0x20 = jeu de bits MAINTENU,
       99 bits chacun, indexes par le CODE DE ROLE.
   
   REVO lit la BANQUE BRUTE, avec les MASQUES arcade :
       Entree_QuelSlotAValide()                  -> masque 1   == role 7
       Entree_EtatMaintenu(slot, 0x10000000..)   -> roles 3..6
       soit g_entreeEnregistrements + port*0x54, recopie VERBATIM de
       notre bloc+0x20 par Entree_ConstruireEnregistrements.
   
   Les deux grilles sont donc SEMANTIQUEMENT IDENTIQUES -- front pour
   valider, maintenu pour les directions, avec le meme compteur de
   repetition maison (0x14 puis 0xA) en [lVar19+0xb0]/[0xb4] (REVO :
   rec[0x30]/rec[0x34]). Elles ne divergent que sur la banque lue.
   
   CONSEQUENCE POUR NOTRE GREFFE : REVO teste la banque brute avec le
   VOCABULAIRE ARCADE. Notre hote remplit bloc+0x20 en vocabulaire
   sl::BUTTON et n'envoie le vocabulaire arcade que par la commande 364,
   que Entree_DecoderRolesDepuis364 (REVO 0x1B2CC0) range dans la couche
   de roles -- couche que la grille de REVO NE LIT PAS. Voir 419.170.
   
   Les quatre roles de validation d'APM3 (9, 7, 8, 0xB) : la table de 13
   entrees de REVO donne 7 -> 0x01, 8 -> 0x02, 9 -> 0x04 ; le role 0xB
   n'y est PAS, il vient d'ailleurs (champ configurable DAT_180795ACC
   dans REVO). REVO n'en garde qu'un, le role 7. */

void SelChara_PasGrillePort(longlong param_1,int param_2)

{
  int *piVar1;
  bool bVar2;
  int iVar3;
  char cVar4;
  char cVar5;
  char cVar6;
  char cVar7;
  undefined4 uVar8;
  int iVar9;
  undefined8 uVar10;
  undefined8 *puVar11;
  int iVar12;
  ulonglong uVar13;
  uint uVar14;
  uint uVar15;
  int iVar16;
  int iVar17;
  uint uVar18;
  longlong lVar19;
  int iVar20;
  int iVar21;
  int iVar22;
  int iVar23;
  char *pcVar24;
  int local_res10;
  undefined4 local_res18;
  undefined8 local_78;
  undefined8 local_70;
  undefined8 local_68;
  undefined8 local_60;
  undefined8 local_58;
  undefined8 local_50;
  
  lVar19 = (longlong)param_2 * 0x40 + param_1;
  uVar10 = Entree_RolesDuPort(param_2);
  pcVar24 = (char *)(((longlong)param_2 + 2) * 0x40 + param_1);
  if (*pcVar24 == '\0') {
    return;
  }
  cVar4 = SelChara_PortAValide(param_1,param_2);
  if (cVar4 != '\0') {
    return;
  }
  if (*(longlong **)(lVar19 + 0x88) == (longlong *)0x0) {
    return;
  }
  if (**(longlong **)(lVar19 + 0x88) == 0) {
    return;
  }
  if (*(char *)(lVar19 + 0x81) == '\0') {
    return;
  }
  if (*(longlong *)(module_execute_info_courant + 0x1fe10) != 0) {
    local_78 = 0xd;
    local_70 = 0x10000;
    local_68 = 0;
    local_60 = 0;
    local_58 = 0;
    local_50 = 0;
    if (*(code **)(module_execute_info_courant + 0x1fe10) != (code *)0x0) {
      (**(code **)(module_execute_info_courant + 0x1fe10))
                (*(undefined8 *)(module_execute_info_courant + 0x1fe18),6,&local_78);
      if (local_70._2_1_ == '\0') {
        return;
      }
    }
  }
  uVar14 = 9;
  cVar4 = Entree_RoleFront(uVar10,9);
  iVar22 = 1;
  cVar5 = Entree_RoleFront(uVar10,7);
  cVar6 = Entree_RoleFront(uVar10,8);
  cVar7 = Entree_RoleFront(uVar10,0xb);
  if ((cVar7 != '\0') || (cVar6 != '\0' || (cVar5 != '\0' || cVar4 != '\0'))) {
    *(undefined8 *)(pcVar24 + 0x18) = *(undefined8 *)(pcVar24 + 8);
    pcVar24[0x28] = '\x06';
    pcVar24[0x29] = '\0';
    pcVar24[0x2a] = '\0';
    pcVar24[0x2b] = '\0';
    return;
  }
  iVar23 = 0;
  iVar16 = *(int *)**(undefined8 **)(lVar19 + 0x88);
  iVar21 = ((int *)**(undefined8 **)(lVar19 + 0x88))[1];
  cVar4 = Entree_RoleMaintenu(uVar10,3);
  local_res10 = -1;
  iVar17 = 0;
  if (cVar4 == '\0') {
    cVar4 = Entree_RoleMaintenu(uVar10,4);
    if (cVar4 == '\0') {
      cVar4 = Entree_RoleMaintenu(uVar10,5);
      if (cVar4 == '\0') {
        cVar4 = Entree_RoleMaintenu(uVar10,6);
        if (cVar4 == '\0') {
          *(undefined8 *)(lVar19 + 0xb0) = 99;
          return;
        }
        if (*(int *)(lVar19 + 0xb0) == 6) {
          iVar9 = *(int *)(lVar19 + 0xb4);
          if (iVar9 != 0) goto LAB_1801733ae;
          uVar8 = 10;
        }
        else {
          uVar8 = 0x14;
        }
        *(undefined4 *)(lVar19 + 0xb4) = uVar8;
        *(undefined4 *)(lVar19 + 0xb0) = 6;
        local_res18 = 5;
        iVar17 = 1;
      }
      else {
        if (*(int *)(lVar19 + 0xb0) == 5) {
          iVar9 = *(int *)(lVar19 + 0xb4);
          if (iVar9 != 0) {
LAB_1801733ae:
            *(int *)(lVar19 + 0xb4) = iVar9 + -1;
            return;
          }
          uVar8 = 10;
        }
        else {
          uVar8 = 0x14;
        }
        *(undefined4 *)(lVar19 + 0xb4) = uVar8;
        local_res18 = 4;
        *(undefined4 *)(lVar19 + 0xb0) = 5;
        iVar17 = -1;
      }
    }
    else {
      if (*(int *)(lVar19 + 0xb0) == 4) {
        iVar9 = *(int *)(lVar19 + 0xb4);
        if (iVar9 != 0) goto LAB_1801733ae;
        uVar8 = 10;
      }
      else {
        uVar8 = 0x14;
      }
      *(undefined4 *)(lVar19 + 0xb4) = uVar8;
      *(undefined4 *)(lVar19 + 0xb0) = 4;
      local_res18 = 3;
      iVar23 = 1;
    }
  }
  else {
    if (*(int *)(lVar19 + 0xb0) == 3) {
      iVar9 = *(int *)(lVar19 + 0xb4);
      if (iVar9 != 0) goto LAB_1801733ae;
      uVar8 = 10;
    }
    else {
      uVar8 = 0x14;
    }
    *(undefined4 *)(lVar19 + 0xb4) = uVar8;
    *(undefined4 *)(lVar19 + 0xb0) = 3;
    local_res18 = 2;
    iVar23 = -1;
  }
  iVar21 = iVar21 + iVar23;
  if (*(char *)(param_1 + 0x100) != '\0') {
    if (*(char *)(param_1 + 0x101) == '\0') {
      if ((-1 < iVar21) && (iVar22 = iVar21, 1 < iVar21)) {
        iVar22 = 0;
      }
      uVar15 = iVar16 + iVar17;
      bVar2 = iVar22 != 1;
      if ((iVar22 == 1) || (cVar4 = FUN_180007450(), cVar4 != '\0')) {
        uVar14 = 10;
      }
      uVar18 = (uint)bVar2;
      if (iVar23 == 0) {
        if (((int)uVar18 <= (int)uVar15) &&
           (bVar2 = (int)uVar14 < (int)uVar15, uVar14 = uVar15, bVar2)) {
          uVar14 = uVar18;
        }
      }
      else {
        if ((int)uVar15 < (int)uVar18) {
          uVar15 = (uint)bVar2;
        }
        if ((int)uVar15 < (int)uVar14) {
          uVar14 = uVar15;
        }
      }
    }
    else {
      if ((-1 < iVar21) && (iVar22 = iVar21, 1 < iVar21)) {
        iVar22 = 0;
      }
      uVar14 = iVar16 + iVar17;
      if ((int)uVar14 < 0) {
        uVar14 = 10;
      }
      else if (10 < (int)uVar14) {
        uVar14 = 0;
      }
    }
    puVar11 = (undefined8 *)FUN_180173a50(param_1,uVar14,iVar22);
    if (puVar11 != (undefined8 *)0x0) {
LAB_1801734b9:
      *(undefined4 *)(pcVar24 + 0x28) = local_res18;
      *(undefined8 **)(pcVar24 + 0x18) = puVar11;
    }
    return;
  }
  iVar22 = *(int *)(param_1 + 100);
  iVar9 = *(int *)(param_1 + 0x6c);
  if (iVar21 < iVar22) {
    iVar21 = iVar9;
  }
  iVar20 = iVar22;
  iVar3 = local_res10;
  iVar12 = -1;
  if (iVar21 <= iVar9) {
    iVar20 = iVar21;
  }
  do {
    local_res10 = iVar3;
    iVar21 = iVar16 + iVar17;
    if (iVar16 + iVar17 < *(int *)(param_1 + 0x60)) {
      iVar21 = *(int *)(param_1 + 0x68);
    }
    iVar16 = iVar21;
    if (*(int *)(param_1 + 0x68) < iVar21) {
      iVar16 = *(int *)(param_1 + 0x60);
    }
    iVar21 = iVar12;
    if (*(undefined8 **)(param_1 + 0x58) != (undefined8 *)0x0) {
      uVar13 = 0;
      puVar11 = *(undefined8 **)(param_1 + 0x58);
      iVar21 = local_res10;
      if (*(ulonglong *)(param_1 + 0x70) != 0) {
        do {
          piVar1 = (int *)*puVar11;
          if (piVar1 == (int *)0x0) break;
          if (((*(char *)((longlong)puVar11 + 0x14) == '\0') && (*piVar1 == iVar16)) &&
             (piVar1[1] == iVar20)) {
            if (puVar11 != (undefined8 *)0x0) goto LAB_1801734b9;
            break;
          }
          uVar13 = uVar13 + 1;
          puVar11 = puVar11 + 3;
        } while (uVar13 < *(ulonglong *)(param_1 + 0x70));
      }
    }
    if (iVar17 == 0) {
      iVar17 = 1;
    }
    if (iVar23 == 0) {
      iVar23 = 1;
    }
    iVar3 = iVar16;
    iVar12 = iVar16;
    if ((-1 < iVar21) && (iVar3 = local_res10, iVar12 = iVar21, iVar21 == iVar16)) {
      iVar17 = 0;
      iVar21 = iVar9;
      if (iVar22 <= iVar23 + iVar20) {
        iVar21 = iVar23 + iVar20;
      }
      iVar20 = iVar21;
      if (iVar9 < iVar21) {
        iVar20 = iVar22;
      }
    }
  } while( true );
}
