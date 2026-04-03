"""Configuration data for skill gap analysis."""

from typing import Dict, List


# Skill categories with their associated skills
SKILL_CATEGORIES = {
    "programming_languages": [
        "python", "javascript", "java", "c++", "c#", "go", "rust", 
        "swift", "kotlin", "php", "ruby", "typescript", "scala", "dart"
    ],
    "web_technologies": [
        "html", "css", "react", "vue", "angular", "node.js", "express", 
        "django", "flask", "spring", "laravel", "next.js", "nuxt.js", "svelte"
    ],
    "databases": [
        "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", 
        "cassandra", "dynamodb", "sqlite", "oracle", "mariadb", "neo4j"
    ],
    "cloud_platforms": [
        "aws", "azure", "gcp", "heroku", "digitalocean", "vercel", "netlify",
        "firebase", "cloudflare", "linode", "rackspace", "ibm cloud"
    ],
    "devops_tools": [
        "docker", "kubernetes", "jenkins", "gitlab", "github", "terraform", 
        "ansible", "circleci", "travis", "bamboo", "gitlab ci", "github actions"
    ],
    "mobile_development": [
        "ios", "android", "react-native", "flutter", "swift", "kotlin", "xamarin",
        "cordova", "ionic", "unity", "android studio", "xcode"
    ],
    "data_analytics": [
        "tableau", "powerbi", "excel", "looker", "qlik", "d3.js", "plotly",
        "matplotlib", "seaborn", "ggplot", "shiny", "streamlit"
    ],
    "machine_learning": [
        "tensorflow", "pytorch", "scikit-learn", "keras", "pandas", "numpy", 
        "jupyter", "r", "sas", "spss", "h2o", "xgboost", "lightgbm"
    ],
    "soft_skills": [
        "communication", "leadership", "teamwork", "problem-solving", 
        "critical-thinking", "creativity", "adaptability", "collaboration",
        "time management", "project management", "mentoring", "presentation"
    ],
    "business_skills": [
        "project-management", "agile", "scrum", "product-management", 
        "business-analysis", "marketing", "sales", "strategy", "finance",
        "negotiation", "stakeholder management", "budgeting"
    ]
}

# Learning resources by skill and category
LEARNING_RESOURCES = {
    "languages": {
        "python": [
            "Python.org tutorial", "Real Python", "Python Crash Course book", 
            "Codecademy", "Coursera Python courses", "edX Python programs"
        ],
        "javascript": [
            "MDN Web Docs", "JavaScript.info", "Eloquent JavaScript book", 
            "FreeCodeCamp", "JavaScript30", "Coursera JS courses"
        ],
        "java": [
            "Oracle Java tutorials", "Baeldung", "Java Code Geeks", 
            "Coursera Java courses", "Spring Boot guides", "Oracle certification"
        ],
        "typescript": [
            "TypeScript Handbook", "TypeScript Deep Dive", "Coursera TypeScript",
            "Udemy TypeScript courses", "Official TypeScript documentation"
        ]
    },
    "frameworks": {
        "react": [
            "React official docs", "React Tutorial", "Egghead.io", 
            "React Patterns", "React Router docs", "Redux documentation"
        ],
        "django": [
            "Django official docs", "Django Girls tutorial", "Two Scoops of Django book",
            "Django for Beginners", "Test-Driven Development with Django"
        ],
        "node.js": [
            "Node.js official docs", "Node.js Best Practices", "Node.js Design Patterns",
            "Node.js in Action", "Mastering Node.js"
        ],
        "next.js": [
            "Next.js documentation", "Next.js tutorial", "Vercel guides",
            "Building Applications with Next.js", "Next.js by Example"
        ]
    },
    "databases": {
        "sql": [
            "SQLBolt", "Mode Analytics SQL tutorial", "LeetCode SQL problems",
            "SQL for Data Analysis", "PostgreSQL Tutorial", "MySQL documentation"
        ],
        "postgresql": [
            "PostgreSQL official docs", "PostgreSQL Tutorial", "The PostgreSQL Guide",
            "PostgreSQL High Performance Cookbook", "PostgreSQL Administration"
        ],
        "mongodb": [
            "MongoDB University", "MongoDB official docs", "MongoDB Basics",
            "MongoDB Applied Patterns", "Building with MongoDB"
        ],
        "redis": [
            "Redis documentation", "Redis University", "Redis in Action",
            "Redis Essentials", "Redis Cookbook"
        ]
    },
    "platforms": {
        "aws": [
            "AWS Training and Certification", "AWS Free Tier", "A Cloud Guru",
            "AWS Solutions Architect certification", "AWS Developer Tools"
        ],
        "docker": [
            "Docker official docs", "Docker Deep Dive book", "Play with Docker",
            "Docker for Developers", "Docker in Action"
        ],
        "kubernetes": [
            "Kubernetes official docs", "Kubernetes Up & Running book",
            "Kubernetes in Action", "Certified Kubernetes Administrator"
        ],
        "azure": [
            "Microsoft Learn", "Azure documentation", "Azure certification paths",
            "Azure Architecture Center", "Azure DevOps"
        ]
    }
}

