import unittest

from ksr.analysis import ArtifactAnalyzer
from ksr.gap import GapModel
from ksr.knowledge import KnowledgeState


class GapModelTests(unittest.TestCase):
    def test_gap_model_detects_low_mastery_concepts(self):
        analysis = ArtifactAnalyzer().analyze("def add(a, b):\n    return a + b\n", "code")
        state = KnowledgeState(
            learner_level="beginner",
            concept_mastery={"function": 0.2, "return_value": 0.1, "function_call": 0.8},
        )

        gaps = GapModel().estimate(analysis, state)
        names = {gap.concept for gap in gaps}

        self.assertIn("function", names)
        self.assertIn("return_value", names)


if __name__ == "__main__":
    unittest.main()
