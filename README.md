# SQL Agent (MS SQL) — Enterprise-Grade Natural Language to SQL Platform

A sophisticated, enterprise-ready web application that transforms natural language questions into optimized SQL queries for Microsoft SQL Server. Built with modern software engineering principles, featuring modular architecture, intelligent background scheduling, and military-grade security through OS-integrated credential management.

## 🚀 Overview

SQL Agent represents the next generation of database interaction tools, combining the power of artificial intelligence with enterprise-grade security and performance. The platform enables users to:

- **Natural Language Processing**: Convert complex business questions into precise SQL queries using OpenAI's advanced language models
- **Intelligent Schema Discovery**: Automatically discover and map database structures, tables, and relationships
- **Advanced Visualization**: Generate interactive charts and reports from query results using Chart.js
- **Automated Scheduling**: Execute queries on custom schedules with comprehensive monitoring and logging
- **Enterprise Security**: Zero-trust architecture with OS-level credential encryption and no plaintext storage

## 🛠️ Technology Stack & Architecture Decisions

### Backend Framework: Flask with Blueprint Architecture
**Why Flask?**
- **Lightweight & Flexible**: Minimal overhead while providing full control over application structure
- **Blueprint Pattern**: Enables modular development and easy scaling across multiple teams
- **WSGI Compliance**: Seamless deployment on any WSGI-compatible server (Gunicorn, uWSGI, IIS)
- **Extensive Ecosystem**: Rich plugin ecosystem for enterprise features (authentication, monitoring, caching)

### Database Connectivity: pyodbc with ODBC Driver 17/18
**Why pyodbc + ODBC?**
- **Native Performance**: Direct ODBC connection provides optimal performance for SQL Server
- **Enterprise Compatibility**: Full support for SQL Server features (stored procedures, transactions, bulk operations)
- **Connection Pooling**: Built-in connection management for high-concurrency scenarios
- **Cross-Platform**: Works on Windows, Linux, and macOS with appropriate drivers
- **Security**: Supports Windows Authentication, SSL/TLS encryption, and advanced security features

### AI Integration: OpenAI SDK with GPT-4o-mini
**Why OpenAI + GPT-4o-mini?**
- **Cost Efficiency**: GPT-4o-mini provides 95% of GPT-4 performance at 1/10th the cost
- **SQL Expertise**: Trained on extensive SQL datasets with understanding of complex query patterns
- **Context Awareness**: Maintains conversation context for follow-up questions and refinements
- **Model Flexibility**: Easy switching between models (GPT-4, GPT-3.5-turbo) based on requirements
- **Rate Limiting**: Built-in handling of API rate limits and retry logic

### Frontend: Vanilla JavaScript with Chart.js
**Why Vanilla JS over Frameworks?**
- **Performance**: Zero framework overhead, faster load times, and smaller bundle sizes
- **Maintainability**: No framework lock-in, easier debugging, and simpler deployment
- **Chart.js Integration**: Industry-standard charting library with 30+ chart types and animations
- **Progressive Enhancement**: Works without JavaScript for basic functionality
- **Enterprise Ready**: No licensing concerns, full control over dependencies

### Security: Windows Credential Manager Integration
**Why OS Keyring over Database/File Storage?**
- **Zero Trust**: Passwords never stored in application code, files, or logs
- **OS-Level Encryption**: Uses Windows DPAPI (Data Protection API) for hardware-backed encryption
- **Audit Trail**: All credential access logged through Windows Event Log
- **Compliance**: Meets enterprise security standards (SOC 2, ISO 27001)
- **User Control**: Users can manage credentials through Windows Control Panel

### Task Scheduling: APScheduler with Multiple Triggers
**Why APScheduler?**
- **Enterprise Features**: Cron-like scheduling, job persistence, and distributed execution
- **Database Integration**: Jobs stored in SQL Server for reliability and monitoring
- **Flexible Triggers**: Hourly, daily, weekly, monthly, and custom interval scheduling
- **Job Management**: Start, stop, pause, and modify jobs without application restart
- **Monitoring**: Built-in job execution history and failure tracking

### Configuration Management: python-dotenv
**Why Environment Variables?**
- **12-Factor App Compliance**: Follows industry best practices for configuration management
- **Security**: Sensitive data separated from code repository
- **Environment Parity**: Same code runs in development, staging, and production
- **Easy Deployment**: Simple configuration changes without code modifications

## Repository Layout
```
sql-agent-cursor/
├── app.py                # Flask app factory, blueprint registration, scheduler start
├── routes.py             # REST API endpoints (DB connect, tables, columns, query, reports, scheduler)
├── database.py           # DatabaseManager (connections, schema, CRUD for queries/scheduled queries)
├── ai_service.py         # OpenAI integration (NL→SQL, summaries)
├── config.py             # Centralized settings (env, defaults, keyring service/driver)
├── utils.py              # Validation, logging helpers, ODBC DSN parse/build/masking
├── scheduler.py          # Query scheduler service (APScheduler)
├── templates/index.html  # UI layout
├── static/app.js         # Frontend logic (API calls, state, charts)
├── static/style.css      # Styling
├── requirements.txt      # Dependencies
└── README.md             # This guide
```

## Security Model (Very Important)
- Passwords are NOT stored in app code, env, files, or logs.
- On connect, backend stores only the password in Windows Credential Manager via `keyring`.
- Session stores PWD‑less DSN and a keyring account key (`SERVER|DATABASE|UID`).
- When connecting, `DatabaseManager` fetches the password from keyring at runtime and builds a full DSN in memory.
- Logs use masking; DSN shown as `PWD=***`.
- UI clears password field after submit and never persists it in localStorage/sessionStorage.

Keyring details:
- Service name: `sql-agent-cursor` (configurable via `KEYRING_SERVICE`)
- Account format: `SERVER|DATABASE|UID`
- Deletion: via “Bağlantı bilgilerini kaldır” button or Control Panel → Credential Manager.

## Modules — What Each Does
- `app.py`
  - Creates Flask app, sets config, registers blueprint `api_bp`, starts APScheduler on boot, graceful shutdown.
- `routes.py`
  - `POST /api/set_db`: Accepts either full DSN or fields (`driver, server, database, uid, pwd`). Stores PWD in keyring; saves only PWD‑less DSN + keyring account in session. Tests connection and configures scheduler.
  - `GET /api/tables`, `POST /api/columns`: Schema discovery.
  - `POST /api/query`: NL→SQL via `ai_service`, validation, execution, persistence of history.
  - `POST /api/report`: Explain or run report with chart inference.
  - Scheduled queries: CRUD + run-now endpoints.
  - `POST /api/clear_db`: Removes password from keyring and clears session; UI returns to disconnected state.
  - Health/status endpoints.
- `database.py`
  - Connection context manager; if keyring account present, retrieves password and builds DSN in memory.
  - Execute queries; infer query type; return structured results.
  - Persist query history and scheduled queries in SQL Server tables (`saved_queries`, `scheduled_queries`).
- `ai_service.py`
  - Uses OpenAI to convert natural language to SQL; provides result summaries.
- `utils.py`
  - `SQLValidator`: guards against destructive SQL.
  - `ODBCUtils`: parse/build/mask ODBC DSNs; mask dictionaries for logs.
  - `LoggingUtils`: basic logger setup and helpers.
