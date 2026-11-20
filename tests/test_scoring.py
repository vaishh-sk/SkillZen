import unittest

from backend.scoring import calculate_match_score


class TestScoring(unittest.TestCase):

    def test_seventy_percent_match(self):

        matching = {
            "programming_languages": ["Python", "Java"],
            "databases": ["SQL", "MySQL"],
            "web_development": ["Flask", "HTML", "CSS"]
        }

        missing = {
            "tools_and_platforms": ["Docker", "AWS"],
            "core_concepts": ["DBMS"]
        }

        result = calculate_match_score(matching, missing)

        self.assertEqual(result["match_score"], 70.0)
        self.assertEqual(result["matching_count"], 7)
        self.assertEqual(result["missing_count"], 3)
        self.assertEqual(result["total_required"], 10)

    def test_perfect_match(self):

        matching = {
            "programming_languages": ["Python", "Java"]
        }

        missing = {}

        result = calculate_match_score(matching, missing)

        self.assertEqual(result["match_score"], 100.0)

    def test_zero_match(self):

        matching = {}

        missing = {
            "programming_languages": ["Python", "Java"]
        }

        result = calculate_match_score(matching, missing)

        self.assertEqual(result["match_score"], 0.0)

    def test_no_required_skills(self):

        result = calculate_match_score({}, {})

        self.assertEqual(result["match_score"], 0)
        self.assertEqual(result["total_required"], 0)

    def test_partial_match(self):

        matching = {
            "programming_languages": ["Python"]
        }

        missing = {
            "programming_languages": ["Java", "C++"]
        }

        result = calculate_match_score(matching, missing)

        self.assertEqual(result["match_score"], 33.33)


if __name__ == "__main__":
    unittest.main()