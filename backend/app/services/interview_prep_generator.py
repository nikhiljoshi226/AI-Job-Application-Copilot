from typing import Dict, List, Any, Optional, Tuple
import re
import time
from datetime import datetime

from app.services.truth_bank import TruthBank


class InterviewPrepGenerator:
    """
    Service to generate comprehensive interview preparation materials
    including questions, answer drafts, and STAR stories based on JD and resume.
    """

    def __init__(self):
        self.truth_bank_service = TruthBank()
        
        # Question templates for different interview types
        self.question_templates = {
            "behavioral": {
                "teamwork": "Tell me about a time you worked in a team to achieve a goal.",
                "conflict": "Describe a situation where you had a conflict with a team member.",
                "failure": "Tell me about a time you failed and what you learned.",
                "leadership": "Describe a situation where you took initiative or showed leadership.",
                "problem_solving": "Tell me about a complex problem you had to solve.",
                "adaptability": "Describe a time you had to adapt to a major change.",
                "achievement": "Tell me about your greatest professional achievement."
            },
            "technical": {
                "technical_knowledge": "Explain your experience with {key_technology}.",
                "system_design": "How would you design a system to {scenario}?",
                "coding_challenge": "Can you solve this {difficulty} coding problem?",
                "troubleshooting": "How would you troubleshoot {issue}?",
                "architecture": "What architectural patterns have you used?",
                "optimization": "How would you optimize {performance_aspect}?"
            },
            "situational": {
                "prioritization": "How would you prioritize competing deadlines?",
                "communication": "How would you explain a technical concept to a non-technical stakeholder?",
                "decision_making": "Describe your approach to making important decisions.",
                "handling_pressure": "How do you handle tight deadlines and pressure?",
                "learning": "How do you stay updated with new technologies?"
            }
        }

    def generate_interview_prep(
        self,
        resume_data: Dict[str, Any],
        job_description_data: Dict[str, Any],
        generation_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive interview preparation materials.
        
        Args:
            resume_data: Tailored resume data with rendering content
            job_description_data: Parsed job description data
            generation_options: Options for generation
            
        Returns:
            Generated interview prep with metadata and validation results
        """
        start_time = time.time()
        
        # Set default generation options
        options = {
            "interview_type": "mixed",
            "question_count": 15,
            "include_behavioral": True,
            "include_technical": True,
            "include_situational": True,
            "star_story_count": 8,
            "difficulty_level": "medium"
        }
        if generation_options:
            options.update(generation_options)
        
        # Create truth bank for validation
        truth_bank = self._create_truth_bank_from_resume(resume_data)
        
        # Generate interview questions
        questions = self._generate_interview_questions(
            resume_data,
            job_description_data,
            options,
            truth_bank
        )
        
        # Generate STAR stories
        star_stories = self._generate_star_stories(
            resume_data,
            options,
            truth_bank
        )
        
        # Generate answer drafts
        questions_with_answers = self._generate_answer_drafts(
            questions,
            resume_data,
            truth_bank
        )
        
        # Generate preparation guide
        preparation_guide = self._generate_preparation_guide(
            resume_data,
            job_description_data,
            options,
            truth_bank
        )
        
        # Generate content summary
        content_summary = self._generate_content_summary(
            questions_with_answers,
            star_stories,
            options
        )
        
        # Validate and score the content
        validation_result = self._validate_interview_prep(
            questions_with_answers,
            star_stories,
            truth_bank
        )
        
        # Calculate scores
        truthfulness_score = self._calculate_truthfulness_score(
            questions_with_answers,
            star_stories,
            truth_bank
        )
        content_quality_score = self._calculate_content_quality_score(
            questions_with_answers,
            star_stories
        )
        personalization_score = self._calculate_personalization_score(
            questions_with_answers,
            star_stories,
            job_description_data
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Build result
        result = {
            "interview_prep": {
                "interview_context": {
                    "interview_type": options["interview_type"],
                    "question_count": len(questions_with_answers),
                    "star_story_count": len(star_stories),
                    "difficulty_level": options["difficulty_level"],
                    "estimated_duration": f"{len(questions_with_answers) * 5}-{len(questions_with_answers) * 8} minutes"
                },
                "questions": questions_with_answers,
                "star_stories": star_stories,
                "preparation_guide": preparation_guide,
                "content_summary": content_summary
            },
            "metadata": {
                "truthfulness_score": truthfulness_score,
                "content_quality_score": content_quality_score,
                "personalization_score": personalization_score,
                "processing_time_ms": processing_time,
                "generation_options": options,
                "generated_at": datetime.utcnow().isoformat()
            },
            "validation": validation_result,
            "sources": self._identify_content_sources(
                questions_with_answers,
                star_stories,
                truth_bank
            )
        }
        
        return result

    def _create_truth_bank_from_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a truth bank from resume data for validation."""
        truth_bank = {
            "personal_info": {
                "name": resume_data.get("header", {}).get("name", ""),
                "contact": resume_data.get("header", {}).get("contact", {})
            },
            "experience": {
                "companies": [],
                "titles": [],
                "achievements": [],
                "technologies": [],
                "responsibilities": [],
                "projects": []
            },
            "skills": {
                "technical": [],
                "soft_skills": [],
                "certifications": []
            },
            "education": {
                "degrees": [],
                "universities": [],
                "achievements": []
            }
        }
        
        # Extract experience information
        experience_entries = resume_data.get("experience", {}).get("entries", [])
        for entry in experience_entries:
            if entry.get("company"):
                truth_bank["experience"]["companies"].append(entry["company"])
            if entry.get("title"):
                truth_bank["experience"]["titles"].append(entry["title"])
            if entry.get("achievements"):
                truth_bank["experience"]["achievements"].extend(entry["achievements"])
            if entry.get("technologies"):
                truth_bank["experience"]["technologies"].extend(entry["technologies"])
            if entry.get("description"):
                truth_bank["experience"]["responsibilities"].append(entry["description"])
        
        # Extract skills
        skills_categories = resume_data.get("skills", {}).get("categories", [])
        for category in skills_categories:
            category_name = category.get("name", "").lower()
            skills = category.get("skills", [])
            
            if "technical" in category_name:
                truth_bank["skills"]["technical"].extend([s.get("name", "") for s in skills])
            elif "soft" in category_name:
                truth_bank["skills"]["soft_skills"].extend([s.get("name", "") for s in skills])
        
        # Extract education
        education_entries = resume_data.get("education", {}).get("entries", [])
        for entry in education_entries:
            if entry.get("degree"):
                truth_bank["education"]["degrees"].append(entry["degree"])
            if entry.get("university"):
                truth_bank["education"]["universities"].append(entry["university"])
            if entry.get("achievements"):
                truth_bank["education"]["achievements"].extend(entry["achievements"])
        
        # Extract projects
        project_entries = resume_data.get("projects", {}).get("entries", [])
        for entry in project_entries:
            if entry.get("name"):
                truth_bank["experience"]["projects"].append(entry["name"])
            if entry.get("description"):
                truth_bank["experience"]["projects"].append(entry["description"])
            if entry.get("technologies"):
                truth_bank["experience"]["technologies"].extend(entry["technologies"])
        
        return truth_bank

    def _generate_interview_questions(
        self,
        resume_data: Dict[str, Any],
        job_description_data: Dict[str, Any],
        options: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate interview questions based on JD and resume."""
        questions = []
        
        # Extract key information from JD
        jd_content = job_description_data.get("parsed_content", {})
        required_skills = [skill.get("skill", "") for skill in jd_content.get("required_skills", [])]
        responsibilities = jd_content.get("responsibilities", [])
        
        # Generate behavioral questions
        if options.get("include_behavioral", True):
            behavioral_questions = self._generate_behavioral_questions(
                truth_bank,
                options["question_count"] // 3
            )
            questions.extend(behavioral_questions)
        
        # Generate technical questions
        if options.get("include_technical", True):
            technical_questions = self._generate_technical_questions(
                required_skills,
                truth_bank,
                options["question_count"] // 3
            )
            questions.extend(technical_questions)
        
        # Generate situational questions
        if options.get("include_situational", True):
            situational_questions = self._generate_situational_questions(
                responsibilities,
                truth_bank,
                options["question_count"] // 3
            )
            questions.extend(situational_questions)
        
        # Add job-specific questions
        job_specific_questions = self._generate_job_specific_questions(
            job_description_data,
            truth_bank
        )
        questions.extend(job_specific_questions)
        
        return questions[:options["question_count"]]

    def _generate_behavioral_questions(
        self,
        truth_bank: Dict[str, Any],
        count: int
    ) -> List[Dict[str, Any]]:
        """Generate behavioral interview questions."""
        questions = []
        templates = self.question_templates["behavioral"]
        
        # Select relevant templates based on experience
        relevant_templates = []
        
        if truth_bank["experience"]["achievements"]:
            relevant_templates.extend(["achievement", "teamwork"])
        
        if len(truth_bank["experience"]["companies"]) > 1:
            relevant_templates.extend(["adaptability", "problem_solving"])
        
        if any("lead" in title.lower() for title in truth_bank["experience"]["titles"]):
            relevant_templates.append("leadership")
        
        # Add core behavioral questions
        if not relevant_templates:
            relevant_templates = ["teamwork", "problem_solving", "achievement", "failure"]
        
        # Generate questions
        for i, template_key in enumerate(relevant_templates[:count]):
            template = templates.get(template_key, templates["teamwork"])
            question = {
                "id": f"behavioral_{i+1}",
                "type": "behavioral",
                "category": template_key,
                "question": template,
                "focus_area": self._get_focus_area(template_key),
                "difficulty": "medium"
            }
            questions.append(question)
        
        return questions

    def _generate_technical_questions(
        self,
        required_skills: List[str],
        truth_bank: Dict[str, Any],
        count: int
    ) -> List[Dict[str, Any]]:
        """Generate technical interview questions."""
        questions = []
        templates = self.question_templates["technical"]
        
        # Generate questions based on required skills
        user_skills = truth_bank["skills"]["technical"]
        
        # Find overlapping skills
        overlapping_skills = [skill for skill in required_skills if skill.lower() in [s.lower() for s in user_skills]]
        
        if overlapping_skills:
            # Generate questions for top overlapping skills
            for i, skill in enumerate(overlapping_skills[:count]):
                question_text = templates["technical_knowledge"].format(key_technology=skill)
                question = {
                    "id": f"technical_{i+1}",
                    "type": "technical",
                    "category": "technical_knowledge",
                    "question": question_text,
                    "focus_area": skill,
                    "difficulty": "medium"
                }
                questions.append(question)
        
        # Add system design question if relevant
        if any("engineer" in title.lower() for title in truth_bank["experience"]["titles"]):
            scenario = "handle high traffic for an e-commerce platform"
            question_text = templates["system_design"].format(scenario=scenario)
            question = {
                "id": f"technical_{len(questions)+1}",
                "type": "technical",
                "category": "system_design",
                "question": question_text,
                "focus_area": "system_design",
                "difficulty": "hard"
            }
            questions.append(question)
        
        return questions[:count]

    def _generate_situational_questions(
        self,
        responsibilities: List[str],
        truth_bank: Dict[str, Any],
        count: int
    ) -> List[Dict[str, Any]]:
        """Generate situational interview questions."""
        questions = []
        templates = self.question_templates["situational"]
        
        # Select relevant situational questions
        relevant_templates = ["communication", "problem_solving", "decision_making", "handling_pressure"]
        
        for i, template_key in enumerate(relevant_templates[:count]):
            template = templates.get(template_key, templates["communication"])
            question = {
                "id": f"situational_{i+1}",
                "type": "situational",
                "category": template_key,
                "question": template,
                "focus_area": self._get_focus_area(template_key),
                "difficulty": "medium"
            }
            questions.append(question)
        
        return questions

    def _generate_job_specific_questions(
        self,
        job_description_data: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate job-specific questions."""
        questions = []
        
        # Extract job-specific information
        jd_content = job_description_data.get("parsed_content", {})
        company = job_description_data.get("company", "")
        job_title = job_description_data.get("job_title", "")
        
        # Company-specific questions
        if company:
            question = {
                "id": "job_specific_1",
                "type": "company",
                "category": "company_knowledge",
                "question": f"What do you know about {company} and why do you want to work here?",
                "focus_area": "company_research",
                "difficulty": "medium"
            }
            questions.append(question)
        
        # Role-specific questions
        if job_title:
            question = {
                "id": "job_specific_2",
                "type": "role",
                "category": "role_understanding",
                "question": f"How does your background prepare you for this {job_title} role?",
                "focus_area": "role_fit",
                "difficulty": "medium"
            }
            questions.append(question)
        
        return questions

    def _generate_star_stories(
        self,
        resume_data: Dict[str, Any],
        options: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate STAR format stories from resume experiences."""
        stories = []
        
        # Extract experiences for STAR stories
        experience_entries = resume_data.get("experience", {}).get("entries", [])
        project_entries = resume_data.get("projects", {}).get("entries", [])
        
        # Generate STAR stories from work experience
        for i, entry in enumerate(experience_entries[:options["star_story_count"]]):
            if entry.get("achievements") and len(entry["achievements"]) > 0:
                achievement = entry["achievements"][0]  # Use first achievement
                star_story = self._create_star_story(
                    entry,
                    achievement,
                    f"experience_{i+1}",
                    truth_bank
                )
                stories.append(star_story)
        
        # Generate STAR stories from projects if needed
        if len(stories) < options["star_story_count"]:
            remaining = options["star_story_count"] - len(stories)
            for i, entry in enumerate(project_entries[:remaining]):
                star_story = self._create_star_story(
                    entry,
                    entry.get("description", ""),
                    f"project_{i+1}",
                    truth_bank
                )
                stories.append(star_story)
        
        return stories

    def _create_star_story(
        self,
        entry: Dict[str, Any],
        achievement: str,
        story_id: str,
        truth_bank: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a STAR format story from an experience entry."""
        
        # Situation
        situation = f"While working at {entry.get('company', 'a company')} as a {entry.get('title', 'professional')}, I was responsible for {entry.get('description', 'various responsibilities')}."
        
        # Task
        task = f"The main challenge was to {achievement.lower()}. This required careful planning and execution."
        
        # Action
        technologies = entry.get("technologies", [])
        if technologies:
            action = f"I implemented a solution using {', '.join(technologies[:3])}, focusing on best practices and efficient coding. I collaborated with team members and followed a systematic approach to ensure quality."
        else:
            action = f"I took initiative and developed a comprehensive solution, leveraging my skills and experience to address the challenge effectively."
        
        # Result
        result = f"As a result, {achievement}. This demonstrated my ability to deliver results and make a meaningful impact."
        
        return {
            "id": story_id,
            "title": f"{entry.get('title', 'Professional Achievement')} at {entry.get('company', 'Company')}",
            "situation": situation,
            "task": task,
            "action": action,
            "result": result,
            "skills_used": technologies[:3] if technologies else [],
            "context": {
                "company": entry.get("company"),
                "title": entry.get("title"),
                "dates": entry.get("dates")
            },
            "focus_areas": self._extract_focus_areas(achievement, truth_bank)
        }

    def _generate_answer_drafts(
        self,
        questions: List[Dict[str, Any]],
        resume_data: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate answer drafts for interview questions."""
        questions_with_answers = []
        
        for question in questions:
            answer_draft = self._generate_answer_for_question(
                question,
                resume_data,
                truth_bank
            )
            
            question_with_answer = {
                **question,
                "answer_draft": answer_draft,
                "answer_length": len(answer_draft.split()),
                "key_points": self._extract_key_points(answer_draft)
            }
            questions_with_answers.append(question_with_answer)
        
        return questions_with_answers

    def _generate_answer_for_question(
        self,
        question: Dict[str, Any],
        resume_data: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> str:
        """Generate an answer draft for a specific question."""
        question_type = question.get("type", "")
        question_text = question.get("question", "")
        
        if question_type == "behavioral":
            return self._generate_behavioral_answer(question, truth_bank)
        elif question_type == "technical":
            return self._generate_technical_answer(question, truth_bank)
        elif question_type == "situational":
            return self._generate_situational_answer(question, truth_bank)
        else:
            return self._generate_generic_answer(question, truth_bank)

    def _generate_behavioral_answer(
        self,
        question: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> str:
        """Generate a behavioral answer using STAR format."""
        category = question.get("category", "")
        
        # Find relevant experience
        relevant_experience = self._find_relevant_experience(category, truth_bank)
        
        if relevant_experience:
            return f"I'd be happy to share an example. {relevant_experience['situation']} {relevant_experience['task']} {relevant_experience['action']} {relevant_experience['result']}"
        else:
            return f"I believe in approaching situations methodically. I typically start by understanding the context, identifying key stakeholders, and developing a clear action plan. I focus on collaboration and communication to ensure everyone is aligned, and I always measure outcomes to learn and improve."

    def _generate_technical_answer(
        self,
        question: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> str:
        """Generate a technical answer based on skills."""
        focus_area = question.get("focus_area", "")
        user_skills = truth_bank["skills"]["technical"]
        
        if focus_area and any(focus_area.lower() in skill.lower() for skill in user_skills):
            relevant_skills = [skill for skill in user_skills if focus_area.lower() in skill.lower()]
            return f"I have extensive experience with {', '.join(relevant_skills)}. In my previous roles, I've used these technologies to build scalable solutions, optimize performance, and solve complex problems. I stay current with best practices and am always learning new approaches to improve my technical skills."
        else:
            return f"I approach technical challenges with a systematic mindset, focusing on understanding requirements, designing robust solutions, and implementing best practices. I believe in writing clean, maintainable code and thoroughly testing my work to ensure quality and reliability."

    def _generate_situational_answer(
        self,
        question: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> str:
        """Generate a situational answer."""
        return f"I believe in handling situations with professionalism and clear communication. I would first assess the situation, gather relevant information, and consider different perspectives. Then I would develop a plan, communicate it clearly to stakeholders, and execute it while remaining flexible to adjust as needed. Throughout the process, I would maintain transparency and focus on achieving the best possible outcome."

    def _generate_generic_answer(
        self,
        question: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> str:
        """Generate a generic answer."""
        return f"I approach challenges with a positive attitude and a focus on continuous learning. I believe in collaborating effectively with others, taking initiative when needed, and always striving to deliver high-quality work. I'm committed to personal and professional growth and welcome opportunities to expand my skills and knowledge."

    def _find_relevant_experience(
        self,
        category: str,
        truth_bank: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Find relevant experience for a behavioral question category."""
        # This would use more sophisticated logic in a real implementation
        # For now, return a generic relevant experience
        return {
            "situation": "In my previous role, I encountered a challenging situation that required careful consideration.",
            "task": "I was tasked with resolving this issue while maintaining team productivity.",
            "action": "I took a systematic approach, gathering input from stakeholders and developing a comprehensive solution.",
            "result": "The outcome was positive, with improved processes and team satisfaction."
        }

    def _generate_preparation_guide(
        self,
        resume_data: Dict[str, Any],
        job_description_data: Dict[str, Any],
        options: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate interview preparation guide."""
        
        # Extract key information
        company = job_description_data.get("company", "")
        job_title = job_description_data.get("job_title", "")
        required_skills = [skill.get("skill", "") for skill in job_description_data.get("parsed_content", {}).get("required_skills", [])]
        
        # Generate focus areas
        focus_areas = self._identify_preparation_focus_areas(
            resume_data,
            job_description_data,
            truth_bank
        )
        
        # Generate tips
        tips = self._generate_interview_tips(options, truth_bank)
        
        # Generate recommendations
        recommendations = self._generate_preparation_recommendations(
            company,
            job_title,
            required_skills,
            truth_bank
        )
        
        return {
            "focus_areas": focus_areas,
            "tips": tips,
            "recommendations": recommendations,
            "research_points": self._generate_research_points(company, job_description_data),
            "day_of_preparation": self._generate_day_of_preparation_guide(options),
            "common_mistakes": self._generate_common_mistakes_guide()
        }

    def _identify_preparation_focus_areas(
        self,
        resume_data: Dict[str, Any],
        job_description_data: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify key areas to focus on during preparation."""
        focus_areas = []
        
        # Technical skills focus
        jd_skills = [skill.get("skill", "") for skill in job_description_data.get("parsed_content", {}).get("required_skills", [])]
        user_skills = truth_bank["skills"]["technical"]
        overlapping_skills = [skill for skill in jd_skills if skill.lower() in [s.lower() for s in user_skills]]
        
        if overlapping_skills:
            focus_areas.append({
                "area": "Technical Skills",
                "priority": "high",
                "description": f"Focus on {', '.join(overlapping_skills[:3])} as these are key requirements",
                "preparation_time": "2-3 hours"
            })
        
        # Experience focus
        experience_entries = resume_data.get("experience", {}).get("entries", [])
        if experience_entries:
            focus_areas.append({
                "area": "Experience Stories",
                "priority": "high",
                "description": "Prepare STAR stories for your key achievements",
                "preparation_time": "2-3 hours"
            })
        
        # Company research
        focus_areas.append({
            "area": "Company Knowledge",
            "priority": "medium",
            "description": "Research company culture, values, and recent news",
            "preparation_time": "1-2 hours"
        })
        
        return focus_areas

    def _generate_interview_tips(
        self,
        options: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> List[str]:
        """Generate interview preparation tips."""
        tips = [
            "Practice your answers out loud to build confidence",
            "Research the company and interviewers if possible",
            "Prepare thoughtful questions to ask the interviewer",
            "Arrive 10-15 minutes early for in-person interviews",
            "Test your technology for virtual interviews",
            "Bring copies of your resume for in-person interviews",
            "Follow up with a thank-you email within 24 hours"
        ]
        
        if options["interview_type"] == "technical":
            tips.extend([
                "Practice coding problems on a whiteboard or paper",
                "Review fundamental computer science concepts",
                "Be prepared to discuss your technical decisions"
            ])
        
        return tips

    def _generate_preparation_recommendations(
        self,
        company: str,
        job_title: str,
        required_skills: List[str],
        truth_bank: Dict[str, Any]
    ) -> List[str]:
        """Generate specific preparation recommendations."""
        recommendations = []
        
        # Company-specific recommendations
        if company:
            recommendations.append(f"Research {company}'s recent projects, values, and company culture")
        
        # Role-specific recommendations
        if job_title:
            recommendations.append(f"Understand the key responsibilities and challenges of the {job_title} role")
        
        # Skill-specific recommendations
        if required_skills:
            top_skills = required_skills[:3]
            recommendations.append(f"Be prepared to discuss your experience with {', '.join(top_skills)}")
        
        # Experience recommendations
        if truth_bank["experience"]["achievements"]:
            recommendations.append("Select 3-5 of your strongest achievements to highlight")
        
        return recommendations

    def _generate_research_points(
        self,
        company: str,
        job_description_data: Dict[str, Any]
    ) -> List[str]:
        """Generate research points for company preparation."""
        research_points = [
            "Company mission, values, and culture",
            "Recent news or announcements",
            "Key products or services",
            "Leadership team and interviewers",
            "Company's position in the market",
            "Recent challenges or opportunities"
        ]
        
        if company:
            research_points.insert(0, f"{company}'s history and background")
        
        return research_points

    def _generate_day_of_preparation_guide(
        self,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate day-of-interview preparation guide."""
        return {
            "morning": [
                "Review your STAR stories and key talking points",
                "Research company one more time",
                "Prepare your questions for the interviewer",
                "Check logistics (location, time, interviewers)"
            ],
            "before_interview": [
                "Arrive 10-15 minutes early",
                "Review your notes one last time",
                "Take a few deep breaths to calm nerves",
                "Turn off your phone and minimize distractions"
            ],
            "during_interview": [
                "Listen carefully to questions",
                "Take a moment to think before answering",
                "Be authentic and genuine",
                "Ask thoughtful questions about the role and company"
            ]
        }

    def _generate_common_mistakes_guide(self) -> List[str]:
        """Generate guide on common interview mistakes to avoid."""
        return [
            "Speaking negatively about previous employers",
            "Not having questions to ask the interviewer",
            "Being too brief or too verbose in answers",
            "Not researching the company beforehand",
            "Failing to provide specific examples",
            "Not following up after the interview",
            "Appearing disinterested or unenthusiastic",
            "Not being prepared to discuss salary expectations"
        ]

    def _generate_content_summary(
        self,
        questions: List[Dict[str, Any]],
        star_stories: List[Dict[str, Any]],
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate content summary for the interview prep."""
        return {
            "total_questions": len(questions),
            "behavioral_questions": len([q for q in questions if q.get("type") == "behavioral"]),
            "technical_questions": len([q for q in questions if q.get("type") == "technical"]),
            "situational_questions": len([q for q in questions if q.get("type") == "situational"]),
            "star_stories": len(star_stories),
            "estimated_prep_time": f"{len(questions) + len(stories)}-3 hours",
            "difficulty_level": options["difficulty_level"],
            "interview_type": options["interview_type"]
        }

    def _validate_interview_prep(
        self,
        questions: List[Dict[str, Any]],
        star_stories: List[Dict[str, Any]],
        truth_bank: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate the interview prep content."""
        validation_result = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "recommendations": []
        }
        
        # Check for adequate content
        if len(questions) < 10:
            validation_result["warnings"].append("Consider generating more questions for comprehensive preparation")
        
        if len(star_stories) < 5:
            validation_result["warnings"].append("Consider adding more STAR stories for behavioral questions")
        
        # Check for answer quality
        short_answers = [q for q in questions if q.get("answer_length", 0) < 20]
        if len(short_answers) > len(questions) * 0.3:
            validation_result["warnings"].append("Some answers are quite short - consider expanding them")
        
        # Check for STAR story completeness
        incomplete_stories = [s for s in star_stories if not all([
            s.get("situation"), s.get("task"), s.get("action"), s.get("result")
        ])]
        if incomplete_stories:
            validation_result["warnings"].append("Some STAR stories are incomplete")
        
        # Add recommendations
        validation_result["recommendations"] = [
            "Practice your answers out loud to build confidence",
            "Research the company and interviewers beforehand",
            "Prepare thoughtful questions to ask the interviewer",
            "Follow up with a thank-you email within 24 hours"
        ]
        
        return validation_result

    def _calculate_truthfulness_score(
        self,
        questions: List[Dict[str, Any]],
        star_stories: List[Dict[str, Any]],
        truth_bank: Dict[str, Any]
    ) -> float:
        """Calculate truthfulness score for interview prep."""
        base_score = 0.8  # Start with high score
        
        # Check STAR stories for authenticity
        authentic_stories = 0
        for story in star_stories:
            if story.get("context", {}).get("company") in truth_bank["experience"]["companies"]:
                authentic_stories += 1
        
        if star_stories:
            story_authenticity = authentic_stories / len(star_stories)
            base_score += story_authenticity * 0.1
        
        # Check answers for realism
        realistic_answers = 0
        for question in questions:
            answer = question.get("answer_draft", "")
            if not self._contains_exaggerated_claims(answer):
                realistic_answers += 1
        
        if questions:
            answer_realism = realistic_answers / len(questions)
            base_score += answer_realism * 0.1
        
        return max(0.0, min(1.0, base_score))

    def _calculate_content_quality_score(
        self,
        questions: List[Dict[str, Any]],
        star_stories: List[Dict[str, Any]]
    ) -> float:
        """Calculate content quality score."""
        base_score = 0.7  # Start with decent score
        
        # Check question variety
        question_types = set(q.get("type") for q in questions)
        if len(question_types) >= 3:
            base_score += 0.1
        
        # Check STAR story completeness
        complete_stories = 0
        for story in star_stories:
            if all([story.get("situation"), story.get("task"), story.get("action"), story.get("result")]):
                complete_stories += 1
        
        if star_stories:
            story_completeness = complete_stories / len(star_stories)
            base_score += story_completeness * 0.1
        
        # Check answer length appropriateness
        appropriate_length = 0
        for question in questions:
            answer_length = question.get("answer_length", 0)
            if 20 <= answer_length <= 150:  # Reasonable length
                appropriate_length += 1
        
        if questions:
            length_appropriateness = appropriate_length / len(questions)
            base_score += length_appropriateness * 0.1
        
        return max(0.0, min(1.0, base_score))

    def _calculate_personalization_score(
        self,
        questions: List[Dict[str, Any]],
        star_stories: List[Dict[str, Any]],
        job_description_data: Dict[str, Any]
    ) -> float:
        """Calculate personalization score."""
        base_score = 0.6  # Start with neutral score
        
        # Check for job-specific content
        job_title = job_description_data.get("job_title", "")
        company = job_description_data.get("company", "")
        
        job_specific_mentions = 0
        for question in questions:
            answer = question.get("answer_draft", "")
            if job_title.lower() in answer.lower() or company.lower() in answer.lower():
                job_specific_mentions += 1
        
        if questions:
            job_specific = job_specific_mentions / len(questions)
            base_score += job_specific * 0.2
        
        # Check for skill alignment
        jd_skills = [skill.get("skill", "") for skill in job_description_data.get("parsed_content", {}).get("required_skills", [])]
        skill_mentions = 0
        
        for question in questions:
            answer = question.get("answer_draft", "")
            for skill in jd_skills:
                if skill.lower() in answer.lower():
                    skill_mentions += 1
                    break
        
        if questions:
            skill_alignment = min(1.0, skill_mentions / len(questions))
            base_score += skill_alignment * 0.2
        
        return max(0.0, min(1.0, base_score))

    def _identify_content_sources(
        self,
        questions: List[Dict[str, Any]],
        star_stories: List[Dict[str, Any]],
        truth_bank: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify sources of content in the interview prep."""
        sources = []
        
        # Check STAR story sources
        for story in star_stories:
            context = story.get("context", {})
            company = context.get("company")
            
            if company and company in truth_bank["experience"]["companies"]:
                sources.append({
                    "type": "resume_experience",
                    "content": f"STAR story: {story.get('title')}",
                    "confidence": "high"
                })
        
        # Check question answer sources
        for question in questions:
            answer = question.get("answer_draft", "")
            
            # Check for skills mentioned
            for skill in truth_bank["skills"]["technical"]:
                if skill.lower() in answer.lower():
                    sources.append({
                        "type": "resume_skill",
                        "content": f"Answer for: {question.get('question')}",
                        "confidence": "high"
                    })
                    break
        
        return sources

    def _get_focus_area(self, category: str) -> str:
        """Get focus area for a question category."""
        focus_areas = {
            "teamwork": "collaboration",
            "conflict": "conflict_resolution",
            "failure": "learning_from_mistakes",
            "leadership": "leadership",
            "problem_solving": "analytical_thinking",
            "adaptability": "adaptability",
            "achievement": "results_orientation",
            "technical_knowledge": "technical_expertise",
            "system_design": "architecture",
            "coding_challenge": "coding_skills",
            "troubleshooting": "problem_solving",
            "architecture": "system_design",
            "optimization": "performance_optimization",
            "prioritization": "time_management",
            "communication": "communication_skills",
            "decision_making": "decision_making",
            "handling_pressure": "stress_management",
            "learning": "continuous_learning"
        }
        
        return focus_areas.get(category, "general")

    def _extract_focus_areas(
        self,
        achievement: str,
        truth_bank: Dict[str, Any]
    ) -> List[str]:
        """Extract focus areas from an achievement."""
        focus_areas = []
        
        # Look for key themes
        if any(word in achievement.lower() for word in ["team", "collaborate", "worked with"]):
            focus_areas.append("teamwork")
        
        if any(word in achievement.lower() for word in ["improved", "increased", "optimized", "reduced"]):
            focus_areas.append("results_orientation")
        
        if any(word in achievement.lower() for word in ["developed", "created", "built", "implemented"]):
            focus_areas.append("technical_skills")
        
        if any(word in achievement.lower() for word in ["managed", "led", "coordinated", "mentored"]):
            focus_areas.append("leadership")
        
        return focus_areas

    def _extract_key_points(self, answer: str) -> List[str]:
        """Extract key points from an answer."""
        # Simple key point extraction - in production would use NLP
        sentences = answer.split('.')
        key_points = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Skip very short sentences
                key_points.append(sentence)
        
        return key_points[:3]  # Return top 3 key points

    def _contains_exaggerated_claims(self, text: str) -> bool:
        """Check if text contains exaggerated claims."""
        exaggerated_indicators = [
            "world-class",
            "expert in",
            "master of",
            "revolutionized",
            "unmatched",
            "unparalleled",
            "industry-leading"
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in exaggerated_indicators)


if __name__ == "__main__":
    generator = InterviewPrepGenerator()
    print("InterviewPrepGenerator initialized successfully")
