"""Repository health reporting helpers."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Iterable, Mapping


def build_health_report(issues: Iterable[Mapping[str, object]]) -> str:
    """Generate a simple repository health report from issue-like objects."""
    items = list(issues)
    labels = Counter()
    stale = 0
    now = datetime.now(timezone.utc)

    for issue in items:
        for label in issue.get("labels", []) or []:
            if isinstance(label, dict):
                labels[str(label.get("name", "unknown"))] += 1
            else:
                labels[str(label)] += 1
        updated = str(issue.get("updated_at", ""))
        if updated:
            try:
                dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                if (now - dt).days >= 30:
                    stale += 1
            except ValueError:
                pass

    lines = ["# Repository Health Report", ""]
    lines.append(f"Open items analyzed: {len(items)}")
    lines.append(f"Potentially stale items: {stale}")
    lines.append("")
    lines.append("## Label distribution")
    if labels:
        for name, count in labels.most_common():
            lines.append(f"- {name}: {count}")
    else:
        lines.append("- No labels found. Consider adding a basic triage label set.")
    lines.append("")
    lines.append("## Suggested maintainer actions")
    if stale:
        lines.append("- Review stale issues and close, update, or mark them as help-wanted.")
    if not labels:
        lines.append("- Add labels such as bug, feature, docs, question, security, and needs-reproduction.")
    lines.append("- Run release-note generation before the next tagged release.")
    return "\n".join(lines) + "\n"
