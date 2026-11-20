// Decompile les fonctions demandees et ecrit leur C dans un fichier.
//
// Ghidra headless ne sait pas decompiler tout seul : il analyse, et c'est un
// script qui appelle le decompileur. Celui-ci prend, en arguments :
//
//     <fichier de sortie> <adresse> [<adresse> ...]
//
// Chaque adresse est cherchee DANS sa fonction (getFunctionContaining), pas au
// debut : on cite souvent une instruction, pas une entree -- et sur ce binaire
// une entree `.pdata` n'est souvent qu'un FRAGMENT d'une fonction plus grande.
//
// @category VF5
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

import java.io.FileWriter;
import java.io.PrintWriter;

public class DecompVF5 extends GhidraScript {

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2) {
            println("usage : DecompVF5.java <sortie> <adresse> [...]");
            return;
        }
        DecompInterface deco = new DecompInterface();
        if (!deco.openProgram(currentProgram)) {
            println("le decompileur refuse le programme : " + deco.getLastMessage());
            return;
        }
        PrintWriter w = new PrintWriter(new FileWriter(args[0]));
        int ok = 0;
        for (int i = 1; i < args.length; i++) {
            Address a = currentProgram.getAddressFactory().getAddress(args[i]);
            if (a == null) {
                w.println("// " + args[i] + " : adresse illisible");
                continue;
            }
            Function f = getFunctionContaining(a);
            if (f == null) {
                f = createFunction(a, null);
            }
            if (f == null) {
                w.println("// " + args[i] + " : aucune fonction a cette adresse");
                continue;
            }
            w.println("// ===================================================");
            w.println("// " + args[i] + "  ->  " + f.getName()
                      + "  (entree " + f.getEntryPoint() + ")");
            w.println("// ===================================================");
            DecompileResults r = deco.decompileFunction(f, 180, monitor);
            if (r.decompileCompleted()) {
                w.println(r.getDecompiledFunction().getC());
                ok++;
            } else {
                w.println("// echec du decompileur : " + r.getErrorMessage());
            }
            w.println();
        }
        w.close();
        deco.dispose();
        println("DecompVF5 : " + ok + " fonction(s) ecrites dans " + args[0]);
    }
}
