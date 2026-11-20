/* FUN_180205440  --  VF5FS+0x205440
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180205440.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined8 * FUN_180205440(undefined8 *param_1)

{
  FUN_1801de060();
  *param_1 = TaskMenuArcade::vftable;
  param_1[0x4a] = 0;
  param_1[0x4b] = 0;
  *(undefined4 *)(param_1 + 0x4c) = 0;
  param_1[0x4d] = 0;
  *(undefined8 *)((longlong)param_1 + 0x274) = 0;
  param_1[0x54] = 0;
  param_1[0x55] = 0;
  *(undefined4 *)(param_1 + 0x56) = 0;
  param_1[0x57] = 0;
  *(undefined8 *)((longlong)param_1 + 0x2c4) = 0;
  FUN_1801de060(param_1 + 0x5c);
  param_1[0x5c] = TaskMenuArcadeNormal::vftable;
  param_1[0xa9] = 0;
  param_1[0xaa] = 0;
  *(undefined4 *)(param_1 + 0xab) = 0;
  param_1[0xac] = 0;
  *(undefined8 *)((longlong)param_1 + 0x56c) = 0;
  param_1[0xb3] = 0;
  param_1[0xb4] = 0;
  *(undefined4 *)(param_1 + 0xb5) = 0;
  param_1[0xb6] = 0;
  *(undefined8 *)((longlong)param_1 + 0x5bc) = 0;
  FUN_1800e4d00(param_1 + 0xba);
  *(undefined8 *)((longlong)param_1 + 0x754) = 0;
  *(undefined8 *)((longlong)param_1 + 0x75c) = 0;
  FUN_1801dfb10(param_1 + 0xe7);
  *(undefined8 *)((longlong)param_1 + 0x764) = 0;
  FUN_1801dfb90(param_1 + 0xe7);
  param_1[0xee] = 0;
  FUN_1801de060(param_1 + 0xef);
  param_1[0xef] = TaskMenuScoreAttack::vftable;
  param_1[0x139] = 0;
  param_1[0x13a] = 0;
  *(undefined4 *)(param_1 + 0x13b) = 0;
  param_1[0x13c] = 0;
  *(undefined8 *)((longlong)param_1 + 0x9ec) = 0;
  param_1[0x140] = 0;
  FUN_1801de060(param_1 + 0x141);
  param_1[0x141] = TaskMenuArcadeLicenceChallenge::vftable;
  param_1[0x18b] = 0;
  param_1[0x18c] = 0;
  *(undefined4 *)(param_1 + 0x18d) = 0;
  param_1[0x18e] = 0;
  *(undefined8 *)((longlong)param_1 + 0xc7c) = 0;
  FUN_1801de060(param_1 + 0x192);
  param_1[0x192] = CTaskAllClearInfoWindow::vftable;
  param_1[0x1dc] = 0;
  param_1[0x1dd] = 0;
  *(undefined4 *)(param_1 + 0x1de) = 0;
  param_1[0x1df] = 0;
  *(undefined8 *)((longlong)param_1 + 0xf04) = 0;
  FUN_1801de060(param_1 + 0x1e3);
  param_1[0x1e3] = CTaskDifficultyChangeWindow::vftable;
  param_1[0x22d] = 0;
  param_1[0x22e] = 0;
  *(undefined4 *)(param_1 + 0x22f) = 0;
  param_1[0x230] = 0;
  *(undefined8 *)((longlong)param_1 + 0x118c) = 0;
  param_1[0x237] = 0;
  param_1[0x238] = 0;
  *(undefined4 *)(param_1 + 0x239) = 0;
  param_1[0x23a] = 0;
  *(undefined8 *)((longlong)param_1 + 0x11dc) = 0;
  *(undefined8 *)((longlong)param_1 + 0x1244) = 0;
  *(undefined8 *)((longlong)param_1 + 0x124c) = 0;
  FUN_1801dfb10();
  FUN_1801aa1f0(param_1 + 0x24b);
  return param_1;
}