# Time estimates for learning different skill categories
TIME_ESTIMATES = {
    "languages": "4-8 weeks",
    "frameworks": "2-6 weeks",
    "databases": "2-4 weeks",
    "platforms": "3-6 weeks",
    "soft_skills": "8-12 weeks",
    "technical": "4-8 weeks",
    "tools": "1-3 weeks"
}

# Prerequisites for learning specific skills
SKILL_PREREQUISITES = {
    "react": ["HTML", "CSS", "JavaScript"],
    "django": ["Python", "HTML", "CSS"],
    "node.js": ["JavaScript"],
    "kubernetes": ["Docker", "Linux basics"],
    "aws": ["Basic networking", "Linux fundamentals"],
    "machine_learning": ["Python", "Statistics", "Linear algebra"],
    "typescript": ["JavaScript"],
    "next.js": ["React", "Node.js"],
    "spring": ["Java", "Maven/Gradle"],
    "flask": ["Python"],
    "angular": ["TypeScript", "JavaScript", "HTML", "CSS"],
    "vue": ["JavaScript", "HTML", "CSS"],
    "postgresql": ["SQL basics"],
    "mongodb": ["NoSQL concepts", "JSON"],
    "redis": ["Basic data structures"],
    "terraform": ["Cloud basics", "CLI experience"],
    "jenkins": ["CI/CD concepts", "Linux"],
    "gitlab": ["Git", "CI/CD concepts"],
    "tableau": ["Data visualization basics", "Excel"],
    "powerbi": ["Data analysis basics", "Excel"],
    "tensorflow": ["Python", "Machine learning basics"],
    "pytorch": ["Python", "Machine learning basics"],
    "pandas": ["Python", "Data analysis basics"],
    "numpy": ["Python", "Mathematical concepts"]
}

# Default analysis options
DEFAULT_ANALYSIS_OPTIONS = {
    "include_soft_skills": True,
    "include_technical_skills": True,
    "min_gap_frequency": 2,
    "project_suggestion_count": 5,
    "learning_recommendation_count": 8,
    "priority_threshold": 0.3
}

# Priority calculation weights
PRIORITY_WEIGHTS = {
    "frequency": 0.7,
    "importance": 0.3
}

# Normalization constants
NORMALIZATION_CONSTANTS = {
    "max_frequency": 10,
    "max_importance": 5,
    "max_priority": 1.0
}

# Assessment thresholds
ASSESSMENT_THRESHOLDS = {
    "excellent": 0.8,
    "good": 0.6,
    "fair": 0.4,
    "needs_improvement": 0.0
}

# Assessment messages
ASSESSMENT_MESSAGES = {
    "excellent": "Your skills align well with job requirements",
    "good": "You have a good foundation but some gaps exist",
    "fair": "Significant skill gaps need attention",
    "needs_improvement": "Major skill gaps require immediate attention"
}
