# ProjectHindsight — Project Experience Memory

> **ProjectHindsight** is an AI-powered project experience memory system that helps teams learn from previous projects instead of repeating the same mistakes.

It captures important experiences from a project's lifecycle—decisions, rejected ideas, technical problems, solutions, failures, testing gaps, deployment issues, and lessons learned—and makes that knowledge available to future projects.

The system uses **Hindsight Cloud** as its long-term project memory and a **FastAPI** backend to connect the frontend with that memory.

---

## 1. Problem Statement

Project knowledge is often lost after a project is completed.

Important information such as:

- Why a technology was rejected
- What assumptions turned out to be wrong
- Which API integration caused problems
- What deployment configuration was missed
- Which testing scenarios were overlooked
- What technical decisions worked or failed
- What lessons the team learned

may remain scattered across meetings, documents, chats, tickets, or individual knowledge.

When a new project faces a similar situation, teams may unknowingly repeat the same mistakes.

### ProjectHindsight solves this by creating a reusable memory of project experiences.

Instead of asking only:

> "What should we do?"

ProjectHindsight also asks:

> "Have we faced something similar before, and what did we learn from it?"

---

## 2. Core Idea

ProjectHindsight treats previous project experiences as organizational memory.

### Example

### Project 1 — Emergency Response System

A routing API returned distance in **meters**, while the application expected **kilometers**.

The team identified the problem and learned:

> Validate external API response units before processing.

### Project 2 — Smart Emergency Platform

A similar routing problem occurs.

ProjectHindsight can retrieve the previous project experience and provide the historical lesson.

This allows the new project to use previous experience as a reference instead of rediscovering the same problem.

---

## 3. Key Features

### 3.1 Project Experience Memory

Teams can store experiences from their projects with information such as:

- Project name
- Experience type
- Title
- What happened
- Solution / decision
- Lesson for future projects

These experiences are stored in Hindsight Cloud.

---

### 3.2 Long-Term AI Memory with Hindsight

ProjectHindsight uses **Hindsight Cloud** to retain and retrieve project knowledge.

The system uses:

- `retain()` — stores project experiences
- `recall()` — retrieves relevant historical memories
- `reflect()` — generates a practical lesson from previous experiences

This allows the system to go beyond simple keyword matching.

---

### 3.3 Cross-Project Memory

Project memories are not isolated.

A new project can retrieve relevant experiences from previous projects.

For example:

```text
Project 1
Emergency Response System
        |
        | stored experience
        v
Hindsight Memory
        |
        | recall
        v
Project 2
Smart Emergency Platform
```

This is the core idea behind ProjectHindsight.

---

### 3.4 "Have We Faced This Before?"

A new project can describe a problem it is currently facing.

Example:

```text
Our routing API is returning distance in meters,
but our application expects kilometers.
```

ProjectHindsight searches previous project memory and identifies whether a similar experience exists.

If relevant history is found, the UI presents:

- Historical project
- What happened
- Historical lesson
- Option to use the experience as a reference
- Option to dismiss it

---

### 3.5 Dynamic Historical Lessons

The historical lesson is not hard-coded into the frontend.

The backend sends the current problem to Hindsight and uses `reflect()` to generate a concise practical lesson based on previous project memory.

Example:

```text
Validate external API response units before processing.
```

This makes the historical lesson dynamic and dependent on stored project experience.

---

### 3.6 Project Creation

Users can create a new project by providing:

- Project name
- Project description

The current project information is stored in browser `localStorage` for the prototype.

The created project becomes the active project workspace.

---

### 3.7 Project Workspace

The project workspace displays:

- Current project name
- Current project description
- Current project problem
- Historical experience search

Users can describe a problem and ask:

> Have We Faced This Before?

---

### 3.8 Hindsight / Project Memory View

The application provides a memory-oriented interface where users can ask questions about previous project experiences.

The backend sends the query to Hindsight and retrieves relevant project memory.

---

### 3.9 Experience Counter

ProjectHindsight maintains a simple experience count for the prototype.

Each successfully stored project experience increases the count.

The count is exposed through:

```text
GET /experience-count
```

---

### 3.10 Revive an Old Idea

ProjectHindsight is designed to help teams reconsider previously rejected ideas.

The concept is:

```text
Old Idea
   ↓
Why was it rejected?
   ↓
Does that reason still apply?
   ↓
Current project context
   ↓
Revive / Keep rejected / Not sure
```

For example, an API or technology may have been rejected in an earlier project because of cost.

A future project may have:

- A different budget
- A different scale
- Different requirements
- New pricing
- New technology capabilities

ProjectHindsight can therefore help teams revisit old decisions rather than permanently treating them as invalid.

---

## 4. Example Project Experiences

The prototype was populated with experiences from the:

### Emergency Response System

Examples include:

- External API returning distance in meters instead of the expected kilometers
- Deployment configuration problems caused by a missing environment variable
- Role-specific access control challenges
- Other development and project lifecycle experiences

These experiences form the historical memory that can be reused by future projects.

---

## 5. System Architecture

Current deployed architecture:

```text
                         ┌──────────────────────┐
                         │       User / Judge   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Frontend           │
                         │ HTML / CSS / JS      │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP API
                                    ▼
                         ┌──────────────────────┐
                         │   Render             │
                         │   FastAPI Backend     │
                         └──────────┬───────────┘
                                    │
                                    │ retain / recall / reflect
                                    ▼
                         ┌──────────────────────┐
                         │   Hindsight Cloud     │
                         │   Project Memory      │
                         └──────────────────────┘
```

### Current Backend Deployment

The FastAPI backend is deployed on:

```text
https://projecthindsight.onrender.com
```

The frontend is configured to use this deployed backend.

---

## 6. Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Browser Local Storage

### Backend

- Python
- FastAPI
- Uvicorn

### AI / Memory

- Hindsight Cloud
- Hindsight Python Client
- `retain()`
- `recall()`
- `reflect()`

### Deployment

- GitHub
- Render

---

## 7. Project Structure

```text
ProjectHindsight/
│
├── backend/
│   ├── .env
│   ├── .gitignore
│   ├── requirements.txt
│   ├── main.py
│   ├── hindsight_service.py
│   ├── test_hindsight.py
│   └── experience_count.json
│
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js
```

### Backend files

#### `main.py`

FastAPI application containing the API routes.

#### `hindsight_service.py`

Contains the Hindsight integration:

- Store experiences
- Recall memories
- Generate historical lessons
- Maintain experience count

#### `test_hindsight.py`

Used for testing the Hindsight integration.

#### `experience_count.json`

Stores the prototype's local experience counter.

#### `.env`

Contains sensitive configuration such as the Hindsight API key.

**This file must never be committed to GitHub.**

---

## 8. API Endpoints

### Health Check

```http
GET /
```

Response:

```json
{
  "message": "ProjectHindsight API is running"
}
```

---

### Store Experience

```http
POST /experiences
```

Example request:

```json
{
  "project_name": "Emergency Response System",
  "experience_type": "Technical Issue",
  "title": "API distance unit mismatch",
  "description": "The routing API returned distance in meters instead of kilometers.",
  "solution": "Converted the API response to the expected unit before processing.",
  "lesson": "Validate external API response units before processing."
}
```

---

### Search Project Memory

```http
GET /memory?query=<query>
```

Example:

```text
GET /memory?query=routing API distance
```

The endpoint uses Hindsight `recall()` to retrieve relevant memories.

---

### Generate Historical Lesson

```http
POST /historical-lesson
```

Example request:

```json
{
  "query": "Our routing API is returning distance in meters, but our application expects kilometers."
}
```

The backend asks Hindsight to identify the relevant historical experience and generate a concise practical lesson.

---

### Generate Hindsight

```http
POST /hindsight
```

Example request:

```json
{
  "query": "What deployment problems did previous projects experience?"
}
```

The endpoint uses Hindsight `reflect()` to generate a response from project memory.

---

### Experience Count

```http
GET /experience-count
```

Example response:

```json
{
  "count": 6
}
```

---

## 9. How the Main Historical Recall Flow Works

```text
User describes current problem
            ↓
"Have We Faced This Before?"
            ↓
Frontend sends query to FastAPI
            ↓
FastAPI calls Hindsight recall()
            ↓
Relevant historical memories retrieved
            ↓
Historical experience displayed
            ↓
FastAPI calls Hindsight reflect()
            ↓
Dynamic historical lesson generated
            ↓
Lesson shown to the user
```

