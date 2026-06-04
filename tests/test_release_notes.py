import unittest

from oss_maintainer_kit.release_notes import build_release_notes, parse_commit


class ReleaseNoteTests(unittest.TestCase):
    def test_parse_scoped_commit(self):
        entry = parse_commit("feat(cli): add health command")
        self.assertEqual(entry.kind, "feat")
        self.assertEqual(entry.scope, "cli")
        self.assertEqual(entry.description, "add health command")

    def test_grouped_release_notes(self):
        notes = build_release_notes(["feat: add triage", "fix: handle empty input"], "0.1.0")
        self.assertIn("# Release Notes: 0.1.0", notes)
        self.assertIn("## Features", notes)
        self.assertIn("## Bug fixes", notes)


if __name__ == "__main__":
    unittest.main()
