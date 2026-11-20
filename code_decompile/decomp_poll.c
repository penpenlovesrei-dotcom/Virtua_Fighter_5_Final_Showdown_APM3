// ===================================================
// 1800fbc30  ->  FUN_1800fbc30  (entree 1800fbc30)
// ===================================================

undefined1 FUN_1800fbc30(undefined4 param_1,byte *param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  char cVar3;
  byte bVar4;
  longlong lVar5;
  
  lVar5 = FUN_1800f9450();
  if (lVar5 == 0) {
    return 0;
  }
  cVar3 = FUN_180217bf0(lVar5);
  if ((cVar3 == '\0') && (cVar3 = FUN_180217bf0(lVar5 + 0x98), cVar3 == '\0')) {
    if ((*(char *)(lVar5 + 500) != '\0') && (*(int *)(lVar5 + 0x1f0) < 1)) {
      uVar1 = FUN_1800f91b0(param_1,0);
      uVar2 = FUN_1800f91b0(param_1,1);
      bVar4 = FUN_1801b6eb0(uVar1);
      *param_2 = bVar4;
      bVar4 = FUN_1801b6eb0(uVar2);
      *param_2 = *param_2 & bVar4;
      return 0;
    }
    *param_2 = 1;
    return 0;
  }
  return 1;
}



// ===================================================
// 1800fbb4d  ->  FUN_1800fb7e0  (entree 1800fb7e0)
// ===================================================

undefined8 FUN_1800fb7e0(undefined8 param_1,char param_2)

