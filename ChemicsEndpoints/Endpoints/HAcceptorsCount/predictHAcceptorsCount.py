from rdkit.Chem import Descriptors
from rdkit import Chem


def HAcceptorsCount(ID, smiles, project, series, CHEMICSMODELDIR):
    mol = Chem.MolFromSmiles(str(smiles))
    NumHAcceptors = Descriptors.NumHAcceptors(mol)
    confidence = "NaN"
    return NumHAcceptors, confidence

if __name__ == "__main__":
    print "Not doing anything!"
