// ===================================================
// 1801A13CB  ->  FUN_1801a1190  (entree 1801a1190)
// ===================================================

void FUN_1801a1190(longlong param_1,longlong param_2)

{
  undefined8 *puVar1;
  int *piVar2;
  undefined8 uVar3;
  longlong lVar4;
  longlong lVar5;
  longlong *plVar6;
  longlong *plVar7;
  undefined4 *puVar8;
  int iVar9;
  longlong *plVar10;
  ulonglong uVar11;
  int local_res8;
  int local_resc;
  undefined1 local_60;
  undefined2 local_5f;
  undefined1 local_5d;
  int local_5c;
  int local_58;
  undefined8 local_50;
  undefined4 local_48;
  undefined4 uStack_44;
  undefined4 local_40;
  undefined **local_38;
  undefined4 local_30;
  
  if (*(char *)(param_1 + 0x58) == '\0') {
    return;
  }
  uVar3 = FUN_1801509b0();
  plVar10 = (longlong *)0x0;
  if ((param_2 != 0) && (lVar4 = FUN_180150990(uVar3,(int)*(char *)(param_2 + 0x44)), lVar4 != 0)) {
    lVar5 = FUN_18013a300(lVar4);
    switch(*(undefined4 *)(lVar5 + 0x88)) {
    case 1:
      iVar9 = 0;
      break;
    case 2:
    case 4:
      lVar4 = FUN_18013a300(lVar4);
      iVar9 = 4;
      if ((*(uint *)(lVar4 + 0xa0) >> 9 & 1) == 0) {
        iVar9 = 1;
      }
      break;
    case 3:
    case 5:
    case 0xd:
      iVar9 = 2;
      break;
    case 6:
      iVar9 = 5;
      break;
    case 7:
      iVar9 = 3;
      break;
    default:
      goto switchD_1801a122c_caseD_8;
    }
    local_38 = GameAuth2d::vftable;
    local_50 = 6;
    local_48 = 0;
    uStack_44 = 0;
    local_40 = 0;
    local_30 = 0;
    uVar11 = *(ulonglong *)(param_1 + 0x70);
    if (uVar11 <= *(longlong *)(param_1 + 0x80) + 1U) {
      FUN_18019cf30(param_1 + 0x60,1);
      uVar11 = *(ulonglong *)(param_1 + 0x70);
    }
    *(ulonglong *)(param_1 + 0x78) = *(ulonglong *)(param_1 + 0x78) & uVar11 - 1;
    uVar11 = *(longlong *)(param_1 + 0x70) - 1U &
             *(longlong *)(param_1 + 0x78) + *(longlong *)(param_1 + 0x80);
    lVar4 = *(longlong *)(param_1 + 0x68);
    if (*(longlong *)(lVar4 + uVar11 * 8) == 0) {
      uVar3 = FUN_180218930(0x28);
      *(undefined8 *)(*(longlong *)(param_1 + 0x68) + uVar11 * 8) = uVar3;
      lVar4 = *(longlong *)(param_1 + 0x68);
    }
    puVar8 = *(undefined4 **)(lVar4 + uVar11 * 8);
    *puVar8 = (undefined4)local_50;
    puVar8[1] = local_50._4_4_;
    *(ulonglong *)(puVar8 + 2) = CONCAT44(uStack_44,local_48);
    puVar8[4] = local_40;
    *(undefined ***)(puVar8 + 6) = GameAuth2d::vftable;
    puVar8[8] = local_30;
    *(longlong *)(param_1 + 0x80) = *(longlong *)(param_1 + 0x80) + 1;
    lVar4 = *(longlong *)(param_1 + 0x78);
    plVar6 = plVar10;
    if ((*(longlong **)(param_1 + 0x60) != (longlong *)0x0) &&
       (puVar1 = (undefined8 *)**(longlong **)(param_1 + 0x60), puVar1 != (undefined8 *)0x0)) {
      plVar6 = (longlong *)*puVar1;
    }
    plVar7 = plVar10;
    if (((plVar6 != (longlong *)0x0) && ((undefined8 *)*plVar6 != (undefined8 *)0x0)) &&
       (puVar1 = *(undefined8 **)*plVar6, puVar1 != (undefined8 *)0x0)) {
      plVar7 = (longlong *)*puVar1;
    }
    piVar2 = *(int **)(plVar7[1] + (plVar7[2] - 1U & *(longlong *)(param_1 + 0x80) + -1 + lVar4) * 8
                      );
    *piVar2 = iVar9;
    piVar2[1] = 0x46;
    FUN_180050e30(piVar2 + 2,param_2 + 0x34,CONCAT71((int7)((ulonglong)lVar4 >> 8),1));
    if (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) == 0) {
      FUN_18008a540(piVar2 + 6,0x2a0,(&PTR_s_hit_high_18040a9a6_2_180649678)[*piVar2],0x1b,0x20000,0
                    ,0);
      local_resc = piVar2[3];
      local_res8 = piVar2[2];
      puVar8 = (undefined4 *)FUN_18016b0c0();
      FUN_18016af60(&local_res8,9,&local_res8,*puVar8);
      piVar2[2] = local_res8;
      piVar2[3] = local_resc;
      FUN_18008a8b0(piVar2 + 6,piVar2 + 2);
    }
    else {
      local_resc = piVar2[3];
      local_res8 = piVar2[2];
      puVar8 = (undefined4 *)FUN_18016b0c0();
      FUN_18016af60(&local_res8,0xe,&local_res8,*puVar8);
      local_5f = 0;
      local_5d = 0;
      local_60 = (undefined1)iVar9;
      local_5c = local_res8;
      local_58 = local_resc;
      if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
        (**(code **)(DAT_180c3b6f0 + 0x1fe10))
                  (*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0x41,&local_60);
      }
    }
    FUN_18008a880(&local_38);
  }
switchD_1801a122c_caseD_8:
  if (0 < (int)*(undefined8 *)(param_1 + 0x80) + -6) {
    plVar6 = *(longlong **)(param_1 + 0x78);
    do {
      lVar4 = *(longlong *)
               (*(longlong *)(param_1 + 0x68) +
               (*(longlong *)(param_1 + 0x70) - 1U & (ulonglong)plVar6) * 8);
      FUN_18008a880(lVar4 + 0x18);
      *(undefined ***)(lVar4 + 0x18) = GameAuth2d::vftable;
      plVar6 = (longlong *)(param_1 + 0x80);
      *plVar6 = *plVar6 + -1;
      if (*plVar6 == 0) {
        *(undefined8 *)(param_1 + 0x78) = 0;
        plVar6 = plVar10;
      }
      else {
        *(longlong *)(param_1 + 0x78) = *(longlong *)(param_1 + 0x78) + 1;
        plVar6 = *(longlong **)(param_1 + 0x78);
      }
    } while (0 < *(int *)(param_1 + 0x80) + -6);
  }
  return;
}



