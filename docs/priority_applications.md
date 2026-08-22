# Priority Applications

This project has two highest-priority applications. Treat these as product and
research anchors when making design or implementation choices.

## 1. Knowledge-State-Conditioned Dialogue Conversion

Convert monologue-style written explanations into two-person student-teacher
dialogue.

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

The privacy-preserving principle also applies to both applications:

- default to offline/local processing
- do not send raw learner data outside the system by default
- allow remote AI only through explicit, restricted, auditable modes
