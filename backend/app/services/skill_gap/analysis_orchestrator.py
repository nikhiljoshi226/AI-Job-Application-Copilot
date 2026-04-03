"""Orchestrator service for coordinating skill gap analysis."""

import time
from datetime import datetime
from typing import Dict, List, Any

from .types import (
    TruthBank, AnalysisOptions, SkillGapAnalysisResult, 
    AnalysisMetadata, CompleteAnalysisResult, Assessment
)
from .config import DEFAULT_ANALYSIS_OPTIONS, ASSESSMENT_THRESHOLDS, ASSESSMENT_MESSAGES
from .truth_bank_extractor import TruthBankExtractor
from .job_skill_extractor import JobSkillExtractor
from .gap_analyzer import GapAnalyzer
from .repeated_gap_analyzer import RepeatedGapAnalyzer
from .recommendation_generator import RecommendationGenerator


class AnalysisOrchestrator:
    """Orchestrates the complete skill gap analysis workflow."""
    
    def __init__(self):
        self.truth_bank_extractor = TruthBankExtractor()
        self.job_skill_extractor = JobSkillExtractor()
        self.gap_analyzer = GapAnalyzer()
        self.repeated_gap_analyzer = RepeatedGapAnalyzer()
        self.recommendation_generator = RecommendationGenerator()
    
    def analyze_skill_gaps(
        self,
        resume_data: Dict[str, Any],
        job_descriptions: List[Dict[str, Any]],
        analysis_options: AnalysisOptions = None
    ) -> CompleteAnalysisResult:
        """
        Perform complete skill gap analysis.
        
        Args:
            resume_data: Resume data with rendering content
            job_descriptions: List of job description data
            analysis_options: Options for analysis
            
        Returns:
            Complete analysis result with metadata
        """
        start_time = time.time()
        
        # Set default options
        options = self._prepare_analysis_options(analysis_options)
        
        # Step 1: Extract truth bank from resume
        truth_bank = self.truth_bank_extractor.extract_from_resume(resume_data)
        
        # Step 2: Extract skills from job descriptions
        raw_job_skills = self.job_skill_extractor.extract_from_job_descriptions(job_descriptions)
        job_skills = self.job_skill_extractor.consolidate_skill_occurrences(raw_job_skills)
        
        # Step 3: Analyze skill gaps
        skill_gaps = self.gap_analyzer.analyze_gaps(truth_bank, job_skills, options)
        
        # Step 4: Identify repeated gaps
        repeated_gaps = self.repeated_gap_analyzer.analyze_repeated_gaps(skill_gaps, options)
        
        # Step 5: Analyze role expectations
        role_expectations = self._analyze_role_expectations(job_descriptions)
        
        # Step 6: Generate learning recommendations
        learning_recommendations = self.recommendation_generator.generate_learning_recommendations(
            repeated_gaps, truth_bank, options
        )
        
        # Step 7: Generate project suggestions
        project_suggestions = self.recommendation_generator.generate_project_suggestions(
            repeated_gaps, truth_bank, options
        )
        
        # Step 8: Calculate skill coverage score
        skill_coverage_score = self._calculate_skill_coverage_score(truth_bank, job_skills)
        
        # Step 9: Generate action items
        action_items = self.recommendation_generator.generate_action_items(
            repeated_gaps, learning_recommendations, project_suggestions, options
        )
        
        # Step 10: Create analysis summary
        analysis_summary = self._create_analysis_summary(
            skill_gaps, repeated_gaps, role_expectations, skill_coverage_score
        )
        
        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)
        
        # Build skill gap analysis result
        skill_gap_analysis: SkillGapAnalysisResult = {
            "analysis_name": f"Skill Gap Analysis - {len(job_descriptions)} Jobs",
            "job_count": len(job_descriptions),
            "analysis_summary": analysis_summary,
            "missing_skills": skill_gaps,
            "repeated_gaps": repeated_gaps,
            "role_expectations": role_expectations,
            "learning_recommendations": learning_recommendations,
            "project_suggestions": project_suggestions,
            "skill_coverage_score": skill_coverage_score,
            "action_items": action_items
        }
        
        # Create metadata
        metadata: AnalysisMetadata = {
            "processing_time_ms": processing_time,
            "analysis_options": options,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return {
            "skill_gap_analysis": skill_gap_analysis,
            "metadata": metadata
        }
    
    def _prepare_analysis_options(self, analysis_options: AnalysisOptions = None) -> AnalysisOptions:
        """Prepare analysis options with defaults."""
        options = DEFAULT_ANALYSIS_OPTIONS.copy()
        if analysis_options:
            options.update(analysis_options)
        return options
    
    def _analyze_role_expectations(self, job_descriptions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze common role expectations across job descriptions.
        
        Args:
            job_descriptions: List of job description data
            
        Returns:
            Role expectations analysis
        """
        from collections import Counter
        
        role_expectations = {
            "common_responsibilities": [],
            "common_qualifications": [],
            "experience_requirements": [],
            "company_culture_aspects": [],
            "industry_trends": []
        }
        
        # Collect data from all job descriptions
        all_responsibilities = []
        all_qualifications = []
        all_experience = []
        
        for jd in job_descriptions:
            parsed_content = jd.get("parsed_content", {})
            
            # Responsibilities
            responsibilities = parsed_content.get("responsibilities", [])
            all_responsibilities.extend(responsibilities)
            
            # Qualifications
            qualifications = parsed_content.get("qualifications", [])
            all_qualifications.extend(qualifications)
            
            # Experience requirements
            experience = parsed_content.get("experience_requirements", [])
            all_experience.extend(experience)
        
        # Find common patterns using Counter
        if all_responsibilities:
            responsibility_counter = Counter(all_responsibilities)
            role_expectations["common_responsibilities"] = [
                {"responsibility": resp, "frequency": count, "jobs": count}
                for resp, count in responsibility_counter.most_common(10)
            ]
        
        if all_qualifications:
            qualification_counter = Counter(all_qualifications)
            role_expectations["common_qualifications"] = [
                {"qualification": qual, "frequency": count, "jobs": count}
                for qual, count in qualification_counter.most_common(10)
            ]
        
        if all_experience:
            experience_counter = Counter(all_experience)
            role_expectations["experience_requirements"] = [
                {"requirement": exp, "frequency": count, "jobs": count}
                for exp, count in experience_counter.most_common(5)
            ]
        
        return role_expectations
    
    def _calculate_skill_coverage_score(
        self, 
        truth_bank: TruthBank, 
        job_skills: Dict[str, List[Dict[str, Any]]]
    ) -> float:
        """
        Calculate overall skill coverage score.
        
        Args:
            truth_bank: User's skills and experience
            job_skills: Required skills from job descriptions
            
        Returns:
            Coverage score between 0 and 1
        """
        total_required_skills = 0
        total_covered_skills = 0
        
        for category in ["technical", "soft_skills", "tools", "languages", "frameworks", "databases", "platforms"]:
            user_skills = set(truth_bank["skills"].get(category, []))
            required_skills = set(job_skills.get(category, {}).keys())
            
            total_required_skills += len(required_skills)
            total_covered_skills += len(user_skills.intersection(required_skills))
        
        # Calculate coverage percentage
        if total_required_skills == 0:
            return 0.0
        
        coverage_score = total_covered_skills / total_required_skills
        return round(coverage_score, 2)
    
    def _create_analysis_summary(
        self,
        skill_gaps: Dict[str, Any],
        repeated_gaps: Dict[str, Any],
        role_expectations: Dict[str, Any],
        skill_coverage_score: float
    ) -> Dict[str, Any]:
        """
        Create a summary of the analysis.
        
        Args:
            skill_gaps: Skill gap analysis results
            repeated_gaps: Repeated gaps analysis
            role_expectations: Role expectations analysis
            skill_coverage_score: Overall skill coverage score
            
        Returns:
            Analysis summary
        """
        total_missing = skill_gaps.get("gap_summary", {}).get("total_missing_skills", 0)
        high_freq_gaps = len(repeated_gaps.get("high_frequency_gaps", []))
        critical_gaps = len(repeated_gaps.get("critical_gaps", []))
        
        # Determine overall assessment
        assessment = self._determine_assessment(skill_coverage_score)
        assessment_message = ASSESSMENT_MESSAGES[assessment]
        
        return {
            "overall_assessment": assessment,
            "assessment_message": assessment_message,
            "skill_coverage_score": skill_coverage_score,
            "total_missing_skills": total_missing,
            "high_frequency_gaps": high_freq_gaps,
            "critical_gaps": critical_gaps,
            "key_findings": [
                f"Your skills cover {skill_coverage_score:.1%} of job requirements",
                f"{total_missing} skills are missing across analyzed positions",
                f"{high_freq_gaps} skills appear repeatedly in job postings",
                f"{critical_gaps} skills are marked as high importance by employers"
            ],
            "recommendations_summary": [
                "Focus on high-frequency, high-importance skills first",
                "Build portfolio projects that demonstrate multiple skills",
                "Consider certifications for in-demand technologies",
                "Network with professionals in your target field"
            ]
        }
    
    def _determine_assessment(self, skill_coverage_score: float) -> Assessment:
        """
        Determine overall assessment based on coverage score.
        
        Args:
            skill_coverage_score: Skill coverage score
            
        Returns:
            Assessment level
        """
        if skill_coverage_score >= ASSESSMENT_THRESHOLDS["excellent"]:
            return Assessment.EXCELLENT
        elif skill_coverage_score >= ASSESSMENT_THRESHOLDS["good"]:
            return Assessment.GOOD
        elif skill_coverage_score >= ASSESSMENT_THRESHOLDS["fair"]:
            return Assessment.FAIR
        else:
            return Assessment.NEEDS_IMPROVEMENT
