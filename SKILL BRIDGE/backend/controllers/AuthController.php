<?php
/**
 * Authentication Controller
 * Handles user registration and login
 */

class AuthController {
    private $db;

    public function __construct($db) {
        $this->db = $db;
    }

    public function register() {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            return ['status' => 'error', 'message' => 'Invalid request method'];
        }

        $data = json_decode(file_get_contents("php://input"), true);

        // Validate input
        if (!isset($data['email'], $data['password'], $data['full_name'])) {
            return ['status' => 'error', 'message' => 'Missing required fields'];
        }

        // Check if user exists
        $user_model = new User($this->db);
        if ($user_model->getByEmail($data['email'])) {
            return ['status' => 'error', 'message' => 'User already exists'];
        }

        // Hash password
        $hashed_password = password_hash($data['password'], PASSWORD_BCRYPT);

        // Create user
        $user_data = [
            'email' => $data['email'],
            'password' => $hashed_password,
            'full_name' => $data['full_name']
        ];

        if ($user_model->create($user_data)) {
            return ['status' => 'success', 'message' => 'User registered successfully'];
        } else {
            return ['status' => 'error', 'message' => 'Registration failed'];
        }
    }

    public function login() {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            return ['status' => 'error', 'message' => 'Invalid request method'];
        }

        $data = json_decode(file_get_contents("php://input"), true);

        if (!isset($data['email'], $data['password'])) {
            return ['status' => 'error', 'message' => 'Missing email or password'];
        }

        $user_model = new User($this->db);
        $user = $user_model->getByEmail($data['email']);

        if (!$user || !password_verify($data['password'], $user['password'])) {
            return ['status' => 'error', 'message' => 'Invalid credentials'];
        }

        // Generate JWT Token
        $token = $this->generateJWT($user['id']);

        return [
            'status' => 'success',
            'message' => 'Login successful',
            'token' => $token,
            'user' => [
                'id' => $user['id'],
                'email' => $user['email'],
                'full_name' => $user['full_name']
            ]
        ];
    }

    private function generateJWT($user_id) {
        $header = json_encode(['alg' => 'HS256', 'typ' => 'JWT']);
        $payload = json_encode([
            'user_id' => $user_id,
            'iat' => time(),
            'exp' => time() + JWT_EXPIRY
        ]);

        $header_encoded = rtrim(strtr(base64_encode($header), '+/', '-_'), '=');
        $payload_encoded = rtrim(strtr(base64_encode($payload), '+/', '-_'), '=');

        $signature = hash_hmac('sha256', "$header_encoded.$payload_encoded", JWT_SECRET, true);
        $signature_encoded = rtrim(strtr(base64_encode($signature), '+/', '-_'), '=');

        return "$header_encoded.$payload_encoded.$signature_encoded";
    }
}
