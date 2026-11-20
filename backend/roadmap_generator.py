import json
from pathlib import Path


RESOURCES_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "learning_resources.json"
)


def load_learning_resources():
    """
    Load learning resources from the JSON file.
    """

    with open(RESOURCES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_roadmap(missing_skills):
    """
    Generate a learning roadmap for missing skills only.

    Args:
        missing_skills: Dictionary of missing skills grouped by category.

    Returns:
        A list of learning roadmaps.
    """

    learning_resources = load_learning_resources()

    roadmap = []

    for category, skills in missing_skills.items():

        for skill in skills:

            skill_resource = learning_resources.get(skill)

            # Skip skills without available learning resources
            if not skill_resource:
                continue

            roadmap.append({
                "skill": skill,
                "category": category,
                "description": skill_resource["description"],
                "importance": skill_resource["importance"],
                "topics": skill_resource["topics"],
                "resources": skill_resource["resources"],
                "practice": skill_resource["practice"]
            })

    return roadmap

def generate_alternative_roadmap(alternative_group):
    """
    Generate learning roadmaps for all skills in an
    alternative requirement group.
    """

    learning_resources = load_learning_resources()

    category = alternative_group["category"]
    alternatives = alternative_group["alternatives"]

    roadmaps = []

    for skill in alternatives:

        skill_resource = learning_resources.get(skill)

        if not skill_resource:
            continue

        roadmaps.append({
            "skill": skill,
            "category": category,
            "description": skill_resource["description"],
            "importance": skill_resource["importance"],
            "topics": skill_resource["topics"],
            "resources": skill_resource["resources"],
            "practice": skill_resource["practice"]
        })

    return roadmaps
