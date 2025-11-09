// src/components/CollapsibleSection.jsx
import React, { useState } from 'react';

const CollapsibleSection = ({ title, icon, children, defaultOpen = false, badge = null }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="collapsible-section">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`collapsible-header ${isOpen ? 'open' : ''}`}
        aria-expanded={isOpen}
      >
        <div className="collapsible-header-content">
          <span className="collapsible-icon">{icon}</span>
          <h3 className="collapsible-title">{title}</h3>
          {badge && (
            <span className="collapsible-badge">{badge}</span>
          )}
        </div>
        <span className={`collapsible-arrow ${isOpen ? 'open' : ''}`}>
          ▼
        </span>
      </button>
      
      {isOpen && (
        <div className="collapsible-content">
          {children}
        </div>
      )}
    </div>
  );
};

export default CollapsibleSection;