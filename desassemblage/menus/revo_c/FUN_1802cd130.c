/* FUN_1802cd130  --  VF5FS+0x2cd130
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1802cd130.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1802cd130(longlong *param_1)

{
  longlong *plVar1;
  undefined8 *puVar2;
  char cVar3;
  
  if (*(int *)((longlong)param_1 + 0x1c) == 1) {
    if (((int)param_1[3] == 1) && (cVar3 = (**(code **)(*param_1 + 8))(), cVar3 != '\0')) {
      *(undefined4 *)((longlong)param_1 + 0x24) = 2;
      *(undefined4 *)(param_1 + 3) = 2;
    }
    if (((int)param_1[3] == 2) && (cVar3 = (**(code **)(*param_1 + 0x10))(param_1), cVar3 != '\0'))
    {
      for (plVar1 = (longlong *)*DAT_180ea7608; plVar1 != (longlong *)0x0;
          plVar1 = (longlong *)plVar1[2]) {
        if (*(longlong **)(*plVar1 + 0x10) == param_1) {
          FUN_1802cd990(*plVar1,2);
        }
      }
      *(undefined4 *)(param_1 + 4) = 2;
      FUN_1802cda90(param_1);
    }
    if (((int)param_1[3] == 3) && (cVar3 = (**(code **)(*param_1 + 0x18))(), cVar3 != '\0')) {
      *(undefined4 *)(param_1 + 5) = 0;
      puVar2 = DAT_180ea7608;
      if (*(char *)((longlong)param_1 + 0x2c) != '\0') {
        param_1[3] = 0;
        param_1[4] = 1;
        if (*(char *)(puVar2 + 3) == '\0') {
          *(undefined4 *)((longlong)param_1 + 0x24) = 1;
          *(undefined4 *)(param_1 + 5) = 1;
          *(undefined4 *)(param_1 + 4) = 0;
          *(undefined4 *)(param_1 + 3) = 1;
          *(undefined4 *)((longlong)param_1 + 0x1c) = 1;
          *(undefined1 *)((longlong)param_1 + 0x2c) = 0;
          return;
        }
        *(undefined4 *)(param_1 + 3) = 0;
        *(undefined4 *)((longlong)param_1 + 0x1c) = 0;
        *(undefined1 *)((longlong)param_1 + 0x2c) = 0;
        return;
      }
      *(undefined4 *)(param_1 + 4) = 0;
      *(undefined4 *)((longlong)param_1 + 0x24) = 4;
    }
  }
  return;
}
