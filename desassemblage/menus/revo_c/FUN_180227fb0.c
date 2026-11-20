/* FUN_180227fb0  --  VF5FS+0x227fb0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180227fb0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_180227fb0(char param_1,undefined8 param_2,undefined4 param_3)

{
  longlong lVar1;
  char cVar2;
  longlong *plVar3;
  undefined4 local_res20;
  undefined1 local_res24;
  
  lVar1 = DAT_18079b7f0;
  local_res24 = 0;
  local_res20 = param_3;
  if (param_1 == '\0') {
    plVar3 = *(longlong **)(DAT_18079b7f0 + 0x70);
  }
  else if (param_1 == '\x01') {
    plVar3 = *(longlong **)(DAT_18079b7f0 + 0x58);
  }
  else {
    if (param_1 != '\x02') {
      return;
    }
    cVar2 = FUN_180228500(*(undefined8 *)(DAT_18079b7f0 + 0x60));
    if (cVar2 != '\0') {
      return;
    }
    plVar3 = *(longlong **)(lVar1 + 0x60);
    if (*(uint *)(plVar3 + 5) <= *(uint *)((longlong)plVar3 + 0x14)) {
      return;
    }
  }
  (**(code **)(*plVar3 + 0x18))(plVar3,param_2,&local_res20,0xffffffff);
  FUN_180228040(lVar1,param_1);
  return;
}
