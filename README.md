# CompliancePilot AI

🚀 **Autonomous Compliance Intelligence Platform for Malaysian Enterprises**

> **NexHack 2026 Submission**
>
> **Track 1: Agentic AI for Internal Enterprise Operations**

---

## Overview

CompliancePilot AI is an AI-powered compliance intelligence platform that automates document compliance reviews against Malaysian regulations including the Employment Act 1955 and Personal Data Protection Act (PDPA) 2010.

The platform combines OCR, Retrieval-Augmented Generation (RAG), risk intelligence, and autonomous AI agents to help organizations detect compliance risks, explain violations, and generate audit-ready reports.

Designed for SMEs, HR departments, compliance teams, auditors, and consulting firms, CompliancePilot AI reduces manual compliance review time from hours to minutes.

---

# Problem Statement

Organizations today face increasing regulatory obligations while operating with limited compliance resources.

Manual compliance reviews are:

* Expensive
* Time-consuming
* Difficult to scale
* Prone to human error

Many SMEs and organizations lack dedicated legal or compliance teams, resulting in:

* Regulatory violations
* Financial penalties
* Audit failures
* Legal disputes
* Operational risks

CompliancePilot AI solves these challenges by providing an autonomous AI workforce capable of reviewing compliance documents quickly, accurately, and consistently.

---

# Solution

CompliancePilot AI acts as an AI-powered Compliance Officer that automatically:

✅ Reviews contracts and policies

✅ Detects compliance violations

✅ Assesses risk severity

✅ Maps findings to Malaysian regulations

✅ Generates compliance recommendations

✅ Produces audit-ready PDF reports

✅ Supports compliance officers and auditors

---

# Key Features

## 📄 Document Processing

Supported file formats:

* PDF
* DOCX
* TXT
* Images (PNG, JPG, JPEG)

Capabilities:

* OCR text extraction
* Scanned document support
* Automatic document parsing
* Multi-format upload processing

---

## 🤖 AI Compliance Analysis

The platform automatically analyzes:

* Employment contracts
* HR policies
* Internal procedures
* Governance documents
* Compliance records

Output includes:

* Compliance findings
* Regulation references
* Risk scores
* Corrective recommendations

---

## 🧠 Multi-Agent Compliance Workforce

CompliancePilot AI utilizes an autonomous AI workforce architecture.

### Agent 1: Legal Compliance Analyst

Responsibilities:

* Reviews document clauses
* Detects regulatory conflicts
* Identifies compliance issues
* Maps findings to laws

Output:

* Compliance findings
* Legal explanations
* Regulation references

---

### Agent 2: Risk Assessment Specialist

Responsibilities:

* Evaluates severity levels
* Calculates risk exposure
* Scores compliance risks

Output:

* Risk Score (0-100)
* Risk Classification

Categories:

* Low Risk
* Medium Risk
* High Risk
* Critical Risk

---

### Agent 3: Recommendation Advisor

Responsibilities:

* Generates remediation plans
* Suggests policy improvements
* Recommends corrective actions

Output:

* Actionable recommendations
* Risk mitigation strategies
* Compliance improvement plans

---

## 📚 Regulation Knowledge Base (RAG)

Powered by:

* ChromaDB
* LangChain
* Retrieval-Augmented Generation (RAG)

Knowledge sources include:

* Employment Act 1955
* Personal Data Protection Act (PDPA) 2010
* Internal compliance frameworks

Capabilities:

* Semantic search
* Clause matching
* Regulation retrieval
* Explainable AI findings

---

## 📊 Compliance Dashboard

Provides:

* Compliance statistics
* Risk analytics
* Document history
* Analysis tracking
* Compliance trends

---

## 📑 Audit Report Generator

Automatically generates:

* Executive summaries
* Compliance findings
* Risk assessments
* Recommendations
* Audit-ready reports

Export format:

* PDF

---

# Business Impact

| Metric                 | Traditional Process | CompliancePilot AI |
| ---------------------- | ------------------- | ------------------ |
| Review Time            | 2–6 Hours           | < 5 Minutes        |
| Initial Screening Cost | High                | Low                |
| Scalability            | Limited             | High               |
| Audit Readiness        | Manual              | Automated          |
| Risk Visibility        | Reactive            | Proactive          |

---

# System Architecture

