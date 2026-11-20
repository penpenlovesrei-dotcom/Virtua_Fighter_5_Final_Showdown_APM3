// ===================================================
// 8230DDF0  ->  FUN_8230ddf0  (entree 8230ddf0)
// ===================================================

/* WARNING: Function: __savegprlr_27 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_27 replaced with injection: x360_restgprlr */

void FUN_8230ddf0(uint param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined1 auStack_90 [4];
  uint uStack_8c;
  undefined4 uStack_7c;
  uint uStack_78;
  undefined1 auStack_70 [4];
  uint uStack_6c;
  undefined4 uStack_5c;
  uint uStack_58;
  undefined1 auStack_50 [4];
  undefined4 uStack_4c;
  uint uStack_38;
  
  if (param_2 != 0) {
    if (999 < param_1) {
      param_1 = param_1 % 1000;
    }
    puVar4 = (undefined4 *)(param_1 * 0x90 + DAT_82acb928);
    FUN_82141968(auStack_90,*puVar4);
    FUN_821ddef8(param_2,auStack_90);
    if (0xf < uStack_78) {
      thunk_FUN_82142f48(uStack_8c);
    }
    uStack_7c = 0;
    uStack_78 = 0xf;
    uStack_8c = uStack_8c & 0xffffff;
    FUN_82141968(auStack_70,puVar4[1]);
    FUN_821ddf68(param_2 + 0x1f,auStack_70);
    if (0xf < uStack_58) {
      thunk_FUN_82142f48(uStack_6c);
    }
    uStack_58 = 0xf;
    uStack_5c = 0;
    uStack_6c = uStack_6c & 0xffffff;
    FUN_82141968(auStack_50,puVar4[2]);
    FUN_821ddf68(param_2 + 0x47,auStack_50);
    if (0xf < uStack_38) {
      thunk_FUN_82142f48(uStack_4c);
    }
    puVar2 = (undefined4 *)(param_2 + 0x7c);
    *(undefined2 *)(param_2 + 0x70) = *(undefined2 *)(puVar4 + 3);
    *(undefined1 *)(param_2 + 0x72) = *(undefined1 *)((int)puVar4 + 0xe);
    *(undefined4 *)(param_2 + 0x74) = puVar4[4];
    *(undefined1 *)(param_2 + 0x78) = *(undefined1 *)(puVar4 + 5);
    *(undefined1 *)(param_2 + 0x79) = *(undefined1 *)((int)puVar4 + 0x15);
    *(undefined1 *)(param_2 + 0x7a) = *(undefined1 *)((int)puVar4 + 0x16);
    if (puVar2 != puVar4 + 6) {
      iVar3 = (int)(puVar4 + 6) - (int)puVar2;
      iVar1 = 0x18;
      do {
        iVar1 = iVar1 + -1;
        *(undefined2 *)puVar2 = *(undefined2 *)(iVar3 + (int)puVar2);
        puVar2 = (undefined4 *)((int)puVar2 + 2);
      } while (iVar1 != 0);
    }
    puVar2 = (undefined4 *)(param_2 + 0xac);
    if (puVar2 != puVar4 + 0x12) {
      iVar3 = (int)(puVar4 + 0x12) - (int)puVar2;
      iVar1 = 0x18;
      do {
        iVar1 = iVar1 + -1;
        *(undefined2 *)puVar2 = *(undefined2 *)(iVar3 + (int)puVar2);
        puVar2 = (undefined4 *)((int)puVar2 + 2);
      } while (iVar1 != 0);
    }
    iVar3 = param_1 * 8;
    *(uint *)(param_2 + 0xdc) = puVar4[0x1e] & 0x3ff;
    *(undefined1 *)(param_2 + 0xe0) = *(undefined1 *)(puVar4 + 0x22);
    *(undefined1 *)(param_2 + 0xe1) = *(undefined1 *)((int)puVar4 + 0x89);
    *(undefined1 *)(param_2 + 0xe2) = *(undefined1 *)((int)puVar4 + 0x8a);
    *(undefined2 *)(param_2 + 0xe4) = *(undefined2 *)(puVar4 + 0x23);
    *(undefined4 *)(param_2 + 0xe8) = (&DAT_82acb934)[param_1 * 2];
    *(undefined4 *)(param_2 + 0xec) = *(undefined4 *)(&DAT_82acb938 + iVar3);
    *(undefined1 *)(param_2 + 0xf0) = (&DAT_82acd874)[iVar3];
    *(undefined2 *)(param_2 + 0xf2) = *(undefined2 *)(&DAT_82acd876 + iVar3);
    *(undefined *)(param_2 + 0xf4) = (&DAT_82acd878)[iVar3];
    *(undefined *)(param_2 + 0xf5) = (&DAT_82acd879)[iVar3];
    *(undefined *)(param_2 + 0xf6) = (&DAT_82acd87a)[iVar3];
    *(undefined *)(param_2 + 0xf7) = (&DAT_82acd87b)[iVar3];
  }
  return;
}



