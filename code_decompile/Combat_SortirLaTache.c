/* Combat_SortirLaTache  --  VF5FS+0xbbcf0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800bbcf0.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined8 Combat_SortirLaTache(longlong param_1)

{
  undefined4 *puVar1;
  longlong lVar2;
  
  FUN_180087260(0x45);
  FUN_1800cb490();
  FUN_1800cb110(0);
  FUN_1800cb110(1);
  _guard_check_icall();
  _guard_check_icall();
  FUN_1800b5930();
  FUN_1801ba8c0();
  _guard_check_icall();
  FUN_180054c90();
  FUN_18009efe0();
  _guard_check_icall();
  FUN_180186d40(0);
  FUN_180186d40(1);
  FUN_180186d40(2);
  FUN_180185f40(0,0,0x3c);
  _guard_check_icall();
  _guard_check_icall();
  FUN_18016b420(0xff000000);
  FUN_180150720(*(undefined8 *)(param_1 + 0x6e8));
  FUN_18018ef20();
  Rendu_LibererReserveA();
  FUN_1802450a0(param_1 + 0x58);
  FUN_1802450a0(param_1 + 0x110);
  FUN_1802450a0(param_1 + 400);
  FUN_1802450a0(param_1 + 0x1f0);
  FUN_1802450a0(param_1 + 0x4c8);
  FUN_1802450a0(param_1 + 0x548);
  FUN_1802450a0(param_1 + 0x5c8);
  FUN_1802450a0(param_1 + 0x3c8);
  FUN_1802450a0(param_1 + 0x448);
  FUN_1802450a0(param_1 + 0x648);
  FUN_1802450a0(param_1 + 0x298);
  FUN_1802450a0(param_1 + 0x300);
  puVar1 = (undefined4 *)(param_1 + 0x6fc);
  lVar2 = 5;
  do {
    FUN_180029be0(*puVar1);
    *puVar1 = 0;
    puVar1 = puVar1 + 1;
    lVar2 = lVar2 + -1;
  } while (lVar2 != 0);
  lVar2 = 6;
  puVar1 = (undefined4 *)(param_1 + 0x25c);
  do {
    FUN_180029be0(*puVar1);
    *puVar1 = 0;
    puVar1 = puVar1 + 1;
    lVar2 = lVar2 + -1;
  } while (lVar2 != 0);
  FUN_180029be0(*(undefined4 *)(param_1 + 0x274));
  *(undefined4 *)(param_1 + 0x274) = 0;
  _guard_check_icall();
  _guard_check_icall();
  _guard_check_icall();
  _guard_check_icall();
  _guard_check_icall();
  _guard_check_icall();
  _guard_check_icall();
  _guard_check_icall();
  FUN_1802450a0(DAT_1806f9c50 + 0x368);
  if (((module_execute_info_courant != 0) &&
      (*(longlong *)(module_execute_info_courant + 0x1fe10) != 0)) &&
     (*(code **)(module_execute_info_courant + 0x1fe10) != (code *)0x0)) {
    (**(code **)(module_execute_info_courant + 0x1fe10))
              (*(undefined8 *)(module_execute_info_courant + 0x1fe18),0x5b,0);
  }
  lVar2 = *(longlong *)(*(longlong *)(param_1 + 0x6c8) + 0x1090);
  if (lVar2 != 0) {
    if (((*(longlong *)(param_1 + 0x6c8) != 0) && (lVar2 != 0)) &&
       (*(char *)(lVar2 + 0xf1d) != '\0')) {
      FUN_180167eb0(lVar2);
    }
    FUN_1801670f0(lVar2);
  }
  FUN_180051a10();
  FUN_18006f8a0(2,0,0);
  FUN_18006f8a0(1,3,1);
  if ((module_execute_info_courant == 0) ||
     (*(longlong *)(module_execute_info_courant + 0x1fe10) == 0)) {
    FUN_1800c26e0();
  }
  FUN_1800c56c0();
  _guard_check_icall();
  lVar2 = FUN_180178a60();
  *(undefined1 *)(lVar2 + 0x334) = 1;
  FUN_1800b7580();
  FUN_1800b75b0();
  FUN_1800b7650();
  thunk_FUN_180115b60();
  *(undefined4 *)(param_1 + 0x720) = 0;
  *(undefined8 *)(param_1 + 0x6e8) = 0;
  *(undefined4 *)(param_1 + 0x6dc) = 0x1a;
  return 1;
}
