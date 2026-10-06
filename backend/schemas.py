from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    domain: str | None = None
    team_size: int | None = None
    technology: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    domain: str | None
    team_size: int | None
    technology: str | None
    current_stage: str
    progress: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class IdeaCreate(BaseModel):

    idea: str
    description: str | None = None
    status: str = "PROPOSED"
    rejection_reason: str | None = None

class IdeaResponse(BaseModel):

    id: int
    project_id: int
    idea: str
    description: str | None
    status: str
    rejection_reason: str | None
    model_config = ConfigDict(
        from_attributes=True
    )

class RequirementCreate(BaseModel):

    title: str
    description: str | None = None
    status: str = "TODO"
    priority: str = "MEDIUM"
    progress: int = 0

class RequirementUpdate(BaseModel):

    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    progress: int | None = None

class RequirementResponse(BaseModel):

    id: int
    project_id: int
    title: str
    description: str | None
    status: str
    priority: str
    progress: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )

class ArchitectureCreate(BaseModel):
    title: str
    description: str | None = None
    technology_stack: str | None = None
    diagram: str | None = None


class ArchitectureResponse(BaseModel):

    id: int
    project_id: int
    title: str
    description: str | None
    technology_stack: str | None
    diagram: str | None
    diagram_image_url: str | None
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    assigned_to: int | None = None
    status: str = "TODO"
    priority: str = "MEDIUM"


class TaskResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: str | None
    assigned_to: int | None
    status: str
    priority: str
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )

class BugCreate(BaseModel):

    title: str

    description: str | None = None

    severity: str = "MEDIUM"

    status: str = "OPEN"

    solution: str | None = None

    stage_id: int | None = None


class BugResponse(BaseModel):

    id: int
    project_id: int
    stage_id: int | None
    title: str
    description: str | None
    severity: str
    status: str
    solution: str | None
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )

class ExperienceCreate(BaseModel):

    type: str
    title: str
    description: str | None = None
    solution: str | None = None
    outcome: str | None = None
    lesson: str | None = None
    source: str | None = None
    stage_id: int | None = None


class ExperienceResponse(BaseModel):

    id: int
    project_id: int
    stage_id: int | None
    type: str
    title: str
    description: str | None
    solution: str | None
    outcome: str | None
    lesson: str | None
    source: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class TestRecordCreate(BaseModel):
    test_type: str
    test_name: str
    status: str = "PENDING"
    result: str | None = None
    bug_id: int | None = None


class TestRecordResponse(BaseModel):
    id: int
    project_id: int
    test_type: str
    test_name: str
    status: str
    result: str | None
    bug_id: int | None
    model_config = ConfigDict(from_attributes=True)

class CreateBugFromTestRequest(BaseModel):
    severity: str = "MEDIUM"

class DeploymentCreate(BaseModel):
    environment: str
    status: str = "PENDING"
    version: str | None = None
    deployment_notes: str | None = None


class DeploymentResponse(BaseModel):
    id: int
    project_id: int
    environment: str
    status: str
    version: str | None
    deployment_notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
