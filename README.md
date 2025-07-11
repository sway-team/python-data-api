# DataApi Management System

A system for quickly configuring data and developing page APPs. You can also think of it as a lightweight low-code platform for personal use, which will shine even more in the AI era. The following is an AI-organized guide. Welcome to try it out.

A modern data management system based on Flask + Vite + Tailwind CSS, providing user authentication, data management, and API services.

## 🚀 Project Features

### Backend Features (Flask)
- **User Management**: User registration, login, authentication
- **Dataset Management**: CRUD operations, filtering, and combined queries
- **API Services**: Provides simple and easy-to-use API interfaces, supporting complex data queries
- **Database Operations**: ORM operations based on SQLAlchemy
- **Logging**: Complete operation log records
- **CORS Support**: Cross-origin request support

### Frontend Features (Vite + Tailwind CSS)
- **Modern UI**: Responsive design based on Tailwind CSS
- **User Interfaces**: Login, registration, user center, data management pages
- **Componentization**: Modular frontend component system
- **Hot Reload**: Vite dev server supports real-time hot updates
- **Animation Effects**: Smooth animations with Animate.css

## 📁 Project Structure

```
python-data-api-open/
├── api/                    # API route modules
│   ├── dataset.py         # Dataset management API
│   ├── frame.py           # Framework-related API
│   ├── service.py         # Service API
│   └── user.py            # User management API
├── comp/                   # Core components
│   ├── base.py            # Base class
│   ├── cache.py           # Cache component
│   ├── datalogic.py       # Data logic
│   ├── db.py              # Database operations
│   ├── emaillogic.py      # Email logic
│   ├── smsJDlogic.py      # SMS logic
│   └── tool.py            # Utility functions
├── conf/                   # Configuration files
│   └── workflow.py        # Workflow configuration
├── static/                 # Frontend static resources
│   ├── app/               # Application pages
│   │   ├── login.html     # Login page
│   │   ├── datamanage.html # Data management page
│   │   └── usercenter.html # User center page
│   ├── assets/            # Static assets
│   │   ├── css/           # Stylesheets
│   │   ├── js/            # JavaScript files
│   │   ├── images/        # Images
│   │   └── template/      # Template files
│   ├── package.json       # Frontend dependencies
│   ├── vite.config.js     # Vite configuration
│   └── tailwind.config.js # Tailwind CSS configuration
├── app.py                  # Flask application entry
├── env.py                  # Environment configuration
├── requirements.txt        # Python dependencies
├── init.py                 # Database initialization script
├── start.sh                # Startup script
├── stop.sh                 # Stop script
└── README.md               # Project documentation
```

## 🛠️ Installation Steps

### 1. Clone the Project
```bash
git clone <repository-url>
cd python-data-api-open
```

### 2. Configure the Environment
Edit the `env.py` file to set up your database connection:
```python
# Database configuration
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "your_username"
DB_PWD = "your_password"
DB_NAME = "your_database"

# Flask configuration
FLASK_RUN_PORT = 5070
SECRET_KEY = "your_secret_key"

# Page configuration
PAGE_HOST = "http://localhost:5173"
```

### 3. Run the Initialization Script
```bash
python init.py
```
This script will automatically:
- Install Python dependencies (`pip install -r requirements.txt`)
- Install frontend dependencies (`cd static && npm install`)
- Initialize database tables
- Import initial data

### 4. Start the Services

#### Method 1: Use the Startup Script (Recommended)
```bash
# Start both backend and frontend
./start.sh

# Stop the services
./stop.sh

# In a new terminal, start frontend service
cd static
npm run dev
```

#### Method 2: Start Manually
```bash
# Start backend service
python app.py

# In a new terminal, start frontend service
cd static
npm run dev
```

## 🎯 Usage Guide

### Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5070

### Main Features

#### 1. User Management
- Visit `/app/login` for user login/registration
- Supports mobile verification code registration
- User authentication and session management

#### 2. Data Management
- Visit `/app/datamanage` for data management
- Supports CRUD operations on data
- Provides advanced filtering and search features
- Supports combined data queries

#### 3. API Endpoints
- `/dataset/*` - Dataset management API (for external system access)
- `/user/*` - User management API (for internal authentication)
- `/frame/*` - Framework configuration API
- `/service/*` - Service API (for internal system access)

### Development Mode

#### Frontend Development
```bash
cd static
npm run dev          # Start Vite dev server
```

#### Backend Development
```bash
python app.py        # Start Flask dev server
```

## 🔧 Tech Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **PyMySQL**: MySQL database driver
- **Flask-CORS**: CORS support
- **Gunicorn**: WSGI server

### Frontend
- **Vite**: Modern build tool
- **Tailwind CSS**: Utility-first CSS framework
- **jQuery**: JavaScript library
- **Animate.css**: CSS animation library
- **Font Awesome**: Icon library
- **jQuery AppManager**: Custom page app manager


#### 🚀 Benefits

- **Low-Code Development**: Rapid UI development with minimal JavaScript
- **Component Reusability**: Modular components that can be shared across pages
- **Consistent UX**: Standardized dialog, form, and interaction patterns
- **Type Safety**: Structured data flow and validation
- **Performance**: Efficient DOM manipulation and event handling

## 📝 Configuration

### Database Configuration
Set database connection parameters in `env.py`:
```python
DB_HOST = "localhost"      # Database host
DB_PORT = 3306            # Database port
DB_USER = "root"          # Database username
DB_PWD = "password"       # Database password
DB_NAME = "datain"        # Database name
```

### Frontend Configuration
Configure Vite in `static/vite.config.js`:
```javascript
import { defineConfig } from 'vite'

export default defineConfig({
  root: '.',
  server: {
    host: '0.0.0.0',
    port: 5173
  }
})
```

## 🚨 Notes

1. **Port Configuration**: Make sure ports 5070 and 5173 are available
2. **Database**: Ensure MySQL service is running and configured correctly
3. **Node.js**: Node.js (v16+) is required
4. **Python**: Python 3.8+ is recommended

## 🐛 Troubleshooting

### Common Issues

1. **Port Occupied**
   ```bash
   # Check port usage
   lsof -i :5070
   lsof -i :5173
   ```

2. **Database Connection Failure**
   - Check database configuration in `env.py`
   - Ensure MySQL service is running

3. **Frontend Dependency Installation Failure**
   ```bash
   cd static
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Python Dependency Installation Failure**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please submit issues and pull requests to help improve this project.

---

**Development Team**: Sway Team  
**Version**: 1.0.0  
**Last Updated**: 2025
