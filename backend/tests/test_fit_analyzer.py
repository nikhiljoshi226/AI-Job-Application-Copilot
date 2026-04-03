import pytest
from app.services.fit_analyzer import FitAnalyzer


class TestFitAnalyzer:
    
    def setup_method(self):
        """Setup test fixtures."""
        self.analyzer = FitAnalyzer()
        
        # Sample parsed resume
        self.sample_resume = {
            "skills": {
                "technical": [
                    {"name": "Python", "years_of_experience": 5, "evidence_source": "experience_section"},
                    {"name": "Django", "years_of_experience": 4, "evidence_source": "experience_section"},
                    {"name": "PostgreSQL", "years_of_experience": 3, "evidence_source": "experience_section"},
                    {"name": "Docker", "years_of_experience": 2, "evidence_source": "experience_section"}
                ],
                "soft_skills": [
                    {"name": "Communication", "proficiency_level": "strong", "evidence_source": "experience_section"},
                    {"name": "Leadership", "proficiency_level": "strong", "evidence_source": "experience_section"}
                ]
            },
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "start_date": "2021-01-15",
                    "end_date": "2023-03-15",
                    "current": False,
                    "description": "Led development of scalable web applications",
                    "technologies": ["Python", "Django", "PostgreSQL", "Redis", "Docker"],
                    "achievements": ["Improved application performance by 40%", "Led team of 5 engineers"]
                },
                {
                    "title": "Software Engineer",
                    "company": "StartupXYZ",
                    "start_date": "2019-03-01",
                    "end_date": "2021-01-10",
                    "current": False,
                    "description": "Developed RESTful APIs and microservices",
                    "technologies": ["Python", "Node.js", "MongoDB", "Docker"],
                    "achievements": ["Built 3 major features", "Improved system reliability"]
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
            "metadata": {
                "total_years_experience": 5
            }
        }
        
        # Sample parsed job description
        self.sample_jd = {
            "job_title": "Senior Software Engineer",
            "company": "Tech Corp",
            "parsed_content": {
                "required_skills": [
                    {
                        "skill": "Python",
                        "category": "technical",
                        "experience_level": "5+ years",
                        "evidence": "5+ years of Python experience required"
                    },
                    {
                        "skill": "Django",
                        "category": "technical",
                        "experience_level": "3+ years",
                        "evidence": "Strong knowledge of Django required"
                    },
                    {
                        "skill": "PostgreSQL",
                        "category": "technical",
                        "experience_level": "2+ years",
                        "evidence": "Experience with PostgreSQL required"
                    }
                ],
                "preferred_skills": [
                    {
                        "skill": "Docker",
                        "category": "technical",
                        "experience_level": "2+ years",
                        "evidence": "Docker experience is a plus"
                    },
                    {
                        "skill": "Kubernetes",
                        "category": "technical",
                        "experience_level": "2+ years",
                        "evidence": "Kubernetes experience is a plus"
                    }
                ],
                "responsibilities": [
                    "Design and develop scalable software solutions",
                    "Lead code reviews and mentor junior developers"
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
                }
            }
        }
    
    def test_analyze_fit_perfect_match(self):
        """Test fit analysis with perfect match."""
        result = self.analyzer.analyze_fit(self.sample_resume, self.sample_jd)
        
        # Test overall structure
        assert "fit_score" in result
        assert "skills_analysis" in result
        assert "experience_analysis" in result
        assert "role_alignment" in result
        assert "education_analysis" in result
        assert "metadata" in result
        
        # Test fit score (should be high for perfect match)
        assert result["fit_score"] >= 80
        
        # Test skills analysis
        skills_analysis = result["skills_analysis"]
        assert len(skills_analysis["matched_skills"]) >= 3  # Python, Django, PostgreSQL
        assert len(skills_analysis["missing_skills"]) == 1  # Kubernetes
        assert len(skills_analysis["partial_matches"]) >= 1  # Docker
        
        # Test matched skills
        python_skill = next((skill for skill in skills_analysis["matched_skills"] 
                            if skill["skill"].lower() == "python"), None)
        assert python_skill is not None
        assert python_skill["category"] == "technical"
        assert python_skill["jd_requirement"] == "required"
        assert python_skill["match_strength"] == "strong"
        
        # Test missing skills
        kubernetes_skill = next((skill for skill in skills_analysis["missing_skills"] 
                                if skill["skill"].lower() == "kubernetes"), None)
        assert kubernetes_skill is not None
        assert kubernetes_skill["jd_requirement"] == "preferred"
        assert kubernetes_skill["importance"] == "medium"
        
        # Test experience analysis
        experience_analysis = result["experience_analysis"]
        assert experience_analysis["level_alignment"] == "aligned"
        assert experience_analysis["years_experience_match"] == "sufficient"
        assert len(experience_analysis["relevant_experience_highlights"]) > 0
        
        # Test role alignment
        role_alignment = result["role_alignment"]
        assert role_alignment["overall_alignment"] == "strong"
        assert role_alignment["alignment_score"] >= 80
        assert len(role_alignment["strengths"]) > 0
        assert len(role_alignment["recommendations"]) > 0
        
        # Test education analysis
        education_analysis = result["education_analysis"]
        assert education_analysis["education_match"] == "meets_requirements"
        assert education_analysis["field_relevance"] == "high"
        
        # Test metadata
        metadata = result["metadata"]
        assert metadata["total_skills_analyzed"] > 0
        assert metadata["matched_skills_count"] > 0
        assert metadata["confidence_score"] > 0.8
    
    def test_analyze_fit_partial_match(self):
        """Test fit analysis with partial match."""
        # Modify resume to have fewer skills
        partial_resume = {
            "skills": {
                "technical": [
                    {"name": "Python", "years_of_experience": 3, "evidence_source": "experience_section"},
                    {"name": "JavaScript", "years_of_experience": 4, "evidence_source": "experience_section"}
                ],
                "soft_skills": [
                    {"name": "Communication", "proficiency_level": "intermediate", "evidence_source": "experience_section"}
                ]
            },
            "experience": [
                {
                    "title": "Software Engineer",
                    "company": "SmallCo",
                    "start_date": "2020-06-01",
                    "end_date": "2023-06-01",
                    "current": False,
                    "description": "Web development work",
                    "technologies": ["Python", "JavaScript", "React"],
                    "achievements": ["Built web applications"]
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Arts",
                    "field": "Marketing",
                    "university": "State University",
                    "end_date": "2019-05-31"
                }
            ],
            "metadata": {
                "total_years_experience": 3
            }
        }
        
        result = self.analyzer.analyze_fit(partial_resume, self.sample_jd)
        
        # Should have lower fit score due to missing skills
        assert result["fit_score"] < 80
        
        # Should have more missing skills
        skills_analysis = result["skills_analysis"]
        assert len(skills_analysis["missing_skills"]) > 1
        
        # Experience level should be misaligned (junior vs senior)
        experience_analysis = result["experience_analysis"]
        assert experience_analysis["level_alignment"] == "misaligned"
        
        # Education should be below requirements
        education_analysis = result["education_analysis"]
        assert education_analysis["education_match"] == "below_requirements"
        assert len(education_analysis["additional_education_needed"]) > 0
    
    def test_extract_resume_skills(self):
        """Test resume skills extraction."""
        skills = self.analyzer._extract_resume_skills(self.sample_resume)
        
        assert len(skills) > 0
        
        # Check technical skills
        python_skill = next((skill for skill in skills if skill["skill"] == "python"), None)
        assert python_skill is not None
        assert python_skill["category"] == "technical"
        assert python_skill["experience_level"] == 5
        
        # Check soft skills
        communication_skill = next((skill for skill in skills if skill["skill"] == "communication"), None)
        assert communication_skill is not None
        assert communication_skill["category"] == "soft"
    
    def test_extract_jd_skills(self):
        """Test job description skills extraction."""
        skills = self.analyzer._extract_jd_skills(self.sample_jd)
        
        assert "required" in skills
        assert "preferred" in skills
        assert len(skills["required"]) > 0
        assert len(skills["preferred"]) > 0
        
        # Check required skills
        python_skill = next((skill for skill in skills["required"] if skill["skill"] == "python"), None)
        assert python_skill is not None
        assert python_skill["category"] == "technical"
        
        # Check preferred skills
        docker_skill = next((skill for skill in skills["preferred"] if skill["skill"] == "docker"), None)
        assert docker_skill is not None
    
    def test_find_skill_match(self):
        """Test skill matching logic."""
        resume_skills = self.analyzer._extract_resume_skills(self.sample_resume)
        jd_skills = self.analyzer._extract_jd_skills(self.sample_jd)
        
        # Test exact match
        jd_skill = jd_skills["required"][0]  # Python
        match_result = self.analyzer._find_skill_match(jd_skill, resume_skills, "required")
        
        assert match_result["match_type"] == "exact"
        assert match_result["skill"] == "Python"
        assert match_result["jd_requirement"] == "required"
        assert match_result["match_strength"] == "strong"
        
        # Test no match
        jd_skill = {"skill": "nonexistent", "category": "technical", "experience_level": "not specified"}
        match_result = self.analyzer._find_skill_match(jd_skill, resume_skills, "required")
        assert match_result["match_type"] == "none"
    
    def test_are_similar_skills(self):
        """Test similar skills detection."""
        # Test exact match
        assert self.analyzer._are_similar_skills("python", "python") == True
        
        # Test similar variants
        assert self.analyzer._are_similar_skills("python", "django") == True
        assert self.analyzer._are_similar_skills("docker", "container") == True
        assert self.analyzer._are_similar_skills("aws", "amazon web services") == True
        
        # Test non-similar
        assert self.analyzer._are_similar_skills("python", "java") == False
        assert self.analyzer._are_similar_skills("react", "vue") == False
    
    def test_determine_match_strength(self):
        """Test match strength determination."""
        jd_skill = {"experience_level": "5+ years"}
        resume_skill = {"experience_level": 5}
        
        # Test strong match
        strength = self.analyzer._determine_match_strength(jd_skill, resume_skill)
        assert strength == "strong"
        
        # Test weak match
        resume_skill = {"experience_level": 1}
        strength = self.analyzer._determine_match_strength(jd_skill, resume_skill)
        assert strength == "weak"
        
        # Test level indicators
        jd_skill = {"experience_level": "senior level"}
        resume_skill = {"experience_level": "senior"}
        strength = self.analyzer._determine_match_strength(jd_skill, resume_skill)
        assert strength == "strong"
    
    def test_extract_experience_level(self):
        """Test experience level extraction."""
        # Test years patterns
        assert self.analyzer._extract_experience_level("5+ years of Python experience") == "5+ years"
        assert self.analyzer._extract_experience_level("3 years of experience") == "3+ years"
        
        # Test level indicators
        assert self.analyzer._extract_experience_level("Senior developer position") == "senior level"
        assert self.analyzer._extract_experience_level("Junior developer role") == "junior level"
        assert self.analyzer._extract_experience_level("Python development skills") == "not specified"
    
    def test_calculate_total_years_experience(self):
        """Test total years experience calculation."""
        experience = [
            {
                "start_date": "2021-01-15",
                "end_date": "2023-03-15"
            },
            {
                "start_date": "2019-03-01",
                "end_date": "2021-01-10"
            }
        ]
        
        years = self.analyzer._calculate_total_years_experience(experience)
        assert years == 4  # 2021-2023 is 2 years, 2019-2021 is ~2 years, max is 4
    
    def test_find_relevant_experience(self):
        """Test relevant experience identification."""
        experience = self.sample_resume["experience"]
        jd_keywords = self.sample_jd["parsed_content"]["keywords"]
        
        highlights = self.analyzer._find_relevant_experience(experience, self.sample_jd)
        
        assert len(highlights) > 0
        
        # Should find the Senior Software Engineer role as highly relevant
        senior_role = next((h for h in highlights if "Senior Software Engineer" in h["experience"]), None)
        assert senior_role is not None
        assert senior_role["relevance_score"] > 0.5
    
    def test_identify_experience_gaps(self):
        """Test experience gap identification."""
        experience = self.sample_resume["experience"]
        jd_requirements = self.sample_jd["parsed_content"]["qualifications"]
        
        gaps = self.analyzer._identify_experience_gaps(experience, jd_requirements)
        
        # Should identify some gaps (e.g., no enterprise experience)
        assert len(gaps) >= 0
        
        for gap in gaps:
            assert "gap" in gap
            assert "impact" in gap
            assert "suggestion" in gap
    
    def test_calculate_role_alignment_score(self):
        """Test role alignment score calculation."""
        skills_analysis = {
            "matched_skills": [{"skill": "Python"}, {"skill": "Django"}],
            "missing_skills": [{"skill": "Kubernetes"}],
            "partial_matches": []
        }
        
        experience_analysis = {
            "level_alignment": "aligned",
            "years_experience_match": "sufficient",
            "relevant_experience_highlights": [
                {"relevance_score": 0.8},
                {"relevance_score": 0.6}
            ],
            "experience_gaps": []
        }
        
        score = self.analyzer._calculate_role_alignment_score(skills_analysis, experience_analysis)
        
        assert 0 <= score <= 100
        assert score > 50  # Should be reasonably high for this example
    
    def test_identify_strengths(self):
        """Test strengths identification."""
        skills_analysis = {
            "matched_skills": [{"skill": "Python"}, {"skill": "Django"}, {"skill": "PostgreSQL"}],
            "missing_skills": [{"skill": "Kubernetes"}]
        }
        
        experience_analysis = {
            "level_alignment": "aligned",
            "years_experience_match": "sufficient",
            "relevant_experience_highlights": [
                {"relevance_score": 0.9}
            ]
        }
        
        strengths = self.analyzer._identify_strengths(skills_analysis, experience_analysis)
        
        assert len(strengths) > 0
        assert any("Strong technical background" in s for s in strengths)
    
    def test_identify_concerns(self):
        """Test concerns identification."""
        skills_analysis = {
            "matched_skills": [{"skill": "Python"}],
            "missing_skills": [
                {"skill": "Kubernetes", "jd_requirement": "required"},
                {"skill": "AWS", "jd_requirement": "required"}
            ]
        }
        
        experience_analysis = {
            "level_alignment": "misaligned",
            "years_experience_match": "insufficient",
            "experience_gaps": [{"impact": "high"}]
        }
        
        concerns = self.analyzer._identify_concerns(skills_analysis, experience_analysis)
        
        assert len(concerns) > 0
        assert any("Missing" in c for c in concerns)
    
    def test_generate_recommendations(self):
        """Test recommendations generation."""
        concerns = [
            "Missing several required skills",
            "Insufficient years of experience",
            "No cloud experience"
        ]
        
        recommendations = self.analyzer._generate_recommendations(concerns, self.sample_jd)
        
        assert len(recommendations) > 0
        assert any("skill development" in r for r in recommendations)
    
    def test_analyze_education(self):
        """Test education analysis."""
        education_analysis = self.analyzer._analyze_education(self.sample_resume, self.sample_jd)
        
        assert "education_match" in education_analysis
        assert "degree_alignment" in education_analysis
        assert "field_relevance" in education_analysis
        assert "additional_education_needed" in education_analysis
    
    def test_calculate_confidence_score(self):
        """Test confidence score calculation."""
        analysis = {
            "metadata": {
                "total_skills_analyzed": 10,
                "matched_skills_count": 8,
                "confidence_score": 0.85
            },
            "experience_analysis": {
                "level_alignment": "aligned"
            },
            "role_alignment": {
                "alignment_score": 85
            }
        }
        
        confidence = self.analyzer._calculate_confidence_score(analysis)
        
        assert 0 <= confidence <= 1.0
        assert confidence > 0.5  # Should be reasonably confident
    
    def test_analyze_fit_empty_data(self):
        """Test fit analysis with empty data."""
        empty_resume = {
            "skills": {"technical": [], "soft_skills": []},
            "experience": [],
            "education": [],
            "metadata": {"total_years_experience": 0}
        }
        
        empty_jd = {
            "job_title": "Software Engineer",
            "company": "Tech Corp",
            "parsed_content": {
                "required_skills": [],
                "preferred_skills": [],
                "responsibilities": [],
                "qualifications": [],
                "keywords": [],
                "role_type": {"experience_level": "unknown"}
            }
        }
        
        result = self.analyzer.analyze_fit(empty_resume, empty_jd)
        
        # Should still produce valid structure
        assert "fit_score" in result
        assert result["fit_score"] == 0.0  # No skills to match
        assert "skills_analysis" in result
        assert "experience_analysis" in result
        assert "role_alignment" in result
        assert "education_analysis" in result


if __name__ == "__main__":
    pytest.main([__file__])
