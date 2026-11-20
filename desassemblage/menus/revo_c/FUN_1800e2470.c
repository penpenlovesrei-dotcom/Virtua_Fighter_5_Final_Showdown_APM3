/* FUN_1800e2470  --  VF5FS+0xe2470
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800e2470.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined4 FUN_1800e2470(void)

{
  undefined8 uVar1;
  char cVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  int iVar7;
  
  uVar1 = FUN_1800b21e0();
  FUN_1800da490(&DAT_18074fe70,3);
  if ((DAT_180751490 == 0) || (DAT_180751490 != 1)) {
    cVar2 = FUN_1802cca00(DAT_1807598b8);
    if (cVar2 != '\0') {
      cVar2 = FUN_18017bb70(DAT_1807598b8);
      if (cVar2 == '\0') {
        cVar2 = FUN_18017ae00(DAT_1807598b8,0);
        if ((cVar2 != '\0') && (cVar2 = FUN_1800b6e60(0), cVar2 != '\0')) {
          FUN_1800b2f30(uVar1,0,1,0);
          FUN_18017b7d0(DAT_1807598b8,0);
        }
        cVar2 = FUN_18017ae00(DAT_1807598b8,1);
        if (cVar2 == '\0') {
          return 0;
        }
        cVar2 = FUN_1800b6e60(1);
        if (cVar2 == '\0') {
          return 0;
        }
        FUN_1800b2f30(uVar1,1,1,0);
        FUN_18017b7d0(DAT_1807598b8,1);
        return 0;
      }
      iVar7 = 0;
      do {
        uVar3 = FUN_18017b820(DAT_1807598b8,iVar7);
        uVar4 = FUN_18017b800(DAT_1807598b8,iVar7);
        uVar5 = FUN_18017b7f0(DAT_1807598b8,iVar7,uVar4);
        uVar6 = FUN_18017b810(DAT_1807598b8,iVar7);
        FUN_1800b2f10(uVar1,iVar7,uVar3,uVar5,uVar4,uVar6);
        iVar7 = iVar7 + 1;
      } while (iVar7 < 2);
    }
    DAT_180751490 = 1;
  }
  cVar2 = FUN_1802cca00(DAT_1807598b8);
  if (cVar2 == '\0') {
    if ((DAT_180c8de18 == '\0') && (cVar2 = FUN_18017bba0(DAT_1807598b8), cVar2 != '\0')) {
      FUN_1801951d0(0);
      FUN_1800e1b00(5);
      return 1;
    }
    cVar2 = FUN_18000ba20();
    if ((cVar2 == '\0') && (cVar2 = FUN_18000ba20(), cVar2 == '\0')) {
      if (*(char *)(DAT_180754a90 + 0x19) != '\0') {
        uVar1 = FUN_180106f30(DAT_180754a90,0);
        _guard_check_icall(0,uVar1,0x4b0);
      }
      if (*(char *)(DAT_180754a90 + 0x609) != '\0') {
        uVar1 = FUN_180106f30(DAT_180754a90,1);
        _guard_check_icall(1,uVar1,0x4b0);
      }
      return 1;
    }
  }
  return 0;
}
