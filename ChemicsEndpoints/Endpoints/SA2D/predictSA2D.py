from rdkit.Chem import Descriptors
from rdkit import Chem
import string

SAFILEPATH = "SMARTSFROMOSCAR.txt"

def SA2D(ID, smiles, project, series, CHEMICSMODELDIR):
    """
    Total number of carbons
    """

    mol = Chem.MolFromSmiles(smiles)
    SAlist = []
    fid = open(SAFILEPATH)
    for line in fid:
        lineList = string.split(line, " ")
        SA = lineList[0]
        SMARTS = string.strip(lineList[1])
        pattern = Chem.MolFromSmarts(SMARTS)
        if mol.HasSubstructMatch(pattern):
            SAlist.append(SA)
    SA = string.join(SAlist, ",")
    confidence = "NaN"

    return SA, confidence


if __name__ == "__main__":
    SA, confidence = SA2D("MyArAmineMol", "Nc1ccc(CC2=CC=CC2)cc1", "project", "series", ".")
    SA, confidence = SA2D("MyBenzyleAmineMol", "NCc1ccccc1", "project", "series", ".")
    SA, confidence = SA2D("MyThiopheneMol", "c1ccc(-c2ccsc2)cc1", "project", "series", ".")
    SA, confidence = SA2D("MyFuran", "c1ccc(-c2ccoc2)cc1", "project", "series", ".")
    print SA
