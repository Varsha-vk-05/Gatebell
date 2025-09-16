# Complete Setup Instructions - Security Management System

## 📋 Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **MongoDB 4.4+** (Community Edition)
- **Git** for version control

## 🚀 Quick Setup Guide

### Step 1: Clone and Setup Project Structure

```bash
# Create project directory
mkdir security_management_system
cd security_management_system

# Create main folders
mkdir backend frontend database docs

# Initialize git repository
git init
```

### Step 2: Backend Setup (Flask)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Create requirements.txt
cat > requirements.txt << EOF
Flask==2.3.2
Flask-JWT-Extended==4.5.2
Flask-CORS==4.0.0
pymongo==4.4.1
python-dotenv==1.0.0
marshmallow==3.20.1
bcrypt==4.0.1
EOF

# Install dependencies
pip install -r requirements.txt

# Create project structure
mkdir -p app/{models,auth,api}
touch app/__init__.py
touch app/config.py
touch app/models/{__init__.py,user.py,visitor.py}
touch app/auth/{__init__.py,routes.py,utils.py}
touch app/api/{__init__.py,resident.py,security_guard.py,admin.py,super_admin.py}
touch run.py

# Create environment file
cat > .env << EOF
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-in-production
FLASK_CONFIG=development

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/security_management

# Debug Mode (true/false)
DEBUG_MODE=true

# CORS Origins
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOF

echo "✅ Backend structure created"
```

### Step 3: Frontend Setup (React)

```bash
cd ../frontend

# Create React app
npx create-react-app . --template typescript

# Install additional dependencies
npm install react-router-dom axios

# Create project structure
mkdir -p src/{components,pages,utils,styles}
mkdir -p src/components/Common

# Create component files
touch src/components/{Login3D.jsx,Registration3D.jsx,Dashboard3D.jsx}
touch src/components/Common/{Header.jsx,ProtectedRoute.jsx}
touch src/pages/{ResidentDashboard.jsx,SecurityGuardDashboard.jsx,AdminDashboard.jsx,SuperAdminDashboard.jsx}
touch src/utils/{auth.js,api.js}
touch src/styles/{3d-effects.css,globals.css}

# Update package.json to add proxy
npm pkg set proxy="http://localhost:5000"

echo "✅ Frontend structure created"
```

### Step 4: Database Setup (MongoDB)

```bash
cd ../database

# Create database initialization scripts
cat > init_db.py << 'EOF'
from pymongo import MongoClient
from datetime import datetime
import os

def init_database():
    """Initialize the MongoDB database with collections and indexes"""
    
    # Connect to MongoDB
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/security_management')
    client = MongoClient(mongo_uri)
    db = client.get_database()
    
    print("🗄️ Initializing Security Management Database...")
    
    # Create collections and indexes
    db.users.create_index("phone_number", unique=True)
    db.users.create_index("role")
    db.visitor_requests.create_index("resident_id")
    db.visitor_requests.create_index("status") 
    db.visitor_requests.create_index("created_at")
    db.guard_activities.create_index("guard_id")
    db.guard_activities.create_index("date")
    
    print("✅ Database initialization completed!")
    return db

if __name__ == "__main__":
    init_database()
EOF

# Create sample data script
cat > sample_data.py << 'EOF'
from pymongo import MongoClient
from datetime import datetime
import os

def create_sample_data():
    """Create sample users for testing"""
    
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/security_management')
    client = MongoClient(mongo_uri)
    db = client.get_database()
    
    # Sample users
    sample_users = [
        {
            "phone_number": "9876543210",
            "full_name": "John Smith",
            "flat_number": "A-101",
            "role": "resident",
            "created_at": datetime.utcnow(),
            "is_active": True
        },
        {
            "phone_number": "9876543211", 
            "full_name": "Security Guard 1",
            "flat_number": "Guard-01",
            "role": "security_guard",
            "created_at": datetime.utcnow(),
            "is_active": True
        },
        {
            "phone_number": "9876543212",
            "full_name": "Admin User",
            "flat_number": "Admin-01", 
            "role": "admin",
            "created_at": datetime.utcnow(),
            "is_active": True
        },
        {
            "phone_number": "9876543213",
            "full_name": "Super Admin",
            "flat_number": "Super-01",
            "role": "super_admin", 
            "created_at": datetime.utcnow(),
            "is_active": True
        }
    ]
    
    try:
        db.users.insert_many(sample_users)
        print("✅ Sample users created successfully")
        print("📱 Test phone numbers:")
        for user in sample_users:
            print(f"   {user['role']}: {user['phone_number']}")
    except Exception as e:
        print(f"ℹ️ Sample users may already exist: {e}")

if __name__ == "__main__":
    create_sample_data()
EOF

echo "✅ Database scripts created"
```

### Step 5: Start MongoDB

```bash
# Start MongoDB service
# On Windows (if installed as service):
net start MongoDB

# On macOS (with Homebrew):
brew services start mongodb-community

# On Linux:
sudo systemctl start mongod

# Or run directly:
mongod --dbpath /path/to/your/db/directory

echo "✅ MongoDB started"
```

### Step 6: Initialize Database

```bash
# From the database directory
cd database

# Run database initialization
python init_db.py

# Create sample data
python sample_data.py

echo "✅ Database initialized with sample data"
```

## 🎯 Running the Application

### Terminal 1: Start Backend

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python run.py
```