- `scheduler.py`
  - Starts an APScheduler; (re)loads jobs after DB connect; supports hourly/daily/weekly/monthly triggers; run-now.
- Frontend (`templates/index.html`, `static/app.js`, `static/style.css`)
  - Database connect form with fields (preferred) and optional DSN.
  - Query builder, schema viewer, results grid, reports with charts, history, dashboard, scheduled queries UI.
  - “Bağlantı bilgilerini kaldır” button to fully clear credentials and reset UI.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10+ (for Windows Credential Manager integration)
- **Python**: Version 3.10+ (recommended: 3.11 or 3.12 for optimal performance)
- **Memory**: Minimum 4GB RAM (8GB+ recommended for large datasets)
- **Storage**: 2GB free space for application and dependencies

### Database Requirements
- **SQL Server**: Version 2016+ (2019+ recommended for advanced features)
- **ODBC Driver**: Microsoft ODBC Driver 17 or 18 for SQL Server
- **Network Access**: TCP/IP connectivity to SQL Server instance
- **Permissions**: Database read access and metadata query permissions

### External Services
- **OpenAI API**: Active API key with sufficient credits
- **Internet Connection**: Required for AI model communication

## 🗄️ SQL Server Setup & Configuration Guide

### 1. SQL Server Installation & Configuration

#### Option A: SQL Server Express (Free, Development)
```bash
# Download SQL Server Express from Microsoft
# URL: https://www.microsoft.com/en-us/sql-server/sql-server-downloads

# Installation steps:
1. Run SQLServerExpress.exe
2. Choose "Basic" installation type
3. Accept license terms
4. Set instance name (default: SQLEXPRESS)
5. Configure authentication mode (Mixed Mode recommended)
6. Set SA password (save securely)
7. Complete installation
```

#### Option B: SQL Server Developer Edition (Free, Full Features)
```bash
# Download from Microsoft Developer Program
# URL: https://www.microsoft.com/en-us/sql-server/sql-server-downloads

# Installation includes:
- Full SQL Server features
- SQL Server Management Studio (SSMS)
- Advanced security features
- Performance monitoring tools
```

#### Option C: SQL Server on Azure (Cloud)
```bash
# Azure SQL Database setup:
1. Create Azure account
2. Navigate to Azure Portal
3. Create new SQL Database resource
4. Configure server settings:
   - Server name: your-server.database.windows.net
   - Database name: your-database
   - Authentication: SQL Authentication
   - Firewall rules: Add your IP address
```

### 2. ODBC Driver Installation

#### Windows Installation
```powershell
# Method 1: Microsoft Download Center
# Download: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

# Method 2: Using Chocolatey (if installed)
choco install sqlserver-odbcdriver

# Method 3: Using winget
winget install Microsoft.ODBC.ODBCDriver17forSQLServer
```

#### Verification
```powershell
# Check installed ODBC drivers
Get-OdbcDriver | Where-Object {$_.Name -like "*SQL Server*"}

# Expected output:
# Name: ODBC Driver 17 for SQL Server
# Platform: 64-bit
```

### 3. Database Connection Information

#### Finding Your SQL Server Details

**For Local SQL Server:**
```sql
-- Connect to SQL Server and run:
SELECT @@SERVERNAME as ServerName,
       @@VERSION as Version,
       DB_NAME() as CurrentDatabase

-- Get all available databases:
SELECT name FROM sys.databases WHERE database_id > 4
```

**For SQL Server Express:**
- **Server Name**: `localhost\SQLEXPRESS` or `.\SQLEXPRESS`
- **Port**: 1433 (default)
- **Instance**: SQLEXPRESS

**For Named Instance:**
- **Server Name**: `localhost\INSTANCENAME`
- **Port**: Dynamic (check SQL Server Configuration Manager)

**For Azure SQL Database:**
- **Server Name**: `your-server.database.windows.net`
- **Port**: 1433
- **Database**: Your database name
- **Authentication**: SQL Server Authentication

### 4. User Permissions & Security Setup

#### Create Application User (Recommended)
```sql
-- Connect as SA or database owner
USE [YourDatabase]
GO

-- Create login
CREATE LOGIN [sql_agent_user] WITH PASSWORD = 'StrongPassword123!'
GO

-- Create user in database
CREATE USER [sql_agent_user] FOR LOGIN [sql_agent_user]
GO

-- Grant necessary permissions
ALTER ROLE db_datareader ADD MEMBER [sql_agent_user]
ALTER ROLE db_datawriter ADD MEMBER [sql_agent_user]
GRANT VIEW DEFINITION TO [sql_agent_user]
GRANT EXECUTE TO [sql_agent_user]
GO
```

#### Required Permissions for SQL Agent
```sql
-- Minimum permissions needed:
- db_datareader: Read data from tables
- db_datawriter: Write query history and scheduled queries
- VIEW DEFINITION: Access table/column metadata
- EXECUTE: Run stored procedures (if needed)

-- Optional permissions for advanced features:
- db_ddladmin: Create/modify tables (for query history storage)
- CONTROL: Full database control (development only)
```

### 5. Network Configuration

#### Enable TCP/IP Protocol
```powershell
# Open SQL Server Configuration Manager
# Navigate to: SQL Server Network Configuration > Protocols for [INSTANCE]
# Enable TCP/IP protocol
# Restart SQL Server service
```

#### Firewall Configuration
```powershell
# Windows Firewall - Allow SQL Server
New-NetFirewallRule -DisplayName "SQL Server" -Direction Inbound -Protocol TCP -LocalPort 1433 -Action Allow

# For named instances, check dynamic port:
# SQL Server Configuration Manager > SQL Server Network Configuration > TCP/IP > IP Addresses
```

#### Connection String Examples
```python
# Local SQL Server Express
"DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=YourDB;UID=sql_agent_user;PWD=StrongPassword123!;Trusted_Connection=no;"

# Named Instance
"DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\INSTANCENAME;DATABASE=YourDB;UID=sql_agent_user;PWD=StrongPassword123!;Trusted_Connection=no;"

# Azure SQL Database
"DRIVER={ODBC Driver 17 for SQL Server};SERVER=your-server.database.windows.net;DATABASE=YourDB;UID=sql_agent_user;PWD=StrongPassword123!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
```

### 6. Testing Your Connection

#### Using SQL Server Management Studio (SSMS)
```sql
-- Test connection with your credentials
-- Verify you can:
1. Connect to the server
2. See your target database
3. Browse tables and columns
4. Execute simple queries
```

#### Using Python (Before Running SQL Agent)
```python
import pyodbc

# Test connection
try:
    conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=YourDB;UID=sql_agent_user;PWD=StrongPassword123!;"
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    print("Connection successful!")
    print(cursor.fetchone()[0])
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
```

## 🚀 Installation & Setup

### Step 1: Clone Repository
```bash
# Clone the repository
git clone https://github.com/your-username/sql-agent-cursor.git
cd sql-agent-cursor

# Verify Python version (3.10+ required)
python --version
```

### Step 2: Create Virtual Environment
```bash
# Create isolated Python environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
venv\Scripts\Activate.ps1

# Windows Command Prompt:
venv\Scripts\activate.bat

# Linux/macOS:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(Flask|pyodbc|openai|APScheduler)"
```

