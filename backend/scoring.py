
def calculate_match_score(
    matching_skills,
    missing_skills,
    matching_alternative_groups=None,
    missing_alternative_groups=None
):
    """
    Calculate the match score using individual requirements
    and alternative skill groups.

    Each alternative group counts as one requirement.
    """

    matching_alternative_groups = matching_alternative_groups or []
    missing_alternative_groups = missing_alternative_groups or []

    matching_count = sum(
        len(skills) for skills in matching_skills.values()
    ) + len(matching_alternative_groups)

    missing_count = sum(
        len(skills) for skills in missing_skills.values()
    ) + len(missing_alternative_groups)

    total_required = matching_count + missing_count

    if total_required == 0:
        return {
            "match_score": 0,
            "matching_count": 0,
            "missing_count": 0,
            "total_required": 0
        }

    score = round(
        (matching_count / total_required) * 100,
        2
    )

    return {
        "match_score": score,
        "matching_count": matching_count,
        "missing_count": missing_count,
        "total_required": total_required
    }
