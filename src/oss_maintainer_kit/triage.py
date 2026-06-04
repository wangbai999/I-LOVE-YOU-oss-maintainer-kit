"""Issue triage helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class TriageSuggestion:
    number: int | str
    title: str
    labels: tuple[str, ...]
    reason: str


KEYWORDS: Mapping[str, tuple[str, ...]] = {
    "bug": ("crash", "error", "fail", "failed", "exception", "broken", "bug", "not working"),
    "feature": ("feature", "request", "add", "support", "enhancement", "proposal"),
    "docs": ("docs", "documentation", "readme", "guide", "typo", "example"),
    "question": ("how", "why", "question", "help", "usage", "can i"),
    "security": ("security", "vulnerability", "cve", "token", "secret", "injection", "xss", "csrf"),
    "frontend": ("ui", "css", "html", "button", "layout", "mobile", "responsive"),
    "backend": ("api", "server", "database", "cache", "auth", "endpoint"),
}

REPRODUCTION_HINTS = ("steps", "reproduce", "expected", "actual", "environment", "version")


def suggest_labels(issue: Mapping[str, object]) -> TriageSuggestion:
    """Suggest labels for a GitHub-like issue object.

    The function accepts dictionaries containing at least `title` and optionally
    `body` and `number`. It is deterministic so maintainers can review and test
    behavior easily.
    """
    title = str(issue.get("title", "")).strip()
    body = str(issue.get("body", "")).strip()
    number = issue.get("number", "?")
    text = f"{title}\n{body}".lower()

    labels: list[str] = []
    matched: list[str] = []
    for label, words in KEYWORDS.items():
        if any(word in text for word in words):
            labels.append(label)
            matched.append(label)

    if "bug" in labels and not any(hint in text for hint in REPRODUCTION_HINTS):
        labels.append("needs-reproduction")

    if not labels:
        labels.append("needs-triage")
        reason = "No strong keyword match; maintainer review required."
    else:
        reason = "Matched categories: " + ", ".join(matched or labels) + "."
        if "needs-reproduction" in labels:
            reason += " Bug report appears to lack reproduction details."

    return TriageSuggestion(number=number, title=title, labels=tuple(dict.fromkeys(labels)), reason=reason)


def suggest_many(issues: Iterable[Mapping[str, object]]) -> list[TriageSuggestion]:
    """Return triage suggestions for multiple issues."""
    return [suggest_labels(issue) for issue in issues]
