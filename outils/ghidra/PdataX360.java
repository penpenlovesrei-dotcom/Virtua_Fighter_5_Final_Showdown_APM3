// Cree une fonction a chaque entree `.pdata` d'une image Xbox 360 chargee
// en binaire brut (tools/xex.py), AVANT l'analyse automatique.
//
// `.pdata` Xbox 360 : des paires {debut, mot} en gros-boutien ; la longueur
// de la fonction est dans les bits 8-29 du mot, en instructions. L'image
// etant chargee a sa base (0x82000000), l'adresse de la table est celle de
// la section, passee en argument avec sa taille :
//
//     PdataX360.java <adresse .pdata> <taille>
//
// @category VF5
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;

public class PdataX360 extends GhidraScript {

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        long debut = Long.decode(args[0]);
        long taille = Long.decode(args[1]);
        int crees = 0, vues = 0;
        for (long k = 0; k + 8 <= taille; k += 8) {
            Address e = toAddr(debut + k);
            long f = getInt(e) & 0xFFFFFFFFL;
            if (f == 0) {
                continue;
            }
            vues++;
            Address a = toAddr(f);
            if (getFunctionAt(a) != null) {
                continue;
            }
            disassemble(a);
            if (createFunction(a, null) != null) {
                crees++;
            }
        }
        println("PdataX360 : " + vues + " entrees, " + crees + " fonctions creees");
    }
}
