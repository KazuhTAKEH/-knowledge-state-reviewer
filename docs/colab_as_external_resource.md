# Colab as an External Execution Resource

This project treats Colab as an external execution resource, not as the center
of the development conversation.

## Conversation Center

The main loop is:

```text
User <-> Codex
```

Colab is used only when GPU, BERT/SentenceTransformer, or other remote runtime
execution is useful.

## Default Division of Labor

Codex:

- updates local files
- updates experiment inputs/configs
- updates scripts and notebooks
- pushes changes to GitHub
- pulls Colab result artifacts from GitHub
- inspects and revises implementation

User:

- opens Colab
- runs the prepared notebook/cells
- grants required Secrets/runtime permissions
- runs the prepared push cell

The user should not normally need to paste Colab outputs back into chat.

## Standard Experiment Inputs

Codex prepares these files locally and pushes them to GitHub:

```text
experiments/current_monologue.txt
experiments/current_dialogue_experiment.json
```

Colab reads these files. The user should not need to edit `custom_text` inside
the notebook for ordinary runs.

## Standard Colab Outputs

Colab writes:

```text
colab_outputs/latest_alignment.json
colab_outputs/latest_dialogue_plan.json
colab_outputs/latest_dialogue.md
```

When the user runs the prepared push cell, Codex can later pull these files from
GitHub and inspect them directly.

## Exceptions

The user may still inspect or edit Colab notebook contents when:

- a Colab-only error appears
- permissions, Secrets, or runtime state need manual intervention
- a notebook workflow itself is being designed
- the user wants to make a specialist judgment on model behavior

These are exceptions, not the default workflow.
