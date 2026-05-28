<?php
/**
 * Job Recommendation Controller
 * Handles job recommendation endpoints
 */

class JobRecommendationController {
    private $db;
    private $ml_service;

    public function __construct($db, $ml_service = null) {
        $this->db = $db;
        $this->ml_service = $ml_service;
    }

    public function getRecommendations($user_id) {
        $job_model = new JobRecommendation($this->db);
        $recommendations = $job_model->getUserRecommendations($user_id);

        return [
            'status' => 'success',
            'data' => $recommendations
        ];
    }

    public function getAllJobs() {
        $job_model = new JobRecommendation($this->db);
        $jobs = $job_model->getAllJobs();

        return [
            'status' => 'success',
            'data' => $jobs
        ];
    }

    public function getJobsByCategory($category) {
        $job_model = new JobRecommendation($this->db);
        $jobs = $job_model->getJobsByCategory($category);

        return [
            'status' => 'success',
            'data' => $jobs
        ];
    }

    public function generateRecommendations($user_id) {
        $skill_model = new Skill($this->db);
        $user_skills = $skill_model->getUserSkills($user_id);

        if (empty($user_skills)) {
            return ['status' => 'error', 'message' => 'User has no skills added'];
        }

        // Call ML model to get recommendations
        $recommendations = $this->callMLModel($user_id, $user_skills);

        return [
            'status' => 'success',
            'message' => 'Recommendations generated',
            'data' => $recommendations
        ];
    }

    private function callMLModel($user_id, $user_skills) {
        // This will call the Python ML model via API
        $python_api_url = 'http://localhost:5000/api/recommend';
        
        $data = [
            'user_id' => $user_id,
            'skills' => $user_skills
        ];

        $options = [
            'http' => [
                'method' => 'POST',
                'header' => 'Content-Type: application/json',
                'content' => json_encode($data)
            ]
        ];

        $context = stream_context_create($options);
        $response = @file_get_contents($python_api_url, false, $context);

        if ($response === false) {
            return ['error' => 'ML service unavailable'];
        }

        return json_decode($response, true);
    }
}
