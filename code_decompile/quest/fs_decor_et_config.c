// ===================================================
// 1800AF400  ->  FUN_1800af400  (entree 1800af400)
// ===================================================

uint FUN_1800af400(uint param_1)

{
  uint *puVar1;
  uint uVar2;
  
  uVar2 = 0xffffffff;
  if (((DAT_1806f9c10 != 0) && (param_1 < 0x15)) && (*(char *)(DAT_1806f9c10 + 0x9c) != '\0')) {
    puVar1 = *(uint **)(DAT_1806f9c10 + 0xa0);
    if (puVar1 != *(uint **)(DAT_1806f9c10 + 0xa8)) {
      while (*puVar1 != param_1) {
        puVar1 = puVar1 + 2;
        if (puVar1 == *(uint **)(DAT_1806f9c10 + 0xa8)) {
          return 0xffffffff;
        }
      }
      uVar2 = puVar1[1];
    }
  }
  return uVar2;
}



// ===================================================
// 1800484B0  ->  FUN_1800484b0  (entree 1800484b0)
// ===================================================

undefined * FUN_1800484b0(void)

{
  return &DAT_18066b830;
}



// ===================================================
// 180047DE0  ->  FUN_180047de0  (entree 180047de0)
// ===================================================

undefined4 FUN_180047de0(longlong *param_1)

{
  longlong lVar1;
  byte bVar2;
  ulonglong uVar3;
  
  bVar2 = (**(code **)(*(longlong *)*param_1 + 8))();
  uVar3 = (ulonglong)bVar2;
  lVar1 = *param_1;
  if ((uVar3 < *(ulonglong *)(lVar1 + 0x10)) || (*(ulonglong *)(lVar1 + 0x18) <= uVar3)) {
    uVar3 = *(ulonglong *)(lVar1 + 8);
  }
  return *(undefined4 *)(*(longlong *)(lVar1 + 0x20) + uVar3 * 0x10);
}



// ===================================================
// 18019C080  ->  FUN_18019c080  (entree 18019c080)
// ===================================================

undefined * FUN_18019c080(void)

{
  return &DAT_180751014;
}



// ===================================================
// 18019C060  ->  FUN_18019c060  (entree 18019c060)
// ===================================================

undefined1 FUN_18019c060(void)

{
  return DAT_18075101a;
}



