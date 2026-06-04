"""Pull request review preparation helpers."""
from __future__ import annotations

from pathlib import PurePosixPath
from typing import Iterable

SECURITY_PATTERNS = ("auth", "token", "secret", "crypto", "permission", "login", "jwt", "oauth")
DOC_EXTENSIONS = {".md", ".rst", ".txt"}
TEST_MARKERS = ("test", "spec", "__tests__")


def build_review_checklist(changed_files: Iterable[str]) -> str:
    """Create a maintainer-facing PR review checklist from changed files."""
    files = [f.strip() for f in changed_files if f.strip()]
    lower = [f.lower() for f in files]

    touches_security = any(any(p in f for p in SECURITY_PATTERNS) for f in lower)
    touches_docs = any(PurePosixPath(f).suffix.lower() in DOC_EXTENSIONS for f in lower)
    touches_tests = any(any(marker in f for marker in TEST_MARKERS) for f in lower)
    touches_ci = any(f.startswith(".github/") or "workflow" in f for f in lower)

    lines = ["# PR Review Checklist", ""]
    lines.append("## Changed files")
    for file in files or ["No changed files provided"]:
        lines.append(f"- `{file}`")
    lines.append("")

    lines.extend([
        "## Required checks",
        "- [ ] Confirm the PR solves the stated issue or clearly explains the change.",
        "- [ ] Run or inspect tests relevant to the changed files.",
        "- [ ] Check for backwards compatibility and breaking changes.",
        "- [ ] Confirm user-facing changes are documented.",
    ])

    if not touches_tests:
        lines.append("- [ ] Ask whether tests are needed; no obvious test file was changed.")
    if touches_security:
        lines.append("- [ ] Security-sensitive files changed: request extra review before merge.")
    if touches_docs:
        lines.append("- [ ] Documentation changed: verify examples and links.")
    if touches_ci:
        lines.append("- [ ] CI/workflow changed: verify permissions and secrets usage.")

    return "\n".join(lines) + "\n"
