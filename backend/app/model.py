"""
ML Model for Student Performance Analysis
Uses RandomForest Classifier to identify learning gaps
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os


class StudentPerformanceModel:
    """ML model for analyzing student performance and identifying learning gaps"""
    
    def __init__(self, model_path='model.pkl'):
        self.model = None
        self.label_encoders = {}
        self.model_path = model_path
        self.feature_columns = ['quiz_score', 'attendance', 'subject_encoded']
        
    def prepare_data(self, df):
        """Preprocess the dataset for training"""
        df = df.copy()
        
        # Encode categorical variables
        if 'subject' in df.columns:
            le_subject = LabelEncoder()
            df['subject_encoded'] = le_subject.fit_transform(df['subject'])
            self.label_encoders['subject'] = le_subject
        
        # Create performance level if not exists
        if 'performance_level' not in df.columns:
            df['performance_level'] = df['quiz_score'].apply(self._categorize_performance)
        
        # Encode performance level
        if 'performance_level' in df.columns:
            le_performance = LabelEncoder()
            df['performance_encoded'] = le_performance.fit_transform(df['performance_level'])
            self.label_encoders['performance'] = le_performance
        
        return df
    
    def _categorize_performance(self, score):
        """Categorize performance based on quiz score"""
        if score >= 80:
            return 'Excellent'
        elif score >= 70:
            return 'Good'
        elif score >= 60:
            return 'Average'
        elif score >= 50:
            return 'Below Average'
        else:
            return 'Poor'
    
    def train(self, df):
        """Train the RandomForest model"""
        df_processed = self.prepare_data(df)
        
        # Features
        X = df_processed[self.feature_columns]
        
        # Target
        y = df_processed['performance_encoded']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Calculate accuracy
        accuracy = self.model.score(X_test, y_test)
        print(f"Model trained with accuracy: {accuracy:.2%}")
        
        return accuracy
    
    def predict(self, student_data):
        """Predict performance level for a student"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Prepare input data
        input_data = pd.DataFrame([student_data])
        
        # Encode subject if needed
        if 'subject' in input_data.columns:
            if 'subject' in self.label_encoders:
                input_data['subject_encoded'] = self.label_encoders['subject'].transform(
                    input_data['subject']
                )
            else:
                raise ValueError("Subject encoder not found. Train model first.")
        
        # Ensure all feature columns exist
        for col in self.feature_columns:
            if col not in input_data.columns:
                raise ValueError(f"Missing required feature: {col}")
        
        # Predict
        prediction_encoded = self.model.predict(input_data[self.feature_columns])[0]
        
        # Decode prediction
        if 'performance' in self.label_encoders:
            performance_level = self.label_encoders['performance'].inverse_transform(
                [prediction_encoded]
            )[0]
        else:
            performance_level = self._categorize_performance(student_data.get('quiz_score', 0))
        
        # Get feature importance for explanation
        feature_importance = dict(zip(
            self.feature_columns,
            self.model.feature_importances_
        ))
        
        return {
            'performance_level': performance_level,
            'prediction_confidence': float(max(self.model.predict_proba(input_data[self.feature_columns])[0])),
            'feature_importance': feature_importance
        }
    
    def identify_learning_gaps(self, student_data, threshold=60):
        """Identify specific learning gaps based on performance"""
        gaps = []
        
        quiz_score = student_data.get('quiz_score', 0)
        attendance = student_data.get('attendance', 0)
        subject = student_data.get('subject', 'Unknown')
        
        if quiz_score < threshold:
            gaps.append({
                'type': 'Low Quiz Score',
                'subject': subject,
                'severity': 'High' if quiz_score < 50 else 'Medium',
                'description': f'Quiz score of {quiz_score}% indicates difficulty understanding {subject} concepts'
            })
        
        if attendance < 75:
            gaps.append({
                'type': 'Low Attendance',
                'subject': subject,
                'severity': 'High' if attendance < 60 else 'Medium',
                'description': f'Attendance rate of {attendance}% may be affecting learning outcomes'
            })
        
        return gaps
    
    def save_model(self):
        """Save the trained model and encoders"""
        if self.model is None:
            raise ValueError("No model to save. Train model first.")
        
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns
        }
        
        joblib.dump(model_data, self.model_path)
        print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load a previously trained model"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        
        model_data = joblib.load(self.model_path)
        self.model = model_data['model']
        self.label_encoders = model_data['label_encoders']
        self.feature_columns = model_data['feature_columns']
        print(f"Model loaded from {self.model_path}")
