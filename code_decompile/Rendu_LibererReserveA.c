/* Rendu_LibererReserveA  --  VF5FS+0x1630c0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801630c0.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void Rendu_LibererReserveA(void)

{
  longlong lVar1;
  longlong *plVar2;
  undefined8 *puVar3;
  longlong lVar4;
  
  FUN_180162ec0();
  plVar2 = DAT_180713fd8;
  lVar1 = DAT_180713fd8[1];
  lVar4 = *DAT_180713fd8;
  if (lVar4 != lVar1) {
    do {
      FUN_1801625b0(lVar4);
      lVar4 = lVar4 + 0x18;
    } while (lVar4 != lVar1);
    lVar4 = *plVar2;
  }
  puVar3 = DAT_180713fe0;
  plVar2[1] = lVar4;
  *puVar3 = 0;
  puVar3[1] = 0;
  puVar3[2] = 0;
  puVar3[3] = 0;
  puVar3[4] = 0;
  puVar3[5] = 0;
  puVar3[6] = 0;
  puVar3[7] = 0;
  *(undefined4 *)(puVar3 + 8) = 0;
  puVar3[10] = puVar3[9];
  *(undefined1 *)(puVar3 + 0xc) = 0;
  *(undefined4 *)((longlong)puVar3 + 100) = 0;
  puVar3[0xd] = 0;
  *(undefined4 *)(puVar3 + 0xe) = 0;
  return;
}
