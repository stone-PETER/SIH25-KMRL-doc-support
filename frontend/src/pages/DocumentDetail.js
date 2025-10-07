import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { documentService, ocrService, classificationService, metadataService } from '../services/api';
import '../styles/DocumentDetail.css';

function DocumentDetail() {
  const { id } = useParams();
  const [document, setDocument] = useState(null);
  const [ocr, setOcr] = useState(null);
  const [classification, setClassification] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDocumentDetails();
  }, [id]);

  const loadDocumentDetails = async () => {
    try {
      setLoading(true);
      const docResult = await documentService.getDocument(id);
      setDocument(docResult);

      // Load additional details
      try {
        const ocrResult = await ocrService.getOCRResult(id);
        setOcr(ocrResult);
      } catch (err) {
        console.log('OCR results not available');
      }

      try {
        const classResult = await classificationService.getClassification(id);
        setClassification(classResult);
      } catch (err) {
        console.log('Classification not available');
      }

      try {
        const metaResult = await metadataService.getMetadata(id);
        setMetadata(metaResult);
      } catch (err) {
        console.log('Metadata not available');
      }
    } catch (err) {
      setError(err.message || 'Error loading document details');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading document details...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!document) {
    return <div className="error-message">Document not found</div>;
  }

  return (
    <div className="document-detail">
      <h2>Document Details</h2>
      
      <div className="detail-section">
        <h3>Basic Information</h3>
        <dl>
          <dt>ID:</dt>
          <dd>{document.id}</dd>
          <dt>Filename:</dt>
          <dd>{document.original_filename}</dd>
          <dt>File Type:</dt>
          <dd>{document.file_type}</dd>
          <dt>File Size:</dt>
          <dd>{document.file_size} bytes</dd>
          <dt>Status:</dt>
          <dd>
            <span className={`status-badge status-${document.status}`}>
              {document.status}
            </span>
          </dd>
          <dt>Upload Date:</dt>
          <dd>{new Date(document.upload_date).toLocaleString()}</dd>
        </dl>
      </div>

      {classification && (
        <div className="detail-section">
          <h3>Classification</h3>
          <dl>
            <dt>Category:</dt>
            <dd>{classification.category}</dd>
            <dt>Subcategory:</dt>
            <dd>{classification.subcategory}</dd>
            <dt>Confidence:</dt>
            <dd>{classification.confidence}%</dd>
            <dt>Tags:</dt>
            <dd>{classification.tags?.join(', ')}</dd>
          </dl>
        </div>
      )}

      {metadata && (
        <div className="detail-section">
          <h3>Metadata</h3>
          <dl>
            {Object.entries(metadata.metadata || {}).map(([key, value]) => (
              <React.Fragment key={key}>
                <dt>{key}:</dt>
                <dd>{JSON.stringify(value.value)}</dd>
              </React.Fragment>
            ))}
          </dl>
        </div>
      )}

      {ocr && (
        <div className="detail-section">
          <h3>Extracted Text</h3>
          <div className="ocr-text">
            {ocr.results?.map((result, idx) => (
              <div key={idx}>
                <h4>Page {result.page}</h4>
                <p>{result.text}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default DocumentDetail;
