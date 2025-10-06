"""
Document search endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from agents.search.service import SearchService
from typing import Optional

router = APIRouter()

@router.get("/")
async def search_documents(
    query: str = Query(..., min_length=1),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Search documents using text query
    """
    search_service = SearchService(db)
    results = await search_service.search(query, skip, limit)
    return {
        "query": query,
        "results": results["documents"],
        "total": results["total"],
        "took": results["took"]
    }

@router.post("/index/{document_id}")
async def index_document(document_id: int, db: Session = Depends(get_db)):
    """
    Index a document for search
    """
    try:
        search_service = SearchService(db)
        result = await search_service.index_document(document_id)
        return {
            "message": "Document indexed successfully",
            "document_id": document_id
        }
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/similar/{document_id}")
async def find_similar_documents(
    document_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Find similar documents using vector similarity
    """
    search_service = SearchService(db)
    results = await search_service.find_similar(document_id, limit)
    return {"similar_documents": results}

@router.get("/advanced")
async def advanced_search(
    query: Optional[str] = None,
    category: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Advanced search with multiple filters
    """
    search_service = SearchService(db)
    results = await search_service.advanced_search(
        query=query,
        category=category,
        date_from=date_from,
        date_to=date_to
    )
    return results
