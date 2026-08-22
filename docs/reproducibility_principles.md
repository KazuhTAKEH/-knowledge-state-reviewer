# Reproducibility Principles

This project should support diverse and unknown inputs while keeping system
behavior reproducibly conditioned on the learner model.

## Core Concern

Input artifacts are inherently diverse:

- instructional monologues
- student reports
- code submissions
- learner reactions
- dialogue histories

They may show statistical tendencies, but the system should assume that future
inputs are open-ended and heterogeneous.

By contrast, the learner model is the main control surface. Even though the
final learner model is not yet fixed, system outputs should depend on the
specified learner state in a stable, inspectable way.

Working principle:

```text
Be flexible with inputs.
Be faithful and reproducible with learner state.
```

## Learner-State-Conditioned Reproducibility

For the same input, learner model, concept schema, policy, and generation
settings, the system should produce substantially similar intermediate decisions
and outputs.

For different inputs but the same learner model, the system may adapt to the
input content, but it should preserve the learner's characteristic tendencies:

- recurring weak concepts
- likely misconceptions
- appropriate question depth
- appropriate feedback granularity
- limits on technical vocabulary
- degree of scaffolding

This is called:

```text
Learner-State-Conditioned Reproducibility
```

Japanese working name:

```text
学習者状態条件付き再現性
```

## Do Not Prematurely Fix the Learner Model

The learner model is not finalized yet.

Before committing to a specific learner-state representation, the project should
continue reviewing DKT and related knowledge tracing research, including:

- DKT
- DKT+
- DKVMN
- SAKT / AKT
- Code-DKT
- Error-DKT
- programming knowledge tracing
- interpretable multi-KC knowledge tracing

Implementation should therefore use adapter boundaries rather than assuming one
final model shape.

Current boundary:

```text
KnowledgeTracer
  -> produces or updates
KnowledgeState
```

The `KnowledgeState` schema is a working interface, not a final theoretical
commitment.

## Separation of Concerns

Avoid sending raw input and learner state directly into a generator as one large
prompt. Prefer an inspectable pipeline:

```text
Input artifact
  -> input analysis
  -> concept / phrase extraction
  -> concept alignment
  -> learner-state comparison
  -> planned learner reaction or feedback intent
  -> final generation
  -> learner-state consistency check
```

This makes it possible to test which part caused an output change.

## Controlled Variation

Some variation is useful, especially for dialogue and教材生成. However, variation
should be controlled by explicit settings:

- learner model version
- concept schema version
- input analysis version
- generation policy version
- random seed when available
- model/provider name
- temperature or sampling settings
- remote AI mode

Generated outputs should record these settings when they are part of an
experiment.

## Consistency Checks

Future implementation should include checks such as:

- Does the student utterance use concepts that the learner model says are weak?
- Does the student ask questions at the right depth?
- Does the teacher explanation over-answer?
- Does the advice require knowledge the learner is unlikely to have?
- Did a remote model produce behavior inconsistent with the learner state?

These checks should be especially important before using generated dialogue or
feedback as training/evaluation data.

## Privacy Connection

Reproducibility and privacy are connected.

If learner-state conditioning is represented in structured, local, inspectable
state, the system can often avoid sending raw learner data to a remote service.
For individualized report review, this is especially important.
