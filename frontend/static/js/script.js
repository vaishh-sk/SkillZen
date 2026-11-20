
document.addEventListener("DOMContentLoaded", () => {

    const analyzerForm = document.getElementById("analyzer-form");
    const resultsSection = document.getElementById("results-section");
    const resultsContent = document.getElementById("results-content");

    if (!analyzerForm) {
        return;
    }

    // Handle clicks on missing required skill buttons
    
resultsContent.addEventListener("click", (event) => {

    const roadmapPanel = document.getElementById("roadmap-content");

    if (!roadmapPanel) {
        return;
    }

    // 1. Handle individual missing skill clicks
    const skillButton = event.target.closest(".missing-skill-btn");

    if (skillButton) {

        const selectedSkill = skillButton.dataset.skill;
        const roadmap = window.skillZenRoadmap || [];

        const selectedRoadmap = roadmap.find(
            item => item.skill === selectedSkill
        );

        document.querySelectorAll(".missing-skill-btn").forEach(button => {
            button.classList.toggle(
                "active",
                button.dataset.skill === selectedSkill
            );
        });

        document.querySelectorAll(".alternative-roadmap-choice").forEach(button => {
            button.classList.remove("active");
        });

        if (!selectedRoadmap) {
            roadmapPanel.innerHTML = `
                <p>A learning roadmap for ${escapeHTML(selectedSkill)}
                is coming soon.</p>
            `;
            return;
        }

        roadmapPanel.innerHTML = renderSingleRoadmap(selectedRoadmap);

        roadmapPanel.scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });

        return;
    }


    // 2. Handle alternative group clicks (e.g. Flask OR Django)
    const alternativeButton = event.target.closest(".alternative-skill-btn");

    if (alternativeButton) {

        const groupIndex = Number(
            alternativeButton.dataset.alternativeIndex
        );

        const alternativeGroups =
            window.skillZenAlternativeRoadmaps || [];

        const selectedGroup = alternativeGroups[groupIndex];

        document.querySelectorAll(".alternative-skill-btn").forEach(button => {
            button.classList.toggle(
                "active",
                button.dataset.alternativeIndex === String(groupIndex)
            );
        });

        document.querySelectorAll(".missing-skill-btn").forEach(button => {
            button.classList.remove("active");
        });

        if (!selectedGroup || !selectedGroup.roadmaps.length) {
            roadmapPanel.innerHTML = `
                <p>Roadmaps for these alternative skills are coming soon.</p>
            `;
            return;
        }

        // Show a choice between the available alternatives
        roadmapPanel.innerHTML = `
            <div class="alternative-roadmap-selector">

                <h4>Choose which skill you want to learn</h4>

                <p>You only need to explore the option that best fits your goal.</p>

                <div class="alternative-roadmap-buttons">

                    ${selectedGroup.roadmaps.map(item => `
                        <button
                            type="button"
                            class="alternative-roadmap-choice"
                            data-alt-skill="${escapeHTML(item.skill)}"
                        >
                            Explore ${escapeHTML(item.skill)}
                        </button>
                    `).join("")}

                </div>

                <div id="alternative-roadmap-detail">
                    <p>Select one of the skills above to view its learning roadmap.</p>
                </div>

            </div>
        `;

        roadmapPanel.scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });

        return;
    }


    // 3. Handle selection of an individual alternative
    const choiceButton = event.target.closest(".alternative-roadmap-choice");

    if (choiceButton) {

        const selectedSkill = choiceButton.dataset.altSkill;

        const alternativeRoadmaps =
            window.skillZenAlternativeRoadmaps || [];

        let selectedRoadmap = null;

        for (const group of alternativeRoadmaps) {

            selectedRoadmap = group.roadmaps.find(
                item => item.skill === selectedSkill
            );

            if (selectedRoadmap) {
                break;
            }
        }

        document.querySelectorAll(".alternative-roadmap-choice").forEach(button => {
            button.classList.toggle(
                "active",
                button.dataset.altSkill === selectedSkill
            );
        });

        const detailPanel = document.getElementById(
            "alternative-roadmap-detail"
        );

        if (!detailPanel) {
            return;
        }

        if (!selectedRoadmap) {
            detailPanel.innerHTML = `
                <p>A roadmap for ${escapeHTML(selectedSkill)}
                is coming soon.</p>
            `;
            return;
        }

        detailPanel.innerHTML = renderSingleRoadmap(selectedRoadmap);
    }

    });



    // Submit the analysis form
    analyzerForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const submitButton = analyzerForm.querySelector("button[type='submit']");
        const formData = new FormData(analyzerForm);
        const originalButtonText = submitButton.textContent;

        submitButton.disabled = true;
        submitButton.textContent = "Analyzing...";

        resultsSection.hidden = true;

        try {

            const response = await fetch("/analyze", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                alert(result.message || "Analysis failed.");
                return;
            }

            displayResults(result);

            resultsSection.hidden = false;

            resultsSection.scrollIntoView({
                behavior: "smooth"
            });

        } catch (error) {

            console.error("Analysis error:", error);
            alert("Unable to connect to SkillZen. Please try again.");

        } finally {

            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;

        }
    });


    // Display all analysis results
    

