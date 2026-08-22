from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ksr.alignment import (  # noqa: E402
    ConceptCandidate,
    LexicalConceptAligner,
    SentenceTransformerConceptAligner,
)
from ksr.analysis import ArtifactAnalysis, ArtifactAnalyzer  # noqa: E402
from ksr.dialogue import DialogueConverter  # noqa: E402
from ksr.gap import GapModel  # noqa: E402
from ksr.knowledge import ReviewerProfile  # noqa: E402
from ksr.phrases import extract_candidate_phrases  # noqa: E402


def load_concepts(path: Path) -> list[ConceptCandidate]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [ConceptCandidate(**item) for item in data]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to experiment config JSON.")
    parser.add_argument("--input", help="Path to monologue text.")
    parser.add_argument("--profile", default="examples/profiles/beginner_python.json")
    parser.add_argument("--concepts", default="examples/concepts/python_basic.json")
    parser.add_argument("--bert", action="store_true")
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--output-dir", default="colab_outputs")
    args = parser.parse_args()
    if args.config:
        config = json.loads((ROOT / args.config).read_text(encoding="utf-8"))
        args.input = config["input"]
        args.profile = config.get("profile", args.profile)
        args.concepts = config.get("concepts", args.concepts)
        args.bert = bool(config.get("use_bert", args.bert))
        args.threshold = config.get("threshold", args.threshold)
        args.output_dir = config.get("output_dir", args.output_dir)
    if not args.input:
        parser.error("--input is required unless --config is provided")

    input_path = ROOT / args.input
    profile_path = ROOT / args.profile
    concepts_path = ROOT / args.concepts
    output_dir = ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    text = input_path.read_text(encoding="utf-8")
    profile = ReviewerProfile.from_json(profile_path)
    concepts = load_concepts(concepts_path)
    phrases = extract_candidate_phrases(text)

    if args.bert:
        aligner = SentenceTransformerConceptAligner()
        threshold = 0.4 if args.threshold is None else args.threshold
    else:
        aligner = LexicalConceptAligner()
        threshold = 0.2 if args.threshold is None else args.threshold

    alignments = aligner.align(phrases, concepts, threshold=threshold)
    analysis = ArtifactAnalyzer().analyze(text, artifact_type="text")
    aligned_concepts = {alignment.concept_id for alignment in alignments}
    merged_analysis = ArtifactAnalysis(
        artifact_type=analysis.artifact_type,
        concepts=set(analysis.concepts) | aligned_concepts,
        signals=analysis.signals,
        warnings=analysis.warnings,
    )
    gaps = GapModel().estimate(merged_analysis, profile.knowledge_state)
    dialogue = DialogueConverter().convert(text, merged_analysis, gaps, profile)

    alignment_payload = {
        "input": args.input,
        "profile": args.profile,
        "concept_schema": args.concepts,
        "method": "bert" if args.bert else "lexical",
        "threshold": threshold,
        "phrases": phrases,
        "artifact_concepts": sorted(analysis.concepts),
        "aligned_concepts": sorted(aligned_concepts),
        "gap_concepts": [gap.concept for gap in gaps],
        "alignments": [asdict(alignment) for alignment in alignments],
        "ok": bool(alignments) and bool(gaps),
    }
    (output_dir / "latest_alignment.json").write_text(
        json.dumps(alignment_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "latest_dialogue.md").write_text(
        dialogue.to_markdown(),
        encoding="utf-8",
    )
    (output_dir / "latest_dialogue_plan.json").write_text(
        dialogue.plan.to_json(),
        encoding="utf-8",
    )

    print(json.dumps(alignment_payload, ensure_ascii=False, indent=2))
    print("\nWrote:")
    print(f"- {output_dir / 'latest_alignment.json'}")
    print(f"- {output_dir / 'latest_dialogue_plan.json'}")
    print(f"- {output_dir / 'latest_dialogue.md'}")
    return 0 if alignment_payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
