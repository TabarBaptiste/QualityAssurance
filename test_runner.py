# test_runner.py
import unittest
from test_suite import suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)  # Affiche plus de détails pendant l'exécution
    test_suite = suite()  # Récupère la suite de tests
    runner.run(test_suite)
