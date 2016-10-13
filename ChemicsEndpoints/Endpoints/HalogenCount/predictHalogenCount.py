from rdkit.Chem import Descriptors
from rdkit import Chem


def HalogenCount(ID, smiles, project, series, CHEMICSMODELDIR):
    """
    Total number of halogen atoms
    """
    mol = Chem.MolFromSmiles(str(smiles))
    HalogenCount = Descriptors.fr_halogen(mol)
    confidence = "NaN"
    return HalogenCount, confidence

if __name__ == "__main__":
    HalogenCount, confidence = HalogenCount("MyMol", "c1(cc(c(cc1)Oc1c(ncc(c1)C(F)(F)F)C(N)=O)C)Cl", "project", "series", ".")
    print HalogenCount
