from rdkit.Chem import Descriptors
from rdkit import Chem


def MolWt(ID, smiles, project, series, CHEMICSMODELDIR):
    mol = Chem.MolFromSmiles(str(smiles))
    MolWt = Descriptors.MolWt(mol)
    confidence = "NaN"
    return MolWt, confidence

if __name__ == "__main__":
    print "Not doing anything!"
