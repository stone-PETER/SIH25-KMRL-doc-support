"""
Database models for document automation system
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database.connection import Base


class DocumentStatus(enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentType(enum.Enum):
    PDF = "pdf"
    IMAGE = "image"
    WORD = "word"
    EXCEL = "excel"
    OTHER = "other"


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(Enum(DocumentType), nullable=False)
    file_size = Column(Integer)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.UPLOADED)
    upload_date = Column(DateTime, default=datetime.utcnow)
    processed_date = Column(DateTime, nullable=True)
    storage_path = Column(String(500))
    checksum = Column(String(64))
    
    # Relationships
    ocr_results = relationship("OCRResult", back_populates="document")
    metadata = relationship("DocumentMetadata", back_populates="document")
    classification = relationship("DocumentClassification", back_populates="document")


class OCRResult(Base):
    __tablename__ = "ocr_results"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    extracted_text = Column(Text)
    confidence_score = Column(Integer)
    page_number = Column(Integer)
    processing_time = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="ocr_results")


class DocumentMetadata(Base):
    __tablename__ = "document_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    key = Column(String(100))
    value = Column(Text)
    extracted_by = Column(String(50))
    confidence = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="metadata")


class DocumentClassification(Base):
    __tablename__ = "document_classifications"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    category = Column(String(100))
    subcategory = Column(String(100), nullable=True)
    confidence_score = Column(Integer)
    tags = Column(JSON)
    model_version = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="classification")


class SearchIndex(Base):
    __tablename__ = "search_indices"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    vector_embedding = Column(JSON)
    indexed_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
