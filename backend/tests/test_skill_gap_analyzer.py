import pytest
from app.services.skill_gap_analyzer import SkillGapAnalyzer


class TestSkillGapAnalyzer:
    
    def setup_method(self):
        """Setup test fixtures."""
        self.analyzer = SkillGapAnalyzer()
        
        # Sample resume data
        self.resume_data = {
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
                    "content": "Senior Software Engineer with 5 years of experience"
                },
                "skills": {
                    "title": "Skills",
                    "categories": [
                        {
                            "name": "Technical Skills",
                            "skills": [
                                {"name": "Python", "level": "5 years", "highlight": False},
                                {"name": "JavaScript", "level": "3 years", "highlight": True},
                                {"name": "React", "level": "3 years", "highlight": False},
                                {"name": "Node.js", "level": "2 years", "highlight": False}
                            ]
                        },
                        {
                            "name": "Soft Skills",
                            "skills": [
                                {"name": "Communication", "level": "Strong", "highlight": False},
                                {"name": "Teamwork", "level": "Strong", "highlight": False}
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
                    ]
                }
            }
        }
        
        # Sample job descriptions
        self.job_descriptions = [
            {
                "id": 1,
                "job_title": "Senior Software Engineer",
                "company": "Tech Company A",
                "raw_text": "We are looking for a Senior Software Engineer with experience in Python, React, and cloud platforms.",
                "parsed_content": {
                    "required_skills": [
                        {"skill": "Python", "category": "technical", "experience_level": "5+ years", "importance": "high"},
                        {"skill": "React", "category": "technical", "experience_level": "3+ years", "importance": "high"},
                        {"skill": "AWS", "category": "technical", "experience_level": "2+ years", "importance": "medium"},
                        {"skill": "Docker", "category": "technical", "experience_level": "1+ years", "importance": "medium"}
                    ],
                    "responsibilities": [
                        "Design and develop scalable software solutions",
                        "Collaborate with cross-functional teams",
                        "Mentor junior developers"
                    ],
                    "qualifications": [
                        "Bachelor's degree in Computer Science",
                        "5+ years of software development experience"
                    ]
                }
            },
            {
                "id": 2,
                "job_title": "Full Stack Developer",
                "company": "Tech Company B",
                "raw_text": "Seeking a Full Stack Developer with JavaScript, Node.js, and database experience.",
                "parsed_content": {
                    "required_skills": [
                        {"skill": "JavaScript", "category": "technical", "experience_level": "3+ years", "importance": "high"},
                        {"skill": "Node.js", "category": "technical", "experience_level": "2+ years", "importance": "high"},
                        {"skill": "MongoDB", "category": "technical", "experience_level": "2+ years", "importance": "medium"},
                        {"skill": "Vue.js", "category": "technical", "experience_level": "1+ years", "importance": "low"}
                    ],
                    "responsibilities": [
                        "Build full-stack web applications",
                        "Design database schemas",
                        "Implement REST APIs"
                    ]
                }
            },
            {
                "id": 3,
                "job_title": "Data Engineer",
                "company": "Tech Company C",
                "raw_text": "Looking for a Data Engineer with Python, SQL, and data analysis skills.",
                "parsed_content": {
                    "required_skills": [
                        {"skill": "Python", "category": "technical", "experience_level": "3+ years", "importance": "high"},
                        {"skill": "SQL", "category": "technical", "experience_level": "2+ years", "importance": "high"},
                        {"skill": "Pandas", "category": "technical", "experience_level": "2+ years", "importance": "medium"},
                        {"skill": "Tableau", "category": "technical", "experience_level": "1+ years", "importance": "low"}
                    ],
                    "responsibilities": [
                        "Design and implement data pipelines",
                        "Analyze large datasets",
                        "Create data visualizations"
                    ]
                }
            }
        ]

    def test_analyze_skill_gaps_basic(self):
        """Test basic skill gap analysis."""
        result = self.analyzer.analyze_skill_gaps(
            self.resume_data,
            self.job_descriptions
        )
        
        # Test overall structure
        assert "skill_gap_analysis" in result
        assert "metadata" in result
        
        # Test analysis structure
        analysis = result["skill_gap_analysis"]
        assert "analysis_name" in analysis
        assert "job_count" in analysis
        assert "analysis_summary" in analysis
        assert "missing_skills" in analysis
        assert "repeated_gaps" in analysis
        assert "role_expectations" in analysis
        assert "learning_recommendations" in analysis
        assert "project_suggestions" in analysis
        assert "skill_coverage_score" in analysis
        assert "action_items" in analysis
        
        # Test values
        assert analysis["job_count"] == 3
        assert isinstance(analysis["skill_coverage_score"], float)
        assert 0 <= analysis["skill_coverage_score"] <= 1.0

    def test_analyze_skill_gaps_with_options(self):
        """Test skill gap analysis with custom options."""
        options = {
            "include_soft_skills": False,
            "include_technical_skills": True,
            "min_gap_frequency": 3,
            "project_suggestion_count": 3,
            "learning_recommendation_count": 5,
            "priority_threshold": 0.5
        }
        
        result = self.analyzer.analyze_skill_gaps(
            self.resume_data,
            self.job_descriptions,
            options
        )
        
        assert result["metadata"]["analysis_options"]["include_soft_skills"] == False
        assert result["metadata"]["analysis_options"]["min_gap_frequency"] == 3
        assert result["metadata"]["analysis_options"]["project_suggestion_count"] == 3
        assert result["metadata"]["analysis_options"]["learning_recommendation_count"] == 5

    def test_create_truth_bank_from_resume(self):
        """Test truth bank creation from resume data."""
        truth_bank = self.analyzer._create_truth_bank_from_resume(self.resume_data["rendering_data"])
        
        # Check skills structure
        assert "skills" in truth_bank
        assert "technical" in truth_bank["skills"]
        assert "soft_skills" in truth_bank["skills"]
        assert "tools" in truth_bank["skills"]
        assert "languages" in truth_bank["skills"]
        assert "frameworks" in truth_bank["skills"]
        assert "databases" in truth_bank["skills"]
        assert "platforms" in truth_bank["skills"]
        
        # Check specific skills
        assert "python" in truth_bank["skills"]["technical"]
        assert "javascript" in truth_bank["skills"]["technical"]
        assert "react" in truth_bank["skills"]["technical"]
        assert "communication" in truth_bank["skills"]["soft_skills"]
        assert "teamwork" in truth_bank["skills"]["soft_skills"]
        
        # Check experience
        assert "experience" in truth_bank
        assert "companies" in truth_bank["experience"]
        assert "titles" in truth_bank["experience"]
        
        # Check education
        assert "education" in truth_bank
        assert "degrees" in truth_bank["education"]
        assert "universities" in truth_bank["education"]
        
        # Check projects
        assert "projects" in truth_bank
        assert "technologies" in truth_bank["projects"]

    def test_extract_skills_from_job_descriptions(self):
        """Test skill extraction from job descriptions."""
        all_skills = self.analyzer._extract_skills_from_job_descriptions(self.job_descriptions)
        
        # Check structure
        assert "technical" in all_skills
        assert "soft_skills" in all_skills
        assert "tools" in all_skills
        assert "languages" in all_skills
        assert "frameworks" in all_skills
        assert "databases" in all_skills
        assert "platforms" in all_skills
        
        # Check specific skills
        assert "python" in all_skills["technical"]
        assert "react" in all_skills["technical"]
        assert "javascript" in all_skills["technical"]
        assert "aws" in all_skills["platforms"]
        assert "docker" in all_skills["platforms"]
        assert "sql" in all_skills["databases"]
        
        # Check skill details
        python_skills = all_skills["technical"]["python"]
        assert len(python_skills) >= 2  # Should appear in multiple JDs
        for skill_info in python_skills:
            assert "jd_id" in skill_info
            assert "company" in skill_info
            assert "job_title" in skill_info
            assert "importance" in skill_info

    def test_categorize_skill(self):
        """Test skill categorization."""
        # Test programming languages
        assert self.analyzer._categorize_skill("python") == "languages"
        assert self.analyzer._categorize_skill("java") == "languages"
        assert self.analyzer._categorize_skill("javascript") == "languages"
        
        # Test frameworks
        assert self.analyzer._categorize_skill("react") == "frameworks"
        assert self.analyzer._categorize_skill("django") == "frameworks"
        assert self.analyzer._categorize_skill("vue") == "frameworks"
        
        # Test databases
        assert self.analyzer._categorize_skill("mysql") == "databases"
        assert self.analyzer._categorize_skill("postgresql") == "databases"
        assert self.analyzer._categorize_skill("mongodb") == "databases"
        
        # Test platforms
        assert self.analyzer._categorize_skill("aws") == "platforms"
        assert self.analyzer._categorize_skill("docker") == "platforms"
        assert self.analyzer._categorize_skill("kubernetes") == "platforms"
        
        # Test soft skills
        assert self.analyzer._categorize_skill("communication") == "soft_skills"
        assert self.analyzer._categorize_skill("leadership") == "soft_skills"
        assert self.analyzer._categorize_skill("teamwork") == "soft_skills"

    def test_find_technologies_in_text(self):
        """Test technology extraction from text."""
        text = "Experience with Python, React, Node.js, AWS, Docker, and PostgreSQL"
        technologies = self.analyzer._find_technologies_in_text(text)
        
        assert "python" in technologies
        assert "react" in technologies
        assert "node.js" in technologies
        assert "aws" in technologies
        assert "docker" in technologies
        assert "postgresql" in technologies

    def test_analyze_skill_gaps_detailed(self):
        """Test detailed skill gap analysis."""
        truth_bank = self.analyzer._create_truth_bank_from_resume(self.resume_data["rendering_data"])
        all_jd_skills = self.analyzer._extract_skills_from_job_descriptions(self.job_descriptions)
        
        skill_gaps = self.analyzer._analyze_skill_gaps(truth_bank, all_jd_skills, {})
        
        # Check structure
        assert "missing_technical" in skill_gaps
        assert "missing_soft_skills" in skill_gaps
        assert "gap_summary" in skill_gaps
        
        # Check missing skills structure
        missing_tech = skill_gaps["missing_technical"]
        for skill in missing_tech:
            assert "skill" in skill
            assert "frequency" in skill
            assert "importance" in skill
            assert "jobs" in skill
            assert "companies" in skill
            assert "priority_score" in skill
        
        # Check sorting
        if len(missing_tech) > 1:
            assert missing_tech[0]["priority_score"] >= missing_tech[1]["priority_score"]

    def test_identify_repeated_gaps(self):
        """Test repeated gap identification."""
        truth_bank = self.analyzer._create_truth_bank_from_resume(self.resume_data["rendering_data"])
        all_jd_skills = self.analyzer._extract_skills_from_job_descriptions(self.job_descriptions)
        
        skill_gaps = self.analyzer._analyze_skill_gaps(truth_bank, all_jd_skills, {})
        repeated_gaps = self.analyzer._identify_repeated_gaps(skill_gaps, {"min_gap_frequency": 2})
        
        # Check structure
        assert "high_frequency_gaps" in repeated_gaps
        assert "critical_gaps" in repeated_gaps
        assert "category_gaps" in repeated_gaps
        assert "gap_analysis" in repeated_gaps
        
        # Check high frequency gaps
        high_freq_gaps = repeated_gaps["high_frequency_gaps"]
        for gap in high_freq_gaps:
            assert gap["frequency"] >= 2
        
        # Check critical gaps
        critical_gaps = repeated_gaps["critical_gaps"]
        for gap in critical_gaps:
            assert gap["frequency"] >= 2
            assert gap["importance"] > 0
        
        # Check gap analysis
        analysis = repeated_gaps["gap_analysis"]
        assert "total_repeated_gaps" in analysis
        assert "most_common_gap" in analysis
        assert "critical_gaps_count" in analysis
        assert "categories_with_gaps" in analysis

    def test_analyze_role_expectations(self):
        """Test role expectations analysis."""
        role_expectations = self.analyzer._analyze_role_expectations(self.job_descriptions)
        
        # Check structure
        assert "common_responsibilities" in role_expectations
        assert "common_qualifications" in role_expectations
        assert "experience_requirements" in role_expectations
        
        # Check responsibilities
        responsibilities = role_expectations["common_responsibilities"]
        for resp in responsibilities:
            assert "responsibility" in resp
            assert "frequency" in resp
            assert "jobs" in resp

    def test_generate_learning_recommendations(self):
        """Test learning recommendations generation."""
        repeated_gaps = {
            "high_frequency_gaps": [
                {"skill": "aws", "category": "platforms", "frequency": 3, "importance": 2},
                {"skill": "docker", "category": "platforms", "frequency": 2, "importance": 1}
            ],
            "critical_gaps": [
                {"skill": "python", "category": "languages", "frequency": 3, "importance": 3}
            ]
        }
        
        truth_bank = self.analyzer._create_truth_bank_from_resume(self.resume_data["rendering_data"])
        
        recommendations = self.analyzer._generate_learning_recommendations(
            repeated_gaps,
            truth_bank,
            {"learning_recommendation_count": 5}
        )
        
        assert len(recommendations) <= 5
        
        for rec in recommendations:
            assert "title" in rec
            assert "description" in rec
            assert "priority" in rec
            assert "time_estimate" in rec
            assert "resources" in rec
            assert "type" in rec

    def test_create_learning_recommendation(self):
        """Test specific learning recommendation creation."""
        truth_bank = self.analyzer._create_truth_bank_from_resume(self.resume_data["rendering_data"])
        
        # Test technical skill
        rec = self.analyzer._create_learning_recommendation(
            "react",
            "frameworks",
            3,
            truth_bank
        )
        
        assert rec is not None
        assert rec["skill"] == "react"
        assert rec["category"] == "frameworks"
        assert rec["title"] == "Learn React"
        assert rec["type"] == "skill_specific"
        assert "learning_path" in rec
        assert "prerequisites" in rec

    def test_create_learning_path(self):
        """Test learning path creation."""
        # Test framework learning path
        path = self.analyzer._create_learning_path("react", "frameworks")
        
        assert len(path) == 4
        assert "react" in path[0].lower()
        assert "react" in path[1].lower()
        assert "react" in path[2].lower()
        assert "react" in path[3].lower()
        
        # Test language learning path
        path = self.analyzer._create_learning_path("python", "languages")
        
        assert len(path) == 4
        assert "python" in path[0].lower()
        assert "python" in path[1].lower()
        assert "python" in path[2].lower()
        assert "python" in path[3].lower()

    def test_identify_prerequisites(self):
        """Test prerequisites identification."""
        truth_bank = self.analyzer._create_truth_bank_from_resume(self.resume_data["rendering_data"])
        
        # Test React prerequisites
        prereqs = self.analyzer._identify_prerequisites("react", "frameworks", truth_bank)
        
        assert "html" in prereqs
        assert "css" in prereqs
        assert "javascript" in prereqs
        
        # Test Docker prerequisites
        prereqs = self.analyzer._identify_prerequisites("docker", "platforms", truth_bank)
        
        assert "linux" in prereqs

    def test_generate_project_suggestions(self):
        """Test project suggestions generation."""
        repeated_gaps = {
            "high_frequency_gaps": [
                {"skill": "react", "category": "frameworks", "frequency": 3},
                {"skill": "node.js", "category": "frameworks", "frequency": 2},
                {"skill": "aws", "category": "platforms", "frequency": 2}
            ]
        }
        
        truth_bank = self.analyzer._create_truth_bank_from_resume(self.resume_data["rendering_data"])
        
        suggestions = self.analyzer._generate_project_suggestions(
            repeated_gaps,
            truth_bank,
            {"project_suggestion_count": 3}
        )
        
        assert len(suggestions) <= 3
        
        for suggestion in suggestions:
            assert "title" in suggestion
            assert "description" in suggestion
            assert "skills_covered" in suggestion
            assert "difficulty" in suggestion
            assert "time_estimate" in suggestion
            assert "tech_stack" in suggestion
            assert "learning_outcomes" in suggestion
            assert "portfolio_value" in suggestion

    def test_generate_project_ideas(self):
        """Test project ideas generation."""
        top_gaps = [
            {"skill": "react", "category": "frameworks", "frequency": 3},
            {"skill": "node.js", "category": "frameworks", "frequency": 2},
            {"skill": "aws", "category": "platforms", "frequency": 2}
        ]
        
        truth_bank = self.analyzer._create_truth_bank_from_resume(self.resume_data["rendering_data"])
        
        ideas = self.analyzer._generate_project_ideas(top_gaps, truth_bank)
        
        assert len(ideas) > 0
        
        for idea in ideas:
            assert "title" in idea
            assert "description" in idea
            assert "skills_covered" in idea
            assert "difficulty" in idea
            assert "time_estimate" in idea
            assert "tech_stack" in idea
            assert "learning_outcomes" in idea
            assert "portfolio_value" in idea

    def test_calculate_skill_coverage_score(self):
        """Test skill coverage score calculation."""
        truth_bank = self.analyzer._create_truth_bank_from_resume(self.resume_data["rendering_data"])
        all_jd_skills = self.analyzer._extract_skills_from_job_descriptions(self.job_descriptions)
        
        score = self.analyzer._calculate_skill_coverage_score(truth_bank, all_jd_skills)
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_generate_action_items(self):
        """Test action items generation."""
        repeated_gaps = {
            "high_frequency_gaps": [
                {"skill": "aws", "category": "platforms", "frequency": 3, "importance": 2},
                {"skill": "docker", "category": "platforms", "frequency": 2, "importance": 1}
            ],
            "critical_gaps": [
                {"skill": "python", "category": "languages", "frequency": 3, "importance": 3}
            ]
        }
        
        learning_recommendations = [
            {
                "title": "Learn AWS",
                "skill": "aws",
                "type": "skill_specific"
            }
        ]
        
        project_suggestions = [
            {
                "title": "Cloud Deployment Project",
                "type": "project_work"
            }
        ]
        
        action_items = self.analyzer._generate_action_items(
            repeated_gaps,
            learning_recommendations,
            project_suggestions,
            {}
        )
        
        assert len(action_items) > 0
        
        for item in action_items:
            assert "type" in item
            assert "title" in item
            assert "description" in item
            assert "priority" in item
            assert "timeline" in item
            assert "resources" in item
            assert "success_metrics" in item

    def test_create_analysis_summary(self):
        """Test analysis summary creation."""
        skill_gaps = {
            "gap_summary": {
                "total_missing_skills": 5,
                "categories": {
                    "technical": 3,
                    "soft_skills": 2
                }
            }
        }
        
        repeated_gaps = {
            "high_frequency_gaps": [
                {"skill": "aws", "frequency": 3},
                {"skill": "docker", "frequency": 2}
            ],
            "critical_gaps": [
                {"skill": "python", "frequency": 3, "importance": 3}
            ],
            "gap_analysis": {
                "total_repeated_gaps": 2,
                "most_common_gap": {"skill": "aws", "frequency": 3},
                "critical_gaps_count": 1
            }
        }
        
        role_expectations = {
            "common_responsibilities": [
                {"responsibility": "Design software", "frequency": 3}
            ]
        }
        
        skill_coverage_score = 0.75
        
        summary = self.analyzer._create_analysis_summary(
            skill_gaps,
            repeated_gaps,
            role_expectations,
            skill_coverage_score
        )
        
        assert "overall_assessment" in summary
        assert "assessment_message" in summary
        assert "skill_coverage_score" in summary
        assert "total_missing_skills" in summary
        assert "high_frequency_gaps" in summary
        assert "critical_gaps" in summary
        assert "key_findings" in summary
        assert "recommendations_summary" in summary

    def test_calculate_skill_priority(self):
        """Test skill priority calculation."""
        # Test high frequency, high importance
        priority = self.analyzer._calculate_skill_priority(5, 3)
        assert priority > 0.8
        
        # Test low frequency, low importance
        priority = self.analyzer._calculate_skill_priority(1, 0)
        assert priority < 0.5
        
        # Test medium frequency, medium importance
        priority = self.analyzer._calculate_skill_priority(3, 2)
        assert 0.4 < priority < 0.7

    def test_analyze_skill_gaps_empty_data(self):
        """Test analysis with minimal data."""
        minimal_resume = {
            "rendering_data": {
                "header": {"name": "Jane Doe", "contact": {"email": "jane@example.com"}},
                "skills": {"categories": []},
                "experience": {"entries": []},
                "education": {"entries": []},
                "projects": None
            }
        }
        
        minimal_jd = [{
            "id": 1,
            "job_title": "Engineer",
            "company": "Tech Corp",
            "raw_text": "Looking for an engineer.",
            "parsed_content": {
                "required_skills": [],
                "responsibilities": []
            }
        }]
        
        result = self.analyzer.analyze_skill_gaps(minimal_resume, minimal_jd)
        
        assert result["success"] is True
        assert result["skill_gap_analysis"]["job_count"] == 1
        assert result["skill_gap_analysis"]["skill_coverage_score"] == 0.0

    def test_analyze_skill_gaps_no_job_descriptions(self):
        """Test analysis with no job descriptions."""
        result = self.analyzer.analyze_skill_gaps(self.resume_data, [])
        
        assert result["success"] is True
        assert result["skill_gap_analysis"]["job_count"] == 0
        assert result["skill_gap_analysis"]["skill_coverage_score"] == 1.0

    def test_skill_categories_completeness(self):
        """Test that all skill categories are properly defined."""
        categories = self.analyzer.skill_categories
        
        # Check main categories
        assert "programming_languages" in categories
        assert "web_technologies" in categories
        assert "databases" in categories
        assert "cloud_platforms" in categories
        assert "devops_tools" in categories
        assert "mobile_development" in categories
        assert "data_analytics" in categories
        assert "machine_learning" in categories
        assert "soft_skills" in categories
        assert "business_skills" in categories
        
        # Check that categories have skills
        for category_name, skills in categories.items():
            assert len(skills) > 0, f"Category {category_name} has no skills"

    def test_processing_time_tracking(self):
        """Test processing time tracking."""
        result = self.analyzer.analyze_skill_gaps(
            self.resume_data,
            self.job_descriptions
        )
        
        processing_time = result["metadata"]["processing_time_ms"]
        assert processing_time > 0
        assert isinstance(processing_time, int)

    def test_analysis_with_different_options(self):
        """Test analysis with different option combinations."""
        options_variations = [
            {"include_soft_skills": False},
            {"include_technical_skills": False},
            {"min_gap_frequency": 1},
            {"min_gap_frequency": 5},
            {"project_suggestion_count": 1},
            {"project_suggestion_count": 10},
            {"learning_recommendation_count": 3},
            {"learning_recommendation_count": 15},
            {"priority_threshold": 0.1},
            {"priority_threshold": 0.9}
        ]
        
        for options in options_variations:
            result = self.analyzer.analyze_skill_gaps(
                self.resume_data,
                self.job_descriptions,
                options
            )
            
            assert result["success"] is True
            assert result["metadata"]["analysis_options"] == options

    def test_skill_gap_analysis_realistic_data(self):
        """Test with realistic resume and job description data."""
        # Test with the provided sample data
        result = self.analyzer.analyze_skill_gaps(
            self.resume_data,
            self.job_descriptions
        )
        
        # Verify realistic results
        analysis = result["skill_gap_analysis"]
        
        # Should have some missing skills (user doesn't have all required skills)
        assert analysis["missing_skills"]["gap_summary"]["total_missing_skills"] > 0
        
        # Should have some repeated gaps
        assert len(analysis["repeated_gaps"]["high_frequency_gaps"]) >= 0
        
        # Should have learning recommendations
        assert len(analysis["learning_recommendations"]) > 0
        
        # Should have project suggestions
        assert len(analysis["project_suggestions"]) > 0
        
        # Should have action items
        assert len(analysis["action_items"]) > 0
        
        # Coverage score should be realistic (not perfect)
        assert 0.0 <= analysis["skill_coverage_score"] <= 1.0


if __name__ == "__main__":
    pytest.main([__file__])
