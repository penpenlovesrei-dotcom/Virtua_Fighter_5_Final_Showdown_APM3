// ===================================================
// 18016B026  ->  FUN_18016af60  (entree 18016af60)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18016af60(float *param_1,int param_2,float *param_3,int param_4)

{
  float fVar1;
  float fVar2;
  longlong lVar3;
  longlong lVar4;
  longlong lVar5;
  
  fVar2 = DAT_180346d38;
  lVar3 = (longlong)param_2;
  lVar5 = (longlong)param_4;
  lVar4 = lVar3 * 0x11 + lVar5;
  fVar1 = (param_3[1] - DAT_180346d38 * (float)(&DAT_1803feb24)[lVar5 * 7]) *
          *(float *)((longlong)&DAT_180714010 + lVar4 * 8 + 4) +
          DAT_180346d38 * (float)(&DAT_1803feb24)[lVar3 * 7];
  *param_1 = (*param_3 - DAT_180346d38 * (float)(&DAT_1803feb20)[lVar5 * 7]) *
             *(float *)(&DAT_180714010 + lVar4) + DAT_180346d38 * (float)(&DAT_1803feb20)[lVar3 * 7]
  ;
  param_1[1] = fVar1;
  if ((param_4 == 9) || (param_4 == 3)) {
    if (param_2 == 0xd) {
      param_1[1] = fVar1 - ((float)(&DAT_1803feb24)[lVar5 * 7] - _UNK_1803fec90) * fVar2;
      return;
    }
    if (param_2 == 0xe) {
      param_1[1] = fVar1 - ((float)(&DAT_1803feb24)[lVar5 * 7] - DAT_1803fed00) * DAT_18034b0c8;
      return;
    }
    if (param_2 == 0xf) {
      param_1[1] = fVar1 - ((float)(&DAT_1803feb24)[lVar5 * 7] - DAT_1803fed00);
      return;
    }
    if (param_2 == 0x10) {
      param_1[1] = fVar1 - ((float)(&DAT_1803feb24)[lVar5 * 7] - DAT_1803fed00) * DAT_18034b408;
    }
  }
  return;
}



// ===================================================
// 18016B17E  ->  FUN_18016b0d0  (entree 18016b0d0)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18016b0d0(uint param_1)

