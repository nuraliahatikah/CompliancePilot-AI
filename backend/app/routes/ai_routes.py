from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.auth import get_current_user
from app.database import get_db
from app.models import Analysis, AuditLog, Document, DocumentStatus, User
from app.schemas import AnalysisRequest, AnalysisResponse, KnowledgeBaseQuery, KnowledgeBaseResponse, KnowledgeBaseResult
from app.services.crew_agents import compliance_pipeline
from app.services.rag_service import rag_service

router = APIRouter(prefix="/ai", tags=["AI Analysis"])


def _log_action(db: Session, user_id: int, action: str, resource_id: str, details: dict | None = None) -> None:
    log = AuditLog(user_id=user_id, action=action, resource_type="analysis", resource_id=resource_id, details=details or {})
    db.add(log)
    db.commit()


@router.post("/analyze/{document_id}", response_model=AnalysisResponse)
def analyze_document(
    document_id: int,
    request: AnalysisRequest,
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

    if doc.status not in (DocumentStatus.OCR_COMPLETE, DocumentStatus.COMPLETED):
        if doc.status == DocumentStatus.PROCESSING:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Document is still being processed")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Document not ready for analysis. Status: {doc.status.value}")

    if doc.analysis and not request.force_reanalyze:
        return doc.analysis

    if not doc.extracted_text or not doc.extracted_text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No text extracted from document")

    doc.status = DocumentStatus.ANALYZING
    db.commit()

    try:
        result = compliance_pipeline.analyze(doc.extracted_text, doc.document_type)

        if doc.analysis and request.force_reanalyze:
            analysis = doc.analysis
            analysis.risk_score = result["risk_score"]
            analysis.risk_level = result["risk_level"]
            analysis.summary = result["summary"]
            analysis.findings = result["findings"]
            analysis.recommendations = result["recommendations"]
            analysis.compliance_gaps = result["compliance_gaps"]
            analysis.agent_outputs = result["agent_outputs"]
            analysis.rag_sources = result["rag_sources"]
            analysis.processing_time_seconds = result["processing_time_seconds"]
        else:
            analysis = Analysis(
                document_id=doc.id,
                risk_score=result["risk_score"],
                risk_level=result["risk_level"],
                summary=result["summary"],
                findings=result["findings"],
                recommendations=result["recommendations"],
                compliance_gaps=result["compliance_gaps"],
                agent_outputs=result["agent_outputs"],
                rag_sources=result["rag_sources"],
                processing_time_seconds=result["processing_time_seconds"],
            )
            db.add(analysis)

        doc.status = DocumentStatus.COMPLETED
        db.commit()
        db.refresh(analysis)

        _log_action(
            db,
            current_user.id,
            "document_analyzed",
            str(document_id),
            {"risk_score": result["risk_score"], "risk_level": result["risk_level"].value},
        )
        return analysis
    except Exception as exc:
        doc.status = DocumentStatus.OCR_COMPLETE
        db.commit()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Analysis failed: {exc}") from exc


@router.get("/analysis/{document_id}", response_model=AnalysisResponse)
def get_analysis(
    document_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    if current_user.role.value != "admin" and doc.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    analysis = db.query(Analysis).filter(Analysis.document_id == document_id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    return analysis


@router.post("/knowledge-base/query", response_model=KnowledgeBaseResponse)
def query_knowledge_base(
    query: KnowledgeBaseQuery,
    current_user: Annotated[User, Depends(get_current_user)],
):
    results = rag_service.query(query.query, top_k=query.top_k)
    return KnowledgeBaseResponse(
        query=query.query,
        results=[KnowledgeBaseResult(**r) for r in results],
        total_results=len(results),
    )


@router.get("/knowledge-base/regulations")
def list_regulations(current_user: Annotated[User, Depends(get_current_user)]):
    return {
        "regulations": rag_service.get_all_regulations(),
        "stats": rag_service.get_stats(),
    }
