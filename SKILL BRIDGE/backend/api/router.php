<?php
/**
 * SkillBridge API Router
 * Handles all API endpoints
 */

require_once __DIR__ . '/../config/config.php';

// Load all models and controllers
require_once __DIR__ . '/../models/Database.php';
require_once __DIR__ . '/../models/User.php';
require_once __DIR__ . '/../models/Skill.php';
require_once __DIR__ . '/../models/JobRecommendation.php';

require_once __DIR__ . '/../controllers/AuthController.php';
require_once __DIR__ . '/../controllers/SkillController.php';
require_once __DIR__ . '/../controllers/JobRecommendationController.php';

// Initialize database connection
$database = new Database();
$db = $database->connect();

// Set response header
header('Content-Type: application/json');

// Get request method and path
$method = $_SERVER['REQUEST_METHOD'];
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$path = str_replace('/api', '', $path);

// Route the requests
try {
    switch ($path) {
        // Authentication routes
        case '/auth/register':
            $controller = new AuthController($db);
            $response = $controller->register();
            break;

        case '/auth/login':
            $controller = new AuthController($db);
            $response = $controller->login();
            break;

        // Skill routes
        case '/skills/add':
            $controller = new SkillController($db);
            $response = $controller->addSkill();
            break;

        case preg_match('/\/skills\/user\/(\d+)/', $path, $matches) ? true : false:
            $user_id = $matches[1];
            $controller = new SkillController($db);
            $response = $controller->getUserSkills($user_id);
            break;

        // Job Recommendation routes
        case '/jobs/all':
            $controller = new JobRecommendationController($db);
            $response = $controller->getAllJobs();
            break;

        case preg_match('/\/jobs\/category\/(.+)/', $path, $matches) ? true : false:
            $category = urldecode($matches[1]);
            $controller = new JobRecommendationController($db);
            $response = $controller->getJobsByCategory($category);
            break;

        case preg_match('/\/recommendations\/user\/(\d+)/', $path, $matches) ? true : false:
            $user_id = $matches[1];
            $controller = new JobRecommendationController($db);
            $response = $controller->getRecommendations($user_id);
            break;

        case preg_match('/\/recommendations\/generate\/(\d+)/', $path, $matches) ? true : false:
            $user_id = $matches[1];
            $controller = new JobRecommendationController($db);
            $response = $controller->generateRecommendations($user_id);
            break;

        default:
            $response = ['status' => 'error', 'message' => 'Endpoint not found'];
            http_response_code(404);
    }
} catch (Exception $e) {
    $response = ['status' => 'error', 'message' => $e->getMessage()];
    http_response_code(500);
}

echo json_encode($response);
$database->close();
