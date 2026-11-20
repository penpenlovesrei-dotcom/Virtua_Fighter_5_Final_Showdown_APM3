/* SE20_MODE_SELECTOR_Phase1_MontageDuMatch  --  VF5FS+0xe2010
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800e2010.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* LE MONTAGE DU MATCH -- ET CE N'EST PAS LE POINTEUR QUI MANQUE, C'EST LE BLOB
   (SS 419.176 ; CORRIGE LE 419.175, QUI SE TROMPAIT DE MECANISME)
   
   Phase 1 du sous-etat 20=MODE_SELECTOR. Mesure du 419.174 : ce sous-etat ne
   dure que 2 IMAGES. Voici pourquoi, et ce que la lecture du 419.176 corrige.
   
   ERRATUM DU 419.175. J'avais ecrit : « [vue+0x1238] est nul, donc
   Partie_MonterLeMatch n'est JAMAIS appele ». C'EST FAUX. Versus_ConstruireEtat
   (0xAFAB0) alloue ce pointeur a la construction :
       lVar5 = FUN_180279BD0(0x10b0);
       if (lVar5 != 0) uVar3 = Match_ConstruireLaDemande(lVar5, 2, 10);
       param_1[0x247] = uVar3;              // 0x247*8 = 0x1238
   et Versus_DetruireEtat (0xAFE50) le libere. Le champ est donc NON NUL en
   service normal, le batisseur EST appele a chaque image, et il echoue plus loin.
   
   OU IL ECHOUE VRAIMENT. Partie_MonterLeMatch appelle d'abord
   Match_DeballerSiBlob -> Match_DeballerLeBlob (0x176970), dont la sortie seche
   est :
       if (param_2 == 0 || (int)param_3 < 1 || !Match_DecoderLeBlob(sub+0xD0,...))
           return 0;
   Or param_2 et param_3 viennent d'ici meme :
       Match_PointeurDuBlob(match)  = [sub+0xB8] ? [sub+0xC0] : 0
       Match_LongueurDuBlob(match)  = [sub+0xB8] ? [sub+0xC8] : 0
   et Match_ConstruireLaDemande met les trois a zero :
       *(undefined8 *)(puVar1 + 0x30) = 0;   // +0xC0 pointeur du blob
       *(undefined8 *)(puVar1 + 0x32) = 0;   // +0xC8 longueur
       *(undefined1 *)(puVar1 + 0x2e) = 0;   // +0xB8 DRAPEAU
   
   LA DEMANDE DE MATCH EST DONC SERIALISEE, et le batisseur la DESERIALISE. Sans
   blob livre, Match_PointeurDuBlob rend 0, Match_DeballerLeBlob sort sur
   param_2 == 0, et Partie_MonterLeMatch rend faux. LA SONDE QUI TRANCHE N'EST
   PLUS LE POINTEUR MAIS UN SEUL OCTET : [[objEntree+0x19C0] + 0xB8].
   
   LE CHEMIN A UN JOUEUR NE MONTE RIEN, ET C'EST LITTERAL :
       iVar5 = Partie_SorteVaut3();  Partie_PoserSorteVaut3(uVar10, iVar5);
       if (iVar5 == 0) { ... FUN_180106F30 / FUN_180041DF0 sur la fiche joueur ... }
       FUN_1800B8860(uVar9);  return 1;
   Aucun match monte, AUCUNE TACHE DE COMBAT INSTALLEE. Et g_montageEtape reste a
   2 : l'etape 3 (qui ferait DemanderSousEtat(0x13), retour au selecteur) n'est
   jamais atteinte, parce que `return 1` fait commettre 21=VS par la pompe des
   l'image suivante. 2 images -- exactement la mesure du 419.174.
   Attention : Partie_PoserSorteVaut3 ecrit [uVar10+8] ou uVar10 = FUN_1800B21F0
   (objet de reglages), PAS le [sub+8] du blob. Ne pas confondre les deux.
   
   LE CHEMIN A DEUX JOUEURS, lui, INSTALLE QUELQUE CHOSE :
       if (Entree_PortEstInscrit(obj,0) && Entree_PortEstInscrit(obj,1)) {
           FUN_1800B93B0(obj, FUN_18017B840(g_tacheSelecteur), 0); return 1;
       }
   Entree_PortEstInscrit est [obj + 0x0C + port] -- l'octet meme qu'InscrireJoueur
   ecrit (419.168). En partie a un joueur le port 1 n'est pas inscrit. C'EST LA
   PISTE ACTIONNABLE : inscrire le port 1 fait prendre ce chemin.
   
   QUI DESSINE LE COMBAT. Combat_MachineAEtats (0xBB170), 28 etats sur
   [tache+0x720], appelee UNIQUEMENT par la table 0x1803C3F48 (slot +0x18) --
   aucun appel direct dans tout le module. Son case 1 lance
   Combat_ChargerLaScene (0xC2550), chargeur a 12 etapes qui a l'etape 10 charge
   la musique ("rom/sound/bgm/vf5revo_bgm_btl_final.adx") puis appelle
   Match_RemplirLesFiches. ET CE SWITCH N'A PAS DE `default` : si [tache+0x720]
   vaut 0, la machine ne fait RIEN -- ni chargement, ni dessin. Cela explique les
   19 tirages par image du 419.174 mieux que « rien a dessiner ».
   
   AUTRE ERRATUM : [match+0x1074] != 2 n'est pas une porte serieuse.
   Match_RemplirLesFiches boucle `do { ... } while (i < 2)` en dur, donc le compte
   atteint TOUJOURS 2 des qu'elle tourne. Sa vraie porte est
   Match_BlobEstDeballe(match) : [sub+8] == 1. */

