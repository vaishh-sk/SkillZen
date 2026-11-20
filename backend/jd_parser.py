
import re


def extract_job_description_text(job_description):
    """
    Validate and clean the submitted job description.
    """

    if not job_description:
        raise ValueError("Please enter a job description.")

    cleaned_text = "\n".join(
        line.strip()
        for line in job_description.splitlines()
        if line.strip()
    )

    if len(cleaned_text) < 30:
        raise ValueError(
            "Job description is too short. Please provide more details."
        )

    return cleaned_text


def extract_job_description_sections(job_description):
    """
    Separate required and preferred sections from a job description.
    """

    cleaned_text = extract_job_description_text(job_description)

    required = []
    preferred = []
    general = []

    current_section = "general"

    required_headings = {
        "required skills",
        "requirements",
        "mandatory skills",
        "minimum qualifications",
        "basic qualifications",
        "what you need",
        "must have"
    }

    preferred_headings = {
        "preferred skills",
        "good to have",
        "nice to have",
        "preferred qualifications",
        "bonus skills",
        "additional qualifications"
    }

    for line in cleaned_text.splitlines():

        line = line.strip()

        if not line:
            continue

        heading = re.sub(r"[^a-z ]", "", line.lower()).strip()

        if heading in required_headings:
            current_section = "required"
            continue

        if heading in preferred_headings:
            current_section = "preferred"
            continue

        if current_section == "required":
            required.append(line)

        elif current_section == "preferred":
            preferred.append(line)

        else:
            general.append(line)

    return {
        "required": "\n".join(required),
        "preferred": "\n".join(preferred),
        "general": "\n".join(general)
    }

def extract_alternative_skill_groups(text):
    """
    Detect alternative skill requirements such as:
    Flask or Django
    MySQL or PostgreSQL
    React / Angular

    Each group represents one requirement.
    """

    from itertools import combinations
    from backend.skill_extractor import load_skills, create_skill_pattern

    if not text:
        return []

    skills_dictionary = load_skills()
    alternative_groups = []

    for category, skills in skills_dictionary.items():

        # Build a list of canonical names and their aliases.
        skill_entries = []

        for skill in skills:
            canonical_name = skill["name"]

            for name in [canonical_name] + skill.get("aliases", []):
                skill_entries.append((name, canonical_name))

        # Check pairs of skills within the same category.
        for first, second in combinations(skill_entries, 2):

            first_name, first_canonical = first
            second_name, second_canonical = second

            # Avoid comparing aliases of the same skill.
            if first_canonical == second_canonical:
                continue

            pattern = (
                create_skill_pattern(first_name)
                + r"\s*(?:or|/)\s*"
                + create_skill_pattern(second_name)
            )

            if re.search(pattern, text, re.IGNORECASE):

                group = {
                    "category": category,
                    "alternatives": [
                        first_canonical,
                        second_canonical
                    ]
                }

                if group not in alternative_groups:
                    alternative_groups.append(group)

    return alternative_groups

