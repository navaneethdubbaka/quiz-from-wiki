// src/services/api.js
import axios from 'axios';

// Base URL for the FastAPI backend
// In Vercel, API routes are under /api, so we use relative URLs
// For local development, use the full URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
  (import.meta.env.PROD ? '/api' : 'http://localhost:8000');

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 2 minutes timeout for quiz generation
});

/**
 * API Service for communicating with FastAPI backend
 */
const api = {
  /**
   * Generate a quiz from a Wikipedia URL
   * @param {string} url - Wikipedia article URL
   * @returns {Promise} Quiz data
   */
  generateQuiz: async (url) => {
    try {
      const response = await apiClient.post('/generate_quiz', { url });
      return {
        success: true,
        data: response.data,
        error: null,
      };
    } catch (error) {
      return {
        success: false,
        data: null,
        error: error.response?.data?.detail || error.message || 'Failed to generate quiz',
      };
    }
  },

  /**
   * Get all quiz history
   * @returns {Promise} Array of quiz history items
   */
  getHistory: async () => {
    try {
      const response = await apiClient.get('/history');
      return {
        success: true,
        data: response.data,
        error: null,
      };
    } catch (error) {
      return {
        success: false,
        data: null,
        error: error.response?.data?.detail || error.message || 'Failed to fetch history',
      };
    }
  },

  /**
   * Get a specific quiz by ID
   * @param {number} quizId - Quiz ID
   * @returns {Promise} Quiz data
   */
  getQuizById: async (quizId) => {
    try {
      const response = await apiClient.get(`/quiz/${quizId}`);
      return {
        success: true,
        data: response.data,
        error: null,
      };
    } catch (error) {
      return {
        success: false,
        data: null,
        error: error.response?.data?.detail || error.message || 'Failed to fetch quiz',
      };
    }
  },

  /**
   * Delete a quiz by ID (for testing)
   * @param {number} quizId - Quiz ID
   * @returns {Promise} Success message
   */
  deleteQuiz: async (quizId) => {
    try {
      const response = await apiClient.delete(`/quiz/${quizId}`);
      return {
        success: true,
        data: response.data,
        error: null,
      };
    } catch (error) {
      return {
        success: false,
        data: null,
        error: error.response?.data?.detail || error.message || 'Failed to delete quiz',
      };
    }
  },

  /**
   * Check API health
   * @returns {Promise} Health status
   */
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/health');
      return {
        success: true,
        data: response.data,
        error: null,
      };
    } catch (error) {
      return {
        success: false,
        data: null,
        error: 'Backend server is not responding',
      };
    }
  },
};

export default api;