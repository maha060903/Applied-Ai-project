import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/Card';
import Button from '../components/Button';
import PerformanceChart from '../components/PerformanceChart';
import { analyzePerformance, getStudentPerformance, healthCheck } from '../services/api';
import { TrendingUp, TrendingDown, BookOpen, Target, AlertCircle, CheckCircle } from 'lucide-react';
import Input from '../components/Input';

const Dashboard = () => {
  const navigate = useNavigate();
  const studentId = localStorage.getItem('studentId') || 'STU001';
  
  const [performanceData, setPerformanceData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [backendConnected, setBackendConnected] = useState(null);
  const [error, setError] = useState(null);
  
  const [formData, setFormData] = useState({
    subject: 'Mathematics',
    quiz_score: 75,
    attendance: 85,
  });

  useEffect(() => {
    checkBackendConnection();
    loadStudentData();
  }, [studentId]);

  const checkBackendConnection = async () => {
    try {
      const health = await healthCheck();
      setBackendConnected(health.status === 'healthy');
    } catch (error) {
      console.error('Backend connection error:', error);
      setBackendConnected(false);
    }
  };

  const loadStudentData = async () => {
    try {
      const data = await getStudentPerformance(studentId);
      if (data.performance_history) {
        setPerformanceData(data.performance_history);
      }
    } catch (error) {
      console.error('Error loading student data:', error);
      // Don't show error for missing student data, it's optional
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const result = await analyzePerformance({
        student_id: studentId,
        ...formData,
      });
      setAnalysisResult(result);
    } catch (error) {
      console.error('Error analyzing performance:', error);
      setError(
        error.response?.data?.detail || 
        error.message || 
        'Backend server se connect nahi ho pa raha. Kripya backend server start karein (port 8000).'
      );
    } finally {
      setLoading(false);
    }
  };

  const getPerformanceColor = (level) => {
    const colors = {
      Excellent: 'text-green-600 bg-green-100',
      Good: 'text-blue-600 bg-blue-100',
      Average: 'text-yellow-600 bg-yellow-100',
      'Below Average': 'text-orange-600 bg-orange-100',
      Poor: 'text-red-600 bg-red-100',
    };
    return colors[level] || colors.Average;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-sm text-gray-600">Student ID: {studentId}</p>
            </div>
            <div className="flex items-center gap-4">
              {/* Backend Connection Status */}
              {backendConnected !== null && (
                <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-sm ${
                  backendConnected 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {backendConnected ? (
                    <>
                      <CheckCircle size={16} />
                      <span>Backend Connected</span>
                    </>
                  ) : (
                    <>
                      <AlertCircle size={16} />
                      <span>Backend Not Connected</span>
                    </>
                  )}
                </div>
              )}
              <Button
                variant="secondary"
                onClick={() => {
                  localStorage.removeItem('studentId');
                  navigate('/');
                }}
              >
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Backend Connection Warning */}
        {backendConnected === false && (
          <Card className="mb-6 border-red-300 bg-red-50">
            <div className="flex items-start gap-3">
              <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
              <div>
                <h3 className="font-semibold text-red-900 mb-1">Backend Server Not Running</h3>
                <p className="text-sm text-red-700 mb-3">
                  Backend server start karein taaki application kaam kare. Terminal mein yeh command run karein:
                </p>
                <code className="block bg-red-100 text-red-900 p-2 rounded text-sm mb-3">
                  cd backend<br />
                  python -m uvicorn app.main:app --reload
                </code>
                <Button 
                  variant="outline" 
                  onClick={checkBackendConnection}
                  className="text-sm"
                >
                  Check Again
                </Button>
              </div>
            </div>
          </Card>
        )}

        {/* Error Message */}
        {error && (
          <Card className="mb-6 border-red-300 bg-red-50">
            <div className="flex items-start gap-3">
              <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
              <div>
                <h3 className="font-semibold text-red-900 mb-1">Error</h3>
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </Card>
        )}
        {/* Performance Analysis Form */}
        <Card title="Analyze Performance" className="mb-8">
          <form onSubmit={handleAnalyze} className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Input
              label="Subject"
              value={formData.subject}
              onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
              required
            />
            <Input
              label="Quiz Score (%)"
              type="number"
              min="0"
              max="100"
              value={formData.quiz_score}
              onChange={(e) => setFormData({ ...formData, quiz_score: parseFloat(e.target.value) })}
              required
            />
            <Input
              label="Attendance (%)"
              type="number"
              min="0"
              max="100"
              value={formData.attendance}
              onChange={(e) => setFormData({ ...formData, attendance: parseFloat(e.target.value) })}
              required
            />
            <div className="md:col-span-3">
              <Button type="submit" disabled={loading} className="w-full md:w-auto">
                {loading ? 'Analyzing...' : 'Analyze Performance'}
              </Button>
            </div>
          </form>
        </Card>

        {/* Analysis Results */}
        {analysisResult && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <Card title="Performance Analysis">
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Performance Level</p>
                  <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getPerformanceColor(analysisResult.performance_level)}`}>
                    {analysisResult.performance_level}
                  </span>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Confidence</p>
                  <p className="text-lg font-semibold">{(analysisResult.prediction_confidence * 100).toFixed(1)}%</p>
                </div>
                {analysisResult.learning_gaps && analysisResult.learning_gaps.length > 0 && (
                  <div>
                    <p className="text-sm text-gray-600 mb-2">Learning Gaps Identified</p>
                    <ul className="space-y-2">
                      {analysisResult.learning_gaps.map((gap, index) => (
                        <li key={index} className="text-sm bg-red-50 border border-red-200 rounded p-2">
                          <span className="font-medium text-red-800">{gap.type}:</span> {gap.description}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </Card>

            <Card title="Feature Importance">
              <div className="space-y-2">
                {Object.entries(analysisResult.feature_importance || {}).map(([feature, importance]) => (
                  <div key={feature} className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 capitalize">{feature.replace('_', ' ')}</span>
                    <div className="flex-1 mx-4 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-primary-600 h-2 rounded-full"
                        style={{ width: `${importance * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-medium">{(importance * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}

        {/* Performance History Chart */}
        {performanceData && performanceData.length > 0 && (
          <Card title="Performance History" className="mb-8">
            <PerformanceChart data={performanceData} type="bar" />
          </Card>
        )}

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card
            title="Learning Plan"
            subtitle="View your personalized study plan"
          >
            <Button
              variant="outline"
              onClick={() => navigate('/learning-plan')}
              className="w-full"
            >
              <BookOpen className="inline mr-2" size={18} />
              View Learning Plan
            </Button>
          </Card>

          <Card
            title="Recommendations"
            subtitle="Get AI-powered study recommendations"
          >
            <Button
              variant="outline"
              onClick={() => navigate('/recommendations')}
              className="w-full"
            >
              <Target className="inline mr-2" size={18} />
              View Recommendations
            </Button>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
