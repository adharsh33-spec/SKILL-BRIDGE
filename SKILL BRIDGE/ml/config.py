"""
SkillBridge ML Module
Main configuration and initialization for ML components
"""

import os
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

# ML Configuration
ML_MODEL_PATH = os.getenv('ML_MODEL_PATH', './ml/models/')
ML_DATA_PATH = os.getenv('ML_DATA_PATH', './ml/data/')
RANDOM_STATE = int(os.getenv('SKLEARN_RANDOM_STATE', '42'))

# Supported Skills
SUPPORTED_SKILLS = [
    'Python', 'Java', 'JavaScript', 'PHP', 'C++', 'C#', 'Ruby', 'Go',
    'Machine Learning', 'Data Science', 'Web Development', 'DevOps',
    'Database Design', 'Cloud Computing', 'Blockchain', 'Mobile Development'
]

# Job Categories
JOB_CATEGORIES = [
    'Software Development', 'Data Science', 'Cloud Engineering',
    'DevOps', 'Web Development', 'Mobile Development', 'Blockchain'
]

class MLModelManager:
    """Manages ML model loading and inference"""
    
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models"""
        try:
            if os.path.exists(f'{ML_MODEL_PATH}job_recommendation_model.pkl'):
                self.models['job_recommendation'] = joblib.load(f'{ML_MODEL_PATH}job_recommendation_model.pkl')
            if os.path.exists(f'{ML_MODEL_PATH}scaler.pkl'):
                self.scaler = joblib.load(f'{ML_MODEL_PATH}scaler.pkl')
        except Exception as e:
            print(f"Error loading models: {e}")
    
    def train_job_recommendation_model(self, X_train, y_train):
        """Train job recommendation model"""
        model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
        model.fit(X_train, y_train)
        self.models['job_recommendation'] = model
        joblib.dump(model, f'{ML_MODEL_PATH}job_recommendation_model.pkl')
        return model
    
    def predict_job_recommendation(self, user_features):
        """Predict job recommendations for a user"""
        if 'job_recommendation' not in self.models:
            return None
        
        scaled_features = self.scaler.transform([user_features])
        prediction = self.models['job_recommendation'].predict(scaled_features)
        probabilities = self.models['job_recommendation'].predict_proba(scaled_features)
        
        return {
            'prediction': int(prediction[0]),
            'probabilities': probabilities[0].tolist()
        }

# Global model manager instance
ml_manager = MLModelManager()
