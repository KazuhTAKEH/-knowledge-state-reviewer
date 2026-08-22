# Knowledge State Reviewer

Implementation-first prototype for a knowledge-state-conditioned feedback engine.

The current MVP does not require OpenAI or any remote model. It uses an explicit
JSON learner profile and deterministic planning rules to generate:

- learner-adaptive report feedback
- student-teacher dialogue from monologue-style writing
- teacher explanation review

Later, `KnowledgeTracer` can be backed by DKT, pyKT, Code-DKT, or Error-DKT.

For Colab-oriented development and BERT-based concept alignment, see
`docs/colab_workflow.md` and `notebooks/ksr_colab_starter.ipynb`.

The two highest-priority applications are documented in
`docs/priority_applications.md`.

## Quick Start

```powershell
python -m ksr.cli report --input examples/report.txt --profile examples/profiles/beginner_writing.json --rubric examples/rubrics/report_basic.json
python -m ksr.cli dialogue --input examples/monologue.txt --profile examples/profiles/beginner_python.json
```

When using from the repository root without installation:

```powershell
$env:PYTHONPATH="src"
$env:PYTHONIOENCODING="utf-8"
python -m ksr.cli report --input examples/report.txt --profile examples/profiles/beginner_writing.json --rubric examples/rubrics/report_basic.json
```

Run tests without external dependencies:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests
```

## Core Ideas

- `KnowledgeState`: observable concept mastery and misconceptions.
- `ArtifactAnalyzer`: extracts concepts and structural signals from input.
- `GapModel`: compares artifact demands with learner knowledge.
- `FeedbackGenerator`: generates scaffolded advice, not finished answers.
- `DialogueConverter`: simulates student utterances and teacher responses.

## Project Status

This is a scaffolded MVP. It is useful for testing task shape, data contracts,
and prompt/control design before connecting a trained DKT model.
