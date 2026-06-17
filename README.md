# CompliancePilot AI
### Autonomous Compliance Intelligence Workforce for Malaysian Enterprises

> **NexHack 2026 Submission**  
> Track 1: Agentic AI for Internal Enterprise Operations

---

## Overview

CompliancePilot AI is an AI-powered compliance review platform that helps organizations automatically analyze contracts, HR policies, compliance documents, and internal procedures against Malaysian regulations.

The platform acts as a digital compliance officer that continuously reviews documents, identifies risks, explains violations, and generates remediation recommendations.

Instead of relying on expensive legal consultations and manual audits, organizations can upload documents and receive AI-generated compliance assessments within minutes.

---

# NexHack 2026 Alignment

## Track

**Track 1: Agentic AI for Internal Enterprise Operations**

## Theme

**Building Autonomous AI Workforce & Trusted Enterprise Ecosystems**

---

# Problem Statement

Organizations face increasing regulatory obligations under:

- Employment Act 1955
- Personal Data Protection Act (PDPA) 2010
- Occupational Safety & Health requirements
- Internal governance policies
- Industry-specific compliance frameworks

Manual compliance reviews are:

- Expensive
- Slow
- Error-prone
- Difficult to scale

Small and medium-sized businesses often lack dedicated legal and compliance teams, resulting in:

- Regulatory violations
- Financial penalties
- Audit failures
- Legal disputes

---

# Solution

CompliancePilot AI provides an AI-powered compliance workforce capable of:

- Automatically reviewing contracts
- Identifying compliance violations
- Performing risk assessments
- Cross-referencing Malaysian regulations
- Generating audit-ready reports
- Providing remediation recommendations

---

# Key Features

## AI Compliance Analysis

Upload:

- Employment contracts
- HR policies
- Internal procedures
- Compliance documents

The system automatically:

- Extracts text
- Reviews clauses
- Identifies violations
- Calculates risk scores
- Produces compliance findings

---

## Multi-Agent Compliance Workforce

CompliancePilot AI utilizes CrewAI-based autonomous agents.

### Agent 1 — Legal Compliance Analyst

**Responsibilities**

- Reviews document clauses
- Detects regulatory conflicts
- Identifies legal concerns

**Output**

- Compliance findings
- Regulation references
- Clause explanations

---

### Agent 2 — Risk Assessment Specialist

**Responsibilities**

- Evaluates severity
- Scores overall risk

**Output**

- Risk Score (0–100)
- Risk Category
  - Low
  - Medium
  - High
  - Critical

---

### Agent 3 — Policy Recommendation Advisor

**Responsibilities**

- Suggests remediation actions
- Generates recommendations

**Output**

- Corrective actions
- Policy improvements
- Risk mitigation steps

---

## Regulation Knowledge Base (RAG)

Powered by:

- LangChain
- ChromaDB
- Semantic Search

Capabilities:

- Regulation retrieval
- Clause matching
- Compliance justification
- Explainable AI outputs

---

## OCR Document Processing

Supported formats:

- PDF
- DOCX
- TXT
- Images

Powered by:

- Tesseract OCR
- PyMuPDF

Features:

- Text extraction
- Scanned document support
- OCR fallback processing

---

## Risk Intelligence Dashboard

Provides:

- Compliance statistics
- Risk distribution
- Analysis history
- Compliance trends

---

## PDF Audit Reports

Automatically generates:

- Executive summary
- Findings
- Risk scores
- Recommendations
- Compliance gaps

Ready for:

- Auditors
- HR teams
- Compliance departments
- Management reviews

---

# Why CompliancePilot AI Matters

## Real Business Pain Point

Compliance reviews consume significant time and resources.

Organizations often:

- Review contracts manually
- Depend on external consultants
- Miss critical violations

CompliancePilot AI reduces review time from hours to minutes.

---

## Business Impact

| Metric | Traditional Process | CompliancePilot AI |
|----------|----------|----------|
| Review Time | 2–6 Hours | < 5 Minutes |
| Initial Screening Cost | High | Low |
| Scalability | Limited | High |
| Audit Readiness | Manual | Automated |
| Risk Visibility | Reactive | Proactive |

---

# System Architecture

