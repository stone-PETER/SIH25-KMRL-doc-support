"""
Document Classification Agent Service
Classifies documents into categories using ML models
"""
from sqlalchemy.orm import Session
from database.models import Document, DocumentClassification, OCRResult


class ClassifierService:
    """
    Service for document classification using ML models
    """
    
    CATEGORIES = {
        "contract": ["legal", "agreement", "mou"],
        "invoice": ["bill", "payment", "receipt"],
        "report": ["analysis", "summary", "technical"],
        "correspondence": ["letter", "email", "memo"],
        "technical": ["specification", "manual", "drawing"],
        "administrative": ["form", "application", "certificate"]
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    async def classify(self, document_id: int) -> dict:
        """
        Classify a document
        """
        # Get document and OCR results
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError(f"Document {document_id} not found")
        
        ocr_result = self.db.query(OCRResult).filter(
            OCRResult.document_id == document_id
        ).first()
        
        # TODO: Implement actual classification using ML model
        # This is a placeholder that simulates classification
        classification_result = self._simulate_classification(
            document.original_filename,
            ocr_result.extracted_text if ocr_result else ""
        )
        
        # Save classification result
        classification = DocumentClassification(
            document_id=document_id,
            category=classification_result["category"],
            subcategory=classification_result["subcategory"],
            confidence_score=classification_result["confidence"],
            tags=classification_result["tags"],
            model_version="v1.0.0"
        )
        
        self.db.add(classification)
        self.db.commit()
        
        return classification_result
    
    async def get_categories(self) -> list:
        """
        Get available categories
        """
        return [
            {
                "category": category,
                "subcategories": subcats
            }
            for category, subcats in self.CATEGORIES.items()
        ]
    
    async def get_result(self, document_id: int) -> dict:
        """
        Get classification result for a document
        """
        result = self.db.query(DocumentClassification).filter(
            DocumentClassification.document_id == document_id
        ).first()
        
        if not result:
            return None
        
        return {
            "document_id": document_id,
            "category": result.category,
            "subcategory": result.subcategory,
            "confidence": result.confidence_score,
            "tags": result.tags
        }
    
    def _simulate_classification(self, filename: str, text: str) -> dict:
        """
        Placeholder for actual classification implementation
        In production, this would use trained ML models
        """
        # Simple keyword-based classification for demonstration
        text_lower = (filename + " " + text).lower()
        
        for category, keywords in self.CATEGORIES.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return {
                        "category": category,
                        "subcategory": keyword,
                        "confidence": 75,
                        "tags": [category, keyword]
                    }
        
        # Default classification
        return {
            "category": "general",
            "subcategory": "unclassified",
            "confidence": 50,
            "tags": ["general"]
        }
