const API_URL = "http://127.0.0.1:8000";


// ------------------------------------
// NAVIGATION
// ------------------------------------

function showSection(sectionId) {

    const sections = document.querySelectorAll(".section");

    sections.forEach(section => {
        section.classList.remove("active");
    });

    document.getElementById(sectionId).classList.add("active");


    const buttons = document.querySelectorAll(".nav-btn");

    buttons.forEach(button => {
        button.classList.remove("active");
    });

}


// ------------------------------------
// SAVE EXPERIENCE
// ------------------------------------

async function saveExperience() {

    const data = {

        project_name:
            document.getElementById("projectName").value,

        experience_type:
            document.getElementById("experienceType").value,

        title:
            document.getElementById("experienceTitle").value,

        description:
            document.getElementById("description").value,

        solution:
            document.getElementById("solution").value,

        lesson:
            document.getElementById("lesson").value
    };


    if (!data.title ||
        !data.description ||
        !data.solution ||
        !data.lesson) {

        document.getElementById("saveMessage").innerText =
            "Please fill all fields.";

        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/experiences`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );


        const result = await response.json();


        if (response.ok) {

            document.getElementById("saveMessage").innerText =
                "✓ Experience saved to Hindsight!";

            // document.getElementById("experienceCount").innerText =
            //     "1";

            // document.getElementById("dashboardExperienceCount").innerText =
            //     "1";

            loadExperienceCount();

        } else {

            document.getElementById("saveMessage").innerText =
                "Error: " + JSON.stringify(result);

        }

    } catch (error) {

        document.getElementById("saveMessage").innerText =
            "Could not connect to backend. Is FastAPI running?";

        console.error(error);
    }

}



// ------------------------------------
// SEARCH MEMORY
// ------------------------------------

async function searchMemory() {

    const query =
        document.getElementById("memoryQuery").value;


    if (!query) {
        return;
    }


    const resultsContainer =
        document.getElementById("memoryResults");


    resultsContainer.innerHTML =
        "<p>Searching project memory...</p>";


    try {

        const response = await fetch(
            `${API_URL}/memory?query=${encodeURIComponent(query)}`
        );


        const data = await response.json();


        resultsContainer.innerHTML = "";


        if (!data.memories || data.memories.length === 0) {

            resultsContainer.innerHTML =
                "<p class='empty-message'>No relevant memories found.</p>";

            return;
        }


        data.memories.forEach(memory => {

            const card =
                document.createElement("div");

            card.className = "memory-result";


            card.innerHTML = `

                <div class="memory-type">
                    ${memory.type || "Memory"}
                </div>

                <p>
                    ${memory.text}
                </p>

            `;


            resultsContainer.appendChild(card);

        });


    } catch (error) {

        resultsContainer.innerHTML =
            "<p>Could not connect to backend.</p>";

        console.error(error);
    }

}



// ------------------------------------
// GENERATE HINDSIGHT
// ------------------------------------

async function generateHindsight() {

    const resultContainer =
        document.getElementById("hindsightResult");


    resultContainer.innerHTML =
        "<p>AI is analyzing project memories...</p>";


    try {

        const response = await fetch(
            `${API_URL}/hindsight`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({


                    query: `
                    You are the ProjectHindsight learning agent.

                    Analyze the previous project experiences.

                    Organize the result into exactly these sections:

                    WHAT WORKED
                    WHAT FAILED
                    IMPORTANT DECISIONS
                    REJECTED IDEAS
                    LESSONS FOR FUTURE PROJECTS

                    Use concise bullet points.

                    Do not invent information.
                    Only use information available in project memory.

                    `
                })
            }
        );


        const data = await response.json();


        resultContainer.innerText =
            data.hindsight || "No hindsight generated.";


    } catch (error) {

        resultContainer.innerText =
            "Could not connect to backend.";

        console.error(error);
    }

}



// ------------------------------------
// REVIVE OLD IDEA
// ------------------------------------


async function reviveIdea() {

    const message =
        document.getElementById("reviveMessage");

    message.innerText =
        "Searching previous project decisions...";

    try {

        const response = await fetch(
            `${API_URL}/revive-idea`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    idea: "Google Maps API"
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

            message.innerText =
                data.result;

        } else {

            message.innerText =
                "Could not find previous decision.";

        }

    } catch (error) {

        message.innerText =
            "Could not connect to backend.";

        console.error(error);

    }

}

// function reviveIdea() {

//     document.getElementById("reviveMessage").innerText =
//         "✓ Old decision found. Consider whether the original reason still applies to the current project.";

// }


function dismissIdea() {

    document.getElementById("reviveMessage").innerText =
        "Idea marked as not relevant to the current project.";

}


// ------------------------------------
// LOAD EXPERIENCE COUNT
// ------------------------------------

async function loadExperienceCount() {

    try {

        const response = await fetch(
            `${API_URL}/experience-count`
        );

        const data = await response.json();

        document.getElementById("experienceCount").innerText =
            data.count;

        document.getElementById("dashboardExperienceCount").innerText =
            data.count;

    } catch (error) {

        console.error(
            "Could not load experience count:",
            error
        );

    }

}


loadExperienceCount();

// ------------------------------------
// CREATE NEW PROJECT
// ------------------------------------

function createProject() {

    const projectName =
        document.getElementById("newProjectName").value.trim();

    const projectDescription =
        document.getElementById("newProjectDescription").value.trim();

    const message =
        document.getElementById("projectMessage");


    if (!projectName || !projectDescription) {

        message.innerText =
            "Please enter the project name and description.";

        return;
    }


    // Save current project information
    localStorage.setItem(
        "currentProjectName",
        projectName
    );

    localStorage.setItem(
        "currentProjectDescription",
        projectDescription
    );


    message.innerText =
        "✓ Project created successfully.";


    // Open the project workspace
    setTimeout(() => {

        showSection("projectWorkspace");

    }, 500);

}



// ------------------------------------
// LOAD CURRENT PROJECT
// ------------------------------------

function loadCurrentProject() {

    const projectName =
        localStorage.getItem("currentProjectName");

    const projectDescription =
        localStorage.getItem("currentProjectDescription");

    if (!projectName) {
        return;
    }

    // Project Workspace

    const nameElement =
        document.getElementById("currentProjectName");

    const descriptionElement =
        document.getElementById("currentProjectDescription");


    if (nameElement) {

        nameElement.innerText =
            projectName;
    }


    if (descriptionElement) {

        descriptionElement.innerText =
            projectDescription;
    }


    // Dashboard

    const dashboardName =
        document.getElementById("dashboardProjectName");

    const dashboardDescription =
        document.getElementById("dashboardProjectDescription");


    if (dashboardName) {

        dashboardName.innerText =
            projectName;
    }


    if (dashboardDescription) {

        dashboardDescription.innerText =
            projectDescription;
    }
}

loadCurrentProject();


// function loadCurrentProject() {

//     const projectName =
//         localStorage.getItem("currentProjectName");

//     const projectDescription =
//         localStorage.getItem("currentProjectDescription");


//     if (!projectName) {
//         return;
//     }


//     const nameElement =
//         document.getElementById("currentProjectName");

//     const descriptionElement =
//         document.getElementById("currentProjectDescription");


//     if (nameElement) {

//         nameElement.innerText =
//             projectName;

//     }


//     if (descriptionElement) {

//         descriptionElement.innerText =
//             projectDescription;

//     }

// }


// loadCurrentProject();

// ------------------------------------
// PROJECT 2 - HAVE WE FACED THIS BEFORE?
// ------------------------------------


async function findHistoricalExperience() {

    const query =
        document.getElementById("projectProblem").value.trim();

    const resultContainer =
        document.getElementById("historicalExperience");


    if (!query) {

        resultContainer.innerHTML =
            "<p class='empty-message'>Please describe the problem first.</p>";

        return;
    }


    resultContainer.innerHTML =
        "<p>Searching previous project experiences...</p>";


    try {

        const response = await fetch(
            `${API_URL}/memory?query=${encodeURIComponent(query)}`
        );


        const data = await response.json();


        resultContainer.innerHTML = "";


        if (!response.ok ||
            !data.memories ||
            data.memories.length === 0) {

            resultContainer.innerHTML = `
                <div class="memory-result">

                    <div class="memory-type">
                        NO HISTORICAL EXPERIENCE FOUND
                    </div>

                    <p>
                        No similar experience was found
                        in previous project history.
                    </p>

                </div>
            `;

            return;
        }


        const memory = data.memories[0];


        const card =
            document.createElement("div");

        card.className = "revive-card";


        card.innerHTML = `

            <span class="small-label">
                POTENTIAL HISTORICAL EXPERIENCE FOUND
            </span>


            <h2>
                Emergency Response System
            </h2>

            <div class="historical-detail">

                <strong>What happened</strong>

                <p>
                    ${memory.text}
                </p>

            </div>

           <div class="historical-detail">

                <strong>Historical Lesson</strong>

                <p id="historicalLesson">
                    Finding applicable lesson...
                </p>

            </div>


            <p class="warning">
                A similar situation was found in
                previous project memory.
            </p>


            <div class="reference-actions">

                <button
                    class="secondary-btn"
                    onclick="useHistoricalReference()">
                    Use as Reference
                </button>


                <button
                    class="text-btn"
                    onclick="dismissHistoricalExperience()">
                    Dismiss
                </button>

            </div>


            <p id="project2Message"></p>

        `;


        resultContainer.appendChild(card);
        getHistoricalLesson(query);


    } catch (error) {

        resultContainer.innerHTML =
            "<p>Could not connect to backend.</p>";

        console.error(error);
    }
}


async function getHistoricalLesson(query) {

    const lessonElement =
        document.getElementById("historicalLesson");

    try {

        const response = await fetch(
            `${API_URL}/historical-lesson`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    query: query
                })
            }
        );


        const data = await response.json();


        if (response.ok && data.lesson) {

            lessonElement.innerText =
                data.lesson;

        } else {

            lessonElement.innerText =
                "No specific historical lesson found.";
        }


    } catch (error) {

        lessonElement.innerText =
            "Could not retrieve historical lesson.";

        console.error(error);
    }
}


// async function findHistoricalExperience() {

//     const query =
//         document.getElementById("projectProblem").value.trim();

//     const resultContainer =
//         document.getElementById("historicalExperience");


//     if (!query) {

//         resultContainer.innerHTML =
//             "<p class='empty-message'>Please describe the problem first.</p>";

//         return;
//     }


//     resultContainer.innerHTML =
//         "<p>Searching previous project experiences...</p>";


//     try {

//         const response = await fetch(
//             `${API_URL}/memory?query=${encodeURIComponent(query)}`
//         );


//         const data = await response.json();


//         resultContainer.innerHTML = "";


//         if (!response.ok ||
//             !data.memories ||
//             data.memories.length === 0) {

//             resultContainer.innerHTML = `
//                 <div class="memory-result">

//                     <div class="memory-type">
//                         NO HISTORICAL EXPERIENCE FOUND
//                     </div>

//                     <p>
//                         No similar experience was found
//                         in previous project history.
//                     </p>

//                 </div>
//             `;

//             return;
//         }


//         const memory = data.memories[0];


//         const card =
//             document.createElement("div");

//         card.className = "revive-card";


//         card.innerHTML = `

//             <span class="small-label">
//                 POTENTIAL HISTORICAL EXPERIENCE FOUND
//             </span>

//             <h2>
//                 ${memory.type || "Historical Experience"}
//             </h2>

//             <p>
//                 ${memory.text}
//             </p>

//             <p class="warning">
//                 ⚠ A similar situation was found in
//                 previous project memory.
//             </p>

//             <button
//                 class="secondary-btn"
//                 onclick="useHistoricalReference()">

//                 Use as Reference

//             </button>

//             <button
//                 class="text-btn"
//                 onclick="dismissHistoricalExperience()">

//                 Dismiss

//             </button>

//             <p id="project2Message"></p>

//         `;


//         resultContainer.appendChild(card);


//     } catch (error) {

//         resultContainer.innerHTML =
//             "<p>Could not connect to backend.</p>";

//         console.error(error);

//     }

// }


// ------------------------------------
// PROJECT 2 - USE AS REFERENCE
// ------------------------------------

function useHistoricalReference() {

    document.getElementById("project2Message").innerText =
        "✓ Historical experience added as guidance for Project 2. The team can now consider the previous solution and lesson before making its decision.";

}


// ------------------------------------
// PROJECT 2 - DISMISS
// ------------------------------------

function dismissHistoricalExperience() {

    document.getElementById("historicalExperience").innerHTML =
        "<p class='empty-message'>Historical experience dismissed.</p>";

}


// ------------------------------------
// OPEN CURRENT PROJECT
// ------------------------------------

function openCurrentProject() {

    const projectName =
        localStorage.getItem("currentProjectName");

    if (!projectName) {

        alert("No project has been created yet.");

        return;
    }

    loadCurrentProject();

    showSection("projectWorkspace");
}