import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.address.*;
import java.io.*;
import java.util.*;

public class CouvVF5 extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        BufferedReader br = new BufferedReader(new FileReader(a[0]));
        Program p = currentProgram;
        AddressFactory af = p.getAddressFactory();
        Listing l = p.getListing();
        Set<Address> fTout = new HashSet<Address>();
        Set<Address> fDocs = new HashSet<Address>();
        long octTout = 0, octDocs = 0;
        int horsFn = 0, horsFnDocs = 0;
        boolean dansDocs = false;
        String ligne;
        while ((ligne = br.readLine()) != null) {
            ligne = ligne.trim();
            if (ligne.equals("TOUT")) { dansDocs = false; continue; }
            if (ligne.equals("DOCS")) { dansDocs = true; continue; }
            if (ligne.isEmpty()) continue;
            Address ad = af.getAddress(ligne);
            Function f = l.getFunctionContaining(ad);
            if (f == null) { if (dansDocs) horsFnDocs++; else horsFn++; continue; }
            Address e = f.getEntryPoint();
            if (dansDocs) {
                if (fDocs.add(e)) octDocs += f.getBody().getNumAddresses();
            } else {
                if (fTout.add(e)) octTout += f.getBody().getNumAddresses();
            }
        }
        br.close();
        println("COUV_TOUT fonctions=" + fTout.size() + " octets=" + octTout
                + " adr_hors_fonction=" + horsFn);
        println("COUV_DOCS fonctions=" + fDocs.size() + " octets=" + octDocs
                + " adr_hors_fonction=" + horsFnDocs);
    }
}
