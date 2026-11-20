// ===================================================
// 18006DB10  ->  FUN_18006db10  (entree 18006db10)
// ===================================================

undefined8 * FUN_18006db10(undefined8 *param_1)

{
  undefined8 *puVar1;

  FUN_180244c80();
  *param_1 = TaskEffectHit::vftable;
  _eh_vector_constructor_iterator_
            ((void *)((longlong)param_1 + 0x6c),4,2,(_func_void_void_ptr *)&LAB_18006db00,
             _guard_check_icall);
  param_1[0xf] = 0;
  *(undefined4 *)(param_1 + 0x10) = 0;
  param_1[0x12] = 0;
  *(undefined4 *)(param_1 + 0x13) = 0;
  puVar1 = param_1 + 0x15;
  FUN_180244c80(puVar1);
  *puVar1 = TaskEffectAuth3D::vftable;
  param_1[0x20] = 0;
  param_1[0x21] = 0;
  param_1[0x22] = 0;
  _eh_vector_constructor_iterator_
            (param_1 + 0x23,4,0x10,(_func_void_void_ptr *)&LAB_18006db00,_guard_check_icall);
  param_1[0x20] = 0;
  param_1[0x21] = 0x10;
  param_1[0x22] = param_1 + 0x23;
  FUN_180070640(puVar1);
  puVar1 = param_1 + 0x2e;
  FUN_180244c80(puVar1);
  *puVar1 = TaskEffectWall::vftable;
  _eh_vector_constructor_iterator_
            ((void *)((longlong)param_1 + 0x1cc),8,0x18,(_func_void_void_ptr *)&LAB_18006daf0,
             _guard_check_icall);
  _eh_vector_constructor_iterator_
            ((void *)((longlong)param_1 + 0x2a4),8,2,(_func_void_void_ptr *)&LAB_18006daf0,
             _guard_check_icall);
  _eh_vector_constructor_iterator_
            (param_1 + 0x58,0x30,4,(_func_void_void_ptr *)&LAB_18006d930,_guard_check_icall);
  FUN_180083d50(puVar1);
  FUN_180244c80(param_1 + 0x1db);
  param_1[0x1db] = TaskEffectLeaf::vftable;
  FUN_180244c80(param_1 + 0x1e9);
  param_1[0x1e9] = TaskEffectWata::vftable;
  FUN_180244c80(param_1 + 0x1f5);
  param_1[0x1f5] = TaskEffectSnow::vftable;
  puVar1 = param_1 + 0x201;
  FUN_180244c80(puVar1);
  *puVar1 = TaskEffectYuka::vftable;
  *(undefined4 *)((longlong)param_1 + 0x1064) = 0xffffffff;
  FUN_180086170(puVar1);
  FUN_180244c80(param_1 + 0x20e);
  param_1[0x20e] = TaskEffectRipple::vftable;
  FUN_180244c80(param_1 + 0x21b);
  param_1[0x21b] = TaskEffectRain::vftable;
  puVar1 = param_1 + 0x227;
  FUN_180244c80(puVar1);
  *puVar1 = TaskEffectThunder::vftable;
  _eh_vector_constructor_iterator_
            (param_1 + 0x232,4,7,(_func_void_void_ptr *)&LAB_18006db00,_guard_check_icall);
  FUN_180082590(puVar1);
  puVar1 = param_1 + 0x240;
  FUN_180244c80(puVar1);
  *puVar1 = TaskEffectDown::vftable;
  _eh_vector_constructor_iterator_
            ((void *)((longlong)param_1 + 0x125c),4,2,(_func_void_void_ptr *)&LAB_18006db00,
             _guard_check_icall);
  FUN_180071390(puVar1);
  puVar1 = param_1 + 0x24e;
  FUN_180244c80(puVar1);
  *puVar1 = TaskEffectMove::vftable;
  _eh_vector_constructor_iterator_
            ((void *)((longlong)param_1 + 0x12cc),4,2,(_func_void_void_ptr *)&LAB_18006db00,
             _guard_check_icall);
  FUN_180076ed0(puVar1);
  FUN_180244c80(param_1 + 0x25b);
  param_1[0x25b] = TaskEffectRingoutSplash::vftable;
  FUN_180079380(param_1 + 0x266);
  FUN_180244c80(param_1 + 0x268);
  param_1[0x268] = TaskEffectWaterRing::vftable;
  FUN_180244c80(param_1 + 0x275);
  param_1[0x275] = TaskEffectSplash::vftable;
  FUN_18007efe0(param_1 + 0x281);
  FUN_180244c80(param_1 + 0x2a3);
  param_1[0x2a3] = TaskEffectSnowRing::vftable;
  FUN_18007d300(param_1 + 0x2b0);
  FUN_180244c80(param_1 + 0x5ed);
  param_1[0x5ed] = TaskEffectFogAnim::vftable;
  FUN_180071650(param_1 + 0x5f8);
  puVar1 = param_1 + 0x601;
  FUN_180244c80(puVar1);
  *puVar1 = TaskEffectWetCloth::vftable;
  FUN_1800859f0(puVar1,0);
  *(undefined4 *)(param_1 + 0x60d) = 0xffffffff;
  *(undefined1 *)(param_1 + 0x60c) = 0;
  *(undefined4 *)((longlong)param_1 + 0x3064) = 0;
  FUN_180244c80(param_1 + 0x612);
  param_1[0x612] = TaskEffectFogRing::vftable;
  FUN_18006d950(param_1 + 0x61d);
  FUN_180244c80(param_1 + 0x676);
  param_1[0x676] = TaskEffectBreath::vftable;
  _eh_vector_constructor_iterator_
            ((void *)((longlong)param_1 + 0x341c),0x24,0xc,(_func_void_void_ptr *)&LAB_180070980,
             FUN_1800709b0);
  FUN_180244c80(param_1 + 0x6ba);
  param_1[0x6ba] = TaskEffectParticle::vftable;
  FUN_180244c80(param_1 + 0x6c7);
  param_1[0x6c7] = TaskEffectPoison::vftable;
  _eh_vector_constructor_iterator_
            (param_1 + 0x6d8,0x1c,0x10,(_func_void_void_ptr *)&LAB_180078130,FUN_180078150);
  FUN_180244c80(param_1 + 0x710);
  param_1[0x710] = TaskEffectEleBoard::vftable;
  _eh_vector_constructor_iterator_
            (param_1 + 0x71c,0x20,2,(_func_void_void_ptr *)&LAB_18006d910,FUN_18000de20);
  _eh_vector_constructor_iterator_
            (param_1 + 0x724,0x20,2,(_func_void_void_ptr *)&LAB_18006d910,FUN_18000de20);
  return param_1;
}

