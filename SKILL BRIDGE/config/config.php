<?php
/**
 * SkillBridge Configuration File
 * Contains all application settings and database configuration
 */

// Database Configuration
define('DB_HOST', getenv('DB_HOST') ?: 'localhost');
define('DB_USER', getenv('DB_USER') ?: 'root');
define('DB_PASSWORD', getenv('DB_PASSWORD') ?: 'skillbridge2024');
define('DB_NAME', getenv('DB_NAME') ?: 'skillbridge_db');
define('DB_PORT', getenv('DB_PORT') ?: 3306);

// Application Environment
define('APP_ENV', getenv('PHP_ENV') ?: 'development');
define('APP_DEBUG', getenv('PHP_DEBUG') ?: true);
define('APP_ROOT', dirname(__DIR__));
define('APP_URL', 'http://localhost:8000');

// JWT Configuration
define('JWT_SECRET', getenv('JWT_SECRET') ?: 'your_jwt_secret_key_here');
define('JWT_EXPIRY', getenv('JWT_EXPIRY') ?: 86400);

// Session Configuration
define('SESSION_TIMEOUT', getenv('SESSION_TIMEOUT') ?: 3600);
define('SESSION_NAME', 'skillbridge_session');

// Blockchain Configuration
define('BLOCKCHAIN_NETWORK', getenv('BLOCKCHAIN_NETWORK') ?: 'testnet');
define('CONTRACT_ADDRESS', getenv('CONTRACT_ADDRESS') ?: '0x0000000000000000000000000000000000000000');

// ML Configuration
define('ML_MODEL_PATH', APP_ROOT . '/ml/models/');
define('ML_DATA_PATH', APP_ROOT . '/ml/data/');

// Supported Skills for ML Model
define('SUPPORTED_SKILLS', [
    'Python', 'Java', 'JavaScript', 'PHP', 'C++', 'C#', 'Ruby', 'Go',
    'Machine Learning', 'Data Science', 'Web Development', 'DevOps',
    'Database Design', 'Cloud Computing', 'Blockchain', 'Mobile Development'
]);

// Job Categories
define('JOB_CATEGORIES', [
    'Software Development', 'Data Science', 'Cloud Engineering',
    'DevOps', 'Web Development', 'Mobile Development', 'Blockchain'
]);

// Skill Levels
define('SKILL_LEVELS', [
    'Beginner' => 1,
    'Intermediate' => 2,
    'Advanced' => 3,
    'Expert' => 4
]);

// Error Reporting
if (APP_DEBUG) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(E_ALL);
    ini_set('display_errors', 0);
    ini_set('log_errors', 1);
}

// Timezone
date_default_timezone_set('UTC');
