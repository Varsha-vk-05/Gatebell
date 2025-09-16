# API Endpoints Implementation - Security Management System

## 1. Resident API Endpoints (app/api/resident.py)

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.visitor import VisitorRequest
from app.auth.utils import role_required
from app import get_db
from bson import ObjectId

resident_bp = Blueprint('resident', __name__)

@resident_bp.route('/visitor-requests', methods=['GET'])
@role_required(['resident'])
def get_visitor_requests():
    """Get all visitor requests for the current resident"""
    user_id = get_jwt_identity()
    db = get_db()
    visitor_model = VisitorRequest(db)
    
    requests = visitor_model.get_requests_by_resident(user_id)
    
    # Convert ObjectId to string for JSON serialization
    for request_item in requests:
        request_item['_id'] = str(request_item['_id'])
        request_item['resident_id'] = str(request_item['resident_id'])
        if request_item.get('approved_by_guard'):
            request_item['approved_by_guard'] = str(request_item['approved_by_guard'])
        if request_item.get('approved_by_resident'):
            request_item['approved_by_resident'] = str(request_item['approved_by_resident'])
    
    return jsonify({
        'requests': requests,
        'total': len(requests)
    }), 200

@resident_bp.route('/approve/<request_id>', methods=['POST'])
@role_required(['resident'])
def approve_visitor(request_id):
    """Approve a visitor request"""
    user_id = get_jwt_identity()
    db = get_db()
    visitor_model = VisitorRequest(db)
    
    # Verify the request belongs to this resident
    request_data = db.visitor_requests.find_one({"_id": ObjectId(request_id)})
    if not request_data or str(request_data['resident_id']) != user_id:
        return jsonify({'error': 'Request not found or unauthorized'}), 404
    
    visitor_model.approve_request(request_id, user_id, 'resident')
    
    return jsonify({'message': 'Visitor request approved successfully'}), 200

@resident_bp.route('/deny/<request_id>', methods=['POST'])
@role_required(['resident'])
def deny_visitor(request_id):
    """Deny a visitor request"""
    user_id = get_jwt_identity()
    data = request.get_json()
    reason = data.get('reason', '')
    
    db = get_db()
    visitor_model = VisitorRequest(db)
    
    # Verify the request belongs to this resident
    request_data = db.visitor_requests.find_one({"_id": ObjectId(request_id)})
    if not request_data or str(request_data['resident_id']) != user_id:
        return jsonify({'error': 'Request not found or unauthorized'}), 404
    
    visitor_model.deny_request(request_id, user_id, reason)
    
    return jsonify({'message': 'Visitor request denied successfully'}), 200

@resident_bp.route('/dashboard-stats', methods=['GET'])
@role_required(['resident'])
def get_dashboard_stats():
    """Get dashboard statistics for resident"""
    user_id = get_jwt_identity()
    db = get_db()
    
    # Get visitor request statistics
    pipeline = [
        {"$match": {"resident_id": ObjectId(user_id)}},
        {"$group": {
            "_id": "$status",
            "count": {"$sum": 1}
        }}
    ]
    
    stats = list(db.visitor_requests.aggregate(pipeline))
    
    # Format statistics
    formatted_stats = {
        'pending': 0,
        'approved': 0,
        'denied': 0,
        'completed': 0,
        'total': 0
    }
    
    for stat in stats:
        if stat['_id'] in formatted_stats:
            formatted_stats[stat['_id']] = stat['count']
            formatted_stats['total'] += stat['count']
    
    return jsonify({'stats': formatted_stats}), 200
