# Implementation Plan

This project prioritizes runnable systems over theory. The immediate goal is a
local, inspectable feedback engine whose behavior is controlled by explicit
knowledge-state JSON.

## Target Applications

### 1. Monologue to Student-Teacher Dialogue

Input:

- explanatory monologue
- learner profile
- optional teacher policy

Output:

- student utterances that reflect weak concepts and misconceptions
- teacher responses that scaffold instead of giving finished answers
- review of teacher explanation quality

MVP module:

- `ArtifactAnalyzer`
- `GapModel`
- `DialogueConverter`

### 2. Learner-Adaptive Report Review

Input:

- student report
- learner profile
- rubric

Output:

- questions the student can answer
- observations about likely misunderstandings
- revision advice that keeps the student responsible for the rewrite
- risks in the current evaluation

MVP module:

- `ArtifactAnalyzer`
- `GapModel`
- `FeedbackGenerator`

## DKT Integration Boundary

`KnowledgeTracer` is intentionally an adapter. The first prototype accepts
manual JSON. Later versions can map these sources into `KnowledgeState`:

- pyKT output vectors
- Code-DKT concept mastery
- Error-DKT error-type predictions
- manually authored instructor profiles

## Near-Term Engineering Tasks

1. Add structured JSON output for downstream apps.
2. Add local LLM backend interface.
3. Add concept schema files for writing, Python, and pedagogy.
4. Add transcript-level teacher explanation review.
5. Add fixtures from downloaded papers for evaluation examples.
