from rdkit.Chem import Descriptors
from rdkit import Chem


def RingCount(ID, smiles, project, series, CHEMICSMODELDIR):
    mol = Chem.MolFromSmiles(str(smiles))
    RingCount = Descriptors.RingCount(mol)
    confidence = "NaN"
    return RingCount, confidence

if __name__ == "__main__":
    print "Not doing anything!"