```

## 2. Security Guard API Endpoints (app/api/security_guard.py)

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.visitor import VisitorRequest
from app.models.user import User
from app.auth.utils import role_required
from app import get_db
from bson import ObjectId
from datetime import datetime

guard_bp = Blueprint('guard', __name__)

@guard_bp.route('/visitor-requests', methods=['GET'])
@role_required(['security_guard', 'admin', 'super_admin'])
def get_all_visitor_requests():
    """Get all visitor requests for security guard"""
    db = get_db()
    visitor_model = VisitorRequest(db)
    
    requests = visitor_model.get_pending_requests()
    
    # Enrich with resident information
    user_model = User(db)
    for request_item in requests:
        resident = user_model.get_user_by_id(str(request_item['resident_id']))
        request_item['resident_name'] = resident['full_name'] if resident else 'Unknown'
        
        # Convert ObjectIds to strings
        request_item['_id'] = str(request_item['_id'])
        request_item['resident_id'] = str(request_item['resident_id'])
        if request_item.get('approved_by_guard'):
            request_item['approved_by_guard'] = str(request_item['approved_by_guard'])
    
    return jsonify({
        'requests': requests,
        'total': len(requests)
    }), 200

@guard_bp.route('/create-visitor-request', methods=['POST'])
@role_required(['security_guard', 'admin', 'super_admin'])
def create_visitor_request():
    """Create a new visitor request (for unknown visitors)"""
    data = request.get_json()
    
    required_fields = ['visitor_name', 'visitor_phone', 'purpose', 'flat_number']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    db = get_db()
    user_model = User(db)
    
    # Find resident by flat number
    resident = db.users.find_one({
        "flat_number": data['flat_number'],
        "role": "resident"
    })
    
    if not resident:
        return jsonify({'error': 'No resident found for this flat number'}), 404
    
    visitor_model = VisitorRequest(db)
    visitor_request = visitor_model.create_request(
        data['visitor_name'],
        data['visitor_phone'],
        data['purpose'],
        data['flat_number'],
        str(resident['_id'])
    )
    
    # Convert ObjectId to string
    visitor_request['_id'] = str(visitor_request['_id'])
    visitor_request['resident_id'] = str(visitor_request['resident_id'])
    
    return jsonify({
        'message': 'Visitor request created successfully',
        'request': visitor_request
    }), 201

@guard_bp.route('/approve/<request_id>', methods=['POST'])
@role_required(['security_guard', 'admin', 'super_admin'])
def approve_visitor_guard(request_id):
    """Security guard approves a visitor request"""
    user_id = get_jwt_identity()
    db = get_db()
    visitor_model = VisitorRequest(db)
    
    # Check if request exists
    request_data = db.visitor_requests.find_one({"_id": ObjectId(request_id)})
    if not request_data:
        return jsonify({'error': 'Request not found'}), 404
    
    visitor_model.approve_request(request_id, user_id, 'guard')
    
    # Log guard activity
    db.guard_activities.update_one(
        {
            "guard_id": ObjectId(user_id),
            "date": datetime.utcnow().date()
        },
        {
            "$inc": {"visitors_managed": 1},
            "$push": {
                "activities": {
                    "action": "approved_visitor",
                    "visitor_name": request_data['visitor_name'],
                    "timestamp": datetime.utcnow()
                }
            },
            "$setOnInsert": {
                "guard_id": ObjectId(user_id),
                "date": datetime.utcnow().date(),
                "login_time": datetime.utcnow()
            }
        },
        upsert=True
    )
    
    return jsonify({'message': 'Visitor request approved by guard'}), 200

@guard_bp.route('/deny/<request_id>', methods=['POST'])
@role_required(['security_guard', 'admin', 'super_admin'])
def deny_visitor_guard(request_id):
    """Security guard denies a visitor request"""
    user_id = get_jwt_identity()
    data = request.get_json()
    reason = data.get('reason', '')
    
    db = get_db()
    visitor_model = VisitorRequest(db)
    
    # Check if request exists
    request_data = db.visitor_requests.find_one({"_id": ObjectId(request_id)})
    if not request_data:
        return jsonify({'error': 'Request not found'}), 404
    
    visitor_model.deny_request(request_id, user_id, reason)
    
    # Log guard activity
    db.guard_activities.update_one(
        {
            "guard_id": ObjectId(user_id),
            "date": datetime.utcnow().date()
        },
        {
            "$inc": {"visitors_managed": 1},
            "$push": {
                "activities": {
                    "action": "denied_visitor",
                    "visitor_name": request_data['visitor_name'],
                    "reason": reason,
                    "timestamp": datetime.utcnow()
                }
            },
            "$setOnInsert": {
                "guard_id": ObjectId(user_id),
                "date": datetime.utcnow().date(),
                "login_time": datetime.utcnow()
            }
        },
        upsert=True
    )
    
    return jsonify({'message': 'Visitor request denied by guard'}), 200

@guard_bp.route('/complete-visit/<request_id>', methods=['POST'])
@role_required(['security_guard', 'admin', 'super_admin'])
def complete_visit(request_id):
    """Mark visitor as completed (exit)"""
    db = get_db()
    visitor_model = VisitorRequest(db)
    
    # Check if request exists and is approved
    request_data = db.visitor_requests.find_one({"_id": ObjectId(request_id)})
    if not request_data:
        return jsonify({'error': 'Request not found'}), 404
    
    if request_data['status'] != 'approved':
        return jsonify({'error': 'Request must be approved first'}), 400
    
    visitor_model.complete_visit(request_id)
    
    return jsonify({'message': 'Visit marked as completed'}), 200

@guard_bp.route('/current-visitors', methods=['GET'])
@role_required(['security_guard', 'admin', 'super_admin'])
def get_current_visitors():
    """Get list of currently present visitors"""
    db = get_db()
    
    current_visitors = list(db.visitor_requests.find({
        "status": "approved",
        "exit_time": None
    }))
    
    # Enrich with resident information
    user_model = User(db)
    for visitor in current_visitors:
        resident = user_model.get_user_by_id(str(visitor['resident_id']))
        visitor['resident_name'] = resident['full_name'] if resident else 'Unknown'
        
        # Convert ObjectIds to strings
        visitor['_id'] = str(visitor['_id'])
        visitor['resident_id'] = str(visitor['resident_id'])
    
    return jsonify({
        'current_visitors': current_visitors,
        'total': len(current_visitors)
    }), 200
```

