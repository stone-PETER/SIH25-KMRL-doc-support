"""
Metadata Extraction Agent Service
Extracts and manages document metadata
"""
from sqlalchemy.orm import Session
from database.models import Document, DocumentMetadata, OCRResult
import re


class MetadataService:
    """
    Service for extracting and managing document metadata
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def extract(self, document_id: int) -> dict:
        """
        Extract metadata from a document
        """
        # Get document and OCR results
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError(f"Document {document_id} not found")
        
        ocr_result = self.db.query(OCRResult).filter(
            OCRResult.document_id == document_id
        ).first()
        
        # Extract metadata
        metadata = self._extract_metadata(
            document,
            ocr_result.extracted_text if ocr_result else ""
        )
        
        # Save metadata to database
        for key, value in metadata.items():
            meta = DocumentMetadata(
                document_id=document_id,
                key=key,
                value=str(value["value"]),
                extracted_by="metadata_agent",
                confidence=value["confidence"]
            )
            self.db.add(meta)
        
        self.db.commit()
        
        return {"metadata": metadata}
    
    async def get_metadata(self, document_id: int) -> dict:
        """
        Get metadata for a document
        """
        results = self.db.query(DocumentMetadata).filter(
            DocumentMetadata.document_id == document_id
        ).all()
        
        if not results:
            return None
        
        metadata = {
            r.key: {
                "value": r.value,
                "confidence": r.confidence,
                "extracted_by": r.extracted_by
            }
            for r in results
        }
        
        return {
            "document_id": document_id,
            "metadata": metadata
        }
    
    async def update_metadata(self, document_id: int, metadata: dict) -> dict:
        """
        Update metadata for a document
        """
        for key, value in metadata.items():
            # Check if metadata exists
            existing = self.db.query(DocumentMetadata).filter(
                DocumentMetadata.document_id == document_id,
                DocumentMetadata.key == key
            ).first()
            
            if existing:
                existing.value = str(value)
                existing.confidence = 100  # Manual update has 100% confidence
            else:
                meta = DocumentMetadata(
                    document_id=document_id,
                    key=key,
                    value=str(value),
                    extracted_by="manual",
                    confidence=100
                )
                self.db.add(meta)
        
        self.db.commit()
        return {"message": "Metadata updated successfully"}
    
    def _extract_metadata(self, document: Document, text: str) -> dict:
        """
        Extract metadata from document and text
        TODO: Implement actual metadata extraction using NER and pattern matching
        """
        metadata = {}
        
        # Extract dates
        date_pattern = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b'
        dates = re.findall(date_pattern, text)
        if dates:
            metadata["dates"] = {
                "value": dates,
                "confidence": 70
            }
        
        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            metadata["emails"] = {
                "value": emails,
                "confidence": 90
            }
        
        # Extract phone numbers
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        if phones:
            metadata["phone_numbers"] = {
                "value": phones,
                "confidence": 80
            }
        
        # Document properties
        metadata["file_size"] = {
            "value": document.file_size,
            "confidence": 100
        }
        
        metadata["file_type"] = {
            "value": document.file_type.value,
            "confidence": 100
        }
        
        return metadata
