# React Frontend Implementation - 3D Security Management UI

## 1. Package.json Dependencies

```json
{
  "name": "security-management-frontend",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.14.2",
    "axios": "^1.4.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "proxy": "http://localhost:5000"
}
```

## 2. 3D CSS Effects (src/styles/3d-effects.css)

```css
/* Root Variables for 3D Effects */
:root {
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  --shadow-color: rgba(0, 0, 0, 0.1);
  --hover-shadow: rgba(0, 0, 0, 0.2);
  --glow-color: rgba(102, 126, 234, 0.4);
}

/* 3D Card Base */
.card-3d {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 2rem;
  transform-style: preserve-3d;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.1),
    0 2px 8px rgba(0, 0, 0, 0.05);
}

.card-3d:hover {
  transform: translateY(-8px) rotateX(2deg);
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 8px 16px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.3);
}

/* 3D Login Card */
.login-card-3d {
  max-width: 400px;
  margin: 2rem auto;
  background: linear-gradient(145deg, 
    rgba(255, 255, 255, 0.1), 
    rgba(255, 255, 255, 0.05)
  );
  perspective: 1000px;
}

.login-card-3d::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--primary-gradient);
  border-radius: 20px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.login-card-3d:hover::before {
  opacity: 0.1;
}

/* 3D Input Fields */
.input-3d {
  width: 100%;
  padding: 1rem 1.5rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: #333;
  font-size: 1rem;
  outline: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
}

.input-3d:focus {
  border-color: #667eea;
  background: rgba(255, 255, 255, 0.2);
  transform: translateZ(4px);
  box-shadow: 
    0 8px 25px rgba(102, 126, 234, 0.15),
    0 4px 10px rgba(0, 0, 0, 0.1);
}

.input-3d::placeholder {
  color: rgba(51, 51, 51, 0.7);
}

/* 3D Buttons */
.btn-3d {
  padding: 1rem 2rem;
  border: none;
  border-radius: 15px;
  background: var(--primary-gradient);
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transform-style: preserve-3d;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.btn-3d::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.3), 
    transparent
  );
  transition: left 0.5s ease;
}

.btn-3d:hover {
  transform: translateY(-2px) translateZ(4px);
  box-shadow: 
    0 10px 30px var(--glow-color),
    0 5px 15px rgba(0, 0, 0, 0.2);
}

.btn-3d:hover::before {
  left: 100%;
}

.btn-3d:active {
  transform: translateY(0) translateZ(2px);
  box-shadow: 
    0 5px 15px var(--glow-color),
    0 2px 8px rgba(0, 0, 0, 0.15);
}

/* 3D Dashboard Cards */
.dashboard-card-3d {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 2rem;
  margin: 1rem;
  transform-style: preserve-3d;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.1),
    0 5px 15px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
}

.dashboard-card-3d::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: conic-gradient(
    from 0deg,
    transparent,
    rgba(102, 126, 234, 0.1),
    transparent,
    rgba(118, 75, 162, 0.1),
    transparent
  );
  animation: rotate 10s linear infinite;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.dashboard-card-3d:hover::after {
  opacity: 1;
}

.dashboard-card-3d:hover {
  transform: translateY(-10px) rotateX(5deg) rotateY(2deg);
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.15),
    0 10px 25px rgba(0, 0, 0, 0.1);
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 3D Loading Animation */
.loading-3d {
  width: 60px;
  height: 60px;
  margin: 2rem auto;
  perspective: 1000px;
}

.loading-cube {
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  animation: cube-spin 2s infinite linear;
}

.loading-face {
  position: absolute;
  width: 60px;
  height: 60px;
  background: var(--primary-gradient);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.loading-face:nth-child(1) { transform: rotateY(0deg) translateZ(30px); }
.loading-face:nth-child(2) { transform: rotateY(90deg) translateZ(30px); }
.loading-face:nth-child(3) { transform: rotateY(180deg) translateZ(30px); }
.loading-face:nth-child(4) { transform: rotateY(-90deg) translateZ(30px); }
.loading-face:nth-child(5) { transform: rotateX(90deg) translateZ(30px); }
.loading-face:nth-child(6) { transform: rotateX(-90deg) translateZ(30px); }

@keyframes cube-spin {
  0% { transform: rotateX(0deg) rotateY(0deg); }
  100% { transform: rotateX(360deg) rotateY(360deg); }
}

/* 3D Hover Effects for Lists */
.list-item-3d {
  padding: 1rem;
  margin: 0.5rem 0;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
  border-left: 4px solid transparent;
}

.list-item-3d:hover {
  transform: translateX(8px) translateZ(4px);
  background: rgba(255, 255, 255, 1);
  border-left-color: #667eea;
  box-shadow: 
    0 8px 25px rgba(0, 0, 0, 0.1),
    0 4px 12px rgba(0, 0, 0, 0.05);
}

/* 3D Notification/Alert */
.alert-3d {
  padding: 1rem 1.5rem;
  border-radius: 15px;
  margin: 1rem 0;
  transform-style: preserve-3d;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.alert-3d.success {
  background: var(--success-gradient);
  color: white;
}

.alert-3d.error {
  background: var(--secondary-gradient);
  color: white;
}

.alert-3d:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

/* Responsive 3D Effects */
@media (max-width: 768px) {
  .card-3d:hover {
    transform: translateY(-4px) rotateX(1deg);
  }
  
  .dashboard-card-3d:hover {
    transform: translateY(-5px) rotateX(2deg);
  }
  
  .btn-3d:hover {
    transform: translateY(-1px) translateZ(2px);
  }
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
  .card-3d {
    background: rgba(0, 0, 0, 0.2);
    border-color: rgba(255, 255, 255, 0.1);
    color: white;
  }
  
  .input-3d {
    background: rgba(0, 0, 0, 0.2);
    border-color: rgba(255, 255, 255, 0.1);
    color: white;
  }
  
  .input-3d::placeholder {
    color: rgba(255, 255, 255, 0.7);
  }
}
```

