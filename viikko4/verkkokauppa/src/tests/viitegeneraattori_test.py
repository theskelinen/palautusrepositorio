import unittest
from viitegeneraattori import Viitegeneraattori


class TestViitegeneraattoriUnit(unittest.TestCase):
    def test_uusi_kasvaa(self):
        viitegeneraattori = Viitegeneraattori()
        self.assertEqual(viitegeneraattori.uusi(), 2)
        self.assertEqual(viitegeneraattori.uusi(), 3)
