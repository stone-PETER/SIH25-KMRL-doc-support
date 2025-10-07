# n8n Workflows

This directory contains n8n workflow definitions for automating document processing tasks.

## Available Workflows

### Document Processing Workflow
**File:** `document-processing-workflow.json`

This workflow automates the complete document processing pipeline:

1. **Webhook Trigger** - Receives document upload notifications
2. **Upload Document** - Calls the ingestion API to upload the document
3. **Process OCR** - Extracts text from the document
4. **Classify Document** - Categorizes the document
5. **Extract Metadata** - Extracts key metadata fields
6. **Index for Search** - Adds the document to the search index
7. **Respond to Webhook** - Returns the processing result

## How to Use

1. Start the n8n service using Docker Compose:
   ```bash
   docker-compose up n8n
   ```

2. Access n8n at `http://localhost:5678`
   - Username: `admin`
   - Password: `admin`

3. Import the workflow:
   - Go to Workflows → Import from File
   - Select `document-processing-workflow.json`
   - Activate the workflow

4. The webhook will be available at:
   ```
   http://localhost:5678/webhook/document-upload
   ```

## Creating Custom Workflows

You can create custom workflows for:
- Scheduled document processing
- Email-triggered document imports
- Batch processing
- Document archival
- Notification systems
- Integration with third-party systems

## Workflow Best Practices

1. Always include error handling nodes
2. Use Set nodes to transform data between steps
3. Add logging for debugging
4. Test workflows with sample data before production use
5. Keep workflows modular and reusable
