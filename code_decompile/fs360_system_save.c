// ===================================================
// 823A35E4  ->  FUN_823a35c8  (entree 823a35c8)
// ===================================================

/* WARNING: Function: __savegprlr_26 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_26 replaced with injection: x360_restgprlr */

void FUN_823a35c8(undefined8 param_1,undefined4 param_2,int param_3,char param_4,undefined4 param_5)

{
  DAT_82e916a0 = param_3 + 0x10;
  DAT_82e9169c = 0;
  FUN_82301988(0xffffffff82e916a4,0xffffffff820db1cc,0x20);
  DAT_82e916d0 = 1;
  DAT_82e916cc = 0x20120313;
  DAT_82e91800 = DAT_82e916a0;
  DAT_82e916c4 = param_2;
  DAT_82e916c8 = param_3;
  FUN_82301988(0xffffffff82e916d4,0xffffffff820db1c4,0x2a);
  FUN_823122e8(0xffffffff82e916fe,0xffffffff820db1b8,0x80);
  if (param_4 != '\0') {
    FUN_823a31e8();
    DAT_82e91690 = param_5;
    return;
  }
  FUN_823a32e8(0xffffffff82e908e0,param_1,0xffffffff820db1a4);
  DAT_82e91690 = param_5;
  return;
}



// ===================================================
// 823A5D74  ->  FUN_823a5d58  (entree 823a5d58)
// ===================================================

/* WARNING: Function: __savegprlr_25 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_25 replaced with injection: x360_restgprlr */

void FUN_823a5d58(undefined8 param_1,undefined4 param_2,int param_3,undefined8 param_4,char param_5,
                 undefined4 param_6)

{
  DAT_82e916a0 = param_3 + 0x10;
  DAT_82e9169c = 0;
  FUN_82301988(0xffffffff82e916a4,0xffffffff820db1cc,0x20);
  DAT_82e916d0 = 1;
  DAT_82e916cc = 0x20120313;
  DAT_82e91800 = DAT_82e916a0;
  DAT_82e916c4 = param_2;
  DAT_82e916c8 = param_3;
  FUN_82301988(0xffffffff82e916d4,0xffffffff820db1c4,0x2a);
  FUN_823122e8(0xffffffff82e916fe,0xffffffff820db1b8,0x80);
  if (param_5 == '\0') {
    FUN_823a3368(0xffffffff82e908e0,param_1,0xffffffff820db1a4,param_4);
  }
  else {
    FUN_823a3268();
  }
  DAT_82e91690 = param_6;
  DAT_82e91694 = FUN_823a5698;
  return;
}



