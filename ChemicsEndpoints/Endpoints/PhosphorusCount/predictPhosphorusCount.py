from rdkit.Chem import Descriptors
from rdkit import Chem


def PhosphorusCount(ID, smiles, project, series, CHEMICSMODELDIR):
    """
    Total number of phosphor
    """

    fragStr = "P"
    mol = Chem.MolFromSmiles(fragStr)
    sma = Chem.MolToSmarts(mol)
    matchIdx = Chem.QuickSmartsMatch(smiles, sma)
    PhosphorCount = len(matchIdx)
    confidence = "NaN"
    return PhosphorCount, confidence

if __name__ == "__main__":
    PhosphorCount, confidence = PhosphorusCount("MyMol", "c1(cc(c(cc1)Oc1c(ncc(c1)C(F)(F)F)C(N)=O)C)Cl", "project", "series", ".")
    print PhosphorCount
