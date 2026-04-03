from typing import Dict, List, Any, Optional, Tuple
import re
import time
from datetime import datetime

from app.services.truth_bank import TruthBank


class OutreachDraftGenerator:
    """
    Service to generate recruiter outreach drafts (email, LinkedIn, formal messages)
    based on approved user background information.
    """

    def __init__(self):
        self.truth_bank_service = TruthBank()
        
        # Outreach type templates
        self.templates = {
            "email_intro": {
                "subject": "Software Engineer Opportunity - {job_title} at {company}",
                "body": "Dear {recruiter_name},\n\nI am writing to express my strong interest in the {job_title} position at {company}.",
                "call_to_action": "I would appreciate the opportunity to discuss how my background aligns with your needs.",
                "closing": "Best regards,\n{name}"
            },
            "linkedin_note": {
                "message": "Hi {recruiter_name}, I came across your post about the {job_title} role at {company} and wanted to connect.",
                "call_to_action": "I would love to learn more about this opportunity.",
                "closing": "Looking forward to connecting!"
            },
            "formal_message": {
                "salutation": "Dear {recruiter_name},",
                "body": "I am writing to formally express my interest in the {job_title} position at {company}.",
                "experience_summary": "With my background in {key_area}, I believe I can contribute effectively to your team.",
                "skills_alignment": "My experience with {top_skills} aligns well with your requirements.",
                "closing": "I would welcome the opportunity to discuss this further.",
                "sign_off": "Sincerely,\n{name}"
            }
        }

    def generate_outreach_draft(
        self,
        resume_data: Dict[str, Any],
        job_description_data: Dict[str, Any],
        outreach_type: str = "email_intro",
        generation_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a recruiter outreach draft.
        
        Args:
            resume_data: Parsed resume data
            job_description_data: Parsed job description data
            outreach_type: Type of outreach (email_intro, linkedin_note, formal_message)
            generation_options: Options for generation
            
        Returns:
            Generated outreach draft with metadata and validation results
        """
        start_time = time.time()
        
        # Set default generation options
        options = {
            "tone": "professional",
            "length": "standard",
            "personalization_level": "medium"
        }
        if generation_options:
            options.update(generation_options)
        
        # Create truth bank for validation
        truth_bank = self._create_truth_bank_from_resume(resume_data)
        
        # Generate draft content
        draft_content = self._generate_draft_content(
            resume_data,
            job_description_data,
            outreach_type,
            options,
            truth_bank
        )
        
        # Validate draft
        validation_result = self._validate_outreach_draft(draft_content, truth_bank)
        
        # Calculate scores
        truthfulness_score = self._calculate_truthfulness_score(draft_content, truth_bank)
        conciseness_score = self._calculate_conciseness_score(draft_content)
        professionalism_score = self._calculate_professionalism_score(draft_content)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Build result
        result = {
            "draft": draft_content,
            "metadata": {
                "outreach_type": outreach_type,
                "truthfulness_score": truthfulness_score,
                "conciseness_score": conciseness_score,
                "professionalism_score": professionalism_score,
                "processing_time_ms": processing_time,
                "generation_options": options,
                "generated_at": datetime.utcnow().isoformat(),
                "word_count": len(draft_content.get("full_text", "").split())
            },
            "validation": validation_result,
            "sources": self._identify_content_sources(draft_content, truth_bank)
        }
        
        return result

    def _create_truth_bank_from_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a truth bank from resume data for validation."""
        truth_bank = {
            "personal_info": {
                "name": resume_data.get("header", {}).get("name", ""),
                "contact": resume_data.get("header", {}).get("contact", {}),
                "location": resume_data.get("header", {}).get("contact", {}).get("location", ""),
                "email": resume_data.get("header", {}).get("contact", {}).get("email", "")
            },
            "experience": {
                "total_years": 0,
                "companies": [],
                "titles": [],
                "skills": [],
                "achievements": []
            },
            "skills": {
                "technical": [],
                "soft_skills": [],
                "certifications": []
            },
            "education": {
                "degrees": [],
                "universities": []
            },
            "projects": {
                "names": [],
                "technologies": []
            }
        }
        
        # Extract experience information
        experience_entries = resume_data.get("experience", {}).get("entries", [])
        for entry in experience_entries:
            if entry.get("company"):
                truth_bank["experience"]["companies"].append(entry["company"])
            if entry.get("title"):
                truth_bank["experience"]["titles"].append(entry["title"])
            if entry.get("technologies"):
                truth_bank["experience"]["skills"].extend(entry["technologies"])
            if entry.get("achievements"):
                truth_bank["experience"]["achievements"].extend(entry["achievements"])
        
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
        
        # Extract projects
        project_entries = resume_data.get("projects", {}).get("entries", [])
        for entry in project_entries:
            if entry.get("name"):
                truth_bank["projects"]["names"].append(entry["name"])
            if entry.get("technologies"):
                truth_bank["projects"]["technologies"].extend(entry["technologies"])
        
        return truth_bank

    def _generate_draft_content(
        self,
        resume_data: Dict[str, Any],
        job_description_data: Dict[str, Any],
        outreach_type: str,
        options: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate the actual outreach draft content."""
        
        # Get template
        template = self.templates.get(outreach_type, self.templates["email_intro"])
        
        # Extract key information
        name = resume_data.get("header", {}).get("name", "")
        summary = resume_data.get("summary", {}).get("content", "")
        
        # Extract job information
        job_title = job_description_data.get("job_title", "")
        company = job_description.get("company", "")
        
        # Extract recruiter information
        recruiter_name = self._extract_recruiter_name(job_description_data)
        
        # Extract experience info
        experience_years = self._calculate_experience_years(resume_data)
        key_skills = self._extract_key_skills(resume_data)
        top_skills = key_skills[:2]  # Top 2 skills for brevity
        
        # Extract company focus
        company_focus = self._extract_company_focus(job_description_data)
        
        # Build draft sections
        sections = {}
        
        # Salutation
        if recruiter_name:
            sections["salutation"] = template["salutation"].format(
                recruiter_name=recruiter_name
            )
        else:
            sections["salutation"] = "Dear Hiring Manager,"
        
        # Introduction
        sections["introduction"] = template["body"].format(
            job_title=job_title,
            company=company
        )
        
        # Body paragraphs
        body_paragraphs = []
        
        # First paragraph - experience and alignment
        key_area = self._determine_key_area(resume_data, job_description_data)
        body_paragraphs.append(template["body"].format(
            years_experience=experience_years,
            key_area=key_area
        ))
        
        # Second paragraph - skills match
        skills_text = " and ".join(top_skills)
        body_paragraphs.append(template["skills_match"].format(
            top_skills=skills_text
        ))
        
        # Additional paragraph for modern tone
        if options["tone"] == "modern" and company_focus:
            body_paragraphs.append(template["body"].format(
                years_experience=experience_years,
                key_area=company_focus
            ))
        
        # Technical template - specific focus
        if options["tone"] == "technical":
            technologies = self._extract_technologies(resume_data)
            achievements = self._extract_key_achievements(resume_data)
            
            if technologies and achievements:
                tech_paragraph = template["skills_match"].format(
                    technologies=", ".join(technologies[:3]),
                    achievements=achievements[0] if achievements else "technical solutions"
                )
                body_paragraphs.append(tech_paragraph)
        
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
                "length": options["length"],
                "personalization_level": options["personalization_level"]
            }
        }

    def _extract_recruiter_name(self, job_description_data: Dict[str, Any]) -> str:
        """Extract recruiter name from job description."""
        text = job_description_data.get("raw_text", "")
        
        # Look for common recruiter patterns
        patterns = [
            r"(?:Hiring Manager|Recruiter|Talent Acquisition)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"Contact\s+([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"reach out to\s+([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"Contact\s+([A-Z][a-z]+\s+[A-Z][a-z]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return "Hiring Manager"

    def _calculate_experience_years(self, resume_data: Dict[str, Any]) -> str:
        """Calculate years of experience from resume data."""
        experience_entries = resume_data.get("experience", {}).get("entries", [])
        
        if experience_entries:
            # Try to extract years from date ranges
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

    def _extract_key_skills(self, resume_data: Dict[str, Any]) -> List[str]:
        """Extract key skills from resume data."""
        skills = []
        
        # From skills section
        skills_categories = resume_data.get("skills", {}).get("categories", [])
        for category in skills_categories:
            category_skills = category.get("skills", [])
            for skill in category_skills:
                skill_name = skill.get("name", "")
                if skill_name:
                    skills.append(skill_name)
        
        # From experience technologies
        experience_entries = resume_data.get("experience", {}).get("entries", [])
        for entry in experience_entries:
            technologies = entry.get("technologies", [])
            for tech in technologies:
                if tech and tech not in skills:
                    skills.append(tech)
        
        return skills[:8]  # Return top 8 skills for brevity

    def _determine_key_area(self, resume_data: Dict[str, Any], job_description_data: Dict[str, Any]) -> str:
        """Determine key area of expertise."""
        all_skills = self._extract_key_skills(resume_data)
        
        # Get JD requirements
        jd_skills = []
        required_skills = job_description_data.get("parsed_content", {}).get("required_skills", [])
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

    def _extract_company_focus(self, job_description_data: Dict[str, Any]) -> str:
        """Extract company focus from job description."""
        text = job_description_data.get("raw_text", "").lower()
        
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

    def _extract_technologies(self, resume_data: Dict[str, Any]) -> List[str]:
        """Extract technologies from resume data."""
        technologies = []
        
        # From experience entries
        experience_entries = resume_data.get("experience", {}).get("entries", [])
        for entry in experience_entries:
            techs = entry.get("technologies", [])
            technologies.extend(techs)
        
        # From projects
        project_entries = resume_data.get("projects", {}).get("entries", [])
        for entry in project_entries:
            techs = entry.get("technologies", [])
            technologies.extend(techs)
        
        # Remove duplicates and return
        return list(set(technologies))

    def _extract_key_achievements(self, resume_data: Dict[str, Any]) -> List[str]:
        """Extract key achievements from resume data."""
        achievements = []
        
        # From experience entries
        experience_entries = resume_data.get("experience", {}).get("entries", [])
        for entry in experience_entries:
            entry_achievements = entry.get("achievements", [])
            achievements.extend(entry_achievements)
        
        return achievements[:3]  # Return top 3 achievements

    def _combine_sections(self, sections: Dict[str, Any]) -> str:
        """Combine sections into full text."""
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

    def _validate_outreach_draft(
        self,
        draft_content: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate the outreach draft for truthfulness and quality."""
        validation_result = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "guardrail_violations": []
        }
        
        full_text = draft_content.get("full_text", "")
        
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
        if word_count < 50:
            validation_result["warnings"].append("Outreach draft is quite short (under 50 words)")
        elif word_count > 300:
            validation_result["warnings"].append("Outreach draft is quite long (over 300 words)")
        
        # Check for basic structure
        sections = draft_content.get("sections", {})
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
        
        if percentage_claims > 2:
            warnings.append(f"Multiple percentage claims ({percentage_claims}) may seem exaggerated")
        
        if metric_claims > 1:
            warnings.append(f"Multiple metric claims ({metric_claims}) may seem exaggerated")
        
        return warnings

    def _calculate_truthfulness_score(
        self,
        draft_content: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> float:
        """Calculate truthfulness score for outreach draft."""
        base_score = 0.8  # Start with high score for outreach
        
        full_text = draft_content.get("full_text", "")
        
        # Deductions for fabrication indicators
        fabrication_indicators = [
            "world-class", "expert in", "master of", "pioneered",
            "revolutionized", "industry-leading", "unmatched"
        ]
        
        text_lower = full_text.lower()
        indicator_count = sum(1 for indicator in fabrication_indicators if indicator in text_lower)
        
        if indicator_count > 0:
            base_score -= min(0.3, indicator_count * 0.1)
        
        # Bonus for personalization
        if truth_bank.get("personal_info", {}).get("name"):
            if truth_bank["personal_info"]["name"].lower() in text_lower:
                base_score += 0.1
        
        return max(0.0, min(1.0, base_score))

    def _calculate_conciseness_score(self, draft_content: Dict[str, Any]) -> float:
        """Calculate conciseness score for the draft."""
        full_text = draft_content.get("full_text", "")
        word_count = len(full_text.split())
        
        # Ideal length for outreach: 100-200 words
        if word_count <= 100:
            return 0.9  # Very concise
        elif word_count <= 150:
            return 1.0  # Good length
        elif word_count <= 200:
            return 0.8  # A bit long but acceptable
        else:
            return max(0.5, 1.0 - (word_count - 200) * 0.005)

    def _calculate_professionalism_score(self, draft_content: Dict[str, Any]) -> float:
        """Calculate professionalism score for the draft."""
        full_text = draft_content.get("full_text", "")
        
        base_score = 0.8  # Start with high score
        
        # Check for professional language
        professional_terms = [
            "dear", "sincerely", "best regards", "regards", "looking forward", "opportunity"
        ]
        
        professional_count = sum(1 for term in professional_terms if term in full_text.lower())
        if professional_count >= 3:
            base_score += 0.1
        
        # Check for informal language
        informal_terms = [
            "hey", "hi", "awesome", "cool", "great", "fantastic"
        ]
        
        informal_count = sum(1 for term in informal_terms if term in full_text.lower())
        if informal_count > 0:
            base_score -= 0.1
        
        return max(0.0, min(1.0, base_score))

    def _identify_content_sources(
        self,
        draft_content: Dict[str, Any],
        truth_bank: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify sources of content in the draft."""
        sources = []
        
        full_text = draft_content.get("full_text", "")
        
        # Check for personal info
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
        
        # Check for company name
        companies = truth_bank.get("experience", {}).get("companies", [])
        for company in companies:
            if company.lower() in full_text.lower():
                sources.append({
                    "type": "resume_experience",
                    "content": company,
                    "confidence": "high"
                })
        
        return sources

    def get_available_outreach_types(self) -> Dict[str, str]:
        """Get available outreach types with descriptions."""
        return {
            "email_intro": "Short email introduction to recruiter",
            "linkedin_note": "Brief LinkedIn connection message",
            "formal_message": "More formal recruiter message"
        }


if __name__ == "__main__":
    generator = OutreachDraftGenerator()
    print("Available outreach types:")
    for outreach_type, description in generator.get_available_outreach_types().items():
        print(f"  {outreach_type}: {description}")
