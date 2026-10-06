from fastapi import (FastAPI, Depends, HTTPException)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import shutil
from fastapi import UploadFile, File

from database import get_db
from models import (Project, ProjectStage,Idea, Requirement, Architecture,Task,Bug,Experience,TestRecord, Deployment)
from schemas import (ProjectCreate, ProjectResponse, IdeaCreate, IdeaResponse, RequirementCreate, RequirementResponse,RequirementUpdate, ArchitectureCreate, ArchitectureResponse, TaskCreate, TaskResponse, BugCreate, BugResponse, ExperienceCreate, ExperienceResponse, TestRecordResponse, TestRecordCreate, CreateBugFromTestRequest, DeploymentCreate, DeploymentResponse)
from fastapi.staticfiles import StaticFiles

from hindsight_service import (
    get_experience_count,
    store_experience,
    search_memory,
    generate_hindsight,
    search_memory_async
)

app = FastAPI(
    title="ProjectHindsight API"
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
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
def get_hindsight(
    data: dict,
    db: Session = Depends(get_db)
):
    query = data["query"]
    project_id = data.get("project_id")
    current_stage = data.get("current_stage")

    context_parts = []

    if project_id:
        project = (
            db.query(Project)
            .filter(Project.id == int(project_id))
            .first()
        )

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )

        context_parts.append(
            f"Project Name: {project.name}"
        )
        context_parts.append(
            f"Domain: {project.domain or 'Not specified'}"
        )
        context_parts.append(
            f"Description: "
            f"{project.description or 'Not specified'}"
        )

    if current_stage:
        context_parts.append(
            f"Current Lifecycle Stage: {current_stage}"
        )

    if context_parts:
        context = "\n".join(context_parts)

        hindsight_query = f"""
You are helping a team learn from previous project experiences.

CURRENT PROJECT CONTEXT:
{context}

USER QUESTION:
{query}

Use the project context and current lifecycle stage to
interpret the question.

Search organizational memory for relevant historical
experiences, failures, decisions, solutions, and lessons.

Prioritize lessons useful for the current stage:
- IDEA: previously rejected ideas and feasibility lessons.
- REQUIREMENTS: requirement gaps and changing requirements.
- ARCHITECTURE: design decisions and integration risks.
- DEVELOPMENT: implementation issues and technical solutions.
- TESTING: test gaps, recurring bugs, and validation lessons.
- DEPLOYMENT: release failures and environment configuration.

Use relevant experiences from other projects where helpful.
Do not invent historical experiences or claim a past event
occurred unless it is supported by the available memory.

Provide clear, practical, structured insights.
"""

    else:
        # Preserve general organizational memory on Dashboard.
        hindsight_query = query

    result = generate_hindsight(hindsight_query)

    return {
        "hindsight": result
    }


@app.post("/projects", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    new_project = Project(
        name=project.name,
        description=project.description,
        domain=project.domain,
        team_size=project.team_size,
        technology=project.technology
    )

    db.add(new_project)
    db.flush()

    stages = [
        "IDEA",
        "REQUIREMENTS",
        "ARCHITECTURE",
        "DEVELOPMENT",
        "TESTING",
        "DEPLOYMENT",
        "HINDSIGHT"
    ]

    for stage_type in stages:
        stage = ProjectStage(
            project_id=new_project.id,
            stage_type=stage_type,
            status="NOT_STARTED",
            progress=0
        )

        db.add(stage)

    db.commit()
    db.refresh(new_project)

    return new_project

@app.get("/projects", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db)
):
    projects = db.query(Project).all()

    return projects

@app.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        return {
            "error": "Project not found"
        }

    return project

@app.get("/projects/{project_id}/stages")
def get_project_stages(
    project_id: int,
    db: Session = Depends(get_db)
):
    stages = (
        db.query(ProjectStage)
        .filter(ProjectStage.project_id == project_id)
        .order_by(ProjectStage.id)
        .all()
    )

    return stages

@app.get("/projects/{project_id}/ideas",
    response_model=list[IdeaResponse]
)
def get_project_ideas(
    project_id: int,
    db: Session = Depends(get_db)
):

    ideas = (
        db.query(Idea)
        .filter(Idea.project_id == project_id)
        .order_by(Idea.id)
        .all()
    )

    return ideas

@app.post("/projects/{project_id}/ideas",
    response_model=IdeaResponse
)
def create_project_idea(
    project_id: int,
    idea: IdeaCreate,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        return {
            "error": "Project not found"
        }

    new_idea = Idea(
        project_id=project_id,
        idea=idea.idea,
        description=idea.description,
        status=idea.status,
        rejection_reason=idea.rejection_reason
    )

    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)

    return new_idea

