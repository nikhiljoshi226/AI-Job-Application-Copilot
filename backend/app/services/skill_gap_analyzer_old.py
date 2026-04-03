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
        
        Args:
            resume_data: Resume data with rendering content
            job_descriptions: List of job description data
            analysis_options: Options for analysis
            
        Returns:
            Comprehensive skill gap analysis with recommendations
        """
        start_time = time.time()
        
        # Set default analysis options
        options = {
            "include_soft_skills": True,
            "include_technical_skills": True,
            "min_gap_frequency": 2,  # Minimum frequency for repeated gaps
            "project_suggestion_count": 5,
            "learning_recommendation_count": 8,
            "priority_threshold": 0.3  # Minimum importance for recommendations
        }
        if analysis_options:
            options.update(analysis_options)
        
        # Create truth bank from resume
        truth_bank = self._create_truth_bank_from_resume(resume_data)
        
        # Extract skills from all job descriptions
        all_jd_skills = self._extract_skills_from_job_descriptions(job_descriptions)
        
        # Analyze skill gaps
        skill_gaps = self._analyze_skill_gaps(truth_bank, all_jd_skills, options)
        
        # Identify repeated gaps across jobs
        repeated_gaps = self._identify_repeated_gaps(skill_gaps, options)
        
        # Analyze role expectations
        role_expectations = self._analyze_role_expectations(job_descriptions)
        
        # Generate learning recommendations
        learning_recommendations = self._generate_learning_recommendations(
            repeated_gaps, truth_bank, options
        )
        
        # Generate project suggestions
        project_suggestions = self._generate_project_suggestions(
            repeated_gaps, truth_bank, options
        )
        
        # Calculate skill coverage score
        skill_coverage_score = self._calculate_skill_coverage_score(truth_bank, all_jd_skills)
        
        # Generate action items
        action_items = self._generate_action_items(
            repeated_gaps, learning_recommendations, project_suggestions, options
        )
        
        # Create analysis summary
        analysis_summary = self._create_analysis_summary(
            skill_gaps, repeated_gaps, role_expectations, skill_coverage_score
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Build result
        result = {
            "skill_gap_analysis": {
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
            },
            "metadata": {
                "processing_time_ms": processing_time,
                "analysis_options": options,
                "generated_at": datetime.utcnow().isoformat()
            }
        }
        
        return result

    def _create_truth_bank_from_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a truth bank from resume data."""
        truth_bank = {
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
        
        # Extract skills from resume
        resume_content = resume_data.get("rendering_data", {})
        
        # Skills section
        skills_categories = resume_content.get("skills", {}).get("categories", [])
        for category in skills_categories:
            category_name = category.get("name", "").lower()
            skills = category.get("skills", [])
            
            for skill in skills:
                skill_name = skill.get("name", "").lower()
                if skill_name:
                    if "technical" in category_name or "programming" in category_name:
                        truth_bank["skills"]["technical"].add(skill_name)
                    elif "soft" in category_name or "interpersonal" in category_name:
                        truth_bank["skills"]["soft_skills"].add(skill_name)
                    elif "tool" in category_name or "software" in category_name:
                        truth_bank["skills"]["tools"].add(skill_name)
                    elif "language" in category_name:
                        truth_bank["skills"]["languages"].add(skill_name)
                    elif "framework" in category_name:
                        truth_bank["skills"]["frameworks"].add(skill_name)
                    elif "database" in category_name:
                        truth_bank["skills"]["databases"].add(skill_name)
                    elif "platform" in category_name or "cloud" in category_name:
                        truth_bank["skills"]["platforms"].add(skill_name)
                    else:
                        truth_bank["skills"]["technical"].add(skill_name)  # Default to technical
        
        # Experience section
        experience_entries = resume_content.get("experience", {}).get("entries", [])
        for entry in experience_entries:
            if entry.get("company"):
                truth_bank["experience"]["companies"].add(entry["company"].lower())
            if entry.get("title"):
                truth_bank["experience"]["titles"].add(entry["title"].lower())
            if entry.get("technologies"):
                for tech in entry["technologies"]:
                    truth_bank["skills"]["technical"].add(tech.lower())
        
        # Education section
        education_entries = resume_content.get("education", {}).get("entries", [])
        for entry in education_entries:
            if entry.get("degree"):
                truth_bank["education"]["degrees"].add(entry["degree"].lower())
            if entry.get("major"):
                truth_bank["education"]["majors"].add(entry["major"].lower())
            if entry.get("university"):
                truth_bank["education"]["universities"].add(entry["university"].lower())
        
        # Projects section
        project_entries = resume_content.get("projects", {}).get("entries", [])
        for entry in project_entries:
            if entry.get("technologies"):
                for tech in entry["technologies"]:
                    truth_bank["skills"]["technical"].add(tech.lower())
            if entry.get("description"):
                # Extract technologies from description
                desc = entry["description"].lower()
                for tech in self._find_technologies_in_text(desc):
                    truth_bank["skills"]["technical"].add(tech)
        
        # Convert sets to lists for easier processing
        for category in truth_bank["skills"]:
            truth_bank["skills"][category] = list(truth_bank["skills"][category])
        
        for category in truth_bank:
            if isinstance(truth_bank[category], dict):
                for subcategory in truth_bank[category]:
                    if isinstance(truth_bank[category][subcategory], set):
                        truth_bank[category][subcategory] = list(truth_bank[category][subcategory])
        
        return truth_bank

    def _extract_skills_from_job_descriptions(self, job_descriptions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract and categorize skills from multiple job descriptions."""
        all_skills = {
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
        
        for i, jd in enumerate(job_descriptions):
            jd_id = f"jd_{i+1}"
            parsed_content = jd.get("parsed_content", {})
            
            # Extract required skills
            required_skills = parsed_content.get("required_skills", [])
            for skill_info in required_skills:
                skill_name = skill_info.get("skill", "").lower()
                if skill_name:
                    category = self._categorize_skill(skill_name)
                    all_skills[category][skill_name].append({
                        "jd_id": jd_id,
                        "company": jd.get("company", ""),
                        "job_title": jd.get("job_title", ""),
                        "experience_level": skill_info.get("experience_level", ""),
                        "importance": skill_info.get("importance", "medium")
                    })
            
            # Extract skills from responsibilities
            responsibilities = parsed_content.get("responsibilities", [])
            for responsibility in responsibilities:
                skills_in_text = self._find_technologies_in_text(responsibility.lower())
                for skill in skills_in_text:
                    category = self._categorize_skill(skill)
                    if skill not in all_skills[category]:
                        all_skills[category][skill].append({
                            "jd_id": jd_id,
                            "company": jd.get("company", ""),
                            "job_title": jd.get("job_title", ""),
                            "source": "responsibilities",
                            "importance": "medium"
                        })
            
            # Extract skills from raw text
            raw_text = jd.get("raw_text", "").lower()
            skills_in_text = self._find_technologies_in_text(raw_text)
            for skill in skills_in_text:
                category = self._categorize_skill(skill)
                if skill not in all_skills[category]:
                    all_skills[category][skill].append({
                        "jd_id": jd_id,
                        "company": jd.get("company", ""),
                        "job_title": jd.get("job_title", ""),
                        "source": "raw_text",
                        "importance": "low"
                    })
        
        return all_skills

    def _categorize_skill(self, skill: str) -> str:
        """Categorize a skill into appropriate category."""
        skill_lower = skill.lower()
        
        # Check against predefined categories
        for category, skills in self.skill_categories.items():
            if any(s in skill_lower for s in skills):
                if category == "programming_languages":
                    return "languages"
                elif category == "web_technologies":
                    return "frameworks"
                elif category == "databases":
                    return "databases"
                elif category == "cloud_platforms":
                    return "platforms"
                elif category == "devops_tools":
                    return "tools"
                elif category == "soft_skills":
                    return "soft_skills"
                else:
                    return category.replace("_", "")
        
        # Default categorization based on common patterns
        if any(word in skill_lower for word in ["python", "java", "javascript", "c++", "c#", "go", "rust"]):
            return "languages"
        elif any(word in skill_lower for word in ["react", "vue", "angular", "django", "flask", "spring"]):
            return "frameworks"
        elif any(word in skill_lower for word in ["mysql", "postgresql", "mongodb", "redis"]):
            return "databases"
        elif any(word in skill_lower for word in ["aws", "azure", "gcp", "docker", "kubernetes"]):
            return "platforms"
        elif any(word in skill_lower for word in ["communication", "leadership", "teamwork", "problem"]):
            return "soft_skills"
        else:
            return "technical"

    def _find_technologies_in_text(self, text: str) -> List[str]:
        """Find technology mentions in text."""
        technologies = []
        
        # Combine all known technologies
        all_technologies = []
        for category_skills in self.skill_categories.values():
            all_technologies.extend(category_skills)
        
        # Find mentions in text
        for tech in all_technologies:
            if tech.lower() in text:
                technologies.append(tech.lower())
        
        return list(set(technologies))

    def _analyze_skill_gaps(
        self,
        truth_bank: Dict[str, Any],
        all_jd_skills: Dict[str, Any],
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze skill gaps between resume and job descriptions."""
        skill_gaps = {
            "missing_technical": [],
            "missing_soft_skills": [],
            "missing_tools": [],
            "missing_languages": [],
            "missing_frameworks": [],
            "missing_databases": [],
            "missing_platforms": [],
            "gap_summary": {}
        }
        
        # Analyze each category
        for category in ["technical", "soft_skills", "tools", "languages", "frameworks", "databases", "platforms"]:
            user_skills = set(truth_bank["skills"].get(category, []))
            required_skills = all_jd_skills.get(category, {})
            
            missing_skills = []
            for skill, occurrences in required_skills.items():
                if skill not in user_skills:
                    # Calculate importance based on frequency and stated importance
                    frequency = len(occurrences)
                    importance_scores = [occ.get("importance", "medium") for occ in occurrences]
                    high_importance = sum(1 for score in importance_scores if score == "high")
                    
                    missing_skills.append({
                        "skill": skill,
                        "frequency": frequency,
                        "importance": high_importance,
                        "jobs": [occ["jd_id"] for occ in occurrences],
                        "companies": list(set([occ["company"] for occ in occurrences])),
                        "priority_score": self._calculate_skill_priority(frequency, high_importance)
                    })
            
            # Sort by priority score
            missing_skills.sort(key=lambda x: x["priority_score"], reverse=True)
            
            # Store in appropriate category
            if category == "technical":
                skill_gaps["missing_technical"] = missing_skills
            elif category == "soft_skills":
                skill_gaps["missing_soft_skills"] = missing_skills
            else:
                skill_gaps[f"missing_{category}"] = missing_skills
        
        # Create summary
        total_missing = sum(len(skill_gaps[key]) for key in skill_gaps if key.startswith("missing_"))
        skill_gaps["gap_summary"] = {
            "total_missing_skills": total_missing,
            "categories": {
                category: len(skill_gaps[f"missing_{category}"]) 
                for category in ["technical", "soft_skills", "tools", "languages", "frameworks", "databases", "platforms"]
                if f"missing_{category}" in skill_gaps
            }
        }
        
        return skill_gaps

    def _identify_repeated_gaps(self, skill_gaps: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """Identify skill gaps that appear repeatedly across job descriptions."""
        repeated_gaps = {
            "high_frequency_gaps": [],
            "critical_gaps": [],
            "category_gaps": {},
            "gap_analysis": {}
        }
        
        min_frequency = options.get("min_gap_frequency", 2)
        all_missing_skills = []
        
        # Collect all missing skills
        for category in ["technical", "soft_skills", "tools", "languages", "frameworks", "databases", "platforms"]:
            key = f"missing_{category}"
            if key in skill_gaps:
                for skill_info in skill_gaps[key]:
                    skill_info["category"] = category
                    all_missing_skills.append(skill_info)
        
        # Find high-frequency gaps
        high_frequency_gaps = [
            skill for skill in all_missing_skills 
            if skill["frequency"] >= min_frequency
        ]
        high_frequency_gaps.sort(key=lambda x: x["frequency"], reverse=True)
        repeated_gaps["high_frequency_gaps"] = high_frequency_gaps[:10]  # Top 10
        
        # Find critical gaps (high importance + frequency)
        critical_gaps = [
            skill for skill in all_missing_skills 
            if skill["frequency"] >= min_frequency and skill["importance"] > 0
        ]
        critical_gaps.sort(key=lambda x: (x["importance"], x["frequency"]), reverse=True)
        repeated_gaps["critical_gaps"] = critical_gaps[:10]  # Top 10
        
        # Analyze gaps by category
        category_gaps = defaultdict(list)
        for skill in all_missing_skills:
            category_gaps[skill["category"]].append(skill)
        
        for category, skills in category_gaps.items():
            # Sort by frequency
            skills.sort(key=lambda x: x["frequency"], reverse=True)
            repeated_gaps["category_gaps"][category] = skills[:5]  # Top 5 per category
        
        # Create gap analysis summary
        repeated_gaps["gap_analysis"] = {
            "total_repeated_gaps": len(high_frequency_gaps),
            "most_common_gap": high_frequency_gaps[0] if high_frequency_gaps else None,
            "critical_gaps_count": len(critical_gaps),
            "categories_with_gaps": len(category_gaps),
            "average_gap_frequency": sum(skill["frequency"] for skill in high_frequency_gaps) / len(high_frequency_gaps) if high_frequency_gaps else 0
        }
        
        return repeated_gaps

    def _analyze_role_expectations(self, job_descriptions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze common role expectations across job descriptions."""
        role_expectations = {
            "common_responsibilities": [],
            "common_qualifications": [],
            "experience_requirements": [],
            "company_culture_aspects": [],
            "industry_trends": []
        }
        
        # Collect responsibilities
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
        
        # Find common patterns
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

    def _generate_learning_recommendations(
        self,
        repeated_gaps: Dict[str, Any],
        truth_bank: Dict[str, Any],
        options: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate learning recommendations based on skill gaps."""
        recommendations = []
        
        # Get top gaps
        top_gaps = repeated_gaps.get("high_frequency_gaps", [])[:options.get("learning_recommendation_count", 8)]
        
        for gap in top_gaps:
            skill = gap["skill"]
            category = gap.get("category", "technical")
            frequency = gap["frequency"]
            
            # Generate recommendation based on skill category
            recommendation = self._create_learning_recommendation(skill, category, frequency, truth_bank)
            if recommendation:
                recommendations.append(recommendation)
        
        # Add general recommendations
        general_recommendations = [
            {
                "type": "general",
                "title": "Practice Projects",
                "description": "Build projects that combine multiple missing skills to gain practical experience",
                "priority": "high",
                "time_estimate": "2-4 weeks",
                "resources": ["GitHub", "Portfolio platforms", "Open source contributions"]
            },
            {
                "type": "general",
                "title": "Certification Preparation",
                "description": "Consider industry certifications to validate your skills",
                "priority": "medium",
                "time_estimate": "4-8 weeks",
                "resources": ["Coursera", "Udemy", "edX", "Official certification programs"]
            },
            {
                "type": "general",
                "title": "Networking and Community",
                "description": "Join professional communities and attend meetups to learn from others",
                "priority": "medium",
                "time_estimate": "Ongoing",
                "resources": ["Meetup.com", "LinkedIn groups", "Professional associations"]
            }
        ]
        
        recommendations.extend(general_recommendations)
        
        return recommendations[:options.get("learning_recommendation_count", 8)]

    def _create_learning_recommendation(
        self,
        skill: str,
        category: str,
        frequency: int,
        truth_bank: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a specific learning recommendation for a skill."""
        
        # Learning resources by category
        learning_resources = {
            "languages": {
                "python": ["Python.org tutorial", "Real Python", "Python Crash Course book", "Codecademy"],
                "javascript": ["MDN Web Docs", "JavaScript.info", "Eloquent JavaScript book", "FreeCodeCamp"],
                "java": ["Oracle Java tutorials", "Baeldung", "Java Code Geeks", "Coursera Java courses"]
            },
            "frameworks": {
                "react": ["React official docs", "React Tutorial", "Egghead.io", "React Patterns"],
                "django": ["Django official docs", "Django Girls tutorial", "Two Scoops of Django book"],
                "node.js": ["Node.js official docs", "Node.js Best Practices", "Node.js Design Patterns"]
            },
            "databases": {
                "sql": ["SQLBolt", "Mode Analytics SQL tutorial", "LeetCode SQL problems"],
                "postgresql": ["PostgreSQL official docs", "PostgreSQL Tutorial"],
                "mongodb": ["MongoDB University", "MongoDB official docs"]
            },
            "platforms": {
                "aws": ["AWS Training and Certification", "AWS Free Tier", "A Cloud Guru"],
                "docker": ["Docker official docs", "Docker Deep Dive book", "Play with Docker"],
                "kubernetes": ["Kubernetes official docs", "Kubernetes Up & Running book"]
            }
        }
        
        # Time estimates by category
        time_estimates = {
            "languages": "4-8 weeks",
            "frameworks": "2-6 weeks",
            "databases": "2-4 weeks",
            "platforms": "3-6 weeks",
            "soft_skills": "8-12 weeks",
            "technical": "4-8 weeks"
        }
        
        # Create recommendation
        resources = learning_resources.get(category, {}).get(skill, ["Online tutorials", "Documentation", "Practice projects"])
        time_estimate = time_estimates.get(category, "4-6 weeks")
        
        # Determine priority based on frequency
        priority = "high" if frequency >= 5 else "medium" if frequency >= 3 else "low"
        
        return {
            "type": "skill_specific",
            "skill": skill,
            "category": category,
            "title": f"Learn {skill.title()}",
            "description": f"Master {skill} to meet requirements in {frequency} job postings",
            "priority": priority,
            "time_estimate": time_estimate,
            "resources": resources[:3],  # Top 3 resources
            "learning_path": self._create_learning_path(skill, category),
            "prerequisites": self._identify_prerequisites(skill, category, truth_bank)
        }

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

    def _identify_prerequisites(self, skill: str, category: str, truth_bank: Dict[str, Any]) -> List[str]:
        """Identify prerequisites for learning a skill."""
        
        prerequisites = {
            "react": ["HTML", "CSS", "JavaScript"],
            "django": ["Python", "HTML", "CSS"],
            "node.js": ["JavaScript"],
            "kubernetes": ["Docker", "Linux basics"],
            "aws": ["Basic networking", "Linux fundamentals"],
            "machine_learning": ["Python", "Statistics", "Linear algebra"]
        }
        
        user_skills = set()
        for skill_category in truth_bank["skills"]:
            user_skills.update(truth_bank["skills"][skill_category])
        
        skill_prereqs = prerequisites.get(skill.lower(), [])
        
        # Filter prerequisites that user doesn't have
        missing_prereqs = [prereq for prereq in skill_prereqs if prereq.lower() not in user_skills]
        
        return missing_prereqs[:3]  # Return top 3 missing prerequisites

    def _generate_project_suggestions(
        self,
        repeated_gaps: Dict[str, Any],
        truth_bank: Dict[str, Any],
        options: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate portfolio project suggestions based on skill gaps."""
        suggestions = []
        
        # Get top gaps for project ideas
        top_gaps = repeated_gaps.get("high_frequency_gaps", [])[:options.get("project_suggestion_count", 5)]
        
        # Generate project ideas based on combinations of missing skills
        project_ideas = self._generate_project_ideas(top_gaps, truth_bank)
        
        for idea in project_ideas:
            suggestion = {
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

    def _generate_project_ideas(self, top_gaps: List[Dict[str, Any]], truth_bank: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific project ideas based on skill gaps."""
        project_ideas = []
        
        # Extract missing skills
        missing_skills = [gap["skill"] for gap in top_gaps]
        
        # Generate project ideas based on skill combinations
        if len(missing_skills) >= 2:
            # Web application project
            web_skills = [skill for skill in missing_skills if skill in ["react", "vue", "angular", "node.js", "django", "flask"]]
            if web_skills:
                project_ideas.append({
                    "title": "Full-Stack Web Application",
                    "description": f"Build a complete web application using {', '.join(web_skills[:2])}",
                    "skills_covered": web_skills[:2],
                    "difficulty": "intermediate",
                    "time_estimate": "4-6 weeks",
                    "tech_stack": web_skills[:2] + ["HTML", "CSS", "JavaScript"],
                    "learning_outcomes": ["Full-stack development", "API design", "Database integration"],
                    "portfolio_value": "high"
                })
        
        # Data project
        data_skills = [skill for skill in missing_skills if skill in ["python", "sql", "pandas", "numpy", "tableau", "powerbi"]]
        if data_skills:
            project_ideas.append({
                "title": "Data Analytics Dashboard",
                "description": f"Create an interactive dashboard using {', '.join(data_skills[:2])}",
                "skills_covered": data_skills[:2],
                "difficulty": "intermediate",
                "time_estimate": "3-4 weeks",
                "tech_stack": data_skills[:2] + ["Data visualization", "Statistics"],
                "learning_outcomes": ["Data analysis", "Visualization", "Business intelligence"],
                "portfolio_value": "high"
            })
        
        # Cloud project
        cloud_skills = [skill for skill in missing_skills if skill in ["aws", "docker", "kubernetes", "azure", "gcp"]]
        if cloud_skills:
            project_ideas.append({
                "title": "Cloud Deployment Project",
                "description": f"Deploy and manage applications using {', '.join(cloud_skills[:2])}",
                "skills_covered": cloud_skills[:2],
                "difficulty": "advanced",
                "time_estimate": "4-5 weeks",
                "tech_stack": cloud_skills[:2] + ["CI/CD", "Monitoring", "Security"],
                "learning_outcomes": ["Cloud architecture", "DevOps practices", "Infrastructure as code"],
                "portfolio_value": "very_high"
            })
        
        # Mobile project
        mobile_skills = [skill for skill in missing_skills if skill in ["react-native", "flutter", "swift", "kotlin", "ios", "android"]]
        if mobile_skills:
            project_ideas.append({
                "title": "Mobile Application",
                "description": f"Develop a mobile app using {', '.join(mobile_skills[:2])}",
                "skills_covered": mobile_skills[:2],
                "difficulty": "intermediate",
                "time_estimate": "5-7 weeks",
                "tech_stack": mobile_skills[:2] + ["Mobile UI/UX", "API integration"],
                "learning_outcomes": ["Mobile development", "Platform-specific best practices", "App deployment"],
                "portfolio_value": "high"
            })
        
        # Machine learning project
        ml_skills = [skill for skill in missing_skills if skill in ["python", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy"]]
        if ml_skills:
            project_ideas.append({
                "title": "Machine Learning Application",
                "description": f"Build an ML model using {', '.join(ml_skills[:2])}",
                "skills_covered": ml_skills[:2],
                "difficulty": "advanced",
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
                "difficulty": "intermediate",
                "time_estimate": "4-6 weeks",
                "tech_stack": missing_skills[:2] + ["Version control", "Testing", "Documentation"],
                "learning_outcomes": ["Project management", "Code organization", "Best practices"],
                "portfolio_value": "medium"
            })
        
        return project_ideas

    def _calculate_skill_coverage_score(
        self,
        truth_bank: Dict[str, Any],
        all_jd_skills: Dict[str, Any]
    ) -> float:
        """Calculate overall skill coverage score."""
        
        # Count total required skills
        total_required_skills = 0
        total_covered_skills = 0
        
        for category in ["technical", "soft_skills", "tools", "languages", "frameworks", "databases", "platforms"]:
            user_skills = set(truth_bank["skills"].get(category, []))
            required_skills = set(all_jd_skills.get(category, {}).keys())
            
            total_required_skills += len(required_skills)
            total_covered_skills += len(user_skills.intersection(required_skills))
        
        # Calculate coverage percentage
        if total_required_skills == 0:
            return 0.0
        
        coverage_score = total_covered_skills / total_required_skills
        return round(coverage_score, 2)

    def _generate_action_items(
        self,
        repeated_gaps: Dict[str, Any],
        learning_recommendations: List[Dict[str, Any]],
        project_suggestions: List[Dict[str, Any]],
        options: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate actionable recommendations."""
        action_items = []
        
        # High-priority skills to learn
        critical_gaps = repeated_gaps.get("critical_gaps", [])[:5]
        
        for gap in critical_gaps:
            action_items.append({
                "type": "skill_learning",
                "priority": "high",
                "title": f"Learn {gap['skill'].title()}",
                "description": f"This skill appears in {gap['frequency']} job postings and is marked as high importance",
                "timeline": "4-8 weeks",
                "resources": [rec["title"] for rec in learning_recommendations if rec["skill"] == gap["skill"]],
                "success_metrics": [f"Complete {gap['skill']} course", f"Build project using {gap['skill']}", f"Add {gap['skill']} to resume"]
            })
        
        # Project recommendations
        for project in project_suggestions[:3]:
            action_items.append({
                "type": "project_work",
                "priority": "medium",
                "title": f"Build {project['title']}",
                "description": project["description"],
                "timeline": project["time_estimate"],
                "resources": project["tech_stack"],
                "success_metrics": ["Complete project", "Deploy to production", "Add to portfolio", "Write documentation"]
            })
        
        # General action items
        general_actions = [
            {
                "type": "networking",
                "priority": "medium",
                "title": "Expand Professional Network",
                "description": "Connect with professionals in your target industry",
                "timeline": "ongoing",
                "resources": ["LinkedIn", "Industry meetups", "Professional associations"],
                "success_metrics": ["10 new connections", "3 informational interviews", "Join 2 professional groups"]
            },
            {
                "type": "certification",
                "priority": "low",
                "title": "Obtain Relevant Certifications",
                "description": "Get certified in high-demand skills",
                "timeline": "3-6 months",
                "resources": ["AWS/Azure/GCP certifications", "Google Cloud certifications", "Industry-specific certs"],
                "success_metrics": ["Pass certification exam", "Add certification to resume", "Update LinkedIn profile"]
            }
        ]
        
        action_items.extend(general_actions)
        
        return action_items

    def _create_analysis_summary(
        self,
        skill_gaps: Dict[str, Any],
        repeated_gaps: Dict[str, Any],
        role_expectations: Dict[str, Any],
        skill_coverage_score: float
    ) -> Dict[str, Any]:
        """Create a summary of the analysis."""
        
        total_missing = skill_gaps.get("gap_summary", {}).get("total_missing_skills", 0)
        high_freq_gaps = len(repeated_gaps.get("high_frequency_gaps", []))
        critical_gaps = len(repeated_gaps.get("critical_gaps", []))
        
        # Determine overall assessment
        if skill_coverage_score >= 0.8:
            assessment = "excellent"
            assessment_message = "Your skills align well with job requirements"
        elif skill_coverage_score >= 0.6:
            assessment = "good"
            assessment_message = "You have a good foundation but some gaps exist"
        elif skill_coverage_score >= 0.4:
            assessment = "fair"
            assessment_message = "Significant skill gaps need attention"
        else:
            assessment = "needs_improvement"
            assessment_message = "Major skill gaps require immediate attention"
        
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

    def _calculate_skill_priority(self, frequency: int, importance: int) -> float:
        """Calculate priority score for a skill based on frequency and importance."""
        # Weight frequency more heavily than importance
        frequency_weight = 0.7
        importance_weight = 0.3
        
        # Normalize frequency (assuming max frequency of 10)
        normalized_frequency = min(frequency / 10.0, 1.0)
        
        # Normalize importance (assuming max importance of 5)
        normalized_importance = min(importance / 5.0, 1.0)
        
        return (normalized_frequency * frequency_weight + normalized_importance * importance_weight)


if __name__ == "__main__":
    analyzer = SkillGapAnalyzer()
    print("SkillGapAnalyzer initialized successfully")
