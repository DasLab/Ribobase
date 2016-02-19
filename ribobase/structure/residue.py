import uuid
import logging
import atom
import residue_type
import util
import basic_io
import numpy as np

#logging.basicConfig()
#logger = logging.getLogger(__name__)


class Residue(object):

    """
    Store residue information from pdb file, stores all Atom objects that
    belong to residue. Implementation is designed to be extremely lightweight.

    :param rtype: residue type, stores information about residue
    :type rtype: ResidueType object

    :param name: residue name
    :type name: str

    :param num: residue num
    :type num: int

    :param chain_id: chain identification
    :type chain_id: str

    :param i_code: insertion code, optional argument if not supplied will be
        set to
    :type i_code: str

    .. code-block:: python

		# example of generating a new adenine residue
		>>>rts = ResidueTypeSet()
		>>>rtype = rts.give_type_for_resname("ADE")
		>>>r = Residue(rtype, "ADE", 1, "A")

		>>>print r.name
		ADE

		# to add atoms to residue, use setup_atoms
		>>>a1 = Atom("P",[1.0,2.0,3.0])
		>>>a2 = Atom("O1P",[2.0,3.0,4.0])
		>>>r.setup_atoms([a1,a2])

	Attributes
	----------
	`atoms` : Atom object list
		holds all atoms that belong to this residue object
	`name` : str
		name of residue, ex. ADE, GUA etc
	`num` : int
		residue num
	`type` : ResidueType objext
		Information about residue type each nucleic acid has its own type
	`chain_id` : str
		chain indentification string, ex. 'A' or 'B'
	`score` : float
		Score associated with secondary structure score
	`i_code`: str
		residue insertion code
    """

    __slots__ = [
        "rtype",
        "name",
        "num",
        "chain_id",
        "i_code",
        "uuid",
        "atoms"]

    def __init__(self, rtype, name, num, chain_id, i_code=""):
        self.rtype = rtype
        self.name = name
        self.num = num
        self.chain_id = chain_id
        self.i_code = i_code
        self.uuid = uuid.uuid1()
        # fix pickle bug
        if len(self.i_code) == 0:
            self.i_code = ""

        self.atoms = []

    def __repr__(self):
        return "<Residue('%s%d%s chain %s')>" % (
            self.name, self.num, self.i_code, self.chain_id)

    def setup_atoms(self, atoms):
        """
        put atoms in correct positon in internal atom list, warns of extra atoms
        are included as well if atoms are missing

        :param atoms: list of atom objects that are to be part of this residue
        :type atoms: list of Atom objects
        """

        self.atoms = [None for x in self.rtype.atom_map.keys()]
        for a in atoms:
            name_change = self.rtype.get_correct_atom_name(a)
            if name_change is not None:
                a.name = name_change[1]
            if a.name in self.rtype.atom_map:
                pos = self.rtype.atom_map[a.name]
                self.atoms[pos] = a
            else:
                pass
                #logger.warning(a.name + " not included in " + repr(self))

        # Warning if an atom is missing
        for i, a in enumerate(self.atoms):
            if a is None:
                correct_name = None
                for name, pos in self.rtype.atom_map.iteritems():
                    if pos == i:
                        correct_name = name

                #logger.warning(correct_name + " is undefined in " + repr(self))

    def get_atom(self, atom_name):
        """
        get atom object by its name

        :param atom_name: name
        :type atom_name: str
        .. code-block:: python
            >>>r.get_atom("P")
            <Atom(name='P', coords='0 1 2')>
        """
        try:
            index = self.rtype.atom_map[atom_name]
            return self.atoms[index]
        except KeyError:
            raise KeyError("cannot find atom")

    def short_name(self):
        return self.rtype.name[0]

    def connected_to(self, res, cutoff=3.0):
        """
		Determine if another residue is connected to this residue, returns 0
		if res is not connected to self, returns 1 if connection is going
		from 5' to 3' and returns -1 if connection is going from 3' to 5'

        :param res: another residue
        :type res: Residue object

        """
        # 5' to 3'
        o3_atom = self.get_atom("O3'")
        p_atom = res.get_atom("P")
        if o3_atom and p_atom:
            if util.distance(o3_atom.coords, p_atom.coords) < cutoff:
                return 1

        # 3' to 5'
        p_atom = self.get_atom("P")
        o3_atom = res.get_atom("O3'")
        if o3_atom and p_atom:
            if util.distance(o3_atom.coords, p_atom.coords) < cutoff:
                return -1

        return 0

    def copy(self):
        """
		performs a deep copy of Residue object
		"""
        copied_r = Residue(self.rtype,self.name,self.num,self.chain_id,self.i_code)
        copied_r.atoms = [None for x in range(len(self.atoms))]
        for i,a in enumerate(self.atoms):
            if a is None:
                continue
            copied_r.atoms[i] = a.copy()

        copied_r.uuid = self.uuid
        return copied_r

    def new_uuid(self):
        """
        give residue a new uuid code, do this with caution
        """
        self.uuid = uuid.uuid1()

    def to_str(self):
        """
        stringifes residue object to string
        """
        s = self.rtype.name + "," + self.name + "," + str(self.num) + "," +\
            self.chain_id + "," + self.i_code + ","
        for a in self.atoms:
            if a is None:
                s += "N,"
            else:
                s += a.to_str() + ","
        return s

    def to_pdb_str(self, acount=1, return_acount=0, rnum=-1, chain_id=""):
        """
        returns pdb formatted of residues coordinate information
        """

        num = self.num
        cid = self.chain_id
        if rnum != -1:
            num = rnum
        if chain_id != "":
            cid = chain_id

        s = ""
        for a in self.atoms:
            if a is None:
                continue
            s += basic_io.PDBLINE_GE100K % \
                 ('ATOM', acount, a.name, '', self.rtype.name[0], cid,
                  num, '', a.coords[0], a.coords[1], a.coords[2], 1.00,
                  0.00, '', '')
            acount += 1

        if return_acount:
            return s,acount
        else:
            return s

    def to_pdb(self, fname="residue.pdb"):
        f = open(fname, "w")
        s = self.to_pdb_str()
        f.write(s)
        f.close()



