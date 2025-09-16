# Flask Backend Implementation - Security Management System

## 1. Project Structure Setup

```bash
mkdir security_management_system
cd security_management_system
mkdir backend frontend database
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

## 2. Requirements.txt

```txt
Flask==2.3.2
Flask-JWT-Extended==4.5.2
Flask-CORS==4.0.0
pymongo==4.4.1
python-dotenv==1.0.0
marshmallow==3.20.1
bcrypt==4.0.1
```

## 3. Configuration (app/config.py)

```python
import os
from datetime import timedelta

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/security_management'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Debug Mode for OTP bypass
    DEBUG_MODE = os.environ.get('DEBUG_MODE', 'True').lower() == 'true'
    
    # CORS Configuration
    CORS_ORIGINS = ['http://localhost:3000']

class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_MODE = True

class ProductionConfig(Config):
    DEBUG = False
    DEBUG_MODE = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

## 4. Flask App Initialization (app/__init__.py)

```python
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from pymongo import MongoClient
from app.config import config

# Global variables
mongo_client = None
db = None
jwt = None

def create_app(config_name='default'):
    global mongo_client, db, jwt
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize MongoDB
    mongo_client = MongoClient(app.config['MONGO_URI'])
    db = mongo_client.get_database()
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from app.auth import auth_bp
    from app.api import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # JWT Error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'message': 'Token has expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'message': 'Invalid token'}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'message': 'Authorization token required'}, 401
    
    return app

def get_db():
    return db
```

## 5. User Models (app/models/user.py)

```python
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re

class User:
    def __init__(self, db):
        self.collection = db.users
        # Create unique index on phone_number
        self.collection.create_index("phone_number", unique=True)
    
    def create_user(self, phone_number, full_name, flat_number, role='resident'):
        """Create a new user"""
        if not self.validate_phone_number(phone_number):
            return None, "Invalid phone number format"
        
        if self.collection.find_one({"phone_number": phone_number}):
            return None, "User already exists"
        
        user_data = {
            "phone_number": phone_number,
            "full_name": full_name,
            "flat_number": flat_number,
            "role": role,
            "created_at": datetime.utcnow(),
            "last_login": None,
            "is_active": True
        }
        
        result = self.collection.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return user_data, None
    
    def get_user_by_phone(self, phone_number):
        """Get user by phone number"""
        return self.collection.find_one({"phone_number": phone_number})
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.collection.find_one({"_id": ObjectId(user_id)})
    
    def update_last_login(self, user_id):
        """Update user's last login time"""
        self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"last_login": datetime.utcnow()}}
        )
    
    def get_users_by_role(self, role):
        """Get all users by role"""
        return list(self.collection.find({"role": role, "is_active": True}))
    
    def validate_phone_number(self, phone_number):
        """Validate 10-digit phone number"""
        pattern = r'^[0-9]{10}$'
        return re.match(pattern, phone_number) is not None
    
    def has_role(self, user_id, required_role):
        """Check if user has required role"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        return user.get('role') == required_role
    
    def get_all_users(self):
        """Get all users (Super Admin only)"""
        return list(self.collection.find({"is_active": True}))
```

## 6. Visitor Models (app/models/visitor.py)