## 3. 3D Login Component (src/components/Login3D.jsx)

```jsx
import React, { useState } from 'react';
import '../styles/3d-effects.css';
import { authAPI } from '../utils/api';

const Login3D = ({ onLogin }) => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [step, setStep] = useState('phone'); // 'phone', 'otp', 'register'
  const [showRegistration, setShowRegistration] = useState(false);

  const handlePhoneSubmit = async (e) => {
    e.preventDefault();
    if (phoneNumber.length !== 10) {
      setError('Please enter a valid 10-digit phone number');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await authAPI.phoneLogin(phoneNumber);
      
      if (response.needs_registration) {
        setShowRegistration(true);
        setStep('register');
      } else if (response.needs_otp_verification) {
        setStep('otp');
      } else {
        // Debug mode - direct login
        localStorage.setItem('token', response.access_token);
        onLogin(response.user);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  const LoadingCube = () => (
    <div className="loading-3d">
      <div className="loading-cube">
        <div className="loading-face"></div>
        <div className="loading-face"></div>
        <div className="loading-face"></div>
        <div className="loading-face"></div>
        <div className="loading-face"></div>
        <div className="loading-face"></div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-400 via-pink-500 to-red-500">
      <div className="card-3d login-card-3d">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Security Management
          </h1>
          <p className="text-gray-600">Enter your phone number to continue</p>
        </div>

        {error && (
          <div className="alert-3d error mb-4">
            {error}
          </div>
        )}

        {isLoading ? (
          <LoadingCube />
        ) : (
          <form onSubmit={handlePhoneSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Phone Number
              </label>
              <input
                type="tel"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value.replace(/\D/g, '').slice(0, 10))}
                placeholder="Enter 10-digit phone number"
                className="input-3d"
                required
              />
            </div>

            <button
              type="submit"
              className="btn-3d w-full"
              disabled={isLoading || phoneNumber.length !== 10}
            >
              {step === 'phone' ? 'Continue' : 'Verify'}
            </button>
          </form>
        )}

        <div className="text-center mt-6">
          <p className="text-sm text-gray-600">
            Secure access for residents, guards, and administrators
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login3D;
```

## 4. 3D Registration Component (src/components/Registration3D.jsx)

