# CodeGraph Colab Test Result Analysis

This note summarizes the first Colab execution of
`scripts/run_codegraph_colab_test.py`.

## Result

The first Colab run succeeded overall.

```text
ok: True
CodeGraph version: 1.5.0
Indexed files: 5
Nodes: 18
Edges: 20
Languages: c, java, python, typescript
```

The concept-evidence checks all passed.

| educational concept | result | evidence |
|---|---|---|
| `loop` | pass | `loop_sum_c`, `sumSquaresJava`, `summarize_scores_py` were searchable |
| `condition` | pass | `max_with_branch_c`, `classify_grade_py` were searchable |
| `function_call` | pass | `helperSquareJava`, `normalizeNameTs`, `buildGreetingTs` were searchable |

The relation queries were also useful.

| query | result | interpretation |
|---|---|---|
| `callees sumSquaresJava` | pass | found `helperSquareJava` as a callee |
| `callers helperSquareJava` | pass | found `sumSquaresJava` as a caller |
| `impact normalizeNameTs` | pass | found `normalizeNameTs` and affected `buildGreetingTs` |
| `explore loop --json` | failed | `explore` does not accept `--json` in CodeGraph 1.5.0 |

The `explore` issue is a script compatibility problem, not evidence that
CodeGraph failed. The script has been adjusted to call `explore loop` without
`--json`.

## Implication For IrealKG

This result supports treating `colbymchenry/codegraph` as a practical local
code-evidence infrastructure candidate.

```text
CodeNet or repository code
  -> CodeGraph local index
  -> searchable symbols and relation evidence
  -> CodeOntology-like structure normalization
  -> local_thesis-style educational concept normalization
  -> IrealKG node/link evidence
```

The result does not show that CodeGraph directly provides educational concepts.
It shows that CodeGraph can provide traceable code evidence:

| criterion | observation |
|---|---|
| structural coverage | functions, methods, files, imports, and classes were indexed |
| queryability | symbol search, callers, callees, and impact queries worked |
| source traceability | results include `filePath`, `startLine`, `endLine`, language, and kind |
| educational mappability | `loop`, `condition`, and `function_call` can be linked to named code evidence |
| language portability | C, Java, Python, and TypeScript were indexed in one sample project |

## Remaining Limits

The first test is intentionally small. It verifies CodeGraph as an indexing and
query layer, not as a full program-analysis or educational-KG engine.

Open checks:

- whether CodeGraph exposes statement-level loop/condition nodes directly, or
  mainly function/method/file level nodes;
- whether line ranges are precise enough for CodeOntology-like statement
  grounding;
- whether C CodeNet submissions can be indexed at useful scale in Colab;
- whether CodeGraph output can be stably aligned with local_thesis relation
  labels such as `Used for`, `Part of`, and `Prerequisite of`.

## Next Test

The next useful test is a statement-level sample:

```text
loop evidence:
  for/while location
  loop condition
  body statements
  updated variable

condition evidence:
  if condition
  then/else branch
  returned value or state update
```

If CodeGraph itself does not expose this level directly, use CodeGraph for
file/function retrieval and add a small tree-sitter/CodeOntology-like extractor
for statement-level educational evidence.
