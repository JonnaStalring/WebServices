from rdkit.Chem import Descriptors
from rdkit import Chem


def FluorineCount(ID, smiles, project, series, CHEMICSMODELDIR):
    """
    Total number of fluorines
    """

    fragStr = "F"
    mol = Chem.MolFromSmiles(fragStr)
    sma = Chem.MolToSmarts(mol)
    matchIdx = Chem.QuickSmartsMatch(smiles, sma)
    FluorineCount = len(matchIdx)
    confidence = "NaN"
    return FluorineCount, confidence

if __name__ == "__main__":
    FluorineCount, confidence = FluorineCount("MyMol", "c1(cc(c(cc1)Oc1c(ncc(c1)C(F)(F)F)C(N)=O)C)Cl", "project", "series", ".")
    print FluorineCount
