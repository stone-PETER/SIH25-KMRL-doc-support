"""
Storage management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from agents.storage.service import StorageService
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/download/{document_id}")
async def download_document(document_id: int, db: Session = Depends(get_db)):
    """
    Download a document
    """
    storage_service = StorageService(db)
    file_path = await storage_service.get_file_path(document_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="Document not found")
    return FileResponse(file_path)

@router.get("/info/{document_id}")
async def get_storage_info(document_id: int, db: Session = Depends(get_db)):
    """
    Get storage information for a document
    """
    storage_service = StorageService(db)
    info = await storage_service.get_storage_info(document_id)
    if not info:
        raise HTTPException(status_code=404, detail="Document not found")
    return info

@router.post("/migrate/{document_id}")
async def migrate_storage(
    document_id: int,
    target_storage: str,
    db: Session = Depends(get_db)
):
    """
    Migrate document to different storage backend
    """
    try:
        storage_service = StorageService(db)
        result = await storage_service.migrate(document_id, target_storage)
        return {
            "message": "Document migrated successfully",
            "document_id": document_id,
            "target_storage": target_storage
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{document_id}")
async def delete_from_storage(document_id: int, db: Session = Depends(get_db)):
    """
    Delete document from storage
    """
    try:
        storage_service = StorageService(db)
        await storage_service.delete(document_id)
        return {"message": "Document deleted from storage successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