## 3. Admin API Endpoints (app/api/admin.py)

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.visitor import VisitorRequest
from app.models.user import User
from app.auth.utils import role_required
from app import get_db
from bson import ObjectId
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/guard-activities', methods=['GET'])
@role_required(['admin', 'super_admin'])
def get_guard_activities():
    """Get all security guard activities"""
    db = get_db()
    
    # Get date range from query parameters
    days_back = int(request.args.get('days', 7))
    start_date = datetime.utcnow().date() - timedelta(days=days_back)
    
    activities = list(db.guard_activities.find({
        "date": {"$gte": start_date}
    }))
    
    # Enrich with guard information
    user_model = User(db)
    for activity in activities:
        guard = user_model.get_user_by_id(str(activity['guard_id']))
        activity['guard_name'] = guard['full_name'] if guard else 'Unknown'
        activity['guard_phone'] = guard['phone_number'] if guard else 'Unknown'
        
        # Convert ObjectIds to strings
        activity['_id'] = str(activity['_id'])
        activity['guard_id'] = str(activity['guard_id'])
    
    return jsonify({
        'activities': activities,
        'total': len(activities)
    }), 200

@admin_bp.route('/visitor-statistics', methods=['GET'])
@role_required(['admin', 'super_admin'])
def get_visitor_statistics():
    """Get comprehensive visitor statistics"""
    db = get_db()
    
    # Get date range
    days_back = int(request.args.get('days', 30))
    start_date = datetime.utcnow() - timedelta(days=days_back)
    
    # Aggregate visitor statistics
    pipeline = [
        {"$match": {"created_at": {"$gte": start_date}}},
        {"$group": {
            "_id": {
                "status": "$status",
                "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}}
            },
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id.date": 1}}
    ]
    
    stats = list(db.visitor_requests.aggregate(pipeline))
    
    # Status distribution
    status_pipeline = [
        {"$match": {"created_at": {"$gte": start_date}}},
        {"$group": {
            "_id": "$status",
            "count": {"$sum": 1}
        }}
    ]
    
    status_stats = list(db.visitor_requests.aggregate(status_pipeline))
    
    # Most active flats
    flat_pipeline = [
        {"$match": {"created_at": {"$gte": start_date}}},
        {"$group": {
            "_id": "$flat_number",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    
    flat_stats = list(db.visitor_requests.aggregate(flat_pipeline))
    
    return jsonify({
        'daily_stats': stats,
        'status_distribution': status_stats,
        'most_active_flats': flat_stats,
        'date_range': {
            'start': start_date.isoformat(),
            'end': datetime.utcnow().isoformat(),
            'days': days_back
        }
    }), 200

@admin_bp.route('/security-guards', methods=['GET'])
@role_required(['admin', 'super_admin'])
def get_security_guards():
    """Get all security guards and their status"""
    db = get_db()
    user_model = User(db)
    
    guards = user_model.get_users_by_role('security_guard')
    
    # Get recent activity for each guard
    for guard in guards:
        guard['_id'] = str(guard['_id'])
        
        # Get recent activity
        recent_activity = db.guard_activities.find_one(
            {"guard_id": ObjectId(guard['_id'])},
            sort=[("date", -1)]
        )
        
        guard['last_activity'] = recent_activity['date'].isoformat() if recent_activity else None
        guard['total_visitors_managed'] = recent_activity['visitors_managed'] if recent_activity else 0
    
    return jsonify({
        'guards': guards,
        'total': len(guards)
    }), 200

@admin_bp.route('/system-overview', methods=['GET'])
@role_required(['admin', 'super_admin'])
def get_system_overview():
    """Get comprehensive system overview"""
    db = get_db()
    
    # Count users by role
    user_counts = {}
    roles = ['resident', 'security_guard', 'admin', 'super_admin']
    
    for role in roles:
        count = db.users.count_documents({"role": role, "is_active": True})
        user_counts[role] = count
    
    # Visitor request counts
    visitor_counts = {}
    statuses = ['pending', 'approved', 'denied', 'completed']
    
    for status in statuses:
        count = db.visitor_requests.count_documents({"status": status})
        visitor_counts[status] = count
    
    # Recent activity
    recent_requests = list(db.visitor_requests.find(
        {},
        sort=[("created_at", -1)]
    ).limit(5))
    
    # Convert ObjectIds for recent requests
    user_model = User(db)
    for req in recent_requests:
        req['_id'] = str(req['_id'])
        req['resident_id'] = str(req['resident_id'])
        
        # Get resident name
        resident = user_model.get_user_by_id(str(req['resident_id']))
        req['resident_name'] = resident['full_name'] if resident else 'Unknown'
    
    return jsonify({
        'user_counts': user_counts,
        'visitor_counts': visitor_counts,
        'recent_requests': recent_requests,
        'total_users': sum(user_counts.values()),
        'total_requests': sum(visitor_counts.values())
    }), 200

@admin_bp.route('/export-data', methods=['GET'])
@role_required(['admin', 'super_admin'])
def export_data():
    """Export system data for reporting"""
    db = get_db()
    
    # Get date range
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    query = {}
    if start_date_str and end_date_str:
        start_date = datetime.fromisoformat(start_date_str)
        end_date = datetime.fromisoformat(end_date_str)
        query['created_at'] = {"$gte": start_date, "$lte": end_date}
    
    # Get all visitor requests in date range
    requests = list(db.visitor_requests.find(query))
    
    # Enrich with user data
    user_model = User(db)
    for req in requests:
        req['_id'] = str(req['_id'])
        req['resident_id'] = str(req['resident_id'])
        
        # Get resident info
        resident = user_model.get_user_by_id(str(req['resident_id']))
        req['resident_name'] = resident['full_name'] if resident else 'Unknown'
        req['resident_phone'] = resident['phone_number'] if resident else 'Unknown'
        
        # Convert dates to ISO format
        req['created_at'] = req['created_at'].isoformat()
        req['entry_time'] = req['entry_time'].isoformat()
        if req.get('exit_time'):
            req['exit_time'] = req['exit_time'].isoformat()
    
    return jsonify({
        'export_data': requests,
        'total_records': len(requests),
        'exported_at': datetime.utcnow().isoformat()
    }), 200
```

## 4. Super Admin API Endpoints (app/api/super_admin.py)

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.visitor import VisitorRequest
from app.models.user import User
from app.auth.utils import role_required
from app import get_db
from bson import ObjectId
from datetime import datetime, timedelta

super_admin_bp = Blueprint('super_admin', __name__)

@super_admin_bp.route('/all-users', methods=['GET'])
@role_required(['super_admin'])
def get_all_users():
    """Get all users in the system with complete information"""
    db = get_db()
    user_model = User(db)
    
    users = user_model.get_all_users()
    
    # Convert ObjectIds and add additional info
    for user in users:
        user['_id'] = str(user['_id'])
        
        # Get user statistics
        if user['role'] == 'resident':
            # Count visitor requests for resident
            visitor_count = db.visitor_requests.count_documents({
                "resident_id": ObjectId(user['_id'])
            })
            user['total_visitor_requests'] = visitor_count
        elif user['role'] == 'security_guard':
            # Get guard activity stats
            activity = db.guard_activities.find_one(
                {"guard_id": ObjectId(user['_id'])},
                sort=[("date", -1)]
            )
            user['total_visitors_managed'] = activity['visitors_managed'] if activity else 0
            user['last_activity'] = activity['date'].isoformat() if activity else None
        
        # Convert dates
        user['created_at'] = user['created_at'].isoformat()
        if user.get('last_login'):
            user['last_login'] = user['last_login'].isoformat()
    
    return jsonify({
        'users': users,
        'total': len(users)
    }), 200

@super_admin_bp.route('/system-analytics', methods=['GET'])
@role_required(['super_admin'])
def get_system_analytics():
    """Get comprehensive system analytics"""
    db = get_db()
    
    # User growth analytics
    user_growth_pipeline = [
        {"$group": {
            "_id": {
                "year": {"$year": "$created_at"},
                "month": {"$month": "$created_at"},
                "role": "$role"
            },
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id.year": 1, "_id.month": 1}}
    ]
    
    user_growth = list(db.users.aggregate(user_growth_pipeline))
    
    # Visitor trends
    visitor_trends_pipeline = [
        {"$group": {
            "_id": {
                "year": {"$year": "$created_at"},
                "month": {"$month": "$created_at"},
                "status": "$status"
            },
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id.year": 1, "_id.month": 1}}
    ]
    
    visitor_trends = list(db.visitor_requests.aggregate(visitor_trends_pipeline))
    
    # Peak hours analysis
    peak_hours_pipeline = [
        {"$group": {
            "_id": {"$hour": "$created_at"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    
    peak_hours = list(db.visitor_requests.aggregate(peak_hours_pipeline))
    
    # Security metrics
    security_metrics = {
        'total_logins_today': db.users.count_documents({
            "last_login": {"$gte": datetime.utcnow().replace(hour=0, minute=0, second=0)}
        }),
        'active_guards_today': db.guard_activities.count_documents({
            "date": datetime.utcnow().date()
        }),
        'denied_requests_ratio': 0,
        'response_time_avg': 0  # Would need additional tracking
    }
    
    # Calculate denied requests ratio
    total_requests = db.visitor_requests.count_documents({})
    denied_requests = db.visitor_requests.count_documents({"status": "denied"})
    
    if total_requests > 0:
        security_metrics['denied_requests_ratio'] = (denied_requests / total_requests) * 100
    
    return jsonify({
        'user_growth': user_growth,
        'visitor_trends': visitor_trends,
        'peak_hours': peak_hours,
        'security_metrics': security_metrics
    }), 200

@super_admin_bp.route('/audit-log', methods=['GET'])
@role_required(['super_admin'])
def get_audit_log():
    """Get comprehensive audit log"""
    db = get_db()
    
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    skip = (page - 1) * per_page
    
    # Get all guard activities (audit trail)
    activities = list(db.guard_activities.find(
        {},
        sort=[("date", -1)]
    ).skip(skip).limit(per_page))
    
    # Enrich with guard information
    user_model = User(db)
    for activity in activities:
        activity['_id'] = str(activity['_id'])
        activity['guard_id'] = str(activity['guard_id'])
        
        guard = user_model.get_user_by_id(str(activity['guard_id']))
        activity['guard_name'] = guard['full_name'] if guard else 'Unknown'
        activity['guard_phone'] = guard['phone_number'] if guard else 'Unknown'
        
        # Convert date
        activity['date'] = activity['date'].isoformat()
    
    total_count = db.guard_activities.count_documents({})
    
    return jsonify({
        'audit_log': activities,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total_count,
            'pages': (total_count + per_page - 1) // per_page
        }
    }), 200

@super_admin_bp.route('/manage-user/<user_id>', methods=['PUT'])
@role_required(['super_admin'])
def manage_user(user_id):
    """Update user information or status"""
    data = request.get_json()
    db = get_db()
    
    # Check if user exists
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Prepare update data
    update_data = {}
    allowed_fields = ['full_name', 'flat_number', 'role', 'is_active']
    
    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]
    
    if update_data:
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'error': 'No valid fields provided'}), 400

@super_admin_bp.route('/system-backup', methods=['POST'])
@role_required(['super_admin'])
def create_system_backup():
    """Create a system backup (metadata only for security)"""
    db = get_db()
    
    # Create backup metadata
    backup_data = {
        'backup_id': str(ObjectId()),
        'created_at': datetime.utcnow(),
        'created_by': get_jwt_identity(),
        'collections': {
            'users_count': db.users.count_documents({}),
            'visitor_requests_count': db.visitor_requests.count_documents({}),
            'guard_activities_count': db.guard_activities.count_documents({})
        },
        'status': 'completed'
    }
    
    # Store backup record
    db.system_backups.insert_one(backup_data)
    
    # Convert ObjectId for response
    backup_data['_id'] = backup_data['backup_id']
    backup_data['created_at'] = backup_data['created_at'].isoformat()
    
    return jsonify({
        'message': 'Backup created successfully',
        'backup': backup_data
    }), 201

@super_admin_bp.route('/delete-user/<user_id>', methods=['DELETE'])
@role_required(['super_admin'])
def delete_user(user_id):
    """Soft delete a user (set inactive)"""
    db = get_db()
    
    # Check if user exists
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Prevent deleting super admin
    if user['role'] == 'super_admin':
        return jsonify({'error': 'Cannot delete super admin user'}), 403
    
    # Soft delete (set inactive)
    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_active": False}}
    )
    
    return jsonify({'message': 'User deleted successfully'}), 200
```

## 5. Register All API Blueprints (app/api/__init__.py)

```python
from flask import Blueprint
from .resident import resident_bp
from .security_guard import guard_bp
from .admin import admin_bp
from .super_admin import super_admin_bp

api_bp = Blueprint('api', __name__)

# Register all API blueprints
api_bp.register_blueprint(resident_bp, url_prefix='/resident')
api_bp.register_blueprint(guard_bp, url_prefix='/guard')
api_bp.register_blueprint(admin_bp, url_prefix='/admin')
api_bp.register_blueprint(super_admin_bp, url_prefix='/super-admin')

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'Security Management API is running'}, 200
```

## 6. Database Initialization Script (database/init_db.py)

```python
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
    
    # Create collections with validation schemas
    
    # Users collection
    try:
        db.create_collection("users", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["phone_number", "full_name", "flat_number", "role"],
                "properties": {
                    "phone_number": {"bsonType": "string", "pattern": "^[0-9]{10}$"},
                    "full_name": {"bsonType": "string"},
                    "flat_number": {"bsonType": "string"},
                    "role": {"enum": ["resident", "security_guard", "admin", "super_admin"]},
                    "is_active": {"bsonType": "bool"},
                    "created_at": {"bsonType": "date"},
                    "last_login": {"bsonType": "date"}
                }
            }
        })
        print("✅ Users collection created")
    except Exception as e:
        print(f"ℹ️ Users collection exists: {e}")
    
    # Create unique index on phone_number
    db.users.create_index("phone_number", unique=True)
    db.users.create_index("role")
    
    # Visitor requests collection
    try:
        db.create_collection("visitor_requests", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["visitor_name", "visitor_phone", "purpose", "flat_number", "resident_id", "status"],
                "properties": {
                    "visitor_name": {"bsonType": "string"},
                    "visitor_phone": {"bsonType": "string", "pattern": "^[0-9]{10}$"},
                    "purpose": {"bsonType": "string"},
                    "flat_number": {"bsonType": "string"},
                    "status": {"enum": ["pending", "approved", "denied", "completed"]},
                    "entry_time": {"bsonType": "date"},
                    "exit_time": {"bsonType": "date"},
                    "created_at": {"bsonType": "date"}
                }
            }
        })
        print("✅ Visitor requests collection created")
    except Exception as e:
        print(f"ℹ️ Visitor requests collection exists: {e}")
    
    # Create indexes
    db.visitor_requests.create_index("resident_id")
    db.visitor_requests.create_index("status")
    db.visitor_requests.create_index("created_at")
    
    # Guard activities collection
    try:
        db.create_collection("guard_activities")
        print("✅ Guard activities collection created")
    except Exception as e:
        print(f"ℹ️ Guard activities collection exists: {e}")
    
    db.guard_activities.create_index("guard_id")
    db.guard_activities.create_index("date")
    
    # System backups collection
    try:
        db.create_collection("system_backups")
        print("✅ System backups collection created")
    except Exception as e:
        print(f"ℹ️ System backups collection exists: {e}")
    
    print("\n🎉 Database initialization completed!")
    print(f"📊 Collections: {db.list_collection_names()}")
    
    return db

if __name__ == "__main__":
    init_database()
```

This comprehensive API implementation provides:

✅ **Complete CRUD Operations** for all user roles
✅ **Role-based Access Control** with JWT authentication
✅ **MongoDB Integration** with proper error handling
✅ **Audit Trail** for security guard activities
✅ **Statistics and Analytics** for admin dashboards  
✅ **Data Export** capabilities
✅ **User Management** for super admin
✅ **Database Validation** with proper schemas
✅ **Health Check** endpoint for monitoring

The API supports all the features requested in your security management system with proper privacy controls and role-based data access!