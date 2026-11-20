# -*- coding: utf-8 -*-
r"""TOUT CE QU'UNE GENERATION DIT DE SES DECORS, lu dans SON binaire.

Frederic, 2026-09-11 : « applique a VF5 R ses propres listes, rien ne doit
venir de FS, applique les effets VF5 a VF5 ». Ce module est la source unique
de ces donnees pour le patcheur et les controles : descripteurs, taches
d'effet, murs, animations, poussiere de chute, et les DOSSIERS des effets.

Deux generations Lindbergh, deux ELF x86-32 (g++) :

    r     extracted/LIND_R/id/disk0/vf5     VF5 R (2008)
    verb  extracted/LIND_VF5/id/disk0/vf5   VF5 ver.B (2007)

LES DOSSIERS D'EFFET. Chaque adresse ci-dessous a ete trouvee en desassemblant
la tache concernee (typeinfo `14TaskEffectSnow` -> vtable -> creneau 7 ou
chargeur), et elle est VERIFIEE a chaque lecture : l'instruction citee doit
porter l'adresse de la table dans ses octets. Si le binaire n'est pas celui
qu'on croit, on refuse -- on ne lit pas une table au hasard.

Les dossiers sont rendus AU FORMAT DE FS (le seul que le moteur APM3 lise),
avec la liste des champs a traduire : les uid (par NOM, dans la base de la
generation), les textures (par NOM chez ver.B, dont la numerotation n'est pas
celle de FS ; telles quelles chez R, qui numerote comme FS) et les objets
(`(objset << 16) | rang`, objset de la generation).

Deux formes ne sont pas des tables figees : la brume animee (FOG_ANIM) est
assemblee par un constructeur statique, qu'on REJOUE (`emu32.py`) ; le
tonnerre et l'anneau d'eau nomment leurs donnees dans le code.
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import tables_generation as tg                                  # noqa: E402

# ---------------------------------------------------------------------------
# LES EMPLACEMENTS, releves au desassembleur le 2026-09-11
#
#   table   adresse du premier dossier     pas   forme de la table chez la
#   ref     l'instruction qui la nomme     n     generation (n = nombre de
#   fin     -1 : liste terminee par -1           dossiers de la boucle)
# ---------------------------------------------------------------------------
EMPLACEMENTS = {
    'r': {
        'SNOW': dict(table=0x89A1560, pas=0x58, fin=True, ref=0x84C0B69),
        'BREATH': dict(table=0x89A18A0, pas=0x14, n=3, ref=0x84CD158),
        'SPLASH': dict(table=0x89A1760, pas=0x38, n=3, ref=0x84C86FD),
        'RIPPLE': dict(table=0x89A16A0, pas=0x2C, n=2, ref=0x84C2480),
        'FOG_ANIM': dict(table=0x8BE4DA0, pas=0x34, n=1,
                         emu=(0x84CB3A4, 0x84CB454), ref=0x84CAED0),
        'THUNDER': dict(litteraux=((0x84C3E5E, 0x84C3E70),
                                   (0x84C3E63, 0x84C3EC8)), n=7),
        'WATER_RING': dict(objet=0x84C5751),
        'DOWN': dict(dense=0x883AAC0, ref=0x84C4891),
        # --- les cinq de la troisieme passe (2026-09-11) ---------------------
        # FOG_RING : deux dossiers en .bss (jin 9, du2 22), batis par le
        # constructeur 0x84CCDE4 ; lus par la boucle de 0x84CBD06 (2 tours).
        'FOG_RING': dict(table=0x8BE4DE0, pas=0x3C, n=2,
                         emu=(0x84CCDE4, 0x84CCFA2), ref=0x84CBD48),
        # RAIN : UN bloc de 0x5C, sans indice -- la tache n'est creee que
        # pour les decors qui la demandent (bar). Recopie champ a champ par
        # 0x84C32C7.. dans l'etat, aux memes decalages que FS.
        'RAIN': dict(bloc=0x89A1700, pas=0x5C, ref=0x84C32D0, tache=8),
        # LEAF : pas de table. Le dessin nomme ses deux objets par des
        # LITTERAUX (`mov dword [esp], imm32`), dans l'ordre de FS.
        'LEAF': dict(objets=((0x84BCAB2, '_DUMMY_SAKURA'),
                             (0x84BCAD8, '_DUMMY_KAGE')), tache=3),
        # WET_CLOTH : `cmp [eax+0x58], imm` puis `cmove edx, [0,4]`, sinon
        # 0,001 (0x84CB4C0, appelee par l'init avec le drapeau 0).
        'WET_CLOTH': dict(cmp=0x84CB4D1, cmove=0x84CB4D5, defaut=0x84CB4C1,
                          tache=17),
        # YUKA (le sol qui se casse, ban) : tout est LITTERAL -- l'objset
        # (`mov [esp], 0x18`, 0x84C14C3), la table 12x12 x 3 couches d'objets
        # (0x883A080, identique a celle de FS), l'uid du debris (0x84C0F35)
        # et l'objet dessine (0x84C1434).
        'YUKA': dict(jeu=0x84C14C3, table=0x883A080, ref=0x84C1513,
                     uid=0x84C0F35, objet=0x84C1434, tache=6),
        # RINGOUT_SPLASH : {indice, uid, uid _S, flottant, chaine}, 0x14
        # octets, trois dossiers (riv, sin, du3) -- boucle de 0x84C5480.
        'RINGOUT_SPLASH': dict(table=0x883AC00, pas=0x14, n=3, ref=0x84C549C),
    },
    'verb': {
        'BREATH': dict(table=0x8661D60, pas=0x14, n=2, ref=0x839D21C),
        'SPLASH': dict(table=0x8661C20, pas=0x38, n=3, ref=0x8396130),
        'RIPPLE': dict(table=0x8661BC0, pas=0x30, n=2, ref=0x839290B),
        'SNOW_RING': dict(table=0x8661D00, pas=0x2C, n=1, ref=0x839A3CB),
        'FOG_ANIM': dict(table=0x8947520, pas=0x34, n=1,
                         emu=(0x839B82D, 0x839B891), ref=0x839B5C7),
        'THUNDER': dict(liste_fixe=(0x8394373, 0x86041E8), n=7,
                        decor='hai'),
        'WATER_RING': dict(objet=0x8395A93),
        'DOWN': dict(dense=0x8604340, ref=0x8394C1F),
        # --- les cinq de la troisieme passe (2026-09-11) ---------------------
        # FOG_RING : un dossier en .bss (sin 10), bati par `rep movsd` depuis
        # la pile (0x839CDE7..) ; lu par 0x839BF3E.
        'FOG_RING': dict(table=0x8947580, pas=0x3C, n=1,
                         emu=(0x839CDE7, 0x839CE59), ref=0x839BF76),
        # RAIN : le bloc de 0x5C est en .bss, bati par 0x83940FD.. ; recopie
        # par 0x839385E aux memes decalages que FS (FS ignore +0x40 et +0x50).
        'RAIN': dict(bloc=0x8947460, pas=0x5C, emu=(0x83940FD, 0x83941AB),
                     ref=0x83938F0, tache=8),
        'LEAF': dict(objets=((0x83911F3, '_DUMMY_SAKURA'),
                             (0x8391229, '_DUMMY_KAGE')), tache=3),
        # WET_CLOTH : aucune comparaison -- 0,001 pour tous (0x839BA82).
        'WET_CLOTH': dict(defaut=0x839BA83, tache=17),
        # YUKA : meme construction que FS et R ; l'objset de ban est le 10.
        'YUKA': dict(jeu=0x8391E40, table=0x8603940, ref=0x8391E49,
                     uid=0x8391B97, objet=0x83924BC, tache=6),
        'RINGOUT_SPLASH': dict(table=0x8604520, pas=0x14, n=2, ref=0x8395133),
    },
}
YUKA_OBJETS = 0x90 * 3          # 144 dalles (12 x 12) x 3 couches

# ---------------------------------------------------------------------------
# LES COMPORTEMENTS CABLES SUR UN NUMERO (2026-09-11)
#
# Le moteur -- celui de FS comme ceux des generations -- teste en dur des
# numeros de DECOR (`decor == 16` : le grillage de yuk) et d'UID (`uid ==
# 0x7F4` : les flashs de smo). Un decor ajoute n'a ni l'un ni l'autre : ces
# comportements ne se declenchent jamais pour lui. On ne les lui rend QUE si
# SA generation les a -- chaque entree ci-dessous cite l'instruction de SON
# code qui le prouve, et elle est verifiee a la lecture : l'immediat compare
# doit etre l'indice du decor DANS CETTE GENERATION (smo vaut 0x27 chez R,
# 0x28 chez FS), ou l'uid de l'animation DANS SA BASE.
#
#   codes    {code du decor: instruction `cmp reg, indice`}
#   uids     {nom de l'animation: instruction qui compare son uid}
#            (`decal` : l'uid vaut celui de l'instruction + decal -- KAWA est
#            teste par `uid - IDOU < 2`)
#   objet    (instruction de depart, suffixe) : l'objet que le code dessine
#            juste apres le test
# ---------------------------------------------------------------------------
CABLAGES = {
    'r': {
        # le grillage qui monte et descend entre les rounds (0x84B9520 : les
        # sons stg_vf5r_wall_gym_on01/off01 juste avant)
        'grillage': dict(codes={'yuk': 0x84B9536, 'gym': 0x84B953D}),
        # le reflet du grillage de gym, dessine apres `decor == 0x26`
        'reflet_grillage': dict(codes={'gym': 0x84BB7FA},
                                objet=(0x84BB7FA, '_SAKU_REFLECT')),
        # la passe S_REFL : plan de coupe -0,8 pour sin, 1000 ailleurs
        'reflet_sin': dict(codes={'sin': 0x81427CB}),
        # bar : un second jeu de parametres (`cmove`, 0x813EB6A)
        'bar': dict(codes={'bar': 0x813EB6A}),
        # TaskEffectAuth3D::setStage (0x84B8D66) : riv -> balancement,
        # smo -> les flashs ne partent qu'en fin de round
        'a3d_riv': dict(codes={'riv': 0x84B8DA4}),
        'a3d_flash': dict(codes={'smo': 0x84B8DA9}),
        # ... et les deux uid que l'init (0x84B8A64) et la mise a jour
        # (0x84B87A8) traitent a part
        'uid_idou': dict(uids={'STGRIV_EFF_IDOU': 0x84B8AF9,
                               'STGRIV_EFF_KAWA': 0x84B8AF9},
                         decal={'STGRIV_EFF_KAWA': 1}),
        'uid_flash': dict(uids={'STGSMO_EFF_FLASH': 0x84B8AA6}),
    },
    'verb': {
        # ver.B n'a ni grillage, ni smo, ni passe de reflet par decor : son
        # TaskEffectAuth3D (0x838C868) ne teste que riv, et ses uid IDOU/KAWA
        'a3d_riv': dict(codes={'riv': 0x838C88D}),
        'uid_idou': dict(uids={'STGRIV_EFF_IDOU': 0x838C97A,
                               'STGRIV_EFF_KAWA': 0x838C97A},
                         decal={'STGRIV_EFF_KAWA': 1}),
    },
}

# Les deux scalaires que le moteur FS sait choisir pour WET_CLOTH
# (`vblendvps` en 0x1800859C1 : 0x180350C00 ou 0x18034AF50).
WET_CLOTH_FS = (0x3A83126F, 0x3ECCCCCD)          # 0,001 et 0,4

# Les champs a traduire, au format de FS (decalages dans le dossier FS)
CHAMPS = {
    'SNOW': dict(pas=0x58, tex=(0x04,)),
    'BREATH': dict(pas=0x14, uids=(0x0C,)),
    'SPLASH': dict(pas=0x38, tex=(0x08,), objets=(0x0C,)),
    'RIPPLE': dict(pas=0x2C, tex=(0x20,)),
    'FOG_ANIM': dict(pas=0x34),
    'SNOW_RING': dict(pas=0x2C, tex=(0x14, 0x18, 0x1C, 0x20), objets=(0x24,)),
    'THUNDER': dict(pas=0x20, uids=(0, 4, 8, 0xC, 0x10, 0x14, 0x18)),
    # la texture de l'anneau de brume : 0x1801957A0(etat+0x1C), dans le
    # dessin 0x180072BA0 -- la fonction de toutes les textures d'effet
    'FOG_RING': dict(pas=0x3C, tex=(0x1C,)),
    'RAIN': dict(pas=0x5C, sans_indice=True),
    # les deux objets dessines par 0x180074A50 : [+0x5C] puis [+0x60]
    'LEAF': dict(pas=0x0C, objets=(0x04, 0x08)),
    'WET_CLOTH': dict(pas=0x04, sans_indice=True),
    # YUKA : un dossier FABRIQUE (FS n'en a pas) -- {indice, objset, uid du
    # debris, objet dessine, table de 0x90 x 3 objets} ; voir patch_moteur,
    # YUKA_SITES, pour les cinq litteraux de FS qu'il remplace.
    'YUKA': dict(pas=0x10 + 4 * 0x90 * 3, jeux=(0x04,), uids=(0x08,),
                 objets=(0x0C,) + tuple(range(0x10, 0x10 + 4 * 0x90 * 3, 4))),
    # RINGOUT_SPLASH au format de FS (0x20) : {indice, uid, uid _S, flottant,
    # POINTEUR de chaine, decalage y de l'animation, y de la liste de
    # 0x180677330}. Les deux derniers n'existent pas chez R ni ver.B : leur
    # code pose l'animation a la position calculee, SANS decalage
    # (0x84C4D20), et ne pousse rien. On ecrit donc 0,0 et le NaN 0xFFFFFFFF,
    # que le stub de 0x180079729 lit comme « ne pas pousser ». La chaine est
    # rendue par `chaine_ringout` ; le patcheur la pose dans `.decors`.
    'RINGOUT_SPLASH': dict(pas=0x20, uids=(0x04, 0x08), chaine=0x10),
}
RINGOUT_SANS_POUSSEE = 0xFFFFFFFF


class Refus(Exception):
    pass


class Generation(object):
    def __init__(self, gen):
        import a3d_db
        self.gen = gen
        g = tg.GENERATIONS[gen]
        self.nom = g['nom']
        self.elf = tg.Elf(g['elf'])
        self.t = tg.lire(gen)
        self.codes = self.t['codes']
        self.uids = a3d_db.charger(os.path.join(g['db'],
                                                'auth_3d_db.bin')).uids()
        od = open(os.path.join(g['db'], 'obj_db.bin'), 'rb').read()
        nj, _, tj, no, to = struct.unpack_from('<5I', od, 0)
        self.jeux = {}
        for k in range(nj):
            po, ident = struct.unpack_from('<2I', od, tj + k * 0x24)
            self.jeux[od[po:od.index(b'\x00', po)].decode('latin-1')] = ident
        self.objets = {}
        for k in range(no):
            ident, po = struct.unpack_from('<2I', od, to + k * 8)
            self.objets[ident] = od[po:od.index(b'\x00', po)].decode('latin-1')
        self._tex = None

    # --- utilitaires ---------------------------------------------------------
    def valeur_uid(self, u):
        """La valeur auth_3d d'un uid de la generation : 'A STGDJO_EFF_FIRE'."""
        v = self.uids.get(u, {}).get('value')
        if v is None:
            raise Refus('%s : uid %d absent de sa base' % (self.nom, u))
        return v

    def nom_texture(self, t):
        if self._tex is None:
            import variantes_vf5
            p = os.path.join(tg.GENERATIONS[self.gen]['db'], 'tex_db.bin')
            self._tex = variantes_vf5._tex_db(p)
        return self._tex.get(t)

    def objset_de(self, code):
        return self.jeux.get('STG%s' % code.upper())

    def _verifier_ref(self, ref, table):
        o = self.elf.off(ref)
        if o is None or struct.pack('<I', table) not in self.elf.d[o:o + 12]:
            raise Refus('%s : l instruction 0x%X ne nomme pas la table 0x%X '
                        '-- ce n est pas le binaire attendu'
                        % (self.nom, ref, table))

    def _octets(self, va, n):
        o = self.elf.off(va)
        return self.elf.d[o:o + n]

    # --- les listes ------------------------------------------------------------
    def taches(self, code):
        import patch_moteur
        noms = dict((n.replace('EFFECT_', ''), i)
                    for i, n in enumerate(patch_moteur.EFFETS_NOMS))
        return [noms[x] for x in self.t['taches'].get(code, [])]

    def animations(self, code):
        return list(self.t['anims'].get(code, []))

    # --- le descripteur --------------------------------------------------------
    def descripteur(self, code):
        """Les objets PAR ROLE {(role): identifiant empaquete}, le second
        objset (ver.B), les trois textures de reflet d'objectif."""
        a = self.t['adresses']
        i = self.codes.index(code)
        base = a['descripteurs'] + i * a['pas_desc']
        e = self.elf
        if a['pas_desc'] == 0x70:          # ver.B
            roles = {'gnd': 0x10, 'sky': 0x14, 'sdw': 0x18, 'reflect': 0x20}
            objset2 = e.i32(base + 0x0C)
            flares = [e.u32(base + 0x28 + 4 * k) for k in range(3)]
        elif a['pas_desc'] == 0x8C:        # VF5 R : l'ordre de FS
            roles = {'gnd': 0x0C, 'ring': 0x10, 'sky': 0x14, 'sdw': 0x18,
                     'reflect': 0x1C}
            objset2 = -1
            flares = [e.u32(base + 0x24 + 4 * k) for k in range(3)]
        else:
            raise Refus('%s : descripteur de 0x%X octets inconnu'
                        % (self.nom, a['pas_desc']))
        objets = dict((r, e.u32(base + o)) for r, o in roles.items())
        # LES ROLES SE CONTROLENT PAR NOM : un descripteur mal lu nommerait
        # un objet quelconque.
        for r, v in objets.items():
            if v == 0xFFFFFFFF:
                continue
            n = self.objets.get(v, '').upper()
            if not n.endswith('_' + r.upper()):
                raise Refus('%s : le %s de %s est %s' % (self.nom, r, code, n))
        return dict(objset=e.i32(base + 8), objset2=objset2, objets=objets,
                    flares=flares)

    # --- le mur -------------------------------------------------------------------
    def mur(self, code):
        """Le mur, complet, ou None : morceaux (objet, 36 octets de
        flottants), second tableau, uid, paires, et les trois champs de VF5 R
        (grillage anime, objets cassables)."""
        a = self.t['adresses']
        e = self.elf
        t, pas = a['murs'], a['pas_murs']
        i_code = self.codes.index(code)
        k = 0
        while e.i32(t + k * pas) != -1:
            if e.i32(t + k * pas) == i_code:
                break
            k += 1
        else:
            return None
        base = t + k * pas
        ch = [e.u32(base + 4 + 4 * j) for j in range((pas - 4) // 4)]
        pm = a['pas_morceau']
        decal = 8 if pm == 0x2C else 4

        def morceaux(p):
            out = []
            while e.i32(p + len(out) * pm) != -1:
                o = e.off(p + len(out) * pm)
                out.append((struct.unpack_from('<I', e.d, o)[0],
                            e.d[o + decal:o + decal + 36]))
                if len(out) > 256:
                    raise Refus('%s : morceaux sans fin' % self.nom)
            return out
        pieces = morceaux(ch[0])
        uids, paires = [], []
        if ch[1]:
            while e.i32(ch[1] + 4 * len(uids)) != -1:
                uids.append(self.valeur_uid(e.i32(ch[1] + 4 * len(uids))))
        if ch[2]:
            while e.i32(ch[2] + 0x10 * len(paires)) != -1:
                q = [e.i32(ch[2] + 0x10 * len(paires) + 4 * j)
                     for j in range(4)]
                paires.append((q[0] & 0xFFFFFFFF, q[1] & 0xFFFFFFFF,
                               self.valeur_uid(q[2]) if q[2] != -1 else None,
                               self.valeur_uid(q[3]) if q[3] != -1 else None))
        r = dict(pieces=pieces, uids=uids, paires=paires,
                 p20=morceaux(ch[3]) if len(ch) > 3 and ch[3] else None,
                 u28=None, o30=None, u38=None)
        # VF5 R : +0x14 grillage anime (2 uid), +0x18 objets cassables,
        # +0x1C un uid par objet cassable. Le moteur en lit min(morceaux, 4) :
        # on en rend autant, comme la generation les lit.
        n4 = min(len(pieces), 4)
        if len(ch) > 4 and ch[4]:
            r['u28'] = [self._uid_ou_none(e.i32(ch[4] + 4 * j))
                        for j in range(2)]
        if len(ch) > 5 and ch[5]:
            r['o30'] = []
            for j in range(n4):
                o = e.off(ch[5] + 0x10 * j)
                ob, u = struct.unpack_from('<Ii', e.d, o)
                r['o30'].append((ob, self._uid_ou_none(u), e.d[o + 8:o + 16]))
        if len(ch) > 6 and ch[6]:
            r['u38'] = [self._uid_ou_none(e.i32(ch[6] + 4 * j))
                        for j in range(n4)]
        return r

    def _uid_ou_none(self, u):
        if u == -1:
            return None
        v = self.uids.get(u, {}).get('value')
        return v            # None si ce n'est pas un uid : on ne l'invente pas

    # --- la poussiere de chute -------------------------------------------------
    def down(self, code):
        em = EMPLACEMENTS[self.gen]['DOWN']
        self._verifier_ref(em['ref'], em['dense'])
        u = self.elf.i32(em['dense'] + 4 * self.codes.index(code))
        return None if u == -1 else self.valeur_uid(u)

    # --- les dossiers d'effet --------------------------------------------------
    def dossiers(self, nom):
        """{code: dossier AU FORMAT FS (bytes)} pour la tache `nom`."""
        if not hasattr(self, '_dossiers'):
            self._dossiers = {}
        if nom not in self._dossiers:
            self._dossiers[nom] = self._lire_dossiers(nom)
        return self._dossiers[nom]

    def _demandeurs(self, tache):
        """Les codes dont la liste de taches (celle de la generation)
        demande `tache` : pour les donnees qui ne portent pas d'indice."""
        return [c for c in self.codes if tache in self.taches(c)]

    def _litteral(self, va):
        """L'immediat 32 bits de l'instruction en `va` (un `mov`)."""
        import capstone
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        md.detail = True
        o = self.elf.off(va)
        ins = next(md.disasm(self.elf.d[o:o + 16], va))
        imm = [op.imm for op in ins.operands
               if op.type == capstone.x86.X86_OP_IMM]
        if ins.mnemonic not in ('mov', 'cmp') or len(imm) != 1:
            raise Refus('%s : 0x%X n est pas un %s a immediat (%s %s)'
                        % (self.nom, va, 'mov/cmp', ins.mnemonic,
                           ins.op_str))
        return imm[0] & 0xFFFFFFFF, ins

    def _lire_dossiers(self, nom):
        em = EMPLACEMENTS[self.gen].get(nom)
        if em is None:
            return {}
        e = self.elf
        out = {}
        # --- les formes SANS indice : la donnee vaut pour tout decor qui
        #     demande la tache (la generation ne la cree que pour eux) -------
        if 'bloc' in em:
            self._verifier_ref(em['ref'], em['bloc'])
            if 'emu' in em:
                import emu32
                m = emu32.rejouer(e, em['emu'][0], em['emu'][1])
                b = emu32.lire_ecrit(m, em['bloc'], em['pas'])
                if b is None:
                    raise Refus('%s : le constructeur n ecrit pas le bloc %s'
                                % (self.nom, nom))
            else:
                b = self._octets(em['bloc'], em['pas'])
            return dict((c, self._au_format_fs(nom, b))
                        for c in self._demandeurs(em['tache']))
        if nom == 'LEAF':
            objs = []
            for va, suffixe in em['objets']:
                v, _ = self._litteral(va)
                n = self.objets.get(v, '').upper()
                if not n.endswith(suffixe):
                    raise Refus('%s : le litteral 0x%X de 0x%X nomme %s, pas '
                                '*%s' % (self.nom, v, va, n, suffixe))
                objs.append(v)
            for c in self._demandeurs(em['tache']):
                out[c] = self._au_format_fs(nom, struct.pack(
                    '<iII', self.codes.index(c), objs[0], objs[1]))
            return out
        if nom == 'YUKA':
            self._verifier_ref(em['ref'], em['table'])
            jeu, _ = self._litteral(em['jeu'])
            uid, _ = self._litteral(em['uid'])
            obj, _ = self._litteral(em['objet'])
            if not self.valeur_uid(uid).upper().endswith('_EFF_YUKA_TOBICHIRI'):
                raise Refus('%s : l uid YUKA %d est %s' % (self.nom, uid,
                                                          self.valeur_uid(uid)))
            if obj >> 16 != jeu or \
                    not self.objets.get(obj, '').upper().endswith('_DUMMY'):
                raise Refus('%s : l objet YUKA 0x%X est %s' % (
                    self.nom, obj, self.objets.get(obj)))
            table = self._octets(em['table'], 4 * YUKA_OBJETS)
            for k in range(YUKA_OBJETS):
                v = struct.unpack_from('<I', table, 4 * k)[0]
                if v >> 16 != jeu or v not in self.objets:
                    raise Refus('%s : la table YUKA porte 0x%X en %d'
                                % (self.nom, v, k))
            for c in self._demandeurs(em['tache']):
                out[c] = self._au_format_fs(nom, struct.pack(
                    '<iIiI', self.codes.index(c), jeu, uid, obj) + table)
            return out
        if nom == 'WET_CLOTH':
            defaut, ins = self._litteral(em['defaut'])
            if defaut not in WET_CLOTH_FS:
                raise Refus('%s : WET_CLOTH vaut 0x%X par defaut, que FS ne '
                            'sait pas choisir' % (self.nom, defaut))
            special = {}
            if 'cmp' in em:
                i_c, _ = self._litteral(em['cmp'])
                import capstone
                md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
                md.detail = True
                o = e.off(em['cmove'])
                ins = next(md.disasm(e.d[o:o + 8], em['cmove']))
                if ins.mnemonic != 'cmove':
                    raise Refus('%s : 0x%X n est pas un cmove'
                                % (self.nom, em['cmove']))
                v = e.u32(ins.operands[1].mem.disp & 0xFFFFFFFF)
                if v not in WET_CLOTH_FS:
                    raise Refus('%s : WET_CLOTH vaut 0x%X pour le decor %d, '
                                'que FS ne sait pas choisir'
                                % (self.nom, v, i_c))
                special[self.codes[i_c]] = v
            for c in self._demandeurs(em['tache']):
                out[c] = struct.pack('<I', special.get(c, defaut))
            return out
        if 'emu' in em:
            import emu32
            self._verifier_ref(em['ref'], em['table'])
            m = emu32.rejouer(e, em['emu'][0], em['emu'][1])
            b = emu32.lire_ecrit(m, em['table'], em['pas'] * em['n'])
            if b is None:
                raise Refus('%s : le constructeur n ecrit pas le dossier %s'
                            % (self.nom, nom))
            recs = [b[k * em['pas']:(k + 1) * em['pas']]
                    for k in range(em['n'])]
        elif 'table' in em:
            self._verifier_ref(em['ref'], em['table'])
            recs = []
            k = 0
            while True:
                b = self._octets(em['table'] + k * em['pas'], em['pas'])
                if em.get('fin') and struct.unpack_from('<i', b, 0)[0] == -1:
                    break
                recs.append(b)
                k += 1
                if not em.get('fin') and k >= em['n']:
                    break
                if k > 64:
                    raise Refus('%s : %s sans fin' % (self.nom, nom))
        elif 'litteraux' in em:
            recs = []
            for ref_cmp, ref_liste in em['litteraux']:
                o = e.off(ref_cmp)
                import capstone
                md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
                md.detail = True
                ins = next(md.disasm(e.d[o:o + 8], ref_cmp))
                if ins.mnemonic != 'cmp':
                    raise Refus('%s : 0x%X n est pas un cmp' % (self.nom,
                                                                 ref_cmp))
                i_dec = ins.operands[1].imm
                o = e.off(ref_liste)
                ins = next(md.disasm(e.d[o:o + 12], ref_liste))
                liste = ins.operands[1].imm & 0xFFFFFFFF
                b = struct.pack('<i', i_dec) + self._octets(liste, 4 * em['n'])
                recs.append(b)
        elif 'liste_fixe' in em:
            ref, liste = em['liste_fixe']
            self._verifier_ref(ref, liste)
            recs = [struct.pack('<i', self.codes.index(em['decor']))
                    + self._octets(liste, 4 * em['n'])]
        else:
            return {}
        for b in recs:
            i = struct.unpack_from('<i', b, 0)[0]
            if not 0 <= i < len(self.codes):
                continue
            out[self.codes[i]] = self._au_format_fs(nom, b)
        return out

    def _au_format_fs(self, nom, b):
        """Le dossier de la generation, rendu au format FS."""
        if nom == 'RIPPLE' and len(b) == 0x30:
            # ver.B a un flottant de plus en +0x10, que FS ne charge plus :
            # FS [4..10] = ver.B [5..11] (chargeurs compares : FS
            # FUN_18007AE10, ver.B 0x8392928).
            b = b[:0x10] + b[0x14:0x30]
        if nom == 'THUNDER':
            # 7 uid, pas d'indice dans le dossier FS : l'indice est ecrit
            # par le patcheur dans le bourrage +0x1C.
            b = b[4:4 + 28] + b'\x00' * 4
        if nom == 'RINGOUT_SPLASH' and len(b) == 0x14:
            # le pointeur de chaine de la GENERATION reste en +0x10 (le
            # patcheur le remplace par sa copie) ; +0x18/+0x1C : voir CHAMPS
            b = b[:0x10] + struct.pack('<QfI', struct.unpack_from(
                '<I', b, 0x10)[0], 0.0, RINGOUT_SANS_POUSSEE)
        if len(b) != CHAMPS[nom]['pas']:
            raise Refus('%s : dossier %s de %d octets, FS en attend %d'
                        % (self.nom, nom, len(b), CHAMPS[nom]['pas']))
        return b

    def _immediat(self, va):
        """L'entier que l'instruction en `va` compare : `cmp r, imm`,
        `sub r, imm`, ou `lea r, [r - imm]`."""
        import capstone
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        md.detail = True
        o = self.elf.off(va)
        ins = next(md.disasm(self.elf.d[o:o + 16], va))
        if ins.mnemonic in ('cmp', 'sub'):
            imm = [op.imm for op in ins.operands
                   if op.type == capstone.x86.X86_OP_IMM]
            if len(imm) == 1:
                return imm[0] & 0xFFFFFFFF
        if ins.mnemonic == 'lea':
            return (-ins.operands[1].mem.disp) & 0xFFFFFFFF
        raise Refus('%s : 0x%X (%s %s) ne compare pas un immediat'
                    % (self.nom, va, ins.mnemonic, ins.op_str))

    def _uid_de_nom(self, nom):
        for k, v in self.uids.items():
            if v.get('value', '').split()[-1] == nom:
                return k
        return None

    def cablages(self):
        """{comportement: {'codes': {code}, 'uids': {nom: uid de la base},
        'objet': identifiant}} -- chaque element VERIFIE dans le code."""
        if hasattr(self, '_cablages'):
            return self._cablages
        out = {}
        for nom_c, c in CABLAGES.get(self.gen, {}).items():
            r = {'codes': set(), 'uids': {}, 'objet': None}
            for code, va in c.get('codes', {}).items():
                v = self._immediat(va)
                if v != self.codes.index(code):
                    raise Refus('%s : %s -- 0x%X compare %d, pas l indice de '
                                '%s (%d)' % (self.nom, nom_c, va, v, code,
                                             self.codes.index(code)))
                r['codes'].add(code)
            for nom_a, va in c.get('uids', {}).items():
                v = self._immediat(va) + c.get('decal', {}).get(nom_a, 0)
                u = self._uid_de_nom(nom_a)
                if u != v:
                    raise Refus('%s : %s -- 0x%X designe l uid %d, %s est %s'
                                % (self.nom, nom_c, va, v, nom_a, u))
                r['uids'][nom_a] = u
            if 'objet' in c:
                import capstone
                md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
                md.detail = True
                va0, suffixe = c['objet']
                o = self.elf.off(va0)
                for ins in md.disasm(self.elf.d[o:o + 0x100], va0):
                    imm = [op.imm & 0xFFFFFFFF for op in ins.operands
                           if op.type == capstone.x86.X86_OP_IMM]
                    if ins.mnemonic == 'mov' and imm and \
                            self.objets.get(imm[0], '').upper().endswith(
                                suffixe):
                        r['objet'] = imm[0]
                        break
                if r['objet'] is None:
                    raise Refus('%s : %s -- aucun objet *%s apres 0x%X'
                                % (self.nom, nom_c, suffixe, va0))
            out[nom_c] = r
        self._cablages = out
        return out

    def chaine(self, va):
        """Le texte que la generation range a `va` (pointeur d'un dossier)."""
        if not va or self.elf.off(va) is None:
            raise Refus('%s : pointeur de chaine 0x%X hors du fichier'
                        % (self.nom, va))
        return self.elf.chaine(va)

    def objet_anneau_eau(self):
        """Le rang de l'objet que la generation dessine pour WATER_RING, et
        son objset : le litteral du code."""
        em = EMPLACEMENTS[self.gen]['WATER_RING']
        v = self.elf.u32(em['objet'])
        n = self.objets.get(v, '').upper()
        if not n.endswith('_WATER_RING'):
            raise Refus('%s : le litteral 0x%X de 0x%X nomme %s'
                        % (self.nom, v, em['objet'], n))
        return v >> 16, v & 0xFFFF


_CACHE = {}


def generation(gen):
    if gen not in _CACHE:
        _CACHE[gen] = Generation(gen)
    return _CACHE[gen]


if __name__ == '__main__':
    for gen in sys.argv[1:] or ('r', 'verb'):
        g = generation(gen)
        print('=' * 60, g.nom)
        for nom in ('SNOW', 'BREATH', 'SPLASH', 'RIPPLE', 'FOG_ANIM',
                    'SNOW_RING', 'THUNDER', 'FOG_RING', 'RAIN', 'LEAF',
                    'WET_CLOTH'):
            d = g.dossiers(nom)
            print('%-9s %s' % (nom, ' '.join(
                c + ('' if nom != 'WET_CLOTH' else '=%.3g' % struct.unpack(
                    '<f', d[c])[0]) for c in sorted(d))))
        print('WATER_RING', g.objet_anneau_eau())
        print('DOWN', dict((c, g.down(c)) for c in ('djo', 'riv', 'slk')))
        for c in ('djo', 'hai', 'nyc', 'yuk'):
            m = g.mur(c)
            print('mur', c, m and (len(m['pieces']), m['uids'], bool(m['p20']),
                                   m['u28'], m['o30'] and len(m['o30'])))
        print('descripteur djo', g.descripteur('djo'))
