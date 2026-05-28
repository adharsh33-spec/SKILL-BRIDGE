# SkillBridge Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                              │
│  (HTML5/CSS3/JavaScript Frontend - Responsive Web Application)      │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                              │
│           (RESTful API - PHP Router - CORS Enabled)                 │
└────────────┬─────────────────────────────────────────┬──────────────┘
             │                                         │
             ▼                                         ▼
┌──────────────────────────────┐        ┌──────────────────────────────┐
│   BACKEND LAYER              │        │     ML SERVICE LAYER         │
│   (PHP MVC Architecture)     │        │  (Python Flask API Server)   │
│                              │        │                              │
│  ├─ Controllers             │        │  ├─ Job Recommender         │
│  ├─ Models                  │        │  ├─ Skill Recommender       │
│  ├─ Business Logic          │        │  ├─ Skill Gap Analyzer      │
│  └─ Database Access         │        │  └─ Training Module         │
└──────────────┬───────────────┘        └──────────────┬───────────────┘
               │                                       │
               │ (HTTP/REST)                           │ (HTTP/REST)
               │                                       │
               ▼                                       ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    BLOCKCHAIN LAYER                                  │
│        (Digital Certificate Management & Verification)              │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    DATA PERSISTENCE LAYER                            │
│                                                                      │
│  ┌─────────────────┐        ┌──────────────┐    ┌────────────────┐ │
│  │   MySQL DB      │        │  ML Models   │    │  Cache Layer   │ │
│  │                 │        │  (Pickled)   │    │  (In-Memory)   │ │
│  └─────────────────┘        └──────────────┘    └────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer
- **Location**: `/frontend`
- **Technology**: HTML5, CSS3, JavaScript
- **Features**:
  - Responsive design (Mobile, Tablet, Desktop)
  - Real-time form validation
  - Dynamic content loading
  - Client-side caching
- **Pages**:
  - Landing page (index.html)
  - Authentication (login.html, register.html)
  - Dashboard (dashboard.html)

### 2. Backend API Layer
- **Location**: `/backend`
- **Technology**: PHP 7.4+
- **Architecture**: MVC Pattern
- **Components**:
  - **Controllers**: Handle HTTP requests
  - **Models**: Database operations
  - **Middleware**: Authentication, CORS
  - **Router**: Request routing

### 3. Machine Learning Layer
- **Location**: `/ml`
- **Technology**: Python 3.8+
- **Framework**: Flask 2.3.0
- **Components**:
  - **Job Recommender**: Content-based + Collaborative filtering
  - **Skill Recommender**: Graph-based recommendations
  - **Training Module**: Model training and evaluation
  - **Data Preparation**: Feature engineering and preprocessing

### 4. Blockchain Layer
- **Location**: `/blockchain`
- **Technology**: Python
- **Features**:
  - Certificate generation
  - Verification
  - QR code generation
  - Transaction logging

### 5. Database Layer
- **Location**: `/database`
- **Technology**: MySQL 8.0+
- **Schema**: 8 main tables + indices
- **Key Tables**:
  - users
  - user_skills
  - jobs
  - job_recommendations
  - digital_certificates
  - skill_gap_analysis

## Data Flow

### User Registration Flow
```
1. User fills registration form (Frontend)
   ↓
2. Form validation (JavaScript)
   ↓
3. POST /api/auth/register (API)
   ↓
4. AuthController validates input
   ↓
5. User Model creates record (MySQL)
   ↓
6. Return success response
```

### Job Recommendation Flow
```
1. User adds skills (Frontend)
   ↓
2. POST /api/skills/add (API)
   ↓
3. SkillController saves skill (MySQL)
   ↓
4. User clicks "Generate Recommendations"
   ↓
5. POST /api/recommendations/generate/{user_id}
   ↓
6. Frontend fetches user skills
   ↓
7. Send to ML API: /api/recommend/jobs
   ↓
8. ML Engine (Python):
   - Load user skills
   - Compare with job requirements
   - Calculate match scores
   - Return ranked recommendations
   ↓
9. Store recommendations (MySQL)
   ↓
10. Display results (Frontend)
```

### ML Model Pipeline
```
Training Phase:
  Raw Data → Data Preparation → Feature Engineering
    ↓
  Train/Test Split → Model Training → Evaluation
    ↓
  Save Model → Model Registry

Inference Phase:
  User Skills → Feature Extraction → Load Model
    ↓
  Prediction → Score Calculation → Return Results
```

## API Communication Patterns

### Request-Response Pattern
```
Client Request:
{
  "method": "POST",
  "endpoint": "/api/skills/add",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer {token}"
  },
  "body": {
    "user_id": 1,
    "skill_name": "Python",
    "level": "Advanced"
  }
}

Server Response:
{
  "status": "success",
  "message": "Skill added successfully",
  "data": {...}
}
```

## Security Architecture

### Authentication Flow
```
1. User Login → Password Hashing (bcrypt)
2. Token Generation → JWT Token
3. Token Storage → Local Storage (Frontend)
4. Subsequent Requests → Include JWT in header
5. Token Validation → Verify signature and expiry
```

### Data Protection
- SQL Injection Prevention: Prepared statements
- XSS Prevention: Input sanitization
- CORS: Configured for trusted domains
- HTTPS/SSL: Required for production

## Performance Optimization

### Database Optimization
- Indexed columns on frequently queried fields
- Connection pooling
- Query optimization

### API Caching
- ML model caching
- Response compression (gzip)
- Client-side caching

### Frontend Optimization
- Lazy loading
- Code splitting
- Asset minification

## Scalability Considerations

### Horizontal Scaling
- Load balancer for API servers
- Database replication
- Separate ML service instances

### Vertical Scaling
- Increase server resources
- Database tuning
- ML model optimization

## Deployment Architecture

### Development Environment
```
Local Machine:
  ├─ PHP Development Server (localhost:8000)
  ├─ Flask ML Server (localhost:5000)
  └─ MySQL (localhost:3306)
```

### Production Environment
```
Server Infrastructure:
  ├─ Load Balancer (Nginx/HAProxy)
  ├─ Web Servers (Apache/Nginx)
  ├─ Application Servers (PHP-FPM)
  ├─ ML Service (Gunicorn/uWSGI)
  ├─ Database Server (MySQL)
  ├─ Cache Server (Redis)
  └─ Monitoring (ELK Stack)
```

## Integration Points

### PHP ↔ Python ML Integration
```
HTTP Request/Response via REST API
Endpoint: http://localhost:5000/api/recommend

JobRecommendationController (PHP)
  ↓
Call ML API with user skills
  ↓
ML Flask App (Python)
  ↓
Process and return recommendations
```

### Frontend ↔ Backend Integration
```
RESTful API Calls
Headers: Authorization Bearer token
Content-Type: application/json
```

## Future Architecture Enhancements

1. **Microservices Architecture**
   - Separate services for each domain
   - API Gateway pattern
   - Service-to-service communication

2. **Async Processing**
   - Message queues (RabbitMQ/Kafka)
   - Background jobs (Celery)
   - WebSocket for real-time updates

3. **Cloud Deployment**
   - Docker containerization
   - Kubernetes orchestration
   - Cloud CDN for frontend assets

4. **Advanced ML**
   - Deep learning models
   - Real-time predictions
   - Continuous learning pipeline

---
**Last Updated**: May 28, 2024
**Version**: 1.0.0
