// src/App.jsx
import React, { useState } from 'react';
import GenerateQuizTab from './tabs/GenerateQuizTab';
import HistoryTab from './tabs/HistoryTab';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState('generate');

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <h1>🧠 AI Wiki Quiz Generator</h1>
        <p>Transform Wikipedia articles into engaging educational quizzes using AI</p>
      </header>

      {/* Tab Navigation */}
      <div className="tab-container">
        <nav className="tab-nav">
          <button
            className={`tab-button ${activeTab === 'generate' ? 'active' : ''}`}
            onClick={() => setActiveTab('generate')}
          >
            🎯 Generate Quiz
          </button>
          <button
            className={`tab-button ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            📚 Quiz History
          </button>
        </nav>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'generate' && <GenerateQuizTab />}
          {activeTab === 'history' && <HistoryTab />}
        </div>
      </div>

      {/* Footer */}
      <footer style={{ 
        textAlign: 'center', 
        marginTop: '40px', 
        padding: '20px',
        color: 'var(--text-secondary)',
        fontSize: '0.9rem'
      }}>
        <p>Powered by FastAPI + React + Gemini AI</p>
      </footer>
    </div>
  );
}

export default App;