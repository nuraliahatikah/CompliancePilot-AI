from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload

from app.auth import get_current_user
from app.database import get_db
from app.models import Analysis, AuditLog, Document, Report, User
from app.schemas import MessageResponse, ReportResponse
from app.utils.report_generator import report_generator

router = APIRouter(prefix="/reports", tags=["Reports"])


def _log_action(db: Session, user_id: int, action: str, resource_id: str) -> None:
    log = AuditLog(user_id=user_id, action=action, resource_type="report", resource_id=resource_id)
    db.add(log)
    db.commit()


@router.post("/generate/{document_id}", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def generate_report(
    document_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    doc = (
        db.query(Document)
        .options(joinedload(Document.analysis))
        .filter(Document.id == document_id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    if current_user.role.value != "admin" and doc.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    if not doc.analysis:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document must be analyzed before generating a report")

    file_path = report_generator.generate_report(doc, doc.analysis, current_user.full_name)
    report = Report(
        document_id=doc.id,
        owner_id=current_user.id,
        title=f"Compliance Audit Report - {doc.title}",
        file_path=file_path,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    _log_action(db, current_user.id, "report_generated", str(report.id))
    return ReportResponse(
        id=report.id,
        document_id=report.document_id,
        title=report.title,
        file_path=report.file_path,
        created_at=report.created_at,
        download_url=f"/api/reports/{report.id}/download",
    )


@router.get("/", response_model=list[ReportResponse])
def list_reports(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    query = db.query(Report)
    if current_user.role.value != "admin":
        query = query.filter(Report.owner_id == current_user.id)
    reports = query.order_by(Report.created_at.desc()).all()
    return [
        ReportResponse(
            id=r.id,
            document_id=r.document_id,
            title=r.title,
            file_path=r.file_path,
            created_at=r.created_at,
            download_url=f"/api/reports/{r.id}/download",
        )
        for r in reports
    ]


@router.get("/{report_id}/download")
def download_report(
    report_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    if current_user.role.value != "admin" and report.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    file_path = Path(report.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report file not found")

    _log_action(db, current_user.id, "report_downloaded", str(report_id))
    return FileResponse(
        path=str(file_path),
        filename=f"compliance_report_{report.document_id}.pdf",
        media_type="application/pdf",
    )


@router.delete("/{report_id}", response_model=MessageResponse)
def delete_report(
    report_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    if current_user.role.value != "admin" and report.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    file_path = Path(report.file_path)
    if file_path.exists():
        file_path.unlink()

    db.delete(report)
    db.commit()
    return MessageResponse(message="Report deleted successfully")
