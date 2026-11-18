# SkillBridge Project

## Overview
SkillBridge is a comprehensive web-based platform designed to bridge the gap between unemployed/underemployed individuals and industry requirements. The system enables users to evaluate their skills, receive personalized job recommendations, upskilling suggestions, and blockchain-based digital certificates for verified skill validation.

## Technology Stack

### Backend
- **Language**: PHP 7.4+
- **Framework**: Custom MVC Architecture
- **Database**: MySQL 8.0+
- **API**: RESTful API with JSON responses

### Machine Learning
- **Language**: Python 3.8+
- **Framework**: Flask 2.3.0
- **Libraries**: 
  - scikit-learn (ML models)
  - pandas (Data manipulation)
  - numpy (Numerical computing)

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Responsive design with modern styling
- **JavaScript**: Vanilla JS (no dependencies for initial version)

### Blockchain
- **Python**: Custom blockchain certificate manager
- **Smart Contracts**: Support for future integration

## Project Structure

```
SKILL BRIDGE/
├── backend/
│   ├── api/
│   │   └── router.php              # API routing
│   ├── controllers/
│   │   ├── AuthController.php      # Authentication
│   │   ├── SkillController.php     # Skill management
│   │   ├── JobRecommendationController.php
│   │   └── BlockchainController.php
│   ├── models/
│   │   ├── Database.php            # DB connection
│   │   ├── User.php                # User model
│   │   ├── Skill.php               # Skill model
│   │   └── JobRecommendation.php   # Job model
│   └── middleware/
│
├── ml/
│   ├── app.py                      # Flask ML API server
│   ├── config.py                   # ML configuration
│   ├── models/
│   │   ├── skill_recommender.py    # Skill recommendation engine
│   │   └── job_recommender.py      # Job recommendation engine
│   └── data/                       # Training data
│
├── frontend/
│   ├── index.html                  # Landing page
│   ├── assets/
│   │   ├── css/
│   │   │   ├── style.css
│   │   │   ├── form.css
│   │   │   ├── dashboard.css
│   │   │   └── responsive.css
│   │   └── js/
│   │       ├── main.js
│   │       ├── auth.js
│   │       └── dashboard.js
│   └── pages/
│       ├── login.html
│       ├── register.html
│       └── dashboard.html
│
├── blockchain/
│   └── certificate_manager.py      # Blockchain integration
│
├── database/
│   └── schema.sql                  # Database schema
│
├── config/
│   └── config.php                  # Configuration file
│
├── .env                            # Environment variables
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Installation & Setup

### Prerequisites
- PHP 7.4 or higher
- MySQL 8.0 or higher
- Python 3.8 or higher
- Composer (optional, for future dependencies)
- Node.js (optional, for build tools)

### Step 1: Clone/Download Project
```bash
cd "SKILL BRIDGE"
```

### Step 2: Setup Database
```bash
mysql -u root -p < database/schema.sql
```

Or manually create the database and import schema.sql using phpMyAdmin.

### Step 3: Configure Environment
1. Copy `.env` file
2. Update database credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=skillbridge_db
```

### Step 4: Setup Backend
```bash
# No additional installation needed for PHP
# Update config/config.php with your settings
```

### Step 5: Setup ML Server
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run ML API server
python ml/app.py
# Server will run on http://localhost:5000
```

### Step 6: Setup Frontend
The frontend runs on any web server:
```bash
# Using PHP built-in server
php -S localhost:8000

# Or use Apache/Nginx
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Skills
- `POST /api/skills/add` - Add user skill
- `GET /api/skills/user/{user_id}` - Get user skills
- `PUT /api/skills/{skill_id}` - Update skill
- `DELETE /api/skills/{skill_id}` - Delete skill

### Job Recommendations
- `GET /api/jobs/all` - Get all jobs
- `GET /api/jobs/category/{category}` - Get jobs by category
- `GET /api/recommendations/user/{user_id}` - Get user recommendations
- `POST /api/recommendations/generate/{user_id}` - Generate recommendations

