from __future__ import annotations

from dataclasses import asdict, dataclass
import json

from ksr.analysis import ArtifactAnalysis
from ksr.gap import ConceptGap
from ksr.knowledge import ReviewerProfile


@dataclass(frozen=True)
class DialogueTurn:
    speaker: str
    text: str


@dataclass(frozen=True)
class DialoguePlanItem:
    concept: str
    severity: str
    mastery: float
    student_intent: str
    teacher_strategy: str
    consistency_rule: str


@dataclass(frozen=True)
class DialoguePlan:
    learner_level: str
    artifact_type: str
    items: list[DialoguePlanItem]
    policy_notes: list[str]

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2) + "\n"


@dataclass(frozen=True)
class DialogueResult:
    turns: list[DialogueTurn]
    teacher_review: list[str]
    plan: DialoguePlan

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
        plan = self.plan(analysis, gaps, profile)
        turns: list[DialogueTurn] = []
        intro = self._compact(monologue)
        turns.append(DialogueTurn("先生", intro))

        if not plan.items:
            turns.append(DialogueTurn("生徒", "だいたい分かりました。自分で確認するとしたら、どこを見るとよいですか？"))
            turns.append(DialogueTurn("先生", "まず大事な語を1つ選んで、自分の言葉で説明してみましょう。"))
        else:
            for item in plan.items:
                turns.append(DialogueTurn("生徒", self._student_question(item, profile)))
                turns.append(DialogueTurn("先生", self._teacher_response(item, profile)))

        teacher_review = [
            "説明は、生徒の弱い概念を先に確認してから進める必要があります。",
            "教師役は完成文を渡すより、短い再記述課題を挟む方が自律修正につながります。",
        ]
        for item in plan.items:
            teacher_review.append(
                f"`{item.concept}` について、理解確認の問いを1つ追加してください。"
            )
        return DialogueResult(turns=turns, teacher_review=teacher_review, plan=plan)

    def plan(
        self,
        analysis: ArtifactAnalysis,
        gaps: list[ConceptGap],
        profile: ReviewerProfile,
    ) -> DialoguePlan:
        items = [
            DialoguePlanItem(
                concept=gap.concept,
                severity=gap.severity,
                mastery=round(gap.mastery, 4),
                student_intent=self._student_intent(gap),
                teacher_strategy=self._teacher_strategy(gap, profile),
                consistency_rule=self._consistency_rule(gap),
            )
            for gap in gaps[:4]
        ]
        notes = [
            "Input may vary, but planned student reactions must follow the learner state.",
            "Teacher responses should scaffold before giving final answers.",
        ]
        if profile.give_answer:
            notes.append("Profile allows more direct answers; monitor over-answering risk.")
        return DialoguePlan(
            learner_level=profile.knowledge_state.learner_level,
            artifact_type=analysis.artifact_type,
            items=items,
            policy_notes=notes,
        )

    def _compact(self, monologue: str) -> str:
        text = " ".join(line.strip() for line in monologue.splitlines() if line.strip())
        return text[:180] + ("..." if len(text) > 180 else "")

    def _student_question(self, item: DialoguePlanItem, profile: ReviewerProfile) -> str:
        level = profile.knowledge_state.learner_level
        if item.student_intent == "ask_basic_meaning":
            return f"{level} の自分には、`{item.concept}` が急に出てきた感じがします。何を表しているんですか？"
        return f"`{item.concept}` は何となく分かるのですが、この説明の中ではどこに効いていますか？"

    def _teacher_response(self, item: DialoguePlanItem, profile: ReviewerProfile) -> str:
        if profile.give_answer:
            return f"`{item.concept}` の要点を明示してから、本文の該当箇所に結びつけます。"
        return f"まず `{item.concept}` が使われている箇所を一緒に探しましょう。その後、自分の言葉で一文にしてみてください。"

    def _student_intent(self, gap: ConceptGap) -> str:
        if gap.severity == "high":
            return "ask_basic_meaning"
        return "ask_contextual_role"

    def _teacher_strategy(self, gap: ConceptGap, profile: ReviewerProfile) -> str:
        if profile.give_answer:
            return "explain_then_ground_in_text"
        if gap.severity == "high":
            return "locate_term_then_student_rephrase"
        return "contextual_check_question"

    def _consistency_rule(self, gap: ConceptGap) -> str:
        if gap.severity == "high":
            return "student must not use the concept as if already mastered"
        return "student may show partial familiarity but should ask for contextual grounding"
