import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import LearningPlan from './pages/LearningPlan';
import Recommendations from './pages/Recommendations';
import ChatbotWidget from './chatbot/ChatbotWidget';
import ProtectedRoute from './components/ProtectedRoute';

// Component to handle studentId state
function AppContent() {
  const [studentId, setStudentId] = useState(() => localStorage.getItem('studentId'));
  const location = useLocation();

  useEffect(() => {
    // Update studentId when location changes (after login)
    const id = localStorage.getItem('studentId');
    setStudentId(id);
  }, [location]);

  return (
    <>
      <Routes>
        <Route 
          path="/" 
          element={studentId ? <Navigate to="/dashboard" replace /> : <Login onLogin={setStudentId} />} 
        />
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/learning-plan" 
          element={
            <ProtectedRoute>
              <LearningPlan />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/recommendations" 
          element={
            <ProtectedRoute>
              <Recommendations />
            </ProtectedRoute>
          } 
        />
      </Routes>
      
      {/* Global Chatbot Widget */}
      {studentId && <ChatbotWidget studentId={studentId} />}
    </>
  );
}

function App() {

  return (
    <Router>
      <div className="App">
        <AppContent />
      </div>
    </Router>
  );
}

export default App;