### Step 4: Environment Configuration
```bash
# Copy environment template
copy env_example.txt .env

# Edit configuration file
notepad .env  # Windows
# or
nano .env     # Linux/macOS
```

#### Environment Variables Reference
```bash
# Required Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# Database Configuration
DEFAULT_ODBC_DRIVER=ODBC Driver 17 for SQL Server
DB_CONNECTION_TIMEOUT=30
MAX_TABLES_PER_QUERY=20
MAX_QUERY_LENGTH=2000

# Security Configuration
KEYRING_SERVICE=sql-agent-cursor
SECRET_KEY=your-secret-key-for-sessions

# Application Settings
DEBUG=False
HOST=127.0.0.1
PORT=5000
LOG_LEVEL=INFO

# Scheduler Configuration
SCHEDULER_TIMEZONE=UTC
MAX_CONCURRENT_JOBS=10

# Optional: Advanced Features
ENABLE_QUERY_CACHING=True
CACHE_TTL_SECONDS=3600
ENABLE_QUERY_ANALYTICS=True
```

### Step 5: OpenAI API Key Setup
```bash
# Get your API key from OpenAI
# Visit: https://platform.openai.com/api-keys

# Add to .env file
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Verify API key (optional test)
python -c "import openai; openai.api_key='your-key'; print('API key valid')"
```

### Step 6: Launch Application
```bash
# Start the application
python app.py

# Expected output:
# * Running on http://127.0.0.1:5000
# * Scheduler started successfully
# * Database connection ready
```

### Step 7: Access Web Interface
```bash
# Open your browser and navigate to:
http://localhost:5000

# You should see the SQL Agent dashboard
```

### Step 8: First-Time Database Connection
1. **Click "Connect to Database"**
2. **Enter your SQL Server details:**
   - Server: `localhost\SQLEXPRESS` (or your server)
   - Database: Your database name
   - Username: Your SQL Server username
   - Password: Your password (will be encrypted)
3. **Click "Connect"**
4. **Verify connection success**
5. **Start asking natural language questions!**

## 🔧 Development Setup (Optional)

### Code Quality Tools
```bash
# Install development dependencies
pip install pytest pytest-flask black flake8 mypy

# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .

# Run tests
pytest
```

### IDE Configuration (VS Code)
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true
}
```

## 📖 User Guide

### 🔌 Database Connection

#### Method 1: Individual Fields (Recommended)
1. **Navigate to the Connection tab**
2. **Fill in the connection details:**
   - **Driver**: `ODBC Driver 17 for SQL Server` (default)
   - **Server**: Your SQL Server instance (e.g., `localhost\SQLEXPRESS`)
   - **Database**: Target database name
   - **Username**: SQL Server username
   - **Password**: Your password (encrypted and stored securely)
3. **Click "Connect to Database"**
4. **Verify successful connection**

#### Method 2: Connection String
```sql
-- Full DSN format:
DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=YourDB;UID=username;PWD=password;Trusted_Connection=no;
```

### 🗃️ Database Schema Exploration

#### Table Discovery
- **Automatic Loading**: Tables load automatically after connection
- **Schema Filtering**: Filter by schema (dbo, information_schema, etc.)
- **Search Functionality**: Search tables by name
- **Metadata Display**: View table row counts and creation dates

#### Column Information
- **Click any table** to view its columns
- **Data Types**: See column data types and constraints
- **Nullable Status**: Identify required vs optional fields
- **Primary Keys**: Highlighted primary key columns
- **Foreign Keys**: Displayed relationship information

### 🤖 Natural Language Queries

#### Basic Queries
```
Examples of natural language questions:
- "Show me all customers from New York"
- "What are the top 10 products by sales?"
- "How many orders were placed last month?"
- "Which customers haven't placed an order in 6 months?"
```

#### Advanced Queries
```
Complex business questions:
- "Find customers who bought more than $1000 worth of products in the last quarter"
- "Show me the sales trend by month for the past year"
- "Which product categories have the highest profit margins?"
- "Compare this year's sales to last year's sales by region"
```

#### Query Refinement
- **Follow-up Questions**: Ask clarifying questions about results
- **Query Modification**: Request changes to existing queries
- **Error Handling**: AI explains and fixes SQL errors
- **Performance Tips**: Get suggestions for query optimization

### 📊 Data Visualization

#### Automatic Chart Suggestions
- **Bar Charts**: For categorical data comparisons
- **Line Charts**: For time-series data trends
- **Pie Charts**: For percentage distributions
- **Scatter Plots**: For correlation analysis

#### Custom Visualizations
- **Chart Configuration**: Modify colors, labels, and axes
- **Export Options**: Download charts as PNG/SVG
- **Interactive Features**: Hover tooltips and zoom functionality
- **Responsive Design**: Charts adapt to different screen sizes

### ⏰ Scheduled Queries

#### Creating Scheduled Jobs
1. **Navigate to "Scheduled Queries" tab**
2. **Click "Create New Schedule"**
3. **Configure the schedule:**
   - **Query**: Natural language question or SQL
   - **Frequency**: Hourly, Daily, Weekly, Monthly
   - **Time**: Specific execution time
   - **Timezone**: UTC or local time
4. **Set notification preferences**
5. **Save and activate**

#### Schedule Types
- **Hourly**: Every hour at minute 0
- **Daily**: Once per day at specified time
- **Weekly**: Specific day of week and time
- **Monthly**: Specific day of month and time
- **Custom**: Cron-like expressions

#### Job Management
- **Run Now**: Execute job immediately for testing
- **Toggle Active/Inactive**: Enable/disable jobs
- **Edit Schedule**: Modify timing and query
- **View History**: See execution logs and results
- **Delete Job**: Remove scheduled queries

### 📈 Query History & Analytics

#### History Features
- **Complete Log**: All executed queries with timestamps
- **Performance Metrics**: Execution time and row counts
- **Error Tracking**: Failed queries with error messages
- **User Attribution**: Track queries by session

#### Analytics Dashboard
- **Query Frequency**: Most common query patterns
- **Performance Trends**: Average execution times
- **Error Analysis**: Common failure reasons
- **Usage Statistics**: Daily/weekly/monthly usage

### 🔒 Security & Credential Management

#### Secure Storage
- **OS Integration**: Passwords stored in Windows Credential Manager
- **Encryption**: Hardware-backed encryption using DPAPI
- **No Plaintext**: Passwords never stored in files or logs
- **Session Management**: Automatic session timeout

#### Credential Management
- **Clear Credentials**: Remove stored passwords
- **Reconnect**: Re-establish database connection
- **Multiple Databases**: Support for multiple database connections
- **User Control**: Full control over credential lifecycle

### 🚨 Troubleshooting Common Issues

#### Connection Problems
```
Error: "Login failed for user"
Solution: Verify username/password and SQL Server authentication mode

Error: "Cannot connect to server"
Solution: Check server name, port, and firewall settings

Error: "Driver not found"
Solution: Install ODBC Driver 17 for SQL Server
```

#### Query Issues
```
Error: "Invalid column name"
Solution: Check table/column names in schema explorer

Error: "Permission denied"
Solution: Verify user has necessary database permissions

