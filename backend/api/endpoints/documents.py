"""
Document management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from database import get_db, Document
from datetime import datetime

router = APIRouter()

@router.get("/")
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all documents with pagination
    """
    documents = db.query(Document).offset(skip).limit(limit).all()
    return {"documents": documents, "total": db.query(Document).count()}

@router.get("/{document_id}")
async def get_document(document_id: int, db: Session = Depends(get_db)):
    """
    Get a specific document by ID
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.delete("/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """
    Delete a document by ID
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    db.delete(document)
    db.commit()
    return {"message": "Document deleted successfully"}

@router.get("/{document_id}/status")
async def get_document_status(document_id: int, db: Session = Depends(get_db)):
    """
    Get the processing status of a document
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {
        "document_id": document.id,
        "status": document.status.value,
        "upload_date": document.upload_date,
        "processed_date": document.processed_date
    }
