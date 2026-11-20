// ===================================================
// 18014F5CA  ->  FUN_18014f4a0  (entree 18014f4a0)
// ===================================================

void FUN_18014f4a0(longlong param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  longlong lVar1;
  undefined8 *puVar2;
  longlong *plVar3;
  undefined8 *puVar4;
  ulonglong uVar5;
  longlong *plVar6;
  longlong lVar7;
  longlong *plVar8;
  longlong *plVar9;
  undefined8 uVar10;
  undefined1 local_70 [16];
  undefined8 local_60;
  undefined8 local_58;
  longlong local_50 [3];
  ulonglong local_38;
  
  uVar10 = 0xfffffffffffffffe;
  uVar5 = 0;
  puVar4 = (undefined8 *)(param_1 + 0x118);
  do {
    if (*(char *)(puVar4 + 0x16) != '\0') {
      *(undefined4 *)(puVar4 + -0x22) = *(undefined4 *)(puVar4 + -6);
      *(undefined4 *)((longlong)puVar4 + -0x10c) = *(undefined4 *)((longlong)puVar4 + -0x2c);
      *(undefined4 *)(puVar4 + -0x21) = *(undefined4 *)(puVar4 + -5);
      puVar4[-0x20] = puVar4[-4];
      *(undefined4 *)(puVar4 + -0x1f) = *(undefined4 *)(puVar4 + -3);
      *(undefined4 *)((longlong)puVar4 + -0xf4) = *(undefined4 *)((longlong)puVar4 + -0x14);
      plVar3 = puVar4 + -2;
      plVar9 = puVar4 + -0x1e;
      if (plVar9 != plVar3) {
        if (0xf < (ulonglong)puVar4[1]) {
          plVar3 = (longlong *)*plVar3;
        }
        FUN_180010a10(plVar9,plVar3,*puVar4,param_4,uVar10);
      }
      plVar3 = puVar4 + 2;
      plVar8 = puVar4 + -0x1a;
      if (plVar8 != plVar3) {
        if (0xf < (ulonglong)puVar4[5]) {
          plVar3 = (longlong *)*plVar3;
        }
        FUN_180010a10(plVar8,plVar3,puVar4[4],param_4,uVar10);
      }
      plVar3 = puVar4 + 6;
      plVar6 = puVar4 + -0x16;
      if (plVar6 != plVar3) {
        if (0xf < (ulonglong)puVar4[9]) {
          plVar3 = (longlong *)*plVar3;
        }
        FUN_180010a10(plVar6,plVar3,puVar4[8],param_4,uVar10);
      }
      puVar4[-0x12] = puVar4[10];
      puVar4[-0x11] = puVar4[0xb];
      puVar4[-0x10] = puVar4[0xc];
      puVar4[-0xf] = puVar4[0xd];
      puVar4[-0xe] = puVar4[0xe];
      puVar4[-0xd] = puVar4[0xf];
      puVar4[-0xc] = puVar4[0x10];
      puVar4[-0xb] = puVar4[0x11];
      puVar4[-10] = puVar4[0x12];
      puVar4[-9] = puVar4[0x13];
      puVar4[-8] = puVar4[0x14];
      puVar4[-7] = puVar4[0x15];
      if (*(int *)((longlong)puVar4 + -0x10c) != 0x15) {
        lVar1 = FUN_18012ca90();
        FUN_1800f9c60(*(undefined4 *)(puVar4 + -0x21),0);
        if (puVar4[-0x20] != 0) {
          FUN_180088420(puVar4[-0x20],*(undefined4 *)((longlong)puVar4 + -0x10c));
          FUN_18014bcd0(puVar4[-0x20]);
        }
        FUN_1800e7140(*(undefined4 *)(puVar4 + -0x1f));
        FUN_1800e7140(*(undefined4 *)((longlong)puVar4 + -0xf4));
        FUN_180159ed0(*(undefined4 *)(puVar4 + -0x1f));
        FUN_180062b30(*(undefined4 *)(puVar4 + -0x22),*(undefined4 *)((longlong)puVar4 + -0x10c));
        if (0xf < (ulonglong)puVar4[-0x1b]) {
          plVar9 = (longlong *)*plVar9;
        }
        FUN_180185a60(plVar9);
        if (0xf < (ulonglong)puVar4[-0x17]) {
          plVar8 = (longlong *)*plVar8;
        }
        FUN_180185a60(plVar8);
        if (puVar4[-0x14] != 0) {
          if (0xf < (ulonglong)puVar4[-0x13]) {
            plVar6 = (longlong *)*plVar6;
          }
          FUN_180185a60(plVar6);
        }
        FUN_18003c200(lVar1);
        local_60 = 0;
        local_58 = 0xf;
        local_70[0] = 0;
        lVar7 = -1;
        do {
          lVar7 = lVar7 + 1;
        } while (*(char *)(lVar1 + lVar7) != '\0');
        FUN_180010a10(local_70,lVar1);
        puVar2 = (undefined8 *)FUN_18014f280(local_50,local_70);
        if (0xf < (ulonglong)puVar2[3]) {
          puVar2 = (undefined8 *)*puVar2;
        }
        FUN_18003c200(puVar2);
        if (0xf < local_38) {
          if (0xfff < local_38 + 1) {
            if (0x1f < (local_50[0] - *(longlong *)(local_50[0] + -8)) - 8U) {
                    /* WARNING: Subroutine does not return */
              FUN_180303af0(*(longlong *)(local_50[0] + -8),local_38 + 0x28);
            }
          }
          FUN_1802fdd80();
        }
        FUN_1801f1010(*(undefined4 *)(puVar4 + -0x22),*(undefined4 *)((longlong)puVar4 + -0x10c));
      }
    }
    uVar5 = uVar5 + 1;
    puVar4 = puVar4 + 0x39;
  } while (uVar5 < 2);
  return;
}