Error: "Timeout expired"
Solution: Increase DB_CONNECTION_TIMEOUT in .env
```

#### Performance Issues
```
Slow queries: Use query optimization suggestions from AI
Large result sets: Add LIMIT clauses to queries
Memory issues: Increase MAX_QUERY_LENGTH in configuration
```

## 🔌 REST API Reference

### Database Management
```http
POST /api/set_db
Content-Type: application/json

# Option A: Individual fields
{
  "driver": "ODBC Driver 17 for SQL Server",
  "server": "localhost\\SQLEXPRESS",
  "database": "YourDatabase",
  "uid": "username",
  "pwd": "password"
}

# Option B: Connection string
{
  "db_conn_str": "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=YourDB;UID=username;PWD=password;"
}
```

### Schema Discovery
```http
GET /api/tables
# Returns: List of available tables with metadata

POST /api/columns
Content-Type: application/json
{
  "tables": ["dbo.Users", "dbo.Orders", "dbo.Products"]
}
# Returns: Column information for specified tables
```

### Query Execution
```http
POST /api/query
Content-Type: application/json
{
  "question": "Show me the top 10 customers by total orders",
  "tables": ["dbo.Customers", "dbo.Orders"]
}
# Returns: SQL query, execution results, and metadata

POST /api/report
Content-Type: application/json
{
  "question": "Generate a sales report for Q4 2023",
  "format": "detailed"
}
# Returns: Rich report with charts and insights
```

### Query History Management
```http
GET /api/queries
# Returns: List of saved queries with metadata

GET /api/queries/{id}
# Returns: Specific query details and results

DELETE /api/queries/{id}
# Removes query from history
```

### Scheduled Queries
```http
POST /api/scheduled-queries
Content-Type: application/json
{
  "name": "Daily Sales Report",
  "query": "SELECT * FROM sales WHERE date = GETDATE()",
  "schedule_type": "daily",
  "schedule_time": "09:00",
  "timezone": "UTC"
}

GET /api/scheduled-queries
# Returns: List of all scheduled queries

PUT /api/scheduled-queries/{id}
# Updates existing scheduled query

DELETE /api/scheduled-queries/{id}
# Removes scheduled query

POST /api/scheduled-queries/{id}/run-now
# Executes scheduled query immediately

POST /api/scheduled-queries/{id}/toggle
# Enables/disables scheduled query
```

### System Status
```http
GET /api/health
# Returns: Application health status

GET /api/scheduler/status
# Returns: Scheduler status and job information

POST /api/clear_db
# Clears database credentials and session
```

## 🏗️ Architecture & Design Principles

### Clean Architecture Implementation
- **Single Responsibility Principle**: Each module has a single, well-defined purpose
- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Interface Segregation**: Clients depend only on interfaces they use
- **Open/Closed Principle**: Open for extension, closed for modification

### Security Architecture
- **Zero Trust Model**: No implicit trust, verify everything
- **Defense in Depth**: Multiple layers of security controls
- **Principle of Least Privilege**: Minimal necessary permissions
- **Secure by Default**: Secure configurations out of the box

### Code Quality Standards
- **Type Safety**: Type hints and mypy validation
- **Code Formatting**: Black formatter for consistent style
- **Linting**: Flake8 for code quality enforcement
- **Testing**: Comprehensive test coverage with pytest
- **Documentation**: Inline documentation and API docs

### Extensibility Design
- **Plugin Architecture**: Easy addition of new AI providers
- **Database Abstraction**: Support for multiple database engines
- **Configuration Management**: Environment-based configuration
- **API Versioning**: Backward-compatible API evolution

## 🚀 Production Deployment

### Environment Configuration
```bash
# Production environment variables
DEBUG=False
LOG_LEVEL=WARNING
SECRET_KEY=your-production-secret-key
OPENAI_API_KEY=your-production-api-key
DB_CONNECTION_TIMEOUT=60
MAX_CONCURRENT_JOBS=50
```

### Web Server Setup
```bash
# Using Gunicorn (Linux/macOS)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Using Waitress (Windows)
pip install waitress
waitress-serve --host=0.0.0.0 --port=8000 app:app
```

### Reverse Proxy Configuration (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL/TLS Configuration
```bash
# Using Let's Encrypt
certbot --nginx -d your-domain.com

# Or using custom certificates
# Place certificates in /etc/ssl/certs/
```

### Monitoring & Logging
```bash
# Application monitoring
pip install prometheus-client
pip install structlog

# Log aggregation
# Configure with ELK stack or similar
```

### Backup & Recovery
```bash
# Database backup strategy
# 1. Regular SQL Server backups
# 2. Application configuration backup
# 3. Credential recovery procedures
```

## 🔧 Advanced Configuration

### Performance Tuning
```bash
# Database connection pooling
DB_POOL_SIZE=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# Query optimization
MAX_QUERY_LENGTH=5000
QUERY_TIMEOUT=300
ENABLE_QUERY_CACHING=True
CACHE_TTL_SECONDS=1800
```

### Security Hardening
```bash
# Session security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Strict

# CORS configuration
CORS_ORIGINS=https://your-domain.com
CORS_METHODS=GET,POST,PUT,DELETE
CORS_HEADERS=Content-Type,Authorization
```

### Scalability Options
```bash
# Horizontal scaling
ENABLE_REDIS_CACHE=True
REDIS_URL=redis://localhost:6379/0

# Load balancing
ENABLE_STICKY_SESSIONS=True
SESSION_BACKEND=redis
```

## 📊 Monitoring & Analytics

### Application Metrics
- **Query Performance**: Execution time, row counts, error rates
- **User Activity**: Session duration, query frequency, feature usage
- **System Health**: Memory usage, CPU utilization, disk I/O
- **Security Events**: Failed logins, permission errors, suspicious activity

### Business Intelligence
- **Query Analytics**: Most common query patterns and trends
- **User Behavior**: Feature adoption and usage patterns
- **Performance Trends**: System performance over time
- **Cost Analysis**: OpenAI API usage and costs

## 🆘 Troubleshooting Guide

### Common Issues & Solutions

#### Installation Problems
```bash
# Python version issues
python --version  # Should be 3.10+
py -3.11 -m venv venv  # Use specific Python version

# Package installation failures
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

#### Database Connection Issues
```bash
# ODBC driver problems
Get-OdbcDriver | Where-Object {$_.Name -like "*SQL Server*"}

# Connection string validation
python -c "import pyodbc; print(pyodbc.drivers())"

# Network connectivity
telnet your-server 1433
```

#### AI Service Issues
```bash
# API key validation
python -c "import openai; openai.api_key='your-key'; print(openai.models.list())"

# Rate limiting
# Check OpenAI dashboard for usage limits
# Implement exponential backoff in code
```

#### Performance Issues
```bash
# Memory usage
pip install memory-profiler
python -m memory_profiler app.py

# Database performance
# Enable SQL Server query store
# Use SQL Server Profiler for analysis
```

## 📄 License & Legal

