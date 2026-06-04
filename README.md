# OSS Maintainer Kit

> A lightweight, dependency-free toolkit for open-source maintainers: issue triage, PR review preparation, release notes generation, and repository health reporting.

OSS Maintainer Kit is built for maintainers who handle many small but important tasks every week: reading issues, preparing review notes, keeping releases consistent, and monitoring repository health. The project is intentionally simple, scriptable, and friendly to automation platforms such as GitHub Actions.

## Why this project exists

Open-source maintainers often spend more time on maintenance than feature work. This toolkit helps reduce repetitive work while keeping humans in control. It does **not** auto-merge code or replace maintainers. Instead, it produces structured suggestions that maintainers can review, edit, and apply.

## Features

- **Issue triage suggestions**: classify issues as `bug`, `feature`, `docs`, `question`, `security`, or `needs-reproduction`.
- **PR review preparation**: produce a checklist for tests, documentation, breaking changes, and security-sensitive files.
- **Release notes generator**: convert Conventional Commit messages into grouped release notes.
- **Repository health report**: summarize open issues, stale items, label coverage, and release readiness.
- **CI-ready CLI**: can be used locally or inside GitHub Actions.
- **No required external AI service**: works with the Python standard library. AI/Codex workflows can be added as optional review helpers.

## Quick start

```bash
PYTHONPATH=src python -m oss_maintainer_kit triage examples/issues.json
PYTHONPATH=src python -m oss_maintainer_kit release-notes examples/commits.txt
PYTHONPATH=src python -m oss_maintainer_kit review-checklist examples/changed_files.txt
```

For local development:

```bash
git clone https://github.com/YOUR_NAME/oss-maintainer-kit.git
cd oss-maintainer-kit
python -m unittest discover -s tests
```

## Example output

```text
# Issue Triage Suggestions

- #12 Login button crashes on mobile
  Suggested labels: bug, needs-reproduction
  Reason: contains failure keywords and lacks reproduction details.

- #15 Add dark mode
  Suggested labels: feature, frontend
  Reason: requests a new user-facing capability.
```

## Use cases

1. A maintainer runs triage before weekly issue cleanup.
2. A contributor opens a PR and the maintainer generates a review checklist.
3. A project prepares a release and generates draft notes from commit messages.
4. A repository uses GitHub Actions to publish a weekly maintenance report.

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md).

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and open an issue before large changes.

## Security

Please report security issues privately by following [SECURITY.md](SECURITY.md).

## License

MIT License. See [LICENSE](LICENSE).
