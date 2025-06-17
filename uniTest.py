import unittest

def add(a, b):
    return a + b

class TestAddFunctionSimple(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)

class MyTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super().run(test)
        print(f"Total des tests: {result.testsRun}, Erreurs: {len(result.errors)}, Echecs : {len(result.failures)}")
        return result

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAddFunctionSimple)
    MyTestRunner().run(suite)
