"""Service for analyzing skill gaps between resume and job requirements."""

from typing import Dict, List, Any

from .types import TruthBank, SkillGap, SkillInfo, AnalysisOptions


class GapAnalyzer:
    """Service for analyzing skill gaps between user skills and job requirements."""
    
    def analyze_gaps(
        self, 
        truth_bank: TruthBank, 
        job_skills: Dict[str, List[SkillInfo]],
        options: AnalysisOptions
    ) -> SkillGap:
        """
        Analyze skill gaps between truth bank and job requirements.
        
        Args:
            truth_bank: User's skills and experience
            job_skills: Skills required by job descriptions
            options: Analysis configuration options
            
        Returns:
            Skill gap analysis results
        """
        skill_gaps = self._initialize_skill_gaps()
        
        # Analyze each skill category
        for category in ["technical", "soft_skills", "tools", "languages", "frameworks", "databases", "platforms"]:
            user_skills = set(truth_bank["skills"].get(category, []))
            required_skills = job_skills.get(category, [])
            
            missing_skills = self._find_missing_skills(user_skills, required_skills)
            skill_gaps[f"missing_{category}"] = missing_skills
        
        # Create summary
        skill_gaps["gap_summary"] = self._create_gap_summary(skill_gaps)
        
        return skill_gaps
    
    def _initialize_skill_gaps(self) -> SkillGap:
        """Initialize empty skill gaps structure."""
        return {
            "missing_technical": [],
            "missing_soft_skills": [],
            "missing_tools": [],
            "missing_languages": [],
            "missing_frameworks": [],
            "missing_databases": [],
            "missing_platforms": [],
            "gap_summary": {}
        }
    
    def _find_missing_skills(
        self, 
        user_skills: set, 
        required_skills: List[SkillInfo]
    ) -> List[SkillInfo]:
        """
        Find skills that user doesn't have but are required.
        
        Args:
            user_skills: Set of user's skills
            required_skills: List of required skills with metadata
            
        Returns:
            List of missing skills
        """
        missing_skills = []
        
        for skill_info in required_skills:
            if skill_info["skill"] not in user_skills:
                missing_skills.append(skill_info)
        
        return missing_skills
    
    def _create_gap_summary(self, skill_gaps: SkillGap) -> Dict[str, Any]:
        """
        Create a summary of skill gaps.
        
        Args:
            skill_gaps: Skill gap analysis results
            
        Returns:
            Summary statistics
        """
        total_missing = 0
        category_counts = {}
        
        # Count missing skills by category
        for category in ["technical", "soft_skills", "tools", "languages", "frameworks", "databases", "platforms"]:
            key = f"missing_{category}"
            count = len(skill_gaps[key])
            category_counts[category] = count
            total_missing += count
        
        return {
            "total_missing_skills": total_missing,
            "categories": category_counts
        }