undefined8 SE20_MODE_SELECTOR_Phase1_MontageDuMatch(void)

{
  undefined2 uVar1;
  char cVar2;
  undefined1 uVar3;
  undefined4 uVar4;
  int iVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  longlong lVar11;
  undefined8 uVar12;
  longlong lVar13;
  
  uVar9 = LireObjetEntree();
  uVar10 = FUN_1800b21f0(uVar9);
  lVar11 = Partie_VueDuContexte(uVar9);
  lVar13 = *(longlong *)(lVar11 + 0x1238);
  if (g_montageEtape == 0) {
LAB_1800e2088:
    cVar2 = FUN_18000ba20();
    if (cVar2 != '\0') {
      return 0;
    }
    g_montageEtape = 1;
LAB_1800e209f:
    cVar2 = FUN_18000ba20(0);
    if (cVar2 != '\0') {
      return 0;
    }
    cVar2 = FUN_18000ba20(1);
    if (cVar2 != '\0') {
      return 0;
    }
    cVar2 = FUN_18000ba20();
    if (cVar2 != '\0') {
      return 0;
    }
    cVar2 = FUN_18000ba20();
    if (cVar2 != '\0') {
      return 0;
    }
    cVar2 = FUN_18000ba20();
    if (cVar2 != '\0') {
      return 0;
    }
    cVar2 = Partie_HoteDemandeAttente();
    if (cVar2 != '\0') {
      return 0;
    }
    cVar2 = Partie_MatchEnChargement(lVar11);
    if (cVar2 != '\0') {
      return 0;
    }
    g_montageEtape = 2;
  }
  else {
    if (g_montageEtape == 1) goto LAB_1800e209f;
    if (g_montageEtape != 2) {
      if (g_montageEtape == 3) {
        cVar2 = Affichage_EstOccupe();
        if (cVar2 == '\0') {
          DemanderSousEtat(0x13);
          return 1;
        }
        return 0;
      }
      goto LAB_1800e2088;
    }
  }
  FUN_1801951d0(0);
  if (lVar13 != 0) {
    uVar4 = Match_LongueurDuBlob(lVar13);
    uVar12 = Match_PointeurDuBlob(lVar13);
    cVar2 = Partie_MonterLeMatch(uVar9,uVar12,uVar4,1,0xffffffff,0,0);
    if (cVar2 != '\0') {
      return 1;
    }
  }
  cVar2 = Entree_PortEstInscrit(uVar9,0);
  if ((cVar2 != '\0') && (cVar2 = Entree_PortEstInscrit(uVar9,1), cVar2 != '\0')) {
    uVar4 = FUN_18017b840(g_tacheSelecteur);
    FUN_1800b93b0(uVar9,uVar4,0);
    return 1;
  }
  iVar5 = Partie_SorteVaut3();
  Partie_PoserSorteVaut3(uVar10,iVar5);
  if (iVar5 == 0) {
    uVar4 = FUN_1800201c0(uVar9);
    lVar13 = FUN_180106f30(DAT_180754a90,uVar4);
    uVar6 = FUN_1800b6c50(uVar4);
    FUN_1800b32f0(uVar10,uVar6);
    FUN_180041ea0(uVar4);
    FUN_180041df0(uVar4,*(undefined1 *)(lVar13 + 0x167));
    cVar2 = *(char *)(lVar13 + 9);
  }
  else {
    if (iVar5 != 1) goto LAB_1800e22d6;
    uVar12 = FUN_180092000();
    uVar4 = FUN_1800201c0(uVar9);
    lVar13 = FUN_180106f30(DAT_180754a90,uVar4);
    uVar6 = FUN_18000ba10();
    uVar7 = FUN_1800120b0();
    uVar8 = FUN_1800120b0();
    FUN_1800925f0(uVar12);
    FUN_180092880(uVar12,lVar13,uVar6,uVar7,uVar8);
    FUN_1800b2800(uVar10,uVar7);
    FUN_1800b2740(uVar10,uVar8);
    uVar1 = *(undefined2 *)(lVar13 + 0x570);
    uVar3 = FUN_1800923b0(uVar12);
    FUN_180041db0(uVar4,uVar1,uVar8,uVar3);
    FUN_180041df0(uVar4,*(undefined1 *)(lVar13 + 0x167));
    cVar2 = *(char *)(lVar13 + 9);
  }
  if (cVar2 != '\0') {
    FUN_180041fe0(uVar4);
  }
LAB_1800e22d6:
  FUN_1800b8860(uVar9);
  return 1;
}
