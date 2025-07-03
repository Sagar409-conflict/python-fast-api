# 🚀 **FastAPI Speech Emotion Recognition - Postman Testing Guide**

## 📋 **Server Status**
✅ **Server is running at: http://localhost:8000**
✅ **API Documentation: http://localhost:8000/docs**
✅ **Model loaded: ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition**

---

## 🎯 **Main API Endpoints for Postman Testing**

### 1. **📊 Get API Information** (GET Request)
- **URL**: `http://localhost:8000/api/v1/speech-emotion/info`
- **Method**: GET
- **Description**: Get complete API information and setup instructions
- **No authentication required**

### 2. **🎤 Analyze Speech Emotion (PUBLIC)** (POST Request) 
- **URL**: `http://localhost:8000/api/v1/speech-emotion/analyze-public`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Body**: 
  - Key: `audio_file` (File type)
  - Value: Select your .wav file
- **No authentication required**
- **Perfect for testing!**

### 3. **🔐 Analyze Speech Emotion (AUTHENTICATED)** (POST Request)
- **URL**: `http://localhost:8000/api/v1/speech-emotion/analyze`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Headers**: `Authorization: Bearer <your_jwt_token>`
- **Body**: 
  - Key: `audio_file` (File type)
  - Value: Select your .wav file

---

## 🛠️ **Step-by-Step Postman Setup**

### **Method 1: Test API Info (Quick Test)**

1. **Open Postman**
2. **Create New Request**
3. **Set Method**: GET
4. **Set URL**: `http://localhost:8000/api/v1/speech-emotion/info`
5. **Click Send**
6. **You should see**: Complete API information with setup instructions

### **Method 2: Test Speech Emotion Analysis (Main Feature)**

1. **Open Postman**
2. **Create New Request**
3. **Set Method**: POST
4. **Set URL**: `http://localhost:8000/api/v1/speech-emotion/analyze-public`
5. **Go to Body tab**
6. **Select**: form-data
7. **Add Key**: `audio_file`
8. **Change Type to**: File (dropdown next to key)
9. **Select Value**: Choose your .wav file from computer
10. **Click Send**

### **Expected Response Format:**
```json
{
  "predicted_emotion": "happy",
  "confidence": 0.876,
  "all_emotions": {
    "happy": 0.876,
    "neutral": 0.098,
    "calm": 0.026,
    "sad": 0.015,
    "angry": 0.003,
    "fearful": 0.002,
    "disgust": 0.001,
    "surprised": 0.001
  },
  "model_name": "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition",
  "processing_time": 2.34,
  "file_info": {
    "filename": "sample.wav",
    "size_bytes": 1245760,
    "size_mb": 1.19
  },
  "processed_by": "public_user",
  "timestamp": "2025-07-03T07:01:30.123456",
  "api_version": "1.0"
}
```

---

## 🎵 **Sample Audio Files for Testing**

You have these sample files available in `d:\Python\sample_audio\`:
- **Happy emotion**: Use `happy_sample_1.wav`
- **Test with any emotion**: Multiple generated samples available

### **Create Your Own Test Audio:**
1. Record a 5-10 second voice clip expressing emotion
2. Save as .wav format
3. Upload via Postman

---

## 🔐 **Authentication Testing (Optional)**

If you want to test the authenticated endpoint:

### **Step 1: Register a User**
- **URL**: `http://localhost:8000/register`
- **Method**: POST
- **Content-Type**: application/json
- **Body**:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123"
}
```

### **Step 2: Login to Get Token**
- **URL**: `http://localhost:8000/login`
- **Method**: POST
- **Content-Type**: application/x-www-form-urlencoded
- **Body** (form-data):
  - `username`: testuser
  - `password`: testpass123

### **Step 3: Use Token for Authenticated Requests**
- **URL**: `http://localhost:8000/api/v1/speech-emotion/analyze`
- **Method**: POST
- **Headers**: `Authorization: Bearer <token_from_step_2>`
- **Body**: Same file upload as public endpoint

---

## 📝 **Postman Collection JSON**

Save this as a .json file and import into Postman:

```json
{
  "info": {
    "name": "Speech Emotion Recognition API",
    "description": "Complete FastAPI Speech Emotion Recognition testing collection",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Get API Info",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/api/v1/speech-emotion/info",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "v1", "speech-emotion", "info"]
        }
      }
    },
    {
      "name": "Analyze Speech Emotion (Public)",
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            {
              "key": "audio_file",
              "type": "file",
              "src": []
            }
          ]
        },
        "url": {
          "raw": "http://localhost:8000/api/v1/speech-emotion/analyze-public",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "v1", "speech-emotion", "analyze-public"]
        }
      }
    },
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/health",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["health"]
        }
      }
    }
  ]
}
```

---

## ✨ **Quick Test Commands**

### **PowerShell/CMD Testing:**
```bash
# Test API info
curl http://localhost:8000/api/v1/speech-emotion/info

# Test file upload (if you have curl with file support)
curl -X POST -F "audio_file=@path/to/your/file.wav" http://localhost:8000/api/v1/speech-emotion/analyze-public
```

---

## 🎯 **Supported Audio Formats**
- **Format**: WAV files only
- **Sample Rate**: 16kHz (auto-converted)
- **Max File Size**: 50MB
- **Duration**: 3-30 seconds recommended

## 🎭 **Supported Emotions**
The model can detect these 8 emotions:
- angry
- calm  
- disgust
- fearful
- happy
- neutral
- sad
- surprised

---

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **"Connection refused"**
   - Check if server is running: `http://localhost:8000/health`
   - Restart server if needed

2. **"Unsupported file format"**
   - Ensure file is .wav format
   - Check file is not corrupted

3. **"File too large"**
   - Maximum file size is 50MB
   - Compress audio if needed

4. **"Empty file"**
   - Ensure audio file has content
   - Check file was uploaded correctly

### **Server Commands:**
```bash
# Start server
cd "d:\Python"
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🎉 **You're Ready to Test!**

The API is now fully configured for Postman testing. Start with the **API Info endpoint** to verify everything is working, then test with the **public speech emotion analysis endpoint** using your .wav files!

**Happy Testing! 🚀**
