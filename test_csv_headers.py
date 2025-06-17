import unittest
import os
import csv

class TestFichierCSV(unittest.TestCase):

    def setUp(self):
        """Prépare le chemin du fichier avant chaque test"""
        self.chemin_fichier = 'data/fichier.csv'

    def test_fichier_existe_et_lisible(self):
        """Vérifie que le fichier CSV existe et peut être lu"""
        self.assertTrue(os.path.isfile(self.chemin_fichier), "Fichier introuvable")
        self.assertTrue(os.access(self.chemin_fichier, os.R_OK), "Fichier non lisible")

    def test_headers_csv(self):
        """Vérifie la présence et le contenu des en-têtes du fichier CSV"""
        with open(self.chemin_fichier, newline='', encoding='utf-8') as fichier:
            lecteur = csv.reader(fichier)
            headers = next(lecteur)  # On lit la première ligne (les en-têtes)

        # On peut afficher les headers pour les tester manuellement
        print("En-têtes du fichier :", headers)

        # Test minimal : il y a des en-têtes
        self.assertGreater(len(headers), 0, "Aucune en-tête détectée dans le fichier CSV")

        # Test plus précis (si on connaît les en-têtes attendues)
        # en_tetes_attendues = [
        #     "nom_departement", "id_radar", "latitude", "longitude", "vitesse", "route", "sens"
        # ]
        # for entete in en_tetes_attendues:
        #     self.assertIn(entete, headers, f"En-tête manquante : {entete}")

# if __name__ == '__main__':
#     unittest.main()