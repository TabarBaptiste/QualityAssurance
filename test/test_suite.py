import unittest
from test_cases import TestRadarCSV

# Fonction qui retourne la suite de tests (3 tests dans test_case.py)
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestRadarCSV))
    return suite

# if __name__ == '__main__':
#     unittest.main()