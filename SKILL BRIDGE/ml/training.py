"""
SkillBridge ML Training Module
Handles model training and evaluation
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from datetime import datetime
import joblib

class ModelTrainer:
    """Trains and evaluates ML models"""
    
    def __init__(self):
        self.models = {}
        self.training_history = []
    
    def train_recommendation_model(self, X, y, test_size=0.2, random_state=42):
        """
        Train job recommendation model
        
        Args:
            X: Feature matrix
            y: Target labels
            test_size: Test set size ratio
            random_state: Random seed
        
        Returns:
            Dictionary with training metrics
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=random_state,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        metrics = self._calculate_metrics(y_test, y_pred)
        
        # Store model
        self.models['recommendation'] = model
        
        # Log training
        self._log_training('job_recommendation', metrics, len(X_train))
        
        return metrics
    
    def _calculate_metrics(self, y_true, y_pred):
        """Calculate evaluation metrics"""
        return {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_true, y_pred, average='weighted', zero_division=0)
        }
    
    def _log_training(self, model_name, metrics, training_samples):
        """Log training details"""
        log_entry = {
            'model_name': model_name,
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'training_samples': training_samples
        }
        self.training_history.append(log_entry)
    
    def save_model(self, model_name, filepath):
        """Save trained model"""
        if model_name in self.models:
            joblib.dump(self.models[model_name], filepath)
            return True
        return False
    
    def load_model(self, model_name, filepath):
        """Load trained model"""
        try:
            self.models[model_name] = joblib.load(filepath)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def get_feature_importance(self, model_name):
        """Get feature importance from model"""
        if model_name in self.models:
            model = self.models[model_name]
            if hasattr(model, 'feature_importances_'):
                return model.feature_importances_
        return None
    
    def get_training_history(self):
        """Get training history"""
        return self.training_history


# Initialize model trainer
model_trainer = ModelTrainer()
