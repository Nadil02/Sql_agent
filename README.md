# SQL Agent - AI-Powered Database Assistant

## Features

- Natural language to SQL query conversion
- SQL Server AdventureWorks database support
- Docker containerization
- Deployed on Render


# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
```


## 🔧 Technologies

- **FastAPI** - Web framework
- **Google Gemini** - AI model
- **LangChain** - AI agent framework
- **SQL Server** - Database (AdventureWorks)
- **Docker** - Containerization
- **Render** - Cloud deployment
