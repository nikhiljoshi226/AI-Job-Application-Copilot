from typing import Dict, List, Any, Optional, Tuple
import copy
import time
from datetime import datetime

from app.services.tailoring_suggester import TailoringSuggester


class TailoredResumeBuilder:
    """
    Service to build the final tailored resume by merging original resume
    with user-approved edits and suggestions.
    """

    def __init__(self):
        self.suggester = TailoringSuggester()

    def build_tailored_resume(
        self,
        original_resume: Dict[str, Any],
        approved_suggestions: Dict[str, List[Dict[str, Any]]],
        truth_bank: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Build the final tailored resume by applying approved suggestions
        to the original resume.
        
        Args:
            original_resume: Original parsed resume JSON
            approved_suggestions: User-approved suggestions organized by section
            truth_bank: Truth bank for validation
            
        Returns:
            Complete tailored resume JSON with metadata
        """
        start_time = time.time()
        
        # Create a deep copy of the original resume
        tailored_resume = copy.deepcopy(original_resume)
        
        # Track applied changes for audit trail
        applied_changes = []
        
        # Apply approved suggestions by section
        for section, suggestions in approved_suggestions.items():
            if section in tailored_resume and suggestions:
                section_changes = self._apply_section_suggestions(
                    tailored_resume[section],
                    suggestions,
                    section
                )
                applied_changes.extend(section_changes)
        
        # Calculate final metrics
        processing_time = int((time.time() - start_time) * 1000)
        truthfulness_score = self._calculate_final_truthfulness(applied_changes, truth_bank)
        
        # Build final result
        result = {
            "tailored_resume": tailored_resume,
            "metadata": {
                "original_resume_id": original_resume.get("id"),
                "total_suggestions_applied": len(applied_changes),
                "processing_time_ms": processing_time,
                "truthfulness_score": truthfulness_score,
                "generated_at": datetime.utcnow().isoformat(),
                "version": 1
            },
            "applied_changes": applied_changes,
            "change_summary": self._generate_change_summary(applied_changes)
        }
        
        return result

    def _apply_section_suggestions(
        self,
        section_data: Any,
        suggestions: List[Dict[str, Any]],
        section_name: str
    ) -> List[Dict[str, Any]]:
        """
        Apply approved suggestions to a specific section.
        
        Args:
            section_data: Original section data
            suggestions: Approved suggestions for this section
            section_name: Name of the section
            
        Returns:
            List of applied changes for audit trail
        """
        applied_changes = []
        
        # Filter only approved suggestions
        approved_suggestions = [s for s in suggestions if s.get('approved', False)]
        
        for suggestion in approved_suggestions:
            change = self._apply_single_suggestion(section_data, suggestion, section_name)
            if change:
                applied_changes.append(change)
        
        return applied_changes

    def _apply_single_suggestion(
        self,
        section_data: Any,
        suggestion: Dict[str, Any],
        section_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Apply a single suggestion to the section data.
        
        Args:
            section_data: Section data to modify
            suggestion: Individual suggestion to apply
            section_name: Name of the section
            
        Returns:
            Applied change record or None if not applicable
        """
        suggestion_type = suggestion.get('type')
        
        try:
            if suggestion_type == 'enhancement':
                return self._apply_enhancement(section_data, suggestion, section_name)
            elif suggestion_type == 'addition':
                return self._apply_addition(section_data, suggestion, section_name)
            elif suggestion_type == 'bullet_enhancement':
                return self._apply_bullet_enhancement(section_data, suggestion, section_name)
            elif suggestion_type == 'description_enhancement':
                return self._apply_description_enhancement(section_data, suggestion, section_name)
            else:
                print(f"Unknown suggestion type: {suggestion_type}")
                return None
        except Exception as e:
            print(f"Error applying suggestion: {e}")
            return None

    def _apply_enhancement(
        self,
        section_data: Any,
        suggestion: Dict[str, Any],
        section_name: str
    ) -> Dict[str, Any]:
        """Apply text enhancement suggestions."""
        current_text = suggestion.get('current_text', '')
        suggested_text = suggestion.get('user_edits') or suggestion.get('suggested_text', '')
        
        # Apply the enhancement
        if isinstance(section_data, str):
            # Simple string replacement
            if section_data == current_text:
                section_data = suggested_text
            else:
                # Partial replacement within text
                section_data = section_data.replace(current_text, suggested_text)
        elif isinstance(section_data, dict):
            # Handle dict structures
            if 'summary' in section_data and section_data['summary'] == current_text:
                section_data['summary'] = suggested_text
        
        return {
            "type": "enhancement",
            "section": section_name,
            "original": current_text,
            "modified": suggested_text,
            "suggestion_id": suggestion.get('id'),
            "truthfulness_score": suggestion.get('truthfulness_score', 0.0)
        }

    def _apply_addition(
        self,
        section_data: Any,
        suggestion: Dict[str, Any],
        section_name: str
    ) -> Dict[str, Any]:
        """Apply addition suggestions (adding new items)."""
        addition = suggestion.get('user_edits') or suggestion.get('suggested_addition', '')
        skill_name = suggestion.get('skill_name', '')
        category = suggestion.get('category', 'technical')
        
        if section_name == 'skills' and isinstance(section_data, dict):
            # Add new skill
            if 'technical' not in section_data:
                section_data['technical'] = []
            if 'soft_skills' not in section_data:
                section_data['soft_skills'] = []
            
            new_skill = {
                "name": skill_name or addition,
                "category": category,
                "added_via_tailoring": True,
                "evidence_source": suggestion.get('evidence', {}).get('source', 'user_approval'),
                "truthfulness_score": suggestion.get('truthfulness_score', 0.0)
            }
            
            if category == 'technical':
                section_data['technical'].append(new_skill)
            else:
                section_data['soft_skills'].append(new_skill)
        
        return {
            "type": "addition",
            "section": section_name,
            "added": addition,
            "skill_name": skill_name,
            "category": category,
            "suggestion_id": suggestion.get('id'),
            "truthfulness_score": suggestion.get('truthfulness_score', 0.0)
        }

    def _apply_bullet_enhancement(
        self,
        section_data: Any,
        suggestion: Dict[str, Any],
        section_name: str
    ) -> Dict[str, Any]:
        """Apply bullet point enhancements for experience sections."""
        current_bullet = suggestion.get('current_bullet', '')
        suggested_bullet = suggestion.get('user_edits') or suggestion.get('suggested_bullet', '')
        
        if section_name == 'experience' and isinstance(section_data, list):
            # Find and replace bullet in experience entries
            for exp_entry in section_data:
                if isinstance(exp_entry, dict) and 'description' in exp_entry:
                    if exp_entry['description'] == current_bullet:
                        exp_entry['description'] = suggested_bullet
                        break
                elif isinstance(exp_entry, dict) and 'achievements' in exp_entry:
                    # Check in achievements list
                    for i, achievement in enumerate(exp_entry['achievements']):
                        if achievement == current_bullet:
                            exp_entry['achievements'][i] = suggested_bullet
                            break
        
        return {
            "type": "bullet_enhancement",
            "section": section_name,
            "original_bullet": current_bullet,
            "modified_bullet": suggested_bullet,
            "suggestion_id": suggestion.get('id'),
            "truthfulness_score": suggestion.get('truthfulness_score', 0.0)
        }

    def _apply_description_enhancement(
        self,
        section_data: Any,
        suggestion: Dict[str, Any],
        section_name: str
    ) -> Dict[str, Any]:
        """Apply description enhancements for project sections."""
        current_text = suggestion.get('current_text', '')
        suggested_text = suggestion.get('user_edits') or suggestion.get('suggested_text', '')
        
        if section_name == 'projects' and isinstance(section_data, list):
            # Find and replace project description
            for project in section_data:
                if isinstance(project, dict) and 'description' in project:
                    if project['description'] == current_text:
                        project['description'] = suggested_text
                        break
        
        return {
            "type": "description_enhancement",
            "section": section_name,
            "original_description": current_text,
            "modified_description": suggested_text,
            "suggestion_id": suggestion.get('id'),
            "truthfulness_score": suggestion.get('truthfulness_score', 0.0)
        }

    def _calculate_final_truthfulness(
        self,
        applied_changes: List[Dict[str, Any]],
        truth_bank: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        Calculate the final truthfulness score based on applied changes.
        
        Args:
            applied_changes: List of applied changes
            truth_bank: Truth bank for validation
            
        Returns:
            Final truthfulness score (0.0 to 1.0)
        """
        if not applied_changes:
            return 1.0  # No changes means original truthfulness
        
        # Calculate weighted average of truthfulness scores
        total_weight = 0
        weighted_score = 0
        
        for change in applied_changes:
            truthfulness = change.get('truthfulness_score', 0.0)
            weight = 1.0  # Equal weight for all changes
            
            weighted_score += truthfulness * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        base_score = weighted_score / total_weight
        
        # Apply penalty for low-confidence additions
        addition_count = len([c for c in applied_changes if c['type'] == 'addition'])
        if addition_count > 0:
            addition_penalty = min(0.1 * addition_count, 0.3)  # Max 30% penalty
            base_score = max(0.0, base_score - addition_penalty)
        
        return round(base_score, 3)

    def _generate_change_summary(self, applied_changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a summary of all applied changes.
        
        Args:
            applied_changes: List of applied changes
            
        Returns:
            Change summary statistics
        """
        summary = {
            "total_changes": len(applied_changes),
            "changes_by_type": {},
            "changes_by_section": {},
            "average_truthfulness": 0.0,
            "high_confidence_changes": 0,
            "medium_confidence_changes": 0,
            "low_confidence_changes": 0
        }
        
        if not applied_changes:
            return summary
        
        # Count changes by type and section
        for change in applied_changes:
            change_type = change.get('type', 'unknown')
            section = change.get('section', 'unknown')
            truthfulness = change.get('truthfulness_score', 0.0)
            
            # Count by type
            if change_type not in summary["changes_by_type"]:
                summary["changes_by_type"][change_type] = 0
            summary["changes_by_type"][change_type] += 1
            
            # Count by section
            if section not in summary["changes_by_section"]:
                summary["changes_by_section"][section] = 0
            summary["changes_by_section"][section] += 1
            
            # Count by confidence level
            if truthfulness >= 0.8:
                summary["high_confidence_changes"] += 1
            elif truthfulness >= 0.6:
                summary["medium_confidence_changes"] += 1
            else:
                summary["low_confidence_changes"] += 1
        
        # Calculate average truthfulness
        total_truthfulness = sum(change.get('truthfulness_score', 0.0) for change in applied_changes)
        summary["average_truthfulness"] = round(total_truthfulness / len(applied_changes), 3)
        
        return summary

    def validate_tailored_resume(
        self,
        tailored_resume: Dict[str, Any],
        original_resume: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        Validate the tailored resume against the original.
        
        Args:
            tailored_resume: The generated tailored resume
            original_resume: The original resume
            
        Returns:
            Tuple of (is_valid, list_of_validation_errors)
        """
        errors = []
        
        # Check required sections
        required_sections = ['summary', 'skills', 'experience', 'metadata']
        for section in required_sections:
            if section not in original_resume:
                errors.append(f"Missing required section in original resume: {section}")
            if section not in tailored_resume:
                errors.append(f"Missing required section in tailored resume: {section}")
        
        # Validate experience structure
        if 'experience' in tailored_resume:
            if not isinstance(tailored_resume['experience'], list):
                errors.append("Experience section must be a list")
            else:
                for i, exp in enumerate(tailored_resume['experience']):
                    if not isinstance(exp, dict):
                        errors.append(f"Experience entry {i} must be a dictionary")
                    else:
                        required_exp_fields = ['title', 'company', 'start_date']
                        for field in required_exp_fields:
                            if field not in exp:
                                errors.append(f"Experience entry {i} missing required field: {field}")
        
        # Validate skills structure
        if 'skills' in tailored_resume:
            if not isinstance(tailored_resume['skills'], dict):
                errors.append("Skills section must be a dictionary")
            else:
                if 'technical' in tailored_resume['skills']:
                    if not isinstance(tailored_resume['skills']['technical'], list):
                        errors.append("Technical skills must be a list")
                if 'soft_skills' in tailored_resume['skills']:
                    if not isinstance(tailored_resume['skills']['soft_skills'], list):
                        errors.append("Soft skills must be a list")
        
        # Check for reasonable truthfulness score
        metadata = tailored_resume.get('metadata', {})
        truthfulness_score = metadata.get('truthfulness_score', 0.0)
        if truthfulness_score < 0.3:
            errors.append("Truthfulness score is too low (< 30%)")
        
        return len(errors) == 0, errors

    def prepare_for_rendering(self, tailored_resume: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare the tailored resume for document rendering.
        
        Args:
            tailored_resume: The tailored resume
            
        Returns:
            Resume data formatted for rendering
        """
        rendering_data = {
            "header": {
                "name": tailored_resume.get("personal_info", {}).get("name", ""),
                "contact": {
                    "email": tailored_resume.get("personal_info", {}).get("email", ""),
                    "phone": tailored_resume.get("personal_info", {}).get("phone", ""),
                    "location": tailored_resume.get("personal_info", {}).get("location", ""),
                    "linkedin": tailored_resume.get("personal_info", {}).get("linkedin", ""),
                    "github": tailored_resume.get("personal_info", {}).get("github", "")
                }
            },
            "summary": tailored_resume.get("summary", ""),
            "skills": {
                "technical": tailored_resume.get("skills", {}).get("technical", []),
                "soft_skills": tailored_resume.get("skills", {}).get("soft_skills", [])
            },
            "experience": tailored_resume.get("experience", []),
            "education": tailored_resume.get("education", []),
            "projects": tailored_resume.get("projects", []),
            "certifications": tailored_resume.get("certifications", []),
            "languages": tailored_resume.get("languages", []),
            "metadata": tailored_resume.get("metadata", {})
        }
        
        return rendering_data
