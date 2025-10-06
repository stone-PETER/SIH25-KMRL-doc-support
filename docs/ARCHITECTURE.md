# Architecture Overview

## System Architecture

The Intelligent Document Automation System is built with a microservices architecture, separating concerns into distinct, independently deployable agents.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Client Layer (Browser)                      │
│                    React Single Page Application                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/REST API
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                           │
│                   FastAPI Backend (main.py)                      │
│                   - CORS Middleware                              │
│                   - Request Routing                              │
│                   - OpenAPI Documentation                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌──────────────────────┐    ┌──────────────────────┐
│   API Endpoints      │    │   Common Utilities   │
│   /api/v1/*          │    │   - Validation       │
│   - documents        │    │   - Formatting       │
│   - ingestion        │    │   - Error Handling   │
│   - ocr              │    └──────────────────────┘
│   - classification   │
│   - metadata         │
│   - search           │
│   - storage          │
└──────────┬───────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Service Layer                           │
│                  (Microservices Architecture)                    │
├──────────────┬──────────────┬──────────────┬──────────────┬─────┤
│  Ingestion   │     OCR      │  Classifier  │   Metadata   │ ... │
│    Agent     │    Agent     │    Agent     │    Agent     │     │
│              │              │              │              │     │
│ - Validate   │ - Extract    │ - Categorize │ - Extract    │     │
│ - Upload     │ - OCR Text   │ - Tag        │ - Parse      │     │
│ - Checksum   │ - Confidence │ - ML Models  │ - Patterns   │     │
└──────┬───────┴──────┬───────┴──────┬───────┴──────┬───────┴─────┘
       │              │              │              │
       └──────────────┴──────────────┴──────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Layer                                  │
├──────────────┬──────────────┬──────────────┬──────────────┬─────┤
│  PostgreSQL  │    Redis     │ Elasticsearch│   Storage    │ ... │
│              │              │              │              │     │
│ - Documents  │ - Cache      │ - Full-text  │ - Local      │     │
│ - OCR Data   │ - Sessions   │ - Vector DB  │ - S3/MinIO   │     │
│ - Metadata   │ - Queue      │ - Indexing   │ - Files      │     │
└──────────────┴──────────────┴──────────────┴──────────────┴─────┘
```

## Component Details

### 1. Frontend (React)

**Technology Stack:**
- React 18
- React Router for navigation
- Axios for API calls
- CSS Modules for styling

**Key Components:**
- Dashboard: System overview with statistics
- Upload: Document upload interface
- DocumentList: Browse all documents
- DocumentDetail: View document details, OCR, classification
- Search: Search and filter documents
- Header: Navigation bar

**Features:**
- Responsive design
- Real-time status updates
- File validation
- Error handling
- Loading states

### 2. Backend (FastAPI)

**Technology Stack:**
- FastAPI (Python)
- SQLAlchemy ORM
- Pydantic for validation
- Uvicorn ASGI server

**API Structure:**
```
/api/v1/
├── documents/
│   ├── GET / (list)
│   ├── GET /{id}
│   ├── DELETE /{id}
│   └── GET /{id}/status
├── ingestion/
│   ├── POST /upload
│   ├── POST /upload/batch
│   └── POST /validate
├── ocr/
│   ├── POST /process/{id}
│   ├── GET /result/{id}
│   └── POST /reprocess/{id}
├── classification/
│   ├── POST /classify/{id}
│   ├── GET /categories
│   └── GET /result/{id}
├── metadata/
│   ├── POST /extract/{id}
│   ├── GET /{id}
│   └── PUT /{id}
├── search/
│   ├── GET /
│   ├── POST /index/{id}
│   ├── GET /similar/{id}
│   └── GET /advanced
└── storage/
    ├── GET /download/{id}
    ├── GET /info/{id}
    ├── POST /migrate/{id}
    └── DELETE /{id}
```

### 3. AI Agent Microservices

#### Ingestion Agent
**Purpose:** Handle document uploads and initial validation

**Capabilities:**
- File type validation
- Size limit enforcement
- Duplicate detection via checksum
- Multi-format support (PDF, images, Office docs)
- Batch processing

**Flow:**
1. Receive file upload
2. Validate file type and size
3. Calculate checksum
4. Check for duplicates
5. Store file
6. Create database record

#### OCR Agent
**Purpose:** Extract text from images and PDFs

**Capabilities:**
- Text extraction from multiple formats
- Multi-page document support
- Confidence scoring
- Support for multiple OCR engines (Tesseract, AWS Textract, etc.)

**Flow:**
1. Retrieve document from storage
2. Process each page
3. Extract text
4. Calculate confidence scores
5. Store OCR results
6. Update document status

**Integration Points:**
- Tesseract OCR (open-source)
- AWS Textract (cloud service)
- Google Cloud Vision (cloud service)

#### Classifier Agent
**Purpose:** Categorize documents using ML models

**Capabilities:**
- Multi-level classification
- Tag generation
- Confidence scoring
- Custom category support
- ML model versioning

**Flow:**
1. Get document OCR text
2. Preprocess text
3. Run classification model
4. Determine category/subcategory
5. Generate tags
6. Store results

**ML Models:**
- Text classification (scikit-learn, transformers)
- Zero-shot classification
- Custom trained models

#### Metadata Agent
**Purpose:** Extract structured metadata from documents

**Capabilities:**
- Named Entity Recognition (NER)
- Pattern-based extraction
- Date/email/phone extraction
- Custom field extraction
- Manual metadata editing

**Flow:**
1. Get document OCR text
2. Apply extraction patterns
3. Run NER models
4. Extract entities (dates, emails, names)
5. Store metadata with confidence scores

**Extraction Types:**
- Dates (various formats)
- Email addresses
- Phone numbers
- Names (people, organizations)
- Custom patterns (invoice numbers, etc.)

#### Storage Agent
**Purpose:** Manage document storage across backends

**Capabilities:**
- Multiple storage backends (local, S3, MinIO)
- File integrity verification
- Storage migration
- Compression support
- Backup management

**Flow:**
1. Store uploaded files
2. Verify checksums
3. Manage storage locations
4. Handle migrations
5. Clean up deleted files

**Storage Backends:**
- Local filesystem
- Amazon S3
- MinIO (S3-compatible)
- Azure Blob Storage
- Google Cloud Storage

#### Search Agent
**Purpose:** Provide semantic search capabilities

**Capabilities:**
- Full-text search
- Vector similarity search
- Advanced filtering
- Similar document finding
- Search result ranking

**Flow:**
1. Index document text
2. Generate vector embeddings
3. Store in Elasticsearch
4. Handle search queries
5. Rank and return results

**Search Technologies:**
- Elasticsearch (full-text)
- Vector embeddings (sentence-transformers)
- Cosine similarity
- BM25 ranking

### 4. Database Schema

#### Documents Table
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_type ENUM('pdf', 'image', 'word', 'excel', 'other'),
    file_size INTEGER,
    status ENUM('uploaded', 'processing', 'completed', 'failed'),
    upload_date TIMESTAMP DEFAULT NOW(),
    processed_date TIMESTAMP,
    storage_path VARCHAR(500),
    checksum VARCHAR(64)
);
```

#### OCR Results Table
```sql
CREATE TABLE ocr_results (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id),
    extracted_text TEXT,
    confidence_score INTEGER,
    page_number INTEGER,
    processing_time INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Document Classifications Table
```sql
CREATE TABLE document_classifications (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    confidence_score INTEGER,
    tags JSON,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 5. Workflow Automation (n8n)

**Purpose:** Orchestrate multi-step document processing

**Workflow Steps:**
1. Webhook trigger (document uploaded)
2. Call ingestion API
3. Process OCR
4. Classify document
5. Extract metadata
6. Index for search
7. Send notifications

**Benefits:**
- Visual workflow design
- Easy integration with external systems
- Scheduled tasks
- Error handling and retry logic
- Monitoring and logging

## Deployment Architecture

### Docker Compose Deployment

```
┌─────────────┐
│   Frontend  │ :3000
│   (nginx)   │
└──────┬──────┘
       │
┌──────▼──────┐
│   Backend   │ :8000
│  (FastAPI)  │
└──────┬──────┘
       │
┌──────┴──────────────────────────────────┐
│                                          │
▼              ▼              ▼            ▼
┌────────┐ ┌────────┐ ┌────────────┐ ┌────────┐
│Postgres│ │ Redis  │ │Elasticsearch│ │  n8n   │
│  :5432 │ │ :6379  │ │   :9200    │ │ :5678  │
└────────┘ └────────┘ └────────────┘ └────────┘
```

### Kubernetes Deployment

```
┌─────────────────────────────────────────────┐
│              Kubernetes Cluster             │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │         Namespace: kmrl-doc-automation│  │
│  │                                       │  │
│  │  ┌──────────┐  ┌──────────┐         │  │
│  │  │ Frontend │  │ Backend  │         │  │
│  │  │ (x2 pods)│  │(x3 pods) │         │  │
│  │  └─────┬────┘  └────┬─────┘         │  │
│  │        │            │               │  │
│  │        └────────┬───┘               │  │
│  │                 │                   │  │
│  │  ┌──────────────┴─────────────┐    │  │
│  │  │                             │    │  │
│  │  ▼              ▼              ▼    │  │
│  │  PostgreSQL    Redis    Elasticsearch│  │
│  │  (PVC)                    (PVC)     │  │
│  └───────────────────────────────────────┘│
└─────────────────────────────────────────────┘
```

## Security Considerations

1. **Authentication & Authorization**
   - JWT tokens for API authentication
   - Role-based access control
   - Session management

2. **Data Security**
   - Encrypted storage
   - SSL/TLS for all connections
   - Secure file upload validation
   - Virus scanning integration

3. **Network Security**
   - CORS configuration
   - API rate limiting
   - Firewall rules
   - DDoS protection

4. **Secret Management**
   - Environment variables
   - Kubernetes secrets
   - AWS Secrets Manager
   - HashiCorp Vault

## Scalability

### Horizontal Scaling
- Multiple backend replicas
- Load balancing
- Database connection pooling
- Redis caching

### Vertical Scaling
- Resource limits per service
- Auto-scaling based on metrics
- Queue-based processing for heavy tasks

### Performance Optimization
- Caching strategy (Redis)
- Database indexing
- CDN for static assets
- Lazy loading
- Pagination

## Monitoring & Logging

### Metrics to Monitor
- API response times
- Error rates
- Document processing time
- Storage usage
- Database performance

### Logging Strategy
- Structured logging (JSON)
- Log aggregation (ELK stack)
- Error tracking (Sentry)
- Performance monitoring (New Relic, Datadog)

### Health Checks
- Liveness probes
- Readiness probes
- Database connectivity
- Storage accessibility

## Future Enhancements

1. **AI Model Improvements**
   - Fine-tuned classification models
   - Custom NER models
   - Multi-language support
   - Advanced OCR for handwriting

2. **Features**
   - Document versioning
   - Collaboration features
   - Approval workflows
   - Email integration
   - Mobile app

3. **Performance**
   - Distributed processing
   - GPU acceleration for ML
   - Advanced caching strategies
   - Real-time updates (WebSockets)

4. **Integration**
   - SharePoint integration
   - Google Drive sync
   - Slack notifications
   - Zapier integration
