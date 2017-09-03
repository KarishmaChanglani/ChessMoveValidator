import unittest
from movegenerator import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    getColAndRow('A4')
    unittest.main()
