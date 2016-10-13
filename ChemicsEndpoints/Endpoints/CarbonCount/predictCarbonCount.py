from rdkit.Chem import Descriptors
from rdkit import Chem


def CarbonCount(ID, smiles, project, series, CHEMICSMODELDIR):
    """
    Total number of carbons
    """

    fragStr = "C"
    mol = Chem.MolFromSmiles(fragStr)
    sma = Chem.MolToSmarts(mol)
    matchIdx = Chem.QuickSmartsMatch(smiles, sma)
    CarbonCount = len(matchIdx)
    confidence = "NaN"
    return CarbonCount, confidence

if __name__ == "__main__":
    CarbonCount, confidence = CarbonCount("MyMol", "c1(cc(c(cc1)Oc1c(ncc(c1)C(F)(F)F)C(N)=O)C)Cl", "project", "series", ".")
    #CarbonCount, confidence = CarbonCount("MyMol", "CCO", "project", "series", ".")
    print CarbonCount