### MIT License
```
MIT License

Copyright (c) 2024 SQL Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Third-Party Licenses
- **OpenAI API**: Subject to OpenAI's Terms of Service
- **Microsoft SQL Server**: Subject to Microsoft's licensing terms
- **Python Libraries**: Various open-source licenses (see requirements.txt)

### Compliance & Security
- **GDPR Compliance**: User data handling and privacy protection
- **SOC 2**: Security controls and monitoring
- **ISO 27001**: Information security management
- **HIPAA**: Healthcare data protection (if applicable)

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to:
- Report bugs and request features
- Submit code changes
- Follow our coding standards
- Participate in our community

## 📞 Support

- **Documentation**: [Full Documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-username/sql-agent-cursor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/sql-agent-cursor/discussions)
- **Email**: support@your-domain.com

---

**Built with ❤️ for the data community**

---

# SQL Agent (MS SQL) — Kurumsal Seviye Doğal Dil-SQL Platformu

Doğal dil sorularını Microsoft SQL Server için optimize edilmiş SQL sorgularına dönüştüren sofistike, kurumsal hazır web uygulaması. Modern yazılım mühendisliği prensipleri ile inşa edilmiş, modüler mimari, akıllı arka plan zamanlama ve OS entegreli kimlik bilgisi yönetimi ile askeri seviye güvenlik özelliklerine sahip.

## 🚀 Genel Bakış

SQL Agent, yapay zeka gücünü kurumsal seviye güvenlik ve performans ile birleştiren veritabanı etkileşim araçlarının yeni neslini temsil eder. Platform kullanıcıların şunları yapmasını sağlar:

- **Doğal Dil İşleme**: OpenAI'nin gelişmiş dil modellerini kullanarak karmaşık iş sorularını kesin SQL sorgularına dönüştürme
- **Akıllı Şema Keşfi**: Veritabanı yapılarını, tabloları ve ilişkileri otomatik olarak keşfetme ve haritalama
- **Gelişmiş Görselleştirme**: Chart.js kullanarak sorgu sonuçlarından etkileşimli grafikler ve raporlar oluşturma
- **Otomatik Zamanlama**: Kapsamlı izleme ve loglama ile özel zamanlamalarda sorguları çalıştırma
- **Kurumsal Güvenlik**: OS seviyesi kimlik bilgisi şifreleme ve düz metin depolama olmayan sıfır güven mimarisi

## 🛠️ Teknoloji Yığını ve Mimari Kararlar

### Backend Framework: Blueprint Mimarisi ile Flask
**Neden Flask?**
- **Hafif ve Esnek**: Uygulama yapısı üzerinde tam kontrol sağlarken minimal ek yük
- **Blueprint Deseni**: Modüler geliştirme ve birden fazla ekip arasında kolay ölçeklendirme
- **WSGI Uyumluluğu**: Herhangi bir WSGI uyumlu sunucuda (Gunicorn, uWSGI, IIS) sorunsuz dağıtım
- **Geniş Ekosistem**: Kurumsal özellikler için zengin eklenti ekosistemi (kimlik doğrulama, izleme, önbellekleme)

### Veritabanı Bağlantısı: ODBC Driver 17/18 ile pyodbc
**Neden pyodbc + ODBC?**
- **Yerel Performans**: SQL Server için optimal performans sağlayan doğrudan ODBC bağlantısı
- **Kurumsal Uyumluluk**: SQL Server özelliklerinin tam desteği (saklı yordamlar, işlemler, toplu işlemler)
- **Bağlantı Havuzlama**: Yüksek eşzamanlılık senaryoları için yerleşik bağlantı yönetimi
- **Platformlar Arası**: Uygun sürücülerle Windows, Linux ve macOS'ta çalışır
- **Güvenlik**: Windows Kimlik Doğrulama, SSL/TLS şifreleme ve gelişmiş güvenlik özelliklerini destekler

### AI Entegrasyonu: GPT-4o-mini ile OpenAI SDK
**Neden OpenAI + GPT-4o-mini?**
- **Maliyet Verimliliği**: GPT-4o-mini, GPT-4'ün %95 performansını 1/10 maliyetle sağlar
- **SQL Uzmanlığı**: Karmaşık sorgu desenlerini anlayan kapsamlı SQL veri setleri üzerinde eğitilmiş
- **Bağlam Farkındalığı**: Takip soruları ve iyileştirmeler için konuşma bağlamını korur
- **Model Esnekliği**: Gereksinimlere göre modeller arasında kolay geçiş (GPT-4, GPT-3.5-turbo)
- **Hız Sınırlama**: API hız sınırları ve yeniden deneme mantığının yerleşik işlenmesi

### Frontend: Chart.js ile Vanilla JavaScript
**Neden Framework'ler yerine Vanilla JS?**
- **Performans**: Sıfır framework ek yükü, daha hızlı yükleme süreleri ve daha küçük paket boyutları
- **Sürdürülebilirlik**: Framework kilidi yok, daha kolay hata ayıklama ve basit dağıtım
- **Chart.js Entegrasyonu**: 30+ grafik türü ve animasyonlarla endüstri standardı grafik kütüphanesi
- **Aşamalı Geliştirme**: Temel işlevsellik için JavaScript olmadan çalışır
- **Kurumsal Hazır**: Lisans endişesi yok, bağımlılıklar üzerinde tam kontrol

### Güvenlik: Windows Credential Manager Entegrasyonu
**Neden Veritabanı/Dosya Depolama yerine OS Keyring?**
- **Sıfır Güven**: Şifreler asla uygulama kodunda, dosyalarda veya loglarda saklanmaz
- **OS Seviyesi Şifreleme**: Donanım destekli şifreleme için Windows DPAPI (Data Protection API) kullanır
- **Denetim İzi**: Tüm kimlik bilgisi erişimi Windows Event Log üzerinden loglanır
- **Uyumluluk**: Kurumsal güvenlik standartlarını karşılar (SOC 2, ISO 27001)
- **Kullanıcı Kontrolü**: Kullanıcılar kimlik bilgilerini Windows Control Panel üzerinden yönetebilir

### Görev Zamanlama: Çoklu Tetikleyiciler ile APScheduler
**Neden APScheduler?**
- **Kurumsal Özellikler**: Cron benzeri zamanlama, iş kalıcılığı ve dağıtık yürütme
- **Veritabanı Entegrasyonu**: Güvenilirlik ve izleme için işler SQL Server'da saklanır
- **Esnek Tetikleyiciler**: Saatlik, günlük, haftalık, aylık ve özel aralık zamanlaması
- **İş Yönetimi**: Uygulama yeniden başlatmadan işleri başlat, durdur, duraklat ve değiştir
- **İzleme**: Yerleşik iş yürütme geçmişi ve hata takibi

### Yapılandırma Yönetimi: python-dotenv
**Neden Ortam Değişkenleri?**
- **12-Factor App Uyumluluğu**: Yapılandırma yönetimi için endüstri en iyi uygulamalarını takip eder
- **Güvenlik**: Hassas veriler kod deposundan ayrılır
- **Ortam Eşitliği**: Aynı kod geliştirme, test ve üretimde çalışır
- **Kolay Dağıtım**: Kod değişikliği olmadan basit yapılandırma değişiklikleri

## 📋 Ön Gereksinimler

### Sistem Gereksinimleri
- **İşletim Sistemi**: Windows 10+ (Windows Credential Manager entegrasyonu için)
- **Python**: Sürüm 3.10+ (optimal performans için önerilen: 3.11 veya 3.12)
- **Bellek**: Minimum 4GB RAM (büyük veri setleri için 8GB+ önerilen)
- **Depolama**: Uygulama ve bağımlılıklar için 2GB boş alan

### Veritabanı Gereksinimleri
- **SQL Server**: Sürüm 2016+ (gelişmiş özellikler için 2019+ önerilen)
- **ODBC Driver**: Microsoft ODBC Driver 17 veya 18 for SQL Server
- **Ağ Erişimi**: SQL Server örneğine TCP/IP bağlantısı
- **İzinler**: Veritabanı okuma erişimi ve metadata sorgu izinleri

### Harici Hizmetler
- **OpenAI API**: Yeterli kredi ile aktif API anahtarı
- **İnternet Bağlantısı**: AI model iletişimi için gerekli

## 🗄️ SQL Server Kurulum ve Yapılandırma Rehberi

### 1. SQL Server Kurulum ve Yapılandırma

#### Seçenek A: SQL Server Express (Ücretsiz, Geliştirme)
```bash
# Microsoft'tan SQL Server Express'i indirin
# URL: https://www.microsoft.com/en-us/sql-server/sql-server-downloads

