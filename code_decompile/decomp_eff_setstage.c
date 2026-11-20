// ===================================================
// 1800706B0  ->  FUN_1800706b0  (entree 1800706b0)
// ===================================================

void FUN_1800706b0(longlong param_1,int param_2)

{
  ulonglong uVar1;
  undefined4 *puVar2;
  longlong lVar3;
  char cVar4;
  undefined *puVar5;
  int iVar6;
  int *piVar7;
  undefined4 local_res18 [4];
  
  puVar5 = &DAT_18034fd20;
  iVar6 = 4;
  do {
    if (iVar6 == param_2) {
      if ((puVar5 != (undefined *)0x0) && (piVar7 = *(int **)(puVar5 + 8), piVar7 != (int *)0x0)) {
        if (param_2 == 8) {
          *(undefined1 *)(param_1 + 0xb1) = 1;
        }
        else if (param_2 == 0x28) {
          *(undefined1 *)(param_1 + 0xb0) = 1;
        }
        iVar6 = *piVar7;
        while ((iVar6 != -1 && (*(longlong *)(param_1 + 0x58) != *(longlong *)(param_1 + 0x60)))) {
          FUN_18003c370(local_res18,iVar6);
          cVar4 = FUN_180041a80(local_res18);
          if (cVar4 != '\0') {
            FUN_180044830(local_res18);
            lVar3 = *(longlong *)(param_1 + 0x58);
            uVar1 = lVar3 + 1;
            if (uVar1 <= *(ulonglong *)(param_1 + 0x60)) {
              *(ulonglong *)(param_1 + 0x58) = uVar1;
              puVar2 = (undefined4 *)(*(longlong *)(param_1 + 0x68) + lVar3 * 4);
              if (puVar2 != (undefined4 *)0x0) {
                *puVar2 = local_res18[0];
              }
            }
          }
          iVar6 = piVar7[1];
          piVar7 = piVar7 + 1;
        }
      }
      return;
    }
    iVar6 = *(int *)(puVar5 + 0x10);
    puVar5 = puVar5 + 0x10;
  } while (iVar6 != -1);
  return;
}



// ===================================================
// 1800843A0  ->  FUN_1800843a0  (entree 1800843a0)
// ===================================================

void FUN_1800843a0(longlong param_1,int param_2)

{
  int iVar1;
  undefined *puVar2;
  
  puVar2 = &DAT_180355c30;
  iVar1 = 10;
  do {
    if (iVar1 == param_2) {
      if (puVar2 != (undefined *)0x0) {
        FUN_1800848c0(param_1,*(undefined8 *)(puVar2 + 8),*(undefined8 *)(puVar2 + 0x10),
                      *(undefined8 *)(puVar2 + 0x18),*(undefined8 *)(puVar2 + 0x28),
                      *(undefined8 *)(puVar2 + 0x30),*(undefined8 *)(puVar2 + 0x38));
        *(undefined8 *)(param_1 + 0xd58) = *(undefined8 *)(puVar2 + 0x20);
      }
      return;
    }
    iVar1 = *(int *)(puVar2 + 0x40);
    puVar2 = puVar2 + 0x40;
  } while (iVar1 != -1);
  return;
}



