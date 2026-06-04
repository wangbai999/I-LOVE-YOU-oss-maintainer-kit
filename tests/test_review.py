import unittest

from oss_maintainer_kit.review import build_review_checklist


class ReviewTests(unittest.TestCase):
    def test_security_file_adds_warning(self):
        checklist = build_review_checklist(["src/auth/token_store.py"])
        self.assertIn("Security-sensitive", checklist)


if __name__ == "__main__":
    unittest.main()
