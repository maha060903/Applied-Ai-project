"""
FastAPI Backend for AI-Powered Personalized Learning Assistant
Main API endpoints for performance analysis, recommendations, and chatbot
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import os
from pathlib import Path

from .model import StudentPerformanceModel
from .recommender import RecommendationEngine
from .chatbot import EducationalChatbot

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Personalized Learning Assistant API",
    description="Backend API for student performance analysis and personalized learning recommendations",
    version="1.0.0"
)

# CORS configuration for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "https://*.vercel.app",   # Vercel deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
model = StudentPerformanceModel()
recommender = RecommendationEngine()
chatbot = EducationalChatbot()

# Global variable to store trained model state
model_trained = False
# Get dataset path - handle both development and production scenarios
base_dir = Path(__file__).parent.parent.parent
dataset_path = os.path.join(base_dir, 'data', 'student_performance.csv')
# Fallback: try relative path from backend directory
if not os.path.exists(dataset_path):
    dataset_path = os.path.join(Path(__file__).parent.parent, '..', 'data', 'student_performance.csv')


# Pydantic models for request/response
class PerformanceAnalysisRequest(BaseModel):
    student_id: str
    subject: str
    quiz_score: float
    attendance: float


class PerformanceAnalysisResponse(BaseModel):
    student_id: str
    subject: str
    performance_level: str
    prediction_confidence: float
    learning_gaps: List[Dict[str, Any]]
    feature_importance: Dict[str, float]


class ChatbotRequest(BaseModel):
    message: str
    student_id: Optional[str] = None
    student_context: Optional[Dict[str, Any]] = None


class ChatbotResponse(BaseModel):
    response: str
    intent: str
    context_used: bool


class RecommendationResponse(BaseModel):
    student_id: str
    recommendations: List[Dict[str, Any]]
    study_plan: Dict[str, Any]


@app.on_event("startup")
async def startup_event():
    """Initialize and train model on startup"""
    global model_trained
    
    try:
        if os.path.exists(dataset_path):
            print(f"Loading dataset from {dataset_path}")
            df = pd.read_csv(dataset_path)
            
            if len(df) > 0:
                print("Training ML model...")
                model.train(df)
                model.save_model()
                model_trained = True
                print("Model trained successfully!")
            else:
                print("Dataset is empty. Model will be trained on first request.")
        else:
            print(f"Dataset not found at {dataset_path}. Model will be trained on first request.")
    except Exception as e:
        print(f"Error during startup: {e}")
        print("Model will be trained on first request.")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI-Powered Personalized Learning Assistant API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyze": "/analyze-performance",
            "recommendations": "/recommendations/{student_id}",
            "chatbot": "/chatbot"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_trained": model_trained
    }


@app.post("/analyze-performance", response_model=PerformanceAnalysisResponse)
async def analyze_performance(request: PerformanceAnalysisRequest):
    """
    Analyze student performance and identify learning gaps
    """
    global model_trained
    try:
        # Ensure model is trained
        if not model_trained:
            if os.path.exists(dataset_path):
                df = pd.read_csv(dataset_path)
                if len(df) > 0:
                    model.train(df)
                    model.save_model()
                    model_trained = True
        
        # Prepare student data
        student_data = {
            'student_id': request.student_id,
            'subject': request.subject,
            'quiz_score': request.quiz_score,
            'attendance': request.attendance
        }
        
        # Predict performance
        prediction = model.predict(student_data)
        
        # Identify learning gaps
        learning_gaps = model.identify_learning_gaps(student_data)
        
        return PerformanceAnalysisResponse(
            student_id=request.student_id,
            subject=request.subject,
            performance_level=prediction['performance_level'],
            prediction_confidence=prediction['prediction_confidence'],
            learning_gaps=learning_gaps,
            feature_importance=prediction['feature_importance']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing performance: {str(e)}")


@app.get("/recommendations/{student_id}", response_model=RecommendationResponse)
async def get_recommendations(
    student_id: str,
    subject: Optional[str] = None,
    quiz_score: Optional[float] = None,
    attendance: Optional[float] = None
):
    """
    Get personalized learning recommendations for a student
    Requires either query params or previous performance analysis
    """
    try:
        # If performance data provided, analyze first
        if subject and quiz_score is not None and attendance is not None:
            student_data = {
                'student_id': student_id,
                'subject': subject,
                'quiz_score': quiz_score,
                'attendance': attendance
            }
            
            # Get performance prediction
            prediction = model.predict(student_data)
            learning_gaps = model.identify_learning_gaps(student_data)
            
            performance_data = {
                'subject': subject,
                'quiz_score': quiz_score,
                'attendance': attendance,
                'performance_level': prediction['performance_level']
            }
        else:
            # Use default values for demonstration
            performance_data = {
                'subject': subject or 'Mathematics',
                'quiz_score': quiz_score or 65.0,
                'attendance': attendance or 80.0,
                'performance_level': 'Average'
            }
            learning_gaps = []
        
        # Generate recommendations
        recommendations = recommender.generate_recommendations(
            student_id=student_id,
            performance_data=performance_data,
            learning_gaps=learning_gaps
        )
        
        # Create study plan
        study_plan = recommender.create_study_plan(
            student_id=student_id,
            recommendations=recommendations,
            duration_weeks=4
        )
        
        return RecommendationResponse(
            student_id=student_id,
            recommendations=recommendations,
            study_plan=study_plan
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")


@app.post("/chatbot", response_model=ChatbotResponse)
async def chatbot_endpoint(request: ChatbotRequest):
    """
    Chatbot endpoint for educational assistance
    """
    try:
        # Get student context if available
        student_context = request.student_context
        
        # If student_id provided but no context, try to get from request
        if request.student_id and not student_context:
            # In production, fetch from database
            student_context = {
                'student_id': request.student_id,
                'subject': 'General',
                'quiz_score': 0,
                'attendance': 0,
                'performance_level': 'Average'
            }
        
        # Generate response
        chatbot_response = chatbot.generate_response(
            user_message=request.message,
            student_context=student_context
        )
        
        return ChatbotResponse(
            response=chatbot_response['response'],
            intent=chatbot_response['intent'],
            context_used=chatbot_response['context_used']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chatbot request: {str(e)}")


@app.get("/students/{student_id}/performance")
async def get_student_performance(student_id: str):
    """
    Get historical performance data for a student
    """
    try:
        if os.path.exists(dataset_path):
            df = pd.read_csv(dataset_path)
            student_data = df[df['student_id'] == student_id].to_dict('records')
            
            if student_data:
                return {
                    "student_id": student_id,
                    "performance_history": student_data
                }
            else:
                raise HTTPException(status_code=404, detail="Student not found")
        else:
            raise HTTPException(status_code=404, detail="Dataset not found")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching student data: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
