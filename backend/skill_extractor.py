
import json
import re
from pathlib import Path


SKILLS_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "skills.json"
)


def load_skills():
    """
    Load the technical skills dictionary.
    """

    with open(SKILLS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def create_skill_pattern(skill):
    """
    Create a regex pattern for matching complete skill names.
    """

    if skill == "C":
        return r"(?<![a-zA-Z0-9])C(?![a-zA-Z0-9+#])"

    return (
        r"(?<![a-zA-Z0-9])"
        + re.escape(skill)
        + r"(?![a-zA-Z0-9])"
    )
def is_negated_skill(text, start, end):
    """
    Check whether a skill mention is explicitly negated.

    Examples:
        no experience with Docker
        no knowledge of Kubernetes
        Docker is not a skill I possess
    """

    # Get the text immediately surrounding the skill mention
    before = text[max(0, start - 100):start]
    after = text[end:end + 100]

    # Check for negation before the skill
    negative_before_patterns = [
        r"\bno\s+(?:prior\s+|practical\s+|hands[- ]on\s+)?experience\s+(?:with|in)\s*$",
        r"\bno\s+knowledge\s+of\s*$",
        r"\bnot\s+familiar\s+with\s*$",
        r"\b(?:don't|do not|doesn't|does not)\s+know\s+about\s*$",
        r"\bnever\s+(?:used|worked\s+with|learned)\s*$",
        r"\black\s+(?:of\s+)?experience\s+(?:with|in)\s*$",
        r"\bwithout\s+experience\s+(?:with|in)\s*$",
    ]

    for pattern in negative_before_patterns:
        if re.search(pattern, before, re.IGNORECASE):
            return True

    # Check for negation after the skill
    negative_after_patterns = [
        r"^\s+(?:is\s+)?not\s+a\s+skill\s+(?:I|we)\s+(?:possess|have|know)\b",
        r"^\s+(?:isn't|is\s+not)\s+something\s+(?:I|we)\s+(?:know|use|possess)\b",
        r"^\s+(?:I|we)\s+(?:do\s+not|don't)\s+(?:know|possess|have|use)\b",
    ]

    for pattern in negative_after_patterns:
        if re.search(pattern, after, re.IGNORECASE):
            return True

    return False

def classify_skill_mentions(text):
    """
    Classify skill mentions globally by context:
    possessed, learning, interested, or not_possessed.

    Context propagates across connected skill lists, even when
    skills belong to different categories.
    """

    if not text:
        return {
            "possessed": {},
            "learning": {},
            "interested": {},
            "not_possessed": {}
        }

    skills_dictionary = load_skills()

    classifications = {
        "possessed": {},
        "learning": {},
        "interested": {},
        "not_possessed": {}
    }

    interest_patterns = [
        r"\binterested\s+in\s+(?:learning|studying)\s*$",
        r"\bwant\s+to\s+(?:learn|study)\s*$",
        r"\bwish\s+to\s+(?:learn|study)\s*$",
        r"\bhope\s+to\s+(?:learn|study)\s*$",
        r"\bplanning\s+to\s+(?:learn|study)\s*$",
        r"\blooking\s+to\s+(?:learn|study)\s*$",
    ]

    learning_patterns = [
        r"\bcurrently\s+learning\s*$",
        r"\blearning\s*$",
        r"\bstudying\s*$",
        r"\bbeginner\s+in\s*$",
        r"\bbeginner\s+with\s*$",
        r"\bworking\s+on\s+learning\s*$",
    ]

    connector_pattern = r"^\s*(?:,|and|or|&)\s*$"

    # Step 1: Collect skill mentions from ALL categories.
    all_mentions = []

    for category, skills in skills_dictionary.items():
        for skill in skills:
            canonical_name = skill["name"]
            possible_names = [canonical_name] + skill.get("aliases", [])

            for name in possible_names:
                pattern = create_skill_pattern(name)

                for match in re.finditer(pattern, text, re.IGNORECASE):
                    all_mentions.append({
                        "start": match.start(),
                        "end": match.end(),
                        "skill": canonical_name,
                        "category": category
                    })

    # Step 2: Sort mentions globally by their text positions.
    all_mentions.sort(
        key=lambda item: (item["start"], item["end"])
    )

    # Step 3: Remove duplicate alias matches at the same location.
    unique_mentions = []
    seen_mentions = set()

    for mention in all_mentions:
        key = (
            mention["start"],
            mention["end"],
            mention["skill"],
            mention["category"]
        )

        if key not in seen_mentions:
            seen_mentions.add(key)
            unique_mentions.append(mention)

    # Step 4: Classify in text order with context propagation.
    previous_state = None
    previous_end = None

    for mention in unique_mentions:
        start = mention["start"]
        end = mention["end"]
        canonical_name = mention["skill"]
        category = mention["category"]

        # Explicit negation takes priority.
        if is_negated_skill(text, start, end):
            state = "not_possessed"

        else:
            context_before = text[max(0, start - 120):start]

            if any(
                re.search(pattern, context_before, re.IGNORECASE)
                for pattern in interest_patterns
            ):
                state = "interested"

            elif any(
                re.search(pattern, context_before, re.IGNORECASE)
                for pattern in learning_patterns
            ):
                state = "learning"

            else:
                gap = (
                    text[previous_end:start]
                    if previous_end is not None
                    else ""
                )

                # Carry context across connected skill mentions,
                # regardless of which category each skill belongs to.
                if (
                    previous_state is not None
                    and re.fullmatch(
                        connector_pattern,
                        gap,
                        re.IGNORECASE
                    )
                ):
                    state = previous_state
                else:
                    state = "possessed"

        category_skills = classifications[state].setdefault(
            category, []
        )

        if canonical_name not in category_skills:
            category_skills.append(canonical_name)

        previous_state = state
        previous_end = end

    return classifications

def extract_skills(text):
    if not text:
        return {}

    skills_dictionary = load_skills()
    extracted_skills = {}

    for category, skills in skills_dictionary.items():
        matched_skills = []

        for skill in skills:
            canonical_name = skill["name"]
            possible_names = [canonical_name] + skill.get("aliases", [])

            for name in possible_names:
                pattern = create_skill_pattern(name)

                matches = re.finditer(pattern, text, re.IGNORECASE)

                for match in matches:
                    # Ignore skills explicitly negated in the text
                    if is_negated_skill(
                        text,
                        match.start(),
                        match.end()
                    ):
                        continue

                    matched_skills.append(canonical_name)
                    break

                if canonical_name in matched_skills:
                    break

        if matched_skills:
            extracted_skills[category] = matched_skills

    return extracted_skills