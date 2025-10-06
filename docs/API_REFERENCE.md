# API Endpoints Reference

## Base URL
`http://localhost:8000/api/v1`

## Documents API

### List Documents
```
GET /documents?skip=0&limit=100
```

### Get Document
```
GET /documents/{document_id}
```

### Delete Document
```
DELETE /documents/{document_id}
```

### Get Document Status
```
GET /documents/{document_id}/status
```

## Ingestion API

### Upload Document
```
POST /ingestion/upload
Content-Type: multipart/form-data

Body: file (binary)
```

### Batch Upload
```
POST /ingestion/upload/batch
Content-Type: multipart/form-data

Body: files[] (multiple files)
```

### Validate Document
```
POST /ingestion/validate
Content-Type: multipart/form-data

Body: file (binary)
```

## OCR API

### Process OCR
```
POST /ocr/process/{document_id}
```

### Get OCR Result
```
GET /ocr/result/{document_id}
```

### Reprocess OCR
```
POST /ocr/reprocess/{document_id}
```

## Classification API

### Classify Document
```
POST /classification/classify/{document_id}
```

### Get Categories
```
GET /classification/categories
```

### Get Classification Result
```
GET /classification/result/{document_id}
```

## Metadata API

### Extract Metadata
```
POST /metadata/extract/{document_id}
```

### Get Metadata
```
GET /metadata/{document_id}
```

### Update Metadata
```
PUT /metadata/{document_id}
Content-Type: application/json

Body: {
  "key1": "value1",
  "key2": "value2"
}
```

## Search API

### Search Documents
```
GET /search?query={search_query}&skip=0&limit=20
```

### Index Document
```
POST /search/index/{document_id}
```

### Find Similar Documents
```
GET /search/similar/{document_id}?limit=10
```

### Advanced Search
```
GET /search/advanced?query={query}&category={category}&date_from={date}&date_to={date}
```

## Storage API

### Download Document
```
GET /storage/download/{document_id}
```

### Get Storage Info
```
GET /storage/info/{document_id}
```

### Migrate Storage
```
POST /storage/migrate/{document_id}
Content-Type: application/json

Body: {
  "target_storage": "s3"
}
```

### Delete from Storage
```
DELETE /storage/{document_id}
```

## Response Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

## Example Usage

### Upload a Document
```bash
curl -X POST "http://localhost:8000/api/v1/ingestion/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

### Search Documents
```bash
curl -X GET "http://localhost:8000/api/v1/search?query=contract"
```

### Get Document Details
```bash
curl -X GET "http://localhost:8000/api/v1/documents/1"
```
