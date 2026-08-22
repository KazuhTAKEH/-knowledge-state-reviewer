from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
import math
import re
from typing import Protocol


@dataclass(frozen=True)
class ConceptCandidate:
    concept_id: str
    label: str
    description: str = ""


@dataclass(frozen=True)
class AlignmentResult:
    input_phrase: str
    concept_id: str
    label: str
    score: float
    method: str


class ConceptAligner(Protocol):
    def align(
        self,
        input_phrases: list[str],
        candidates: list[ConceptCandidate],
        threshold: float = 0.55,
    ) -> list[AlignmentResult]:
        ...


class LexicalConceptAligner:
    """Dependency-free fallback for concept alignment."""

    def align(
        self,
        input_phrases: list[str],
        candidates: list[ConceptCandidate],
        threshold: float = 0.55,
    ) -> list[AlignmentResult]:
        results: list[AlignmentResult] = []
        for phrase in input_phrases:
            best: AlignmentResult | None = None
            for candidate in candidates:
                score = self._score(phrase, candidate)
                if score >= threshold and (best is None or score > best.score):
                    best = AlignmentResult(
                        input_phrase=phrase,
                        concept_id=candidate.concept_id,
                        label=candidate.label,
                        score=round(score, 4),
                        method="lexical",
                    )
            if best is not None:
                results.append(best)
        return results

    def _score(self, phrase: str, candidate: ConceptCandidate) -> float:
        left = self._normalize(phrase)
        right = self._normalize(candidate.label + " " + candidate.description)
        if not left or not right:
            return 0.0
        exact = 1.0 if left in right or right in left else 0.0
        ratio = SequenceMatcher(None, left, right).ratio()
        overlap = self._token_overlap(left, right)
        return max(exact, ratio, overlap)

    def _normalize(self, text: str) -> str:
        return re.sub(r"\s+", " ", text.lower()).strip()

    def _token_overlap(self, left: str, right: str) -> float:
        a = set(re.findall(r"[\w一-龥ぁ-んァ-ン]+", left))
        b = set(re.findall(r"[\w一-龥ぁ-んァ-ン]+", right))
        if not a or not b:
            return 0.0
        return len(a & b) / math.sqrt(len(a) * len(b))


class SentenceTransformerConceptAligner:
    """Optional BERT/SentenceTransformer-based aligner for Colab/local GPU."""

    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "sentence-transformers is required. Install requirements-colab.txt "
                "or fall back to LexicalConceptAligner."
            ) from exc
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    def align(
        self,
        input_phrases: list[str],
        candidates: list[ConceptCandidate],
        threshold: float = 0.55,
    ) -> list[AlignmentResult]:
        if not input_phrases or not candidates:
            return []

        candidate_texts = [
            f"{candidate.label}. {candidate.description}".strip()
            for candidate in candidates
        ]
        phrase_embeddings = self.model.encode(input_phrases, normalize_embeddings=True)
        candidate_embeddings = self.model.encode(candidate_texts, normalize_embeddings=True)

        results: list[AlignmentResult] = []
        for phrase, phrase_embedding in zip(input_phrases, phrase_embeddings):
            scores = candidate_embeddings @ phrase_embedding
            best_index = int(scores.argmax())
            best_score = float(scores[best_index])
            if best_score >= threshold:
                candidate = candidates[best_index]
                results.append(
                    AlignmentResult(
                        input_phrase=phrase,
                        concept_id=candidate.concept_id,
                        label=candidate.label,
                        score=round(best_score, 4),
                        method=f"sentence-transformers:{self.model_name}",
                    )
                )
        return results
