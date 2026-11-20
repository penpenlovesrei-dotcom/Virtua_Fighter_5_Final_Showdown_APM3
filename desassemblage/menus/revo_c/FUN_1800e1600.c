/* FUN_1800e1600  --  VF5FS+0xe1600
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800e1600.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1800e1600(void)

{
  bool bVar1;
  char cVar2;
  int iVar3;
  ulonglong uVar4;
  int *piVar5;
  undefined4 uVar6;
  ulonglong uVar7;
  ulonglong uVar8;
  
  iVar3 = FUN_18000ba10(&DAT_1806af364);
  if (iVar3 != 0) {
    _guard_check_icall(iVar3);
  }
  if (DAT_180751400 == '\0') {
    if ((DAT_18075141c != '\0') && (DAT_18075141d != '\0')) {
      cVar2 = FUN_1802cca60();
      if (cVar2 != '\0') goto LAB_1800e1886;
      uVar6 = 0xe;
      iVar3 = DAT_180751410;
      goto LAB_1800e1687;
    }
  }
  else {
    if ((DAT_180751401 != '\0') && (DAT_18075141d != '\0')) {
      cVar2 = FUN_1802cca60();
      if (cVar2 != '\0') goto LAB_1800e1886;
      uVar6 = DAT_1807513f4;
      iVar3 = 0x49;
      if (DAT_18075141c != '\0') {
        iVar3 = DAT_180751410;
      }
LAB_1800e1687:
      FUN_1800e1960(uVar6,iVar3);
      DAT_18075141d = '\0';
      DAT_180751401 = '\0';
    }
    if ((DAT_180751400 != '\0') && (DAT_18075141d != '\0')) {
      DAT_1807513fc = 2;
    }
  }
  uVar8 = 0;
  uVar4 = uVar8;
  uVar7 = uVar8;
  while (*(int *)((longlong)&DAT_1803c8240 + uVar4) != DAT_1807513f0) {
    uVar7 = uVar7 + 1;
    uVar4 = uVar4 + 0x68;
    if (0x5af < uVar4) {
      _DAT_180751404 = _DAT_180751404 + 1;
      return;
    }
  }
  if (uVar7 * 0x68 == -0x1803c8240) goto LAB_1800e1886;
  cVar2 = DAT_1807513fc != 1;
  if ((code *)(&PTR_FUN_1803c8248)[uVar7 * 0xd + (longlong)DAT_1807513fc] != (code *)0x0) {
    cVar2 = (*(code *)(&PTR_FUN_1803c8248)[uVar7 * 0xd + (longlong)DAT_1807513fc])();
  }
  if (cVar2 == '\0') {
LAB_1800e1772:
    if (DAT_1807513fc == 0) goto LAB_1800e1886;
  }
  else if (DAT_1807513fc == 0) {
    DAT_1807513fc = 1;
  }
  else if (DAT_1807513fc == 1) {
    DAT_1807513fc = 2;
  }
  else {
    if (DAT_1807513fc != 2) goto LAB_1800e1772;
    if (DAT_180751400 == '\0') {
      DAT_180751400 = '\x01';
      DAT_18075141c = '\x01';
    }
    DAT_180751401 = '\x01';
  }
  if (DAT_18075141d == '\0') {
    if ((DAT_180751400 != '\0') || (DAT_18075141c != '\0')) {
      DAT_180751418 = 2;
    }
    piVar5 = &DAT_1803c87f0;
    bVar1 = false;
    do {
      if (*piVar5 == DAT_18075140c) {
        if ((uVar8 * 0x20 != -0x1803c87f0) &&
           (((DAT_180751418 == 3 ||
             ((code *)(&PTR_FUN_1803c87f8)[uVar8 * 4 + (longlong)DAT_180751418] == (code *)0x0)) ||
            (cVar2 = (*(code *)(&PTR_FUN_1803c87f8)[uVar8 * 4 + (longlong)DAT_180751418])(),
            cVar2 != '\0')))) {
          if (DAT_180751418 != 0) {
            if (DAT_180751418 == 1) {
              DAT_180751418 = 2;
            }
            else if (DAT_180751418 == 2) {
              bVar1 = true;
              goto LAB_1800e1837;
            }
            _DAT_180751420 = _DAT_180751420 + 1;
            goto LAB_1800e1886;
          }
          DAT_180751418 = 1;
        }
LAB_1800e1837:
        _DAT_180751420 = _DAT_180751420 + 1;
        if (bVar1) {
          if (((DAT_180751400 == '\0') && (DAT_18075141c == '\0')) &&
             (DAT_18075141c = '\x01', DAT_180751410 == 0x49)) {
            DAT_180751400 = '\x01';
            DAT_180751410 = 0x49;
          }
          DAT_18075141d = '\x01';
        }
        goto LAB_1800e1886;
      }
      uVar8 = uVar8 + 1;
      piVar5 = piVar5 + 8;
    } while (uVar8 < 0x49);
    _DAT_180751420 = _DAT_180751420 + 1;
  }
LAB_1800e1886:
  _DAT_180751404 = _DAT_180751404 + 1;
  return;
}
