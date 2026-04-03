"""Skill Gap Analysis Service."""

from typing import Dict, List, Any, Optional

from .skill_gap import SkillGapAnalyzer as ModularSkillGapAnalyzer

# Maintain backward compatibility with existing interface
class SkillGapAnalyzer:
    """
    Legacy interface for skill gap analysis.
    
    This class maintains backward compatibility while using the new modular architecture.
    """
    
    def __init__(self):
        self._analyzer = ModularSkillGapAnalyzer()
    
    def analyze_skill_gaps(
        self,
        resume_data: Dict[str, Any],
        job_descriptions: List[Dict[str, Any]],
        analysis_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze skill gaps between resume and multiple job descriptions.
        
        Args:
            resume_data: Resume data with rendering content
            job_descriptions: List of job description data
            analysis_options: Options for analysis
            
        Returns:
            Comprehensive skill gap analysis with recommendations
        """
        return self._analyzer.analyze_skill_gaps(
            resume_data, job_descriptions, analysis_options
        )
