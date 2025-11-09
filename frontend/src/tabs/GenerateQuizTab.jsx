// src/tabs/GenerateQuizTab.jsx
import React, { useState } from 'react';
import api from '../services/api';
import QuizDisplay from '../components/QuizDisplay';

const GenerateQuizTab = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [quizData, setQuizData] = useState(null);
  const [urlError, setUrlError] = useState('');

  // Validate Wikipedia URL
  const validateUrl = (url) => {
    const wikipediaPattern = /^https?:\/\/(en\.)?wikipedia\.org\/wiki\/.+/;
    return wikipediaPattern.test(url);
  };

  // Handle URL input change
  const handleUrlChange = (e) => {
    const value = e.target.value;
    setUrl(value);
    
    // Clear errors when user starts typing
    if (urlError) setUrlError('');
    if (error) setError(null);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Reset states
    setError(null);
    setUrlError('');
    setQuizData(null);

    // Validate URL
    if (!url.trim()) {
      setUrlError('Please enter a Wikipedia URL');
      return;
    }

    if (!validateUrl(url.trim())) {
      setUrlError('Please enter a valid Wikipedia article URL (e.g., https://en.wikipedia.org/wiki/Alan_Turing)');
      return;
    }

    // Generate quiz
    setLoading(true);

    try {
      const result = await api.generateQuiz(url.trim());

      if (result.success) {
        setQuizData(result.data);
        setError(null);
      } else {
        setError(result.error);
        setQuizData(null);
      }
    } catch (err) {
      setError('An unexpected error occurred. Please try again.');
      setQuizData(null);
    } finally {
      setLoading(false);
    }
  };

  // Handle example URL click
  const handleExampleClick = (exampleUrl) => {
    setUrl(exampleUrl);
    setUrlError('');
    setError(null);
  };

  return (
    <div className="generate-quiz-tab">
      {/* Input Form Card */}
      <div className="card">
        <h2 className="card-title">🎯 Generate Quiz from Wikipedia</h2>
        <p className="card-subtitle" style={{ marginBottom: '20px' }}>
          Enter a Wikipedia article URL to generate an AI-powered educational quiz
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="wikipedia-url" className="form-label">
              Wikipedia Article URL
            </label>
            <input
              id="wikipedia-url"
              type="text"
              className={`form-input ${urlError ? 'error' : ''}`}
              value={url}
              onChange={handleUrlChange}
              placeholder="https://en.wikipedia.org/wiki/Alan_Turing"
              disabled={loading}
            />
            {urlError && <p className="form-error">{urlError}</p>}
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }}></span>
                Generating Quiz...
              </>
            ) : (
              <>
                🚀 Generate Quiz
              </>
            )}
          </button>
        </form>

        {/* Example URLs */}
        <div className="mt-20">
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '10px' }}>
            <strong>Try these examples:</strong>
          </p>
          <div className="flex gap-10" style={{ flexWrap: 'wrap' }}>
            <button
              onClick={() => handleExampleClick('https://en.wikipedia.org/wiki/Alan_Turing')}
              className="btn btn-secondary btn-small"
              disabled={loading}
            >
              Alan Turing
            </button>
            <button
              onClick={() => handleExampleClick('https://en.wikipedia.org/wiki/Artificial_intelligence')}
              className="btn btn-secondary btn-small"
              disabled={loading}
            >
              Artificial Intelligence
            </button>
            <button
              onClick={() => handleExampleClick('https://en.wikipedia.org/wiki/World_War_II')}
              className="btn btn-secondary btn-small"
              disabled={loading}
            >
              World War II
            </button>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="card loading-container">
          <div className="spinner"></div>
          <p className="loading-text">
            🤖 AI is analyzing the Wikipedia article and generating your quiz...
          </p>
          <p style={{ marginTop: '10px', fontSize: '0.9rem', color: 'var(--text-light)' }}>
            This may take 30-60 seconds
          </p>
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

      {/* Success State - Display Quiz */}
      {quizData && !loading && (
        <>
          <div className="alert alert-success">
            <span style={{ fontSize: '1.5rem' }}>✅</span>
            <div>
              <strong>Success!</strong> Quiz generated successfully! Scroll down to view.
            </div>
          </div>
          <QuizDisplay quizData={quizData} />
        </>
      )}
    </div>
  );
};

export default GenerateQuizTab;