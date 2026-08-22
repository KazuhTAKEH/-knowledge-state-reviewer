import unittest

from ksr.analysis import ArtifactAnalyzer
from ksr.dialogue import DialogueConverter
from ksr.gap import GapModel
from ksr.knowledge import KnowledgeState, ReviewerProfile


class DialoguePlanTests(unittest.TestCase):
    def test_plan_exposes_state_conditioned_intermediate_decisions(self):
        text = "Pythonの関数はdefで定義し、returnで結果を返します。"
        profile = ReviewerProfile(
            knowledge_state=KnowledgeState(
                learner_level="beginner_python",
                concept_mastery={"function": 0.2, "return_value": 0.1},
            )
        )
        analysis = ArtifactAnalyzer().analyze(text, artifact_type="text")
        gaps = GapModel().estimate(analysis, profile.knowledge_state)

        result = DialogueConverter().convert(text, analysis, gaps, profile)
        concepts = {item.concept for item in result.plan.items}
        intents = {item.student_intent for item in result.plan.items}

        self.assertIn("function", concepts)
        self.assertIn("return_value", concepts)
        self.assertIn("ask_basic_meaning", intents)


if __name__ == "__main__":
    unittest.main()
