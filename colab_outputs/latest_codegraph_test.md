# CodeGraph Colab Test Result

- ok: `True`
- sample_root: `/content/-knowledge-state-reviewer/examples/codegraph_samples`

## Concept Evidence Checks

| concept | judgment | found | note |
|---|---|---:|---|
| `loop` | `pass` | 3/3 | Loop structures should be recoverable as code evidence for the educational concept `loop`. |
| `condition` | `pass` | 2/2 | Branching structures should be recoverable as code evidence for the educational concept `condition`. |
| `function_call` | `pass` | 3/3 | Call relationships should support the educational concepts `function` and `function_call`. |

## Command Summary

| command | ok | returncode | duration_sec |
|---|---:|---:|---:|
| `commands.help` | `True` | `0` | `0.236` |
| `commands.init` | `True` | `0` | `2.504` |
| `commands.status` | `True` | `0` | `0.527` |
| `queries.loop_sum_c` | `True` | `0` | `0.341` |
| `queries.max_with_branch_c` | `True` | `0` | `0.356` |
| `queries.classify_grade_py` | `True` | `0` | `0.366` |
| `queries.summarize_scores_py` | `True` | `0` | `0.333` |
| `queries.helperSquareJava` | `True` | `0` | `0.377` |
| `queries.sumSquaresJava` | `True` | `0` | `0.365` |
| `queries.normalizeNameTs` | `True` | `0` | `0.344` |
| `queries.buildGreetingTs` | `True` | `0` | `0.358` |
| `relations.callees_sumSquaresJava` | `True` | `0` | `0.311` |
| `relations.callers_helperSquareJava` | `True` | `0` | `0.338` |
| `relations.impact_normalizeNameTs` | `True` | `0` | `0.349` |
| `relations.explore_loop` | `True` | `0` | `0.369` |

## Compatibility Notes

- `status`, `query`, `callers`, `callees`, and `impact` are tested with JSON output.
- `explore` is tested as text output because CodeGraph 1.5.0 does not accept `explore --json`.

## Interpretation

This test does not treat CodeGraph as an educational concept model.
It checks whether CodeGraph can provide local, queryable code evidence that can later be aligned with CodeOntology-like structures and local_thesis-style educational concepts.

