
// src/components/QuizDisplay.jsx
import React, { useState, useEffect } from 'react';
import CollapsibleSection from './CollapsibleSection';

const QuizDisplay = ({ quizData }) => {
  const [quizMode, setQuizMode] = useState('view'); // 'view' or 'take'
  const [userAnswers, setUserAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0); // NEW: Current question index

  if (!quizData) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📝</div>
        <h3 className="empty-state-title">No Quiz Data</h3>
        <p className="empty-state-text">Unable to display quiz information</p>
      </div>
    );
  }

  const {
    title,
    summary,
    key_entities,
    sections,
    quiz,
    related_topics,
    date_generated,
    url,
  } = quizData;

  // NEW: Keyboard navigation
  useEffect(() => {
    const handleKeyPress = (e) => {
      if (quizMode === 'take' || (quizMode === 'take' && showResults)) {
        if (e.key === 'ArrowLeft') {
          handlePrevQuestion();
        } else if (e.key === 'ArrowRight') {
          handleNextQuestion();
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [currentQuestionIndex, quiz.length, quizMode]);

  // NEW: Navigation handlers
  const handleNextQuestion = () => {
    if (currentQuestionIndex < quiz.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handlePrevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleGoToQuestion = (index) => {
    setCurrentQuestionIndex(index);
  };

  // Handle answer selection
  const handleAnswerSelect = (questionIndex, selectedOption) => {
    if (showResults) return;
    
    setUserAnswers({
      ...userAnswers,
      [questionIndex]: selectedOption
    });

    // Auto-advance to next question after selection
    if (questionIndex < quiz.length - 1 && !showResults) {
      setTimeout(() => {
        setCurrentQuestionIndex(questionIndex + 1);
      }, 300);
    }
  };

  // Handle quiz submission
  const handleSubmitQuiz = () => {
    setShowResults(true);
    setCurrentQuestionIndex(0);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Reset quiz
  const handleResetQuiz = () => {
    setUserAnswers({});
    setShowResults(false);
    setCurrentQuestionIndex(0);
    setQuizMode('take');
  };

  // Calculate score
  const calculateScore = () => {
    let correct = 0;
    quiz.forEach((question, index) => {
      if (userAnswers[index] === question.answer) {
        correct++;
      }
    });
    return correct;
  };

  // Toggle between view and take mode
  const toggleQuizMode = () => {
    if (quizMode === 'view') {
      setQuizMode('take');
      setUserAnswers({});
      setShowResults(false);
      setCurrentQuestionIndex(0);
    } else {
      setQuizMode('view');
      setUserAnswers({});
      setShowResults(false);
      setCurrentQuestionIndex(0);
    }
  };

  // NEW: Determine if we should show all questions or just current one
  const showAllQuestions = quizMode === 'view';

  return (
    <div className="quiz-display">
      {/* Header Card */}
      <div className="card quiz-header-card">
        <div className="quiz-header-info">
          <h2 className="quiz-main-title">{title}</h2>
          {date_generated && (
            <p className="quiz-date">
              Generated: {new Date(date_generated).toLocaleString()}
            </p>
          )}
          {url && (
            <a 
              href={url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="quiz-source-link"
            >
              🔗 View Wikipedia Article
            </a>
          )}
        </div>

        {/* Quiz Mode Toggle */}
        <div className="quiz-mode-controls">
          <button
            onClick={toggleQuizMode}
            className={`btn ${quizMode === 'take' ? 'btn-primary' : 'btn-secondary'}`}
          >
            {quizMode === 'view' ? '🎮 Take Quiz Mode' : '👁️ View All Answers'}
          </button>
          
          {quizMode === 'take' && showResults && (
            <button
              onClick={handleResetQuiz}
              className="btn btn-secondary"
            >
              🔄 Retake Quiz
            </button>
          )}
        </div>
      </div>

      {/* Score Display (Take Quiz Mode - After Submission) */}
      {quizMode === 'take' && showResults && (
        <div className="score-card">
          <h2 className="score-title">🎉 Quiz Complete!</h2>
          <div className="score-display">
            {calculateScore()} / {quiz.length}
          </div>
          <p className="score-message">
            {calculateScore() === quiz.length ? 'Perfect Score! 🌟' :
             calculateScore() >= quiz.length * 0.7 ? 'Great Job! 👏' :
             calculateScore() >= quiz.length * 0.5 ? 'Good Effort! 💪' :
             'Keep Learning! 📚'}
          </p>
          <p className="score-percentage">
            Score: {Math.round((calculateScore() / quiz.length) * 100)}%
          </p>
        </div>
      )}

      {/* Collapsible Sections */}

      {/* Summary Section */}
      {summary && (
        <CollapsibleSection title="Summary" icon="📄" defaultOpen={true}>
          <p className="summary-text">{summary}</p>
        </CollapsibleSection>
      )}

      {/* Key Entities Section */}
      {key_entities && (
        <CollapsibleSection title="Key Entities" icon="🏷️" defaultOpen={false}>
          {key_entities.people && key_entities.people.length > 0 && (
            <div className="entity-group">
              <h4 className="entity-group-title">👥 People</h4>
              <div className="entity-list">
                {key_entities.people.map((person, index) => (
                  <span key={index} className="entity-item entity-people">
                    {person}
                  </span>
                ))}
              </div>
            </div>
          )}

          {key_entities.organizations && key_entities.organizations.length > 0 && (
            <div className="entity-group">
              <h4 className="entity-group-title">🏢 Organizations</h4>
              <div className="entity-list">
                {key_entities.organizations.map((org, index) => (
                  <span key={index} className="entity-item entity-org">
                    {org}
                  </span>
                ))}
              </div>
            </div>
          )}

          {key_entities.locations && key_entities.locations.length > 0 && (
            <div className="entity-group">
              <h4 className="entity-group-title">📍 Locations</h4>
              <div className="entity-list">
                {key_entities.locations.map((location, index) => (
                  <span key={index} className="entity-item entity-location">
                    {location}
                  </span>
                ))}
              </div>
            </div>
          )}
        </CollapsibleSection>
      )}

      {/* Article Sections */}
      {sections && sections.length > 0 && (
        <CollapsibleSection title="Article Sections" icon="📑" defaultOpen={false}>
          <div className="sections-grid">
            {sections.map((section, index) => (
              <div key={index} className="section-item">
                {section}
              </div>
            ))}
          </div>
        </CollapsibleSection>
      )}

      {/* Quiz Questions Section */}
      {quiz && quiz.length > 0 && (
        <CollapsibleSection 
          title="Quiz Questions" 
          icon="❓" 
          defaultOpen={true}
          badge={`${quiz.length} Questions`}
        >
          {/* Navigation Controls - NEW (Only in Take Quiz Mode) */}
          {!showAllQuestions && (
            <>
              <div className="question-nav-controls">
                <div className="question-nav-buttons">
                  <button
                    className="nav-btn"
                    onClick={handlePrevQuestion}
                    disabled={currentQuestionIndex === 0}
                  >
                    ← Previous
                  </button>
                  <button
                    className="nav-btn"
                    onClick={handleNextQuestion}
                    disabled={currentQuestionIndex === quiz.length - 1}
                  >
                    Next →
                  </button>
                </div>

                <div className="question-progress">
                  <span className="question-counter">
                    Question {currentQuestionIndex + 1} of {quiz.length}
                  </span>
                  <div className="progress-bar-container">
                    <div 
                      className="progress-bar-fill" 
                      style={{ width: `${((currentQuestionIndex + 1) / quiz.length) * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              
              {/* Keyboard shortcuts hint */}
              <div className="keyboard-hint">
                
                💡 Use <kbd>←</kbd> <kbd>→</kbd> arrow keys to navigate between questions
              </div>
            </>
          )}

          {quizMode === 'take' && !showResults && (
            <div className="quiz-instructions">
              <span className="quiz-instructions-icon">💡</span>
              <div className="quiz-instructions-content">
                <p>
                  Select your answers for all questions, then click "Submit Quiz" to see your results.
                </p>
                <p className="quiz-progress">
                  <strong>Answered: {Object.keys(userAnswers).length} / {quiz.length}</strong>
                </p>
              </div>
              <button
                onClick={handleSubmitQuiz}
                className="btn btn-primary"
                disabled={Object.keys(userAnswers).length !== quiz.length}
              >
                ✅ Submit Quiz
              </button>
            </div>
          )}
          
          {/* Display Questions */}
          {showAllQuestions ? (
            // VIEW MODE: Show all questions
            quiz.map((question, index) => (
              <div key={index} className="question-card">
                <div className="question-header">
                  <span className="question-number">Question {index + 1}</span>
                  <div className="question-badges">
                    <span className={`badge badge-${question.difficulty}`}>
                      {question.difficulty}
                    </span>
                  </div>
                </div>

                <p className="question-text">{question.question}</p>

                <ul className="options-list">
                  {question.options.map((option, optIndex) => {
                    const isCorrect = option === question.answer;

                    return (
                      <li
                        key={optIndex}
                        className={`option-item ${isCorrect ? 'correct' : ''}`}
                        style={{ cursor: 'default' }}
                      >
                        <span className="option-label">
                          {String.fromCharCode(65 + optIndex)}.
                        </span>
                        <span className="option-text">{option}</span>
                        
                        {isCorrect && (
                          <span className="correct-label">✓ Correct Answer</span>
                        )}
                      </li>
                    );
                  })}
                </ul>

                {question.explanation && (
                  <div className="explanation">
                    <strong>💡 Explanation: </strong>
                    {question.explanation}
                  </div>
                )}
              </div>
            ))
          ) : (
            // TAKE QUIZ MODE: Show current question only
            <div className="question-carousel">
              {quiz.map((question, index) => (
                index === currentQuestionIndex && (
                  <div key={index} className="question-card">
                    <div className="question-header">
                      <span className="question-number">Question {index + 1}</span>
                      <div className="question-badges">
                        <span className={`badge badge-${question.difficulty}`}>
                          {question.difficulty}
                        </span>
                        
                        {showResults && (
                          <span className={`badge ${
                            userAnswers[index] === question.answer ? 'badge-success' : 'badge-danger'
                          }`}>
                            {userAnswers[index] === question.answer ? '✓ Correct' : '✗ Wrong'}
                          </span>
                        )}
                      </div>
                    </div>

                    <p className="question-text">{question.question}</p>

                    <ul className="options-list">
                      {question.options.map((option, optIndex) => {
                        const isSelected = userAnswers[index] === option;
                        const isCorrect = option === question.answer;
                        const showAnswer = showResults;

                        let optionClass = 'option-item-interactive';
                        
                        if (showAnswer) {
                          if (isCorrect) {
                            optionClass += ' correct-answer';
                          } else if (isSelected && !isCorrect) {
                            optionClass += ' wrong-answer';
                          }
                        } else if (isSelected) {
                          optionClass += ' selected';
                        }

                        return (
                          <li
                            key={optIndex}
                            className={optionClass}
                            onClick={() => !showResults && handleAnswerSelect(index, option)}
                            style={{ cursor: showResults ? 'default' : 'pointer' }}
                          >
                            <span className="option-label">
                              {String.fromCharCode(65 + optIndex)}.
                            </span>
                            <span className="option-text">{option}</span>
                            
                            {showAnswer && isCorrect && (
                              <span className="option-indicator success">✓</span>
                            )}
                            {showAnswer && isSelected && !isCorrect && (
                              <span className="option-indicator error">✗</span>
                            )}
                          </li>
                        );
                      })}
                    </ul>

                    {showResults && question.explanation && (
                      <div className="explanation">
                        <strong>💡 Explanation: </strong>
                        {question.explanation}
                      </div>
                    )}
                  </div>
                )
              ))}
            </div>
          )}
        </CollapsibleSection>
      )}

      {/* Related Topics Section */}
      {related_topics && related_topics.length > 0 && (
        <CollapsibleSection title="Related Topics" icon="🔗" defaultOpen={false}>
          <p className="related-topics-intro">
            Explore these related topics to learn more:
          </p>
          <div className="related-topics">
            {related_topics.map((topic, index) => (
              <a
                key={index}
                href={`https://en.wikipedia.org/wiki/${topic.replace(/ /g, '_')}`}
                target="_blank"
                rel="noopener noreferrer"
                className="topic-link"
              >
                {topic} →
              </a>
            ))}
          </div>
        </CollapsibleSection>
      )}
    </div>
  );
};

export default QuizDisplay;

