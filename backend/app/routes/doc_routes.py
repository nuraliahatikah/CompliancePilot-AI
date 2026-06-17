import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session, joinedload

from app.auth import get_current_user
from app.config import get_settings
from app.database import SessionLocal, get_db
from app.models import AuditLog, Document, DocumentStatus, User
from app.schemas import DocumentDetailResponse, DocumentResponse, MessageResponse
from app.services.ocr_service import ocr_service

router = APIRouter(prefix="/documents", tags=["Documents"])
settings = get_settings()

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".png", ".jpg", ".jpeg", ".tiff"}


def _log_action(db: Session, user_id: int, action: str, resource_id: str, details: dict | None = None) -> None:
    log = AuditLog(user_id=user_id, action=action, resource_type="document", resource_id=resource_id, details=details or {})
    db.add(log)
    db.commit()


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


def _process_document_ocr(document_id: int) -> None:
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return
        doc.status = DocumentStatus.PROCESSING
        db.commit()

        text, ocr_used = ocr_service.extract_text(doc.file_path, doc.file_type)
        doc.extracted_text = text
        doc.ocr_used = ocr_used
        doc.status = DocumentStatus.OCR_COMPLETE if text.strip() else DocumentStatus.FAILED
        db.commit()
    except Exception as exc:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if doc:
            doc.status = DocumentStatus.FAILED
            doc.extracted_text = f"OCR failed: {exc}"
            db.commit()
    finally:
        db.close()


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    file: UploadFile = File(...),
    title: str = Form(...),
    document_type: str = Form(default="contract"),
):
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided")

    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    settings.upload_path.mkdir(parents=True, exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}{extension}"
    file_path = settings.upload_path / unique_name

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    document = Document(
        title=title,
        filename=file.filename,
        file_path=str(file_path),
        file_type=extension.lstrip("."),
        file_size=len(content),
        document_type=document_type,
        status=DocumentStatus.UPLOADED,
        owner_id=current_user.id,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    background_tasks.add_task(_process_document_ocr, document.id)
    _log_action(db, current_user.id, "document_uploaded", str(document.id), {"title": title})

    return _document_to_response(document)


@router.get("/", response_model=list[DocumentResponse])
def list_documents(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 50,
):
    query = db.query(Document).options(joinedload(Document.analysis))
    if current_user.role.value != "admin":
        query = query.filter(Document.owner_id == current_user.id)
    documents = query.order_by(Document.created_at.desc()).offset(skip).limit(limit).all()
    return [_document_to_response(doc) for doc in documents]


@router.get("/{document_id}", response_model=DocumentDetailResponse)
def get_document(
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

    response = DocumentDetailResponse(
        **_document_to_response(doc).model_dump(),
        extracted_text=doc.extracted_text,
        analysis=doc.analysis,
    )
    return response


@router.delete("/{document_id}", response_model=MessageResponse)
def delete_document(
    document_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    if current_user.role.value != "admin" and doc.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    file_path = Path(doc.file_path)
    if file_path.exists():
        file_path.unlink()

    db.delete(doc)
    db.commit()
    _log_action(db, current_user.id, "document_deleted", str(document_id))
    return MessageResponse(message="Document deleted successfully")


@router.post("/{document_id}/reprocess", response_model=DocumentResponse)
def reprocess_document(
    document_id: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    doc = db.query(Document).options(joinedload(Document.analysis)).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    if current_user.role.value != "admin" and doc.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    doc.status = DocumentStatus.UPLOADED
    doc.extracted_text = None
    db.commit()
    background_tasks.add_task(_process_document_ocr, document.id)
    return _document_to_response(doc)
