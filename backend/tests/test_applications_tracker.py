import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.user import User
from app.models.application import Application, ApplicationStatus
from app.models.job_description import JobDescription
from app.models.resume import Resume


class TestApplicationsTracker:
    
    def setup_method(self):
        """Setup test fixtures."""
        self.base_url = "/api/v1/applications-tracker"
        
        # Sample application data
        self.sample_application = {
            "company": "Tech Corp",
            "position_title": "Software Engineer",
            "position_level": "Senior",
            "department": "Engineering",
            "employment_type": "full-time",
            "salary_min": 80000,
            "salary_max": 120000,
            "currency": "USD",
            "location": "San Francisco, CA",
            "remote_policy": "hybrid",
            "priority": "high",
            "source": "LinkedIn",
            "source_url": "https://linkedin.com/jobs/123",
            "notes": "Great opportunity for career growth",
            "tags": ["backend", "python", "django"],
            "planned_date": datetime(2023, 1, 15),
            "job_description_id": 1
        }
        
        self.sample_update = {
            "status": "applied",
            "applied_date": datetime(2023, 1, 20),
            "notes": "Applied through company website"
        }

    def test_create_application_success(self, client: TestClient, db: Session):
        """Test successful application creation."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        db.add(user)
        
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(job_description)
        db.commit()
        
        response = client.post(f"{self.base_url}/", json=self.sample_application)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["company"] == "Tech Corp"
        assert data["position_title"] == "Software Engineer"
        assert data["status"] == ApplicationStatus.PLANNED
        assert data["priority"] == "high"
        assert data["job_description_id"] == 1
        assert "id" in data
        assert "created_at" in data

    def test_create_application_validation_error(self, client: TestClient, db: Session):
        """Test application creation with validation errors."""
        # Missing required fields
        invalid_data = {
            "company": "",  # Empty company
            "position_title": "",  # Empty position
            "job_description_id": 999  # Non-existent JD
        }
        
        response = client.post(f"{self.base_url}/", json=invalid_data)
        
        assert response.status_code == 422  # Validation error

    def test_create_application_job_description_not_found(self, client: TestClient, db: Session):
        """Test application creation with non-existent job description."""
        # Create test user
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        db.add(user)
        db.commit()
        
        response = client.post(f"{self.base_url}/", json=self.sample_application)
        
        assert response.status_code == 404
        assert "Job description not found" in response.json()["detail"]

    def test_get_applications_empty(self, client: TestClient, db: Session):
        """Test getting applications when none exist."""
        # Create test user
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        db.add(user)
        db.commit()
        
        response = client.get(f"{self.base_url}/")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_get_applications_with_data(self, client: TestClient, db: Session):
        """Test getting applications with data."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(user)
        db.add(job_description)
        
        # Create applications
        app1 = Application(
            user_id=1,
            company="Tech Corp",
            position_title="Software Engineer",
            status=ApplicationStatus.PLANNED,
            job_description_id=1
        )
        app2 = Application(
            user_id=1,
            company="Data Corp",
            position_title="Data Scientist",
            status=ApplicationStatus.APPLIED,
            job_description_id=1
        )
        db.add(app1)
        db.add(app2)
        db.commit()
        
        response = client.get(f"{self.base_url}/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["company"] == "Data Corp"  # Ordered by created_at desc
        assert data[1]["company"] == "Tech Corp"

    def test_get_applications_with_filters(self, client: TestClient, db: Session):
        """Test getting applications with filters."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(user)
        db.add(job_description)
        
        # Create applications with different statuses
        app1 = Application(
            user_id=1,
            company="Tech Corp",
            position_title="Software Engineer",
            status=ApplicationStatus.PLANNED,
            priority="high",
            job_description_id=1
        )
        app2 = Application(
            user_id=1,
            company="Data Corp",
            position_title="Data Scientist",
            status=ApplicationStatus.APPLIED,
            priority="medium",
            job_description_id=1
        )
        db.add(app1)
        db.add(app2)
        db.commit()
        
        # Test status filter
        response = client.get(f"{self.base_url}/?status=planned")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == ApplicationStatus.PLANNED
        
        # Test priority filter
        response = client.get(f"{self.base_url}/?priority=high")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["priority"] == "high"
        
        # Test company filter
        response = client.get(f"{self.base_url}/?company=Tech")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["company"] == "Tech Corp"
        
        # Test search
        response = client.get(f"{self.base_url}/?search=Software")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "Software" in data[0]["position_title"]

    def test_get_applications_with_pagination(self, client: TestClient, db: Session):
        """Test getting applications with pagination."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(user)
        db.add(job_description)
        
        # Create multiple applications
        for i in range(5):
            app = Application(
                user_id=1,
                company=f"Company {i}",
                position_title=f"Position {i}",
                status=ApplicationStatus.PLANNED,
                job_description_id=1
            )
            db.add(app)
        db.commit()
        
        # Test pagination
        response = client.get(f"{self.base_url}/?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2  # Limit applied
        # Verify ordering (created_at desc)
        assert data[0]["company"] == "Company 2"
        assert data[1]["company"] == "Company 1"

    def test_get_application_by_id_success(self, client: TestClient, db: Session):
        """Test getting a specific application by ID."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(user)
        db.add(job_description)
        
        # Create application
        app = Application(
            user_id=1,
            company="Tech Corp",
            position_title="Software Engineer",
            status=ApplicationStatus.PLANNED,
            job_description_id=1
        )
        db.add(app)
        db.commit()
        
        response = client.get(f"{self.base_url}/{app.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["company"] == "Tech Corp"
        assert data["position_title"] == "Software Engineer"
        assert data["id"] == app.id

    def test_get_application_by_id_not_found(self, client: TestClient, db: Session):
        """Test getting a non-existent application."""
        # Create test user
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        db.add(user)
        db.commit()
        
        response = client.get(f"{self.base_url}/999")
        
        assert response.status_code == 404
        assert "Application not found" in response.json()["detail"]

    def test_update_application_success(self, client: TestClient, db: Session):
        """Test successful application update."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(user)
        db.add(job_description)
        
        # Create application
        app = Application(
            user_id=1,
            company="Tech Corp",
            position_title="Software Engineer",
            status=ApplicationStatus.PLANNED,
            job_description_id=1
        )
        db.add(app)
        db.commit()
        
        # Update application
        response = client.put(f"{self.base_url}/{app.id}", json=self.sample_update)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == ApplicationStatus.APPLIED
        assert data["applied_date"] == "2023-01-20T00:00:00"
        assert data["notes"] == "Applied through company website"

    def test_update_application_not_found(self, client: TestClient, db: Session):
        """Test updating a non-existent application."""
        # Create test user
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        db.add(user)
        db.commit()
        
        response = client.put(f"{self.base_url}/999", json=self.sample_update)
        
        assert response.status_code == 404
        assert "Application not found" in response.json()["detail"]

    def test_delete_application_success(self, client: TestClient, db: Session):
        """Test successful application deletion."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(user)
        db.add(job_description)
        
        # Create application
        app = Application(
            user_id=1,
            company="Tech Corp",
            position_title="Software Engineer",
            status=ApplicationStatus.PLANNED,
            job_description_id=1
        )
        db.add(app)
        db.commit()
        
        # Delete application
        response = client.delete(f"{self.base_url}/{app.id}")
        
        assert response.status_code == 200
        assert "Application deleted successfully" in response.json()["message"]
        
        # Verify deletion
        deleted_app = db.query(Application).filter(Application.id == app.id).first()
        assert deleted_app is None

    def test_delete_application_not_found(self, client: TestClient, db: Session):
        """Test deleting a non-existent application."""
        # Create test user
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        db.add(user)
        db.commit()
        
        response = client.delete(f"{self.base_url}/999")
        
        assert response.status_code == 404
        assert "Application not found" in response.json()["detail"]

    def test_get_dashboard_success(self, client: TestClient, db: Session):
        """Test getting application dashboard."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(user)
        db.add(job_description)
        
        # Create applications with different statuses
        app1 = Application(
            user_id=1,
            company="Tech Corp",
            position_title="Software Engineer",
            status=ApplicationStatus.PLANNED,
            priority="high",
            job_description_id=1
        )
        app2 = Application(
            user_id=1,
            company="Data Corp",
            position_title="Data Scientist",
            status=ApplicationStatus.APPLIED,
            priority="medium",
            job_description_id=1
        )
        app3 = Application(
            user_id=1,
            company="AI Corp",
            position_title="ML Engineer",
            status=ApplicationStatus.INTERVIEW,
            priority="low",
            job_description_id=1
        )
        db.add(app1)
        db.add(app2)
        db.add(app3)
        db.commit()
        
        response = client.get(f"{self.base_url}/dashboard")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check structure
        assert "applications" in data
        assert "total_count" in data
        assert "status_counts" in data
        assert "priority_counts" in data
        assert "recent_activity" in data
        
        # Check counts
        assert data["total_count"] == 3
        assert len(data["applications"]) == 3  # Recent activity limited to 10
        assert data["status_counts"]["planned"] == 1
        assert data["status_counts"]["applied"] == 1
        assert data["status_counts"]["interview"] == 1
        assert data["priority_counts"]["high"] == 1
        assert data["priority_counts"]["medium"] == 1
        assert data["priority_counts"]["low"] == 1

    def test_get_statistics_success(self, client: TestClient, db: Session):
        """Test getting application statistics."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(user)
        db.add(job_description)
        
        # Create applications with different outcomes
        app1 = Application(
            user_id=1,
            company="Tech Corp",
            position_title="Software Engineer",
            status=ApplicationStatus.APPLIED,
            job_description_id=1
        )
        app2 = Application(
            user_id=1,
            company="Data Corp",
            position_title="Data Scientist",
            status=ApplicationStatus.OFFER,
            final_status="offer",
            job_description_id=1
        )
        db.add(app1)
        db.add(app2)
        db.commit()
        
        response = client.get(f"{self.base_url}/statistics")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check structure
        assert "total_applications" in data
        assert "recent_applications" in data
        assert "success_rate" in data
        assert "status_distribution" in data
        assert "priority_distribution" in data
        assert "offers_count" in data
        
        # Check values
        assert data["total_applications"] == 2
        assert data["offers_count"] == 1
        assert data["success_rate"] == 50.0  # 1 offer out of 2 applications
        assert data["status_distribution"]["applied"] == 1
        assert data["status_distribution"]["offer"] == 1

    def test_get_statuses_success(self, client: TestClient):
        """Test getting available application statuses."""
        response = client.get(f"{self.base_url}/statuses")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "statuses" in data
        assert len(data["statuses"]) == 5
        
        # Check status structure
        for status in data["statuses"]:
            assert "value" in status
            assert "label" in status
            assert "description" in status
        
        # Check required statuses
        status_values = [s["value"] for s in data["statuses"]]
        assert "planned" in status_values
        assert "applied" in status_values
        assert "interview" in status_values
        assert "rejected" in status_values
        assert "offer" in status_values

    def test_get_priorities_success(self, client: TestClient):
        """Test getting available application priorities."""
        response = client.get(f"{self.base_url}/priorities")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "priorities" in data
        assert len(data["priorities"]) == 3
        
        # Check priority structure
        for priority in data["priorities"]:
            assert "value" in priority
            assert "label" in priority
            assert "description" in priority
        
        # Check required priorities
        priority_values = [p["value"] for p in data["priorities"]]
        assert "high" in priority_values
        assert "medium" in priority_values
        assert "low" in priority_values

    def test_get_sources_success(self, client: TestClient):
        """Test getting common application sources."""
        response = client.get(f"{self.base_url}/sources")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "sources" in data
        assert len(data["sources"]) >= 7  # At least the common ones
        
        # Check source structure
        for source in data["sources"]:
            assert "value" in source
            assert "label" in source
            assert "description" in source
        
        # Check common sources
        source_values = [s["value"] for s in data["sources"]]
        assert "LinkedIn" in source_values
        assert "Indeed" in source_values
        assert "Company Website" in source_values

    def test_create_application_with_linked_resources(self, client: TestClient, db: Session):
        """Test creating application with linked resources."""
        # Create test user and resources
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        resume = Resume(
            id=1,
            user_id=1,
            title="Software Engineer Resume",
            raw_text="Resume text"
        )
        db.add(user)
        db.add(job_description)
        db.add(resume)
        db.commit()
        
        # Create application with linked resources
        application_data = {
            **self.sample_application,
            "resume_id": 1,
            "tailored_resume_id": None,  # Not created yet
            "cover_letter_id": None,  # Not created yet
            "outreach_draft_id": None  # Not created yet
        }
        
        response = client.post(f"{self.base_url}/", json=application_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["resume_id"] == 1
        assert data["tailored_resume_id"] is None
        assert data["cover_letter_id"] is None
        assert data["outreach_draft_id"] is None

    def test_create_application_with_invalid_linked_resources(self, client: TestClient, db: Session):
        """Test creating application with invalid linked resources."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(user)
        db.add(job_description)
        db.commit()
        
        # Create application with non-existent resume
        application_data = {
            **self.sample_application,
            "resume_id": 999  # Non-existent
        }
        
        response = client.post(f"{self.base_url}/", json=application_data)
        
        assert response.status_code == 400
        assert "Resume not found" in response.json()["detail"]

    def test_update_application_with_linked_resources(self, client: TestClient, db: Session):
        """Test updating application with linked resources."""
        # Create test user and resources
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        resume = Resume(
            id=1,
            user_id=1,
            title="Software Engineer Resume",
            raw_text="Resume text"
        )
        db.add(user)
        db.add(job_description)
        db.add(resume)
        
        # Create application
        app = Application(
            user_id=1,
            company="Tech Corp",
            position_title="Software Engineer",
            status=ApplicationStatus.PLANNED,
            job_description_id=1
        )
        db.add(app)
        db.commit()
        
        # Update application with linked resume
        update_data = {
            "resume_id": 1,
            "status": "applied"
        }
        
        response = client.put(f"{self.base_url}/{app.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["resume_id"] == 1
        assert data["status"] == ApplicationStatus.APPLIED

    def test_application_validation_rules(self, client: TestClient, db: Session):
        """Test application validation rules."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(user)
        db.add(job_description)
        db.commit()
        
        # Test invalid priority
        invalid_priority = {
            **self.sample_application,
            "priority": "invalid"
        }
        
        response = client.post(f"{self.base_url}/", json=invalid_priority)
        assert response.status_code == 422
        
        # Test invalid employment type length
        invalid_employment = {
            **self.sample_application,
            "employment_type": "a" * 51  # Too long
        }
        
        response = client.post(f"{self.base_url}/", json=invalid_employment)
        assert response.status_code == 422
        
        # Test negative salary
        invalid_salary = {
            **self.sample_application,
            "salary_min": -1000
        }
        
        response = client.post(f"{self.base_url}/", json=invalid_salary)
        assert response.status_code == 422

    def test_application_date_fields(self, client: TestClient, db: Session):
        """Test application date fields."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(user)
        db.add(job_description)
        
        # Create application with dates
        application_data = {
            **self.sample_application,
            "planned_date": datetime(2023, 1, 15),
            "applied_date": datetime(2023, 1, 20),
            "interview_date": datetime(2023, 2, 1)
        }
        
        response = client.post(f"{self.base_url}/", json=application_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["planned_date"] == "2023-01-15T00:00:00"
        assert data["applied_date"] == "2023-01-20T00:00:00"
        assert data["interview_date"] == "2023-02-01T00:00:00"

    def test_application_tags_field(self, client: TestClient, db: Session):
        """Test application tags field."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(user)
        db.add(job_description)
        
        # Create application with tags
        application_data = {
            **self.sample_application,
            "tags": ["python", "django", "backend", "remote"]
        }
        
        response = client.post(f"{self.base_url}/", json=application_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["tags"] == ["python", "django", "backend", "remote"]

    def test_application_search_functionality(self, client: TestClient, db: Session):
        """Test application search functionality."""
        # Create test user and job description
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        job_description = JobDescription(
            id=1,
            user_id=1,
            job_title="Software Engineer",
            company="Tech Corp",
            raw_text="Job description text"
        )
        db.add(user)
        db.add(job_description)
        
        # Create applications
        app1 = Application(
            user_id=1,
            company="Tech Corp",
            position_title="Software Engineer",
            notes="Python and Django experience",
            job_description_id=1
        )
        app2 = Application(
            user_id=1,
            company="Data Corp",
            position_title="Data Scientist",
            notes="Machine learning background",
            job_description_id=1
        )
        db.add(app1)
        db.add(app2)
        db.commit()
        
        # Test search in company
        response = client.get(f"{self.base_url}/?search=Tech")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["company"] == "Tech Corp"
        
        # Test search in position title
        response = client.get(f"{self.base_url}/?search=Engineer")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "Engineer" in data[0]["position_title"]
        
        # Test search in notes
        response = client.get(f"{self.base_url}/search=Python")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "Python" in data[0]["notes"]


if __name__ == "__main__":
    pytest.main([__file__])