{
  int iVar1;
  undefined8 *puVar2;
  char cVar3;
  longlong lVar4;
  longlong lVar5;
  undefined8 uVar6;
  longlong lVar7;
  ulonglong uVar8;
  longlong lVar9;
  ulonglong uVar10;
  ulonglong uVar11;
  int *piVar12;
  uint uVar13;
  int *piVar15;
  int iVar16;
  longlong lVar17;
  ulonglong uVar18;
  int local_res18;
  int iStackX_1c;
  ulonglong uVar14;
  
  uVar6 = 1;
  lVar4 = FUN_1800f9450();
  if (lVar4 == 0) {
    return 0;
  }
  uVar18 = 0;
  if ((*(char *)(lVar4 + 0x90) == '\0') && (cVar3 = FUN_180217bf0(lVar4), cVar3 == '\0')) {
    lVar5 = FUN_180217940(lVar4);
    if (lVar5 == 0) {
      uVar6 = 0;
    }
    else {
      uVar14 = lVar4 + 0x130;
      if (*(char *)(lVar4 + 0x138) == '\0') {
        uVar14 = uVar18;
      }
      *(longlong *)(lVar4 + 0x130) = lVar5;
      uVar6 = FUN_180217be0(lVar4);
      cVar3 = FUN_1800fa2e0(uVar14,lVar5,uVar6);
      if (cVar3 != '\0') {
        piVar15 = *(int **)(lVar4 + 0x130);
        if (*piVar15 == 0x5062500) {
          iVar1 = piVar15[1];
          if (0 < iVar1) {
            uVar14 = uVar18;
            do {
              iVar16 = piVar15[6];
              uVar10 = uVar18;
              if (iVar16 != 0) {
                uVar10 = (longlong)(piVar15 + 6) + (longlong)iVar16;
              }
              puVar2 = *(undefined8 **)(lVar4 + 0x160);
              iVar16 = (int)uVar14;
              local_res18 = *(int *)(uVar10 + (longlong)iVar16 * 4);
              iStackX_1c = iVar16;
              if (*(undefined8 **)(lVar4 + 0x168) == puVar2) {
                FUN_1800d4210(lVar4 + 0x158,puVar2,&local_res18);
              }
              else {
                *puVar2 = CONCAT44(iVar16,local_res18);
                *(longlong *)(lVar4 + 0x160) = *(longlong *)(lVar4 + 0x160) + 8;
              }
              uVar14 = (ulonglong)(iVar16 + 1U);
            } while ((int)(iVar16 + 1U) < iVar1);
          }
          FUN_18001fa10(*(longlong *)(lVar4 + 0x158),*(longlong *)(lVar4 + 0x160),
                        *(longlong *)(lVar4 + 0x160) - *(longlong *)(lVar4 + 0x158) >> 3,0);
          piVar15 = *(int **)(lVar4 + 0x130);
        }
        iVar1 = piVar15[1];
        *(int *)(lVar4 + 0x1c4) = iVar1;
        lVar5 = FUN_180218410(0,(longlong)iVar1 << 4,"OBJVB",0);
        *(longlong *)(lVar4 + 0x1c8) = lVar5;
        if (lVar5 != 0) {
          FUN_1802ff420(lVar5,0,(longlong)*(int *)(lVar4 + 0x1c4) << 4);
          if (0 < *(int *)(lVar4 + 0x1c4)) {
            uVar14 = uVar18;
            uVar10 = uVar18;
            do {
              iVar1 = piVar15[3];
              uVar8 = uVar18;
              if (iVar1 != 0) {
                uVar8 = (longlong)(piVar15 + 3) + (longlong)iVar1;
              }
              iVar1 = *(int *)(uVar10 + uVar8);
              uVar11 = uVar18;
              if (iVar1 != 0) {
                uVar11 = (longlong)(uVar10 + uVar8) + (longlong)iVar1;
              }
              cVar3 = FUN_1800f83e0((longlong)(int)uVar14 * 0x10 + *(longlong *)(lVar4 + 0x1c8),
                                    uVar11,0);
              if (cVar3 == '\0') goto LAB_1800fbb45;
              uVar13 = (int)uVar14 + 1;
              uVar14 = (ulonglong)uVar13;
              uVar10 = uVar10 + 4;
            } while ((int)uVar13 < *(int *)(lVar4 + 0x1c4));
          }
          lVar5 = *(longlong *)(lVar4 + 0x130);
          iVar1 = *(int *)(lVar5 + 4);
          *(int *)(lVar4 + 0x1d0) = iVar1;
          lVar7 = FUN_180218410(0,(longlong)iVar1 << 4,"OBJIB",0);
          *(longlong *)(lVar4 + 0x1d8) = lVar7;
          if (lVar7 != 0) {
            FUN_1802ff420(lVar7,0,(longlong)*(int *)(lVar4 + 0x1d0) << 4);
            if (0 < *(int *)(lVar4 + 0x1d0)) {
              piVar15 = (int *)(lVar5 + 0xc);
              uVar14 = uVar18;
              uVar10 = uVar18;
              do {
                iVar1 = *piVar15;
                uVar8 = uVar18;
                if (iVar1 != 0) {
                  uVar8 = (longlong)piVar15 + (longlong)iVar1;
                }
                iVar1 = *(int *)(uVar10 + uVar8);
                uVar11 = uVar18;
                if (iVar1 != 0) {
                  uVar11 = (longlong)(uVar10 + uVar8) + (longlong)iVar1;
                }
                cVar3 = FUN_1800f8200((longlong)(int)uVar14 * 0x10 + *(longlong *)(lVar4 + 0x1d8),
                                      uVar11,0);
                if (cVar3 == '\0') goto LAB_1800fbb45;
                uVar13 = (int)uVar14 + 1;
                uVar14 = (ulonglong)uVar13;
                uVar10 = uVar10 + 4;
              } while ((int)uVar13 < *(int *)(lVar4 + 0x1d0));
            }
            lVar5 = *(longlong *)(lVar4 + 0x130);
            if (0 < *(int *)(lVar5 + 4)) {
              lVar7 = 0;
              do {
                iVar1 = *(int *)(lVar5 + 0xc);
                lVar9 = 0;
                if (iVar1 != 0) {
                  lVar9 = lVar5 + 0xc + (longlong)iVar1;
                }
                lVar17 = 0;
                iVar1 = *(int *)(lVar7 + lVar9);
                if (iVar1 != 0) {
                  lVar17 = lVar7 + lVar9 + (longlong)iVar1;
                }
                uVar14 = 0;
                if (*(int *)(lVar17 + 0x18) != 0) {
                  do {
                    iVar1 = *(int *)(lVar17 + 0x1c);
                    lVar9 = 0;
                    if (iVar1 != 0) {
                      lVar9 = lVar17 + 0x1c + (longlong)iVar1;
                    }
                    FUN_1800f7a10(lVar9 + uVar14 * 0xd8);
                    uVar13 = (int)uVar14 + 1;
                    uVar14 = (ulonglong)uVar13;
                  } while (uVar13 < *(uint *)(lVar17 + 0x18));
                }
                uVar13 = (int)uVar18 + 1;
                uVar18 = (ulonglong)uVar13;
                lVar7 = lVar7 + 4;
              } while ((int)uVar13 < *(int *)(lVar5 + 4));
            }
            if ((*(char *)(lVar4 + 0x138) != '\0') && (param_2 != '\0')) {
              FUN_180217900(lVar4,1);
            }
            FUN_180218120(lVar4 + 0x98,3);
            *(undefined1 *)(lVar4 + 0x90) = 1;
            uVar6 = 1;
            goto LAB_1800fbb4d;
          }
        }
      }
LAB_1800fbb45:
      uVar6 = 0;
    }
  }
LAB_1800fbb4d:
  if (((*(char *)(lVar4 + 0x90) != '\0') && (*(char *)(lVar4 + 0x128) == '\0')) &&
     (cVar3 = FUN_180217bf0(lVar4 + 0x98), cVar3 == '\0')) {
    cVar3 = FUN_1800f9890(lVar4);
    if (cVar3 == '\x01') {
      uVar6 = 0;
    }
    else {
      lVar5 = *(longlong *)(lVar4 + 0x130);
      if (lVar5 != 0) {
        uVar18 = (ulonglong)*(uint *)(lVar5 + 4);
        piVar15 = (int *)0x0;
        if (*(int *)(lVar5 + 0xc) != 0) {
          piVar15 = (int *)(lVar5 + 0xc + (longlong)*(int *)(lVar5 + 0xc));
        }
        if (0 < (int)*(uint *)(lVar5 + 4)) {
          do {
            piVar12 = (int *)0x0;
            if (*piVar15 != 0) {
              piVar12 = (int *)((longlong)piVar15 + (longlong)*piVar15);
            }
            FUN_1800f7760(lVar4,piVar12);
            piVar15 = piVar15 + 1;
            uVar18 = uVar18 - 1;
          } while (uVar18 != 0);
        }
      }
      FUN_180217900(lVar4 + 0x98,1);
      *(undefined1 *)(lVar4 + 0x128) = 1;
    }
  }
  if (*(char *)(lVar4 + 0x90) == '\0') {
    return uVar6;
  }
  if (*(char *)(lVar4 + 0x128) != '\0') {
    uVar6 = 0;
  }
  return uVar6;
}



