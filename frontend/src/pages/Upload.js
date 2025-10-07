import React, { useState } from 'react';
import { ingestionService } from '../services/api';
import '../styles/Upload.css';

function Upload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
    setError('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    setError('');
    setMessage('');

    try {
      const result = await ingestionService.uploadDocument(file);
      setMessage(`Document uploaded successfully! ID: ${result.document_id}`);
      setFile(null);
      e.target.reset();
    } catch (err) {
      setError(err.message || 'Error uploading document');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload">
      <h2>Upload Document</h2>
      <form onSubmit={handleUpload} className="upload-form">
        <div className="form-group">
          <label htmlFor="file">Select Document:</label>
          <input
            type="file"
            id="file"
            onChange={handleFileChange}
            accept=".pdf,.jpg,.jpeg,.png,.tiff,.doc,.docx,.xls,.xlsx"
            disabled={uploading}
          />
        </div>
        <button type="submit" disabled={uploading || !file} className="btn-primary">
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
      {message && <div className="success-message">{message}</div>}
      {error && <div className="error-message">{error}</div>}
      <div className="upload-info">
        <h3>Supported Formats:</h3>
        <ul>
          <li>PDF (.pdf)</li>
          <li>Images (.jpg, .jpeg, .png, .tiff)</li>
          <li>Word Documents (.doc, .docx)</li>
          <li>Excel Spreadsheets (.xls, .xlsx)</li>
        </ul>
        <p>Maximum file size: 50MB</p>
      </div>
    </div>
  );
}

export default Upload;
