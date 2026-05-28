"""
SkillBridge ML Data Preparation Module
Prepares data for model training and testing
"""

import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

class DataPreparation:
    """Handles data loading and preprocessing for ML models"""
    
    def __init__(self):
        self.skill_encoder = LabelEncoder()
        self.category_encoder = LabelEncoder()
        self.level_encoder = LabelEncoder()
        self.training_data = None
    
    def load_training_data(self, filepath):
        """Load training data from CSV"""
        try:
            self.training_data = pd.read_csv(filepath)
            return self.training_data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def encode_categorical_features(self, df):
        """Encode categorical features"""
        encoded_df = df.copy()
        
        # Encode skills, category, and levels
        if 'skill_name' in encoded_df.columns:
            encoded_df['skill_encoded'] = self.skill_encoder.fit_transform(encoded_df['skill_name'])
        
        if 'category' in encoded_df.columns:
            encoded_df['category_encoded'] = self.category_encoder.fit_transform(encoded_df['category'])
        
        if 'level' in encoded_df.columns:
            level_mapping = {
                'Beginner': 1,
                'Intermediate': 2,
                'Advanced': 3,
                'Expert': 4
            }
            encoded_df['level_encoded'] = encoded_df['level'].map(level_mapping)
        
        return encoded_df
    
    def create_feature_vectors(self, skills_list):
        """Create feature vector from skills list"""
        features = []
        for skill in skills_list:
            encoded = self.skill_encoder.transform([skill])[0]
            features.append(encoded)
        
        return np.array(features)
    
    def prepare_job_matching_data(self, user_skills, job_skills):
        """Prepare data for job matching"""
        user_set = set(user_skills)
        job_set = set(job_skills)
        
        # Calculate various similarity metrics
        jaccard_sim = len(user_set & job_set) / len(user_set | job_set)
        cosine_sim = self._cosine_similarity(user_skills, job_skills)
        
        return {
            'jaccard_similarity': jaccard_sim,
            'cosine_similarity': cosine_sim,
            'matched_count': len(user_set & job_set),
            'total_required': len(job_set)
        }
    
    def _cosine_similarity(self, list1, list2):
        """Calculate cosine similarity between two lists"""
        set1 = set(list1)
        set2 = set(list2)
        
        if len(set1) == 0 or len(set2) == 0:
            return 0
        
        intersection = len(set1 & set2)
        return intersection / (len(set1) * len(set2)) ** 0.5
    
    def generate_synthetic_data(self, num_samples=1000):
        """Generate synthetic training data"""
        skills = ['Python', 'Java', 'JavaScript', 'Machine Learning', 'Data Science']
        categories = ['Software Development', 'Data Science', 'Web Development']
        levels = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
        
        data = {
            'user_id': np.random.randint(1, 100, num_samples),
            'skill_name': np.random.choice(skills, num_samples),
            'level': np.random.choice(levels, num_samples),
            'years_experience': np.random.randint(0, 20, num_samples),
            'category': np.random.choice(categories, num_samples),
            'match_score': np.random.rand(num_samples) * 100
        }
        
        return pd.DataFrame(data)


# Initialize data preparation
data_prep = DataPreparation()
