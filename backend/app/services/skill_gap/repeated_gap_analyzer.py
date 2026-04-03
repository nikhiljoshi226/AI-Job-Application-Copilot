"""Service for identifying repeated skill gaps across job descriptions."""

from typing import Dict, List, Any
from collections import defaultdict

from .types import SkillGap, RepeatedGaps, AnalysisOptions, SkillInfo


class RepeatedGapAnalyzer:
    """Service for analyzing repeated skill gaps across multiple job descriptions."""
    
    def analyze_repeated_gaps(
        self, 
        skill_gaps: SkillGap, 
        options: AnalysisOptions
    ) -> RepeatedGaps:
        """
        Identify skill gaps that appear repeatedly across job descriptions.
        
        Args:
            skill_gaps: Skill gap analysis results
            options: Analysis configuration options
            
        Returns:
            Repeated gaps analysis
        """
        repeated_gaps = self._initialize_repeated_gaps()
        
        # Collect all missing skills
        all_missing_skills = self._collect_all_missing_skills(skill_gaps)
        
        # Find high-frequency gaps
        repeated_gaps["high_frequency_gaps"] = self._find_high_frequency_gaps(
            all_missing_skills, options
        )
        
        # Find critical gaps (high importance + frequency)
        repeated_gaps["critical_gaps"] = self._find_critical_gaps(
            all_missing_skills, options
        )
        
        # Analyze gaps by category
        repeated_gaps["category_gaps"] = self._analyze_category_gaps(all_missing_skills)
        
        # Create analysis summary
        repeated_gaps["gap_analysis"] = self._create_gap_analysis_summary(
            repeated_gaps["high_frequency_gaps"],
            repeated_gaps["critical_gaps"],
            repeated_gaps["category_gaps"]
        )
        
        return repeated_gaps
    
    def _initialize_repeated_gaps(self) -> RepeatedGaps:
        """Initialize empty repeated gaps structure."""
        return {
            "high_frequency_gaps": [],
            "critical_gaps": [],
            "category_gaps": {},
            "gap_analysis": {}
        }
    
    def _collect_all_missing_skills(self, skill_gaps: SkillGap) -> List[SkillInfo]:
        """
        Collect all missing skills from different categories.
        
        Args:
            skill_gaps: Skill gap analysis results
            
        Returns:
            List of all missing skills with category information
        """
        all_missing_skills = []
        
        for category in ["technical", "soft_skills", "tools", "languages", "frameworks", "databases", "platforms"]:
            key = f"missing_{category}"
            if key in skill_gaps:
                for skill_info in skill_gaps[key]:
                    skill_info["category"] = category
                    all_missing_skills.append(skill_info)
        
        return all_missing_skills
    
    def _find_high_frequency_gaps(
        self, 
        all_missing_skills: List[SkillInfo], 
        options: AnalysisOptions
    ) -> List[SkillInfo]:
        """
        Find skills that appear frequently across job descriptions.
        
        Args:
            all_missing_skills: List of all missing skills
            options: Analysis configuration options
            
        Returns:
            High-frequency gaps sorted by frequency
        """
        min_frequency = options.get("min_gap_frequency", 2)
        
        high_frequency_gaps = [
            skill for skill in all_missing_skills 
            if skill["frequency"] >= min_frequency
        ]
        
        # Sort by frequency (descending)
        high_frequency_gaps.sort(key=lambda x: x["frequency"], reverse=True)
        
        # Return top 10
        return high_frequency_gaps[:10]
    
    def _find_critical_gaps(
        self, 
        all_missing_skills: List[SkillInfo], 
        options: AnalysisOptions
    ) -> List[SkillInfo]:
        """
        Find skills that are both high frequency and high importance.
        
        Args:
            all_missing_skills: List of all missing skills
            options: Analysis configuration options
            
        Returns:
            Critical gaps sorted by importance and frequency
        """
        min_frequency = options.get("min_gap_frequency", 2)
        
        critical_gaps = [
            skill for skill in all_missing_skills 
            if skill["frequency"] >= min_frequency and skill["importance"] > 0
        ]
        
        # Sort by importance first, then frequency (both descending)
        critical_gaps.sort(key=lambda x: (x["importance"], x["frequency"]), reverse=True)
        
        # Return top 10
        return critical_gaps[:10]
    
    def _analyze_category_gaps(self, all_missing_skills: List[SkillInfo]) -> Dict[str, List[SkillInfo]]:
        """
        Analyze gaps by skill category.
        
        Args:
            all_missing_skills: List of all missing skills
            
        Returns:
            Dictionary mapping categories to top gaps
        """
        category_gaps = defaultdict(list)
        
        # Group skills by category
        for skill in all_missing_skills:
            category_gaps[skill["category"]].append(skill)
        
        # Sort each category by frequency and return top 5
        result = {}
        for category, skills in category_gaps.items():
            skills.sort(key=lambda x: x["frequency"], reverse=True)
            result[category] = skills[:5]
        
        return result
    
    def _create_gap_analysis_summary(
        self,
        high_frequency_gaps: List[SkillInfo],
        critical_gaps: List[SkillInfo],
        category_gaps: Dict[str, List[SkillInfo]]
    ) -> Dict[str, Any]:
        """
        Create a summary of the gap analysis.
        
        Args:
            high_frequency_gaps: High-frequency gaps
            critical_gaps: Critical gaps
            category_gaps: Gaps by category
            
        Returns:
            Analysis summary statistics
        """
        total_repeated_gaps = len(high_frequency_gaps)
        critical_gaps_count = len(critical_gaps)
        categories_with_gaps = len(category_gaps)
        
        # Calculate average gap frequency
        average_gap_frequency = 0
        if high_frequency_gaps:
            total_frequency = sum(skill["frequency"] for skill in high_frequency_gaps)
            average_gap_frequency = total_frequency / total_repeated_gaps
        
        # Find most common gap
        most_common_gap = None
        if high_frequency_gaps:
            most_common_gap = high_frequency_gaps[0]
        
        return {
            "total_repeated_gaps": total_repeated_gaps,
            "most_common_gap": most_common_gap,
            "critical_gaps_count": critical_gaps_count,
            "categories_with_gaps": categories_with_gaps,
            "average_gap_frequency": round(average_gap_frequency, 2)
        }
