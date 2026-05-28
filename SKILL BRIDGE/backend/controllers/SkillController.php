<?php
/**
 * Skill Controller
 * Handles skill management endpoints
 */

class SkillController {
    private $db;

    public function __construct($db) {
        $this->db = $db;
    }

    public function addSkill() {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            return ['status' => 'error', 'message' => 'Invalid request method'];
        }

        $data = json_decode(file_get_contents("php://input"), true);

        if (!isset($data['user_id'], $data['skill_name'], $data['level'])) {
            return ['status' => 'error', 'message' => 'Missing required fields'];
        }

        $skill_model = new Skill($this->db);
        $skill_data = [
            'user_id' => $data['user_id'],
            'skill_name' => $data['skill_name'],
            'level' => $data['level'],
            'years_experience' => $data['years_experience'] ?? 0
        ];

        if ($skill_model->addSkill($skill_data)) {
            return ['status' => 'success', 'message' => 'Skill added successfully'];
        } else {
            return ['status' => 'error', 'message' => 'Failed to add skill'];
        }
    }

    public function getUserSkills($user_id) {
        $skill_model = new Skill($this->db);
        $skills = $skill_model->getUserSkills($user_id);
        return ['status' => 'success', 'data' => $skills];
    }

    public function updateSkill($skill_id) {
        if ($_SERVER['REQUEST_METHOD'] !== 'PUT') {
            return ['status' => 'error', 'message' => 'Invalid request method'];
        }

        $data = json_decode(file_get_contents("php://input"), true);

        $skill_model = new Skill($this->db);
        if ($skill_model->updateSkill($skill_id, $data)) {
            return ['status' => 'success', 'message' => 'Skill updated successfully'];
        } else {
            return ['status' => 'error', 'message' => 'Failed to update skill'];
        }
    }

    public function deleteSkill($skill_id) {
        if ($_SERVER['REQUEST_METHOD'] !== 'DELETE') {
            return ['status' => 'error', 'message' => 'Invalid request method'];
        }

        $skill_model = new Skill($this->db);
        if ($skill_model->deleteSkill($skill_id)) {
            return ['status' => 'success', 'message' => 'Skill deleted successfully'];
        } else {
            return ['status' => 'error', 'message' => 'Failed to delete skill'];
        }
    }
}
