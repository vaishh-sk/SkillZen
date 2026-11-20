import unittest

from backend.skill_matcher import compare_skills


class TestSkillMatcher(unittest.TestCase):

    def test_matching_and_missing_skills(self):

        resume_skills = {
            "programming_languages": ["Python", "Java"],
            "databases": ["SQL"]
        }

        jd_skills = {
            "programming_languages": ["Python", "C++"],
            "databases": ["SQL", "MongoDB"]
        }

        result = compare_skills(resume_skills, jd_skills)

        self.assertEqual(
            result["matching_skills"]["programming_languages"],
            ["Python"]
        )

        self.assertEqual(
            result["missing_skills"]["programming_languages"],
            ["C++"]
        )

        self.assertEqual(
            result["matching_skills"]["databases"],
            ["SQL"]
        )

        self.assertEqual(
            result["missing_skills"]["databases"],
            ["MongoDB"]
        )

    def test_all_skills_match(self):

        resume_skills = {
            "programming_languages": ["Python", "Java"]
        }

        jd_skills = {
            "programming_languages": ["Python", "Java"]
        }

        result = compare_skills(resume_skills, jd_skills)

        self.assertEqual(
            result["matching_skills"]["programming_languages"],
            ["Python", "Java"]
        )

        self.assertEqual(result["missing_skills"], {})

    def test_all_skills_missing(self):

        resume_skills = {}

        jd_skills = {
            "programming_languages": ["Python", "Java"]
        }

        result = compare_skills(resume_skills, jd_skills)

        self.assertEqual(result["matching_skills"], {})

        self.assertEqual(
            result["missing_skills"]["programming_languages"],
            ["Python", "Java"]
        )

    def test_empty_job_description_skills(self):

        result = compare_skills(
            {"programming_languages": ["Python"]},
            {}
        )

        self.assertEqual(result["matching_skills"], {})
        self.assertEqual(result["missing_skills"], {})

    def test_resume_has_extra_skills(self):

        resume_skills = {
            "programming_languages": ["Python", "Java", "C++"]
        }

        jd_skills = {
            "programming_languages": ["Python"]
        }

        result = compare_skills(resume_skills, jd_skills)

        self.assertEqual(
            result["matching_skills"]["programming_languages"],
            ["Python"]
        )

        self.assertEqual(result["missing_skills"], {})


if __name__ == "__main__":
    unittest.main()