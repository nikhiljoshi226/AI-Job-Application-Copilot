import pytest
from app.services.interview_prep_generator import InterviewPrepGenerator


class TestInterviewPrepGenerator:
    
    def setup_method(self):
        """Setup test fixtures."""
        self.generator = InterviewPrepGenerator()
        
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
                                {"name": "React", "level": "3 years", "highlight": False},
                                {"name": "PostgreSQL", "level": "3 years", "highlight": False}
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
                                "Led team of 3 junior developers",
                                "Implemented CI/CD pipeline reducing deployment time by 50%"
                            ],
                            "technologies": ["Python", "Django", "React", "PostgreSQL", "Docker"]
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
        
        # Sample job description data
        self.job_description_data = {
            "parsed_content": {
                "job_title": "Senior Software Engineer",
                "company": "Enterprise Corp",
                "required_skills": [
                    {"skill": "Python", "category": "technical", "experience_level": "5+ years"},
                    {"skill": "Django", "category": "technical", "experience_level": "3+ years"},
                    {"skill": "React", "category": "technical", "experience_level": "2+ years"},
                    {"skill": "PostgreSQL", "category": "technical", "experience_level": "2+ years"}
                ],
                "responsibilities": [
                    "Design and develop scalable software solutions",
                    "Lead code reviews and mentor junior developers",
                    "Collaborate with cross-functional teams"
                ]
            },
            "raw_text": "We are looking for a Senior Software Engineer to join our team at Enterprise Corp. Contact Hiring Manager Jane Smith at jane.smith@enterprisecorp.com.",
            "job_title": "Senior Software Engineer",
            "company": "Enterprise Corp"
        }

    def test_generate_interview_prep_basic(self):
        """Test basic interview prep generation."""
        result = self.generator.generate_interview_prep(
            self.tailored_resume_data,
            self.job_description_data
        )
        
        # Test overall structure
        assert "interview_prep" in result
        assert "metadata" in result
        assert "validation" in result
        assert "sources" in result
        
        # Test interview prep structure
        interview_prep = result["interview_prep"]
        assert "interview_context" in interview_prep
        assert "questions" in interview_prep
        assert "star_stories" in interview_prep
        assert "preparation_guide" in interview_prep
        assert "content_summary" in interview_prep
        
        # Test metadata
        metadata = result["metadata"]
        assert metadata["truthfulness_score"] >= 0.0
        assert metadata["truthfulness_score"] <= 1.0
        assert metadata["content_quality_score"] >= 0.0
        assert metadata["content_quality_score"] <= 1.0
        assert metadata["personalization_score"] >= 0.0
        assert metadata["personalization_score"] <= 1.0
        assert "processing_time_ms" in metadata

    def test_generate_interview_prep_with_options(self):
        """Test interview prep generation with custom options."""
        options = {
            "interview_type": "technical",
            "question_count": 20,
            "include_behavioral": False,
            "include_technical": True,
            "include_situational": False,
            "star_story_count": 10,
            "difficulty_level": "hard"
        }
        
        result = self.generator.generate_interview_prep(
            self.tailored_resume_data,
            self.job_description_data,
            options
        )
        
        assert result["metadata"]["generation_options"]["interview_type"] == "technical"
        assert result["metadata"]["generation_options"]["question_count"] == 20
        assert result["metadata"]["generation_options"]["difficulty_level"] == "hard"
        
        # Check that only technical questions were generated
        questions = result["interview_prep"]["questions"]
        question_types = set(q.get("type") for q in questions)
        assert "technical" in question_types
        assert "behavioral" not in question_types
        assert "situational" not in question_types

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
        assert "Django" in truth_bank["skills"]["technical"]
        assert "Communication" in truth_bank["skills"]["soft_skills"]
        
        # Check education
        assert "Bachelor of Science" in truth_bank["education"]["degrees"]
        assert "State University" in truth_bank["education"]["universities"]
        
        # Check projects
        assert "E-commerce Platform" in truth_bank["experience"]["projects"]
        assert "React" in truth_bank["experience"]["technologies"]

    def test_generate_interview_questions(self):
        """Test interview question generation."""
        questions = self.generator._generate_interview_questions(
            self.tailored_resume_data,
            self.job_description_data,
            {"question_count": 10},
            {}
        )
        
        assert len(questions) <= 10  # Should not exceed requested count
        
        # Check question structure
        for question in questions:
            assert "id" in question
            assert "type" in question
            assert "category" in question
            assert "question" in question
            assert "focus_area" in question
            assert "difficulty" in question
        
        # Check question types
        question_types = set(q.get("type") for q in questions)
        assert len(question_types) >= 2  # Should have multiple types

    def test_generate_behavioral_questions(self):
        """Test behavioral question generation."""
        questions = self.generator._generate_behavioral_questions(
            self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"]),
            5
        )
        
        assert len(questions) <= 5
        
        for question in questions:
            assert question["type"] == "behavioral"
            assert question["question"] is not None
            assert question["difficulty"] == "medium"

    def test_generate_technical_questions(self):
        """Test technical question generation."""
        required_skills = ["Python", "Django", "React"]
        
        questions = self.generator._generate_technical_questions(
            required_skills,
            self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"]),
            5
        )
        
        assert len(questions) <= 5
        
        for question in questions:
            assert question["type"] == "technical"
            assert question["question"] is not None
            assert question["difficulty"] in ["medium", "hard"]

    def test_generate_situational_questions(self):
        """Test situational question generation."""
        responsibilities = ["Design and develop software solutions", "Collaborate with teams"]
        
        questions = self.generator._generate_situational_questions(
            responsibilities,
            self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"]),
            5
        )
        
        assert len(questions) <= 5
        
        for question in questions:
            assert question["type"] == "situational"
            assert question["question"] is not None
            assert question["difficulty"] == "medium"

    def test_generate_job_specific_questions(self):
        """Test job-specific question generation."""
        questions = self.generator._generate_job_specific_questions(
            self.job_description_data,
            self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        )
        
        assert len(questions) >= 2  # Should generate company and role questions
        
        # Check company question
        company_questions = [q for q in questions if q.get("type") == "company"]
        assert len(company_questions) >= 1
        assert "Enterprise Corp" in company_questions[0]["question"]
        
        # Check role question
        role_questions = [q for q in questions if q.get("type") == "role"]
        assert len(role_questions) >= 1
        assert "Senior Software Engineer" in role_questions[0]["question"]

    def test_generate_star_stories(self):
        """Test STAR story generation."""
        options = {"star_story_count": 5}
        
        stories = self.generator._generate_star_stories(
            self.tailored_resume_data,
            options,
            self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        )
        
        assert len(stories) <= 5
        
        for story in stories:
            assert "id" in story
            assert "title" in story
            assert "situation" in story
            assert "task" in story
            assert "action" in story
            assert "result" in story
            assert "context" in story
            assert "skills_used" in story
            assert "focus_areas" in story

    def test_create_star_story(self):
        """Test individual STAR story creation."""
        entry = {
            "title": "Software Engineer",
            "company": "Tech Corp",
            "description": "Developed scalable web applications",
            "achievements": ["Improved application performance by 40%"],
            "technologies": ["Python", "Django", "React"]
        }
        
        achievement = "Improved application performance by 40%"
        truth_bank = self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        
        story = self.generator._create_star_story(entry, achievement, "test_story", truth_bank)
        
        assert story["id"] == "test_story"
        assert "Tech Corp" in story["title"]
        assert story["situation"] is not None
        assert story["task"] is not None
        assert story["action"] is not None
        assert story["result"] is not None
        assert story["context"]["company"] == "Tech Corp"
        assert story["context"]["title"] == "Software Engineer"

    def test_generate_answer_drafts(self):
        """Test answer draft generation."""
        questions = [
            {
                "id": "test_1",
                "type": "behavioral",
                "question": "Tell me about a time you worked in a team."
            },
            {
                "id": "test_2",
                "type": "technical",
                "question": "Explain your experience with Python."
            }
        ]
        
        questions_with_answers = self.generator._generate_answer_drafts(
            questions,
            self.tailored_resume_data,
            self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        )
        
        assert len(questions_with_answers) == len(questions)
        
        for question_with_answer in questions_with_answers:
            assert "answer_draft" in question_with_answer
            assert "answer_length" in question_with_answer
            assert "key_points" in question_with_answer
            assert isinstance(question_with_answer["answer_length"], int)
            assert isinstance(question_with_answer["key_points"], list)

    def test_generate_behavioral_answer(self):
        """Test behavioral answer generation."""
        question = {
            "id": "test_1",
            "type": "behavioral",
            "category": "teamwork",
            "question": "Tell me about a time you worked in a team."
        }
        
        truth_bank = self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        answer = self.generator._generate_behavioral_answer(question, truth_bank)
        
        assert answer is not None
        assert len(answer) > 10  # Should be a reasonable length
        assert isinstance(answer, str)

    def test_generate_technical_answer(self):
        """Test technical answer generation."""
        question = {
            "id": "test_1",
            "type": "technical",
            "focus_area": "Python",
            "question": "Explain your experience with Python."
        }
        
        truth_bank = self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        answer = self.generator._generate_technical_answer(question, truth_bank)
        
        assert answer is not None
        assert len(answer) > 10  # Should be a reasonable length
        assert isinstance(answer, str)

    def test_generate_situational_answer(self):
        """Test situational answer generation."""
        question = {
            "id": "test_1",
            "type": "situational",
            "category": "communication",
            "question": "How do you handle tight deadlines?"
        }
        
        truth_bank = self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        answer = self.generator._generate_situational_answer(question, truth_bank)
        
        assert answer is not None
        assert len(answer) > 10  # Should be a reasonable length
        assert isinstance(answer, str)

    def test_generate_preparation_guide(self):
        """Test preparation guide generation."""
        options = {"interview_type": "mixed", "difficulty_level": "medium"}
        
        guide = self.generator._generate_preparation_guide(
            self.tailored_resume_data,
            self.job_description_data,
            options,
            self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        )
        
        assert "focus_areas" in guide
        assert "tips" in guide
        assert "recommendations" in guide
        assert "research_points" in guide
        assert "day_of_preparation" in guide
        assert "common_mistakes" in guide
        
        # Check structure
        assert isinstance(guide["focus_areas"], list)
        assert isinstance(guide["tips"], list)
        assert isinstance(guide["recommendations"], list)
        assert isinstance(guide["research_points"], list)
        assert isinstance(guide["day_of_preparation"], dict)
        assert isinstance(guide["common_mistakes"], list)

    def test_generate_content_summary(self):
        """Test content summary generation."""
        questions = [
            {"type": "behavioral"},
            {"type": "technical"},
            {"type": "situational"}
        ]
        
        star_stories = [
            {"id": "story_1"},
            {"id": "story_2"}
        ]
        
        options = {"question_count": 3, "difficulty_level": "medium", "interview_type": "mixed"}
        
        summary = self.generator._generate_content_summary(questions, star_stories, options)
        
        assert summary["total_questions"] == 3
        assert summary["behavioral_questions"] == 1
        assert summary["technical_questions"] == 1
        assert summary["situational_questions"] == 1
        assert summary["star_stories"] == 2
        assert summary["difficulty_level"] == "medium"
        assert summary["interview_type"] == "mixed"
        assert "estimated_prep_time" in summary

    def test_validate_interview_prep(self):
        """Test interview prep validation."""
        questions = [
            {
                "id": "test_1",
                "answer_draft": "This is a reasonable answer with good length and detail.",
                "answer_length": 50
            }
        ]
        
        star_stories = [
            {
                "id": "story_1",
                "situation": "While working at Tech Corp...",
                "task": "The main challenge was...",
                "action": "I implemented...",
                "result": "As a result..."
            }
        ]
        
        truth_bank = self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        
        validation = self.generator._validate_interview_prep(questions, star_stories, truth_bank)
        
        assert "is_valid" in validation
        assert "warnings" in validation
        assert "errors" in validation
        assert "recommendations" in validation
        assert isinstance(validation["warnings"], list)
        assert isinstance(validation["errors"], list)
        assert isinstance(validation["recommendations"], list)

    def test_validate_interview_prep_inadequate_content(self):
        """Test validation with inadequate content."""
        questions = [
            {
                "id": "test_1",
                "answer_draft": "Too short",
                "answer_length": 5
            }
        ]
        
        star_stories = [
            {
                "id": "story_1",
                "situation": "Incomplete story"
                # Missing other STAR components
            }
        ]
        
        truth_bank = self.generator._create_truth_bank_from_resume(self.tailored_resume_data["rendering_data"])
        
        validation = self.generator._validate_interview_prep(questions, star_stories, truth_bank)
        
        assert len(validation["warnings"]) > 0  # Should have warnings for inadequate content

    def test_calculate_truthfulness_score(self):
        """Test truthfulness score calculation."""
        questions = [
            {
                "answer_draft": "I have experience with Python and Django."
            }
        ]
        
        star_stories = [
            {
                "context": {"company": "Tech Corp"},
                "situation": "While working at Tech Corp...",
                "task": "The challenge was...",
                "action": "I implemented...",
                "result": "The result was..."
            }
        ]
        
        truth_bank = {
            "experience": {"companies": ["Tech Corp"]},
            "skills": {"technical": ["Python", "Django"]}
        }
        
        score = self.generator._calculate_truthfulness_score(questions, star_stories, truth_bank)
        
        assert score >= 0.0
        assert score <= 1.0

    def test_calculate_content_quality_score(self):
        """Test content quality score calculation."""
        questions = [
            {
                "answer_draft": "This is a well-structured answer with appropriate length and detail.",
                "answer_length": 75
            }
        ]
        
        star_stories = [
            {
                "situation": "While working at Tech Corp...",
                "task": "The challenge was...",
                "action": "I implemented...",
                "result": "The result was..."
            }
        ]
        
        score = self.generator._calculate_content_quality_score(questions, star_stories)
        
        assert score >= 0.0
        assert score <= 1.0

    def test_calculate_personalization_score(self):
        """Test personalization score calculation."""
        questions = [
            {
                "answer_draft": "I'm excited about the Senior Software Engineer role at Enterprise Corp."
            }
        ]
        
        star_stories = [
            {"id": "story_1"}
        ]
        
        job_description_data = {
            "job_title": "Senior Software Engineer",
            "company": "Enterprise Corp",
            "parsed_content": {
                "required_skills": [
                    {"skill": "Python", "category": "technical"}
                ]
            }
        }
        
        score = self.generator._calculate_personalization_score(questions, star_stories, job_description_data)
        
        assert score >= 0.0
        assert score <= 1.0

    def test_identify_content_sources(self):
        """Test content source identification."""
        questions = [
            {
                "answer_draft": "I have experience with Python and Django."
            }
        ]
        
        star_stories = [
            {
                "context": {"company": "Tech Corp"},
                "title": "Achievement at Tech Corp"
            }
        ]
        
        truth_bank = {
            "experience": {"companies": ["Tech Corp"]},
            "skills": {"technical": ["Python", "Django"]}
        }
        
        sources = self.generator._identify_content_sources(questions, star_stories, truth_bank)
        
        assert len(sources) >= 2  # Should find sources for both questions and stories
        for source in sources:
            assert "type" in source
            assert "content" in source
            assert "confidence" in source

    def test_get_focus_area(self):
        """Test focus area mapping."""
        focus_area = self.generator._get_focus_area("teamwork")
        assert focus_area == "collaboration"
        
        focus_area = self.generator._get_focus_area("technical_knowledge")
        assert focus_area == "technical_expertise"
        
        focus_area = self.generator._get_focus_area("unknown")
        assert focus_area == "general"

    def test_extract_focus_areas(self):
        """Test focus area extraction from achievements."""
        achievement = "I improved performance by 40% through team collaboration."
        truth_bank = {}
        
        focus_areas = self.generator._extract_focus_areas(achievement, truth_bank)
        
        assert "teamwork" in focus_areas
        assert "results_orientation" in focus_areas

    def test_extract_key_points(self):
        """Test key point extraction from answers."""
        answer = "This is the first point. This is the second point with more detail. This is the third point."
        
        key_points = self.generator._extract_key_points(answer)
        
        assert len(key_points) <= 3  # Should limit to 3 points
        assert all(point.strip() for point in key_points)  # All points should be non-empty

    def test_contains_exaggerated_claims(self):
        """Test exaggerated claims detection."""
        normal_text = "I have experience with Python and Django."
        exaggerated_text = "I am a world-class expert in everything."
        
        assert not self.generator._contains_exaggerated_claims(normal_text)
        assert self.generator._contains_exaggerated_claims(exaggerated_text)

    def test_generate_interview_prep_minimal_data(self):
        """Test interview prep generation with minimal data."""
        minimal_resume = {
            "rendering_data": {
                "header": {"name": "Jane Doe", "contact": {"email": "jane@example.com"}},
                "experience": {"entries": []},
                "skills": {"categories": []},
                "education": {"entries": []},
                "projects": None
            }
        }
        
        minimal_jd = {
            "parsed_content": {"job_title": "Engineer", "company": "Tech Corp"},
            "raw_text": "We are looking for an engineer.",
            "job_title": "Engineer",
            "company": "Tech Corp"
        }
        
        result = self.generator.generate_interview_prep(minimal_resume, minimal_jd)
        
        assert result["success"] is True
        assert result["interview_prep"]["interview_context"] is not None
        assert result["interview_prep"]["questions"] is not None

    def test_generate_interview_prep_validation_failure(self):
        """Test interview prep generation with validation failures."""
        # Create content that will trigger validation failures
        resume_with_issues = {
            "rendering_data": {
                "header": {"name": "John Doe", "contact": {"email": "john@example.com"}},
                "experience": {"entries": []},
                "skills": {"categories": []},
                "education": {"entries": []}
            }
        }
        
        result = self.generator.generate_interview_prep(resume_with_issues, self.job_description_data)
        
        # Should still generate but with validation warnings
        assert result["success"] is True
        assert len(result["validation"]["warnings"]) > 0

    def test_question_templates_structure(self):
        """Test that all question templates have required keys."""
        for template_type, templates in self.generator.question_templates.items():
            for template_key, template in templates.items():
                assert isinstance(template, str)
                assert len(template) > 0  # Should not be empty

    def test_processing_time_tracking(self):
        """Test processing time tracking."""
        result = self.generator.generate_interview_prep(
            self.tailored_resume_data,
            self.job_description_data
        )
        
        processing_time = result["metadata"]["processing_time_ms"]
        assert processing_time > 0
        assert isinstance(processing_time, int)

    def test_sources_confidence_levels(self):
        """Test content sources have confidence levels."""
        result = self.generator.generate_interview_prep(
            self.tailored_resume_data,
            self.job_description_data
        )
        
        sources = result["sources"]
        for source in sources:
            assert "confidence" in source
            assert source["confidence"] in ["high", "medium", "low"]

    def test_different_interview_types(self):
        """Test generation with different interview types."""
        interview_types = ["behavioral", "technical", "situational", "mixed"]
        
        for interview_type in interview_types:
            options = {"interview_type": interview_type}
            
            result = self.generator.generate_interview_prep(
                self.tailored_resume_data,
                self.job_description_data,
                options
            )
            
            assert result["metadata"]["generation_options"]["interview_type"] == interview_type
            assert result["success"] is True

    def test_different_difficulty_levels(self):
        """Test generation with different difficulty levels."""
        difficulty_levels = ["easy", "medium", "hard"]
        
        for difficulty in difficulty_levels:
            options = {"difficulty_level": difficulty}
            
            result = self.generator.generate_interview_prep(
                self.tailored_resume_data,
                self.job_description_data,
                options
            )
            
            assert result["metadata"]["generation_options"]["difficulty_level"] == difficulty
            assert result["success"] is True

    def test_question_count_limits(self):
        """Test question count limits."""
        question_counts = [5, 10, 20, 30]
        
        for count in question_counts:
            options = {"question_count": count}
            
            result = self.generator.generate_interview_prep(
                self.tailored_resume_data,
                self.job_description_data,
                options
            )
            
            questions = result["interview_prep"]["questions"]
            assert len(questions) <= count

    def test_star_story_count_limits(self):
        """Test STAR story count limits."""
        story_counts = [3, 5, 10, 15]
        
        for count in story_counts:
            options = {"star_story_count": count}
            
            result = self.generator.generate_interview_prep(
                self.tailored_resume_data,
                self.job_description_data,
                options
            )
            
            stories = result["interview_prep"]["star_stories"]
            assert len(stories) <= count

    def test_question_type_inclusion_options(self):
        """Test question type inclusion options."""
        options = {
            "include_behavioral": False,
            "include_technical": True,
            "include_situational": False
        }
        
        result = self.generator.generate_interview_prep(
            self.tailored_resume_data,
            self.job_description_data,
            options
        )
        
        questions = result["interview_prep"]["questions"]
        question_types = set(q.get("type") for q in questions)
        
        assert "technical" in question_types
        assert "behavioral" not in question_types
        assert "situational" not in question_types


if __name__ == "__main__":
    pytest.main([__file__])