function displayResults(result) {

    const score = result.score;

    window.skillZenRoadmap = result.roadmap || [];
    window.skillZenAlternativeRoadmaps =
        result.alternative_roadmaps || [];

    const requiredMatchingGroups =
        result.required_matching_groups || [];

    const requiredMissingGroups =
        result.required_missing_groups || [];

    const preferredMatchingGroups =
        result.preferred_matching_groups || [];

    const preferredMissingGroups =
        result.preferred_missing_groups || [];

    function renderAlternativeGroups(
        groups,
        isMissing = false,
        clickable = false
    ) {

        if (!groups.length) {
            return "";
        }

        return `
            <div class="alternative-groups">

                <h4>Alternative Requirements</h4>

                ${groups.map((group, index) => {

                    const alternatives =
                        group.alternatives.join(" OR ");

                    if (isMissing && clickable) {

                        return `
                            <button
                                type="button"
                                class="skill-tag missing-alternative alternative-skill-btn"
                                data-alternative-index="${index}"
                            >
                                ${escapeHTML(alternatives)}
                                <span>Not matched · Click for roadmap</span>
                            </button>
                        `;
                    }

                    if (isMissing) {

                        return `
                            <div class="skill-tag missing-alternative">
                                ${escapeHTML(alternatives)}
                                <span>Not matched</span>
                            </div>
                        `;
                    }

                    return `
                        <div class="skill-tag matched-alternative">
                            ${escapeHTML(alternatives)}
                            <span>
                                Matched: ${escapeHTML(group.matched_skill)}
                            </span>
                        </div>
                    `;

                }).join("")}

            </div>
        `;
    }

    resultsContent.innerHTML = `

        <div class="score-card">
            <h3>Overall Match Score</h3>

            <div class="score-value">
                ${score.match_score}%
            </div>

            <p>Your resume matches ${score.matching_count}
            out of ${score.total_required} required skills.</p>
        </div>


        <div class="summary-cards">

            <div class="summary-card">
                <h3>${score.total_required}</h3>
                <p>Total Required Skills</p>
            </div>

            <div class="summary-card">
                <h3>${score.matching_count}</h3>
                <p>Matching Skills</p>
            </div>

            <div class="summary-card">
                <h3>${score.missing_count}</h3>
                <p>Missing Skills</p>
            </div>

        </div>


        <h3 class="section-heading">Required Skills</h3>

        <div class="skills-container">

            <div class="skills-card">
                <h3>Matching Skills</h3>

                ${renderSkills(result.matching_skills, false)}

                ${renderAlternativeGroups(
                    requiredMatchingGroups
                )}
            </div>

            <div class="skills-card">
                <h3>Skills to Develop</h3>

                <p>Select a skill to explore its learning roadmap.</p>

                ${renderSkills(result.missing_skills, true)}

                ${renderAlternativeGroups(
                    requiredMissingGroups,
                    true,
                    true
                )}
            </div>

        </div>


        <h3 class="section-heading">Preferred Skills</h3>

        <div class="skills-container">

            <div class="skills-card">
                <h3>Preferred Skills You Have</h3>

                ${renderSkills(
                    result.preferred_matching_skills,
                    false
                )}

                ${renderAlternativeGroups(
                    preferredMatchingGroups
                )}
            </div>

            <div class="skills-card">
                <h3>Additional Skills to Explore</h3>

                ${renderSkills(
                    result.preferred_missing_skills,
                    false
                )}

                ${renderAlternativeGroups(
                    preferredMissingGroups,
                    true,
                    false
                )}
            </div>

        </div>


        <div class="roadmap-card" id="roadmap-section">

            <h3>Your Learning Roadmap</h3>

            <div id="roadmap-content">
                <p>Select a missing required skill above to view its learning roadmap.</p>
            </div>

        </div>

    `;
}




    // Render skills by category
    function renderSkills(skills, clickable = false) {

        let html = "";

        for (const [category, skillList] of Object.entries(skills || {})) {

            html += `
                <div class="skill-category">

                    <h4>${formatCategory(category)}</h4>

                    <div class="skill-tags">

                        ${skillList.map(skill => {

                            const safeSkill = escapeHTML(skill);

                            if (clickable) {
                                return `
                                    <button
                                        type="button"
                                        class="skill-tag missing-skill-btn"
                                        data-skill="${safeSkill}"
                                    >
                                        ${safeSkill}
                                    </button>
                                `;
                            }

                            return `
                                <span class="skill-tag">
                                    ${safeSkill}
                                </span>
                            `;

                        }).join("")}

                    </div>

                </div>
            `;
        }

        return html || "<p>No skills found.</p>";
    }


    // Render one selected skill's roadmap
    function renderSingleRoadmap(item) {

        return `
            <div class="roadmap-item">

                <h4>${escapeHTML(item.skill)}</h4>

                <p>${escapeHTML(item.description)}</p>

                <p>
                    <strong>Why it matters:</strong>
                    ${escapeHTML(item.importance)}
                </p>

                <h5>Topics to Learn</h5>

                <ul>
                    ${(item.topics || []).map(topic =>
                        `<li>${escapeHTML(topic)}</li>`
                    ).join("")}
                </ul>

                <h5>Practice</h5>

                <ul>
                    ${(item.practice || []).map(task =>
                        `<li>${escapeHTML(task)}</li>`
                    ).join("")}
                </ul>

                <h5>Learning Resources</h5>

                ${(item.resources || []).map(resource => `
                    <p>
                        <a href="${escapeHTML(resource.url)}"
                           target="_blank"
                           rel="noopener noreferrer">
                            ${escapeHTML(resource.name)}
                        </a>
                    </p>
                `).join("")}

            </div>
        `;
    }


    // Escape HTML before inserting dynamic text
    function escapeHTML(value) {

        return String(value).replace(/[&<>"']/g, character => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        })[character]);
    }


    // Format category names
    function formatCategory(category) {

        return category
            .replaceAll("_", " ")
            .replace(/\b\w/g, letter => letter.toUpperCase());
    }

});
