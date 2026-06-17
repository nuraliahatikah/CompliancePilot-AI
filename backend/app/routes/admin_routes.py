from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.auth import RequireAdmin, get_current_user
from app.database import get_db
from app.models import Analysis, AuditLog, Document, DocumentStatus, RiskLevel, User, UserRole
from app.schemas import AuditLogResponse, DashboardStats, DocumentResponse, MessageResponse, UserResponse, UserUpdate

router = APIRouter(prefix="/admin", tags=["Admin & Dashboard"])


def _document_to_response(doc: Document) -> DocumentResponse:
    return DocumentResponse(
        id=doc.id,
        title=doc.title,
        filename=doc.filename,
        file_type=doc.file_type,
        file_size=doc.file_size,
        document_type=doc.document_type,
        status=doc.status,
        ocr_used=doc.ocr_used,
        owner_id=doc.owner_id,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        has_analysis=doc.analysis is not None,
        risk_score=doc.analysis.risk_score if doc.analysis else None,
        risk_level=doc.analysis.risk_level if doc.analysis else None,
    )


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    doc_query = db.query(Document)
    if current_user.role.value != "admin":
        doc_query = doc_query.filter(Document.owner_id == current_user.id)

    total_documents = doc_query.count()
    completed = doc_query.filter(Document.status == DocumentStatus.COMPLETED).count()
    pending = doc_query.filter(
        Document.status.in_([DocumentStatus.UPLOADED, DocumentStatus.PROCESSING, DocumentStatus.OCR_COMPLETE, DocumentStatus.ANALYZING])
    ).count()

    analysis_query = db.query(Analysis).join(Document)
    if current_user.role.value != "admin":
        analysis_query = analysis_query.filter(Document.owner_id == current_user.id)

    avg_score = analysis_query.with_entities(func.avg(Analysis.risk_score)).scalar() or 0.0

    risk_dist = {level.value: 0 for level in RiskLevel}
    risk_counts = (
        analysis_query.with_entities(Analysis.risk_level, func.count(Analysis.id))
        .group_by(Analysis.risk_level)
        .all()
    )
    for level, count in risk_counts:
        risk_dist[level.value] = count

    week_ago = datetime.now(UTC) - timedelta(days=7)
    analyses_this_week = analysis_query.filter(Analysis.created_at >= week_ago).count()

    type_counts: dict[str, int] = {}
    type_rows = doc_query.with_entities(Document.document_type, func.count(Document.id)).group_by(Document.document_type).all()
    for doc_type, count in type_rows:
        type_counts[doc_type] = count

    recent = (
        doc_query.options(joinedload(Document.analysis))
        .order_by(Document.created_at.desc())
        .limit(5)
        .all()
    )

    return DashboardStats(
        total_documents=total_documents,
        completed_analyses=completed,
        pending_documents=pending,
        average_risk_score=round(float(avg_score), 1),
        risk_distribution=risk_dist,
        recent_documents=[_document_to_response(d) for d in recent],
        documents_by_type=type_counts,
        analyses_this_week=analyses_this_week,
    )


@router.get("/users", response_model=list[UserResponse])
def list_users(
    admin: Annotated[User, Depends(RequireAdmin)],
    db: Annotated[Session, Depends(get_db)],
):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    update: UserUpdate,
    admin: Annotated[User, Depends(RequireAdmin)],
    db: Annotated[Session, Depends(get_db)],
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if update.full_name is not None:
        user.full_name = update.full_name
    if update.role is not None:
        user.role = update.role
    if update.is_active is not None:
        user.is_active = update.is_active

    db.commit()
    db.refresh(user)
    return user


@router.get("/audit-logs", response_model=list[AuditLogResponse])
def get_audit_logs(
    admin: Annotated[User, Depends(RequireAdmin)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()


@router.post("/seed-demo", response_model=MessageResponse)
def seed_demo_data(
    admin: Annotated[User, Depends(RequireAdmin)],
    db: Annotated[Session, Depends(get_db)],
):
    demo_users = [
        {"email": "officer@compliancepilot.ai", "full_name": "Sarah Chen", "role": UserRole.COMPLIANCE_OFFICER, "password": "Demo1234!"},
        {"email": "auditor@compliancepilot.ai", "full_name": "James Wong", "role": UserRole.AUDITOR, "password": "Demo1234!"},
    ]
    from app.auth import get_password_hash

    created = 0
    for demo in demo_users:
        if not db.query(User).filter(User.email == demo["email"]).first():
            user = User(
                email=demo["email"],
                full_name=demo["full_name"],
                hashed_password=get_password_hash(demo["password"]),
                role=demo["role"],
            )
            db.add(user)
            created += 1

    db.commit()
    return MessageResponse(message=f"Demo seed complete. Created {created} users.")
