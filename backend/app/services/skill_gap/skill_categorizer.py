"""Service for categorizing and processing skills."""

from typing import Dict, List, Set
from collections import defaultdict

from .config import SKILL_CATEGORIES
from .types import SkillCategory


class SkillCategorizer:
    """Service for categorizing skills into appropriate categories."""
    
    def __init__(self):
        # Pre-compute skill lookup for better performance
        self._skill_lookup = self._build_skill_lookup()
    
    def _build_skill_lookup(self) -> Dict[str, str]:
        """Build a lookup dictionary for quick skill categorization."""
        lookup = {}
        
        for category, skills in SKILL_CATEGORIES.items():
            for skill in skills:
                lookup[skill.lower()] = category
        
        return lookup
    
    def categorize_skill(self, skill: str) -> SkillCategory:
        """
        Categorize a skill into appropriate category.
        
        Args:
            skill: The skill name to categorize
            
        Returns:
            The skill category
        """
        skill_lower = skill.lower()
        
        # Check against precomputed lookup first
        if skill_lower in self._skill_lookup:
            category = self._skill_lookup[skill_lower]
            return self._map_category_to_enum(category)
        
        # Fallback to pattern-based categorization
        return self._categorize_by_patterns(skill_lower)
    
    def _map_category_to_enum(self, category: str) -> SkillCategory:
        """Map string category to enum value."""
        mapping = {
            "programming_languages": SkillCategory.LANGUAGES,
            "web_technologies": SkillCategory.FRAMEWORKS,
            "databases": SkillCategory.DATABASES,
            "cloud_platforms": SkillCategory.PLATFORMS,
            "devops_tools": SkillCategory.TOOLS,
            "soft_skills": SkillCategory.SOFT_SKILLS,
            "business_skills": SkillCategory.SOFT_SKILLS,
            "mobile_development": SkillCategory.FRAMEWORKS,
            "data_analytics": SkillCategory.TOOLS,
            "machine_learning": SkillCategory.FRAMEWORKS
        }
        return mapping.get(category, SkillCategory.TECHNICAL)
    
    def _categorize_by_patterns(self, skill: str) -> SkillCategory:
        """Categorize skill based on common patterns."""
        
        # Programming languages pattern
        if any(word in skill for word in [
            "python", "java", "javascript", "c++", "c#", "go", "rust", 
            "typescript", "scala", "dart", "php", "ruby"
        ]):
            return SkillCategory.LANGUAGES
        
        # Frameworks pattern
        if any(word in skill for word in [
            "react", "vue", "angular", "django", "flask", "spring", 
            "laravel", "next.js", "nuxt.js", "svelte", "express"
        ]):
            return SkillCategory.FRAMEWORKS
        
        # Databases pattern
        if any(word in skill for word in [
            "mysql", "postgresql", "mongodb", "redis", "sqlite", 
            "oracle", "cassandra", "dynamodb", "neo4j"
        ]):
            return SkillCategory.DATABASES
        
        # Platforms pattern
        if any(word in skill for word in [
            "aws", "azure", "gcp", "docker", "kubernetes", "heroku", 
            "vercel", "netlify", "firebase", "cloudflare"
        ]):
            return SkillCategory.PLATFORMS
        
        # Tools pattern
        if any(word in skill for word in [
            "git", "jenkins", "gitlab", "github", "terraform", "ansible", 
            "circleci", "travis", "bamboo", "tableau", "powerbi"
        ]):
            return SkillCategory.TOOLS
        
        # Soft skills pattern
        if any(word in skill for word in [
            "communication", "leadership", "teamwork", "problem", 
            "critical", "creative", "collaboration", "management"
        ]):
            return SkillCategory.SOFT_SKILLS
        
        # Default to technical
        return SkillCategory.TECHNICAL
    
    def find_technologies_in_text(self, text: str) -> List[str]:
        """
        Find technology mentions in text.
        
        Args:
            text: The text to search for technologies
            
        Returns:
            List of technologies found in the text
        """
        technologies = set()
        text_lower = text.lower()
        
        # Search for all known technologies
        for category_skills in SKILL_CATEGORIES.values():
            for tech in category_skills:
                if tech.lower() in text_lower:
                    technologies.add(tech.lower())
        
        return list(technologies)
    
    def categorize_multiple_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """
        Categorize multiple skills at once.
        
        Args:
            skills: List of skill names to categorize
            
        Returns:
            Dictionary mapping categories to lists of skills
        """
        categorized = defaultdict(list)
        
        for skill in skills:
            category = self.categorize_skill(skill)
            categorized[category.value].append(skill)
        
        return dict(categorized)
