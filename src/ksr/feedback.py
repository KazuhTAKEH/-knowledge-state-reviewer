from __future__ import annotations

from dataclasses import dataclass

from ksr.analysis import ArtifactAnalysis
from ksr.gap import ConceptGap
from ksr.knowledge import ReviewerProfile


@dataclass(frozen=True)
class ReviewReport:
    summary: str
    questions: list[str]
    observations: list[str]
    revision_advice: list[str]
    risks: list[str]

    def to_markdown(self) -> str:
        parts = [f"# Review Report\n\n{self.summary}\n"]
        for title, items in [
            ("Questions", self.questions),
            ("Observations", self.observations),
            ("Revision Advice", self.revision_advice),
            ("Risks", self.risks),
        ]:
            parts.append(f"## {title}\n")
            parts.extend(f"- {item}\n" for item in items)
            parts.append("\n")
        return "".join(parts).strip() + "\n"


class FeedbackGenerator:
    def generate_report_feedback(
        self,
        text: str,
        analysis: ArtifactAnalysis,
        gaps: list[ConceptGap],
        profile: ReviewerProfile,
        rubric: dict[str, str] | None = None,
    ) -> ReviewReport:
        state = profile.knowledge_state
        questions = [
            self._question_for_gap(gap, analysis.artifact_type) for gap in gaps
        ] or ["この文章で一番伝えたい主張を、1文で言い直せますか？"]
        observations = [
            f"`{gap.concept}` の理解負荷が高い読者には、この箇所で説明が飛んで見える可能性があります。"
            for gap in gaps
        ]
        for misconception in state.misconceptions:
            observations.append(f"想定される誤解: {misconception}")

        revision_advice = [
            self._advice_for_gap(gap) for gap in gaps
        ] or ["段落ごとに「主張」「理由」「具体例」のどれを担っているかを確認してください。"]
        if rubric:
            revision_advice.append(
                "ルーブリック観点: "
                + ", ".join(f"{key}={value}" for key, value in rubric.items())
            )

        risks = []
        if profile.give_answer:
            risks.append("give_answer=true のため、学習者の自律修正を弱める可能性があります。")
        if not gaps:
            risks.append("現在の簡易分析では概念ギャップが少なく見えます。詳細な採点にはルーブリック拡張が必要です。")

        return ReviewReport(
            summary=f"{state.learner_level} レベルの知識状態を前提に、理解可能性と自律修正の観点から評価しました。",
            questions=questions,
            observations=observations,
            revision_advice=revision_advice,
            risks=risks,
        )

    def _question_for_gap(self, gap: ConceptGap, artifact_type: str) -> str:
        if artifact_type == "code":
            mapping = {
                "function": "この `def` は何をひとまとまりの処理として名前付けしていますか？",
                "return_value": "`return` された値は、その後どこで使われますか？",
                "loop": "この繰り返しは、何回・何に対して実行されますか？",
                "condition": "この条件分岐では、どの場合にどちらへ進みますか？",
            }
            return mapping.get(gap.concept, f"`{gap.concept}` が何を意味するか説明できますか？")
        mapping = {
            "claim": "この段落の主張は、どの1文ですか？",
            "evidence": "その主張を支える根拠は、本文中のどこにありますか？",
            "counterargument": "反対意見があるとしたら、どの点に向けられますか？",
            "conclusion": "結論は、本文で示した根拠から自然に出ていますか？",
        }
        return mapping.get(gap.concept, f"`{gap.concept}` を読者にどう伝えるか確認してください。")

    def _advice_for_gap(self, gap: ConceptGap) -> str:
        if gap.severity == "high":
            return f"`{gap.concept}` は前提知識が弱いので、定義か具体例を1つ足してから先に進ませてください。"
        return f"`{gap.concept}` は短い確認質問を入れると、自律的な修正につながります。"
