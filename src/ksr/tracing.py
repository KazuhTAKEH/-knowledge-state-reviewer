from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ksr.knowledge import KnowledgeState


@dataclass(frozen=True)
class Interaction:
    concept: str
    correct: bool
    error_type: str | None = None


class KnowledgeTracer(ABC):
    """Adapter boundary for DKT/pyKT/Code-DKT integrations."""

    @abstractmethod
    def update(self, state: KnowledgeState, interactions: list[Interaction]) -> KnowledgeState:
        raise NotImplementedError


class NoOpKnowledgeTracer(KnowledgeTracer):
    def update(self, state: KnowledgeState, interactions: list[Interaction]) -> KnowledgeState:
        return state
