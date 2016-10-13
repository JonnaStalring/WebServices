from rdkit.Chem import Descriptors
from rdkit import Chem


def ChlorineCount(ID, smiles, project, series, CHEMICSMODELDIR):
    """
    Total number of Cl
    """

    fragStr = "Cl"
    mol = Chem.MolFromSmiles(fragStr)
    sma = Chem.MolToSmarts(mol)
    matchIdx = Chem.QuickSmartsMatch(smiles, sma)
    ChlorineCount = len(matchIdx)
    confidence = "NaN"
    return ChlorineCount, confidence

if __name__ == "__main__":
    ChlorineCount, confidence = ChlorineCount("MyMol", "c1(cc(c(cc1)Oc1c(ncc(c1)C(F)(F)F)C(N)=O)C)Cl", "project", "series", ".")
    print ChlorineCount
