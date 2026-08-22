import unittest

from ksr.phrases import extract_candidate_phrases


class PhraseExtractionTests(unittest.TestCase):
    def test_extracts_keyword_windows(self):
        phrases = extract_candidate_phrases(
            "Pythonの関数はdefで定義し、returnで結果を返します。"
        )

        self.assertTrue(any("関数" in phrase for phrase in phrases))
        self.assertTrue(any("return" in phrase for phrase in phrases))


if __name__ == "__main__":
    unittest.main()
