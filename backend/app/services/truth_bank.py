from typing import Dict, List, Any
import json

class TruthBank:
    """Service to create and manage factual profile information from resume."""
    
    def __init__(self):
        self.facts = []
    
    def create_truth_bank(self, parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a truth bank object summarizing factual profile information from resume.
        
        Returns:
        {
            "personal_facts": {
                "name": "John Doe",
                "contact_info": {
                    "email": "john.doe@example.com",
                    "phone": "+1-555-0123",
                    "location": "San Francisco, CA"
                },
                "professional_links": {
                    "linkedin": "https://linkedin.com/in/johndoe",
                    "portfolio": "https://johndoe.dev"
                }
            },
            "professional_facts": {
                "total_years_experience": 8,
                "current_role": "Senior Software Engineer",
                "current_company": "Tech Corp",
                "industry": "Software Development",
                "career_level": "Senior"
            },
            "education_facts": {
                "highest_degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "university": "University of California, Berkeley",
                "graduation_year": 2018,
                "gpa": "3.8"
            },
            "skill_facts": {
                "verified_technical_skills": [
                    {
                        "skill": "Python",
                        "years_experience": 5,
                        "proficiency_level": "advanced",
                        "evidence_source": "experience_section"
                    }
                ],
                "verified_soft_skills": [
                    {
                        "skill": "Communication",
                        "proficiency_level": "strong",
                        "evidence_source": "experience_section"
                    }
                ],
                "skill_categories": {
                    "programming_languages": ["Python", "JavaScript", "Java"],
                    "databases": ["PostgreSQL", "MongoDB", "Redis"],
                    "cloud_platforms": ["AWS", "Azure"],
                    "devops_tools": ["Docker", "Kubernetes", "Git"],
                    "methodologies": ["Agile", "Scrum"]
                }
            },
            "experience_facts": {
                "companies_worked": [
                    {
                        "company": "Tech Corp",
                        "title": "Senior Software Engineer",
                        "duration": "2021-2023",
                        "verified": True
                    }
                ],
                "total_companies": 3,
                "management_experience": True,
                "team_leadership": True,
                "project_management": False
            },
            "achievement_facts": {
                "quantifiable_achievements": [
                    {
                        "achievement": "Improved application performance by 40%",
                        "metric": "40% performance improvement",
                        "context": "Web application optimization",
                        "verified": True
                    }
                ],
                "leadership_achievements": [
                    {
                        "achievement": "Led team of 5 engineers",
                        "team_size": 5,
                        "duration": "2 years",
                        "verified": True
                    }
                ],
                "technical_achievements": [
                    {
                        "achievement": "Reduced bug reports by 60%",
                        "metric": "60% reduction in bug reports",
                        "context": "Quality improvement initiative",
                        "verified": True
                    }
                ]
            },
            "education_facts": {
                "degrees": [
                    {
                        "degree": "Bachelor of Science",
                        "field": "Computer Science",
                        "university": "University of California, Berkeley",
                        "graduation_year": 2018,
                        "verified": True
                    }
                ],
                "certifications": [
                    {
                        "name": "AWS Certified Solutions Architect",
                        "issuer": "Amazon Web Services",
                        "date": "2022-06-15",
                        "verified": True
                    }
                ],
                "continuous_learning": True,
                "certifications_count": 3
            },
            "project_facts": {
                "completed_projects": [
                    {
                        "name": "E-commerce Platform",
                        "technologies": ["React", "Node.js", "MongoDB"],
                        "impact": "Handled 10,000+ concurrent users",
                        "verified": True
                    }
                ],
                "total_projects": 5,
                "open_source_contributions": 0,
                "personal_projects": 2
            },
            "metadata": {
                "total_facts": 25,
                "verified_facts": 20,
                "confidence_score": 0.85,
                "data_sources": ["resume_text", "structured_sections"],
                "last_updated": "2026-04-02T22:19:00Z",
                "verification_status": "high_confidence"
            }
        }
        """
        truth_bank = {
            "personal_facts": self._extract_personal_facts(parsed_resume),
            "professional_facts": self._extract_professional_facts(parsed_resume),
            "education_facts": self._extract_education_facts(parsed_resume),
            "skill_facts": self._extract_skill_facts(parsed_resume),
            "experience_facts": self._extract_experience_facts(parsed_resume),
            "achievement_facts": self._extract_achievement_facts(parsed_resume),
            "project_facts": self._extract_project_facts(parsed_resume),
            "metadata": self._calculate_truth_metadata(parsed_resume)
        }
        
        return truth_bank
    
    def _extract_personal_facts(self, parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
        """Extract personal facts from parsed resume."""
        personal_info = parsed_resume.get("personal_info", {})
        
        return {
            "name": personal_info.get("name", "Unknown"),
            "contact_info": {
                "email": personal_info.get("email", ""),
                "phone": personal_info.get("phone", ""),
                "location": personal_info.get("location", "")
            },
            "professional_links": {
                "linkedin": personal_info.get("linkedin", ""),
                "portfolio": personal_info.get("portfolio", "")
            }
        }
    
    def _extract_professional_facts(self, parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
        """Extract professional facts from parsed resume."""
        experience = parsed_resume.get("experience", [])
        metadata = parsed_resume.get("metadata", {})
        
        current_role = ""
        current_company = ""
        career_level = "Unknown"
        
        if experience:
            # Find current or most recent position
            current_exp = None
            for exp in experience:
                if exp.get("current", False):
                    current_exp = exp
                    break
            
            if not current_exp:
                # Get most recent by end date
                current_exp = max(experience, key=lambda x: x.get("end_date", ""))
            
            if current_exp:
                current_role = current_exp.get("title", "")
                current_company = current_exp.get("company", "")
        
        # Determine career level
        total_years = metadata.get("total_years_experience", 0)
        if total_years >= 8:
            career_level = "Senior"
        elif total_years >= 4:
            career_level = "Mid-level"
        elif total_years >= 2:
            career_level = "Junior"
        else:
            career_level = "Entry-level"
        
        return {
            "total_years_experience": total_years,
            "current_role": current_role,
            "current_company": current_company,
            "industry": "Software Development",  # Default, could be enhanced
            "career_level": career_level
        }
    
    def _extract_education_facts(self, parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
        """Extract education facts from parsed resume."""
        education = parsed_resume.get("education", [])
        certifications = parsed_resume.get("certifications", [])
        
        highest_degree = "Unknown"
        field_of_study = ""
        university = ""
        graduation_year = None
        gpa = ""
        
        if education:
            # Find highest degree
            degree_levels = {
                "phd": 4,
                "master": 3,
                "bachelor": 2,
                "associate": 1,
                "high school": 0
            }
            
            highest_edu = None
            highest_level = -1
            
            for edu in education:
                degree = edu.get("degree", "").lower()
                for level_name, level_value in degree_levels.items():
                    if level_name in degree and level_value > highest_level:
                        highest_level = level_value
                        highest_edu = edu
            
            if highest_edu:
                highest_degree = highest_edu.get("degree", "Unknown")
                field_of_study = highest_edu.get("field", "")
                university = highest_edu.get("university", "")
                graduation_year = self._extract_year(highest_edu.get("end_date", ""))
                gpa = highest_edu.get("gpa", "")
        
        return {
            "highest_degree": highest_degree,
            "field_of_study": field_of_study,
            "university": university,
            "graduation_year": graduation_year,
            "gpa": gpa,
            "certifications": certifications,
            "certifications_count": len(certifications),
            "continuous_learning": len(certifications) > 0
        }
    
    def _extract_skill_facts(self, parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
        """Extract skill facts from parsed resume."""
        skills = parsed_resume.get("skills", {})
        technical_skills = skills.get("technical", [])
        soft_skills = skills.get("soft_skills", [])
        
        # Categorize skills
        categories = {
            "programming_languages": [],
            "databases": [],
            "cloud_platforms": [],
            "devops_tools": [],
            "methodologies": []
        }
        
        # Enhanced technical skills with evidence
        verified_technical = []
        for skill in technical_skills:
            verified_skill = {
                "skill": skill.get("name", ""),
                "years_experience": skill.get("years_of_experience", 0),
                "proficiency_level": skill.get("level", "intermediate"),
                "evidence_source": "experience_section",
                "verified": True
            }
            verified_technical.append(verified_skill)
            
            # Categorize
            skill_name = skill.get("name", "").lower()
            if skill_name in ["python", "javascript", "java", "cpp", "c++", "c", "typescript"]:
                categories["programming_languages"].append(skill.get("name", ""))
            elif skill_name in ["postgresql", "mysql", "mongodb", "redis", "nosql", "sql"]:
                categories["databases"].append(skill.get("name", ""))
            elif skill_name in ["aws", "azure", "gcp"]:
                categories["cloud_platforms"].append(skill.get("name", ""))
            elif skill_name in ["docker", "kubernetes", "git", "jenkins", "ci/cd"]:
                categories["devops_tools"].append(skill.get("name", ""))
            elif skill_name in ["agile", "scrum", "kanban"]:
                categories["methodologies"].append(skill.get("name", ""))
        
        # Enhanced soft skills with evidence
        verified_soft = []
        for skill in soft_skills:
            verified_skill = {
                "skill": skill.get("name", ""),
                "proficiency_level": skill.get("level", "intermediate"),
                "evidence_source": "experience_section",
                "verified": True
            }
            verified_soft.append(verified_skill)
        
        return {
            "verified_technical_skills": verified_technical,
            "verified_soft_skills": verified_soft,
            "skill_categories": categories,
            "total_technical_skills": len(verified_technical),
            "total_soft_skills": len(verified_soft)
        }
    
    def _extract_experience_facts(self, parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
        """Extract experience facts from parsed resume."""
        experience = parsed_resume.get("experience", [])
        
        companies_worked = []
        total_companies = len(experience)
        management_experience = False
        team_leadership = False
        project_management = False
        
        for exp in experience:
            company_fact = {
                "company": exp.get("company", ""),
                "title": exp.get("title", ""),
                "duration": f"{exp.get('start_date', '')} - {exp.get('end_date', 'present')}",
                "verified": True
            }
            companies_worked.append(company_fact)
            
            # Check for leadership/management keywords
            title = exp.get("title", "").lower()
            description = exp.get("description", "").lower()
            
            if any(keyword in title for keyword in ["manager", "lead", "principal", "director", "head"]):
                management_experience = True
                team_leadership = True
            
            if any(keyword in title or keyword in description for keyword in ["project manager", "pm", "agile", "scrum master"]):
                project_management = True
            
            # Check achievements for leadership
            achievements = exp.get("achievements", [])
            for achievement in achievements:
                if any(keyword in achievement.lower() for keyword in ["led", "managed", "team", "mentored", "supervised"]):
                    team_leadership = True
                    break
        
        return {
            "companies_worked": companies_worked,
            "total_companies": total_companies,
            "management_experience": management_experience,
            "team_leadership": team_leadership,
            "project_management": project_management
        }
    
    def _extract_achievement_facts(self, parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
        """Extract achievement facts from parsed resume."""
        experience = parsed_resume.get("experience", [])
        projects = parsed_resume.get("projects", [])
        
        quantifiable_achievements = []
        leadership_achievements = []
        technical_achievements = []
        
        # Extract from experience
        for exp in experience:
            achievements = exp.get("achievements", [])
            for achievement in achievements:
                achievement_lower = achievement.lower()
                
                # Look for quantifiable achievements
                if any(indicator in achievement_lower for indicator in ["%", "increased", "decreased", "reduced", "improved", "saved", "generated", "handled", "managed"]):
                    quantifiable_achievements.append({
                        "achievement": achievement,
                        "metric": self._extract_metric(achievement),
                        "context": exp.get("title", ""),
                        "verified": True
                    })
                
                # Look for leadership achievements
                if any(indicator in achievement_lower for indicator in ["led", "managed", "team", "mentored", "supervised", "trained"]):
                    team_size = self._extract_team_size(achievement)
                    leadership_achievements.append({
                        "achievement": achievement,
                        "team_size": team_size,
                        "duration": "unknown",  # Could be enhanced
                        "verified": True
                    })
                
                # Look for technical achievements
                if any(indicator in achievement_lower for indicator in ["developed", "built", "implemented", "designed", "architected", "optimized"]):
                    technical_achievements.append({
                        "achievement": achievement,
                        "metric": self._extract_metric(achievement),
                        "context": exp.get("title", ""),
                        "verified": True
                    })
        
        # Extract from projects
        for project in projects:
            project_achievements = project.get("achievements", [])
            for achievement in project_achievements:
                achievement_lower = achievement.lower()
                
                if any(indicator in achievement_lower for indicator in ["%", "users", "performance", "speed", "time"]):
                    quantifiable_achievements.append({
                        "achievement": achievement,
                        "metric": self._extract_metric(achievement),
                        "context": project.get("name", ""),
                        "verified": True
                    })
        
        return {
            "quantifiable_achievements": quantifiable_achievements,
            "leadership_achievements": leadership_achievements,
            "technical_achievements": technical_achievements,
            "total_achievements": len(quantifiable_achievements) + len(leadership_achievements) + len(technical_achievements)
        }
    
    def _extract_project_facts(self, parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
        """Extract project facts from parsed resume."""
        projects = parsed_resume.get("projects", [])
        
        completed_projects = []
        total_projects = len(projects)
        personal_projects = 0
        
        for project in projects:
            project_fact = {
                "name": project.get("name", ""),
                "technologies": project.get("technologies", []),
                "impact": self._extract_impact(project),
                "verified": True
            }
            completed_projects.append(project_fact)
            
            # Count personal projects (simplified logic)
            if "personal" in project.get("name", "").lower() or "portfolio" in project.get("name", "").lower():
                personal_projects += 1
        
        return {
            "completed_projects": completed_projects,
            "total_projects": total_projects,
            "open_source_contributions": 0,  # Could be enhanced
            "personal_projects": personal_projects
        }
    
    def _calculate_truth_metadata(self, parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate metadata for truth bank."""
        metadata = parsed_resume.get("metadata", {})
        
        # Calculate confidence score based on completeness
        sections = ["personal_info", "summary", "skills", "experience", "education", "certifications", "projects"]
        completed_sections = sum(1 for section in sections if parsed_resume.get(section))
        confidence_score = completed_sections / len(sections)
        
        # Count total facts (simplified)
        total_facts = (
            len(parsed_resume.get("experience", [])) +
            len(parsed_resume.get("education", [])) +
            len(parsed_resume.get("certifications", [])) +
            len(parsed_resume.get("projects", [])) +
            len(parsed_resume.get("skills", {}).get("technical", [])) +
            len(parsed_resume.get("skills", {}).get("soft_skills", []))
        )
        
        verification_status = "high_confidence" if confidence_score >= 0.8 else "medium_confidence" if confidence_score >= 0.6 else "low_confidence"
        
        return {
            "total_facts": total_facts,
            "verified_facts": total_facts,  # All from resume are considered verified
            "confidence_score": round(confidence_score, 2),
            "data_sources": ["resume_text", "structured_sections"],
            "last_updated": metadata.get("last_updated", ""),
            "verification_status": verification_status
        }
    
    def _extract_year(self, date_string: str) -> int:
        """Extract year from date string."""
        import re
        year_match = re.search(r'\b(19|20)\d{2}\b', date_string)
        return int(year_match.group()) if year_match else None
    
    def _extract_metric(self, achievement: str) -> str:
        """Extract metric from achievement text."""
        import re
        
        # Look for percentages
        percent_match = re.search(r'(\d+)%', achievement)
        if percent_match:
            return f"{percent_match.group(1)}%"
        
        # Look for numbers with units
        number_match = re.search(r'(\d+(?:,\d+)*)\s*(?:users|times|hours|days|months|years|dollars|USD|$)', achievement)
        if number_match:
            return number_match.group(0)
        
        # Look for time improvements
        time_match = re.search(r'(\d+%)\s*(?:faster|slower|improvement|reduction)', achievement)
        if time_match:
            return time_match.group(0)
        
        return achievement
    
    def _extract_team_size(self, achievement: str) -> int:
        """Extract team size from achievement text."""
        import re
        
        # Look for team size
        team_match = re.search(r'team\s+of\s+(\d+)', achievement.lower())
        if team_match:
            return int(team_match.group(1))
        
        # Look for "managed X people"
        managed_match = re.search(r'managed\s+(\d+)', achievement.lower())
        if managed_match:
            return int(managed_match.group(1))
        
        # Look for "led X"
        led_match = re.search(r'led\s+(\d+)', achievement.lower())
        if led_match:
            return int(led_match.group(1))
        
        return 0
    
    def _extract_impact(self, project: Dict[str, Any]) -> str:
        """Extract impact from project."""
        achievements = project.get("achievements", [])
        if achievements:
            # Return the first achievement as impact
            return achievements[0]
        
        # Look for impact indicators in description
        description = project.get("description", "").lower()
        if any(indicator in description for indicator in ["users", "customers", "clients", "performance", "scalability"]):
            return project.get("description", "")
        
        return "Project completed successfully"
