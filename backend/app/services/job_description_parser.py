import re
from typing import Dict, List, Any, Optional
from datetime import datetime

class JobDescriptionParser:
    """Service to parse job description text into structured JSON."""
    
    def __init__(self):
        # Role type indicators
        self.role_types = {
            "full_time": ["full-time", "full time", "permanent", "direct hire"],
            "part_time": ["part-time", "part time", "contract", "temporary"],
            "contract": ["contract", "temporary", "freelance", "consultant"],
            "internship": ["intern", "internship", "co-op", "student"],
            "remote": ["remote", "work from home", "wfh", "virtual"],
            "hybrid": ["hybrid", "flexible", "partial remote"]
        }
        
        # Skill level indicators
        self.skill_levels = {
            "required": ["required", "must have", "essential", "necessary"],
            "preferred": ["preferred", "desired", "nice to have", "bonus"],
            "pluses": ["plus", "advantage", "helpful", "beneficial"]
        }
        
        # Common technical skills
        self.technical_skills = [
            "python", "javascript", "java", "cpp", "c++", "c#", "php", "ruby", "go", "rust",
            "react", "angular", "vue", "node", "express", "django", "flask", "spring",
            "aws", "azure", "gcp", "cloud", "serverless", "lambda", "functions",
            "docker", "kubernetes", "k8s", "container", "orchestration",
            "sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
            "git", "github", "gitlab", "bitbucket", "ci/cd", "jenkins", "travis",
            "testing", "unittest", "pytest", "jest", "cypress", "selenium",
            "html", "css", "sass", "webpack", "babel", "typescript",
            "rest", "api", "graphql", "microservices", "soa", "web services",
            "machine learning", "ai", "tensorflow", "pytorch", "scikit-learn",
            "data science", "pandas", "numpy", "jupyter", "analytics",
            "linux", "unix", "bash", "shell", "scripting", "automation",
            "security", "authentication", "oauth", "jwt", "ssl", "encryption",
            "devops", "monitoring", "logging", "metrics", "alerting",
            "agile", "scrum", "kanban", "jira", "confluence", "slack"
        ]
        
        # Common soft skills
        self.soft_skills = [
            "communication", "teamwork", "leadership", "management", "mentoring",
            "problem solving", "critical thinking", "analytical", "creativity",
            "collaboration", "interpersonal", "presentation", "written communication",
            "time management", "organization", "planning", "prioritization",
            "adaptability", "flexibility", "learning", "continuous improvement",
            "attention to detail", "quality assurance", "customer service",
            "negotiation", "conflict resolution", "decision making", "strategic thinking"
        ]
        
        # Domain/industry keywords
        self.domain_keywords = [
            "fintech", "healthcare", "e-commerce", "retail", "manufacturing",
            "education", "government", "nonprofit", "startup", "enterprise",
            "saas", "b2b", "b2c", "mobile", "web", "desktop", "embedded",
            "gaming", "social media", "marketing", "sales", "finance",
            "insurance", "banking", "logistics", "supply chain", "transportation",
            "energy", "utilities", "telecommunications", "media", "entertainment",
            "real estate", "construction", "agriculture", "biotech", "pharmaceutical"
        ]
        
        # Experience level indicators
        self.experience_levels = {
            "entry": ["entry level", "junior", "0-2 years", "recent graduate"],
            "mid": ["mid-level", "3-5 years", "intermediate", "associate"],
            "senior": ["senior", "5-7 years", "lead", "principal"],
            "expert": ["expert", "8+ years", "staff", "architect", "director"]
        }
    
    def parse_job_description(self, job_title: str, company: str, jd_text: str) -> Dict[str, Any]:
        """
        Parse job description text into structured JSON format.
        
        Returns:
        {
            "job_title": "Senior Software Engineer",
            "company": "Tech Corp",
            "parsed_content": {
                "summary": "We are looking for a Senior Software Engineer...",
                "required_skills": [
                    {
                        "skill": "Python",
                        "category": "technical",
                        "experience_level": "5+ years",
                        "evidence": "5+ years of Python experience required"
                    }
                ],
                "preferred_skills": [
                    {
                        "skill": "AWS",
                        "category": "technical",
                        "experience_level": "2+ years",
                        "evidence": "AWS experience is a plus"
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
                "keywords": [
                    "python", "django", "postgresql", "aws", "agile", "scrum"
                ],
                "role_type": {
                    "employment_type": "full_time",
                    "work_arrangement": "hybrid",
                    "experience_level": "senior"
                },
                "domain_clues": [
                    {
                        "domain": "saas",
                        "confidence": 0.8,
                        "evidence": "SaaS platform development"
                    }
                ],
                "compensation": {
                    "salary_min": 120000,
                    "salary_max": 180000,
                    "currency": "USD",
                    "benefits": ["Health insurance", "401k", "Unlimited PTO"]
                },
                "location": {
                    "city": "San Francisco",
                    "state": "CA",
                    "country": "USA",
                    "remote_policy": "hybrid"
                }
            },
            "metadata": {
                "total_skills": 15,
                "required_skills_count": 8,
                "preferred_skills_count": 7,
                "responsibilities_count": 6,
                "keywords_count": 12,
                "parsing_confidence": 0.85,
                "last_updated": "2026-04-02T22:29:00Z"
            }
        }
        """
        parsed = {
            "job_title": job_title.strip(),
            "company": company.strip(),
            "parsed_content": {
                "summary": self._extract_summary(jd_text),
                "required_skills": self._extract_required_skills(jd_text),
                "preferred_skills": self._extract_preferred_skills(jd_text),
                "responsibilities": self._extract_responsibilities(jd_text),
                "qualifications": self._extract_qualifications(jd_text),
                "keywords": self._extract_keywords(jd_text),
                "role_type": self._extract_role_type(jd_text),
                "domain_clues": self._extract_domain_clues(jd_text),
                "compensation": self._extract_compensation(jd_text),
                "location": self._extract_location(jd_text)
            },
            "metadata": self._calculate_metadata(parsed["parsed_content"])
        }
        
        return parsed
    
    def _extract_summary(self, jd_text: str) -> str:
        """Extract job summary/description."""
        lines = jd_text.split('\n')
        summary_lines = []
        
        # Look for summary in first few paragraphs
        for i, line in enumerate(lines[:10]):
            line = line.strip()
            if not line:
                continue
            
            # Skip headers and section titles
            if any(header in line.lower() for header in ['requirements', 'responsibilities', 'qualifications', 'skills', 'about']):
                break
            
            # Skip very short lines (likely headers)
            if len(line) < 20:
                continue
            
            summary_lines.append(line)
            
            # Stop after 2-3 sentences or 300 characters
            if len(' '.join(summary_lines)) > 300 or line.endswith('.') and len(summary_lines) >= 3:
                break
        
        return ' '.join(summary_lines)[:500]  # Limit to 500 characters
    
    def _extract_required_skills(self, jd_text: str) -> List[Dict[str, Any]]:
        """Extract required skills with evidence."""
        required_skills = []
        lines = jd_text.lower().split('\n')
        
        # Look for required skills section
        in_required_section = False
        section_keywords = ['required', 'must have', 'essential', 'necessary', 'qualifications']
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if we're in a required skills section
            if any(keyword in line for keyword in section_keywords):
                in_required_section = True
                continue
            
            # Exit section when we hit a different section
            if in_required_section and any(section in line for section in ['preferred', 'nice to have', 'bonus', 'responsibilities']):
                break
            
            # Extract skills from current line if in required section
            if in_required_section or any(keyword in line for keyword in section_keywords):
                skills = self._extract_skills_from_line(line, "required")
                required_skills.extend(skills)
        
        return required_skills
    
    def _extract_preferred_skills(self, jd_text: str) -> List[Dict[str, Any]]:
        """Extract preferred skills with evidence."""
        preferred_skills = []
        lines = jd_text.lower().split('\n')
        
        # Look for preferred skills section
        in_preferred_section = False
        section_keywords = ['preferred', 'desired', 'nice to have', 'bonus', 'plus']
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if we're in a preferred skills section
            if any(keyword in line for keyword in section_keywords):
                in_preferred_section = True
                continue
            
            # Exit section when we hit a different section
            if in_preferred_section and any(section in line for section in ['required', 'must have', 'responsibilities']):
                break
            
            # Extract skills from current line if in preferred section
            if in_preferred_section or any(keyword in line for keyword in section_keywords):
                skills = self._extract_skills_from_line(line, "preferred")
                preferred_skills.extend(skills)
        
        return preferred_skills
    
    def _extract_skills_from_line(self, line: str, skill_type: str) -> List[Dict[str, Any]]:
        """Extract skills from a single line of text."""
        skills = []
        
        # Check for technical skills
        for tech_skill in self.technical_skills:
            if tech_skill in line:
                experience_level = self._extract_experience_level(line)
                skills.append({
                    "skill": tech_skill.title(),
                    "category": "technical",
                    "experience_level": experience_level,
                    "evidence": line[:100] + "..." if len(line) > 100 else line,
                    "skill_type": skill_type
                })
        
        # Check for soft skills
        for soft_skill in self.soft_skills:
            if soft_skill in line:
                skills.append({
                    "skill": soft_skill.title(),
                    "category": "soft",
                    "experience_level": "not specified",
                    "evidence": line[:100] + "..." if len(line) > 100 else line,
                    "skill_type": skill_type
                })
        
        return skills
    
    def _extract_experience_level(self, line: str) -> str:
        """Extract experience level from text."""
        # Look for years of experience
        year_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)', line)
        if year_match:
            years = int(year_match.group(1))
            if years >= 8:
                return "8+ years"
            elif years >= 5:
                return "5+ years"
            elif years >= 3:
                return "3+ years"
            elif years >= 2:
                return "2+ years"
            else:
                return "1+ years"
        
        # Look for level indicators
        if any(level in line for level in ["senior", "lead", "principal"]):
            return "senior level"
        elif any(level in line for level in ["junior", "entry", "associate"]):
            return "junior level"
        elif any(level in line for level in ["mid", "intermediate"]):
            return "mid level"
        
        return "not specified"
    
    def _extract_responsibilities(self, jd_text: str) -> List[str]:
        """Extract job responsibilities."""
        responsibilities = []
        lines = jd_text.split('\n')
        
        in_responsibilities_section = False
        section_keywords = ['responsibilities', 'duties', 'what you\'ll do', 'role', 'position']
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if we're in responsibilities section
            if any(keyword in line.lower() for keyword in section_keywords):
                in_responsibilities_section = True
                continue
            
            # Exit section when we hit a different section
            if in_responsibilities_section and any(section in line.lower() for section in ['requirements', 'qualifications', 'skills', 'about']):
                break
            
            # Extract responsibilities if in section
            if in_responsibilities_section:
                # Look for bullet points or numbered lists
                if line.startswith(('•', '-', '*', '·', '1.', '2.', '3.', '4.', '5.')):
                    responsibility = line.lstrip('•-*·123456789. ')
                    if len(responsibility) > 10:  # Filter out very short lines
                        responsibilities.append(responsibility)
                elif len(line) > 20 and any(verb in line.lower() for verb in ['develop', 'design', 'create', 'manage', 'lead', 'implement', 'build', 'maintain']):
                    responsibilities.append(line)
        
        return responsibilities[:10]  # Limit to 10 responsibilities
    
    def _extract_qualifications(self, jd_text: str) -> List[str]:
        """Extract job qualifications."""
        qualifications = []
        lines = jd_text.split('\n')
        
        in_qualifications_section = False
        section_keywords = ['qualifications', 'requirements', 'what you need', 'education', 'experience']
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if we're in qualifications section
            if any(keyword in line.lower() for keyword in section_keywords):
                in_qualifications_section = True
                continue
            
            # Exit section when we hit a different section
            if in_qualifications_section and any(section in line.lower() for section in ['responsibilities', 'duties', 'benefits']):
                break
            
            # Extract qualifications if in section
            if in_qualifications_section:
                # Look for bullet points or degree/experience patterns
                if line.startswith(('•', '-', '*', '·', '1.', '2.', '3.', '4.', '5.')):
                    qualification = line.lstrip('•-*·123456789. ')
                    if len(qualification) > 10:
                        qualifications.append(qualification)
                elif any(indicator in line.lower() for indicator in ['degree', 'bachelor', 'master', 'phd', 'years', 'experience']):
                    qualifications.append(line)
        
        return qualifications[:10]  # Limit to 10 qualifications
    
    def _extract_keywords(self, jd_text: str) -> List[str]:
        """Extract important keywords from job description."""
        keywords = []
        jd_lower = jd_text.lower()
        
        # Extract technical keywords
        for skill in self.technical_skills:
            if skill in jd_lower:
                keywords.append(skill)
        
        # Extract soft skill keywords
        for skill in self.soft_skills:
            if skill in jd_lower:
                keywords.append(skill)
        
        # Extract domain keywords
        for domain in self.domain_keywords:
            if domain in jd_lower:
                keywords.append(domain)
        
        # Remove duplicates and return
        return list(set(keywords))[:50]  # Limit to 50 keywords
    
    def _extract_role_type(self, jd_text: str) -> Dict[str, str]:
        """Extract role type information."""
        role_type = {
            "employment_type": "unknown",
            "work_arrangement": "unknown",
            "experience_level": "unknown"
        }
        
        jd_lower = jd_text.lower()
        
        # Extract employment type
        for emp_type, indicators in self.role_types.items():
            if any(indicator in jd_lower for indicator in indicators):
                if emp_type in ["full_time", "part_time", "contract", "internship"]:
                    role_type["employment_type"] = emp_type
                elif emp_type in ["remote", "hybrid"]:
                    role_type["work_arrangement"] = emp_type
        
        # Extract experience level
        for exp_level, indicators in self.experience_levels.items():
            if any(indicator in jd_lower for indicator in indicators):
                role_type["experience_level"] = exp_level
                break
        
        return role_type
    
    def _extract_domain_clues(self, jd_text: str) -> List[Dict[str, Any]]:
        """Extract domain/industry clues."""
        domain_clues = []
        jd_lower = jd_text.lower()
        
        for domain in self.domain_keywords:
            if domain in jd_lower:
                # Find the context around the domain keyword
                domain_index = jd_lower.find(domain)
                start = max(0, domain_index - 50)
                end = min(len(jd_text), domain_index + 50)
                context = jd_text[start:end].strip()
                
                domain_clues.append({
                    "domain": domain,
                    "confidence": 0.8,  # Default confidence
                    "evidence": context
                })
        
        return domain_clues[:20]  # Limit to 20 domain clues
    
    def _extract_compensation(self, jd_text: str) -> Dict[str, Any]:
        """Extract compensation information."""
        compensation = {
            "salary_min": None,
            "salary_max": None,
            "currency": "USD",
            "benefits": []
        }
        
        # Look for salary ranges
        salary_patterns = [
            r'\$(\d{2,3},?\d{3})\s*-\s*\$(\d{2,3},?\d{3})',
            r'(\d{2,3},?\d{3})\s*-\s*(\d{2,3},?\d{3})\s*(?:k|k?/year|per year)',
            r'\$(\d{2,3},?\d{3})\s*(?:k|k?/year|per year)',
            r'(\d{2,3},?\d{3})\s*(?:k|k?/year|per year)'
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, jd_text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    min_salary = int(match.group(1).replace(',', ''))
                    max_salary = int(match.group(2).replace(',', ''))
                    compensation["salary_min"] = min_salary * 1000 if min_salary < 100 else min_salary
                    compensation["salary_max"] = max_salary * 1000 if max_salary < 100 else max_salary
                else:
                    salary = int(match.group(1).replace(',', ''))
                    compensation["salary_min"] = salary * 1000 if salary < 100 else salary
                    compensation["salary_max"] = salary * 1000 if salary < 100 else salary
                break
        
        # Look for benefits
        benefits_keywords = ['health insurance', '401k', '401(k)', 'paid time off', 'pto', 'vacation', 'dental', 'vision', 'stock options', 'bonus', 'remote work', 'flexible hours']
        for benefit in benefits_keywords:
            if benefit in jd_text.lower():
                compensation["benefits"].append(benefit.title())
        
        return compensation
    
    def _extract_location(self, jd_text: str) -> Dict[str, str]:
        """Extract location information."""
        location = {
            "city": "",
            "state": "",
            "country": "",
            "remote_policy": "unknown"
        }
        
        # Look for common city/state patterns
        location_patterns = [
            r'([A-Z][a-z]+),\s*([A-Z]{2})',
            r'([A-Z][a-z\s]+),\s*([A-Z]{2})',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, jd_text)
            if match:
                location["city"] = match.group(1)
                location["state"] = match.group(2)
                break
        
        # Look for remote policy
        jd_lower = jd_text.lower()
        if 'remote' in jd_lower:
            location["remote_policy"] = "remote"
        elif 'hybrid' in jd_lower or 'flexible' in jd_lower:
            location["remote_policy"] = "hybrid"
        elif 'on-site' in jd_lower or 'onsite' in jd_lower or 'in-office' in jd_lower:
            location["remote_policy"] = "on-site"
        
        return location
    
    def _calculate_metadata(self, parsed_content: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate metadata for parsed job description."""
        metadata = {
            "total_skills": len(parsed_content.get("required_skills", [])) + len(parsed_content.get("preferred_skills", [])),
            "required_skills_count": len(parsed_content.get("required_skills", [])),
            "preferred_skills_count": len(parsed_content.get("preferred_skills", [])),
            "responsibilities_count": len(parsed_content.get("responsibilities", [])),
            "qualifications_count": len(parsed_content.get("qualifications", [])),
            "keywords_count": len(parsed_content.get("keywords", [])),
            "domain_clues_count": len(parsed_content.get("domain_clues", [])),
            "parsing_confidence": self._calculate_confidence(parsed_content),
            "last_updated": datetime.utcnow().isoformat()
        }
        
        return metadata
    
    def _calculate_confidence(self, parsed_content: Dict[str, Any]) -> float:
        """Calculate parsing confidence based on extracted content."""
        confidence_factors = []
        
        # Check if we have required sections
        if parsed_content.get("required_skills"):
            confidence_factors.append(0.2)
        if parsed_content.get("responsibilities"):
            confidence_factors.append(0.2)
        if parsed_content.get("qualifications"):
            confidence_factors.append(0.2)
        if parsed_content.get("keywords"):
            confidence_factors.append(0.2)
        if parsed_content.get("role_type", {}).get("experience_level") != "unknown":
            confidence_factors.append(0.2)
        
        return min(1.0, sum(confidence_factors))
    
    def validate_parsed_data(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parsed job description data."""
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check required fields
        if not parsed_data.get("job_title"):
            validation_result["errors"].append("Job title is required")
            validation_result["is_valid"] = False
        
        if not parsed_data.get("company"):
            validation_result["errors"].append("Company is required")
            validation_result["is_valid"] = False
        
        # Check parsed content
        parsed_content = parsed_data.get("parsed_content", {})
        
        if not parsed_content.get("required_skills") and not parsed_content.get("preferred_skills"):
            validation_result["warnings"].append("No skills found in job description")
        
        if not parsed_content.get("responsibilities"):
            validation_result["warnings"].append("No responsibilities found in job description")
        
        if not parsed_content.get("keywords"):
            validation_result["warnings"].append("No keywords found in job description")
        
        # Check confidence
        confidence = parsed_data.get("metadata", {}).get("parsing_confidence", 0)
        if confidence < 0.5:
            validation_result["warnings"].append(f"Low parsing confidence: {confidence}")
        
        return validation_result