```jsx
import React, { useState } from 'react';
import '../styles/3d-effects.css';
import { authAPI } from '../utils/api';

const Registration3D = ({ phoneNumber, onRegister }) => {
  const [formData, setFormData] = useState({
    full_name: '',
    flat_number: '',
    role: 'resident'
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await authAPI.register({
        phone_number: phoneNumber,
        ...formData
      });
      
      localStorage.setItem('token', response.access_token);
      onRegister(response.user);
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-400 via-purple-500 to-pink-500">
      <div className="card-3d login-card-3d">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Complete Registration
          </h1>
          <p className="text-gray-600">Phone: {phoneNumber}</p>
        </div>

        {error && (
          <div className="alert-3d error mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Full Name
            </label>
            <input
              type="text"
              name="full_name"
              value={formData.full_name}
              onChange={handleInputChange}
              placeholder="Enter your full name"
              className="input-3d"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Flat Number
            </label>
            <input
              type="text"
              name="flat_number"
              value={formData.flat_number}
              onChange={handleInputChange}
              placeholder="e.g., A-101"
              className="input-3d"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Role
            </label>
            <select
              name="role"
              value={formData.role}
              onChange={handleInputChange}
              className="input-3d"
            >
              <option value="resident">Resident</option>
              <option value="security_guard">Security Guard</option>
              <option value="admin">Admin</option>
              <option value="super_admin">Super Admin</option>
            </select>
          </div>

          <button
            type="submit"
            className="btn-3d w-full"
            disabled={isLoading || !formData.full_name || !formData.flat_number}
          >
            {isLoading ? 'Creating Account...' : 'Complete Registration'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Registration3D;
```

## 5. 3D Dashboard Component (src/components/Dashboard3D.jsx)

```jsx
import React from 'react';
import '../styles/3d-effects.css';

const Dashboard3D = ({ user, children }) => {
  const getRoleColor = (role) => {
    const colors = {
      resident: 'from-blue-400 to-blue-600',
      security_guard: 'from-green-400 to-green-600',
      admin: 'from-purple-400 to-purple-600',
      super_admin: 'from-red-400 to-red-600'
    };
    return colors[role] || colors.resident;
  };

  const getRoleTitle = (role) => {
    const titles = {
      resident: 'Resident Dashboard',
      security_guard: 'Security Guard Dashboard',
      admin: 'Admin Dashboard',
      super_admin: 'Super Admin Dashboard'
    };
    return titles[role] || 'Dashboard';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-gray-200">
      {/* Header */}
      <div className={`bg-gradient-to-r ${getRoleColor(user.role)} p-6 shadow-lg`}>
        <div className="container mx-auto">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-white mb-1">
                {getRoleTitle(user.role)}
              </h1>
              <p className="text-white/80">
                Welcome, {user.full_name} • Flat {user.flat_number}
              </p>
            </div>
            <div className="text-right">
              <p className="text-white/80 text-sm">Role</p>
              <p className="text-white font-semibold capitalize">
                {user.role.replace('_', ' ')}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto p-6">
        {children}
      </div>
    </div>
  );
};

export const EmptyDashboard3D = () => (
  <div className="dashboard-card-3d text-center">
    <div className="text-6xl mb-4">🏠</div>
    <h2 className="text-2xl font-bold text-gray-800 mb-2">
      Welcome to Your Dashboard
    </h2>
    <p className="text-gray-600 mb-4">
      No visitor requests yet. When visitors request access to your flat, 
      they will appear here for your approval.
    </p>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
      <div className="list-item-3d text-center p-4">
        <div className="text-3xl mb-2">👥</div>
        <h3 className="font-semibold">Visitor Requests</h3>
        <p className="text-sm text-gray-600">Approve or deny visitor access</p>
      </div>
      <div className="list-item-3d text-center p-4">
        <div className="text-3xl mb-2">🔐</div>
        <h3 className="font-semibold">Security</h3>
        <p className="text-sm text-gray-600">Secure access control system</p>
      </div>
      <div className="list-item-3d text-center p-4">
        <div className="text-3xl mb-2">📱</div>
        <h3 className="font-semibold">Real-time Updates</h3>
        <p className="text-sm text-gray-600">Get notified instantly</p>
      </div>
    </div>
  </div>
);

export default Dashboard3D;
```

## 6. API Utilities (src/utils/api.js)

