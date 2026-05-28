/* Sample data for SkillBridge ML Models */

-- Insert sample users
INSERT INTO users (email, password, full_name) VALUES
('john@example.com', PASSWORD('password123'), 'John Doe'),
('jane@example.com', PASSWORD('password123'), 'Jane Smith'),
('mike@example.com', PASSWORD('password123'), 'Mike Johnson');

-- Insert sample skills for users
INSERT INTO user_skills (user_id, skill_name, level, years_experience) VALUES
(1, 'Python', 'Advanced', 4),
(1, 'Machine Learning', 'Intermediate', 2),
(1, 'Data Science', 'Intermediate', 2),
(2, 'JavaScript', 'Expert', 6),
(2, 'Web Development', 'Expert', 6),
(2, 'React', 'Advanced', 3),
(3, 'Java', 'Advanced', 5),
(3, 'Spring Boot', 'Intermediate', 3),
(3, 'Cloud Computing', 'Beginner', 1);

-- Insert sample jobs
INSERT INTO jobs (title, description, category, required_skills, salary_range, company, status) VALUES
('Senior Python Developer', 'Looking for experienced Python developer with ML background', 'Software Development', '["Python", "Machine Learning", "Django"]', '120000-150000', 'TechCorp', 'active'),
('ML Engineer', 'Machine Learning Engineer for AI team', 'Data Science', '["Python", "Machine Learning", "Data Science", "TensorFlow"]', '130000-160000', 'AI Solutions', 'active'),
('Full Stack Developer', 'MERN Stack developer needed', 'Web Development', '["JavaScript", "React", "Node.js", "MongoDB"]', '100000-130000', 'WebDev Inc', 'active'),
('Java Backend Developer', 'Java developer for microservices', 'Software Development', '["Java", "Spring Boot", "SQL"]', '110000-140000', 'Enterprise Solutions', 'active'),
('Cloud Solutions Architect', 'Cloud infrastructure design', 'Cloud Engineering', '["Cloud Computing", "DevOps", "AWS", "Kubernetes"]', '140000-180000', 'CloudTech', 'active');
