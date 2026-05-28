"""
Flask API Server for ML Models
Provides endpoints for skill and job recommendations
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.skill_recommender import skill_recommendation_engine
from models.job_recommender import job_recommendation_engine

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JSON_SORT_KEYS'] = False

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'ML API Server is running'}), 200

@app.route('/api/recommend/skills', methods=['POST'])
def recommend_skills():
    """
    Recommend skills based on user's current skills
    
    Request body:
    {
        "user_skills": ["Python", "JavaScript"],
        "current_level": 2
    }
    """
    try:
        data = request.get_json()
        user_skills = data.get('user_skills', [])
        
        if not user_skills:
            return jsonify({'status': 'error', 'message': 'user_skills required'}), 400
        
        recommendations = skill_recommendation_engine.recommend_skills(user_skills)
        
        return jsonify({
            'status': 'success',
            'data': recommendations
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/recommend/jobs', methods=['POST'])
def recommend_jobs():
    """
    Recommend jobs based on user skills
    
    Request body:
    {
        "user_skills": ["Python", "Machine Learning"],
        "top_n": 5
    }
    """
    try:
        data = request.get_json()
        user_skills = data.get('user_skills', [])
        top_n = data.get('top_n', 5)
        
        if not user_skills:
            return jsonify({'status': 'error', 'message': 'user_skills required'}), 400
        
        recommendations = job_recommendation_engine.recommend_jobs(user_skills, top_n)
        
        return jsonify({
            'status': 'success',
            'data': recommendations
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/skill-gap', methods=['POST'])
def calculate_skill_gap():
    """
    Calculate skill gap for a target job
    
    Request body:
    {
        "user_skills": ["Python"],
        "target_job_skills": ["Python", "Machine Learning", "Data Science"]
    }
    """
    try:
        data = request.get_json()
        user_skills = data.get('user_skills', [])
        target_job_skills = data.get('target_job_skills', [])
        
        if not user_skills or not target_job_skills:
            return jsonify({'status': 'error', 'message': 'user_skills and target_job_skills required'}), 400
        
        gap_analysis = skill_recommendation_engine.calculate_skill_gap(user_skills, target_job_skills)
        
        return jsonify({
            'status': 'success',
            'data': gap_analysis
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/job/<int:job_id>', methods=['GET'])
def get_job_details(job_id):
    """Get details of a specific job"""
    try:
        job = job_recommendation_engine.get_job_details(job_id)
        
        if not job:
            return jsonify({'status': 'error', 'message': 'Job not found'}), 404
        
        return jsonify({
            'status': 'success',
            'data': job
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """
    Main recommendation endpoint that combines job and skill recommendations
    
    Request body:
    {
        "user_id": 1,
        "user_skills": ["Python", "Web Development"],
        "include_skill_gaps": true
    }
    """
    try:
        data = request.get_json()
        user_skills = data.get('user_skills', [])
        include_skill_gaps = data.get('include_skill_gaps', False)
        
        if not user_skills:
            return jsonify({'status': 'error', 'message': 'user_skills required'}), 400
        
        # Get job recommendations
        job_recommendations = job_recommendation_engine.recommend_jobs(user_skills, top_n=10)
        
        # Get skill recommendations
        skill_recommendations = skill_recommendation_engine.recommend_skills(user_skills)
        
        response = {
            'status': 'success',
            'job_recommendations': job_recommendations,
            'skill_recommendations': skill_recommendations
        }
        
        # Add skill gaps if requested
        if include_skill_gaps and job_recommendations:
            top_job = job_recommendations[0]
            gap_analysis = skill_recommendation_engine.calculate_skill_gap(
                user_skills,
                top_job['required_skills']
            )
            response['skill_gap_analysis'] = gap_analysis
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting SkillBridge ML API Server...")
    print("Available endpoints:")
    print("  GET  /health")
    print("  POST /api/recommend/skills")
    print("  POST /api/recommend/jobs")
    print("  POST /api/skill-gap")
    print("  GET  /api/job/<job_id>")
    print("  POST /api/recommend")
    print("\nServer running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
