from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class KnowledgeState:
    """Observable learner/reviewer knowledge state."""

    learner_level: str
    concept_mastery: dict[str, float]
    misconceptions: list[str] = field(default_factory=list)
    traits: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "KnowledgeState":
        return cls(
            learner_level=str(data.get("learner_level", "unknown")),
            concept_mastery={
                str(key): float(value)
                for key, value in data.get("concept_mastery", {}).items()
            },
            misconceptions=[str(item) for item in data.get("misconceptions", [])],
            traits=dict(data.get("traits", {})),
        )

    @classmethod
    def from_json(cls, path: str | Path) -> "KnowledgeState":
        with Path(path).open("r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    def mastery(self, concept: str, default: float = 0.0) -> float:
        return max(0.0, min(1.0, self.concept_mastery.get(concept, default)))

    def weak_concepts(self, threshold: float = 0.45) -> list[str]:
        return [
            concept
            for concept, score in sorted(self.concept_mastery.items())
            if score < threshold
        ]


@dataclass(frozen=True)
class ReviewerProfile:
    knowledge_state: KnowledgeState
    feedback_directness: str = "medium"
    scaffolding: str = "high"
    give_answer: bool = False

    @classmethod
    def from_json(cls, path: str | Path) -> "ReviewerProfile":
        with Path(path).open("r", encoding="utf-8") as f:
            data = json.load(f)
        state = KnowledgeState.from_dict(data)
        style = data.get("feedback_style", {})
        return cls(
            knowledge_state=state,
            feedback_directness=str(style.get("directness", "medium")),
            scaffolding=str(style.get("scaffolding", "high")),
            give_answer=bool(style.get("give_answer", False)),
        )
