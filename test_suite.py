import unittest
from test_cases import TestMathFunctions  # On importe les tests définis dans test_cases.py

# Création manuelle de la suite de tests
def suite():
    suite = unittest.TestSuite()

    # On ajoute les méthodes de test spécifiques
    suite.addTest(TestMathFunctions("test_addition"))
    suite.addTest(TestMathFunctions("test_division"))
    suite.addTest(TestMathFunctions("test_division_by_zero"))

    return suite
