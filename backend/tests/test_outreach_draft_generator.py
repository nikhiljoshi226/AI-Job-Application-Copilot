import pytest
from app.services.outreach_draft_generator import OutreachDraftGenerator


class TestOutreachDraftGenerator:
    
    def setup_method(self):
        """Setup test fixtures."""
        self.generator = OutreachDraftGenerator()
        
        # Sample resume data
        self.resume_data = {
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
            }
        }
        
        # Sample job description data
        self.job_description_data = {
            "job_title": "Senior Software Engineer",
            "company": "Enterprise Corp",
            "raw_text": "We are looking for a Senior Software Engineer to join our team at Enterprise Corp. Contact Hiring Manager Jane Smith at jane.smith@enterprisecorp.com.",
            "parsed_content": {
                "required_skills": [
                    {"skill": "Python", "category": "technical", "experience_level": "5+ years"},
                    {"skill": "Django", "category": "technical", "experience_level": "3+ years"},
                    {"skill": "React", "category": "technical", "experience_level": "2+ years"}
                ]
            }
        }

    def test_generate_email_intro_draft(self):
        """Test email intro draft generation."""
        result = self.generator.generate_outreach_draft(
            self.resume_data,
            self.job_description_data,
            "email_intro"
        )
        
        # Test overall structure
        assert "draft" in result
        assert "metadata" in result
        assert "validation" in result
        assert "sources" in result
        
        # Test draft structure
        draft = result["draft"]
        assert "sections" in draft
        assert "full_text" in draft
        
        # Test sections
        sections = draft["sections"]
        assert "salutation" in sections
        assert "introduction" in sections
        assert "body_paragraphs" in sections
        assert "closing" in sections
        assert "sign_off" in sections
        assert "signature" in sections
        
        # Test metadata
        metadata = result["metadata"]
        assert metadata["outreach_type"] == "email_intro"
        assert metadata["truthfulness_score"] >= 0.0
        assert metadata["truthfulness_score"] <= 1.0
        assert metadata["conciseness_score"] >= 0.0
        assert metadata["conciseness_score"] <= 1.0
        assert metadata["professionalism_score"] >= 0.0
        assert metadata["professionalism_score"] <= 1.0
        assert "processing_time_ms" in metadata
        assert "word_count" in metadata

    def test_generate_linkedin_note_draft(self):
        """Test LinkedIn note draft generation."""
        result = self.generator.generate_outreach_draft(
            self.resume_data,
            self.job_description_data,
            "linkedin_note"
        )
        
        assert result["metadata"]["outreach_type"] == "linkedin_note"
        assert result["draft"]["sections"]["salutation"] is not None
        assert result["draft"]["sections"]["introduction"] is not None
        
        # LinkedIn notes should be more concise
        word_count = result["metadata"]["word_count"]
        assert word_count < 200  # LinkedIn notes should be shorter

    def test_generate_formal_message_draft(self):
        """Test formal message draft generation."""
        result = self.generator.generate_outreach_draft(
            self.resume_data,
            self.job_description_data,
            "formal_message"
        )
        
        assert result["metadata"]["outreach_type"] == "formal_message"
        assert result["draft"]["sections"]["salutation"] is not None
        assert result["draft"]["sections"]["introduction"] is not None
        
        # Formal messages should have more body paragraphs
        body_paragraphs = result["draft"]["sections"]["body_paragraphs"]
        assert len(body_paragraphs) >= 2  # Formal template has more content

    def test_generate_with_options(self):
        """Test draft generation with custom options."""
        options = {
            "tone": "modern",
            "length": "standard",
            "personalization_level": "high"
        }
        
        result = self.generator.generate_outreach_draft(
            self.resume_data,
            self.job_description_data,
            "email_intro",
            options
        )
        
        assert result["metadata"]["generation_options"]["tone"] == "modern"
        assert result["metadata"]["generation_options"]["personalization_level"] == "high"

    def test_create_truth_bank_from_resume(self):
        """Test truth bank creation from resume data."""
        truth_bank = self.generator._create_truth_bank_from_resume(self.resume_data)
        
        # Check personal info
        assert truth_bank["personal_info"]["name"] == "John Doe"
        assert truth_bank["personal_info"]["contact"]["email"] == "john@example.com"
        
        # Check experience
        assert "Tech Corp" in truth_bank["experience"]["companies"]
        assert "Software Engineer" in truth_bank["experience"]["titles"]
        assert "Python" in truth_bank["experience"]["skills"]
        assert "Improved application performance by 40%" in truth_bank["experience"]["achievements"]
        
        # Check skills
        assert "Python" in truth_bank["skills"]["technical"]
        assert "Communication" in truth_bank["skills"]["soft_skills"]
        
        # Check education
        assert "Bachelor of Science" in truth_bank["education"]["degrees"]
        assert "State University" in truth_bank["education"]["universities"]
        
        # Check projects
        assert "E-commerce Platform" in truth_bank["projects"]["names"]
        assert "React" in truth_bank["projects"]["technologies"]

    def test_extract_recruiter_name(self):
        """Test recruiter name extraction from JD."""
        # Test with recruiter in JD
        jd_with_recruiter = {
            "raw_text": "Contact Hiring Manager Jane Smith at jane.smith@company.com for this position."
        }
        
        recruiter_name = self.generator._extract_recruiter_name(jd_with_recruiter)
        assert recruiter_name == "Jane Smith"
        
        # Test without recruiter
        jd_without_recruiter = {
            "raw_text": "We are looking for a software engineer to join our team."
        }
        
        recruiter_name = self.generator._extract_recruiter_name(jd_without_recruiter)
        assert recruiter_name == "Hiring Manager"

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
        skills = self.generator._extract_key_skills(self.resume_data)
        
        assert len(skills) > 0
        assert "Python" in skills
        assert "Django" in skills
        assert "React" in skills
        assert "Communication" in skills

    def test_determine_key_area(self):
        """Test key area determination."""
        key_area = self.generator._determine_key_area(
            self.resume_data,
            self.job_description_data
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

    def test_extract_technologies(self):
        """Test technologies extraction."""
        technologies = self.generator._extract_technologies(self.resume_data)
        
        assert len(technologies) > 0
        assert "Python" in technologies
        assert "Django" in technologies
        assert "React" in technologies

    def test_extract_key_achievements(self):
        """Test key achievements extraction."""
        achievements = self.generator._extract_key_achievements(self.resume_data)
        
        assert len(achievements) > 0
        assert "Improved application performance by 40%" in achievements
        assert "Led team of 3 junior developers" in achievements

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

    def test_validate_outreach_draft_valid(self):
        """Test validation of valid outreach draft."""
        valid_content = {
            "sections": {
                "salutation": "Dear Hiring Manager,",
                "introduction": "I am writing to express my interest.",
                "body_paragraphs": ["First paragraph."],
                "closing": "I look forward to hearing from you."
            },
            "full_text": "Dear Hiring Manager,\n\nI am writing to express my interest.\n\nFirst paragraph.\n\nI look forward to hearing from you.\n\nSincerely,\nJohn Doe"
        }
        
        truth_bank = self.generator._create_truth_bank_from_resume(self.resume_data)
        
        validation = self.generator._validate_outreach_draft(valid_content, truth_bank)
        
        assert validation["is_valid"] == True
        assert len(validation["errors"]) == 0
        assert len(validation["warnings"]) == 0
        assert len(validation["guardrail_violations"]) == 0

    def test_validate_outreach_draft_invalid(self):
        """Test validation of invalid outreach draft."""
        invalid_content = {
            "sections": {
                "salutation": "",  # Missing salutation
                "introduction": "",  # Missing introduction
                "body_paragraphs": [],
                "closing": ""  # Missing closing
            },
            "full_text": "Invalid content"
        }
        
        truth_bank = self.generator._create_truth_bank_from_resume(self.resume_data)
        
        validation = self.generator._validate_outreach_draft(invalid_content, truth_bank)
        
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
        text_with_claims = "Improved performance by 50%, increased revenue by 40%, served 100,000 users."
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

    def test_calculate_conciseness_score(self):
        """Test conciseness score calculation."""
        # Test with ideal length
        ideal_content = {
            "full_text": " ".join(["word"] * 150)  # 150 words
        }
        
        score = self.generator._calculate_conciseness_score(ideal_content)
        assert score >= 0.8  # Should be high for ideal length
        
        # Test with too long content
        long_content = {
            "full_text": " ".join(["word"] * 300)  # 300 words
        }
        
        score = self.generator._calculate_conciseness_score(long_content)
        assert score < 0.8  # Should be lower for long content

    def test_calculate_professionalism_score(self):
        """Test professionalism score calculation."""
        # Test with professional content
        professional_content = {
            "full_text": "Dear Hiring Manager, I am writing to express my interest. Best regards."
        }
        
        score = self.generator._calculate_professionalism_score(professional_content)
        assert score >= 0.8  # Should be high for professional content
        
        # Test with informal content
        informal_content = {
            "full_text": "Hey, I'm awesome and cool. Let's connect!"
        }
        
        score = self.generator._calculate_professionalism_score(informal_content)
        assert score < 0.8  # Should be lower for informal content

    def test_identify_content_sources(self):
        """Test content source identification."""
        draft_content = {
            "full_text": "I am John Doe and I have experience with Python and Django. I worked at Tech Corp."
        }
        
        truth_bank = self.generator._create_truth_bank_from_resume(self.resume_data)
        
        sources = self.generator._identify_content_sources(draft_content, truth_bank)
        
        assert len(sources) >= 3  # Should find name, skills, and company
        
        # Check source types
        source_types = [s["type"] for s in sources]
        assert "resume_personal_info" in source_types
        assert "resume_skill" in source_types
        assert "resume_experience" in source_types

    def test_get_available_outreach_types(self):
        """Test available outreach types."""
        types = self.generator.get_available_outreach_types()
        
        assert "email_intro" in types
        assert "linkedin_note" in types
        assert "formal_message" in types
        
        # Check descriptions
        for outreach_type, description in types.items():
            assert isinstance(description, str)
            assert len(description) > 0

    def test_generate_outreach_draft_minimal_data(self):
        """Test draft generation with minimal data."""
        minimal_resume = {
            "header": {"name": "Jane Doe", "contact": {"email": "jane@example.com"}},
            "experience": {"entries": []},
            "skills": {"categories": []},
            "education": {"entries": []},
            "projects": None
        }
        
        minimal_jd = {
            "job_title": "Engineer",
            "company": "Tech Corp",
            "raw_text": "We are looking for an engineer.",
            "parsed_content": {}
        }
        
        result = self.generator.generate_outreach_draft(minimal_resume, minimal_jd, "email_intro")
        
        assert result["success"] is True
        assert result["draft"]["sections"]["salutation"] is not None
        assert result["draft"]["sections"]["introduction"] is not None

    def test_template_structure(self):
        """Test that all templates have required keys."""
        for template_name, template in self.generator.templates.items():
            required_keys = ["subject", "body", "call_to_action", "closing", "sign_off"]
            
            for key in required_keys:
                assert key in template, f"Missing key '{key}' in {template_name} template"
                assert template[key] is not None, f"Key '{key}' is None in {template_name} template"

    def test_word_count_calculation(self):
        """Test word count calculation in metadata."""
        result = self.generator.generate_outreach_draft(
            self.resume_data,
            self.job_description_data,
            "email_intro"
        )
        
        word_count = result["metadata"]["word_count"]
        assert word_count > 0
        assert word_count == len(result["draft"]["full_text"].split())

    def test_processing_time_tracking(self):
        """Test processing time tracking."""
        result = self.generator.generate_outreach_draft(
            self.resume_data,
            self.job_description_data,
            "email_intro"
        )
        
        processing_time = result["metadata"]["processing_time_ms"]
        assert processing_time > 0
        assert isinstance(processing_time, int)

    def test_sources_confidence_levels(self):
        """Test content sources have confidence levels."""
        result = self.generator.generate_outreach_draft(
            self.resume_data,
            self.job_description_data,
            "email_intro"
        )
        
        sources = result["sources"]
        for source in sources:
            assert "confidence" in source
            assert source["confidence"] in ["high", "medium", "low"]

    def test_different_tones(self):
        """Test generation with different tones."""
        tones = ["professional", "modern", "technical"]
        
        for tone in tones:
            options = {"tone": tone}
            
            result = self.generator.generate_outreach_draft(
                self.resume_data,
                self.job_description_data,
                "email_intro",
                options
            )
            
            assert result["metadata"]["generation_options"]["tone"] == tone
            assert result["success"] is True

    def test_length_validation(self):
        """Test length validation in outreach drafts."""
        # Test very short draft
        short_content = {
            "sections": {
                "salutation": "Dear Hiring Manager,",
                "introduction": "I am interested.",
                "body_paragraphs": [],
                "closing": "Thanks."
            },
            "full_text": "Dear Hiring Manager,\n\nI am interested.\n\nThanks.\n\nSincerely,\nJohn"
        }
        
        truth_bank = self.generator._create_truth_bank_from_resume(self.resume_data)
        validation = self.generator._validate_outreach_draft(short_content, truth_bank)
        
        assert len(validation["warnings"]) > 0
        assert any("quite short" in warning for warning in validation["warnings"])
        
        # Test very long draft
        long_content = {
            "sections": {
                "salutation": "Dear Hiring Manager,",
                "introduction": "I am writing to express my strong interest in this position.",
                "body_paragraphs": ["This is a very long paragraph. " * 50] * 5,  # 5 long paragraphs
                "closing": "I look forward to hearing from you."
            },
            "full_text": "Very long content " * 1000
        }
        
        validation = self.generator._validate_outreach_draft(long_content, truth_bank)
        
        assert len(validation["warnings"]) > 0
        assert any("quite long" in warning for warning in validation["warnings"])


if __name__ == "__main__":
    pytest.main([__file__])
