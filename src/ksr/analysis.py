from __future__ import annotations

from dataclasses import dataclass, field
import ast
import re


@dataclass(frozen=True)
class ArtifactAnalysis:
    artifact_type: str
    concepts: set[str]
    signals: dict[str, int | float | str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


class ArtifactAnalyzer:
    """Small local analyzer for text and Python code."""

    def analyze(self, text: str, artifact_type: str = "auto") -> ArtifactAnalysis:
        inferred = self._infer_type(text) if artifact_type == "auto" else artifact_type
        if inferred == "code":
            return self._analyze_python_code(text)
        return self._analyze_text(text)

    def _infer_type(self, text: str) -> str:
        code_markers = ["def ", "class ", "import ", "return ", "for ", "while "]
        return "code" if any(marker in text for marker in code_markers) else "text"

    def _analyze_python_code(self, text: str) -> ArtifactAnalysis:
        concepts: set[str] = set()
        warnings: list[str] = []
        try:
            tree = ast.parse(text)
        except SyntaxError as exc:
            return ArtifactAnalysis(
                artifact_type="code",
                concepts={"syntax"},
                signals={"syntax_error_line": exc.lineno or 0},
                warnings=[f"Syntax error: {exc.msg}"],
            )

        node_count = 0
        for node in ast.walk(tree):
            node_count += 1
            if isinstance(node, ast.FunctionDef):
                concepts.add("function")
            elif isinstance(node, ast.Return):
                concepts.add("return_value")
            elif isinstance(node, (ast.For, ast.While)):
                concepts.add("loop")
            elif isinstance(node, ast.If):
                concepts.add("condition")
            elif isinstance(node, ast.Call):
                concepts.add("function_call")
            elif isinstance(node, ast.ClassDef):
                concepts.add("class")
            elif isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp)):
                concepts.add("comprehension")

        return ArtifactAnalysis(
            artifact_type="code",
            concepts=concepts or {"basic_expression"},
            signals={"node_count": node_count, "line_count": len(text.splitlines())},
            warnings=warnings,
        )

    def _analyze_text(self, text: str) -> ArtifactAnalysis:
        lowered = text.lower()
        concepts: set[str] = set()
        if self._contains_any(lowered, ["thesis", "claim", "argue", "主張", "論点"]):
            concepts.add("claim")
        if self._contains_any(lowered, ["evidence", "data", "example", "because", "根拠", "事例", "理由", "なぜなら"]):
            concepts.add("evidence")
        if self._contains_any(lowered, ["however", "although", "counter", "反論", "一方"]):
            concepts.add("counterargument")
        if self._contains_any(lowered, ["conclusion", "therefore", "結論", "したがって"]):
            concepts.add("conclusion")
        if self._contains_any(lowered, ["function", "def", "関数"]):
            concepts.add("function")
        if self._contains_any(lowered, ["return", "戻り値", "返します", "返す"]):
            concepts.add("return_value")
        if self._contains_any(lowered, ["argument", "parameter", "引数"]):
            concepts.add("function_call")
        if self._contains_any(lowered, ["loop", "for", "while", "繰り返し"]):
            concepts.add("loop")
        if len([p for p in re.split(r"\n\s*\n", text.strip()) if p]) >= 2:
            concepts.add("paragraph_structure")

        sentences = [s for s in re.split(r"[。.!?]\s*", text.strip()) if s]
        avg_sentence_len = (
            sum(len(sentence) for sentence in sentences) / len(sentences)
            if sentences
            else 0
        )
        return ArtifactAnalysis(
            artifact_type="text",
            concepts=concepts or {"plain_explanation"},
            signals={
                "sentence_count": len(sentences),
                "avg_sentence_len": round(avg_sentence_len, 1),
                "paragraph_count": len([p for p in re.split(r"\n\s*\n", text.strip()) if p]),
            },
        )

    def _contains_any(self, text: str, terms: list[str]) -> bool:
        return any(term in text for term in terms)
