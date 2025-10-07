# Getting Started Guide

This guide will help you get the Intelligent Document Automation System up and running.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker Desktop** (recommended for quick start)
  - Windows/Mac: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
  - Linux: Install Docker Engine and Docker Compose
  
- **For Local Development:**
  - Python 3.11 or higher
  - Node.js 18 or higher
  - PostgreSQL 15 or higher
  - Redis 7 or higher (optional but recommended)

## Quick Start with Docker (Recommended)

This is the fastest way to get the entire system running.

### Step 1: Clone the Repository

```bash
git clone https://github.com/stone-PETER/SIH25-KMRL-doc-support.git
cd SIH25-KMRL-doc-support
```

### Step 2: Start All Services

```bash
cd deployment/docker
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Elasticsearch (port 9200)
- Backend API (port 8000)
- Frontend React app (port 3000)
- n8n workflow automation (port 5678)

### Step 3: Verify Services

Check that all services are running:

```bash
docker-compose ps
```

You should see all services with status "Up".

### Step 4: Access the Application

Open your browser and navigate to:

- **Frontend Application**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **n8n Workflows**: http://localhost:5678 (login: admin/admin)

### Step 5: Test the System

1. Go to http://localhost:3000/upload
2. Upload a test document (PDF or image)
3. View the document in the Documents list
4. Check the processing status

## Local Development Setup

For development without Docker, follow these steps:

### Backend Setup

#### 1. Set Up Python Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

Update these key settings:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=document_automation
```

#### 3. Set Up Database

Start PostgreSQL and create the database:

```sql
CREATE DATABASE document_automation;
```

#### 4. Run Database Migrations

```bash
# If using Alembic (optional, for production)
alembic upgrade head

# Or let SQLAlchemy create tables automatically
# Tables will be created when you first run the application
```

#### 5. Start the Backend

```bash
python main.py
```

The API will be available at http://localhost:8000

### Frontend Setup

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Configure Environment (Optional)

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

#### 3. Start Development Server

```bash
npm start
```

The frontend will open at http://localhost:3000

## Using the System

### Uploading Documents

1. Navigate to the Upload page
2. Click "Choose File" or drag and drop
3. Select a document (PDF, image, Word, or Excel)
4. Click "Upload"
5. The document will be processed automatically

### Viewing Documents

1. Go to the Documents page
2. Browse the list of uploaded documents
3. Click "View" on any document to see details
4. View OCR results, classification, and metadata

### Searching Documents

1. Go to the Search page
2. Enter your search query
3. Click "Search"
4. Results will show matching documents

### Monitoring with n8n

1. Access n8n at http://localhost:5678
2. Import the workflow from `n8n-workflows/document-processing-workflow.json`
3. Activate the workflow
4. Monitor document processing in real-time

## API Usage Examples

### Upload a Document

```bash
curl -X POST "http://localhost:8000/api/v1/ingestion/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/document.pdf"
```

### Get Document List

```bash
curl -X GET "http://localhost:8000/api/v1/documents"
```

### Search Documents

```bash
curl -X GET "http://localhost:8000/api/v1/search?query=invoice"
```

### Get Document Details

```bash
curl -X GET "http://localhost:8000/api/v1/documents/1"
```

## Troubleshooting

### Backend Won't Start

**Problem:** Database connection error

**Solution:**
1. Check PostgreSQL is running: `pg_isready`
2. Verify database credentials in `.env`
3. Ensure database exists: `psql -l | grep document_automation`

**Problem:** Import errors

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Won't Start

**Problem:** Module not found errors

**Solution:**
1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Clear npm cache: `npm cache clean --force`

**Problem:** Cannot connect to API

**Solution:**
1. Check backend is running at http://localhost:8000
2. Verify CORS settings in backend configuration
3. Check `REACT_APP_API_URL` in frontend `.env`

### Docker Issues

**Problem:** Port already in use

**Solution:**
1. Stop conflicting services
2. Or modify ports in `docker-compose.yml`

**Problem:** Container keeps restarting

