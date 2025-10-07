"""
API endpoints package
"""
from . import documents, ingestion, ocr, classification, metadata, search, storage

__all__ = [
    "documents",
    "ingestion",
    "ocr",
    "classification",
    "metadata",
    "search",
    "storage"
]
