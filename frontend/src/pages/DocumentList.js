import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { documentService } from '../services/api';
import '../styles/DocumentList.css';

function DocumentList() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      setLoading(true);
      const result = await documentService.getDocuments();
      setDocuments(result.documents || []);
    } catch (err) {
      setError(err.message || 'Error loading documents');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading documents...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="document-list">
      <h2>Documents</h2>
      {documents.length === 0 ? (
        <p className="no-documents">No documents found. <Link to="/upload">Upload one now</Link></p>
      ) : (
        <table className="documents-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Filename</th>
              <th>Type</th>
              <th>Status</th>
              <th>Upload Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc) => (
              <tr key={doc.id}>
                <td>{doc.id}</td>
                <td>{doc.original_filename}</td>
                <td>{doc.file_type}</td>
                <td>
                  <span className={`status-badge status-${doc.status}`}>
                    {doc.status}
                  </span>
                </td>
                <td>{new Date(doc.upload_date).toLocaleString()}</td>
                <td>
                  <Link to={`/documents/${doc.id}`} className="btn-link">
                    View
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default DocumentList;