// ===================================================
// 18006EDC0  ->  FUN_18006edc0  (entree 18006edc0)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18006edc0(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  longlong lVar1;

  lVar1 = FUN_18027ca60(0x3978,0x10,param_3,param_4,0xfffffffffffffffe);
  if (lVar1 == 0) {
    DAT_180677260 = 0;
  }
  else {
    DAT_180677260 = FUN_18006db10(lVar1);
  }
  _DAT_180677270 = DAT_180677260;
  DAT_180677278 = DAT_180677260 + 0xa8;
  _DAT_180677280 = DAT_180677260 + 0x170;
  _DAT_180677288 = DAT_180677260 + 0xed8;
  _DAT_180677290 = DAT_180677260 + 0xf48;
  _DAT_180677298 = DAT_180677260 + 0xfa8;
  _DAT_1806772a0 = DAT_180677260 + 0x1008;
  _DAT_1806772a8 = DAT_180677260 + 0x1070;
  _DAT_1806772b0 = DAT_180677260 + 0x10d8;
  _DAT_1806772b8 = DAT_180677260 + 0x1138;
  _DAT_1806772c0 = DAT_180677260 + 0x1200;
  _DAT_1806772c8 = DAT_180677260 + 0x1270;
  _DAT_1806772d0 = DAT_180677260 + 0x12d8;
  _DAT_1806772d8 = DAT_180677260 + 0x1340;
  _DAT_1806772e0 = DAT_180677260 + 0x13a8;
  _DAT_1806772e8 = DAT_180677260 + 0x1518;
  _DAT_1806772f0 = DAT_180677260 + 0x2f68;
  _DAT_1806772f8 = DAT_180677260 + 0x3008;
  _DAT_180677300 = DAT_180677260 + 0x3090;
  _DAT_180677308 = DAT_180677260 + 0x33b0;
  _DAT_180677310 = DAT_180677260 + 0x35d0;
  _DAT_180677318 = DAT_180677260 + 0x3638;
  _DAT_180677320 = DAT_180677260 + 0x3880;
  return;
}

// ===================================================
// 18006EF40  ->  FUN_18006ef40  (entree 18006ef40)
// ===================================================

void FUN_18006ef40(void)

