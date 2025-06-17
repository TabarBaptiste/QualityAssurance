# Qualité, tests et maintenances pour application wb

## Auteurs

- Harena ANDRIAMANANJARA MANDIMBY
- Andil ABAYOMI
- Elhadj Ibrahima BAH
- Baptiste TABAR LABONNE

---

Voici une description claire et bien structurée que tu peux coller en haut de chaque fichier pour servir de **documentation**. Elle explique **ce que fait chaque fichier**, **le but des tests**, et **les décisions techniques importantes** (comme l'encodage).

---

### 📝 `tests/test_cases.py`

Fichier : test_cases.py
But : Définir les différents cas de test (TestCase) liés à l’analyse d’un fichier CSV.

Fonctionnalités testées :

1. Vérifie que le fichier 'data/covid.csv' existe et est lisible.
2. Lit le fichier CSV avec l'encodage 'ISO-8859-1' (utile pour les caractères accentués).
3. Vérifie que certaines en-têtes de colonne attendues sont bien présentes (définies dans HEADERS_REFERENCE).
4. Affiche la dernière en-tête inconnue (non spécifiée dans HEADERS_REFERENCE) et sa position dans le fichier (sous forme de lettre Excel).

Notes techniques :

- Utilise la bibliothèque `pandas` pour lire le fichier CSV.
- Le fichier est lu avec l’encodage `ISO-8859-1` pour éviter les erreurs dues à des caractères accentués mal interprétés.
- Tous les tests sont regroupés dans une classe `TestRadarCSV` héritant de `unittest.TestCase`.

Pré-requis :

- Fichier CSV existant à l'emplacement `data/covid.csv`.
- La bibliothèque `pandas` doit être installée.

---

### 📝 `tests/test_suite.py`

Fichier : test_suite.py
But : Regrouper les cas de test définis dans test_cases.py dans une suite de tests unifiée.

Contenu :

- Importe la classe de test `TestRadarCSV` depuis test_cases.py.
- Définit une fonction `suite()` qui retourne une `unittest.TestSuite` contenant tous les tests.

Utilisation :
Ce fichier est importé par test_runner.py pour exécuter tous les tests définis dans test_cases.py.

---

### 📝 `tests/test_runner.py`

Fichier : test_runner.py
But : Exécuter la suite de tests définie dans test_suite.py.

Contenu :

- Importe la fonction `suite()` depuis test_suite.py.
- Utilise `unittest.TextTestRunner` pour exécuter les tests avec un niveau de verbosité 2 (affichage détaillé).

Utilisation :
Lancer ce fichier exécute automatiquement tous les tests unitaires définis dans test_cases.py.
