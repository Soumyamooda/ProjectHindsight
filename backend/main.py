from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hindsight_service import (
    get_experience_count,
    store_experience,
    search_memory,
    generate_hindsight
)

app = FastAPI(
    title="ProjectHindsight API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "message": "ProjectHindsight API is running"
    }


@app.post("/experiences")
def add_experience(data: dict):

    return store_experience(
        project_name=data["project_name"],
        experience_type=data["experience_type"],
        title=data["title"],
        description=data["description"],
        solution=data["solution"],
        lesson=data["lesson"]
    )


@app.get("/memory")
def get_memory(query: str):

    memories = search_memory(query)

    return {
        "memories": memories
    }

@app.post("/historical-lesson")
def get_historical_lesson(data: dict):

    result = generate_hindsight(
        f"""
        A new project is facing this problem:

        {data["query"]}

        Look at previous project experiences in memory.

        Identify the most relevant historical experience
        and explain the lesson that should be applied
        to the current project.

        Give only the practical historical lesson.
        Keep it concise.
        """
    )

    return {
        "lesson": result
    }


@app.post("/revive-idea")
def revive_idea(data: dict):

    result = generate_hindsight(
        f"""
        A new project is considering this idea:

        {data["idea"]}

        Search previous project experiences in memory.

        Find whether this idea, technology, approach, or decision
        was previously rejected or not selected.

        If a previous rejection exists, explain:

        1. What was rejected?
        2. Why was it rejected?
        3. What project made that decision?
        4. What should the current project reconsider?

        If no relevant historical rejection exists, say:
        No previous rejected decision was found.

        Keep the response concise and practical.
        """
    )

    return {
        "result": result
    }


@app.get("/experience-count")
def experience_count():

    count = get_experience_count()

    return {
        "count": count
    }

@app.post("/hindsight")
def get_hindsight(data: dict):

    result = generate_hindsight(
        data["query"]
    )

    return {
        "hindsight": result
    }