```text
┌───────────────────────────────────┐
│           Next.js Frontend        │
│ React 19 + TypeScript + Tailwind  │
└─────────────────┬─────────────────┘
                  │
                  ▼
┌───────────────────────────────────┐
│           FastAPI Backend         │
│ JWT Authentication + RBAC         │
└───────┬──────────┬───────────┬────┘
        │          │           │

        ▼          ▼           ▼

 PostgreSQL    ChromaDB     OCR Engine
 Database      RAG KB      Tesseract OCR

                    │
                    ▼

          Compliance AI Pipeline

     ┌──────────┬──────────┬──────────┐
     ▼          ▼          ▼

 Legal      Risk       Recommendation
 Agent      Agent      Agent

                    │
                    ▼

            PDF Audit Report
```

---

# Technology Stack

| Category       | Technology                         |
| -------------- | ---------------------------------- |
| Frontend       | Next.js 15                         |
| UI Framework   | React 19                           |
| Language       | TypeScript                         |
| Styling        | Tailwind CSS                       |
| Components     | Shadcn/UI                          |
| Backend        | FastAPI                            |
| Database       | PostgreSQL                         |
| ORM            | SQLAlchemy                         |
| Authentication | JWT                                |
| Authorization  | RBAC                               |
| OCR            | Tesseract OCR                      |
| AI Framework   | CrewAI-inspired Multi-Agent System |
| RAG            | LangChain + ChromaDB               |
| PDF Reports    | ReportLab                          |
| Deployment     | Docker Compose                     |

---

# Security Architecture

## Authentication

* JWT Access Tokens
* Secure Login System

## Authorization

Role-Based Access Control (RBAC)

Supported Roles:

### Admin

* Full system access
* User management
* Dashboard management
* System configuration

### Compliance Officer

* Upload documents
* Run analyses
* Generate reports

### Auditor

* View reports
* Download reports
* Review compliance history

---

# Target Market

## Primary Customers

### Small and Medium Enterprises (SMEs)

Challenges:

* No dedicated compliance team
* Limited legal expertise
* Cost-sensitive operations

---

### HR Departments

Use Cases:

* Employment contract reviews
* HR policy validation

---

### Compliance Teams

Use Cases:

* Internal audits
* Regulatory monitoring

---

### Consulting Firms

Use Cases:

* Client compliance assessments
* Compliance advisory services

---

# Commercial Potential

## SaaS Subscription Model

### Starter Plan

RM49/month

Features:

* 50 document analyses
* Basic reporting

---

### Professional Plan

RM199/month

Features:

* Unlimited analyses
* Advanced reporting
* Team collaboration

---

### Enterprise Plan

Custom Pricing

Features:

* Dedicated deployment
* API integrations
* Compliance monitoring
* Priority support

---

## Revenue Streams

* SaaS subscriptions
* Enterprise licensing
* Compliance consulting partnerships
* API access

---

# Innovation & Differentiation

Most compliance tools offer:

❌ Static compliance checklists

❌ Basic keyword matching

❌ Generic document storage

CompliancePilot AI provides:

✅ Autonomous AI workforce

✅ Explainable AI findings

✅ Risk intelligence scoring

✅ Malaysian regulation-focused analysis

✅ Automated audit reporting

✅ RAG-powered compliance verification

✅ Multi-agent compliance reasoning

---

# Implementation Roadmap

## Phase 1 (Current MVP)

* User authentication
* Document upload
* OCR processing
* Compliance analysis
* PDF reports

---

## Phase 2

* Additional Malaysian regulations
* Clause comparison engine
* Enhanced risk analytics

---

## Phase 3

* Real-time compliance monitoring
* Scheduled audits
* Email notifications
* Workflow approvals

---

## Phase 4

* ERP integration
* HRMS integration
* Government compliance APIs
* Enterprise deployment options

---

# Installation

## Clone Repository

```bash
git clone https://github.com/nuraliahatikah/CompliancePilot-AI.git

cd CompliancePilot-AI
```

## Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

## Docker Deployment

```bash
docker compose up --build
```

---

# Application Access

| Service          | URL                          |
| ---------------- | ---------------------------- |
| Frontend         | http://localhost:3000        |
| Backend API      | http://localhost:8000        |
| Swagger API Docs | http://localhost:8000/docs   |
| Health Check     | http://localhost:8000/health |


---

# Team Vision

CompliancePilot AI aims to become Malaysia's leading AI-powered Compliance Workforce Platform, enabling organizations to transition from reactive compliance management to proactive compliance intelligence.

### Mission

To make enterprise-grade compliance accessible, affordable, and scalable for every organization.

---


## Built for NexHack 2026 🚀

**"From Manual Compliance Reviews to Autonomous Compliance Intelligence."**
