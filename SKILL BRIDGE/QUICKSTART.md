# SkillBridge Quick Start Guide

## 5-Minute Setup for Development

### Prerequisites Check
```bash
# Check PHP
php -v

# Check Python
python3 --version

# Check MySQL
mysql --version

# Check Git
git --version
```

### Quick Start Steps

#### 1. Database Setup (2 minutes)
```bash
# Start MySQL
net start MySQL80

# Import schema
mysql -u root -p < "c:\Users\micro\Downloads\SKILL BRIDGE\database\schema.sql"

# Verify
mysql -u root -p -e "USE skillbridge_db; SHOW TABLES;"
```

#### 2. Environment Configuration (1 minute)
```bash
# Copy .env file (already created)
# Update with your credentials if needed

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password  # Update this
DB_NAME=skillbridge_db
```

#### 3. Start PHP Backend (1 minute)
```bash
cd "c:\Users\micro\Downloads\SKILL BRIDGE"
php -S localhost:8000

# Backend API running at: http://localhost:8000/api
```

#### 4. Start ML Server (1 minute)
```bash
# Open new terminal

cd "c:\Users\micro\Downloads\SKILL BRIDGE\ml"

# Install dependencies
pip install -r ../requirements.txt

# Start Flask server
python app.py

# ML API running at: http://localhost:5000
```

### Verify Installation

#### Test Backend API
```bash
# In new terminal
curl http://localhost:8000/api/health

# Expected: Success response
```

#### Test ML API
```bash
curl http://localhost:5000/health

# Expected: {"status": "ok", "message": "ML API Server is running"}
```

#### Access Frontend
```
Open Browser:
http://localhost:8000/frontend/index.html
```

## First Time Usage

### Step 1: Register Account
1. Click "Register" button
2. Fill in: Full Name, Email, Password
3. Click "Register"

### Step 2: Add Skills
1. Go to Dashboard
2. Click "Add Skill"
3. Enter: Skill Name, Level, Years of Experience
4. Add 2-3 skills for best recommendations

### Step 3: Get Recommendations
1. Click "Recommendations" tab
2. Click "Generate Recommendations"
3. View personalized job recommendations

### Step 4: Analyze Skills
1. Go to Dashboard
2. Click on any recommendation
3. View skill match percentage
4. See missing skills for target jobs

## Common Commands

### View Logs
```bash
# PHP errors
type php-error.log

# ML server
# Check terminal where Flask is running

# Database queries
mysql> SHOW VARIABLES LIKE 'log_%';
```

### Database Management
```bash
# Connect to database
mysql -u root -p skillbridge_db

# View users
SELECT * FROM users;

# View skills
SELECT * FROM user_skills;

# View recommendations
SELECT * FROM job_recommendations;
```

### Restart Services
```powershell
# Stop PHP server
# Use Ctrl+C in PHP terminal

# Stop ML server
# Use Ctrl+C in Python terminal

# Restart MySQL
net stop MySQL80
net start MySQL80
```

## Troubleshooting

### "Port Already in Use"
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <process_id> /F

# Alternative port
php -S localhost:8001
```

### "Database Connection Failed"
- Check MySQL is running: `net start MySQL80`
- Verify credentials in .env file
- Check database exists: `mysql -u root -p -e "SHOW DATABASES;"`

### "ML API Not Responding"
- Check Python dependencies installed: `pip install -r requirements.txt`
- Verify Flask running on port 5000
- Check Python version >= 3.8

### "Page Not Loading"
- Verify PHP server running on port 8000
- Check browser console for JavaScript errors
- Clear browser cache (Ctrl+Shift+Delete)

## Directory Structure Quick Reference

```
SKILL BRIDGE/
├── backend/          ← PHP code
├── ml/               ← Python ML code
├── frontend/         ← HTML/CSS/JS
├── database/         ← MySQL schema
├── blockchain/       ← Blockchain code
├── config/           ← Configuration
├── .env              ← Environment variables
├── requirements.txt  ← Python dependencies
└── README.md         ← Full documentation
```

## API Quick Test

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\",\"full_name\":\"Test User\"}"
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

### Add Skill
```bash
curl -X POST http://localhost:8000/api/skills/add ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\":1,\"skill_name\":\"Python\",\"level\":\"Advanced\",\"years_experience\":4}"
```

### Get Recommendations
```bash
curl http://localhost:8000/api/recommendations/user/1
```

### ML Skill Recommendation
```bash
curl -X POST http://localhost:5000/api/recommend/skills ^
  -H "Content-Type: application/json" ^
  -d "{\"user_skills\":[\"Python\",\"Web Development\"]}"
```

## Next Steps

1. ✅ Setup complete
2. 📝 Explore the dashboard
3. 🔧 Customize skills list in ML models
4. 📊 Test with sample data
5. 🚀 Deploy to production (see DEPLOYMENT.md)

## Getting Help

- **API Docs**: Open `docs/API_DOCUMENTATION.html`
- **Architecture**: Read `docs/ARCHITECTURE.md`
- **Deployment**: See `docs/DEPLOYMENT.md`
- **README**: Full details in main `README.md`

## Key Endpoints for Testing

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /api/auth/register | Create account |
| POST | /api/auth/login | Login |
| POST | /api/skills/add | Add skill |
| GET | /api/skills/user/1 | View skills |
| GET | /api/jobs/all | List jobs |
| GET | /api/recommendations/user/1 | View recommendations |
| POST | /ml/api/recommend/jobs | Get job recommendations |
| POST | /ml/api/recommend/skills | Get skill recommendations |

---

**Ready to Go! 🚀**

Start using SkillBridge now and begin bridging the gap between skills and opportunity!

**Need Help?** Refer to full documentation in docs/ folder.
