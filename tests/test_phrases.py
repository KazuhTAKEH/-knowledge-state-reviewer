import unittest

from ksr.phrases import extract_candidate_phrases


class PhraseExtractionTests(unittest.TestCase):
    def test_extracts_keyword_windows(self):
        phrases = extract_candidate_phrases(
            "Pythonの関数はdefで定義し、returnで結果を返します。"
        )

        self.assertTrue(any("関数" in phrase for phrase in phrases))
        self.assertTrue(any("return" in phrase for phrase in phrases))

    def test_extracts_condition_keyword_windows(self):
        phrases = extract_candidate_phrases("if文は条件分岐をする役割を持ちます。")

        self.assertTrue(any("条件分岐" in phrase for phrase in phrases))


if __name__ == "__main__":
    unittest.main()
