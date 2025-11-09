// src/components/HistoryTable.jsx
import React from 'react';

const HistoryTable = ({ history, onViewDetails, onDelete }) => {
  if (!history || history.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📚</div>
        <h3 className="empty-state-title">No Quiz History</h3>
        <p className="empty-state-text">
          Generate your first quiz to see it here!
        </p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const truncateUrl = (url, maxLength = 50) => {
    if (url.length <= maxLength) return url;
    return url.substring(0, maxLength) + '...';
  };

  return (
    <div className="table-container">
      <table className="table">
        <thead>
          <tr>
            
            <th>Title</th>
            <th>Wikipedia URL</th>
            <th style={{ width: '200px' }}>Date Generated</th>
            <th style={{ width: '200px' }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {history.map((item) => (
            <tr key={item.id}>
              
              <td>
                <strong style={{ color: 'var(--text-primary)' }}>
                  {item.title}
                </strong>
              </td>
              <td>
                <a
                  href={item.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: 'var(--primary-color)' }}
                  title={item.url}
                >
                  {truncateUrl(item.url)}
                </a>
              </td>
              <td>{formatDate(item.date_generated)}</td>
              <td>
                <div className="flex gap-10">
                  <button
                    onClick={() => onViewDetails(item.id)}
                    className="btn btn-primary btn-small"
                  >
                    📖 Details
                  </button>
                  {onDelete && (
                    <button
                      onClick={() => onDelete(item.id)}
                      className="btn btn-danger btn-small"
                    >
                      🗑️
                    </button>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default HistoryTable;