// ===================================================
// 180062BF2  ->  FUN_180062b30  (entree 180062b30)
// ===================================================

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_180062b30(int param_1,int param_2)

{
  undefined8 *puVar1;
  ulonglong uVar2;
  int *piVar3;
  longlong lVar4;
  longlong *plVar5;
  undefined8 *puVar6;
  undefined8 *puVar7;
  undefined8 *puVar8;
  undefined1 *puVar9;
  undefined8 *******pppppppuVar10;
  int local_res18;
  int iStackX_1c;
  longlong local_228 [2];
  longlong lStack_218;
  ulonglong uStack_210;
  undefined8 *******local_208;
  longlong lStack_200;
  ulonglong uStack_1f8;
  ulonglong uStack_1f0;
  undefined8 local_1e8;
  undefined8 *******local_1e0;
  longlong lStack_1d8;
  longlong lStack_1d0;
  ulonglong uStack_1c8;
  undefined **local_1b8;
  undefined4 local_1b0;
  undefined1 local_1a8;
  longlong local_198;
  ulonglong uStack_190;
  undefined1 local_188 [144];
  undefined4 local_f8;
  int local_e8 [2];
  undefined1 local_e0 [200];
  
  local_1e8 = 0xfffffffffffffffe;
  if (param_2 == 0x13) {
    param_2 = 0;
  }
  for (piVar3 = (int *)*DAT_180676f38; piVar3 != (int *)DAT_180676f38[1]; piVar3 = piVar3 + 2) {
    if (*piVar3 == param_1) {
      if (-1 < piVar3[1]) goto LAB_180062beb;
      break;
    }
  }
  if ((ulonglong)(DAT_180676f38[2] - (longlong)*DAT_180676f38 >> 3) < 4) {
    FUN_18003bb00(DAT_180676f38,4);
  }
  puVar6 = DAT_180676f38;
  puVar1 = (undefined8 *)DAT_180676f38[1];
  local_res18 = param_1;
  iStackX_1c = param_2;
  if ((undefined8 *)DAT_180676f38[2] == puVar1) {
    FUN_18002c630(DAT_180676f38,puVar1,&local_res18);
  }
  else {
    *puVar1 = CONCAT44(param_2,param_1);
    puVar6[1] = puVar6[1] + 8;
  }
LAB_180062beb:
  lVar4 = FUN_18012ca90(param_2);
  if (lVar4 == 0) {
    FUN_1801d8720("request_load_ctrl_file(): illegal chara_id(%d).\n",param_2);
    return;
  }
  uStack_1f8 = 0;
  uStack_1f0 = 0xf;
  local_208 = (undefined8 *******)((ulonglong)local_208 & 0xffffffffffffff00);
  FUN_1800524e0(&local_208,lVar4);
  lStack_218 = _DAT_1803478a0;
  uStack_210 = _UNK_1803478a8;
  local_228[0]._0_1_ = 0;
  FUN_180012df0(local_228,uStack_1f8 + 0xf);
  if (uStack_210 - lStack_218 < 0xf) {
    FUN_18000bff0(local_228,0xf,0,"./rom/rob/ctrl_",0xf);
  }
  else {
    puVar9 = (undefined1 *)local_228;
    if (0xf < uStack_210) {
      puVar9 = (undefined1 *)CONCAT71(local_228[0]._1_7_,(undefined1)local_228[0]);
    }
    puVar9 = puVar9 + lStack_218;
    lStack_218 = lStack_218 + 0xf;
    FUN_180300010(puVar9,"./rom/rob/ctrl_",0xf);
    puVar9[0xf] = 0;
  }
  uVar2 = uStack_1f8;
  pppppppuVar10 = &local_208;
  if (0xf < uStack_1f0) {
    pppppppuVar10 = local_208;
  }
  if (uStack_210 - lStack_218 < uStack_1f8) {
    FUN_18000bff0(local_228,uStack_1f8,0,pppppppuVar10,uStack_1f8);
  }
  else {
    puVar9 = (undefined1 *)local_228;
    if (0xf < uStack_210) {
      puVar9 = (undefined1 *)CONCAT71(local_228[0]._1_7_,(undefined1)local_228[0]);
    }
    puVar9 = puVar9 + lStack_218;
    lStack_218 = lStack_218 + uStack_1f8;
    FUN_180300010(puVar9,pppppppuVar10,uStack_1f8);
    puVar9[uVar2] = 0;
  }
  if (uStack_210 - lStack_218 < 4) {
    plVar5 = (longlong *)FUN_18000bff0(local_228,4,0,&DAT_18034c110,4);
  }
  else {
    puVar9 = (undefined1 *)local_228;
    if (0xf < uStack_210) {
      puVar9 = (undefined1 *)CONCAT71(local_228[0]._1_7_,(undefined1)local_228[0]);
    }
    puVar9 = puVar9 + lStack_218;
    lStack_218 = lStack_218 + 4;
    FUN_180300010(puVar9,&DAT_18034c110,4);
    puVar9[4] = 0;
    plVar5 = local_228;
  }
  local_1e0 = (undefined8 *******)*plVar5;
  lStack_1d8 = plVar5[1];
  lStack_1d0 = plVar5[2];
  uStack_1c8 = plVar5[3];
  plVar5[2] = 0;
  plVar5[3] = 0xf;
  *(undefined1 *)plVar5 = 0;
  FUN_18000de20(&local_208);
  local_208 = local_1e0;
  lStack_200 = lStack_1d8;
  uStack_1f8 = lStack_1d0;
  uStack_1f0 = uStack_1c8;
  if (0xf < uStack_210) {
    if (0xfff < uStack_210 + 1) {
      lVar4 = *(longlong *)(CONCAT71(local_228[0]._1_7_,(undefined1)local_228[0]) + -8);
      if (0x1f < (CONCAT71(local_228[0]._1_7_,(undefined1)local_228[0]) - lVar4) - 8U) {
                    /* WARNING: Subroutine does not return */
        FUN_180303af0(lVar4,uStack_210 + 0x28);
      }
    }
    FUN_1802fdd80();
  }
  lStack_218 = _DAT_1803478a0;
  uStack_210 = _UNK_1803478a8;
  local_228[0]._0_1_ = 0;
  puVar1 = (undefined8 *)*DAT_180676f40;
  puVar6 = (undefined8 *)puVar1[1];
  puVar8 = puVar1;
  if (*(char *)((longlong)puVar1[1] + 0x19) == '\0') {
    do {
      if (*(int *)(puVar6 + 4) < param_2) {
        puVar7 = (undefined8 *)puVar6[2];
      }
      else {
        puVar7 = (undefined8 *)*puVar6;
        puVar8 = puVar6;
      }
      puVar6 = puVar7;
    } while (*(char *)((longlong)puVar7 + 0x19) == '\0');
    if ((puVar8 == puVar1) || (param_2 < *(int *)(puVar8 + 4))) goto LAB_180062e57;
  }
  else {
LAB_180062e57:
    puVar8 = puVar1;
  }
  if (puVar8 == puVar1) {
    local_1b8 = CtrlFile::vftable;
    local_198 = _DAT_1803478a0;
    uStack_190 = _UNK_1803478a8;
    local_1a8 = 0;
    FUN_1802161d0(local_188);
    local_1b0 = 0xffffffff;
    FUN_180217900(local_188,1);
    local_f8 = 0;
    local_e8[0] = param_2;
    FUN_1800622f0(local_e0,&local_1b8);
    plVar5 = DAT_180676f40;
    lVar4 = FUN_180061e90(DAT_180676f40,local_e8);
    FUN_180062160(plVar5,&local_1e0,0,lVar4 + 0x20,lVar4);
    FUN_180062460(local_e0);
    FUN_180062460(&local_1b8);
  }
  puVar1 = (undefined8 *)*DAT_180676f40;
  puVar6 = (undefined8 *)puVar1[1];
  puVar8 = puVar1;
  if (*(char *)((longlong)puVar6 + 0x19) == '\0') {
    do {
      if (*(int *)(puVar6 + 4) < param_2) {
        puVar7 = (undefined8 *)puVar6[2];
      }
      else {
        puVar7 = (undefined8 *)*puVar6;
        puVar8 = puVar6;
      }
      puVar6 = puVar7;
    } while (*(char *)((longlong)puVar7 + 0x19) == '\0');
    if ((puVar8 != puVar1) && (*(int *)(puVar8 + 4) <= param_2)) goto LAB_180062f34;
  }
  puVar8 = puVar1;
LAB_180062f34:
  pppppppuVar10 = &local_208;
  if (0xf < uStack_1f0) {
    pppppppuVar10 = local_208;
  }
  if (*(int *)(puVar8 + 0x1d) < 1) {
    *(int *)(puVar8 + 6) = param_2;
    FUN_1800524e0(puVar8 + 7,pppppppuVar10);
    FUN_180217e70(puVar8 + 0xb,pppppppuVar10,0);
    *(int *)(puVar8 + 0x1d) = *(int *)(puVar8 + 0x1d) + 1;
  }
  else {
    *(int *)(puVar8 + 0x1d) = *(int *)(puVar8 + 0x1d) + 1;
  }
  if (0xf < uStack_1f0) {
    if (0xfff < uStack_1f0 + 1) {
      if (0x1f < (ulonglong)((longlong)local_208 + (-8 - (longlong)local_208[-1]))) {
                    /* WARNING: Subroutine does not return */
        FUN_180303af0(local_208[-1],uStack_1f0 + 0x28);
      }
    }
    FUN_1802fdd80();
  }
  return;
}



