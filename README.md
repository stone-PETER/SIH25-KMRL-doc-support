# SIH25-KMRL-doc-support
Document Overload at Kochi Metro Rail Limited (KMRL) - An automated solution

## Intelligent Document Automation System

A comprehensive AI-powered document processing system designed to automate document management workflows for KMRL. This full-stack solution includes document ingestion, OCR, classification, metadata extraction, storage management, and semantic search capabilities.

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/stone-PETER/SIH25-KMRL-doc-support.git
cd SIH25-KMRL-doc-support

# Start all services
cd deployment/docker
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# n8n: http://localhost:5678
```

## 📋 Features

### Core Capabilities
- **Document Ingestion**: Upload PDFs, images, Word, and Excel files
- **OCR Processing**: Automatic text extraction from images and scanned documents
- **AI Classification**: Intelligent document categorization using ML models
- **Metadata Extraction**: Automatic extraction of key information (dates, emails, etc.)
- **Storage Management**: Flexible storage with local, S3, and MinIO support
- **Semantic Search**: Advanced search using vector embeddings and full-text search

### Technology Stack
- **Backend**: FastAPI (Python) with modular microservices architecture
- **Frontend**: React with modern UI components
- **Database**: PostgreSQL for structured data
- **Cache**: Redis for performance optimization
- **Search**: Elasticsearch for advanced search capabilities
- **Workflow**: n8n for automation and integration

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                     │
│              Dashboard, Upload, Search UI                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Backend API (FastAPI)                   │
│                  REST API with OpenAPI                   │
└─┬───────────────┬─────────────┬──────────────┬─────────┘
  │               │             │              │
  ▼               ▼             ▼              ▼
┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│Ingestion│  │   OCR    │  │Classifier│  │ Metadata │
│ Agent  │  │  Agent   │  │  Agent   │  │  Agent   │
└────────┘  └──────────┘  └──────────┘  └──────────┘
     │            │              │              │
     └────────────┴──────────────┴──────────────┘
                     │
            ┌────────┴─────────┐
            ▼                  ▼
      ┌──────────┐      ┌──────────┐
      │ Storage  │      │  Search  │
      │  Agent   │      │  Agent   │
      └──────────┘      └──────────┘
            │                  │
     ┌──────┴──────┐    ┌─────┴──────┐
     ▼             ▼    ▼            ▼
┌──────────┐  ┌──────┐ ┌──────┐ ┌──────────┐
│PostgreSQL│  │Redis │ │ S3/  │ │Elastic-  │
│          │  │      │ │MinIO │ │search    │
└──────────┘  └──────┘ └──────┘ └──────────┘
```

## 📁 Project Structure

```
.
├── backend/                    # FastAPI backend
│   ├── agents/                # AI agent microservices
│   │   ├── ingestion/        # Document ingestion agent
│   │   ├── ocr/              # OCR processing agent
│   │   ├── classifier/       # Document classification agent
│   │   ├── metadata/         # Metadata extraction agent
│   │   ├── storage/          # Storage management agent
│   │   └── search/           # Search agent
│   ├── api/                  # API routes and endpoints
│   ├── database/             # Database models and connection
│   ├── config/               # Configuration settings
│   └── main.py              # Application entry point
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service layer
│   │   └── styles/         # CSS stylesheets
│   └── package.json
├── deployment/              # Deployment configurations
│   ├── docker/             # Docker Compose setup
│   └── kubernetes/         # Kubernetes manifests
├── n8n-workflows/          # Workflow automation
└── docs/                   # Documentation

```

## 🔧 Local Development

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run the server
python main.py
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 📚 API Documentation

Once the backend is running, access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🚢 Deployment

### Docker Deployment
```bash
cd deployment/docker
docker-compose up -d
```

### Kubernetes Deployment
```bash
cd deployment/kubernetes
kubectl apply -f namespace.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f redis-deployment.yaml
kubectl apply -f elasticsearch-deployment.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
```

## 📖 Documentation

Detailed documentation is available in the [docs](./docs) directory:
- Architecture overview
- API reference
- Deployment guides
- Configuration options

## 🤝 Contributing

This project is developed for Kochi Metro Rail Limited (KMRL) as part of Smart India Hackathon 2025.

## 📝 License

Copyright © 2025 KMRL Document Automation Team

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation in the `docs/` directory