// ===================================================
// 1800fb80b  ->  FUN_1800fb7e0  (entree 1800fb7e0)
// ===================================================

undefined8 FUN_1800fb7e0(undefined8 param_1,char param_2)

{
  int iVar1;
  undefined8 *puVar2;
  char cVar3;
  longlong lVar4;
  longlong lVar5;
  undefined8 uVar6;
  longlong lVar7;
  ulonglong uVar8;
  longlong lVar9;
  ulonglong uVar10;
  ulonglong uVar11;
  int *piVar12;
  uint uVar13;
  int *piVar15;
  int iVar16;
  longlong lVar17;
  ulonglong uVar18;
  int local_res18;
  int iStackX_1c;
  ulonglong uVar14;
  
  uVar6 = 1;
  lVar4 = FUN_1800f9450();
  if (lVar4 == 0) {
    return 0;
  }
  uVar18 = 0;
  if ((*(char *)(lVar4 + 0x90) == '\0') && (cVar3 = FUN_180217bf0(lVar4), cVar3 == '\0')) {
    lVar5 = FUN_180217940(lVar4);
    if (lVar5 == 0) {
      uVar6 = 0;
    }
    else {
      uVar14 = lVar4 + 0x130;
      if (*(char *)(lVar4 + 0x138) == '\0') {
        uVar14 = uVar18;
      }
      *(longlong *)(lVar4 + 0x130) = lVar5;
      uVar6 = FUN_180217be0(lVar4);
      cVar3 = FUN_1800fa2e0(uVar14,lVar5,uVar6);
      if (cVar3 != '\0') {
        piVar15 = *(int **)(lVar4 + 0x130);
        if (*piVar15 == 0x5062500) {
          iVar1 = piVar15[1];
          if (0 < iVar1) {
            uVar14 = uVar18;
            do {
              iVar16 = piVar15[6];
              uVar10 = uVar18;
              if (iVar16 != 0) {
                uVar10 = (longlong)(piVar15 + 6) + (longlong)iVar16;
              }
              puVar2 = *(undefined8 **)(lVar4 + 0x160);
              iVar16 = (int)uVar14;
              local_res18 = *(int *)(uVar10 + (longlong)iVar16 * 4);
              iStackX_1c = iVar16;
              if (*(undefined8 **)(lVar4 + 0x168) == puVar2) {
                FUN_1800d4210(lVar4 + 0x158,puVar2,&local_res18);
              }
              else {
                *puVar2 = CONCAT44(iVar16,local_res18);
                *(longlong *)(lVar4 + 0x160) = *(longlong *)(lVar4 + 0x160) + 8;
              }
              uVar14 = (ulonglong)(iVar16 + 1U);
            } while ((int)(iVar16 + 1U) < iVar1);
          }
          FUN_18001fa10(*(longlong *)(lVar4 + 0x158),*(longlong *)(lVar4 + 0x160),
                        *(longlong *)(lVar4 + 0x160) - *(longlong *)(lVar4 + 0x158) >> 3,0);
          piVar15 = *(int **)(lVar4 + 0x130);
        }
        iVar1 = piVar15[1];
        *(int *)(lVar4 + 0x1c4) = iVar1;
        lVar5 = FUN_180218410(0,(longlong)iVar1 << 4,"OBJVB",0);
        *(longlong *)(lVar4 + 0x1c8) = lVar5;
        if (lVar5 != 0) {
          FUN_1802ff420(lVar5,0,(longlong)*(int *)(lVar4 + 0x1c4) << 4);
          if (0 < *(int *)(lVar4 + 0x1c4)) {
            uVar14 = uVar18;
            uVar10 = uVar18;
            do {
              iVar1 = piVar15[3];
              uVar8 = uVar18;
              if (iVar1 != 0) {
                uVar8 = (longlong)(piVar15 + 3) + (longlong)iVar1;
              }
              iVar1 = *(int *)(uVar10 + uVar8);
              uVar11 = uVar18;
              if (iVar1 != 0) {
                uVar11 = (longlong)(uVar10 + uVar8) + (longlong)iVar1;
              }
              cVar3 = FUN_1800f83e0((longlong)(int)uVar14 * 0x10 + *(longlong *)(lVar4 + 0x1c8),
                                    uVar11,0);
              if (cVar3 == '\0') goto LAB_1800fbb45;
              uVar13 = (int)uVar14 + 1;
              uVar14 = (ulonglong)uVar13;
              uVar10 = uVar10 + 4;
            } while ((int)uVar13 < *(int *)(lVar4 + 0x1c4));
          }
          lVar5 = *(longlong *)(lVar4 + 0x130);
          iVar1 = *(int *)(lVar5 + 4);
          *(int *)(lVar4 + 0x1d0) = iVar1;
          lVar7 = FUN_180218410(0,(longlong)iVar1 << 4,"OBJIB",0);
          *(longlong *)(lVar4 + 0x1d8) = lVar7;
          if (lVar7 != 0) {
            FUN_1802ff420(lVar7,0,(longlong)*(int *)(lVar4 + 0x1d0) << 4);
            if (0 < *(int *)(lVar4 + 0x1d0)) {
              piVar15 = (int *)(lVar5 + 0xc);
              uVar14 = uVar18;
              uVar10 = uVar18;
              do {
                iVar1 = *piVar15;
                uVar8 = uVar18;
                if (iVar1 != 0) {
                  uVar8 = (longlong)piVar15 + (longlong)iVar1;
                }
                iVar1 = *(int *)(uVar10 + uVar8);
                uVar11 = uVar18;
                if (iVar1 != 0) {
                  uVar11 = (longlong)(uVar10 + uVar8) + (longlong)iVar1;
                }
                cVar3 = FUN_1800f8200((longlong)(int)uVar14 * 0x10 + *(longlong *)(lVar4 + 0x1d8),
                                      uVar11,0);
                if (cVar3 == '\0') goto LAB_1800fbb45;
                uVar13 = (int)uVar14 + 1;
                uVar14 = (ulonglong)uVar13;
                uVar10 = uVar10 + 4;
              } while ((int)uVar13 < *(int *)(lVar4 + 0x1d0));
            }
            lVar5 = *(longlong *)(lVar4 + 0x130);
            if (0 < *(int *)(lVar5 + 4)) {
              lVar7 = 0;
              do {
                iVar1 = *(int *)(lVar5 + 0xc);
                lVar9 = 0;
                if (iVar1 != 0) {
                  lVar9 = lVar5 + 0xc + (longlong)iVar1;
                }
                lVar17 = 0;
                iVar1 = *(int *)(lVar7 + lVar9);
                if (iVar1 != 0) {
                  lVar17 = lVar7 + lVar9 + (longlong)iVar1;
                }
                uVar14 = 0;
                if (*(int *)(lVar17 + 0x18) != 0) {
                  do {
                    iVar1 = *(int *)(lVar17 + 0x1c);
                    lVar9 = 0;
                    if (iVar1 != 0) {
                      lVar9 = lVar17 + 0x1c + (longlong)iVar1;
                    }
                    FUN_1800f7a10(lVar9 + uVar14 * 0xd8);
                    uVar13 = (int)uVar14 + 1;
                    uVar14 = (ulonglong)uVar13;
                  } while (uVar13 < *(uint *)(lVar17 + 0x18));
                }
                uVar13 = (int)uVar18 + 1;
                uVar18 = (ulonglong)uVar13;
                lVar7 = lVar7 + 4;
              } while ((int)uVar13 < *(int *)(lVar5 + 4));
            }
            if ((*(char *)(lVar4 + 0x138) != '\0') && (param_2 != '\0')) {
              FUN_180217900(lVar4,1);
            }
            FUN_180218120(lVar4 + 0x98,3);
            *(undefined1 *)(lVar4 + 0x90) = 1;
            uVar6 = 1;
            goto LAB_1800fbb4d;
          }
        }
      }
LAB_1800fbb45:
      uVar6 = 0;
    }
  }
LAB_1800fbb4d:
  if (((*(char *)(lVar4 + 0x90) != '\0') && (*(char *)(lVar4 + 0x128) == '\0')) &&
     (cVar3 = FUN_180217bf0(lVar4 + 0x98), cVar3 == '\0')) {
    cVar3 = FUN_1800f9890(lVar4);
    if (cVar3 == '\x01') {
      uVar6 = 0;
    }
    else {
      lVar5 = *(longlong *)(lVar4 + 0x130);
      if (lVar5 != 0) {
        uVar18 = (ulonglong)*(uint *)(lVar5 + 4);
        piVar15 = (int *)0x0;
        if (*(int *)(lVar5 + 0xc) != 0) {
          piVar15 = (int *)(lVar5 + 0xc + (longlong)*(int *)(lVar5 + 0xc));
        }
        if (0 < (int)*(uint *)(lVar5 + 4)) {
          do {
            piVar12 = (int *)0x0;
            if (*piVar15 != 0) {
              piVar12 = (int *)((longlong)piVar15 + (longlong)*piVar15);
            }
            FUN_1800f7760(lVar4,piVar12);
            piVar15 = piVar15 + 1;
            uVar18 = uVar18 - 1;
          } while (uVar18 != 0);
        }
      }
      FUN_180217900(lVar4 + 0x98,1);
      *(undefined1 *)(lVar4 + 0x128) = 1;
    }
  }
  if (*(char *)(lVar4 + 0x90) == '\0') {
    return uVar6;
  }
  if (*(char *)(lVar4 + 0x128) != '\0') {
    uVar6 = 0;
  }
  return uVar6;
}