```text
┌─────────────────────────────┐
│        Next.js Frontend     │
│    React + TypeScript UI    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        FastAPI Backend      │
│ Authentication & API Layer  │
└──────────────┬──────────────┘
               │
     ┌─────────┼─────────┐
     ▼         ▼         ▼

 PostgreSQL  ChromaDB   CrewAI
 Database       RAG    AI Agents

                         │
                         ▼

             Compliance Analysis Engine

                         │
                         ▼

                PDF Report Generator
```

---

# Technical Architecture

## Frontend

### Technologies

- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- Shadcn UI
- Recharts
- Framer Motion

### Features

- User authentication
- Document upload
- Dashboard analytics
- Report downloads

---

## Backend

### Technologies

- FastAPI
- Python 3.11
- SQLAlchemy
- PostgreSQL

### Features

- Authentication
- Role-based authorization
- AI orchestration
- Document processing
- Report generation

---

## AI Layer

### CrewAI

Multi-agent orchestration:

1. Compliance Analyst
2. Risk Assessor
3. Recommendation Advisor

### LangChain

Used for:

- Prompt management
- Knowledge retrieval
- Agent workflows

### ChromaDB

Used for:

- Regulation indexing
- Semantic search
- Retrieval-Augmented Generation (RAG)

### OpenAI

Provides:

- Advanced legal reasoning
- Compliance explanation
- Contextual recommendations

Fallback:

- Rule-based compliance engine

---

# Security Architecture

## Authentication

- JWT Access Tokens

## Authorization

- Admin
- Compliance Officer
- Auditor

## Data Protection

- Role-based access control
- Secure API endpoints
- Audit-ready workflows

---

# User Roles

## Admin

- Full system access
- User management
- Dashboard management
- Demo data seeding

## Compliance Officer

- Upload documents
- Run analyses
- Generate reports

## Auditor

- View analyses
- Download reports
- Review compliance history

---

# Target Customers

## SMEs in Malaysia

Challenges:

- No internal legal department
- Limited compliance expertise

## HR Departments

Use Cases:

- Employment contract reviews
- Internal policy validation

## Compliance Teams

Use Cases:

- Regulatory monitoring
- Audit preparation

## Consulting Firms

Use Cases:

- Client compliance screening
- Faster audit workflows

---

# Business Model

## Starter Plan

RM49/month

- 50 document analyses
- Basic reporting

## Professional Plan

RM199/month

- Unlimited analyses
- PDF reporting
- Team collaboration

## Enterprise Plan

Custom Pricing

- Dedicated deployment
- API integration
- Compliance monitoring
- Priority support

---

# Innovation & Differentiation

Most compliance tools provide:

- Static checklists
- Keyword matching
- Basic document storage

CompliancePilot AI provides:

- Autonomous AI workforce
- Explainable AI findings
- Risk intelligence scoring
- Malaysian regulation-focused analysis
- Automated audit reporting
- RAG-powered compliance verification

---

# Implementation Roadmap

## Phase 1 — MVP

- User authentication
- Document upload
- OCR processing
- Compliance analysis
- PDF reports

## Phase 2

- Additional Malaysian regulations
- Clause comparison engine
- Real-time compliance monitoring

## Phase 3

- Autonomous compliance monitoring
- Scheduled audits
- Email alerts
- Workflow approvals

## Phase 4

- ERP integrations
- HRMS integrations
- Government compliance APIs

---

# Technology Stack

| Category | Technology |
|-----------|-----------|
| Frontend | Next.js 15, React 19 |
| Backend | FastAPI |
| Database | PostgreSQL |
| AI Framework | CrewAI |
| LLM | OpenAI |
| RAG | LangChain + ChromaDB |
| OCR | Tesseract OCR |
| Reporting | ReportLab |
| Deployment | Docker |

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-team/CompliancePilot-AI.git

cd CompliancePilot-AI
```

## Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

## Docker Deployment

```bash
docker compose up --build
```

---

# Demo Flow

1. Register account
2. Login
3. Upload employment contract
4. Run AI analysis
5. Review findings
6. Check risk score
7. Generate PDF report

---



---

# Vision

CompliancePilot AI aims to become Malaysia's first AI-powered Compliance Workforce Platform, enabling organizations to move from reactive compliance management to proactive regulatory intelligence.

> **"From Manual Compliance Reviews to Autonomous Compliance Intelligence."**

---

## Built for NexHack 2026 🚀

Building the Future of Autonomous Enterprise Operations.
