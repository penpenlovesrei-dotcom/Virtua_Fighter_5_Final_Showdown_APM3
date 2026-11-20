// =============================================================================
// LES TEMOINS DE DESSIN, et les poseurs d etat qu ils partagent avec FOG_RING.
//
// Lus le 20 novembre 2026 pour repondre a UNE question : l etat de melange de
// FUN_180072BA0 (FOG_RING, dans fogring_dessin_fs.c) differe-t-il de celui des
// effets qui, eux, dessinent ? Reponse : NON. Voir analysis/brume_decor_aoi.md
// section 33.
//
// FUN_18007E420 est le VRAI dessin de SnowRing ; effets_snowring_fs.c ne porte
// que son init et ses voisines, pas lui.
// FUN_1800819B0 est le JUMEAU GEOMETRIQUE de FOG_RING : meme pas 0x20, memes
// decalages +0 / +0x0C / +0x1C, meme format 0x161, meme mode de tirage 2.
// ATTENTION : il n est PAS etabli que FUN_1800819B0 dessine a l ecran.
// =============================================================================


// =====================================================
// 18007E420  ->  FUN_18007e420   SnowRing, le dessin
// =====================================================

void FUN_18007e420(undefined4 *param_1)

{
  FUN_18024e5a0(1,0,0,0);
  FUN_180175870("SN_FOOT");
  FUN_180252390();
  FUN_18024a6a0(2);
  FUN_180247100(300);
  FUN_1802473b0(0x12d);
  FUN_18024e900(0x318);
  FUN_18024e900(0xac);
  FUN_18024e300(0x3d2);
  FUN_18024e330(1);
  FUN_180256d50(0x21d);
  FUN_180256da0(*(undefined4 *)(*(longlong *)(param_1 + 8) + 0x14),
                *(undefined4 *)(*(longlong *)(param_1 + 8) + 0x10));
  FUN_1802573a0(0x318,0x319,1);
  FUN_180247600(3,0x161,0,*(undefined8 *)(param_1 + 2));
  FUN_1802470a0(4,0x15c,0,*(undefined8 *)(param_1 + 4));
  FUN_18024f2d0(param_1[6]);
  FUN_1802573a0(0x318,0x319,1);
  FUN_18024e900(0x2cd);
  FUN_18024f2a0(0x311);
  FUN_180247430(0xe);
  FUN_1802475b0(0xe,1,0x161,0,4,*(undefined8 *)(param_1 + 10));
  FUN_180247230(2,0,*param_1);
  FUN_18024e8d0(0xac);
  FUN_1802573a0(0x318,0x319,0);
  FUN_18024f2d0(0x3f800000);
  FUN_180256da0(*(undefined4 *)(*(longlong *)(param_1 + 8) + 0x14),0);
  FUN_18024e300(0x3ce);
  FUN_18024e330(1);
  FUN_18024e8d0(0x2cd);
  FUN_1802573a0(0x318,0x319,0);
  FUN_18024e8d0(0x318);
  FUN_18024a650();
  FUN_180252530();
  FUN_18024e5a0(1,1,1);
  FUN_180176960();
  return;
}


// =====================================================
// 18007B4A0  ->  FUN_18007b4a0   Ripple, le dessin
// =====================================================

void FUN_18007b4a0(undefined4 *param_1)

{
  undefined4 uVar1;

  FUN_18024e5a0(0,0,0,1);
  FUN_18024f270(0x28e,&DAT_180350ee0);
  FUN_18024f2a0(0x311);
  uVar1 = 0;
  FUN_18024f240(0x28c,0);
  FUN_18024f240(0x28d,0x3f800000);
  FUN_18024f2d0(0x3f800000);
  FUN_18024e8d0(0x2cd);
  FUN_18024e900(0x318);
  _DAT_1807154dc = *param_1;
  DAT_180715468._4_4_ = param_1[1];
  FUN_180175870("RIPEMIT");
  FUN_180252a80(0x48b,0,0x3b800000,0x3b800000,uVar1,uVar1);
  FUN_180252390();
  FUN_18024a6a0(2);
  FUN_180247100(300);
  FUN_1802473b0(0x12d);
  FUN_180247600(3,0x161,0,*(undefined8 *)(param_1 + 4));
  FUN_1802470a0(4,0x15c,0,*(undefined8 *)(param_1 + 6));
  if (*(char *)(DAT_1806f2160 + 0x28) == '\0') {
    FUN_18024f2d0(param_1[8]);
  }
  else {
    FUN_18024e900(0x2cd);
  }
  FUN_180247230(2,0,param_1[2]);
  if (*(char *)(DAT_1806f2160 + 0x28) == '\0') {
    FUN_18024f2d0(0x3f800000);
  }
  else {
    FUN_18024e8d0(0x2cd);
  }
  FUN_18024a650();
  FUN_180252530();
  FUN_18024e5a0(1,1,1);
  FUN_180176960();
  return;
}


// =====================================================
// 1800819B0  ->  FUN_1800819b0   le JUMEAU GEOMETRIQUE
// =====================================================

void FUN_1800819b0(longlong param_1)

