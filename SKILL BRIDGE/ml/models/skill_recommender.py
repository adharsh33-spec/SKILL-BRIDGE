"""
Skill Recommendation Engine
ML module for recommending skills and upskilling paths
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

class SkillRecommendationEngine:
    """Recommends skills based on job market demands"""
    
    def __init__(self):
        # Define skill relationships and demand
        self.skill_relationships = {
            'Python': ['Machine Learning', 'Data Science', 'Web Development'],
            'Java': ['Web Development', 'Cloud Computing'],
            'JavaScript': ['Web Development', 'Mobile Development'],
            'Machine Learning': ['Python', 'Data Science', 'C++'],
            'Data Science': ['Python', 'Machine Learning', 'Database Design'],
            'Web Development': ['JavaScript', 'PHP', 'Database Design'],
            'Cloud Computing': ['DevOps', 'Java', 'C#'],
            'DevOps': ['Cloud Computing', 'Go', 'Database Design'],
            'Blockchain': ['C++', 'Go', 'Java'],
            'Mobile Development': ['JavaScript', 'Java', 'C#']
        }
        
        self.skill_demand_score = {
            'Machine Learning': 9.5,
            'Data Science': 9.2,
            'Cloud Computing': 9.0,
            'Python': 8.8,
            'DevOps': 8.5,
            'Blockchain': 8.2,
            'Web Development': 8.0,
            'Java': 7.8,
            'JavaScript': 7.6,
            'Mobile Development': 7.4
        }
    
    def recommend_skills(self, user_skills, current_level=None):
        """
        Recommend upskilling paths based on current skills
        
        Args:
            user_skills: List of user's current skills
            current_level: Optional minimum demand level
        
        Returns:
            List of recommended skills sorted by relevance
        """
        recommendations = []
        recommended_set = set()
        
        # Get related skills from current skills
        for skill in user_skills:
            if skill in self.skill_relationships:
                for related_skill in self.skill_relationships[skill]:
                    if related_skill not in user_skills and related_skill not in recommended_set:
                        demand_score = self.skill_demand_score.get(related_skill, 5.0)
                        recommendations.append({
                            'skill': related_skill,
                            'reason': f'Related to {skill}',
                            'demand_score': demand_score,
                            'learning_path': self._get_learning_path(related_skill)
                        })
                        recommended_set.add(related_skill)
        
        # Sort by demand score
        recommendations = sorted(recommendations, key=lambda x: x['demand_score'], reverse=True)
        
        return recommendations[:10]  # Return top 10 recommendations
    
    def _get_learning_path(self, skill):
        """Get learning resources for a skill"""
        learning_paths = {
            'Python': ['Codecademy', 'DataCamp', 'Coursera'],
            'Machine Learning': ['Coursera ML Specialization', 'Fast.ai', 'Kaggle'],
            'Data Science': ['DataCamp', 'Coursera', 'edX'],
            'Cloud Computing': ['AWS Training', 'Azure Learning', 'Google Cloud Skills'],
            'DevOps': ['Linux Academy', 'A Cloud Guru', 'Udemy DevOps'],
            'Blockchain': ['Udemy Blockchain', 'Coursera Blockchain', 'CryptoZombies']
        }
        return learning_paths.get(skill, ['Udemy', 'Coursera', 'edX'])
    
    def calculate_skill_gap(self, user_skills, target_job_skills):
        """
        Calculate skill gap between user and target job
        
        Args:
            user_skills: List of user skills
            target_job_skills: List of required job skills
        
        Returns:
            Dictionary with gap analysis
        """
        user_set = set(user_skills)
        target_set = set(target_job_skills)
        
        missing_skills = target_set - user_set
        surplus_skills = user_set - target_set
        matched_skills = user_set & target_set
        
        gap_percentage = (len(missing_skills) / len(target_set) * 100) if target_set else 0
        
        return {
            'matched_skills': list(matched_skills),
            'missing_skills': list(missing_skills),
            'surplus_skills': list(surplus_skills),
            'match_percentage': 100 - gap_percentage,
            'gap_percentage': gap_percentage,
            'learning_priority': sorted(missing_skills, 
                                      key=lambda x: self.skill_demand_score.get(x, 5.0), 
                                      reverse=True)
        }


# Initialize the recommendation engine
skill_recommendation_engine = SkillRecommendationEngine()
