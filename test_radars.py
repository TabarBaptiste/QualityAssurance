import unittest
import pandas as pd

# Chemin vers le fichier csv
PATH = "data/jeu-de-donnees-liste-des-radars-fixes-en-france-2024-.csv"

class TestChargementFichier(unittest.TestCase):
    def test_chargement_csv(self):
        """Test si le fichier CSV peut être chargé sans erreur."""
        try:
            df = pd.read_csv(PATH, sep=";", encoding="ISO-8859-1")
            self.assertFalse(df.empty, "Le fichier CSV est vide.")
        except Exception as e:
            self.fail(f"Erreur lors du chargement du fichier CSV : {e}")

class TestValeursFichier(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv(PATH, sep=";", encoding="ISO-8859-1")

    def test_latitude_valide(self):
        """Test si toutes les latitudes sont comprises entre -90 et 90 degrés."""
        self.assertTrue(self.df["Latitude"].between(-90, 90).all(), "Certaines latitudes sont hors limites.")

    def test_longitude_valide(self):
        """Test si toutes les longitudes sont comprises entre -180 et 180 degrés."""
        self.assertTrue(self.df["Longitude"].between(-180, 180).all(), "Certaines longitudes sont hors limites.")


class TestStructureFichier(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv(PATH, sep=";", encoding="ISO-8859-1")

    def test_colonnes_existantes(self):
        """Vérifie que les colonnes attendues sont présentes dans le fichier CSV."""
        colonnes_attendues = [
            "Numéro de radar",
            "Latitude",
            "Longitude",
            "VMA"
        ]
        for col in colonnes_attendues:
            self.assertIn(col, self.df.columns, f"Colonne manquante : {col}")

if __name__ == "__main__":
    unittest.main(verbosity=2)