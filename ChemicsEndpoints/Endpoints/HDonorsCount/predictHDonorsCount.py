from rdkit.Chem import Descriptors
from rdkit import Chem


def HDonorsCount(ID, smiles, project, series, CHEMICSMODELDIR):
    mol = Chem.MolFromSmiles(str(smiles))
    NumHDonors = Descriptors.NumHDonors(mol)
    confidence = "NaN"
    return NumHDonors, confidence

if __name__ == "__main__":
    print "Not doing anything!"
