from rdkit.Chem import Descriptors
from rdkit import Chem


def RotatableBondsCount(ID, smiles, project, series, CHEMICSMODELDIR):
    mol = Chem.MolFromSmiles(str(smiles))
    NumRotatableBonds = Descriptors.NumRotatableBonds(mol)
    confidence = "NaN"
    return NumRotatableBonds, confidence

if __name__ == "__main__":
    print "Not doing anything!"