{
  float *pfVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  char cVar5;
  undefined1 auVar6 [16];
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  byte bVar13;
  uint uVar14;
  float *pfVar15;
  float *pfVar16;
  uint uVar17;
  uint uVar18;
  longlong lVar19;
  char *pcVar20;
  float fVar21;
  uint uStack_6c;
  int iStack_68;
  undefined4 uStack_64;
  double dStack_60;
  undefined7 uStack_57;
  
  fVar12 = DAT_1803fed08;
  fVar11 = DAT_1803fed04;
  fVar10 = DAT_18034b408;
  fVar9 = DAT_18034a51c;
  fVar8 = DAT_1803480b8;
  fVar7 = DAT_180346d3c;
  lVar19 = (longlong)(int)param_1;
  if (param_1 == 0x11) {
    uStack_6c = DAT_1806490dc;
    iStack_68 = DAT_1806490e0;
    dStack_60 = DAT_1806490e8;
  }
  else {
    uStack_6c = (uint)(float)(&DAT_1803feb20)[lVar19 * 7];
    iStack_68 = (int)(float)(&DAT_1803feb24)[lVar19 * 7];
    dStack_60 = (double)(int)uStack_6c / (double)iStack_68;
    DAT_1806490f0 = (&DAT_1803feb28)[lVar19 * 0x1c];
  }
  _DAT_1806490d0 = (ulonglong)param_1;
  lRam00000001806490d8 = (ulonglong)uStack_6c << 0x20;
  _DAT_1806490e0 = CONCAT44(uStack_64,iStack_68);
  lVar19 = lVar19 * 0x1c;
  pfVar16 = (float *)((longlong)&DAT_180714010 + 4);
  _DAT_1806490f0 = CONCAT71(uStack_57,DAT_1806490f0);
  DAT_1806490e8 = dStack_60;
  _DAT_1806490fc = *(undefined4 *)(&DAT_1803feb2c + lVar19);
  pcVar20 = "";
  uVar18 = 0;
  _DAT_180649100 = *(undefined4 *)(&DAT_1803feb30 + lVar19);
  _DAT_180649108 = *(int *)(&DAT_1803feb38 + lVar19);
  _DAT_180649104 = *(int *)(&DAT_1803feb34 + lVar19);
  _DAT_180649110 = (double)_DAT_180649104 / (double)_DAT_180649108;
  DAT_180649118 = (&DAT_1803feb28)[lVar19];
  _DAT_180649120 = ZEXT416(0) << 0x40;
  _DAT_1806490f8 = param_1;
  do {
    uVar17 = 0;
    pfVar15 = pfVar16;
    do {
      pfVar1 = pfVar15 + -1;
      if (pfVar1 != (float *)0x0) {
        *pfVar1 = 1.0;
        *pfVar15 = 1.0;
        if (((uVar18 != 0x11) && (uVar17 != 0x11)) && (uVar18 != uVar17)) {
          fVar2 = *(float *)(pcVar20 + -8);
          fVar3 = *(float *)(pcVar20 + -4);
          lVar19 = (longlong)(int)uVar17;
          cVar5 = *pcVar20;
          fVar4 = (float)(&DAT_1803feb20)[lVar19 * 7];
          fVar21 = fVar3 / (float)(&DAT_1803feb24)[lVar19 * 7];
          *pfVar15 = fVar21;
          *pfVar1 = fVar2 / fVar4;
          if ((&DAT_1803feb28)[lVar19 * 0x1c] == cVar5) {
            if ((uVar17 == 10) || (uVar17 - 0xd < 4)) {
              uVar14 = 1;
            }
            else {
              uVar14 = 0;
            }
            if ((uVar18 == 10) || (uVar18 - 0xd < 4)) {
              bVar13 = 1;
            }
            else {
              bVar13 = 0;
            }
            auVar6 = vpcmpeqd_avx(ZEXT416(uVar14),ZEXT116(bVar13));
            auVar6 = vblendvps_avx(ZEXT416((uint)(fVar2 / fVar4)),ZEXT416((uint)*pfVar15),auVar6);
            *pfVar15 = auVar6._0_4_;
          }
          else if (uVar17 == 3) {
            if (uVar18 == 0xd) {
              *pfVar1 = fVar7;
              *pfVar15 = 1.0;
            }
            else if (uVar18 == 0xe) {
              *pfVar1 = fVar10;
              *pfVar15 = 1.5;
            }
            else {
              if (uVar18 != 0xf) {
                if (uVar18 == 0x10) {
                  *pfVar15 = 3.0;
                  fVar21 = fVar8;
                }
                goto LAB_18016b340;
              }
              *pfVar1 = fVar9;
              *pfVar15 = 2.0;
            }
          }
          else if (uVar17 == 0xd) {
            *pfVar15 = fVar3 / fVar11;
            *pfVar1 = fVar3 / fVar11;
          }
          else if (uVar17 == 0xe) {
            *pfVar15 = fVar3 / fVar12;
            *pfVar1 = fVar3 / fVar12;
          }
          else {
LAB_18016b340:
            *pfVar1 = fVar21;
          }
        }
      }
      uVar17 = uVar17 + 1;
      pfVar15 = pfVar15 + 2;
    } while (uVar17 < 0x11);
    uVar18 = uVar18 + 1;
    pfVar16 = pfVar16 + 0x22;
    pcVar20 = pcVar20 + 0x1c;
    if (0x10 < uVar18) {
      return;
    }
  } while( true );
}



