import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from io import BytesIO
import json

from app.main import app
from app.core.database import get_db, Base
from app.models.resume import Resume
from app.models.user import User


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db_session():
    # Create in-memory database for testing
    from sqlalchemy import create_engine
    from sqlalchemy.orm.sessionmaker
    
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_user(db_session):
    user = User(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


class TestResumeUpload:
    
    def test_upload_resume_text_success(self, client, db_session, test_user):
        """Test successful resume upload with text."""
        response = client.post(
            "/api/v1/resumes/upload",
            data={
                "text": "Software Engineer with 5 years of experience in Python and JavaScript.",
                "title": "Software Engineer Resume"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Software Engineer Resume"
        assert data["message"] == "Resume uploaded successfully"
        assert data["text_length"] > 0
        
        # Verify database record
        resume = db_session.query(Resume).filter(Resume.id == data["id"]).first()
        assert resume is not None
        assert resume.title == "Software Engineer Resume"
        assert resume.raw_text == "Software Engineer with 5 years of experience in Python and JavaScript."
    
    def test_upload_resume_text_empty(self, client):
        """Test resume upload with empty text."""
        response = client.post(
            "/api/v1/resumes/upload",
            data={"text": ""}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Resume text cannot be empty" in data["detail"]
    
    def test_upload_resume_text_missing_fields(self, client):
        """Test resume upload with missing both file and text."""
        response = client.post(
            "/api/v1/resumes/upload",
            data={}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Either file or text must be provided" in data["detail"]
    
    def test_upload_resume_file_success(self, client, db_session, test_user):
        """Test successful resume upload with file."""
        # Create a mock file
        file_content = b"Software Engineer\n\nExperience: 5 years\nSkills: Python, JavaScript"
        file_data = BytesIO(file_content)
        
        response = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("resume.txt", file_data, "text/plain")},
            data={"title": "Test Resume"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Resume"
        assert data["file_type"] == "txt"
        assert data["message"] == "Resume uploaded successfully"
    
    def test_upload_resume_file_invalid_type(self, client):
        """Test resume upload with invalid file type."""
        file_content = b"Invalid file content"
        file_data = BytesIO(file_content)
        
        response = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("resume.xyz", file_data, "application/octet-stream")},
            data={"title": "Test Resume"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Unsupported file type" in data["detail"]
    
    def test_upload_resume_file_too_large(self, client):
        """Test resume upload with file exceeding size limit."""
        # Create a large file (over 10MB)
        large_content = b"x" * (11 * 1024 * 1024)  # 11MB
        file_data = BytesIO(large_content)
        
        response = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("large_resume.txt", file_data, "text/plain")},
            data={"title": "Large Resume"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "File size exceeds maximum allowed size" in data["detail"]
    
    def test_get_resumes_success(self, client, db_session, test_user):
        """Test getting all resumes for a user."""
        # Create test resumes
        resume1 = Resume(
            user_id=test_user.id,
            title="Resume 1",
            raw_text="First resume content",
            file_type="txt",
            is_active="draft"
        )
        resume2 = Resume(
            user_id=test_user.id,
            title="Resume 2",
            raw_text="Second resume content",
            file_type="txt",
            is_active="active"
        )
        db_session.add(resume1)
        db_session.add(resume2)
        db_session.commit()
        
        response = client.get("/api/v1/resumes/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["resumes"]) == 2
        
        # Check resume order (newest first)
        assert data["resumes"][0]["title"] == "Resume 2"  # active resume should be first
        assert data["resumes"][1]["title"] == "Resume 1"
    
    def test_get_resume_by_id_success(self, client, db_session, test_user):
        """Test getting a specific resume by ID."""
        resume = Resume(
            user_id=test_user.id,
            title="Test Resume",
            raw_text="Test resume content",
            file_type="txt",
            is_active="draft"
        )
        db_session.add(resume)
        db_session.commit()
        db_session.refresh(resume)
        
        response = client.get(f"/api/v1/resumes/{resume.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == resume.id
        assert data["title"] == "Test Resume"
        assert data["raw_text"] == "Test resume content"
    
    def test_get_resume_by_id_not_found(self, client, db_session, test_user):
        """Test getting a resume that doesn't exist."""
        response = client.get("/api/v1/resumes/99999")
        
        assert response.status_code == 404
        data = response.json()
        assert "Resume not found" in data["detail"]
    
    def test_update_resume_success(self, client, db_session, test_user):
        """Test updating a resume."""
        resume = Resume(
            user_id=test_user.id,
            title="Original Title",
            raw_text="Original content",
            file_type="txt",
            is_active="draft"
        )
        db_session.add(resume)
        db_session.commit()
        db_session.refresh(resume)
        
        response = client.put(
            f"/api/v1/resumes/{resume.id}",
            json={"title": "Updated Title", "is_active": "active"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["is_active"] == "active"
        assert "updated_at" in data
    
    def test_update_resume_invalid_status(self, client, db_session, test_user):
        """Test updating a resume with invalid status."""
        resume = Resume(
            user_id=test_user.id,
            title="Test Resume",
            raw_text="Test content",
            file_type="txt",
            is_active="draft"
        )
        db_session.add(resume)
        db_session.commit()
        db_session.refresh(resume)
        
        response = client.put(
            f"/api/v1/resumes/{resume.id}",
            json={"is_active": "invalid_status"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Invalid status" in data["detail"]
    
    def test_delete_resume_success(self, client, db_session, test_user):
        """Test deleting a resume."""
        resume = Resume(
            user_id=test_user.id,
            title="Test Resume",
            raw_text="Test content",
            file_type="txt",
            is_active="draft"
        )
        db_session.add(resume)
        db_session.commit()
        db_session.refresh(resume)
        resume_id = resume.id
        
        response = client.delete(f"/api/v1/resumes/{resume_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Resume deleted successfully"
        
        # Verify resume is deleted
        deleted_resume = db_session.query(Resume).filter(Resume.id == resume_id).first()
        assert deleted_resume is None
    
    def test_delete_resume_not_found(self, client):
        """Test deleting a resume that doesn't exist."""
        response = client.delete("/api/v1/resumes/99999")
        
        assert response.status_code == 404
        data = response.json()
        assert "Resume not found" in data["detail"]


if __name__ == "__main__":
    pytest.main([__file__])
