# CompliancePilot AI
An AI-powered Compliance & Contract Intelligence Platform that automatically reviews contracts, policies, and business documents, identifies compliance risks, provides explainable recommendations, and generates audit-ready reports

**AI-powered Compliance & Contract Intelligence Platform** for Malaysian regulatory compliance (Employment Act 1955 & PDPA 2010).

Built for hackathon demos with a fully wired Next.js 15 frontend, FastAPI backend, PostgreSQL, ChromaDB RAG, CrewAI multi-agent pipeline, and Tesseract OCR.

---

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Next.js 15     │────▶│  FastAPI Backend │────▶│  PostgreSQL     │
│  React 19 UI    │     │  JWT + RBAC      │     │  SQLAlchemy     │
└─────────────────┘     └────────┬─────────┘     └─────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
              ┌──────────┐ ┌──────────┐ ┌──────────────┐
              │ Tesseract│ │ ChromaDB │ │ CrewAI Agents│
              │ OCR      │ │ RAG      │ │ (3 agents)   │
              └──────────┘ └──────────┘ └──────────────┘
```

### Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS, Shadcn/UI, Framer Motion, Recharts |
| Backend | FastAPI, Python 3.11+, Uvicorn |
| Database | PostgreSQL, SQLAlchemy |
| Auth | JWT, Role-Based Access Control (Admin, Compliance Officer, Auditor) |
| AI | CrewAI, LangChain, ChromaDB, Tesseract OCR |
| Reports | ReportLab PDF generation |
| Deploy | Docker & Docker Compose |

---

## Quick Start (Docker)

### Prerequisites

- Docker & Docker Compose
- (Optional) OpenAI API key for full CrewAI LLM analysis

### 1. Clone and configure

```bash
cd CompliancePilot-AI
cp backend/.env.example backend/.env
# Optionally set OPENAI_API_KEY in backend/.env or export it
```

### 2. Start all services

```bash
docker compose up --build
```

### 3. Access the application

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

### 4. Register & demo

1. Open http://localhost:3000/register
2. **First user becomes Admin automatically**
3. Upload `sample-documents/sample-employment-contract.txt`
4. Wait for OCR processing (~3 seconds)
5. Click **Run AI Analysis**
6. Download the PDF audit report to computer

---

## Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

# Requires PostgreSQL running locally
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

---

## User Roles

| Role | Permissions |
|------|-------------|
| **Admin** | Full access, user management, audit logs, seed demo data |
| **Compliance Officer** | Upload documents, run analysis, generate reports |
| **Auditor** | View documents, analysis results, download reports |

---

## API Endpoints

### Authentication
- `POST /api/auth/register` — Register new user
- `POST /api/auth/login` — Login, receive JWT
- `GET /api/auth/me` — Current user profile

### Documents
- `POST /api/documents/upload` — Upload document (multipart)
- `GET /api/documents/` — List documents
- `GET /api/documents/{id}` — Document detail + analysis
- `DELETE /api/documents/{id}` — Delete document

### AI Analysis
- `POST /api/ai/analyze/{id}` — Run CrewAI compliance analysis
- `GET /api/ai/analysis/{id}` — Get analysis results
- `POST /api/ai/knowledge-base/query` — RAG semantic search
- `GET /api/ai/knowledge-base/regulations` — List all regulations

### Reports
- `POST /api/reports/generate/{document_id}` — Generate PDF report
- `GET /api/reports/{id}/download` — Download PDF

### Admin
- `GET /api/admin/dashboard` — Dashboard statistics
- `GET /api/admin/users` — List users (Admin only)
- `POST /api/admin/seed-demo` — Seed demo users (Admin only)

---

## AI Pipeline

### Without OpenAI API Key (Default Demo Mode)
Uses **rule-based RAG analysis** that:
- Pattern-matches compliance risk indicators in document text
- Cross-references ChromaDB/keyword search against 15 Malaysian regulations
- Produces risk scores, findings, and recommendations

### With OpenAI API Key
Activates full **CrewAI multi-agent pipeline**:
1. **Legal Compliance Analyst** — Identifies regulatory issues
2. **Risk Assessment Specialist** — Calculates risk score (0–100)
3. **Policy Recommendation Advisor** — Generates remediation steps

Set `OPENAI_API_KEY` in `backend/.env` or docker-compose environment.

---

## Project Structure

```
CompliancePilot-AI/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Settings
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── models.py            # ORM models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── auth.py              # JWT & RBAC
│   │   ├── routes/              # API route handlers
│   │   ├── services/            # OCR, RAG, CrewAI
│   │   ├── utils/               # PDF report generator
│   │   └── data/                # Malaysian regulations seed
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js App Router pages
│   │   ├── components/          # UI components
│   │   └── lib/                 # API client & utilities
│   ├── Dockerfile
│   └── package.json
├── sample-documents/            # Demo contract for testing
├── docker-compose.yml
└── README.md
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://compliance:compliance123@localhost:5432/compliancepilot` | PostgreSQL connection |
| `SECRET_KEY` | (change in production) | JWT signing key |
| `OPENAI_API_KEY` | (empty) | Enables CrewAI LLM pipeline |
| `CORS_ORIGINS` | `http://localhost:3000` | Allowed frontend origins |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend URL for frontend |

---


---

## License

MIT — Built for hackathon demonstration purposes.
