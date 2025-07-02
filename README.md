# FastAPI Jumpstart

A comprehensive FastAPI starter template with authentication, CRUD operations, and modern Python practices.

## Features

- ✅ **FastAPI Framework** - Modern, fast web framework for building APIs
- ✅ **Authentication** - JWT-based authentication with bcrypt password hashing
- ✅ **CRUD Operations** - Complete task management system
- ✅ **Pydantic Models** - Data validation and serialization
- ✅ **CORS Support** - Cross-origin resource sharing configured
- ✅ **Auto Documentation** - Interactive API docs with Swagger UI
- ✅ **Security** - HTTP Bearer token authentication
- ✅ **Environment Variables** - Configuration management with python-decouple
- ✅ **Database Ready** - SQLAlchemy and Alembic included for database integration
- ✅ **Testing** - Pytest configuration for API testing
- ✅ **Background Tasks** - Celery integration for async task processing

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /register` - Register a new user
- `POST /login` - Login and get access token
- `GET /users/me` - Get current user information

### Tasks
- `POST /tasks` - Create a new task
- `GET /tasks` - Get all tasks for current user
- `GET /tasks/{task_id}` - Get a specific task
- `PUT /tasks/{task_id}` - Update a specific task
- `DELETE /tasks/{task_id}` - Delete a specific task

### Health
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

## Usage Examples

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "johndoe",
       "email": "john@example.com",
       "password": "secretpassword"
     }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=johndoe&password=secretpassword"
```

### 3. Create a Task (with Bearer token)

```bash
curl -X POST "http://localhost:8000/tasks" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Learn FastAPI",
       "description": "Study FastAPI documentation and build a project",
       "completed": false
     }'
```

## Configuration

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
REDIS_URL=redis://localhost:6379
```

## Database Integration

To use with a real database:

1. **Install database driver** (PostgreSQL example):
   ```bash
   pip install psycopg2-binary
   ```

2. **Update database configuration** in `database.py`

3. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=.
```

## Project Structure

```
fastapi-jumpstart/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── database.py          # Database configuration (optional)
├── models.py           # Database models (optional)
├── schemas.py          # Pydantic schemas (optional)
├── crud.py             # CRUD operations (optional)
├── auth.py             # Authentication utilities (optional)
├── tests/              # Test files
├── alembic/            # Database migrations
├── .env                # Environment variables
└── README.md           # This file
```

## Next Steps

1. **Database Integration**: Replace in-memory storage with SQLAlchemy models
2. **File Upload**: Add endpoints for file handling
3. **Email Integration**: Add email notifications
4. **Rate Limiting**: Implement API rate limiting
5. **Logging**: Add comprehensive logging
6. **Docker**: Containerize the application
7. **CI/CD**: Set up continuous integration and deployment

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py
```

## Production Deployment

For production deployment, consider:

1. Use a production ASGI server like Gunicorn with Uvicorn workers
2. Set up a reverse proxy (Nginx)
3. Use environment variables for configuration
4. Set up logging and monitoring
5. Use a production database (PostgreSQL, MySQL)
6. Implement proper security headers

## License

MIT License - feel free to use this template for your projects!
