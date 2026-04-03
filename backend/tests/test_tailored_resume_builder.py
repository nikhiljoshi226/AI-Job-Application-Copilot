import pytest
from app.services.tailored_resume_builder import TailoredResumeBuilder


class TestTailoredResumeBuilder:
    
    def setup_method(self):
        """Setup test fixtures."""
        self.builder = TailoredResumeBuilder()
        
        # Sample original resume
        self.original_resume = {
            "id": 1,
            "personal_info": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "555-1234",
                "location": "New York, NY"
            },
            "summary": "Software engineer with 5 years of experience",
            "skills": {
                "technical": [
                    {"name": "Python", "years_of_experience": 5}
                ],
                "soft_skills": [
                    {"name": "Communication", "proficiency_level": "strong"}
                ]
            },
            "experience": [
                {
                    "title": "Software Engineer",
                    "company": "Tech Corp",
                    "start_date": "2021-01-15",
                    "end_date": "2023-03-15",
                    "current": False,
                    "description": "Developed web applications",
                    "achievements": [
                        "Improved application performance by 40%"
                    ]
                }
            ],
            "projects": [
                {
                    "name": "E-commerce Platform",
                    "description": "Built a web application for online shopping",
                    "technologies": ["React", "Node.js"]
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Science",
                    "major": "Computer Science",
                    "university": "State University",
                    "graduation_year": "2020"
                }
            ],
            "metadata": {
                "total_years_experience": 5
            }
        }
        
        # Sample approved suggestions
        self.approved_suggestions = {
            "summary": [
                {
                    "type": "enhancement",
                    "current_text": "Software engineer with 5 years of experience",
                    "suggested_text": "Senior Software Engineer with 5 years of experience in full-stack development",
                    "approved": True,
                    "truthfulness_score": 0.95,
                    "evidence": {"source": "resume_experience", "confidence": "high"}
                }
            ],
            "skills": [
                {
                    "type": "addition",
                    "skill_name": "Django",
                    "category": "technical",
                    "suggested_addition": "Django",
                    "approved": True,
                    "truthfulness_score": 0.7,
                    "evidence": {"source": "gap_analysis", "confidence": "medium"}
                }
            ],
            "experience": [
                {
                    "type": "bullet_enhancement",
                    "current_bullet": "Developed web applications",
                    "suggested_bullet": "Developed scalable web applications using Python and Django, serving 10,000+ users",
                    "approved": True,
                    "truthfulness_score": 0.8,
                    "evidence": {"source": "resume_experience", "confidence": "high"}
                }
            ],
            "projects": [
                {
                    "type": "description_enhancement",
                    "current_text": "Built a web application for online shopping",
                    "suggested_text": "Built a scalable e-commerce web application serving 5,000+ daily active users with 99.9% uptime",
                    "approved": True,
                    "truthfulness_score": 0.75,
                    "evidence": {"source": "project_analysis", "confidence": "medium"}
                }
            ]
        }
        
        # Sample truth bank
        self.truth_bank = {
            "professional_facts": {
                "total_years_experience": 5,
                "current_role": "Software Engineer",
                "career_level": "mid"
            },
            "experience_facts": {
                "companies_worked": [
                    {
                        "company": "Tech Corp",
                        "title": "Software Engineer",
                        "duration": "2021-2023",
                        "verified": True
                    }
                ],
                "total_companies": 1,
                "management_experience": False
            },
            "skill_facts": {
                "verified_technical_skills": [
                    {
                        "skill": "Python",
                        "years_experience": 5,
                        "proficiency_level": "advanced",
                        "evidence_source": "experience_section"
                    }
                ]
            }
        }

    def test_build_tailored_resume_basic(self):
        """Test basic tailored resume building."""
        result = self.builder.build_tailored_resume(
            self.original_resume,
            self.approved_suggestions,
            self.truth_bank
        )
        
        # Test overall structure
        assert "tailored_resume" in result
        assert "metadata" in result
        assert "applied_changes" in result
        assert "change_summary" in result
        
        # Test metadata
        metadata = result["metadata"]
        assert metadata["original_resume_id"] == 1
        assert metadata["total_suggestions_applied"] == 4
        assert metadata["truthfulness_score"] >= 0.0
        assert metadata["truthfulness_score"] <= 1.0
        assert "processing_time_ms" in metadata
        assert "generated_at" in metadata
        assert metadata["version"] == 1
        
        # Test applied changes
        applied_changes = result["applied_changes"]
        assert len(applied_changes) == 4
        
        # Test change summary
        summary = result["change_summary"]
        assert summary["total_changes"] == 4
        assert "changes_by_type" in summary
        assert "changes_by_section" in summary
        assert summary["average_truthfulness"] >= 0.0

    def test_apply_enhancement_suggestion(self):
        """Test applying enhancement suggestions."""
        section_data = "Software engineer with 5 years of experience"
        suggestion = {
            "type": "enhancement",
            "current_text": "Software engineer with 5 years of experience",
            "suggested_text": "Senior Software Engineer with 5 years of experience in full-stack development",
            "truthfulness_score": 0.95
        }
        
        change = self.builder._apply_enhancement(section_data, suggestion, "summary")
        
        assert change is not None
        assert change["type"] == "enhancement"
        assert change["section"] == "summary"
        assert change["original"] == "Software engineer with 5 years of experience"
        assert change["modified"] == "Senior Software Engineer with 5 years of experience in full-stack development"
        assert change["truthfulness_score"] == 0.95

    def test_apply_addition_suggestion(self):
        """Test applying addition suggestions."""
        section_data = {
            "technical": [{"name": "Python", "years_of_experience": 5}],
            "soft_skills": [{"name": "Communication", "proficiency_level": "strong"}]
        }
        suggestion = {
            "type": "addition",
            "skill_name": "Django",
            "category": "technical",
            "suggested_addition": "Django",
            "truthfulness_score": 0.7
        }
        
        change = self.builder._apply_addition(section_data, suggestion, "skills")
        
        assert change is not None
        assert change["type"] == "addition"
        assert change["section"] == "skills"
        assert change["added"] == "Django"
        assert change["skill_name"] == "Django"
        assert change["category"] == "technical"
        
        # Check that the skill was actually added
        assert len(section_data["technical"]) == 2
        assert section_data["technical"][1]["name"] == "Django"
        assert section_data["technical"][1]["added_via_tailoring"] == True

    def test_apply_bullet_enhancement_suggestion(self):
        """Test applying bullet enhancement suggestions."""
        section_data = [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "description": "Developed web applications",
                "achievements": ["Improved application performance by 40%"]
            }
        ]
        suggestion = {
            "type": "bullet_enhancement",
            "current_bullet": "Developed web applications",
            "suggested_bullet": "Developed scalable web applications using Python and Django, serving 10,000+ users",
            "truthfulness_score": 0.8
        }
        
        change = self.builder._apply_bullet_enhancement(section_data, suggestion, "experience")
        
        assert change is not None
        assert change["type"] == "bullet_enhancement"
        assert change["section"] == "experience"
        assert change["original_bullet"] == "Developed web applications"
        assert change["modified_bullet"] == "Developed scalable web applications using Python and Django, serving 10,000+ users"
        
        # Check that the bullet was actually changed
        assert section_data[0]["description"] == "Developed scalable web applications using Python and Django, serving 10,000+ users"

    def test_apply_description_enhancement_suggestion(self):
        """Test applying description enhancement suggestions."""
        section_data = [
            {
                "name": "E-commerce Platform",
                "description": "Built a web application for online shopping",
                "technologies": ["React", "Node.js"]
            }
        ]
        suggestion = {
            "type": "description_enhancement",
            "current_text": "Built a web application for online shopping",
            "suggested_text": "Built a scalable e-commerce web application serving 5,000+ daily active users with 99.9% uptime",
            "truthfulness_score": 0.75
        }
        
        change = self.builder._apply_description_enhancement(section_data, suggestion, "projects")
        
        assert change is not None
        assert change["type"] == "description_enhancement"
        assert change["section"] == "projects"
        assert change["original_description"] == "Built a web application for online shopping"
        assert change["modified_description"] == "Built a scalable e-commerce web application serving 5,000+ daily active users with 99.9% uptime"
        
        # Check that the description was actually changed
        assert section_data[0]["description"] == "Built a scalable e-commerce web application serving 5,000+ daily active users with 99.9% uptime"

    def test_calculate_final_truthfulness(self):
        """Test final truthfulness score calculation."""
        # Test with high confidence changes
        high_confidence_changes = [
            {"type": "enhancement", "truthfulness_score": 0.9},
            {"type": "bullet_enhancement", "truthfulness_score": 0.8}
        ]
        score = self.builder._calculate_final_truthfulness(high_confidence_changes)
        assert score >= 0.8
        
        # Test with low confidence additions (should have penalty)
        low_confidence_changes = [
            {"type": "addition", "truthfulness_score": 0.4},
            {"type": "addition", "truthfulness_score": 0.3}
        ]
        score = self.builder._calculate_final_truthfulness(low_confidence_changes)
        assert score < 0.4  # Should have penalty applied
        
        # Test with no changes
        score = self.builder._calculate_final_truthfulness([])
        assert score == 1.0

    def test_generate_change_summary(self):
        """Test change summary generation."""
        applied_changes = [
            {"type": "enhancement", "section": "summary", "truthfulness_score": 0.9},
            {"type": "addition", "section": "skills", "truthfulness_score": 0.7},
            {"type": "bullet_enhancement", "section": "experience", "truthfulness_score": 0.8},
            {"type": "description_enhancement", "section": "projects", "truthfulness_score": 0.6}
        ]
        
        summary = self.builder._generate_change_summary(applied_changes)
        
        assert summary["total_changes"] == 4
        assert summary["changes_by_type"]["enhancement"] == 1
        assert summary["changes_by_type"]["addition"] == 1
        assert summary["changes_by_type"]["bullet_enhancement"] == 1
        assert summary["changes_by_type"]["description_enhancement"] == 1
        assert summary["changes_by_section"]["summary"] == 1
        assert summary["changes_by_section"]["skills"] == 1
        assert summary["changes_by_section"]["experience"] == 1
        assert summary["changes_by_section"]["projects"] == 1
        assert summary["high_confidence_changes"] == 1
        assert summary["medium_confidence_changes"] == 2
        assert summary["low_confidence_changes"] == 1
        assert 0.0 <= summary["average_truthfulness"] <= 1.0

    def test_validate_tailored_resume_valid(self):
        """Test validation of a valid tailored resume."""
        tailored_resume = {
            "summary": "Senior Software Engineer with 5 years of experience",
            "skills": {"technical": [], "soft_skills": []},
            "experience": [
                {
                    "title": "Software Engineer",
                    "company": "Tech Corp",
                    "start_date": "2021-01-15"
                }
            ],
            "metadata": {"truthfulness_score": 0.85}
        }
        
        is_valid, errors = self.builder.validate_tailored_resume(tailored_resume, self.original_resume)
        
        assert is_valid == True
        assert len(errors) == 0

    def test_validate_tailored_resume_invalid(self):
        """Test validation of an invalid tailored resume."""
        tailored_resume = {
            "summary": "Senior Software Engineer with 5 years of experience",
            "skills": "invalid_structure",  # Should be dict
            "experience": [
                {
                    "title": "Software Engineer"
                    # Missing company and start_date
                }
            ],
            "metadata": {"truthfulness_score": 0.2}  # Too low
        }
        
        is_valid, errors = self.builder.validate_tailored_resume(tailored_resume, self.original_resume)
        
        assert is_valid == False
        assert len(errors) > 0
        assert any("Skills section must be a dictionary" in error for error in errors)
        assert any("missing required field" in error for error in errors)
        assert any("Truthfulness score is too low" in error for error in errors)

    def test_prepare_for_rendering(self):
        """Test preparation of resume for document rendering."""
        tailored_resume = {
            "personal_info": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "555-1234",
                "location": "New York, NY",
                "linkedin": "linkedin.com/in/johndoe",
                "github": "github.com/johndoe"
            },
            "summary": "Senior Software Engineer with 5 years of experience",
            "skills": {
                "technical": [{"name": "Python", "years_of_experience": 5}],
                "soft_skills": [{"name": "Communication", "proficiency_level": "strong"}]
            },
            "experience": [
                {
                    "title": "Software Engineer",
                    "company": "Tech Corp",
                    "start_date": "2021-01-15"
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Science",
                    "major": "Computer Science",
                    "university": "State University"
                }
            ],
            "projects": [
                {"name": "E-commerce Platform", "description": "Built online store"}
            ],
            "certifications": [
                {"name": "AWS Certified Developer", "year": "2022"}
            ],
            "languages": [
                {"language": "English", "proficiency": "native"}
            ],
            "metadata": {"truthfulness_score": 0.85}
        }
        
        rendering_data = self.builder.prepare_for_rendering(tailored_resume)
        
        # Check structure
        assert "header" in rendering_data
        assert "summary" in rendering_data
        assert "skills" in rendering_data
        assert "experience" in rendering_data
        assert "education" in rendering_data
        assert "projects" in rendering_data
        assert "certifications" in rendering_data
        assert "languages" in rendering_data
        assert "metadata" in rendering_data
        
        # Check header structure
        header = rendering_data["header"]
        assert header["name"] == "John Doe"
        assert "contact" in header
        assert header["contact"]["email"] == "john@example.com"
        assert header["contact"]["phone"] == "555-1234"
        
        # Check skills structure
        skills = rendering_data["skills"]
        assert "technical" in skills
        assert "soft_skills" in skills
        assert len(skills["technical"]) == 1
        assert len(skills["soft_skills"]) == 1

    def test_build_tailored_resume_with_user_edits(self):
        """Test building tailored resume with user-edited suggestions."""
        # Add user edits to suggestions
        edited_suggestions = {
            "summary": [
                {
                    "type": "enhancement",
                    "current_text": "Software engineer with 5 years of experience",
                    "suggested_text": "Senior Software Engineer with 5 years of experience in full-stack development",
                    "user_edits": "Senior Full-Stack Developer with 5 years of experience building scalable web applications",
                    "approved": True,
                    "truthfulness_score": 0.9
                }
            ]
        }
        
        result = self.builder.build_tailored_resume(
            self.original_resume,
            edited_suggestions,
            self.truth_bank
        )
        
        # Check that user edits were applied
        tailored_resume = result["tailored_resume"]
        assert tailored_resume["summary"] == "Senior Full-Stack Developer with 5 years of experience building scalable web applications"
        
        # Check applied changes reflect user edits
        applied_changes = result["applied_changes"]
        summary_change = next(c for c in applied_changes if c["section"] == "summary")
        assert summary_change["modified"] == "Senior Full-Stack Developer with 5 years of experience building scalable web applications"

    def test_build_tailored_resume_empty_suggestions(self):
        """Test building tailored resume with no approved suggestions."""
        empty_suggestions = {
            "summary": [],
            "skills": [],
            "experience": [],
            "projects": []
        }
        
        result = self.builder.build_tailored_resume(
            self.original_resume,
            empty_suggestions,
            self.truth_bank
        )
        
        # Should return original resume unchanged
        assert result["metadata"]["total_suggestions_applied"] == 0
        assert result["metadata"]["truthfulness_score"] == 1.0
        assert len(result["applied_changes"]) == 0
        assert result["tailored_resume"] == self.original_resume

    def test_build_tailored_resume_mixed_approval(self):
        """Test building tailored resume with mixed approval status."""
        mixed_suggestions = {
            "summary": [
                {
                    "type": "enhancement",
                    "current_text": "Software engineer with 5 years of experience",
                    "suggested_text": "Senior Software Engineer with 5 years of experience",
                    "approved": True,
                    "truthfulness_score": 0.95
                },
                {
                    "type": "enhancement",
                    "current_text": "Some other text",
                    "suggested_text": "Some suggested change",
                    "approved": False,  # This should be ignored
                    "truthfulness_score": 0.8
                }
            ]
        }
        
        result = self.builder.build_tailored_resume(
            self.original_resume,
            mixed_suggestions,
            self.truth_bank
        )
        
        # Should only apply approved suggestions
        assert result["metadata"]["total_suggestions_applied"] == 1
        assert len(result["applied_changes"]) == 1
        
        # Check that only the approved change was applied
        tailored_resume = result["tailored_resume"]
        assert "Senior Software Engineer" in tailored_resume["summary"]

    def test_error_handling_invalid_suggestion_type(self):
        """Test error handling for invalid suggestion types."""
        invalid_suggestions = {
            "summary": [
                {
                    "type": "invalid_type",
                    "current_text": "Some text",
                    "suggested_text": "Some change",
                    "approved": True,
                    "truthfulness_score": 0.8
                }
            ]
        }
        
        result = self.builder.build_tailored_resume(
            self.original_resume,
            invalid_suggestions,
            self.truth_bank
        )
        
        # Should handle gracefully and not apply invalid suggestions
        assert result["metadata"]["total_suggestions_applied"] == 0
        assert len(result["applied_changes"]) == 0


if __name__ == "__main__":
    pytest.main([__file__])
