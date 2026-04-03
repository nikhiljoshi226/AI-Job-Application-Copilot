from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re

class TailoringSuggester:
    """Service to generate resume tailoring suggestions based on JD analysis."""
    
    def __init__(self):
        # Suggestion types
        self.suggestion_types = {
            "summary": "Professional summary optimization",
            "skills": "Skills section enhancement",
            "experience": "Experience bullet improvement",
            "projects": "Project emphasis adjustment"
        }
        
        # Evidence confidence levels
        self.confidence_levels = {
            "high": 0.9,
            "medium": 0.7,
            "low": 0.5,
            "none": 0.0
        }
        
        # Common action verbs for experience bullets
        self.action_verbs = [
            "developed", "built", "created", "implemented", "designed", "architected",
            "led", "managed", "mentored", "trained", "guided", "supervised",
            "optimized", "improved", "enhanced", "streamlined", "automated",
            "launched", "deployed", "maintained", "updated", "upgraded",
            "collaborated", "coordinated", "partnered", "integrated", "connected"
        ]
        
        # Quantifiable metrics
        self.metric_patterns = [
            r"(\d+)%\s*(?:improvement|reduction|increase|decrease|growth)",
            r"(\d+)(?:x|fold|times)\s*(?:improvement|reduction|increase|growth)",
            r"(\d+)\s*(?:users|customers|clients|employees|team members)",
            r"\$(\d+(?:,\d{3})*(?:k|m|b?)",
            r"(\d+)\s*(?:days|weeks|months|years)",
            r"(\d+\.?\d*)\s*(?:seconds|minutes|hours)"
        ]
    
    def generate_suggestions(self, parsed_resume: Dict[str, Any], truth_bank: Dict[str, Any], parsed_jd: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate tailoring suggestions for resume improvement.
        
        Returns:
        {
            "suggestions": {
                "summary": [
                    {
                        "type": "enhancement",
                        "current_text": "Software engineer with 5 years of experience",
                        "suggested_text": "Senior Software Engineer with 5 years of experience in full-stack development, specializing in Python and Django applications",
                        "reasoning": "Added seniority level and specific technologies to match JD requirements",
                        "evidence": {
                            "source": "resume_experience",
                            "confidence": "high",
                            "reference": "Senior Software Engineer at Tech Corp (2021-2023)"
                        },
                        "truthfulness_score": 0.95
                    }
                ],
                "skills": [
                    {
                        "type": "addition",
                        "current_section": "Skills",
                        "current_content": ["Python", "JavaScript", "React"],
                        "suggested_addition": "Django, PostgreSQL, Docker",
                        "reasoning": "Missing JD-required skills: Django and PostgreSQL are required, Docker is preferred",
                        "evidence": {
                            "source": "resume_experience",
                            "confidence": "high",
                            "reference": "Python experience in multiple roles"
                        },
                        "truthfulness_score": 0.90
                    }
                ],
                "experience": [
                    {
                        "type": "bullet_enhancement",
                        "section": "Senior Software Engineer at Tech Corp",
                        "current_bullet": "Developed web applications",
                        "suggested_bullet": "Developed scalable web applications using Python and Django, serving 10,000+ concurrent users with 99.9% uptime",
                        "reasoning": "Added quantifiable metrics and specific technologies to demonstrate impact",
                        "evidence": {
                            "source": "resume_experience",
                            "confidence": "high",
                            "reference": "Achievements: Improved application performance by 40%"
                        },
                        "truthfulness_score": 0.85
                    }
                ],
                "projects": [
                    {
                        "type": "emphasis_adjustment",
                        "project_name": "E-commerce Platform",
                        "current_description": "Built a web application",
                        "suggested_description": "Built a full-stack e-commerce platform using React and Node.js, implementing payment processing, inventory management, and real-time analytics for 10,000+ monthly users",
                        "reasoning": "Enhanced description to highlight scale, technologies, and business impact relevant to JD requirements",
                        "evidence": {
                            "source": "resume_projects",
                            "confidence": "medium",
                            "reference": "Project exists in resume"
                        },
                        "truthfulness_score": 0.80
                    }
                ]
            },
            "unsupported_requirements": [
                {
                    "requirement": "Kubernetes expertise",
                    "jd_section": "required_skills",
                    "impact": "high",
                    "suggestion": "Cannot fabricate Kubernetes experience. Consider highlighting any containerization or cloud platform experience instead."
                }
            ],
            "guardrail_violations": [],
            "metadata": {
                "total_suggestions": 4,
                "high_confidence_suggestions": 3,
                "unsupported_count": 1,
                "truthfulness_score": 0.88,
                "processing_time_ms": 1250,
                "generated_at": "2026-04-02T23:34:00Z"
            }
        }
        """
        suggestions = {
            "suggestions": {
                "summary": [],
                "skills": [],
                "experience": [],
                "projects": []
            },
            "unsupported_requirements": [],
            "guardrail_violations": [],
            "metadata": {}
        }
        
        # Generate suggestions for each section
        suggestions["suggestions"]["summary"] = self._generate_summary_suggestions(parsed_resume, truth_bank, parsed_jd)
        suggestions["suggestions"]["skills"] = self._generate_skills_suggestions(parsed_resume, truth_bank, parsed_jd)
        suggestions["suggestions"]["experience"] = self._generate_experience_suggestions(parsed_resume, truth_bank, parsed_jd)
        suggestions["suggestions"]["projects"] = self._generate_projects_suggestions(parsed_resume, truth_bank, parsed_jd)
        
        # Identify unsupported requirements
        suggestions["unsupported_requirements"] = self._identify_unsupported_requirements(parsed_resume, parsed_jd)
        
        # Check for guardrail violations
        suggestions["guardrail_violations"] = self._check_guardrail_violations(suggestions["suggestions"])
        
        # Calculate metadata
        suggestions["metadata"] = self._calculate_suggestions_metadata(suggestions)
        
        return suggestions
    
    def _generate_summary_suggestions(self, parsed_resume: Dict[str, Any], truth_bank: Dict[str, Any], parsed_jd: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate summary section suggestions."""
        suggestions = []
        
        current_summary = parsed_resume.get("summary", "")
        jd_summary = parsed_jd.get("parsed_content", {}).get("summary", "")
        jd_title = parsed_jd.get("job_title", "")
        jd_level = parsed_jd.get("parsed_content", {}).get("role_type", {}).get("experience_level", "")
        
        # Extract key skills from JD
        jd_required_skills = [skill["skill"] for skill in parsed_jd.get("parsed_content", {}).get("required_skills", [])]
        jd_keywords = parsed_jd.get("parsed_content", {}).get("keywords", [])
        
        # Extract user's experience level
        user_experience = truth_bank.get("professional_facts", {}).get("total_years_experience", 0)
        current_role = truth_bank.get("professional_facts", {}).get("current_role", "")
        
        # Suggestion 1: Add seniority level if missing
        if jd_level in ["senior", "lead", "principal"] and "senior" not in current_summary.lower():
            suggestion = self._create_summary_suggestion(
                current_summary,
                f"{jd_level.title()} {jd_title}",
                f"Added seniority level and job title to match JD requirements. Experience level: {user_experience} years.",
                "enhancement",
                {
                    "source": "truth_bank",
                    "confidence": "high",
                    "reference": f"Professional facts: {user_experience} years experience, current role: {current_role}"
                }
            )
            suggestions.append(suggestion)
        
        # Suggestion 2: Add key skills if missing
        missing_skills = []
        for skill in jd_required_skills[:3]:  # Top 3 skills
            skill_lower = skill.lower()
            if skill_lower not in current_summary.lower():
                missing_skills.append(skill)
        
        if missing_skills:
            suggested_summary = self._add_skills_to_summary(current_summary, missing_skills)
            suggestion = self._create_summary_suggestion(
                current_summary,
                suggested_summary,
                f"Added key skills: {', '.join(missing_skills)} to match JD requirements.",
                "enhancement",
                {
                    "source": "jd_analysis",
                    "confidence": "high",
                    "reference": f"JD required skills: {', '.join(jd_required_skills)}"
                }
            )
            suggestions.append(suggestion)
        
        # Suggestion 3: Add industry/domain context
        domain_clues = parsed_jd.get("parsed_content", {}).get("domain_clues", [])
        if domain_clues:
            domain = domain_clues[0]["domain"]
            if domain.lower() not in current_summary.lower():
                suggested_summary = f"{current_summary} with expertise in {domain.title()} solutions"
                suggestion = self._create_summary_suggestion(
                    current_summary,
                    suggested_summary,
                    f"Added domain expertise to align with company focus: {domain.title()}",
                    "enhancement",
                    {
                        "source": "jd_analysis",
                        "confidence": "medium",
                        "reference": f"JD domain clues: {domain}"
                    }
                )
                suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_skills_suggestions(self, parsed_resume: Dict[str, Any], truth_bank: Dict[str, Any], parsed_jd: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate skills section suggestions."""
        suggestions = []
        
        resume_skills = self._extract_resume_skills(parsed_resume)
        jd_required = parsed_jd.get("parsed_content", {}).get("required_skills", [])
        jd_preferred = parsed_jd.get("parsed_content", {}).get("preferred_skills", [])
        
        # Find missing required skills
        missing_required = []
        for jd_skill in jd_required:
            if not self._has_skill(resume_skills, jd_skill["skill"]):
                missing_required.append(jd_skill)
        
        # Find missing preferred skills
        missing_preferred = []
        for jd_skill in jd_preferred:
            if not self._has_skill(resume_skills, jd_skill["skill"]):
                missing_preferred.append(jd_skill)
        
        # Generate suggestions for missing skills
        all_missing = missing_required + missing_preferred
        for missing_skill in all_missing[:5]:  # Limit to top 5
            suggestion = self._create_skill_suggestion(
                missing_skill,
                resume_skills,
                truth_bank
            )
            suggestions.append(suggestion)
        
        # Suggest skill improvements for existing skills
        existing_skills = [skill for skill in resume_skills 
                          if self._should_improve_skill(skill, jd_required + jd_preferred)]
        
        for skill in existing_skills[:3]:  # Limit to top 3
            suggestion = self._create_skill_improvement_suggestion(skill, jd_required + jd_preferred)
            suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_experience_suggestions(self, parsed_resume: Dict[str, Any], truth_bank: Dict[str, Any], parsed_jd: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate experience section suggestions."""
        suggestions = []
        
        resume_experience = parsed_resume.get("experience", [])
        jd_responsibilities = parsed_jd.get("parsed_content", {}).get("responsibilities", [])
        jd_keywords = parsed_jd.get("parsed_content", {}).get("keywords", [])
        
        for exp in resume_experience:
            exp_suggestions = []
            
            # Analyze each bullet point
            if "achievements" in exp:
                for i, achievement in enumerate(exp["achievements"]):
                    enhanced_bullet = self._enhance_experience_bullet(achievement, jd_keywords, jd_responsibilities)
                    if enhanced_bullet != achievement:
                        suggestion = self._create_experience_suggestion(
                            exp,
                            i,
                            achievement,
                            enhanced_bullet,
                            "bullet_enhancement"
                        )
                        exp_suggestions.append(suggestion)
            
            # Suggest adding missing responsibilities
            current_responsibilities = [exp.get("description", "") for exp in resume_experience]
            missing_resps = self._find_missing_responsibilities(current_responsibilities, jd_responsibilities)
            
            for missing_resp in missing_resps[:2]:  # Limit to 2 per experience
                suggestion = self._create_experience_addition_suggestion(
                    exp,
                    missing_resp,
                    "addition"
                )
                exp_suggestions.append(suggestion)
            
            suggestions.extend(exp_suggestions)
        
        return suggestions
    
    def _generate_projects_suggestions(self, parsed_resume: Dict[str, Any], truth_bank: Dict[str, Any], parsed_jd: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate projects section suggestions."""
        suggestions = []
        
        resume_projects = parsed_resume.get("projects", [])
        jd_keywords = parsed_jd.get("parsed_content", {}).get("keywords", [])
        jd_tech = [kw.lower() for kw in jd_keywords if kw.lower() in ["python", "java", "javascript", "react", "docker", "aws", "sql"]]
        
        for project in resume_projects:
            project_suggestions = []
            
            # Enhance project description
            current_desc = project.get("description", "")
            enhanced_desc = self._enhance_project_description(current_desc, jd_keywords, jd_tech)
            
            if enhanced_desc != current_desc:
                suggestion = self._create_project_suggestion(
                    project,
                    "description",
                    current_desc,
                    enhanced_desc,
                    "description_enhancement"
                )
                project_suggestions.append(suggestion)
            
            # Suggest adding missing technologies
            current_tech = project.get("technologies", [])
            missing_tech = [tech for tech in jd_tech if tech not in [t.lower() for t in current_tech]]
            
            if missing_tech:
                suggestion = self._create_project_tech_suggestion(
                    project,
                    current_tech,
                    missing_tech,
                    "technology_addition"
                )
                project_suggestions.append(suggestion)
            
            # Suggest adding achievements/metrics
            if not project.get("achievements"):
                suggestion = self._create_project_achievement_suggestion(project)
                project_suggestions.append(suggestion)
            
            suggestions.extend(project_suggestions)
        
        return suggestions
    
    def _create_summary_suggestion(self, current_text: str, suggested_text: str, reasoning: str, suggestion_type: str, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary suggestion."""
        return {
            "type": suggestion_type,
            "current_text": current_text,
            "suggested_text": suggested_text,
            "reasoning": reasoning,
            "evidence": evidence,
            "truthfulness_score": self._calculate_truthfulness_score(evidence)
        }
    
    def _create_skill_suggestion(self, jd_skill: Dict[str, Any], resume_skills: List[Dict[str, Any]], truth_bank: Dict[str, Any]) -> Dict[str, Any]:
        """Create a skill addition suggestion."""
        skill_name = jd_skill["skill"]
        
        # Check if user has any related experience
        related_experience = self._find_related_experience(resume_skills, skill_name, truth_bank)
        
        return {
            "type": "addition",
            "skill_name": skill_name,
            "category": jd_skill.get("category", "unknown"),
            "jd_requirement": jd_skill.get("skill_type", "unknown"),
            "current_section": "Skills",
            "suggested_addition": skill_name,
            "reasoning": f"Missing JD-{'required' if jd_skill.get('skill_type') == 'required' else 'preferred'} skill: {skill_name}",
            "evidence": {
                "source": "gap_analysis",
                "confidence": "low" if not related_experience else "medium",
                "reference": f"Related experience: {related_experience}" if related_experience else "No related experience found"
            },
            "truthfulness_score": 0.3 if not related_experience else 0.7
        }
    
    def _create_skill_improvement_suggestion(self, resume_skill: Dict[str, Any], jd_skills: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a skill improvement suggestion."""
        skill_name = resume_skill["skill"]
        
        # Find JD requirements for this skill
        jd_requirements = [skill for skill in jd_skills if skill["skill"].lower() == skill_name.lower()]
        
        if not jd_requirements:
            return None
        
        jd_req = jd_requirements[0]
        required_level = jd_req.get("experience_level", "not specified")
        
        return {
            "type": "improvement",
            "skill_name": skill_name,
            "category": resume_skill.get("category", "unknown"),
            "current_level": resume_skill.get("experience_level", "not specified"),
            "suggested_level": required_level,
            "reasoning": f"JD requires {required_level} of {skill_name} experience",
            "evidence": {
                "source": "jd_analysis",
                "confidence": "high",
                "reference": f"JD requirement: {required_level}"
            },
            "truthfulness_score": 0.8
        }
    
    def _create_experience_suggestion(self, experience: Dict[str, Any], bullet_index: int, current_text: str, suggested_text: str, suggestion_type: str) -> Dict[str, Any]:
        """Create an experience bullet suggestion."""
        return {
            "type": suggestion_type,
            "section": f"{experience.get('title', '')} at {experience.get('company', '')}",
            "bullet_index": bullet_index,
            "current_bullet": current_text,
            "suggested_bullet": suggested_text,
            "reasoning": "Enhanced bullet with quantifiable metrics and specific technologies",
            "evidence": {
                "source": "resume_experience",
                "confidence": "high",
                "reference": f"Experience at {experience.get('company', '')}"
            },
            "truthfulness_score": 0.85
        }
    
    def _create_experience_addition_suggestion(self, experience: Dict[str, Any], missing_resp: str, suggestion_type: str) -> Dict[str, Any]:
        """Create an experience addition suggestion."""
        return {
            "type": suggestion_type,
            "section": f"{experience.get('title', '')} at {experience.get('company', '')}",
            "suggested_addition": missing_resp,
            "reasoning": f"Add missing responsibility: {missing_resp}",
            "evidence": {
                "source": "gap_analysis",
                "confidence": "medium",
                "reference": f"JD responsibilities: {missing_resp}"
            },
            "truthfulness_score": 0.6
        }
    
    def _create_project_suggestion(self, project: Dict[str, Any], field: str, current_text: str, suggested_text: str, suggestion_type: str) -> Dict[str, Any]:
        """Create a project suggestion."""
        return {
            "type": suggestion_type,
            "project_name": project.get("name", ""),
            "field": field,
            "current_text": current_text,
            "suggested_text": suggested_text,
            "reasoning": f"Enhanced {field} to better align with JD requirements",
            "evidence": {
                "source": "resume_projects",
                "confidence": "medium",
                "reference": f"Project: {project.get('name', '')}"
            },
            "truthfulness_score": 0.75
        }
    
    def _create_project_tech_suggestion(self, project: Dict[str, Any], current_tech: List[str], missing_tech: List[str], suggestion_type: str) -> Dict[str, Any]:
        """Create a project technology suggestion."""
        return {
            "type": suggestion_type,
            "project_name": project.get("name", ""),
            "current_technologies": current_tech,
            "suggested_addition": missing_tech,
            "reasoning": f"Add missing JD-relevant technologies: {', '.join(missing_tech)}",
            "evidence": {
                "source": "gap_analysis",
                "confidence": "medium",
                "reference": f"Project: {project.get('name', '')}"
            },
            "truthfulness_score": 0.7
        }
    
    def _create_project_achievement_suggestion(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Create a project achievement suggestion."""
        return {
            "type": "addition",
            "project_name": project.get("name", ""),
            "suggested_addition": "Add quantifiable achievements with metrics (e.g., 'Improved performance by X%', 'Served Y users', 'Reduced costs by $Z')",
            "reasoning": "Projects without quantifiable impact are less compelling to recruiters",
            "evidence": {
                "source": "best_practices",
                "confidence": "low",
                "reference": "Project enhancement guidelines"
            },
            "truthfulness_score": 0.4
        }
    
    def _identify_unsupported_requirements(self, parsed_resume: Dict[str, Any], parsed_jd: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify JD requirements that cannot be supported by resume."""
        unsupported = []
        
        resume_skills = self._extract_resume_skills(parsed_resume)
        resume_experience = parsed_resume.get("experience", [])
        
        # Check required skills
        required_skills = parsed_jd.get("parsed_content", {}).get("required_skills", [])
        for skill in required_skills:
            if not self._has_skill(resume_skills, skill["skill"]):
                impact = "high" if skill.get("skill_type") == "required" else "medium"
                unsupported.append({
                    "requirement": skill["skill"],
                    "jd_section": "required_skills",
                    "impact": impact,
                    "suggestion": f"Cannot fabricate {skill['skill']} experience. Consider highlighting any related experience instead."
                })
        
        # Check experience level requirements
        jd_level = parsed_jd.get("parsed_content", {}).get("role_type", {}).get("experience_level", "")
        resume_level = self._get_resume_experience_level(parsed_resume)
        
        if self._is_level_mismatch(resume_level, jd_level):
            unsupported.append({
                "requirement": f"{jd_level.title()} level experience",
                "jd_section": "role_type",
                "impact": "high",
                "suggestion": f"Cannot fabricate {jd_level} experience. Consider highlighting transferable skills and relevant accomplishments instead."
            })
        
        # Check specific experience requirements
        jd_qualifications = parsed_jd.get("parsed_content", {}).get("qualifications", [])
        for qual in jd_qualifications:
            if "years" in qual.lower():
                years_required = self._extract_years_requirement(qual)
                user_years = self._calculate_total_years_experience(resume_experience)
                if user_years < years_required:
                    unsupported.append({
                        "requirement": qual,
                        "jd_section": "qualifications",
                        "impact": "high",
                        "suggestion": f"Cannot fabricate additional years of experience. Focus on transferable skills and accomplishments."
                    })
        
        return unsupported
    
    def _check_guardrail_violations(self, suggestions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for guardrail violations in suggestions."""
        violations = []
        
        for section, section_suggestions in suggestions.items():
            if section == "suggestions":
                for suggestion in section_suggestions:
                    # Check for fabrication indicators
                    if self._contains_fabrication_indicators(suggestion):
                        violations.append({
                            "type": "fabrication_detected",
                            "section": section,
                            "suggestion_id": suggestion.get("skill_name", suggestion.get("project_name", "unknown")),
                            "reason": "Suggestion contains indicators of fabricated experience",
                            "suggestion": suggestion
                        })
                    
                    # Check for excessive claims
                    if self._contains_excessive_claims(suggestion):
                        violations.append({
                            "type": "excessive_claims",
                            "section": section,
                            "suggestion_id": suggestion.get("skill_name", suggestion.get("project_name", "unknown")),
                            "reason": "Suggestion makes excessive claims beyond reasonable scope",
                            "suggestion": suggestion
                        })
        
        return violations
    
    def _contains_fabrication_indicators(self, suggestion: Dict[str, Any]) -> bool:
        """Check if suggestion contains indicators of fabrication."""
        text = f"{suggestion.get('suggested_text', '')} {suggestion.get('suggested_addition', '')}".lower()
        
        fabrication_indicators = [
            "expert in", "master of", "world-class", "best in class",
            "revolutionized", "pioneered", "invented", "created from scratch",
            "10+ years", "15+ years", "20+ years"  # Unless supported by evidence
        ]
        
        return any(indicator in text for indicator in fabrication_indicators)
    
    def _contains_excessive_claims(self, suggestion: Dict[str, Any]) -> Dict[str, Any]:
        """Check if suggestion makes excessive claims."""
        text = f"{suggestion.get('suggested_text', '')} {suggestion.get('suggested_addition', '')}".lower()
        
        # Look for multiple high-value metrics without evidence
        metric_count = 0
        for pattern in self.metric_patterns:
            matches = re.findall(pattern, text)
            metric_count += len(matches)
        
        return metric_count > 3  # More than 3 quantifiable metrics without evidence
    
    def _extract_resume_skills(self, parsed_resume: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract skills from parsed resume."""
        skills = []
        
        technical_skills = parsed_resume.get("skills", {}).get("technical", [])
        for skill in technical_skills:
            skills.append({
                "skill": skill.get("name", "").lower(),
                "category": "technical",
                "experience_level": skill.get("years_of_experience", 0),
                "evidence": skill.get("evidence_source", "unknown")
            })
        
        soft_skills = parsed_resume.get("skills", {}).get("soft_skills", [])
        for skill in soft_skills:
            skills.append({
                "skill": skill.get("name", "").lower(),
                "category": "soft",
                "experience_level": skill.get("proficiency_level", "intermediate"),
                "evidence": skill.get("evidence_source", "unknown")
            })
        
        return skills
    
    def _has_skill(self, resume_skills: List[Dict[str, Any]], skill_name: str) -> bool:
        """Check if resume contains a specific skill."""
        skill_name_lower = skill_name.lower()
        return any(skill["skill"] == skill_name_lower for skill in resume_skills)
    
    def _should_improve_skill(self, resume_skill: Dict[str, Any], jd_skills: List[Dict[str, Any]]) -> bool:
        """Check if a skill should be improved."""
        skill_name = resume_skill["skill"].lower()
        
        # Find JD requirements for this skill
        jd_requirements = [skill for skill in jd_skills if skill["skill"].lower() == skill_name.lower()]
        
        if not jd_requirements:
            return False
        
        # Check if JD requires higher level
        jd_req = jd_requirements[0]
        required_level = jd_req.get("experience_level", "not specified")
        current_level = str(resume_skill.get("experience_level", 0))
        
        if required_level != "not specified":
            if "5+" in required_level and current_level not in ["5+", "6+", "7+", "8+", "9+", "10+"]:
                return True
            if "3+" in required_level and current_level not in ["3+", "4+", "5+", "6+", "7+", "8+", "9+", "10+"]:
                return True
            if "2+" in required_level and current_level not in ["2+", "3+", "4+", "5+", "6+", "7+", "8+", "9+", "10+"]:
                return True
        
        return False
    
    def _find_related_experience(self, resume_skills: List[Dict[str, Any]], skill_name: str, truth_bank: Dict[str, Any]) -> str:
        """Find related experience for a skill."""
        # Check if skill appears in experience descriptions
        experience_facts = truth_bank.get("experience_facts", {})
        companies_worked = experience_facts.get("companies_worked", [])
        
        for company in companies_worked:
            company_desc = f"{company.get('title', '')} {company.get('description', '')}".lower()
            if skill_name.lower() in company_desc:
                return company.get("title", "")
        
        return ""
    
    def _enhance_experience_bullet(self, bullet: str, jd_keywords: List[str], jd_responsibilities: List[str]) -> str:
        """Enhance an experience bullet with quantifiable metrics."""
        enhanced = bullet
        
        # Add action verb if missing
        if not any(verb in enhanced.lower() for verb in self.action_verbs):
            for verb in self.action_verbs:
                if verb in enhanced.lower():
                    enhanced = enhanced.replace(enhanced.split()[0], verb, 1)
                    break
        
        # Add quantifiable metrics if missing
        has_metrics = any(re.search(pattern, enhanced) for pattern in self.metric_patterns)
        if not has_metrics:
            # Try to infer metrics from context
            if "performance" in enhanced.lower():
                enhanced += " with measurable improvements"
            elif "team" in enhanced.lower():
                enhanced += " for team of 5+ engineers"
            elif "users" in enhanced.lower():
                enhanced += " for 10,000+ users"
            elif "revenue" in enhanced.lower():
                enhanced += " contributing to revenue growth"
        
        # Add JD-relevant keywords if missing
        for keyword in jd_keywords[:3]:  # Top 3 keywords
            if keyword.lower() not in enhanced.lower():
                enhanced += f" using {keyword.title()}"
                break
        
        return enhanced
    
    def _enhance_project_description(self, description: str, jd_keywords: List[str], jd_tech: List[str]) -> str:
        """Enhance project description with JD-relevant details."""
        enhanced = description
        
        # Add scale if missing
        if "users" not in enhanced.lower() and "customers" not in enhanced.lower() and "clients" not in enhanced.lower():
            enhanced += " for 10,000+ users"
        
        # Add relevant technologies
        tech_to_add = [tech for tech in jd_tech if tech not in enhanced.lower()]
        if tech_to_add:
            enhanced += f" using {', '.join([t.title() for t in tech_to_add[:3]])}"
        
        # Add business impact
        if "impact" not in enhanced.lower() and "business" in jd_keywords:
            enhanced += " with measurable business impact"
        
        return enhanced
    
    def _find_missing_responsibilities(self, current_responsibilities: List[str], jd_responsibilities: List[str]) -> List[str]:
        """Find missing responsibilities from JD."""
        current_text = " ".join(current_responsibilities).lower()
        missing = []
        
        for resp in jd_responsibilities:
            resp_lower = resp.lower()
            if resp_lower not in current_text:
                missing.append(resp)
        
        return missing
    
    def _add_skills_to_summary(self, summary: str, skills: List[str]) -> str:
        """Add skills to summary."""
        if not skills:
            return summary
        
        skills_text = ", ".join([skill.title() for skill in skills])
        return f"{summary} with expertise in {skills_text}"
    
    def _get_resume_experience_level(self, parsed_resume: Dict[str, Any]) -> str:
        """Get experience level from resume."""
        metadata = parsed_resume.get("metadata", {})
        total_years = metadata.get("total_years_experience", 0)
        
        if total_years >= 8:
            return "senior"
        elif total_years >= 5:
            return "mid"
        elif total_years >= 2:
            return "junior"
        else:
            return "entry"
    
    def _is_level_mismatch(self, resume_level: str, jd_level: str) -> bool:
        """Check if experience levels are mismatched."""
        level_mapping = {
            "entry": 1, "junior": 2, "mid": 3, "senior": 4, "lead": 5, "principal": 6, "expert": 7
        }
        
        resume_score = level_mapping.get(resume_level, 0)
        jd_score = level_mapping.get(jd_level, 0)
        
        return resume_score < jd_score
    
    def _extract_years_requirement(self, qualification: str) -> int:
        """Extract years requirement from qualification text."""
        import re
        match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)', qualification.lower())
        return int(match.group(1)) if match else 0
    
    def _calculate_total_years_experience(self, experience: List[Dict[str, Any]]) -> int:
        """Calculate total years of experience."""
        total_years = 0
        for exp in experience:
            start_date = exp.get("start_date", "")
            end_date = exp.get("end_date", "")
            
            if start_date and end_date:
                try:
                    start_year = int(start_date[:4])
                    end_year = int(end_date[:4])
                    years = end_year - start_year
                    total_years = max(total_years, years)
                except (ValueError, IndexError):
                    continue
        
        return total_years
    
    def _calculate_truthfulness_score(self, evidence: Dict[str, Any]) -> float:
        """Calculate truthfulness score based on evidence."""
        source = evidence.get("source", "unknown")
        confidence = evidence.get("confidence", "low")
        
        # Base score on evidence source
        source_scores = {
            "resume_experience": 0.9,
            "truth_bank": 0.95,
            "jd_analysis": 0.7,
            "gap_analysis": 0.3,
            "best_practices": 0.2,
            "unknown": 0.1
        }
        
        base_score = source_scores.get(source, 0.5)
        
        # Adjust based on confidence
        return base_score * confidence
    
    def _calculate_suggestions_metadata(self, suggestions: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate metadata for suggestions."""
        all_suggestions = []
        
        for section in suggestions.get("suggestions", {}).values():
            all_suggestions.extend(section)
        
        high_confidence = len([s for s in all_suggestions if s.get("truthfulness_score", 0) >= 0.8])
        
        return {
            "total_suggestions": len(all_suggestions),
            "high_confidence_suggestions": high_confidence,
            "unsupported_count": len(suggestions.get("unsupported_requirements", [])),
            "truthfulness_score": sum(s.get("truthfulness_score", 0) for s in all_suggestions) / len(all_suggestions) if all_suggestions else 0,
            "processing_time_ms": 0,  # Would be set by actual processing time
            "generated_at": datetime.utcnow().isoformat()
        }
