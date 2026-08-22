from __future__ import annotations

import argparse
import json
from pathlib import Path

from ksr.analysis import ArtifactAnalyzer
from ksr.dialogue import DialogueConverter
from ksr.feedback import FeedbackGenerator
from ksr.gap import GapModel
from ksr.knowledge import ReviewerProfile


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ksr")
    sub = parser.add_subparsers(dest="command", required=True)

    report = sub.add_parser("report", help="Generate learner-adaptive report feedback.")
    report.add_argument("--input", required=True)
    report.add_argument("--profile", required=True)
    report.add_argument("--rubric")
    report.add_argument("--artifact-type", default="text", choices=["auto", "text", "code"])

    dialogue = sub.add_parser("dialogue", help="Convert monologue into student-teacher dialogue.")
    dialogue.add_argument("--input", required=True)
    dialogue.add_argument("--profile", required=True)
    dialogue.add_argument("--artifact-type", default="auto", choices=["auto", "text", "code"])
    dialogue.add_argument("--show-plan", action="store_true", help="Print the reproducible dialogue plan before the draft.")

    args = parser.parse_args(argv)
    text = Path(args.input).read_text(encoding="utf-8")
    profile = ReviewerProfile.from_json(args.profile)
    analysis = ArtifactAnalyzer().analyze(text, artifact_type=args.artifact_type)
    gaps = GapModel().estimate(analysis, profile.knowledge_state)

    if args.command == "report":
        rubric = None
        if args.rubric:
            rubric = json.loads(Path(args.rubric).read_text(encoding="utf-8"))
        result = FeedbackGenerator().generate_report_feedback(
            text=text,
            analysis=analysis,
            gaps=gaps,
            profile=profile,
            rubric=rubric,
        )
        print(result.to_markdown())
        return 0

    if args.command == "dialogue":
        result = DialogueConverter().convert(
            monologue=text,
            analysis=analysis,
            gaps=gaps,
            profile=profile,
        )
        if args.show_plan:
            print(result.plan.to_json())
        print(result.to_markdown())
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
