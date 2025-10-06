"""
Document classification endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from agents.classifier.service import ClassifierService

router = APIRouter()

@router.post("/classify/{document_id}")
async def classify_document(document_id: int, db: Session = Depends(get_db)):
    """
    Classify a document
    """
    try:
        classifier_service = ClassifierService(db)
        result = await classifier_service.classify(document_id)
        return {
            "message": "Document classified successfully",
            "document_id": document_id,
            "category": result["category"],
            "subcategory": result["subcategory"],
            "confidence": result["confidence"],
            "tags": result["tags"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_categories():
    """
    Get available document categories
    """
    classifier_service = ClassifierService(None)
    categories = await classifier_service.get_categories()
    return {"categories": categories}

@router.get("/result/{document_id}")
async def get_classification_result(document_id: int, db: Session = Depends(get_db)):
    """
    Get classification results for a document
    """
    classifier_service = ClassifierService(db)
    result = await classifier_service.get_result(document_id)
    if not result:
        raise HTTPException(status_code=404, detail="Classification result not found")
    return result
