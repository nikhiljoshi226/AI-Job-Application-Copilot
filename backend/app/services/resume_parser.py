import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class ResumeParser:
    """Service to parse raw resume text into structured JSON."""
    
    def __init__(self):
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'\b?(\d{3})\)?[-.\s]?(\d{3})\d{4}\b')
        self.date_pattern = re.compile(r'\b(\d{1,2})[-/](\d{1,2})[-/](\d{4})\b|\b(\d{4})[-/](\d{1,2})[-/](\d{4})\b')
        self.skill_keywords = [
            'python', 'javascript', 'react', 'node', 'django', 'flask', 'aws', 'docker',
            'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis',
            'git', 'github', 'gitlab', 'ci/cd', 'jenkins', 'travis',
            'aws', 'azure', 'gcp', 'kubernetes', 'docker', 'terraform',
            'agile', 'scrum', 'kanban', 'jira', 'confluence', 'slack',
            'communication', 'teamwork', 'leadership', 'management', 'mentoring',
            'java', 'spring', 'hibernate', 'maven', 'gradle', 'intellij',
            'cpp', 'c++', 'c', 'algorithms', 'data structures', 'oop',
            'testing', 'unittest', 'pytest', 'selenium', 'cypress',
            'html', 'css', 'javascript', 'typescript', 'webpack', 'babel',
            'rest', 'api', 'graphql', 'microservices', 'soa',
            'security', 'authentication', 'oauth', 'jwt', 'ssl', 'encryption',
            'linux', 'unix', 'bash', 'shell', 'scripting', 'automation',
            'machine learning', 'ai', 'tensorflow', 'pytorch', 'scikit-learn',
            'data science', 'pandas', 'numpy', 'matplotlib', 'jupyter',
            'devops', 'monitoring', 'logging', 'metrics', 'alerting',
            'cloud', 'serverless', 'lambda', 'functions', 'api gateway'
        ]
    
    def parse_resume(self, raw_text: str) -> Dict[str, Any]:
        """
        Parse raw resume text into structured JSON format.
        
        Returns:
        {
            "personal_info": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-0123",
                "location": "San Francisco, CA",
                "linkedin": "https://linkedin.com/in/johndoe",
                "portfolio": "https://johndoe.dev"
            },
            "summary": "Software engineer with 5 years of experience...",
            "skills": {
                "technical": [
                    {
                        "name": "Python",
                        "level": "advanced",
                        "years_of_experience": 5,
                        "last_used": "current"
                    }
                ],
                "soft_skills": [
                    {
                        "name": "Communication",
                        "level": "strong"
                    }
                ]
            },
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "location": "San Francisco, CA",
                    "start_date": "2021-01-15",
                    "end_date": "2023-03-15",
                    "current": false,
                    "description": "Led development of scalable web applications...",
                    "achievements": [
                        "Improved application performance by 40%",
                        "Led team of 5 engineers",
                        "Reduced bug reports by 60%"
                    ],
                    "technologies": ["Python", "Django", "PostgreSQL", "Redis", "Docker"]
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "university": "University of California, Berkeley",
                    "location": "Berkeley, CA",
                    "start_date": "2014-09-01",
                    "end_date": "2018-05-31",
                    "gpa": "3.8"
                }
            ],
            "certifications": [
                {
                    "name": "AWS Certified Solutions Architect",
                    "issuer": "Amazon Web Services",
                    "date": "2022-06-15",
                    "expiry_date": "2025-06-15",
                    "credential_id": "AWS-SAA-123456"
                }
            ],
            "projects": [
                {
                    "name": "E-commerce Platform",
                    "description": "Built a full-stack e-commerce platform...",
                    "technologies": ["React", "Node.js", "MongoDB", "Docker"],
                    "start_date": "2022-01-01",
                    "end_date": "2022-06-30",
                    "url": "https://project-demo.com",
                    "achievements": [
                        "Handled 10,000+ concurrent users",
                        "Implemented real-time inventory management",
                        "Reduced page load time by 50%"
                    ]
                }
            ],
            "languages": [
                {
                    "language": "English",
                    "proficiency": "native"
                },
                {
                    "language": "Spanish",
                    "proficiency": "professional"
                }
            ],
            "metadata": {
                "total_years_experience": 8,
                "education_level": "bachelor",
                "certifications_count": 3,
                "projects_count": 5,
                "technical_skills_count": 15,
                "soft_skills_count": 8,
                "last_updated": "2026-04-02T22:19:00Z"
            }
        }
        """
        lines = raw_text.split('\n')
        parsed = {
            "personal_info": {},
            "summary": "",
            "skills": {"technical": [], "soft_skills": []},
            "experience": [],
            "education": [],
            "certifications": [],
            "projects": [],
            "languages": [],
            "metadata": {}
        }
        
        current_section = None
        current_experience = None
        current_education = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Personal Information
            if line.lower().startswith('email:'):
                email = line.split(':', 1)[1].strip()
                if self.email_pattern.match(email):
                    parsed["personal_info"]["email"] = email
            
            elif line.lower().startswith('phone:'):
                phone = line.split(':', 1)[1].strip()
                if self.phone_pattern.match(phone):
                    parsed["personal_info"]["phone"] = phone
            
            elif line.lower().startswith('linkedin:'):
                linkedin = line.split(':', 1)[1].strip()
                if linkedin.startswith('http'):
                    parsed["personal_info"]["linkedin"] = linkedin
            
            elif line.lower().startswith('summary:'):
                parsed["summary"] = line.split(':', 1)[1].strip()
            
            # Skills
            elif line.lower().startswith('skills:'):
                skills_text = line.split(':', 1)[1].strip()
                technical_skills, soft_skills = self._parse_skills(skills_text)
                parsed["skills"]["technical"] = technical_skills
                parsed["skills"]["soft_skills"] = soft_skills
            
            # Experience
            elif line.lower().startswith('experience:'):
                if current_experience:
                    parsed["experience"].append(current_experience)
                    current_experience = None
                experience_data = line.split(':', 1)[1].strip()
                current_experience = self._parse_experience(experience_data)
            
            # Education
            elif line.lower().startswith('education:'):
                if current_education:
                    parsed["education"].append(current_education)
                    current_education = None
                education_data = line.split(':', 1)[1].strip()
                current_education = self._parse_education(education_data)
            
            # Certifications
            elif line.lower().startswith('certifications:'):
                cert_data = line.split(':', 1)[1].strip()
                parsed["certifications"].append(self._parse_certification(cert_data))
            
            # Projects
            elif line.lower().startswith('projects:'):
                project_data = line.split(':', 1)[1].strip()
                parsed["projects"].append(self._parse_project(project_data))
            
            # Languages
            elif line.lower().startswith('languages:'):
                languages_data = line.split(':', 1)[1].strip()
                parsed["languages"] = self._parse_languages(languages_data)
        
        # Complete any ongoing sections
        if current_experience:
            parsed["experience"].append(current_experience)
        if current_education:
            parsed["education"].append(current_education)
        
        # Calculate metadata
        parsed["metadata"] = self._calculate_metadata(parsed)
        
        return parsed
    
    def _parse_skills(self, skills_text: str) -> List[Dict[str, Any]]:
        """Parse skills section into technical and soft skills."""
        technical_skills = []
        soft_skills = []
        
        # Simple keyword-based parsing for skills
        words = re.findall(r'\b\w+\b', skills_text.lower())
        
        for word in words:
            word = word.lower()
            if word in self.skill_keywords:
                skill = {
                    "name": word.title(),
                    "level": "intermediate",  # Default assumption
                    "years_of_experience": self._estimate_experience(word, skills_text),
                    "last_used": "current"
                }
                
                # Try to determine level from context
                if any(level_word in skills_text.lower() for level_word in ['expert', 'senior', 'lead', 'principal']):
                    skill["level"] = "advanced"
                elif any(level_word in skills_text.lower() for level_word in ['junior', 'entry', 'beginner']):
                    skill["level"] = "beginner"
                
                if self._is_technical_skill(word):
                    technical_skills.append(skill)
                else:
                    soft_skills.append(skill)
        
        return technical_skills + soft_skills
    
    def _is_technical_skill(self, word: str) -> bool:
        """Determine if a word is likely a technical skill."""
        technical_indicators = [
            'python', 'java', 'javascript', 'react', 'node', 'angular', 'vue',
            'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'git', 'github', 'ci/cd', 'devops', 'linux', 'unix',
            'html', 'css', 'api', 'rest', 'graphql', 'microservices',
            'machine learning', 'ai', 'tensorflow', 'pytorch', 'data science',
            'algorithms', 'data structures', 'testing', 'agile', 'scrum'
        ]
        return word.lower() in technical_indicators
    
    def _estimate_experience(self, skill: str, context: str) -> int:
        """Estimate years of experience for a skill based on context."""
        # Look for years mentioned near the skill
        year_matches = re.findall(r'\b(\d+)\s*(?:years?|yrs?)\b', context.lower())
        if year_matches:
            return int(year_matches[0])
        
        # Look for months mentioned
        month_matches = re.findall(r'\b(\d+)\s*(?:months?|mos?)\b', context.lower())
        if month_matches:
            return max(1, int(month_matches[0]) // 12)
        
        return 2  # Default assumption
    
    def _parse_experience(self, experience_text: str) -> Dict[str, Any]:
        """Parse experience section."""
        lines = experience_text.split('\n')
        experience = {
            "title": "",
            "company": "",
            "location": "",
            "start_date": "",
            "end_date": "",
            "current": False,
            "description": "",
            "achievements": [],
            "technologies": []
        }
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.lower().startswith('title:'):
                experience["title"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('company:'):
                experience["company"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('location:'):
                experience["location"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('dates:'):
                dates = line.split(':', 1)[1].strip()
                start_end = re.findall(r'(\d{4}[-/]\d{1,2}[-/]\d{4})', dates)
                if start_end:
                    experience["start_date"] = start_end[0]
                    experience["end_date"] = start_end[1]
            elif line.lower().startswith('current:'):
                experience["current"] = 'true' in line.lower()
            elif line.lower().startswith('description:'):
                experience["description"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('achievements:'):
                achievements_text = line.split(':', 1)[1].strip()
                experience["achievements"] = [
                    achievement.strip() for achievement in achievements_text.split(',') if achievement.strip()
                ]
            elif line.lower().startswith('technologies:'):
                tech_text = line.split(':', 1)[1].strip()
                experience["technologies"] = [
                    tech.strip() for tech in tech_text.split(',') if tech.strip()
                ]
        
        return experience
    
    def _parse_education(self, education_text: str) -> Dict[str, Any]:
        """Parse education section."""
        lines = education_text.split('\n')
        education = {
            "degree": "",
            "field": "",
            "university": "",
            "location": "",
            "start_date": "",
            "end_date": "",
            "gpa": ""
        }
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.lower().startswith('degree:'):
                education["degree"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('field:'):
                education["field"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('university:'):
                education["university"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('location:'):
                education["location"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('dates:'):
                dates = line.split(':', 1)[1].strip()
                start_end = re.findall(r'(\d{4}[-/]\d{1,2}[-/]\d{4})', dates)
                if start_end:
                    education["start_date"] = start_end[0]
                    education["end_date"] = start_end[1]
            elif line.lower().startswith('gpa:'):
                education["gpa"] = line.split(':', 1)[1].strip()
        
        return education
    
    def _parse_certification(self, cert_text: str) -> Dict[str, Any]:
        """Parse certification section."""
        lines = cert_text.split('\n')
        certification = {
            "name": "",
            "issuer": "",
            "date": "",
            "expiry_date": "",
            "credential_id": ""
        }
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.lower().startswith('name:'):
                certification["name"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('issuer:'):
                certification["issuer"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('date:'):
                certification["date"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('expires:'):
                certification["expiry_date"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('id:'):
                certification["credential_id"] = line.split(':', 1)[1].strip()
        
        return certification
    
    def _parse_project(self, project_text: str) -> Dict[str, Any]:
        """Parse project section."""
        lines = project_text.split('\n')
        project = {
            "name": "",
            "description": "",
            "technologies": [],
            "start_date": "",
            "end_date": "",
            "url": "",
            "achievements": []
        }
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.lower().startswith('name:'):
                project["name"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('description:'):
                project["description"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('technologies:'):
                tech_text = line.split(':', 1)[1].strip()
                project["technologies"] = [
                    tech.strip() for tech in tech_text.split(',') if tech.strip()
                ]
            elif line.lower().startswith('dates:'):
                dates = line.split(':', 1)[1].strip()
                start_end = re.findall(r'(\d{4}[-/]\d{1,2}[-/]\d{4})', dates)
                if start_end:
                    project["start_date"] = start_end[0]
                    project["end_date"] = start_end[1]
            elif line.lower().startswith('url:'):
                project["url"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('achievements:'):
                achievements_text = line.split(':', 1)[1].strip()
                project["achievements"] = [
                    achievement.strip() for achievement in achievements_text.split(',') if achievement.strip()
                ]
        
        return project
    
    def _parse_languages(self, languages_text: str) -> List[Dict[str, Any]]:
        """Parse languages section."""
        languages = []
        lines = languages_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.lower().startswith('language:'):
                parts = line.split(':', 1)
                if len(parts) > 1:
                    language = parts[1].strip()
                    proficiency = "intermediate"  # Default
                    if len(parts) > 2:
                        proficiency = parts[2].strip().lower()
                        if proficiency in ['native', 'fluent', 'professional', 'advanced', 'intermediate', 'basic']:
                            proficiency = proficiency
                    
                    languages.append({
                        "language": language,
                        "proficiency": proficiency
                    })
        
        return languages
    
    def _calculate_metadata(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate metadata from parsed resume."""
        metadata = {
            "total_years_experience": 0,
            "education_level": "unknown",
            "certifications_count": len(parsed.get("certifications", [])),
            "projects_count": len(parsed.get("projects", [])),
            "technical_skills_count": len(parsed.get("skills", {}).get("technical", [])),
            "soft_skills_count": len(parsed.get("skills", {}).get("soft_skills", [])),
            "last_updated": datetime.utcnow().isoformat()
        }
        
        # Calculate total years of experience
        for exp in parsed.get("experience", []):
            if exp.get("start_date") and exp.get("end_date"):
                # Simple year calculation
                start_year = int(exp["start_date"][:4])
                end_year = int(exp["end_date"][:4])
                years = end_year - start_year
                metadata["total_years_experience"] = max(metadata["total_years_experience"], years)
        
        # Determine education level
        education = parsed.get("education", [])
        if education:
            highest_degree = "unknown"
            for edu in education:
                degree = edu.get("degree", "").lower()
                if "bachelor" in degree or "bs" in degree:
                    highest_degree = "bachelor"
                elif "master" in degree or "ms" in degree:
                    highest_degree = "master"
                elif "phd" in degree or "doctorate" in degree:
                    highest_degree = "phd"
            metadata["education_level"] = highest_degree
        
        return metadata
