from rdkit.Chem import Descriptors
from rdkit import Chem


def HeavyAtomCount(ID, smiles, project, series, CHEMICSMODELDIR):
    mol = Chem.MolFromSmiles(str(smiles))
    HeavyAtomCount = Descriptors.HeavyAtomCount(mol)
    confidence = "NaN"
    return HeavyAtomCount, confidence

if __name__ == "__main__":
    print "Not doing anything!"
