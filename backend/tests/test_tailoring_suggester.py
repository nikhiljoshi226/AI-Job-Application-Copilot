import pytest
from app.services.tailoring_suggester import TailoringSuggester


class TestTailoringSuggester:
    
    def setup_method(self):
        """Setup test fixtures."""
        self.suggester = TailoringSuggester()
        
        # Sample parsed resume
        self.sample_resume = {
            "summary": "Software engineer with 5 years of experience in web development",
            "skills": {
                "technical": [
                    {"name": "Python", "years_of_experience": 5, "evidence_source": "experience_section"},
                    {"name": "JavaScript", "years_of_experience": 4, "evidence_source": "experience_section"},
                    {"name": "React", "years_of_experience": 3, "evidence_source": "experience_section"}
                ],
                "soft_skills": [
                    {"name": "Communication", "proficiency_level": "strong", "evidence_source": "experience_section"},
                    {"name": "Teamwork", "proficiency_level": "strong", "evidence_source": "experience_section"}
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
                    "technologies": ["Python", "JavaScript", "React", "Django"],
                    "achievements": [
                        "Improved application performance by 40%",
                        "Led team of 3 junior developers"
                    ]
                }
            ],
            "projects": [
                {
                    "name": "E-commerce Platform",
                    "description": "Built a web application for online shopping",
                    "technologies": ["React", "Node.js", "MongoDB"],
                    "start_date": "2022-01-01",
                    "end_date": "2022-06-30"
                }
            ],
            "metadata": {
                "total_years_experience": 5
            }
        }
        
        # Sample truth bank
        self.sample_truth_bank = {
            "professional_facts": {
                "total_years_experience": 5,
                "current_role": "Software Engineer",
                "current_company": "Tech Corp",
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
                "management_experience": True,
                "team_leadership": True
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
        
        # Sample parsed job description
        self.sample_jd = {
            "job_title": "Senior Software Engineer",
            "company": "Enterprise Corp",
            "parsed_content": {
                "required_skills": [
                    {
                        "skill": "Python",
                        "category": "technical",
                        "experience_level": "5+ years",
                        "skill_type": "required"
                    },
                    {
                        "skill": "Django",
                        "category": "technical",
                        "experience_level": "3+ years",
                        "skill_type": "required"
                    },
                    {
                        "skill": "PostgreSQL",
                        "category": "technical",
                        "experience_level": "2+ years",
                        "skill_type": "required"
                    }
                ],
                "preferred_skills": [
                    {
                        "skill": "Docker",
                        "category": "technical",
                        "experience_level": "2+ years",
                        "skill_type": "preferred"
                    },
                    {
                        "skill": "AWS",
                        "category": "technical",
                        "experience_level": "2+ years",
                        "skill_type": "preferred"
                    }
                ],
                "responsibilities": [
                    "Design and develop scalable software solutions",
                    "Lead code reviews and mentor junior developers",
                    "Collaborate with cross-functional teams"
                ],
                "qualifications": [
                    "Bachelor's degree in Computer Science or related field",
                    "5+ years of software development experience"
                ],
                "keywords": ["python", "django", "postgresql", "aws", "agile", "scrum"],
                "role_type": {
                    "employment_type": "full_time",
                    "work_arrangement": "hybrid",
                    "experience_level": "senior"
                },
                "domain_clues": [
                    {
                        "domain": "fintech",
                        "confidence": 0.8,
                        "evidence": "Financial technology solutions"
                    }
                ]
            }
        }
    
    def test_generate_suggestions_basic(self):
        """Test basic suggestion generation."""
        result = self.suggester.generate_suggestions(
            self.sample_resume,
            self.sample_truth_bank,
            self.sample_jd
        )
        
        # Test overall structure
        assert "suggestions" in result
        assert "unsupported_requirements" in result
        assert "guardrail_violations" in result
        assert "metadata" in result
        
        # Test suggestions sections
        suggestions = result["suggestions"]
        assert "summary" in suggestions
        assert "skills" in suggestions
        assert "experience" in suggestions
        assert "projects" in suggestions
        
        # Test metadata
        metadata = result["metadata"]
        assert metadata["total_suggestions"] > 0
        assert metadata["truthfulness_score"] >= 0
        assert "generated_at" in metadata
    
    def test_generate_summary_suggestions(self):
        """Test summary section suggestions."""
        suggestions = self.suggester._generate_summary_suggestions(
            self.sample_resume,
            self.sample_truth_bank,
            self.sample_jd
        )
        
        assert len(suggestions) > 0
        
        # Should suggest adding seniority level
        seniority_suggestion = next(
            (s for s in suggestions if "senior" in s.get("suggested_text", "").lower()),
            None
        )
        assert seniority_suggestion is not None
        assert seniority_suggestion["type"] == "enhancement"
        assert seniority_suggestion["evidence"]["source"] == "truth_bank"
        assert seniority_suggestion["truthfulness_score"] >= 0.8
    
    def test_generate_skills_suggestions(self):
        """Test skills section suggestions."""
        suggestions = self.suggester._generate_skills_suggestions(
            self.sample_resume,
            self.sample_truth_bank,
            self.sample_jd
        )
        
        assert len(suggestions) > 0
        
        # Should suggest adding missing required skills
        missing_skills = [s for s in suggestions if s["type"] == "addition"]
        assert len(missing_skills) > 0
        
        # Check for Django suggestion (missing required skill)
        django_suggestion = next(
            (s for s in missing_skills if s["skill_name"].lower() == "django"),
            None
        )
        assert django_suggestion is not None
        assert django_suggestion["jd_requirement"] == "required"
        assert django_suggestion["truthfulness_score"] < 0.8  # Low confidence for missing skill
    
    def test_generate_experience_suggestions(self):
        """Test experience section suggestions."""
        suggestions = self.suggester._generate_experience_suggestions(
            self.sample_resume,
            self.sample_truth_bank,
            self.sample_jd
        )
        
        assert len(suggestions) > 0
        
        # Should enhance existing bullets
        bullet_suggestions = [s for s in suggestions if s["type"] == "bullet_enhancement"]
        assert len(bullet_suggestions) > 0
        
        # Check bullet enhancement
        bullet_suggestion = bullet_suggestions[0]
        assert "current_bullet" in bullet_suggestion
        assert "suggested_bullet" in bullet_suggestion
        assert bullet_suggestion["truthfulness_score"] >= 0.8
        assert "Enhanced bullet" in bullet_suggestion["reasoning"]
    
    def test_generate_projects_suggestions(self):
        """Test projects section suggestions."""
        suggestions = self.suggester._generate_projects_suggestions(
            self.sample_resume,
            self.sample_truth_bank,
            self.sample_jd
        )
        
        assert len(suggestions) > 0
        
        # Should enhance project description
        desc_suggestions = [s for s in suggestions if s["type"] == "description_enhancement"]
        assert len(desc_suggestions) > 0
        
        # Check description enhancement
        desc_suggestion = desc_suggestions[0]
        assert "current_text" in desc_suggestion
        assert "suggested_text" in desc_suggestion
        assert desc_suggestion["truthfulness_score"] >= 0.7
    
    def test_identify_unsupported_requirements(self):
        """Test identification of unsupported requirements."""
        # Create resume with missing skills
        limited_resume = {
            "skills": {"technical": [], "soft_skills": []},
            "experience": [],
            "metadata": {"total_years_experience": 2}
        }
        
        unsupported = self.suggester._identify_unsupported_requirements(limited_resume, self.sample_jd)
        
        assert len(unsupported) > 0
        
        # Should flag missing required skills
        missing_skills = [u for u in unsupported if u["jd_section"] == "required_skills"]
        assert len(missing_skills) > 0
        
        # Should flag experience level mismatch
        level_mismatch = [u for u in unsupported if u["jd_section"] == "role_type"]
        assert len(level_mismatch) > 0
        
        # Check structure
        for unsupported_req in unsupported:
            assert "requirement" in unsupported_req
            assert "impact" in unsupported_req
            assert "suggestion" in unsupported_req
            assert "Cannot fabricate" in unsupported_req["suggestion"]
    
    def test_check_guardrail_violations(self):
        """Test guardrail violation detection."""
        # Create suggestions with fabrication indicators
        problematic_suggestions = {
            "summary": [
                {
                    "type": "enhancement",
                    "suggested_text": "World-class expert in Python with 15+ years of experience",
                    "truthfulness_score": 0.3
                }
            ]
        }
        
        violations = self.suggester._check_guardrail_violations(problematic_suggestions)
        
        assert len(violations) > 0
        
        # Check violation structure
        violation = violations[0]
        assert violation["type"] == "fabrication_detected"
        assert "reason" in violation
        assert "suggestion" in violation
    
    def test_contains_fabrication_indicators(self):
        """Test fabrication indicator detection."""
        # Test with fabrication indicators
        problematic_suggestion = {
            "suggested_text": "World-class expert in Python with 15+ years of experience",
            "suggested_addition": "Pioneered revolutionary algorithms"
        }
        
        assert self.suggester._contains_fabrication_indicators(problematic_suggestion) == True
        
        # Test without fabrication indicators
        normal_suggestion = {
            "suggested_text": "Experienced Python developer with 5 years of experience",
            "suggested_addition": "Developed web applications"
        }
        
        assert self.suggester._contains_fabrication_indicators(normal_suggestion) == False
    
    def test_contains_excessive_claims(self):
        """Test excessive claims detection."""
        # Test with excessive claims
        excessive_suggestion = {
            "suggested_text": "Improved performance by 50%, increased revenue by 40%, reduced costs by 30%, served 100,000 users, saved $1M, and completed 6 months ahead of schedule"
        }
        
        assert self.suggester._contains_excessive_claims(excessive_suggestion) == True
        
        # Test without excessive claims
        normal_suggestion = {
            "suggested_text": "Improved performance by 30% and served 10,000 users"
        }
        
        assert self.suggester._contains_excessive_claims(normal_suggestion) == False
    
    def test_enhance_experience_bullet(self):
        """Test experience bullet enhancement."""
        current_bullet = "Developed web applications"
        jd_keywords = ["python", "django", "postgresql"]
        jd_responsibilities = ["Design and develop scalable software solutions"]
        
        enhanced = self.suggester._enhance_experience_bullet(
            current_bullet,
            jd_keywords,
            jd_responsibilities
        )
        
        assert enhanced != current_bullet
        assert len(enhanced) > len(current_bullet)
        assert any(verb in enhanced.lower() for verb in self.suggester.action_verbs)
    
    def test_enhance_project_description(self):
        """Test project description enhancement."""
        current_desc = "Built a web application"
        jd_keywords = ["python", "django", "postgresql", "aws"]
        jd_tech = ["python", "django", "postgresql"]
        
        enhanced = self.suggester._enhance_project_description(
            current_desc,
            jd_keywords,
            jd_tech
        )
        
        assert enhanced != current_desc
        assert len(enhanced) > len(current_desc)
        assert "users" in enhanced.lower()  # Should add scale
    
    def test_extract_resume_skills(self):
        """Test resume skills extraction."""
        skills = self.suggester._extract_resume_skills(self.sample_resume)
        
        assert len(skills) > 0
        
        # Check technical skills
        python_skill = next((s for s in skills if s["skill"] == "python"), None)
        assert python_skill is not None
        assert python_skill["category"] == "technical"
        assert python_skill["experience_level"] == 5
        
        # Check soft skills
        communication_skill = next((s for s in skills if s["skill"] == "communication"), None)
        assert communication_skill is not None
        assert communication_skill["category"] == "soft"
    
    def test_has_skill(self):
        """Test skill presence checking."""
        skills = [
            {"skill": "python", "category": "technical"},
            {"skill": "javascript", "category": "technical"}
        ]
        
        assert self.suggester._has_skill(skills, "Python") == True
        assert self.suggester._has_skill(skills, "Java") == False
        assert self.suggester._has_skill(skills, "python") == True  # Case insensitive
    
    def test_should_improve_skill(self):
        """Test skill improvement checking."""
        resume_skill = {"skill": "python", "experience_level": 3}
        jd_skills = [
            {"skill": "Python", "experience_level": "5+ years"}
        ]
        
        assert self.suggester._should_improve_skill(resume_skill, jd_skills) == True
        
        # Test with matching level
        resume_skill = {"skill": "python", "experience_level": "5+"}
        assert self.suggester._should_improve_skill(resume_skill, jd_skills) == False
    
    def test_calculate_truthfulness_score(self):
        """Test truthfulness score calculation."""
        # High confidence evidence
        evidence_high = {"source": "resume_experience", "confidence": "high"}
        score = self.suggester._calculate_truthfulness_score(evidence_high)
        assert score >= 0.8
        
        # Medium confidence evidence
        evidence_medium = {"source": "jd_analysis", "confidence": "medium"}
        score = self.suggester._calculate_truthfulness_score(evidence_medium)
        assert 0.5 <= score < 0.8
        
        # Low confidence evidence
        evidence_low = {"source": "gap_analysis", "confidence": "low"}
        score = self.suggester._calculate_truthfulness_score(evidence_low)
        assert score < 0.5
    
    def test_find_related_experience(self):
        """Test related experience finding."""
        skills = [{"skill": "python", "category": "technical"}]
        skill_name = "python"
        
        related = self.suggester._find_related_experience(skills, skill_name, self.sample_truth_bank)
        assert "Software Engineer" in related
    
    def test_is_level_mismatch(self):
        """Test experience level mismatch detection."""
        # Mismatch
        assert self.suggester._is_level_mismatch("junior", "senior") == True
        assert self.suggester._is_level_mismatch("mid", "lead") == True
        
        # No mismatch
        assert self.suggester._is_level_mismatch("senior", "senior") == False
        assert self.suggester._is_level_mismatch("lead", "senior") == False
    
    def test_extract_years_requirement(self):
        """Test years requirement extraction."""
        assert self.suggester._extract_years_requirement("5+ years of experience") == 5
        assert self.suggester._extract_years_requirement("3 years required") == 3
        assert self.suggester._extract_years_requirement("No years mentioned") == 0
    
    def test_generate_suggestions_with_empty_data(self):
        """Test suggestion generation with empty data."""
        empty_resume = {
            "summary": "",
            "skills": {"technical": [], "soft_skills": []},
            "experience": [],
            "projects": [],
            "metadata": {"total_years_experience": 0}
        }
        
        empty_truth_bank = {
            "professional_facts": {"total_years_experience": 0},
            "experience_facts": {"companies_worked": []},
            "skill_facts": {"verified_technical_skills": []}
        }
        
        empty_jd = {
            "job_title": "Software Engineer",
            "parsed_content": {
                "required_skills": [],
                "preferred_skills": [],
                "responsibilities": [],
                "keywords": [],
                "role_type": {"experience_level": "unknown"}
            }
        }
        
        result = self.suggester.generate_suggestions(empty_resume, empty_truth_bank, empty_jd)
        
        # Should still produce valid structure
        assert "suggestions" in result
        assert "unsupported_requirements" in result
        assert "guardrail_violations" in result
        assert "metadata" in result
    
    def test_guardrail_prevention_fabrication(self):
        """Test that guardrails prevent fabrication."""
        # Create a scenario where user might want to fabricate experience
        limited_resume = {
            "summary": "Junior developer",
            "skills": {"technical": [{"name": "HTML", "years_of_experience": 1}], "soft_skills": []},
            "experience": [
                {
                    "title": "Junior Developer",
                    "company": "Small Co",
                    "start_date": "2022-01-01",
                    "end_date": "2023-01-01",
                    "description": "Basic web development",
                    "technologies": ["HTML", "CSS"],
                    "achievements": ["Built simple websites"]
                }
            ],
            "projects": [],
            "metadata": {"total_years_experience": 1}
        }
        
        limited_truth_bank = {
            "professional_facts": {"total_years_experience": 1},
            "experience_facts": {"companies_worked": []},
            "skill_facts": {"verified_technical_skills": []}
        }
        
        # Senior JD requiring 5+ years experience
        senior_jd = {
            "job_title": "Senior Software Engineer",
            "parsed_content": {
                "required_skills": [
                    {"skill": "Python", "category": "technical", "experience_level": "5+ years", "skill_type": "required"},
                    {"skill": "Kubernetes", "category": "technical", "experience_level": "3+ years", "skill_type": "required"}
                ],
                "preferred_skills": [],
                "responsibilities": ["Lead development team"],
                "qualifications": ["5+ years of software development experience"],
                "keywords": ["python", "kubernetes", "leadership"],
                "role_type": {"experience_level": "senior"}
            }
        }
        
        result = self.suggester.generate_suggestions(limited_resume, limited_truth_bank, senior_jd)
        
        # Should identify unsupported requirements
        unsupported = result["unsupported_requirements"]
        assert len(unsupported) > 0
        
        # Should flag experience level mismatch
        level_mismatch = [u for u in unsupported if "senior level experience" in u["requirement"].lower()]
        assert len(level_mismatch) > 0
        
        # Should flag missing required skills
        missing_skills = [u for u in unsupported if u["jd_section"] == "required_skills"]
        assert len(missing_skills) > 0
        
        # Should not suggest fabricating experience
        suggestions = result["suggestions"]
        for section_suggestions in suggestions.values():
            for suggestion in section_suggestions:
                suggested_text = f"{suggestion.get('suggested_text', '')} {suggestion.get('suggested_addition', '')}".lower()
                assert "expert in" not in suggested_text
                assert "master of" not in suggested_text
                assert "10+ years" not in suggested_text
                assert "15+ years" not in suggested_text
    
    def test_truthfulness_score_validation(self):
        """Test truthfulness score validation."""
        result = self.suggester.generate_suggestions(
            self.sample_resume,
            self.sample_truth_bank,
            self.sample_jd
        )
        
        # Check that all suggestions have truthfulness scores
        all_suggestions = []
        for section in result["suggestions"].values():
            all_suggestions.extend(section)
        
        for suggestion in all_suggestions:
            assert "truthfulness_score" in suggestion
            assert 0 <= suggestion["truthfulness_score"] <= 1.0
        
        # Check overall truthfulness score
        metadata = result["metadata"]
        assert "truthfulness_score" in metadata
        assert 0 <= metadata["truthfulness_score"] <= 1.0


if __name__ == "__main__":
    pytest.main([__file__])
