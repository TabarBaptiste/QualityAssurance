import unittest
from test_suite import suite

# Exécuter la suite de tests (3 tests dans test_suite.py qui appel lui même test_cases.py)
if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
