"""
API routes for the document automation system
"""
from fastapi import APIRouter
from api.endpoints import (
    documents,
    ingestion,
    ocr,
    classification,
    metadata,
    search,
    storage
)

router = APIRouter()

# Include all endpoint routers
router.include_router(documents.router, prefix="/documents", tags=["documents"])
router.include_router(ingestion.router, prefix="/ingestion", tags=["ingestion"])
router.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
router.include_router(classification.router, prefix="/classification", tags=["classification"])
router.include_router(metadata.router, prefix="/metadata", tags=["metadata"])
router.include_router(search.router, prefix="/search", tags=["search"])
router.include_router(storage.router, prefix="/storage", tags=["storage"])
