from rdkit.Chem import Descriptors
from rdkit import Chem


def AtomCount(ID, smiles, project, series, CHEMICSMODELDIR):
    """
    Total number of atoms including H
    """
    mol = Chem.MolFromSmiles(str(smiles))
    mol2 = Chem.AddHs(mol)
    AtomCount = mol2.GetNumAtoms()
    confidence = "NaN"
    return AtomCount, confidence

if __name__ == "__main__":
    AtomCount, confidence = AtomCount("MyMol", "CCO", "project", "series", ".")
    print AtomCount
