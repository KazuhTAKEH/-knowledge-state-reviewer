# Colab-Codex Workflow

Use Colab for GPU-heavy experiments and Codex for repository structure,
interfaces, tests, and documentation.

## Recommended Repository Shape

```text
knowledge-state-reviewer/
  src/ksr/                 # reusable library code
  notebooks/               # Colab entry points
  examples/                # small portable fixtures
  experiments/             # ignored or lightweight experiment configs
  outputs/                 # generated results, usually not committed
  papers/                  # local paper archive
```

## Colab Loop

1. Open `notebooks/ksr_colab_starter.ipynb` in Colab.
2. Mount Google Drive only if data or checkpoints need persistence.
3. Clone or pull the Git repository into `/content/knowledge-state-reviewer`.
4. Install `requirements-colab.txt`.
5. Run alignment/embedding experiments.
6. Save only reusable code changes back to `src/ksr`.
7. Export small result samples to `examples/` or `experiments/`.
8. Let Codex review, refactor, test, and document those changes locally.

## Minimal Colab Test Program

After cloning the repository in Colab, run the dependency-free smoke test first:

```python
%cd /content/-knowledge-state-reviewer
!PYTHONPATH=src PYTHONIOENCODING=utf-8 python scripts/colab_smoke_test.py
```

Expected result:

- `ok` is `true`
- `artifact_concepts` includes concepts such as `function` and `return_value`
- `gap_concepts` includes weak concepts from the learner profile
- `colab_outputs/latest_smoke_test.json` is created

Then install Colab dependencies and run the BERT/SentenceTransformer test:

```python
!pip install -q -r requirements-colab.txt
!PYTHONPATH=src PYTHONIOENCODING=utf-8 python scripts/colab_smoke_test.py --bert
```

Expected result:

- `ok` is `true`
- at least two phrases align to DKT-side concept IDs
- the `method` field starts with `sentence-transformers:`

This confirms the planned pipeline:

```text
input phrase
  -> BERT/SentenceTransformer embedding
  -> DKT concept candidate
  -> KnowledgeState concept ID
  -> feedback/dialogue engine
```

## Design Rule

Colab notebooks should be thin orchestration layers. Any reusable logic belongs
in `src/ksr`, so Codex can edit and test it without needing the notebook runtime.

## DKT and Input Consistency

The consistency check should map phrases/concepts found in the current input to
the concept IDs used by the DKT model.

Implementation layers:

- `ConceptCandidate`: DKT-side concept ID, label, and description.
- `ConceptAligner`: interface for mapping input phrases to concept IDs.
- `LexicalConceptAligner`: deterministic fallback.
- `SentenceTransformerConceptAligner`: BERT-style semantic alignment for Colab.

Suggested Colab model:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

It is small, multilingual, and practical for Japanese/English mixed prototypes.
For stronger Japanese performance, test Japanese SBERT models later and keep the
chosen model name in the experiment config.

## Git Hygiene

Prefer this division:

- Commit: `src/`, `tests/`, `examples/`, `docs/`, small notebooks.
- Do not commit: checkpoints, raw datasets, large generated outputs.
- For reproducibility, commit a small CSV/JSON sample plus a README explaining
  where the full data lives.

## Optional Google Drive Layout

```text
MyDrive/ksr/
  data/
  checkpoints/
  experiment_outputs/
```

Keep Drive paths configurable inside notebooks. Do not hard-code personal paths
inside library code.
