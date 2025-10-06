"""
Search Agent Service
Provides semantic search capabilities using vector embeddings and Elasticsearch
"""
from sqlalchemy.orm import Session
from database.models import Document, SearchIndex, OCRResult, DocumentClassification
import time


class SearchService:
    """
    Service for document search using vector embeddings and text search
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def search(self, query: str, skip: int = 0, limit: int = 20) -> dict:
        """
        Search documents using text query
        TODO: Implement actual search using Elasticsearch or vector similarity
        """
        start_time = time.time()
        
        # Placeholder: Simple SQL-based search
        # In production, this would use Elasticsearch or vector similarity search
        documents = self.db.query(Document).join(OCRResult).filter(
            OCRResult.extracted_text.ilike(f"%{query}%")
        ).offset(skip).limit(limit).all()
        
        total = self.db.query(Document).join(OCRResult).filter(
            OCRResult.extracted_text.ilike(f"%{query}%")
        ).count()
        
        took = int((time.time() - start_time) * 1000)
        
        return {
            "documents": [
                {
                    "id": doc.id,
                    "filename": doc.original_filename,
                    "upload_date": doc.upload_date.isoformat(),
                    "status": doc.status.value
                }
                for doc in documents
            ],
            "total": total,
            "took": took
        }
    
    async def index_document(self, document_id: int) -> dict:
        """
        Index a document for search
        """
        # Get document and OCR results
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError(f"Document {document_id} not found")
        
        ocr_result = self.db.query(OCRResult).filter(
            OCRResult.document_id == document_id
        ).first()
        
        if not ocr_result:
            raise ValueError(f"OCR results not found for document {document_id}")
        
        # TODO: Generate actual vector embeddings using sentence transformers
        # Placeholder: Store text for indexing
        indexed_text = ocr_result.extracted_text
        vector_embedding = []  # Placeholder for actual embeddings
        
        # Check if index exists
        existing_index = self.db.query(SearchIndex).filter(
            SearchIndex.document_id == document_id
        ).first()
        
        if existing_index:
            existing_index.indexed_text = indexed_text
            existing_index.vector_embedding = vector_embedding
        else:
            search_index = SearchIndex(
                document_id=document_id,
                indexed_text=indexed_text,
                vector_embedding=vector_embedding
            )
            self.db.add(search_index)
        
        self.db.commit()
        
        return {
            "success": True,
            "document_id": document_id
        }
    
    async def find_similar(self, document_id: int, limit: int = 10) -> list:
        """
        Find similar documents using vector similarity
        TODO: Implement actual vector similarity search
        """
        # Get document's search index
        search_index = self.db.query(SearchIndex).filter(
            SearchIndex.document_id == document_id
        ).first()
        
        if not search_index:
            return []
        
        # Placeholder: Return random documents
        # In production, this would use cosine similarity on vector embeddings
        similar_docs = self.db.query(Document).filter(
            Document.id != document_id
        ).limit(limit).all()
        
        return [
            {
                "id": doc.id,
                "filename": doc.original_filename,
                "similarity_score": 0.75  # Placeholder score
            }
            for doc in similar_docs
        ]
    
    async def advanced_search(
        self,
        query: str = None,
        category: str = None,
        date_from: str = None,
        date_to: str = None
    ) -> dict:
        """
        Advanced search with multiple filters
        """
        # Build query
        db_query = self.db.query(Document)
        
        if query:
            db_query = db_query.join(OCRResult).filter(
                OCRResult.extracted_text.ilike(f"%{query}%")
            )
        
        if category:
            db_query = db_query.join(DocumentClassification).filter(
                DocumentClassification.category == category
            )
        
        if date_from:
            db_query = db_query.filter(Document.upload_date >= date_from)
        
        if date_to:
            db_query = db_query.filter(Document.upload_date <= date_to)
        
        documents = db_query.all()
        
        return {
            "documents": [
                {
                    "id": doc.id,
                    "filename": doc.original_filename,
                    "upload_date": doc.upload_date.isoformat(),
                    "status": doc.status.value
                }
                for doc in documents
            ],
            "total": len(documents)
        }
