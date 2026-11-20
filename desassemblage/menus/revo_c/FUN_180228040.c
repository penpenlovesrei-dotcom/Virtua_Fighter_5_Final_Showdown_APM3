/* FUN_180228040  --  VF5FS+0x228040
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180228040.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_180228040(longlong param_1,char param_2)

{
  longlong *plVar1;
  longlong lVar2;
  undefined1 auVar3 [15];
  undefined1 auVar4 [16];
  char cVar5;
  undefined8 uVar6;
  undefined1 *local_38;
  undefined4 local_30;
  undefined1 local_28 [12];
  undefined1 uStack_1c;
  undefined1 uStack_1b;
  undefined2 uStack_1a;
  undefined8 local_18;
  ulonglong local_10;
  
  local_18 = 0;
  local_10 = 0xf;
  stack0xffffffffffffffd9 = SUB1615((undefined1  [16])0x0,1);
  auVar3 = stack0xffffffffffffffd9;
  auVar4[0xf] = 0;
  auVar4._0_15_ = stack0xffffffffffffffd9;
  _local_28 = auVar4 << 8;
  auVar4 = _local_28;
  if (param_2 == '\0') {
    if (*(longlong **)(param_1 + 0x80) != (longlong *)0x0) {
      cVar5 = (**(code **)(**(longlong **)(param_1 + 0x80) + 0x40))();
      auVar4 = _local_28;
      if (cVar5 == '\0') {
        uVar6 = FUN_180228680(*(undefined8 *)(param_1 + 0x70));
        FUN_180228760(*(undefined8 *)(param_1 + 0x70));
        FUN_1802cd400(*(undefined8 *)(param_1 + 0x80),"REPLAY_ONLINE");
        (**(code **)(**(longlong **)(param_1 + 0x80) + 0x50))(*(longlong **)(param_1 + 0x80),uVar6);
        *(undefined4 *)(param_1 + 0x90) = 3;
        auVar4 = _local_28;
      }
    }
  }
  else {
    _uStack_1c = auVar3._11_4_;
    if (param_2 == '\x01') {
      *(undefined8 *)(param_1 + 0x68) = *(undefined8 *)(param_1 + 0x58);
      uVar6 = 0x616c7065725f796d;
    }
    else {
      if (param_2 != '\x02') goto LAB_1802281d2;
      *(undefined8 *)(param_1 + 0x68) = *(undefined8 *)(param_1 + 0x60);
      uVar6 = 0x616c7065725f6c64;
    }
    local_28 = ZEXT412(0x61642e79) << 0x40;
    auVar4 = _local_28;
    uStack_1a = auVar3._13_2_;
    _local_28 = auVar4._0_13_;
    uStack_1b = 0;
    uStack_1c = 0x74;
    local_28._0_8_ = uVar6;
    local_18 = 0xd;
    if (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0) {
      if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
        (**(code **)(DAT_180c8df28 + 0x1ff08))(*(undefined8 *)(DAT_180c8df28 + 0x1ff10),0x84,0);
      }
      *(undefined4 *)(param_1 + 0x8c) = 0x3c;
    }
    local_30 = FUN_180228760(*(undefined8 *)(param_1 + 0x68));
    local_38 = local_28;
    if (0xf < local_10) {
      local_38 = (undefined1 *)local_28._0_8_;
    }
    plVar1 = *(longlong **)(param_1 + 0x78);
    lVar2 = *plVar1;
    FUN_180228680(*(undefined8 *)(param_1 + 0x68));
    (**(code **)(lVar2 + 0x20))(plVar1,&local_38);
    *(undefined4 *)(param_1 + 0x88) = 3;
    auVar4 = _local_28;
  }
LAB_1802281d2:
  _local_28 = auVar4;
  if (0xf < local_10) {
    if (0xfff < local_10 + 1) {
      if (0x1f < (local_28._0_8_ - *(longlong *)(local_28._0_8_ + -8)) - 8U) {
                    /* WARNING: Subroutine does not return */
        _invoke_watson((wchar_t *)0x0,(wchar_t *)0x0,(wchar_t *)0x0,0,0);
      }
    }
    FUN_18001d8a0();
  }
  return;
}
