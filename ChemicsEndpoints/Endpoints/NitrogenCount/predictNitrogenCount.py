from rdkit.Chem import Descriptors
from rdkit import Chem


def NitrogenCount(ID, smiles, project, series, CHEMICSMODELDIR):
    """
    Total number of N
    """

    fragStr = "N"
    mol = Chem.MolFromSmiles(fragStr)
    sma = Chem.MolToSmarts(mol)
    matchIdx = Chem.QuickSmartsMatch(smiles, sma)
    NitrogenCount = len(matchIdx)
    confidence = "NaN"
    return NitrogenCount, confidence

if __name__ == "__main__":
    NitrogenCount, confidence = NitrogenCount("MyMol", "c1(cc(c(cc1)Oc1c(ncc(c1)C(F)(F)F)C(N)=O)C)Cl", "project", "series", ".")
    print NitrogenCount
