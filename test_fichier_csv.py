import unittest
import os

class TestFichierCSV(unittest.TestCase):

    def test_fichier_existe_et_lisible(self):
        """Vérifie que le fichier CSV existe et peut être lu"""

        # Chemin relatif vers le fichier
        chemin_fichier = 'data/fichier.csv'

        # Vérifie que le fichier existe
        self.assertTrue(os.path.isfile(chemin_fichier), f"Le fichier {chemin_fichier} n'existe pas.")

        # Vérifie que le fichier est lisible (droits de lecture)
        self.assertTrue(os.access(chemin_fichier, os.R_OK), f"Le fichier {chemin_fichier} n'est pas lisible.")

if __name__ == '__main__':
    unittest.main()