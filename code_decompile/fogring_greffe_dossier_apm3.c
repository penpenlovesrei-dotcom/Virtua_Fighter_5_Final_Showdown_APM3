// ===================================================
// 180EA6C50  ->  FUN_180ea6c50  (entree 180ea6c50)
// ===================================================
//
// CE CODE EST A NOUS. Ce n est pas du FS d origine : c est la greffe posee
// dans la zone ajoutee de la DLL, qui remplace le dossier FOG_RING statique
// par un dossier choisi selon l indice du decor.
//
// La table est a DAT_180ea6cc0, pas de 0x3C octets (= piVar1 + 0xf sur des
// int). TROIS cles sont testees -- les entrees 0, 1 et 2 -- et quand iVar2
// tombe a zero la boucle sort avec piVar1 sur l entree 3, qui sert donc de
// REPLI. Les cles sont 48 (jn5), 68 (snb), 83 (d25) ; l entree de repli porte
// 22 et est octet pour octet le dossier FS d origine de 0x1806431C8.
//
// La copie fait 0x38 octets plus l entier de +0x38, soit les 0x3C du pas.
// Puis appel terminal a FUN_180072130 -- l init de la tache FOG_RING.
// ===================================================

void FUN_180ea6c50(undefined8 param_1,int param_2)

{
  int *piVar1;
  int iVar2;

  iVar2 = 3;
  for (piVar1 = &DAT_180ea6cc0; (iVar2 != 0 && (param_2 != *piVar1)); piVar1 = piVar1 + 0xf) {
    iVar2 = iVar2 + -1;
  }
  DAT_1806431c8 = *(undefined8 *)piVar1;
  DAT_1806431d0 = *(undefined8 *)(piVar1 + 2);
  DAT_1806431d8 = *(undefined8 *)(piVar1 + 4);
  DAT_1806431e0 = *(undefined8 *)(piVar1 + 6);
  DAT_1806431e8 = *(undefined8 *)(piVar1 + 8);
  DAT_1806431f0 = *(undefined8 *)(piVar1 + 10);
  DAT_1806431f8 = *(undefined8 *)(piVar1 + 0xc);
  DAT_180643200 = piVar1[0xe];
  FUN_180072130();
  return;
}