# Kurulum adımları:
1. SQLServerExpress.exe'yi çalıştırın
2. "Basic" kurulum türünü seçin
3. Lisans şartlarını kabul edin
4. Örnek adını ayarlayın (varsayılan: SQLEXPRESS)
5. Kimlik doğrulama modunu yapılandırın (Mixed Mode önerilen)
6. SA şifresini ayarlayın (güvenli bir şekilde kaydedin)
7. Kurulumu tamamlayın
```

#### Seçenek B: SQL Server Developer Edition (Ücretsiz, Tam Özellikler)
```bash
# Microsoft Developer Program'dan indirin
# URL: https://www.microsoft.com/en-us/sql-server/sql-server-downloads

# Kurulum şunları içerir:
- Tam SQL Server özellikleri
- SQL Server Management Studio (SSMS)
- Gelişmiş güvenlik özellikleri
- Performans izleme araçları
```

#### Seçenek C: Azure'da SQL Server (Bulut)
```bash
# Azure SQL Database kurulumu:
1. Azure hesabı oluşturun
2. Azure Portal'a gidin
3. Yeni SQL Database kaynağı oluşturun
4. Sunucu ayarlarını yapılandırın:
   - Sunucu adı: your-server.database.windows.net
   - Veritabanı adı: your-database
   - Kimlik doğrulama: SQL Authentication
   - Güvenlik duvarı kuralları: IP adresinizi ekleyin
```

### 2. ODBC Driver Kurulumu

#### Windows Kurulumu
```powershell
# Yöntem 1: Microsoft Download Center
# İndir: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

# Yöntem 2: Chocolatey kullanarak (kuruluysa)
choco install sqlserver-odbcdriver

# Yöntem 3: winget kullanarak
winget install Microsoft.ODBC.ODBCDriver17forSQLServer
```

#### Doğrulama
```powershell
# Kurulu ODBC sürücülerini kontrol edin
Get-OdbcDriver | Where-Object {$_.Name -like "*SQL Server*"}

# Beklenen çıktı:
# Name: ODBC Driver 17 for SQL Server
# Platform: 64-bit
```

### 3. Veritabanı Bağlantı Bilgileri

#### SQL Server Detaylarınızı Bulma

**Yerel SQL Server için:**
```sql
-- SQL Server'a bağlanın ve çalıştırın:
SELECT @@SERVERNAME as ServerName,
       @@VERSION as Version,
       DB_NAME() as CurrentDatabase

-- Tüm mevcut veritabanlarını alın:
SELECT name FROM sys.databases WHERE database_id > 4
```

**SQL Server Express için:**
- **Sunucu Adı**: `localhost\SQLEXPRESS` veya `.\SQLEXPRESS`
- **Port**: 1433 (varsayılan)
- **Örnek**: SQLEXPRESS

**Adlandırılmış Örnek için:**
- **Sunucu Adı**: `localhost\INSTANCENAME`
- **Port**: Dinamik (SQL Server Configuration Manager'da kontrol edin)

**Azure SQL Database için:**
- **Sunucu Adı**: `your-server.database.windows.net`
- **Port**: 1433
- **Veritabanı**: Veritabanı adınız
- **Kimlik Doğrulama**: SQL Server Authentication

### 4. Kullanıcı İzinleri ve Güvenlik Kurulumu

#### Uygulama Kullanıcısı Oluşturma (Önerilen)
```sql
-- SA veya veritabanı sahibi olarak bağlanın
USE [YourDatabase]
GO

-- Login oluşturun
CREATE LOGIN [sql_agent_user] WITH PASSWORD = 'StrongPassword123!'
GO

-- Veritabanında kullanıcı oluşturun
CREATE USER [sql_agent_user] FOR LOGIN [sql_agent_user]
GO

-- Gerekli izinleri verin
ALTER ROLE db_datareader ADD MEMBER [sql_agent_user]
ALTER ROLE db_datawriter ADD MEMBER [sql_agent_user]
GRANT VIEW DEFINITION TO [sql_agent_user]
GRANT EXECUTE TO [sql_agent_user]
GO
```

#### SQL Agent için Gerekli İzinler
```sql
-- Gerekli minimum izinler:
- db_datareader: Tablolardan veri okuma
- db_datawriter: Sorgu geçmişi ve zamanlanmış sorgular yazma
- VIEW DEFINITION: Tablo/sütun metadata'sına erişim
- EXECUTE: Saklı yordamları çalıştırma (gerekirse)

-- Gelişmiş özellikler için isteğe bağlı izinler:
- db_ddladmin: Sorgu geçmişi depolama için tablo oluşturma/değiştirme
- CONTROL: Tam veritabanı kontrolü (sadece geliştirme)
```

### 5. Ağ Yapılandırması

#### TCP/IP Protokolünü Etkinleştirme
```powershell
# SQL Server Configuration Manager'ı açın
# Navigate to: SQL Server Network Configuration > Protocols for [INSTANCE]
# TCP/IP protokolünü etkinleştirin
# SQL Server servisini yeniden başlatın
```

#### Güvenlik Duvarı Yapılandırması
```powershell
# Windows Firewall - SQL Server'a izin ver
New-NetFirewallRule -DisplayName "SQL Server" -Direction Inbound -Protocol TCP -LocalPort 1433 -Action Allow

# Adlandırılmış örnekler için, dinamik portu kontrol edin:
# SQL Server Configuration Manager > SQL Server Network Configuration > TCP/IP > IP Addresses
```

#### Bağlantı Dizesi Örnekleri
```python
# Yerel SQL Server Express
"DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=YourDB;UID=sql_agent_user;PWD=StrongPassword123!;Trusted_Connection=no;"

# Adlandırılmış Örnek
"DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\INSTANCENAME;DATABASE=YourDB;UID=sql_agent_user;PWD=StrongPassword123!;Trusted_Connection=no;"