You should see:
```
🔧 Debug Mode: ON
🔑 JWT Secret: ***key
🗄️ MongoDB URI: mongodb://localhost:27017/security_management
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[::1]:5000
```

### Terminal 2: Start Frontend

```bash
cd frontend
npm start
```

You should see:
```
Compiled successfully!

You can now view security-management-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.x:3000
```

## 🧪 Testing the Application

### 1. Test Debug Mode Login

1. Open http://localhost:3000
2. Enter any of these test phone numbers:
   - **Resident**: `9876543210`
   - **Security Guard**: `9876543211` 
   - **Admin**: `9876543212`
   - **Super Admin**: `9876543213`
3. Click "Continue" - should login directly (Debug Mode)

### 2. Test Registration Flow

1. Enter a new 10-digit phone number
2. Should show registration form
3. Fill in name and flat number
4. Should create account and login

### 3. Test Role-Based Dashboards

Each role should see different dashboard content:
- **Resident**: Visitor request management
- **Security Guard**: Visitor approval interface
- **Admin**: Guard activity monitoring
- **Super Admin**: Complete system overview

## 🔧 Configuration Options

### Debug Mode Toggle

Edit `backend/.env`:
```env
# Enable debug mode (skip OTP)
DEBUG_MODE=true

# Disable debug mode (require OTP)
DEBUG_MODE=false
```

### MongoDB Connection

Edit `backend/.env`:
```env
# Local MongoDB
MONGO_URI=mongodb://localhost:27017/security_management

# MongoDB Atlas (Cloud)
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/security_management

# MongoDB with authentication
MONGO_URI=mongodb://username:password@localhost:27017/security_management
```

### JWT Configuration

Edit `backend/.env`:
```env
# JWT secret (change in production)
JWT_SECRET_KEY=your-production-jwt-secret

# Token expiration (default: 24 hours)
JWT_ACCESS_TOKEN_EXPIRES_HOURS=24
```

## 📱 API Testing

### Using cURL

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test phone login (debug mode)
curl -X POST http://localhost:5000/auth/phone-login \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "9876543210"}'

# Test protected endpoint (replace JWT_TOKEN)
curl -X GET http://localhost:5000/auth/profile \
  -H "Authorization: Bearer JWT_TOKEN"
```

### Using Postman

1. Import the API collection
2. Set base URL: `http://localhost:5000`
3. Test authentication endpoints
4. Use JWT token in subsequent requests

## 🚀 Production Deployment

### Backend Deployment

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Or with environment variables
export FLASK_CONFIG=production
export DEBUG_MODE=false
gunicorn run:app
```

### Frontend Deployment

```bash
# Build for production
npm run build

# Serve with static server
npm install -g serve
serve -s build -l 3000

# Or deploy to hosting service (Netlify, Vercel, etc.)
```

### MongoDB Production Setup

1. **MongoDB Atlas** (Recommended)
   - Create cluster at mongodb.com
   - Update connection string in `.env`
   - Enable network access

2. **Self-hosted MongoDB**
   - Enable authentication
   - Configure replica sets
   - Set up backup strategy

## 🔒 Security Considerations

### Production Security Checklist

- [ ] Change all default secrets and keys
- [ ] Enable MongoDB authentication
- [ ] Use HTTPS for all connections
- [ ] Set up proper CORS policies
- [ ] Configure rate limiting
- [ ] Enable request logging
- [ ] Set up monitoring and alerts
- [ ] Regular security audits

### Environment Variables

Create production `.env`:
```env
SECRET_KEY=complex-production-secret-key
JWT_SECRET_KEY=complex-jwt-production-secret
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/prod_db
DEBUG_MODE=false
FLASK_CONFIG=production
CORS_ORIGINS=https://yourdomain.com
```

## 📊 Monitoring and Maintenance

### Health Checks

```bash
# Check backend health
curl http://localhost:5000/api/health

# Check database connection
python -c "from pymongo import MongoClient; print('Connected:', MongoClient().admin.command('ping'))"

# Check frontend build
npm run build
```

### Log Monitoring

- Backend logs: Check Flask application logs
- Frontend logs: Browser developer console
- Database logs: MongoDB logs
- System logs: Application server logs

## 🆘 Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   ```
   Solution: Check MongoDB service is running
   mongod --version
   ```

2. **Port Already in Use**
   ```bash
   # Kill process on port 5000
   lsof -ti:5000 | xargs kill -9
   ```

3. **JWT Token Invalid**
   ```
   Solution: Check JWT_SECRET_KEY matches in .env
   ```

4. **CORS Errors**
   ```
   Solution: Update CORS_ORIGINS in backend/.env
   ```

### Debug Commands

```bash
# Check Python dependencies
pip list

# Check Node dependencies  
npm ls

# Test MongoDB connection
mongo security_management --eval "db.stats()"

# Check environment variables
env | grep -E "(SECRET|JWT|MONGO)"
```

## 📚 Additional Resources

### Documentation
- Flask: https://flask.palletsprojects.com/
- React: https://reactjs.org/docs/
- MongoDB: https://docs.mongodb.com/
- JWT: https://jwt.io/

### Development Tools
- MongoDB Compass (GUI)
- Postman (API testing)
- VS Code Extensions (Python, React)
- React Developer Tools

This completes the full setup instructions for your Security Management System! 🎉