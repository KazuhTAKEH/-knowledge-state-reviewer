from __future__ import annotations

from dataclasses import dataclass

from ksr.analysis import ArtifactAnalysis
from ksr.gap import ConceptGap
from ksr.knowledge import ReviewerProfile


@dataclass(frozen=True)
class DialogueTurn:
    speaker: str
    text: str


@dataclass(frozen=True)
class DialogueResult:
    turns: list[DialogueTurn]
    teacher_review: list[str]

    def to_markdown(self) -> str:
        lines = ["# Dialogue Draft\n"]
        for turn in self.turns:
            lines.append(f"**{turn.speaker}:** {turn.text}\n")
        lines.append("\n## Teacher Explanation Review\n")
        lines.extend(f"- {item}\n" for item in self.teacher_review)
        return "\n".join(lines).strip() + "\n"


class DialogueConverter:
    def convert(
        self,
        monologue: str,
        analysis: ArtifactAnalysis,
        gaps: list[ConceptGap],
        profile: ReviewerProfile,
    ) -> DialogueResult:
        turns: list[DialogueTurn] = []
        intro = self._compact(monologue)
        turns.append(DialogueTurn("先生", intro))

        if not gaps:
            turns.append(DialogueTurn("生徒", "だいたい分かりました。自分で確認するとしたら、どこを見るとよいですか？"))
            turns.append(DialogueTurn("先生", "まず大事な語を1つ選んで、自分の言葉で説明してみましょう。"))
        else:
            for gap in gaps[:4]:
                turns.append(DialogueTurn("生徒", self._student_question(gap, profile)))
                turns.append(DialogueTurn("先生", self._teacher_response(gap, profile)))

        teacher_review = [
            "説明は、生徒の弱い概念を先に確認してから進める必要があります。",
            "教師役は完成文を渡すより、短い再記述課題を挟む方が自律修正につながります。",
        ]
        for gap in gaps:
            teacher_review.append(
                f"`{gap.concept}` について、理解確認の問いを1つ追加してください。"
            )
        return DialogueResult(turns=turns, teacher_review=teacher_review)

    def _compact(self, monologue: str) -> str:
        text = " ".join(line.strip() for line in monologue.splitlines() if line.strip())
        return text[:180] + ("..." if len(text) > 180 else "")

    def _student_question(self, gap: ConceptGap, profile: ReviewerProfile) -> str:
        level = profile.knowledge_state.learner_level
        if gap.severity == "high":
            return f"{level} の自分には、`{gap.concept}` が急に出てきた感じがします。何を表しているんですか？"
        return f"`{gap.concept}` は何となく分かるのですが、この説明の中ではどこに効いていますか？"

    def _teacher_response(self, gap: ConceptGap, profile: ReviewerProfile) -> str:
        if profile.give_answer:
            return f"`{gap.concept}` の要点を明示してから、本文の該当箇所に結びつけます。"
        return f"まず `{gap.concept}` が使われている箇所を一緒に探しましょう。その後、自分の言葉で一文にしてみてください。"