### ML Endpoints
- `POST /api/recommend/skills` - Recommend skills
- `POST /api/recommend/jobs` - Recommend jobs
- `POST /api/skill-gap` - Calculate skill gap

## Features Implemented

### Phase 1: Core Features
 User Authentication
 Skill Management
 Database Schema
 RESTful API
 Job Database
 ML Job Recommendation Engine
 ML Skill Recommendation Engine
 Responsive Frontend
 Dashboard UI
 Blockchain Certificate Integration

### Phase 2: Enhancement (Future)
- [ ] Email notifications
- [ ] Skill endorsements
- [ ] User portfolio
- [ ] Interview preparation
- [ ] Advanced ML models
- [ ] Mobile app
- [ ] Payment integration

## ML Models & Algorithms

### Job Recommendation Engine
- **Algorithm**: Collaborative Filtering + Content-based Filtering
- **Matching Score**: Jaccard Similarity (0-100%)
- **Features**: User skills vs. Job requirements

### Skill Recommendation Engine
- **Algorithm**: Graph-based recommendation with demand scoring
- **Features**: Skill relationships, market demand, learning paths
- **Output**: Personalized upskilling recommendations

### Skill Gap Analysis
- **Input**: User skills, Target job skills
- **Output**: Missing skills, Learning priority, Match percentage

## Running the Application

### 1. Start MySQL
```bash
# Windows
net start MySQL80

# Linux
sudo service mysql start
```

### 2. Start ML API Server
```bash
python ml/app.py
# Runs on http://localhost:5000
```

### 3. Start Backend API
```bash
php -S localhost:8000
# API available at http://localhost:8000/api
```

### 4. Access Frontend
```
http://localhost:8000/frontend/index.html
```

## User Flow

1. **Registration** → User creates account
2. **Skill Assessment** → Add skills and experience levels
3. **Job Matching** → System generates recommendations
4. **Skill Gap Analysis** → View missing skills for target jobs
5. **Upskilling Path** → Get personalized learning recommendations
6. **Certificate** → Earn blockchain-verified certificates upon completion

## Database Tables

- `users` - User accounts
- `user_skills` - User skill records
- `jobs` - Job listings
- `job_recommendations` - Job match records
- `upskilling_paths` - Learning paths
- `digital_certificates` - Blockchain certificates
- `skill_gap_analysis` - Gap analysis records
- `job_applications` - Application tracking
- `ml_training_logs` - ML model training history

## Security Considerations

1. **Password Hashing**: bcrypt with salt
2. **JWT Tokens**: For API authentication
3. **Input Validation**: All user inputs validated
4. **SQL Injection Prevention**: Prepared statements
5. **CORS**: Configured for cross-origin requests
6. **Environment Variables**: Sensitive data in .env

## Performance Optimization

1. **Database Indexing**: Indexes on frequently queried columns
2. **Caching**: ML model caching in memory
3. **Lazy Loading**: Frontend data loading
4. **Response Compression**: Gzip enabled
5. **API Rate Limiting**: Planned implementation

## Testing

### Unit Tests
```bash
# Python tests
pytest ml/tests/

# PHP tests (PHPUnit)
vendor/bin/phpunit backend/tests/
```

### API Testing
- Use Postman collection: `docs/api-collection.json`
- cURL examples in `docs/api-examples.txt`

## Deployment

### Production Setup
1. Use Apache/Nginx instead of PHP built-in server
2. Enable HTTPS/SSL
3. Configure database backups
4. Set up monitoring and logging
5. Use environment-specific configs
6. Enable rate limiting and DDoS protection

## Troubleshooting

### ML API Not Responding
```bash
# Check if Flask server is running
curl http://localhost:5000/health

# Restart Flask
python ml/app.py
```

### Database Connection Error
- Verify MySQL is running
- Check .env credentials
- Verify database exists: `SHOW DATABASES;`

### API 404 Errors
- Check router.php routing rules
- Verify endpoint path
- Check request method (GET/POST/PUT/DELETE)

## Support & Documentation

- API Documentation: `docs/api-docs.md`
- Setup Guide: `docs/setup-guide.md`
- Architecture: `docs/architecture.md`


