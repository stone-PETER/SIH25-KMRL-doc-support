# Intelligent Document Automation System

An AI-powered document processing system for Kochi Metro Rail Limited (KMRL) to automate document ingestion, OCR, classification, metadata extraction, storage, and search.

## Architecture

This system consists of:

### Backend (FastAPI)
- **Main API**: FastAPI application with REST endpoints
- **Database**: PostgreSQL for storing document metadata
- **Cache**: Redis for performance optimization
- **Search**: Elasticsearch for full-text and semantic search

### AI Agent Microservices
1. **Ingestion Agent**: Handles document upload and validation
2. **OCR Agent**: Extracts text from images and PDFs
3. **Classifier Agent**: Categorizes documents using ML models
4. **Metadata Agent**: Extracts structured metadata
5. **Storage Agent**: Manages document storage
6. **Search Agent**: Provides semantic search capabilities

### Frontend (React)
- Modern React application with responsive UI
- Document upload and management
- Search interface
- Real-time status tracking

### Workflow Automation (n8n)
- Automated document processing pipelines
- Integration with external systems
- Scheduled tasks

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

### Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/stone-PETER/SIH25-KMRL-doc-support.git
   cd SIH25-KMRL-doc-support
   ```

2. Start all services:
   ```bash
   cd deployment/docker
   docker-compose up -d
   ```

3. Access the services:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - n8n Workflows: http://localhost:5678

### Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Update .env with your configuration

# Run the server
python main.py
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## API Documentation

The API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Main API Endpoints

#### Documents
- `GET /api/v1/documents` - List all documents
- `GET /api/v1/documents/{id}` - Get document details
- `DELETE /api/v1/documents/{id}` - Delete a document
- `GET /api/v1/documents/{id}/status` - Get processing status

#### Ingestion
- `POST /api/v1/ingestion/upload` - Upload a document
- `POST /api/v1/ingestion/upload/batch` - Upload multiple documents
- `POST /api/v1/ingestion/validate` - Validate document before upload

#### OCR
- `POST /api/v1/ocr/process/{id}` - Process OCR for a document
- `GET /api/v1/ocr/result/{id}` - Get OCR results
- `POST /api/v1/ocr/reprocess/{id}` - Reprocess OCR

#### Classification
- `POST /api/v1/classification/classify/{id}` - Classify a document
- `GET /api/v1/classification/categories` - Get available categories
- `GET /api/v1/classification/result/{id}` - Get classification results

#### Metadata
- `POST /api/v1/metadata/extract/{id}` - Extract metadata
- `GET /api/v1/metadata/{id}` - Get document metadata
- `PUT /api/v1/metadata/{id}` - Update metadata

#### Search
- `GET /api/v1/search?query={query}` - Search documents
- `POST /api/v1/search/index/{id}` - Index a document
- `GET /api/v1/search/similar/{id}` - Find similar documents
- `GET /api/v1/search/advanced` - Advanced search with filters

#### Storage
- `GET /api/v1/storage/download/{id}` - Download a document
- `GET /api/v1/storage/info/{id}` - Get storage information
- `POST /api/v1/storage/migrate/{id}` - Migrate to different storage
- `DELETE /api/v1/storage/{id}` - Delete from storage

## Database Schema

### Documents Table
- Document metadata and status
- File information
- Upload timestamps

### OCR Results Table
- Extracted text
- Confidence scores
- Processing metrics

### Document Classifications Table
- Categories and subcategories
- Confidence scores
- Tags

### Document Metadata Table
- Key-value metadata pairs
- Extraction confidence
- Source information

### Search Indices Table
- Vector embeddings
- Indexed text
- Search metadata

## Deployment

### Docker Deployment

Use the provided Docker Compose configuration:

```bash
cd deployment/docker
docker-compose up -d
```

### Kubernetes Deployment

Apply the Kubernetes manifests:

```bash
cd deployment/kubernetes

# Create namespace
kubectl apply -f namespace.yaml

# Deploy services
kubectl apply -f postgres-deployment.yaml
kubectl apply -f redis-deployment.yaml
kubectl apply -f elasticsearch-deployment.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
```

## Configuration

### Backend Configuration

Edit `backend/.env` to configure:
- Database connection
- Redis connection
- Storage settings
- API keys for AI models
- CORS origins

### Frontend Configuration

Edit `frontend/.env` to configure:
- API base URL
- Other frontend settings

## Project Structure

```
.
├── backend/
│   ├── agents/
│   │   ├── ingestion/
│   │   ├── ocr/
│   │   ├── classifier/
│   │   ├── metadata/
│   │   ├── storage/
│   │   └── search/
│   ├── api/
│   │   └── endpoints/
│   ├── common/
│   ├── config/
│   ├── database/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── styles/
│   │   └── App.js
│   ├── package.json
│   └── Dockerfile
├── deployment/
│   ├── docker/
│   │   └── docker-compose.yml
│   └── kubernetes/
│       └── *.yaml
├── n8n-workflows/
│   └── document-processing-workflow.json
└── README.md
```

## Features

### Document Ingestion
- Multi-format support (PDF, images, Word, Excel)
- File validation and virus scanning
- Duplicate detection
- Batch upload

### OCR Processing
- Text extraction from images and PDFs
- Multi-page document support
- Confidence scoring
- Multiple OCR engine support

### Document Classification
- ML-based categorization
- Custom category support
- Tag generation
- Confidence scoring

### Metadata Extraction
- Named Entity Recognition (NER)
- Pattern-based extraction
- Custom metadata fields
- Manual metadata editing

### Storage Management
- Multiple storage backends (local, S3, MinIO)
- File integrity verification
- Storage migration
- Compression support

### Search Capabilities
- Full-text search
- Semantic search using vector embeddings
- Similar document finding
- Advanced filtering
- Multi-field search

## Contributing

Please read the contributing guidelines before submitting pull requests.

## License

This project is developed for Kochi Metro Rail Limited (KMRL) as part of Smart India Hackathon 2025.

## Support

For issues and questions, please create an issue in the GitHub repository.
