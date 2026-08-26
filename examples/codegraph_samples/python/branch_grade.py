def classify_grade_py(score: int) -> str:
    if score >= 80:
        return "A"
    if score >= 60:
        return "B"
    return "C"


def summarize_scores_py(scores: list[int]) -> dict[str, int]:
    counts = {"A": 0, "B": 0, "C": 0}
    for score in scores:
        grade = classify_grade_py(score)
        counts[grade] += 1
    return counts
