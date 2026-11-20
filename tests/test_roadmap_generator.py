import unittest

from backend.roadmap_generator import generate_roadmap


class TestRoadmapGenerator(unittest.TestCase):

    def test_generate_roadmap_for_missing_skills(self):

        missing_skills = {
            "tools_and_platforms": ["Docker", "AWS"],
            "web_development": ["Flask"]
        }

        result = generate_roadmap(missing_skills)

        self.assertEqual(len(result), 3)

        roadmap_skills = [
            item["skill"] for item in result
        ]

        self.assertIn("Docker", roadmap_skills)
        self.assertIn("AWS", roadmap_skills)
        self.assertIn("Flask", roadmap_skills)

    def test_matched_skills_not_included(self):

        missing_skills = {
            "tools_and_platforms": ["Docker"]
        }

        result = generate_roadmap(missing_skills)

        roadmap_skills = [
            item["skill"] for item in result
        ]

        self.assertNotIn("Python", roadmap_skills)
        self.assertIn("Docker", roadmap_skills)

    def test_empty_missing_skills(self):

        result = generate_roadmap({})

        self.assertEqual(result, [])

    def test_unknown_skill_is_skipped(self):

        missing_skills = {
            "programming_languages": ["SomeUnknownSkill"]
        }

        result = generate_roadmap(missing_skills)

        self.assertEqual(result, [])

    def test_roadmap_contains_required_information(self):

        missing_skills = {
            "tools_and_platforms": ["Docker"]
        }

        result = generate_roadmap(missing_skills)

        docker_roadmap = result[0]

        self.assertIn("description", docker_roadmap)
        self.assertIn("importance", docker_roadmap)
        self.assertIn("topics", docker_roadmap)
        self.assertIn("resources", docker_roadmap)
        self.assertIn("practice", docker_roadmap)


if __name__ == "__main__":
    unittest.main()