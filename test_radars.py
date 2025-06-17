import unittest
import pandas as pd

# Chemin vers le fichier
PATH = "data/jeu-de-donnees-liste-des-radars-fixes-en-france-2024-.csv"

class TestChargementFichier(unittest.TestCase):
    def test_chargement_csv(self):
        """Test si le fichier CSV peut être chargé sans erreur."""
        try:
            df = pd.read_csv(PATH, sep=";", encoding="ISO-8859-1")
            self.assertFalse(df.empty, "Le fichier CSV est vide.")
        except Exception as e:
            self.fail(f"Erreur lors du chargement du fichier CSV : {e}")

class TestStructureFichier(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv(PATH, sep=";", encoding="ISO-8859-1")

    def test_colonnes_existantes(self):
        """Vérifie que les colonnes attendues sont présentes dans le fichier CSV."""
        colonnes_attendues = [
            "Numéro de radar ",
            "Latitude",
            "Longitude",
            "VMA"
        ]
        for col in colonnes_attendues:
            self.assertIn(col, self.df.columns, f"Colonne manquante : {col}")

if __name__ == "__main__":
    unittest.main(verbosity=2)