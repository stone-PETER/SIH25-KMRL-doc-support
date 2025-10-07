import React, { useState, useEffect } from 'react';
import { documentService } from '../services/api';
import '../styles/Dashboard.css';

function Dashboard() {
  const [stats, setStats] = useState({
    total: 0,
    processing: 0,
    completed: 0,
    failed: 0
  });

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      // Placeholder: In production, call actual stats endpoint
      setStats({
        total: 0,
        processing: 0,
        completed: 0,
        failed: 0
      });
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Documents</h3>
          <p className="stat-value">{stats.total}</p>
        </div>
        <div className="stat-card">
          <h3>Processing</h3>
          <p className="stat-value">{stats.processing}</p>
        </div>
        <div className="stat-card">
          <h3>Completed</h3>
          <p className="stat-value">{stats.completed}</p>
        </div>
        <div className="stat-card">
          <h3>Failed</h3>
          <p className="stat-value">{stats.failed}</p>
        </div>
      </div>
      <div className="dashboard-info">
        <p>Welcome to the Intelligent Document Automation System</p>
        <p>Upload documents to automatically extract text, classify, and manage metadata</p>
      </div>
    </div>
  );
}

export default Dashboard;
