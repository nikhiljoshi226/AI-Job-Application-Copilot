# Skill Gap Analysis Module

This module provides comprehensive skill gap analysis functionality with a clean, modular architecture.

## Architecture

### Core Components

#### 1. Types and Configuration
- **`types.py`** - Type definitions and enums for type safety
- **`config.py`** - Configuration data and constants

#### 2. Service Layer
- **`skill_categorizer.py`** - Skill categorization logic
- **`truth_bank_extractor.py`** - Resume data extraction
- **`job_skill_extractor.py`** - Job description skill extraction
- **`gap_analyzer.py`** - Core gap analysis logic
- **`repeated_gap_analyzer.py`** - Repeated gap identification
- **`recommendation_generator.py`** - Learning and project recommendations
- **`analysis_orchestrator.py`** - Main workflow coordinator

#### 3. Entry Point
- **`__init__.py`** - Main SkillGapAnalyzer interface

## Naming Conventions

### Classes
- Use PascalCase with descriptive names
- Service classes end with "Service" (e.g., `SkillGapAnalysisService`)
- Analyzer classes end with "Analyzer" (e.g., `GapAnalyzer`)
- Extractor classes end with "Extractor" (e.g., `TruthBankExtractor`)
- Generator classes end with "Generator" (e.g., `RecommendationGenerator`)

### Methods
- Use snake_case with descriptive verbs
- Private methods start with underscore
- Methods should be self-documenting: `extract_from_resume()`, `analyze_gaps()`

### Variables
- Use snake_case
- Use descriptive names: `job_descriptions` instead of `jobs`
- Booleans should start with `is_`, `has_`, `can_`: `is_high_priority`, `has_prerequisites`

### Constants
- Use UPPER_SNAKE_CASE
- Group related constants: `SKILL_CATEGORIES`, `DEFAULT_ANALYSIS_OPTIONS`

### Type Hints
- Use specific types instead of `Dict[str, Any]` when possible
- Use TypedDict for structured data
- Use Enums for fixed sets of values

## Key Improvements from Refactor

### 1. Separation of Concerns
- **Before**: Single monolithic class with 970+ lines
- **After**: 8 focused classes with single responsibilities

### 2. Type Safety
- **Before**: Extensive use of `Dict[str, Any]`
- **After**: Comprehensive TypedDict and Enum usage

### 3. Configuration Management
- **Before**: Hard-coded data scattered throughout code
- **After**: Centralized configuration in `config.py`

### 4. Code Duplication
- **Before**: Repeated patterns for skill processing
- **After**: Reusable components and common base classes

### 5. Maintainability
- **Before**: Difficult to test and modify individual components
- **After**: Each component can be tested and modified independently

## Usage

```python
from app.services.skill_gap import SkillGapAnalyzer

# Initialize analyzer
analyzer = SkillGapAnalyzer()

# Perform analysis
result = analyzer.analyze_skill_gaps(
    resume_data=resume,
    job_descriptions=jobs,
    analysis_options=options
)
```

## Testing

Each component can be tested independently:

```python
from app.services.skill_gap.skill_categorizer import SkillCategorizer

categorizer = SkillCategorizer()
category = categorizer.categorize_skill("python")
assert category == SkillCategory.LANGUAGES
```