```python
from bson import ObjectId
from datetime import datetime

class VisitorRequest:
    def __init__(self, db):
        self.collection = db.visitor_requests
    
    def create_request(self, visitor_name, visitor_phone, purpose, flat_number, resident_id):
        """Create a new visitor request"""
        request_data = {
            "visitor_name": visitor_name,
            "visitor_phone": visitor_phone,
            "purpose": purpose,
            "flat_number": flat_number,
            "resident_id": ObjectId(resident_id),
            "entry_time": datetime.utcnow(),
            "exit_time": None,
            "status": "pending",
            "approved_by_guard": None,
            "approved_by_resident": None,
            "created_at": datetime.utcnow(),
            "notes": ""
        }
        
        result = self.collection.insert_one(request_data)
        request_data['_id'] = result.inserted_id
        return request_data
    
    def get_requests_by_resident(self, resident_id):
        """Get all visitor requests for a specific resident"""
        return list(self.collection.find({"resident_id": ObjectId(resident_id)}))
    
    def get_pending_requests(self):
        """Get all pending visitor requests"""
        return list(self.collection.find({"status": "pending"}))
    
    def approve_request(self, request_id, approved_by, approver_type):
        """Approve a visitor request"""
        update_data = {"status": "approved"}
        
        if approver_type == "guard":
            update_data["approved_by_guard"] = ObjectId(approved_by)
        elif approver_type == "resident":
            update_data["approved_by_resident"] = ObjectId(approved_by)
        
        self.collection.update_one(
            {"_id": ObjectId(request_id)},
            {"$set": update_data}
        )
    
    def deny_request(self, request_id, denied_by, reason=""):
        """Deny a visitor request"""
        self.collection.update_one(
            {"_id": ObjectId(request_id)},
            {"$set": {
                "status": "denied",
                "notes": reason,
                "denied_by": ObjectId(denied_by)
            }}
        )
    
    def complete_visit(self, request_id):
        """Mark visit as completed"""
        self.collection.update_one(
            {"_id": ObjectId(request_id)},
            {"$set": {
                "status": "completed",
                "exit_time": datetime.utcnow()
            }}
        )
    
    def get_all_requests(self):
        """Get all visitor requests (Admin/Super Admin)"""
        return list(self.collection.find({}))
```

## 7. Authentication Routes (app/auth/routes.py)

```python
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import get_db
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/phone-login', methods=['POST'])
def phone_login():
    """Step 1: Phone number input with debug mode support"""
    data = request.get_json()
    phone_number = data.get('phone_number')
    
    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400
    
    # Validate phone number format
    if not re.match(r'^[0-9]{10}$', phone_number):
        return jsonify({'error': 'Invalid phone number format'}), 400
    
    db = get_db()
    user_model = User(db)
    user = user_model.get_user_by_phone(phone_number)
    
    # Check if debug mode is enabled
    if current_app.config['DEBUG_MODE']:
        if user:
            # User exists, proceed to login
            user_model.update_last_login(str(user['_id']))
            access_token = create_access_token(
                identity=str(user['_id']),
                additional_claims={
                    'role': user['role'],
                    'phone_number': user['phone_number']
                }
            )
            return jsonify({
                'message': 'Login successful (Debug Mode)',
                'access_token': access_token,
                'user': {
                    'id': str(user['_id']),
                    'phone_number': user['phone_number'],
                    'full_name': user['full_name'],
                    'flat_number': user['flat_number'],
                    'role': user['role']
                },
                'needs_registration': False
            }), 200
        else:
            # User doesn't exist, needs registration
            return jsonify({
                'message': 'Phone number verified (Debug Mode)',
                'needs_registration': True,
                'phone_number': phone_number
            }), 200
    else:
        # Production mode - would integrate with OTP service
        # For now, return placeholder response
        return jsonify({
            'message': 'OTP sent to phone number',
            'needs_otp_verification': True,
            'phone_number': phone_number
        }), 200

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Step 2: OTP verification (Production mode)"""
    data = request.get_json() 
    phone_number = data.get('phone_number')
    otp = data.get('otp')
    
    if current_app.config['DEBUG_MODE']:
        return jsonify({'error': 'Use phone-login endpoint in debug mode'}), 400
    
    # In production, verify OTP with service (Firebase/Twilio)
    # For demo purposes, accept any 6-digit OTP
    if not otp or len(otp) != 6:
        return jsonify({'error': 'Invalid OTP'}), 400
    
    db = get_db()
    user_model = User(db)
    user = user_model.get_user_by_phone(phone_number)
    
    if user:
        user_model.update_last_login(str(user['_id']))
        access_token = create_access_token(
            identity=str(user['_id']),
            additional_claims={
                'role': user['role'],
                'phone_number': user['phone_number']
            }
        )
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': str(user['_id']),
                'phone_number': user['phone_number'],
                'full_name': user['full_name'],
                'flat_number': user['flat_number'],
                'role': user['role']
            },
            'needs_registration': False
        }), 200
    else:
        return jsonify({
            'message': 'OTP verified',
            'needs_registration': True,
            'phone_number': phone_number
        }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """Step 3: User registration"""
    data = request.get_json()
    phone_number = data.get('phone_number')
    full_name = data.get('full_name')
    flat_number = data.get('flat_number')
    role = data.get('role', 'resident')  # Default to resident
    
    if not all([phone_number, full_name, flat_number]):
        return jsonify({'error': 'All fields are required'}), 400
    
    db = get_db()
    user_model = User(db)
    
    user_data, error = user_model.create_user(phone_number, full_name, flat_number, role)
    
    if error:
        return jsonify({'error': error}), 400
    
    # Create access token
    access_token = create_access_token(
        identity=str(user_data['_id']),
        additional_claims={
            'role': user_data['role'],
            'phone_number': user_data['phone_number']
        }
    )
    
    return jsonify({
        'message': 'Registration successful',
        'access_token': access_token,
        'user': {
            'id': str(user_data['_id']),
            'phone_number': user_data['phone_number'],
            'full_name': user_data['full_name'],
            'flat_number': user_data['flat_number'],
            'role': user_data['role']
        }
    }), 201

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    user_id = get_jwt_identity()
    db = get_db()
    user_model = User(db)
    
    user = user_model.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': str(user['_id']),
            'phone_number': user['phone_number'],
            'full_name': user['full_name'],
            'flat_number': user['flat_number'],
            'role': user['role'],
            'created_at': user['created_at'].isoformat(),
            'last_login': user['last_login'].isoformat() if user['last_login'] else None
        }
    }), 200
```

