from rdkit.Chem import Descriptors
from rdkit import Chem


def TPSA(ID, smiles, project, series, CHEMICSMODELDIR):
    mol = Chem.MolFromSmiles(str(smiles))
    TPSA = Descriptors.TPSA(mol)
    confidence = "NaN"
    return TPSA, confidence

if __name__ == "__main__":
    print "Not doing anything!"
