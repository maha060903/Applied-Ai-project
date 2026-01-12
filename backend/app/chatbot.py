"""
AI Chatbot for Educational Assistance
Provides context-aware responses based on student performance data
"""

from typing import Dict, List, Any, Optional
import random


class EducationalChatbot:
    """
    Educational chatbot that provides personalized guidance
    Compatible with LLM-style interfaces (IBM Granite/Watsonx ready)
    """
    
    def __init__(self):
        self.system_prompt = """You are an AI educational assistant helping students improve learning outcomes based on academic performance data. 
Your role is to:
- Explain weak topics clearly and supportively
- Suggest what to study next based on performance analysis
- Provide motivation and encouragement
- Never provide medical or psychological diagnosis
- Focus on educational guidance only
- Be empathetic and understanding"""
        
        self.context_templates = {
            'performance_explanation': [
                "Based on your recent performance in {subject}, I can see you scored {score}%. This places you in the {level} category. Let's work together to improve this!",
                "Your {subject} quiz shows a score of {score}%, which is {level}. I'm here to help you understand the concepts better.",
                "Looking at your {subject} performance ({score}%), you're at {level} level. We can definitely improve this with focused practice."
            ],
            'gap_identification': [
                "I've identified that you might be struggling with {gap_type} in {subject}. This is common and totally fixable!",
                "One area we should focus on is {gap_type} for {subject}. Let's create a plan to address this.",
                "I notice {gap_type} could be improved in {subject}. Here's how we can work on it together."
            ],
            'encouragement': [
                "Remember, every expert was once a beginner. You're making progress!",
                "Learning is a journey, not a destination. Keep going!",
                "It's okay to struggle - that's how we grow. I believe in you!",
                "Small steps lead to big improvements. You've got this!"
            ],
            'study_suggestion': [
                "I recommend focusing on {topic} next. Start with the basics and build up gradually.",
                "For {subject}, I suggest studying {topic}. Break it down into smaller concepts.",
                "Let's prioritize {topic} in {subject}. Practice makes perfect!"
            ]
        }
    
    def generate_response(
        self,
        user_message: str,
        student_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a contextual response based on user message and student data
        In production, this would integrate with IBM Granite/Watsonx API
        """
        user_message_lower = user_message.lower()
        
        # Extract intent
        intent = self._classify_intent(user_message_lower)
        
        # Generate contextual response
        if intent == 'performance_inquiry' and student_context:
            response = self._handle_performance_inquiry(student_context)
        elif intent == 'study_help' and student_context:
            response = self._handle_study_help(user_message, student_context)
        elif intent == 'motivation':
            response = self._handle_motivation()
        elif intent == 'recommendation_request' and student_context:
            response = self._handle_recommendation_request(student_context)
        else:
            response = self._handle_general_query(user_message, student_context)
        
        return {
            'response': response,
            'intent': intent,
            'context_used': student_context is not None
        }
    
    def _classify_intent(self, message: str) -> str:
        """Classify user intent from message"""
        performance_keywords = ['score', 'performance', 'grade', 'result', 'how am i doing']
        study_keywords = ['study', 'learn', 'practice', 'help', 'understand', 'topic']
        motivation_keywords = ['motivate', 'encourage', 'discouraged', 'difficult', 'hard']
        recommendation_keywords = ['recommend', 'suggest', 'what should', 'next', 'plan']
        
        if any(keyword in message for keyword in performance_keywords):
            return 'performance_inquiry'
        elif any(keyword in message for keyword in study_keywords):
            return 'study_help'
        elif any(keyword in message for keyword in motivation_keywords):
            return 'motivation'
        elif any(keyword in message for keyword in recommendation_keywords):
            return 'recommendation_request'
        else:
            return 'general'
    
    def _handle_performance_inquiry(self, context: Dict[str, Any]) -> str:
        """Handle questions about performance"""
        performance_level = context.get('performance_level', 'Average')
        quiz_score = context.get('quiz_score', 0)
        subject = context.get('subject', 'your subjects')
        
        template = random.choice(self.context_templates['performance_explanation'])
        response = template.format(
            subject=subject,
            score=quiz_score,
            level=performance_level
        )
        
        # Add encouragement
        encouragement = random.choice(self.context_templates['encouragement'])
        response += f"\n\n{encouragement}"
        
        return response
    
    def _handle_study_help(self, message: str, context: Dict[str, Any]) -> str:
        """Handle study-related questions"""
        subject = context.get('subject', 'the subject')
        performance_level = context.get('performance_level', 'Average')
        
        response = f"I'm here to help you with {subject}! "
        
        if performance_level in ['Below Average', 'Poor']:
            response += "Let's start with the fundamentals. I recommend reviewing the basic concepts first, then gradually moving to more complex topics. "
            response += "Would you like me to suggest specific study resources or create a study plan?"
        else:
            response += "You're doing well! To improve further, I suggest practicing more challenging problems and exploring advanced topics. "
            response += "What specific area would you like help with?"
        
        return response
    
    def _handle_motivation(self) -> str:
        """Provide motivational support"""
        encouragement = random.choice(self.context_templates['encouragement'])
        response = f"{encouragement}\n\n"
        response += "Remember that learning takes time and effort. Every small step forward is progress. "
        response += "If you're feeling stuck, try breaking down your goals into smaller, manageable tasks. "
        response += "You've got this! 💪"
        
        return response
    
    def _handle_recommendation_request(self, context: Dict[str, Any]) -> str:
        """Handle requests for study recommendations"""
        subject = context.get('subject', 'your studies')
        performance_level = context.get('performance_level', 'Average')
        
        response = f"Based on your performance in {subject}, here's what I recommend:\n\n"
        
        if performance_level in ['Below Average', 'Poor']:
            response += "1. Review fundamental concepts - make sure you understand the basics\n"
            response += "2. Practice regularly - consistency is key\n"
            response += "3. Seek help when needed - don't hesitate to ask questions\n"
            response += "4. Track your progress - celebrate small wins\n"
        elif performance_level == 'Average':
            response += "1. Focus on areas where you can improve\n"
            response += "2. Challenge yourself with more difficult problems\n"
            response += "3. Join study groups to reinforce learning\n"
            response += "4. Review and practice regularly\n"
        else:
            response += "1. Explore advanced topics to deepen understanding\n"
            response += "2. Help others learn - teaching reinforces your knowledge\n"
            response += "3. Take on challenging projects\n"
            response += "4. Maintain your excellent performance\n"
        
        return response
    
    def _handle_general_query(self, message: str, context: Optional[Dict[str, Any]]) -> str:
        """Handle general queries"""
        response = "I'm here to help you with your learning journey! "
        
        if context:
            subject = context.get('subject', 'your studies')
            response += f"I can see you're working on {subject}. "
        
        response += "I can help you with:\n"
        response += "- Understanding your performance\n"
        response += "- Creating study plans\n"
        response += "- Recommending resources\n"
        response += "- Providing motivation and support\n\n"
        response += "What would you like to know?"
        
        return response
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for LLM integration"""
        return self.system_prompt
    
    def format_context_for_llm(self, student_context: Dict[str, Any]) -> str:
        """Format student context for LLM API calls"""
        context_str = f"Student Performance Context:\n"
        context_str += f"- Subject: {student_context.get('subject', 'N/A')}\n"
        context_str += f"- Quiz Score: {student_context.get('quiz_score', 0)}%\n"
        context_str += f"- Performance Level: {student_context.get('performance_level', 'N/A')}\n"
        context_str += f"- Attendance: {student_context.get('attendance', 0)}%\n"
        
        if 'learning_gaps' in student_context:
            context_str += f"- Learning Gaps: {len(student_context['learning_gaps'])} identified\n"
        
        return context_str