@app.get(
    "/projects/{project_id}/requirements",
    response_model=list[RequirementResponse]
)
def get_project_requirements(project_id: int, db: Session = Depends(get_db)):
    requirements = (
        db.query(Requirement)
        .filter(
            Requirement.project_id == project_id
        )
        .order_by(Requirement.id)
        .all()
    )

    return requirements

@app.post(
    "/projects/{project_id}/requirements",
    response_model=RequirementResponse
)
def create_project_requirement(
    project_id: int,
    requirement: RequirementCreate,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(
            Project.id == project_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if requirement.progress < 0 or requirement.progress > 100:
        raise HTTPException(
            status_code=400,
            detail="Progress must be between 0 and 100"
        )

    new_requirement = Requirement(
        project_id=project_id,
        title=requirement.title,
        description=requirement.description,
        status=requirement.status,
        priority=requirement.priority,
        progress=requirement.progress
    )

    db.add(new_requirement)
    db.commit()
    db.refresh(new_requirement)

    return new_requirement

@app.patch(
    "/requirements/{requirement_id}",
    response_model=RequirementResponse
)
def update_requirement(
    requirement_id: int,
    requirement: RequirementUpdate,
    db: Session = Depends(get_db)
):

    existing_requirement = (
        db.query(Requirement)
        .filter(
            Requirement.id == requirement_id
        )
        .first()
    )

    if not existing_requirement:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found"
        )

    if (
        requirement.progress is not None
        and (
            requirement.progress < 0
            or requirement.progress > 100
        )
    ):
        raise HTTPException(
            status_code=400,
            detail="Progress must be between 0 and 100"
        )

    update_data = requirement.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            existing_requirement,
            field,
            value
        )

    db.commit()
    db.refresh(existing_requirement)

    return existing_requirement

@app.get("/projects/{project_id}/architectures",response_model=list[ArchitectureResponse])
def get_project_architectures(
    project_id: int,
    db: Session = Depends(get_db)
):

    architectures = (
        db.query(Architecture)
        .filter(
            Architecture.project_id == project_id
        )
        .order_by(Architecture.id)
        .all()
    )

    return architectures

