"""Skill Gap Analysis Module."""

from .analysis_orchestrator import AnalysisOrchestrator
from .types import (
    SkillCategory, ImportanceLevel, Priority, Difficulty, Assessment,
    AnalysisOptions, TruthBank, SkillGapAnalysisResult
)

# Main entry point for skill gap analysis
class SkillGapAnalyzer:
    """
    Main interface for skill gap analysis.
    
    This class provides a simplified interface that maintains backward compatibility
    while using the new modular architecture internally.
    """
    
    def __init__(self):
        self.orchestrator = AnalysisOrchestrator()
    
    def analyze_skill_gaps(
        self,
        resume_data: Dict[str, Any],
        job_descriptions: List[Dict[str, Any]],
        analysis_options: AnalysisOptions = None
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
        return self.orchestrator.analyze_skill_gaps(
            resume_data, job_descriptions, analysis_options
        )
