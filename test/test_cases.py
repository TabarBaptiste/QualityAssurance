# tests/test_cases.py
import unittest
import os
import pandas as pd

class TestRadarCSV(unittest.TestCase):
    FILE_PATH = 'data/covid.csv'
    HEADERS_REFERENCE = ['fra;jour;clage_90;PourAvec;tx_indic_7J_DC;tx_indic_7J_hosp;tx_indic_7J_SC;tx_prev_hosp;tx_prev_SC']

    #* 1. Test si le fichier CSV existe et est lisible
    def test_file_exists_and_readable(self):
        self.assertTrue(os.path.exists(self.FILE_PATH), "Le fichier CSV n'existe pas.")
        self.assertTrue(os.access(self.FILE_PATH, os.R_OK), "Le fichier CSV n'est pas lisible.")

    #* 2. Test si le fichier CSV contient les en-têtes attendues (variable HEADERS_REFERENCE)
    def test_csv_headers(self):
        df = pd.read_csv(self.FILE_PATH, encoding='ISO-8859-1')
        headers = list(df.columns)
        self.assertTrue(len(headers) > 0, "Le fichier ne contient aucune colonne.")

        # Vérifie si les en-têtes attendues sont bien présentes
        for header in self.HEADERS_REFERENCE:
            self.assertIn(header, headers, f"L'en-tête '{header}' est manquante.")

    #* 3. Test si le fichier CSV contient des en-têtes inconnues
    def test_unknown_headers_display(self):
        df = pd.read_csv(self.FILE_PATH)
        headers = list(df.columns)
        unknown_headers = [h for h in headers if h not in self.HEADERS_REFERENCE]

        if unknown_headers:
            last = unknown_headers[-1]
            index = headers.index(last)
            excel_letter = chr(ord('A') + index)
            print(f"Dernière colonne non spécifiée : {last} (Colonne {excel_letter})")

# if __name__ == '__main__':
#     unittest.main()