```javascript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  phoneLogin: (phoneNumber) => 
    apiClient.post('/auth/phone-login', { phone_number: phoneNumber }),
  
  verifyOTP: (phoneNumber, otp) => 
    apiClient.post('/auth/verify-otp', { phone_number: phoneNumber, otp }),
  
  register: (userData) => 
    apiClient.post('/auth/register', userData),
  
  getProfile: () => 
    apiClient.get('/auth/profile'),
};

export const residentAPI = {
  getVisitorRequests: () => 
    apiClient.get('/api/resident/visitor-requests'),
  
  approveVisitor: (requestId) => 
    apiClient.post(`/api/resident/approve/${requestId}`),
  
  denyVisitor: (requestId, reason) => 
    apiClient.post(`/api/resident/deny/${requestId}`, { reason }),
};

export const guardAPI = {
  getVisitorRequests: () => 
    apiClient.get('/api/guard/visitor-requests'),
  
  approveVisitor: (requestId) => 
    apiClient.post(`/api/guard/approve/${requestId}`),
  
  denyVisitor: (requestId, reason) => 
    apiClient.post(`/api/guard/deny/${requestId}`, { reason }),
  
  createVisitorRequest: (visitorData) => 
    apiClient.post('/api/guard/visitor-request', visitorData),
};

export const adminAPI = {
  getGuardActivities: () => 
    apiClient.get('/api/admin/guard-activities'),
  
  getAllVisitorRequests: () => 
    apiClient.get('/api/admin/visitor-requests'),
  
  getStatistics: () => 
    apiClient.get('/api/admin/statistics'),
};

export const superAdminAPI = {
  getAllUsers: () => 
    apiClient.get('/api/super-admin/users'),
  
  getAllData: () => 
    apiClient.get('/api/super-admin/all-data'),
  
  getSystemStats: () => 
    apiClient.get('/api/super-admin/system-stats'),
};

export default apiClient;
```

## 7. Main App Component (src/App.jsx)

```jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login3D from './components/Login3D';
import Registration3D from './components/Registration3D';
import Dashboard3D, { EmptyDashboard3D } from './components/Dashboard3D';
import ResidentDashboard from './pages/ResidentDashboard';
import SecurityGuardDashboard from './pages/SecurityGuardDashboard';
import AdminDashboard from './pages/AdminDashboard';
import SuperAdminDashboard from './pages/SuperAdminDashboard';
import { authAPI } from './utils/api';
import './styles/3d-effects.css';

function App() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showRegistration, setShowRegistration] = useState(false);
  const [phoneNumber, setPhoneNumber] = useState('');

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await authAPI.getProfile();
        setUser(response.user);
      } catch (error) {
        localStorage.removeItem('token');
      }
    }
    setIsLoading(false);
  };

  const handleLogin = (userData) => {
    setUser(userData);
    setShowRegistration(false);
  };

  const handleRegistration = (userData) => {
    setUser(userData);
    setShowRegistration(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const getDashboardComponent = () => {
    if (!user) return <Navigate to="/login" />;

    switch (user.role) {
      case 'resident':
        return (
          <Dashboard3D user={user}>
            <ResidentDashboard user={user} />
          </Dashboard3D>
        );
      case 'security_guard':
        return (
          <Dashboard3D user={user}>
            <SecurityGuardDashboard user={user} />
          </Dashboard3D>
        );
      case 'admin':
        return (
          <Dashboard3D user={user}>
            <AdminDashboard user={user} />
          </Dashboard3D>
        );
      case 'super_admin':
        return (
          <Dashboard3D user={user}>
            <SuperAdminDashboard user={user} />
          </Dashboard3D>
        );
      default:
        return (
          <Dashboard3D user={user}>
            <EmptyDashboard3D />
          </Dashboard3D>
        );
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="loading-3d">
          <div className="loading-cube">
            <div className="loading-face"></div>
            <div className="loading-face"></div>
            <div className="loading-face"></div>
            <div className="loading-face"></div>
            <div className="loading-face"></div>
            <div className="loading-face"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route 
            path="/login" 
            element={
              user ? <Navigate to="/dashboard" /> : 
              showRegistration ? 
                <Registration3D 
                  phoneNumber={phoneNumber} 
                  onRegister={handleRegistration} 
                /> :
                <Login3D 
                  onLogin={(userData, needsRegistration, phone) => {
                    if (needsRegistration) {
                      setPhoneNumber(phone);
                      setShowRegistration(true);
                    } else {
                      handleLogin(userData);
                    }
                  }} 
                />
            } 
          />
          <Route 
            path="/dashboard" 
            element={getDashboardComponent()} 
          />
          <Route 
            path="/" 
            element={
              user ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
            } 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
```

This React frontend provides:
- ✅ 3D login card with phone number input
- ✅ 3D registration form with role selection
- ✅ 3D dashboard with role-based layouts
- ✅ Modern CSS 3D effects and animations
- ✅ JWT token management
- ✅ Role-based routing and components
- ✅ Responsive design with mobile support
- ✅ Loading animations and error handling