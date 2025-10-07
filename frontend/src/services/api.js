import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Document Service
export const documentService = {
  getDocuments: async (skip = 0, limit = 100) => {
    const response = await api.get(`/documents?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getDocument: async (id) => {
    const response = await api.get(`/documents/${id}`);
    return response.data;
  },

  deleteDocument: async (id) => {
    const response = await api.delete(`/documents/${id}`);
    return response.data;
  },

  getDocumentStatus: async (id) => {
    const response = await api.get(`/documents/${id}/status`);
    return response.data;
  },
};

// Ingestion Service
export const ingestionService = {
  uploadDocument: async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/ingestion/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  uploadBatch: async (files) => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    const response = await api.post('/ingestion/upload/batch', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  validateDocument: async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/ingestion/validate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

// OCR Service
export const ocrService = {
  processOCR: async (documentId) => {
    const response = await api.post(`/ocr/process/${documentId}`);
    return response.data;
  },

  getOCRResult: async (documentId) => {
    const response = await api.get(`/ocr/result/${documentId}`);
    return response.data;
  },

  reprocessOCR: async (documentId) => {
    const response = await api.post(`/ocr/reprocess/${documentId}`);
    return response.data;
  },
};

// Classification Service
export const classificationService = {
  classifyDocument: async (documentId) => {
    const response = await api.post(`/classification/classify/${documentId}`);
    return response.data;
  },

  getCategories: async () => {
    const response = await api.get('/classification/categories');
    return response.data;
  },

  getClassification: async (documentId) => {
    const response = await api.get(`/classification/result/${documentId}`);
    return response.data;
  },
};

// Metadata Service
export const metadataService = {
  extractMetadata: async (documentId) => {
    const response = await api.post(`/metadata/extract/${documentId}`);
    return response.data;
  },

  getMetadata: async (documentId) => {
    const response = await api.get(`/metadata/${documentId}`);
    return response.data;
  },

  updateMetadata: async (documentId, metadata) => {
    const response = await api.put(`/metadata/${documentId}`, metadata);
    return response.data;
  },
};

// Search Service
export const searchService = {
  search: async (query, skip = 0, limit = 20) => {
    const response = await api.get(`/search?query=${encodeURIComponent(query)}&skip=${skip}&limit=${limit}`);
    return response.data;
  },

  indexDocument: async (documentId) => {
    const response = await api.post(`/search/index/${documentId}`);
    return response.data;
  },

  findSimilar: async (documentId, limit = 10) => {
    const response = await api.get(`/search/similar/${documentId}?limit=${limit}`);
    return response.data;
  },

  advancedSearch: async (params) => {
    const queryParams = new URLSearchParams(params).toString();
    const response = await api.get(`/search/advanced?${queryParams}`);
    return response.data;
  },
};

// Storage Service
export const storageService = {
  downloadDocument: async (documentId) => {
    const response = await api.get(`/storage/download/${documentId}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  getStorageInfo: async (documentId) => {
    const response = await api.get(`/storage/info/${documentId}`);
    return response.data;
  },

  migrateStorage: async (documentId, targetStorage) => {
    const response = await api.post(`/storage/migrate/${documentId}`, {
      target_storage: targetStorage,
    });
    return response.data;
  },

  deleteFromStorage: async (documentId) => {
    const response = await api.delete(`/storage/${documentId}`);
    return response.data;
  },
};

export default api;
