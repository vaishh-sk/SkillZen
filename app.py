
from flask import Flask, render_template, jsonify, request

from backend.resume_parser import extract_text_from_pdf
from backend.jd_parser import (
    extract_job_description_sections,
    extract_alternative_skill_groups
)
from backend.skill_extractor import (
    extract_skills,
    classify_skill_mentions
)
from backend.skill_matcher import compare_job_skills
from backend.scoring import calculate_match_score
from backend.roadmap_generator import (
    generate_roadmap,
    generate_alternative_roadmap
)

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "success",
        "message": "SkillZen is running."
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    # 1. Validate resume upload
    if "resume" not in request.files:
        return jsonify({
            "status": "error",
            "message": "Please upload your resume."
        }), 400

    resume_file = request.files["resume"]

    if resume_file.filename == "":
        return jsonify({
            "status": "error",
            "message": "No resume selected."
        }), 400

    if not resume_file.filename.lower().endswith(".pdf"):
        return jsonify({
            "status": "error",
            "message": "Only PDF files are allowed."
        }), 400

    try:

        # 2. Extract resume text
        resume_text = extract_text_from_pdf(resume_file)

        # 2.1 Classify resume skill mentions by context
        resume_skill_classification = classify_skill_mentions(resume_text)

        # 3. Separate job description sections
        job_description = request.form.get(
            "job_description", ""
        )

        jd_sections = extract_job_description_sections(
            job_description
        )

        # 4. Extract skills from resume
        resume_skills = extract_skills(resume_text)

        # 5. Extract required and preferred JD skills
        # If no required section exists, use general text.
        required_text = (
            jd_sections["required"]
            if jd_sections["required"].strip()
            else jd_sections["general"]
        )

        required_skills = extract_skills(required_text)

        preferred_skills = extract_skills(
            jd_sections["preferred"]
        )
        required_alternative_groups = extract_alternative_skill_groups(
            required_text
        )

        preferred_alternative_groups = extract_alternative_skill_groups(
            jd_sections["preferred"]
        )

        # 6. Compare required and preferred skills separately
        comparison = compare_job_skills(
            resume_skills,
            required_skills,
            preferred_skills,
            required_alternative_groups,
            preferred_alternative_groups
        )

        required_comparison = comparison["required"]
        preferred_comparison = comparison["preferred"]

        required_matching_groups = required_comparison[
            "matching_alternative_groups"
        ]

        required_missing_groups = required_comparison[
            "missing_alternative_groups"
        ]

        preferred_matching_groups = preferred_comparison[
            "matching_alternative_groups"
        ]

        preferred_missing_groups = preferred_comparison[
            "missing_alternative_groups"
        ]

        matching_skills = required_comparison["matching_skills"]
        missing_skills = required_comparison["missing_skills"]

        preferred_matching_skills = (
            preferred_comparison["matching_skills"]
        )

        preferred_missing_skills = (
            preferred_comparison["missing_skills"]
        )

        # 7. Calculate score using required skills only
        score = calculate_match_score(
            matching_skills,
            missing_skills,
            required_matching_groups,
            required_missing_groups
        )

        # 8. Generate roadmap for missing required skills
        roadmap = generate_roadmap(missing_skills)
        alternative_roadmaps = []

        for group in required_missing_groups:

            alternative_roadmaps.append({
                "alternatives": group["alternatives"],
                "roadmaps": generate_alternative_roadmap(group)
            })

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except Exception:
        app.logger.exception("Analysis failed.")

        return jsonify({
            "status": "error",
            "message": "Something went wrong during analysis."
        }), 500

    # 9. Return complete analysis
    return jsonify({
    "status": "success",
    "message": "Skill analysis completed successfully.",
    "resume_skills": resume_skills,
    "required_jd_skills": required_skills,
    "resume_skill_classification": resume_skill_classification,
    "preferred_jd_skills": preferred_skills,
    "matching_skills": matching_skills,
    "missing_skills": missing_skills,
    "preferred_matching_skills": preferred_matching_skills,
    "preferred_missing_skills": preferred_missing_skills,

    # Alternative skill groups
    "required_matching_groups": required_matching_groups,
    "required_missing_groups": required_missing_groups,
    "preferred_matching_groups": preferred_matching_groups,
    "preferred_missing_groups": preferred_missing_groups,

    "score": score,
    "roadmap": roadmap,
    "alternative_roadmaps": alternative_roadmaps,
    })


if __name__ == "__main__":
    app.run(debug=True)
