import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/Card';
import Button from '../components/Button';
import { getRecommendations } from '../services/api';
import { Lightbulb, Target, BookOpen, TrendingUp, AlertCircle } from 'lucide-react';

const Recommendations = () => {
  const navigate = useNavigate();
  const studentId = localStorage.getItem('studentId') || 'STU001';
  
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    try {
      const data = await getRecommendations(studentId);
      if (data.recommendations) {
        setRecommendations(data.recommendations);
      }
    } catch (error) {
      console.error('Error loading recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  const getIcon = (type) => {
    const icons = {
      motivational: TrendingUp,
      resources: BookOpen,
      action_plan: Target,
      study_tips: Lightbulb,
    };
    return icons[type] || Lightbulb;
  };

  const getPriorityColor = (priority) => {
    const colors = {
      high: 'bg-red-100 text-red-800 border-red-200',
      medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      low: 'bg-blue-100 text-blue-800 border-blue-200',
    };
    return colors[priority] || colors.medium;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading recommendations...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Personalized Recommendations</h1>
              <p className="text-sm text-gray-600">AI-powered study suggestions for Student ID: {studentId}</p>
            </div>
            <Button variant="secondary" onClick={() => navigate('/dashboard')}>
              Back to Dashboard
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {recommendations.length > 0 ? (
          <div className="space-y-6">
            {recommendations.map((rec, index) => {
              const Icon = getIcon(rec.type);
              return (
                <Card key={index} className="border-l-4 border-primary-500">
                  <div className="flex items-start">
                    <div className="bg-primary-100 p-3 rounded-full mr-4">
                      <Icon className="text-primary-600" size={24} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-xl font-semibold text-gray-900">{rec.title}</h3>
                        <span className={`px-2 py-1 rounded text-xs font-medium border ${getPriorityColor(rec.priority)}`}>
                          {rec.priority} priority
                        </span>
                      </div>
                      <p className="text-gray-600 mb-4">{rec.description}</p>
                      
                      {rec.action_items && rec.action_items.length > 0 && (
                        <div>
                          <h4 className="font-medium text-gray-900 mb-2">Action Items:</h4>
                          <ul className="space-y-2">
                            {rec.action_items.map((item, itemIndex) => (
                              <li key={itemIndex} className="flex items-start text-sm text-gray-700">
                                <span className="text-primary-600 mr-2">•</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        ) : (
          <Card>
            <div className="text-center py-8">
              <AlertCircle className="mx-auto text-gray-400 mb-4" size={48} />
              <p className="text-gray-600 mb-4">No recommendations available yet.</p>
              <p className="text-sm text-gray-500 mb-6">
                Please analyze your performance first to get personalized recommendations.
              </p>
              <Button onClick={() => navigate('/dashboard')}>
                Go to Dashboard
              </Button>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Recommendations;
