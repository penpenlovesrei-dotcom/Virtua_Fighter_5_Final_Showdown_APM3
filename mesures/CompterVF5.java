import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.address.*;
import ghidra.program.model.data.*;
import java.util.*;

public class CompterVF5 extends GhidraScript {
    @Override
    public void run() throws Exception {
        Program p = currentProgram;
        Listing l = p.getListing();
        int tot = 0, thunk = 0, cEntete = 0;
        long octets = 0, octetsU = 0, octetsI = 0;
        Map<String,Integer> parSrc = new TreeMap<String,Integer>();
        FunctionIterator it = l.getFunctions(true);
        while (it.hasNext()) {
            Function f = it.next();
            if (f.isExternal()) continue;
            tot++;
            long t = f.getBody().getNumAddresses();
            octets += t;
            if (f.isThunk()) thunk++;
            Symbol s = f.getSymbol();
            String src = (s == null) ? "null" : s.getSource().toString();
            String n = f.getName();
            boolean auto = n.startsWith("FUN_") || n.startsWith("thunk_FUN_");
            String cle = (auto ? "AUTO_FUN" : src);
            Integer v = parSrc.get(cle);
            parSrc.put(cle, (v == null ? 0 : v) + 1);
            if (!auto && "USER_DEFINED".equals(src)) octetsU += t;
            if (!auto && "IMPORTED".equals(src)) octetsI += t;
            if (f.getComment() != null && f.getComment().length() > 0) cEntete++;
        }
        AddressIterator ai = l.getCommentAddressIterator(p.getMemory(), true);
        int comm = 0;
        while (ai.hasNext()) { ai.next(); comm++; }
        SymbolTable st = p.getSymbolTable();
        Map<String,Integer> symSrc = new TreeMap<String,Integer>();
        SymbolIterator si = st.getAllSymbols(false);
        int symTot = 0;
        while (si.hasNext()) {
            Symbol s = si.next();
            symTot++;
            String k = s.getSource().toString();
            Integer v = symSrc.get(k);
            symSrc.put(k, (v == null ? 0 : v) + 1);
        }
        int stru = 0;
        Iterator<Composite> ci = p.getDataTypeManager().getAllComposites();
        while (ci.hasNext()) { ci.next(); stru++; }
        println("### " + p.getDomainFile().getPathname() + " | "
                + p.getLanguageID() + " | base " + p.getImageBase()
               );
        println("FONCTIONS total=" + tot + " thunks=" + thunk
                + " octets_code=" + octets
                + " octets_USER=" + octetsU + " octets_IMPORTED=" + octetsI);
        println("FN_PAR_SOURCE " + parSrc);
        println("SYMBOLES total=" + symTot + " " + symSrc);
        println("AUTRES comm_entete=" + cEntete + " comm_total=" + comm
                + " composites=" + stru);
    }
}
