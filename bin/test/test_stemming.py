import unittest

from stemming import stem

class TestStemming(unittest.TestCase):

    def test_stem(self):
        words = [
            'aufeinander',
            'aufeinanderbiss',
            'aufeinanderfolge',
            'aufeinanderfolgen',
            'aufeinanderfolgend',
            'aufeinanderfolgende',
            'aufeinanderfolgenden',
            'aufeinanderfolgender',
            'aufeinanderfolgt',
            'Käufer',
            'Kätzchen',
            'katholischer',
            'auffallen',
            'auffallend',
            'auffallenden',
            'auffallender',
            'auffällig',
            'auffälligen',
            'auffälliges'
            
        ]
        stems = [
            'aufeinand',
            'aufeinanderbiss',
            'aufeinanderfolg',
            'aufeinanderfolg',
            'aufeinanderfolg',
            'aufeinanderfolg',
            'aufeinanderfolg',
            'aufeinanderfolg',
            'aufeinanderfolgt',
            'kauf',
            'katzch',
            'kathol',
            'auffall',
            'auffall',
            'auffall',
            'auffall',
            'auffall',
            'auffall',
            'auffall'
        ]
        results = [stem(word) for word in words]
        self.assertEqual(results, stems)


if __name__ == '__main__':
    unittest.main()