/* FUN_1801d5920  --  VF5FS+0x1d5920
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801d5920.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1801d5920(undefined8 *param_1)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  longlong lVar4;
  
  lVar4 = DAT_180796db0;
  uVar1 = param_1[1];
  uVar2 = param_1[2];
  uVar3 = param_1[3];
  *(undefined8 *)(DAT_180796db0 + 0x95d4) = *param_1;
  *(undefined8 *)(lVar4 + 0x95dc) = uVar1;
  *(undefined8 *)(lVar4 + 0x95e4) = uVar2;
  *(undefined8 *)(lVar4 + 0x95ec) = uVar3;
  uVar1 = param_1[5];
  uVar2 = param_1[6];
  uVar3 = param_1[7];
  *(undefined8 *)(lVar4 + 0x95f4) = param_1[4];
  *(undefined8 *)(lVar4 + 0x95fc) = uVar1;
  *(undefined8 *)(lVar4 + 0x9604) = uVar2;
  *(undefined8 *)(lVar4 + 0x960c) = uVar3;
  uVar1 = param_1[9];
  uVar2 = param_1[10];
  uVar3 = param_1[0xb];
  *(undefined8 *)(lVar4 + 0x9614) = param_1[8];
  *(undefined8 *)(lVar4 + 0x961c) = uVar1;
  *(undefined8 *)(lVar4 + 0x9624) = uVar2;
  *(undefined8 *)(lVar4 + 0x962c) = uVar3;
  uVar1 = param_1[0xd];
  uVar2 = param_1[0xe];
  uVar3 = param_1[0xf];
  *(undefined8 *)(lVar4 + 0x9634) = param_1[0xc];
  *(undefined8 *)(lVar4 + 0x963c) = uVar1;
  *(undefined8 *)(lVar4 + 0x9644) = uVar2;
  *(undefined8 *)(lVar4 + 0x964c) = uVar3;
  *(undefined8 *)(lVar4 + 0x9654) = param_1[0x10];
  return;
}
