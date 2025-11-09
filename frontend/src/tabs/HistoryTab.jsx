// src/tabs/HistoryTab.jsx
import React, { useState, useEffect, useMemo } from 'react';
import api from '../services/api';
import HistoryTable from '../components/HistoryTable';
import Modal from '../components/Modal';
import QuizDisplay from '../components/QuizDisplay';

const HistoryTab = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [loadingQuiz, setLoadingQuiz] = useState(false);

  // Search and Filter States
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('date_desc');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');

  // Fetch history on component mount
  useEffect(() => {
    fetchHistory();
  }, []);

  // Fetch quiz history
  const fetchHistory = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await api.getHistory();

      if (result.success) {
        setHistory(result.data);
        setError(null);
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Failed to fetch quiz history. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Filter and Sort Logic with useMemo for performance
  const filteredAndSortedHistory = useMemo(() => {
    let filtered = [...history];

    // Search filter (by title or URL)
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(item =>
        item.title.toLowerCase().includes(query) ||
        item.url.toLowerCase().includes(query)
      );
    }

    // Date range filter - From date
    if (dateFrom) {
      filtered = filtered.filter(item =>
        new Date(item.date_generated) >= new Date(dateFrom)
      );
    }

    // Date range filter - To date
    if (dateTo) {
      const endDate = new Date(dateTo);
      endDate.setHours(23, 59, 59, 999); // Include the entire day
      filtered = filtered.filter(item =>
        new Date(item.date_generated) <= endDate
      );
    }

    // Sorting
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'date_desc':
          return new Date(b.date_generated) - new Date(a.date_generated);
        case 'date_asc':
          return new Date(a.date_generated) - new Date(b.date_generated);
        case 'title_asc':
          return a.title.localeCompare(b.title);
        case 'title_desc':
          return b.title.localeCompare(a.title);
        default:
          return 0;
      }
    });

    return filtered;
  }, [history, searchQuery, sortBy, dateFrom, dateTo]);

  // Handle view details
  const handleViewDetails = async (quizId) => {
    setLoadingQuiz(true);
    setModalOpen(true);
    setSelectedQuiz(null);

    try {
      const result = await api.getQuizById(quizId);

      if (result.success) {
        setSelectedQuiz(result.data);
      } else {
        setError(result.error);
        setModalOpen(false);
      }
    } catch (err) {
      setError('Failed to fetch quiz details. Please try again.');
      setModalOpen(false);
    } finally {
      setLoadingQuiz(false);
    }
  };

  // Handle delete quiz
  const handleDelete = async (quizId) => {
    if (!window.confirm('Are you sure you want to delete this quiz?')) {
      return;
    }

    try {
      const result = await api.deleteQuiz(quizId);

      if (result.success) {
        // Refresh history after deletion
        await fetchHistory();
        // Show success message
        alert('Quiz deleted successfully!');
      } else {
        alert(`Failed to delete quiz: ${result.error}`);
      }
    } catch (err) {
      alert('An error occurred while deleting the quiz.');
    }
  };

  // Close modal
  const handleCloseModal = () => {
    setModalOpen(false);
    setSelectedQuiz(null);
  };

  // Clear all filters
  const handleClearFilters = () => {
    setSearchQuery('');
    setSortBy('date_desc');
    setDateFrom('');
    setDateTo('');
  };

  // Check if any filters are active
  const hasActiveFilters = searchQuery || dateFrom || dateTo || sortBy !== 'date_desc';

  return (
    <div className="history-tab">
      {/* Header with Search/Filter */}
      <div className="card">
        <div className="flex-between" style={{ marginBottom: '20px' }}>
          <div>
            <h2 className="card-title">📚 Quiz History</h2>
            <p className="card-subtitle">
              View and manage all previously generated quizzes
            </p>
          </div>
          <button
            onClick={fetchHistory}
            className="btn btn-secondary"
            disabled={loading}
          >
            🔄 Refresh
          </button>
        </div>

        {/* Search and Filter Section */}
        <div className="search-filter-container">
          {/* Search Input */}
          <div className="filter-item filter-item-full">
            <label htmlFor="search" className="form-label">
              🔍 Search
            </label>
            <input
              id="search"
              type="text"
              className="form-input"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by title or URL..."
            />
          </div>

          {/* Date From */}
          <div className="filter-item">
            <label htmlFor="date-from" className="form-label">
              📅 From Date
            </label>
            <input
              id="date-from"
              type="date"
              className="form-input"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
            />
          </div>

          {/* Date To */}
          <div className="filter-item">
            <label htmlFor="date-to" className="form-label">
              📅 To Date
            </label>
            <input
              id="date-to"
              type="date"
              className="form-input"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
            />
          </div>

          {/* Sort By */}
          <div className="filter-item">
            <label htmlFor="sort-by" className="form-label">
              🔀 Sort By
            </label>
            <select
              id="sort-by"
              className="form-input"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="date_desc">Date (Newest First)</option>
              <option value="date_asc">Date (Oldest First)</option>
              <option value="title_asc">Title (A-Z)</option>
              <option value="title_desc">Title (Z-A)</option>
            </select>
          </div>
        </div>

        {/* Active Filters Indicator */}
        {hasActiveFilters && (
          <div className="alert alert-info" style={{ marginTop: '15px' }}>
            <span style={{ fontSize: '1.2rem' }}>🔍</span>
            <div style={{ flex: 1 }}>
              <strong>Filters Active:</strong> Showing {filteredAndSortedHistory.length} of {history.length} quizzes
            </div>
            <button
              onClick={handleClearFilters}
              className="btn btn-small btn-secondary"
            >
              ✖ Clear Filters
            </button>
          </div>
        )}
      </div>

      {/* Loading State */}
      {loading && (
        <div className="card loading-container">
          <div className="spinner"></div>
          <p className="loading-text">Loading quiz history...</p>
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="alert alert-error">
          <span style={{ fontSize: '1.5rem' }}>⚠️</span>
          <div>
            <strong>Error:</strong> {error}
          </div>
        </div>
      )}

      {/* History Table */}
      {!loading && !error && (
        <>
          {filteredAndSortedHistory.length > 0 && (
            <div className="card" style={{ padding: '0' }}>
              <HistoryTable
                history={filteredAndSortedHistory}
                onViewDetails={handleViewDetails}
                onDelete={handleDelete}
              />
            </div>
          )}

          {filteredAndSortedHistory.length === 0 && (
            <div className="card">
              <div className="empty-state">
                <div className="empty-state-icon">
                  {history.length === 0 ? '📚' : '🔍'}
                </div>
                <h3 className="empty-state-title">
                  {history.length === 0 ? 'No Quiz History' : 'No Results Found'}
                </h3>
                <p className="empty-state-text">
                  {history.length === 0 
                    ? 'Generate your first quiz to see it here!'
                    : 'Try adjusting your search or filters'
                  }
                </p>
                {hasActiveFilters && (
                  <button
                    onClick={handleClearFilters}
                    className="btn btn-primary"
                    style={{ marginTop: '15px' }}
                  >
                    Clear All Filters
                  </button>
                )}
              </div>
            </div>
          )}
        </>
      )}

      {/* Quiz Details Modal */}
      <Modal
        isOpen={modalOpen}
        onClose={handleCloseModal}
        title={selectedQuiz ? selectedQuiz.title : 'Quiz Details'}
      >
        {loadingQuiz ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p className="loading-text">Loading quiz details...</p>
          </div>
        ) : selectedQuiz ? (
          <QuizDisplay quizData={selectedQuiz} />
        ) : (
          <div className="empty-state">
            <p>Failed to load quiz details</p>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default HistoryTab;