// ===================================================
// 1801EFE51  ->  FUN_1801efdd0  (entree 1801efdd0)
// ===================================================

undefined8 FUN_1801efdd0(void)

{
  char cVar1;
  longlong lVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  uint uVar5;
  uint *puVar6;
  
  if (((DAT_180c3b6f0 == 0) || (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) == 0)) &&
     (DAT_180753900 == (uint *)0x0)) {
    cVar1 = FUN_180217bf0(&DAT_180753870);
    if ((cVar1 == '\0') && (lVar2 = FUN_180217940(&DAT_180753870), lVar2 != 0)) {
      uVar3 = FUN_180217be0(&DAT_180753870);
      DAT_180753900 = (uint *)FUN_180218410(0,uVar3,"str_ary",0);
      uVar3 = FUN_180217be0(&DAT_180753870);
      uVar4 = FUN_180217940(&DAT_180753870);
      FUN_180300010(DAT_180753900,uVar4,uVar3);
      FUN_180217900(&DAT_180753870,1);
      puVar6 = DAT_180753900;
      do {
        uVar5 = *puVar6;
        *puVar6 = uVar5 >> 0x18 | (uVar5 & 0xff0000) >> 8 | (uVar5 & 0xff00) << 8 | uVar5 << 0x18;
        if (*puVar6 != 0) {
          uVar5 = 0;
          lVar2 = (longlong)(int)*puVar6 + (longlong)DAT_180753900;
          if (lVar2 != 0) {
            uVar5 = (int)lVar2 - (int)puVar6;
          }
          *puVar6 = uVar5;
        }
        puVar6 = puVar6 + 1;
        lVar2 = 0;
        if (*puVar6 != 0) {
          lVar2 = (longlong)puVar6 + (longlong)(int)*puVar6;
        }
      } while (lVar2 != 0);
      return 0;
    }
    return 1;
  }
  return 0;
}



