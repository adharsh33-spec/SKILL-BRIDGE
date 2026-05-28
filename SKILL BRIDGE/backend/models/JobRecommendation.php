<?php
/**
 * Job Recommendation Model
 * Handles job matching and recommendations
 */

class JobRecommendation {
    private $db;

    public function __construct($db) {
        $this->db = $db;
    }

    public function getAllJobs() {
        $result = $this->db->query("SELECT * FROM jobs WHERE status = 'active'");
        return $result->fetch_all(MYSQLI_ASSOC);
    }

    public function getJobById($job_id) {
        $stmt = $this->db->prepare("SELECT * FROM jobs WHERE id = ?");
        $stmt->bind_param("i", $job_id);
        $stmt->execute();
        return $stmt->get_result()->fetch_assoc();
    }

    public function getJobsByCategory($category) {
        $stmt = $this->db->prepare("SELECT * FROM jobs WHERE category = ? AND status = 'active'");
        $stmt->bind_param("s", $category);
        $stmt->execute();
        return $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    }

    public function saveRecommendation($user_id, $job_id, $match_score) {
        $stmt = $this->db->prepare("INSERT INTO job_recommendations (user_id, job_id, match_score, created_at) VALUES (?, ?, ?, NOW())");
        $stmt->bind_param("iid", $user_id, $job_id, $match_score);
        return $stmt->execute();
    }

    public function getUserRecommendations($user_id) {
        $sql = "SELECT j.*, r.match_score FROM jobs j 
                INNER JOIN job_recommendations r ON j.id = r.job_id 
                WHERE r.user_id = ? ORDER BY r.match_score DESC";
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        return $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    }

    public function addJob($job_data) {
        $stmt = $this->db->prepare("INSERT INTO jobs (title, description, category, required_skills, salary_range, company, status, created_at) VALUES (?, ?, ?, ?, ?, ?, 'active', NOW())");
        $stmt->bind_param("ssssss", $job_data['title'], $job_data['description'], $job_data['category'], $job_data['required_skills'], $job_data['salary_range'], $job_data['company']);
        return $stmt->execute();
    }
}
