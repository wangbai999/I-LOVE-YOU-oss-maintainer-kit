import unittest

from oss_maintainer_kit.triage import suggest_labels


class TriageTests(unittest.TestCase):
    def test_bug_without_reproduction_gets_needs_reproduction(self):
        issue = {"number": 1, "title": "App crashes on mobile", "body": "It fails"}
        suggestion = suggest_labels(issue)
        self.assertIn("bug", suggestion.labels)
        self.assertIn("needs-reproduction", suggestion.labels)

    def test_docs_issue(self):
        issue = {"number": 2, "title": "README typo", "body": "Small documentation fix"}
        suggestion = suggest_labels(issue)
        self.assertIn("docs", suggestion.labels)


if __name__ == "__main__":
    unittest.main()
