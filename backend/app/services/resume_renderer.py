from typing import Dict, Any, Optional
from datetime import datetime
import json


class ResumeRenderer:
    """
    Service to prepare tailored resume data for document rendering (PDF, DOCX, etc.).
    """

    def __init__(self):
        self.templates = {
            "modern": "modern_template",
            "professional": "professional_template",
            "technical": "technical_template",
            "creative": "creative_template"
        }

    def prepare_for_pdf_rendering(
        self,
        tailored_resume_data: Dict[str, Any],
        template: str = "professional",
        include_metadata: bool = False
    ) -> Dict[str, Any]:
        """
        Prepare tailored resume data for PDF rendering.
        
        Args:
            tailored_resume_data: Tailored resume data from TailoredResumeBuilder
            template: Template style to use for rendering
            include_metadata: Whether to include metadata in the output
            
        Returns:
            Resume data structured for PDF rendering
        """
        rendering_data = self._structure_resume_content(tailored_resume_data)
        
        pdf_data = {
            "template": template,
            "content": rendering_data,
            "formatting": self._get_formatting_rules(template),
            "metadata": self._get_rendering_metadata(tailored_resume_data) if include_metadata else None,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return pdf_data

    def prepare_for_docx_rendering(
        self,
        tailored_resume_data: Dict[str, Any],
        template: str = "professional"
    ) -> Dict[str, Any]:
        """
        Prepare tailored resume data for DOCX rendering.
        
        Args:
            tailored_resume_data: Tailored resume data
            template: Template style to use
            
        Returns:
            Resume data structured for DOCX rendering
        """
        rendering_data = self._structure_resume_content(tailored_resume_data)
        
        docx_data = {
            "template": template,
            "content": rendering_data,
            "styles": self._get_docx_styles(template),
            "sections": self._get_docx_sections(rendering_data),
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return docx_data

    def _structure_resume_content(self, tailored_resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Structure the resume content for rendering.
        
        Args:
            tailored_resume_data: Raw tailored resume data
            
        Returns:
            Structured content ready for rendering
        """
        content = tailored_resume_data.get("rendering_data", {})
        
        structured_content = {
            "header": self._structure_header(content.get("header", {})),
            "summary": self._structure_summary(content.get("summary", "")),
            "skills": self._structure_skills(content.get("skills", {})),
            "experience": self._structure_experience(content.get("experience", [])),
            "education": self._structure_education(content.get("education", [])),
            "projects": self._structure_projects(content.get("projects", [])),
            "certifications": self._structure_certifications(content.get("certifications", [])),
            "languages": self._structure_languages(content.get("languages", []))
        }
        
        return structured_content

    def _structure_header(self, header_data: Dict[str, Any]) -> Dict[str, Any]:
        """Structure the header section."""
        return {
            "name": header_data.get("name", ""),
            "contact": {
                "email": header_data.get("contact", {}).get("email", ""),
                "phone": header_data.get("contact", {}).get("phone", ""),
                "location": header_data.get("contact", {}).get("location", ""),
                "linkedin": header_data.get("contact", {}).get("linkedin", ""),
                "github": header_data.get("contact", {}).get("github", ""),
                "website": header_data.get("contact", {}).get("website", "")
            },
            "layout": "centered"  # Can be customized based on template
        }

    def _structure_summary(self, summary_text: str) -> Dict[str, Any]:
        """Structure the summary section."""
        return {
            "title": "Professional Summary",
            "content": summary_text,
            "style": "paragraph",
            "max_lines": 4
        }

    def _structure_skills(self, skills_data: Dict[str, Any]) -> Dict[str, Any]:
        """Structure the skills section."""
        technical_skills = skills_data.get("technical", [])
        soft_skills = skills_data.get("soft_skills", [])
        
        return {
            "title": "Skills",
            "categories": [
                {
                    "name": "Technical Skills",
                    "skills": [self._format_skill(skill) for skill in technical_skills],
                    "layout": "columns" if len(technical_skills) > 6 else "list"
                },
                {
                    "name": "Soft Skills",
                    "skills": [self._format_skill(skill) for skill in soft_skills],
                    "layout": "list"
                }
            ]
        }

    def _format_skill(self, skill: Any) -> Dict[str, Any]:
        """Format a single skill entry."""
        if isinstance(skill, dict):
            return {
                "name": skill.get("name", ""),
                "level": skill.get("proficiency_level", skill.get("years_of_experience", "")),
                "highlight": skill.get("added_via_tailoring", False)
            }
        else:
            return {
                "name": str(skill),
                "level": "",
                "highlight": False
            }

    def _structure_experience(self, experience_data: list) -> Dict[str, Any]:
        """Structure the experience section."""
        return {
            "title": "Professional Experience",
            "entries": [self._format_experience_entry(entry) for entry in experience_data],
            "reverse_chronological": True
        }

    def _format_experience_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Format a single experience entry."""
        return {
            "title": entry.get("title", ""),
            "company": entry.get("company", ""),
            "location": entry.get("location", ""),
            "dates": self._format_dates(entry.get("start_date"), entry.get("end_date"), entry.get("current")),
            "description": entry.get("description", ""),
            "achievements": entry.get("achievements", []),
            "technologies": entry.get("technologies", []),
            "layout": "standard"
        }

    def _format_dates(self, start_date: str, end_date: str, current: bool) -> str:
        """Format date range for display."""
        if not start_date:
            return ""
        
        start_formatted = self._format_single_date(start_date)
        
        if current:
            return f"{start_formatted} - Present"
        
        if end_date:
            end_formatted = self._format_single_date(end_date)
            return f"{start_formatted} - {end_formatted}"
        
        return start_formatted

    def _format_single_date(self, date_str: str) -> str:
        """Format a single date."""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%B %Y")
        except ValueError:
            return date_str

    def _structure_education(self, education_data: list) -> Dict[str, Any]:
        """Structure the education section."""
        return {
            "title": "Education",
            "entries": [self._format_education_entry(entry) for entry in education_data],
            "reverse_chronological": True
        }

    def _format_education_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Format a single education entry."""
        return {
            "degree": entry.get("degree", ""),
            "major": entry.get("major", ""),
            "university": entry.get("university", ""),
            "location": entry.get("location", ""),
            "graduation_year": entry.get("graduation_year", ""),
            "gpa": entry.get("gpa", ""),
            "honors": entry.get("honors", []),
            "layout": "standard"
        }

    def _structure_projects(self, projects_data: list) -> Dict[str, Any]:
        """Structure the projects section."""
        if not projects_data:
            return None
        
        return {
            "title": "Projects",
            "entries": [self._format_project_entry(entry) for entry in projects_data],
            "max_entries": 3,  # Limit to most relevant projects
            "reverse_chronological": True
        }

    def _format_project_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Format a single project entry."""
        return {
            "name": entry.get("name", ""),
            "description": entry.get("description", ""),
            "technologies": entry.get("technologies", []),
            "dates": self._format_dates(entry.get("start_date"), entry.get("end_date"), False),
            "url": entry.get("url", ""),
            "layout": "standard"
        }

    def _structure_certifications(self, certifications_data: list) -> Optional[Dict[str, Any]]:
        """Structure the certifications section."""
        if not certifications_data:
            return None
        
        return {
            "title": "Certifications",
            "entries": [self._format_certification_entry(entry) for entry in certifications_data],
            "reverse_chronological": True
        }

    def _format_certification_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Format a single certification entry."""
        return {
            "name": entry.get("name", ""),
            "issuer": entry.get("issuer", ""),
            "date": entry.get("date", entry.get("year", "")),
            "credential_id": entry.get("credential_id", ""),
            "url": entry.get("url", ""),
            "layout": "compact"
        }

    def _structure_languages(self, languages_data: list) -> Optional[Dict[str, Any]]:
        """Structure the languages section."""
        if not languages_data:
            return None
        
        return {
            "title": "Languages",
            "languages": [self._format_language_entry(entry) for entry in languages_data],
            "layout": "inline"
        }

    def _format_language_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Format a single language entry."""
        return {
            "language": entry.get("language", ""),
            "proficiency": entry.get("proficiency", ""),
            "certification": entry.get("certification", "")
        }

    def _get_formatting_rules(self, template: str) -> Dict[str, Any]:
        """Get formatting rules for the specified template."""
        base_rules = {
            "font_family": "Arial",
            "font_size": 11,
            "line_spacing": 1.15,
            "margin_top": 0.5,
            "margin_bottom": 0.5,
            "margin_left": 0.75,
            "margin_right": 0.75
        }
        
        template_specific = {
            "professional": {
                "font_family": "Calibri",
                "font_size": 11,
                "header_font_size": 14,
                "section_spacing": 1.2
            },
            "modern": {
                "font_family": "Helvetica",
                "font_size": 10,
                "header_font_size": 16,
                "section_spacing": 1.5
            },
            "technical": {
                "font_family": "Consolas",
                "font_size": 10,
                "header_font_size": 12,
                "section_spacing": 1.1
            },
            "creative": {
                "font_family": "Georgia",
                "font_size": 12,
                "header_font_size": 18,
                "section_spacing": 1.3
            }
        }
        
        return {**base_rules, **template_specific.get(template, {})}

    def _get_docx_styles(self, template: str) -> Dict[str, Any]:
        """Get DOCX-specific styles for the template."""
        return {
            "heading_1": {
                "font_size": 16,
                "bold": True,
                "color": "#2C3E50",
                "spacing_after": 12
            },
            "heading_2": {
                "font_size": 14,
                "bold": True,
                "color": "#34495E",
                "spacing_after": 8
            },
            "normal": {
                "font_size": 11,
                "spacing_after": 6
            },
            "contact_info": {
                "font_size": 10,
                "italic": True,
                "color": "#7F8C8D"
            },
            "skills": {
                "font_size": 10,
                "spacing_after": 3
            }
        }

    def _get_docx_sections(self, content: Dict[str, Any]) -> list:
        """Get section order for DOCX rendering."""
        sections = []
        
        if content.get("header"):
            sections.append({"type": "header", "content": content["header"]})
        
        if content.get("summary"):
            sections.append({"type": "summary", "content": content["summary"]})
        
        if content.get("experience"):
            sections.append({"type": "experience", "content": content["experience"]})
        
        if content.get("education"):
            sections.append({"type": "education", "content": content["education"]})
        
        if content.get("skills"):
            sections.append({"type": "skills", "content": content["skills"]})
        
        if content.get("projects"):
            sections.append({"type": "projects", "content": content["projects"]})
        
        if content.get("certifications"):
            sections.append({"type": "certifications", "content": content["certifications"]})
        
        if content.get("languages"):
            sections.append({"type": "languages", "content": content["languages"]})
        
        return sections

    def _get_rendering_metadata(self, tailored_resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get metadata for the rendering process."""
        metadata = tailored_resume_data.get("metadata", {})
        
        return {
            "alignment_score": metadata.get("final_alignment_score", 0),
            "truthfulness_score": metadata.get("truthfulness_score", 0.0),
            "total_changes": metadata.get("total_changes_applied", 0),
            "processing_time": metadata.get("processing_time_ms", 0),
            "generated_at": metadata.get("created_at", datetime.utcnow().isoformat()),
            "version": 1
        }

    def validate_rendering_data(self, rendering_data: Dict[str, Any]) -> tuple[bool, list]:
        """
        Validate the rendering data before document generation.
        
        Args:
            rendering_data: Structured rendering data
            
        Returns:
            Tuple of (is_valid, list_of_validation_errors)
        """
        errors = []
        
        # Check required sections
        content = rendering_data.get("content", {})
        
        if not content.get("header", {}).get("name"):
            errors.append("Missing name in header section")
        
        if not content.get("summary", {}).get("content"):
            errors.append("Missing summary content")
        
        if not content.get("experience", {}).get("entries"):
            errors.append("Missing experience entries")
        
        # Validate experience entries
        experience_entries = content.get("experience", {}).get("entries", [])
        for i, entry in enumerate(experience_entries):
            if not entry.get("title"):
                errors.append(f"Experience entry {i+1} missing title")
            if not entry.get("company"):
                errors.append(f"Experience entry {i+1} missing company")
        
        # Check for reasonable content length
        summary_content = content.get("summary", {}).get("content", "")
        if len(summary_content) > 500:
            errors.append("Summary is too long (max 500 characters)")
        
        if len(experience_entries) > 10:
            errors.append("Too many experience entries (max 10)")
        
        return len(errors) == 0, errors

    def generate_rendering_preview(
        self,
        rendering_data: Dict[str, Any],
        format_type: str = "text"
    ) -> str:
        """
        Generate a text preview of the rendered resume.
        
        Args:
            rendering_data: Structured rendering data
            format_type: Format for preview ("text" or "markdown")
            
        Returns:
            Text preview of the resume
        """
        content = rendering_data.get("content", {})
        
        if format_type == "markdown":
            return self._generate_markdown_preview(content)
        else:
            return self._generate_text_preview(content)

    def _generate_text_preview(self, content: Dict[str, Any]) -> str:
        """Generate plain text preview."""
        lines = []
        
        # Header
        header = content.get("header", {})
        lines.append(header.get("name", "").upper())
        
        contact = header.get("contact", {})
        contact_info = [
            contact.get("email", ""),
            contact.get("phone", ""),
            contact.get("location", ""),
            contact.get("linkedin", ""),
            contact.get("github", "")
        ]
        lines.append(" | ".join(filter(None, contact_info)))
        lines.append("")
        
        # Summary
        summary = content.get("summary", {})
        if summary.get("content"):
            lines.append(summary.get("title", "PROFESSIONAL SUMMARY"))
            lines.append(summary.get("content", ""))
            lines.append("")
        
        # Experience
        experience = content.get("experience", {})
        if experience.get("entries"):
            lines.append(experience.get("title", "PROFESSIONAL EXPERIENCE"))
            for entry in experience.get("entries", []):
                lines.append(f"{entry.get('title', '')} at {entry.get('company', '')}")
                lines.append(f"{entry.get('dates', '')}")
                if entry.get("description"):
                    lines.append(entry.get("description", ""))
                for achievement in entry.get("achievements", []):
                    lines.append(f"• {achievement}")
                lines.append("")
        
        # Skills
        skills = content.get("skills", {})
        if skills.get("categories"):
            lines.append(skills.get("title", "SKILLS"))
            for category in skills.get("categories", []):
                lines.append(f"{category.get('name', '')}: {', '.join([s.get('name', '') for s in category.get('skills', [])])}")
            lines.append("")
        
        return "\n".join(lines)

    def _generate_markdown_preview(self, content: Dict[str, Any]) -> str:
        """Generate markdown preview."""
        lines = []
        
        # Header
        header = content.get("header", {})
        lines.append(f"# {header.get('name', '')}")
        
        contact = header.get("contact", {})
        contact_info = [
            contact.get("email", ""),
            contact.get("phone", ""),
            contact.get("location", ""),
            contact.get("linkedin", ""),
            contact.get("github", "")
        ]
        lines.append("*" + " | ".join(filter(None, contact_info)) + "*")
        lines.append("")
        
        # Summary
        summary = content.get("summary", {})
        if summary.get("content"):
            lines.append(f"## {summary.get('title', 'Professional Summary')}")
            lines.append(summary.get("content", ""))
            lines.append("")
        
        # Experience
        experience = content.get("experience", {})
        if experience.get("entries"):
            lines.append(f"## {experience.get('title', 'Professional Experience')}")
            for entry in experience.get("entries", []):
                lines.append(f"### {entry.get('title', '')} at {entry.get('company', '')}")
                lines.append(f"*{entry.get('dates', '')}*")
                if entry.get("description"):
                    lines.append(entry.get("description", ""))
                for achievement in entry.get("achievements", []):
                    lines.append(f"- {achievement}")
                lines.append("")
        
        # Skills
        skills = content.get("skills", {})
        if skills.get("categories"):
            lines.append(f"## {skills.get('title', 'Skills')}")
            for category in skills.get("categories", []):
                skill_names = [s.get('name', '') for s in category.get('skills', [])]
                lines.append(f"**{category.get('name', '')}:** {', '.join(skill_names)}")
            lines.append("")
        
        return "\n".join(lines)
