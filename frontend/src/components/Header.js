import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-container">
        <h1 className="header-title">KMRL Document Automation</h1>
        <nav className="nav">
          <Link to="/" className="nav-link">Dashboard</Link>
          <Link to="/upload" className="nav-link">Upload</Link>
          <Link to="/documents" className="nav-link">Documents</Link>
          <Link to="/search" className="nav-link">Search</Link>
        </nav>
      </div>
    </header>
  );
}

export default Header;
