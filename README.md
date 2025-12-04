# Maternal Health Monitoring API - MVP v1.0

Backend API for the Maternal Health Monitoring App, designed to support first-time pregnant mothers during their first trimester by providing secure health tracking and personalized educational content.

## Project Overview

This FastAPI backend implements the MVP architecture as defined in the System Architecture Document, focusing on:
- Secure user registration and authentication
- Daily health metric logging (symptoms, weight, mood)
- Week-specific educational content delivery
- Progress visualization and PDF export

## Project Structure

```
maternal-health-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── routers/             # API endpoint routes
│   │   └── __init__.py
│   ├── schemas/             # Pydantic models for validation
│   │   └── __init__.py
│   ├── db/                  # Database models and connection
│   │   └── __init__.py
│   └── services/            # Business logic layer
│       └── __init__.py
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- PostgreSQL (for production database)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd maternal-health-api
```

### 2. Create a virtual environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Server

### Development Mode

Start the development server with auto-reload:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/api/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Current Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with API information |
| `/health` | GET | Health check endpoint |

### Planned Endpoints (MVP v1.0)

Based on the System Architecture Document:

**Authentication & User Management**
- `POST /v1/auth/register` - User registration
- `POST /v1/users/profile` - Create pregnancy profile
- `PUT /v1/users/profile` - Update profile
- `GET /v1/users/profile` - Fetch user profile

**Daily Logging**
- `POST /v1/logs/daily` - Submit daily check-in
- `GET /v1/logs/weight` - Fetch weight trends
- `GET /v1/logs/mood` - Fetch mood history
- `GET /v1/logs/summary/pdf` - Generate PDF export

**Content Delivery**
- `GET /v1/content/week/{week_number}` - Get week-specific content
- `GET /v1/content/symptom/check` - Get symptom guidance

**Feedback**
- `POST /v1/feedback` - Submit user feedback (NPS)

## Development Roadmap

### Phase 1: Foundation (Current)
- [x] Project structure setup
- [x] Basic FastAPI application
- [x] Health check endpoint
- [ ] Database configuration
- [ ] Authentication service integration

### Phase 2: Core Features
- [ ] User registration and authentication
- [ ] Pregnancy profile management
- [ ] Daily logging endpoints
- [ ] Content delivery system

### Phase 3: Advanced Features
- [ ] Progress visualization
- [ ] PDF generation
- [ ] Push notification system
- [ ] NPS feedback collection

## Testing

```bash
# Install testing dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Database Setup

The application uses PostgreSQL for data persistence. To set up the database:

1. Create a PostgreSQL database:
```sql
CREATE DATABASE maternal_health_db;
```

2. Update the `DATABASE_URL` in your `.env` file

3. Run migrations (once implemented):
```bash
alembic upgrade head
```

## Contributing

This is an MVP project. Future contributions should:
- Follow the PRD and Architecture documents
- Maintain focus on first-trimester features (Weeks 1-12)
- Prioritize user anxiety reduction and data security
- Include appropriate tests

## Security Notes

- All endpoints (except health check) will require authentication
- Sensitive health data must be encrypted at rest
- HTTPS must be used in production
- Regular security audits are required

## License

Apache License Version 2.0, January 2004 http://www.apache.org/licenses/


## Support

For questions or issues, please contact the development team.