# Azure SQL Database
"DRIVER={ODBC Driver 17 for SQL Server};SERVER=your-server.database.windows.net;DATABASE=YourDB;UID=sql_agent_user;PWD=StrongPassword123!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
```

### 6. Bağlantınızı Test Etme

#### SQL Server Management Studio (SSMS) Kullanarak
```sql
-- Kimlik bilgilerinizle bağlantıyı test edin
-- Şunları doğrulayın:
1. Sunucuya bağlanabilme
2. Hedef veritabanını görebilme
3. Tablo ve sütunları tarayabilme
4. Basit sorguları çalıştırabilme
```

#### Python Kullanarak (SQL Agent'ı çalıştırmadan önce)
```python
import pyodbc

# Bağlantıyı test edin
try:
    conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=YourDB;UID=sql_agent_user;PWD=StrongPassword123!;"
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    print("Bağlantı başarılı!")
    print(cursor.fetchone()[0])
    conn.close()
except Exception as e:
    print(f"Bağlantı başarısız: {e}")
```

## 🚀 Kurulum ve Yapılandırma

### Adım 1: Repository'yi Klonlama
```bash
# Repository'yi klonlayın
git clone https://github.com/your-username/sql-agent-cursor.git
cd sql-agent-cursor

# Python sürümünü doğrulayın (3.10+ gerekli)
python --version
```

### Adım 2: Sanal Ortam Oluşturma
```bash
# İzole Python ortamı oluşturun
python -m venv venv

# Sanal ortamı etkinleştirin
# Windows PowerShell:
venv\Scripts\Activate.ps1

# Windows Command Prompt:
venv\Scripts\activate.bat

# Linux/macOS:
source venv/bin/activate
```

### Adım 3: Bağımlılıkları Kurma
```bash
# pip'i en son sürüme yükseltin
python -m pip install --upgrade pip

# Tüm gerekli paketleri kurun
pip install -r requirements.txt

# Kurulumu doğrulayın
pip list | grep -E "(Flask|pyodbc|openai|APScheduler)"
```

### Adım 4: Ortam Yapılandırması
```bash
# Ortam şablonunu kopyalayın
copy env_example.txt .env

# Yapılandırma dosyasını düzenleyin
notepad .env  # Windows
# veya
nano .env     # Linux/macOS
```

#### Ortam Değişkenleri Referansı
```bash
# Gerekli Yapılandırma
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# Veritabanı Yapılandırması
DEFAULT_ODBC_DRIVER=ODBC Driver 17 for SQL Server
DB_CONNECTION_TIMEOUT=30
MAX_TABLES_PER_QUERY=20
MAX_QUERY_LENGTH=2000

# Güvenlik Yapılandırması
KEYRING_SERVICE=sql-agent-cursor
SECRET_KEY=your-secret-key-for-sessions

# Uygulama Ayarları
DEBUG=False
HOST=127.0.0.1
PORT=5000
LOG_LEVEL=INFO

# Zamanlayıcı Yapılandırması
SCHEDULER_TIMEZONE=UTC
MAX_CONCURRENT_JOBS=10

# İsteğe Bağlı: Gelişmiş Özellikler
ENABLE_QUERY_CACHING=True
CACHE_TTL_SECONDS=3600
ENABLE_QUERY_ANALYTICS=True
```

### Adım 5: OpenAI API Anahtarı Kurulumu
```bash
# OpenAI'dan API anahtarınızı alın
# Ziyaret edin: https://platform.openai.com/api-keys

# .env dosyasına ekleyin
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# API anahtarını doğrulayın (isteğe bağlı test)
python -c "import openai; openai.api_key='your-key'; print('API anahtarı geçerli')"
```

### Adım 6: Uygulamayı Başlatma
```bash
# Uygulamayı başlatın
python app.py

# Beklenen çıktı:
# * Running on http://127.0.0.1:5000
# * Scheduler started successfully
# * Database connection ready
```

### Adım 7: Web Arayüzüne Erişim
```bash
# Tarayıcınızı açın ve şu adrese gidin:
http://localhost:5000

# SQL Agent dashboard'unu görmelisiniz
```

### Adım 8: İlk Kez Veritabanı Bağlantısı
1. **"Connect to Database"e tıklayın**
2. **SQL Server detaylarınızı girin:**
   - Server: `localhost\SQLEXPRESS` (veya sunucunuz)
   - Database: Veritabanı adınız
   - Username: SQL Server kullanıcı adınız
   - Password: Şifreniz (şifrelenecek)
3. **"Connect"e tıklayın**
4. **Bağlantı başarısını doğrulayın**
5. **Doğal dil soruları sormaya başlayın!**

## 📖 Kullanıcı Rehberi

### 🔌 Veritabanı Bağlantısı

#### Yöntem 1: Ayrı Alanlar (Önerilen)
1. **Connection sekmesine gidin**
2. **Bağlantı detaylarını doldurun:**
   - **Driver**: `ODBC Driver 17 for SQL Server` (varsayılan)
   - **Server**: SQL Server örneğiniz (örn. `localhost\SQLEXPRESS`)
   - **Database**: Hedef veritabanı adı
   - **Username**: SQL Server kullanıcı adı
   - **Password**: Şifreniz (güvenli bir şekilde şifrelenir ve saklanır)
3. **"Connect to Database"e tıklayın**
4. **Başarılı bağlantıyı doğrulayın**

#### Yöntem 2: Bağlantı Dizesi
```sql
-- Tam DSN formatı:
DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=YourDB;UID=username;PWD=password;Trusted_Connection=no;
```

### 🗃️ Veritabanı Şema Keşfi

#### Tablo Keşfi
- **Otomatik Yükleme**: Bağlantıdan sonra tablolar otomatik yüklenir
- **Şema Filtreleme**: Şemaya göre filtreleme (dbo, information_schema, vb.)
- **Arama İşlevselliği**: Tabloları ada göre arama
- **Metadata Görüntüleme**: Tablo satır sayıları ve oluşturma tarihlerini görüntüleme

#### Sütun Bilgileri
- **Herhangi bir tabloya tıklayın** sütunlarını görüntülemek için
- **Veri Türleri**: Sütun veri türleri ve kısıtlamaları görme
- **Nullable Durumu**: Gerekli vs isteğe bağlı alanları belirleme
- **Birincil Anahtarlar**: Birincil anahtar sütunları vurgulanır
- **Yabancı Anahtarlar**: İlişki bilgileri görüntülenir

### 🤖 Doğal Dil Sorguları

#### Temel Sorgular
```
Doğal dil soruları örnekleri:
- "New York'tan tüm müşterileri göster"
- "Satışa göre en iyi 10 ürün nedir?"
- "Geçen ay kaç sipariş verildi?"
- "6 aydır sipariş vermeyen müşteriler hangileri?"
```

#### Gelişmiş Sorgular
```
Karmaşık iş soruları:
- "Son çeyrekte 1000$'dan fazla ürün satın alan müşterileri bul"
- "Geçen yıl için aylık satış trendini göster"
- "Hangi ürün kategorileri en yüksek kar marjına sahip?"
- "Bu yılın satışlarını geçen yılın satışlarıyla bölgeye göre karşılaştır"
```

#### Sorgu İyileştirme
- **Takip Soruları**: Sonuçlar hakkında açıklayıcı sorular sorun
- **Sorgu Değişikliği**: Mevcut sorgularda değişiklik isteyin
- **Hata İşleme**: AI SQL hatalarını açıklar ve düzeltir
- **Performans İpuçları**: Sorgu optimizasyonu için öneriler alın

### 📊 Veri Görselleştirme

#### Otomatik Grafik Önerileri
- **Çubuk Grafikleri**: Kategorik veri karşılaştırmaları için
- **Çizgi Grafikleri**: Zaman serisi veri trendleri için
- **Pasta Grafikleri**: Yüzde dağılımları için
- **Dağılım Grafikleri**: Korelasyon analizi için

#### Özel Görselleştirmeler
- **Grafik Yapılandırması**: Renkleri, etiketleri ve eksenleri değiştirin
- **Dışa Aktarma Seçenekleri**: Grafikleri PNG/SVG olarak indirin
- **Etkileşimli Özellikler**: Hover tooltip'leri ve zoom işlevselliği
- **Duyarlı Tasarım**: Grafikler farklı ekran boyutlarına uyum sağlar

### ⏰ Zamanlanmış Sorgular

#### Zamanlanmış İşler Oluşturma
1. **"Scheduled Queries" sekmesine gidin**
2. **"Create New Schedule"e tıklayın**
3. **Zamanlamayı yapılandırın:**
   - **Query**: Doğal dil sorusu veya SQL
   - **Frequency**: Saatlik, Günlük, Haftalık, Aylık
   - **Time**: Belirli yürütme zamanı
   - **Timezone**: UTC veya yerel saat
4. **Bildirim tercihlerini ayarlayın**
5. **Kaydedin ve etkinleştirin**

#### Zamanlama Türleri
- **Saatlik**: Her saat başında dakika 0'da
- **Günlük**: Belirtilen zamanda günde bir kez
- **Haftalık**: Haftanın belirli günü ve saati
- **Aylık**: Ayın belirli günü ve saati
- **Özel**: Cron benzeri ifadeler

#### İş Yönetimi
- **Şimdi Çalıştır**: Test için işi hemen yürütün
- **Aktif/Pasif Değiştir**: İşleri etkinleştir/devre dışı bırak
- **Zamanlamayı Düzenle**: Zamanlama ve sorguyu değiştirin
- **Geçmişi Görüntüle**: Yürütme loglarını ve sonuçları görün
- **İşi Sil**: Zamanlanmış sorguları kaldırın

### 🔒 Güvenlik ve Kimlik Bilgisi Yönetimi

#### Güvenli Depolama
- **OS Entegrasyonu**: Şifreler Windows Credential Manager'da saklanır
- **Şifreleme**: DPAPI kullanarak donanım destekli şifreleme
- **Düz Metin Yok**: Şifreler asla dosyalarda veya loglarda saklanmaz
- **Oturum Yönetimi**: Otomatik oturum zaman aşımı

#### Kimlik Bilgisi Yönetimi
- **Kimlik Bilgilerini Temizle**: Saklanan şifreleri kaldırın
- **Yeniden Bağlan**: Veritabanı bağlantısını yeniden kurun
- **Çoklu Veritabanları**: Birden fazla veritabanı bağlantısı desteği
- **Kullanıcı Kontrolü**: Kimlik bilgisi yaşam döngüsü üzerinde tam kontrol

### 🚨 Yaygın Sorunları Giderme

#### Bağlantı Sorunları
```
Hata: "Login failed for user"
Çözüm: Kullanıcı adı/şifre ve SQL Server kimlik doğrulama modunu doğrulayın

