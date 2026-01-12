import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Input from '../components/Input';
import Button from '../components/Button';
import { GraduationCap } from 'lucide-react';

const Login = ({ onLogin }) => {
  const [studentId, setStudentId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!studentId.trim()) {
      setError('Please enter a Student ID');
      return;
    }

    setLoading(true);
    
    try {
      // Store student ID in localStorage
      const trimmedId = studentId.trim().toUpperCase();
      localStorage.setItem('studentId', trimmedId);
      
      // Notify parent component
      if (onLogin) {
        onLogin(trimmedId);
      }
      
      // Small delay to ensure state updates
      setTimeout(() => {
        navigate('/dashboard', { replace: true });
      }, 100);
    } catch (err) {
      setError('An error occurred. Please try again.');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100 px-4">
      <div className="max-w-md w-full">
        <div className="card text-center">
          <div className="flex justify-center mb-6">
            <div className="bg-primary-600 p-4 rounded-full">
              <GraduationCap className="text-white" size={48} />
            </div>
          </div>
          
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            AI-Powered Learning Assistant
          </h1>
          <p className="text-gray-600 mb-8">
            Personalized learning recommendations powered by AI
          </p>

          <form onSubmit={handleSubmit}>
            <Input
              label="Student ID"
              value={studentId}
              onChange={(e) => {
                setStudentId(e.target.value);
                setError('');
              }}
              placeholder="Enter your Student ID (e.g., STU001)"
              required
              error={error}
            />
            
            <Button 
              type="submit" 
              className="w-full" 
              disabled={loading}
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
                  Loading...
                </span>
              ) : (
                'Get Started'
              )}
            </Button>
          </form>

          <p className="text-sm text-gray-500 mt-4">
            Demo: Use STU001, STU002, etc. from the dataset
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
