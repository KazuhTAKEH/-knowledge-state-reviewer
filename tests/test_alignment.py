import unittest

from ksr.alignment import ConceptCandidate, LexicalConceptAligner


class AlignmentTests(unittest.TestCase):
    def test_lexical_aligner_maps_phrase_to_candidate(self):
        aligner = LexicalConceptAligner()
        results = aligner.align(
            input_phrases=["returnで結果を返す"],
            candidates=[
                ConceptCandidate(
                    concept_id="return_value",
                    label="戻り値 return",
                    description="関数の処理結果を返す仕組み",
                )
            ],
            threshold=0.2,
        )

        self.assertEqual(results[0].concept_id, "return_value")


if __name__ == "__main__":
    unittest.main()
