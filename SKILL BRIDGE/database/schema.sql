-- SkillBridge Database Schema
-- MySQL Database for SkillBridge Platform

-- Create Database
CREATE DATABASE IF NOT EXISTS skillbridge_db;
USE skillbridge_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    profile_summary TEXT,
    profile_picture_url VARCHAR(500),
    phone_number VARCHAR(20),
    location VARCHAR(255),
    linkedin_profile VARCHAR(500),
    github_profile VARCHAR(500),
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_status (status)
);

-- User Skills Table
CREATE TABLE IF NOT EXISTS user_skills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    level ENUM('Beginner', 'Intermediate', 'Advanced', 'Expert') NOT NULL,
    years_experience INT DEFAULT 0,
    endorsements INT DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_skill (user_id, skill_name),
    INDEX idx_skill_level (skill_name, level)
);

-- Jobs Table
CREATE TABLE IF NOT EXISTS jobs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description LONGTEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    required_skills JSON NOT NULL,
    salary_range VARCHAR(100),
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    job_type ENUM('Full-time', 'Part-time', 'Contract', 'Remote') DEFAULT 'Full-time',
    experience_level ENUM('Entry', 'Mid', 'Senior') DEFAULT 'Mid',
    status ENUM('active', 'inactive', 'closed') DEFAULT 'active',
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_status (status),
    INDEX idx_company (company)
);

-- Job Recommendations Table
CREATE TABLE IF NOT EXISTS job_recommendations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    match_score DECIMAL(5, 2) NOT NULL,
    matched_skills JSON,
    missing_skills JSON,
    view_count INT DEFAULT 0,
    is_applied BOOLEAN DEFAULT FALSE,
    is_rejected BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    INDEX idx_user_job (user_id, job_id),
    INDEX idx_match_score (match_score)
);

-- Upskilling Paths Table
CREATE TABLE IF NOT EXISTS upskilling_paths (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    learning_resources JSON,
    estimated_duration_weeks INT,
    difficulty_level ENUM('Easy', 'Medium', 'Hard') DEFAULT 'Medium',
    status ENUM('not_started', 'in_progress', 'completed') DEFAULT 'not_started',
    progress_percentage INT DEFAULT 0,
    started_date DATETIME,
    completed_date DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_skill (user_id, skill_name)
);

-- Digital Certificates Table
CREATE TABLE IF NOT EXISTS digital_certificates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    certificate_hash VARCHAR(255) UNIQUE NOT NULL,
    blockchain_address VARCHAR(255),
    issuer VARCHAR(255) NOT NULL,
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date DATE,
    verification_url VARCHAR(500),
    is_verified BOOLEAN DEFAULT FALSE,
    verification_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_certificate_hash (certificate_hash),
    INDEX idx_blockchain_address (blockchain_address)
);

-- Skill Gap Analysis Table
CREATE TABLE IF NOT EXISTS skill_gap_analysis (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    target_job_id INT NOT NULL,
    matched_skills JSON,
    missing_skills JSON,
    match_percentage DECIMAL(5, 2),
    gap_analysis JSON,
    recommendation_priority JSON,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (target_job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    INDEX idx_user_job (user_id, target_job_id)
);

-- Applications Table
CREATE TABLE IF NOT EXISTS job_applications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    resume_file_path VARCHAR(500),
    cover_letter TEXT,
    application_status ENUM('submitted', 'reviewed', 'shortlisted', 'rejected', 'offered') DEFAULT 'submitted',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at DATETIME,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    UNIQUE KEY unique_application (user_id, job_id),
    INDEX idx_status (application_status)
);

-- ML Model Training Log Table
CREATE TABLE IF NOT EXISTS ml_training_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    model_name VARCHAR(100) NOT NULL,
    training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accuracy DECIMAL(5, 4),
    precision DECIMAL(5, 4),
    recall DECIMAL(5, 4),
    f1_score DECIMAL(5, 4),
    training_samples INT,
    execution_time_seconds DECIMAL(8, 2),
    status ENUM('success', 'failed', 'in_progress') DEFAULT 'in_progress',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_model_name (model_name),
    INDEX idx_training_date (training_date)
);

-- Create Indexes for Performance
CREATE INDEX idx_user_skills_user ON user_skills(user_id);
CREATE INDEX idx_job_recommendations_user ON job_recommendations(user_id);
CREATE INDEX idx_job_applications_user ON job_applications(user_id);
CREATE INDEX idx_certificates_user ON digital_certificates(user_id);
