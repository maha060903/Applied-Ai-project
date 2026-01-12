import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/Card';
import Button from '../components/Button';
import { getRecommendations } from '../services/api';
import { Calendar, CheckCircle, Clock, BookOpen } from 'lucide-react';

const LearningPlan = () => {
  const navigate = useNavigate();
  const studentId = localStorage.getItem('studentId') || 'STU001';
  
  const [studyPlan, setStudyPlan] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStudyPlan();
  }, []);

  const loadStudyPlan = async () => {
    try {
      const data = await getRecommendations(studentId);
      if (data.study_plan) {
        setStudyPlan(data.study_plan);
      }
    } catch (error) {
      console.error('Error loading study plan:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your learning plan...</p>
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
              <h1 className="text-2xl font-bold text-gray-900">Learning Plan</h1>
              <p className="text-sm text-gray-600">Student ID: {studentId}</p>
            </div>
            <Button variant="secondary" onClick={() => navigate('/dashboard')}>
              Back to Dashboard
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {studyPlan ? (
          <>
            <Card title={`${studyPlan.duration_weeks}-Week Study Plan`} className="mb-8">
              <div className="flex items-center text-gray-600 mb-4">
                <Calendar className="mr-2" size={18} />
                <span>Duration: {studyPlan.duration_weeks} weeks</span>
              </div>
            </Card>

            {/* Weekly Goals */}
            <div className="space-y-6">
              {studyPlan.weekly_goals?.map((week, weekIndex) => (
                <Card key={weekIndex} title={`Week ${week.week}`} className="mb-6">
                  {week.goals?.map((goal, goalIndex) => (
                    <div key={goalIndex} className="mb-6 last:mb-0">
                      <div className="flex items-start mb-4">
                        <div className="bg-primary-100 p-2 rounded-full mr-3">
                          <BookOpen className="text-primary-600" size={20} />
                        </div>
                        <div className="flex-1">
                          <h4 className="font-semibold text-gray-900 mb-2">{goal.goal}</h4>
                          {goal.recommendations?.map((rec, recIndex) => (
                            <div key={recIndex} className="bg-gray-50 rounded-lg p-4 mb-3">
                              <h5 className="font-medium text-gray-900 mb-2">{rec.title}</h5>
                              <p className="text-sm text-gray-600 mb-3">{rec.description}</p>
                              {rec.action_items && rec.action_items.length > 0 && (
                                <ul className="space-y-2">
                                  {rec.action_items.map((item, itemIndex) => (
                                    <li key={itemIndex} className="flex items-start text-sm text-gray-700">
                                      <CheckCircle className="text-green-500 mr-2 mt-0.5 flex-shrink-0" size={16} />
                                      <span>{item}</span>
                                    </li>
                                  ))}
                                </ul>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </Card>
              ))}
            </div>
          </>
        ) : (
          <Card>
            <p className="text-gray-600">No study plan available. Please analyze your performance first.</p>
            <Button onClick={() => navigate('/dashboard')} className="mt-4">
              Go to Dashboard
            </Button>
          </Card>
        )}
      </div>
    </div>
  );
};

export default LearningPlan;
