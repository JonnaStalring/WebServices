from rdkit.Chem import Descriptors
from rdkit import Chem


def SulfurCount(ID, smiles, project, series, CHEMICSMODELDIR):
    """
    Total number of S
    """

    fragStr = "S"
    mol = Chem.MolFromSmiles(fragStr)
    sma = Chem.MolToSmarts(mol)
    matchIdx = Chem.QuickSmartsMatch(smiles, sma)
    SulfurCount = len(matchIdx)
    confidence = "NaN"
    return SulfurCount, confidence

if __name__ == "__main__":
    SulfurCount, confidence = SulfurCount("MyMol", "c1(cc(c(cc1)Oc1c(ncc(c1)C(F)(F)F)C(N)=O)C)Cl", "project", "series", ".")
    print SulfurCount
