from __future__ import annotations

from dataclasses import dataclass

from ksr.analysis import ArtifactAnalysis
from ksr.knowledge import KnowledgeState


@dataclass(frozen=True)
class ConceptGap:
    concept: str
    mastery: float
    severity: str
    reason: str


class GapModel:
    def estimate(self, analysis: ArtifactAnalysis, state: KnowledgeState) -> list[ConceptGap]:
        gaps: list[ConceptGap] = []
        for concept in sorted(analysis.concepts):
            mastery = state.mastery(concept, default=0.35)
            if mastery < 0.25:
                severity = "high"
            elif mastery < 0.55:
                severity = "medium"
            else:
                continue
            gaps.append(
                ConceptGap(
                    concept=concept,
                    mastery=mastery,
                    severity=severity,
                    reason=f"{concept} is required by the artifact, but mastery is {mastery:.2f}.",
                )
            )
        return gaps