**Solution:**
1. Check logs: `docker-compose logs [service-name]`
2. Verify environment variables
3. Check if dependent services are healthy

### Database Issues

**Problem:** Cannot connect to PostgreSQL

**Solution:**
1. Check PostgreSQL is running
2. Verify port (default 5432) is not blocked
3. Check credentials in `.env`

**Problem:** Tables not created

**Solution:**
1. Stop the backend
2. Run: `python -c "from database.models import Base; from database.connection import engine; Base.metadata.create_all(engine)"`
3. Restart the backend

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Configuration Options

### Backend Configuration (.env)

Key configuration options:

```env
# Application
DEBUG=True  # Set to False in production

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=document_automation

# Storage
STORAGE_TYPE=local  # Options: local, s3, minio
STORAGE_PATH=./storage

# OCR
TESSERACT_PATH=/usr/bin/tesseract

# AI Models
HUGGINGFACE_MODEL=sentence-transformers/all-MiniLM-L6-v2
OPENAI_API_KEY=your_api_key_here
```

### Frontend Configuration

Minimal configuration required. Create `.env` in frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## Next Steps

After getting the system running:

1. **Review the Architecture**: Read `docs/ARCHITECTURE.md` to understand system design
2. **Explore the API**: Visit http://localhost:8000/docs for interactive API documentation
3. **Customize Agents**: Modify agent services in `backend/agents/` to fit your needs
4. **Set Up Workflows**: Create custom n8n workflows for automation
5. **Deploy to Production**: Follow `docs/DEPLOYMENT.md` for production deployment

## Common Tasks

### Adding New Document Types

1. Update `ALLOWED_EXTENSIONS` in `backend/agents/ingestion/service.py`
2. Add new `DocumentType` enum in `backend/database/models.py`
3. Update file validation logic

### Customizing Classification

1. Edit categories in `backend/agents/classifier/service.py`
2. Train custom ML models
3. Update `_simulate_classification` method with your model

### Adding New Metadata Fields

1. Update extraction patterns in `backend/agents/metadata/service.py`
2. Add new metadata keys
3. Update UI to display new fields

### Integrating External Storage

1. Install storage client library (boto3 for S3)
2. Update `backend/agents/storage/service.py`
3. Add configuration in `.env`

## Support and Resources

- **Documentation**: Check the `docs/` directory
- **API Reference**: http://localhost:8000/docs
- **Issues**: Create issues on GitHub
- **Community**: Join project discussions

## Development Tips

1. **Code Formatting**: Use `black` for Python, `prettier` for JavaScript
2. **Linting**: Run `flake8` for Python, `eslint` for JavaScript
3. **Git Hooks**: Set up pre-commit hooks for code quality
4. **Testing**: Write tests for new features
5. **Documentation**: Update docs when adding features

## Environment-Specific Notes

### Windows

- Use Git Bash or PowerShell for commands
- Path separators use backslashes: `venv\Scripts\activate`
- Install Tesseract OCR separately if needed

### macOS

- Install Homebrew first: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- Install PostgreSQL: `brew install postgresql`
- Install Tesseract: `brew install tesseract`

### Linux

- Use package manager: `sudo apt-get install postgresql redis-server`
- Install Tesseract: `sudo apt-get install tesseract-ocr`
- May need to install additional dependencies

## Production Deployment Checklist

Before deploying to production:

- [ ] Change all default passwords
- [ ] Set `DEBUG=False` in backend
- [ ] Configure SSL/TLS certificates
- [ ] Set up database backups
- [ ] Configure monitoring and alerts
- [ ] Set resource limits
- [ ] Enable authentication
- [ ] Set up logging
- [ ] Configure firewall rules
- [ ] Test disaster recovery plan

## Performance Optimization

For better performance:

1. **Enable Redis caching**
2. **Use connection pooling**
3. **Optimize database queries**
4. **Implement CDN for frontend**
5. **Use Elasticsearch for search**
6. **Enable gzip compression**
7. **Implement rate limiting**

Congratulations! You now have the Intelligent Document Automation System running. Explore the features and customize it to your needs.
