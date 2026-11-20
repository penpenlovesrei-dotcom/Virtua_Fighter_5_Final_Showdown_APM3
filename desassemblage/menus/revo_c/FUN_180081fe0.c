/* FUN_180081fe0  --  VF5FS+0x81fe0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180081fe0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


ulonglong FUN_180081fe0(int param_1,longlong param_2,longlong param_3,char param_4)

{
  longlong lVar1;
  longlong *plVar2;
  bool bVar3;
  longlong *plVar4;
  longlong *plVar5;
  ulonglong in_RAX;
  longlong lVar6;
  
  plVar5 = DAT_18073aa18;
  lVar6 = (longlong)param_1;
  bVar3 = true;
  if (DAT_18073aa10 == 0) {
    return in_RAX & 0xffffffffffffff00;
  }
  lVar1 = *(longlong *)(&DAT_18073aa28 + lVar6 * 0x10);
  do {
    if (lVar1 == 0) {
LAB_180082039:
      if (DAT_18073aa18 == (longlong *)0x0) {
        return 0;
      }
      if (bVar3) {
        lVar1 = *DAT_18073aa18;
        DAT_18073aa18 = (longlong *)DAT_18073aa18[1];
        if (lVar1 != 0) {
          *(longlong **)(lVar1 + 8) = DAT_18073aa18;
        }
        if ((longlong *)plVar5[1] != (longlong *)0x0) {
          *(longlong *)plVar5[1] = *plVar5;
        }
        plVar5[3] = param_2;
        *plVar5 = 0;
        plVar5[1] = 0;
        plVar5[2] = param_3;
        *(undefined1 *)(plVar5 + 4) = 1;
        plVar2 = *(longlong **)(&DAT_18073aa28 + lVar6 * 0x10);
        if (param_4 == '\0') {
          if (plVar2 != (longlong *)0x0) {
            *plVar5 = *plVar2;
            plVar5[1] = (longlong)plVar2;
            *plVar2 = (longlong)plVar5;
          }
          *(longlong **)(&DAT_18073aa28 + lVar6 * 0x10) = plVar5;
        }
        else {
          if (plVar2 != (longlong *)0x0) {
            for (plVar4 = (longlong *)plVar2[1]; plVar4 != (longlong *)0x0;
                plVar4 = (longlong *)plVar4[1]) {
              plVar2 = plVar4;
            }
            plVar2[1] = (longlong)plVar5;
            *plVar5 = (longlong)plVar2;
          }
          if (*(longlong *)(&DAT_18073aa28 + lVar6 * 0x10) == 0) {
            *(longlong **)(&DAT_18073aa28 + lVar6 * 0x10) = plVar5;
            return 1;
          }
        }
      }
      return (ulonglong)bVar3;
    }
    if ((*(longlong *)(lVar1 + 0x18) == param_2) && (*(longlong *)(lVar1 + 0x10) == param_3)) {
      bVar3 = false;
      goto LAB_180082039;
    }
    lVar1 = *(longlong *)(lVar1 + 8);
  } while( true );
}
