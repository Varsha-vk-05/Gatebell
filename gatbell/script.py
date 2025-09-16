# Create a comprehensive project structure and implementation files
import json
import os

# Project structure
project_structure = {
    "security_management_system/": {
        "backend/": {
            "app/": {
                "__init__.py": "Flask app initialization",
                "config.py": "Configuration settings including debug mode",
                "models/": {
                    "__init__.py": "",
                    "user.py": "User models for all roles",
                    "visitor.py": "Visitor request models"
                },
                "auth/": {
                    "__init__.py": "",
                    "routes.py": "Authentication routes",
                    "utils.py": "JWT and auth utilities"
                },
                "api/": {
                    "__init__.py": "",
                    "resident.py": "Resident API endpoints",
                    "security_guard.py": "Security guard endpoints", 
                    "admin.py": "Admin endpoints",
                    "super_admin.py": "Super admin endpoints"
                }
            },
            "requirements.txt": "Python dependencies",
            "run.py": "Flask application runner"
        },
        "frontend/": {
            "src/": {
                "components/": {
                    "Login3D.jsx": "3D login card component",
                    "Registration3D.jsx": "3D registration form",
                    "Dashboard3D.jsx": "3D dashboard components",
                    "Common/": {
                        "Header.jsx": "Navigation header",
                        "ProtectedRoute.jsx": "Route protection"
                    }
                },
                "pages/": {
                    "ResidentDashboard.jsx": "Resident dashboard page",
                    "SecurityGuardDashboard.jsx": "Security guard page",
                    "AdminDashboard.jsx": "Admin dashboard",
                    "SuperAdminDashboard.jsx": "Super admin dashboard"
                },
                "utils/": {
                    "auth.js": "JWT auth utilities",
                    "api.js": "API client"
                },
                "styles/": {
                    "3d-effects.css": "3D CSS animations",
                    "globals.css": "Global styles"
                }
            },
            "package.json": "React dependencies",
            "public/": {
                "index.html": "Main HTML file"
            }
        },
        "database/": {
            "init_db.py": "Database initialization script",
            "sample_data.py": "Sample data for testing"
        },
        "README.md": "Setup instructions",
        ".env.example": "Environment variables template"
    }
}

print("🏗️ Security Management System Project Structure")
print("=" * 50)

def print_structure(structure, indent=0):
    for key, value in structure.items():
        print("  " * indent + "📁 " + key if key.endswith("/") else "  " * indent + "📄 " + key)
        if isinstance(value, dict):
            print_structure(value, indent + 1)
        elif value:
            print("  " * (indent + 1) + "💡 " + value)

print_structure(project_structure)

# Database schema design
database_schema = {
    "users": {
        "_id": "ObjectId (auto-generated)",
        "phone_number": "String (10 digits, unique)",
        "full_name": "String",
        "flat_number": "String", 
        "role": "String (resident/security_guard/admin/super_admin)",
        "created_at": "DateTime",
        "last_login": "DateTime",
        "is_active": "Boolean"
    },
    "visitor_requests": {
        "_id": "ObjectId (auto-generated)",
        "visitor_name": "String",
        "visitor_phone": "String (10 digits)",
        "purpose": "String",
        "flat_number": "String (requested flat)",
        "resident_id": "ObjectId (reference to users)",
        "entry_time": "DateTime",
        "exit_time": "DateTime (nullable)",
        "status": "String (pending/approved/denied/completed)",
        "approved_by_guard": "ObjectId (reference to security guard)",
        "approved_by_resident": "ObjectId (reference to resident)",
        "created_at": "DateTime",
        "notes": "String (optional)"
    },
    "guard_activities": {
        "_id": "ObjectId (auto-generated)", 
        "guard_id": "ObjectId (reference to users)",
        "login_time": "DateTime",
        "logout_time": "DateTime (nullable)",
        "visitors_managed": "Integer",
        "activities": "Array of activity logs",
        "date": "Date"
    }
}

print("\n\n🗄️ Database Schema Design")
print("=" * 30)
for collection, fields in database_schema.items():
    print(f"\n📋 Collection: {collection}")
    for field, description in fields.items():
        print(f"   • {field}: {description}")

# Save project info to CSV for reference
import csv
import pandas as pd

# Create implementation checklist
checklist_data = [
    ["Component", "Description", "Priority", "Dependencies"],
    ["Flask Backend Setup", "Initialize Flask app with MongoDB", "High", "Flask, PyMongo, Flask-JWT-Extended"],
    ["User Authentication", "Phone number login with debug mode", "High", "JWT, MongoDB"],
    ["Role-Based Access Control", "Implement RBAC with JWT claims", "High", "Flask-JWT-Extended"],
    ["3D Frontend Components", "React components with 3D CSS effects", "Medium", "React, CSS3"],
    ["API Endpoints", "CRUD operations for all user roles", "High", "Flask-RESTful"],
    ["Database Models", "MongoDB schemas for users and visitors", "High", "PyMongo, Marshmallow"],
    ["JWT Integration", "Token-based authentication", "High", "Flask-JWT-Extended"],
    ["Debug Mode Toggle", "Configuration-based debug mode", "Medium", "Config management"],
    ["3D CSS Animations", "Hover effects and transitions", "Low", "CSS3 transforms"],
    ["Dashboard Components", "Role-specific dashboards", "Medium", "React components"]
]

# Convert to DataFrame and save
df = pd.DataFrame(checklist_data[1:], columns=checklist_data[0])
df.to_csv('security_system_implementation_checklist.csv', index=False)

print(f"\n\n✅ Implementation checklist saved as CSV")
print("File: security_system_implementation_checklist.csv")
print(f"Total components: {len(df)} items")