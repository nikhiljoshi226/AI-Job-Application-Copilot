import pytest
from app.services.resume_parser import ResumeParser
from app.services.truth_bank import TruthBank


class TestResumeParser:
    
    def setup_method(self):
        """Setup test fixtures."""
        self.parser = ResumeParser()
        self.truth_bank = TruthBank()
    
    def test_parse_simple_resume(self):
        """Test parsing a simple resume with basic structure."""
        resume_text = """
        Email: john.doe@example.com
        Phone: +1-555-0123
        Summary: Software engineer with 5 years of experience in Python and JavaScript
        Skills: Python, JavaScript, React, Docker, PostgreSQL, Communication, Leadership
        Experience: Title: Senior Software Engineer, Company: Tech Corp, Location: San Francisco, CA, Dates: 2021-01-15 - 2023-03-15, Current: false, Description: Led development of scalable web applications, Achievements: Improved application performance by 40%, Led team of 5 engineers, Technologies: Python, Django, PostgreSQL, Redis, Docker
        Education: Degree: Bachelor of Science, Field: Computer Science, University: University of California, Berkeley, Location: Berkeley, CA, Dates: 2014-09-01 - 2018-05-31, GPA: 3.8
        """
        
        result = self.parser.parse_resume(resume_text)
        
        # Test personal info
        assert result["personal_info"]["email"] == "john.doe@example.com"
        assert result["personal_info"]["phone"] == "+1-555-0123"
        
        # Test summary
        assert "Software engineer with 5 years of experience" in result["summary"]
        
        # Test skills
        assert len(result["skills"]["technical"]) > 0
        assert len(result["skills"]["soft_skills"]) > 0
        
        # Test experience
        assert len(result["experience"]) == 1
        experience = result["experience"][0]
        assert experience["title"] == "Senior Software Engineer"
        assert experience["company"] == "Tech Corp"
        assert experience["location"] == "San Francisco, CA"
        assert experience["current"] == False
        assert "Improved application performance by 40%" in experience["achievements"]
        
        # Test education
        assert len(result["education"]) == 1
        education = result["education"][0]
        assert education["degree"] == "Bachelor of Science"
        assert education["field"] == "Computer Science"
        assert education["university"] == "University of California, Berkeley"
        assert education["gpa"] == "3.8"
        
        # Test metadata
        assert result["metadata"]["total_years_experience"] >= 2
        assert result["metadata"]["education_level"] == "bachelor"
    
    def test_parse_resume_with_certifications(self):
        """Test parsing resume with certifications."""
        resume_text = """
        Email: jane.smith@example.com
        Summary: Cloud architect with AWS expertise
        Skills: AWS, Docker, Kubernetes, Leadership
        Experience: Title: Cloud Architect, Company: Cloud Solutions Inc, Dates: 2020-06-01 - 2023-01-15, Current: true
        Education: Degree: Master of Science, Field: Cloud Computing, University: Stanford University, Dates: 2018-09-01 - 2020-05-31
        Certifications: Name: AWS Certified Solutions Architect, Issuer: Amazon Web Services, Date: 2022-06-15, Expires: 2025-06-15, ID: AWS-SAA-123456
        Projects: Name: Cloud Migration Platform, Technologies: AWS, Terraform, Docker, Dates: 2021-01-01 - 2021-12-31, URL: https://cloud-platform.com, Achievements: Migrated 50+ applications to cloud, Reduced infrastructure costs by 30%
        """
        
        result = self.parser.parse_resume(resume_text)
        
        # Test certifications
        assert len(result["certifications"]) == 1
        cert = result["certifications"][0]
        assert cert["name"] == "AWS Certified Solutions Architect"
        assert cert["issuer"] == "Amazon Web Services"
        assert cert["date"] == "2022-06-15"
        assert cert["expiry_date"] == "2025-06-15"
        assert cert["credential_id"] == "AWS-SAA-123456"
        
        # Test projects
        assert len(result["projects"]) == 1
        project = result["projects"][0]
        assert project["name"] == "Cloud Migration Platform"
        assert "AWS" in project["technologies"]
        assert "Migrated 50+ applications to cloud" in project["achievements"]
        
        # Test metadata
        assert result["metadata"]["certifications_count"] == 1
        assert result["metadata"]["projects_count"] == 1
    
    def test_parse_resume_with_languages(self):
        """Test parsing resume with languages."""
        resume_text = """
        Email: carlos.garcia@example.com
        Summary: Bilingual software developer
        Skills: Python, Java, Communication
        Experience: Title: Software Developer, Company: Global Tech, Dates: 2019-03-01 - 2023-01-15
        Languages: Language: English, Proficiency: Native
        Languages: Language: Spanish, Proficiency: Professional
        """
        
        result = self.parser.parse_resume(resume_text)
        
        # Test languages
        assert len(result["languages"]) == 2
        languages = result["languages"]
        
        english_lang = next((lang for lang in languages if lang["language"] == "English"), None)
        assert english_lang is not None
        assert english_lang["proficiency"] == "native"
        
        spanish_lang = next((lang for lang in languages if lang["language"] == "Spanish"), None)
        assert spanish_lang is not None
        assert spanish_lang["proficiency"] == "professional"
    
    def test_parse_empty_resume(self):
        """Test parsing empty resume."""
        result = self.parser.parse_resume("")
        
        # Should return empty structure
        assert result["personal_info"] == {}
        assert result["summary"] == ""
        assert result["skills"]["technical"] == []
        assert result["skills"]["soft_skills"] == []
        assert result["experience"] == []
        assert result["education"] == []
        assert result["certifications"] == []
        assert result["projects"] == []
        assert result["languages"] == []
    
    def test_parse_malformed_resume(self):
        """Test parsing malformed resume."""
        resume_text = """
        Invalid: This is not a valid section
        Random text without proper structure
        Some more random content
        """
        
        result = self.parser.parse_resume(resume_text)
        
        # Should handle gracefully and return empty structure
        assert result["personal_info"] == {}
        assert result["summary"] == ""
        assert result["experience"] == []
    
    def test_skill_categorization(self):
        """Test skill categorization logic."""
        # Test technical skills
        technical_skills = self.parser._parse_skills("Python, JavaScript, React, Docker, PostgreSQL")
        assert len(technical_skills) > 0
        
        # Check if skills are properly categorized
        python_skill = next((skill for skill in technical_skills if skill["name"].lower() == "python"), None)
        assert python_skill is not None
        assert python_skill["level"] in ["beginner", "intermediate", "advanced"]
        
        # Test technical skill detection
        assert self.parser._is_technical_skill("python") == True
        assert self.parser._is_technical_skill("react") == True
        assert self.parser._is_technical_skill("communication") == False
    
    def test_experience_parsing(self):
        """Test experience section parsing."""
        experience_text = """
        Title: Senior Software Engineer
        Company: Tech Corp
        Location: San Francisco, CA
        Dates: 2021-01-15 - 2023-03-15
        Current: false
        Description: Led development of scalable web applications
        Achievements: Improved application performance by 40%, Led team of 5 engineers
        Technologies: Python, Django, PostgreSQL, Redis, Docker
        """
        
        result = self.parser._parse_experience(experience_text)
        
        assert result["title"] == "Senior Software Engineer"
        assert result["company"] == "Tech Corp"
        assert result["location"] == "San Francisco, CA"
        assert result["start_date"] == "2021-01-15"
        assert result["end_date"] == "2023-03-15"
        assert result["current"] == False
        assert "scalable web applications" in result["description"]
        assert "Improved application performance by 40%" in result["achievements"]
        assert "Python" in result["technologies"]
    
    def test_education_parsing(self):
        """Test education section parsing."""
        education_text = """
        Degree: Bachelor of Science
        Field: Computer Science
        University: University of California, Berkeley
        Location: Berkeley, CA
        Dates: 2014-09-01 - 2018-05-31
        GPA: 3.8
        """
        
        result = self.parser._parse_education(education_text)
        
        assert result["degree"] == "Bachelor of Science"
        assert result["field"] == "Computer Science"
        assert result["university"] == "University of California, Berkeley"
        assert result["location"] == "Berkeley, CA"
        assert result["start_date"] == "2014-09-01"
        assert result["end_date"] == "2018-05-31"
        assert result["gpa"] == "3.8"
    
    def test_certification_parsing(self):
        """Test certification parsing."""
        cert_text = """
        Name: AWS Certified Solutions Architect
        Issuer: Amazon Web Services
        Date: 2022-06-15
        Expires: 2025-06-15
        ID: AWS-SAA-123456
        """
        
        result = self.parser._parse_certification(cert_text)
        
        assert result["name"] == "AWS Certified Solutions Architect"
        assert result["issuer"] == "Amazon Web Services"
        assert result["date"] == "2022-06-15"
        assert result["expiry_date"] == "2025-06-15"
        assert result["credential_id"] == "AWS-SAA-123456"
    
    def test_project_parsing(self):
        """Test project parsing."""
        project_text = """
        Name: E-commerce Platform
        Description: Built a full-stack e-commerce platform
        Technologies: React, Node.js, MongoDB, Docker
        Dates: 2022-01-01 - 2022-06-30
        URL: https://project-demo.com
        Achievements: Handled 10,000+ concurrent users, Reduced page load time by 50%
        """
        
        result = self.parser._parse_project(project_text)
        
        assert result["name"] == "E-commerce Platform"
        assert "full-stack e-commerce platform" in result["description"]
        assert "React" in result["technologies"]
        assert result["start_date"] == "2022-01-01"
        assert result["end_date"] == "2022-06-30"
        assert result["url"] == "https://project-demo.com"
        assert "10,000+ concurrent users" in result["achievements"]
    
    def test_years_experience_calculation(self):
        """Test years of experience calculation."""
        # Test with years mentioned
        years = self.parser._estimate_experience("python", "5 years of python experience")
        assert years == 5
        
        # Test with months mentioned
        years = self.parser._estimate_experience("javascript", "24 months of javascript")
        assert years == 2
        
        # Test with no time mentioned
        years = self.parser._estimate_experience("react", "react development")
        assert years == 2  # Default
    
    def test_metadata_calculation(self):
        """Test metadata calculation."""
        parsed_data = {
            "experience": [
                {"start_date": "2021-01-15", "end_date": "2023-03-15"}
            ],
            "education": [
                {"degree": "Bachelor of Science"}
            ],
            "certifications": [
                {"name": "AWS Certified Solutions Architect"}
            ],
            "projects": [
                {"name": "Project 1"}
            ],
            "skills": {
                "technical": [{"name": "Python"}, {"name": "JavaScript"}],
                "soft_skills": [{"name": "Communication"}]
            }
        }
        
        metadata = self.parser._calculate_metadata(parsed_data)
        
        assert metadata["total_years_experience"] >= 2
        assert metadata["education_level"] == "bachelor"
        assert metadata["certifications_count"] == 1
        assert metadata["projects_count"] == 1
        assert metadata["technical_skills_count"] == 2
        assert metadata["soft_skills_count"] == 1
        assert "last_updated" in metadata


