// Neutralise les routines de sauvegarde / restauration des registres du
// compilateur Xbox 360, pour que le decompileur lise les fonctions.
//
// Chaque fonction du jeu commence par `mflr r12 ; bl __savegprlr_N` et finit
// par `b __restgprlr_N`. Ces routines sont UNE suite de `std rN` (resp.
// `ld rN`) ou l'on entre a la ligne du premier registre a sauver : 16 entrees
// de sauvegarde (0x825FFA10..0x825FFA4C, fin `stw r12,-8(r1) ; blr`) et 16 de
// restauration (0x825FFA60..0x825FFA9C, fin `mtlr r12 ; blr`). Ghidra en
// faisait des fonctions qui ne reviennent pas : tout ce qui suivait
// l'appel etait perdu (« Subroutine does not return »).
//
// Remede SANS toucher a l'installation de Ghidra : un « call fixup » ajoute
// au PROGRAMME (SpecExtension), au corps neutre, pose sur 32 fonctions d'une
// instruction chacune.
//
//     SauvegardesX360.java <debut sauve> <fin sauve> <debut rest> <fin rest>
//
// @category VF5
import ghidra.app.script.GhidraScript;
import ghidra.program.database.SpecExtension;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSet;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;

public class SauvegardesX360 extends GhidraScript {

    private static final String FIXUP =
        "<callfixup name=\"%s\">\n" +
        "  <pcode>\n" +
        "    <body><![CDATA[\n" +
        "      r12 = r12;\n" +
        "    ]]></body>\n" +
        "  </pcode>\n" +
        "</callfixup>\n";

    private int poser(long debut, long fin, String prefixe, String fixup)
            throws Exception {
        int n = 0;
        for (long a = debut; a <= fin; a += 4) {
            Address e = toAddr(a);
            Function f = getFunctionContaining(e);
            if (f != null) {
                removeFunction(f);
            }
            Function g = getFunctionAt(e);
            if (g != null) {
                removeFunction(g);
            }
        }
        for (long a = debut; a <= fin; a += 4) {
            Address e = toAddr(a);
            disassemble(e);
            int r = 14 + (int) ((a - debut) / 4);
            Function f = currentProgram.getFunctionManager().createFunction(
                prefixe + r, e, new AddressSet(e, e.add(3)),
                SourceType.USER_DEFINED);
            f.setNoReturn(false);
            f.setCallFixup(fixup);
            n++;
        }
        return n;
    }

    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        SpecExtension ext = new SpecExtension(currentProgram);
        ext.addReplaceCompilerSpecExtension(
            String.format(FIXUP, "x360_savegprlr"), monitor);
        ext.addReplaceCompilerSpecExtension(
            String.format(FIXUP, "x360_restgprlr"), monitor);
        int s = poser(Long.decode(a[0]), Long.decode(a[1]), "__savegprlr_",
                      "x360_savegprlr");
        int r = poser(Long.decode(a[2]), Long.decode(a[3]), "__restgprlr_",
                      "x360_restgprlr");
        println("SauvegardesX360 : " + s + " sauvegardes, " + r
                + " restaurations neutralisees");
    }
}
