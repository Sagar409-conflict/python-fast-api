@echo off
REM FastAPI Jumpstart Development Server
REM This script starts the FastAPI development server with hot reload

echo 🚀 Starting FastAPI Jumpstart Development Server...
echo 📍 Server will be available at: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo 📖 ReDoc Documentation: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo ----------------------------------------

REM Check if virtual environment exists
if not exist "venv" (
    echo ⚠️  Virtual environment not found. Creating one...
    python -m venv venv
    echo ✅ Virtual environment created.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if requirements.txt is newer than the last install
if not exist ".last_install" (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    echo. > .last_install
    echo ✅ Dependencies installed.
) else (
    for %%f in (requirements.txt) do set req_time=%%~tf
    for %%f in (.last_install) do set install_time=%%~tf
    REM Simple check - in production you might want a more sophisticated comparison
    echo 📦 Checking dependencies...
    pip install -r requirements.txt --quiet
)

REM Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
