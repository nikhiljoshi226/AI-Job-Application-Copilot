from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Job Application Copilot API",
    version="0.1.0",
    description="Simple API for frontend testing"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "AI Job Application Copilot API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/v1/resumes")
async def get_resumes():
    return [
        {
            "id": 1,
            "title": "Senior Frontend Developer Resume",
            "file_name": "john_doe_frontend_dev.pdf",
            "uploaded_at": "2024-01-15T10:30:00Z",
            "status": "processed"
        },
        {
            "id": 2,
            "title": "Full Stack Developer Resume",
            "file_name": "jane_smith_full_stack.pdf", 
            "uploaded_at": "2024-01-10T14:20:00Z",
            "status": "processed"
        }
    ]

@app.get("/api/v1/analyses")
async def get_analyses():
    return [
        {
            "id": 1,
            "resume_id": 1,
            "job_title": "Senior Frontend Developer",
            "company": "TechCorp",
            "fit_score": 85,
            "status": "completed",
            "created_at": "2024-01-15T10:30:00Z"
        },
        {
            "id": 2,
            "resume_id": 2,
            "job_title": "Full Stack Developer",
            "company": "StartupXYZ",
            "fit_score": 72,
            "status": "completed",
            "created_at": "2024-01-10T14:20:00Z"
        }
    ]

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "simple_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
