# test_cases.py
import unittest

# Une fonction simple à tester
def addition(a, b):
    return a + b

def division(a, b):
    if b == 0:
        raise ValueError("Division par zéro")
    return a / b

# Définition de la classe de test
class TestMathFunctions(unittest.TestCase):

    def test_addition(self):
        """Test de la fonction addition"""
        self.assertEqual(addition(2, 3), 5)
        self.assertEqual(addition(-1, 1), 0)

    def test_division(self):
        """Test de la fonction division"""
        self.assertEqual(division(10, 2), 5.0)
        self.assertAlmostEqual(division(1, 3), 0.333333, places=5)

    def test_division_by_zero(self):
        """Vérifie qu'une division par zéro soulève une exception"""
        with self.assertRaises(ValueError):
            division(5, 0)

# Si on lance ce fichier directement, les tests seront exécutés
if __name__ == '__main__':
    unittest.main()
