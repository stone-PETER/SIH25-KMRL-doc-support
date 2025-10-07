import React, { useState } from 'react';
import { searchService } from '../services/api';
import { Link } from 'react-router-dom';
import '../styles/Search.css';

function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    setSearching(true);
    setError('');
    
    try {
      const result = await searchService.search(query);
      setResults(result.results || []);
    } catch (err) {
      setError(err.message || 'Error searching documents');
    } finally {
      setSearching(false);
    }
  };

  return (
    <div className="search">
      <h2>Search Documents</h2>
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter search query..."
          className="search-input"
          disabled={searching}
        />
        <button type="submit" disabled={searching} className="btn-primary">
          {searching ? 'Searching...' : 'Search'}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}

      {results.length > 0 && (
        <div className="search-results">
          <h3>Search Results ({results.length})</h3>
          <div className="results-list">
            {results.map((doc) => (
              <div key={doc.id} className="result-item">
                <h4>{doc.filename}</h4>
                <p>Status: {doc.status}</p>
                <p>Upload Date: {new Date(doc.upload_date).toLocaleString()}</p>
                <Link to={`/documents/${doc.id}`} className="btn-link">
                  View Details
                </Link>
              </div>
            ))}
          </div>
        </div>
      )}

      {!searching && query && results.length === 0 && !error && (
        <div className="no-results">No documents found matching your query</div>
      )}
    </div>
  );
}

export default Search;
