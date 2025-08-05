# SQL Agent - FastAPI Backend

A FastAPI backend for an AI-powered SQL agent that can interact with SQL Server AdventureWorks database to answer user queries.

## Features

- User authentication (sign up/login) with JWT tokens
- AI-powered SQL query generation using OpenAI GPT
- Natural language to SQL translation
- Multi-turn conversation support
- Session management
- AdventureWorks database integration
- User-friendly response formatting

## Project Structure

```
├── app/
│   ├── routes/          # API endpoints
│   │   ├── auth.py      # User authentication routes
│   │   ├── signin.py    # User sign up routes
│   │   └── query.py     # Question/query handling routes
│   ├── schemas/         # Pydantic models
│   │   ├── auth.py      # Authentication schemas
│   │   ├── signin.py    # Sign up schemas
│   │   └── query.py     # Query schemas
│   ├── services/        # Business logic
│   │   ├── auth.py      # Authentication service
│   │   ├── signin.py    # Sign up service
│   │   └── answering.py # Query answering service
│   ├── agent/           # AI agent components
│   │   ├── tools/       # Individual agent tools
│   │   │   ├── schema_tool.py
│   │   │   ├── query_tool.py
│   │   │   ├── relevance_tool.py
│   │   │   └── format_tool.py
│   │   └── main_agent.py # Main agent orchestrator
│   ├── database/        # Database configuration
│   │   ├── connection.py
│   │   └── models.py
│   └── core/            # Core configurations
│       ├── config.py
│       └── security.py
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
└── .env.example         # Environment variables template
```

## Setup Instructions

### 1. Environment Setup

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
AUTH_DATABASE_URL=mssql+pyodbc://username:password@server/auth_database?driver=ODBC+Driver+17+for+SQL+Server

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Redis Configuration (for session management)
REDIS_URL=redis://localhost:6379
```

### 2. Database Setup

1. Install SQL Server and SQL Server Management Studio
2. Download and restore AdventureWorks sample database
3. Create a separate database for user authentication
4. Update connection strings in `.env` file

### 3. Installation

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
```

### 4. API Endpoints

- `POST /auth/signin` - User registration
- `POST /auth/login` - User login
- `POST /query/ask` - Submit questions to the SQL agent
- `GET /query/history` - Get conversation history

## Usage Examples

### User Registration
```json
POST /auth/signin
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password"
}
```

### User Login
```json
POST /auth/login
{
    "username": "john_doe",
    "password": "secure_password"
}
```

### Ask Question
```json
POST /query/ask
{
    "question": "Show me the top 5 customers by total sales",
    "session_id": "optional_session_id"
}
```

## Sample Questions

The agent can handle questions like:
- "Show me the top 10 products by sales"
- "What are the total sales for each category?"
- "List customers from California"
- "Show monthly sales trends for 2023"
- "Which employees have the highest sales?"

## Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **OpenAI GPT**: For natural language understanding and SQL generation
- **LangChain**: For building the AI agent
- **JWT**: For secure authentication
- **Redis**: For session management
- **SQL Server**: Database engine

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is for educational purposes as part of BSc Hons in AI coursework.