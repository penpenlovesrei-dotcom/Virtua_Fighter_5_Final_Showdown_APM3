// ===================================================
// 18024F500  ->  FUN_18024f500  (entree 18024f500)
// ===================================================

void FUN_18024f500(int param_1,int param_2,int param_3,int param_4)

{
  longlong lVar1;
  longlong *plVar2;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  
  lVar1 = FUN_180253c90();
  *(uint *)(lVar1 + 0xd8bd4) = *(uint *)(lVar1 + 0xd8bd4) | 0x800;
  *(int *)(lVar1 + 0xd961c) = param_1;
  *(int *)(lVar1 + 0xd9620) = param_2;
  *(int *)(lVar1 + 0xd9624) = param_3;
  *(int *)(lVar1 + 0xd9628) = param_4;
  local_10 = param_1 + param_3;
  local_c = param_2 + param_4;
  if ((0 < param_3) && (0 < param_4)) {
    local_18 = param_1;
    local_14 = param_2;
    plVar2 = (longlong *)FUN_180253c90();
    lVar1 = *plVar2;
    if (lVar1 != 0) {
      FUN_180261840(lVar1,&local_18,lVar1 + 0x1e50,0,1);
    }
  }
  return;
}



