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
| `commands.help` | `True` | `0` | `0.158` |
| `commands.init` | `True` | `0` | `2.461` |
| `commands.status` | `True` | `0` | `0.568` |
| `queries.loop_sum_c` | `True` | `0` | `0.507` |
| `queries.max_with_branch_c` | `True` | `0` | `0.528` |
| `queries.classify_grade_py` | `True` | `0` | `0.578` |
| `queries.summarize_scores_py` | `True` | `0` | `0.369` |
| `queries.helperSquareJava` | `True` | `0` | `0.363` |
| `queries.sumSquaresJava` | `True` | `0` | `0.345` |
| `queries.normalizeNameTs` | `True` | `0` | `0.357` |
| `queries.buildGreetingTs` | `True` | `0` | `0.342` |
| `relations.callees_sumSquaresJava` | `True` | `0` | `0.322` |
| `relations.callers_helperSquareJava` | `True` | `0` | `0.342` |
| `relations.impact_normalizeNameTs` | `True` | `0` | `0.348` |
| `relations.explore_loop` | `False` | `1` | `0.154` |

## Interpretation

This test does not treat CodeGraph as an educational concept model.
It checks whether CodeGraph can provide local, queryable code evidence that can later be aligned with CodeOntology-like structures and local_thesis-style educational concepts.

