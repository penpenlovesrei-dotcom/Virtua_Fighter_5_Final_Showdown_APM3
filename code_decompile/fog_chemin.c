// ===================================================
// 1800D71AD  ->  FUN_1800d7150  (entree 1800d7150)
// ===================================================

void FUN_1800d7150(longlong param_1,undefined8 param_2)

{
  char cVar1;
  longlong lVar2;
  longlong lVar3;
  
  if (*(int *)(param_1 + 0x14) != 0) {
    lVar2 = param_1 + 0x620;
    lVar3 = 6;
    do {
      cVar1 = FUN_180217bf0(lVar2);
      if (cVar1 != '\0') {
        FUN_180216620(lVar2,1);
      }
      lVar2 = lVar2 + 0x90;
      lVar3 = lVar3 + -1;
    } while (lVar3 != 0);
  }
  *(undefined8 *)(param_1 + 0x18) = param_2;
  FUN_1800172b0(param_1 + 0x20,0x100,"%s/%s.ibl","./rom/ibl",param_2);
  FUN_1800172b0(param_1 + 0x120,0x100,"%s/light_%s.txt","./rom/light_param",param_2);
  FUN_1800172b0(param_1 + 0x220,0x100,"%s/fog_%s.txt","./rom/light_param",param_2);
  FUN_1800172b0(param_1 + 800,0x100,"%s/glow_%s.txt","./rom/light_param",param_2);
  FUN_1800172b0(param_1 + 0x420,0x100,"%s/wind_%s.txt","./rom/light_param",param_2);
  FUN_1800172b0(param_1 + 0x520,0x100,"%s/envmap_correct_%s.txt","./rom/light_param",param_2);
  *(undefined4 *)(param_1 + 0x14) = 1;
  return;
}



