"""Service for extracting truth bank data from resume."""

from typing import Dict, List, Any, Set

from .skill_categorizer import SkillCategorizer
from .types import TruthBank


class TruthBankExtractor:
    """Service for extracting truth bank information from resume data."""
    
    def __init__(self):
        self.categorizer = SkillCategorizer()
    
    def extract_from_resume(self, resume_data: Dict[str, Any]) -> TruthBank:
        """
        Extract truth bank from resume data.
        
        Args:
            resume_data: Resume data with rendering content
            
        Returns:
            Truth bank containing extracted skills and experience
        """
        truth_bank = self._initialize_truth_bank()
        
        # Extract skills from resume content
        resume_content = resume_data.get("rendering_data", {})
        
        # Extract from skills section
        self._extract_from_skills_section(resume_content, truth_bank)
        
        # Extract from experience section
        self._extract_from_experience_section(resume_content, truth_bank)
        
        # Extract from education section
        self._extract_from_education_section(resume_content, truth_bank)
        
        # Extract from projects section
        self._extract_from_projects_section(resume_content, truth_bank)
        
        # Convert sets to lists for JSON serialization
        self._convert_sets_to_lists(truth_bank)
        
        return truth_bank
    
    def _initialize_truth_bank(self) -> TruthBank:
        """Initialize an empty truth bank structure."""
        return {
            "skills": {
                "technical": set(),
                "soft_skills": set(),
                "certifications": set(),
                "tools": set(),
                "languages": set(),
                "frameworks": set(),
                "databases": set(),
                "platforms": set()
            },
            "experience": {
                "companies": set(),
                "titles": set(),
                "industries": set(),
                "years_of_experience": 0
            },
            "education": {
                "degrees": set(),
                "majors": set(),
                "universities": set()
            },
            "projects": {
                "technologies": set(),
                "domains": set(),
                "achievements": set()
            }
        }
    
    def _extract_from_skills_section(self, resume_content: Dict[str, Any], truth_bank: TruthBank) -> None:
        """Extract skills from the skills section of resume."""
        skills_categories = resume_content.get("skills", {}).get("categories", [])
        
        for category in skills_categories:
            category_name = category.get("name", "").lower()
            skills = category.get("skills", [])
            
            for skill in skills:
                skill_name = skill.get("name", "").lower()
                if not skill_name:
                    continue
                
                # Categorize the skill
                skill_category = self.categorizer.categorize_skill(skill_name)
                
                # Add to appropriate category
                if skill_category == "technical":
                    truth_bank["skills"]["technical"].add(skill_name)
                elif skill_category == "soft_skills":
                    truth_bank["skills"]["soft_skills"].add(skill_name)
                elif skill_category == "tools":
                    truth_bank["skills"]["tools"].add(skill_name)
                elif skill_category == "languages":
                    truth_bank["skills"]["languages"].add(skill_name)
                elif skill_category == "frameworks":
                    truth_bank["skills"]["frameworks"].add(skill_name)
                elif skill_category == "databases":
                    truth_bank["skills"]["databases"].add(skill_name)
                elif skill_category == "platforms":
                    truth_bank["skills"]["platforms"].add(skill_name)
                else:
                    # Default to technical if categorization fails
                    truth_bank["skills"]["technical"].add(skill_name)
    
    def _extract_from_experience_section(self, resume_content: Dict[str, Any], truth_bank: TruthBank) -> None:
        """Extract skills and experience from the experience section."""
        experience_entries = resume_content.get("experience", {}).get("entries", [])
        
        for entry in experience_entries:
            # Extract company and title information
            if entry.get("company"):
                truth_bank["experience"]["companies"].add(entry["company"].lower())
            
            if entry.get("title"):
                truth_bank["experience"]["titles"].add(entry["title"].lower())
            
            # Extract technologies mentioned in experience
            if entry.get("technologies"):
                for tech in entry["technologies"]:
                    truth_bank["skills"]["technical"].add(tech.lower())
            
            # Extract technologies from job description
            if entry.get("description"):
                desc = entry["description"].lower()
                technologies = self.categorizer.find_technologies_in_text(desc)
                for tech in technologies:
                    truth_bank["skills"]["technical"].add(tech)
            
            # Calculate years of experience (simplified)
            if entry.get("start_date") and entry.get("end_date"):
                # This is a simplified calculation - in practice, you'd parse dates properly
                truth_bank["experience"]["years_of_experience"] += 1
    
    def _extract_from_education_section(self, resume_content: Dict[str, Any], truth_bank: TruthBank) -> None:
        """Extract education information."""
        education_entries = resume_content.get("education", {}).get("entries", [])
        
        for entry in education_entries:
            if entry.get("degree"):
                truth_bank["education"]["degrees"].add(entry["degree"].lower())
            
            if entry.get("major"):
                truth_bank["education"]["majors"].add(entry["major"].lower())
            
            if entry.get("university"):
                truth_bank["education"]["universities"].add(entry["university"].lower())
    
    def _extract_from_projects_section(self, resume_content: Dict[str, Any], truth_bank: TruthBank) -> None:
        """Extract skills and achievements from projects section."""
        project_entries = resume_content.get("projects", {}).get("entries", [])
        
        for entry in project_entries:
            # Extract technologies from projects
            if entry.get("technologies"):
                for tech in entry["technologies"]:
                    truth_bank["skills"]["technical"].add(tech.lower())
            
            # Extract technologies from project description
            if entry.get("description"):
                desc = entry["description"].lower()
                technologies = self.categorizer.find_technologies_in_text(desc)
                for tech in technologies:
                    truth_bank["skills"]["technical"].add(tech)
            
            # Extract project achievements
            if entry.get("achievements"):
                for achievement in entry["achievements"]:
                    truth_bank["projects"]["achievements"].add(achievement.lower())
            
            # Extract project domains
            if entry.get("domain"):
                truth_bank["projects"]["domains"].add(entry["domain"].lower())
    
    def _convert_sets_to_lists(self, truth_bank: TruthBank) -> None:
        """Convert all sets in truth bank to lists for JSON serialization."""
        for category in truth_bank["skills"]:
            if isinstance(truth_bank["skills"][category], set):
                truth_bank["skills"][category] = list(truth_bank["skills"][category])
        
        for section in truth_bank:
            if isinstance(truth_bank[section], dict):
                for subsection in truth_bank[section]:
                    if isinstance(truth_bank[section][subsection], set):
                        truth_bank[section][subsection] = list(truth_bank[section][subsection])