{
  longlong lVar1;

  lVar1 = DAT_180677260;
  DAT_180677260 = 0;
  if (lVar1 != 0) {
    FUN_18006e1e0(lVar1);
    FUN_18027cab0(lVar1);
  }
  FUN_1802ff420(&DAT_180677270,0,0xb8);
  return;
}

// ===================================================
// 18006FA70  ->  FUN_18006fa70  (entree 18006fa70)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_18006fa70(void)

{
  char cVar1;
  int iVar2;
  uint uVar3;
  int *piVar5;
  ulonglong uVar6;
  longlong *plVar7;
  ulonglong uVar4;

  uVar6 = 0;
  if (DAT_1806430b8 == 5) {
    if (0 < DAT_180642ff0) {
      plVar7 = &DAT_180643038;
      uVar4 = uVar6;
      iVar2 = DAT_180642ff0;
      do {
        if ((*plVar7 != 0) && (cVar1 = FUN_180244ea0(), iVar2 = DAT_180642ff0, cVar1 != '\0')) {
          return 1;
        }
        uVar3 = (int)uVar4 + 1;
        uVar4 = (ulonglong)uVar3;
        plVar7 = plVar7 + 1;
      } while ((int)uVar3 < iVar2);
    }
    FUN_18003c0f0("EFFEFFCMN");
    piVar5 = &DAT_18034d510;
    uVar4 = uVar6;
    do {
      if (*piVar5 == -1) break;
      FUN_1800f86c0();
      uVar3 = (int)uVar4 + 1;
      uVar4 = (ulonglong)uVar3;
      piVar5 = piVar5 + 1;
    } while ((int)uVar3 < 8);
    do {
      if (*(int *)(uVar6 + DAT_180642fe8) == -1) {
        _DAT_180642fe0 = 0xffffffff;
        DAT_180642fe8 = 0;
        DAT_180642ff0 = 0;
        _DAT_180642ff4 = 0xffffffffffffffff;
        _DAT_180642ffc = 0xffffffffffffffff;
        _DAT_180643004 = 0xffffffffffffffff;
        _DAT_18064300c = 0xffffffffffffffff;
        _DAT_180643014 = 0xffffffffffffffff;
        _DAT_18064301c = 0xffffffffffffffff;
        _DAT_180643024 = 0xffffffffffffffff;
        _DAT_18064302c = 0xffffffffffffffff;
        DAT_180643038 = 0;
        DAT_180643040 = 0;
        _DAT_180643048 = 0;
        _DAT_180643050 = 0;
        _DAT_180643058 = 0;
        _DAT_180643060 = 0;
        _DAT_180643068 = 0;
        _DAT_180643070 = 0;
        _DAT_180643078 = 0;
        _DAT_180643080 = 0;
        _DAT_180643088 = 0;
        _DAT_180643090 = 0;
        _DAT_180643098 = 0;
        _DAT_1806430a0 = 0;
        _DAT_1806430a8 = 0;
        _DAT_1806430b0 = 0;
        DAT_1806430b8 = 0;
        DAT_1806430bc = 1;
        return 0;
      }
      FUN_1800f86c0();
      uVar6 = uVar6 + 4;
    } while ((longlong)uVar6 < 0x20);
  }
  _DAT_180642fe0 = 0xffffffff;
  DAT_180642fe8 = 0;
  DAT_180642ff0 = 0;
  DAT_1806430bc = 1;
  _DAT_180642ff4 = 0xffffffffffffffff;
  DAT_180643038 = 0;
  DAT_180643040 = 0;
  _DAT_180642ffc = 0xffffffffffffffff;
  _DAT_180643048 = 0;
  _DAT_180643050 = 0;
  _DAT_180643004 = 0xffffffffffffffff;
  _DAT_180643058 = 0;
  _DAT_180643060 = 0;
  _DAT_18064300c = 0xffffffffffffffff;
  _DAT_180643068 = 0;
  _DAT_180643070 = 0;
  _DAT_180643014 = 0xffffffffffffffff;
  _DAT_180643078 = 0;
  _DAT_180643080 = 0;
  _DAT_18064301c = 0xffffffffffffffff;
  _DAT_180643088 = 0;
  _DAT_180643090 = 0;
  _DAT_180643024 = 0xffffffffffffffff;
  _DAT_180643098 = 0;
  _DAT_1806430a0 = 0;
  _DAT_18064302c = 0xffffffffffffffff;
  _DAT_1806430a8 = 0;
  _DAT_1806430b0 = 0;
  DAT_1806430b8 = 0;
  return 0;
}
