from rdkit.Chem import Descriptors
from rdkit import Chem


def OxygenCount(ID, smiles, project, series, CHEMICSMODELDIR):
    """
    Total number of O
    """

    fragStr = "O"
    mol = Chem.MolFromSmiles(fragStr)
    sma = Chem.MolToSmarts(mol)
    matchIdx = Chem.QuickSmartsMatch(smiles, sma)
    OxygenCount = len(matchIdx)
    confidence = "NaN"
    return OxygenCount, confidence

if __name__ == "__main__":
    OxygenCount, confidence = OxygenCount("MyMol", "c1(cc(c(cc1)Oc1c(ncc(c1)C(F)(F)F)C(N)=O)C)Cl", "project", "series", ".")
    print OxygenCount
