<?php
/**
 * User Model
 * Handles user database operations
 */

class User {
    private $db;

    public function __construct($db) {
        $this->db = $db;
    }

    public function create($user_data) {
        $stmt = $this->db->prepare("INSERT INTO users (email, password, full_name, created_at) VALUES (?, ?, ?, NOW())");
        $stmt->bind_param("sss", $user_data['email'], $user_data['password'], $user_data['full_name']);
        return $stmt->execute();
    }

    public function getById($id) {
        $stmt = $this->db->prepare("SELECT * FROM users WHERE id = ?");
        $stmt->bind_param("i", $id);
        $stmt->execute();
        return $stmt->get_result()->fetch_assoc();
    }

    public function getByEmail($email) {
        $stmt = $this->db->prepare("SELECT * FROM users WHERE email = ?");
        $stmt->bind_param("s", $email);
        $stmt->execute();
        return $stmt->get_result()->fetch_assoc();
    }

    public function update($id, $user_data) {
        $stmt = $this->db->prepare("UPDATE users SET full_name=?, profile_summary=?, updated_at=NOW() WHERE id=?");
        $stmt->bind_param("ssi", $user_data['full_name'], $user_data['profile_summary'], $id);
        return $stmt->execute();
    }

    public function getAllUsers() {
        $result = $this->db->query("SELECT id, email, full_name, created_at FROM users");
        return $result->fetch_all(MYSQLI_ASSOC);
    }

    public function delete($id) {
        $stmt = $this->db->prepare("DELETE FROM users WHERE id = ?");
        $stmt->bind_param("i", $id);
        return $stmt->execute();
    }
}
