import pytest
from app.services.job_description_parser import JobDescriptionParser


class TestJobDescriptionParser:
    
    def setup_method(self):
        """Setup test fixtures."""
        self.parser = JobDescriptionParser()
    
    def test_parse_tech_company_job_description(self):
        """Test parsing a typical tech company job description."""
        job_title = "Senior Software Engineer"
        company = "TechCorp"
        jd_text = """
        We are looking for a Senior Software Engineer to join our growing team. 
        This is a full-time, hybrid position in San Francisco, CA.
        
        Requirements:
        • 5+ years of Python experience
        • Strong knowledge of Django and PostgreSQL
        • Experience with AWS and Docker
        • Bachelor's degree in Computer Science
        
        Responsibilities:
        • Design and develop scalable software solutions
        • Lead code reviews and mentor junior developers
        • Collaborate with cross-functional teams
        
        Preferred Skills:
        • Kubernetes experience is a plus
        • Knowledge of React and frontend development
        
        We offer competitive salary ($120k-$180k) and great benefits including health insurance, 401k, and unlimited PTO.
        """
        
        result = self.parser.parse_job_description(job_title, company, jd_text)
        
        # Test basic structure
        assert result["job_title"] == "Senior Software Engineer"
        assert result["company"] == "TechCorp"
        assert "parsed_content" in result
        assert "metadata" in result
        
        # Test summary extraction
        summary = result["parsed_content"]["summary"]
        assert "Senior Software Engineer" in summary
        assert "growing team" in summary
        
        # Test required skills
        required_skills = result["parsed_content"]["required_skills"]
        assert len(required_skills) > 0
        
        python_skill = next((skill for skill in required_skills if skill["skill"].lower() == "python"), None)
        assert python_skill is not None
        assert python_skill["category"] == "technical"
        assert python_skill["skill_type"] == "required"
        assert "5+ years" in python_skill["experience_level"]
        
        # Test preferred skills
        preferred_skills = result["parsed_content"]["preferred_skills"]
        kubernetes_skill = next((skill for skill in preferred_skills if skill["skill"].lower() == "kubernetes"), None)
        assert kubernetes_skill is not None
        assert kubernetes_skill["skill_type"] == "preferred"
        
        # Test responsibilities
        responsibilities = result["parsed_content"]["responsibilities"]
        assert len(responsibilities) > 0
        assert any("Design and develop" in resp for resp in responsibilities)
        
        # Test qualifications
        qualifications = result["parsed_content"]["qualifications"]
        assert len(qualifications) > 0
        assert any("Bachelor's degree" in qual for qual in qualifications)
        
        # Test role type
        role_type = result["parsed_content"]["role_type"]
        assert role_type["employment_type"] == "full_time"
        assert role_type["work_arrangement"] == "hybrid"
        assert role_type["experience_level"] == "senior"
        
        # Test compensation
        compensation = result["parsed_content"]["compensation"]
        assert compensation["salary_min"] == 120000
        assert compensation["salary_max"] == 180000
        assert compensation["currency"] == "USD"
        assert "health insurance" in compensation["benefits"]
        
        # Test location
        location = result["parsed_content"]["location"]
        assert location["city"] == "San Francisco"
        assert location["state"] == "CA"
        assert location["remote_policy"] == "hybrid"
        
        # Test metadata
        metadata = result["metadata"]
        assert metadata["total_skills"] > 0
        assert metadata["required_skills_count"] > 0
        assert metadata["preferred_skills_count"] > 0
        assert metadata["parsing_confidence"] > 0.5
    
    def test_parse_startup_job_description(self):
        """Test parsing a startup job description with different style."""
        job_title = "Full Stack Developer"
        company = "StartupXYZ"
        jd_text = """
        About the Role:
        We're seeking a talented Full Stack Developer to help build our SaaS platform. 
        This is a remote, contract position for 6 months with potential for full-time.
        
        What you'll do:
        - Build new features using React and Node.js
        - Work with MongoDB and PostgreSQL databases
        - Implement RESTful APIs and microservices
        - Collaborate with our small, agile team
        
        Must have:
        - 3+ years of JavaScript/TypeScript experience
        - React and Node.js proficiency
        - Experience with cloud platforms (AWS preferred)
        
        Nice to have:
        - Python/Django experience
        - Docker and Kubernetes knowledge
        - Previous startup experience
        
        We're in the fintech space, revolutionizing how small businesses manage their finances.
        Salary: $90k-$130k depending on experience.
        """
        
        result = self.parser.parse_job_description(job_title, company, jd_text)
        
        # Test role type
        role_type = result["parsed_content"]["role_type"]
        assert role_type["employment_type"] == "contract"
        assert role_type["work_arrangement"] == "remote"
        assert role_type["experience_level"] == "mid"
        
        # Test required skills
        required_skills = result["parsed_content"]["required_skills"]
        javascript_skill = next((skill for skill in required_skills if skill["skill"].lower() == "javascript"), None)
        assert javascript_skill is not None
        assert javascript_skill["experience_level"] == "3+ years"
        
        # Test domain clues
        domain_clues = result["parsed_content"]["domain_clues"]
        fintech_domain = next((domain for domain in domain_clues if domain["domain"] == "fintech"), None)
        assert fintech_domain is not None
        assert fintech_domain["confidence"] == 0.8
        
        # Test compensation
        compensation = result["parsed_content"]["compensation"]
        assert compensation["salary_min"] == 90000
        assert compensation["salary_max"] == 130000
    
    def test_parse_enterprise_job_description(self):
        """Test parsing an enterprise job description with formal structure."""
        job_title = "Data Scientist"
        company = "EnterpriseCorp"
        jd_text = """
        JOB SUMMARY
        
        Enterprise Corporation is seeking a Data Scientist to join our Analytics team.
        This is a full-time, on-site position at our headquarters in New York, NY.
        
        ESSENTIAL FUNCTIONS AND RESPONSIBILITIES
        
        1. Develop machine learning models using Python and TensorFlow
        2. Analyze large datasets using pandas and SQL
        3. Create data visualizations and reports for stakeholders
        4. Collaborate with business teams to identify data-driven insights
        
        QUALIFICATIONS
        
        Required:
        - Master's degree in Data Science, Computer Science, or related field
        - 2+ years of experience in data science or analytics
        - Strong programming skills in Python
        - Experience with machine learning frameworks
        
        Preferred:
        - PhD in relevant field
        - Experience with big data technologies (Spark, Hadoop)
        - Knowledge of cloud platforms (Azure, AWS, GCP)
        
        BENEFITS
        
        We offer a comprehensive benefits package including medical, dental, vision insurance,
        401(k) with company match, and generous PTO. Salary range: $110,000-$160,000.
        """
        
        result = self.parser.parse_job_description(job_title, company, jd_text)
        
        # Test role type
        role_type = result["parsed_content"]["role_type"]
        assert role_type["employment_type"] == "full_time"
        assert role_type["work_arrangement"] == "on-site"
        assert role_type["experience_level"] == "mid"
        
        # Test location
        location = result["parsed_content"]["location"]
        assert location["city"] == "New York"
        assert location["state"] == "NY"
        assert location["remote_policy"] == "on-site"
        
        # Test qualifications
        qualifications = result["parsed_content"]["qualifications"]
        master_degree = next((qual for qual in qualifications if "Master's degree" in qual), None)
        assert master_degree is not None
        
        # Test required skills
        required_skills = result["parsed_content"]["required_skills"]
        python_skill = next((skill for skill in required_skills if skill["skill"].lower() == "python"), None)
        assert python_skill is not None
        
        # Test preferred skills
        preferred_skills = result["parsed_content"]["preferred_skills"]
        spark_skill = next((skill for skill in preferred_skills if skill["skill"].lower() == "spark"), None)
        assert spark_skill is not None
    
    def test_parse_minimal_job_description(self):
        """Test parsing a minimal job description."""
        job_title = "Junior Developer"
        company = "SmallCo"
        jd_text = """
        Looking for a junior developer. Must know Python and have some experience with web development.
        This is a part-time position. Contact us for more details.
        """
        
        result = self.parser.parse_job_description(job_title, company, jd_text)
        
        # Test basic structure
        assert result["job_title"] == "Junior Developer"
        assert result["company"] == "SmallCo"
        
        # Test role type
        role_type = result["parsed_content"]["role_type"]
        assert role_type["employment_type"] == "part_time"
        assert role_type["experience_level"] == "entry"
        
        # Test skills extraction
        required_skills = result["parsed_content"]["required_skills"]
        python_skill = next((skill for skill in required_skills if skill["skill"].lower() == "python"), None)
        assert python_skill is not None
        
        # Test metadata
        metadata = result["metadata"]
        assert metadata["parsing_confidence"] < 0.8  # Should be lower confidence for minimal JD
    
    def test_extract_summary(self):
        """Test summary extraction."""
        jd_text = """
        We are looking for a Senior Software Engineer to join our growing team.
        This is a full-time position with great benefits and competitive salary.
        
        Requirements:
        • 5+ years of experience
        • Strong programming skills
        """
        
        summary = self.parser._extract_summary(jd_text)
        assert "Senior Software Engineer" in summary
        assert "growing team" in summary
        assert len(summary) <= 500
    
    def test_extract_required_skills(self):
        """Test required skills extraction."""
        jd_text = """
        Requirements:
        • 5+ years of Python experience
        • Strong knowledge of Django and PostgreSQL
        • Experience with AWS and Docker
        • Bachelor's degree in Computer Science
        
        Preferred Skills:
        • Kubernetes experience is a plus
        """
        
        required_skills = self.parser._extract_required_skills(jd_text)
        assert len(required_skills) > 0
        
        python_skill = next((skill for skill in required_skills if skill["skill"].lower() == "python"), None)
        assert python_skill is not None
        assert python_skill["skill_type"] == "required"
        assert "5+ years" in python_skill["experience_level"]
    
    def test_extract_preferred_skills(self):
        """Test preferred skills extraction."""
        jd_text = """
        Requirements:
        • 5+ years of Python experience
        
        Preferred Skills:
        • Kubernetes experience is a plus
        • Knowledge of React and frontend development
        • Nice to have: AWS experience
        """
        
        preferred_skills = self.parser._extract_preferred_skills(jd_text)
        assert len(preferred_skills) > 0
        
        kubernetes_skill = next((skill for skill in preferred_skills if skill["skill"].lower() == "kubernetes"), None)
        assert kubernetes_skill is not None
        assert kubernetes_skill["skill_type"] == "preferred"
    
    def test_extract_responsibilities(self):
        """Test responsibilities extraction."""
        jd_text = """
        Responsibilities:
        • Design and develop scalable software solutions
        • Lead code reviews and mentor junior developers
        • Collaborate with cross-functional teams
        • Write clean, maintainable code
        """
        
        responsibilities = self.parser._extract_responsibilities(jd_text)
        assert len(responsibilities) > 0
        assert any("Design and develop" in resp for resp in responsibilities)
        assert any("Lead code reviews" in resp for resp in responsibilities)
    
    def test_extract_qualifications(self):
        """Test qualifications extraction."""
        jd_text = """
        Qualifications:
        • Bachelor's degree in Computer Science or related field
        • 5+ years of software development experience
        • Strong problem-solving skills
        • Excellent communication abilities
        """
        
        qualifications = self.parser._extract_qualifications(jd_text)
        assert len(qualifications) > 0
        assert any("Bachelor's degree" in qual for qual in qualifications)
        assert any("5+ years" in qual for qual in qualifications)
    
    def test_extract_keywords(self):
        """Test keywords extraction."""
        jd_text = """
        We need a Python developer with experience in Django, PostgreSQL, AWS, and Docker.
        Must have strong communication skills and be able to work in an agile environment.
        Experience with React and frontend development is a plus.
        """
        
        keywords = self.parser._extract_keywords(jd_text)
        assert "python" in keywords
        assert "django" in keywords
        assert "postgresql" in keywords
        assert "aws" in keywords
        assert "docker" in keywords
        assert "communication" in keywords
        assert "agile" in keywords
        assert "react" in keywords
    
    def test_extract_role_type(self):
        """Test role type extraction."""
        jd_text = """
        This is a full-time, remote position for a senior developer.
        We offer flexible working hours and hybrid options.
        """
        
        role_type = self.parser._extract_role_type(jd_text)
        assert role_type["employment_type"] == "full_time"
        assert role_type["work_arrangement"] == "remote"
        assert role_type["experience_level"] == "senior"
    
    def test_extract_compensation(self):
        """Test compensation extraction."""
        jd_text = """
        Salary: $120,000 - $180,000 per year.
        We offer great benefits including health insurance, 401k, and unlimited PTO.
        """
        
        compensation = self.parser._extract_compensation(jd_text)
        assert compensation["salary_min"] == 120000
        assert compensation["salary_max"] == 180000
        assert compensation["currency"] == "USD"
        assert "health insurance" in compensation["benefits"]
        assert "401k" in compensation["benefits"]
    
    def test_extract_location(self):
        """Test location extraction."""
        jd_text = """
        Position is located in San Francisco, CA.
        This is a hybrid role with 3 days in office.
        """
        
        location = self.parser._extract_location(jd_text)
        assert location["city"] == "San Francisco"
        assert location["state"] == "CA"
        assert location["remote_policy"] == "hybrid"
    
    def test_extract_experience_level(self):
        """Test experience level extraction."""
        # Test years of experience
        level = self.parser._extract_experience_level("5+ years of Python experience")
        assert level == "5+ years"
        
        level = self.parser._extract_experience_level("3 years of experience")
        assert level == "3+ years"
        
        # Test level indicators
        level = self.parser._extract_experience_level("Senior developer position")
        assert level == "senior level"
        
        level = self.parser._extract_experience_level("Junior developer role")
        assert level == "junior level"
        
        # Test no experience mentioned
        level = self.parser._extract_experience_level("Python development skills")
        assert level == "not specified"
    
    def test_extract_skills_from_line(self):
        """Test skill extraction from a single line."""
        line = "Experience with Python, Django, PostgreSQL, and AWS required"
        skills = self.parser._extract_skills_from_line(line, "required")
        
        assert len(skills) > 0
        
        python_skill = next((skill for skill in skills if skill["skill"].lower() == "python"), None)
        assert python_skill is not None
        assert python_skill["category"] == "technical"
        assert python_skill["skill_type"] == "required"
    
    def test_calculate_confidence(self):
        """Test confidence calculation."""
        parsed_content = {
            "required_skills": [{"skill": "Python"}],
            "responsibilities": ["Develop software"],
            "qualifications": ["Bachelor's degree"],
            "keywords": ["python", "django"],
            "role_type": {"experience_level": "mid"}
        }
        
        confidence = self.parser._calculate_confidence(parsed_content)
        assert confidence == 1.0  # All sections present
        
        # Test with missing sections
        parsed_content = {
            "required_skills": [],
            "responsibilities": [],
            "qualifications": [],
            "keywords": [],
            "role_type": {"experience_level": "unknown"}
        }
        
        confidence = self.parser._calculate_confidence(parsed_content)
        assert confidence == 0.0  # No confidence
    
    def test_validate_parsed_data(self):
        """Test parsed data validation."""
        # Test valid data
        valid_data = {
            "job_title": "Software Engineer",
            "company": "TechCorp",
            "parsed_content": {
                "required_skills": [{"skill": "Python"}],
                "responsibilities": ["Develop software"],
                "keywords": ["python"]
            },
            "metadata": {"parsing_confidence": 0.8}
        }
        
        validation = self.parser.validate_parsed_data(valid_data)
        assert validation["is_valid"] == True
        assert len(validation["errors"]) == 0
        
        # Test invalid data
        invalid_data = {
            "job_title": "",  # Missing
            "company": "",     # Missing
            "parsed_content": {
                "required_skills": [],
                "responsibilities": [],
                "keywords": []
            },
            "metadata": {"parsing_confidence": 0.3}
        }
        
        validation = self.parser.validate_parsed_data(invalid_data)
        assert validation["is_valid"] == False
        assert len(validation["errors"]) > 0
        assert len(validation["warnings"]) > 0
    
    def test_extract_domain_clues(self):
        """Test domain clues extraction."""
        jd_text = """
        We are a fintech startup revolutionizing how small businesses manage their finances.
        Our SaaS platform serves customers in the e-commerce and retail sectors.
        """
        
        domain_clues = self.parser._extract_domain_clues(jd_text)
        assert len(domain_clues) > 0
        
        fintech_domain = next((domain for domain in domain_clues if domain["domain"] == "fintech"), None)
        assert fintech_domain is not None
        assert fintech_domain["confidence"] == 0.8
        
        saas_domain = next((domain for domain in domain_clues if domain["domain"] == "saas"), None)
        assert saas_domain is not None
        
        ecommerce_domain = next((domain for domain in domain_clues if domain["domain"] == "e-commerce"), None)
        assert ecommerce_domain is not None


if __name__ == "__main__":
    pytest.main([__file__])
