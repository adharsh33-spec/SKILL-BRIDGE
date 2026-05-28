<?php
/**
 * Skill Model
 * Handles user skills database operations
 */

class Skill {
    private $db;

    public function __construct($db) {
        $this->db = $db;
    }

    public function addSkill($skill_data) {
        $stmt = $this->db->prepare("INSERT INTO user_skills (user_id, skill_name, level, years_experience, created_at) VALUES (?, ?, ?, ?, NOW())");
        $stmt->bind_param("issi", $skill_data['user_id'], $skill_data['skill_name'], $skill_data['level'], $skill_data['years_experience']);
        return $stmt->execute();
    }

    public function getUserSkills($user_id) {
        $stmt = $this->db->prepare("SELECT * FROM user_skills WHERE user_id = ?");
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        return $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    }

    public function updateSkill($skill_id, $skill_data) {
        $stmt = $this->db->prepare("UPDATE user_skills SET level=?, years_experience=?, updated_at=NOW() WHERE id=?");
        $stmt->bind_param("sii", $skill_data['level'], $skill_data['years_experience'], $skill_id);
        return $stmt->execute();
    }

    public function deleteSkill($skill_id) {
        $stmt = $this->db->prepare("DELETE FROM user_skills WHERE id = ?");
        $stmt->bind_param("i", $skill_id);
        return $stmt->execute();
    }

    public function getSkillStats($skill_name) {
        $stmt = $this->db->prepare("SELECT COUNT(*) as count, AVG(level) as avg_level FROM user_skills WHERE skill_name = ?");
        $stmt->bind_param("s", $skill_name);
        $stmt->execute();
        return $stmt->get_result()->fetch_assoc();
    }
}
