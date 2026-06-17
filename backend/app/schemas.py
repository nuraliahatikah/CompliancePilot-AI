from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import DocumentStatus, RiskLevel, UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None
    email: str | None = None
    role: UserRole | None = None


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.COMPLIANCE_OFFICER


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: UserRole
    is_active: bool
    created_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    document_type: str = "contract"


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    filename: str
    file_type: str
    file_size: int
    document_type: str
    status: DocumentStatus
    ocr_used: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime
    has_analysis: bool = False
    risk_score: float | None = None
    risk_level: RiskLevel | None = None


class DocumentDetailResponse(DocumentResponse):
    extracted_text: str | None = None
    analysis: "AnalysisResponse | None" = None


class FindingItem(BaseModel):
    category: str
    severity: str
    title: str
    description: str
    regulation_reference: str | None = None
    clause_excerpt: str | None = None


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_id: int
    risk_score: float
    risk_level: RiskLevel
    summary: str
    findings: list[FindingItem | dict[str, Any]]
    recommendations: list[str]
    compliance_gaps: list[str]
    agent_outputs: dict[str, Any]
    rag_sources: list[dict[str, Any]]
    processing_time_seconds: float
    created_at: datetime


class AnalysisRequest(BaseModel):
    force_reanalyze: bool = False


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_id: int
    title: str
    file_path: str
    created_at: datetime
    download_url: str | None = None


class DashboardStats(BaseModel):
    total_documents: int
    completed_analyses: int
    pending_documents: int
    average_risk_score: float
    risk_distribution: dict[str, int]
    recent_documents: list[DocumentResponse]
    documents_by_type: dict[str, int]
    analyses_this_week: int


class KnowledgeBaseQuery(BaseModel):
    query: str = Field(min_length=3, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)


class KnowledgeBaseResult(BaseModel):
    content: str
    source: str
    regulation: str
    section: str
    relevance_score: float


class KnowledgeBaseResponse(BaseModel):
    query: str
    results: list[KnowledgeBaseResult]
    total_results: int


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None
    action: str
    resource_type: str
    resource_id: str | None
    details: dict[str, Any]
    created_at: datetime


class MessageResponse(BaseModel):
    message: str
    detail: str | None = None


class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    chroma: str


DocumentDetailResponse.model_rebuild()
