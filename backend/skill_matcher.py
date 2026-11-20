
def compare_skills(resume_skills, jd_skills):
    """
    Compare individual resume skills against job skills.
    """

    matching_skills = {}
    missing_skills = {}

    for category, required_skills in jd_skills.items():

        candidate_skills = resume_skills.get(category, [])

        matched = [
            skill for skill in required_skills
            if skill in candidate_skills
        ]

        missing = [
            skill for skill in required_skills
            if skill not in candidate_skills
        ]

        if matched:
            matching_skills[category] = matched

        if missing:
            missing_skills[category] = missing

    return {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }


def compare_alternative_groups(resume_skills, alternative_groups):
    """
    Check whether at least one skill in each alternative group
    is present in the candidate's resume.
    """

    matching_groups = []
    missing_groups = []

    for group in alternative_groups:

        category = group["category"]
        alternatives = group["alternatives"]

        candidate_skills = resume_skills.get(category, [])

        matched_alternatives = [
            skill for skill in alternatives
            if skill in candidate_skills
        ]

        group_result = {
            "category": category,
            "alternatives": alternatives,
            "matched_skill": (
                matched_alternatives[0]
                if matched_alternatives else None
            )
        }

        if matched_alternatives:
            matching_groups.append(group_result)
        else:
            missing_groups.append(group_result)

    return {
        "matching_alternative_groups": matching_groups,
        "missing_alternative_groups": missing_groups
    }


def compare_job_skills(
    resume_skills,
    required_skills,
    preferred_skills,
    required_alternative_groups=None,
    preferred_alternative_groups=None
):
    """
    Compare resume skills against required and preferred skills,
    including alternative skill requirements.
    """

    required_alternative_groups = required_alternative_groups or []
    preferred_alternative_groups = preferred_alternative_groups or []

    # Remove alternative skills from individual requirements
    # to prevent counting them twice.
    def remove_alternative_skills(skills, groups):

        filtered_skills = {
            category: list(category_skills)
            for category, category_skills in skills.items()
        }

        for group in groups:

            category = group["category"]
            alternatives = group["alternatives"]

            if category in filtered_skills:
                filtered_skills[category] = [
                    skill for skill in filtered_skills[category]
                    if skill not in alternatives
                ]

        return filtered_skills

    normal_required_skills = remove_alternative_skills(
        required_skills,
        required_alternative_groups
    )

    normal_preferred_skills = remove_alternative_skills(
        preferred_skills,
        preferred_alternative_groups
    )

    # Compare individual skills.
    required_comparison = compare_skills(
        resume_skills,
        normal_required_skills
    )

    preferred_comparison = compare_skills(
        resume_skills,
        normal_preferred_skills
    )

    # Compare alternative groups.
    required_group_comparison = compare_alternative_groups(
        resume_skills,
        required_alternative_groups
    )

    preferred_group_comparison = compare_alternative_groups(
        resume_skills,
        preferred_alternative_groups
    )

    return {
        "required": {
            **required_comparison,
            **required_group_comparison
        },
        "preferred": {
            **preferred_comparison,
            **preferred_group_comparison
        }
    }

