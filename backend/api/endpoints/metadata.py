"""
Metadata extraction endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from agents.metadata.service import MetadataService

router = APIRouter()

@router.post("/extract/{document_id}")
async def extract_metadata(document_id: int, db: Session = Depends(get_db)):
    """
    Extract metadata from a document
    """
    try:
        metadata_service = MetadataService(db)
        result = await metadata_service.extract(document_id)
        return {
            "message": "Metadata extracted successfully",
            "document_id": document_id,
            "metadata": result["metadata"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}")
async def get_metadata(document_id: int, db: Session = Depends(get_db)):
    """
    Get metadata for a document
    """
    metadata_service = MetadataService(db)
    result = await metadata_service.get_metadata(document_id)
    if not result:
        raise HTTPException(status_code=404, detail="Metadata not found")
    return result

@router.put("/{document_id}")
async def update_metadata(
    document_id: int,
    metadata: dict,
    db: Session = Depends(get_db)
):
    """
    Update metadata for a document
    """
    try:
        metadata_service = MetadataService(db)
        result = await metadata_service.update_metadata(document_id, metadata)
        return {
            "message": "Metadata updated successfully",
            "document_id": document_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
