/**
 * API Service for communicating with FastAPI backend
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Analyze student performance
 */
export const analyzePerformance = async (studentData) => {
  try {
    const response = await api.post('/analyze-performance', studentData);
    return response.data;
  } catch (error) {
    console.error('Error analyzing performance:', error);
    throw error;
  }
};

/**
 * Get personalized recommendations
 */
export const getRecommendations = async (studentId, options = {}) => {
  try {
    const params = new URLSearchParams();
    if (options.subject) params.append('subject', options.subject);
    if (options.quiz_score !== undefined) params.append('quiz_score', options.quiz_score);
    if (options.attendance !== undefined) params.append('attendance', options.attendance);
    
    const url = `/recommendations/${studentId}${params.toString() ? '?' + params.toString() : ''}`;
    const response = await api.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    throw error;
  }
};

/**
 * Chat with educational chatbot
 */
export const chatWithBot = async (message, studentId = null, studentContext = null) => {
  try {
    const response = await api.post('/chatbot', {
      message,
      student_id: studentId,
      student_context: studentContext,
    });
    return response.data;
  } catch (error) {
    console.error('Error chatting with bot:', error);
    throw error;
  }
};

/**
 * Get student performance history
 */
export const getStudentPerformance = async (studentId) => {
  try {
    const response = await api.get(`/students/${studentId}/performance`);
    return response.data;
  } catch (error) {
    console.error('Error fetching student performance:', error);
    throw error;
  }
};

/**
 * Health check
 */
export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    return { status: 'unhealthy' };
  }
};

export default api;