class TestTruthBank:
    
    def setup_method(self):
        """Setup test fixtures."""
        self.parser = ResumeParser()
        self.truth_bank = TruthBank()
    
    def test_create_truth_bank_complete(self):
        """Test creating truth bank from complete parsed resume."""
        parsed_resume = {
            "personal_info": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-0123",
                "location": "San Francisco, CA",
                "linkedin": "https://linkedin.com/in/johndoe",
                "portfolio": "https://johndoe.dev"
            },
            "summary": "Software engineer with 5 years of experience",
            "skills": {
                "technical": [
                    {"name": "Python", "level": "advanced", "years_of_experience": 5}
                ],
                "soft_skills": [
                    {"name": "Communication", "level": "strong"}
                ]
            },
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "start_date": "2021-01-15",
                    "end_date": "2023-03-15",
                    "current": False,
                    "achievements": ["Improved application performance by 40%"],
                    "technologies": ["Python", "Django"]
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "university": "University of California, Berkeley",
                    "end_date": "2018-05-31"
                }
            ],
            "certifications": [
                {
                    "name": "AWS Certified Solutions Architect",
                    "issuer": "Amazon Web Services",
                    "date": "2022-06-15"
                }
            ],
            "projects": [
                {
                    "name": "E-commerce Platform",
                    "technologies": ["React", "Node.js"],
                    "achievements": ["Handled 10,000+ concurrent users"]
                }
            ],
            "metadata": {
                "total_years_experience": 5,
                "last_updated": "2026-04-02T22:19:00Z"
            }
        }
        
        truth_bank = self.truth_bank.create_truth_bank(parsed_resume)
        
        # Test personal facts
        assert truth_bank["personal_facts"]["name"] == "John Doe"
        assert truth_bank["personal_facts"]["contact_info"]["email"] == "john.doe@example.com"
        assert truth_bank["personal_facts"]["professional_links"]["linkedin"] == "https://linkedin.com/in/johndoe"
        
        # Test professional facts
        assert truth_bank["professional_facts"]["total_years_experience"] == 5
        assert truth_bank["professional_facts"]["current_role"] == "Senior Software Engineer"
        assert truth_bank["professional_facts"]["current_company"] == "Tech Corp"
        assert truth_bank["professional_facts"]["career_level"] == "Senior"
        
        # Test education facts
        assert truth_bank["education_facts"]["highest_degree"] == "Bachelor of Science"
        assert truth_bank["education_facts"]["field_of_study"] == "Computer Science"
        assert truth_bank["education_facts"]["university"] == "University of California, Berkeley"
        assert truth_bank["education_facts"]["certifications_count"] == 1
        
        # Test skill facts
        assert len(truth_bank["skill_facts"]["verified_technical_skills"]) == 1
        assert len(truth_bank["skill_facts"]["verified_soft_skills"]) == 1
        assert truth_bank["skill_facts"]["verified_technical_skills"][0]["skill"] == "Python"
        assert truth_bank["skill_facts"]["verified_technical_skills"][0]["years_experience"] == 5
        
        # Test experience facts
        assert len(truth_bank["experience_facts"]["companies_worked"]) == 1
        assert truth_bank["experience_facts"]["companies_worked"][0]["company"] == "Tech Corp"
        
        # Test achievement facts
        assert len(truth_bank["achievement_facts"]["quantifiable_achievements"]) == 1
        assert "40%" in truth_bank["achievement_facts"]["quantifiable_achievements"][0]["metric"]
        
        # Test project facts
        assert len(truth_bank["project_facts"]["completed_projects"]) == 1
        assert truth_bank["project_facts"]["completed_projects"][0]["name"] == "E-commerce Platform"
        
        # Test metadata
        assert truth_bank["metadata"]["total_facts"] > 0
        assert truth_bank["metadata"]["confidence_score"] >= 0.8
        assert truth_bank["metadata"]["verification_status"] == "high_confidence"
    
    def test_create_truth_bank_minimal(self):
        """Test creating truth bank from minimal parsed resume."""
        parsed_resume = {
            "personal_info": {
                "name": "Jane Smith",
                "email": "jane.smith@example.com"
            },
            "skills": {
                "technical": [],
                "soft_skills": []
            },
            "experience": [],
            "education": [],
            "certifications": [],
            "projects": [],
            "metadata": {
                "total_years_experience": 0,
                "last_updated": "2026-04-02T22:19:00Z"
            }
        }
        
        truth_bank = self.truth_bank.create_truth_bank(parsed_resume)
        
        # Should still create structure with default values
        assert truth_bank["personal_facts"]["name"] == "Jane Smith"
        assert truth_bank["professional_facts"]["total_years_experience"] == 0
        assert truth_bank["education_facts"]["highest_degree"] == "Unknown"
        assert truth_bank["skill_facts"]["verified_technical_skills"] == []
        assert truth_bank["experience_facts"]["companies_worked"] == []
        assert truth_bank["metadata"]["confidence_score"] < 0.8
        assert truth_bank["metadata"]["verification_status"] != "high_confidence"
    
    def test_metric_extraction(self):
        """Test metric extraction from achievements."""
        # Test percentage extraction
        metric = self.truth_bank._extract_metric("Improved performance by 40%")
        assert metric == "40%"
        
        # Test number extraction
        metric = self.truth_bank._extract_metric("Managed team of 5 people")
        assert metric == "5 people"
        
        # Test user count extraction
        metric = self.truth_bank._extract_metric("Handled 10,000 concurrent users")
        assert metric == "10,000 concurrent users"
        
        # Test fallback to full text
        metric = self.truth_bank._extract_metric("General achievement statement")
        assert metric == "General achievement statement"
    
    def test_team_size_extraction(self):
        """Test team size extraction from achievements."""
        # Test "team of X" pattern
        team_size = self.truth_bank._extract_team_size("Led team of 5 engineers")
        assert team_size == 5
        
        # Test "managed X" pattern
        team_size = self.truth_bank._extract_team_size("Managed 3 developers")
        assert team_size == 3
        
        # Test "led X" pattern
        team_size = self.truth_bank._extract_team_size("Led 2 junior developers")
        assert team_size == 2
        
        # Test no team size found
        team_size = self.truth_bank._extract_team_size("Improved performance significantly")
        assert team_size == 0
    
    def test_year_extraction(self):
        """Test year extraction from date strings."""
        year = self.truth_bank._extract_year("2018-05-31")
        assert year == 2018
        
        year = self.truth_bank._extract_year("05/31/2018")
        assert year == 2018
        
        year = self.truth_bank._extract_year("No date here")
        assert year is None


if __name__ == "__main__":
    pytest.main([__file__])
