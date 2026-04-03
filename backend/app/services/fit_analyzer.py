from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

class FitAnalyzer:
    """Service to analyze fit between resume and job description."""
    
    def __init__(self):
        # Skill importance weights
        self.skill_weights = {
            "required": 1.0,
            "preferred": 0.7,
            "bonus": 0.3
        }
        
        # Experience level mapping
        self.experience_levels = {
            "entry": 1,
            "junior": 2,
            "mid": 3,
            "senior": 4,
            "lead": 5,
            "principal": 6,
            "expert": 7,
            "architect": 8,
            "director": 9,
            "vp": 10
        }
        
        # Skill category importance
        self.category_weights = {
            "technical": 1.0,
            "soft": 0.8,
            "domain": 0.6
        }
    
    def analyze_fit(self, parsed_resume: Dict[str, Any], parsed_jd: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze fit between resume and job description.
        
        Returns:
        {
            "fit_score": 85.5,
            "skills_analysis": {
                "matched_skills": [
                    {
                        "skill": "Python",
                        "category": "technical",
                        "resume_evidence": "5+ years of Python experience",
                        "jd_requirement": "required",
                        "match_strength": "strong"
                    }
                ],
                "missing_skills": [
                    {
                        "skill": "Kubernetes",
                        "category": "technical",
                        "jd_requirement": "preferred",
                        "importance": "medium",
                        "gap_reason": "No Kubernetes experience found in resume"
                    }
                ],
                "partial_matches": [
                    {
                        "skill": "Docker",
                        "category": "technical",
                        "resume_evidence": "Basic Docker experience",
                        "jd_requirement": "preferred",
                        "match_strength": "partial"
                    }
                ]
            },
            "experience_analysis": {
                "level_alignment": "aligned",
                "years_experience_match": "sufficient",
                "relevant_experience_highlights": [
                    {
                        "experience": "Senior Software Engineer at Tech Corp",
                        "relevance_score": 0.9,
                        "alignment_reason": "Direct experience with required technologies and leadership"
                    }
                ],
                "experience_gaps": [
                    {
                        "gap": "No experience with enterprise-scale systems",
                        "impact": "medium",
                        "suggestion": "Highlight any large-scale projects or consider gaining this experience"
                    }
                ]
            },
            "role_alignment": {
                "overall_alignment": "strong",
                "alignment_score": 88.0,
                "strengths": [
                    "Strong technical background with required skills",
                    "Leadership experience matches senior role requirements",
                    "Relevant industry experience"
                ],
                "concerns": [
                    "Limited experience with cloud platforms",
                    "No formal certifications mentioned"
                ],
                "recommendations": [
                    "Highlight cloud projects in resume",
                    "Consider obtaining relevant certifications"
                ]
            },
            "education_analysis": {
                "education_match": "meets_requirements",
                "degree_alignment": "aligned",
                "field_relevance": "high",
                "additional_education_needed": []
            },
            "metadata": {
                "analysis_date": "2026-04-02T23:31:00Z",
                "total_skills_analyzed": 25,
                "matched_skills_count": 18,
                "missing_skills_count": 7,
                "confidence_score": 0.92
            }
        }
        """
        analysis = {
            "fit_score": 0.0,
            "skills_analysis": self._analyze_skills(parsed_resume, parsed_jd),
            "experience_analysis": self._analyze_experience(parsed_resume, parsed_jd),
            "role_alignment": self._analyze_role_alignment(parsed_resume, parsed_jd),
            "education_analysis": self._analyze_education(parsed_resume, parsed_jd),
            "metadata": {}
        }
        
        # Calculate overall fit score
        analysis["fit_score"] = self._calculate_fit_score(analysis)
        
        # Add metadata
        analysis["metadata"] = self._calculate_analysis_metadata(analysis)
        
        return analysis
    
    def _analyze_skills(self, parsed_resume: Dict[str, Any], parsed_jd: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze skill matching between resume and job description."""
        resume_skills = self._extract_resume_skills(parsed_resume)
        jd_skills = self._extract_jd_skills(parsed_jd)
        
        matched_skills = []
        missing_skills = []
        partial_matches = []
        
        # Analyze required skills
        for jd_skill in jd_skills["required"]:
            match_result = self._find_skill_match(jd_skill, resume_skills, "required")
            if match_result["match_type"] == "exact":
                matched_skills.append(match_result)
            elif match_result["match_type"] == "partial":
                partial_matches.append(match_result)
            else:
                missing_skills.append({
                    "skill": jd_skill["skill"],
                    "category": jd_skill.get("category", "unknown"),
                    "jd_requirement": "required",
                    "importance": "high",
                    "gap_reason": f"No {jd_skill['skill']} experience found in resume"
                })
        
        # Analyze preferred skills
        for jd_skill in jd_skills["preferred"]:
            match_result = self._find_skill_match(jd_skill, resume_skills, "preferred")
            if match_result["match_type"] == "exact":
                matched_skills.append(match_result)
            elif match_result["match_type"] == "partial":
                partial_matches.append(match_result)
            else:
                missing_skills.append({
                    "skill": jd_skill["skill"],
                    "category": jd_skill.get("category", "unknown"),
                    "jd_requirement": "preferred",
                    "importance": "medium",
                    "gap_reason": f"No {jd_skill['skill']} experience found in resume"
                })
        
        return {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "partial_matches": partial_matches
        }
    
    def _extract_resume_skills(self, parsed_resume: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract skills from parsed resume."""
        skills = []
        
        # Get technical skills
        technical_skills = parsed_resume.get("skills", {}).get("technical", [])
        for skill in technical_skills:
            skills.append({
                "skill": skill.get("name", "").lower(),
                "category": "technical",
                "experience_level": skill.get("years_of_experience", 0),
                "evidence": skill.get("evidence_source", "experience_section")
            })
        
        # Get soft skills
        soft_skills = parsed_resume.get("skills", {}).get("soft_skills", [])
        for skill in soft_skills:
            skills.append({
                "skill": skill.get("name", "").lower(),
                "category": "soft",
                "experience_level": skill.get("proficiency_level", "intermediate"),
                "evidence": skill.get("evidence_source", "experience_section")
            })
        
        return skills
    
    def _extract_jd_skills(self, parsed_jd: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Extract skills from parsed job description."""
        jd_skills = {
            "required": [],
            "preferred": []
        }
        
        # Get required skills
        required_skills = parsed_jd.get("parsed_content", {}).get("required_skills", [])
        for skill in required_skills:
            jd_skills["required"].append({
                "skill": skill.get("skill", "").lower(),
                "category": skill.get("category", "unknown"),
                "experience_level": skill.get("experience_level", "not specified")
            })
        
        # Get preferred skills
        preferred_skills = parsed_jd.get("parsed_content", {}).get("preferred_skills", [])
        for skill in preferred_skills:
            jd_skills["preferred"].append({
                "skill": skill.get("skill", "").lower(),
                "category": skill.get("category", "unknown"),
                "experience_level": skill.get("experience_level", "not specified")
            })
        
        return jd_skills
    
    def _find_skill_match(self, jd_skill: Dict[str, Any], resume_skills: List[Dict[str, Any]], requirement_type: str) -> Dict[str, Any]:
        """Find matching skill in resume skills."""
        jd_skill_name = jd_skill["skill"].lower()
        
        for resume_skill in resume_skills:
            resume_skill_name = resume_skill["skill"].lower()
            
            # Exact match
            if jd_skill_name == resume_skill_name:
                match_strength = self._determine_match_strength(jd_skill, resume_skill)
                return {
                    "skill": jd_skill["skill"].title(),
                    "category": resume_skill["category"],
                    "resume_evidence": resume_skill.get("evidence", ""),
                    "jd_requirement": requirement_type,
                    "match_strength": match_strength,
                    "match_type": "exact"
                }
            
            # Partial match (similar skills)
            if self._are_similar_skills(jd_skill_name, resume_skill_name):
                return {
                    "skill": f"{jd_skill['skill'].title()} ({resume_skill['skill'].title()})",
                    "category": resume_skill["category"],
                    "resume_evidence": resume_skill.get("evidence", ""),
                    "jd_requirement": requirement_type,
                    "match_strength": "partial",
                    "match_type": "partial"
                }
        
        return {"match_type": "none"}
    
    def _are_similar_skills(self, skill1: str, skill2: str) -> bool:
        """Check if two skills are similar."""
        # Similar skill mappings
        similar_skills = {
            "javascript": ["js", "ecmascript", "node", "nodejs"],
            "python": ["django", "flask", "fastapi"],
            "java": ["spring", "hibernate", "maven"],
            "react": ["reactjs", "react.js"],
            "docker": ["container", "containers"],
            "aws": ["amazon web services", "ec2", "s3"],
            "sql": ["postgresql", "mysql", "database"],
            "git": ["github", "gitlab", "version control"]
        }
        
        for base_skill, variants in similar_skills.items():
            if skill1 in [base_skill] + variants and skill2 in [base_skill] + variants:
                return True
        
        return False
    
    def _determine_match_strength(self, jd_skill: Dict[str, Any], resume_skill: Dict[str, Any]) -> str:
        """Determine match strength based on experience levels."""
        jd_level = jd_skill.get("experience_level", "not specified").lower()
        resume_level = str(resume_skill.get("experience_level", 0)).lower()
        
        # If JD doesn't specify level, assume good match
        if jd_level == "not specified":
            return "strong"
        
        # Extract years from resume level if it's a number
        try:
            resume_years = int(resume_level)
            if "5+" in jd_level and resume_years >= 5:
                return "strong"
            elif "3+" in jd_level and resume_years >= 3:
                return "strong"
            elif "2+" in jd_level and resume_years >= 2:
                return "strong"
            elif resume_years >= 1:
                return "moderate"
            else:
                return "weak"
        except (ValueError, TypeError):
            # Non-numeric experience level
            if resume_level in ["senior", "lead", "expert", "advanced"]:
                return "strong"
            elif resume_level in ["mid", "intermediate"]:
                return "moderate"
            else:
                return "weak"
    
    def _analyze_experience(self, parsed_resume: Dict[str, Any], parsed_jd: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze experience alignment."""
        resume_experience = parsed_resume.get("experience", [])
        jd_requirements = parsed_jd.get("parsed_content", {}).get("qualifications", [])
        
        # Extract experience level requirements
        jd_level = self._extract_jd_experience_level(parsed_jd)
        resume_level = self._extract_resume_experience_level(parsed_resume)
        
        level_alignment = self._compare_experience_levels(resume_level, jd_level)
        
        # Analyze relevant experience highlights
        relevant_highlights = self._find_relevant_experience(resume_experience, parsed_jd)
        
        # Identify experience gaps
        experience_gaps = self._identify_experience_gaps(resume_experience, jd_requirements)
        
        return {
            "level_alignment": level_alignment,
            "years_experience_match": self._assess_years_experience(resume_experience, jd_requirements),
            "relevant_experience_highlights": relevant_highlights,
            "experience_gaps": experience_gaps
        }
    
    def _extract_jd_experience_level(self, parsed_jd: Dict[str, Any]) -> str:
        """Extract experience level from job description."""
        role_type = parsed_jd.get("parsed_content", {}).get("role_type", {})
        return role_type.get("experience_level", "unknown")
    
    def _extract_resume_experience_level(self, parsed_resume: Dict[str, Any]) -> str:
        """Extract experience level from resume."""
        metadata = parsed_resume.get("metadata", {})
        total_years = metadata.get("total_years_experience", 0)
        
        if total_years >= 8:
            return "senior"
        elif total_years >= 4:
            return "mid"
        elif total_years >= 2:
            return "junior"
        else:
            return "entry"
    
    def _compare_experience_levels(self, resume_level: str, jd_level: str) -> str:
        """Compare experience levels."""
        if jd_level == "unknown":
            return "unknown"
        
        resume_score = self.experience_levels.get(resume_level, 0)
        jd_score = self.experience_levels.get(jd_level, 0)
        
        if resume_score >= jd_score:
            return "aligned"
        elif resume_score >= jd_score - 1:
            return "close"
        else:
            return "misaligned"
    
    def _assess_years_experience(self, resume_experience: List[Dict[str, Any]], jd_requirements: List[str]) -> str:
        """Assess if years of experience match requirements."""
        # Look for years requirements in JD
        for requirement in jd_requirements:
            if "years" in requirement.lower():
                # Extract number from requirement
                import re
                match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)', requirement.lower())
                if match:
                    required_years = int(match.group(1))
                    total_years = self._calculate_total_years_experience(resume_experience)
                    if total_years >= required_years:
                        return "sufficient"
                    else:
                        return "insufficient"
        
        return "not_specified"
    
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
    
    def _find_relevant_experience(self, resume_experience: List[Dict[str, Any]], parsed_jd: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find relevant experience highlights."""
        relevant_highlights = []
        jd_keywords = parsed_jd.get("parsed_content", {}).get("keywords", [])
        
        for exp in resume_experience:
            relevance_score = 0
            alignment_reasons = []
            
            # Check title alignment
            title = exp.get("title", "").lower()
            jd_title = parsed_jd.get("job_title", "").lower()
            
            if any(keyword in title for keyword in jd_title.split()):
                relevance_score += 0.3
                alignment_reasons.append("Title matches job requirements")
            
            # Check technology alignment
            technologies = exp.get("technologies", [])
            jd_tech = [kw.lower() for kw in jd_keywords if kw.lower() in ["python", "java", "javascript", "react", "docker", "aws", "sql"]]
            
            matching_tech = [tech for tech in technologies if tech.lower() in jd_tech]
            if matching_tech:
                relevance_score += 0.4 * (len(matching_tech) / len(jd_tech))
                alignment_reasons.append(f"Experience with {', '.join(matching_tech)}")
            
            # Check description alignment
            description = exp.get("description", "").lower()
            matching_keywords = [kw for kw in jd_keywords if kw.lower() in description]
            if matching_keywords:
                relevance_score += 0.3 * (len(matching_keywords) / len(jd_keywords))
                alignment_reasons.append(f"Relevant experience with {', '.join(matching_keywords[:3])}")
            
            if relevance_score > 0.3:
                relevant_highlights.append({
                    "experience": f"{exp.get('title', '')} at {exp.get('company', '')}",
                    "relevance_score": round(relevance_score, 2),
                    "alignment_reason": "; ".join(alignment_reasons)
                })
        
        # Sort by relevance score
        relevant_highlights.sort(key=lambda x: x["relevance_score"], reverse=True)
        return relevant_highlights[:5]  # Top 5 highlights
    
    def _identify_experience_gaps(self, resume_experience: List[Dict[str, Any]], jd_requirements: List[str]) -> List[Dict[str, Any]]:
        """Identify experience gaps."""
        gaps = []
        
        # Common gap patterns
        gap_patterns = {
            "leadership": ["lead", "manage", "supervise", "mentor"],
            "cloud": ["cloud", "aws", "azure", "gcp"],
            "enterprise": ["enterprise", "large scale", "production"],
            "certifications": ["certified", "certification"],
            "industry": ["industry", "domain", "sector"]
        }
        
        resume_text = " ".join([
            exp.get("description", "") + " " + " ".join(exp.get("technologies", []))
            for exp in resume_experience
        ]).lower()
        
        for gap_type, keywords in gap_patterns.items():
            if not any(keyword in resume_text for keyword in keywords):
                # Check if JD requires this
                jd_text = " ".join(jd_requirements).lower()
                if any(keyword in jd_text for keyword in keywords):
                    gaps.append({
                        "gap": f"No experience with {gap_type.replace('_', ' ')}",
                        "impact": "medium" if gap_type in ["cloud", "certifications"] else "low",
                        "suggestion": self._get_gap_suggestion(gap_type)
                    })
        
        return gaps[:5]  # Top 5 gaps
    
    def _get_gap_suggestion(self, gap_type: str) -> str:
        """Get suggestion for experience gap."""
        suggestions = {
            "leadership": "Highlight any leadership or mentoring experience, even from volunteer work",
            "cloud": "Consider obtaining cloud certifications or highlight any cloud-related projects",
            "enterprise": "Emphasize any large-scale projects or high-traffic applications",
            "certifications": "Consider obtaining relevant certifications to strengthen your profile",
            "industry": "Research the industry and highlight any transferable experience"
        }
        return suggestions.get(gap_type, "Gain experience in this area through projects or certifications")
    
    def _analyze_role_alignment(self, parsed_resume: Dict[str, Any], parsed_jd: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze overall role alignment."""
        skills_analysis = self._analyze_skills(parsed_resume, parsed_jd)
        experience_analysis = self._analyze_experience(parsed_resume, parsed_jd)
        
        # Calculate alignment score
        alignment_score = self._calculate_role_alignment_score(skills_analysis, experience_analysis)
        
        # Determine overall alignment
        if alignment_score >= 80:
            overall_alignment = "strong"
        elif alignment_score >= 60:
            overall_alignment = "moderate"
        else:
            overall_alignment = "weak"
        
        # Identify strengths
        strengths = self._identify_strengths(skills_analysis, experience_analysis)
        
        # Identify concerns
        concerns = self._identify_concerns(skills_analysis, experience_analysis)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(concerns, parsed_jd)
        
        return {
            "overall_alignment": overall_alignment,
            "alignment_score": alignment_score,
            "strengths": strengths,
            "concerns": concerns,
            "recommendations": recommendations
        }
    
    def _calculate_role_alignment_score(self, skills_analysis: Dict[str, Any], experience_analysis: Dict[str, Any]) -> float:
        """Calculate role alignment score."""
        score = 0.0
        
        # Skills matching (40% weight)
        total_required = len(skills_analysis["matched_skills"]) + len(skills_analysis["missing_skills"])
        if total_required > 0:
            skills_match_rate = len(skills_analysis["matched_skills"]) / total_required
            score += skills_match_rate * 40
        
        # Experience alignment (30% weight)
        if experience_analysis["level_alignment"] == "aligned":
            score += 30
        elif experience_analysis["level_alignment"] == "close":
            score += 20
        elif experience_analysis["level_alignment"] == "misaligned":
            score += 5
        
        # Relevant experience (20% weight)
        if experience_analysis["relevant_experience_highlights"]:
            avg_relevance = sum(h["relevance_score"] for h in experience_analysis["relevant_experience_highlights"]) / len(experience_analysis["relevant_experience_highlights"])
            score += avg_relevance * 20
        
        # Experience gaps (10% weight, negative)
        gap_count = len(experience_analysis["experience_gaps"])
        if gap_count == 0:
            score += 10
        elif gap_count <= 2:
            score += 5
        else:
            score += 0
        
        return min(100.0, score)
    
    def _identify_strengths(self, skills_analysis: Dict[str, Any], experience_analysis: Dict[str, Any]) -> List[str]:
        """Identify candidate strengths."""
        strengths = []
        
        # Skills strengths
        if len(skills_analysis["matched_skills"]) >= len(skills_analysis["missing_skills"]):
            strengths.append("Strong technical background with required skills")
        
        strong_matches = [s for s in skills_analysis["matched_skills"] if s["match_strength"] == "strong"]
        if len(strong_matches) >= 3:
            strengths.append("Multiple strong skill matches")
        
        # Experience strengths
        if experience_analysis["level_alignment"] == "aligned":
            strengths.append("Experience level matches role requirements")
        
        if experience_analysis["years_experience_match"] == "sufficient":
            strengths.append("Sufficient years of experience")
        
        if len(experience_analysis["relevant_experience_highlights"]) >= 2:
            strengths.append("Relevant experience in similar roles")
        
        return strengths[:5]  # Top 5 strengths
    
    def _identify_concerns(self, skills_analysis: Dict[str, Any], experience_analysis: Dict[str, Any]) -> List[str]:
        """Identify concerns."""
        concerns = []
        
        # Skills concerns
        if len(skills_analysis["missing_skills"]) > len(skills_analysis["matched_skills"]):
            concerns.append("Missing several required skills")
        
        required_missing = [s for s in skills_analysis["missing_skills"] if s["jd_requirement"] == "required"]
        if len(required_missing) >= 2:
            concerns.append("Missing multiple required skills")
        
        # Experience concerns
        if experience_analysis["level_alignment"] == "misaligned":
            concerns.append("Experience level doesn't match requirements")
        
        if experience_analysis["years_experience_match"] == "insufficient":
            concerns.append("Insufficient years of experience")
        
        high_impact_gaps = [g for g in experience_analysis["experience_gaps"] if g["impact"] == "high"]
        if len(high_impact_gaps) >= 1:
            concerns.append("Significant experience gaps identified")
        
        return concerns[:5]  # Top 5 concerns
    
    def _generate_recommendations(self, concerns: List[str], parsed_jd: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on concerns."""
        recommendations = []
        
        for concern in concerns:
            if "skills" in concern.lower():
                recommendations.append("Highlight relevant projects and consider skill development in missing areas")
            elif "experience" in concern.lower():
                recommendations.append("Emphasize transferable experience and consider additional projects")
            elif "cloud" in concern.lower():
                recommendations.append("Gain cloud experience through certifications or personal projects")
            elif "leadership" in concern.lower():
                recommendations.append("Highlight any leadership or mentoring experience")
            elif "certifications" in concern.lower():
                recommendations.append("Consider obtaining relevant certifications")
        
        # Add general recommendations if needed
        if len(recommendations) < 2:
            recommendations.extend([
                "Tailor resume to highlight most relevant experience",
                "Consider a cover letter to address gaps"
            ])
        
        return recommendations[:5]  # Top 5 recommendations
    
    def _analyze_education(self, parsed_resume: Dict[str, Any], parsed_jd: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze education alignment."""
        resume_education = parsed_resume.get("education", [])
        jd_qualifications = parsed_jd.get("parsed_content", {}).get("qualifications", [])
        
        education_match = "meets_requirements"
        degree_alignment = "aligned"
        field_relevance = "medium"
        additional_education_needed = []
        
        # Check degree requirements
        degree_requirements = [qual for qual in jd_qualifications if "degree" in qual.lower()]
        if degree_requirements:
            has_required_degree = False
            for edu in resume_education:
                degree = edu.get("degree", "").lower()
                if any(req in degree for req in ["bachelor", "master", "phd"]):
                    has_required_degree = True
                    break
            
            if not has_required_degree:
                education_match = "below_requirements"
                additional_education_needed.append("Obtain required degree")
        
        # Check field relevance
        resume_fields = [edu.get("field", "").lower() for edu in resume_education]
        jd_keywords = parsed_jd.get("parsed_content", {}).get("keywords", [])
        
        if any(field in " ".join(jd_keywords).lower() for field in resume_fields):
            field_relevance = "high"
        elif resume_fields:
            field_relevance = "medium"
        else:
            field_relevance = "low"
        
        return {
            "education_match": education_match,
            "degree_alignment": degree_alignment,
            "field_relevance": field_relevance,
            "additional_education_needed": additional_education_needed
        }
    
    def _calculate_fit_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall fit score."""
        # Use role alignment score as the primary fit score
        return analysis["role_alignment"]["alignment_score"]
    
    def _calculate_analysis_metadata(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate analysis metadata."""
        skills_analysis = analysis["skills_analysis"]
        
        return {
            "analysis_date": datetime.utcnow().isoformat(),
            "total_skills_analyzed": len(skills_analysis["matched_skills"]) + len(skills_analysis["missing_skills"]) + len(skills_analysis["partial_matches"]),
            "matched_skills_count": len(skills_analysis["matched_skills"]),
            "missing_skills_count": len(skills_analysis["missing_skills"]),
            "partial_matches_count": len(skills_analysis["partial_matches"]),
            "confidence_score": self._calculate_confidence_score(analysis)
        }
    
    def _calculate_confidence_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for the analysis."""
        confidence_factors = []
        
        # Skills analysis confidence
        total_skills = analysis["metadata"]["total_skills_analyzed"]
        if total_skills > 0:
            match_rate = analysis["metadata"]["matched_skills_count"] / total_skills
            confidence_factors.append(match_rate)
        
        # Experience analysis confidence
        if analysis["experience_analysis"]["level_alignment"] != "unknown":
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.4)
        
        # Role alignment confidence
        alignment_score = analysis["role_alignment"]["alignment_score"]
        if alignment_score > 0:
            confidence_factors.append(alignment_score / 100)
        
        return min(1.0, sum(confidence_factors) / len(confidence_factors)) if confidence_factors else 0.5
