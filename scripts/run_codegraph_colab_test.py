from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_ROOT = ROOT / "examples" / "codegraph_samples"


def run_command(
    command: list[str],
    *,
    cwd: Path = ROOT,
    timeout: int = 120,
) -> dict[str, Any]:
    started = time.time()
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        return {
            "command": command,
            "cwd": str(cwd),
            "returncode": completed.returncode,
            "duration_sec": round(time.time() - started, 3),
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "ok": completed.returncode == 0,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "cwd": str(cwd),
            "returncode": None,
            "duration_sec": round(time.time() - started, 3),
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or f"Timed out after {timeout} seconds.",
            "ok": False,
            "timeout": True,
        }
    except OSError as exc:
        return {
            "command": command,
            "cwd": str(cwd),
            "returncode": None,
            "duration_sec": round(time.time() - started, 3),
            "stdout": "",
            "stderr": str(exc),
            "ok": False,
        }


def maybe_json(text: str) -> Any:
    stripped = text.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return None


def command_stdout_contains(command_result: dict[str, Any], needles: list[str]) -> bool:
    text = f"{command_result.get('stdout', '')}\n{command_result.get('stderr', '')}".lower()
    return any(needle.lower() in text for needle in needles)


def ensure_codegraph_available(install: bool) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = [
        run_command(["node", "--version"], timeout=30),
        run_command(["npm", "--version"], timeout=30),
        run_command(["npx", "--version"], timeout=30),
    ]
    if shutil.which("codegraph"):
        checks.append(run_command(["codegraph", "--version"], timeout=30))
        return checks

    if install:
        checks.append(
            run_command(
                ["npm", "install", "-g", "@colbymchenry/codegraph"],
                timeout=300,
            )
        )
        checks.append(run_command(["codegraph", "--version"], timeout=30))
    return checks


def codegraph_command(args: list[str]) -> list[str]:
    if shutil.which("codegraph"):
        return ["codegraph", *args]
    return ["npx", "--yes", "@colbymchenry/codegraph", *args]


def run_codegraph_probe() -> dict[str, Any]:
    if not SAMPLE_ROOT.exists():
        raise FileNotFoundError(f"Sample root not found: {SAMPLE_ROOT}")

    commands: dict[str, dict[str, Any]] = {}
    commands["help"] = run_command(codegraph_command(["help"]), timeout=90)
    commands["init"] = run_command(codegraph_command(["init", str(SAMPLE_ROOT)]), timeout=240)
    commands["status"] = run_command(
        codegraph_command(["status", str(SAMPLE_ROOT), "--json"]),
        timeout=120,
    )

    query_terms = [
        "loop_sum_c",
        "max_with_branch_c",
        "classify_grade_py",
        "summarize_scores_py",
        "helperSquareJava",
        "sumSquaresJava",
        "normalizeNameTs",
        "buildGreetingTs",
    ]
    queries: dict[str, dict[str, Any]] = {}
    for term in query_terms:
        queries[term] = run_command(
            codegraph_command(["query", term, "--limit", "10", "--json"]),
            cwd=SAMPLE_ROOT,
            timeout=120,
        )

    relation_commands = {
        "callees_sumSquaresJava": ["callees", "sumSquaresJava", "--json"],
        "callers_helperSquareJava": ["callers", "helperSquareJava", "--json"],
        "impact_normalizeNameTs": ["impact", "normalizeNameTs", "--depth", "2", "--json"],
        "explore_loop": ["explore", "loop", "--json"],
    }
    relations = {
        name: run_command(codegraph_command(args), cwd=SAMPLE_ROOT, timeout=120)
        for name, args in relation_commands.items()
    }

    expectations = {
        "loop": {
            "query_terms": ["loop_sum_c", "sumSquaresJava", "summarize_scores_py"],
            "educational_mapping": "Loop structures should be recoverable as code evidence for the educational concept `loop`.",
        },
        "condition": {
            "query_terms": ["max_with_branch_c", "classify_grade_py"],
            "educational_mapping": "Branching structures should be recoverable as code evidence for the educational concept `condition`.",
        },
        "function_call": {
            "query_terms": ["helperSquareJava", "normalizeNameTs", "buildGreetingTs"],
            "educational_mapping": "Call relationships should support the educational concepts `function` and `function_call`.",
        },
    }

    judgments: dict[str, Any] = {}
    for concept, expectation in expectations.items():
        term_results = [queries[term] for term in expectation["query_terms"]]
        found_count = sum(
            1 for result in term_results if result["ok"] and command_stdout_contains(result, expectation["query_terms"])
        )
        judgments[concept] = {
            **expectation,
            "found_count": found_count,
            "total": len(term_results),
            "judgment": "pass" if found_count == len(term_results) else "partial" if found_count else "fail",
        }

    status_json = maybe_json(commands["status"].get("stdout", ""))
    return {
        "test": "codegraph_to_irealkg_evidence_alignment",
        "sample_root": str(SAMPLE_ROOT),
        "commands": commands,
        "queries": queries,
        "relations": relations,
        "status_json": status_json,
        "expectations": judgments,
        "ok": commands["init"]["ok"] and commands["status"]["ok"] and any(
            item["judgment"] in {"pass", "partial"} for item in judgments.values()
        ),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# CodeGraph Colab Test Result",
        "",
        f"- ok: `{result['ok']}`",
        f"- sample_root: `{result['sample_root']}`",
        "",
        "## Concept Evidence Checks",
        "",
        "| concept | judgment | found | note |",
        "|---|---|---:|---|",
    ]
    for concept, item in result["expectations"].items():
        lines.append(
            f"| `{concept}` | `{item['judgment']}` | {item['found_count']}/{item['total']} | {item['educational_mapping']} |"
        )

    lines.extend(["", "## Command Summary", "", "| command | ok | returncode | duration_sec |", "|---|---:|---:|---:|"])
    for group_name in ["commands", "queries", "relations"]:
        for name, item in result[group_name].items():
            lines.append(
                f"| `{group_name}.{name}` | `{item['ok']}` | `{item['returncode']}` | `{item['duration_sec']}` |"
            )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This test does not treat CodeGraph as an educational concept model.",
            "It checks whether CodeGraph can provide local, queryable code evidence that can later be aligned with CodeOntology-like structures and local_thesis-style educational concepts.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true", help="Install CodeGraph globally with npm if needed.")
    parser.add_argument("--output-json", default="colab_outputs/latest_codegraph_test.json")
    parser.add_argument("--output-md", default="colab_outputs/latest_codegraph_test.md")
    args = parser.parse_args()

    environment = {
        "python": sys.version,
        "platform": sys.platform,
        "cwd": os.getcwd(),
    }
    availability = ensure_codegraph_available(args.install)
    result = run_codegraph_probe()
    result["environment"] = environment
    result["availability"] = availability

    output_json = ROOT / args.output_json
    output_md = ROOT / args.output_md
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(result) + "\n", encoding="utf-8")
    print(json.dumps({"ok": result["ok"], "json": str(output_json), "markdown": str(output_md)}, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
