"""Service for generating learning and project recommendations."""

from typing import Dict, List, Any, Optional

from .config import LEARNING_RESOURCES, TIME_ESTIMATES, SKILL_PREREQUISITES
from .types import (
    RepeatedGaps, TruthBank, AnalysisOptions, 
    LearningRecommendation, ProjectSuggestion, ActionItem,
    SkillInfo, Priority, Difficulty
)


class RecommendationGenerator:
    """Service for generating learning and project recommendations."""
    
    def generate_learning_recommendations(
        self,
        repeated_gaps: RepeatedGaps,
        truth_bank: TruthBank,
        options: AnalysisOptions
    ) -> List[LearningRecommendation]:
        """
        Generate learning recommendations based on skill gaps.
        
        Args:
            repeated_gaps: Analysis of repeated skill gaps
            truth_bank: User's current skills and experience
            options: Analysis configuration options
            
        Returns:
            List of learning recommendations
        """
        recommendations = []
        
        # Get top gaps for specific recommendations
        top_gaps = repeated_gaps.get("high_frequency_gaps", [])[
            :options.get("learning_recommendation_count", 8)
        ]
        
        # Generate skill-specific recommendations
        for gap in top_gaps:
            recommendation = self._create_skill_recommendation(gap, truth_bank)
            if recommendation:
                recommendations.append(recommendation)
        
        # Add general recommendations
        general_recommendations = self._create_general_recommendations()
        
        # Combine and limit to requested count
        all_recommendations = recommendations + general_recommendations
        return all_recommendations[:options.get("learning_recommendation_count", 8)]
    
    def generate_project_suggestions(
        self,
        repeated_gaps: RepeatedGaps,
        truth_bank: TruthBank,
        options: AnalysisOptions
    ) -> List[ProjectSuggestion]:
        """
        Generate portfolio project suggestions based on skill gaps.
        
        Args:
            repeated_gaps: Analysis of repeated skill gaps
            truth_bank: User's current skills and experience
            options: Analysis configuration options
            
        Returns:
            List of project suggestions
        """
        # Get top gaps for project ideas
        top_gaps = repeated_gaps.get("high_frequency_gaps", [])[
            :options.get("project_suggestion_count", 5)
        ]
        
        # Generate project ideas based on skill combinations
        project_ideas = self._generate_project_ideas(top_gaps)
        
        # Convert to project suggestions
        suggestions = []
        for idea in project_ideas:
            suggestion: ProjectSuggestion = {
                "title": idea["title"],
                "description": idea["description"],
                "skills_covered": idea["skills_covered"],
                "difficulty": idea["difficulty"],
                "time_estimate": idea["time_estimate"],
                "tech_stack": idea["tech_stack"],
                "learning_outcomes": idea["learning_outcomes"],
                "portfolio_value": idea["portfolio_value"]
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def generate_action_items(
        self,
        repeated_gaps: RepeatedGaps,
        learning_recommendations: List[LearningRecommendation],
        project_suggestions: List[ProjectSuggestion],
        options: AnalysisOptions
    ) -> List[ActionItem]:
        """
        Generate actionable recommendations.
        
        Args:
            repeated_gaps: Analysis of repeated skill gaps
            learning_recommendations: Learning recommendations
            project_suggestions: Project suggestions
            options: Analysis configuration options
            
        Returns:
            List of action items
        """
        action_items = []
        
        # High-priority skill learning actions
        critical_gaps = repeated_gaps.get("critical_gaps", [])[:5]
        
        for gap in critical_gaps:
            action_item = self._create_skill_learning_action(gap, learning_recommendations)
            action_items.append(action_item)
        
        # Project-based actions
        for project in project_suggestions[:3]:
            action_item = self._create_project_action(project)
            action_items.append(action_item)
        
        # General career development actions
        general_actions = self._create_general_actions()
        action_items.extend(general_actions)
        
        return action_items
    
    def _create_skill_recommendation(self, gap: SkillInfo, truth_bank: TruthBank) -> Optional[LearningRecommendation]:
        """
        Create a specific learning recommendation for a skill.
        
        Args:
            gap: Skill gap information
            truth_bank: User's current skills
            
        Returns:
            Learning recommendation or None if not applicable
        """
        skill = gap["skill"]
        category = gap.get("category", "technical")
        frequency = gap["frequency"]
        
        # Get learning resources
        resources = LEARNING_RESOURCES.get(category, {}).get(skill, [
            "Online tutorials", "Documentation", "Practice projects"
        ])
        
        # Get time estimate
        time_estimate = TIME_ESTIMATES.get(category, "4-6 weeks")
        
        # Determine priority
        priority = self._determine_priority(frequency)
        
        # Create learning path
        learning_path = self._create_learning_path(skill, category)
        
        # Identify prerequisites
        prerequisites = self._identify_prerequisites(skill, category, truth_bank)
        
        return {
            "type": "skill_specific",
            "skill": skill,
            "category": category,
            "title": f"Learn {skill.title()}",
            "description": f"Master {skill} to meet requirements in {frequency} job postings",
            "priority": priority,
            "time_estimate": time_estimate,
            "resources": resources[:3],  # Top 3 resources
            "learning_path": learning_path,
            "prerequisites": prerequisites
        }
    
    def _create_general_recommendations(self) -> List[LearningRecommendation]:
        """Create general learning recommendations."""
        return [
            {
                "type": "general",
                "skill": None,
                "category": None,
                "title": "Practice Projects",
                "description": "Build projects that combine multiple missing skills to gain practical experience",
                "priority": Priority.HIGH,
                "time_estimate": "2-4 weeks",
                "resources": ["GitHub", "Portfolio platforms", "Open source contributions"],
                "learning_path": [
                    "Identify skill gaps to address",
                    "Design project architecture",
                    "Implement core features",
                    "Add portfolio documentation"
                ],
                "prerequisites": []
            },
            {
                "type": "general",
                "skill": None,
                "category": None,
                "title": "Certification Preparation",
                "description": "Consider industry certifications to validate your skills",
                "priority": Priority.MEDIUM,
                "time_estimate": "4-8 weeks",
                "resources": ["Coursera", "Udemy", "edX", "Official certification programs"],
                "learning_path": [
                    "Choose relevant certification",
                    "Study official materials",
                    "Practice with sample questions",
                    "Schedule and take exam"
                ],
                "prerequisites": []
            },
            {
                "type": "general",
                "skill": None,
                "category": None,
                "title": "Networking and Community",
                "description": "Join professional communities and attend meetups to learn from others",
                "priority": Priority.MEDIUM,
                "time_estimate": "Ongoing",
                "resources": ["Meetup.com", "LinkedIn groups", "Professional associations"],
                "learning_path": [
                    "Identify relevant communities",
                    "Attend events and meetings",
                    "Contribute to discussions",
                    "Build professional relationships"
                ],
                "prerequisites": []
            }
        ]
    
    def _generate_project_ideas(self, top_gaps: List[SkillInfo]) -> List[Dict[str, Any]]:
        """
        Generate specific project ideas based on skill gaps.
        
        Args:
            top_gaps: Top skill gaps to address
            
        Returns:
            List of project ideas
        """
        project_ideas = []
        
        # Extract missing skills
        missing_skills = [gap["skill"] for gap in top_gaps]
        
        # Web application project
        web_skills = self._find_skills_in_category(missing_skills, [
            "react", "vue", "angular", "node.js", "django", "flask", "next.js"
        ])
        if web_skills:
            project_ideas.append({
                "title": "Full-Stack Web Application",
                "description": f"Build a complete web application using {', '.join(web_skills[:2])}",
                "skills_covered": web_skills[:2],
                "difficulty": Difficulty.INTERMEDIATE,
                "time_estimate": "4-6 weeks",
                "tech_stack": web_skills[:2] + ["HTML", "CSS", "JavaScript"],
                "learning_outcomes": ["Full-stack development", "API design", "Database integration"],
                "portfolio_value": "high"
            })
        
        # Data project
        data_skills = self._find_skills_in_category(missing_skills, [
            "python", "sql", "pandas", "numpy", "tableau", "powerbi"
        ])
        if data_skills:
            project_ideas.append({
                "title": "Data Analytics Dashboard",
                "description": f"Create an interactive dashboard using {', '.join(data_skills[:2])}",
                "skills_covered": data_skills[:2],
                "difficulty": Difficulty.INTERMEDIATE,
                "time_estimate": "3-4 weeks",
                "tech_stack": data_skills[:2] + ["Data visualization", "Statistics"],
                "learning_outcomes": ["Data analysis", "Visualization", "Business intelligence"],
                "portfolio_value": "high"
            })
        
        # Cloud project
        cloud_skills = self._find_skills_in_category(missing_skills, [
            "aws", "docker", "kubernetes", "azure", "gcp"
        ])
        if cloud_skills:
            project_ideas.append({
                "title": "Cloud Deployment Project",
                "description": f"Deploy and manage applications using {', '.join(cloud_skills[:2])}",
                "skills_covered": cloud_skills[:2],
                "difficulty": Difficulty.ADVANCED,
                "time_estimate": "4-5 weeks",
                "tech_stack": cloud_skills[:2] + ["CI/CD", "Monitoring", "Security"],
                "learning_outcomes": ["Cloud architecture", "DevOps practices", "Infrastructure as code"],
                "portfolio_value": "very_high"
            })
        
        # Mobile project
        mobile_skills = self._find_skills_in_category(missing_skills, [
            "react-native", "flutter", "swift", "kotlin", "ios", "android"
        ])
        if mobile_skills:
            project_ideas.append({
                "title": "Mobile Application",
                "description": f"Develop a mobile app using {', '.join(mobile_skills[:2])}",
                "skills_covered": mobile_skills[:2],
                "difficulty": Difficulty.INTERMEDIATE,
                "time_estimate": "5-7 weeks",
                "tech_stack": mobile_skills[:2] + ["Mobile UI/UX", "API integration"],
                "learning_outcomes": ["Mobile development", "Platform-specific best practices", "App deployment"],
                "portfolio_value": "high"
            })
        
        # Machine learning project
        ml_skills = self._find_skills_in_category(missing_skills, [
            "python", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy"
        ])
        if ml_skills:
            project_ideas.append({
                "title": "Machine Learning Application",
                "description": f"Build an ML model using {', '.join(ml_skills[:2])}",
                "skills_covered": ml_skills[:2],
                "difficulty": Difficulty.ADVANCED,
                "time_estimate": "6-8 weeks",
                "tech_stack": ml_skills[:2] + ["Data preprocessing", "Model evaluation", "Deployment"],
                "learning_outcomes": ["Machine learning", "Data science", "Model deployment"],
                "portfolio_value": "very_high"
            })
        
        # Add a general project if no specific ones were generated
        if not project_ideas and missing_skills:
            project_ideas.append({
                "title": "Portfolio Showcase Project",
                "description": f"Create a project that demonstrates your skills in {', '.join(missing_skills[:2])}",
                "skills_covered": missing_skills[:2],
                "difficulty": Difficulty.INTERMEDIATE,
                "time_estimate": "4-6 weeks",
                "tech_stack": missing_skills[:2] + ["Version control", "Testing", "Documentation"],
                "learning_outcomes": ["Project management", "Code organization", "Best practices"],
                "portfolio_value": "medium"
            })
        
        return project_ideas
    
    def _create_skill_learning_action(
        self, 
        gap: SkillInfo, 
        learning_recommendations: List[LearningRecommendation]
    ) -> ActionItem:
        """
        Create an action item for skill learning.
        
        Args:
            gap: Skill gap information
            learning_recommendations: Available learning recommendations
            
        Returns:
            Action item for skill learning
        """
        # Find relevant learning resources
        resources = [
            rec["title"] for rec in learning_recommendations 
            if rec["skill"] == gap["skill"]
        ]
        
        return {
            "type": "skill_learning",
            "priority": Priority.HIGH,
            "title": f"Learn {gap['skill'].title()}",
            "description": f"This skill appears in {gap['frequency']} job postings and is marked as high importance",
            "timeline": "4-8 weeks",
            "resources": resources[:3],  # Top 3 resources
            "success_metrics": [
                f"Complete {gap['skill']} course",
                f"Build project using {gap['skill']}",
                f"Add {gap['skill']} to resume"
            ]
        }
    
    def _create_project_action(self, project: ProjectSuggestion) -> ActionItem:
        """
        Create an action item for project work.
        
        Args:
            project: Project suggestion
            
        Returns:
            Action item for project work
        """
        return {
            "type": "project_work",
            "priority": Priority.MEDIUM,
            "title": f"Build {project['title']}",
            "description": project["description"],
            "timeline": project["time_estimate"],
            "resources": project["tech_stack"],
            "success_metrics": [
                "Complete project",
                "Deploy to production",
                "Add to portfolio",
                "Write documentation"
            ]
        }
    
    def _create_general_actions(self) -> List[ActionItem]:
        """Create general career development actions."""
        return [
            {
                "type": "networking",
                "priority": Priority.MEDIUM,
                "title": "Expand Professional Network",
                "description": "Connect with professionals in your target industry",
                "timeline": "ongoing",
                "resources": ["LinkedIn", "Industry meetups", "Professional associations"],
                "success_metrics": [
                    "10 new connections",
                    "3 informational interviews",
                    "Join 2 professional groups"
                ]
            },
            {
                "type": "certification",
                "priority": Priority.LOW,
                "title": "Obtain Relevant Certifications",
                "description": "Get certified in high-demand skills",
                "timeline": "3-6 months",
                "resources": [
                    "AWS/Azure/GCP certifications",
                    "Google Cloud certifications",
                    "Industry-specific certs"
                ],
                "success_metrics": [
                    "Pass certification exam",
                    "Add certification to resume",
                    "Update LinkedIn profile"
                ]
            }
        ]
    
    def _determine_priority(self, frequency: int) -> Priority:
        """Determine priority based on frequency."""
        if frequency >= 5:
            return Priority.HIGH
        elif frequency >= 3:
            return Priority.MEDIUM
        else:
            return Priority.LOW
    
    def _create_learning_path(self, skill: str, category: str) -> List[str]:
        """Create a learning path for a skill."""
        learning_paths = {
            "languages": [
                f"Learn {skill} fundamentals and syntax",
                f"Practice with basic {skill} exercises",
                f"Build a small project using {skill}",
                f"Learn advanced {skill} concepts and best practices"
            ],
            "frameworks": [
                f"Understand {skill} architecture and concepts",
                f"Learn {skill} setup and configuration",
                f"Build a complete application with {skill}",
                f"Master {skill} advanced features and optimization"
            ],
            "databases": [
                f"Learn {skill} fundamentals and data modeling",
                f"Practice {skill} queries and operations",
                f"Design and implement {skill} schemas",
                f"Learn {skill} optimization and administration"
            ],
            "platforms": [
                f"Understand {skill} core concepts and services",
                f"Set up {skill} development environment",
                f"Deploy applications using {skill}",
                f"Master {skill} advanced features and best practices"
            ]
        }
        
        return learning_paths.get(category, [
            f"Learn {skill} basics",
            f"Practice {skill} fundamentals",
            f"Build projects with {skill}",
            f"Master advanced {skill} concepts"
        ])
    
    def _identify_prerequisites(self, skill: str, category: str, truth_bank: TruthBank) -> List[str]:
        """Identify prerequisites for learning a skill."""
        # Get prerequisites for this skill
        skill_prereqs = SKILL_PREREQUISITES.get(skill.lower(), [])
        
        # Get user's current skills
        user_skills = set()
        for skill_category in truth_bank["skills"]:
            user_skills.update(truth_bank["skills"][skill_category])
        
        # Filter prerequisites that user doesn't have
        missing_prereqs = [
            prereq for prereq in skill_prereqs 
            if prereq.lower() not in user_skills
        ]
        
        return missing_prereqs[:3]  # Return top 3 missing prerequisites
    
    def _find_skills_in_category(self, missing_skills: List[str], target_skills: List[str]) -> List[str]:
        """Find skills from missing skills that match target skills."""
        return [
            skill for skill in missing_skills 
            if skill.lower() in [target.lower() for target in target_skills]
        ]
