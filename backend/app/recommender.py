"""
Recommendation Engine for Personalized Learning Plans
Generates study recommendations based on student performance analysis
"""

from typing import List, Dict, Any
import random


class RecommendationEngine:
    """Rule-based recommendation engine for personalized learning"""
    
    def __init__(self):
        self.recommendation_templates = {
            'Excellent': [
                "Great job! You're excelling in this subject. Consider exploring advanced topics or helping peers.",
                "Your performance is outstanding. Challenge yourself with more complex problems.",
                "Excellent work! You might want to mentor other students or take on leadership roles."
            ],
            'Good': [
                "You're doing well! Focus on maintaining consistency and reviewing key concepts regularly.",
                "Good progress! Try to identify any minor gaps and practice more challenging problems.",
                "Keep up the good work! Consider joining study groups to reinforce your understanding."
            ],
            'Average': [
                "You're on the right track. Focus on regular practice and review of fundamental concepts.",
                "Consider dedicating more time to this subject. Break down topics into smaller, manageable chunks.",
                "Average performance suggests room for improvement. Create a structured study schedule."
            ],
            'Below Average': [
                "Let's work on improving. Start with basics and build up gradually. Don't hesitate to ask for help.",
                "Focus on understanding core concepts first. Practice daily and track your progress.",
                "Consider seeking additional support. Review foundational material and practice regularly."
            ],
            'Poor': [
                "Let's create a focused improvement plan. Start with the basics and practice consistently.",
                "Don't worry, we can improve! Break down the subject into small steps and celebrate small wins.",
                "Consider one-on-one tutoring or additional resources. Focus on understanding, not just memorizing."
            ]
        }
        
        self.study_resources = {
            'Mathematics': [
                "Khan Academy - Algebra and Calculus",
                "Practice problem sets from textbook",
                "Online math tutoring sessions",
                "Math study groups"
            ],
            'Science': [
                "Interactive science simulations",
                "Laboratory practice sessions",
                "Science documentaries and videos",
                "Concept mapping exercises"
            ],
            'English': [
                "Reading comprehension exercises",
                "Writing practice with feedback",
                "Grammar and vocabulary building",
                "Literature discussion groups"
            ],
            'History': [
                "Timeline creation activities",
                "Primary source analysis",
                "Historical documentaries",
                "Study guides and flashcards"
            ],
            'Computer Science': [
                "Coding practice platforms",
                "Project-based learning",
                "Algorithm visualization tools",
                "Peer programming sessions"
            ]
        }
    
    def generate_recommendations(
        self,
        student_id: str,
        performance_data: Dict[str, Any],
        learning_gaps: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate personalized learning recommendations"""
        recommendations = []
        
        # Get overall performance level
        performance_level = performance_data.get('performance_level', 'Average')
        
        # Add motivational message
        motivational_msg = random.choice(self.recommendation_templates.get(performance_level, []))
        recommendations.append({
            'type': 'motivational',
            'priority': 'high',
            'title': 'Learning Guidance',
            'description': motivational_msg,
            'action_items': []
        })
        
        # Add subject-specific recommendations
        subject = performance_data.get('subject', 'General')
        if subject in self.study_resources:
            recommendations.append({
                'type': 'resources',
                'priority': 'medium',
                'title': f'Recommended Resources for {subject}',
                'description': f'Here are some resources to help you improve in {subject}',
                'action_items': self.study_resources[subject]
            })
        
        # Add gap-specific recommendations
        for gap in learning_gaps:
            gap_recommendations = self._generate_gap_recommendations(gap)
            recommendations.extend(gap_recommendations)
        
        # Add general study tips
        recommendations.append({
            'type': 'study_tips',
            'priority': 'low',
            'title': 'General Study Tips',
            'description': 'Best practices for effective learning',
            'action_items': [
                "Study in 25-30 minute focused sessions (Pomodoro technique)",
                "Review material within 24 hours of learning",
                "Teach concepts to others to reinforce understanding",
                "Use active recall instead of passive reading",
                "Get adequate sleep for better memory retention"
            ]
        })
        
        return recommendations
    
    def _generate_gap_recommendations(self, gap: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific recommendations for identified learning gaps"""
        recommendations = []
        
        gap_type = gap.get('type', '')
        severity = gap.get('severity', 'Medium')
        subject = gap.get('subject', 'Unknown')
        
        if gap_type == 'Low Quiz Score':
            recommendations.append({
                'type': 'action_plan',
                'priority': 'high' if severity == 'High' else 'medium',
                'title': f'Improve {subject} Performance',
                'description': gap.get('description', ''),
                'action_items': [
                    f"Review {subject} fundamentals this week",
                    f"Complete 3 practice quizzes on {subject}",
                    f"Schedule a review session with instructor",
                    f"Focus on understanding concepts, not just memorization"
                ]
            })
        
        elif gap_type == 'Low Attendance':
            recommendations.append({
                'type': 'action_plan',
                'priority': 'high' if severity == 'High' else 'medium',
                'title': 'Improve Attendance',
                'description': gap.get('description', ''),
                'action_items': [
                    "Set reminders for class schedules",
                    "Review missed class materials",
                    "Connect with classmates for notes",
                    "Communicate with instructors about absences"
                ]
            })
        
        return recommendations
    
    def create_study_plan(
        self,
        student_id: str,
        recommendations: List[Dict[str, Any]],
        duration_weeks: int = 4
    ) -> Dict[str, Any]:
        """Create a structured study plan"""
        study_plan = {
            'student_id': student_id,
            'duration_weeks': duration_weeks,
            'weekly_goals': [],
            'daily_tasks': []
        }
        
        # Prioritize recommendations
        high_priority = [r for r in recommendations if r.get('priority') == 'high']
        medium_priority = [r for r in recommendations if r.get('priority') == 'medium']
        
        # Create weekly goals
        for week in range(1, duration_weeks + 1):
            week_goals = []
            
            if week == 1 and high_priority:
                week_goals.append({
                    'goal': 'Address critical learning gaps',
                    'recommendations': high_priority[:2]
                })
            elif week == 2 and medium_priority:
                week_goals.append({
                    'goal': 'Focus on improvement areas',
                    'recommendations': medium_priority[:2]
                })
            else:
                week_goals.append({
                    'goal': 'Maintain progress and review',
                    'recommendations': recommendations[:1]
                })
            
            study_plan['weekly_goals'].append({
                'week': week,
                'goals': week_goals
            })
        
        return study_plan
