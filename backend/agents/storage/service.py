"""
Storage Agent Service
Manages document storage across different backends (local, S3, MinIO)
"""
import os
from sqlalchemy.orm import Session
from database.models import Document
from config.settings import settings


class StorageService:
    """
    Service for managing document storage
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.storage_type = settings.STORAGE_TYPE
        self.storage_path = settings.STORAGE_PATH
    
    async def get_file_path(self, document_id: int) -> str:
        """
        Get file path for a document
        """
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return None
        
        return document.storage_path
    
    async def get_storage_info(self, document_id: int) -> dict:
        """
        Get storage information for a document
        """
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return None
        
        file_exists = os.path.exists(document.storage_path) if document.storage_path else False
        
        return {
            "document_id": document_id,
            "storage_type": self.storage_type,
            "storage_path": document.storage_path,
            "file_size": document.file_size,
            "file_exists": file_exists,
            "checksum": document.checksum
        }
    
    async def migrate(self, document_id: int, target_storage: str) -> dict:
        """
        Migrate document to different storage backend
        TODO: Implement actual migration logic for S3, MinIO, etc.
        """
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError(f"Document {document_id} not found")
        
        # Placeholder for actual migration
        # In production, this would:
        # 1. Copy file to target storage
        # 2. Verify copy
        # 3. Update database with new path
        # 4. Delete from old storage
        
        return {
            "success": True,
            "old_storage": self.storage_type,
            "new_storage": target_storage,
            "message": "Migration simulated (not implemented)"
        }
    
    async def delete(self, document_id: int):
        """
        Delete document from storage
        """
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError(f"Document {document_id} not found")
        
        # Delete physical file
        if document.storage_path and os.path.exists(document.storage_path):
            os.remove(document.storage_path)
        
        # Delete database record handled by documents endpoint
        return True
    
    async def verify_integrity(self, document_id: int) -> dict:
        """
        Verify file integrity using checksum
        """
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError(f"Document {document_id} not found")
        
        if not os.path.exists(document.storage_path):
            return {
                "valid": False,
                "error": "File not found"
            }
        
        # Calculate current checksum
        import hashlib
        with open(document.storage_path, 'rb') as f:
            current_checksum = hashlib.sha256(f.read()).hexdigest()
        
        is_valid = current_checksum == document.checksum
        
        return {
            "valid": is_valid,
            "stored_checksum": document.checksum,
            "current_checksum": current_checksum
        }
