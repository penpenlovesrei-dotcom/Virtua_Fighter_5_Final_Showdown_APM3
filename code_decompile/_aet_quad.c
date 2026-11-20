// ===================================================
// 180025870  ->  FUN_180025870  (entree 180025870)
// ===================================================

void FUN_180025870(longlong *param_1,undefined8 *param_2,longlong param_3,float param_4,
                  float param_5)

{
  float fVar1;
  undefined1 auVar2 [16];
  float *pfVar3;
  longlong lVar4;
  longlong lVar5;
  float local_res18 [2];
  float local_res20 [2];
  undefined8 local_58;
  undefined8 uStack_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined8 local_38;
  undefined8 uStack_30;
  undefined8 uStack_28;
  undefined8 uStack_20;
  
  if ((((*(float *)(param_3 + 4) <= param_4) && (param_4 < *(float *)(param_3 + 8))) &&
      (*(char *)(param_3 + 0x17) != '\x02')) &&
     (((*(byte *)(param_3 + 0x14) & 1) != 0 || (*(char *)((longlong)param_1 + 0x9c) != '\0')))) {
    local_58 = *param_2;
    uStack_50 = param_2[1];
    uStack_48 = param_2[2];
    uStack_40 = param_2[3];
    local_38 = param_2[4];
    uStack_30 = param_2[5];
    uStack_28 = param_2[6];
    uStack_20 = param_2[7];
    (**(code **)(*param_1 + 0xd8))(param_1,&local_58);
    lVar5 = 0;
    lVar4 = lVar5;
    if (*(int *)(param_3 + 0x28) != 0) {
      lVar4 = param_3 + 0x28 + (longlong)*(int *)(param_3 + 0x28);
    }
    local_res18[0] = (float)FUN_18001a3c0(lVar4 + 0x3c);
    local_res20[0] = 0.0;
    pfVar3 = local_res20;
    if (0.0 <= local_res18[0]) {
      pfVar3 = local_res18;
    }
    auVar2 = vcmpss_avx(ZEXT416((uint)*pfVar3),ZEXT416(DAT_180346d3c),1);
    auVar2 = vblendvps_avx(ZEXT416(DAT_180346d3c),ZEXT416((uint)*pfVar3),auVar2);
    param_5 = auVar2._0_4_ * param_5;
    fVar1 = (param_4 - *(float *)(param_3 + 4)) * *(float *)(param_3 + 0x10) +
            *(float *)(param_3 + 0xc);
    if (*(char *)(param_3 + 0x17) == '\x01') {
      (**(code **)(*param_1 + 0xc0))(param_1,&local_58,param_3,fVar1,param_5);
    }
    else if (*(char *)(param_3 + 0x17) == '\x03') {
      if (*(int *)(param_3 + 0x18) != 0) {
        lVar5 = param_3 + 0x18 + (longlong)*(int *)(param_3 + 0x18);
      }
      (**(code **)(*param_1 + 0xa8))(param_1,&local_58,lVar5,fVar1,param_5);
    }
  }
  return;
}



