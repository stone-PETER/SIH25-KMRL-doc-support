"""
Document ingestion endpoints
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from agents.ingestion.service import IngestionService
from typing import List

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and ingest a new document
    """
    try:
        ingestion_service = IngestionService(db)
        result = await ingestion_service.process_upload(file)
        return {
            "message": "Document uploaded successfully",
            "document_id": result["document_id"],
            "filename": result["filename"],
            "status": "processing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload/batch")
async def upload_documents_batch(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload multiple documents in batch
    """
    ingestion_service = IngestionService(db)
    results = []
    
    for file in files:
        try:
            result = await ingestion_service.process_upload(file)
            results.append({
                "filename": result["filename"],
                "document_id": result["document_id"],
                "status": "success"
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "failed",
                "error": str(e)
            })
    
    return {"results": results}

@router.post("/validate")
async def validate_document(file: UploadFile = File(...)):
    """
    Validate document before upload
    """
    ingestion_service = IngestionService(None)
    validation_result = await ingestion_service.validate_file(file)
    return validation_result
