from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    role = Column(String(50), nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Project(Base):

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), nullable=False)

    description = Column(Text)

    domain = Column(String(100))

    team_size = Column(
        Integer,
        nullable=True
    )

    technology = Column(
        String(255),
        nullable=True
    )

    status = Column(String(50), default="ACTIVE")

    current_stage = Column(
        String(50),
        default="IDEA"
    )

    progress = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class ProjectMember(Base):

    __tablename__ = "project_members"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    role = Column(
        String(50),
        nullable=False
    )

    joined_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class ProjectStage(Base):

    __tablename__ = "project_stages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    stage_type = Column(
        String(50),
        nullable=False
    )

    status = Column(
        String(50),
        default="NOT_STARTED"
    )

    progress = Column(
        Integer,
        default=0
    )

    started_at = Column(DateTime)

    completed_at = Column(DateTime)

class Idea(Base):

    __tablename__ = "ideas"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    idea = Column(
        Text,
        nullable=False
    )

    description = Column(
        Text
    )

    status = Column(
        String(50),
        default="PROPOSED"
    )

    rejection_reason = Column(
        Text
    )

class Requirement(Base):

    __tablename__ = "requirements"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text
    )

    status = Column(
        String(50),
        default="TODO"
    )

    priority = Column(
        String(30),
        default="MEDIUM"
    )

    progress = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

class Architecture(Base):

    __tablename__ = "architectures"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text
    )

    technology_stack = Column(
        Text
    )

    diagram = Column(
        Text
    )

    diagram_image_url = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class Task(Base):

    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text
    )

    assigned_to = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    status = Column(
        String(50),
        default="TODO"
    )

    priority = Column(
        String(50),
        default="MEDIUM"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class Bug(Base):

    __tablename__ = "bugs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    stage_id = Column(
        Integer,
        ForeignKey("project_stages.id"),
        nullable=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text
    )

    severity = Column(
        String(50),
        default="MEDIUM"
    )

    status = Column(
        String(50),
        default="OPEN"
    )

    solution = Column(
        Text
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class Experience(Base):

    __tablename__ = "experiences"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    stage_id = Column(
        Integer,
        ForeignKey("project_stages.id"),
        nullable=True
    )

    type = Column(
        String(100),
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text
    )

    solution = Column(
        Text
    )

    outcome = Column(
        Text
    )

    lesson = Column(
        Text
    )

    source = Column(
        String(100)
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class TestRecord(Base):
    __tablename__ = "test_records"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer,ForeignKey("projects.id"),nullable=False)
    test_type = Column(String(100), nullable=False)
    test_name = Column(String(200), nullable=False)
    status = Column(String(50), default="PENDING")
    result = Column(Text)
    bug_id = Column(Integer,ForeignKey("bugs.id"),nullable=True)

class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )
    environment = Column(String(100), nullable=False)
    status = Column(String(50), default="PENDING")
    version = Column(String(100), nullable=True)
    deployment_notes = Column(Text, nullable=True)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
