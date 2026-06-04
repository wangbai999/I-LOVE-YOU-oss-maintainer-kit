"""Release note generation from Conventional Commit style messages."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable


GROUPS = {
    "feat": "Features",
    "fix": "Bug fixes",
    "docs": "Documentation",
    "perf": "Performance",
    "refactor": "Refactoring",
    "test": "Tests",
    "build": "Build system",
    "ci": "Continuous integration",
    "chore": "Maintenance",
    "security": "Security",
}


@dataclass(frozen=True)
class CommitEntry:
    kind: str
    scope: str | None
    description: str
    breaking: bool = False


def parse_commit(line: str) -> CommitEntry:
    """Parse a Conventional Commit message line."""
    raw = line.strip()
    if not raw:
        return CommitEntry("chore", None, "")

    head, _, description = raw.partition(":")
    if not description:
        return CommitEntry("chore", None, raw)

    breaking = "!" in head or "BREAKING CHANGE" in raw.upper()
    head = head.replace("!", "")

    if "(" in head and head.endswith(")"):
        kind, scope = head[:-1].split("(", 1)
    else:
        kind, scope = head, None

    return CommitEntry(kind=kind.lower(), scope=scope, description=description.strip(), breaking=breaking)


def build_release_notes(lines: Iterable[str], version: str = "Unreleased") -> str:
    """Build markdown release notes from commit messages."""
    grouped: dict[str, list[CommitEntry]] = defaultdict(list)
    breaking_changes: list[CommitEntry] = []

    for line in lines:
        entry = parse_commit(line)
        if not entry.description:
            continue
        group = GROUPS.get(entry.kind, "Other changes")
        grouped[group].append(entry)
        if entry.breaking:
            breaking_changes.append(entry)

    output = [f"# Release Notes: {version}", ""]
    if breaking_changes:
        output.extend(["## Breaking changes", ""])
        for entry in breaking_changes:
            output.append(_format_entry(entry))
        output.append("")

    for group in GROUPS.values():
        if group not in grouped:
            continue
        output.extend([f"## {group}", ""])
        for entry in grouped[group]:
            output.append(_format_entry(entry))
        output.append("")

    if "Other changes" in grouped:
        output.extend(["## Other changes", ""])
        for entry in grouped["Other changes"]:
            output.append(_format_entry(entry))
        output.append("")

    if len(output) == 2:
        output.append("No notable changes detected.")

    return "\n".join(output).strip() + "\n"


def _format_entry(entry: CommitEntry) -> str:
    scope = f"**{entry.scope}:** " if entry.scope else ""
    marker = " ⚠️" if entry.breaking else ""
    return f"- {scope}{entry.description}{marker}"
