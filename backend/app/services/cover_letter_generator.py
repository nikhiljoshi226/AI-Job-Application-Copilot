from typing import Dict, List, Any, Optional, Tuple
import re
import time
from datetime import datetime

from app.services.truth_bank import TruthBank


class CoverLetterGenerator:
    """
    Service to generate truthful, professional cover letters based on 
    tailored resume data and job description information.
    """

    def __init__(self):
        self.truth_bank_service = TruthBank()
        
        # Cover letter structure templates
        self.structure_templates = {
            "professional": {
                "salutation": "Dear {hiring_manager},",
                "intro": "I am writing to express my strong interest in the {position} position at {company}.",
                "body": "With my {years_experience} years of experience in {key_area}, I believe my skills align perfectly with your requirements.",
                "skills_match": "My expertise in {top_skills} makes me well-equipped to contribute to your team.",
                "closing": "I would welcome the opportunity to discuss how my background aligns with your needs.",
                "sign_off": "Sincerely,",
                "signature": "{name}"
            },
            "modern": {
                "salutation": "Dear {hiring_manager},",
                "intro": "I'm excited to apply for the {position} role at {company} where I can bring my {years_experience} years of {key_area} expertise.",
                "body": "Your focus on {company_focus} resonates with my professional experience and career goals.",
                "skills_match": "I've developed strong capabilities in {top_skills} that directly address the key requirements of this role.",
                "closing": "I'm eager to explore how my background can help {company} achieve its objectives.",
                "sign_off": "Best regards,",
                "signature": "{name}"
            },
            "technical": {
                "salutation": "Dear {hiring_manager},",
                "intro": "I am writing to apply for the {position} position at {company}, bringing {years_experience} years of technical expertise.",
                "body": "My background in {key_area} and experience with {top_skills} aligns well with your technical requirements.",
                "skills_match": "I have hands-on experience with {technologies} and a proven track record of delivering {achievements}.",
                "closing": "I would appreciate the opportunity to discuss how my technical skills can benefit your team.",
                "sign_off": "Best regards,",
                "signature": "{name}"
            }
        }

    def generate_cover_letter(
        self,
        tailored_resume_data: Dict[str, Any],
        job_description_data: Dict[str, Any],
        generation_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a truthful, professional cover letter.
        
        Args:
            tailored_resume_data: Tailored resume data with rendering content
            job_description_data: Parsed job description data
            generation_options: Options for generation (tone, focus, etc.)
            
        Returns:
            Generated cover letter with metadata and validation results
        """
        start_time = time.time()
        
        # Set default generation options
        options = {
            "tone": "professional",
            "focus": "skills_match",
            "length": "standard",
            "personalization_level": "medium"
        }
        if generation_options:
            options.update(generation_options)
        
        # Extract relevant data
        resume_content = tailored_resume_data.get("rendering_data", {})
        jd_content = job_description_data.get("parsed_content", {})
        
        # Create truth bank for validation
        truth_bank = self._create_truth_bank_from_resume(resume_content)
        
        # Generate cover letter content
        cover_letter_content = self._generate_letter_content(
            resume_content,
            jd_content,
            options,
            truth_bank
        )
        
        # Validate and score the content
        validation_result = self._validate_cover_letter(cover_letter_content, truth_bank)
        
        # Calculate scores
        truthfulness_score = self._calculate_truthfulness_score(cover_letter_content, truth_bank)
        grammar_score = self._calculate_grammar_score(cover_letter_content)
        personalization_score = self._calculate_personalization_score(
            cover_letter_content, resume_content, jd_content
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Build result
        result = {
            "cover_letter": cover_letter_content,
            "metadata": {
                "truthfulness_score": truthfulness_score,
                "grammar_score": grammar_score,
                "personalization_score": personalization_score,
                "processing_time_ms": processing_time,
                "generation_options": options,
                "generated_at": datetime.utcnow().isoformat(),
                "word_count": len(cover_letter_content.get("full_text", "").split())
            },
            "validation": validation_result,
            "sources": self._identify_content_sources(cover_letter_content, truth_bank)
        }
        
        return result

    def _create_truth_bank_from_resume(self, resume_content: Dict[str, Any]) -> Dict[str, Any]:
        """Create a truth bank from resume content for validation."""
        truth_bank = {
            "personal_info": {
                "name": resume_content.get("header", {}).get("name", ""),
                "contact": resume_content.get("header", {}).get("contact", {})
            },
            "experience": {
                "total_years": 0,
                "companies": [],
                "titles": [],
                "achievements": [],
                "technologies": []
            },
            "skills": {
                "technical": [],
                "soft_skills": []
            },
            "education": {
                "degrees": [],
                "universities": []
            },
            "projects": {
                "names": [],
                "technologies": [],
                "descriptions": []
            }
        }
        
        # Extract experience information
        experience_entries = resume_content.get("experience", {}).get("entries", [])
        for entry in experience_entries:
            if entry.get("company"):
                truth_bank["experience"]["companies"].append(entry["company"])
            if entry.get("title"):
                truth_bank["experience"]["titles"].append(entry["title"])
            if entry.get("achievements"):
                truth_bank["experience"]["achievements"].extend(entry["achievements"])
            if entry.get("technologies"):
                truth_bank["experience"]["technologies"].extend(entry["technologies"])
        
        # Extract skills
        skills_categories = resume_content.get("skills", {}).get("categories", [])
        for category in skills_categories:
            category_name = category.get("name", "").lower()
            skills = category.get("skills", [])
            
            if "technical" in category_name:
                truth_bank["skills"]["technical"].extend([s.get("name", "") for s in skills])
            elif "soft" in category_name:
                truth_bank["skills"]["soft_skills"].extend([s.get("name", "") for s in skills])
        
        # Extract education
        education_entries = resume_content.get("education", {}).get("entries", [])
        for entry in education_entries:
            if entry.get("degree"):
                truth_bank["education"]["degrees"].append(entry["degree"])
            if entry.get("university"):
                truth_bank["education"]["universities"].append(entry["university"])
        
        # Extract projects
        project_entries = resume_content.get("projects", {}).get("entries", [])
        for entry in project_entries:
            if entry.get("name"):
                truth_bank["projects"]["names"].append(entry["name"])
            if entry.get("technologies"):
                truth_bank["projects"]["technologies"].extend(entry["technologies"])
            if entry.get("description"):
                truth_bank["projects"]["descriptions"].append(entry["description"])
        
        return truth_bank

    def _generate_letter_content(
        self,
        resume_content: Dict[str, Any],
        jd_content: Dict[str, Any],
        options: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate the actual cover letter content."""
        
        # Get template
        template = self.structure_templates.get(options["tone"], self.structure_templates["professional"])
        
        # Extract key information
        name = resume_content.get("header", {}).get("name", "")
        summary = resume_content.get("summary", {}).get("content", "")
        
        # Extract job information
        job_title = jd_content.get("job_title", "")
        company = jd_content.get("company", "")
        hiring_manager = self._extract_hiring_manager(jd_content)
        
        # Extract experience info
        experience_years = self._calculate_experience_years(resume_content)
        key_skills = self._extract_key_skills(resume_content)
        top_skills = key_skills[:3]  # Top 3 skills
        
        # Extract company focus from JD
        company_focus = self._extract_company_focus(jd_content)
        
        # Build cover letter sections
        sections = {}
        
        # Salutation
        sections["salutation"] = template["salutation"].format(
            hiring_manager=hiring_manager or "Hiring Manager"
        )
        
        # Introduction
        sections["introduction"] = template["intro"].format(
            position=job_title,
            company=company
        )
        
        # Body paragraphs
        body_paragraphs = []
        
        # First body paragraph - experience and alignment
        key_area = self._determine_key_area(resume_content, jd_content)
        body_paragraphs.append(template["body"].format(
            years_experience=experience_years,
            key_area=key_area
        ))
        
        # Second body paragraph - skills match
        skills_text = ", ".join(top_skills)
        body_paragraphs.append(template["skills_match"].format(
            top_skills=skills_text
        ))
        
        # Additional paragraph for technical template
        if options["tone"] == "technical":
            technologies = self._extract_technologies(resume_content)
            achievements = self._extract_key_achievements(resume_content)
            
            tech_paragraph = template["skills_match"].format(
                technologies=", ".join(technologies[:5]),
                achievements=achievements[0] if achievements else "technical solutions"
            )
            body_paragraphs.append(tech_paragraph)
        
        # Modern template - company focus paragraph
        if options["tone"] == "modern" and company_focus:
            body_paragraphs.append(template["body"].format(
                years_experience=experience_years,
                key_area=company_focus
            ))
        
        sections["body_paragraphs"] = body_paragraphs
        
        # Closing
        sections["closing"] = template["closing"]
        
        # Sign off
        sections["sign_off"] = template["sign_off"]
        sections["signature"] = template["signature"].format(name=name)
        
        # Combine into full text
        full_text = self._combine_sections(sections)
        
        return {
            "sections": sections,
            "full_text": full_text,
            "metadata": {
                "word_count": len(full_text.split()),
                "paragraph_count": len(body_paragraphs) + 2,  # intro + closing
                "tone": options["tone"],
                "focus": options["focus"]
            }
        }

    def _extract_hiring_manager(self, jd_content: Dict[str, Any]) -> Optional[str]:
        """Extract hiring manager name from job description."""
        # Look for common patterns in job description
        text = jd_content.get("raw_text", "")
        
        patterns = [
            r"(?:Hiring Manager|Recruiter|Talent Acquisition)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"Contact\s+([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"reach out to\s+([A-Z][a-z]+\s+[A-Z][a-z]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None

    def _calculate_experience_years(self, resume_content: Dict[str, Any]) -> str:
        """Calculate years of experience from resume."""
        # Try to extract from metadata or calculate from experience entries
        experience_entries = resume_content.get("experience", {}).get("entries", [])
        
        if experience_entries:
            # Simple calculation - count unique years mentioned
            years_mentioned = set()
            for entry in experience_entries:
                dates = entry.get("dates", "")
                if dates:
                    # Extract years from date strings
                    year_matches = re.findall(r'\b(20\d{2})\b', dates)
                    years_mentioned.update(year_matches)
            
            if years_mentioned:
                years_span = max(years_mentioned) - min(years_mentioned) + 1
                return f"{years_span}"
        
        return "several"

    def _extract_key_skills(self, resume_content: Dict[str, Any]) -> List[str]:
        """Extract key skills from resume."""
        skills = []
        
        # From skills section
        skills_categories = resume_content.get("skills", {}).get("categories", [])
        for category in skills_categories:
            category_skills = category.get("skills", [])
            for skill in category_skills:
                skill_name = skill.get("name", "")
                if skill_name and skill_name not in skills:
                    skills.append(skill_name)
        
        # From experience technologies
        experience_entries = resume_content.get("experience", {}).get("entries", [])
        for entry in experience_entries:
            technologies = entry.get("technologies", [])
            for tech in technologies:
                if tech and tech not in skills:
                    skills.append(tech)
        
        return skills[:10]  # Return top 10 skills

    def _determine_key_area(self, resume_content: Dict[str, Any], jd_content: Dict[str, Any]) -> str:
        """Determine the key area of expertise."""
        # Get most mentioned skills/technologies
        all_skills = self._extract_key_skills(resume_content)
        
        # Get JD requirements
        jd_skills = []
        required_skills = jd_content.get("parsed_content", {}).get("required_skills", [])
        for skill in required_skills:
            jd_skills.append(skill.get("skill", ""))
        
        # Find overlap
        overlap = [skill for skill in all_skills if skill.lower() in [s.lower() for s in jd_skills]]
        
        if overlap:
            return overlap[0]
        
        # Fallback to most common skill
        if all_skills:
            return all_skills[0]
        
        return "software development"

    def _extract_company_focus(self, jd_content: Dict[str, Any]) -> str:
        """Extract company focus from job description."""
        # Look for keywords that indicate company focus
        text = jd_content.get("raw_text", "").lower()
        
        focus_keywords = {
            "fintech": ["financial", "banking", "finance", "payments"],
            "healthcare": ["health", "medical", "healthcare", "patient"],
            "ecommerce": ["e-commerce", "retail", "shopping", "online"],
            "education": ["education", "learning", "students", "academic"],
            "gaming": ["gaming", "games", "entertainment", "players"],
            "automotive": ["automotive", "cars", "vehicles", "driving"]
        }
        
        for focus, keywords in focus_keywords.items():
            if any(keyword in text for keyword in keywords):
                return focus
        
        return "technology"

    def _extract_technologies(self, resume_content: Dict[str, Any]) -> List[str]:
        """Extract technologies from resume."""
        technologies = []
        
        # From experience entries
        experience_entries = resume_content.get("experience", {}).get("entries", [])
        for entry in experience_entries:
            techs = entry.get("technologies", [])
            technologies.extend(techs)
        
        # From projects
        project_entries = resume_content.get("projects", {}).get("entries", [])
        for entry in project_entries:
            techs = entry.get("technologies", [])
            technologies.extend(techs)
        
        # Remove duplicates and return
        return list(set(technologies))

    def _extract_key_achievements(self, resume_content: Dict[str, Any]) -> List[str]:
        """Extract key achievements from resume."""
        achievements = []
        
        # From experience entries
        experience_entries = resume_content.get("experience", {}).get("entries", [])
        for entry in experience_entries:
            entry_achievements = entry.get("achievements", [])
            achievements.extend(entry_achievements)
        
        return achievements[:5]  # Return top 5 achievements

    def _combine_sections(self, sections: Dict[str, Any]) -> str:
        """Combine sections into full cover letter text."""
        parts = []
        
        # Salutation
        parts.append(sections.get("salutation", ""))
        parts.append("")  # Empty line after salutation
        
        # Introduction
        parts.append(sections.get("introduction", ""))
        parts.append("")  # Empty line after introduction
        
        # Body paragraphs
        body_paragraphs = sections.get("body_paragraphs", [])
        for paragraph in body_paragraphs:
            parts.append(paragraph)
            parts.append("")  # Empty line after each paragraph
        
        # Closing
        parts.append(sections.get("closing", ""))
        parts.append("")  # Empty line after closing
        
        # Sign off
        parts.append(sections.get("sign_off", ""))
        parts.append("")  # Empty line after sign off
        parts.append(sections.get("signature", ""))
        
        return "\n".join(parts)

    def _validate_cover_letter(
        self,
        cover_letter_content: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate the cover letter for truthfulness and quality."""
        validation_result = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "guardrail_violations": []
        }
        
        full_text = cover_letter_content.get("full_text", "")
        
        # Check for fabrication indicators
        fabrication_violations = self._check_fabrication_indicators(full_text, truth_bank)
        if fabrication_violations:
            validation_result["guardrail_violations"].extend(fabrication_violations)
            validation_result["is_valid"] = False
        
        # Check for excessive claims
        excessive_claims = self._check_excessive_claims(full_text, truth_bank)
        if excessive_claims:
            validation_result["warnings"].extend(excessive_claims)
        
        # Check length
        word_count = len(full_text.split())
        if word_count < 150:
            validation_result["warnings"].append("Cover letter is quite short (under 150 words)")
        elif word_count > 400:
            validation_result["warnings"].append("Cover letter is quite long (over 400 words)")
        
        # Check for basic structure
        if not sections.get("salutation"):
            validation_result["errors"].append("Missing salutation")
        
        if not sections.get("introduction"):
            validation_result["errors"].append("Missing introduction")
        
        if not sections.get("closing"):
            validation_result["errors"].append("Missing closing")
        
        if validation_result["errors"]:
            validation_result["is_valid"] = False
        
        return validation_result

    def _check_fabrication_indicators(
        self,
        text: str,
        truth_bank: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check for potential fabrication indicators."""
        violations = []
        
        fabrication_indicators = [
            "world-class",
            "expert in",
            "master of",
            "pioneered",
            "revolutionized",
            "industry-leading",
            "best in the world",
            "unmatched",
            "unparalleled"
        ]
        
        text_lower = text.lower()
        
        for indicator in fabrication_indicators:
            if indicator in text_lower:
                violations.append({
                    "type": "fabrication_indicator",
                    "indicator": indicator,
                    "context": "Potentially exaggerated claim detected",
                    "severity": "medium"
                })
        
        return violations

    def _check_excessive_claims(
        self,
        text: str,
        truth_bank: Dict[str, Any]
    ) -> List[str]:
        """Check for excessive claims."""
        warnings = []
        
        # Count quantifiable claims
        percentage_claims = len(re.findall(r'\d+%', text))
        metric_claims = len(re.findall(r'\d+\s+(?:users|customers|clients|employees|projects)', text))
        
        if percentage_claims > 3:
            warnings.append(f"Multiple percentage claims ({percentage_claims}) may seem exaggerated")
        
        if metric_claims > 2:
            warnings.append(f"Multiple metric claims ({metric_claims}) may seem exaggerated")
        
        return warnings

    def _calculate_truthfulness_score(
        self,
        cover_letter_content: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> float:
        """Calculate truthfulness score for the cover letter."""
        base_score = 0.8  # Start with high score for cover letters
        
        full_text = cover_letter_content.get("full_text", "")
        
        # Deductions for fabrication indicators
        fabrication_indicators = [
            "world-class", "expert in", "master of", "pioneered",
            "revolutionized", "industry-leading", "unmatched"
        ]
        
        text_lower = full_text.lower()
        indicator_count = sum(1 for indicator in fabrication_indicators if indicator in text_lower)
        
        if indicator_count > 0:
            base_score -= min(0.3, indicator_count * 0.1)
        
        # Deductions for excessive claims
        percentage_claims = len(re.findall(r'\d+%', text_lower))
        metric_claims = len(re.findall(r'\d+\s+(?:users|customers|clients)', text_lower))
        
        if percentage_claims > 3:
            base_score -= 0.1
        if metric_claims > 2:
            base_score -= 0.1
        
        # Bonus for personalization
        if truth_bank.get("personal_info", {}).get("name"):
            if truth_bank["personal_info"]["name"].lower() in text_lower:
                base_score += 0.1
        
        return max(0.0, min(1.0, base_score))

    def _calculate_grammar_score(self, cover_letter_content: Dict[str, Any]) -> float:
        """Calculate grammar score (basic implementation)."""
        # This is a simplified grammar check
        # In production, you'd use a proper grammar checking service
        full_text = cover_letter_content.get("full_text", "")
        
        base_score = 0.9  # Start with high score
        
        # Basic checks
        if not full_text.strip():
            return 0.0
        
        # Check for proper sentence structure
        sentences = re.split(r'[.!?]+', full_text)
        proper_sentences = [s for s in sentences if s.strip()]
        
        if len(proper_sentences) < 3:
            base_score -= 0.2
        
        # Check for common grammar issues
        if re.search(r'\bi\s+', full_text):  # Capital 'I' in middle of sentence
            base_score -= 0.1
        
        if full_text.count('  ') > 5:  # Multiple spaces
            base_score -= 0.1
        
        return max(0.0, min(1.0, base_score))

    def _calculate_personalization_score(
        self,
        cover_letter_content: Dict[str, Any],
        resume_content: Dict[str, Any],
        jd_content: Dict[str, Any]
    ) -> float:
        """Calculate how well personalized the cover letter is."""
        full_text = cover_letter_content.get("full_text", "").lower()
        
        base_score = 0.5  # Start with neutral score
        
        # Check for company name
        company = jd_content.get("company", "").lower()
        if company and company in full_text:
            base_score += 0.2
        
        # Check for job title
        job_title = jd_content.get("job_title", "").lower()
        if job_title and job_title in full_text:
            base_score += 0.1
        
        # Check for skills from JD
        jd_skills = []
        required_skills = jd_content.get("parsed_content", {}).get("required_skills", [])
        for skill in required_skills:
            jd_skills.append(skill.get("skill", "").lower())
        
        resume_skills = self._extract_key_skills(resume_content)
        matched_skills = [skill for skill in resume_skills if skill.lower() in jd_skills]
        
        if matched_skills:
            base_score += min(0.2, len(matched_skills) * 0.05)
        
        return max(0.0, min(1.0, base_score))

    def _identify_content_sources(
        self,
        cover_letter_content: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify sources of content in the cover letter."""
        sources = []
        
        full_text = cover_letter_content.get("full_text", "")
        
        # Check for resume content
        if truth_bank.get("personal_info", {}).get("name"):
            name = truth_bank["personal_info"]["name"]
            if name.lower() in full_text.lower():
                sources.append({
                    "type": "resume_personal_info",
                    "content": name,
                    "confidence": "high"
                })
        
        # Check for skills from resume
        resume_skills = truth_bank.get("skills", {}).get("technical", []) + truth_bank.get("skills", {}).get("soft_skills", [])
        for skill in resume_skills:
            if skill.lower() in full_text.lower():
                sources.append({
                    "type": "resume_skill",
                    "content": skill,
                    "confidence": "high"
                })
        
        # Check for experience content
        companies = truth_bank.get("experience", {}).get("companies", [])
        for company in companies:
            if company.lower() in full_text.lower():
                sources.append({
                    "type": "resume_experience",
                    "content": company,
                    "confidence": "high"
                })
        
        return sources