## 8. API Authorization Utils (app/auth/utils.py)

```python
from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.models.user import User
from app import get_db

def role_required(allowed_roles):
    """Decorator to check if user has required role"""
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role not in allowed_roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    """Get current user from JWT token"""
    user_id = get_jwt_identity()
    db = get_db()
    user_model = User(db)
    return user_model.get_user_by_id(user_id)

def resident_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return role_required(['resident'])(f)(*args, **kwargs)
    return decorated_function

def security_guard_or_above(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return role_required(['security_guard', 'admin', 'super_admin'])(f)(*args, **kwargs)
    return decorated_function

def admin_or_above(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return role_required(['admin', 'super_admin'])(f)(*args, **kwargs)
    return decorated_function

def super_admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return role_required(['super_admin'])(f)(*args, **kwargs)
    return decorated_function
```

## 9. API Blueprint (app/api/__init__.py)

```python
from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import resident, security_guard, admin, super_admin
```

## 10. Main Application Runner (run.py)

```python
from app import create_app
import os

if __name__ == '__main__':
    config_name = os.environ.get('FLASK_CONFIG', 'development')
    app = create_app(config_name)
    
    # Print debug mode status
    print(f"🔧 Debug Mode: {'ON' if app.config['DEBUG_MODE'] else 'OFF'}")
    print(f"🔑 JWT Secret: {'***' + app.config['JWT_SECRET_KEY'][-4:]}")
    print(f"🗄️ MongoDB URI: {app.config['MONGO_URI']}")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
```

## 11. Environment Variables (.env.example)

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-here
FLASK_CONFIG=development

# JWT Configuration  
JWT_SECRET_KEY=your-jwt-secret-key-here

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/security_management

# Debug Mode (true/false)
DEBUG_MODE=true

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

3. **Start MongoDB:**
   ```bash
   mongod
   ```

4. **Run Application:**
   ```bash
   python run.py
   ```

5. **Toggle Debug Mode:**
   - Set `DEBUG_MODE=true` in .env for development
   - Set `DEBUG_MODE=false` in .env for production

The Flask backend is now ready with JWT authentication, role-based access control, and MongoDB integration!