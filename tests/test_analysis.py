import unittest

from ksr.analysis import ArtifactAnalyzer


class AnalysisTests(unittest.TestCase):
    def test_text_analysis_detects_condition_explanation(self):
        analysis = ArtifactAnalyzer().analyze(
            "if文は条件分岐をする役割を持ちます。",
            artifact_type="text",
        )

        self.assertIn("condition", analysis.concepts)


if __name__ == "__main__":
    unittest.main()