@app.post("/projects/{project_id}/architectures",response_model=ArchitectureResponse)
def create_project_architecture(
    project_id: int,
    architecture: ArchitectureCreate,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(
            Project.id == project_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_architecture = Architecture(
        project_id=project_id,
        title=architecture.title,
        description=architecture.description,
        technology_stack=architecture.technology_stack,
        diagram=architecture.diagram
    )

    db.add(new_architecture)
    db.commit()
    db.refresh(new_architecture)

    return new_architecture


@app.delete("/architectures/{architecture_id}")
def delete_architecture(
    architecture_id: int,
    db: Session = Depends(get_db)
):

    architecture = (
        db.query(Architecture)
        .filter(
            Architecture.id == architecture_id
        )
        .first()
    )

    if not architecture:
        raise HTTPException(
            status_code=404,
            detail="Architecture not found"
        )

    db.delete(architecture)
    db.commit()

    return {
        "success": True,
        "message": "Architecture deleted successfully"
    }

@app.put("/architectures/{architecture_id}",
    response_model=ArchitectureResponse
)
def update_architecture(
    architecture_id: int,
    architecture: ArchitectureCreate,
    db: Session = Depends(get_db)
):

    existing_architecture = (
        db.query(Architecture)
        .filter(
            Architecture.id == architecture_id
        )
        .first()
    )

    if not existing_architecture:
        raise HTTPException(
            status_code=404,
            detail="Architecture not found"
        )

    existing_architecture.title = architecture.title
    existing_architecture.description = architecture.description
    existing_architecture.technology_stack = architecture.technology_stack
    existing_architecture.diagram = architecture.diagram

    db.commit()
    db.refresh(existing_architecture)

    return existing_architecture

@app.post("/architectures/{architecture_id}/diagram-image",
    response_model=ArchitectureResponse)
def upload_architecture_image(
    architecture_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    architecture = (
        db.query(Architecture)
        .filter(
            Architecture.id == architecture_id
        )
        .first()
    )

    if not architecture:
        raise HTTPException(
            status_code=404,
            detail="Architecture not found"
        )

    allowed_types = {
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/webp"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PNG, JPG, JPEG and WEBP images are allowed"
        )

    upload_directory = "uploads/architecture"

    os.makedirs(
        upload_directory,
        exist_ok=True
    )

    extension = os.path.splitext(
        file.filename or ""
    )[1].lower()

    filename = (
        f"architecture_"
        f"{architecture_id}"
        f"{extension}"
    )

    file_path = os.path.join(
        upload_directory,
        filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    image_url = (
        f"/uploads/architecture/{filename}"
    )

    architecture.diagram_image_url = image_url

    db.commit()
    db.refresh(architecture)

    return architecture

@app.get("/projects/{project_id}/tasks",
    response_model=list[TaskResponse]
)
def get_project_tasks(
    project_id: int,
    db: Session = Depends(get_db)
):

    tasks = (
        db.query(Task)
        .filter(
            Task.project_id == project_id
        )
        .order_by(Task.id)
        .all()
    )

    return tasks

@app.post(
    "/projects/{project_id}/tasks",
    response_model=TaskResponse
)
def create_project_task(
    project_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(
            Project.id == project_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_task = Task(
        project_id=project_id,
        title=task.title,
        description=task.description,
        assigned_to=task.assigned_to,
        status=task.status,
        priority=task.priority
    )

    db.add(new_task)

    db.commit()

    db.refresh(new_task)

    return new_task

@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db)
):

    existing_task = (
        db.query(Task)
        .filter(
            Task.id == task_id
        )
        .first()
    )

    if not existing_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    existing_task.title = task.title

    existing_task.description = (
        task.description
    )

    existing_task.assigned_to = (
        task.assigned_to
    )

    existing_task.status = (
        task.status
    )

    existing_task.priority = (
        task.priority
    )

    db.commit()

    db.refresh(existing_task)

    return existing_task

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)

    db.commit()

    return {
        "message": "Task deleted successfully"
    }

@app.get(
    "/projects/{project_id}/bugs",
    response_model=list[BugResponse]
)
def get_project_bugs(
    project_id: int,
    db: Session = Depends(get_db)
):

    bugs = (
        db.query(Bug)
        .filter(
            Bug.project_id == project_id
        )
        .order_by(Bug.id.desc())
        .all()
    )

    return bugs

@app.post(
    "/projects/{project_id}/bugs",
    response_model=BugResponse
)
def create_project_bug(
    project_id: int,
    bug: BugCreate,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(
            Project.id == project_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_bug = Bug(
        project_id=project_id,
        stage_id=bug.stage_id,
        title=bug.title,
        description=bug.description,
        severity=bug.severity,
        status=bug.status,
        solution=bug.solution
    )

    db.add(new_bug)

    db.commit()

    db.refresh(new_bug)

    return new_bug

@app.put(
    "/bugs/{bug_id}",
    response_model=BugResponse
)
def update_bug(
    bug_id: int,
    bug: BugCreate,
    db: Session = Depends(get_db)
):

    existing_bug = (
        db.query(Bug)
        .filter(
            Bug.id == bug_id
        )
        .first()
    )

    if not existing_bug:
        raise HTTPException(
            status_code=404,
            detail="Bug not found"
        )

    previous_status = existing_bug.status

    existing_bug.title = bug.title
    existing_bug.description = bug.description
    existing_bug.severity = bug.severity
    existing_bug.status = bug.status
    existing_bug.solution = bug.solution
    existing_bug.stage_id = bug.stage_id

    db.commit()

    db.refresh(existing_bug)

    # -----------------------------------------
    # Send resolved bug to Hindsight
    # -----------------------------------------

    if (bug.status == "RESOLVED" and previous_status != "RESOLVED"):

        project = (
            db.query(Project)
            .filter(
                Project.id == existing_bug.project_id
            )
            .first()
        )

        if project:

            lesson = (
                f"Development issue resolved: "
                f"{existing_bug.title}. "
                f"Future projects should consider "
                f"the problem and solution recorded "
                f"for this issue."
            )

              # ----------------------------------------
            # 1. Create structured experience
            # ----------------------------------------

            new_experience = Experience(
                project_id=existing_bug.project_id,
                stage_id=existing_bug.stage_id,
                type="BUG",
                title=existing_bug.title,
                description=existing_bug.description,
                solution=existing_bug.solution,
                outcome=(
                    "Issue resolved successfully."
                ),
                lesson=lesson,
                source="DEVELOPMENT"
            )

            db.add(new_experience)
            db.commit()
            db.refresh(new_experience)

            store_experience(
                project_name=project.name,
                experience_type="BUG",
                title=existing_bug.title,
                description=existing_bug.description or "",
                solution=existing_bug.solution or "",
                lesson=lesson
            )
    return existing_bug

@app.delete(
    "/bugs/{bug_id}"
)
def delete_bug(
    bug_id: int,
    db: Session = Depends(get_db)
):

    existing_bug = (
        db.query(Bug)
        .filter(
            Bug.id == bug_id
        )
        .first()
    )

    if not existing_bug:
        raise HTTPException(
            status_code=404,
            detail="Bug not found"
        )

    db.delete(existing_bug)

    db.commit()

    return {
        "success": True,
        "message": "Bug deleted successfully"
    }

@app.get(
    "/projects/{project_id}/experiences",
    response_model=list[ExperienceResponse]
)
def get_project_experiences(
    project_id: int,
    db: Session = Depends(get_db)
):
    experiences = (
        db.query(Experience)
        .filter(
            Experience.project_id == project_id
        )
        .order_by(Experience.id.desc())
        .all()
    )

    return experiences

@app.post(
    "/projects/{project_id}/experiences",
    response_model=ExperienceResponse
)
def create_project_experience(
    project_id: int,
    experience: ExperienceCreate,
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_experience = Experience(
        project_id=project_id,
        stage_id=experience.stage_id,
        type=experience.type,
        title=experience.title,
        description=experience.description,
        solution=experience.solution,
        outcome=experience.outcome,
        lesson=experience.lesson,
        source=experience.source
    )

    db.add(new_experience)
    db.commit()
    db.refresh(new_experience)

    return new_experience

@app.get(
    "/projects/{project_id}/tests",
    response_model=list[TestRecordResponse]
)
def get_project_tests(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    tests = (
        db.query(TestRecord)
        .filter(TestRecord.project_id == project_id)
        .order_by(TestRecord.id.desc())
        .all()
    )

    return tests

@app.post(
    "/projects/{project_id}/tests",
    response_model=TestRecordResponse
)
def create_project_test(
    project_id: int,
    test: TestRecordCreate,
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_test = TestRecord(
        project_id=project_id,
        test_type=test.test_type,
        test_name=test.test_name,
        status=test.status,
        result=test.result,
        bug_id=test.bug_id
    )

    db.add(new_test)
    db.commit()
    db.refresh(new_test)

    return new_test

@app.put(
    "/tests/{test_id}",
    response_model=TestRecordResponse
)
def update_test(
    test_id: int,
    test: TestRecordCreate,
    db: Session = Depends(get_db)
):
    existing_test = (
        db.query(TestRecord)
        .filter(TestRecord.id == test_id)
        .first()
    )

    if not existing_test:
        raise HTTPException(
            status_code=404,
            detail="Test record not found"
        )

    existing_test.test_type = test.test_type
    existing_test.test_name = test.test_name
    existing_test.status = test.status
    existing_test.result = test.result
    existing_test.bug_id = test.bug_id

    db.commit()
    db.refresh(existing_test)

    return existing_test

@app.delete("/tests/{test_id}")
def delete_test(
    test_id: int,
    db: Session = Depends(get_db)
):
    existing_test = (
        db.query(TestRecord)
        .filter(TestRecord.id == test_id)
        .first()
    )

    if not existing_test:
        raise HTTPException(
            status_code=404,
            detail="Test record not found"
        )

    db.delete(existing_test)
    db.commit()

    return {
        "success": True,
        "message": "Test record deleted successfully"
    }

@app.post(
    "/tests/{test_id}/create-bug",
    response_model=BugResponse
)
def create_bug_from_test(
    test_id: int,
    data: CreateBugFromTestRequest,
    db: Session = Depends(get_db)
):
    test = (
        db.query(TestRecord)
        .filter(TestRecord.id == test_id)
        .first()
    )

    if not test:
        raise HTTPException(
            status_code=404,
            detail="Test record not found"
        )

    if test.status != "FAILED":
        raise HTTPException(
            status_code=400,
            detail="Only failed tests can be converted into issues"
        )

    if test.bug_id:
        existing_bug = (
            db.query(Bug)
            .filter(Bug.id == test.bug_id)
            .first()
        )

        if existing_bug:
            return existing_bug

    new_bug = Bug(
        project_id=test.project_id,
        stage_id=None,
        title=f"Test failure: {test.test_name}",
        description=test.result,
        severity=data.severity,
        status="OPEN",
        solution=None
    )

    db.add(new_bug)
    db.flush()

    test.bug_id = new_bug.id

    db.commit()
    db.refresh(new_bug)

    return new_bug

@app.get("/projects/{project_id}/testing-insights")
async def get_testing_insights(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    query = (
        f"Testing lessons and historical experiences "
        f"related to project {project.name}. "
        f"Find previous bugs, testing failures, "
        f"test issues, database problems, integration "
        f"failures, and lessons that could help during "
        f"the testing stage."
    )

    memories = await search_memory_async(query)

    return {
        "project_id": project_id,
        "insights": memories
    }

@app.get(
    "/projects/{project_id}/deployments",
    response_model=list[DeploymentResponse]
)
def get_project_deployments(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    deployments = (
        db.query(Deployment)
        .filter(
            Deployment.project_id == project_id
        )
        .order_by(Deployment.id.desc())
        .all()
    )

    return deployments

@app.post(
    "/projects/{project_id}/deployments",
    response_model=DeploymentResponse
)
def create_project_deployment(
    project_id: int,
    deployment: DeploymentCreate,
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_deployment = Deployment(
        project_id=project_id,
        environment=deployment.environment,
        status=deployment.status,
        version=deployment.version,
        deployment_notes=deployment.deployment_notes
    )

    db.add(new_deployment)
    db.commit()
    db.refresh(new_deployment)

    return new_deployment

@app.put(
    "/deployments/{deployment_id}",
    response_model=DeploymentResponse
)
@app.put(
    "/deployments/{deployment_id}",
    response_model=DeploymentResponse
)
def update_deployment(
    deployment_id: int,
    deployment: DeploymentCreate,
    db: Session = Depends(get_db)
):
    existing_deployment = (
        db.query(Deployment)
        .filter(
            Deployment.id == deployment_id
        )
        .first()
    )

    if not existing_deployment:
        raise HTTPException(
            status_code=404,
            detail="Deployment not found"
        )

    previous_status = existing_deployment.status

    existing_deployment.environment = (
        deployment.environment
    )

    existing_deployment.status = (
        deployment.status
    )

    existing_deployment.version = (
        deployment.version
    )

    existing_deployment.deployment_notes = (
        deployment.deployment_notes
    )

    db.commit()
    db.refresh(existing_deployment)

    # Capture failed deployment as project experience
    if (
        deployment.status == "FAILED"
        and previous_status != "FAILED"
    ):
        project = (
            db.query(Project)
            .filter(
                Project.id ==
                existing_deployment.project_id
            )
            .first()
        )

        if project:

            lesson = (
                f"Deployment failed in the "
                f"{existing_deployment.environment} "
                f"environment for version "
                f"{existing_deployment.version or 'unknown'}. "
                f"Future projects should review the "
                f"deployment notes and environment "
                f"configuration before deployment."
            )

            new_experience = Experience(
                project_id=existing_deployment.project_id,
                stage_id=None,
                type="DEPLOYMENT",
                title=(
                    f"Deployment failure - "
                    f"{existing_deployment.environment}"
                ),
                description=(
                    existing_deployment.deployment_notes
                    or ""
                ),
                solution=None,
                outcome="Deployment failed.",
                lesson=lesson,
                source="DEPLOYMENT"
            )

            db.add(new_experience)
            db.commit()
            db.refresh(new_experience)

            store_experience(
                project_name=project.name,
                experience_type="DEPLOYMENT",
                title=(
                    f"Deployment failure - "
                    f"{existing_deployment.environment}"
                ),
                description=(
                    existing_deployment.deployment_notes
                    or ""
                ),
                solution="",
                lesson=lesson
            )

    return existing_deployment


@app.delete("/deployments/{deployment_id}")
def delete_deployment(
    deployment_id: int,
    db: Session = Depends(get_db)
):
    existing_deployment = (
        db.query(Deployment)
        .filter(
            Deployment.id == deployment_id
        )
        .first()
    )

    if not existing_deployment:
        raise HTTPException(
            status_code=404,
            detail="Deployment not found"
        )

    db.delete(existing_deployment)
    db.commit()

    return {
        "success": True,
        "message": "Deployment deleted successfully"
    }

@app.get("/projects/{project_id}/deployment-insights")
async def get_deployment_insights(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    query = (
        f"Deployment lessons and historical experiences "
        f"related to project {project.name}. "
        f"Find previous deployment failures, "
        f"environment configuration problems, "
        f"release issues, deployment solutions, "
        f"and lessons that could help during deployment."
    )

    memories = await search_memory_async(query)

    return {
        "project_id": project_id,
        "insights": memories
    }
