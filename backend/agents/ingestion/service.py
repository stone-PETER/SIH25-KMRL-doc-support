"""
Document Ingestion Agent Service
Handles document upload, validation, and initial processing
"""
import os
import hashlib
from datetime import datetime
from fastapi import UploadFile
from sqlalchemy.orm import Session
from database.models import Document, DocumentType, DocumentStatus
from config.settings import settings


class IngestionService:
    """
    Service for handling document ingestion
    """
    
    ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.doc', '.docx', '.xls', '.xlsx'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    def __init__(self, db: Session):
        self.db = db
        self.storage_path = settings.STORAGE_PATH
        
    async def validate_file(self, file: UploadFile) -> dict:
        """
        Validate uploaded file
        """
        errors = []
        
        # Check file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in self.ALLOWED_EXTENSIONS:
            errors.append(f"File type {file_ext} not allowed")
        
        # Check file size (read first chunk to estimate)
        content = await file.read()
        await file.seek(0)  # Reset file pointer
        
        if len(content) > self.MAX_FILE_SIZE:
            errors.append(f"File size exceeds maximum allowed size of {self.MAX_FILE_SIZE / (1024*1024)}MB")
        
        if errors:
            return {"valid": False, "errors": errors}
        
        return {"valid": True, "file_size": len(content), "file_type": file_ext}
    
    async def process_upload(self, file: UploadFile) -> dict:
        """
        Process document upload
        """
        # Validate file
        validation = await self.validate_file(file)
        if not validation["valid"]:
            raise ValueError(f"File validation failed: {validation['errors']}")
        
        # Read file content
        content = await file.read()
        
        # Calculate checksum
        checksum = hashlib.sha256(content).hexdigest()
        
        # Check for duplicates
        existing = self.db.query(Document).filter(Document.checksum == checksum).first()
        if existing:
            return {
                "document_id": existing.id,
                "filename": existing.filename,
                "duplicate": True
            }
        
        # Determine file type
        file_ext = os.path.splitext(file.filename)[1].lower()
        file_type = self._get_document_type(file_ext)
        
        # Generate unique filename
        unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{checksum[:8]}_{file.filename}"
        
        # Create storage directory if not exists
        os.makedirs(self.storage_path, exist_ok=True)
        
        # Save file to storage
        file_path = os.path.join(self.storage_path, unique_filename)
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Create database record
        document = Document(
            filename=unique_filename,
            original_filename=file.filename,
            file_type=file_type,
            file_size=len(content),
            status=DocumentStatus.UPLOADED,
            storage_path=file_path,
            checksum=checksum
        )
        
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        return {
            "document_id": document.id,
            "filename": document.filename,
            "duplicate": False
        }
    
    def _get_document_type(self, file_ext: str) -> DocumentType:
        """
        Determine document type from file extension
        """
        type_mapping = {
            '.pdf': DocumentType.PDF,
            '.jpg': DocumentType.IMAGE,
            '.jpeg': DocumentType.IMAGE,
            '.png': DocumentType.IMAGE,
            '.tiff': DocumentType.IMAGE,
            '.doc': DocumentType.WORD,
            '.docx': DocumentType.WORD,
            '.xls': DocumentType.EXCEL,
            '.xlsx': DocumentType.EXCEL
        }
        return type_mapping.get(file_ext, DocumentType.OTHER)
