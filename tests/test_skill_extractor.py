import unittest

from backend.skill_extractor import extract_skills


class TestSkillExtractor(unittest.TestCase):

    def test_extract_programming_languages(self):
        text = "I have experience in Python, Java and C++."

        result = extract_skills(text)

        self.assertIn(
            "Python",
            result["programming_languages"]
        )

        self.assertIn(
            "Java",
            result["programming_languages"]
        )

        self.assertIn(
            "C++",
            result["programming_languages"]
        )

    def test_extract_multiple_categories(self):
        text = """
        Python, Flask, SQL, MySQL, Git and Docker.
        """

        result = extract_skills(text)

        self.assertIn("Python", result["programming_languages"])
        self.assertIn("Flask", result["web_development"])
        self.assertIn("SQL", result["databases"])
        self.assertIn("Docker", result["tools_and_platforms"])

    def test_case_insensitive_matching(self):
        text = "PYTHON and flask developer"

        result = extract_skills(text)

        self.assertIn("Python", result["programming_languages"])
        self.assertIn("Flask", result["web_development"])

    def test_empty_text(self):
        result = extract_skills("")

        self.assertEqual(result, {})

    def test_no_partial_match_for_c(self):
        text = "I have good communication skills."

        result = extract_skills(text)

        self.assertNotIn(
            "C",
            result.get("programming_languages", [])
        )


if __name__ == "__main__":
    unittest.main()