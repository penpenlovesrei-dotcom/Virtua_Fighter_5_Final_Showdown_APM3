// ===================================================
// 839511C  ->  FUN_0839511c  (entree 0839511c)
// ===================================================

void FUN_0839511c(int *param_1,int param_2)

{
  char cVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  char *pcVar5;
  undefined4 local_20;
  int local_1c;
  int local_14;
  
  iVar2 = 0;
  iVar4 = 0;
  local_14 = 0;
  do {
    if (*(int *)((int)&DAT_08604520 + iVar2) == param_2) {
      local_14 = (int)&DAT_08604520 + iVar2;
      break;
    }
    iVar4 = iVar4 + 1;
    iVar2 = iVar2 + 0x14;
  } while (iVar4 < 2);
  if ((local_14 != 0) && (iVar2 = 0, 0 < *param_1)) {
    local_1c = 0;
    do {
      iVar4 = local_1c + param_1[1];
      *(undefined4 *)(iVar4 + 0x20) = *(undefined4 *)(local_14 + 0xc);
      if (*(int *)(iVar4 + 8) == 0) {
        local_20 = *(undefined4 *)(local_14 + 4);
        iVar3 = -1;
        pcVar5 = *(char **)(local_14 + 0x10);
        do {
          if (iVar3 == 0) break;
          iVar3 = iVar3 + -1;
          cVar1 = *pcVar5;
          pcVar5 = pcVar5 + 1;
        } while (cVar1 != '\0');
        std::string::assign((char *)(iVar4 + 0x24),(uint)*(char **)(local_14 + 0x10));
      }
      else {
        local_20 = *(undefined4 *)(local_14 + 8);
      }
      iVar2 = iVar2 + 1;
      FUN_083954c4(iVar4,local_20);
      local_1c = local_1c + 0x28;
    } while (iVar2 < *param_1);
  }
  return;
}



