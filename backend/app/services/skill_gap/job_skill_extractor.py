"""Service for extracting skills from job descriptions."""

from typing import Dict, List, Any, DefaultDict
from collections import defaultdict

from .skill_categorizer import SkillCategorizer
from .types import SkillInfo, ImportanceLevel


class JobSkillExtractor:
    """Service for extracting and categorizing skills from job descriptions."""
    
    def __init__(self):
        self.categorizer = SkillCategorizer()
    
    def extract_from_job_descriptions(self, job_descriptions: List[Dict[str, Any]]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        Extract and categorize skills from multiple job descriptions.
        
        Args:
            job_descriptions: List of job description data
            
        Returns:
            Dictionary mapping skill categories to skill information with job associations
        """
        all_skills = self._initialize_skill_structure()
        
        for i, jd in enumerate(job_descriptions):
            jd_id = f"jd_{i+1}"
            parsed_content = jd.get("parsed_content", {})
            
            # Extract from required skills section
            self._extract_from_required_skills(parsed_content, jd, jd_id, all_skills)
            
            # Extract from responsibilities section
            self._extract_from_responsibilities(parsed_content, jd, jd_id, all_skills)
            
            # Extract from raw text
            self._extract_from_raw_text(jd, jd_id, all_skills)
        
        return all_skills
    
    def _initialize_skill_structure(self) -> Dict[str, DefaultDict[str, List[Dict[str, Any]]]]:
        """Initialize the structure for storing extracted skills."""
        return {
            "technical": defaultdict(list),
            "soft_skills": defaultdict(list),
            "tools": defaultdict(list),
            "languages": defaultdict(list),
            "frameworks": defaultdict(list),
            "databases": defaultdict(list),
            "platforms": defaultdict(list),
            "experience_levels": defaultdict(list),
            "certifications": defaultdict(list)
        }
    
    def _extract_from_required_skills(
        self, 
        parsed_content: Dict[str, Any], 
        jd: Dict[str, Any], 
        jd_id: str,
        all_skills: Dict[str, DefaultDict[str, List[Dict[str, Any]]]]
    ) -> None:
        """Extract skills from the required skills section."""
        required_skills = parsed_content.get("required_skills", [])
        
        for skill_info in required_skills:
            skill_name = skill_info.get("skill", "").lower()
            if not skill_name:
                continue
            
            # Categorize the skill
            category = self.categorizer.categorize_skill(skill_name)
            
            # Add to appropriate category with metadata
            all_skills[category.value][skill_name].append({
                "jd_id": jd_id,
                "company": jd.get("company", ""),
                "job_title": jd.get("job_title", ""),
                "experience_level": skill_info.get("experience_level", ""),
                "importance": skill_info.get("importance", ImportanceLevel.MEDIUM.value),
                "source": "required_skills"
            })
    
    def _extract_from_responsibilities(
        self, 
        parsed_content: Dict[str, Any], 
        jd: Dict[str, Any], 
        jd_id: str,
        all_skills: Dict[str, DefaultDict[str, List[Dict[str, Any]]]]
    ) -> None:
        """Extract skills from responsibilities section."""
        responsibilities = parsed_content.get("responsibilities", [])
        
        for responsibility in responsibilities:
            # Find technologies mentioned in responsibility text
            skills_in_text = self.categorizer.find_technologies_in_text(responsibility.lower())
            
            for skill in skills_in_text:
                category = self.categorizer.categorize_skill(skill)
                
                # Avoid duplicates
                if not any(occurrence["jd_id"] == jd_id and occurrence["source"] == "responsibilities" 
                          for occurrence in all_skills[category.value][skill]):
                    all_skills[category.value][skill].append({
                        "jd_id": jd_id,
                        "company": jd.get("company", ""),
                        "job_title": jd.get("job_title", ""),
                        "source": "responsibilities",
                        "importance": ImportanceLevel.MEDIUM.value
                    })
    
    def _extract_from_raw_text(
        self, 
        jd: Dict[str, Any], 
        jd_id: str,
        all_skills: Dict[str, DefaultDict[str, List[Dict[str, Any]]]]
    ) -> None:
        """Extract skills from raw job description text."""
        raw_text = jd.get("raw_text", "").lower()
        skills_in_text = self.categorizer.find_technologies_in_text(raw_text)
        
        for skill in skills_in_text:
            category = self.categorizer.categorize_skill(skill)
            
            # Avoid duplicates from other sources
            if not any(occurrence["jd_id"] == jd_id and occurrence["source"] == "raw_text" 
                      for occurrence in all_skills[category.value][skill]):
                all_skills[category.value][skill].append({
                    "jd_id": jd_id,
                    "company": jd.get("company", ""),
                    "job_title": jd.get("job_title", ""),
                    "source": "raw_text",
                    "importance": ImportanceLevel.LOW.value
                })
    
    def consolidate_skill_occurrences(self, all_skills: Dict[str, DefaultDict[str, List[Dict[str, Any]]]]) -> Dict[str, List[SkillInfo]]:
        """
        Consolidate skill occurrences into skill information objects.
        
        Args:
            all_skills: Raw skill occurrences from job descriptions
            
        Returns:
            Dictionary mapping categories to consolidated skill information
        """
        consolidated = {}
        
        for category in ["technical", "soft_skills", "tools", "languages", "frameworks", "databases", "platforms"]:
            consolidated[category] = []
            
            for skill_name, occurrences in all_skills[category].items():
                # Calculate frequency and importance
                frequency = len(occurrences)
                high_importance_count = sum(
                    1 for occ in occurrences 
                    if occ.get("importance") == ImportanceLevel.HIGH.value
                )
                
                # Get unique jobs and companies
                jobs = list(set(occ["jd_id"] for occ in occurrences))
                companies = list(set(occ["company"] for occ in occurrences if occ["company"]))
                
                # Calculate priority score
                priority_score = self._calculate_priority_score(frequency, high_importance_count)
                
                skill_info: SkillInfo = {
                    "skill": skill_name,
                    "frequency": frequency,
                    "importance": high_importance_count,
                    "jobs": jobs,
                    "companies": companies,
                    "priority_score": priority_score,
                    "category": category
                }
                
                consolidated[category].append(skill_info)
            
            # Sort by priority score
            consolidated[category].sort(key=lambda x: x["priority_score"], reverse=True)
        
        return consolidated
    
    def _calculate_priority_score(self, frequency: int, high_importance_count: int) -> float:
        """
        Calculate priority score for a skill based on frequency and importance.
        
        Args:
            frequency: How many times the skill appears
            high_importance_count: How many times marked as high importance
            
        Returns:
            Priority score between 0 and 1
        """
        from .config import PRIORITY_WEIGHTS, NORMALIZATION_CONSTANTS
        
        # Weight frequency more heavily than importance
        frequency_weight = PRIORITY_WEIGHTS["frequency"]
        importance_weight = PRIORITY_WEIGHTS["importance"]
        
        # Normalize values
        normalized_frequency = min(frequency / NORMALIZATION_CONSTANTS["max_frequency"], 1.0)
        normalized_importance = min(high_importance_count / NORMALIZATION_CONSTANTS["max_importance"], 1.0)
        
        return (normalized_frequency * frequency_weight + normalized_importance * importance_weight)
