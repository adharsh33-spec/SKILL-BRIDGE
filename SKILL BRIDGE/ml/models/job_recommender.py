"""
Job Recommendation Engine
ML module for matching jobs with user skills
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import json

class JobRecommendationEngine:
    """Recommends jobs based on user skills"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 2))
        self.scaler = MinMaxScaler()
        
        # Sample job database
        self.jobs_database = [
            {
                'id': 1,
                'title': 'Python Developer',
                'skills': ['Python', 'Web Development', 'Database Design'],
                'category': 'Software Development',
                'salary_range': '80000-120000'
            },
            {
                'id': 2,
                'title': 'Machine Learning Engineer',
                'skills': ['Python', 'Machine Learning', 'Data Science'],
                'category': 'Data Science',
                'salary_range': '100000-150000'
            },
            {
                'id': 3,
                'title': 'Cloud Architect',
                'skills': ['Cloud Computing', 'DevOps', 'Java'],
                'category': 'Cloud Engineering',
                'salary_range': '120000-160000'
            },
            {
                'id': 4,
                'title': 'Blockchain Developer',
                'skills': ['Blockchain', 'C++', 'Go'],
                'category': 'Blockchain',
                'salary_range': '110000-180000'
            },
            {
                'id': 5,
                'title': 'Full Stack Developer',
                'skills': ['JavaScript', 'Web Development', 'Database Design'],
                'category': 'Web Development',
                'salary_range': '75000-110000'
            }
        ]
    
    def recommend_jobs(self, user_skills, top_n=5):
        """
        Recommend jobs based on user skills
        
        Args:
            user_skills: List of user skills
            top_n: Number of top recommendations to return
        
        Returns:
            List of recommended jobs with match scores
        """
        recommendations = []
        user_skills_str = ' '.join(user_skills).lower()
        
        for job in self.jobs_database:
            job_skills_str = ' '.join(job['skills']).lower()
            
            # Calculate skill match
            match_score = self._calculate_match_score(user_skills, job['skills'])
            
            recommendations.append({
                'job_id': job['id'],
                'title': job['title'],
                'category': job['category'],
                'required_skills': job['skills'],
                'salary_range': job['salary_range'],
                'match_score': match_score,
                'matched_skills': [s for s in user_skills if s in job['skills']],
                'missing_skills': [s for s in job['skills'] if s not in user_skills]
            })
        
        # Sort by match score
        recommendations = sorted(recommendations, key=lambda x: x['match_score'], reverse=True)
        
        return recommendations[:top_n]
    
    def _calculate_match_score(self, user_skills, job_skills):
        """
        Calculate match score between user skills and job skills
        
        Args:
            user_skills: List of user skills
            job_skills: List of required job skills
        
        Returns:
            Match score (0-100)
        """
        if not job_skills:
            return 0
        
        user_set = set(s.lower() for s in user_skills)
        job_set = set(s.lower() for s in job_skills)
        
        if not job_set:
            return 0
        
        # Calculate Jaccard similarity
        intersection = len(user_set & job_set)
        union = len(user_set | job_set)
        
        jaccard_similarity = intersection / union if union > 0 else 0
        
        # Normalize to 0-100
        match_score = jaccard_similarity * 100
        
        return round(match_score, 2)
    
    def get_job_details(self, job_id):
        """Get details of a specific job"""
        for job in self.jobs_database:
            if job['id'] == job_id:
                return job
        return None
    
    def add_job(self, job_data):
        """Add a new job to the database"""
        new_id = max([j['id'] for j in self.jobs_database]) + 1
        job_data['id'] = new_id
        self.jobs_database.append(job_data)
        return job_data


# Initialize the recommendation engine
job_recommendation_engine = JobRecommendationEngine()