---

## 10. Example End-to-End Scenario

### Step 1 — Previous Project

Emergency Response System encounters:

```text
Routing API returned distance in meters.
```

The team records:

```text
Lesson:
Validate external API response units before processing.
```

The experience is stored in Hindsight.

### Step 2 — New Project

A new project called:

```text
Smart Emergency Platform
```

is created.

### Step 3 — New Problem

The team enters:

```text
Our routing API is returning distance in meters,
but our application expects kilometers.
```

### Step 4 — Historical Search

ProjectHindsight searches the shared project memory.

It finds the Emergency Response System experience.

### Step 5 — Historical Lesson

Hindsight generates a practical lesson based on the previous experience.

The user can then use that historical information as a reference for the current project.

---

## 11. Local Setup

### Prerequisites

Install:

- Python 3
- Git
- A Hindsight Cloud account/API key

---

### Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ProjectHindsight
```

---

### Backend Setup

Move into the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```cmd
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### Environment Variables

Create:

```text
backend/.env
```

Add:

```env
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
HINDSIGHT_API_KEY=YOUR_HINDSIGHT_API_KEY
```

Never commit `.env`.

---

### Start the Backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

---

## 12. Frontend Setup

The frontend is a static HTML/CSS/JavaScript application.

The API URL in `frontend/app.js` should point to the backend.

For the current deployed version:

```javascript
const API_URL = "https://projecthindsight.onrender.com";
```

For local development, it can be changed to:

```javascript
const API_URL = "http://127.0.0.1:8000";
```

---

## 13. Security

Sensitive information is kept outside the source code.

The backend uses environment variables:

```env
HINDSIGHT_BASE_URL=...
HINDSIGHT_API_KEY=...
```

The `.gitignore` contains:

```text
venv/
.env
__pycache__/
```

The Hindsight API key should never be committed to the GitHub repository or exposed in frontend JavaScript.

---

## 14. Deployment

### GitHub

The source code is maintained in a GitHub repository.

### Render

The FastAPI backend is deployed on Render.

Current backend URL:

```text
https://projecthindsight.onrender.com
```

Render configuration:

```text
Root Directory: backend
Runtime: Python
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Required Render environment variables:

```text
HINDSIGHT_BASE_URL
HINDSIGHT_API_KEY
```

---

## 15. Current Prototype Limitations

This is a hackathon/prototype implementation.

### Project metadata

The current project name and description are stored in browser `localStorage`.

Therefore, project metadata is currently browser-specific.

### Experience count

The experience counter uses a local JSON file:

```text
experience_count.json
```

This is suitable for the prototype but is not a production-grade persistent counter.

### Authentication

There is currently no user authentication or role-based account system.

### Multi-user collaboration

The current prototype does not provide separate accounts or isolated project memories per user/team.

### Frontend deployment

The backend is currently deployed on Render. A static frontend deployment can be added separately.

---

## 16. Future Enhancements

Potential future improvements include:

- AI agent-based project memory workflows
- Better project lifecycle categorization
- Automatic extraction of lessons from project documents
- More intelligent "Revive Old Idea" reasoning
- Project-specific and organization-wide memory scopes
- User authentication
- Team collaboration
- Persistent project metadata database
- Production-grade experience counters
- Automated project retrospectives
- Integration with GitHub, Jira, Slack, and project management tools
- Deployment and production incident ingestion
- AI-generated project risk warnings
- Automatic "Don't Repeat This" recommendations

---

## 17. Why ProjectHindsight Is Different

Traditional project management systems primarily answer:

```text
What is the current status?
What is the task?
Who is assigned?
When is the deadline?
```

ProjectHindsight focuses on another question:

```text
What did we learn from previous projects,
and can that knowledge help us now?
```

The goal is to turn project history into reusable engineering knowledge.

---

## 18. Project Lifecycle Memory

ProjectHindsight is designed to remember experiences across the complete project lifecycle:

```text
Idea
  ↓
Assumptions
  ↓
Stakeholder Decisions
  ↓
Estimates
  ↓
Architecture
  ↓
Development
  ↓
Testing
  ↓
Deployment
  ↓
Production Incidents
  ↓
Retrospective
  ↓
Reusable Project Memory
```

That memory can then influence future project decisions through historical references.

---


