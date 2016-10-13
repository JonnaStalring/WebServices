from rdkit.Chem import Descriptors
from rdkit import Chem


def SMILES(ID, smiles, project, series, CHEMICSMODELDIR):
    """
    Retrun canonical smiles
    """

    mol = Chem.MolFromSmiles(smiles)
    SMILES = Chem.MolToSmiles(mol)
    confidence = "NaN"
    return SMILES, confidence

if __name__ == "__main__":
    SMILES, confidence = SMILES("MyMol", "c1(cc(c(cc1)Oc1c(ncc(c1)C(F)(F)F)C(N)=O)C)Cl", "project", "series", ".")
    print SMILES
