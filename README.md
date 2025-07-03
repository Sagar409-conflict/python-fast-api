# FastAPI Jumpstart

A comprehensive FastAPI starter template with authentication, CRUD operations, and modern Python practices.

## Features

- ✅ **FastAPI Framework** - Modern, fast web framework for building APIs
- ✅ **Authentication** - JWT-based authentication with bcrypt password hashing
- ✅ **CRUD Operations** - Complete task management system
- ✅ **Speech Emotion Recognition** - AI-powered emotion analysis from audio files using Hugging Face models
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

### Speech Emotion Recognition

- `POST /analyze-speech-emotion` - Analyze emotion from WAV audio file (authenticated)
- `POST /analyze-speech-emotion-public` - Analyze emotion from WAV audio file (public)
- `GET /speech-emotion/model-info` - Get information about the emotion recognition model

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

### 4. Analyze Speech Emotion (with WAV file)

```bash
# Public endpoint (no authentication required)
curl -X POST "http://localhost:8000/analyze-speech-emotion-public" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@path/to/your/audio.wav"

# Authenticated endpoint
curl -X POST "http://localhost:8000/analyze-speech-emotion" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@path/to/your/audio.wav"
```

### 5. Get Model Information

```bash
curl -X GET "http://localhost:8000/speech-emotion/model-info"
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

## Speech Emotion Recognition

This application includes AI-powered speech emotion recognition using the Hugging Face model `firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3`.

### Features:
- **Real-time emotion analysis** from WAV audio files
- **Multiple emotion detection** with confidence scores
- **Public and authenticated endpoints** for different use cases
- **Automatic audio preprocessing** (resampling, normalization)
- **Model caching** for faster subsequent requests

### Supported Audio Formats:
- WAV files (recommended: 16kHz sample rate)
- Mono or stereo audio
- Duration: up to 30 seconds (optimal: 2-10 seconds)

### Response Format:
```json
{
  "predicted_emotion": "happy",
  "confidence": 0.85,
  "all_emotions": {
    "happy": 0.85,
    "neutral": 0.10,
    "sad": 0.03,
    "angry": 0.02
  },
  "model_name": "firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3",
  "processing_time": 1.23
}
```

### Testing:
1. Generate sample audio files: `python generate_sample_audio.py`
2. Test the API: `python test_api.py`
3. Or use the interactive docs at http://localhost:8000/docs

### First Run:
The model will be downloaded automatically on first use (~1-2GB). This may take a few minutes depending on your internet connection. Subsequent requests will be much faster.

## Configuration
