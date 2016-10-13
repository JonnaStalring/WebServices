from rdkit.Chem import Descriptors
from rdkit import Chem


def BondCount(ID, smiles, project, series, CHEMICSMODELDIR):
    """
    Total number of bonds excluding H
    """
    mol = Chem.MolFromSmiles(str(smiles))
    BondCount = mol.GetNumBonds(onlyHeavy=True)
    confidence = "NaN"
    return BondCount, confidence

if __name__ == "__main__":
    BondCount, confidence = BondCount("MyMol", "CCO", "project", "series", ".")
    print BondCount
