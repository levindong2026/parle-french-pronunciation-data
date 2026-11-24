import sys
import unicodedata
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))

from search_french_sounds import ipa_key, load_indexes, spelling_key


class SoundSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.by_spelling, cls.by_ipa = load_indexes(ROOT / "french-sound-chart.csv")

    def spell(self, value):
        return [row["ipa"] for row in self.by_spelling[spelling_key(value)]]

    def test_canonically_equivalent_written_queries_match(self):
        self.assertEqual(self.spell("É"), ["/e/"])
        self.assertEqual(self.spell("e\u0301"), ["/e/"])

    def test_spelling_diacritics_and_multiple_matches_are_preserved(self):
        self.assertEqual(self.spell("ou"), ["/u/", "/w/"])
        self.assertEqual(self.spell("où"), ["/u/"])
        self.assertEqual(self.spell("o"), ["/o/", "/ɔ/"])

    def test_ipa_nasal_vowels_do_not_collapse_into_oral_vowels(self):
        for nasal, oral, nasal_example, oral_example in (
            ("/ɛ̃/", "/ɛ/", "vin", "mère"),
            ("/ɔ̃/", "/ɔ/", "bon", "porte"),
        ):
            with self.subTest(nasal=nasal, oral=oral):
                dropped_marks = "".join(
                    char
                    for char in unicodedata.normalize("NFD", nasal)
                    if unicodedata.category(char) != "Mn"
                )
                self.assertEqual(dropped_marks, oral)
                self.assertNotEqual(ipa_key(nasal), ipa_key(oral))
                self.assertIn(nasal_example, self.by_ipa[ipa_key(nasal)]["example_words"])
                self.assertIn(oral_example, self.by_ipa[ipa_key(oral)]["example_words"])

    def test_ipa_canonical_form_preserves_the_archived_labels(self):
        self.assertEqual(len(self.by_ipa), 35)
        self.assertIn(ipa_key("/ɑ̃/"), self.by_ipa)
        self.assertNotIn(ipa_key("/ɑ/"), self.by_ipa)