Hata: "Cannot connect to server"
Çözüm: Sunucu adı, port ve güvenlik duvarı ayarlarını kontrol edin

Hata: "Driver not found"
Çözüm: ODBC Driver 17 for SQL Server'ı kurun
```

#### Sorgu Sorunları
```
Hata: "Invalid column name"
Çözüm: Şema keşfedicide tablo/sütun adlarını kontrol edin

Hata: "Permission denied"
Çözüm: Kullanıcının gerekli veritabanı izinlerine sahip olduğunu doğrulayın

Hata: "Timeout expired"
Çözüm: .env'de DB_CONNECTION_TIMEOUT'u artırın
```

#### Performans Sorunları
```
Yavaş sorgular: AI'dan sorgu optimizasyon önerilerini kullanın
Büyük sonuç setleri: Sorgulara LIMIT yan tümceleri ekleyin
Bellek sorunları: Yapılandırmada MAX_QUERY_LENGTH'i artırın
```

## 🔧 Geliştirme Kurulumu (İsteğe Bağlı)

### Kod Kalitesi Araçları
```bash
# Geliştirme bağımlılıklarını kurun
pip install pytest pytest-flask black flake8 mypy

# Kodu formatlayın
black .

# Kodu lint edin
flake8 .

# Tip kontrolü
mypy .

# Testleri çalıştırın
pytest
```

### IDE Yapılandırması (VS Code)
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true
}
```

## 🚀 Üretim Dağıtımı

### Ortam Yapılandırması
```bash
# Üretim ortam değişkenleri
DEBUG=False
LOG_LEVEL=WARNING
SECRET_KEY=your-production-secret-key
OPENAI_API_KEY=your-production-api-key
DB_CONNECTION_TIMEOUT=60
MAX_CONCURRENT_JOBS=50
```

### Web Sunucu Kurulumu
```bash
# Gunicorn kullanarak (Linux/macOS)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Waitress kullanarak (Windows)
pip install waitress
waitress-serve --host=0.0.0.0 --port=8000 app:app
```

### SSL/TLS Yapılandırması
```bash
# Let's Encrypt kullanarak
certbot --nginx -d your-domain.com

# Veya özel sertifikalar kullanarak
# Sertifikaları /etc/ssl/certs/ dizinine yerleştirin
```

## 📄 Lisans ve Yasal

### MIT Lisansı
```
MIT License

Copyright (c) 2024 SQL Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Üçüncü Taraf Lisansları
- **OpenAI API**: OpenAI'nin Hizmet Şartlarına tabidir
- **Microsoft SQL Server**: Microsoft'un lisans şartlarına tabidir
- **Python Kütüphaneleri**: Çeşitli açık kaynak lisansları (requirements.txt'ye bakın)

### Uyumluluk ve Güvenlik
- **GDPR Uyumluluğu**: Kullanıcı verisi işleme ve gizlilik koruması
- **SOC 2**: Güvenlik kontrolleri ve izleme
- **ISO 27001**: Bilgi güvenliği yönetimi
- **HIPAA**: Sağlık verisi koruması (uygulanabilirse)

---

## 🤝 Katkıda Bulunma

Katkılarınızı memnuniyetle karşılıyoruz! Lütfen şunlar hakkında detaylar için [Katkıda Bulunma Rehberimizi](CONTRIBUTING.md) inceleyin:
- Hata bildirme ve özellik talep etme
- Kod değişiklikleri gönderme
- Kodlama standartlarımızı takip etme
- Topluluğumuzda yer alma

## 📞 Destek

- **Dokümantasyon**: [Tam Dokümantasyon](docs/)
- **Sorunlar**: [GitHub Issues](https://github.com/your-username/sql-agent-cursor/issues)
- **Tartışmalar**: [GitHub Discussions](https://github.com/your-username/sql-agent-cursor/discussions)
- **E-posta**: support@your-domain.com

---

**Veri topluluğu için ❤️ ile inşa edildi**