{
  longlong lVar1;

  lVar1 = FUN_1801957a0(*(undefined4 *)(param_1 + 0x3c));
  FUN_180248bc0(0xffffffff);
  FUN_18024a6a0(0xffffffff);
  FUN_180247100(300);
  FUN_18024f2d0(*(undefined4 *)(param_1 + 0x18));
  FUN_18024f240(0x28c,DAT_180643538);
  FUN_18024f240(0x28d,DAT_18064353c);
  FUN_18024f270(0x28e,&DAT_180643540);
  FUN_18024f2a0(0x311);
  if (lVar1 != 0) {
    FUN_180256d50(0x21d);
    FUN_180256da0(*(undefined4 *)(lVar1 + 0x14),*(undefined4 *)(lVar1 + 0x10));
  }
  FUN_18024e900(0x318);
  FUN_1802573a0(0x318,0x319,1);
  FUN_18024e900(0x2cd);
  FUN_180175970(0x1b);
  if (0 < *(int *)(param_1 + 0x38)) {
    FUN_180247600(3,0x161,0x20,*(undefined8 *)(param_1 + 0x20));
    FUN_180247430(3);
    FUN_1802475b0(3,4,0x161,0,0x20,*(longlong *)(param_1 + 0x20) + 0xc);
    FUN_180247430(8);
    FUN_1802475b0(8,1,0x161,0,0x20,*(longlong *)(param_1 + 0x20) + 0x1c);
    FUN_180252390();
    FUN_180247230(2,0,*(undefined4 *)(param_1 + 0x38));
    FUN_180252530();
  }
  FUN_180176960();
  FUN_18024a650();
  FUN_180248ba0();
  return;
}


// =============================================================================
// LES POSEURS D ETAT PARTAGES -- ce que chaque appel veut dire
// =============================================================================
//
// FUN_180247600(canal,fmt,pas,ptr)  -> FUN_180246b30(flux,...,0)  canal 0 = POSITION
// FUN_1802470a0(canal,fmt,pas,ptr)  -> FUN_180246b30(flux,...,3)  canal 3
//   Les deux ne different QUE par ce dernier argument. C est ce qui etablit
//   que le premier attribut de FOG_RING est la position, sur 12 octets, dans
//   un sommet de 0x20.
//
// FUN_18024A6A0(masque) : EMPILE l etat (pile de 16). Avec le bit 2, recopie
//                         l etat courant. FUN_18024A650() DEPILE.
// FUN_18024E900(cle)    -> FUN_18024DD20(etats,cle,1) : ALLUME l etat <cle>.
//   LE SENS DES CLES, lu dans FUN_18024DD20 le 20 novembre 2026 :
//     0xAC  = LE MELANGE. Allume -> ecrit 0xE dans les bits BAS de l
//             octet [objet+0x50], et recopie SIX facteurs depuis
//             [etats+0x5C..0x61] vers [objet+0x51..0x56].
//             Eteint -> l octet &= 0xF0.
//     0x318 = ecrit [etats+0x9E4], leve 0x2002.
//     0x8D  = ecrit [etats+0x70], touche la profondeur
//             [objet+0x58..0x60].
//     0x7A  = ecrit [etats+0xA0C], touche [objet+0x40..0x4C].
//   ET FUN_18024E5A0 ecrit les bits HAUTS (0x10/0x20/0x40/0x80) du
//   MEME octet [objet+0x50]. UN SEUL OCTET porte le melange ET le
//   masque d ecriture de couleur.
//   La chaine : contexte = [0x180C414F8] (FUN_180253C90 rend ce
//               global), objet = [contexte+0], octet a objet+0x50.
// FUN_18024E8D0(cle)    : l ETEINT.  FUN_18024C4B0(etats,cle) : le LIT.
// FUN_18024F240(cle,v)  -> FUN_18024DA80(etats,cle,&v) : pose une VALEUR.
// FUN_18024F2D0(v)      : ecrit UN scalaire global (contexte+0xD9598).
//                         Ripple et SnowRing le RESTAURENT a 0x3F800000 = 1.0.
//                         FOG_RING lui donne [S+0x30] = 18.0 -- taille de point
//                         plausible, et c est la valeur D ORIGINE de SEGA,
//                         identique dans les QUATRE dossiers, DU2 compris.
// FUN_18024E5A0(a,b,c,d): masque d ecriture de couleur (contexte+0xD8BEC..EF,
//                         et les bits 0x10/0x20/0x40/0x80 de l objet courant).
//                         FOG_RING NE L APPELLE JAMAIS : il HERITE.
//                         Ripple et SnowRing le restaurent a (1,1,1) -- TROIS
//                         arguments sur quatre.
//
// FUN_180175970(indice) : choisit le programme par INDICE dans la table
//                         DAT_180714B00, pas 0x30, en .bss. 22 appelants.
// FUN_180175870(nom)    : le choisit par NOM, avec repli 0x31 et une
//                         indirection par le champ +0x08. 2 appelants.
//                         -> l INDICE est la norme ; FOG_RING n a rien
//                            d anormal a passer 0x2A.
