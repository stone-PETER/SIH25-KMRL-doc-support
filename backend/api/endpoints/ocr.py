"""
OCR processing endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from agents.ocr.service import OCRService

router = APIRouter()

@router.post("/process/{document_id}")
async def process_ocr(document_id: int, db: Session = Depends(get_db)):
    """
    Process OCR for a specific document
    """
    try:
        ocr_service = OCRService(db)
        result = await ocr_service.process_document(document_id)
        return {
            "message": "OCR processing completed",
            "document_id": document_id,
            "text_length": len(result["text"]),
            "confidence": result["confidence"],
            "pages": result["pages"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/result/{document_id}")
async def get_ocr_result(document_id: int, db: Session = Depends(get_db)):
    """
    Get OCR results for a document
    """
    ocr_service = OCRService(db)
    result = await ocr_service.get_result(document_id)
    if not result:
        raise HTTPException(status_code=404, detail="OCR result not found")
    return result

@router.post("/reprocess/{document_id}")
async def reprocess_ocr(document_id: int, db: Session = Depends(get_db)):
    """
    Reprocess OCR for a document
    """
    try:
        ocr_service = OCRService(db)
        result = await ocr_service.reprocess_document(document_id)
        return {
            "message": "OCR reprocessing completed",
            "document_id": document_id,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
