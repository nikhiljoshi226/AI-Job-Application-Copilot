import pytest
from app.services.cover_letter_generator import CoverLetterGenerator


class TestCoverLetterGenerator:
    
    def setup_method(self):
        """Setup test fixtures."""
        self.generator = CoverLetterGenerator()
        
        # Sample tailored resume data
        self.tailored_resume_data = {
            "rendering_data": {
                "header": {
                    "name": "John Doe",
                    "contact": {
                        "email": "john@example.com",
                        "phone": "555-1234",
                        "location": "New York, NY",
                        "linkedin": "linkedin.com/in/johndoe",
                        "github": "github.com/johndoe"
                    }
                },
                "summary": {
                    "title": "Professional Summary",
                    "content": "Senior Software Engineer with 5 years of experience in full-stack development"
                },
                "skills": {
                    "title": "Skills",
                    "categories": [
                        {
                            "name": "Technical Skills",
                            "skills": [
                                {"name": "Python", "level": "5 years", "highlight": False},
                                {"name": "Django", "level": "3 years", "highlight": True},
                                {"name": "React", "level": "3 years", "highlight": False}
                            ]
                        },
                        {
                            "name": "Soft Skills",
                            "skills": [
                                {"name": "Communication", "level": "Strong", "highlight": False},
                                {"name": "Leadership", "level": "Strong", "highlight": False}
                            ]
                        }
                    ]
                },
                "experience": {
                    "title": "Professional Experience",
                    "entries": [
                        {
                            "title": "Software Engineer",
                            "company": "Tech Corp",
                            "location": "San Francisco, CA",
                            "dates": "January 2021 - March 2023",
                            "description": "Developed scalable web applications",
                            "achievements": [
                                "Improved application performance by 40%",
                                "Led team of 3 junior developers"
                            ],
                            "technologies": ["Python", "Django", "React", "PostgreSQL"]
                        }
                    ]
                },
                "education": {
                    "title": "Education",
                    "entries": [
                        {
                            "degree": "Bachelor of Science",
                            "major": "Computer Science",
                            "university": "State University",
                            "location": "Boston, MA",
                            "graduation_year": "2020",
                            "gpa": "3.8"
                        }
                    ]
                },
                "projects": {
                    "title": "Projects",
                    "entries": [
                        {
                            "name": "E-commerce Platform",
                            "description": "Built a scalable e-commerce web application",
                            "technologies": ["React", "Node.js", "MongoDB"],
                            "dates": "June 2022 - December 2022"
                        }
                    ],
                    "max_entries": 3
                },
                "certifications": {
                    "title": "Certifications",
                    "entries": [
                        {
                            "name": "AWS Certified Developer",
                            "issuer": "Amazon Web Services",
                            "date": "2022",
                            "credential_id": "AWS-DEV-123"
                        }
                    ]
                },
                "languages": {
                    "title": "Languages",
                    "languages": [
                        {"language": "English", "proficiency": "Native"},
                        {"language": "Spanish", "proficiency": "Conversational"}
                    ]
                }
            }
        }
        
        # Sample job description data
        self.job_description_data = {
            "parsed_content": {
                "job_title": "Senior Software Engineer",
                "company": "Enterprise Corp",
                "required_skills": [
                    {"skill": "Python", "category": "technical", "experience_level": "5+ years"},
                    {"skill": "Django", "category": "technical", "experience_level": "3+ years"},
                    {"skill": "React", "category": "technical", "experience_level": "2+ years"}
                ],
                "preferred_skills": [
                    {"skill": "AWS", "category": "technical", "experience_level": "2+ years"},
                    {"skill": "PostgreSQL", "category": "technical", "experience_level": "2+ years"}
                ],
                "responsibilities": [
                    "Design and develop scalable software solutions",
                    "Lead code reviews and mentor junior developers"
                ],
                "qualifications": [
                    "Bachelor's degree in Computer Science or related field",
                    "5+ years of software development experience"
                ]
            },
            "raw_text": "We are looking for a Senior Software Engineer to join our team at Enterprise Corp. Contact Hiring Manager Jane Smith at jane.smith@enterprisecorp.com.",
            "job_title": "Senior Software Engineer",
            "company": "Enterprise Corp"
        }

    def test_generate_cover_letter_basic(self):
        """Test basic cover letter generation."""
        result = self.generator.generate_cover_letter(
            self.tailored_resume_data,
            self.job_description_data
        )
        
        # Test overall structure
        assert "cover_letter" in result
        assert "metadata" in result
        assert "validation" in result
        assert "sources" in result
        
        # Test cover letter structure
        cover_letter = result["cover_letter"]
        assert "sections" in cover_letter
        assert "full_text" in cover_letter
        
        # Test sections
        sections = cover_letter["sections"]
        assert "salutation" in sections
        assert "introduction" in sections
        assert "body_paragraphs" in sections
        assert "closing" in sections
        assert "sign_off" in sections
        assert "signature" in sections
        
        # Test metadata
        metadata = result["metadata"]
        assert metadata["truthfulness_score"] >= 0.0
        assert metadata["truthfulness_score"] <= 1.0
        assert metadata["grammar_score"] >= 0.0
        assert metadata["grammar_score"] <= 1.0
        assert metadata["personalization_score"] >= 0.0
        assert metadata["personalization_score"] <= 1.0
        assert "processing_time_ms" in metadata
        assert "word_count" in metadata

    def test_generate_cover_letter_with_options(self):
        """Test cover letter generation with custom options."""
        options = {
            "tone": "modern",
            "focus": "skills_match",
            "length": "standard",
            "personalization_level": "high"
        }
        
        result = self.generator.generate_cover_letter(
            self.tailored_resume_data,
            self.job_description_data,
            options
        )
        
        assert result["success"] is True
        assert result["metadata"]["generation_options"]["tone"] == "modern"
        assert result["metadata"]["generation_options"]["focus"] == "skills_match"

    def test_generate_cover_letter_technical_tone(self):
        """Test cover letter generation with technical tone."""
        options = {"tone": "technical"}
        
        result = self.generator.generate_cover_letter(
            self.tailored_resume_data,
            self.job_description_data,
            options
        )
        
        assert result["success"] is True
        assert result["metadata"]["generation_options"]["tone"] == "technical"
        
        # Technical tone should have more body paragraphs
        body_paragraphs = result["cover_letter"]["sections"]["body_paragraphs"]
        assert len(body_paragraphs) >= 3  # Technical template adds extra paragraph

    def test_create_truth_bank_from_resume(self):
        """Test truth bank creation from resume data."""
        truth_bank = self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        
        # Check personal info
        assert truth_bank["personal_info"]["name"] == "John Doe"
        assert truth_bank["personal_info"]["contact"]["email"] == "john@example.com"
        
        # Check experience
        assert "Tech Corp" in truth_bank["experience"]["companies"]
        assert "Software Engineer" in truth_bank["experience"]["titles"]
        assert "Improved application performance by 40%" in truth_bank["experience"]["achievements"]
        assert "Python" in truth_bank["experience"]["technologies"]
        
        # Check skills
        assert "Python" in truth_bank["skills"]["technical"]
        assert "Communication" in truth_bank["skills"]["soft_skills"]
        
        # Check education
        assert "Bachelor of Science" in truth_bank["education"]["degrees"]
        assert "State University" in truth_bank["education"]["universities"]
        
        # Check projects
        assert "E-commerce Platform" in truth_bank["projects"]["names"]
        assert "React" in truth_bank["projects"]["technologies"]

    def test_extract_hiring_manager(self):
        """Test hiring manager extraction from JD."""
        # Test with hiring manager in JD
        jd_with_manager = {
            "raw_text": "Contact Hiring Manager Jane Smith at jane.smith@company.com for this position."
        }
        
        hiring_manager = self.generator._extract_hiring_manager(jd_with_manager)
        assert hiring_manager == "Jane Smith"
        
        # Test without hiring manager
        jd_without_manager = {
            "raw_text": "We are looking for a software engineer to join our team."
        }
        
        hiring_manager = self.generator._extract_hiring_manager(jd_without_manager)
        assert hiring_manager is None

    def test_calculate_experience_years(self):
        """Test experience years calculation."""
        # Test with date ranges
        resume_with_dates = {
            "experience": {
                "entries": [
                    {"dates": "2020-2022"},
                    {"dates": "2022-2023"}
                ]
            }
        }
        
        years = self.generator._calculate_experience_years(resume_with_dates)
        assert years == "4"  # 2020-2023 inclusive
        
        # Test without dates
        resume_without_dates = {
            "experience": {"entries": []}
        }
        
        years = self.generator._calculate_experience_years(resume_without_dates)
        assert years == "several"

    def test_extract_key_skills(self):
        """Test key skills extraction."""
        skills = self.generator._extract_key_skills(self.tailored_resume_data["rendering_data"])
        
        assert len(skills) > 0
        assert "Python" in skills
        assert "Django" in skills
        assert "React" in skills
        assert "Communication" in skills

    def test_determine_key_area(self):
        """Test key area determination."""
        key_area = self.generator._determine_key_area(
            self.tailored_resume_data["rendering_data"],
            self.job_description_data["parsed_content"]
        )
        
        assert key_area in ["Python", "Django", "React", "software development"]

    def test_extract_company_focus(self):
        """Test company focus extraction."""
        # Test with fintech JD
        fintech_jd = {
            "raw_text": "We are a financial technology company focused on payments and banking services."
        }
        
        focus = self.generator._extract_company_focus(fintech_jd)
        assert focus == "fintech"
        
        # Test with healthcare JD
        healthcare_jd = {
            "raw_text": "Our healthcare company provides medical services to patients."
        }
        
        focus = self.generator._extract_company_focus(healthcare_jd)
        assert focus == "healthcare"
        
        # Test with no clear focus
        general_jd = {
            "raw_text": "We are looking for talented engineers to join our team."
        }
        
        focus = self.generator._extract_company_focus(general_jd)
        assert focus == "technology"

    def test_combine_sections(self):
        """Test section combination into full text."""
        sections = {
            "salutation": "Dear Hiring Manager,",
            "introduction": "I am writing to express my interest in the position.",
            "body_paragraphs": ["First paragraph.", "Second paragraph."],
            "closing": "I look forward to hearing from you.",
            "sign_off": "Sincerely,",
            "signature": "John Doe"
        }
        
        full_text = self.generator._combine_sections(sections)
        
        assert "Dear Hiring Manager," in full_text
        assert "I am writing to express my interest in the position." in full_text
        assert "First paragraph." in full_text
        assert "Second paragraph." in full_text
        assert "I look forward to hearing from you." in full_text
        assert "Sincerely," in full_text
        assert "John Doe" in full_text
        
        # Check proper spacing
        lines = full_text.split('\n')
        assert lines[1] == ""  # Empty line after salutation

    def test_validate_cover_letter_valid(self):
        """Test validation of valid cover letter."""
        valid_content = {
            "sections": {
                "salutation": "Dear Hiring Manager,",
                "introduction": "I am writing to express my interest.",
                "body_paragraphs": ["First paragraph."],
                "closing": "I look forward to hearing from you."
            },
            "full_text": "Dear Hiring Manager,\n\nI am writing to express my interest.\n\nFirst paragraph.\n\nI look forward to hearing from you.\n\nSincerely,\nJohn Doe"
        }
        
        truth_bank = self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        
        validation = self.generator._validate_cover_letter(valid_content, truth_bank)
        
        assert validation["is_valid"] == True
        assert len(validation["errors"]) == 0
        assert len(validation["warnings"]) == 0
        assert len(validation["guardrail_violations"]) == 0

    def test_validate_cover_letter_invalid(self):
        """Test validation of invalid cover letter."""
        invalid_content = {
            "sections": {
                "salutation": "",  # Missing salutation
                "introduction": "",  # Missing introduction
                "body_paragraphs": [],
                "closing": ""  # Missing closing
            },
            "full_text": "Invalid content"
        }
        
        truth_bank = self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        
        validation = self.generator._validate_cover_letter(invalid_content, truth_bank)
        
        assert validation["is_valid"] == False
        assert len(validation["errors"]) >= 3  # Missing sections

    def test_check_fabrication_indicators(self):
        """Test fabrication indicator detection."""
        text_with_indicators = "I am a world-class expert in software development with industry-leading skills."
        truth_bank = {}
        
        violations = self.generator._check_fabrication_indicators(text_with_indicators, truth_bank)
        
        assert len(violations) >= 2  # Should catch "world-class" and "industry-leading"
        
        for violation in violations:
            assert violation["type"] == "fabrication_indicator"
            assert violation["severity"] == "medium"

    def test_check_excessive_claims(self):
        """Test excessive claims detection."""
        text_with_claims = "Improved performance by 50%, increased revenue by 40%, reduced costs by 30%, served 100,000 users, saved $1M."
        truth_bank = {}
        
        warnings = self.generator._check_excessive_claims(text_with_claims, truth_bank)
        
        assert len(warnings) >= 2  # Should catch excessive percentage and metric claims

    def test_calculate_truthfulness_score(self):
        """Test truthfulness score calculation."""
        # Test with clean content
        clean_content = {
            "full_text": "I am writing to express my interest in the position at Company."
        }
        truth_bank = {}
        
        score = self.generator._calculate_truthfulness_score(clean_content, truth_bank)
        assert score >= 0.8  # Should be high for clean content
        
        # Test with fabrication indicators
        fabricated_content = {
            "full_text": "I am a world-class expert with industry-leading skills."
        }
        
        score = self.generator._calculate_truthfulness_score(fabricated_content, truth_bank)
        assert score < 0.8  # Should be lower for fabricated content

    def test_calculate_grammar_score(self):
        """Test grammar score calculation."""
        # Test with well-formed content
        good_content = {
            "full_text": "I am writing to express my interest in the position. I have five years of experience. I look forward to hearing from you."
        }
        
        score = self.generator._calculate_grammar_score(good_content)
        assert score >= 0.8  # Should be high for good grammar
        
        # Test with poor grammar
        poor_content = {
            "full_text": "i am writing to express my interest in the position. i have five years of experience. i look forward to hearing from you."
        }
        
        score = self.generator._calculate_grammar_score(poor_content)
        assert score < 0.8  # Should be lower for poor grammar

    def test_calculate_personalization_score(self):
        """Test personalization score calculation."""
        # Test with personalized content
        personalized_content = {
            "full_text": "I am writing to express my interest in the Senior Software Engineer position at Enterprise Corp. I have experience with Python and Django."
        }
        
        resume_content = self.tailored_resume_data["rendering_data"]
        jd_content = self.job_description_data["parsed_content"]
        
        score = self.generator._calculate_personalization_score(
            personalized_content, resume_content, jd_content
        )
        
        assert score >= 0.7  # Should be reasonably high for personalized content

    def test_identify_content_sources(self):
        """Test content source identification."""
        cover_letter_content = {
            "full_text": "I am John Doe and I have experience with Python and Django. I worked at Tech Corp."
        }
        
        truth_bank = self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        
        sources = self.generator._identify_content_sources(cover_letter_content, truth_bank)
        
        assert len(sources) >= 3  # Should find name, skills, and company
        
        # Check source types
        source_types = [s["type"] for s in sources]
        assert "resume_personal_info" in source_types
        assert "resume_skill" in source_types
        assert "resume_experience" in source_types

    def test_generate_cover_letter_empty_data(self):
        """Test cover letter generation with minimal data."""
        minimal_resume = {
            "rendering_data": {
                "header": {"name": "Jane Doe", "contact": {"email": "jane@example.com"}},
                "summary": {"content": "Experienced professional"},
                "experience": {"entries": []},
                "skills": {"categories": []},
                "education": {"entries": []},
                "projects": None,
                "certifications": None,
                "languages": None
            }
        }
        
        minimal_jd = {
            "parsed_content": {"job_title": "Engineer", "company": "Tech Corp"},
            "raw_text": "We are looking for an engineer.",
            "job_title": "Engineer",
            "company": "Tech Corp"
        }
        
        result = self.generator.generate_cover_letter(minimal_resume, minimal_jd)
        
        assert result["success"] is True
        assert result["cover_letter"]["sections"]["salutation"] is not None
        assert result["cover_letter"]["sections"]["introduction"] is not None

    def test_generate_cover_letter_validation_failure(self):
        """Test cover letter generation with validation failure."""
        # Create content that will trigger validation failures
        resume_with_fabrication = {
            "rendering_data": {
                "header": {"name": "John Doe", "contact": {"email": "john@example.com"}},
                "summary": {"content": "I am a world-class expert in everything."},
                "experience": {"entries": []},
                "skills": {"categories": []},
                "education": {"entries": []}
            }
        }
        
        result = self.generator.generate_cover_letter(resume_with_fabrication, self.job_description_data)
        
        # Should still generate but with validation warnings
        assert result["success"] is True
        assert len(result["validation"]["warnings"]) > 0 or len(result["validation"]["guardrail_violations"]) > 0

    def test_structure_templates(self):
        """Test that all structure templates have required keys."""
        for template_name, template in self.generator.structure_templates.items():
            required_keys = ["salutation", "intro", "body", "skills_match", "closing", "sign_off", "signature"]
            
            for key in required_keys:
                assert key in template, f"Missing key '{key}' in {template_name} template"
                assert template[key] is not None, f"Key '{key}' is None in {template_name} template"

    def test_word_count_calculation(self):
        """Test word count calculation in metadata."""
        result = self.generator.generate_cover_letter(
            self.tailored_resume_data,
            self.job_description_data
        )
        
        word_count = result["metadata"]["word_count"]
        assert word_count > 0
        assert word_count == len(result["cover_letter"]["full_text"].split())

    def test_processing_time_tracking(self):
        """Test processing time tracking."""
        result = self.generator.generate_cover_letter(
            self.tailored_resume_data,
            self.job_description_data
        )
        
        processing_time = result["metadata"]["processing_time_ms"]
        assert processing_time > 0
        assert isinstance(processing_time, int)

    def test_sources_confidence_levels(self):
        """Test content sources have confidence levels."""
        result = self.generator.generate_cover_letter(
            self.tailored_resume_data,
            self.job_description_data
        )
        
        sources = result["sources"]
        for source in sources:
            assert "confidence" in source
            assert source["confidence"] in ["high", "medium", "low"]


if __name__ == "__main__":
    pytest.main([__file__])
