from __future__ import annotations

import argparse
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
from ksr.analysis import ArtifactAnalyzer  # noqa: E402
from ksr.gap import GapModel  # noqa: E402
from ksr.knowledge import ReviewerProfile  # noqa: E402


def load_concepts(path: Path) -> list[ConceptCandidate]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [ConceptCandidate(**item) for item in data]


def run_lightweight_test() -> dict:
    text = (ROOT / "examples" / "monologue.txt").read_text(encoding="utf-8")
    profile = ReviewerProfile.from_json(ROOT / "examples" / "profiles" / "beginner_python.json")
    concepts = load_concepts(ROOT / "examples" / "concepts" / "python_basic.json")

    analysis = ArtifactAnalyzer().analyze(text, artifact_type="text")
    gaps = GapModel().estimate(analysis, profile.knowledge_state)
    phrases = ["関数を定義する", "returnで結果を返す", "引数として値を受け取る"]
    alignments = LexicalConceptAligner().align(phrases, concepts, threshold=0.2)

    return {
        "test": "lightweight",
        "artifact_concepts": sorted(analysis.concepts),
        "gap_concepts": [gap.concept for gap in gaps],
        "alignments": [alignment.__dict__ for alignment in alignments],
        "ok": bool(gaps) and bool(alignments),
    }


def run_bert_test() -> dict:
    concepts = load_concepts(ROOT / "examples" / "concepts" / "python_basic.json")
    phrases = [
        "defで処理に名前を付ける",
        "関数から計算結果を呼び出し元へ戻す",
        "同じ処理を何度も実行する",
    ]
    aligner = SentenceTransformerConceptAligner()
    alignments = aligner.align(phrases, concepts, threshold=0.35)
    return {
        "test": "bert_alignment",
        "alignments": [alignment.__dict__ for alignment in alignments],
        "ok": len(alignments) >= 2,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bert", action="store_true", help="Run SentenceTransformer alignment test.")
    parser.add_argument("--output", default="colab_outputs/latest_smoke_test.json")
    args = parser.parse_args()

    result = run_bert_test() if args.bert else run_lightweight_test()
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
