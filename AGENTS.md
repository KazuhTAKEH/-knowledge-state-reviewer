# AGENTS.md

Project instructions for Codex when working in this repository.

## Project Identity

This repository implements a knowledge-state-conditioned learning support
prototype. The local project theme is:

```text
Use learner knowledge state to condition dialogue generation, review, and
feedback while preserving reproducibility and privacy.
```

The learner model is not finalized. Keep DKT and related knowledge tracing
research under review, and keep implementation boundaries flexible.

## Priority Applications

Prioritize these applications in this order:

1. **Knowledge-State-Conditioned Dialogue Conversion**
   - Japanese: `知識状態条件付き対話化`
   - Convert monologue-style instructional text into student-teacher dialogue.
   - This is the first implementation priority.
   - Commercial generative AI may be used for教材生成, dialogue quality, and
     system tuning when explicitly configured and auditable.

2. **Learner-Adaptive Report Review**
   - Japanese: `学習者適応型レポートレビュー`
   - Evaluate student reports and generate scaffolded advice for autonomous
     revision.
   - This is the second implementation priority.
   - Minimize remote communication because learner-specific data is more
     sensitive.

See:

- `docs/priority_applications.md`
- `docs/reproducibility_principles.md`

## Core Design Principle

Follow learner-state-conditioned reproducibility:

```text
Be flexible with inputs.
Be faithful and reproducible with learner state.
```

Inputs such as monologues, reports, code, and learner reactions may be diverse
and unknown. Outputs should remain reproducibly conditioned on the specified
learner model, concept schema, policy, and generation settings.

Avoid collapsing the whole task into one opaque generation prompt. Prefer an
inspectable pipeline:

```text
input artifact
  -> analysis
  -> phrase/concept extraction
  -> concept alignment
  -> learner-state comparison
  -> DialoguePlan / feedback plan
  -> final generation
  -> consistency review
```

## Colab Workflow

Treat Google Colab as an external execution resource.

The conversation center is:

```text
User <-> Codex
```

Colab is not the conversation center. The user should normally only:

- open the prepared notebook
- run cells
- grant Secrets/runtime permissions
- run the prepared push cell

The user should not normally paste Colab outputs into chat. Codex should pull
the results from GitHub and inspect them directly.

Standard flow:

```text
Codex updates local files
Codex pushes GitHub
User runs Colab notebook
User runs prepared result-push cell
Codex pulls GitHub
Codex inspects colab_outputs/latest_*
```

See:

- `docs/colab_as_external_resource.md`
- `docs/colab_workflow.md`
- `notebooks/ksr_colab_starter.ipynb`

## Standard Experiment Files

Codex prepares experiment inputs locally:

```text
experiments/current_monologue.txt
experiments/current_dialogue_experiment.json
```

Colab reads those files. Do not require the user to edit `custom_text` inside
Colab for ordinary runs.

Colab writes small result artifacts:

```text
colab_outputs/latest_alignment.json
colab_outputs/latest_dialogue_plan.json
colab_outputs/latest_dialogue.md
```

These are intentionally ignored by default, but the prepared Colab push cell may
force-add them when the user wants Codex to inspect the latest result.

Do not commit large data, checkpoints, raw student data, API tokens, or
personally identifying learner data.

## Notebook Hygiene

Keep notebooks as lightweight orchestration documents:

- no saved cell outputs unless explicitly needed
- no widgets metadata
- no embedded secrets
- no large result blobs
- reusable logic belongs in `src/ksr` or `scripts`

Before committing a notebook, validate that it is JSON and small enough to
remain reviewable.

## Local Commands

From repository root:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests
```

Run the local lexical dialogue experiment:

```powershell
$env:PYTHONPATH="src"
$env:PYTHONIOENCODING="utf-8"
python scripts/colab_dialogue_experiment.py --input experiments/current_monologue.txt --profile examples/profiles/beginner_python.json --concepts examples/concepts/python_basic.json
```

Colab runs the same script with:

```text
--config experiments/current_dialogue_experiment.json
```

The config may enable BERT/SentenceTransformer, which is expected to run in
Colab rather than the local environment.

## Privacy and Remote AI

Default to local/offline processing when possible.

Remote AI use must be explicit and auditable. Do not send raw learner data or
full learner profiles to remote services by default.

For dialogue conversion, remote generative AI is acceptable when explicitly
configured for教材生成 or system tuning. For learner-adaptive report review,
remote communication should be minimized.
