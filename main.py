from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from decouple import config
from speech_emotion import get_speech_emotion_recognizer

# Configuration
SECRET_KEY = config("SECRET_KEY", default="your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Jumpstart with Speech Emotion Recognition",
    description="A comprehensive FastAPI starter template with authentication, CRUD operations, and speech emotion recognition using Hugging Face models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime

class SpeechEmotionResponse(BaseModel):
    predicted_emotion: str
    confidence: float
    all_emotions: Dict[str, float]
    model_name: str
    processing_time: Optional[float] = None

# In-memory storage (replace with database in production)
users_db = []
tasks_db = []
user_id_counter = 1
task_id_counter = 1

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = next((user for user in users_db if user["username"] == username), None)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to FastAPI Jumpstart!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# User authentication routes
@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Register a new user"""
    global user_id_counter
    
    # Check if user already exists
    if any(u["username"] == user.username or u["email"] == user.email for u in users_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    new_user = {
        "id": user_id_counter,
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    users_db.append(new_user)
    user_id_counter += 1
    
    return UserResponse(**new_user)

@app.post("/login", response_model=Token)
async def login(username: str, password: str):
    """Login and get access token"""
    user = next((user for user in users_db if user["username"] == username), None)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(**current_user)

# Task management routes
@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, current_user: dict = Depends(get_current_user)):
    """Create a new task"""
    global task_id_counter
    
    new_task = {
        "id": task_id_counter,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "user_id": current_user["id"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    tasks_db.append(new_task)
    task_id_counter += 1
    
    return TaskResponse(**new_task)

@app.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(current_user: dict = Depends(get_current_user)):
    """Get all tasks for the current user"""
    user_tasks = [task for task in tasks_db if task["user_id"] == current_user["id"]]
    return [TaskResponse(**task) for task in user_tasks]

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, current_user: dict = Depends(get_current_user)):
    """Get a specific task"""
    task = next((task for task in tasks_db if task["id"] == task_id and task["user_id"] == current_user["id"]), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(**task)

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskCreate, current_user: dict = Depends(get_current_user)):
    """Update a specific task"""
    task_index = next((i for i, task in enumerate(tasks_db) if task["id"] == task_id and task["user_id"] == current_user["id"]), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks_db[task_index].update({
        "title": task_update.title,
        "description": task_update.description,
        "completed": task_update.completed,
        "updated_at": datetime.utcnow()
    })
    
    return TaskResponse(**tasks_db[task_index])

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    """Delete a specific task"""
    task_index = next((i for i, task in enumerate(tasks_db) if task["id"] == task_id and task["user_id"] == current_user["id"]), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    deleted_task = tasks_db.pop(task_index)
    return {"message": "Task deleted successfully", "task": TaskResponse(**deleted_task)}

# Speech Emotion Recognition routes
@app.post("/api/v1/speech-emotion/analyze", response_model=SpeechEmotionResponse)
async def analyze_speech_emotion_authenticated(
    audio_file: UploadFile = File(..., description="WAV audio file for emotion analysis"),
    current_user: dict = Depends(get_current_user)
):
    """
    🔐 Analyze emotion from uploaded WAV audio file (Authenticated endpoint)
    
    **Required Authentication**: Bearer token in Authorization header
    
    **Request**:
    - Method: POST
    - Content-Type: multipart/form-data
    - Body: audio_file (WAV file)
    - Header: Authorization: Bearer <your_jwt_token>
    
    **Response**: Emotion analysis with confidence scores
    """
    return await _process_audio_emotion(audio_file, current_user["username"])

async def _process_audio_emotion(audio_file: UploadFile, user_identifier: str = "anonymous"):
    """Internal function to process audio emotion recognition"""
    import time
    start_time = time.time()
    
    # Validate file type
    if not audio_file.filename:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "FILE_NAME_MISSING",
                "message": "Audio file name is required",
                "supported_formats": ["wav", "wave"]
            }
        )
    
    if not audio_file.filename.lower().endswith(('.wav', '.wave')):
        raise HTTPException(
            status_code=400,
            detail={
                "error": "UNSUPPORTED_FORMAT",
                "message": f"File '{audio_file.filename}' is not a supported format",
                "supported_formats": ["wav", "wave"],
                "received_format": audio_file.filename.split('.')[-1] if '.' in audio_file.filename else "unknown"
            }
        )
    
    try:
        # Read audio file bytes
        audio_bytes = await audio_file.read()
        
        if len(audio_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "EMPTY_FILE",
                    "message": "Uploaded audio file is empty",
                    "file_size": 0
                }
            )
        
        if len(audio_bytes) > 50 * 1024 * 1024:  # 50MB limit
            raise HTTPException(
                status_code=413,
                detail={
                    "error": "FILE_TOO_LARGE",
                    "message": "Audio file is too large",
                    "max_size_mb": 50,
                    "received_size_mb": round(len(audio_bytes) / (1024 * 1024), 2)
                }
            )
        
        # Get emotion recognizer instance
        recognizer = get_speech_emotion_recognizer()
        
        # Analyze emotion
        result = recognizer.predict_emotion_from_bytes(audio_bytes, audio_file.filename)
        
        # Add processing metadata
        processing_time = time.time() - start_time
        result.update({
            "processing_time": round(processing_time, 2),
            "file_info": {
                "filename": audio_file.filename,
                "size_bytes": len(audio_bytes),
                "size_mb": round(len(audio_bytes) / (1024 * 1024), 2)
            },
            "processed_by": user_identifier,
            "timestamp": datetime.utcnow().isoformat(),
            "api_version": "1.0"
        })
        
        return SpeechEmotionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "PROCESSING_ERROR",
                "message": f"Error processing audio file: {str(e)}",
                "file_name": audio_file.filename if audio_file.filename else "unknown"
            }
        )

@app.post("/api/v1/speech-emotion/analyze-public", response_model=SpeechEmotionResponse)
async def analyze_speech_emotion_public(
    audio_file: UploadFile = File(..., description="WAV audio file for emotion analysis")
):
    """
    🌐 Analyze emotion from uploaded WAV audio file (Public endpoint - No authentication required)
    
    **Perfect for Postman Testing!**
    
    **Request Setup for Postman**:
    1. Method: POST
    2. URL: http://localhost:8000/api/v1/speech-emotion/analyze-public
    3. Body: form-data
    4. Key: audio_file (type: File)
    5. Value: Select your .wav file
    
    **Response**: Detailed emotion analysis with confidence scores
    
    **Supported formats**: WAV files only
    **Max file size**: 50MB
    """
    return await _process_audio_emotion(audio_file, "public_user")

@app.get("/api/v1/speech-emotion/info")
async def get_speech_emotion_info():
    """
    📋 Get comprehensive information about the speech emotion recognition system
    
    **Perfect for Postman Testing**:
    - Method: GET
    - URL: http://localhost:8000/api/v1/speech-emotion/info
    """
    return {
        "service": "Speech Emotion Recognition API",
        "version": "1.0",
        "model": {
            "name": "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition",
            "type": "Wav2Vec2 Audio Classification",
            "emotions": ["angry", "calm", "disgust", "fearful", "happy", "neutral", "sad", "surprised"],
            "description": "Advanced speech emotion recognition using Wav2Vec2 transformer model"
        },
        "api_endpoints": {
            "public_analysis": "/api/v1/speech-emotion/analyze-public",
            "authenticated_analysis": "/api/v1/speech-emotion/analyze",
            "model_info": "/api/v1/speech-emotion/info",
            "health_check": "/health"
        },
        "supported_formats": ["wav", "wave"],
        "max_file_size": "50MB",
        "sample_rate": "16kHz (auto-converted)",
        "postman_setup": {
            "method": "POST",
            "url": "http://localhost:8000/api/v1/speech-emotion/analyze-public",
            "body_type": "form-data",
            "field_name": "audio_file",
            "field_type": "File",
            "instructions": "Select a WAV audio file from your computer"
        },
        "example_response": {
            "predicted_emotion": "happy",
            "confidence": 0.876,
            "all_emotions": {
                "happy": 0.876,
                "neutral": 0.098,
                "calm": 0.026
            },
            "model_name": "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition",
            "processing_time": 2.34,
            "file_info": {
                "filename": "sample.wav",
                "size_mb": 1.2
            }
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
