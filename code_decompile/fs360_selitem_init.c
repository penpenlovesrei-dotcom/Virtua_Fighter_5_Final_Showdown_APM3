// ===================================================
// 82235068  ->  FUN_82235068  (entree 82235068)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82235068(int param_1)

{
  byte bVar1;
  undefined8 uVar2;
  int iVar3;
  undefined4 local_100;
  undefined *local_fc;
  undefined4 local_f8;
  undefined4 local_f4;
  undefined4 local_e8;
  undefined4 local_e4;
  undefined4 local_dc;
  undefined4 local_a0;
  
  FUN_82217e18(param_1,0);
  FUN_82217f40(param_1);
  iVar3 = param_1 + 0x1c4;
  *(undefined1 *)(param_1 + 0x738) = 0;
  *(undefined4 *)(param_1 + 0x4c) = 0;
  *(undefined4 *)(param_1 + 0x750) = 0;
  *(undefined4 *)(param_1 + 0x74c) = 0;
  *(undefined4 *)(param_1 + 0x704) = 0;
  FUN_822184e8(iVar3);
  FUN_82217950(iVar3,8);
  FUN_82218c30(iVar3,0x3f);
  iVar3 = param_1 + 0x708;
  FUN_82218060(iVar3);
  FUN_82217968(iVar3,0xffffffffffffffff,*(int *)(param_1 + 0x74c) != 0);
  FUN_82217968(iVar3,1,-((ulonglong)*(uint *)(param_1 + 0x74c) + 0x28 <
                        (ulonglong)
                        (longlong)(*(int *)(param_1 + 0x740) - *(int *)(param_1 + 0x73c) >> 1)) & 1)
  ;
  bVar1 = (&DAT_82010c68)[*(ushort *)(param_1 + 0x73a)];
  FUN_821c6270(&local_100);
  local_f8 = 0;
  local_f4 = 0;
  local_100 = 0x2a7;
  local_dc = 10;
  local_e8 = 0x10000;
  local_a0 = DAT_82000830;
  local_e4 = 2;
  local_fc = (&PTR_s_itemsel_title_head_8272330c)[bVar1];
  uVar2 = FUN_821c6940(&local_100);
  *(int *)(param_1 + 0x734) = (int)uVar2;
  FUN_821c5e40(uVar2,1);
  FUN_821c61a8(&local_100);
  return 1;
}



