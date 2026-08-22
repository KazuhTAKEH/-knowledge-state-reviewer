# Priority Applications

This project has two highest-priority applications. Treat these as product and
research anchors when making design or implementation choices.

## 1. Knowledge-State-Conditioned Dialogue Conversion

Convert monologue-style written explanations into two-person student-teacher
dialogue.

This is the first implementation priority.

Because this application is strongly generative and may be used for教材生成
and system tuning, commercial generative AI can be used when it materially helps
quality, variation, or rapid iteration. The system should still keep remote AI
use explicit and auditable, but this application does not require the strictest
offline-only posture during early development.

The student role must not be a generic assistant or simple listener. It should
be generated from an explicit learner knowledge state, such as:

- weak understanding of functions
- confusion between `return` and `print`
- unclear understanding of arguments/parameters
- beginner-level reading of programming explanations

The system should generate and review:

- where the student naturally asks questions
- what the student is likely to misunderstand
- where the teacher explanation skips necessary prerequisites
- whether the teacher response scaffolds learning instead of simply giving an
  answer

Japanese working name:

```text
知識状態条件付き対話化
```

English working name:

```text
Knowledge-State-Conditioned Dialogue Conversion
```

## 2. Learner-Adaptive Report Review

Evaluate student reports for a specified learner level and generate advice that
helps the student revise the report autonomously.

This is the second implementation priority, after the dialogue conversion
pipeline is usable.

Because this application involves highly individualized learner guidance,
communication with external AI services should be more restricted than in the
dialogue-generation use case. The default design should minimize remote calls
and avoid sending raw learner data outside the system unless explicitly enabled.

The goal is not only grading. The system should produce scaffolded feedback that
the learner can act on without receiving a finished answer.

The system should adapt feedback to the learner's knowledge state, such as:

- weak distinction between claim and summary
- weak use of evidence
- confusion between examples and evidence
- difficulty handling counterarguments
- beginner/intermediate differences in writing structure

The system should generate:

- evaluation observations
- learner-understandable questions
- next-step revision advice
- warnings when feedback may over-answer

Japanese working name:

```text
学習者適応型レポートレビュー
```

English working name:

```text
Learner-Adaptive Report Review
```

## Design Implication

When priorities conflict, prefer implementation choices that support these two
applications before general-purpose review features.

Implementation order:

1. Build and iterate on `Knowledge-State-Conditioned Dialogue Conversion`.
2. Reuse the stable knowledge-state, alignment, and feedback components for
   `Learner-Adaptive Report Review`.

The privacy-preserving principle also applies to both applications:

- default to offline/local processing
- do not send raw learner data outside the system by default
- allow remote AI only through explicit, restricted, auditable modes

Remote AI posture by application:

- Dialogue conversion: remote generative AI is acceptable for教材生成,
  dialogue quality, and system tuning when configured explicitly.
- Report review: remote AI should be minimized because learner-specific data is
  more sensitive and communication costs scale with individualized use.

Both applications should follow the reproducibility principles in
`docs/reproducibility_principles.md`. In particular, inputs may be diverse and
unknown, but outputs should remain reproducibly conditioned on the specified
learner model.
