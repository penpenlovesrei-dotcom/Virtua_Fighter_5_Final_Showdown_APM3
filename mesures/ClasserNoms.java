import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.util.*;

public class ClasserNoms extends GhidraScript {
    @Override
    public void run() throws Exception {
        Program p = currentProgram;
        Map<String,Integer> cat = new TreeMap<String,Integer>();
        List<String> autres = new ArrayList<String>();
        FunctionIterator it = p.getListing().getFunctions(true);
        while (it.hasNext()) {
            Function f = it.next();
            if (f.isExternal()) continue;
            String nm = f.getName();
            if (nm.startsWith("FUN_") || nm.startsWith("thunk_FUN_")) continue;
            String k;
            if (nm.startsWith("Unwind@") || nm.startsWith("Catch@")
                || nm.startsWith("switchD") || nm.startsWith("caseD"))
                k = "bloc_exception_ou_switch";
            else if (nm.startsWith("_") || nm.startsWith("__")
                     || nm.startsWith("std::") || nm.contains("acrt")
                     || nm.startsWith("operator"))
                k = "bibliotheque_C_ou_CPP";
            else if (nm.startsWith("<lambda") || nm.contains("lambda_"))
                k = "lambda";
            else if (nm.startsWith("FID_conflict"))
                k = "FID_conflict";
            else { k = "AUTRE"; if (autres.size() < 60) autres.add(nm + " @" + f.getEntryPoint()); }
            Integer v = cat.get(k); cat.put(k, (v==null?0:v)+1);
        }
        println("CATEGORIES " + cat);
        for (String a : autres) println("  AUTRE " + a);
    }
}
