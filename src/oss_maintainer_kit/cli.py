"""Command line interface for OSS Maintainer Kit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .health import build_health_report
from .release_notes import build_release_notes
from .review import build_review_checklist
from .triage import suggest_many


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="oss-maintainer-kit")
    sub = parser.add_subparsers(dest="command", required=True)

    triage = sub.add_parser("triage", help="Suggest labels for issues from a JSON file.")
    triage.add_argument("issues_json", help="Path to a JSON array of issue objects.")

    release = sub.add_parser("release-notes", help="Generate release notes from commit messages.")
    release.add_argument("commits_txt", help="Path to a text file containing one commit per line.")
    release.add_argument("--version", default="Unreleased")

    review = sub.add_parser("review-checklist", help="Create a PR review checklist from changed files.")
    review.add_argument("changed_files_txt", help="Path to a text file containing one changed file per line.")

    health = sub.add_parser("health", help="Create a repository health report from issues JSON.")
    health.add_argument("issues_json", help="Path to a JSON array of issue objects.")

    args = parser.parse_args(argv)

    if args.command == "triage":
        issues = json.loads(Path(args.issues_json).read_text(encoding="utf-8"))
        print("# Issue Triage Suggestions\n")
        for suggestion in suggest_many(issues):
            print(f"- #{suggestion.number} {suggestion.title}")
            print(f"  Suggested labels: {', '.join(suggestion.labels)}")
            print(f"  Reason: {suggestion.reason}\n")
        return 0

    if args.command == "release-notes":
        lines = Path(args.commits_txt).read_text(encoding="utf-8").splitlines()
        print(build_release_notes(lines, version=args.version))
        return 0

    if args.command == "review-checklist":
        lines = Path(args.changed_files_txt).read_text(encoding="utf-8").splitlines()
        print(build_review_checklist(lines))
        return 0

    if args.command == "health":
        issues = json.loads(Path(args.issues_json).read_text(encoding="utf-8"))
        print(build_health_report(issues))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
